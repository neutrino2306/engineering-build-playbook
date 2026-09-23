# 03 异步任务队列（Task Queue）设计文档

## 一、题目理解

### 可能的原题表述

> Build a background job system. Clients submit jobs through an API and can check their status. Jobs are processed asynchronously by workers. Failed jobs should be retried, and jobs that keep failing should not retry forever.

中文：实现一个后台任务系统。客户端通过 API 提交任务并查询状态，任务由 worker 异步处理。失败的任务要重试，一直失败的任务不能无限重试。

### 核心问题是什么

**四个难点，按重要性排**：

1. **worker 崩溃怎么办**：抢到任务后崩溃，任务永远卡在 running
2. **多个 worker 不能抢到同一个任务**
3. **重试策略**：立刻重试会压垮下游，要退避
4. **一直失败的任务**：要有死信（dead letter）状态，不能无限循环

**面试官最想听的一个认知**：分布式系统里"恰好执行一次"（exactly-once）基本做不到，实际做法是"至少执行一次 + 任务处理本身幂等"。

### 为什么 DO 会出这道题

DO 的产品里大量异步操作：创建 Droplet、打快照、调整磁盘大小，这些都是几十秒到几分钟的后台任务。用户点了按钮之后看到的是"进行中"状态，背后就是任务队列。

---

## 二、3 小时 Scope

### Must-have

1. 提交任务、查询任务状态
2. worker 异步处理
3. 失败重试 + 指数退避
4. 最大重试次数 + 死信状态
5. **租约机制**：worker 崩溃后任务能被重新处理
6. 部署

### Nice-to-have

1. 死信任务手动重试
2. 按状态筛选任务列表
3. 后台 worker 线程（生产）+ 手动触发接口（测试和 demo）
4. **fencing token**：防止租约过期的 worker 覆盖别人的结果

**本项目全部实现了。**fencing token 是进阶设计，code review 时能讲出来会很加分。

### Out-of-scope

| 不做的功能 | 为什么 | code review 时怎么说 |
|---|---|---|
| 优先级队列 | 增加复杂度，核心逻辑不变 | "I'd add a priority column and order by it before next_run_at." |
| 定时任务（cron） | 不同的问题 | "Scheduled jobs would insert tasks with a future next_run_at." |
| 任务依赖（DAG） | 复杂度爆炸 | "That's a workflow engine, a different system." |
| 独立 worker 进程 | 部署复杂 | "In production workers would be a separate component so they scale independently." |
| 任务结果过期清理 | 非核心 | "I'd delete succeeded tasks after a retention period." |

---

## 三、API 设计

| 方法 | 路径 | 作用 | 状态码 |
|---|---|---|---|
| GET | `/health` | 健康检查 | 200 |
| POST | `/tasks` | 提交任务 | 201 / 422 未知类型 |
| GET | `/tasks/{id}` | 查询任务 | 200 / 404 |
| GET | `/tasks?status=dead` | 按状态列出 | 200 |
| POST | `/tasks/{id}/retry` | 手动重试死信任务 | 200 / 404 / 409 |
| POST | `/worker/run-once` | 手动触发一轮处理 | 200 |

### 设计要点

**提交任务立刻返回，不等执行完**：这是异步的本质。客户端拿到任务 ID 后轮询状态。

**手动重试只允许 dead 状态**：对 queued 或 running 的任务调用重试返回 409，因为它们已经在处理流程里了。

**`/worker/run-once` 为什么存在**：后台线程的行为是不确定的（什么时候跑、跑几次），测试和 demo 需要确定性。这个接口让你能精确控制"现在处理一轮"。生产环境靠后台循环，这个接口可以关掉。

---

## 四、数据模型

```sql
CREATE TABLE tasks (
    id           TEXT    PRIMARY KEY,
    type         TEXT    NOT NULL,
    payload      TEXT    NOT NULL,     -- JSON
    status       TEXT    NOT NULL
                 CHECK (status IN ('queued', 'running', 'succeeded', 'dead')),
    attempts     INTEGER NOT NULL DEFAULT 0,
    max_attempts INTEGER NOT NULL,
    next_run_at  INTEGER NOT NULL,     -- 退避调度
    locked_until INTEGER,              -- 租约过期时间
    lease_token  TEXT,                 -- fencing token
    last_error   TEXT,
    result       TEXT,
    created_at   INTEGER NOT NULL,
    updated_at   INTEGER NOT NULL
);
CREATE INDEX idx_tasks_ready ON tasks (status, next_run_at);
```

### 每个字段的作用

| 字段 | 作用 |
|---|---|
| `status` | 状态机的当前状态 |
| `attempts` | 已尝试次数，**在抢到任务时就 +1**，不是失败时 |
| `next_run_at` | 最早可执行时间，退避就是把它往后推 |
| `locked_until` | 租约到期时间，超过就认为 worker 挂了 |
| `lease_token` | 每次抢任务生成一个新的随机值，完成时必须出示 |
| `last_error` | 最后一次失败原因，排查用 |

**为什么 attempts 在抢任务时加而不是失败时加**：如果 worker 抢到任务后直接崩溃，永远不会走到"失败"那一步。如果在失败时才加，这种任务的 attempts 永远不增长，会无限重试。**在抢任务时加，崩溃也算一次尝试。**

**索引 `(status, next_run_at)`**：worker 的核心查询是"状态为 queued 且已到期的最早任务"，这个索引让它不用全表扫描。

---

## 五、状态机

```
                    ┌─────────── 手动重试 ───────────┐
                    │                                │
                    ▼                                │
   提交 ──▶ queued ──抢任务──▶ running ──成功──▶ succeeded
               ▲                  │
               │                  ├──失败且有剩余次数──┐
               │                  │                   │
               └──────退避后──────┘◀──────────────────┘
               │                  │
               │                  └──失败且无剩余次数──▶ dead
               │                  │
               └───租约过期────────┘（worker 崩溃）
```

**每一次状态转换都是条件更新**，比如抢任务是 `WHERE id=? AND status='queued'`，保证非法转换不会发生。

---

## 六、核心难点与实现

### 难点一：多个 worker 不能抢到同一个任务

```python
with transaction(immediate=True) as conn:
    candidate = SELECT id FROM tasks
                WHERE status='queued' AND next_run_at <= now
                ORDER BY next_run_at LIMIT 1
    UPDATE tasks SET status='running', attempts=attempts+1, ...
    WHERE id = candidate.id AND status = 'queued'   -- 关键：再检查一次
```

**两层保护**：
1. `BEGIN IMMEDIATE` 让抢任务的事务串行
2. UPDATE 里再次检查 `status='queued'`，即使两个 worker 选中了同一个候选，也只有一个 UPDATE 能匹配

**生产环境（PostgreSQL）的标准做法**：`SELECT ... FOR UPDATE SKIP LOCKED`，多个 worker 可以并行抢不同的任务，不会互相阻塞。**面试时提一句这个会很加分。**

### 难点二：worker 崩溃（租约机制）

**问题**：worker 抢到任务，状态改成 running，然后进程被杀了。任务永远卡在 running。

**解法**：抢任务时设置租约过期时间 `locked_until = now + 30`。每轮处理开始时先回收过期租约：

```sql
UPDATE tasks SET status = 'queued', ...
WHERE status = 'running' AND locked_until < now
```

**这就是 AWS SQS 的 visibility timeout 机制。**

**一个边界情况**：某个任务每次都让 worker 崩溃（比如触发了内存溢出）。如果回收时不检查次数，它会无限循环。所以回收逻辑分两种：还有剩余次数的放回队列，没有剩余次数的直接进死信。测试 `test_task_that_repeatedly_crashes_worker_eventually_dies` 覆盖了这个。

### 难点三：fencing token（进阶，很加分）

**问题场景**：

```
t=0    Worker A 抢到任务，租约到 t=30
t=0    Worker A 开始执行，但它卡住了（网络慢、GC 停顿）
t=31   租约过期，任务被回收
t=31   Worker B 抢到任务，开始执行
t=35   Worker B 完成，写入结果 "B"
t=40   Worker A 终于醒了，也完成了，写入结果 "A"  ← 覆盖了 B 的结果！
```

A 已经没有租约了，它不应该能写结果。但如果完成逻辑只检查 `status='running'`，A 的写入会成功（因为 B 完成之前状态也是 running，或者时机不巧）。

**解法**：每次抢任务时生成一个随机的 `lease_token`，完成时必须出示：

```sql
UPDATE tasks SET status='succeeded', result=?
WHERE id = ? AND status = 'running' AND lease_token = ?
```

A 的 token 在 B 抢任务时已经被替换了，所以 A 的 UPDATE 匹配不到任何行，`rowcount = 0`，结果被丢弃。

测试 `test_fencing_token_rejects_stale_worker` 精确模拟了这个场景。

**这个概念出自 Martin Kleppmann 的分布式锁分析**（批评 Redlock 的那篇文章）。面试时能讲出 fencing token，说明你对分布式系统的理解超过了一般应届生。

### 难点四：退避与抖动

```python
def backoff_seconds(attempts):
    base = min(2 * (2 ** (attempts - 1)), 300)   # 2, 4, 8, 16... 上限 300
    return max(1, int(base * random.uniform(0.5, 1.5)))  # 抖动
```

**为什么要抖动**：下游服务故障时，大量任务同时失败。如果退避时间完全相同，它们会在同一时刻一起重试，再次把刚恢复的下游压垮。这叫**惊群效应**（thundering herd）。抖动把重试时间打散。

### 难点五：handler 在事务外执行

```python
task = claim_next(now)        # 事务 1：抢任务
result = handler(payload)     # 不在任何事务里！
complete(task_id, token, ...) # 事务 2：写结果
```

**为什么**：`BEGIN IMMEDIATE` 持有的是写锁。如果在事务里执行任务，一个跑 30 秒的任务会让所有其他写操作（包括提交新任务）等 30 秒。

**代价**：抢任务和写结果之间有空隙，这正是需要租约和 fencing token 的原因。**这些设计是环环相扣的。**

### 难点六：handler 的 bug 也只是一次失败

```python
except TaskError as e:        # 预期内的失败
    record_failure(...)
except Exception as e:        # handler 代码本身的 bug
    record_failure(...)       # 同样处理，不能让 worker 崩溃
```

测试 `test_handler_exception_counts_as_failed_attempt` 覆盖了这个。

---

## 七、一个真实踩到的坑：测试时钟和真实时钟不一致

**现象**：第一版测试里，所有涉及重试的测试都失败了，成功的那条却通过了。

**原因**：
- 通过 API 提交的任务，`next_run_at` 是服务器真实时间（2026 年，约 17.9 亿）
- 测试里用了一个固定时间戳 `T0 = 1_700_000_000`（2023 年）
- 在 T0 时刻看来，任务的执行时间还没到，worker 什么都没处理
- 成功那条测试没传 `now` 参数，用的也是真实时间，所以碰巧通过了

**修复**：`T0 = int(time.time()) + 60`

**面试时的价值**：这说明你理解"时间是一个需要显式注入的依赖"。所有函数都接受可选的 `now` 参数，就是为了让时间相关的逻辑可以被精确测试。

> "Every time-dependent function takes an optional `now` parameter. That made retry and lease-expiry logic testable without sleeping. I did hit a bug where my test clock was in 2023 while the API used real time, so nothing looked due. It's a good reminder that time is a dependency you need to control explicitly."

---

## 八、关键 Trade-off

### Trade-off 1：数据库当队列 vs 专用消息队列

| | SQLite/PostgreSQL（本项目） | Redis / RabbitMQ / SQS |
|---|---|---|
| 部署 | 零额外组件 | 多一个服务 |
| 持久性 | 强 | 看配置 |
| 事务一致性 | 任务状态和业务数据能在同一个事务里 | 做不到 |
| 吞吐量 | 中等 | 高 |

**选择理由**：三小时内不引入新组件。而且"用数据库当队列"在生产环境里也是合理选择（比如 Rails 的 GoodJob、Python 的 Procrastinate），**直到吞吐量真的成为瓶颈**。

**关键优势**：如果业务操作和"提交后续任务"需要原子性（比如"创建订单并提交发邮件任务"），数据库队列能在一个事务里完成，消息队列做不到。这叫 **transactional outbox pattern**。

### Trade-off 2：进程内 worker vs 独立 worker 进程

**本项目**：worker 是 API 进程里的一个后台线程。

**问题**：
1. 任务执行会和 API 请求抢 CPU
2. 扩容 API 时 worker 也跟着扩，扩 worker 时 API 也跟着扩
3. API 部署重启时正在执行的任务会被打断

**生产演进**：worker 做成独立组件。App Platform 支持 Worker 类型的组件，和 web service 分开部署、分开扩容。

### Trade-off 3：轮询 vs 通知

**本项目**：worker 每秒查一次数据库。

**问题**：空闲时也在不停查询；任务延迟最多一个轮询间隔。

**生产演进**：PostgreSQL 的 `LISTEN/NOTIFY`，提交任务时发通知，worker 被唤醒。或者用消息队列的推送模式。

### Trade-off 4：至少一次 vs 恰好一次

**本项目提供至少一次**。worker 执行完但在写结果前崩溃，任务会被再执行一次。

**为什么不做恰好一次**：分布式系统里基本不可能保证。"执行"和"记录已执行"是两个动作，中间任何时刻都可能崩溃。

**正确做法**：让任务处理本身幂等。比如"给用户发邮件"任务，先查"这封邮件发过没有"，发过就跳过。

---

## 九、3 小时时间分配

| 时间 | 做什么 | 检查点 |
|---|---|---|
| 0:00-0:15 | 读题、定 scope、建仓库 | |
| 0:15-0:30 | 骨架 + `/health` | |
| 0:30-0:45 | **第一次部署** | 线上可访问 |
| 0:45-1:10 | 提交、查询、handler 注册表 | |
| 1:10-1:45 | 抢任务 + run-once + 成功路径 | 能处理任务 |
| 1:45-2:10 | 失败重试 + 退避 + 死信 | 重试流程通 |
| 2:10-2:30 | 租约回收 + 后台线程 | |
| 2:30-2:40 | 冻结功能，确认线上 | |
| 2:40-3:00 | README + 讲解准备 | |

**如果时间紧**：砍掉 fencing token（口头讲就行）、砍掉手动重试。**租约回收不能砍**，那是核心考点。

---

## 十、测试策略

13 个测试，按价值排序：

1. **fencing token 拒绝过期 worker**：最能体现深度
2. **租约过期被回收**：核心考点
3. **反复崩溃的任务最终进死信**：边界情况
4. 失败后按退避延迟重试，而不是立刻重试
5. 达到上限进入死信
6. handler 异常也算一次失败
7. 退避时间增长且有上限

---

## 十一、Code Review 高频问题

### Q1：What happens if a worker crashes mid-task?

> "Every claim sets a lease, `locked_until = now + 30`. At the start of each processing round, expired leases are reclaimed and those tasks go back to queued. The attempt was already counted when it was claimed, so a task that keeps crashing its worker still ends up dead instead of looping forever."

### Q2：Can a task run twice?

> "Yes, this is at-least-once. If a worker finishes the work but crashes before recording the result, the lease expires and another worker runs it again. Exactly-once isn't really achievable in a distributed system, because doing the work and recording it are two separate steps. The practical answer is at-least-once plus idempotent handlers."

### Q3：How do you stop two workers from taking the same task?

> "The claim is a conditional update that re-checks `status = 'queued'`, so only one UPDATE can match. On PostgreSQL I'd use `SELECT ... FOR UPDATE SKIP LOCKED`, which lets multiple workers claim different tasks in parallel without blocking each other."

### Q4：What's the lease_token for?

> "It's a fencing token. If worker A stalls past its lease, worker B takes over. When A wakes up and tries to write its result, it has to present its token, but B's claim already replaced it, so A's update matches zero rows and is discarded. Without it, a stale worker could overwrite the result of the worker that actually owns the task."

**这个问题如果被问到，你能答上来就是大加分。**

### Q5：Why not run the handler inside the transaction?

> "The transaction holds SQLite's write lock. A 30-second task would block every other write for 30 seconds, including new submissions. So the claim and the result write are two short transactions, and the gap between them is exactly why the lease and fencing token exist."

### Q6：Why use the database as a queue?

> "It avoids adding another component within three hours, and it has a real advantage: task state can be updated in the same transaction as business data. That's the transactional outbox pattern. I'd move to a dedicated broker only when throughput actually becomes the bottleneck."

### Q7：How would you scale this?

> "First, move workers out of the API process into their own component, so they scale independently and API deploys don't interrupt tasks. Then move to PostgreSQL with SKIP LOCKED for parallel claims, and replace polling with LISTEN/NOTIFY to cut latency and idle load."

---

## 十二、已知限制

1. SQLite 数据不持久，重新部署后任务丢失
2. worker 在 API 进程里，不能独立扩容
3. 轮询带来最多一秒延迟和空闲时的无效查询
4. 没有优先级
5. 已完成的任务永久保存
6. handler 必须在代码里注册，不能动态添加

---

## 十三、和你自己经历的连接

**这道题的每一个机制你都在 nOps 真实做过**：

| 这道题 | 你在 nOps 的并发标注服务 |
|---|---|
| 重试 + 指数退避 + 抖动 | 按错误类型区分退避（限流用 4 的幂次，其他用 2 的幂次），加随机抖动 |
| 熔断 | **滚动窗口失败率熔断**（最近 20 次失败率超过 50% 中止） |
| 断点续跑 | 每 100 条写一次 checkpoint，中断后只补跑缺失的 |
| 结果顺序 | 并发结果按原始索引写回，保证可复现 |
| handler 异常处理 | 截断、限流、权限错误分别处理 |

**面试时可以这样开场**：
> "I built something close to this in my internship: a concurrent labeling service that sent 6,000 events through AWS Bedrock across 8 workers. It had exponential backoff with jitter, checkpointed resumption, and order-preserving writes. One design choice I'm happy with is the circuit breaker: I used a rolling failure rate over the last 20 calls rather than N consecutive failures, because with concurrent workers, successes and failures interleave, so you might never see N failures in a row even during a full outage."

**这个开场会让面试官立刻知道你真做过，不是背的。**

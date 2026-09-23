# 01 资源配额服务（Quota Service）设计文档

## 一、题目理解

### 可能的原题表述

> Build a service that enforces resource quotas for cloud customers. Each customer (tenant) has limits on how many of each resource type they can create (e.g. droplets, volumes, load balancers). The service should allow setting limits, checking usage, and reserving/releasing resources. Make sure the limits cannot be exceeded.

中文：为云服务客户实现一个资源配额服务。每个租户对每种资源（虚拟机、存储卷、负载均衡器等）有数量上限。需要支持设置上限、查询用量、预留和释放资源，并且保证上限不会被突破。

### 核心问题是什么

**表面上是 CRUD，实际上考的是并发正确性。**

"保证上限不被突破"这句话是整道题的考点。如果你写成"先查用量，再判断，再更新"，单个请求测试完全正常，但两个请求同时到达时就会超限。**面试官会专门问这个。**

### 为什么 DO 会出这道题

这就是 DO 的真实业务。你在 DO 控制台创建 Droplet 时，背后一定有一个配额检查。有资料提到 DO 过去的题目里出现过"对云资源配额强制执行使用限制"。**这道题出现的概率很高。**

---

## 二、3 小时 Scope

### Must-have（必须做完）

1. 设置/更新某租户某资源的上限
2. 查询某租户所有资源的用量和余量
3. 预留资源（成功返回 201，超限返回 409）
4. 释放资源（归还配额）
5. **并发安全**：多个请求同时预留，不能超限
6. 部署到 App Platform

### Nice-to-have（有时间就做）

1. 幂等键：客户端重试不会重复扣配额
2. 释放操作幂等：释放两次不会退还两次
3. 降低上限到低于当前用量的处理
4. 并发测试（这个其实很值得做，code review 时是杀手锏）

**本项目的实现已经把 nice-to-have 全做了**，因为它们代码量不大，但 code review 价值极高。

### Out-of-scope（明确不做）

| 不做的功能 | 为什么不做 | code review 时怎么说 |
|---|---|---|
| 认证鉴权 | 与核心问题无关，会吃掉 30 分钟 | "In production I'd add auth at the gateway and scope tenant_id to the authenticated principal." |
| 预留过期（TTL） | 需要后台任务，复杂度翻倍 | "Reservations that are never released would leak quota. I'd add an expires_at and a sweeper job." |
| 多区域配额 | 超出三小时范围 | "Regional quotas would add region to the primary key." |
| 配额变更审计日志 | 非核心 | "I'd log every limit change for compliance." |
| 前端页面 | FastAPI 的 `/docs` 已经足够 demo | 不用说，面试官不会问 |

---

## 三、API 设计

| 方法 | 路径 | 作用 | 成功 | 失败 |
|---|---|---|---|---|
| GET | `/health` | 健康检查 | 200 | |
| PUT | `/tenants/{tenant_id}/quotas/{resource}` | 设置上限 | 200 | 422 参数非法 |
| GET | `/tenants/{tenant_id}/quotas` | 查询用量 | 200 | |
| POST | `/tenants/{tenant_id}/reservations` | 预留 | 201 新建 / 200 重放 | 404 未配置 / 409 超限 / 422 幂等冲突 |
| DELETE | `/reservations/{reservation_id}` | 释放 | 200 | 404 |

### 设计要点

**为什么设置上限用 PUT 不用 POST**：PUT 是幂等的（同样的请求发多少次结果一样），语义上就是"把这个资源的上限设为 X"。

**为什么预留返回 201 但重放返回 200**：201 表示"创建了新资源"，重放没有创建任何东西，只是返回已有结果，所以用 200。这个细节面试官可能会注意到。

**为什么超限用 409 不用 400 或 429**：
- 400 表示请求本身格式有问题，但这个请求格式完全正确
- 429 是**限流**（单位时间内请求太频繁），和**配额**（总量上限）是两个概念
- 409 Conflict 表示"请求合法但和资源当前状态冲突"，最准确

**超限时返回详细信息**：`{limit, used, requested}`，让客户端知道还剩多少，可以调整请求量。

---

## 四、数据模型

```sql
CREATE TABLE quotas (
    tenant_id   TEXT    NOT NULL,
    resource    TEXT    NOT NULL,
    limit_value INTEGER NOT NULL CHECK (limit_value >= 0),
    used        INTEGER NOT NULL DEFAULT 0 CHECK (used >= 0),
    updated_at  TEXT    NOT NULL,
    PRIMARY KEY (tenant_id, resource)
);

CREATE TABLE reservations (
    id          TEXT    PRIMARY KEY,   -- 幂等键或自动生成的 UUID
    tenant_id   TEXT    NOT NULL,
    resource    TEXT    NOT NULL,
    amount      INTEGER NOT NULL CHECK (amount > 0),
    status      TEXT    NOT NULL CHECK (status IN ('active', 'released')),
    created_at  TEXT    NOT NULL,
    released_at TEXT
);
```

### 设计要点

**为什么 limit 和 used 放在同一张表同一行**：这是整个设计的关键。只有放在同一行，才能用**一条** UPDATE 语句同时读取 used、读取 limit、判断、写入。如果分成两张表，就需要 JOIN 或者两步操作，原子性就难保证了。

**为什么还要单独一张 reservations 表**：
1. 释放时要知道当初预留了多少
2. 幂等键需要一个地方存
3. 审计：能查到谁在什么时候预留了什么

**`used` 是冗余字段**：理论上可以每次 `SUM(amount) FROM reservations WHERE status='active'` 算出来。但那样每次预留都要全表聚合，而且聚合和更新之间又有竞态。**冗余存储 used 是用空间换原子性和性能。**

**CHECK 约束是最后一道防线**：`CHECK (used >= 0)` 保证即使代码有 bug，数据库也不会接受负数用量。

---

## 五、架构与请求流

```
Client
  │
  ▼
main.py  ── 解析参数、Pydantic 校验、异常映射为状态码
  │
  ▼
service.py ── 业务规则：幂等检查、原子预留、释放
  │
  ▼
db.py ── BEGIN IMMEDIATE 事务 → SQLite
```

### 预留请求的完整流程

```
1. 进入 BEGIN IMMEDIATE 事务（拿写锁）
2. 查 reservations 表：这个 id 是否已存在？
   ├─ 存在且内容一致 → 返回原结果（replayed=True），不扣配额
   ├─ 存在但内容不同 → 抛 IdempotencyConflict（422）
   └─ 不存在 → 继续
3. 执行条件 UPDATE：
   UPDATE quotas SET used = used + amount
   WHERE tenant_id=? AND resource=? AND used + amount <= limit_value
4. 看 rowcount：
   ├─ 1 → 成功，插入 reservation 记录
   └─ 0 → 再查一次 quotas 表区分原因
          ├─ 记录不存在 → QuotaNotFound（404）
          └─ 记录存在 → QuotaExceeded（409）
5. COMMIT
```

---

## 六、核心难点与实现（这一节最重要）

### 难点一：并发下不能超限

**错误写法**（很多人第一反应会这么写）：

```python
quota = SELECT used, limit_value FROM quotas WHERE ...
if quota.used + amount > quota.limit_value:
    raise QuotaExceeded
UPDATE quotas SET used = used + amount WHERE ...
```

**问题**：两个请求同时执行第一行，都读到 `used=9, limit=10`，都通过判断，都执行 UPDATE，最终 `used=11`。

**正确写法**：

```sql
UPDATE quotas SET used = used + ?
WHERE tenant_id = ? AND resource = ? AND used + ? <= limit_value
```

**为什么这样就安全了**：数据库执行单条 UPDATE 时，找到匹配行、评估 WHERE 条件、修改数据这三步是原子的。第二个请求执行时看到的已经是第一个请求修改后的 `used=10`，条件 `10 + 1 <= 10` 不成立，rowcount 为 0。

**测试证明**：`test_concurrent_reservations_never_exceed_limit` 用 20 个线程发起 50 次请求抢 10 个配额，结果恰好 10 次成功，`used == 10`。

### 难点二：rowcount 为 0 时区分原因

条件 UPDATE 失败只告诉你"没更新"，不告诉你为什么。可能是配额不存在，也可能是超限了。所以失败后要再查一次。

**这次查询在同一个事务里**，所以看到的数据是一致的，不会出现"刚才没有、现在有了"的情况。

### 难点三：幂等

客户端预留请求超时，它不知道服务端有没有处理，于是重试。没有幂等保护的话会扣两次配额。

**实现**：客户端在请求头带 `Idempotency-Key`，服务端把它直接作为 reservation 的主键。重试时发现主键已存在，就返回原记录。

**为什么幂等检查需要 BEGIN IMMEDIATE**："查是否存在"和"插入"之间如果被别的事务插进来，两个相同 key 的请求可能都查到"不存在"，然后都去插入。虽然主键约束会让第二个插入失败，但那时配额已经被扣了两次（UPDATE 在 INSERT 之前）。`BEGIN IMMEDIATE` 保证整个流程串行。

### 难点四：释放幂等

释放两次不能退还两次配额。实现方式是看 reservation 的 status，已经是 `released` 就直接返回。

### 难点五：降低上限

管理员把上限从 5 降到 2，但当前已用 4。怎么办？

**本项目的选择**：允许降低，不强制回收已有资源，但新预留会被阻止，直到用量降到 2 以下。`available` 显示为 0 而不是 -2。

**为什么**：强制回收（比如删掉用户的虚拟机）是产品决策，不应该由配额服务自作主张。配额服务只负责"不让超"，不负责"让它不超"。

---

## 七、关键 Trade-off

### Trade-off 1：条件更新 vs 应用层加锁

| | 条件更新（本项目） | Python `threading.Lock` |
|---|---|---|
| 单进程 | 安全 | 安全 |
| 多进程/多实例 | **安全**（原子性由数据库保证） | **不安全**（锁只在进程内有效） |
| 代码复杂度 | 低 | 低 |

**选择理由**：原子性应该由数据库提供，这样扩容到多实例时逻辑不用改。

### Trade-off 2：SQLite vs PostgreSQL

**选 SQLite 的理由**：零配置，三小时内不用操心数据库部署。

**代价**：
1. App Platform 文件系统是临时的，重新部署数据就丢了
2. `BEGIN IMMEDIATE` 是库级写锁，并发写吞吐有限
3. 多实例时每个实例有自己的数据库文件，状态不共享

**生产演进**：换 DO Managed PostgreSQL。条件更新语句不用改，PostgreSQL 的行锁比 SQLite 的库锁粒度更细，并发性能好得多。

### Trade-off 3：冗余存储 used vs 实时聚合

**选冗余的理由**：预留时只需要操作一行，O(1)，而且原子性容易保证。

**代价**：used 和 reservations 表可能不一致（比如有 bug 或者手工改数据）。

**生产演进**：加一个定期对账任务，`SUM(amount) FROM reservations WHERE status='active'` 和 `used` 对比，不一致就告警。

### Trade-off 4：预留是否过期

**本项目不过期。**如果客户端预留了但永远不释放（比如它崩溃了），配额就会泄漏。

**生产演进**：加 `expires_at`，后台定期扫描过期的 active 预留并自动释放。或者采用"预留 + 确认"两阶段模式：预留有短 TTL，客户端真正创建资源后调用确认接口转为永久占用。

---

## 八、3 小时时间分配（这道题专用）

| 时间 | 做什么 | 检查点 |
|---|---|---|
| 0:00-0:15 | 读题、选题、定 scope、建 GitHub 仓库 | 仓库已创建 |
| 0:15-0:30 | 生成骨架（db/models/service/main），只实现 `/health` | 本地能跑 |
| 0:30-0:45 | **第一次部署** | 线上 `/health` 能访问 |
| 0:45-1:15 | 设置上限、查询用量 | 两个接口线上可用 |
| 1:15-1:50 | 预留（条件更新）和释放 | 核心流程通了 |
| 1:50-2:15 | 幂等键、并发测试 | 并发测试通过 |
| 2:15-2:35 | 冻结功能，补测试，确认线上是最新版 | 所有测试绿 |
| 2:35-3:00 | README、commit 整理、准备讲解 | 可以 demo |

**如果 1:50 还没做完预留**：砍掉幂等键，保证预留和释放能用。

**如果 0:45 还没部署成功**：停下一切，专门解决部署。

---

## 九、测试策略

本项目有 12 个测试，按价值排序：

1. **并发测试**（最重要）：证明核心不变量在并发下成立
2. 超限返回 409 且用量不变：证明失败请求没有副作用
3. 幂等重放不重复扣费
4. 幂等键配不同内容被拒绝
5. 释放幂等
6. 降低上限后阻止新预留
7. 基础 CRUD 和参数校验

**如果时间只够写三个**：并发测试、超限测试、幂等测试。

**并发测试为什么直接调 service 层**：TestClient 不适合多线程并发，而且我们要测的就是 service 层的原子性。每个线程开自己的 SQLite 连接，这是真实的并发场景。

---

## 十、Code Review 高频问题

### Q1：How do you guarantee the limit is never exceeded?

**中文思路**：条件更新，检查写在 UPDATE 语句里，数据库保证原子性。有并发测试证明。

**英文回答**：
> "The check is inside the UPDATE statement: `SET used = used + amount WHERE used + amount <= limit`. The database evaluates the condition and applies the write atomically, so two concurrent requests can't both pass. I check the affected row count to know whether it succeeded. I also have a test that runs 50 concurrent reservations against a limit of 10 and asserts exactly 10 succeed."

### Q2：What happens with multiple instances?

> "Right now each instance would have its own SQLite file, so they wouldn't share state. That's the first thing to change before scaling out. Once it's on a shared PostgreSQL database, the same conditional UPDATE works across instances, because the atomicity comes from the database, not the application. That's why I didn't use an in-process lock."

### Q3：Why not use a lock in Python?

> "A threading lock only protects a single process. The moment you run two instances, each has its own lock and the guarantee is gone. Pushing the condition into SQL keeps the correctness guarantee independent of how many app instances are running."

### Q4：What if a client reserves but never releases?

> "That's a real gap: the quota leaks. I'd add an expires_at column and a background sweeper that releases expired reservations. A cleaner production design is a two-phase reserve-then-confirm flow, where unconfirmed reservations expire quickly."

### Q5：Why 409 instead of 429?

> "429 is for rate limiting, too many requests in a time window. This is a quota, a cap on total allocation. The request is valid but conflicts with the current state of the resource, which is what 409 means."

### Q6：What happens if the limit is lowered below current usage?

> "I allow it, but I don't revoke existing reservations. New reservations are blocked until usage drops below the new limit. Forcibly deleting a customer's resources is a product decision, not something a quota service should decide on its own."

### Q7：Why store `used` instead of computing it from reservations?

> "It lets a reservation touch a single row, which keeps the atomic check simple and makes it O(1). The trade-off is that the counter could drift from the reservations table if there's a bug. In production I'd add a periodic reconciliation job that compares the two and alerts on mismatch."

### Q8：What did the AI generate and what did you verify?

> "The AI scaffolded the routes and models. I wrote the conditional UPDATE deliberately because it's the core correctness guarantee, and I wrote the concurrency test to verify it actually holds rather than trusting that it looks right."

**这个问题很可能被问**，因为 DO 的面试就是评估你怎么用 AI。回答的关键是：**核心正确性你自己把关，并且有测试证明。**

---

## 十一、已知限制（README 里要写）

1. SQLite 在 App Platform 上数据不持久
2. 单实例，不能水平扩展
3. 没有认证，任何人都能改任何租户的配额
4. 预留不过期，客户端崩溃会导致配额泄漏
5. 没有审计日志
6. used 计数器和 reservations 表没有对账机制

---

## 十二、和你自己经历的连接

**这道题的核心模式你在 nOps 用过**：

- **原子性交给确定性系统**：你在 nOps 把算术从 LLM 移到确定性 SQL，理由是可验证。这里把配额检查交给数据库的条件更新，理由是可保证。**同一个工程直觉：正确性关键的逻辑，交给能提供保证的那一层。**
- **幂等**：你的并发标注服务按原始索引写回结果保证可复现，本质上也是让重复执行产生相同结果。

**面试时可以说**：
> "I tend to push correctness-critical logic into the layer that can actually guarantee it. In my internship I moved arithmetic out of an LLM into deterministic SQL for the same reason: you want the guarantee to come from something that can provide it, not from code that happens to look right."

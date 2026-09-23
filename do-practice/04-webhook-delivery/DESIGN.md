# 04 Webhook 可靠投递服务（Webhook Delivery）设计文档

## 一、题目理解

### 可能的原题表述

> Build a webhook delivery service. Customers register URLs to receive notifications when events happen (e.g. "droplet.created"). When an event occurs, the service should deliver it to every subscribed URL. Deliveries must be reliable: if a customer's server is down, retry later. Customers must be able to verify that requests really came from us.

中文：实现一个 Webhook 投递服务。客户注册 URL 来接收事件通知（比如"虚拟机已创建"）。事件发生时，服务要把它投递给所有订阅了的 URL。投递必须可靠：客户服务器宕机时要稍后重试。客户必须能验证请求确实来自我们。

### 核心问题是什么

**四个难点**：

1. **扇出（fan-out）**：一个事件要发给多个订阅者，每个订阅者独立重试、独立成功失败
2. **可靠投递**：对方挂了要重试，但不能无限重试，也不能压垮对方
3. **签名验证**：接收方怎么知道请求真的来自你，而不是攻击者伪造的
4. **重放攻击**：攻击者截获一个合法请求，过几天再发一遍怎么办

### 为什么 DO 会出这道题

DO 的很多服务都有事件通知（比如 App Platform 部署完成、Droplet 状态变化）。而且 Stripe、GitHub 的 webhook 设计是业界标准，面试官会期待你知道这套做法。

---

## 二、3 小时 Scope

### Must-have

1. 注册 endpoint（URL + 订阅的事件类型）
2. 发布事件，扇出到所有匹配的 endpoint
3. 投递 + 失败重试 + 退避 + 上限
4. **HMAC 签名**
5. 查询投递状态
6. 部署

### Nice-to-have

1. **时间戳防重放**
2. 区分可重试和不可重试的错误码
3. 扇出幂等（重复执行不会重复创建投递）
4. 停用 endpoint
5. 手动重试死信投递
6. **内置接收端，能现场 demo 完整闭环**

**本项目全部实现了。**

### Out-of-scope

| 不做的功能 | 为什么 | code review 时怎么说 |
|---|---|---|
| 后台自动投递 | 同任务队列，用手动触发 | "A background dispatcher would call dispatch_once on a loop." |
| 密钥轮换 | 需要支持新旧两个密钥并存 | "I'd allow two active secrets during a rotation window." |
| 投递顺序保证 | 非常难，而且大部分场景不需要 | "Ordering across retries isn't guaranteed. Receivers should use the event timestamp." |
| endpoint 自动熔断 | 需要统计失败率 | "An endpoint failing consistently would be auto-disabled." |
| 投递内容过滤/转换 | 非核心 | 被问到再说 |

---

## 三、API 设计

| 方法 | 路径 | 作用 | 状态码 |
|---|---|---|---|
| GET | `/health` | 健康检查 | 200 |
| POST | `/endpoints` | 注册 | 201 / 422 |
| GET | `/endpoints` | 列出（不含 secret） | 200 |
| DELETE | `/endpoints/{id}` | 停用 | 200 / 404 |
| POST | `/events` | 发布事件并扇出 | 201 |
| GET | `/events/{id}/deliveries` | 查投递状态 | 200 |
| POST | `/deliveries/{id}/retry` | 重试死信 | 200 / 404 / 409 |
| POST | `/dispatcher/run-once` | 触发一轮投递 | 200 |
| POST | `/receiver` | **demo 用的验签接收端** | 200 / 401 |
| GET | `/receiver/log` | 看接收端收到了什么 | 200 |

### 设计要点

**secret 只在创建时返回一次**：之后列表接口永远不返回。这和 Stripe、GitHub 的做法一致，也是 API key 的标准处理方式。测试 `test_create_endpoint_returns_secret_once` 验证了这一点。

**DELETE 是停用不是删除**：已有的投递记录还引用着这个 endpoint，物理删除会破坏历史。软删除保留审计能力。

**内置接收端**：这是为 demo 设计的。部署后，把 `https://你的域名/receiver` 注册成 endpoint，发布事件，触发投递，再看 `/receiver/log`，就能现场展示完整的"签名 → 投递 → 验签"闭环，不需要第二个服务。

---

## 四、数据模型

```sql
CREATE TABLE endpoints (
    id          TEXT    PRIMARY KEY,
    url         TEXT    NOT NULL,
    secret      TEXT    NOT NULL,
    event_types TEXT    NOT NULL,     -- JSON 列表，["*"] 表示全部
    active      INTEGER NOT NULL DEFAULT 1,
    created_at  INTEGER NOT NULL
);

CREATE TABLE events (
    id         TEXT    PRIMARY KEY,
    type       TEXT    NOT NULL,
    payload    TEXT    NOT NULL,
    created_at INTEGER NOT NULL
);

CREATE TABLE deliveries (
    id               TEXT    PRIMARY KEY,
    event_id         TEXT    NOT NULL REFERENCES events (id),
    endpoint_id      TEXT    NOT NULL REFERENCES endpoints (id),
    status           TEXT    NOT NULL CHECK (status IN ('pending', 'succeeded', 'dead')),
    attempts         INTEGER NOT NULL DEFAULT 0,
    max_attempts     INTEGER NOT NULL,
    next_attempt_at  INTEGER NOT NULL,
    last_status_code INTEGER,
    last_error       TEXT,
    created_at       INTEGER NOT NULL,
    updated_at       INTEGER NOT NULL,
    UNIQUE (event_id, endpoint_id)       -- 关键
);
```

### 设计要点

**为什么事件和投递分开存**：一个事件对应多个投递（每个订阅者一个）。每个投递有独立的状态、重试次数、错误信息。A 客户的服务器挂了不应该影响 B 客户收到通知。

**`UNIQUE (event_id, endpoint_id)` 的作用**：保证同一个事件不会给同一个接收方创建两次投递。配合 `INSERT OR IGNORE`，扇出操作就变成幂等的，重复执行也安全。

**事件 ID 用 `evt_` 前缀**：这是 Stripe 的风格。带前缀的 ID 在日志里一眼就能看出是什么类型的对象（`evt_` 事件、`ep_` endpoint、`dlv_` 投递），排查问题时很有用。

---

## 五、架构与请求流

```
业务系统 ──▶ POST /events
               │
               ▼
       ┌───────────────────┐
       │  一个事务里：      │
       │  1. 存事件         │
       │  2. 找匹配的endpoint│
       │  3. 为每个创建投递  │
       └───────────────────┘
               │
               ▼
        deliveries 表（pending）
               │
调度器 ──▶ POST /dispatcher/run-once
               │
               ▼
     查出所有到期的 pending 投递
               │
       ┌───────┴───────┐
       ▼               ▼
   构造请求 + 签名    （事务外）
       │
       ▼
   HTTP POST 到客户 URL
       │
   ┌───┼──────────────┐
   ▼   ▼              ▼
  2xx  可重试错误      不可重试错误
   │   │              │
   ▼   ▼              ▼
成功  pending+退避     dead
      （次数用完→dead）
```

---

## 六、核心难点与实现

### 难点一：HMAC 签名

**问题**：你的 webhook URL 是公开的，任何人都能往上发请求。接收方怎么知道请求真的来自你？

**解法**：双方共享一个 secret。发送方用 secret 对请求体算 HMAC，放在请求头里。接收方用同一个 secret 再算一遍，对比是否一致。攻击者没有 secret，算不出正确的签名。

```python
def sign(secret, timestamp, body):
    signed = f"{timestamp}.".encode() + body
    digest = hmac.new(secret.encode(), signed, hashlib.sha256).hexdigest()
    return f"v1={digest}"
```

**签名前缀 `v1=`**：为以后换签名算法留余地。如果要升级到 v2，可以同时发两个签名，接收方逐步迁移。

### 难点二：防重放攻击

**问题**：攻击者截获一个合法请求（签名是对的），过几天原样再发一遍。签名验证会通过，接收方会重复处理。

**解法**：**把时间戳也纳入签名**，接收方拒绝时间戳太旧的请求（本项目是 5 分钟）。

```python
def verify(secret, timestamp, body, signature, now, tolerance=300):
    if abs(now - timestamp) > tolerance:   # 太旧或太新都拒绝
        return False
    return hmac.compare_digest(sign(secret, timestamp, body), signature)
```

**为什么时间戳必须在签名里**：如果时间戳只是一个普通请求头，攻击者可以把它改成当前时间再重放。签名里包含时间戳，改了时间戳签名就对不上了。

测试 `test_signature_rejects_tampered_body_and_old_timestamp` 验证了三种攻击：篡改内容、延迟重放、错误密钥。

### 难点三：常量时间比较

```python
return hmac.compare_digest(expected, signature)   # 正确
return expected == signature                       # 错误！
```

**为什么**：普通的 `==` 比较字符串时，遇到第一个不同的字符就返回。攻击者可以通过测量响应时间，逐个字符猜出正确的签名（猜对第一个字符时响应稍慢一点）。这叫**时序攻击**（timing attack）。

`compare_digest` 无论哪里不同，都比较完整个字符串才返回，耗时恒定。

**面试时提这一点会很加分**，这是安全意识的直接体现。

### 难点四：区分可重试和不可重试的错误

```python
RETRYABLE_4XX = {408, 429}

def is_retryable(status_code):
    if status_code is None:        # 网络错误、超时 → 重试
        return True
    if 400 <= status_code < 500:   # 客户端错误
        return status_code in RETRYABLE_4XX
    return True                     # 5xx → 重试
```

| 状态码 | 含义 | 重试？ | 理由 |
|---|---|---|---|
| 2xx | 成功 | 不需要 | |
| 400、401、404 等 | 对方拒绝了请求本身 | **不重试** | 发同样的请求，结果还是一样 |
| 408 Request Timeout | 对方超时 | 重试 | 暂时性问题 |
| 429 Too Many Requests | 对方限流 | 重试 | 暂时性问题 |
| 5xx | 对方服务器错误 | 重试 | 可能是暂时的 |
| 网络错误 | 连不上 | 重试 | 可能是暂时的 |

**为什么这个区分重要**：如果对 404 也重试，一个配错了 URL 的客户会让你的系统白白发起几十次注定失败的请求。

### 难点五：扇出幂等

```sql
INSERT OR IGNORE INTO deliveries (...) VALUES (...)
-- 配合 UNIQUE (event_id, endpoint_id)
```

**场景**：扇出过程中服务崩溃了，只给一半的 endpoint 创建了投递。重新执行扇出时，已经创建的会被 IGNORE 跳过，只补上缺的。

测试 `test_fan_out_is_idempotent` 证明重复扇出不会产生重复投递。

### 难点六：事件和投递在同一个事务里写入

```python
with transaction(immediate=True) as conn:
    conn.execute("INSERT INTO events ...")
    _fan_out(conn, ...)    # 同一个事务
```

**保证**：不会出现"事件存了但投递没创建"或者"投递创建了但事件不存在"的中间状态。

### 难点七：HTTP 请求在事务外

投递循环里，HTTP 请求不在任何数据库事务里执行。

**为什么**：客户的服务器可能要 5 秒才响应（超时时间）。如果在事务里等，SQLite 的写锁会被占用 5 秒，这期间谁都没法写数据库。

---

## 七、关键 Trade-off

### Trade-off 1：同步投递 vs 异步投递

**本项目：异步**。发布事件只写数据库，投递由调度器单独执行。

**另一种：同步**。发布事件时直接发 HTTP 请求。

| | 异步（本项目） | 同步 |
|---|---|---|
| 发布事件的延迟 | 快（只写数据库） | 慢（要等所有接收方响应） |
| 一个接收方慢 | 不影响其他 | 拖慢整个发布 |
| 可靠性 | 高（崩溃了可以重试） | 低（崩溃了就丢了） |
| 实时性 | 取决于调度频率 | 实时 |

**选择理由**：一个客户的服务器慢或者挂了，绝不能影响事件发布本身和其他客户。

### Trade-off 2：至少一次 vs 恰好一次

**本项目提供至少一次**。

**会重复投递的场景**：客户服务器收到请求、处理完了，但它的 200 响应在网络上丢了。我们以为失败了，会重试，客户就收到两次。

**解决办法**：每个请求带 `X-Webhook-Id`（事件 ID），接收方用它去重。**这是接收方的责任**，Stripe 的文档也是这么要求客户的。

### Trade-off 3：投递顺序

**本项目不保证顺序。**事件 A 先发布、B 后发布，但如果 A 投递失败在退避中，B 可能先到。

**为什么不保证**：严格顺序需要"A 没成功之前 B 不能发"，一个事件卡住会堵死后面所有事件。这个代价通常不值得。

**客户端怎么处理**：用事件里的 `created_at` 判断先后，或者收到通知后回调 API 拿最新状态（而不是依赖 webhook 内容本身）。

### Trade-off 4：密钥存明文

**本项目的 secret 在数据库里是明文。**

**为什么不能存哈希**：和密码不同，HMAC 签名需要原始 secret 才能计算，所以不能单向哈希。

**生产演进**：用 KMS（密钥管理服务）加密存储，应用启动时解密到内存。

---

## 八、3 小时时间分配

| 时间 | 做什么 | 检查点 |
|---|---|---|
| 0:00-0:15 | 读题、定 scope、建仓库 | |
| 0:15-0:30 | 骨架 + `/health` | |
| 0:30-0:45 | **第一次部署** | 线上可访问 |
| 0:45-1:10 | endpoint 注册、事件发布、扇出 | 能创建投递 |
| 1:10-1:40 | 签名 + 投递 + 成功路径 | 能发出请求 |
| 1:40-2:05 | 重试退避 + 可重试判断 + 死信 | |
| 2:05-2:25 | 内置接收端 + 现场验证闭环 | 线上 demo 通 |
| 2:25-2:40 | 冻结功能 | |
| 2:40-3:00 | README + 讲解准备 | |

**如果时间紧**：砍掉手动重试、停用 endpoint。**签名不能砍**，那是这道题的核心。

---

## 九、测试策略

15 个测试，按价值排序：

1. **签名拒绝篡改、重放、错误密钥**：安全核心
2. **内置接收端验签**：端到端
3. 5xx 重试且按退避延迟
4. 4xx 立即进死信，429 重试
5. 扇出按事件类型过滤、幂等
6. 达到上限进死信

**测试技巧**：`FakeSender` 类可以编排返回码序列（比如先返回 503 再返回 200），让重试逻辑完全可控，不需要真的网络。

---

## 十、Code Review 高频问题

### Q1：How does a receiver know the request came from you?

> "Every request is signed with HMAC-SHA256 using a secret shared only with that endpoint. The receiver recomputes the signature and compares. An attacker without the secret can't produce a valid signature."

### Q2：What about replay attacks?

> "The timestamp is included in the signed payload, and the receiver rejects anything more than five minutes old. It has to be inside the signature, otherwise an attacker could just update the timestamp header on a captured request."

### Q3：Why compare_digest instead of ==?

> "Normal string comparison returns at the first differing character, so response timing leaks how much of a forged signature was correct. An attacker could recover the signature byte by byte. compare_digest runs in constant time."

### Q4：Can a receiver get the same event twice?

> "Yes, delivery is at-least-once. If the receiver processed the request but its 200 was lost in transit, we'll retry. Every request carries the event id in X-Webhook-Id, and receivers are expected to deduplicate on it. That's the same contract Stripe documents."

### Q5：Why not retry on 404?

> "A 4xx means the receiver rejected the request itself. Sending the identical request again won't change the answer, it just wastes resources. The exceptions are 408 and 429, which describe transient conditions on the receiver's side."

### Q6：What if one customer's endpoint is really slow?

> "Delivery is asynchronous and each delivery is independent, so a slow endpoint doesn't delay event publishing or other customers. Requests have a five-second timeout. In production I'd also add per-endpoint concurrency limits and auto-disable endpoints that fail consistently."

### Q7：Do you guarantee ordering?

> "No. If event A is in backoff, event B can arrive first. Strict ordering would mean one stuck event blocks everything behind it. Receivers should use the event's created_at, or treat the webhook as a signal and fetch current state from the API."

### Q8：How would you rotate secrets?

> "Allow two active secrets per endpoint during a rotation window, and send a signature for each. The receiver accepts either, switches to the new one, and then the old one is retired."

---

## 十一、已知限制

1. SQLite 数据不持久
2. 投递需要外部触发，没有后台调度器
3. secret 明文存储
4. 不支持密钥轮换
5. 不保证投递顺序
6. 没有 endpoint 自动熔断
7. 内置接收端的日志存在内存里，重启就没了

---

## 十二、和你自己经历的连接

| 这道题 | 你的经历 |
|---|---|
| 重试 + 退避 + 区分错误类型 | nOps：限流错误用 4 的幂次退避，其他错误用 2 的幂次 |
| 可重试 vs 不可重试 | nOps：输出截断用分级提高 max_tokens 救回，权限错误直接升级给 manager |
| 验证外部输入 | nOps：自建 grounding checker，把模型输出的每个数字对照源数据校验 |
| 异步解耦 | nOps：并发标注服务和主流程分离 |

**面试时可以说**：
> "In my internship I handled a similar split between retryable and non-retryable failures. Throttling errors got a longer backoff than other errors, truncated responses were recovered by raising the token limit in stages, and an IAM permission failure wasn't something to retry at all. I traced it to a policy rollback and escalated. The general principle is the same as here: retry what's transient, stop immediately on what isn't."

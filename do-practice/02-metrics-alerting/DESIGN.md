# 02 指标采集与告警服务（Metrics & Alerting）设计文档

## 一、题目理解

### 可能的原题表述

> Build a service that collects metrics from cloud resources (e.g. CPU usage from Droplets), lets users query them over time, and fires alerts when a metric crosses a threshold. For example: "alert me if average CPU on droplet-1 is above 80% over the last 5 minutes."

中文：实现一个指标服务，从云资源（比如虚拟机的 CPU 使用率）采集指标，支持按时间查询，并在指标越过阈值时触发告警。例如"如果 droplet-1 过去 5 分钟平均 CPU 超过 80% 就告警"。

### 核心问题是什么

**三个难点**：

1. **时间窗口聚合**：原始数据点很多，查询时要按时间桶聚合（比如每分钟一个平均值）
2. **告警去重**：CPU 持续超标一小时，不应该每次评估都发一条新告警。**这是最容易被忽略、面试官最可能问的点**
3. **缺失数据的语义**：没有数据时，告警该保持还是解除？

### 为什么 DO 会出这道题

DO 自己就有 Monitoring 产品，给 Droplet 提供 CPU、内存、磁盘等指标和告警策略。这道题几乎就是他们产品的简化版。

---

## 二、3 小时 Scope

### Must-have

1. 批量写入指标点
2. 按资源、指标名、时间范围查询，支持按时间桶聚合
3. 创建告警规则（资源、指标、比较方向、阈值、时间窗口）
4. 评估规则，产生告警
5. **告警去重**：持续超标只产生一条告警
6. 告警恢复：指标回落后自动解除
7. 部署

### Nice-to-have

1. 多种聚合方式（avg/max/min/sum/count）
2. 缺失数据不解除告警
3. 拒绝未来时间戳
4. 批量写入部分成功（一个坏点不拖累整批）

**本项目全部实现了。**

### Out-of-scope

| 不做的功能 | 为什么 | code review 时怎么说 |
|---|---|---|
| 定时自动评估 | 需要后台调度器，难测试难 demo | "I exposed evaluation as an endpoint. In production a scheduler would call it every minute." |
| 告警通知（邮件/Slack） | 集成外部服务吃时间 | "Firing alerts would be pushed to a notification queue, consumed by a separate sender." |
| 数据保留与降采样 | 需要后台任务 | "I'd downsample old data to hourly and drop raw points after 7 days." |
| 专用时序数据库 | 部署复杂 | "Prometheus or TimescaleDB would replace SQLite at scale." |
| 告警静默/抑制 | 非核心 | 被问到再说 |

---

## 三、API 设计

| 方法 | 路径 | 作用 | 状态码 |
|---|---|---|---|
| GET | `/health` | 健康检查 | 200 |
| POST | `/metrics` | 批量写入 | 202 |
| GET | `/metrics` | 聚合查询 | 200 / 422 |
| POST | `/alert-rules` | 创建规则 | 201 |
| GET | `/alert-rules` | 列出规则 | 200 |
| POST | `/alerts/evaluate` | 评估所有规则 | 200 |
| GET | `/alerts?state=firing` | 查询告警 | 200 |

### 设计要点

**写入为什么返回 202 不是 201**：202 Accepted 表示"已接收"，语义上适合指标写入这种高频、可能异步处理的场景。生产环境里写入通常先进消息队列，202 为以后改成异步留了余地。

**写入为什么是批量接口**：真实的监控 agent 每隔几秒上报一批指标，逐条发 HTTP 请求开销太大。批量上限 1000 条，防止单个请求过大。

**批量写入部分成功**：返回 `{accepted, rejected, errors}`。一个坏数据点（比如时间戳错误）不应该导致整批数据丢失。

**查询的防护**：`(end - start) / bucket_seconds > 10000` 时拒绝，防止有人查一年的数据却用 1 秒的桶，返回几千万行把服务拖死。

**评估接口暴露 `now` 参数**：让测试和 demo 能在固定时间点评估，结果完全确定。

---

## 四、数据模型

```sql
CREATE TABLE metrics (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    resource_id TEXT    NOT NULL,
    name        TEXT    NOT NULL,
    value       REAL    NOT NULL,
    ts          INTEGER NOT NULL      -- Unix 秒
);
CREATE INDEX idx_metrics_lookup ON metrics (resource_id, name, ts);

CREATE TABLE alert_rules (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    resource_id    TEXT    NOT NULL,
    metric_name    TEXT    NOT NULL,
    comparator     TEXT    NOT NULL CHECK (comparator IN ('gt', 'lt')),
    threshold      REAL    NOT NULL,
    window_seconds INTEGER NOT NULL CHECK (window_seconds > 0),
    created_at     INTEGER NOT NULL
);

CREATE TABLE alerts (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_id     INTEGER NOT NULL REFERENCES alert_rules (id),
    state       TEXT    NOT NULL CHECK (state IN ('firing', 'resolved')),
    value       REAL    NOT NULL,     -- 触发时的聚合值
    started_at  INTEGER NOT NULL,
    resolved_at INTEGER
);
CREATE INDEX idx_alerts_rule_state ON alerts (rule_id, state);
```

### 设计要点

**复合索引 `(resource_id, name, ts)` 为什么是这个顺序**：所有查询都是"某资源 + 某指标 + 某时间范围"。等值条件的列放前面（resource_id, name），范围条件的列放最后（ts）。这样数据库能先精确定位到某资源某指标，再在 ts 上做范围扫描。**如果顺序反了（ts 在前），索引几乎没用。**

**时间戳用整数秒而不是字符串**：整数可以直接做除法算时间桶，比较和范围查询也快。

**告警是独立的表而不是规则上的一个字段**：因为一条规则会多次触发和恢复，每次都是一条历史记录。如果只在规则上存一个 `is_firing` 字段，就丢失了历史。

---

## 五、架构与请求流

```
监控 Agent ──批量上报──▶ POST /metrics ──▶ metrics 表
                                              │
用户 ──▶ GET /metrics ──▶ 按时间桶聚合 ◀────────┤
                                              │
调度器 ──▶ POST /alerts/evaluate ──▶ 读规则 ──▶ 窗口聚合
                                        │
                                        ▼
                                  状态机转换
                                        │
                                        ▼
                                   alerts 表
```

### 评估流程

```
对每条规则：
  1. 算窗口内平均值：AVG(value) WHERE ts > now - window AND ts <= now
  2. 窗口内没有数据 → 记为 no_data，不改变状态，跳过
  3. 查这条规则当前有没有 firing 的告警
  4. 按下表转换：

     超标？  当前 firing？   动作
     ─────  ────────────   ──────────────────
     是      否            新建 firing 告警
     是      是            不动（去重的关键）
     否      是            把告警改为 resolved
     否      否            不动
```

---

## 六、核心难点与实现

### 难点一：时间桶聚合

```sql
SELECT (ts / 60) * 60 AS bucket_start, AVG(value), COUNT(*)
FROM metrics
WHERE resource_id = ? AND name = ? AND ts >= ? AND ts < ?
GROUP BY bucket_start
```

`(ts / 60) * 60` 利用整数除法把时间戳向下取整到分钟边界。比如 `ts = 125` → `(125/60)*60 = 2*60 = 120`。

**一个真实踩到的坑**：桶边界是**按 Unix epoch 对齐**的，不是按你的查询起点对齐的。如果你的起点是 `1700000000`，而 `1700000000 % 30 = 20`，那 30 秒的桶边界会落在起点之前 20 秒的位置，数据点被切到意料之外的桶里。

**测试里就踩了这个坑**，第一版测试用了一个没对齐的起点，断言失败了。修复方法是把测试起点对齐到整小时。

**面试时的说法**：
> "Buckets are aligned to the Unix epoch, not to the query start. That's usually what you want, because it means the same minute always falls in the same bucket regardless of who's querying. I actually hit this in my first test, where an unaligned start time split points across buckets unexpectedly."

### 难点二：告警去重（最重要）

**如果不做去重**：CPU 持续超标一小时，调度器每分钟评估一次，就会产生 60 条告警，用户手机被通知轰炸。

**解法**：把告警建模成状态机。每条规则同一时刻最多一条 firing 告警。只在"不在告警 → 告警"这个**转换**时新建记录。

测试 `test_sustained_breach_does_not_duplicate_alert` 证明了这一点：连续评估两次，第二次 `fired` 为空，总告警数仍为 1。

**这和你在 nOps 做的事情本质一样**：你发现 30 天滚动基线会让同一次成本阶跃被连续 28 天重复判为异常，于是做了 episode 聚合，把连续异常合并成一个事件。**同一个问题，同一个思路。**

### 难点三：缺失数据的语义

**场景**：CPU 超标告警已经在 firing，然后监控 agent 挂了，一个小时没有上报任何数据。

**错误做法**：窗口内没数据 → 平均值算不出来 → 当作"不超标" → 自动解除告警。

**问题**：agent 挂了往往意味着机器出了大问题，这时候反而把告警解除了，是最危险的情况。

**正确做法**：没有数据时不改变状态。**没有数据不等于健康。**

测试 `test_no_data_does_not_resolve_firing_alert` 覆盖了这个场景。

**生产演进**：应该单独有一个"数据缺失"告警（absence alert），agent 超过一定时间没上报就告警。

### 难点四：NaN 导致 500（一个真实的 bug）

**现象**：客户端发送一个 NaN 值，期望得到 422，实际得到 500。

**原因**：
1. Pydantic 验证器正确地拒绝了 NaN（`math.isfinite` 检查）
2. FastAPI 默认的 422 错误响应会把**原始输入值回显**在错误信息里
3. NaN 不能被序列化成合法 JSON
4. 序列化错误响应时崩溃，变成 500

**修复**：自定义 `RequestValidationError` 处理器，错误信息里不回显原始输入。

**为什么这个值得讲**：这就是 DO 博客里说的那个时刻，"AI 自信地产出一个看起来对但实际跑不通的东西"。验证器本身写得完全正确，问题出在框架的错误处理路径上，**只有写了测试才会发现**。

**面试时的说法**：
> "My validator correctly rejected NaN, but the test got a 500 instead of a 422. FastAPI's default error handler echoes the rejected input back in the response, and NaN can't be serialized to JSON, so building the error response crashed. I replaced the handler to omit the raw input. It's a good example of why I test the failure paths, not just the happy path."

### 难点五：为什么用平均值而不是任意一个点

规则是"窗口内平均值超过阈值"。测试 `test_brief_spike_averaged_out` 证明了单个尖峰不会触发告警。

**trade-off**：平均值能过滤噪声，但会延迟发现真正的问题。生产系统通常支持多种策略（比如"窗口内所有点都超标"或者"最大值超标"）。

---

## 七、关键 Trade-off

### Trade-off 1：拉取式评估 vs 推送式评估

**本项目：定期拉取评估**（调度器每隔一段时间调用 evaluate）。

**另一种：推送式**，每写入一个数据点就检查相关规则。

| | 定期评估 | 写入时评估 |
|---|---|---|
| 告警延迟 | 最多一个评估周期 | 几乎实时 |
| 写入性能 | 不受影响 | 每次写入都变慢 |
| 缺失数据检测 | 能做 | 做不了（没写入就不会触发） |
| 实现复杂度 | 低 | 中 |

**选择理由**：缺失数据检测只有定期评估能做，而且写入路径保持简单快速。Prometheus 也是这个模型。

### Trade-off 2：SQLite vs 时序数据库

**SQLite 的问题**：指标数据写入量巨大、按时间有序、很少更新、经常按时间范围查询。这些特征正好是关系型数据库不擅长的。

**生产演进**：
- 中等规模：TimescaleDB（PostgreSQL 扩展，SQL 不用大改）
- 大规模：Prometheus、InfluxDB，或者 ClickHouse 这种列存

### Trade-off 3：原始数据永久保存

**问题**：每台机器每 10 秒一个点，1000 台机器一天就是 860 万行，存储无限增长。

**生产演进**：降采样（downsampling）。最近 7 天保留原始数据，7 到 90 天降为每小时一个点，90 天以上降为每天一个点。

### Trade-off 4：每次评估读全部规则

**问题**：规则多了之后，每次评估要跑几千条聚合查询。

**生产演进**：按规则分片，多个评估 worker 并行；或者按资源分组，一次查询算出一个资源的所有规则。

---

## 八、3 小时时间分配

| 时间 | 做什么 | 检查点 |
|---|---|---|
| 0:00-0:15 | 读题、定 scope、建仓库 | |
| 0:15-0:30 | 骨架 + `/health` | 本地能跑 |
| 0:30-0:45 | **第一次部署** | 线上可访问 |
| 0:45-1:15 | 写入 + 聚合查询 | 能查到数据 |
| 1:15-1:55 | 规则 + 评估 + **状态机去重** | 核心流程通 |
| 1:55-2:15 | 恢复逻辑 + 缺失数据处理 | |
| 2:15-2:35 | 冻结功能，补测试 | |
| 2:35-3:00 | README + 讲解准备 | |

**如果时间紧**：砍掉多种聚合方式（只留 avg），砍掉未来时间戳校验。**状态机去重不能砍**，那是这道题的核心考点。

---

## 九、测试策略

11 个测试，按价值排序：

1. **持续超标不重复告警**：核心考点
2. **缺失数据不解除告警**：体现对生产语义的理解
3. 超标触发、恢复解除
4. 单个尖峰被平均掉
5. NaN 返回 422 而不是 500
6. 时间桶聚合正确
7. 部分成功的批量写入

---

## 十、Code Review 高频问题

### Q1：How do you avoid alert spam during a sustained breach?

> "Alerts are a state machine per rule. There's at most one firing alert per rule, and I only create a new alert on the transition from not-firing to firing. If it's already firing, the next evaluation does nothing. I have a test that evaluates twice during a sustained breach and asserts only one alert exists."

### Q2：What happens if a server stops reporting metrics?

> "The rule sees no data in the window and I leave the state unchanged. I deliberately don't resolve the alert, because missing data isn't healthy data. A server that's stopped reporting is often in the worst state, and it shouldn't silently clear its own alert. In production I'd add a separate absence alert for that case."

### Q3：Why evaluate on a schedule instead of on every write?

> "Two reasons. It keeps the write path fast, since ingestion is high-volume. And it's the only way to detect missing data: if nothing is written, a write-triggered check never runs. The trade-off is up to one evaluation interval of alert latency."

### Q4：How would this scale?

> "SQLite is the first bottleneck. Metrics are write-heavy, append-only, and queried by time range, which is exactly what time-series databases are built for. I'd move to TimescaleDB first since it keeps SQL, and add downsampling so raw points don't grow without bound. For evaluation, I'd shard rules across multiple workers."

### Q5：Why is the index on (resource_id, name, ts)?

> "Every query filters by exact resource and metric name, then a time range. Equality columns go first and the range column last, so the database can seek directly to one series and scan a contiguous range. If ts were first, the index would barely help."

### Q6：Tell me about a bug you hit.

用难点四（NaN 导致 500）或者难点一（时间桶对齐），都是这次真实发生的。

---

## 十一、已知限制

1. SQLite 数据不持久，且不适合时序数据的写入量
2. 评估需要外部调用，没有内置调度器
3. 没有通知渠道
4. 原始数据无限增长，没有保留策略
5. 只支持平均值规则，不支持百分位数（p95、p99）
6. 没有缺失数据告警

---

## 十二、和你自己经历的连接

**这道题几乎就是你 nOps 项目的简化版**：

| 这道题 | 你在 nOps 做的 |
|---|---|
| 时间窗口聚合 | 30 天滚动基线、小时级聚合 |
| 告警去重 | episode 聚合，把连续异常小时合并成一个事件 |
| 缺失数据语义 | CUR 投递延迟处理：最近 24 小时不产生事件 |
| 按时段分组的基线 | 按服务 × 小时 × 工作日/周末分组，用中位数和 MAD |

**面试时可以说**：
> "This is close to what I built in my internship: a cost anomaly detection system over AWS billing data. The alert deduplication here is the same problem I solved there with episode aggregation. A rolling baseline was flagging a single permanent cost change as a new anomaly every day for 28 days, and I merged consecutive anomalous periods into one event structurally, rather than cleaning up duplicates afterwards."

**如果被问"你会怎么改进阈值"**：
> "A fixed threshold ignores that normal load varies by time of day. In my internship I grouped baselines by service, hour-of-day, and weekday versus weekend, and used median and MAD instead of mean and a fixed percentage band, so the threshold adapts to each series' own volatility."

**这一条非常强**，因为它直接展示了你在真实系统里做过更复杂的版本。

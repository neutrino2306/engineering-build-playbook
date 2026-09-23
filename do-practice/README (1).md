# DigitalOcean 面试练习：五个后端小系统

五个能跑的 FastAPI 小项目，对应 DO 3 小时 build session 最可能出的五类题。

**用法**：现场拿到题目后，先用下面的「关键词匹配表」找到最像的那个项目，再打开它的 `DESIGN.md` 看核心难点和 code review 答法。

---

## 一、五个系统一句话介绍

### 01-quota-service　配额服务

**名字翻译**：quota = 配额，service = 服务

**它是干什么的**：限制每个客户最多能用多少资源。比如"张三最多只能开 5 台服务器"，第 6 台就拒绝。

**生活类比**：食堂饭卡每天限额 50 块，刷超了就刷不出来。

**核心难点**：两个人同时刷卡时，不能都刷成功导致超额。

---

### 02-metrics-alerting　指标监控与告警

**名字翻译**：metrics = 指标（CPU、内存这类数字），alerting = 告警

**它是干什么的**：收集服务器的 CPU 等数据，超过阈值就报警。比如"CPU 平均超过 80% 持续 5 分钟就告警"。

**生活类比**：体温计一直测体温，连续发烧就提醒你。

**核心难点**：一直发烧时不能每分钟都提醒一次（去重）；体温计没电了不能当作"退烧了"。

---

### 03-task-queue　任务队列

**名字翻译**：task = 任务，queue = 队列

**它是干什么的**：用户提交一个耗时任务（比如"帮我备份磁盘"），系统先说"收到了"，然后后台慢慢做，用户可以随时查进度。失败了会自动重试。

**生活类比**：去奶茶店点单，拿个号，后面做好了叫你。做坏了重做，重做三次还坏就放弃。

**核心难点**：做奶茶的店员中途晕倒了，这杯要能被别人接手，不能永远卡着。

---

### 04-webhook-delivery　Webhook 推送

**名字翻译**：webhook = 回调通知（我方主动去通知你的网址），delivery = 投递

**它是干什么的**：客户登记一个网址，系统里发生事情时（比如"服务器创建好了"），我们主动发请求通知这个网址。对方挂了就过会儿再发。

**生活类比**：快递到了，快递员主动打电话通知你。没接就过会儿再打。

**核心难点**：对方怎么确认这个电话真的是快递公司打的，不是骗子（签名验证）。

---

### 05-url-shortener　短链接服务

**名字翻译**：URL = 网址，shortener = 缩短器

**它是干什么的**：把一个很长的网址变成短的，比如 `abc.com/Xk9pQ2m`，点开自动跳转到原网址，并统计点了多少次、从哪来的。

**生活类比**：给一个很长的地址起个短门牌号，谁来问路就指过去，顺便记一下来了几个人。

**核心难点**：跳转要用 307 不能用 301（否则浏览器缓存后就统计不到了）；`/{短码}` 这个路由必须放最后。

---

## 二、现场关键词匹配表（最重要）

读题时找这些词，出现哪个就对应哪个项目。

| 题目里出现这些词 | 对应项目 |
|---|---|
| quota、limit、usage、allocate、reserve、"cannot exceed"、资源上限 | **01 配额服务** |
| rate limit、throttle、requests per minute | **01 配额服务**（思路相同，改成按时间窗口计数） |
| metrics、monitoring、CPU、threshold、alert、time series、dashboard | **02 指标告警** |
| job、task、background、async、worker、retry、"long-running"、status polling | **03 任务队列** |
| schedule、cron、"run later" | **03 任务队列**（加一个执行时间字段） |
| webhook、callback、notify、subscribe、event、"push to customer URL" | **04 Webhook** |
| short link、redirect、alias、click tracking、analytics | **05 短链接** |

### 如果题目不完全一样怎么办

**题目是两个项目的组合**，比如"用户提交任务，完成后通知他的网址"：
→ 03 任务队列 + 04 Webhook，先做 03，再把 04 的签名和重试加上去。

**题目是 CRUD 加一点可靠性**，比如"管理虚拟机的创建和删除"：
→ 创建是耗时操作，按 03 任务队列的状态机思路做（queued → running → succeeded / failed）。

**完全匹配不上**：
→ 打开根目录的 `COMMON_PATTERNS.md`，看题目需要哪个通用模式（防超额、防重复、状态机、重试退避）。五个项目都是这几个模式的不同组合。

---

## 三、五个项目的共同结构

每个项目都一样，看懂一个就看懂全部：

```
app/
  main.py      接口层：定义有哪些网址可以访问，出错时返回什么状态码
  service.py   业务层：真正的逻辑都在这里
  db.py        存储层：连接数据库、建表
  models.py    数据格式：规定请求和返回长什么样
tests/
  test_api.py  测试
DESIGN.md      中文设计文档（给你复习用）
README.md      英文说明（给面试官看的）
```

**现场说法**：
> "I split it into three layers: routes in main.py, business logic in service.py, and storage in db.py. That keeps each part testable on its own."

---

## 四、每个项目最该记住的一句话

| 项目 | 核心技巧 | 面试时一句话 |
|---|---|---|
| 01 配额 | 把"检查余额"写进 UPDATE 语句里 | "The check is inside the UPDATE, so the database makes it atomic." |
| 02 告警 | 同一条规则同时最多一条告警在响 | "I only create an alert when it goes from not-firing to firing." |
| 03 任务队列 | 抢任务时加租约，超时自动收回 | "If a worker crashes, its lease expires and another worker picks it up." |
| 04 Webhook | 用密钥对内容和时间戳签名 | "Receivers verify an HMAC signature that includes a timestamp." |
| 05 短链 | 307 跳转，catch-all 路由放最后 | "307 keeps every click hitting my server, so analytics stay accurate." |

---

## 五、术语翻译表

看代码和文档时遇到不懂的词查这里。

| 英文 | 中文 | 一句话解释 |
|---|---|---|
| tenant | 租户 | 一个客户（公司或个人） |
| reservation | 预留 | 占用一部分配额 |
| atomic | 原子的 | 要么全做完，要么全没做，中间不会被打断 |
| race condition | 竞态条件 | 两个请求同时来，结果取决于谁快，导致出错 |
| idempotent / idempotency | 幂等 | 同一个请求发多少次，结果都和发一次一样 |
| Idempotency-Key | 幂等键 | 客户端给请求起的唯一编号，服务端用它去重 |
| transaction | 事务 | 一组数据库操作，打包成一个整体执行 |
| state machine | 状态机 | 一个东西有几个固定状态，只能按规定路线切换 |
| retry | 重试 | 失败了再试一次 |
| exponential backoff | 指数退避 | 每次重试等待时间翻倍：2 秒、4 秒、8 秒 |
| jitter | 抖动 | 等待时间加点随机，避免大家同时重试 |
| dead letter / dead | 死信 | 重试次数用完，放弃，等人工处理 |
| worker | 工作进程 | 在后台真正干活的那部分程序 |
| lease | 租约 | 抢到任务时的"占用期限"，过期没做完就收回 |
| fencing token | 防护令牌 | 每次抢任务发一个新编号，旧编号的结果作废 |
| at-least-once | 至少一次 | 保证至少执行一次，但可能重复 |
| fan-out | 扇出 | 一个事件同时发给多个接收方 |
| HMAC signature | HMAC 签名 | 用密钥算出的"指纹"，证明内容没被改、来源可信 |
| replay attack | 重放攻击 | 坏人截获一个合法请求，过后原样再发一遍 |
| threshold | 阈值 | 超过就触发的那个界限值 |
| window | 时间窗口 | 比如"最近 5 分钟" |
| bucket | 时间桶 | 把数据按每分钟、每小时分组 |
| redirect | 重定向 / 跳转 | 访问 A 网址，自动跳到 B 网址 |
| 301 / 307 | 永久跳转 / 临时跳转 | 301 浏览器会缓存，307 不会 |
| collision | 碰撞 | 随机生成的码和已有的重复了 |
| health check | 健康检查 | `/health` 接口，用来确认服务活着 |
| ephemeral | 临时的 | App Platform 上的文件重新部署就没了 |
| trade-off | 取舍 | 选了一个好处，就要接受一个代价 |

---

## 六、本地运行任意一个项目

```bash
cd 01-quota-service
pip install -r requirements.txt
uvicorn app.main:app --reload
```

浏览器打开 `http://127.0.0.1:8000/docs`，可以直接点按钮试每个接口。

跑测试：

```bash
pytest -v
```

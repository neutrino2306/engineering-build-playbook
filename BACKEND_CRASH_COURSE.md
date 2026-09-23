# 后端 / 全栈 / 容器化 速成复习（零基础版）

**这一版的规则**：
1. 每一句英文后面都跟着中文翻译
2. 所有专业词第一次出现时都会解释，不默认你知道
3. 先讲"这是什么"，再讲"为什么"，最后给"面试怎么说"

**时间不够的阅读顺序**：第 0 节（基础词）→ 第 1 节（review 怎么进行）→ 第 3 节（FastAPI）→ 第 8 节（Docker）→ 第 10 节（扩展性）→ 第 14 节（自测题）

---

## 第 0 节：先搞懂这些最基础的词

后面所有内容都建立在这些词上。**这一节不用背，看懂就行。**

### 服务器和客户端

**客户端（client）**：发出请求的一方。比如你的浏览器、手机 App、另一个程序。

**服务器（server）**：接收请求、处理、返回结果的一方。你写的 FastAPI 程序跑起来就是一个服务器。

类比：去餐厅点菜。你是客户端，厨房是服务器。你说"我要一份炒饭"（请求），厨房做好端给你（响应）。

### 后端、前端、全栈

**前端（frontend）**：用户看得见的部分，网页上的按钮、输入框、页面。用 HTML、CSS、JavaScript 写，在用户的浏览器里运行。

**后端（backend）**：用户看不见的部分，处理数据、存数据库、执行业务逻辑。你的 FastAPI 项目就是后端，在服务器上运行。

**全栈（full-stack）**：前端和后端都做。

### API

**API（Application Programming Interface，应用程序接口）**：程序之间约定好的"沟通方式"。你的后端对外提供一组网址，每个网址做一件事，别的程序按约定调用就行。

比如你的配额服务：访问 `PUT /tenants/acme/quotas/droplets` 就是"设置 acme 的服务器配额"。这一组网址合起来就叫这个服务的 API。

### 请求和响应

**请求（request）**：客户端发给服务器的消息，包含四部分：
**方法**：要做什么动作（GET 是读取，POST 是创建）
**路径**：要操作哪个东西（`/tenants/acme/quotas`）
**请求头（headers）**：附加信息，一行一行的"名字: 值"。比如 `Content-Type: application/json` 表示"我发的内容是 JSON 格式"
**请求体（body）**：要发送的具体数据

**响应（response）**：服务器返回的消息，包含：
**状态码**：一个三位数字，表示结果（200 成功、404 找不到）
**响应头**和**响应体**

### JSON

**JSON**：一种文本格式，用来在程序之间传数据。长得很像 Python 的字典：

```json
{"resource": "droplets", "amount": 3}
```

前后端之间、API 之间，几乎都用 JSON 传数据。

### IP、端口、localhost

**IP 地址**：一台机器在网络上的地址，比如 `192.168.1.5`。

**localhost / 127.0.0.1**：特殊地址，意思是"本机自己"。你在自己电脑上访问 `127.0.0.1:8000`，就是访问自己电脑上跑的程序。

**端口（port）**：一台机器上可以同时跑很多程序，端口号用来区分找哪个程序。类比：IP 是小区地址，端口是门牌号。`127.0.0.1:8000` 就是"本机的 8000 号门"。

**0.0.0.0**：服务器启动时写这个，意思是"任何地址来的请求我都接"。如果写 127.0.0.1，就只接受本机自己发来的请求，外面的人访问不到。

### 框架和库

**库（library）**：别人写好的一堆函数，你拿来调用。比如 `sqlite3` 是操作数据库的库。

**框架（framework）**：别人搭好的架子，你往里填自己的代码。FastAPI 是框架：它负责接收请求、解析参数、返回 JSON，你只需要写"收到这个请求时做什么"。

### 数据库、表、SQL

**数据库**：存数据的地方，程序关掉数据还在。

**表（table）**：数据库里的一张表格，有列（字段）和行（记录）。比如 `quotas` 表有 `tenant_id`、`limit_value`、`used` 这几列，每一行是一个客户的一种资源配额。

**SQL**：操作数据库的语言。你在 nOps 写过很多，四个基本动作：
`SELECT`（查）、`INSERT`（插入）、`UPDATE`（修改）、`DELETE`（删除）

**SQLite**：一种最简单的数据库，整个数据库就是一个文件，不需要单独安装服务。
**PostgreSQL**：一种功能完整的数据库，需要单独运行一个数据库服务，生产环境常用。

### 进程和线程

**进程（process）**：一个正在运行的程序。你启动一次 uvicorn，就是一个进程。每个进程有自己独立的内存，进程之间默认不共享数据。

**线程（thread）**：一个进程内部可以有多个线程，同时做几件事。同一个进程里的线程共享内存。

类比：进程是一家店，线程是店里的店员。多开几家店（多进程）互相独立；一家店多雇几个店员（多线程）可以同时服务几个客人，但共用一个仓库。

### 阻塞

**阻塞（blocking）**：一个操作要等结果回来才能继续往下走，等待期间什么都干不了。比如查数据库、发网络请求、`time.sleep(5)`。

类比：店员去仓库拿货，拿回来之前没法接待别的客人。

### 环境变量

**环境变量**：操作系统层面的"配置项"，程序启动时可以读取。比如设置 `DB_PATH=/tmp/test.db`，程序里用 `os.environ.get("DB_PATH")` 读到这个值。

**为什么用它**：同一份代码，在你电脑上和在服务器上连不同的数据库，只需要改环境变量，不用改代码。

### Git 和 GitHub

**Git**：版本管理工具，记录代码的每一次修改（每次叫一个 commit，提交）。
**GitHub**：存放 Git 仓库的网站。
**push**：把本地的提交上传到 GitHub。

### 部署

**部署（deploy）**：把你的程序放到一台公网能访问的服务器上跑起来，让别人能用。

**App Platform**：DigitalOcean 提供的部署服务。你给它 GitHub 仓库，它自动帮你装依赖、启动程序、分配一个网址。

---

## 第 1 节：45 分钟 Code Review 会怎么进行

**Code Review（代码评审）**：面试官和你一起看你写的代码，你讲解，他提问。

根据 DO 官方博客，这一轮分两段：

**前半段，大约 15 到 20 分钟**：你带面试官走一遍你写的东西，讲你的设计选择、取舍、以及如果时间更多会怎么改。

**后半段，大约 25 分钟**：面试官问假设性问题，比如"流量涨 10 倍怎么办""如果有一小时停机时间可以用，你会做什么"。

所以你只需要准备三样东西：
**一个 60 秒的开场介绍**
**每个关键决策的"为什么"和"代价"**
**一套回答扩展性问题的框架**（第 10 节）

### 60 秒开场模板

> "I built a quota service. The core flow is: set a limit, reserve, and release."

中文：我做了一个配额服务。核心流程是：设置上限、预留、释放。

> "I split it into three layers: routes in main.py, business logic in service.py, and storage in db.py."

中文：我把它分成三层：接口在 main.py，业务逻辑在 service.py，存储在 db.py。

> "The most important decision was making the limit check atomic inside the UPDATE statement."

中文：最重要的决定是把上限检查写进 UPDATE 语句里，让它成为原子操作（不会被并发打断）。

> "I deployed it on App Platform early, before writing business logic. After that, every feature went through the same loop: commit, deploy, verify."

中文：我在写业务逻辑之前就先部署到了 App Platform。之后每个功能都走同样的循环：提交、部署、验证。

> "The main limitations are that SQLite is ephemeral and the service is single-instance. I'm happy to talk about how I'd evolve it."

中文：主要的局限是 SQLite 的数据是临时的（重新部署会丢），而且服务只能单实例运行。我很乐意聊聊我会怎么改进它。

### 讲代码的顺序

**先讲数据模型（表结构），再讲请求流程，最后讲难点。**不要从第一行代码开始念。

> "Let me start with the data model, because everything else follows from it."

中文：我先从数据模型讲起，因为其他所有东西都是从它推出来的。

然后打开 `db.py` 讲表结构，再打开 `service.py` 讲核心函数，最后打开 `tests/` 展示你怎么验证的。

---

## 第 2 节：HTTP 基础

**HTTP**：浏览器和服务器之间通信的规则。所有 API 请求都用它。

### HTTP 方法

方法告诉服务器"你想做什么动作"：

| 方法 | 用途 | 幂等吗 | 例子 |
|---|---|---|---|
| GET | 读取 | 是 | 查询配额 |
| POST | 创建或触发动作 | **否** | 创建一个预留 |
| PUT | 整体设置 | 是 | 把上限设为 5 |
| PATCH | 改一部分 | 通常否 | 只改名字 |
| DELETE | 删除 | 是 | 释放预留 |

### 幂等（idempotent）是什么

**幂等**：同一个请求发一次和发十次，服务器最后的状态一模一样。

例子：
"把上限设为 5"（PUT）：发十次，上限还是 5。**幂等。**
"创建一个预留"（POST）：发十次，就创建了十个预留。**不幂等。**

**为什么重要**：网络不可靠，客户端发了请求没收到回复，不知道服务器处理了没有，就会重发。如果是 POST，重发就会重复创建。所以 POST 需要额外的**幂等键**（客户端给每个请求一个唯一编号，服务器看到重复编号就不再执行）。

> "PUT is idempotent by definition. Setting the limit to 5 twice still leaves it at 5."

中文：PUT 按定义就是幂等的。把上限设成 5，设两次还是 5。

> "POST isn't, so for reservations I added an Idempotency-Key header to make retries safe."

中文：POST 不是幂等的，所以我给预留接口加了一个 Idempotency-Key 请求头，让重试变得安全。

### 状态码

状态码是服务器返回的三位数字，告诉客户端结果如何。**第一位数字代表大类**：2 开头是成功，3 开头是跳转，4 开头是客户端的错，5 开头是服务器的错。

| 状态码 | 含义 | 什么时候用 |
|---|---|---|
| 200 OK | 成功 | 普通成功 |
| 201 Created | 创建成功 | POST 新建了东西 |
| 202 Accepted | 收到了，稍后处理 | 异步任务 |
| 204 No Content | 成功，没有返回内容 | 删除成功 |
| 307 Temporary Redirect | 临时跳转 | 短链接 |
| 400 Bad Request | 请求格式坏了 | JSON 写错了 |
| 401 Unauthorized | 没认证 | 没带密钥、签名错 |
| 403 Forbidden | 没权限 | 想访问别人的数据 |
| 404 Not Found | 不存在 | |
| 409 Conflict | 和当前状态冲突 | 配额满了 |
| 410 Gone | 以前有，现在永久没了 | 过期的短链接 |
| 422 Unprocessable Entity | 格式对，但内容不合法 | 数量填了负数 |
| 429 Too Many Requests | 请求太频繁 | 被限流 |
| 500 Internal Server Error | 服务器代码出 bug 了 | |
| 503 Service Unavailable | 服务暂时不可用 | |

**常被问的三组区分**：

**401 和 403**：401 是"我不知道你是谁"（没登录），403 是"我知道你是谁，但你没权限做这个"。

**400 和 422**：400 是请求本身坏了（比如 JSON 少了个括号），422 是格式没问题但内容不对（比如数量是 -1）。FastAPI 参数校验失败默认返回 422。

**409 和 429**：409 是和资源状态冲突（配额总量满了），429 是单位时间内请求次数太多（限流）。

### REST 风格的网址设计

**REST**：一种设计 API 网址的习惯。规则是：网址用名词表示"东西"，用 HTTP 方法表示"动作"。

```
GET    /tenants/acme/quotas              查看 acme 的所有配额
PUT    /tenants/acme/quotas/droplets     设置 acme 的服务器配额
POST   /tenants/acme/reservations        给 acme 创建一个预留
DELETE /reservations/abc123              释放编号 abc123 的预留
```

**例外**：像 `POST /tasks/123/retry`（重试任务）这种，本身就是一个"动作"，用动词也可以接受。

---

## 第 3 节：FastAPI 核心

### 最小的 FastAPI 程序

```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
```

逐行解释：
`from fastapi import FastAPI`：导入 FastAPI。
`app = FastAPI()`：创建一个应用对象，名字叫 `app`。
`@app.get("/health")`：这叫**装饰器**。意思是"下面这个函数负责处理 GET /health 这个请求"。
`def health():`：定义处理函数。
`return {"status": "ok"}`：返回一个字典，FastAPI 自动把它转成 JSON 发给客户端。

### 参数从哪里来

一个请求里的数据可能在四个地方：网址路径里、网址问号后面、请求头里、请求体里。FastAPI 根据你怎么写函数参数，自动判断从哪里取：

```python
@app.post("/tenants/{tenant_id}/reservations")
def reserve(
    tenant_id: str,             # 网址里有 {tenant_id}，所以从路径取
    body: ReservationIn,        # 类型是 Pydantic 模型，所以从请求体取
    dry_run: bool = False,      # 普通类型，从问号后面取：?dry_run=true
    idempotency_key: str | None = Header(default=None),   # 用 Header() 标注，从请求头取
): ...
```

**`tenant_id: str` 里的 `: str` 叫类型注解**，告诉 Python 这个参数应该是字符串。FastAPI 会用它来检查和转换数据。

### Pydantic：自动检查数据

**Pydantic** 是一个库，让你定义"数据应该长什么样"，然后自动检查。

```python
from pydantic import BaseModel, Field

class ReservationIn(BaseModel):
    resource: str = Field(min_length=1, max_length=64)
    amount: int = Field(gt=0, le=1_000_000)
```

意思是：请求体必须有 `resource`（字符串，长度 1 到 64）和 `amount`（整数，大于 0，小于等于一百万）。

如果客户端发了 `{"amount": -1}`，**FastAPI 在调用你的函数之前就拒绝了**，返回 422。所以你的函数里拿到的数据一定是合法的，不用自己再检查。

> "Validation happens at the boundary with Pydantic, so the service layer can assume its inputs are well-formed."

中文：数据校验在入口处用 Pydantic 完成，所以业务层可以默认拿到的输入都是合法的。

### response_model：控制返回哪些字段

```python
@app.get("/endpoints", response_model=list[EndpointOut])
```

`EndpointOut` 这个模型里没有 `secret`（密钥）字段。所以就算数据库里查出来的数据有密钥，FastAPI 也会把它过滤掉，不会返回给客户端。**这是一层安全保护。**

### 抛出错误

```python
from fastapi import HTTPException
raise HTTPException(status_code=404, detail="Not found")
```

`raise` 是 Python 里"抛出异常"的意思，程序会立刻停止当前函数。FastAPI 捕获到 `HTTPException` 后，会返回对应的状态码和错误信息给客户端。

**你的项目里的做法**：service.py 里抛出自己定义的异常（比如 `QuotaExceeded`），main.py 捕获它，再转换成 `HTTPException(409)`。

**为什么这么分**：业务逻辑不应该知道自己是被网页请求调用的。同一个函数可能被 API 调用，也可能被后台任务调用，也可能被测试直接调用。

> "The service layer raises domain exceptions and doesn't know about HTTP. The route layer maps them to status codes."

中文：业务层抛出的是业务异常，它不知道 HTTP 的存在。接口层负责把这些异常转换成状态码。

> "That way the same service function could be called from a background job or a test."

中文：这样同一个业务函数也可以被后台任务或测试调用。

### 依赖注入 Depends（被问"怎么加认证"时用）

**依赖注入**：把"很多接口都要做的事"抽成一个函数，让 FastAPI 在每次调用接口前自动执行。

```python
from fastapi import Depends

def get_current_user(api_key: str = Header()):
    user = lookup(api_key)          # 根据密钥查用户
    if not user:
        raise HTTPException(401)    # 查不到就返回 401
    return user

@app.get("/me")
def me(user = Depends(get_current_user)):   # 调用这个接口前，先执行 get_current_user
    return user
```

> "I'd add authentication as a FastAPI dependency. It reads the API key, looks up the caller, and raises 401 if it's invalid."

中文：我会把认证做成一个 FastAPI 依赖。它读取 API 密钥，查找调用者是谁，无效就返回 401。

> "Every route that needs auth declares it with Depends, and tenant_id would come from the authenticated identity rather than the URL."

中文：每个需要认证的接口都用 Depends 声明它。而且 tenant_id 应该从认证后的身份里取，而不是从网址里取（否则任何人改网址就能访问别人的数据）。

### lifespan：程序启动和关闭时做的事

```python
@asynccontextmanager
async def lifespan(app):
    init_db()     # 启动时执行：建数据库表
    yield         # 程序在这里正常运行
    # yield 后面的代码在程序关闭时执行，比如停掉后台线程

app = FastAPI(lifespan=lifespan)
```

### async def 和 def 的区别（高频问题，一定要看懂）

先理解两个概念：

**线程池（thread pool）**：提前准备好的一批线程，有活来了就派一个去干。

**事件循环（event loop）**：一个线程，像一个特别快的服务员，同时照看很多桌客人。某桌在等菜（等数据库、等网络）时，他就去服务别的桌，菜来了再回来。**但前提是每桌都要"主动告诉他我在等"，他才会去别处。**

现在看 FastAPI 的两种写法：

**写成 `def`（普通函数）**：FastAPI 把它交给线程池里的一个线程执行。函数里查数据库要等一会儿，只是这一个线程在等，别的线程照样处理别的请求。**安全。**

**写成 `async def`（异步函数）**：FastAPI 把它交给事件循环执行。如果函数里用了会阻塞的操作（比如 `sqlite3` 查询），这个操作不会"主动告诉服务员我在等"，服务员就只能干站着等它，**所有其他请求都卡住了**。只有用专门的异步库（比如 `asyncpg`）并写 `await`，才能正确地让出。

**你的项目用的是 `def`，因为 `sqlite3` 是阻塞的库。这是正确的选择。**

> "I used plain def for routes because sqlite3 is a blocking library."

中文：我的接口用的是普通的 def，因为 sqlite3 是阻塞式的库。

> "FastAPI runs def routes in a thread pool, so a slow query only occupies one thread."

中文：FastAPI 会把 def 接口放到线程池里运行，所以一个慢查询只会占用一个线程。

> "If I had used async def with a blocking call, it would stall the event loop and block every request."

中文：如果我用 async def 却在里面调用阻塞操作，就会卡住事件循环，导致所有请求都被堵住。

> "To go fully async, I'd switch to an async driver like asyncpg."

中文：如果要完全异步化，我会换成像 asyncpg 这样的异步数据库驱动。

### 自动文档 /docs

FastAPI 根据你写的类型注解，自动生成一个交互式的 API 说明页面。访问 `你的网址/docs` 就能看到，每个接口都能直接点按钮测试。**demo 时直接打开它给面试官看。**

### 中间件和 CORS（全栈相关）

**中间件（middleware）**：每个请求进来之前、出去之后都会执行的代码。比如记录每个请求的日志。

**跨域（cross-origin）**：前端网页在 `a.com`，调用 `b.com` 的 API，这叫跨域。**浏览器默认会拦截跨域请求**（为了安全），除非 `b.com` 明确说"我允许 a.com 访问"。

**CORS**：告诉浏览器"允许哪些网站访问我"的机制。

```python
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware, allow_origins=["https://my-frontend.com"])
```

> "If a browser frontend on a different domain calls this API, I'd add CORSMiddleware with an explicit list of allowed origins, not a wildcard."

中文：如果有一个在别的域名上的前端网页要调用这个 API，我会加上 CORS 中间件，并且明确列出允许的来源，而不是用通配符（*，允许所有网站）。

---

## 第 4 节：Uvicorn、进程、线程

### Uvicorn 是什么

**FastAPI 只负责"收到请求后怎么处理"，它自己不会去监听网络。**

**Uvicorn** 是一个**服务器程序**，负责在某个端口上等待请求、把请求交给 FastAPI、再把结果发回去。

类比：FastAPI 是厨师，Uvicorn 是前台接单的服务员。

```
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

逐个解释：
`app.main:app`：冒号前是文件路径（`app/main.py`，斜杠写成点），冒号后是那个文件里的变量名 `app`。
`--host 0.0.0.0`：接受任何地址来的请求。**部署时必须写**，默认的 127.0.0.1 只接受本机请求，外面访问不到。
`--port 8080`：在 8080 端口等待请求。
`--reload`：代码一改就自动重启，只在开发时用，**部署时不要加**。

**ASGI**：Python 里 web 服务器和框架之间约定的一种接口标准，支持异步。FastAPI 和 Uvicorn 都遵守它，所以能配合使用。（老标准叫 WSGI，不支持异步，Flask 传统上用这个。）

### 多进程

```
uvicorn app.main:app --workers 4
```

启动 4 个进程同时处理请求，能利用多核 CPU。

**注意**：每个进程的内存是独立的。你 webhook 项目里存在内存里的接收记录（`RECEIVED` 变量），4 个进程就有 4 份，互相看不到。

### GIL（可能被问）

**GIL（全局解释器锁）**：Python 的一个限制，同一个进程里，同一时刻只有一个线程在真正执行 Python 代码。

**影响**：
如果任务主要在"等"（等数据库、等网络），线程在等的时候会让出 GIL，别的线程能执行。所以**多线程对 web 服务很有效**。
如果任务主要在"算"（大量计算），多个线程也只能轮流执行，没有加速效果，**需要用多进程**。

> "Web requests are mostly I/O-bound, meaning they spend most of their time waiting on the database or network, so threads work well despite the GIL."

中文：web 请求大多是 I/O 密集型的，也就是大部分时间在等数据库或网络，所以尽管有 GIL，多线程依然很有效。

> "For CPU-heavy work, I'd use multiple processes or a separate worker."

中文：对于计算量大的工作，我会用多进程或者单独的 worker（后台工作进程）。

---

## 第 5 节：数据库（最容易被深挖）

### 事务（transaction）

**事务**：把几个数据库操作打包成一个整体，要么全部成功，要么全部撤销。

例子：预留配额时要做两件事：1. 把 used 加 1；2. 插入一条预留记录。如果第 1 步成功了第 2 步失败了，数据就不一致了。放在一个事务里，第 2 步失败时第 1 步也会被撤销。

**提交（commit）**：事务成功，改动正式生效。
**回滚（rollback）**：事务失败，撤销所有改动。

### ACID（事务的四个保证）

**A 原子性（Atomicity）**：要么全做，要么全不做。
**C 一致性（Consistency）**：事务前后数据都符合规则（比如"used 不能是负数"）。
**I 隔离性（Isolation）**：多个事务同时进行时，互相不干扰。
**D 持久性（Durability）**：提交后就算断电，数据也不会丢。

### 你项目里的事务写法

```python
with transaction(immediate=True) as conn:
    conn.execute("SELECT ...")
    conn.execute("UPDATE ...")
```

`with` 是 Python 的**上下文管理器**语法：进入时开始事务，正常离开时自动提交，出错时自动回滚。

`immediate=True` 对应 SQLite 的 `BEGIN IMMEDIATE`：事务一开始就锁住数据库，其他想写的事务要排队。

### rowcount 是什么

执行 UPDATE 或 DELETE 后，`cur.rowcount` 告诉你**实际改了几行**。你的配额服务用它判断条件更新是否成功：改了 1 行说明检查通过了，改了 0 行说明条件不满足（超限或者不存在）。

### 竞态条件（race condition）

**竞态条件**：两个操作同时进行，结果取决于谁先谁后，导致出错。

例子：配额上限 10，已用 9。两个请求同时来，都各要 1 个：
1. 请求 A 查询：used = 9，还有余量
2. 请求 B 查询：used = 9，还有余量（A 还没改）
3. 请求 A 写入：used = 10
4. 请求 B 写入：used = 11 ← **超限了**

这种"先查再改"的问题叫 **check-then-act**。

**解法就是你项目里的条件更新**：把检查写进 UPDATE 语句本身，数据库保证这一条语句执行时不会被打断。

### 隔离级别（知道大意就行）

数据库可以设置"事务之间隔离得多严格"。越严格越安全，但越慢。

| 级别 | 大意 |
|---|---|
| Read Uncommitted | 最松，能读到别人还没提交的数据 |
| **Read Committed**（PostgreSQL 默认） | 只能读到已提交的，但同一事务里两次读结果可能不同 |
| Repeatable Read | 同一事务里同一行读几次都一样 |
| Serializable | 最严，效果等同于一个一个排队执行 |

**关键点**：PostgreSQL 默认的 Read Committed 级别下，"先查再改"**依然会有竞态问题**。所以要么用条件更新（你的做法），要么用 `SELECT ... FOR UPDATE` 锁住那一行。

### 悲观锁和乐观锁

**悲观锁**：假设一定会冲突，所以先锁住再改。
```sql
SELECT * FROM quotas WHERE id = 1 FOR UPDATE
```
`FOR UPDATE` 的意思是"锁住这一行，我改完之前别人不能改"。

**乐观锁**：假设一般不会冲突，不加锁，改的时候检查一下有没有被别人改过。如果被改过就失败重试。

**你项目里的条件更新 `WHERE used + amount <= limit_value` 就是乐观的做法。**

> "My conditional update is a form of optimistic concurrency. There's no explicit lock; the write only succeeds if the condition still holds."

中文：我的条件更新是一种乐观并发控制。没有显式加锁，只有条件依然成立时写入才会成功。

> "The pessimistic alternative on PostgreSQL is SELECT FOR UPDATE, which locks the row until the transaction commits."

中文：在 PostgreSQL 上，悲观的做法是 SELECT FOR UPDATE，它会锁住那一行直到事务提交。

### SKIP LOCKED（任务队列必提）

```sql
SELECT * FROM tasks WHERE status = 'queued' LIMIT 1 FOR UPDATE SKIP LOCKED
```

多个 worker 同时抢任务时，`SKIP LOCKED` 的意思是"被别人锁住的行直接跳过，去拿下一个"，不用排队等。**这是用 PostgreSQL 做任务队列的标准写法。**

> "On PostgreSQL, I'd use SELECT FOR UPDATE SKIP LOCKED, so multiple workers can claim different tasks in parallel without blocking each other."

中文：在 PostgreSQL 上，我会用 SELECT FOR UPDATE SKIP LOCKED，这样多个 worker 可以并行地抢不同的任务，互不阻塞。

### 索引（index）

**索引**：类似书的目录。没有目录要一页一页翻，有目录直接跳到那一页。

没有索引时，数据库查询要一行一行扫描整张表（1 亿行就扫 1 亿次）。有索引时，能直接定位，速度快成千上万倍。

**复合索引**：用多个列一起建的索引，比如 `(resource_id, name, ts)`。

**最左前缀原则**：复合索引像电话簿，先按姓排、再按名排。你能快速找"姓张的"或"姓张名三的"，但没法快速找"名叫三的"（因为名字散落在各个姓里）。

所以索引 `(resource_id, name, ts)`：
能加速：`WHERE resource_id = ?`、`WHERE resource_id = ? AND name = ?`、三个都用
**不能加速**：`WHERE name = ?`、`WHERE ts > ?`（跳过了最左边的列）

**建索引的原则**：用"等于"条件的列放前面，用"大于小于"条件的列放最后。

**索引的代价**：每次插入数据都要同时更新索引，所以写入会变慢，也会占更多空间。

> "Indexes speed up reads but cost something on every write, so I only indexed the columns the hot queries filter on."

中文：索引能加快读取，但每次写入都有代价，所以我只给最常用的查询条件建了索引。

### N+1 查询问题

```python
events = 查询所有事件                    # 1 次数据库查询
for e in events:
    查询这个事件的投递记录               # 每个事件查 1 次，共 N 次
```

100 个事件就要查 101 次数据库，很慢。

**解决**：用 JOIN（把两张表连起来一次查）或者 `WHERE event_id IN (1, 2, 3, ...)` 一次查完。

你 webhook 项目里的投递函数用一个 JOIN 同时查出投递、事件、endpoint 信息，就是避免了 N+1。

### ORM 和原生 SQL

**ORM**：一种库（Python 里最常用的是 SQLAlchemy），让你用 Python 类和对象操作数据库，不用直接写 SQL。

**你的项目直接写 SQL**。

> "I used raw SQL because the core correctness guarantees, like the conditional UPDATE, are easier to see and explain in plain SQL."

中文：我直接写 SQL，因为核心的正确性保证（比如条件更新）用原生 SQL 更容易看清楚、也更容易解释。

> "For a larger codebase, I'd likely use SQLAlchemy for models and migrations, and use raw SQL only for the few critical queries."

中文：如果代码规模更大，我可能会用 SQLAlchemy 来管理模型和迁移，只在少数关键查询上用原生 SQL。

### 数据库迁移（migration）

**问题**：程序上线后，想给表加一列，怎么办？不能直接去生产数据库手动改（容易出错，没有记录，没法撤销）。

**迁移**：把每次表结构的修改写成一个脚本文件，带版本号，按顺序执行，可以回退。Python 里常用的工具叫 **Alembic**。

**你的项目用的是 `CREATE TABLE IF NOT EXISTS`**：只能在表不存在时创建，表已经存在就什么都不做，**没法修改已有的表**。

> "Right now the schema is created with CREATE TABLE IF NOT EXISTS, which can't change an existing table."

中文：目前表结构是用 CREATE TABLE IF NOT EXISTS 创建的，它没法修改已经存在的表。

> "In production, I'd use Alembic so every schema change is a versioned, reviewable migration."

中文：在生产环境我会用 Alembic，让每次表结构变更都是一个有版本号、可以审查的迁移脚本。

### 连接池（connection pool）

**问题**：每次查数据库都要先"建立连接"（像打电话要先拨号接通），PostgreSQL 建一次连接要几毫秒到几十毫秒，请求多了很慢。

**连接池**：提前建好一批连接放着，用的时候拿一个，用完放回去，不用每次重新拨号。

**你的项目每次都新建连接**，对 SQLite 没问题（它只是打开一个本地文件，很快），换 PostgreSQL 就必须用连接池。

### SQLite 和 PostgreSQL 对比

| | SQLite | PostgreSQL |
|---|---|---|
| 是什么 | 一个文件 | 一个独立运行的数据库服务 |
| 安装配置 | 不需要 | 需要 |
| 同时写入 | 整个数据库一把锁，一次只能一个写 | 可以锁单独一行，并发好 |
| 多个程序实例共享 | 不能 | 能 |
| 在 App Platform 上 | **每次重新部署数据就丢** | 用 DO 托管数据库，数据持久 |

---

## 第 6 节：测试

### 你项目里的测试怎么工作

```python
@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("DB_PATH", str(tmp_path / "test.db"))
    from app.main import app
    with TestClient(app) as c:
        yield c

def test_reserve_within_limit(client):
    client.put("/tenants/acme/quotas/droplets", json={"limit": 5})
    r = client.post("/tenants/acme/reservations", json={"resource": "droplets", "amount": 3})
    assert r.status_code == 201
```

逐个解释：

**pytest**：Python 最常用的测试工具。运行 `pytest` 命令，它会自动找到所有 `test_` 开头的函数并执行。

**fixture**：测试的"准备工作"。上面的 `client` 就是一个 fixture，每个测试函数参数里写了 `client`，pytest 就会先执行 fixture 准备好，再把结果传进去。

**tmp_path**：pytest 自带的 fixture，给每个测试一个全新的临时文件夹，测试完自动删除。

**monkeypatch**：pytest 自带的 fixture，可以临时修改环境变量或者替换函数，测试结束自动恢复原样。

上面这段的效果是：**每个测试都用一个全新的空数据库**，测试之间完全不互相影响。

**TestClient**：模拟发 HTTP 请求，但不用真的启动服务器，直接在内存里调用。

**assert**：断言。`assert r.status_code == 201` 意思是"我断定状态码是 201，如果不是，这个测试就失败"。

### 测试的类型

**单元测试**：只测一个小函数。比如测 `backoff_seconds(3)` 的返回值在合理范围内。
**集成测试**：测多个部分一起工作。比如通过接口创建预留，再查配额，看数字对不对。你的大部分测试是这种。
**端到端测试**：模拟真实用户，测完整流程，包括真实部署的服务。

### Mock（替身）

测试 webhook 时不能真的往外发请求（慢、不稳定、可能打扰别人）。所以写一个假的发送函数 `FakeSender` 替换真的，而且能控制它返回什么状态码（比如先返回 503 再返回 200），用来测重试逻辑。

**这个假的替代品就叫 mock。**能替换是因为代码设计时把"发送函数"做成了可以从外面传进来的参数，这叫**依赖注入**。

> "The HTTP sender is injectable, so tests use a fake that returns scripted status codes."

中文：HTTP 发送函数是可以注入替换的，所以测试里用了一个假的，它会按预先编好的顺序返回状态码。

> "That lets me test retry and dead-letter paths deterministically, without touching the network."

中文：这让我可以确定性地（每次结果都一样）测试重试和死信的路径，完全不需要真的联网。

### 应该优先测什么

**优先测"最不能出错的规则"和"失败的情况"**，而不是只测一切正常的情况。

> "I prioritized tests for the core invariant and the failure paths. A happy-path test would pass even if the concurrency logic were broken."

中文：我优先测试了核心不变量（永远必须成立的规则，比如"用量不超过上限"）和失败路径。只测正常流程的话，就算并发逻辑有 bug 测试也照样会通过。

---

## 第 7 节：配置、密钥、日志

### 12-Factor App

**12-Factor App**：一套构建云上应用的 12 条原则。面试最常涉及三条：

**第一条：配置放在环境变量里。**数据库地址、密钥不写死在代码里。你项目里的 `DB_PATH`、`BASE_URL` 就是这样。

**第二条：进程无状态（stateless）。**程序本身不在自己的硬盘上保存需要长期保留的数据，数据都放在外部数据库里。这样任何一个实例挂了、重启了、多开几个，都没关系。

**你的项目违反了这一条**，因为 SQLite 文件存在程序本地。这就是为什么不能多开实例、重新部署会丢数据。

**第三条：日志直接打印到标准输出（stdout）。**stdout 就是程序 `print` 出来的地方。程序只管打印，平台负责收集。App Platform 的 Runtime Logs 收集的就是这个。

### 密钥管理

**绝对不要把密钥写进代码提交到 Git。**一旦提交，就算后来删掉，Git 历史里还能找到。

**正确做法**：
本地开发时放在 `.env` 文件里，并把 `.env` 写进 `.gitignore`（告诉 Git 忽略这个文件）。
提供一个 `.env.example` 文件，只写变量名不写真实值，告诉别人需要配置哪些。
部署时在 App Platform 的环境变量设置里配置，类型选 **Secret**（会加密存储，日志里也不会显示）。

> "Secrets come from environment variables, never the repository. On App Platform, they're stored as encrypted secret variables."

中文：密钥从环境变量读取，永远不放进代码仓库。在 App Platform 上，它们以加密的 Secret 类型变量存储。

---

## 第 8 节：Docker 容器化（重点看）

### 容器要解决什么问题

最常见的情况："在我电脑上能跑，放到服务器上就跑不了。"原因通常是 Python 版本不一样、少装了某个系统库、依赖包版本不一样。

**容器**：把你的程序和它运行需要的**整个环境**（特定版本的 Python、所有依赖包、系统库）打包在一起。在哪台机器上跑都一模一样。

类比：搬家时不是只搬家具，而是把整个房间连墙带地板一起打包运走，到了新地方原样放下。

### 容器和虚拟机的区别

**虚拟机**：在一台电脑里模拟出另一台完整的电脑，包括一个完整的操作系统。很重，启动要几分钟。

**容器**：不模拟整台电脑，共用宿主机的操作系统核心，只把程序和它的文件隔离开。很轻，启动只要几秒。

### 两个核心概念

**镜像（image）**：一个打包好的、只读的模板，里面有代码、依赖、运行环境。类比：安装光盘，或者菜谱。

**容器（container）**：镜像运行起来的实例。类比：用光盘装好、正在运行的系统，或者按菜谱做出来的那道菜。

一个镜像可以同时运行出多个容器。

**Dockerfile**：一个文本文件，写着"怎么一步步制作这个镜像"的指令。

### 一份标准的 FastAPI Dockerfile，逐行解释

```dockerfile
FROM python:3.12-slim
```
**从一个现成的镜像开始**。`python:3.12-slim` 是官方提供的、装好了 Python 3.12 的精简版 Linux 系统。`slim` 表示精简版，体积小（大约 50MB，完整版大约 400MB），不必要的东西少，也更安全。

```dockerfile
WORKDIR /app
```
**设置工作目录**。后面所有命令都在容器里的 `/app` 文件夹里执行。相当于 `cd /app`。

```dockerfile
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
```
**设置环境变量**。
第一个：不生成 `.pyc` 文件（Python 的缓存文件，容器里没用）。
第二个：**让 print 的内容立刻输出**。默认 Python 会先攒一批再输出，导致日志延迟很久才出现，排查问题时很痛苦。

```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```
**先只复制依赖清单文件，然后安装依赖**。`COPY` 是把你电脑上的文件复制进镜像，`RUN` 是在镜像里执行命令。`--no-cache-dir` 是安装完不保留下载的安装包，让镜像更小。

**为什么要先单独复制 requirements.txt，下面专门讲。**

```dockerfile
COPY . .
```
**再复制全部代码**。第一个点是你电脑上的当前目录，第二个点是镜像里的当前目录（`/app`）。

```dockerfile
RUN useradd --create-home appuser
USER appuser
```
**创建一个普通用户并切换过去**。容器默认用 root（最高权限的管理员）运行，万一程序被黑客攻破，他就拿到了最高权限。用普通用户更安全。

```dockerfile
EXPOSE 8080
```
**声明程序会用 8080 端口**。这一行只是说明作用，真正让外面能访问要靠运行时的 `-p` 参数。

```dockerfile
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```
**容器启动时执行的命令**。用方括号数组的写法（叫 exec form），这样 uvicorn 直接成为容器的主进程，平台要停止容器时，uvicorn 能收到停止信号（SIGTERM），处理完手上的请求再退出。

### 层缓存：为什么要先复制 requirements.txt

**Dockerfile 的每一行指令会生成一"层"，Docker 会把每一层缓存起来。**下次构建时，如果某一层的内容没变，就直接用缓存，不用重新执行。

**但是**：某一层变了，**它和它后面的所有层都要重新执行**。

**如果写成这样：**
```dockerfile
COPY . .                              # 复制全部代码
RUN pip install -r requirements.txt   # 安装依赖
```
你改了一行业务代码，`COPY . .` 这一层就变了，后面的 `pip install` 也要重新跑，每次都要等几分钟装依赖。

**正确写法：**先复制 requirements.txt 并安装，再复制代码。依赖没变时，安装那一层直接用缓存，改代码只重新执行最后的 `COPY . .`，几秒钟就好。

> "I copy requirements.txt and install dependencies before copying the source code, so code changes don't invalidate the dependency layer."

中文：我先复制 requirements.txt 并安装依赖，再复制源代码，这样改代码时不会让依赖那一层的缓存失效。

> "Rebuilds take seconds instead of minutes."

中文：重新构建只需要几秒，而不是几分钟。

### .dockerignore

和 `.gitignore` 类似，告诉 Docker 复制文件时跳过哪些：

```
__pycache__
*.pyc
.git
.env
*.db
.pytest_cache
venv
```

**`.env` 一定要写进去**，否则你的密钥会被打包进镜像里。

### 常用命令（知道意思就行）

```bash
docker build -t quota-service .
```
根据当前目录的 Dockerfile 构建镜像，`-t` 给镜像起名叫 quota-service，最后的点表示当前目录。

```bash
docker run -p 8080:8080 quota-service
```
运行镜像，启动一个容器。`-p 8080:8080` 是**端口映射**：前面是你电脑的端口，后面是容器里的端口。容器有自己独立的网络，不做映射的话，你电脑上访问不到容器里的程序。

```bash
docker run -p 8080:8080 -e DB_PATH=/data/q.db quota-service
```
`-e` 给容器传环境变量。

```bash
docker run -v $(pwd)/data:/data quota-service
```
`-v` 是**挂载卷**：把你电脑上的一个文件夹接到容器里。**容器删掉后，容器内部的文件都会消失；但挂载进去的文件夹是在你电脑上的，数据会保留。**

```bash
docker ps                       # 查看正在运行的容器
docker logs <容器ID>             # 查看容器的日志
docker exec -it <容器ID> sh      # 进入容器内部，像登录一台机器一样排查问题
```

**重要联系**：容器文件系统是临时的，这和"App Platform 上 SQLite 重新部署就丢数据"是**同一个原因**。

### 多阶段构建（知道概念即可）

```dockerfile
FROM python:3.12 AS builder          # 第一阶段：用完整版镜像，里面有编译工具
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.12-slim                # 第二阶段：用精简版镜像
COPY --from=builder /root/.local /root/.local   # 只把第一阶段装好的包拷过来
COPY . .
```

有些依赖包安装时需要编译，要用到编译器。第一阶段用带编译器的完整镜像装好，第二阶段只把结果拷到精简镜像里。**最终镜像里没有编译器，更小更安全。**

### Docker Compose：同时启动多个容器

如果你的程序需要 PostgreSQL 数据库，本地开发时要同时跑两个容器。Compose 用一个配置文件一次启动全部：

```yaml
services:
  api:                           # 第一个服务：你的程序
    build: .                     # 用当前目录的 Dockerfile 构建
    ports: ["8080:8080"]
    environment:
      DATABASE_URL: postgresql://app:secret@db:5432/app
    depends_on: [db]             # 先启动 db 再启动 api
  db:                            # 第二个服务：数据库
    image: postgres:16           # 直接用官方的 PostgreSQL 镜像
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: app
    volumes: ["pgdata:/var/lib/postgresql/data"]   # 数据库文件存在卷里，不会丢
volumes:
  pgdata:
```

运行 `docker compose up`，两个都起来了。注意 api 连接数据库时，地址写的是 `db`（服务名），Compose 会自动让它们互相找得到。

### 为什么你这次没用 Docker（被问时这么答）

> "App Platform's Python buildpack detected the project from requirements.txt and built it automatically."

中文：App Platform 的 Python buildpack（自动构建工具）通过 requirements.txt 识别出这是一个 Python 项目，自动完成了构建。

> "So under a three-hour limit, I avoided writing and debugging a Dockerfile."

中文：所以在三小时的限制下，我省掉了编写和调试 Dockerfile 的时间。

> "For production, I'd containerize it for reproducibility: a slim Python base image, dependencies installed in their own layer for caching, a non-root user, and uvicorn as the exec-form entrypoint so it handles shutdown signals correctly."

中文：在生产环境，我会把它容器化以保证可复现性（在哪里跑结果都一样）：用精简版 Python 基础镜像、把依赖安装单独放一层以利用缓存、用非 root 用户运行、并用 exec 形式启动 uvicorn，让它能正确处理关闭信号。

**这段回答本身就证明了你懂 Docker**，面试官不需要你现场写 Dockerfile。

### Kubernetes（一段话就够）

**Kubernetes（简称 K8s）**：当你有很多个容器，要跑在很多台机器上时，需要一个"总调度"。K8s 负责：决定每个容器放在哪台机器上跑、容器挂了自动重启、流量大了自动多开几个、更新版本时逐个替换不停机。

DO 的托管 Kubernetes 产品叫 **DOKS**。

> "For a single service, App Platform is simpler. I'd move to Kubernetes when there are many services that need fine-grained control over scaling and networking."

中文：对于单个服务，App Platform 更简单。当有很多个服务、需要精细控制扩容和网络时，我才会迁移到 Kubernetes。

---

## 第 9 节：部署与 DigitalOcean 产品

### App Platform 是什么

**PaaS（平台即服务）**：你只管写代码，服务器、网络、HTTPS 证书、负载均衡这些都由平台负责。App Platform 就是 DO 的 PaaS。

**App Platform 里的组件类型**：
**Service**：对外提供网址访问的服务，你的 API 就是这种。
**Worker**：后台运行的程序，不对外提供网址。任务队列的处理程序应该用这种。
**Job**：执行一次就结束的任务，比如数据库迁移、每天定时清理数据。
**Static Site**：纯前端的静态网页。

### DO 主要产品（知道名字和用途）

你在 nOps 用过 AWS，可以用这张表对应：

| DO 产品 | 是什么 | 对应 AWS |
|---|---|---|
| Droplets | 虚拟机（一台云上的电脑） | EC2 |
| App Platform | 自动部署平台 | App Runner / Elastic Beanstalk |
| Managed Databases | 托管数据库（PostgreSQL、MySQL、Redis 等） | RDS |
| Spaces | 对象存储（存文件、图片） | S3 |
| Volumes | 块存储（给虚拟机加硬盘） | EBS |
| Load Balancers | 负载均衡器 | ELB |
| DOKS | 托管 Kubernetes | EKS |
| Functions | 无服务器函数 | Lambda |

### 部署相关的关键概念

**负载均衡器（load balancer）**：放在多个程序实例前面，把进来的请求分配给不同的实例。类比：银行门口的叫号机，把客人分到不同窗口。

**健康检查（health check）**：平台定期访问你的 `/health` 接口，如果连续失败，就认为这个实例坏了，自动重启它或者不再给它分请求。

**垂直扩展（scale up）**：换一台更强的机器（更多 CPU、更多内存）。简单，但有上限。

**水平扩展（scale out）**：多开几个实例一起干活。理论上可以无限扩展，**但要求程序是无状态的**（数据不存在程序本地）。

**滚动部署（rolling deploy）**：发布新版本时，一个一个替换旧实例，始终有实例在工作，用户感觉不到中断。App Platform 默认就是这样。

**回滚（rollback）**：新版本有问题，一键切回上一个能用的版本。

**优雅关闭（graceful shutdown）**：平台要停掉一个实例时，先发一个信号（叫 SIGTERM）通知它。程序收到后停止接收新请求，把手上正在处理的做完，再退出。你任务队列项目里关闭时停止后台线程，就是这个思路。

### CI/CD

**CI（持续集成，Continuous Integration）**：每次提交代码，自动运行测试。
**CD（持续部署，Continuous Deployment）**：测试通过后，自动部署上线。

**你用的 App Platform autodeploy 只做了 CD**：每次 push 就部署，不管测试有没有通过。

**加上 CI 最简单的方法是 GitHub Actions**（GitHub 自带的自动化工具）。在仓库里建一个文件 `.github/workflows/test.yml`：

```yaml
name: tests
on: [push, pull_request]          # 每次 push 或者提 PR 时触发
jobs:
  test:
    runs-on: ubuntu-latest        # 在一台 Ubuntu 虚拟机上运行
    steps:
      - uses: actions/checkout@v4          # 拉取代码
      - uses: actions/setup-python@v5      # 安装 Python
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt   # 装依赖
      - run: pytest -v                         # 跑测试
```

> "Right now, App Platform deploys on every push to main."

中文：目前 App Platform 在每次推送到 main 分支时都会部署。

> "I'd add a GitHub Actions workflow that runs pytest on every push and pull request, and protect main so only passing builds can be merged. That way a failing test blocks the deploy."

中文：我会加一个 GitHub Actions 工作流，在每次推送和提 PR 时跑 pytest，并且保护 main 分支，只有测试通过的代码才能合并进去。这样测试失败就会阻止部署。

**如果现场时间富余，加这个文件是性价比很高的加分项，五分钟就能搞定。**

---

## 第 10 节：扩展性万能回答框架（后半段追问的核心）

面试官几乎一定会问："如果流量涨 10 倍（或 100 倍），你会怎么办？"

**按下面六步的顺序回答，永远不会没话说。**

### 第一步：先说出第一个会出问题的地方（瓶颈）

**瓶颈（bottleneck）**：整个系统里最先扛不住的那个部分。

> "The first thing that breaks is the SQLite file and the single instance."

中文：最先扛不住的是 SQLite 文件和单实例部署。

**你的五个项目，第一个瓶颈几乎都是这个。**

### 第二步：让程序无状态，然后多开实例

> "I'd move state out of the process into a shared database, Managed PostgreSQL."

中文：我会把数据从程序本地移到一个共享的数据库里，也就是 DO 的托管 PostgreSQL。

> "Once the app is stateless, I can run multiple instances behind a load balancer and scale horizontally."

中文：程序变成无状态之后，我就可以在负载均衡器后面运行多个实例，进行水平扩展。

### 第三步：数据库层

**读多写少时**：加**只读副本（read replica）**。主数据库负责写，复制出几个副本专门负责读，读请求分散到副本上。

**某些数据被读得特别频繁时**：加**缓存**（最常用的是 Redis，一个把数据存在内存里的超快数据库）。

**写入实在太多时**：**分片（sharding）**，比如按客户 ID 把数据分散到几个不同的数据库。这是最后的手段，因为复杂度很高。

### 第四步：把慢的、不紧急的工作移出请求流程

**消息队列（message queue）**：一个中间的"待办箱"。请求处理时只把任务扔进去就马上返回，后台的 worker 慢慢从箱子里取出来处理。

> "Anything not needed for the response, like recording analytics or sending notifications, goes onto a queue and is processed by separate workers."

中文：任何不是返回响应所必需的工作，比如记录统计数据、发送通知，都放进队列，由单独的 worker 处理。

短链的点击记录、webhook 投递都属于这类。

### 第五步：保护系统

**限流（rate limiting）**：限制每个客户单位时间内的请求次数，防止一个客户把系统打垮。

**超时（timeout）**：调用别的服务时必须设最长等待时间，不能无限期等下去。

**熔断（circuit breaker）**：某个下游服务一直失败时，暂时停止调用它，过一会儿再试。你在 nOps 做过。

**背压（backpressure）**：队列满了就拒绝新请求，而不是无限堆积直到内存爆掉。

### 第六步：可观测性（observability）

**可观测性**：能看清楚系统内部在发生什么。

> "Before scaling, I'd want visibility: structured logs with a request ID, metrics on request rate, error rate, and latency, and alerts on those."

中文：在扩容之前，我需要先能看清楚系统：带请求 ID 的结构化日志，关于请求速率、错误率和延迟的指标，以及基于这些指标的告警。

> "You can't fix a bottleneck you can't see."

中文：看不见的瓶颈是没法修的。

**名词解释**：
**结构化日志**：日志输出成 JSON 格式而不是随便一句话，方便搜索和统计。每条带一个 request_id（请求编号），能把同一个请求的所有日志串起来。
**延迟（latency）**：一个请求从发出到收到响应花了多长时间。
**p95、p99**：把所有请求的延迟从小到大排，第 95%、第 99% 位置的值。比如 p99 = 500 毫秒，意思是 99% 的请求都在 500 毫秒内完成。比平均值更能反映"慢请求"的情况。
**RED 指标**：Rate（请求速率）、Errors（错误率）、Duration（耗时），监控服务最基本的三个指标。

### 缓存专题（常被单独追问）

**Cache-aside 模式**（最常用的缓存用法）：
1. 先去缓存里找，找到了直接返回
2. 没找到就去数据库查，查到后放进缓存，再返回
3. 数据更新时，**删除**缓存里对应的数据（下次读时会重新从数据库加载）

**缓存最大的难题：数据不一致**。数据库里的数据改了，缓存里还是旧的，用户就读到了过期数据。
**TTL（Time To Live，存活时间）**：给缓存里的每条数据设一个过期时间，到期自动删除。就算忘了删缓存，最多也只会旧这么长时间。

> "For the URL shortener, I'd cache the code-to-URL mapping in Redis using cache-aside."

中文：对于短链服务，我会用 cache-aside 模式把"短码到原网址"的对应关系缓存在 Redis 里。

> "Links rarely change, so the hit rate would be very high. On delete, I'd invalidate the key, and a TTL limits how stale an entry can get if an invalidation is missed."

中文：链接很少改变，所以缓存命中率会非常高。删除链接时我会让缓存里对应的数据失效，而 TTL 能保证就算漏删了，数据最多也只会过期一段时间。

### "有停机窗口"类问题

DO 博客专门提到这个方向。例子："你要把 SQLite 迁移到 PostgreSQL，有一个小时的停机时间可以用，怎么做？"

**停机窗口（downtime window）**：允许服务暂停对外提供服务的一段时间。

**有停机窗口时**（简单可靠）：
停止写入 → 导出旧数据 → 导入新数据库 → 核对行数和关键数据 → 修改程序的数据库连接配置 → 重新启动 → 验证功能

**没有停机窗口时**（更难，说出思路就加分）：**双写**。程序同时往新旧两个数据库写入，后台把历史数据慢慢迁移过去，确认两边一致后，把读取切换到新库，最后停掉对旧库的写入。

> "With a downtime window, I'd do it offline: stop writes, export, import, verify row counts and a sample of records, switch the connection string, and bring it back up."

中文：如果有停机窗口，我会离线完成迁移：停止写入、导出、导入、核对行数并抽查部分记录、切换数据库连接地址、再重新启动服务。

> "Without one, I'd dual-write to both databases, backfill the history in the background, verify they match, switch reads over, then retire the old one."

中文：如果没有停机窗口，我会同时写入两个数据库，在后台回填历史数据，验证两边一致后把读取切换过去，最后下线旧数据库。

---

## 第 11 节：全栈基础（万一题目要求有网页界面）

### 前后端怎么配合

前端（浏览器里运行的 JavaScript）用 `fetch()` 函数发 HTTP 请求给后端 API，后端返回 JSON，前端把数据显示在页面上。

### 最快的做法：让 FastAPI 直接返回一个网页

```python
from fastapi.responses import HTMLResponse

@app.get("/ui", response_class=HTMLResponse)
def ui():
    return """
    <html><body>
      <input id="url" placeholder="Long URL">
      <button onclick="shorten()">Shorten</button>
      <p id="out"></p>
      <script>
        async function shorten() {
          const r = await fetch('/links', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({url: document.getElementById('url').value})
          });
          const data = await r.json();
          document.getElementById('out').textContent =
            r.ok ? data.short_url : JSON.stringify(data.detail);
        }
      </script>
    </body></html>
    """
```

**这段代码在做什么**：访问 `/ui` 会返回一个网页，上面有一个输入框和一个按钮。点按钮时，JavaScript 把输入框里的网址用 POST 发给 `/links` 接口，拿到结果后显示在页面上。

**好处**：网页和 API 在同一个网址下，所以**没有跨域问题**，不用配 CORS。三小时里如果要求有界面，这是最快的做法。

**注意**：这个 `/ui` 路由在短链项目里也要放在最后那个 `/{code}` 路由**前面**。

> "I served a minimal HTML page from the same app, so there's no separate frontend deployment and no CORS configuration."

中文：我在同一个程序里直接返回一个简单的 HTML 页面，所以不需要单独部署前端，也不需要配置 CORS。

> "For a real product, I'd build the frontend separately and deploy it as a static site."

中文：如果是真正的产品，我会单独开发前端，并把它部署成一个静态网站。

### 认证的几种方式（被问"怎么加登录"）

**认证（authentication）**：确认"你是谁"。
**授权（authorization）**：确认"你能做什么"。

三种常见方式：

**API Key（API 密钥）**：客户端在请求头里带一个密钥字符串，服务端查数据库看这个密钥属于谁。简单，适合程序调用程序。

**Session + Cookie（会话和 Cookie）**：用户登录后，服务器在自己这边记下"这个用户登录了"，并给浏览器一个编号（存在 Cookie 里）。浏览器之后每次请求自动带上这个编号。传统网站常用。

**JWT（JSON Web Token）**：用户登录后，服务器生成一个带签名的令牌，里面直接写着用户信息。之后客户端每次带着这个令牌，服务器只要验证签名是真的就行，**不用在自己这边记录任何东西**。适合无状态的 API。

---

## 第 12 节：安全基础

### SQL 注入

**SQL 注入**：攻击者在输入里夹带 SQL 代码，让你的程序执行了他想执行的查询。

```python
# 错误写法：把用户输入直接拼进 SQL 字符串
conn.execute(f"SELECT * FROM links WHERE code = '{code}'")
# 如果攻击者输入 code = x' OR '1'='1
# 实际执行的 SQL 变成：SELECT * FROM links WHERE code = 'x' OR '1'='1'
# '1'='1' 永远成立，于是查出了所有数据

# 正确写法：用 ? 占位符，把用户输入作为参数单独传
conn.execute("SELECT * FROM links WHERE code = ?", (code,))
```

用 `?` 占位时，数据库会把传进来的值**当作纯数据**处理，永远不会当作 SQL 代码执行。**这叫参数化查询。**

**你的项目全部用了 `?` 参数化查询。**

> "Every query uses parameter placeholders, never string formatting, so user input can't change the structure of the query."

中文：每个查询都使用参数占位符，从不用字符串拼接，所以用户的输入没法改变查询的结构。

**唯一的例外**：告警项目里，聚合函数名（avg、max 这些）是用 f-string 拼进 SQL 的。但它来自一个固定的白名单字典，而且用户输入先经过了 `Literal["avg", "max", ...]` 校验，只能是那几个固定值，所以是安全的。**被问到时能说出这一点更好。**

### 其他要点

**输入校验**：在入口处用 Pydantic 检查格式、长度、范围，防止超大或恶意输入。
**HTTPS**：加密传输，App Platform 自动提供。
**最小权限**：容器用普通用户运行，数据库账号只给它需要的权限。
**不泄露内部信息**：错误信息里不要返回代码的报错堆栈；用 response_model 防止返回敏感字段。
**常量时间比较**：比较签名或密钥时用 `hmac.compare_digest`，不用 `==`，防止攻击者通过测量响应时间来猜密钥（webhook 项目里讲过）。

---

## 第 13 节：被问"你怎么用 AI 的"（DO 一定会问）

这是 DO 面试的核心评估点。**回答的关键：AI 负责产出代码，你负责判断和验证。**

**回答的四个部分**：
1. AI 帮你做了什么（搭项目结构、写重复性的样板代码）
2. 你自己把关了什么（核心的正确性逻辑）
3. 你怎么验证的（写测试）
4. 一个你发现 AI 出错的具体例子

> "I used AI to scaffold the project structure, routes, and Pydantic models. That's boilerplate, where speed matters more than judgment."

中文：我用 AI 搭建了项目结构、接口和 Pydantic 模型。这些是样板代码，速度比判断力更重要。

> "The correctness-critical parts, like the atomic check or the route ordering, I reviewed line by line."

中文：对正确性至关重要的部分，比如原子检查、路由顺序，我逐行审查过。

> "And I wrote tests that target exactly those guarantees, rather than trusting that the code looked right."

中文：而且我专门针对这些保证写了测试，而不是因为代码看起来对就相信它。

> "One concrete case: the generated code put the catch-all route before /health, and my test caught it."

中文：一个具体的例子：AI 生成的代码把那个匹配所有路径的路由放在了 /health 前面，我的测试发现了这个问题。

（这个例子要换成你现场真实遇到的情况。）

**千万不要说**："都是 AI 写的，我没太看。"也不要假装"全是我自己手写的"。

---

## 第 14 节：自测题（面试前过一遍）

每题能用一两句话答出来就行。

**1. FastAPI 里 async def 和 def 有什么区别？**
def 放在线程池里运行，里面可以做阻塞操作；async def 在事件循环上运行，里面做阻塞操作会卡住所有请求。

**2. 为什么 uvicorn 启动时要加 `--host 0.0.0.0`？**
默认只监听 127.0.0.1，只接受本机请求，部署后外面访问不到。

**3. 你的服务能直接开 3 个实例吗？**
不能。每个实例有自己的 SQLite 文件，数据不共享。要先把数据库换成共享的 PostgreSQL。

**4. 两个请求同时预留最后一个配额，会发生什么？**
条件更新保证只有一个成功，另一个 rowcount 是 0，返回 409。

**5. 为什么"先查询再更新"是错的？**
两个请求可能同时查到同样的旧值，都通过检查，都写入，结果超限。

**6. 401 和 403 有什么区别？**
401 是不知道你是谁，403 是知道你是谁但不让你做。

**7. POST 请求为什么需要幂等键？**
POST 本身不幂等，客户端超时后重试会导致重复创建。

**8. Dockerfile 为什么要先复制 requirements.txt？**
利用层缓存。改代码时依赖那一层不变，不用重新安装依赖。

**9. 镜像和容器有什么区别？**
镜像是只读的模板，容器是镜像运行起来的实例。

**10. 容器里的数据为什么会丢？**
容器的文件系统是临时的，要保留数据需要挂载卷或者用外部数据库。

**11. 复合索引 (a, b, c) 能加速 `WHERE b = ?` 吗？**
不能。最左前缀原则，必须从 a 开始用。

**12. 什么是 N+1 查询？**
先查 1 次拿到列表，再对每一项各查 1 次，总共 N+1 次。用 JOIN 或 IN 一次查完。

**13. 数据库迁移用什么工具？为什么需要？**
Alembic。表结构的修改要有版本记录、能审查、能回退，不能手动改生产数据库。

**14. 为什么密钥不能写在代码里？**
会进入 Git 历史，任何能看到仓库的人都能拿到，就算删了历史里也还在。

**15. CI 和 CD 有什么区别？你的项目有吗？**
CI 是自动跑测试，CD 是自动部署。App Platform 的自动部署是 CD，没有 CI。加一个 GitHub Actions 跑 pytest 就有了。

**16. 流量涨 100 倍，第一个撑不住的是什么？**
SQLite 和单实例。先换 PostgreSQL 让程序无状态，再水平扩展；频繁读的数据加缓存；不紧急的写入移到队列。

**17. 数据库改了，缓存里的旧数据怎么办？**
更新数据库后删除缓存里的对应数据，再加 TTL 兜底。

**18. 什么是"至少一次"投递？为什么不做"恰好一次"？**
保证至少执行一次，但可能重复。"执行"和"记录已执行"是两个步骤，中间崩溃就没法知道到底执行了没有，所以"恰好一次"基本做不到，要靠处理逻辑本身幂等来弥补。

**19. 怎么防 SQL 注入？**
用参数化查询（? 占位符），永远不把用户输入拼接进 SQL 字符串。

**20. 怎么给 API 加认证？**
写一个 FastAPI 依赖函数，读取 API 密钥或 JWT，验证失败返回 401，需要认证的接口用 Depends 声明。

**21. Python 的 GIL 对你的服务有影响吗？**
影响不大。web 请求大部分时间在等待数据库和网络，等待时会释放 GIL。只有计算量大的任务才需要多进程。

**22. 有一小时停机窗口，怎么把 SQLite 迁移到 PostgreSQL？**
停止写入 → 导出 → 导入 → 核对 → 切换连接地址 → 启动并验证。

**23. 健康检查是干什么的？**
平台定期访问 /health，失败就重启实例或者不再给它分配请求。

**24. 什么是滚动部署？**
新版本实例一个一个替换旧实例，始终有实例在工作，用户感觉不到中断。

**25. 你为什么选 SQLite？**
零配置，三小时里能专注在业务逻辑上。代价是数据不持久、不能多实例。生产环境会换托管 PostgreSQL，数据库操作都集中在 db.py 里，迁移主要就是换连接层。

---

## 第 15 节：卡住时的救命句式

**没听懂问题时**：

> "Sorry, could you rephrase that?"

中文：抱歉，您能换个说法再问一遍吗？

> "Just to make sure I understand, are you asking about X?"

中文：我确认一下我理解得对不对，您是在问关于 X 的问题吗？

**需要想一下时**：

> "Let me think about that for a moment."

中文：让我想一下。

（停顿三秒完全正常，比乱说好一百倍。）

**不知道答案时**：

> "I haven't worked with that directly, but my understanding is X. I'd want to verify that before relying on it."

中文：我没有直接用过这个，但我的理解是 X。在真正依赖它之前我会先去验证一下。

> "I'm not sure, but here's how I'd reason about it."

中文：我不太确定，但我会这样来推理。

**被指出问题时**：

> "That's a good point. I didn't handle that."

中文：您说得对，这一点我没有处理。

> "My reasoning at the time was X, but you're right that Y would be a problem. I'd fix it by Z."

中文：我当时的考虑是 X，但您说得对，Y 确实会是个问题。我会通过 Z 来修复它。

**想把话题引到你熟悉的经历时**：

> "I dealt with something similar in my internship."

中文：我在实习中处理过类似的问题。

（然后讲你在 nOps 或 ViiVAI 的具体故事。）

**讲完一个点，确认对方是否满意**：

> "Does that answer your question, or should I go deeper on any part?"

中文：这样回答了您的问题吗？还是需要我在某个部分讲得更深入一些？

---

## 第 16 节：最后三件最重要的事

**一、你不需要什么都知道。**三小时原型的 code review，面试官期待的是：你清楚自己做了什么、为什么这么做、代价是什么、下一步怎么改进。

**二、主动说出局限，比被面试官问出来好得多。**比如主动说"这里用 SQLite 是有意的取舍，代价是……"，面试官立刻就知道你心里有数。

**三、用你的真实经历。**你在 nOps 做过重试退避、熔断、断点续跑、用确定性 SQL 替代模型计算；在 ViiVAI 做过八状态编排机、多级降级。**这些都是真的，讲起来有细节，面试官一听就知道不是背的。**

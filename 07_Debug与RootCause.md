# 07 Debug 与 Root Cause

## 先诊断，不要乱改

> 先不要修改代码。
>
> 根据当前 error / logs / behavior 做 root-cause analysis。
>
> 告诉我：
> 1. 最可能 root cause
> 2. supporting evidence
> 3. 最小验证方法
> 4. 最小修复
> 5. 修复后跑什么 test
>
> 不要为了一个 bug 大规模重构。

---

## AI 连续乱修时

> 停止继续随机修改。
>
> 回到事实：
> - expected behavior:
> - actual behavior:
> - exact error:
> - last known working state:
>
> 重新建立 hypothesis。
> 一次只验证一个 hypothesis。

---

## 时间有限时

> 这个 bug 已经花了 [X] 分钟。
> 我还剩 [Y] 分钟。
>
> 帮我判断：
> - 继续修是否值得
> - 有没有最小 workaround
> - 是否应该 rollback
> - 是否应该缩 scope
>
> 优先保护 working demo 和 deployment。

---

## 常见后端 debug 检查

- request payload
- validation
- serialization
- database state
- transaction / commit
- exception handling
- status code
- endpoint path
- environment variable
- port / host
- dependency mismatch
- runtime version

- - 请求负载
- 验证
- 序列化
- 数据库状态
- 事务/提交
- 异常处理
- 状态码
- 端点路径
- 环境变量
- 端口/主机
- 依赖项不匹配
- 运行时版本

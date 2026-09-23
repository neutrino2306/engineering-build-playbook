# Debugging

## Root cause first

> 先不要修改代码。
>
> 根据当前 error / logs / behavior，先做 root-cause analysis。
>
> 请告诉我：
> 1. 最可能的 root cause
> 2. 支持这个判断的 evidence
> 3. 最小验证方法
> 4. 最小修复方法
> 5. 修复后应该跑什么 test
>
> 不要为了修一个 bug 大规模重构。

## If AI keeps failing

> 停止继续尝试随机修改。
>
> 回到当前已知事实：
> - expected behavior:
> - actual behavior:
> - exact error:
> - last known working state:
>
> 请重新建立 hypothesis。
> 一次只验证一个 hypothesis。

## Deployment bug

> 这是 deployment-only failure。
>
> local behavior:
> [PASTE]
>
> deployed behavior/log:
> [PASTE]
>
> 先不要改业务逻辑。
>
> 优先检查：
> - start command
> - port binding
> - environment variables
> - dependency install
> - runtime version
> - filesystem assumptions
> - database path/persistence
> - network binding
> - health check
>
> 给我最小 diagnostic sequence。

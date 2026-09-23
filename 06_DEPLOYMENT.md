# Deployment Checklist

## Before first deployment

Check:

- [ ] App runs locally
- [ ] Core user flow works
- [ ] Dependencies are explicitly declared
- [ ] Start command is known
- [ ] Server binds correctly for hosted environment
- [ ] Required environment variables are documented
- [ ] No secrets are committed
- [ ] Database/filesystem assumptions are understood
- [ ] Health/root endpoint is available if useful
- [ ] README contains run instructions

## Deployment planning prompt

> 现在准备第一次 deploy。
>
> 先不要增加功能。
>
> 根据当前项目，给我一个最短 deployment checklist。
>
> 重点检查：
> - repository requirements
> - runtime
> - dependencies
> - start command
> - host/port
> - environment variables
> - database/storage assumptions
> - health check
> - logs
>
> 请告诉我最可能的三个 deployment failure points。

## After deployment succeeds

- [ ] Open live endpoint
- [ ] Run the core happy path
- [ ] Verify at least one error path
- [ ] Re-run after a clean restart if practical
- [ ] Record the live URL
- [ ] Do not break deployment for optional polish

## If deployment is consuming too much time

> deployment 已经花了 [X] 分钟。
>
> 当前 failure：
> [PASTE]
>
> 我还剩 [Y] 分钟。
>
> 请判断：
> - 最小修复路径
> - 是否应该使用 fallback
> - 什么情况下应该停止继续折腾 deployment
>
> 不要引入新的 infrastructure，除非没有更简单方案。

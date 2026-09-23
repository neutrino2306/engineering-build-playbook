# Time Management

## Build the initial 180-minute plan

> 我需要从 0 到最终 working + deployment，在 180 分钟内完成。
>
> deployment environment 对我相对陌生，请给 deployment 留出额外 buffer。
>
> 根据我们刚才定义的 scope，给我一个风险导向的 180-minute execution plan。
>
> 不要平均分配时间。
>
> 要求：
> - 尽早得到 end-to-end working vertical slice
> - 尽早验证 deployment path
> - 给 debugging 和 deployment 留 buffer
> - 最后留时间做 tests、cleanup、README 和 demo preparation
> - 最后阶段不要再增加 optional feature
>
> 对每个阶段告诉我：
> - 时间范围
> - 唯一最重要目标
> - 必须完成什么
> - 可以放弃什么
> - checkpoint 时项目至少应该是什么状态
>
> 最后给我 3 个 hard checkpoints：
>
> Checkpoint 1:
> 如果到这个时间 core flow 还没跑通，我应该怎么砍 scope。
>
> Checkpoint 2:
> 如果到这个时间 deployment 还没有成功，我应该采用什么 fallback。
>
> Checkpoint 3:
> 从什么时候开始禁止增加新 feature，只允许 testing / cleanup / docs / demo prep。
>
> 请用中文详细解释。

## Re-plan during the session

> 现在已经过去 [X] 分钟，还剩 [Y] 分钟。
>
> 已完成：
> - [ ]
>
> 未完成：
> - [ ]
>
> 当前 blocker：
> - [ ]
>
> 请重新 prioritize。
>
> 告诉我：
> 1. 现在唯一最重要的目标
> 2. 接下来 20–30 分钟应该完成什么
> 3. 哪些 feature 现在直接砍掉
> 4. 是否应该立刻转向 deployment
> 5. 哪些问题留到 code review，不要现在实现
>
> 不要修改代码，先做 time/scope decision。

## Last 60 minutes

> 还剩 60 分钟。
>
> 不要增加任何新 feature，除非缺的是明确 must-have。
>
> 根据当前状态，重新安排：
> - deployment
> - correctness
> - tests
> - cleanup
> - README
> - demo readiness
> - code review readiness
>
> 给我一个严格 priority order。

## Last 30 minutes

> 还剩 30 分钟。
>
> 禁止 scope expansion。
>
> 只允许：
> - fix critical bugs
> - verify deployment
> - verify core flow
> - run tests
> - cleanup obvious issues
> - README
> - prepare demo
> - prepare code review notes
>
> 根据当前状态告诉我现在先做什么。

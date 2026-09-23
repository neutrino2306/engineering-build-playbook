# Build With AI

## Before implementation

> 根据已经确认的 scope，先给我 implementation order。
>
> 目标是尽快形成一个最小 end-to-end vertical slice。
>
> 不要一次实现所有 feature。
>
> 请把第一阶段限制在最少文件和最少依赖。
>
> 先解释你准备改哪些文件、为什么。
> 等我确认后再开始修改。

## Implement one slice

> 只实现下面这一小步：
>
> [TASK]
>
> 不要扩大 scope。
> 不要做 unrelated refactor。
> 完成后告诉我：
> - changed files
> - behavior implemented
> - how to verify it
> - remaining risks

## Before accepting a large AI change

> 先 review 你准备做的改动。
>
> 有没有：
> - unnecessary abstraction
> - new dependency we do not need
> - hidden behavior change
> - code I may have difficulty explaining
> - scope expansion
>
> 如果有，先简化，不要继续写。

## Review current diff

> Review the current git diff as a senior engineer.
>
> 用中文解释。
>
> 检查：
> - correctness
> - accidental scope expansion
> - readability
> - duplicated logic
> - error handling
> - security basics
> - tests
> - deployment risk
>
> 把问题分成：
> 1. fix now
> 2. fix if time remains
> 3. discuss in code review only

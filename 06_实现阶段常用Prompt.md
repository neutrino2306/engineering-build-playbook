# 06 实现阶段常用 Prompt

## 开始第一阶段

> 根据已经确认的 scope，先给 implementation order。
>
> 目标是尽快形成最小 end-to-end vertical slice。
>
> 不要一次实现所有 feature。
> 第一阶段限制在最少文件、最少依赖。
>
> 先解释你准备怎么做，等我确认后再修改。

---

## 一次只实现一个任务

> 只实现：
>
> [TASK]
>
> 不要扩大 scope。
> 不要 unrelated refactor。
>
> 完成后告诉我：
> - changed files
> - implemented behavior
> - how to verify
> - remaining risk

---

## 检查 AI 有没有写太多

> 先 review 你刚才的改动。
>
> 有没有：
> - unnecessary abstraction
> - unnecessary dependency
> - hidden behavior change
> - code I may have difficulty explaining
> - scope expansion
>
> 如果有，先简化。

---

## Review git diff

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
> - validation
> - tests
> - deployment risk
>
> 分成：
> 1. fix now
> 2. fix if time remains
> 3. discuss in code review only

---

## 加测试

> 不要追求覆盖率。
>
> 根据当前项目，告诉我最高价值的 4–6 个 tests。
>
> 优先：
> - happy path
> - invalid input
> - not found / conflict
> - core business rule
> - critical failure
>
> 先解释为什么，再实现。

---

## AI 给的代码我不确定

> 我不想盲信这段实现。
>
> 请逐步解释：
> - input
> - state change
> - side effects
> - failure mode
> - concurrency concern
> - why this is correct
>
> 不要修改代码。

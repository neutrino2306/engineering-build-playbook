# 06 实现阶段常用 Prompt（加强版）

这一页只管“真正写项目的那两个小时”。

---

## 1. 开始实现前

> 根据当前 scope 和剩余时间，先给 implementation order。
>
> 目标是尽快形成最小 end-to-end vertical slice。
>
> 不要一次实现所有功能。
> 先告诉我：
> - 第一阶段做什么
> - 需要哪些文件
> - 成功标准
> - 暂时不做什么
>
> 先解释，不要改代码。

---

## 2. 创建 FastAPI 最小骨架

> 只创建最小可运行 FastAPI 项目。
>
> 需要：
> - app 能启动
> - 一个 health/root endpoint
> - dependencies 明确
> - 结构简单
>
> 不要加业务功能。
> 完成后给我启动命令和验证方式。

---

## 3. Core Vertical Slice

> 现在只完成最核心的一条端到端流程。
>
> request → validation → business logic → state/persistence → response
>
> 不要补其他 feature。
> 不要 over-engineer。
>
> 完成后告诉我怎么验证它真的工作。

---

## 4. 单 Endpoint 实现

> 只实现：
> [ENDPOINT]
>
> 检查：
> - request schema
> - validation
> - response schema
> - status code
> - error handling
>
> 不改 unrelated code。

---

## 5. 加下一个 Must-have

> 当前核心流程已跑通。
>
> 现在只添加：
> [FEATURE]
>
> 不要增加其他 feature。
>
> 完成后告诉我：
> - 新增 edge cases
> - 需要补的 tests
> - 是否增加 deployment risk

---

## 6. 判断某 Feature 值不值得做

> 我还剩 [X] 分钟。
>
> 我考虑继续做：
> [FEATURE]
>
> 请判断：
> - must-have
> - high-value nice-to-have
> - low-value
> - 直接砍掉
>
> 从 completion / demo / code review value / risk 判断。

---

## 7. Review AI 生成代码

> 先停。
>
> 检查刚才改动有没有：
> - unnecessary abstraction
> - unnecessary dependency
> - too many layers
> - hidden behavior changes
> - scope expansion
> - code I may not be able to explain
>
> 先分析，不要继续改。

---

## 8. 我没看懂

> 先解释这段代码。
>
> 按执行顺序讲：
> - input
> - data flow
> - state change
> - side effects
> - error handling
> - why this is correct
> - potential bug
>
> 不要改代码。

---

## 9. Review Diff

> 作为 senior engineer review 当前 git diff。
>
> 分成：
> 1. 必须现在修
> 2. 有时间再修
> 3. code review 讨论即可
>
> 重点：correctness / readability / validation / error handling / tests / deployment risk。

---

## 10. 手动验证 Core Flow

> 不要加功能。
>
> 给我最短的手动验证流程：
> - service start
> - happy path
> - invalid input
> - one error path
>
> 用最简单请求方式。

---

## 11. 加 Testing

> 告诉我最高价值的 5–8 个 tests。
>
> 不追求 coverage。
> 优先业务行为。
>
> 先分析，不写测试。

---

## 12. 实现 Tests

> 根据确认的优先级，实现最小 pytest suite。
>
> 不测试 framework。
> 不写重复测试。
>
> 完成后告诉我未覆盖风险。

---

## 13. Tests 失败

> 先判断失败属于：
> - implementation bug
> - test expectation
> - fixture/setup
> - environment
>
> 先给 evidence。
> 不要直接改。

---

## 14. Implementation Freeze 前检查

> 现在准备停止开发新功能。
>
> 请检查：
> - must-have 是否完整
> - core flow 是否稳定
> - tests 是否覆盖关键行为
> - deployment 是否验证
> - 有没有明显 dead/debug code
>
> 只列最高风险项。

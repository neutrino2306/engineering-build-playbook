# 14A 没有中文输入法时：可直接复制的中文 Prompt（执行加强版）

这个文件的目标：

**现场即使没有中文输入法，也尽量不需要临时组织复杂英文。**

用法：
1. 在 GitHub 打开本页
2. Ctrl+F 搜当前阶段，比如“实现”“测试”“部署”“剩60分钟”
3. 复制整段中文 Prompt
4. 只改数字、文件名、endpoint、error、当前状态
5. 粘给 Claude / Cursor

---

## 开场总指令

> 这是一个严格限时的 3 小时 software engineering coding interview。
>
> 请主要用中文和我讨论、分析、解释和做时间管理，以降低沟通成本。
>
> 所有最终工程 artifact 必须使用英文，包括 code、identifier、API name、file name、comment、docstring、test name、README、commit message 和 user-facing text。
>
> 我负责最终技术判断。你是我的 AI pair programmer / reviewer / temporary project manager。
>
> 当我说“先分析”时，不要自动修改代码。
>
> 不要 over-engineer。
>
> 优先级：
> correctness > end-to-end working > deployability > explainability > testing > polish > optional features
>
> 回答默认先给结论、再给下一步、再说风险。
> 不要重复已经明确的背景。

---

## 选题比较

> 下面是所有候选项目。
>
> 先不要写代码。
>
> 我的默认偏好：
> - Python
> - FastAPI
> - REST API
> - SQLite / SQL
> - pytest
> - backend-first
> - 尽量避免复杂 frontend
> - deployment 需要额外 buffer
>
> 请逐个分析：
> - 3 小时 MVP
> - must-have
> - out-of-scope
> - architecture
> - implementation risk
> - deployment risk
> - demo 效果
> - code review value
>
> 最后给第一推荐、第二推荐、最大风险。
>
> 候选题：
> [PASTE]

---

## Scope

> 好，我决定做这个项目。
>
> 现在不要写代码。
>
> 请从 senior engineer 角度定义严格适合 3 小时的 scope。
>
> 给我：
> - core user flow
> - must-have
> - nice-to-have
> - out-of-scope
> - API
> - data model
> - architecture
> - tests
> - deployment
> - edge cases
> - 留到 production discussion 的内容
>
> 明确指出哪里可能 over-engineer。

---

## 180 分钟计划

> 根据当前 scope，给我一个风险导向的 180 分钟计划。
>
> 要求：
> - 早做 vertical slice
> - 早 deploy
> - 给 debug / deployment 留 buffer
> - 最后留 tests / cleanup / README / REVIEW_NOTES / demo prep
>
> 每个阶段写：
> - 时间
> - 唯一目标
> - 必须完成
> - 超时先砍什么
> - checkpoint 最低状态

---

# 执行阶段

## 开始实现前

> 根据当前 scope 和剩余时间，先给 implementation order。
>
> 目标是尽快形成最小 end-to-end vertical slice。
>
> 先告诉我：
> - 第一阶段做什么
> - 需要哪些文件
> - 成功标准
> - 暂时不做什么
>
> 先解释，不要改代码。

## FastAPI 最小骨架

> 只创建最小可运行 FastAPI 项目。
>
> 要求：
> - 能启动
> - health/root endpoint
> - dependency 明确
> - 结构简单
>
> 不加业务功能。
> 完成后给启动命令和验证方式。

## Core Vertical Slice

> 现在只完成最核心的一条端到端流程。
>
> request → validation → business logic → state/persistence → response
>
> 不补其他 feature。
> 不 over-engineer。
>
> 完成后告诉我怎么验证。

## 单 Endpoint

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

## 加下一个 Must-have

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

## 判断 Feature 值不值得做

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

## 检查 AI 是否写太多

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

## 我没看懂

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

## Review Diff

> 作为 senior engineer review 当前 git diff。
>
> 分成：
> 1. 必须现在修
> 2. 有时间再修
> 3. code review 讨论即可
>
> 重点：correctness / readability / validation / error handling / tests / deployment risk。

---

# Testing 阶段

## 先决定测什么

> 不追求 coverage。
>
> 根据当前项目告诉我最高价值的 5–8 个 tests。
>
> 优先：
> - happy path
> - invalid input
> - not found
> - conflict
> - core business rule
> - failure path
> - edge case
>
> 先解释为什么值得测，不要写测试。

## 实现最小测试集

> 根据刚才确认的优先级，实现最小 pytest suite。
>
> 不测试 framework。
> 不写重复测试。
>
> 完成后告诉我：
> - 每个 test 测什么
> - 还没覆盖什么
> - 哪些未覆盖项可以留到 code review

## 测试失败

> 当前 test failure：
> [PASTE]
>
> 先不要改。
>
> 判断属于：
> - implementation bug
> - test expectation
> - fixture/setup
> - environment
>
> 给 evidence，然后给最小修复方案。

## 手动验证 API

> 不要加功能。
>
> 给我最短手动验证流程：
> - service start
> - happy path
> - invalid input
> - one error path
>
> 用最简单请求方式。

---

# Debug 阶段

## Root Cause First

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
> 不要大规模重构。
>
> 当前错误：
> [PASTE]

## AI 连续修错

> 停止继续随机修改。
>
> Expected:
> [填]
>
> Actual:
> [填]
>
> Exact error:
> [PASTE]
>
> Last working state:
> [填]
>
> 重新建立 hypothesis。
> 一次只验证一个 hypothesis。

## Bug 卡太久

> 这个问题已经花了 [X] 分钟。
> 我还剩 [Y] 分钟。
>
> 请判断：
> - 是否值得继续修
> - 有没有 workaround
> - 是否 rollback
> - 是否缩 scope
> - 如果不修，code review 怎么解释
>
> 优先保护 working demo 和 deployment。

---

# Deployment 阶段

## 部署前

> 现在准备第一次 deploy。
>
> 不要增加功能。
>
> 检查：
> - runtime
> - dependencies
> - requirements.txt / pyproject
> - start command
> - FastAPI app import path
> - host / port
> - env vars
> - database/storage
> - health endpoint
> - logs
>
> 告诉我最高风险的三个 deployment failure points。

## FastAPI 部署专项

> 这是 FastAPI 项目。
>
> 只检查 deployment：
> - uvicorn command
> - app import path
> - host 0.0.0.0
> - port/environment variable
> - requirements
> - Python version
> - env vars
> - SQLite/file path
> - health endpoint
>
> 不要改业务逻辑。

## Deployment 失败

> Local 正常，deployment 失败。
>
> Logs:
> [PASTE]
>
> 先不要改业务逻辑。
>
> 按概率排查：
> 1. start command
> 2. app import
> 3. port
> 4. env vars
> 5. dependency
> 6. runtime
> 7. filesystem/database
>
> 一次只验证一个原因。

## Deployment 成功后

> deployment 已成功。
>
> 给我一个 5–10 分钟 live verification checklist。
>
> 至少：
> - live URL
> - health
> - happy path
> - invalid input
> - error path
> - logs
>
> 验证完成前不要加新 feature。

## Deployment 卡太久

> deployment 已经花了 [X] 分钟。
> 我还剩 [Y] 分钟。
>
> 当前错误：
> [PASTE]
>
> 请判断：
> - 最小修复路径
> - 是否有 fallback
> - 什么时候停止继续 debug
>
> 不要引入新 infrastructure。

---

# 时间管理

## 通用重规划

> 现在已经过去 [X] 分钟。
> 还剩 [Y] 分钟。
>
> 已完成：
> - [填]
>
> 未完成：
> - [填]
>
> 当前 blocker：
> - [填]
>
> 请重新 prioritize。
>
> 告诉我：
> 1. 现在唯一最重要目标
> 2. 接下来 20–30 分钟做什么
> 3. 哪些 feature 立即砍
> 4. 是否应该立刻 deploy
> 5. 哪些问题留到 code review
>
> 先做 time/scope decision，不要改代码。

## 剩 90 分钟

> 还剩 90 分钟。
>
> 重新评估：
> - core flow
> - deployment
> - must-have
> - tests
> - 最大风险
>
> 砍掉低价值工作。
> 给我接下来 30 分钟最高优先级。

## 剩 60 分钟

> 还剩 60 分钟。
>
> 除非缺明确 must-have，否则不要增加新 feature。
>
> 优先级：
> deployment > correctness > tests > cleanup > README > REVIEW_NOTES > demo > code review readiness

## 剩 30 分钟

> 还剩 30 分钟。
>
> 禁止 scope expansion。
>
> 只允许：
> - critical bug fix
> - verify deployment
> - verify core flow
> - tests
> - cleanup
> - README
> - REVIEW_NOTES
> - demo prep
> - code review prep

## 剩 15 分钟

> 还剩最后 15 分钟。
>
> 停止开发新功能。
>
> 帮我完成：
> - README 最小补全
> - REVIEW_NOTES 更新
> - 60 秒 demo 顺序
> - 5 个主要 decisions
> - 5 个 limitations
> - 5 个 production improvements
> - top 10 Tech Lead questions
>
> 输出要短。

---

# 收尾 / Code Review

## 更新 REVIEW_NOTES

> 请更新 REVIEW_NOTES.md。
>
> 不写流水账。
>
> 只记录值得 Tech Lead 讨论的：
> scope / architecture / API / persistence / error handling / testing / deployment / security / scaling / reliability / observability / AI-assisted development
>
> 每个重要 decision 写：
> - What I chose
> - Why
> - Alternative
> - Trade-off
> - Production version

## Final Review

> 现在进入 final review。
>
> 不加 feature。
> 不大规模 refactor。
> 不重新设计 architecture。
>
> 只找：
> 1. 会导致 demo 失败的 critical issue
> 2. 明显 correctness issue
> 3. deployment risk
> 4. code review 高风险点
>
> 只建议 high-value + low-risk 修改。

## README

> 根据当前真实项目，帮我补一个简洁英文 README。
>
> 只包括：
> - Overview
> - Core Features
> - Architecture
> - Tech Stack
> - Run Locally
> - Tests
> - API / Usage
> - Design Decisions
> - Known Limitations
> - Production Improvements
>
> 不要写没实现的东西。

## 60 秒开场

> 根据当前最终项目，给我一个约 60 秒的英文 opening。
>
> 要自然，不像背稿。
>
> 覆盖：
> what I built / core user flow / architecture / prioritized / intentionally left out / tests / deployment
>
> 先中文解释逻辑，再给英文版本。

## 模拟 Technical Review

> Implementation phase is finished.
>
> 不要再加 feature。
>
> 读取当前 repository 和 REVIEW_NOTES.md。
>
> 中文帮我理解，同时给简洁英文表达。
>
> 准备：
> - 60-second walkthrough
> - architecture
> - data flow
> - 5–8 个 engineering decisions
> - alternatives / trade-offs / production version
> - 5 个 weakness
> - 5 个 production improvements
> - one more hour / one more day / production
>
> 然后模拟严格 Senior Engineer。
>
> 每题给：
> - Question
> - Short English Answer
> - 中文解释
> - Potential Follow-up

---

# 万能短 Prompt

> 回答太长。先给结论和下一步，最多 5 个 bullet。

> 根据当前状态和剩余时间，只告诉我最高价值的下一步。

> 如果我正在做低价值工作，请直接叫停。

> 如果 scope 已经够了，请明确告诉我停止加 feature。

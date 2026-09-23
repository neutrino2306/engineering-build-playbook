# 14A 没有中文输入法时：可直接复制的中文 Prompt

这个文件的用途非常简单：

**如果现场电脑没有中文输入法，不要临时硬打英文长句。直接从 GitHub 打开本页，复制中文 Prompt 到 Cursor / Claude。**

你只需要：
- 粘贴题目
- 填数字
- 填英文文件名 / endpoint / error
- 复制错误信息

其余复杂表达全部提前准备好。

---

# 0. 最重要的开场总指令

第一条直接复制：

> 这是一个严格限时的 3 小时 software engineering coding interview。
>
> 请主要用中文和我讨论、分析、解释和做时间管理，因为这样能显著降低我的沟通成本。
>
> 但是所有最终工程 artifact 必须使用英文，包括：
> - code
> - identifier
> - API name
> - file name
> - comment / docstring
> - test name
> - README
> - commit message
> - user-facing text
>
> 我负责最终技术判断。你是我的 AI pair programmer / reviewer / temporary project manager。
>
> 你可以帮助我：
> - 分析题目
> - 比较候选项目
> - 定义 3 小时 scope
> - 设计最简单可靠的 architecture
> - 做 implementation planning
> - 辅助写代码
> - debug
> - testing
> - deployment planning
> - time management
> - technical code review preparation
>
> 当我说“先分析”时，不要自动修改代码。
>
> 不要 over-engineer。
> 如果某个 production concern 不值得在 3 小时 prototype 中实现，请明确告诉我，并留到 code review 讨论。
>
> 优先级：
> correctness > end-to-end working > deployability > explainability > testing > polish > optional features
>
> 如果发生重要 architecture / scope / implementation decision，请提醒我更新 REVIEW_NOTES.md。
>
> 如果你的回答太长，请优先给我：
> 1. 结论
> 2. 下一步
> 3. 风险
>
> 不要重复已经明确的背景。

---

# 1. 拿到多个题目：帮我选题

把所有 prompts 粘贴在后面：

> 下面是本次 coding interview 的所有候选项目。
>
> 先不要写代码，不要创建文件。
>
> 我的默认技术偏好：
> - Python
> - FastAPI（默认首选）
> - Flask（fallback，如果当前题目/环境下明显更简单）
> - REST API
> - SQL / SQLite / MySQL
> - pytest
> - backend-first
> - 尽量避免复杂 frontend
> - deployment 对我相对陌生，因此要降低 deployment risk
>
> 请逐个分析每一个题：
>
> 1. 核心问题
> 2. 3 小时合理 MVP scope
> 3. must-have
> 4. nice-to-have
> 5. 明确 out-of-scope
> 6. 推荐 architecture
> 7. implementation risk
> 8. deployment risk
> 9. debugging risk
> 10. demo 效果
> 11. code review 能讨论的 engineering trade-offs
> 12. 对我的技术背景是否合适
> 13. 3 小时完成 polished working prototype 的概率
>
> 最后告诉我：
> - 第一推荐
> - 第二推荐
> - 为什么
> - 最大风险
> - 如果你是 senior engineer，你会怎么选
>
> 评价优先级：
> completion > reliability > deployability > explainability > engineering depth > optional features
>
> 请用中文详细解释。
> 不要开始实现。
>
> 候选题如下：
>
> [把题目粘贴这里]

---

# 2. 我已经倾向某一道题：帮我挑战判断

> 我目前更倾向选择：
>
> [题目名称 / A / B]
>
> 不要顺着我说。
>
> 如果你是 senior engineer，请挑战这个选择。
>
> 重点考虑：
> - 3 小时完成率
> - deployment risk
> - demo 完整度
> - code review depth
> - 我是否能完全理解和解释代码
> - 是否容易 over-engineer
>
> 如果你认为有更好的题，请直接说。
>
> 先分析，不要写代码。

---

# 3. 选定项目后：定义 3 小时 Scope

> 好，我决定做这个项目。
>
> 现在不要写代码。
>
> 如果你是要 review 这个项目的 senior engineer，请帮我定义一个严格适合 3 小时的 scope。
>
> 我要从 0 做到：
> - working
> - testable
> - demoable
> - preferably deployed
> - explainable
>
> 请给我：
>
> 1. Core user flow
> 2. Must-have requirements
> 3. Nice-to-have requirements
> 4. Explicitly out-of-scope
> 5. Minimal API design
> 6. Minimal data model
> 7. Recommended architecture
> 8. Technology stack
> 9. Minimal project structure
> 10. Testing strategy
> 11. Deployment strategy
> 12. Main failure cases / edge cases
> 13. Security basics worth doing now
> 14. Production concerns that should NOT be implemented now
> 15. Code review 时值得讨论的 trade-offs
>
> Constraints:
> - strict 3-hour limit
> - single engineer + AI-assisted development
> - deployment environment relatively unfamiliar
> - must remain understandable and explainable
> - avoid unnecessary infrastructure
> - get a working vertical slice early
>
> 请明确指出：
> - 哪里可能 over-engineer
> - 哪里 scope 太薄
> - 哪些 production concerns 应该留到 code review
>
> 用中文详细解释。
> 不要开始写代码。

---

# 4. 让 AI 给我做完整 180 分钟时间表

> 根据刚才确认的 scope，给我一个严格的 180 分钟 execution plan。
>
> deployment environment 对我相对陌生，请给 deployment 比通常更多 buffer。
>
> 不要平均分配时间。
>
> 必须满足：
> - 尽早得到 end-to-end working vertical slice
> - 尽早验证 deployment path
> - 给 debugging 留 buffer
> - 最后留 testing / cleanup / README / REVIEW_NOTES / demo prep
> - 最后阶段禁止 optional feature
>
> 对每个阶段告诉我：
> - 时间范围
> - 唯一最重要目标
> - 必须完成什么
> - 如果超时先砍什么
> - checkpoint 时项目最低可接受状态
>
> 最后给我 3 个 hard checkpoints：
>
> 1. 到什么时间 core flow 还没通，就必须缩 scope
> 2. 到什么时间 deployment 还没成功，就必须执行 fallback
> 3. 从什么时间开始禁止增加 feature，只允许 testing / cleanup / docs / demo prep
>
> 请中文详细解释。

---

# 5. 开始实现前：先给 implementation order

> 根据已经确认的 scope 和时间表，先给我 implementation order。
>
> 目标是尽快形成最小 end-to-end vertical slice。
>
> 不要一次实现所有 feature。
> 第一阶段限制在最少文件、最少依赖。
>
> 先告诉我：
> - 你准备创建 / 修改哪些文件
> - 每个文件为什么需要
> - 第一阶段成功标准是什么
>
> 等我确认后再开始修改代码。

---

# 6. 只实现当前一步，不许扩 Scope

> 只实现下面这一小步：
>
> [TASK]
>
> 不要扩大 scope。
> 不要 unrelated refactor。
> 不要顺手加 optional feature。
>
> 完成后告诉我：
> - changed files
> - implemented behavior
> - how to verify
> - remaining risks

---

# 7. AI 写了一堆代码：先帮我检查是不是过度设计

> 先不要继续写。
>
> Review 你刚才的改动。
>
> 检查有没有：
> - unnecessary abstraction
> - unnecessary dependency
> - hidden behavior change
> - scope expansion
> - code I may have difficulty explaining
> - architecture complexity that is unnecessary for a 3-hour prototype
>
> 如果有，请告诉我哪里可以简化。
>
> 先分析，不要修改。

---

# 8. Review 当前 Git Diff

> 请作为 senior engineer review 当前 git diff。
>
> 用中文解释。
>
> 重点检查：
> - correctness
> - accidental scope expansion
> - readability
> - duplicated logic
> - validation
> - error handling
> - tests
> - deployment risk
> - code I may not be able to explain
>
> 把问题分成：
>
> 1. 必须现在修
> 2. 有时间再修
> 3. 不要现在实现，只在 code review 讨论
>
> 不要直接修改代码。

---

# 9. Debug：先 Root Cause，不要乱修

> 先不要修改代码。
>
> 根据当前 error / logs / behavior 做 root-cause analysis。
>
> 请告诉我：
>
> 1. 最可能的 root cause
> 2. 支持这个判断的 evidence
> 3. 最小验证方法
> 4. 最小修复方法
> 5. 修复后应该跑什么 test
>
> 不要为了一个 bug 大规模重构。
>
> 当前错误：
>
> [粘贴 error / log]

---

# 10. AI 已经连续修错几次：停止随机修改

> 停止继续随机修改。
>
> 回到当前已知事实。
>
> Expected behavior:
> [填]
>
> Actual behavior:
> [填]
>
> Exact error:
> [粘贴]
>
> Last known working state:
> [填]
>
> 请重新建立 hypothesis。
>
> 一次只验证一个 hypothesis。
> 不要同时改多个地方。

---

# 11. 这个 Bug 已经花太久：帮我判断还值不值得修

> 这个问题已经花了 [X] 分钟。
>
> 我还剩 [Y] 分钟。
>
> 请从面试完成度和风险角度判断：
>
> 1. 是否值得继续修
> 2. 有没有最小 workaround
> 3. 是否应该 rollback
> 4. 是否应该缩 scope
> 5. 如果暂时不修，我在 code review 中应该如何解释
>
> 优先保护：
> working demo > deployment > correctness of core flow > optional features

---

# 12. 准备第一次 Deployment

> 现在准备第一次 deploy。
>
> 不要增加任何新功能。
>
> 根据当前项目给我一个最短 deployment checklist。
>
> 重点检查：
> - repository requirements
> - runtime
> - dependencies
> - start command
> - host / port
> - environment variables
> - database / storage assumptions
> - health check
> - logs
>
> 告诉我最可能的三个 deployment failure points。
>
> 先检查，不要大改代码。

---

# 13. Deployment 出错

> 这是 deployment-only failure。
>
> Local behavior:
> [填]
>
> Deployed behavior:
> [填]
>
> Logs:
> [粘贴]
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
> - database path / persistence
> - network binding
> - health check
>
> 给我最小 diagnostic sequence。
> 一次只验证最可能的原因。

---

# 14. 中途重新做时间管理

> 现在已经过去 [X] 分钟。
>
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
> 2. 接下来 20–30 分钟应该完成什么
> 3. 哪些 feature 立即砍掉
> 4. 是否应该立刻转向 deployment
> 5. 哪些问题留到 code review，不要现在实现
>
> 先做 time/scope decision。
> 不要修改代码。

---

# 15. 还剩 90 分钟

> 现在还剩 90 分钟。
>
> 请重新评估：
> - core flow 是否完整
> - deployment 是否已验证
> - must-have 还缺什么
> - tests 是否足够
> - 最大风险是什么
>
> 砍掉低价值工作。
>
> 给我接下来 30 分钟唯一最高优先级目标。

---

# 16. 还剩 60 分钟

> 现在还剩 60 分钟。
>
> 除非缺题目明确 must-have，否则不要增加新 feature。
>
> 按优先级重新安排：
> 1. deployment
> 2. correctness
> 3. tests
> 4. cleanup
> 5. README
> 6. REVIEW_NOTES
> 7. demo readiness
> 8. code review readiness
>
> 告诉我现在最应该做什么。
> 不要扩大 scope。

---

# 17. 还剩 30 分钟

> 现在还剩 30 分钟。
>
> 禁止 scope expansion。
>
> 只允许：
> - critical bug fix
> - verify deployment
> - verify core flow
> - run tests
> - cleanup obvious issues
> - README
> - REVIEW_NOTES
> - demo prep
> - code review prep
>
> 只告诉我最高价值的下一步。
> 不要提出新的 architecture 或 optional feature。

---

# 18. 让 AI 帮我持续维护 REVIEW_NOTES.md

> 请创建 / 更新 REVIEW_NOTES.md。
>
> 这个文件用于后面的 technical code review。
>
> 不要写流水账。
> 不要记录每个小改动。
>
> 只记录值得 Tech Lead 讨论的 engineering decisions。
>
> 每个重要 decision 尽量包含：
> - What I chose
> - Why
> - Alternative
> - Trade-off
> - Production version
>
> 同时记录：
> - architecture
> - scope
> - persistence
> - API design
> - error handling
> - testing
> - deployment
> - known limitations
> - scaling
> - reliability
> - observability
> - security
> - AI-assisted development: what AI helped with / what I verified / what I rejected
>
> 保持简洁。

---

# 19. 最后 Final Review：不准再乱加东西

> 现在进入 final review。
>
> 不要增加新 feature。
> 不要大规模 refactor。
> 不要重新设计 architecture。
>
> 请作为 senior engineer review 当前项目。
>
> 只找：
>
> 1. 会导致 demo 失败的 critical issue
> 2. 明显 correctness issue
> 3. deployment risk
> 4. code review 高风险点
>
> 只建议：
> high-value + low-risk 的最后修改。
>
> 如果某个问题应该留到 code review 讨论，而不是现在修，请明确说。

---

# 20. 生成 60 秒 Code Review Opening

> 根据当前最终项目，给我一个大约 60 秒的英文 opening。
>
> 要自然，不要像背稿。
>
> 覆盖：
> - what I built
> - core user flow
> - architecture
> - what I prioritized
> - what I intentionally left out
> - testing
> - deployment
>
> 先用中文解释逻辑，再给最终英文版本。

---

# 21. 生成 45 分钟技术拷打准备

> Implementation phase is finished.
>
> 不要再加 feature。
> 不要大规模 refactor。
>
> 你现在帮我准备接下来 45 分钟 Technical Lead code review。
>
> 请读取当前 repository 和 REVIEW_NOTES.md。
>
> 请用中文帮助我彻底理解，同时给我能直接在面试中使用的简洁英文表达。
>
> 请准备：
>
> 1. 60-second walkthrough
> 2. architecture summary
> 3. main data flow
> 4. 5–8 个最重要 engineering decisions
> 5. 每个 decision 的 alternative / trade-off / production version
> 6. 5 个最明显 weakness
> 7. 5 个 production improvements
> 8. if I had one more hour
> 9. if I had one more day
> 10. if this were production
>
> 然后模拟一个严格的 Senior Engineer / Tech Lead。
>
> 根据我的实际 repository，生成 20 个最可能 technical questions。
>
> 每题给：
> - Question
> - Short English Answer
> - 中文解释
> - Potential Follow-up
>
> 优先覆盖：
> architecture
> API design
> data model
> concurrency
> idempotency
> error handling
> database
> scalability
> reliability
> security
> observability
> testing
> deployment
> performance
> production readiness
> AI-assisted development
>
> 最后给我一页极短速查表。

---

# 22. 只给我“一页速查”，不要长篇大论

> 不要再详细解释。
>
> 现在只给我一页超短速查表。
>
> 包含：
> - 1 句话 problem statement
> - 1 句话 architecture
> - 5 major decisions
> - 5 trade-offs
> - 5 known limitations
> - 5 production improvements
> - 10 most likely questions
> - 每个问题 1–2 句英文回答
>
> 我只有几分钟复习。
> 不要输出额外背景。

---

# 23. 我脑子知道但英文说不出来：帮我转成自然英文

> 下面是我想表达的中文意思。
>
> 请不要改变技术含义。
>
> 把它改成一个 software engineer 在 technical code review 中自然会说的英文。
>
> 要求：
> - 简洁
> - 不要太书面
> - 不要复杂句
> - 不要夸张
> - 保留技术准确性
>
> 中文：
> [把中文粘贴这里]

---

# 24. AI 回答太长：立刻压缩

> 回答太长。
>
> 从现在开始：
> - 先给结论
> - 最多 5 个 bullet
> - 如果我没要求，不要重复背景
> - 只告诉我当前阶段最高价值的信息

---

# 25. 我很赶时间：只告诉我下一步

> 不要解释背景。
>
> 根据当前项目状态和剩余时间，只告诉我：
>
> 1. 下一步做什么
> 2. 为什么
> 3. 成功标准
>
> 最多 5 行。

---

# 26. 万能 Senior Engineer Review Prompt

这个可以反复复制：

> 如果你是现在负责 review 我项目的 senior engineer，请从真实工程角度 challenge 当前方案。
>
> 不要为了显得高级而增加复杂度。
>
> 重点判断：
> - correctness
> - scope discipline
> - simplicity
> - deployment risk
> - failure handling
> - testing
> - explainability
> - production trade-offs
>
> 请把建议分成：
> 1. 必须现在做
> 2. 有时间再做
> 3. 不要现在做，只在 code review 讨论
>
> 先分析，不要修改代码。

---

# 27. 万能“现在到底该干嘛” Prompt

> 根据：
> - 当前 repository 状态
> - 剩余时间
> - 已确认 scope
> - deployment 状态
>
> 告诉我现在最高价值的下一步是什么。
>
> 如果我正在做低价值工作，请直接叫停。
>
> 如果 scope 已经足够，请明确告诉我停止加 feature。
>
> 中文回答。
> 最多 5 个 bullet。

---

# 使用方式总结

如果没有中文输入法：

1. 打开这个 GitHub 文件
2. 找到当前阶段
3. 复制整段
4. 粘到 Cursor / Claude
5. 只用数字、英文文件名、endpoint、error log 做最少修改

**不要因为没有中文输入法，就强迫自己现场组织复杂英文。**

最终目标不是展示英语 Prompt 文采。

最终目标是：

**快速做出一个 working、deployed、tested、你能够完整解释的系统。**

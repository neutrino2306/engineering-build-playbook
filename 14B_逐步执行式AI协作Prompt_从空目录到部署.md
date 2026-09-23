# 14B 逐步执行式 AI 协作 Prompt：从空目录到部署

这份文件不是“让 AI 一次把整个项目做完”。

它的目标是：

**先让 AI 给完整 roadmap，然后一次只执行一个阶段。每一步都明确：做什么、改哪些文件、怎么测试、什么算通过、失败了怎么 debug、什么时候进入下一步。**

这更适合三小时 coding interview，也更适合我自己的工作方式。

---

# 一、最开始：给 AI 一个总控指令

> 这是一个严格限时 3 小时的 coding interview。
>
> 我希望你充当：
> - senior engineer
> - pair programmer
> - implementation guide
> - temporary project manager
>
> 但不要替我做最终技术判断。
>
> 我需要一种非常具体的逐步执行方式：
>
> 1. 先给我完整 roadmap
> 2. 然后一次只执行一个阶段
> 3. 每个阶段开始前先告诉我：
>    - 目标是什么
>    - 为什么现在做
>    - 要创建/修改哪些文件
>    - 每个文件负责什么
>    - 需要执行什么命令
>    - 怎么测试
>    - 什么结果算通过
> 4. 当前阶段没有通过前，不要自动进入下一阶段
> 5. 如果出现 bug，先定位 root cause，不要连续随机修改
> 6. 每次修改后都告诉我需要重新跑什么
> 7. 如果我做完一步，把结果发给你，请先判断“是否真的通过”
> 8. 如果没有通过，明确告诉我卡在哪里
> 9. 随时根据剩余时间重新缩 scope
> 10. 不要 over-engineer
>
> 请主要用中文跟我解释。
> 所有最终工程产物保持英文：
> code、identifier、file name、API、test、README、commit message。
>
> 如果我说“先解释”，不要改代码。
> 如果我说“只告诉我下一步”，不要继续展开未来步骤。
> 如果我说“这样算成功了吗”，请根据可验证结果判断，不要只说“看起来可以”。

---

# 二、拿到题目：先生成完整 Roadmap

> 这是题目：
>
> [PASTE PROMPT]
>
> 先不要创建文件，也不要写代码。
>
> 请根据 3 小时时间限制，给我一个从 0 到 deploy 的完整 implementation roadmap。
>
> 必须具体到：
>
> Phase 0：需求和 scope
> - 最小 MVP
> - out-of-scope
> - 数据模型
> - API
> - reliability concern
>
> Phase 1：项目骨架
> - 创建什么目录
> - 创建哪些文件
> - 每个文件职责
> - 最小依赖
>
> Phase 2：第一个可运行版本
> - 先写哪些文件
> - 先实现哪个 endpoint
> - 怎么启动
> - 怎么验证
>
> Phase 3：核心业务流程
> - 按什么顺序实现
> - 每完成一个功能要测什么
>
> Phase 4：数据库 / persistence
> - 什么时候加
> - 怎么验证数据真的写进去
>
> Phase 5：tests
> - 什么时间开始写
> - 哪些 test 必须有
> - 什么叫 test pass
>
> Phase 6：第一次 deployment
> - 什么状态下就应该开始 deploy
> - 需要哪些文件
> - 可能失败在哪里
>
> Phase 7：deployment 后完善
> - 哪些功能值得继续做
> - 哪些应该停止
>
> Phase 8：final freeze
> - README
> - REVIEW_NOTES
> - final tests
> - live verification
>
> 对每一个 Phase 给：
> - Estimated time
> - Goal
> - Files
> - Commands
> - Test / validation
> - Success criteria
> - Common failure
> - 如果时间不足先砍什么
>
> 最后再给一个：
> “如果我完全慌了，只按最小路线走”的版本。

---

# 三、Roadmap 有了以后：不要一起做，开始 Step 1

> 好，现在 roadmap 确认了。
>
> 从现在开始一次只做一个阶段。
>
> 现在只告诉我 Step 1。
>
> 请具体告诉我：
> 1. 当前目标
> 2. 要创建哪些文件/目录
> 3. 每个文件先写什么
> 4. 如果需要代码，请给最小代码
> 5. 我应该执行什么命令
> 6. 应该看到什么结果
> 7. 什么结果代表 Step 1 已经通过
>
> 不要提前进入 Step 2。

---

# 四、我不知道为什么要建这些文件

> 先不要继续写。
>
> 你刚才让我创建这些文件：
>
> [FILES]
>
> 请逐个用中文解释：
> - 这个文件为什么存在
> - 谁会调用它
> - 它输入什么
> - 输出什么
> - 如果删掉会怎样
> - 现在是否真的必须
>
> 如果有为了“结构漂亮”而不是 MVP 必需的文件，请删掉建议。

---

# 五、我不知道这个目录到底对不对

> 这是我现在的目录：
>
> [PASTE TREE]
>
> 先不要改。
>
> 请判断：
> 1. 是否足够支撑当前 MVP
> 2. 是否缺必要文件
> 3. 是否有不必要文件
> 4. import path 会不会有问题
> 5. deployment 时可能有什么问题
>
> 最后给我“现在保持不动”或“只改这几个地方”。

---

# 六、准备创建第一个文件

> 现在只处理这个文件：
>
> [FILE NAME]
>
> 请告诉我：
> - 它当前阶段唯一职责是什么
> - 最小需要写什么
> - 什么暂时不要写
>
> 然后给我最小实现。
>
> 不要同时生成其他文件。

---

# 七、文件写完以后：怎么知道它没问题

> 我已经写完：
>
> [FILE]
>
> 先不要进入下一步。
>
> 告诉我怎么验证这个文件/功能：
> - 需要运行什么命令
> - 需要发什么请求
> - 预期输出是什么
> - 哪些 warning 可以暂时忽略
> - 哪些 error 必须现在解决
>
> 最后明确告诉我：
> “满足哪些条件以后才能进入下一步”。

---

# 八、最小 FastAPI 启动验证

> 我现在只想确认项目骨架能运行。
>
> 不要加业务逻辑。
>
> 请告诉我：
> 1. 最小 main.py 应该长什么样
> 2. requirements.txt 最少需要什么
> 3. 启动命令
> 4. /health 应该返回什么
> 5. Swagger /docs 是否应该能打开
> 6. 哪些结果算这个阶段通过
>
> 如果通过，再告诉我下一步，不要提前实现。

---

# 九、我执行完了：这样算成功了吗？

> 我刚执行了：
>
> [COMMAND]
>
> 得到：
>
> [OUTPUT]
>
> 这样算通过了吗？
>
> 请不要泛泛回答。
>
> 按下面格式判断：
> - 当前目标：
> - 实际结果：
> - 是否满足 success criteria：
> - 是否还有隐藏问题：
> - 结论：PASS / NOT PASS
> - 如果 PASS：下一步是什么
> - 如果 NOT PASS：现在只修什么

---

# 十、现在下一步到底是什么？

> 当前状态：
>
> 已完成：
> [DONE]
>
> 当前能运行：
> [WORKING]
>
> 当前失败：
> [FAILURE]
>
> 还剩：
> [TIME]
>
> 现在只告诉我最高价值的下一步。
>
> 请具体到：
> - 哪个文件
> - 改什么
> - 为什么
> - 改完跑什么
> - 看到什么算通过
>
> 不要给我后面五步。

---

# 十一、实现 Core Flow

> 现在开始 core flow。
>
> 请先把 core flow 拆成最小的连续步骤。
>
> 例如：
> request
> → validation
> → service
> → database/state
> → response
>
> 对每一步告诉我：
> - 修改哪个文件
> - 写什么
> - 完成后怎么验证
>
> 然后只执行第一步。
> 不要一次把整个 core flow 全写完。

---

# 十二、AI 一次改太多了

> 停一下。
>
> 你刚才一次修改太多，我现在无法确认每个改动是否正确。
>
> 请重新拆分。
>
> 先告诉我：
> - 哪些改动是必须的
> - 哪些可以后做
> - 哪些应该撤回
>
> 然后只保留当前阶段最小改动。
>
> 我希望每一步都能单独测试和确认。

---

# 十三、什么时候应该开始写 Tests？

> 当前项目状态：
>
> [STATUS]
>
> 现在是否已经应该开始写 tests？
>
> 请根据当前阶段判断，而不是固定套路。
>
> 如果应该：
> - 先测哪 3–5 个行为
> - 为什么
> - tests/test_api.py 现在应该写什么
>
> 如果不应该：
> - 还缺什么
> - 达到什么状态后立刻开始写 tests

---

# 十四、生成测试之前先列 Test Plan

> 先不要写测试代码。
>
> 根据当前实现，给我 test plan。
>
> 分成：
>
> MUST TEST NOW
> - core happy path
> - critical validation
> - most important failure path
> - important business invariant
>
> TEST IF TIME
> - secondary edge cases
>
> CODE REVIEW ONLY
> - 不值得三小时现场实现的复杂测试
>
> 对每个 test 告诉我：
> - setup
> - action
> - expected result
> - 为什么重要

---

# 十五、现在写测试文件

> 好，只实现刚才确认的 MUST TEST NOW。
>
> 请生成最小 tests/test_api.py。
>
> 要求：
> - 每个 test 名字清楚
> - test data 很小
> - 不为了 coverage 写无意义测试
> - 不测试 framework 自己
> - 测业务行为
>
> 完成后告诉我：
> - 怎么运行
> - 应该看到多少 passed
> - 如果 failure 最先看哪里

---

# 十六、测试通过了吗？

> pytest 输出：
>
> [PASTE]
>
> 请判断：
> - 一共有多少 test
> - passed / failed / skipped
> - 当前是否可以认为 core behavior 已经通过
> - 有没有 warning 值得现在处理
> - 下一步是否应该 deploy
>
> 明确给：
> PASS / NOT PASS。

---

# 十七、测试失败了：不要立刻改

> 当前 test failure：
>
> [TRACEBACK]
>
> 先不要改代码。
>
> 请按顺序判断：
> 1. test expectation 错
> 2. implementation bug
> 3. fixture/setup bug
> 4. import/path 问题
> 5. environment/dependency 问题
>
> 告诉我最可能的原因和 evidence。
>
> 然后只给一个最小验证动作。
> 等我跑完再继续。

---

# 十八、我跑了你说的验证，结果是这样

> 我刚按你说的验证：
>
> [COMMAND]
>
> 结果：
>
> [OUTPUT]
>
> 现在这个 hypothesis 被证实了吗？
>
> 如果没有，请不要同时给三个新猜测。
> 只选下一个最可能的 hypothesis 和一个验证方法。

---

# 十九、Bug 修完以后到底要重跑什么

> 我刚修了：
>
> [CHANGE]
>
> 现在请告诉我重新验证顺序。
>
> 我希望从最便宜的验证开始：
> 1. targeted test
> 2. relevant test group
> 3. full pytest
> 4. manual API
> 5. deployment
>
> 哪些需要跑，哪些现在不用跑？
>
> 说明原因。

---

# 二十、Bug 修复后：这样算彻底解决了吗？

> 原 bug：
> [BUG]
>
> 修改：
> [CHANGE]
>
> 现在结果：
> [RESULT]
>
> 请检查：
> - 原 bug 是否真的消失
> - 有没有 regression risk
> - 需要什么 test 防止以后重新出现
> - 当前可以进入下一阶段了吗
>
> 最后给 PASS / NOT PASS。

---

# 二十一、我觉得 AI 在乱修

> 停止修改。
>
> 我感觉现在开始出现“修一个地方坏另一个地方”的情况。
>
> 请重新建立事实：
>
> Last known good state:
> [STATE]
>
> Expected:
> [EXPECTED]
>
> Actual:
> [ACTUAL]
>
> Exact error:
> [ERROR]
>
> Current diff:
> [DIFF]
>
> 请：
> 1. 找出从 last known good state 到现在最可能引入问题的改动
> 2. 判断是否应该 rollback
> 3. 一次只验证一个 hypothesis
>
> 不要继续堆 patch。

---

# 二十二、我要不要现在 Deploy？

> 当前状态：
>
> Core flow：
> [STATUS]
>
> Tests：
> [STATUS]
>
> Known bugs：
> [STATUS]
>
> Remaining time：
> [TIME]
>
> 现在是否应该立刻第一次 deploy？
>
> 请明确回答：
> DEPLOY NOW / NOT YET
>
> 如果 DEPLOY NOW：
> 给我 deployment 前最小 checklist。
>
> 如果 NOT YET：
> 只告诉我 deploy 前唯一必须完成的事情。

---

# 二十三、第一次 Deployment Roadmap

> 现在进入第一次 deployment。
>
> 请一次一步带我做，不要一次给十步让我自己猜。
>
> 先检查当前 repo 是否具备 deployment 最低条件：
> - requirements
> - start command
> - app import path
> - host
> - port
> - env vars
> - database/file assumptions
> - health endpoint
>
> 然后告诉我 Step 1：
> - 去哪里
> - 点击/输入什么
> - 应该看到什么
> - 什么算 Step 1 完成
>
> 等我告诉你结果以后再给下一步。

---

# 二十四、部署页面我看到这个，不知道选什么

> 我现在在 deployment 页面。
>
> 页面上有：
>
> [PASTE OPTIONS / SCREEN TEXT]
>
> 不要泛泛解释所有选项。
>
> 根据当前 FastAPI 项目告诉我：
> - 选哪个
> - 为什么
> - 哪些保持默认
> - 哪些必须改
> - 下一步点什么
>
> 如果有风险，先指出。

---

# 二十五、Deployment Build 失败

> build failed。
>
> Build log：
>
> [PASTE]
>
> 先判断失败发生在哪一层：
> - dependency install
> - build
> - import
> - startup
> - port binding
> - runtime
> - database/filesystem
>
> 不要改业务逻辑。
>
> 给我：
> - root cause hypothesis
> - evidence
> - 最小修改
> - 修改后重新部署前要不要先 local test
>
> 一次只修一个问题。

---

# 二十六、Deployment 成功了：真的算成功吗？

> deployment 页面显示 success。
>
> 现在请不要默认项目就真的正常。
>
> 给我 live verification 顺序：
> 1. /health
> 2. core happy path
> 3. important failure path
> 4. logs
> 5. database/persistence assumption
>
> 每一步告诉我预期结果。
>
> 最后再判断：
> DEPLOYMENT VERIFIED / NOT VERIFIED。

---

# 二十七、部署成功以后下一步做什么

> 当前：
> - deployment 已验证
> - core flow 已工作
> - tests [X] passed
> - 还剩 [Y] 分钟
>
> 现在请重新评估 roadmap。
>
> 把剩余事项分成：
>
> MUST DO
> SHOULD DO
> ONLY IF TIME
> CODE REVIEW ONLY
>
> 然后只告诉我下一步具体做什么。

---

# 二十八、我看到一个新需求，不知道要不要加

> 我想到/AI建议增加：
>
> [FEATURE]
>
> 当前还剩 [TIME]。
>
> 请不要因为它“更 production”就默认应该做。
>
> 判断：
> - 对核心正确性是否必要
> - 对 demo 是否明显增值
> - 实现风险
> - 测试成本
> - deployment risk
> - code review 是否只讲就够
>
> 最后给：
> DO NOW / ONLY IF TIME / CODE REVIEW ONLY / CUT。

---

# 二十九、我不理解一个技术概念

> 先暂停实现。
>
> 我不理解：
>
> [TERM]
>
> 请结合当前项目，用非常具体的例子解释：
> 1. 它解决什么问题
> 2. 不做会发生什么
> 3. 当前 prototype 是否需要实现
> 4. 如果实现，放在哪个文件
> 5. production 中通常怎么做
>
> 解释完以后再告诉我：
> “现在需要处理它吗？”

---

# 三十、我大概懂了，但想确认理解

> 我的理解是：
>
> [MY UNDERSTANDING]
>
> 你帮我判断：
> - 哪部分对
> - 哪部分不准确
> - 缺了什么
>
> 不要重新从头讲一遍。
> 只纠正关键点。
>
> 最后给我一个正确版本的一句话总结。

---

# 三十一、我觉得现在东西太多了

> 当前信息太多，我开始不好判断优先级。
>
> 请把当前状态压缩成：
>
> 1. 已经确定没问题的
> 2. 现在唯一 blocker
> 3. 下一步唯一动作
> 4. 成功标准
> 5. 下一步完成后再考虑什么
>
> 不要再给额外建议。

---

# 三十二、还剩 90 分钟

> 还剩 90 分钟。
>
> 请根据当前真实状态重新生成剩余 roadmap。
>
> 不要沿用原计划。
>
> 必须回答：
> - deployment 是否已经打通
> - core flow 是否完整
> - tests 是否足够
> - 最大 blocker
> - 哪些功能立刻砍
>
> 然后给未来 30 分钟逐步计划。

---

# 三十三、还剩 60 分钟

> 还剩 60 分钟。
>
> 现在我需要保守策略。
>
> 请：
> - 停止 optional feature
> - 优先 deployment / correctness / tests
> - 标出任何可能导致 demo 挂掉的问题
>
> 给我未来 20 分钟一步一步怎么做。
> 每一步都要有 success criteria。

---

# 三十四、还剩 30 分钟

> 只剩 30 分钟。
>
> 禁止增加新功能。
>
> 请带我按顺序完成：
> 1. critical bug check
> 2. full tests
> 3. live deployment verification
> 4. README
> 5. REVIEW_NOTES
> 6. code review preparation
>
> 一次只给一个步骤。

---

# 三十五、最后 15 分钟

> 最后 15 分钟。
>
> 不再改 architecture。
>
> 请先判断有没有必须修的 critical issue。
>
> 如果没有：
> - 不再写新代码
> - 帮我确认 tests
> - 确认 live URL
> - 更新 README
> - 更新 REVIEW_NOTES
> - 准备 code review
>
> 一次只处理一个。

---

# 三十六、准备 Code Review：从项目里帮我找问题

> coding 结束。
>
> 现在不要再修改代码。
>
> 请作为严格的 Technical Lead 阅读当前 repo。
>
> 先给我：
> 1. 这个项目完整数据流
> 2. 我做的关键 decisions
> 3. 哪些是 prototype shortcut
> 4. 最大 5 个 production weaknesses
> 5. 哪些问题 interviewer 最可能追问
>
> 对每个问题：
> - 中文解释
> - 简短英文回答
> - follow-up

---

# 三十七、如果 interviewer 问“为什么这样做”

> 针对这个 decision：
>
> [DECISION]
>
> 帮我准备：
> - What I chose
> - Why
> - Alternative
> - Why I did not choose it in 3 hours
> - Production version
>
> 先中文讲透，再给简短英文回答。

---

# 三十八、如果 interviewer 问“AI 做了什么”

> 根据当前项目和我们的实际开发过程，帮我总结 AI-assisted development。
>
> 只基于真实发生的事情。
>
> 分成：
> - AI scaffolded
> - I reviewed
> - I verified
> - I changed/rejected
> - Bugs AI introduced or failed to solve
> - Decisions I made myself
>
> 不要编造。
>
> 然后给我一个 30–45 秒英文回答。

---

# 三十九、我的典型交互方式：可以直接这样问

下面这些不是“漂亮 prompt”，而是现场最自然、最可能真的会说的话。

### “所以我现在到底先干嘛？”

> 你不要先讲后面。
> 根据当前状态告诉我我现在第一件事要干嘛。
> 具体到哪个文件、写什么、跑什么、什么算成功。

### “这个文件为什么现在要有？”

> 我不确定这个文件现在是不是必须。
> 你告诉我它解决什么问题。
> 如果只是为了结构漂亮就先不要建。

### “我现在做到这里了，接下来呢？”

> 我现在做到：
> [STATUS]
>
> 接下来最合理的一步是什么？
> 不要一次给我很多步。

### “这样是不是彻底好了？”

> 这是当前结果：
> [RESULT]
>
> 你帮我严格检查，这样是真的解决了吗？
> 还有没有需要验证的地方？

### “这个报错到底是什么意思？”

> 这是完整 error：
> [ERROR]
>
> 先给我人话解释：
> 它在哪一层、为什么发生、和我刚才哪个修改最可能有关。
> 然后再告诉我怎么验证。

### “你刚才是不是改太多了？”

> 我感觉刚才的改动范围太大。
> 重新告诉我最小必要改动是什么。
> 能不能先只改一个点，然后测试？

### “这个真的要现在做吗？”

> 这个东西到底是 MVP 必须，还是 production 才需要？
> 现在还剩 [TIME]。
> 请直接告诉我 DO NOW / LATER / CODE REVIEW ONLY。

### “我现在有点乱，你帮我重新整理。”

> 先不要继续开发。
> 把当前状态重新整理成：
> 已完成 / 未完成 / blocker / 下一步 / success criteria。
> 只保留最重要的。

### “我是不是理解错了？”

> 我的理解：
> [MY UNDERSTANDING]
>
> 哪里错了直接指出。
> 不要为了完整重新讲一遍。

### “这个通过以后我才能做下一步，对吗？”

> 请明确告诉我当前 checkpoint。
> 什么条件全部满足以后才能进入下一阶段？

---

# 四十、最推荐的现场循环

整个三小时最推荐一直重复：

```text
AI 给当前一步
        ↓
我理解为什么
        ↓
创建/修改最少文件
        ↓
运行
        ↓
测试/请求验证
        ↓
把输出给 AI
        ↓
AI 判断 PASS / NOT PASS
        ↓
如果失败：root cause → 最小修复 → 重测
        ↓
如果通过：下一步
```

而不是：

```text
给 AI 一整道题
        ↓
让 AI 一次生成完整项目
        ↓
祈祷能运行
```

---

# 四十一、我什么时候应该主动打断 AI

出现任何一个情况就打断：

- 一次创建很多文件
- 突然引入 Redis/Kafka/Celery
- 没测试就继续加功能
- 一个 bug 连续 patch 三次
- 改了 unrelated code
- 解释不了它生成的代码
- deployment 还没打通却不停加 feature
- 剩 60 分钟还在扩大 scope
- AI 说“production best practice”但没有考虑三小时时间

直接说：

> 停。先不要继续。
> 重新根据 3 小时时间限制判断当前最小必要动作。

---

# 四十二、最短总控 Prompt

如果现场只能复制一段，就用这个：

> 这是一个 3 小时 coding interview。
>
> 请用中文作为我的 senior pair programmer 和 implementation guide。
>
> 先给完整 roadmap，但执行时一次只带我做一个步骤。
>
> 每一步必须告诉我：
> - 当前目标
> - 为什么现在做
> - 创建/修改哪个文件
> - 最小代码
> - 运行什么命令
> - 怎么测试
> - 什么结果算 PASS
>
> 当前步骤没有验证通过前，不要进入下一步。
>
> 如果报错，先 root cause，不要随机改。
> 每次修改后告诉我重新跑什么。
> 随时根据剩余时间砍 scope。
>
> 所有解释用中文；代码、文件、API、tests、README 保持英文。
>
> 我负责最终技术判断。

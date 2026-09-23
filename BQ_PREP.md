# DigitalOcean Behavioral 面试准备（45 分钟，全双语）

**这份材料的用法**：
1. 先读第 1 节（这一轮怎么进行、满分回答的方法）
2. 再读第 3 节（你的故事库），把 6 个核心故事讲熟
3. 然后按题目看，每道题都有：回答思路、满分答案（英文 + 中文翻译）、追问和追问的答案
4. 第 9 节是模板，用来把**你还没告诉我的故事**套进去

**重要提醒**：我只用了你告诉过我的真实经历和数字。标了【需要你补充】的地方，一定填你自己的真实细节，**不要编**。行为面试最怕被追问两层就露馅。

---

## 第 1 节：这一轮怎么进行

**面试官**：hiring team（招聘团队的人，可能是未来的经理或同事）。

**45 分钟大概这样分**：
开场寒暄和自我介绍：5 分钟
4 到 6 个行为问题，每个都会追问：30 分钟
你问他们问题：5 到 10 分钟

**他们在评估什么**：你的经历是否体现 DO 的七个价值观（邮件里写的：Bold、Fast、Learning、Simple、Love、Community、Proud）。

### 满分回答的结构：STAR + R

| 字母 | 英文 | 中文 | 占多少时间 |
|---|---|---|---|
| S | Situation | 背景：在哪、什么项目 | 15% |
| T | Task | 你的任务或面临的问题 | 10% |
| A | Action | **你具体做了什么** | **50%** |
| R | Result | 结果，最好有数字 | 15% |
| R | Reflection | 你学到了什么、下次怎么做 | 10% |

### 五条规则

**一、每个回答 1.5 到 2 分钟。**太短显得没内容，太长面试官会走神。

**二、用 "I" 不用 "We"。**面试官要知道**你**做了什么。团队做的事可以提，但重点放在你的部分。
错误：*"We built a pipeline..."*
正确：*"I built the pipeline. My teammate handled the dashboard."*

**三、Action 部分要讲"为什么这么做"。**不只是"我做了 X"，而是"我做了 X，因为我发现 Y"。这是展示判断力的地方。

**四、结果要有数字。**你的经历里数字很多，全都用上。

**五、结尾加一句反思。**"What I learned was..." 这一句会让回答从"及格"变成"优秀"。

### 追问（follow-up）一定会有

行为面试的追问是在**验证你是不是真的做过**，以及**挖你的思考深度**。最常见的追问：

| 追问（英文） | 中文 | 他在看什么 |
|---|---|---|
| What was the hardest part? | 最难的部分是什么？ | 你是不是亲自做的 |
| Why did you choose that approach? | 为什么选这个方法？ | 判断力 |
| What would you do differently? | 如果重来你会怎么做？ | 反思能力 |
| How did others react? | 别人怎么反应的？ | 协作和沟通 |
| What if it hadn't worked? | 如果没成功呢？ | 应变能力 |
| How did you measure success? | 你怎么衡量成功？ | 结果导向 |
| What did you learn? | 你学到了什么？ | 成长心态 |

**应对追问的心法**：追问说明面试官感兴趣，是好事。**实话实说，细节越具体越可信。**不记得就说不记得，不要编。

---

## 第 2 节：DO 七个价值观（官方定义翻译）

来自 DO 官网：

**Bold（大胆）**：我们敢想敢做，不怕打破现状、挑战常规思维，突破边界去想 10 倍的可能。

**Fast（快速）**：我们以行动为先。快速行动、适应变化、抓住机会。**速度和进展比完美更重要。**

**Learning（学习）**：我们拥抱成长型思维，鼓励好奇、敢想、快速学习。

**Simple（简单）**：客户喜欢我们，因为我们简单易用。我们让 AI 和 ML 应用开发在 DO 上变得容易。

**Love（热爱客户）**：客户和社区是我们一切工作的核心。我们执着于理解他们的需求、预判他们的困难。

**Community（社区）**：开发者社区是我们的核心，他们的热情和专业推动平台成长。

**Proud（自豪 / 主人翁精神）**：我们像主人一样行事，以行动为先，对客户、产品、同事和决策有强烈的责任感。

### 每个价值观对应你的哪个故事

| 价值观 | 你最好的故事 | 在第几节 |
|---|---|---|
| Simple | nOps：把算术从模型移到 SQL | 4.1 |
| Bold | ViiVAI：推翻"VLM 能直接输出运动轨迹"的设计假设 | 4.2 |
| Fast | nOps：权限故障时当天定位并升级，断点续跑不丢进度 | 4.3 |
| Learning | nOps：从零上手 Databricks，发现 10 倍重复计数 | 4.4 |
| Love | nOps：一个错误数字毁掉用户信任，于是重新设计 | 4.5 |
| Community | ViiVAI：做了录制回放客户端和单元测试，让团队能低成本测试 | 4.6 |
| Proud | ViiVAI：主动发现数据泄漏，报告更低但真实的指标 | 4.7 |

---

## 第 3 节：你的故事库

先把这几个故事的**事实**记住（中文），英文答案在后面各题里。

### 故事 A：nOps，一个错误的数字（Simple / Love）

**背景**：nOps 实习，做 FinOps 助手 Clara，用 LLM 解释云成本异常。
**问题**：第一版让模型直接算数，它输出了一个 62.6 万美元的年化成本数字，是错的。一个错误数字就让用户对整个工具失去信任。
**你做了什么**：把所有算术从模型里移出来，交给确定性的 SQL 计算；模型只负责判断和解释。还建了一个 grounding checker，把模型输出的每个数字对照源数据校验。
**结果**：每个数字都可验证、可追溯。

### 故事 B：nOps，10 倍重复计数（Learning）

**背景**：处理 AWS 账单数据，超过 50 亿条记录，你之前没用过 Databricks。
**问题**：成本数字对不上。
**你做了什么**：一层层排查，发现 Kubernetes pod 的成本分摊导致同一笔费用被重复计算，最高到 10 倍。
**结果**：修正后数据可信，后续的异常检测才有意义。

### 故事 C：nOps，一次成本变化被报了 28 天（Simple / Proud）

**问题**：30 天滚动基线让同一次永久性的成本上涨，被连续 28 天重复判定为异常。
**你做了什么**：做了 episode 聚合，把连续的异常时段合并成一个事件；基线按服务 × 小时 × 工作日/周末分组，用中位数和 MAD。
**结果**：9050 万个小时级异常压缩成 3300 个事件。

### 故事 D：nOps，并发标注服务与权限故障（Fast）

**背景**：用 AWS Bedrock 给 6000 个事件打标签，8 个并发 worker。
**你做了什么**：按错误类型区分退避（限流错误退避更久），滚动窗口失败率熔断（最近 20 次失败率超过 50% 就停），每 100 条存一次 checkpoint，结果按原始顺序写回。
**一个插曲**：跑到中途出现权限错误。你没有盲目重试，而是定位到是 IAM 策略被回滚了，当天升级给 manager。因为有 checkpoint，恢复后只补跑缺失部分。

### 故事 E：ViiVAI，数据泄漏（Proud / Learning）

**背景**：ViiVAI，压力垫姿态识别，11.4 万帧数据。
**问题**：发现评估方式有数据泄漏，同一个人的数据同时出现在训练集和测试集，分数虚高。
**你做了什么**：改成 leave-one-subject-out（每次留一个人完全不参与训练，只用来测试）的评估方式；做了几何教师模型（LoG）和 20 个用例的回归测试集。
**结果**：在未见过的人身上 100% 检出；PostureNet（350 万参数）从 62.5% 提升到 81.8%。
【需要你补充：泄漏被修正前后分数差了多少、你是怎么跟 Ali 汇报的】

### 故事 F：ViiVAI，推翻一个设计假设（Bold）

**背景**：Agent Hayward，多智能体 LLM 流水线，为视频生成触觉内容。
**问题**：原设计假设 VLM（视觉语言模型）能直接返回物体运动轨迹。你发现它的输出尺寸始终不变，说明它在"估计"而不是"测量"。
**你做了什么**：提出这个假设不成立，重构了视频处理路径，加了三级追踪器降级方案。
**结果**：【需要你补充：重构后效果】
【需要你补充：这个假设是谁定的，你是怎么提出反对的，对方怎么反应】

### 故事 G：ViiVAI，静默失效的 bug 和测试基础设施（Community / Learning）

**你做了什么**：发现合并顺序的 bug 让跨模态优先级规则静默失效（不报错但不生效）；写了 38 个单元测试；做了可插拔的客户端，支持录制和回放 API 调用，测试时不用真的调用付费 API。

### 故事 H：grounding checker 自己有 bug（失败 / 犯错）

**问题**：你建的数字校验器本身有 bug，放过了应该拦截的错误输出。
**你做了什么**：加了注入测试，故意喂错误输入，确认检查器能抓住。
**反思**：验证工具本身也需要被验证。

### 其他经历（细节需要你补充）

**EdgeDiffuse 毕设**：6 人团队，模型压缩到约 2.18 亿参数（减少 25.3%），W8A16 量化加速 2.69 倍，跨 PyTorch → ONNX → RKNN 三个运行时移植并排查算子不兼容。
**两段实习并行**：nOps 兼职和 ViiVAI 同时进行。
**Valve（南京）**：【需要你补充】
**云南大学 deepfake 检测**：IWADI 2024 论文，97.3% / 92.1%。

---

## 第 4 节：价值观题（最可能被问）

---

### 4.1 Simple：简化复杂问题

**题目**：
> Tell me about a time you simplified something complex.

中文：讲一次你把复杂的东西变简单的经历。

**变体**：*"Tell me about a time you chose a simpler solution over a more sophisticated one."*（讲一次你选了简单方案而不是复杂方案的经历。）

**回答思路**：用故事 A。重点是"不是让模型更聪明，而是让它少做事"，这正是 Simple 的精神。

**满分答案**：

> "At nOps, I was building an assistant that explains cloud cost anomalies using an LLM."

中文：在 nOps，我在做一个用 LLM 解释云成本异常的助手。

> "In the first version, the model did the math itself. It produced an annualized cost of 626,000 dollars that was simply wrong. And one wrong number was enough to make users stop trusting the whole tool."

中文：在第一版里，模型自己做计算。它算出了一个 62.6 万美元的年化成本，而这个数字是错的。一个错误的数字就足以让用户不再信任整个工具。

> "The obvious fix was to make the model better at math, with better prompts or a bigger model. I went the other way. I moved all arithmetic out of the model into deterministic SQL, and the model only did what it's good at: judgment and explanation."

中文：显而易见的修法是让模型算得更好，比如改进 prompt 或者换更大的模型。我反其道而行之：我把所有计算都从模型里移到确定性的 SQL 里，模型只做它擅长的事：判断和解释。

> "I also built a grounding checker that verifies every number in the output against the source data."

中文：我还做了一个 grounding checker，把输出里的每个数字都和源数据核对。

> "As a result, every number became traceable and verifiable. What I learned is that the simplest reliable system often comes from giving each component less to do, not from making one component smarter."

中文：结果是每个数字都变得可追溯、可验证。我学到的是：最简单可靠的系统，往往来自让每个组件做更少的事，而不是让某一个组件变得更聪明。

**追问 1**：
> Why not just use a better model?

中文：为什么不直接换一个更好的模型？

> "Even a better model would still be probabilistic. It might be right 99% of the time, but users can't tell which 1% is wrong. SQL gives the same answer every time, and anyone can check it."

中文：就算换更好的模型，它依然是概率性的。它可能 99% 的时候是对的，但用户分不出哪 1% 是错的。SQL 每次都给出同样的答案，而且任何人都能检查。

**追问 2**：
> Did anyone disagree with that approach?

中文：有人不同意这个做法吗？

【需要你补充真实情况。如果没有明显反对，可以这样说：】

> "Not strongly, but it did mean more upfront work, because I had to write the SQL for each calculation. I explained it in terms of trust: one wrong number costs more than the time to write the query."

中文：没有强烈反对，但这意味着前期工作更多，因为每种计算我都要写 SQL。我是从信任的角度解释的：一个错误数字的代价，比写一个查询的时间大得多。

**追问 3**：
> How did you know the grounding checker itself was correct?

中文：你怎么知道 grounding checker 本身是对的？

> "Good question, and actually it wasn't at first. I found a bug where it let through outputs it should have flagged. So I added injection tests: I deliberately fed it wrong numbers to make sure it catches them."

中文：好问题，而且一开始它确实不对。我发现了一个 bug，它放过了本应拦截的输出。所以我加了注入测试：故意喂给它错误的数字，确保它能抓住。

（这个追问正好接到故事 H，非常加分。）

---

### 4.2 Bold：挑战现状 / 反对意见

**题目**：
> Tell me about a time you challenged an assumption or pushed back on a decision.

中文：讲一次你挑战某个假设、或者反对某个决定的经历。

**变体**：*"Tell me about a time you disagreed with your team or manager."*（讲一次你和团队或经理意见不同的经历。）

**回答思路**：用故事 F。重点是**用证据说话，而不是凭感觉反对**。然后讲你怎么提出、对方怎么接受。

**满分答案**：

> "At ViiVAI, I worked on a multi-agent pipeline that generates haptic effects from video."

中文：在 ViiVAI，我参与做一个多智能体流水线，从视频生成触觉效果。

> "The original design assumed a vision-language model could return object motion trajectories directly. The whole video path was built on that assumption."

中文：原来的设计假设视觉语言模型可以直接返回物体的运动轨迹。整个视频处理路径都是建立在这个假设上的。

> "While testing, I noticed something odd: the sizes it returned were almost constant, no matter how the object moved. That told me the model was estimating, not measuring. It was producing plausible-looking numbers without tracking anything."

中文：测试时我注意到一个奇怪的现象：不管物体怎么动，它返回的尺寸几乎是不变的。这说明模型是在估计，而不是在测量。它在输出看起来合理的数字，但实际上什么都没追踪。

> "I brought this to [需要你补充：Ali / 团队] with the evidence: the outputs side by side with the actual motion. I proposed restructuring the video path to use a real tracker, with a three-level fallback when tracking fails."

中文：我带着证据找了 [Ali / 团队]：把模型输出和真实运动并排对比。我提议重构视频路径，改用真正的追踪器，并在追踪失败时有三级降级方案。

> "[需要你补充：结果，比如团队同意了、重构后效果如何]"

> "What I learned is that challenging a design is much easier when you bring evidence instead of opinions. Nobody argued with the data."

中文：我学到的是：带着证据而不是观点去挑战一个设计，会容易得多。没有人会和数据争论。

**追问 1**：
> How did you feel about pushing back on the original design?

中文：反对原来的设计时你心里是什么感受？

> "A bit nervous, because a lot of work was already built on it. But I thought it was worse to keep building on something I knew was broken. Raising it early was cheaper than finding out later."

中文：有点紧张，因为很多工作已经建立在它上面了。但我觉得在明知有问题的东西上继续建更糟。早点提出来，比以后才发现代价小得多。

**追问 2**：
> What if they had disagreed with you?

中文：如果他们不同意你呢？

> "I would have suggested a small experiment: run both approaches on a few videos and compare. If the data showed I was wrong, I'd accept that. The goal isn't to win the argument, it's to get the right answer."

中文：我会建议做一个小实验：在几个视频上跑两种方法对比。如果数据证明我错了，我会接受。目的不是赢得争论，而是得到正确的答案。

**追问 3**：
> What's the three-level fallback?

中文：三级降级方案是什么？

【需要你补充具体三级是什么。结构可以这样说：】

> "If the primary tracker loses the object, it falls back to [第二级], and if that also fails, to [第三级]. The point is that the pipeline degrades gracefully instead of failing completely."

中文：如果主追踪器跟丢了物体，就降级到 [第二级]；如果那个也失败了，再降级到 [第三级]。关键是流水线会平滑降级，而不是彻底失败。

---

### 4.3 Fast：快速行动 / 压力下的决策

**题目**：
> Tell me about a time you had to act quickly without complete information.

中文：讲一次你在信息不完整的情况下必须快速行动的经历。

**变体**：*"Tell me about a time something broke and you had to fix it fast."*（讲一次东西坏了你必须快速修好的经历。）

**回答思路**：用故事 D。重点是**快不等于乱**：你没有盲目重试，而是快速定位根因、立刻升级，同时因为事先设计了断点续跑，没有损失进度。

**满分答案**：

> "At nOps, I built a service that labeled 6,000 cost events using AWS Bedrock, with 8 concurrent workers."

中文：在 nOps，我做了一个服务，用 AWS Bedrock 给 6000 个成本事件打标签，8 个 worker 并发运行。

> "Partway through a run, calls started failing with a permission error. The easy reaction would be to retry, but retrying a permission error never helps. It just burns time."

中文：跑到一半，调用开始报权限错误。最容易的反应是重试，但权限错误重试永远没用，只是浪费时间。

> "So I stopped the run and looked at what had changed. I traced it to an IAM policy that had been rolled back. That's not something I could fix myself, so I escalated it to my manager the same day, with the exact policy and the error."

中文：所以我停下运行，去查什么东西变了。我定位到是一个 IAM 权限策略被回滚了。这不是我自己能修的，所以我当天就升级给了经理，附上具体是哪个策略和错误信息。

> "Because I had designed the service to checkpoint every 100 events, nothing was lost. Once the policy was restored, it resumed and only processed what was missing."

中文：因为我设计服务时每 100 个事件存一次进度，所以什么都没丢。策略恢复后，服务接着跑，只处理缺失的部分。

> "What I took from it: moving fast isn't about reacting fast. It's about telling quickly what's worth retrying and what isn't, and building things so a failure doesn't cost you everything."

中文：我的收获是：快速行动不是快速反应。而是能快速判断什么值得重试、什么不值得，并且让系统设计成失败时不会让你损失全部。

**追问 1**：
> How did you know it was a permission error and not something else?

中文：你怎么知道是权限错误而不是别的问题？

> "The service classified errors by type. Throttling, timeouts, and truncated outputs each had their own handling. This one was an access-denied error, which is a different category. It's not transient, so the service shouldn't keep trying."

中文：服务会按类型区分错误。限流、超时、输出截断各有各的处理方式。这次是访问被拒绝的错误，属于另一类。它不是暂时性的，所以服务不应该一直重试。

**追问 2**：
> Tell me more about how you handled different errors.

中文：多讲讲你怎么处理不同的错误。

> "Throttling errors got a longer backoff than other errors. Truncated outputs were recovered by raising the token limit in stages. And for the circuit breaker, I used a rolling failure rate over the last 20 calls instead of counting consecutive failures."

中文：限流错误的退避时间比其他错误更长。输出被截断的情况通过分阶段提高 token 上限来挽救。熔断方面，我用最近 20 次调用的滚动失败率，而不是数连续失败次数。

> "With 8 concurrent workers, successes and failures interleave, so you might never see 5 failures in a row even during a full outage."

中文：因为有 8 个 worker 并发，成功和失败是交错的，所以就算完全宕机，也可能永远看不到连续 5 次失败。

**追问 3**：
> What would you do differently?

中文：如果重来你会怎么做？

> "I'd add an alert that fires on the first access-denied error, instead of noticing it from the logs. Permission errors should stop the run immediately and notify someone."

中文：我会加一个告警，第一次出现访问被拒绝就触发，而不是靠看日志才发现。权限错误应该立刻停止运行并通知人。

---

### 4.4 Learning：快速学习新东西

**题目**：
> Tell me about a time you had to learn something new quickly.

中文：讲一次你必须快速学会新东西的经历。

**回答思路**：用故事 B。重点是"边学边发现问题"，学习不是看教程，而是在真实问题里学会的。

**满分答案**：

> "When I joined nOps, I had never used Databricks, and I had to work with AWS billing data at the scale of over five billion records."

中文：刚加入 nOps 时，我从来没用过 Databricks，而我要处理超过 50 亿条的 AWS 账单数据。

> "I didn't start with tutorials. I started with a question I needed to answer: do the cost totals match what AWS reports? Learning the tool around a real question was much faster for me."

中文：我没有从看教程开始，而是从一个必须回答的问题开始：成本总额和 AWS 报告的一致吗？围绕一个真实问题去学工具，对我来说快得多。

> "They didn't match. I broke the data down layer by layer and found that Kubernetes pod cost allocation was counting the same spend multiple times, up to ten times in some cases."

中文：结果对不上。我一层一层拆解数据，发现 Kubernetes pod 的成本分摊把同一笔费用重复计算了多次，有些情况下高达 10 倍。

> "After fixing that, I built a seven-layer hourly pipeline on top of the corrected data."

中文：修正之后，我在正确的数据基础上搭建了一个七层的小时级数据管道。

> "What I learned is that when you're new to a system, the most valuable habit is checking totals against an independent source. The tool was new, but that habit caught a bug that would have made everything downstream wrong."

中文：我学到的是：当你刚接触一个系统时，最有价值的习惯是拿总数和一个独立来源对账。工具是新的，但这个习惯抓住了一个会让下游所有结果都出错的 bug。

**追问 1**：
> How did you find the double counting?

中文：你是怎么发现重复计数的？

> "I compared totals at each layer against the raw billing export. The numbers matched until the step where pod costs were allocated. That narrowed it down to one join."

中文：我把每一层的总数和原始账单导出数据对比。一直都对得上，直到分摊 pod 成本的那一步。这样就把问题缩小到了一个 join（表连接）上。

**追问 2**：
> How do you usually learn new technologies?

中文：你通常怎么学新技术？

> "I start from a concrete problem, read just enough documentation to make progress, and verify each step against something I trust. I also moved a model across three runtimes in my capstone, PyTorch to ONNX to RKNN, and learned each one by debugging where operators weren't supported."

中文：我从一个具体问题出发，只读够推进用的文档，每一步都和我信任的东西对照验证。我在毕设里也把一个模型跨三个运行时移植过，从 PyTorch 到 ONNX 再到 RKNN，每一个都是通过调试"哪些算子不支持"学会的。

---

### 4.5 Love：以客户为中心

**题目**：
> Tell me about a time you focused on the user or customer's needs.

中文：讲一次你以用户或客户需求为中心的经历。

**变体**：*"How do you make sure what you build is actually useful?"*（你怎么确保你做的东西真的有用？）

**回答思路**：可以用故事 A 从"用户信任"的角度讲，也可以用故事 C（用户不想被重复告警轰炸）。**如果前面已经讲过故事 A，这里用故事 C。**

**满分答案（故事 C 版本）**：

> "At nOps, the users were FinOps teams who look at cost anomalies and decide what to act on."

中文：在 nOps，用户是 FinOps 团队，他们看成本异常，然后决定要处理哪些。

> "I noticed a problem from their point of view. When a cost went up permanently, say a new service was launched, our 30-day rolling baseline flagged it as a new anomaly every single day for 28 days."

中文：我从他们的角度发现了一个问题。当某项成本永久性地上升了，比如上线了一个新服务，我们的 30 天滚动基线会连续 28 天每天都把它标成新的异常。

> "For a user, that's 28 alerts for one event. They would learn to ignore the tool."

中文：对用户来说，这是一件事收到 28 条告警。他们会学会无视这个工具。

> "So I merged consecutive anomalous periods into single episodes, and I made baselines time-aware, grouped by service, hour of day, and weekday versus weekend. That reduced 90.5 million hourly anomaly flags to about 3,300 episodes."

中文：所以我把连续的异常时段合并成一个"事件"，并且让基线考虑时间因素，按服务、一天中的小时、工作日还是周末分组。这把 9050 万个小时级异常标记减少到了大约 3300 个事件。

> "I also excluded a 113,000-dollar-per-year pattern that looked like an anomaly but was just a pricing tier resetting. Showing it would have been technically correct but misleading."

中文：我还排除了一个每年 11.3 万美元的模式，它看起来像异常，但其实只是价格档位重置。把它展示出来技术上没错，但会误导用户。

> "What I learned is that for an alerting product, every false alarm spends a bit of the user's trust."

中文：我学到的是：对于告警类产品，每一次误报都在消耗用户的一点信任。

**追问 1**：
> Did you talk to users directly?

中文：你直接和用户交流过吗？

【如实回答。如果没有直接接触：】

> "Not directly as an intern. I got their perspective through my manager and by using the tool the way they would, going through the alerts one by one. That's how the 28-day repeat became obvious."

中文：作为实习生没有直接接触。我通过经理了解他们的视角，并且像用户那样去使用这个工具，一条一条地看告警。28 天重复的问题就是这样变得明显的。

**追问 2**：
> Why median and MAD instead of mean and standard deviation?

中文：为什么用中位数和 MAD，而不是平均值和标准差？

> "Cost data has spikes. A single big spike pulls the mean and standard deviation a lot, which makes the baseline less sensitive right after. Median and MAD are robust to outliers."

中文：成本数据有尖峰。一个大尖峰会把平均值和标准差拉偏很多，导致之后的基线变得不敏感。中位数和 MAD 对异常值更稳健。

（MAD 是中位数绝对偏差，一种不受极端值影响的波动度量。）

---

### 4.6 Community：团队协作 / 帮助他人

**题目**：
> Tell me about a time you helped a teammate or made the team more effective.

中文：讲一次你帮助队友、或者让团队更高效的经历。

**回答思路**：用故事 G。重点是你做的东西**让别人受益**。如果你有 EdgeDiffuse 团队里帮助队友的真实例子，那个更贴切。

**满分答案（故事 G 版本）**：

> "At ViiVAI, our multi-agent pipeline called paid model APIs on every run. That made testing slow and expensive, so people tested less."

中文：在 ViiVAI，我们的多智能体流水线每跑一次都要调用付费的模型 API。这让测试又慢又贵，所以大家测得越来越少。

> "I built a pluggable client that can record real API responses once and replay them later. Anyone on the team could run the full pipeline locally, for free, with the same results every time."

中文：我做了一个可插拔的客户端，可以把真实的 API 响应录制一次，之后反复回放。团队里任何人都可以在本地免费跑完整的流水线，而且每次结果都一样。

> "I also wrote 38 unit tests. One of them caught a merge-order bug that had silently disabled a cross-modal priority rule. It didn't crash, it just quietly stopped working."

中文：我还写了 38 个单元测试。其中一个抓到了一个合并顺序的 bug，它让一个跨模态优先级规则静默失效了。程序没崩溃，只是悄悄地不起作用了。

> "[需要你补充：队友怎么用了这个工具、效果如何]"

> "What I learned is that making testing cheap changes how often people test. The tooling mattered as much as the tests."

中文：我学到的是：让测试变便宜，会改变大家测试的频率。工具本身和测试一样重要。

**追问 1**：
> How did you find a bug that doesn't crash?

中文：一个不会崩溃的 bug 你是怎么发现的？

> "The test checked the output, not just that the code ran. It expected the visual signal to take priority in a specific case, and it didn't. That's why I prefer tests that assert behavior, not just 'no exception'."

中文：测试检查的是输出结果，而不只是代码能跑。它期望在某个特定情况下视觉信号优先，结果没有。这就是为什么我更喜欢断言行为的测试，而不只是"没报错"。

**追问 2**：
> Tell me about working on a larger team.

中文：讲讲你在更大团队里工作的经历。

> "In my capstone, I was on a team of six compressing a diffusion model for an edge device. [需要你补充：你负责哪部分、怎么和队友分工和同步、有没有帮过谁]"

中文：在毕设里，我在一个 6 人团队里，把一个扩散模型压缩到边缘设备上运行。[需要你补充]

---

### 4.7 Proud：主人翁精神 / 端到端负责

**题目**：
> Tell me about a time you took ownership beyond what was asked.

中文：讲一次你承担了超出要求的责任的经历。

**变体**：*"Tell me about a project you're most proud of."*（讲一个你最自豪的项目。）

**回答思路**：用故事 E。这个故事很强，因为它体现了**诚信**：你主动发现了一个让分数变好看的问题，并且报告了更低但真实的数字。

**满分答案**：

> "At ViiVAI, I worked on classifying sitting posture from pressure-mat data, about 114,000 frames."

中文：在 ViiVAI，我做基于压力垫数据的坐姿分类，大约 11.4 万帧。

> "The early results looked great. But I noticed the evaluation split frames randomly, so frames from the same person were in both training and testing. The model could recognize the person instead of the posture."

中文：早期结果看起来很好。但我注意到评估时是随机划分帧的，所以同一个人的帧同时出现在训练集和测试集里。模型可能是在认人，而不是在认姿势。

> "Nobody had asked me to question the evaluation. But if we shipped based on those numbers, it would fail on every new user."

中文：没有人要求我去质疑评估方式。但如果我们基于那些数字上线，产品在每一个新用户身上都会失败。

> "So I switched to leave-one-subject-out evaluation, where each person is held out completely. The honest numbers were lower [需要你补充：具体数字]. I reported them and explained why."

中文：所以我改用 leave-one-subject-out 评估，每次把一个人完全排除在训练之外。真实的数字更低 [需要你补充]。我如实汇报了，并解释了原因。

> "Then I worked on closing the gap. I built a geometric teacher model and a 20-case regression suite. Under the honest evaluation, the model improved from 62.5% to 81.8%, and the geometric pipeline detected 100% of cases on unseen subjects."

中文：然后我着手缩小差距。我做了一个几何教师模型和一套 20 个用例的回归测试。在真实的评估方式下，模型从 62.5% 提升到 81.8%，几何流水线在没见过的人身上检出率 100%。

> "I'm proud of it because the most important decision wasn't a model change. It was choosing to report a worse number because it was the true one."

中文：我为它自豪，因为最重要的决定不是改模型，而是选择报告一个更差的数字，因为它是真实的。

**追问 1**：
> How did your manager react to the lower numbers?

中文：你的经理对更低的数字是什么反应？

【需要你补充真实反应。如果是正面的：】

> "[Ali] appreciated it, because the whole point of the product is working on new users. A high number that doesn't hold up is worse than no number."

中文：[Ali] 很认可，因为这个产品的意义就在于对新用户有效。一个站不住的高分比没有分数更糟。

**追问 2**：
> What's a geometric teacher?

中文：几何教师模型是什么？

> "Instead of learning everything from data, it uses the physical shape of the pressure pattern, like where the pressure peaks are, to derive labels and features. I used a Laplacian of Gaussian filter to find those peaks. It gives the neural network structured guidance, which helps when you don't have many subjects."

中文：它不是完全从数据里学，而是利用压力分布的物理形状，比如压力峰值在哪里，来推导标签和特征。我用高斯拉普拉斯（LoG）滤波来找这些峰值。它给神经网络提供了结构化的指导，在受试者不多的时候很有帮助。

---

## 第 5 节：开场三题（几乎一定会问）

---

### 5.1 自我介绍

**题目**：
> Tell me about yourself. / Walk me through your background.

中文：介绍一下你自己。 / 讲讲你的背景。

**回答思路**：60 到 90 秒。**现在 → 过去 → 为什么在这里**。不要从出生讲起，也不要念简历。

**满分答案**：

> "I'm a master's student in Electrical and Computer Engineering at the University of Washington, graduating in June 2027."

中文：我是华盛顿大学电子与计算机工程的硕士生，2027 年 6 月毕业。

> "Over the past few months, I've done two internships in parallel. At nOps, a cloud cost company, I built data pipelines over billions of AWS billing records and an LLM-based assistant that explains cost anomalies. At ViiVAI, I've worked on a multi-agent pipeline and on posture recognition from sensor data."

中文：过去几个月，我同时做了两段实习。在云成本公司 nOps，我在数十亿条 AWS 账单记录上搭建了数据管道，还做了一个基于 LLM 解释成本异常的助手。在 ViiVAI，我做了一个多智能体流水线，以及基于传感器数据的姿态识别。

> "Across both, the part I enjoyed most wasn't the models. It was the engineering around them: retries, fallbacks, making sure numbers are correct, and making systems behave predictably when things go wrong."

中文：在这两段经历里，我最喜欢的部分不是模型本身，而是围绕模型的工程：重试、降级、确保数字正确，让系统在出问题时依然表现得可预测。

> "That's why I'm excited about DigitalOcean. You build infrastructure that developers rely on, where reliability and simplicity matter a lot."

中文：这就是为什么我对 DigitalOcean 很感兴趣。你们做的是开发者依赖的基础设施，可靠性和简洁性非常重要。

---

### 5.2 为什么选 DigitalOcean

**题目**：
> Why DigitalOcean?

中文：为什么选择 DigitalOcean？

**满分答案**：

> "Three reasons."

中文：三个原因。

> "First, simplicity. DigitalOcean is known for making the cloud easy for developers. In my own work, I've seen how much complexity hurts, like one wrong number destroying trust in a tool. I like building things that are simple to use and hard to misuse."

中文：第一，简洁。DigitalOcean 以让开发者轻松使用云而闻名。在我自己的工作里，我见过复杂性有多伤人，比如一个错误数字就毁掉了用户对工具的信任。我喜欢做简单易用、不容易被误用的东西。

> "Second, the direction toward AI inference. I have a background in ML and model compression, and I'd like to work on the infrastructure that makes AI practical for developers."

中文：第二，往 AI 推理方向的发展。我有机器学习和模型压缩的背景，我想做让开发者能真正用上 AI 的基础设施。

> "Third, this interview itself. Building and deploying something real in three hours with AI tools is very close to how I actually work. It told me the team values judgment and shipping, not just puzzles."

中文：第三，这场面试本身。用 AI 工具在三小时里构建并部署一个真实的东西，非常接近我实际的工作方式。这让我知道团队看重的是判断力和交付，而不只是解题。

---

### 5.3 为什么从 ML 转向 SWE

**题目**：
> Your background is quite ML-heavy. Why a software engineering role?

中文：你的背景偏机器学习，为什么申请软件工程岗位？

**满分答案**：

> "When I look at what I actually spent my time on, most of it was software engineering. At nOps, the hard problems were the data pipeline, concurrency, retries, and making outputs verifiable. At ViiVAI, it was the orchestrator, error handling, and tests."

中文：回顾我实际花时间做的事，大部分都是软件工程。在 nOps，难题是数据管道、并发、重试、让输出可验证。在 ViiVAI，是编排器、错误处理和测试。

> "The ML parts worked because the engineering around them was solid. That's the part I want to keep growing in."

中文：机器学习的部分之所以能跑通，是因为它周围的工程足够扎实。这正是我想继续成长的方向。

> "And my ML background is still useful here. More and more systems have a model somewhere inside them, and knowing how models fail helps me build systems around them."

中文：而且我的机器学习背景在这里依然有用。越来越多的系统内部都有模型，知道模型会怎么出错，能帮我围绕它们搭建系统。

---

## 第 6 节：经典通用题

---

### 6.1 失败 / 犯错

**题目**：
> Tell me about a mistake you made, or a time you failed.

中文：讲一次你犯的错误，或者失败的经历。

**回答思路**：用故事 H。**选一个真实的、有代价的错误，重点讲你怎么发现、怎么补救、之后改变了什么习惯。**不要选"我太追求完美"这种假失败。

**满分答案**：

> "At nOps, I built a grounding checker to verify that every number the LLM produced matched the source data. It was the safety net for the whole system."

中文：在 nOps，我做了一个 grounding checker，用来验证 LLM 输出的每个数字都和源数据一致。它是整个系统的安全网。

> "Later, I found that the checker itself had a bug. It was letting through some outputs it should have flagged. So for a while, I had more confidence in the system than it deserved."

中文：后来我发现检查器本身有 bug，它放过了一些本该拦截的输出。所以有一段时间，我对系统的信心超过了它实际应得的。

> "The mistake was that I tested the checker on good outputs and assumed it would catch bad ones. I never deliberately tested whether it fails when it should."

中文：我的错误在于：我只用正确的输出测试了检查器，就假设它能抓住错误的输出。我从来没有故意去测试它在该失败的时候会不会失败。

> "I fixed the bug and added injection tests: I deliberately feed it wrong numbers and assert that it flags them."

中文：我修复了 bug，并加了注入测试：故意喂给它错误的数字，断言它会把它们标出来。

> "Now I always ask: how would I know if this check stopped working? Every safety check needs a test that proves it can fail."

中文：现在我总是会问：如果这个检查失效了，我怎么会知道？每一个安全检查都需要一个测试来证明它确实能失败。

**追问**：
> What was the impact of the bug?

中文：这个 bug 造成了什么影响？

【需要你补充真实影响。如果影响有限：】

> "I caught it before it reached users, but it could have. That's what made me take it seriously."

中文：我在它影响到用户之前发现了，但它本来是可能影响到的。这就是我认真对待它的原因。

---

### 6.2 处理模糊的需求

**题目**：
> Tell me about a time you worked on something ambiguous.

中文：讲一次你处理模糊不清的任务的经历。

**满分答案**：

> "At nOps, my task was roughly 'detect cost anomalies'. But what counts as an anomaly wasn't defined. Is a price change an anomaly? A usage increase? A planned launch?"

中文：在 nOps，我的任务大致是"检测成本异常"。但什么算异常并没有定义。价格变化算吗？用量增加算吗？计划中的上线算吗？

> "Instead of waiting for a perfect definition, I made the ambiguity explicit. I decomposed every cost change into a price part and a quantity part, and attributed it hierarchically down to specific resources."

中文：我没有等一个完美的定义，而是把模糊性变得明确。我把每一次成本变化拆解成价格部分和用量部分，并逐层归因到具体资源。

> "That turned 'is this an anomaly?' into concrete questions the team could decide on, like: should a pricing tier reset count? We decided it shouldn't, which removed a 113,000-dollar-per-year false signal."

中文：这把"这算不算异常"变成了团队可以决定的具体问题，比如：价格档位重置算不算？我们决定不算，这去掉了一个每年 11.3 万美元的虚假信号。

> "What I learned is that with an ambiguous task, the first deliverable is often a clearer question."

中文：我学到的是：面对模糊的任务，第一个交付物往往是一个更清晰的问题。

---

### 6.3 时间紧 / 多任务并行

**题目**：
> Tell me about a time you had to manage competing priorities.

中文：讲一次你必须处理多个互相竞争的优先事项的经历。

**满分答案**：

> "This past summer, I did two internships at the same time: nOps part-time and ViiVAI, while also preparing for my program."

中文：今年夏天，我同时做了两段实习：nOps 兼职和 ViiVAI，同时还在为学业做准备。

> "What made it work was being strict about two things. First, I wrote down each week what 'done' meant for each project, so I didn't drift. Second, I built things so they could be interrupted, like checkpointing long jobs, so switching context didn't cost me progress."

中文：能做下来是因为我对两件事很严格。第一，我每周写下每个项目"完成"的标准是什么，这样不会跑偏。第二，我把东西设计成可以被打断的，比如长任务存断点，这样切换上下文不会让我丢失进度。

> "[需要你补充：一个具体冲突的例子，比如某周两边都有截止日期时你怎么取舍、怎么沟通的]"

> "I also sent written progress updates every week at nOps, which kept my manager informed without needing extra meetings."

中文：我在 nOps 每周都发书面进度更新，这样经理能了解进展，不需要额外开会。

【注意：只说你真的做过的。每周更新这一条如果属实就保留。】

---

### 6.4 你的弱点

**题目**：
> What's your biggest weakness? / What's an area you're working on?

中文：你最大的弱点是什么？ / 你正在改进哪方面？

**回答思路**：选一个**真实的、和工作相关的、你已经在改进的**弱点。下面两个选项，**选符合你真实情况的那个**。

**选项 A：过度验证，影响交付速度**

> "I tend to go deep on correctness. I want to verify every number, which sometimes slows down shipping."

中文：我倾向于在正确性上钻得很深，想验证每一个数字，有时候会拖慢交付。

> "I've been working on it by separating what must be correct from what can be good enough. For example, in a time-boxed build, I deploy a working version first, then add verification to the critical path only."

中文：我在改进的方法是：区分哪些必须正确、哪些够用就行。比如在限时的构建中，我先部署一个能跑的版本，然后只在关键路径上加验证。

**选项 B：英语口头表达**

> "English is my second language. My written English is solid, but in fast discussions I sometimes need a moment to find the precise words."

中文：英语是我的第二语言。我的书面英语没问题，但在快节奏的讨论中，我有时需要停一下来找准确的措辞。

> "I handle it by writing things down, like design notes and decisions in the README, and by not being afraid to say 'let me think for a second' before answering."

中文：我的应对方式是把东西写下来，比如设计笔记、README 里的决策记录；并且在回答前不怕说"让我想一下"。

---

### 6.5 你怎么使用 AI 工具（DO 特别关心）

**题目**：
> How do you use AI tools in your work?

中文：你在工作中怎么使用 AI 工具？

**满分答案**：

> "I use them a lot, but I treat their output as a draft, not an answer."

中文：我用得很多，但我把它们的输出当作草稿，而不是答案。

> "For boilerplate, like project structure, routes, and data models, AI saves a lot of time and the risk is low. For correctness-critical logic, I review every line and write tests that target exactly the guarantee I need."

中文：对于样板代码，比如项目结构、接口、数据模型，AI 能节省大量时间，风险也低。对于正确性至关重要的逻辑，我逐行审查，并写专门针对我需要的保证的测试。

> "My work at nOps was partly about this problem at the system level: LLMs produce confident outputs that can be wrong. So I built evaluation and grounding checks around them. I apply the same idea when I use AI to write code."

中文：我在 nOps 的工作，某种程度上就是在系统层面解决这个问题：LLM 会自信地输出可能是错的东西。所以我在它们周围建了评估和校验。我用 AI 写代码时也用同样的思路。

---

### 6.6 收到的反馈

**题目**：
> Tell me about a time you received critical feedback.

中文：讲一次你收到批评性反馈的经历。

**回答思路**：你告诉过我的一个真实例子：几位导师看了你的简历，说太偏 ML，应该突出工程。**但这是求职场景不是工作场景**，如果有工作中的反馈例子更好。

【需要你补充：工作中被经理或同事指出问题的真实例子。】

**如果用求职的例子**：

> "Recently, a few engineers I respect reviewed how I describe my work. Their feedback was that I was presenting myself as an ML person, when most of what I'd actually done was engineering."

中文：最近，几位我很尊重的工程师看了我怎么描述自己的工作。他们的反馈是：我把自己包装成了一个做机器学习的人，但我实际做的大部分是工程。

> "At first I resisted a bit, because ML felt like my identity. But when I looked at my work honestly, they were right. The retries, the fallbacks, the pipeline, those were the hard parts."

中文：一开始我有点抗拒，因为机器学习感觉像是我的身份标签。但当我诚实地审视自己的工作时，发现他们是对的。重试、降级、数据管道，那些才是难的部分。

> "It changed how I think about my direction, and it's part of why I'm applying for this role."

中文：这改变了我对自己方向的思考，也是我申请这个岗位的原因之一。

---

### 6.7 关于 nOps 实习提前结束（如果被问到）

**可能的问法**：
> Are you still at nOps? / Why did the internship end?

中文：你还在 nOps 吗？ / 实习为什么结束了？

**回答原则**：**如实、简短、中性、往前看**。不要抱怨，不要过度解释，一两句话说完就转到你做成了什么。

**模板**（把括号里换成真实原因）：

> "My internship at nOps wrapped up in September, a bit earlier than originally planned, [真实原因，一句话]. I'm glad I got to finish the main pieces of work before it ended, like the pipeline and the evaluation harness."

中文：我在 nOps 的实习在九月结束了，比原计划早一些，[真实原因]。我很高兴在结束前完成了主要的工作，比如数据管道和评估框架。

**注意**：如果简历或申请里写的是 "Present"（至今），被问到时如实说明已经结束即可，不要含糊。

---

## 第 7 节：你问面试官的问题（一定要问）

DO 把面试当作双向交流，**不问问题会减分**。准备 3 到 4 个，挑 2 个问。

> "What does a typical first few months look like for a new grad on this team?"

中文：团队里的应届生，最初几个月通常是怎样的？

> "How does the team use AI tools day to day? Has it changed how you do code review?"

中文：团队日常怎么使用 AI 工具？它改变了你们做 code review 的方式吗？

> "What's a recent project the team shipped that you're proud of?"

中文：团队最近上线的哪个项目让你觉得自豪？

> "What distinguishes engineers who do really well here?"

中文：在这里表现特别好的工程师，有什么共同特点？

> "How do you balance moving fast with reliability, since customers depend on the platform?"

中文：客户依赖你们的平台，你们怎么在快速迭代和可靠性之间平衡？

（最后一个问题直接连接 Fast 和 Love 两个价值观，面试官会喜欢。）

---

## 第 8 节：追问的通用应对

**追问一：结果不够好怎么办**

> "The result wasn't perfect. [说实话]. If I did it again, I would [具体改进]."

中文：结果并不完美。[说实话]。如果重来，我会 [具体改进]。

**追问二：细节不记得了**

> "I don't remember the exact number, but it was roughly [范围]. What I remember clearly is [你确定的部分]."

中文：我不记得确切数字了，但大概是 [范围]。我清楚记得的是 [你确定的部分]。

**追问三：被问到团队其他人做的部分**

> "That part was handled by [teammate]. My part was [你的部分], and I worked with them on [交接的地方]."

中文：那部分是 [队友] 负责的。我的部分是 [你的部分]，我和他们在 [交接的地方] 合作。

**追问四：同一个故事被从另一个角度问**

完全可以复用同一个故事，只要换重点。比如故事 A 可以讲 Simple（简化）、Love（用户信任）、Learning（验证习惯）三个角度。

> "I'll use the same project, but a different part of it."

中文：我还是用同一个项目，但讲它的另一个部分。

**追问五：听不懂问题**

> "Could you give me an example of what you mean?"

中文：您能举个例子说明您的意思吗？

---

## 第 9 节：把你还没告诉我的故事套进来

你说还有很多故事没告诉我，比如 Valve 的工作、deepfake 研究、毕设团队的协作。用下面的模板整理，每个故事 5 分钟就能准备好。

### 故事整理表

```
故事名称：
对应价值观（可以多个）：

S 背景（一句话）：
T 问题或任务（一句话）：
A 我做了什么（三到四个动作，每个都要有"因为"）：
  1. 我做了 ____，因为 ____
  2. 我做了 ____，因为 ____
  3. 我做了 ____，因为 ____
R 结果（最好有数字）：
R 反思（我学到了 ____）：

可能的追问：
  最难的部分是什么？
  如果重来会怎么做？
  别人怎么反应的？
```

### 英文句式模板（直接填空）

**开头（S）**：

> "At [company], I was working on [project], which [does what]."

中文：在 [公司]，我在做 [项目]，它的作用是 [做什么]。

**问题（T）**：

> "The problem was [problem]. This mattered because [why it matters]."

中文：问题是 [问题]。这很重要，因为 [为什么重要]。

**行动（A）**：

> "First, I [action], because I noticed [reason]."

中文：首先，我 [行动]，因为我注意到 [原因]。

> "Then I [action]. The tricky part was [difficulty]."

中文：然后我 [行动]。棘手的部分是 [难点]。

**结果（R）**：

> "As a result, [metric] went from [X] to [Y]."

中文：结果，[指标] 从 [X] 变成了 [Y]。

**反思（R）**：

> "What I learned is [lesson]. Since then, I [how you work differently]."

中文：我学到的是 [教训]。从那以后，我 [工作方式上的改变]。

### 值得补充的故事（如果你有的话）

**冲突故事**：和队友或经理意见不同，最后怎么解决的。这是必问题，你现在的故事 F 需要补充细节才完整。

**帮助别人的故事**：教过队友什么、帮谁解决过问题。

**Valve 的故事**：在工业环境里做 ML 的经历，可能有很好的"客户导向"素材。

**毕设团队故事**：6 人团队里的分工、协调、遇到的困难。

---

## 第 10 节：面试前最后检查

**必须能流利讲出来的**：
1. 自我介绍（60 到 90 秒）
2. 为什么选 DO
3. 故事 A（Simple）
4. 故事 E（Proud）
5. 故事 D（Fast）
6. 失败故事（故事 H）

**每个故事都要确认**：
用的是 "I" 不是 "We"
有具体数字
有一句反思
能答上"最难的部分是什么"

**心态**：你的故事都是真的、有细节的。面试官追问越深，越能看出你真的做过。**追问不是在为难你，是在给你展示的机会。**

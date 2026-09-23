# 3 小时 AI-Assisted Engineering Interview 私人作战手册

这是一个 **私人、通用、可复用的 interview workflow repository**。

它不是任何特定公司的真题答案，也不包含泄露题目。
用途是：在严格限时的 build interview 中，快速调用已经准备好的工作方法，减少临场认知负担。

---

## 我的核心原则

1. **我负责最终判断，AI 是 pair programmer / reviewer / project manager。**
2. 优先级：
   **正确性 > end-to-end working > 可部署 > 可解释 > 测试 > polish > 额外 feature**
3. 先做最小 vertical slice，再扩展。
4. 尽早验证 deployment，不要最后 10 分钟第一次部署。
5. 不 over-engineer。
6. 所有最终工程 artifact 使用英文：
   - code
   - identifiers
   - API
   - filenames in the actual interview project
   - comments/docstrings
   - tests
   - README
   - commit messages
7. 与 AI 的内部 reasoning 可以中文，以减少沟通时间和认知压力。
8. 如果现场规则与本仓库冲突，以现场规则为最高优先级。

---

## 我的默认技术路线

除非题目明确要求其他方案：

### Backend
- Python
- FastAPI（默认首选）
- RESTful JSON API
- Pydantic-style request / response validation
- 简单、明确的 error handling

### Persistence
- 优先 SQLite（如果满足 prototype）
- 如题目确实需要更完整 relational DB，再考虑 PostgreSQL / MySQL

### Testing
- pytest
- 优先验证：
  - happy path
  - invalid input
  - not found / conflict
  - core business rule
  - critical failure path

### Frontend
- 非必要不做复杂 frontend
- 如果必须有 UI：最小可用即可
- 不把时间浪费在视觉 polish

### Deployment
- 选择最简单、最熟悉、最少依赖的 path
- 早 deploy
- 给陌生环境留 buffer

### 架构风格
优先：

**simple + working + deployed + tested + explainable**

而不是：

**complex + impressive-looking + partially working**

---

## 推荐现场顺序

1. `00_开场与规则.md`
2. `01_我的技术背景与默认偏好.md`
3. `02_拿到题后的选题比较.md`
4. `03_三小时Scope与架构设计.md`
5. `04_180分钟时间计划.md`
6. `05_Cursor_Claude协作方式.md`
7. `06_实现阶段常用Prompt.md`
8. `07_Debug与RootCause.md`
9. `08_部署作战手册.md`
10. `09_中途时间重规划.md`
11. `10_最后45分钟冻结与检查.md`
12. `11_CodeReview持续记录模板.md`
13. `12_15分钟Break技术拷打准备.md`
14. `13_45分钟CodeReview模拟.md`
15. `14_没有中文输入法时的英文救命句.md`
16. `14A_没有中文输入法时_可直接复制的中文Prompt.md`
17. `15_最终项目README模板.md`
18. `16_行为面快速准备.md`

---

## 面试当天的一句话

**不要证明我能把系统做复杂。证明我能在约束下做出正确判断，并把一个完整东西 ship 出来。**

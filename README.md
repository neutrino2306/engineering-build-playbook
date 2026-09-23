# 3 小时私人作战手册

如果没有中文输入法 我就谷歌翻译算了  网页开一下 然后复制粘贴英文的
https://www.archchinese.com/type_chinese.html
---
## 陌生电脑上 到底要怎么设置中文输入法

如果对方电脑是 Windows 11，你现场想临时加中文输入法，通常不需要装第三方软件，直接开系统自带的 微软拼音 就行。

最稳的路径是：打开 Settings → Time & language → Language & region。在 “Preferred languages” 那里点 Add a language，搜索 Chinese (Simplified, China)，选中后安装。安装时重点保留语言基本包和键盘输入；不需要额外装语音、手写之类，除非系统自己强制带上。Windows 自带的简体中文输入法就是 Microsoft Pinyin。
Settings → Time & language → Language & region → Add a language → Chinese (Simplified, China) → Microsoft Pinyin → Win + Space
公司管理的电脑可能禁止下载语言包。 如果 Add a language 是灰的、要求管理员权限、或者下载一直失败，就别折腾太久。
有些机器其实已经有中文，只是没切出来。先按一次 Win + Space 看看，有可能直接就有。
如果出现中文输入法但打出来还是英文，点任务栏里的 中/英，或者按一下 Shift，微软拼音里 Shift 常用来切中英文状态。
不要为了装输入法浪费 10 分钟。你现场可以给自己设一个上限，比如 2–3 分钟。搞不定就直接切到你准备好的 fallback：Google Translate 语音转英文 → 复制给 Claude。

如果现场是 Mac，加系统自带中文拼音其实比 Windows 还直接，不需要安装搜狗。

按这个路径：
点左上角  Apple menu
打开 System Settings
左侧点 Keyboard
找到 Text Input
点旁边的 Edit
点左下角 +
搜索或选择 Chinese, Simplified
右侧选择 Pinyin - Simplified
点 Add
加完以后，菜单栏右上角应该会出现输入法图标。切换时一般直接用：
Control + Space
在英文和简体拼音之间切换。
 → System Settings → Keyboard → Text Input → Edit → + → Chinese, Simplified → Pinyin - Simplified
如果是受公司管理的 Mac，最坏情况可能是某些设置被锁，但添加系统自带 input source 通常比下载安装第三方输入法靠谱得多。拿到机器我建议先直接按一下 Control + Space，说不定中文拼音本来就已经装好了


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

# 05 Cursor + Claude 协作方式

目标：把陌生工具变成熟悉的“我和 Claude 一句一句干活”。

---

## 使用原则

不要一上来：

> build the whole project

优先：

1. 我先决定 scope
2. AI 解释 implementation order
3. 一次只做一个阶段
4. 每轮 review diff
5. 重要 decision 记录
6. AI 可以快，但不能失去我的 mental model

---

## 推荐节奏

### Step 1 — 分析，不改代码

> 先分析，不要修改任何文件。

### Step 2 — 说明计划

> 告诉我你准备改哪些文件、每个文件为什么需要。

### Step 3 — 小步实现

> 只实现这一阶段，不要扩大 scope。

### Step 4 — 验证

> 告诉我怎么验证。先运行最小必要 test。

### Step 5 — Review

> review current diff，找 correctness / scope expansion / unnecessary abstraction。

### Step 6 — 下一步

> 根据剩余时间，告诉我下一步最高价值任务。

---

## AI 输出太长时

直接说：

> 缩短回答。先给结论和下一步，不要重复背景。

或者：

> 只告诉我现在最重要的 3 件事。

---

## AI 开始过度设计时

> Stop. This is a 3-hour prototype.
>
> 重新设计成更简单版本。
> 不要增加新的 infrastructure / framework / abstraction，除非它直接解决题目 must-have。

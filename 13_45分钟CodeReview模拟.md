# 13 45 分钟 Code Review 模拟

## 让 AI 扮演严格 Tech Lead

> 你现在扮演一个严格的 Senior Engineer / Technical Lead。
>
> 根据我当前 repository 的真实实现，模拟接下来 45 分钟 technical code review。
>
> 不要泛泛问 textbook question。
> 问题必须针对我的实际代码和 architecture。
>
> 优先覆盖：
> - architecture
> - API design
> - data model
> - concurrency
> - idempotency
> - error handling
> - database
> - scalability
> - reliability
> - security
> - observability
> - testing
> - deployment
> - performance
> - production readiness
> - AI-assisted development
>
> 生成 20 个最可能问题。
>
> 每题给：
>
> **Question**
>
> **Short English Answer**
>
> **中文解释**
>
> **Potential Follow-up**
>
> 如果当前实现有明显 weakness，请不要回避。

---

## 必须能回答的通用问题

1. Why did you choose this architecture?
2. Why Flask?
3. Why this persistence layer?
4. Why not PostgreSQL / Redis / queue?
5. What did you intentionally leave out?
6. What would you do with one more hour?
7. What would you do with one more day?
8. What changes for production?
9. What breaks first at 100x traffic?
10. What happens under concurrent requests?
11. Is this operation idempotent?
12. What happens if a dependency fails?
13. How do you validate input?
14. How do you handle errors?
15. How would you add authentication/authorization?
16. How would you manage secrets?
17. What would you monitor?
18. What tests matter most?
19. What did AI generate?
20. What did you personally verify or reject?

---

## 60 秒 opening 模板

> I focused on shipping the smallest complete end-to-end workflow first.
>
> The current prototype supports [CORE FLOW].
>
> I chose [STACK] because it let me keep the implementation simple and deployable within the time constraint.
>
> I intentionally left [X] out of scope because it wasn't necessary for the prototype, but in production I would [Y].
>
> I validated the implementation with [TESTS] and verified [DEPLOYMENT / CORE FLOW].

根据实际项目修改，不要死背。

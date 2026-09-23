# Code Review Preparation

## Generate review notes

> 根据当前最终实现，帮我准备 45 分钟 technical code review。
>
> 不要修改代码。
>
> 请用中文详细解释，并在最后给我简短英文 bullets。
>
> 覆盖：
>
> 1. Problem and scope
> 2. Core architecture
> 3. Why I chose this stack
> 4. Main data flow
> 5. Important implementation decisions
> 6. What I intentionally left out
> 7. Biggest trade-offs
> 8. Error handling
> 9. Testing strategy
> 10. Deployment decisions
> 11. Security basics
> 12. Scaling limitations
> 13. Reliability limitations
> 14. Observability I would add in production
> 15. What I would change with one more day
> 16. What I would change for production
>
> 然后模拟 senior engineer 追问我 15 个最可能的问题。

## 60-second opening

Prepare something like:

> I focused on shipping the smallest complete end-to-end workflow first.  
> The current prototype supports [CORE FLOW].  
> I intentionally kept [X] simple because of the time constraint, and I would evolve it to [Y] in production.  
> I validated the implementation with [TESTS] and deployed it using [DEPLOYMENT APPROACH].

Adapt to the actual project.

## Questions to be ready for

- Why this architecture?
- Why this database/storage choice?
- Why not use X?
- What fails first under load?
- What happens on concurrent requests?
- What happens if a dependency fails?
- Is the operation idempotent?
- How would you add authentication/authorization?
- How would you handle secrets?
- What would you monitor?
- What would you cache?
- What would you move async?
- How would you migrate the data model?
- What did AI generate?
- What did you personally verify?

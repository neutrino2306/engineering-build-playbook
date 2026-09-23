# 11 Code Review 持续记录模板

建议在实际 challenge repo 中让 AI 创建：

`REVIEW_NOTES.md`

不要等三小时结束后才第一次总结。

---

# REVIEW_NOTES.md Template

## 1. Problem

What problem does this project solve?

## 2. Scope

### Implemented
- ...

### Intentionally Out of Scope
- ...

## 3. Architecture

- Main components:
- Data flow:
- Key dependencies:

## 4. API Design

- Endpoints:
- Validation:
- Status codes:
- Error model:

## 5. Data Model / Persistence

### Prototype Decision
...

### Why
...

### Production Evolution
...

## 6. Major Engineering Decisions

### Decision 1
- Choice:
- Reason:
- Alternative:
- Trade-off:
- Production version:

### Decision 2
...

## 7. Error Handling

...

## 8. Testing

### Covered
- ...

### Not Covered
- ...

## 9. Deployment

- Approach:
- Risks:
- What was verified:

## 10. Security

- Implemented:
- Deferred:

## 11. Scaling Limitations

...

## 12. Reliability Limitations

...

## 13. Observability

What I would add:
- logs
- metrics
- tracing
- alerts

## 14. If I Had More Time

### One more hour
...

### One more day
...

### Production
...

## 15. AI-Assisted Development

### AI helped with
- ...

### I explicitly verified
- ...

### AI output I rejected / changed
- ...

---

## 更新 Prompt

> 更新 REVIEW_NOTES.md。
>
> 只记录值得 technical code review 讨论的 engineering decision。
>
> 不要写流水账。
> 不要记录每一次小改动。
>
> 新增内容必须帮助我回答：
> - why did you choose this?
> - what was the alternative?
> - what is the trade-off?
> - what would change in production?

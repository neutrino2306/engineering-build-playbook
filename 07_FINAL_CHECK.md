# Final Check

## Final 30–45 minutes

Stop adding optional features.

### Correctness
- [ ] Core flow works
- [ ] Important validation works
- [ ] Errors are handled intentionally
- [ ] No obvious crash path

### Tests
- [ ] Happy path
- [ ] Invalid input
- [ ] Not-found/conflict if relevant
- [ ] Core business rule
- [ ] Tests pass

### Deployment
- [ ] Live service is reachable
- [ ] Core demo works in deployed environment
- [ ] Logs do not show obvious failures

### Code
- [ ] Remove dead/debug code
- [ ] No secrets
- [ ] Names are understandable
- [ ] No unexplained giant AI-generated abstraction
- [ ] I understand every important file

### Documentation
- [ ] What it does
- [ ] How to run
- [ ] How to test
- [ ] Architecture summary
- [ ] Known limitations
- [ ] What I would do next

### Demo
- [ ] 60-second project summary
- [ ] One clean happy-path demo
- [ ] One meaningful error/edge case if useful
- [ ] Architecture can be explained quickly

## Final AI review

> 现在进入 final review。
>
> 不要增加新 feature，不要大规模 refactor。
>
> 请作为 senior engineer review 当前项目。
>
> 找出：
> 1. 任何会导致 demo 失败的 critical issue
> 2. 任何明显 correctness issue
> 3. 任何 deployment risk
> 4. 任何我很可能在 code review 被问到的地方
>
> 只建议高价值、低风险的最后修改。

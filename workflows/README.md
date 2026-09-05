# Workflows — Skill Compositions by Situation

A workflow is an ordered composition of skills for a recurring engineering situation, with the gate after each stage and the size-class variations. The `sdlc-orchestrator` selects one workflow per situation, skips steps whose outputs are already current, and stops at the listed human decisions. Skill and gate ids match `skills/registry.yaml`.

| Situation (orchestrator classification) | Workflow | Validation scenario |
|---|---|---|
| New system from an idea | [new-product.md](new-product.md) | A small SaaS (S) · B mobile app (M) · C large API (L) |
| Change to an existing, documented system | [add-feature.md](add-feature.md) | steady state after any of the above |
| Production failure, degradation, breach | [production-incident.md](production-incident.md) | D |
| Existing system with thin docs/tests, EOL, blocking debt | [legacy-modernization.md](legacy-modernization.md) | E |
| Security / performance / reliability uplift | [hardening.md](hardening.md) | follow-up to D or audit findings |

Reading a workflow table: **Entry point / mode** names the sub-procedure of the skill (e.g., `security` A–G, `requirements` delta); **Gate after** is evaluated with `skills/sdlc-orchestrator/references/gates.md`; **Condition** rows (add-feature) are skipped with a logged reason when false.

Every workflow ends by returning STATE to a steady situation (`add-feature`) or to the workflow it interrupted (incident).

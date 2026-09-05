# Workflow: new-product

Idea → production for a new system. Covers validation scenarios A (small SaaS, S), B (mobile app, M) and C (large API, L) through size-class variations.

## Entry conditions
- Situation classified `new-product` by `sdlc-orchestrator` (empty repository or no application code; request describes something to build).
- User intent available; stack may be named (→ `CON-`) or open.

## Sequence

| # | Skill | Entry point / mode | Produces | Gate after |
|---|---|---|---|---|
| 1 | `discovery` | full | Discovery Brief, Risk Register | — |
| 2 | `security` | A risk profile | profile in brief/risks | `discovery-to-requirements` (human go/no-go H1) |
| 3 | `requirements` | full | Requirements Spec | — |
| 4 | `security` | B security requirements, ASVS level | §5 of spec | `requirements-to-design` |
| 5 | `agile-delivery` | backlog + DoR/DoD | Backlog | — |
| 6 | `domain-model` | `S:` skip unless trigger; `M/L:` run | Domain Model | — |
| 7 | `architecture` | full | Architecture Overview, ADRs | — |
| 8 | `security` | C threat model | Threat Model | — |
| 9 | `data-design` | full | Data Model, migrations | — |
| 10 | `api-design` | `S:` skip if no external consumer; else run | API Contract | — |
| 11 | `testing` | strategy mode | Test Strategy | — |
| 12 | `delivery-pipeline` | skeleton (environments + CI stages running on the empty project) | Deployment Plan (draft), pipeline config | `design-to-construction` |
| 13 | `agile-delivery` | iteration planning | iteration in Backlog | — |
| 14 | `implementation` ⇄ `testing` (per story) | story build; per-feature test plan | code, tests, traceability | `story-done` (repeat per story) |
| 15 | `security` | D per story (inside `story-done`); E security tests before release | findings, security test results | — |
| 16 | `security` | F release hardening | release checklist evidence | — |
| 17 | `operations` | pre-release runbook | Runbook | `construction-to-release` (human deploy approval H7) |
| 18 | `delivery-pipeline` | release execution and handover | production release | `release-to-operations` |
| 19 | `operations` | post-release readiness, metrics | Runbook updates | — |
| 20 | `maintenance` | register creation; steady state | Tech Debt Register | — |

Steps 13–15 repeat per iteration; the orchestrator re-plans between iterations. Step 18 runs `add-feature` semantics for subsequent releases. Design steps 6–12 are scoped to the first release (walking skeleton, `gates.md` scope rule): decisions that are expensive to change (style, store, hosting, authn) are made up front; Data Model, API Contract and Test Strategy grow per epic. In step 14, `implementation` writes the story's TEST rows itself; `testing` is invoked only when a new test level or non-trivial test design is needed.

## Size-class variations
- **S (scenario A)**: one-page brief; NFR table only; skip `domain-model` and `api-design` when triggers absent; threat table inside Architecture Overview; test strategy = levels table + exit criteria; runbook one page; ≤ 3 ADRs.
- **M (scenario B, mobile)**: `api-design` mandatory (mobile client is an external consumer); `implementation` loads `references/mobile.md` (offline/sync, permissions, secure storage) and `backend.md`; contract tests; ASVS L2 when PII; store review lead time in the Deployment Plan; server-side kill switches.
- **L (scenario C, large API)**: component views for hot spots; capacity model; SLOs per service; ASVS L2–L3; SBOM/signing; performance and resilience suites; DR plan; formal traceability matrix; more ADRs; human review at every gate.

## Exit criteria
Production release passed `release-to-operations`; Runbook current; Tech Debt Register exists; STATE stage `operations`; next action is the first review date or the next iteration.

## Typical human stops
H1 go/no-go · H2 scope changes · H3 costly NFR targets · H4 stack replacement · H5 High/Critical risk acceptance · H7 production deploy · H10 vendor/cost commitments.

## Dead-end checks
- Feasibility verdict no-go → stop with report; STATE records the verdict (no orphan artifacts).
- Missing stack decision at step 7 → `architecture` proposes; H4/H10 as needed; never invents commands.
- Security finding at step 15 with High/Critical → blocks `construction-to-release` until fixed or H5 accepted.

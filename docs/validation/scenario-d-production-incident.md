# Scenario D — Production incident

**Request (verbatim, invented):** "Checkout is returning 500s for about a third of users since the deploy 20 minutes ago. Customers are complaining on support. What do we do?"

## Orchestrator run

| Step | Result |
|---|---|
| Situation | `incident` — "500s", "since the deploy", customer impact |
| STATE | exists (system in `add-feature` steady state, iteration 14 in progress) → orchestrator records `Suspended workflow / resume point = add-feature, STORY-142 in implementation` |
| Size class | unchanged (M) |
| Workflow | `workflows/production-incident.md` |

## Sequence selected

| # | Skill · entry | Decision | Reason |
|---|---|---|---|
| 1 | incident-response steps 1–4 | run | declare S1 (user-visible, revenue path); roles: agent = Incident Commander + Communications + Planning, human on-call = Operations Lead (only role changing systems); live record `INC-20260904-1`; mitigation: rollback of the last deploy — Runbook pre-authorizes rollback for S1 → executed by Operations Lead without H7; comms every 30 min |
| 2 | incident-response steps 5–6 | run | after rollback error rate returns to baseline (mitigated); diagnosis: the deploy introduced a new discount rule that dereferences a null coupon for guests; confirmed with logs (correlation ids) and a failing reproduction test; resolved by fix + regression test through the normal pipeline (H7 for the fix deploy since not pre-authorized) |
| 3 | incident-response step 7 | run | blameless postmortem: impact 33 % of checkouts for 27 min; detection by support, not alerts (alert threshold on 5xx too high — detection gap); root cause: missing test for guest checkout path + no canary; action items: `STORY-150` guest-path tests, `DEBT-031` canary deploys with SLO watch, alert threshold fix |
| 4 | maintenance | run | intake action items; fix already merged with regression test; `DEBT-031` registered with interest (each risky deploy) |
| 5 | security G | **skip** | root cause not a vulnerability (logged) |
| 6 | operations | run | Runbook failure mode added (checkout 5xx after deploy → rollback); alert on checkout error-rate burn; detection improvement |
| — | gate incident-closure | pass | action items linked; runbook updated; STATE resumes `add-feature` at STORY-142 |

Skills not invoked: discovery, requirements, agile-delivery (action items entered directly as stories/debt with links — `agile-delivery` picks them up at the next iteration planning), architecture, data-design, api-design, delivery-pipeline (canary work becomes a hardening item), legacy-modernization.

## Artifact outline
- **Incident record + Postmortem** (`docs/engineering/incidents/2026-09-04-checkout-500s.md`): roles table; timeline (T+0 deploy, T+12 support tickets, T+20 declared, T+24 rollback, T+27 recovered, T+90 fix deployed); impact with SLO/error-budget consumption; detection analysis; root cause and trigger; action items with owners/links/due dates; lessons.
- **Runbook** update; **Tech Debt Register** `DEBT-031`; **Backlog** `STORY-150`.

## Human stops
H7 for the fix deploy (rollback itself pre-authorized in Runbook) · H12 for customer-facing status message · none for H6/H9.

## Criteria check

| Criterion | Result | Note |
|---|---|---|
| Classification | pass | |
| Skill selection | pass | 4 of 16 skills; security G skipped with reason |
| Mitigation before diagnosis | pass | procedure order enforced |
| Communication | pass | cadence + H12 |
| Root cause and prevention | pass | blameless, systemic, detection gap analyzed |
| Testing considerations | pass | regression test required by maintenance/story-done |
| Return to steady state | pass | resume point recorded |
| Dead ends | none | |

## Gaps found → fixes applied
1. STATE template had no field to record the interrupted workflow and resume point, although `production-incident.md` requires resuming it. → Added `Suspended workflow / resume point` to `templates/project-state.md` and `state-file.md §1`.

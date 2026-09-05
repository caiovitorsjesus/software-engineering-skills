# Workflow: add-feature

A capability change on an existing, documented system. The default for most day-to-day work after the first release.

## Entry conditions
- Situation `add-feature`: application code exists; request adds or changes behaviour; STATE exists (or is repaired via `skills/sdlc-orchestrator/references/state-file.md §4`).
- If documentation is thin and the change is risky, the orchestrator may reclassify to `legacy` (H14).

## Sequence

| # | Skill | Entry point / mode | Condition | Produces | Gate after |
|---|---|---|---|---|---|
| 1 | `requirements` | delta mode | always | new/changed REQs, change log, traceability rows | `requirements-to-design` (delta: affected REQs only) |
| 2 | `agile-delivery` | stories for the change; iteration plan | always | Backlog update | — |
| 3 | `architecture` | ADR-lite or full | only if a driver changes (new integration, data class, load, client type) | ADR(s), overview update | — |
| 4 | `security` | C threat model update | if the change touches authentication, authorization, session/tokens, secrets, personal or regulated data, payments, file upload, a new external interface or trust boundary — the story's DoR "security-relevant" flag decides | Threat Model update | — |
| 5 | `data-design` | delta | only if schema or access paths change | Data Model update, migration | — |
| 6 | `api-design` | delta | only if a contract changes | API Contract update (additive within version) | `design-to-construction` (delta) |
| 7 | `implementation` ⇄ `testing` | per story | always | code, tests, traceability | `story-done` |
| 8 | `security` | D per story; E/F before release | always (D); E/F per release | checklist, scans | — |
| 9 | `delivery-pipeline` | release via existing pipeline | always | release; Deployment Plan updated if environments changed | `construction-to-release`, `release-to-operations` |
| 10 | `operations` | runbook/alert deltas | if new failure modes or SLIs | Runbook update | — |

Steps 3–6 are conditional; the orchestrator logs "skipped — no driver/schema/contract change" for each skipped step.

## Size-class variations
- **S**: steps 3–6 usually skipped; security D only; release via existing pipeline.
- **M/L**: contract tests must pass before merge when step 6 runs; threat model update reviewed; canary/flags for risky changes.

## Exit criteria
Story(ies) released; traceability status `released`; Backlog updated; STATE next action.

## Typical human stops
H2 scope change · H4 stack deviation · H6 irreversible migration · H7 production deploy.

## Dead-end checks
- A story that cannot be built without an architecture change → step 3 runs (never a silent workaround; else `DEBT-###` with H-approval).
- Requirements change discovered during implementation → back to step 1 delta (change log), not ad-hoc.

# Scenario E — Existing legacy system

**Request (verbatim, invented):** "We have a 10-year-old PHP 5.6 monolith with a MySQL database that runs our B2B ordering portal. No automated tests, the original developers left, hosting provider ends PHP 5.6 support in six months. We want to modernize without stopping the business."

## Orchestrator run

| Step | Result |
|---|---|
| Situation | `legacy` — existing code, thin tests/docs, EOL platform, "modernize" |
| Stack | detected: PHP (composer absent → legacy includes), MySQL, Apache config, cron jobs; commands unknown → assessment must recover them |
| Size class | **M** — external B2B users, customer and order data beyond identity, business-critical; L only if regulated data is found (assessment checks) |
| Workflow | `workflows/legacy-modernization.md` |

## Sequence selected

| # | Skill · entry | Decision | Reason |
|---|---|---|---|
| 1 | legacy-modernization steps 1–6 | run | inventory (1 repo, 214 PHP files, 41 tables, 6 cron jobs, 2 integrations: ERP export, email); reverse-engineered as-is C4; quality findings (no tests; 12 hotspot files; SQL built by string concatenation → injection exposure; secrets in config file in VCS; no observability); knowledge risk high; `DEBT-001…018`; `RISK-001` EOL date, `RISK-002` unknown behaviours; options matrix → recommendation: **refactor + incremental rearchitecture** (strangler) over rebuild; **H11** asked |
| 2 | discovery | run | modernization goals (keep business running, remove EOL risk in 6 months, enable testable changes), constraints (`CON-001` same team of 3, `CON-002` MySQL stays for now), feasibility `go` for incremental; `no-go` for rebuild within 6 months |
| 3 | requirements | run | behaviours to preserve as `REQ-F` from observed flows (order placement, approval, ERP export); `REQ-N` targets for the target (availability during cut-over, performance parity); security REQs (ASVS L2; fix injection exposure; secrets out of VCS) |
| 4 | architecture | run | target: modular monolith on supported runtime (PHP 8.x per H4 — same language family, or replatform decision) fronted by a routing layer; strangler extraction order: authentication → ordering → reporting; ADRs: runtime upgrade path, routing layer, anti-corruption layer for ERP export |
| 5 | security C | run | threat model for transition state (two runtimes, shared DB); injection and secrets as High → mitigated in first increments |
| 6 | data-design | run | shared MySQL during transition; schema ownership per module; expand/contract for renamed columns; backup and restore test before any migration (H6 for irreversible steps) |
| 7 | testing | run | characterization mode: golden-master tests on the top 10 flows via HTTP; DB snapshot fixtures; regression suite in CI |
| — | gate modernization-plan-approved | pass after H11 | option approved; characterization first; rollback per increment |
| 8 | legacy-modernization steps 7–8 | run | roadmap: M1 runnable baseline + CI + characterization (weeks 1–3); M2 runtime upgrade behind routing (weeks 4–8); M3 secrets/injection fixes; M4 ordering module extraction; decommission plan |
| — | gate design-to-construction | pass | |
| 9 | agile-delivery | run | epics per milestone; stories with DoR (characterization coverage present) |
| 10 | implementation ⇄ testing | run per increment | `backend.md`; every change behind characterization tests |
| 11 | delivery-pipeline | run | new pipeline; parallel run with shadow traffic for ordering; cut-over/rollback criteria; H7 |
| 12 | operations | run | SLIs on old and new paths; decommission steps |
| 13 | maintenance | run | debt register ownership after M4 |

Skipped: domain-model (run partially inside step 1 term recovery; full run deferred until ordering extraction — logged), api-design (no external API consumers; ERP export is a file integration — logged).

## Human stops
H11 option/decommission · H4 runtime/replatform choice · H6 data migrations · H9 licensing of legacy components (none found) · H7 cut-overs.

## Criteria check

| Criterion | Result | Note |
|---|---|---|
| Classification | pass | |
| Reverse engineering → evidence | pass | inventory, as-is views, findings with severity |
| Debt and risk analysis | pass | registers seeded |
| Options vs. rebuild bias | pass | rebuild rejected with evidence; gate enforces |
| Incremental migration safety | pass | characterization first; rollback per increment; H6 |
| Security | pass | injection/secrets High fixed early; transition-state threat model |
| Testing | pass | characterization + regression |
| Re-entry into lifecycle | pass | discovery → … → operations |
| Dead ends | none | "cannot run" case handled by roadmap M1 |

## Gaps found → fixes applied
1. Registry `legacy-modernization` sequence omitted `security`, the second `legacy-modernization` pass, `agile-delivery` and `maintenance` present in the workflow file. → Registry aligned.
2. `discovery` registry inputs lacked `legacy-assessment?` though the skill consumes it in legacy mode. → Added.
3. `testing` registry inputs lacked `source-code?` needed for characterization mode. → Added.

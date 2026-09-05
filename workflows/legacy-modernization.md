# Workflow: legacy-modernization

Existing system with thin documentation or tests → evidence → decision → incremental, reversible migration. Validation scenario E.

## Entry conditions
- Situation `legacy`: user asks to understand, migrate or modernize; components EOL; debt blocks change; or `add-feature` was reclassified because documentation is too thin for safe change.

## Sequence

| # | Skill | Entry point / mode | Produces | Gate after |
|---|---|---|---|---|
| 1 | `legacy-modernization` | steps 1–6: inventory, reverse engineering, quality/security assessment, criticality, debt/risks, options | Legacy Assessment (draft), Tech Debt Register, Risk Register entries | — (H11 option decision) |
| 2 | `discovery` | modernization goals, constraints, feasibility of the chosen option | Discovery Brief (modernization) | `discovery-to-requirements` |
| 3 | `requirements` | behaviours to preserve, compliance found, NFR targets for the target system | Requirements Spec | `requirements-to-design` |
| 4 | `architecture` | target architecture and migration structure (strangler routing, anti-corruption layer) | Architecture Overview (target), ADRs | — |
| 5 | `security` | C threat model for target and transition state | Threat Model | — |
| 6 | `data-design` | migration approach (dual-write/backfill, verification, cut-over, rollback) | Data Model, migration plan | — |
| 7 | `testing` | characterization tests around every seam to change; regression suite | Test Strategy (characterization mode) | `modernization-plan-approved` |
| 8 | `legacy-modernization` | step 7–8: roadmap with milestones, rollback criteria, decommission plan | Legacy Assessment §7–8 final | `design-to-construction` |
| 9 | `agile-delivery` | increments as stories/epics by business capability | Backlog | — |
| 10 | `implementation` ⇄ `testing` | per increment: extract, route, verify against characterization tests | code, tests | `story-done` |
| 11 | `delivery-pipeline` | parallel run / shadow traffic; cut-over per increment; rollback rehearsed | Deployment Plan | `construction-to-release`, `release-to-operations` |
| 12 | `operations` | SLIs on both old and new paths during transition; decommission steps | Runbook | — |
| 13 | `maintenance` | debt register ownership; remaining items | Tech Debt Register | — |

## Size-class variations
- Usually **M** or **L** (legacy systems that matter). **S** legacy (small internal tool): steps 1–3 compressed into the assessment plus a short brief; still characterization tests before change.

## Exit criteria
Legacy components decommissioned or the program's approved scope delivered; Runbook covers the new system; STATE situation returns to `add-feature` steady state.

## Typical human stops
H11 option and decommission dates · H6 data migration with loss risk · H4 stack replacement · H9 licensing/compliance of legacy components · H7 cut-over deploys.

## Dead-end checks
- Cannot build/run the legacy system → assessment records the blockers; migration strategy must include a plan to obtain a runnable baseline before any change.
- Rebuild chosen without evidence that incremental options fail → gate `modernization-plan-approved` fails.
- Increment without characterization coverage → `story-done` fails.

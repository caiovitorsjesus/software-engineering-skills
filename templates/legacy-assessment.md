<!--
Purpose: Capture what an existing system actually is (inventory, as-is architecture, quality, risks, debt) and compare modernization options with an incremental migration strategy.
Producer: legacy-modernization.
Consumers: discovery (modernization goals), requirements (what to preserve), architecture (target), data-design (migration), testing (characterization), sponsor (option decision).
Update when: new findings during reverse engineering; option decision made; roadmap milestones reached.
Size: M/L document; S systems may use only §1–§3 and §6.
-->
# Legacy Assessment — <system>

| Field | Value |
|---|---|
| Date / author | |
| Business criticality | |
| Knowledge risk (who understands it) | |
| Recommended option | rehost / replatform / refactor / rearchitect / rebuild / retire — ADR-… |

## 1. Inventory
| Item | Type (repo / service / job / DB / integration / infra) | Technology / version | Owner | Runs where | Notes |
|---|---|---|---|---|---|

## 2. As-is architecture (recovered)
C4 context and container (text list acceptable) · module map · data flows · external dependencies · build/run instructions recovered.

## 3. Quality findings
| Area | Finding | Evidence | ISO/IEC 25010:2023 characteristic | Severity |
|---|---|---|---|---|
| Tests | coverage, presence of characterization tests | | maintainability › testability | |
| Code health | complexity hotspots, duplication, dead code | | maintainability | |
| Dependencies | outdated / EOL / vulnerable | | security, maintainability | |
| Security exposure | auth model, secrets, known issues | | security | |
| Operations | observability, deploy process, backups | | reliability | |
| Data | schema quality, integrity issues, undocumented tables | | functional correctness | |

## 4. Risks
Top `RISK-###` for continuing as-is and for migrating.

## 5. Debt summary
Link to Tech Debt Register; totals by priority.

## 6. Options
| Option | What changes | Preserves | Cost / duration | Risk | Fits drivers (REQ/CON) |
|---|---|---|---|---|---|
| Rehost | | | | | |
| Replatform | | | | | |
| Refactor | | | | | |
| Rearchitect | | | | | |
| Rebuild | | | | | |
| Retire / replace | | | | | |

## 7. Target and migration strategy
Target architecture link · characterization tests first · incremental extraction order (by module/business capability) · data migration approach · parallel run / shadow traffic · cut-over and rollback criteria · decommission plan.

## 8. Roadmap
| Milestone | Scope | Exit criteria | Dependencies | Target date |
|---|---|---|---|---|

## 9. Open questions

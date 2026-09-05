# Workflow: hardening

Security, performance or reliability uplift of an existing system without changing its functional scope.

## Entry conditions
- Situation `hardening`: audit findings, pen-test report, SLO misses, performance complaints, scaling need, compliance deadline; system is documented enough (else `legacy`).

## Sequence

| # | Skill | Entry point / mode | Produces | Gate after |
|---|---|---|---|---|
| 1 | `operations` | baseline: SLIs measured, current SLO attainment, alert quality, capacity headroom | Runbook (baseline section) | — |
| 2 | `security` | C threat model refresh + ASVS gap analysis at the target level; G for open findings | Threat Model, findings list | — (H5 for accepted risks) |
| 3 | `architecture` | re-evaluate quality attribute scenarios against measurements; ADRs for structural changes (caching, scaling, isolation) | Architecture Overview update, ADRs | `design-to-construction` (for structural changes) |
| 4 | `maintenance` | register debt from findings; dependency and patch review | Tech Debt Register | — |
| 5 | `agile-delivery` | prioritized hardening backlog (risk reduction first) | Backlog | — |
| 6 | `implementation` ⇄ `testing` | per item; performance/resilience/security tests as evidence | code, tests | `story-done` |
| 7 | `security` | E/F before release | test results, release checklist | — |
| 8 | `delivery-pipeline` | release; supply-chain controls if in scope (SBOM, signing) | Deployment Plan update | `construction-to-release`, `release-to-operations` |
| 9 | `operations` | re-measure against baseline; alert/runbook updates | Runbook | — |

## Size-class variations
- **S**: steps 1–2 as tables; step 3 only if a scenario fails.
- **M/L**: ASVS L2/L3 gap analysis; load/resilience test suites required as evidence; DORA and SLO trends compared before/after.

## Exit criteria
Measured improvement against the baseline for the targeted characteristics; no open High/Critical findings without acceptance; STATE situation returns to `add-feature`.

## Typical human stops
H5 risk acceptance · H3/H10 targets or tiers that cost · H7 production deploy · H13 requests to skip verification.

## Dead-end checks
- Findings without owners → `agile-delivery` refuses to plan them (DoR).
- Improvement not measurable → step 1 baseline missing; go back rather than declaring success.

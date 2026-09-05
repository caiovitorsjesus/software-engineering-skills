<!--
Purpose: Define how quality will be verified: which test levels exist, what each covers (ISO/IEC 25010:2023 characteristics), where they run, data and environments, exit criteria, and the per-feature plan pattern.
Producer: testing.
Consumers: implementation, delivery-pipeline (CI stages), agile-delivery (DoD).
Update when: architecture or NFRs change, a new level is added, exit criteria change; per-feature sections added per story/epic.
Size: S one page (levels table + exit criteria); M/L all sections. Concepts per references/testing-foundations.md.
-->
# Test Strategy — <project>

| Field | Value |
|---|---|
| Version / date | |
| Test frameworks / tools | from STATE.md › Stack |
| CI stages | link to Deployment Plan |

## 1. Objectives and quality coverage
| ISO/IEC 25010:2023 characteristic | REQ-N ids | Verified by (level / tool) |
|---|---|---|

## 2. Test levels
| Level | Purpose | Scope | Technique families (spec / structure / experience) | Tools | Runs where / when | Exit criteria |
|---|---|---|---|---|---|---|
| Unit | | | | | every commit | 100 % pass; coverage on changed code ≥ …% |
| Component | | | | | CI | |
| Integration | | | | | CI (slow stage) | |
| Contract | | | | | CI both sides | no breaking change |
| End-to-end | critical journeys only | | | | nightly / pre-release | |
| Performance | REQ-N performance rows | | | | pre-release | targets met |
| Security | SAST / DAST / dependency / abuse cases | | | | CI + pre-release | zero open High/Critical |
| Resilience (M/L) | | | | | pre-release | |
| Accessibility / usability | | | | | pre-release | WCAG level … |
| Exploratory | | charters | | | before release | notes filed |
| Acceptance | AC walk-through with stakeholder | | | | release gate | sign-off |

## 3. Environments and test data
| Environment | Purpose | Data (fixtures / synthetic / anonymized) | Parity with prod | Owner |
|---|---|---|---|---|

## 4. Automation and CI mapping
Which levels gate merge, which gate release, which are scheduled; time budget per stage.

## 5. Flakiness policy
Quarantine within one day → `DEBT-###` → fix or delete within <n> days.

## 6. Regression policy
Every fixed defect gets a test at the lowest reproducing level; critical journeys in the e2e suite.

## 7. Per-feature test plan pattern
For each story/epic: `TEST-###` · REQ/STORY · level(s) · cases (happy, boundary, invalid, abuse) · data · expected evidence.

| TEST | REQ / STORY | Level | Cases | Status |
|---|---|---|---|---|

## 8. Known gaps and risks

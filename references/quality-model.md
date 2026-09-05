# Quality Model — ISO/IEC 25010:2023

> Covers: ISO/IEC 25010:2023 product quality model (nine characteristics, sub-characteristics, renames from the 2011 edition) and how each lifecycle stage uses it
> Retrieved: 2026-09-04
> Sources: https://iso25000.com/index.php/en/iso-25000-standards/iso-25010, https://quality.arc42.org/standards/iso-25010, https://blog.spree.de/2024/01/02/iso-iec-25010-news-from-the-2nd-edition-2023-11/ (iso.org page https://www.iso.org/standard/78176.html returned 403; three secondary sources cross-checked)
> Evidence: STANDARD, RECOMMENDATION, DECISION

Load when: writing non-functional requirements, quality attribute scenarios, test coverage by quality, or SLIs.

## 1. Characteristics and sub-characteristics (STANDARD)

| # | Characteristic | Sub-characteristics | Typical measurable target |
|---|---|---|---|
| 1 | Functional suitability | functional completeness, functional correctness, functional appropriateness | % of specified functions implemented; defect rate per function |
| 2 | Performance efficiency | time behaviour, resource utilization, capacity | p95 latency, throughput, CPU/memory per request, max concurrent users |
| 3 | Compatibility | co-existence, interoperability | passes contract tests with named systems; runs alongside X without degradation |
| 4 | Interaction capability (formerly *usability*) | appropriateness recognizability, learnability, operability, user error protection, user engagement, inclusivity, user assistance, self-descriptiveness | task completion rate, time to first success, WCAG conformance level |
| 5 | Reliability | faultlessness (formerly *maturity*), availability, fault tolerance, recoverability | availability %, MTBF, RPO/RTO, graceful degradation under dependency failure |
| 6 | Security | confidentiality, integrity, non-repudiation, accountability, authenticity, resistance (new) | ASVS level, zero High/Critical open findings, audit log coverage |
| 7 | Maintainability | modularity, reusability, analysability, modifiability, testability | change lead time, cyclomatic complexity ceilings, test coverage on changed code, dependency freshness |
| 8 | Flexibility (formerly *portability*) | adaptability, scalability (new), installability, replaceability | horizontal scale-out verified to N×, install time, environment parity |
| 9 | Safety (new) | operational constraint, risk identification, fail safe, hazard warning, safe integration | hazard list with mitigations; fail-safe behaviour tested |

Placement note: *testability* sits under Maintainability (consistent with the 2011 edition and two of three sources consulted).

## 2. 2011 → 2023 rename map (STANDARD)

| 2011 term | 2023 term |
|---|---|
| Usability | Interaction capability |
| Portability | Flexibility |
| Reliability › maturity | Reliability › faultlessness |
| Usability › accessibility | Interaction capability › inclusivity + user assistance |
| Usability › user interface aesthetics | Interaction capability › user engagement |
| — | Security › resistance (added) |
| — | Flexibility › scalability (added) |
| — | Interaction capability › self-descriptiveness (added) |
| — | Safety (added as ninth characteristic) |

## 3. How each stage uses the model (DECISION)

| Stage / skill | Use |
|---|---|
| requirements | Every `REQ-N-###` names one characteristic (and sub-characteristic when useful), a numeric target, and a measurement method. Walk all nine; record "not applicable" explicitly for the rest. |
| architecture | Top NFRs become quality attribute scenarios: *stimulus · source · environment · artifact · response · response measure*. Each style/decision is judged against them (see `architecture-styles.md`). |
| testing | Test Strategy has a coverage row per characteristic: which test level verifies it (e.g., performance → load test; security → SAST/DAST/abuse cases; reliability → chaos/failover test; interaction capability → accessibility and usability checks). |
| operations | SLIs derive from performance efficiency, reliability and security NFRs; SLO targets equal or relax the REQ-N target with an error budget. |
| maintenance | Maintainability sub-characteristics drive the tech debt register's impact column. |
| gates | Requirements→Design gate fails if any applicable characteristic lacks a REQ-N or an explicit "not applicable" line. |

## 4. NFR statement pattern (RECOMMENDATION)

`REQ-N-### [Characteristic › sub-characteristic] Under <condition>, the system shall <behaviour> such that <metric> is <operator> <value>, measured by <method> in <environment>.`

Example: `REQ-N-004 [Performance efficiency › time behaviour] Under 200 concurrent users, the search endpoint shall return results such that p95 latency is ≤ 400 ms, measured by k6 load test against staging with production-like data.`

Rules: one characteristic per NFR; a number and a method in every NFR; targets confirmed with the stakeholder when they imply cost (see `skills/sdlc-orchestrator/references/human-decisions.md`).

## 5. Right-sizing (RECOMMENDATION)

- `S`: one NFR table row per applicable characteristic (often 5–7 rows); no formal quality scenarios.
- `M`: full NFR set plus 3–6 quality attribute scenarios for the drivers.
- `L`: full NFR set, scenarios for every driver, and SLIs/SLOs per user-facing path.

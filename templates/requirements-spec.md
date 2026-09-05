<!--
Purpose: Specify what the software must do (FR) and how well (NFR, ISO/IEC 25010:2023), with acceptance criteria and the traceability table that follows each requirement to design, tests and release.
Producer: requirements.
Consumers: agile-delivery, domain-model, architecture, testing, security, implementation, operations.
Update when: a change request is accepted (log it in §10); implementation/testing/release update traceability status.
Size: S 2–4 pages (FR as a table, NFR one row per applicable characteristic); M/L full sections. Follows ISO/IEC/IEEE 29148 quality criteria (see references/requirements-quality.md).
-->
# Requirements Spec — <project>

| Field | Value |
|---|---|
| Version / date | |
| Source | Discovery Brief <path> v<…> |
| Prioritization method | MoSCoW / WSJF / Kano / risk-first |
| ASVS level (security) | L1 / L2 / L3 |

## 1. Product context
Purpose · users and roles · main workflows · boundaries with other systems (one paragraph or a context diagram reference).

## 2. Functional requirements
| ID | Statement (shall …) | Acceptance criteria (Given/When/Then or rule) | Priority | Source | Notes |
|---|---|---|---|---|---|
| REQ-F-001 | | | Must | stakeholder / brief §… | |

## 3. Non-functional requirements (ISO/IEC 25010:2023)
One row per applicable characteristic; write "n/a — reason" for the rest.
| ID | Characteristic › sub-characteristic | Requirement (condition · behaviour · metric · operator · value) | Measurement method / environment | Priority |
|---|---|---|---|---|
| REQ-N-001 | Performance efficiency › time behaviour | | | |
| REQ-N-002 | Reliability › availability | | | |
| REQ-N-003 | Security › … | | | |
| REQ-N-004 | Maintainability › … | | | |
| REQ-N-005 | Interaction capability › … | | | |
| REQ-N-006 | Flexibility › … | | | |
| REQ-N-007 | Compatibility › … | | | |
| REQ-N-008 | Functional suitability › … | | | |
| REQ-N-009 | Safety › … | | | |

## 4. Constraints, assumptions, dependencies
| ID | Type | Statement | Source / owner |
|---|---|---|---|
| CON-001 | constraint | | |
| ASM-001 | assumption | | validation plan: … |
| DEP-001 | dependency | | |

## 5. Security requirements (SSDF PO.1)
Data classification · authentication and session model · authorization model (roles/attributes, tenant isolation) · data protection (encryption, retention, erasure) · logging/audit needs · compliance obligations. Each becomes a `REQ-F` or `REQ-N` row above; list ids here.

## 6. Interfaces and integrations
| System / actor | Direction | Data / contract | Constraints |
|---|---|---|---|

## 7. Data requirements
Key entities and volumes · retention · migration from existing data (if any).

## 8. Out of scope
Explicit exclusions carried from the Discovery Brief plus new ones.

## 9. Open questions
| # | Question | Blocks | Owner | Due |
|---|---|---|---|---|

## 10. Change log
| # | Date | Change | Reason / source | Impact (REQ, ADR, TEST ids) | Approved by |
|---|---|---|---|---|---|

## 11. Traceability
| REQ | Priority | STORY | ADR / component | TEST | Status (specified / designed / implemented / verified / released) |
|---|---|---|---|---|---|

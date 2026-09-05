# Lifecycle Map and Glossary

> Covers: ISO/IEC/IEEE 12207:2017 technical processes; SWEBOK Guide v4.0 (2024) knowledge areas; NIST SSDF v1.1; OWASP SAMM v2.0; this system's stage keys, artifact names and identifier prefixes
> Retrieved: 2026-09-04
> Sources: https://en.wikipedia.org/wiki/ISO/IEC_12207 (iso.org page returned 403), https://www.computer.org/education/bodies-of-knowledge/software-engineering, https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf, https://owaspsamm.org/model/
> Evidence: STANDARD, INDUSTRY, DECISION

Load when: you need the canonical stage key, artifact name or ID prefix; or you must justify a stage against a standard.

## 1. Stage keys (use exactly these)

| Stage key | Meaning | Primary skills |
|---|---|---|
| `discovery` | Problem framing, stakeholders, objectives, scope, constraints, feasibility, initial risks | discovery |
| `requirements` | Functional and non-functional requirements, acceptance criteria, traceability | requirements |
| `planning` | Backlog, prioritization, iteration planning, DoR/DoD | agile-delivery |
| `design` | Domain model, architecture, data model, API contracts | domain-model, architecture, data-design, api-design |
| `construction` | Detailed module design and coding | implementation |
| `verification` | Test strategy and execution; security testing | testing, security |
| `deployment` | Pipeline, environments, release, rollback, handover | delivery-pipeline |
| `operations` | SLOs, observability, runbooks, incidents | operations, incident-response |
| `evolution` | Maintenance, technical debt, modernization | maintenance, legacy-modernization |
| `transversal` | Applies at every stage | security (also quality via references) |

## 2. Mapping to standards (STANDARD)

| Stage key | ISO/IEC/IEEE 12207:2017 technical process | SWEBOK v4 knowledge area | SSDF v1.1 / SAMM v2 |
|---|---|---|---|
| discovery | Business or mission analysis; Stakeholder needs and requirements definition | Software Requirements; SE Economics; SE Management | SAMM Design › Threat Assessment (risk profile) |
| requirements | System/software requirements definition | Software Requirements | SSDF PO.1; SAMM Design › Security Requirements |
| planning | Project planning; Project assessment and control (technical management group) | SE Management; SE Process | — |
| design | Architecture definition; Design definition; System analysis | Software Architecture; Software Design; Models and Methods | SSDF PW.1, PW.2; SAMM Design › Secure Architecture |
| construction | Implementation; Integration | Software Construction | SSDF PW.4–PW.7; SAMM Implementation › Secure Build |
| verification | Verification; Validation | Software Testing; Software Quality | SSDF PW.8; SAMM Verification (all three practices) |
| deployment | Transition | SE Operations; Software Configuration Management | SSDF PS.1–PS.3, PW.9; SAMM Implementation › Secure Deployment |
| operations | Operation | SE Operations | SSDF RV.1–RV.3; SAMM Operations (all three practices) |
| evolution | Maintenance | Software Maintenance | SSDF RV.2, RV.3; SAMM Implementation › Defect Management |

12207 "Disposal" is covered only as data retention/deletion (data-design) and deprecation (maintenance) — DECISION.

12207 also defines Agreement processes (acquisition, supply), Organizational project-enabling processes, and Technical management processes (planning, assessment and control, decision management, risk management, configuration management, information management, quality assurance). This system covers decision management (ADRs), risk management (risk register), configuration management (delivery-pipeline) and quality assurance (gates); the others are out of scope.

## 3. Artifact names (canonical) and default locations

`docs_root` defaults to `docs/engineering/` in the target repository (overridable in STATE.md).

| Artifact | File | Producer |
|---|---|---|
| Project State | `STATE.md` | sdlc-orchestrator |
| Discovery Brief | `discovery-brief.md` | discovery |
| Risk Register | `risk-register.md` | discovery (owner); others append |
| Requirements Spec | `requirements.md` | requirements |
| Backlog | `backlog.md` | agile-delivery |
| Domain Model | `domain-model.md` | domain-model |
| Architecture Overview | `architecture.md` | architecture |
| ADR | `adr/NNNN-kebab-title.md` | architecture, data-design, legacy-modernization |
| Data Model | `data-model.md` | data-design |
| API Contract | `api/` (OpenAPI/GraphQL SDL/AsyncAPI) or stack convention | api-design |
| Threat Model | `threat-model.md` | security |
| Test Strategy | `test-strategy.md` | testing |
| Deployment Plan | `deployment-plan.md` | delivery-pipeline |
| Runbook | `runbook.md` | operations |
| Incident Postmortem | `incidents/YYYY-MM-DD-slug.md` | incident-response |
| Tech Debt Register | `tech-debt.md` | maintenance, legacy-modernization |
| Legacy Assessment | `legacy-assessment.md` | legacy-modernization |

## 4. Identifier prefixes

| Prefix | Meaning | Assigned by |
|---|---|---|
| `REQ-F-###` | Functional requirement | requirements |
| `REQ-N-###` | Non-functional requirement (names an ISO/IEC 25010:2023 characteristic) | requirements |
| `CON-###` | Constraint | discovery, requirements |
| `ASM-###` | Assumption (must be validated or accepted) | any skill |
| `RISK-###` | Risk | discovery; any skill appends |
| `ADR-####` | Architecture decision record | architecture, data-design, legacy-modernization |
| `THR-###` | Threat | security |
| `TEST-###` | Test case / suite identifier used in traceability | testing |
| `DEBT-###` | Technical debt item | maintenance, legacy-modernization |
| `INC-YYYYMMDD-#` | Incident | incident-response |
| `STORY-###` / `EPIC-##` | Backlog items | agile-delivery |

Traceability chain: `REQ → STORY → ADR/component → TEST → status`, held as a table in the Requirements Spec (L-class projects may extract it to `traceability.md` with the same columns).

## 5. Size classes

`S` small (1–2 developers, single deployable, up to a few hundred users, identity-only personal data) · `M` medium (small team, thousands of external users or multi-tenant, personal data beyond identity) · `L` large (multiple teams/services, regulated or high-value data, high traffic). Full criteria and per-artifact depth: `skills/sdlc-orchestrator/references/rightsizing.md`.

## 6. Terminology rules

- "Requirements Spec" (not PRD/SRS) — one document with a product-context section.
- "Discovery Brief" (not feasibility study / problem statement as separate docs).
- "Iteration" is used generically; "Sprint" only when the team runs Scrum (see `scrum-vocabulary.md`).
- "Gate" = checklist evaluated at a stage transition (`skills/sdlc-orchestrator/references/gates.md`).
- "Stop and ask" = a human decision trigger (`skills/sdlc-orchestrator/references/human-decisions.md`).

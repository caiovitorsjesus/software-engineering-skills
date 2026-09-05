# Requirements Quality

> Covers: ISO/IEC/IEEE 29148:2018 requirement quality criteria (verified subset) and requirement smells; acceptance-criteria patterns; prioritization methods; change control; traceability
> Retrieved: 2026-09-04
> Sources: https://en.wikipedia.org/wiki/Software_requirements_specification (29148 summary; iso.org page returned 403)
> Evidence: STANDARD, RECOMMENDATION

Load when: writing, reviewing or changing requirements and acceptance criteria.

## 1. Quality criteria (STANDARD — ISO/IEC/IEEE 29148:2018 as summarized)

Individual requirement: **necessary**, **appropriate** (right level of abstraction), **unambiguous**.
Requirement set: **complete**, **consistent**, **feasible**, **comprehensible**.

Additional criteria this system applies (RECOMMENDATION; commonly associated with 29148 but not verified against the standard text here): singular (one requirement per statement), verifiable (a test or measurement can show it is met), correct (agreed by the stakeholder), traceable (linked to source and to design/tests).

29148 supersedes IEEE 830-1998 and defines the information items BRS (business), StRS (stakeholder), SyRS (system) and SRS (software). This system merges the product context and the software requirements into one Requirements Spec (DECISION D-14, D-15 lineage).

## 2. Requirement smells (STANDARD list; examples RECOMMENDATION)

| Smell | Example | Fix |
|---|---|---|
| Subjective language | "user-friendly", "fast" | Name the 25010 sub-characteristic and a number |
| Ambiguous adverbs/adjectives | "quickly", "appropriate", "several" | Quantify or enumerate |
| Superlatives | "best", "maximum performance" | Replace with a measurable target |
| Negative statements | "shall not be slow" | State the positive behaviour and bound |
| Non-verifiable terms | "shall support", "shall handle" | Define observable outcome |
| Totality words | "all", "always", "never" | Bound the scope or list the cases |
| Implementation in the requirement | "shall use Redis" | Move to a constraint (`CON-`) or an ADR |
| Compound requirement | "shall X and Y" | Split into two IDs |

## 3. Acceptance-criteria patterns (RECOMMENDATION)

- **Scenario**: `Given <precondition> When <action> Then <observable result>`. Use for behaviour with state.
- **Rule**: `Rule: <condition> → <outcome>`; list boundary values explicitly. Use for validations and calculations.
- **Example table**: inputs → expected outputs, including at least one boundary and one invalid case.
- Every `REQ-F` has ≥ 1 criterion; every criterion is executable as a test or an inspection.
- Non-functional acceptance = the `REQ-N` target and method (see `quality-model.md §4`).

## 4. Prioritization methods (RECOMMENDATION — record the method used)

| Method | When | Output |
|---|---|---|
| MoSCoW | S/M; fixed scope negotiation | Must / Should / Could / Won't (this release) |
| WSJF (cost of delay ÷ job size) | backlog with many similar-size items | numeric rank |
| Kano | user-facing product decisions | basic / performance / delighter |
| Risk-first | security/compliance-heavy or legacy | order by risk reduction |

## 5. Elicitation checklist (RECOMMENDATION)

Users and roles · goals per role · main workflows and their exceptions · data owned/read/written and its sensitivity · integrations and their contracts · volumes and peaks · environments and devices · legal/regulatory constraints · operational constraints (support hours, languages, time zones) · existing systems to preserve or replace · what "done" means to the sponsor.

## 6. Change control (RECOMMENDATION)

1. Every change gets an entry in the Requirements Spec change log: id, date, what, why, source, impact (REQ ids, ADRs, tests).
2. A change that alters scope, cost or a quality target versus the Discovery Brief is a **Stop and ask**.
3. Update the traceability row(s) and mark dependent tests as "to re-run".
4. Re-run the Requirements→Design gate for the affected REQs only.

## 7. Traceability table columns (DECISION)

`REQ id · Priority · STORY id(s) · ADR / component · TEST id(s) · Status (specified / designed / implemented / verified / released)`. Kept in the Requirements Spec; `implementation` fills component and moves status to implemented; `testing` fills TEST and moves to verified; `delivery-pipeline` moves to released.

<!--
Purpose: Ordered, executable plan of work derived from the Requirements Spec: epics, stories with acceptance criteria, Definition of Ready/Done, and the current iteration.
Producer: agile-delivery.
Consumers: implementation (picks stories), testing, maintenance, incident-response (corrective actions land here).
Update when: refinement, iteration planning, review, retrospective, or when requirements change.
Size: S a single table of stories plus DoD; M/L full sections. Vocabulary per references/scrum-vocabulary.md (no Scrum-conformance claim).
-->
# Backlog — <project>

**Product goal:** <one sentence from the Discovery Brief vision>

## 1. Epics
| ID | Epic | REQ coverage | Outcome / metric | Status |
|---|---|---|---|---|
| EPIC-01 | | REQ-F-001…005 | | |

## 2. Stories
| ID | Epic | Story (As a … I want … so that …) | REQ links | Acceptance criteria | Estimate | Priority | Status |
|---|---|---|---|---|---|---|---|
| STORY-001 | EPIC-01 | | REQ-F-001 | (reuse REQ AC; add UI/edge cases) | | | ready / in progress / done |

## 3. Definition of Ready (a story may start when…)
- [ ] Linked to at least one `REQ` id (or a `DEBT`/`INC` id for corrective work)
- [ ] Acceptance criteria written and testable
- [ ] Dependencies (design, contract, data) identified and available
- [ ] Size estimated and small enough for one iteration
- [ ] Security-relevant? (touches auth, data, input, secrets) — flagged for the checklist

## 4. Definition of Done (a story is done only when…)
- [ ] Code implements every acceptance criterion
- [ ] Tests at the levels agreed in the Test Strategy written and passing; regression test for any bug fixed
- [ ] Secure-coding checklist items for touched areas done; dependency scan clean or triaged
- [ ] Reviewed (code review skill or peer)
- [ ] Docs updated (API contract, runbook entry, ADR if a decision was made)
- [ ] Traceability row updated (STORY, component, TEST, status)
- [ ] Deployed to the agreed environment; feature flag state recorded

## 5. Current iteration
| Field | Value |
|---|---|
| Iteration / dates | |
| Iteration goal | |
| Items | STORY-… |
| Capacity notes | |

## 6. Review checkpoint (end of iteration)
Increment inspected against AC · stakeholder feedback · backlog changes made.

## 7. Retrospective checkpoint
| What to keep | What to change | Action → STATE.md |
|---|---|---|

## 8. Parking lot / later
Ideas and deferred items with the reason for deferral.

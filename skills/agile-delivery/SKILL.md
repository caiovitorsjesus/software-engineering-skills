---
name: agile-delivery
description: >-
  Turn a Requirements Spec into an executable Backlog: product goal, epics, stories with acceptance
  criteria, Definition of Ready and Done, iteration plan, review and retrospective checkpoints. Use when
  work must be planned or re-planned, a story lacks AC or is too big, at iteration start or end, or to
  schedule corrective actions from incidents or debt. Not for writing requirements (use requirements)
  or coding (use implementation).
license: MIT
compatibility: Designed for Claude Code and other Agent Skills runtimes. Reads and writes Markdown under docs/engineering/ in the target repository.
metadata:
  se-layer: discipline
  se-stage: planning
  se-version: "0.1.0"
---

# Agile Delivery

## Purpose

Maintain a Backlog that an agent or team can execute story by story: every story links to requirements, has testable acceptance criteria, meets a Definition of Ready before it starts and a Definition of Done before it counts. Uses Scrum vocabulary (Product Goal, Backlog, iteration goal, Definition of Done) without claiming Scrum conformance (see `../../references/scrum-vocabulary.md §3`).

## Use when

- The Requirements Spec passed its gate and no Backlog exists.
- An iteration starts (plan) or ends (review, retrospective).
- A story is too large, lacks AC, or fails Definition of Ready.
- Corrective actions (incident postmortem, tech debt, security findings) must be scheduled against features.
- Requirements changed and stories must be re-linked or re-prioritized.

## Do not use when

- Requirements are missing or ambiguous: `requirements`.
- A single story is ready and must be built: `implementation`.
- Process ceremony for a human team is requested (facilitation is out of scope; provide the checkpoints only).

## Inputs

| Input | Required | Source |
|---|---|---|
| Requirements Spec | yes | `docs/engineering/requirements.md` |
| Discovery Brief (vision, objectives) | no | `docs/engineering/discovery-brief.md` |
| Test Strategy (levels for DoD) | no | `docs/engineering/test-strategy.md` |
| Corrective items | no | postmortems, Tech Debt Register, security findings |
| Team capacity / iteration length | no | user (default: 2-week iterations, capacity unknown) |

## Procedure

1. **Set the Product Goal** from the vision and objectives (one sentence).
   Done when: the goal names the outcome and its measure.

2. **Form epics** from groups of `REQ-F` that deliver one outcome; each epic lists REQ coverage and an outcome metric.
   Done when: every Must/Should REQ-F belongs to exactly one epic.

3. **Write stories** `STORY-###`: "As a <role> I want <capability> so that <benefit>"; link REQ ids; reuse REQ acceptance criteria and add UI/edge cases; size so a story fits in one iteration and one reviewable change (`S:` ≤ 2 days of work; split otherwise by workflow step, data variation or interface).
   Done when: every REQ-F with priority Must/Should has ≥ 1 story; no story spans two epics.

4. **Define Ready and Done.** DoR: linked REQ (or DEBT/INC), testable AC, dependencies available, sized, security-relevance flagged. DoD: imports test levels from the Test Strategy, secure-coding checklist, review, docs, traceability, deployment/flag state (`../../templates/backlog.md §3–4`). `M/L:` add performance/accessibility items when REQ-N demands.
   Done when: DoR and DoD each have ≥ 5 checkable items and match the `story-done` gate.

5. **Prioritize** using the spec's method; security patches and blocking debt rank above features of equal value; record tie-break rule.
   Done when: the stories table is ordered; top items meet DoR.

6. **Plan the iteration.** Iteration goal (why this increment is valuable), items that fit capacity, dependencies confirmed; record in §5 of the Backlog.
   Done when: every planned story meets DoR; goal written.

7. **Review checkpoint** (iteration end): inspect the increment against AC with the stakeholder; record feedback → new/changed stories; requirement changes → `requirements` delta.
   Done when: every planned story is done, carried over (with reason) or dropped.

8. **Retrospective checkpoint**: what to keep, what to change, one to three actions → STATE.md log; measure throughput/cycle time trend (`../../references/engineering-metrics.md §2`).
   Done when: actions have owners; metrics noted.

9. **Refine continuously**: split, clarify, re-link stories until DoR; keep the "later" list explicit.
   Done when: the next iteration's candidate stories meet DoR.

## Outputs

| Artifact | Template | Location | Consumers |
|---|---|---|---|
| Backlog (goal, epics, stories, DoR, DoD, iteration, review/retro notes) | `../../templates/backlog.md` | `docs/engineering/backlog.md` | implementation, testing, maintenance, incident-response |

## Validation

- [ ] Product Goal present and measurable.
- [ ] Every Must/Should REQ-F maps to ≥ 1 story; every story links ≥ 1 REQ/DEBT/INC.
- [ ] Every story has testable AC.
- [ ] DoR and DoD present; DoD matches the `story-done` gate items.
- [ ] Order and tie-break rule recorded; security patches/blocking debt not below features of equal value.
- [ ] Iteration goal and items recorded; items meet DoR.
- [ ] Traceability table in the Requirements Spec updated with STORY ids.

## Stop and ask

- Priority conflict between stakeholders (H8).
- Scope change needed to make a story feasible (H2).
- Capacity unknown and the user wants a date commitment: "I can order the work but cannot forecast dates without capacity. Provide capacity, or accept an order without dates?"
- A corrective action from an incident competes with a committed feature: "Schedule <fix> before <feature>? Recommendation: yes because <risk>."

## Handoff

- → `implementation`: the top ready story (id, REQ links, AC, design pointers).
- → `testing`: DoD test levels; per-feature test plan hooks.
- → `requirements`: change requests discovered in review.
- STATE: Backlog row current; current iteration; next action = `implementation` for `STORY-###`.

## References

- `../../templates/backlog.md` — load when writing the backlog.
- `../../references/scrum-vocabulary.md` — load for vocabulary and the non-conformance boundary.
- `../../references/engineering-metrics.md` — load at retrospective for flow metrics.
- `../../references/requirements-quality.md` — load for AC patterns when stories lack criteria.
- `../sdlc-orchestrator/references/gates.md` — load to align DoD with `story-done`.

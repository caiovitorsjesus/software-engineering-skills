# Scrum Vocabulary as Used by This System

> Covers: Scrum Guide 2020 elements (theory, values, accountabilities, events, artifacts, commitments) and the explicit boundary of what `agile-delivery` borrows
> Retrieved: 2026-09-04
> Sources: https://scrumguides.org/scrum-guide.html
> Evidence: INDUSTRY, DECISION

Load when: planning iterations, writing Definition of Ready/Done, or when a team says it "does Scrum" and artifacts must map to theirs.

## 1. Scrum Guide 2020 in one table (INDUSTRY — Schwaber & Sutherland)

| Element | Content |
|---|---|
| Definition | "a lightweight framework that helps people, teams and organizations generate value through adaptive solutions for complex problems"; purposefully incomplete |
| Theory | empiricism and lean thinking; pillars: transparency, inspection, adaptation |
| Values | commitment, focus, openness, respect, courage |
| Scrum Team | Developers; Product Owner; Scrum Master (accountabilities); typically 10 or fewer people; cross-functional, self-managing |
| Events | the Sprint (≤ 1 month; container); Sprint Planning (≤ 8 h for a one-month Sprint); Daily Scrum (15 min); Sprint Review (≤ 4 h); Sprint Retrospective (≤ 3 h) |
| Artifacts → commitments | Product Backlog → Product Goal; Sprint Backlog → Sprint Goal; Increment → Definition of Done |
| Integrity clause | changing the core design, leaving out elements or not following the rules "covers up problems and limits the benefits of Scrum" — "the result is not Scrum" |

## 2. What `agile-delivery` borrows (DECISION D-10)

| Borrowed | How it is used here |
|---|---|
| Product Goal | one sentence at the top of the Backlog, derived from the Discovery Brief's vision |
| Product Backlog | the Backlog artifact: epics and stories linked to `REQ` ids, ordered |
| Sprint Goal / Sprint Backlog | "Iteration goal" and "Iteration items" sections; the word *Sprint* is used only when the team runs Scrum |
| Definition of Done | the DoD list in the Backlog, importing test/security/traceability hooks from other skills; a story is not done until every DoD item is checked |
| Sprint Planning purpose | the iteration planning step: why this iteration is valuable, what can be done, how |
| Sprint Review purpose | the review checkpoint: inspect the increment against AC with stakeholders; adapt the backlog |
| Sprint Retrospective purpose | the retrospective checkpoint: process changes recorded in STATE.md |
| Refinement | ongoing story splitting/clarification until DoR is met |

## 3. What this system does not claim

- It does not claim Scrum conformance. An AI agent cannot hold a Daily Scrum, be a Scrum Master, or self-manage as a team.
- Scrum organizes iterative work; it does not replace requirements engineering, architecture, testing, security, delivery engineering, operations or documentation. Those are separate skills here.
- Timeboxes above are informational; the system does not enforce event durations.
- Definition of Ready is not a Scrum Guide element; it is an industry practice adopted here to make stories agent-executable.

## 4. Mapping for teams that run Scrum

Backlog ≙ Product Backlog · Iteration ≙ Sprint · Iteration goal ≙ Sprint Goal · Review checkpoint ≙ Sprint Review · Retrospective checkpoint ≙ Sprint Retrospective · DoD ≙ Definition of Done. Keep the team's own tool as the source of truth for ordering; keep `REQ` links and DoD in both.

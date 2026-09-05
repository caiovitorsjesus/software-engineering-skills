---
name: discovery
description: >-
  Frame a software problem before requirements: problem statement, stakeholders, objectives with success
  criteria, scope, constraints, assumptions, options, feasibility verdict and initial risks. Use for a new
  idea or product, a "should we build this" question, a feasibility check, or when scope and stakeholders
  are unclear at the start of a modernization. Not for writing requirements (use requirements) or the
  backlog (use agile-delivery).
license: MIT
compatibility: Designed for Claude Code and other Agent Skills runtimes. Reads and writes Markdown under docs/engineering/ in the target repository.
metadata:
  se-layer: discipline
  se-stage: discovery
  se-version: "0.1.0"
---

# Discovery

## Purpose

Produce a Discovery Brief that states what problem is being solved, for whom, under which constraints, whether it is feasible, and how success will be measured — plus a seeded Risk Register — so that requirements work starts from an agreed, evidence-based frame and a go/no-go decision.

## Use when

- A new product, service or internal tool is proposed ("idea", "MVP", "build an app for …").
- Someone asks whether something should be built, bought or extended.
- Objectives, stakeholders or scope are unclear or contested.
- A legacy modernization needs its goals and feasibility framed (after `legacy-modernization` has produced the assessment).

## Do not use when

- The problem is framed and agreed: write requirements (`requirements`).
- The request is a feature on an existing, documented product: `requirements` (delta) via the add-feature workflow.
- Only a technical option must be chosen: `architecture` (ADR).

## Inputs

| Input | Required | Source |
|---|---|---|
| User intent (idea, request, pain point) | yes | user |
| Existing material (docs, tickets, market notes, legacy assessment) | no | repository / user |
| Stakeholder access or their known concerns | no | user |
| Stack or platform constraints already decided | no | user → `CON-###` |

## Procedure

1. **State the problem.** Who has it, what happens today, evidence (numbers, quotes, observations), cost of the problem, why now. Reject solution language ("we need an app") until the problem is stated without it.
   Done when: the problem statement names a user group, a current situation and at least one piece of evidence or an `ASM-###`.

2. **Map stakeholders and concerns.** List sponsors, users by role, operators, security/compliance, integrators. For each: influence, primary concerns, what success looks like (ISO/IEC/IEEE 42010 vocabulary: stakeholder → concern).
   Done when: every user role named in step 1 appears; a decision-maker for scope is identified (→ STATE roles).

3. **Set objectives and success criteria.** 2–5 objectives; each with a measurable criterion, how and when it is measured.
   Done when: every objective has a number or an observable outcome and a measurement method.

4. **Draw scope.** In / out / later. Out-of-scope items are explicit sentences, not omissions.
   Done when: at least three explicit exclusions exist or the sponsor confirms none.

5. **Record constraints and assumptions.** `CON-###`: technical, legal, budget, time, stack, organizational (a user-named stack is a constraint). `ASM-###`: each with the risk if false and a validation plan.
   Done when: every constraint has a source; every assumption has a validation plan.

6. **Compare options.** Build / buy or SaaS / extend existing / do nothing. Rough cost, time, fit. `S:` one row each; `M/L:` add integration and lock-in considerations.
   Done when: the table has all four rows with pros and cons.

7. **Assess feasibility.** Technical (known unknowns, spikes needed), operational (who runs and supports it), economic (cost vs. value), schedule, legal/regulatory (data classes: PII, payment, health → raises size class). Verdict: `go`, `no-go`, or `pivot` with the option.
   Done when: each dimension has an assessment and evidence; verdict stated with one-line reason.

8. **Seed risks.** Cause → event → consequence, likelihood, impact, response, owner, trigger. `S:` top 5 inside the brief; `M/L:` `risk-register.md`. Include the security risk profile inputs (data classes, exposure, attacker interest) for `security › A`.
   Done when: at least the top risks have responses and owners.

9. **Write the vision sentence** ("For <users> who <need>, <product> is a <category> that <benefit>; unlike <alternative>, it <differentiator>").
   Done when: one sentence, no adjectives without evidence.

10. **Propose size class** using `../sdlc-orchestrator/references/rightsizing.md §1`; list open questions with owners.
    Done when: STATE has size class + driver; every open question has an owner and a needed-by date.

## Outputs

| Artifact | Template | Location | Consumers |
|---|---|---|---|
| Discovery Brief | `../../templates/discovery-brief.md` | `docs/engineering/discovery-brief.md` | requirements, security, agile-delivery, architecture, sponsor |
| Risk Register | `../../templates/risk-register.md` | `docs/engineering/risk-register.md` (S: section in brief) | orchestrator, architecture, security, operations |

## Validation

- [ ] Problem statement contains no solution and cites evidence or an `ASM-`.
- [ ] Every objective has a measurable criterion and a measurement method.
- [ ] Explicit out-of-scope list present.
- [ ] Every `CON-` has a source; every `ASM-` has a validation plan.
- [ ] Feasibility has five dimensions assessed and a verdict.
- [ ] Data classes identified; size class proposed with driver.
- [ ] Top risks have response and owner.
- [ ] Vision sentence present.
- [ ] Gate `discovery-to-requirements` items answerable from the brief.

## Stop and ask

- Verdict `no-go` or `pivot` (H1): "Feasibility is <verdict> because <evidence>. Proceed anyway / pivot to <option> / stop? Recommendation: <…>."
- Stakeholders disagree on objectives or scope (H8): present both positions and a recommendation.
- Budget or deadline unknown and it decides feasibility: "Feasibility depends on <budget/date>. What is the ceiling / date? If unknown, I will assume <ASM> and mark the verdict provisional."
- Regulated data suspected (H9): "The product appears to process <data class>. Confirm, so compliance requirements and size class M/L apply."

## Handoff

- → `requirements`: Discovery Brief (objectives, scope, constraints, assumptions, stakeholders) and the Risk Register.
- → `security` (entry point A, risk profile): data classes, exposure, users, attacker interest.
- STATE: situation confirmed, size class + driver, artifact index rows for brief and risks, open questions (go/no-go), next action = `requirements`.

## References

- `../../templates/discovery-brief.md` — load when writing the brief.
- `../../templates/risk-register.md` — load when seeding risks.
- `../../references/lifecycle-map.md` — load for ID prefixes and stage names.
- `../sdlc-orchestrator/references/rightsizing.md` — load in step 10.
- `../sdlc-orchestrator/references/human-decisions.md` — load when a stop condition fires.

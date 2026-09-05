---
name: testing
description: >-
  Define and maintain the test strategy and per-feature test plans: levels (unit, component,
  integration, contract, end-to-end, performance, security, resilience, accessibility, exploratory,
  acceptance), what each verifies against ISO/IEC 25010, where they run, data, environments, exit
  criteria. Use when a Test Strategy is missing, a story needs tests planned, suites are flaky, or exit
  criteria are unclear. Not for product code (implementation).
license: MIT
compatibility: Designed for Claude Code and other Agent Skills runtimes. Reads and writes Markdown under docs/engineering/ and test code in the target repository.
metadata:
  se-layer: discipline
  se-stage: verification
  se-version: "0.1.0"
---

# Testing

## Purpose

Make verification deterministic: a Test Strategy that maps every quality characteristic and requirement to the level and technique that verifies it, exit criteria that gate releases, and per-feature test plans that implementation and the Definition of Done can execute.

## Use when

- Requirements and architecture exist and no Test Strategy exists (design stage, before construction starts).
- A story needs a test level that does not exist yet (contract, performance, e2e journey, resilience) or non-trivial test design; routine per-story `TEST-###` rows are written by `implementation` from the strategy's pattern.
- A release approaches and exit criteria must be evaluated.
- Suites are slow, flaky or missing levels (e.g., no contract tests between services).
- Legacy code needs characterization tests before modernization.

## Do not use when

- Writing the product code itself: `implementation` (which writes tests alongside).
- Security test *design* beyond what the strategy specifies: `security` (E) provides abuse cases; this skill places them in levels.
- Diagnosing a failing test's cause: `diagnosing-bugs` if available, else `implementation` reproduce → isolate.

## Inputs

| Input | Required | Source |
|---|---|---|
| Requirements Spec (AC, REQ-N methods) | yes | `docs/engineering/requirements.md` |
| Architecture Overview (containers, integrations) | strategy mode | `docs/engineering/architecture.md` |
| Story / Backlog item | per-feature mode | `docs/engineering/backlog.md` |
| Data Model, API Contract | no | `docs/engineering/` |
| Threat Model abuse cases | no | `docs/engineering/threat-model.md` |
| Stack test tooling and CI | yes | `STATE.md › Stack` |

## Procedure

1. **Map quality to verification.** For each ISO/IEC 25010:2023 characteristic with a `REQ-N`, name the level and tool that verifies it (`../../references/quality-model.md §3`, `../../references/testing-foundations.md §2`).
   Done when: every REQ-N has a verifying level; every characteristic row filled or "n/a".

2. **Define levels** for the size class: purpose, scope, technique families (specification-, structure-, experience-based), tools from the stack, where/when they run, exit criteria. `S:` unit, component, few e2e, dependency scan; a basic load check only if a performance `REQ-N` exists. `M:` + integration, contract, DAST, accessibility. `L:` + performance suites, resilience, exploratory, formal acceptance.
   Done when: the levels table is complete and every tool exists in the stack or is justified as new.

3. **Set environments and data**: fixtures/builders for unit/component; containerized dependencies for integration; anonymized or synthetic data for e2e/performance; no real PII outside production; per-test data isolation for parallel runs.
   Done when: every level has an environment and data source row.

4. **Map to CI**: which levels gate merge, which gate release, which are scheduled; time budget per stage (hand to `delivery-pipeline`).
   Done when: the automation section names stages and budgets.

5. **Write policies**: flakiness (quarantine within a day → `DEBT-###` → fix/delete window), regression (test at lowest reproducing level for every fixed defect), coverage rule (on changed code, not a global number).
   Done when: three policies written with numbers.

6. **Per-feature test plan** (each story): `TEST-###` rows — REQ/STORY, level(s), cases (happy, boundary, invalid, abuse from threat model), data, expected evidence. Push abuse cases and NFR checks that the story touches.
   Done when: every AC of the story has ≥ 1 TEST row; traceability TEST column filled.

7. **Evaluate exit criteria** before release: per level pass/fail with evidence; performance REQ-N verified; zero open High/Critical security findings or accepted; defects triaged.
   Done when: the `construction-to-release` gate test items are answerable with evidence links.

8. **Characterization mode (legacy)**: capture current behaviour as tests around the seams to be changed before any refactor; record known-wrong behaviour explicitly.
   Done when: every module scheduled for change has characterization coverage of its public behaviour.

## Outputs

| Artifact | Template | Location | Consumers |
|---|---|---|---|
| Test Strategy (levels, coverage, environments, CI mapping, policies, per-feature plans) | `../../templates/test-strategy.md` | `docs/engineering/test-strategy.md` | implementation, delivery-pipeline, agile-delivery |
| Test code and fixtures | stack convention | repository | delivery-pipeline |
| Traceability TEST ids and `verified` status | `../../templates/requirements-spec.md §11` | `docs/engineering/requirements.md` | orchestrator |

## Validation

- [ ] Every REQ-N has a verifying level; every 25010 characteristic addressed.
- [ ] Levels table complete for the size class; tools exist in the stack or justified.
- [ ] Environments and data rows for every level; no real PII outside production.
- [ ] CI mapping with merge/release/scheduled gates and time budgets.
- [ ] Flakiness, regression and coverage policies with numbers.
- [ ] Per-feature: every AC has a TEST row; traceability updated.
- [ ] Exit criteria measurable and evaluated with evidence at release.

## Stop and ask

- A performance or availability target cannot be verified without paid/large environments (H10): "Verifying <REQ-N> needs <environment/cost>. Provision / verify at reduced scale with extrapolation (risk) / relax target?"
- User asks to release with failing exit criteria (H13): state the specific risk; record acceptance as `RISK-###` if confirmed.
- Real production data requested for testing (H9): refuse by default; offer anonymization.

## Handoff

- → `implementation`: test plan rows for the story; fixtures/builders to use.
- → `delivery-pipeline`: CI stage mapping, budgets, tools to install.
- → `agile-delivery`: DoD test items; flaky-test debt.
- → `security`: gaps in abuse-case coverage.
- STATE: Test Strategy row current; traceability statuses.

## References

- `../../templates/test-strategy.md` — load when writing the strategy or a per-feature plan.
- `../../references/testing-foundations.md` — load for levels, technique families, contract tests, flakiness, exit criteria.
- `../../references/quality-model.md` — load in step 1.
- `../../references/security-framework-map.md` — load for the security test level (SSDF PW.8, ASVS use as test design).

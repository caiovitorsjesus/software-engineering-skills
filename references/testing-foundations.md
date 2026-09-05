# Testing Foundations

> Covers: test levels and purposes; ISO/IEC/IEEE 29119 concepts adopted (process layers, technique families) and the documentation-weight controversy; test pyramid guidance; contract testing; test data and environments; flakiness; exit criteria
> Retrieved: 2026-09-04
> Sources: https://en.wikipedia.org/wiki/ISO/IEC_29119 ; ISO/IEC 25010:2023 vocabulary via references/quality-model.md
> Evidence: STANDARD, INDUSTRY, RECOMMENDATION, DECISION

Load when: writing the Test Strategy, deciding which tests a story needs, or diagnosing weak/flaky suites.

## 1. What is adopted from ISO/IEC/IEEE 29119 (STANDARD → DECISION D-11)

- Parts: 1 Concepts and definitions (2022), 2 Test processes (2021), 3 Test documentation (2021), 4 Test techniques (2021), 5 Keyword-driven testing (2024).
- Process layers (Part 2): organizational test process; test management processes; dynamic test processes. This system keeps one **Test Strategy** (organizational + management, lite) with **per-feature test plan sections** (dynamic), and records completion evidence in the traceability table — not the full Part 3 document set.
- Technique families (Part 4): **specification-based** (equivalence partitioning, boundary values, decision tables, state transitions, scenario tests), **structure-based** (statement/branch/condition coverage), **experience-based** (error guessing, exploratory, checklist-based). Use all three families; name which applies per level.
- Context: professional testing associations criticized 29119 for documentation weight; this system therefore treats strategy and evidence as the minimum documentation and lets tests themselves be the specification of detail.

## 2. Test levels and purpose (INDUSTRY/RECOMMENDATION)

| Level | Verifies | Typical scope | Where it runs | Quality characteristics covered |
|---|---|---|---|---|
| Unit | one module's logic in isolation | functions, classes, pure rules | every commit, local + CI | functional correctness, maintainability (testability) |
| Component | one deployable's behaviour with real internal wiring, fakes at the edges | service with in-memory DB / test containers | CI | functional suitability |
| Integration | interaction with real dependencies (DB, queue, external API sandbox) | repository/adapters, message handlers | CI (slower stage) | compatibility, reliability |
| Contract | provider and consumer agree on the interface | API schema / event schema, consumer-driven contracts | CI on both sides | compatibility (interoperability) |
| End-to-end | a user journey across the system | few critical journeys | CI nightly / pre-release | functional suitability, interaction capability |
| Performance | time behaviour, capacity, resource use under load | load, stress, soak, spike | pre-release / scheduled | performance efficiency, flexibility (scalability) |
| Security | absence of known vulnerability classes; abuse cases | SAST, DAST, dependency scan, auth/authz abuse tests | CI + pre-release | security |
| Resilience | behaviour under dependency failure | fault injection, failover, restart | M/L pre-release | reliability (fault tolerance, recoverability) |
| Accessibility / usability | inclusivity, operability | automated a11y checks + manual review | pre-release | interaction capability |
| Exploratory | unknown unknowns | charter-based sessions | before release | all |
| Acceptance | stakeholder confirms value | AC walk-through, UAT | release gate | functional appropriateness |

Right-sizing: `S` unit + component + a few e2e + dependency scan + basic load check; `M` adds integration, contract (if >1 service or external consumers), security DAST, accessibility; `L` adds performance suites, resilience, exploratory sessions, formal acceptance.

## 3. Shape of the suite (RECOMMENDATION)

Many fast unit/component tests; fewer integration/contract; very few e2e. Rule of thumb: an e2e test exists only for a journey whose failure would be a P1 incident. Every defect fixed gets a regression test at the lowest level that reproduces it.

## 4. Contract testing (INDUSTRY)

Use when two independently deployed parts communicate. Provider publishes/validates against the contract (OpenAPI/GraphQL/AsyncAPI); consumer-driven contracts when the consumer is known and evolves independently. Breaking-change detection runs in CI before merge.

## 5. Test data and environments (RECOMMENDATION)

- Data: deterministic fixtures/builders for unit/component; anonymized or synthetic production-like data for performance and e2e; never real PII outside production (`data-foundations.md §6`).
- Environments: ephemeral per-branch where possible; a stable staging with production parity (Twelve-Factor dev/prod parity); seed scripts versioned with the code.
- Isolation: each test owns its data (unique ids/tenants) so suites run in parallel.

## 6. Flakiness policy (RECOMMENDATION)

A test that fails intermittently is quarantined within one day, tracked as `DEBT-###`, and fixed or deleted within an agreed window. Root causes are usually: shared state, timing/sleep, order dependence, real network calls, clock dependence. Treat as a concurrency bug first (`cs-foundations.md §2`).

## 7. Exit criteria per level (RECOMMENDATION)

Define numerically in the Test Strategy: e.g., unit/component pass 100 %; coverage on changed code ≥ X %; zero open High/Critical security findings; performance targets met for all `REQ-N` performance rows; e2e critical journeys green; accessibility checks at the agreed WCAG level; known defects triaged with severity and decision.

## 8. Definition of Done hooks

`agile-delivery` DoD imports: tests at agreed levels written and passing; regression test for each bug fixed; traceability `TEST-###` filled; flaky tests not merged.

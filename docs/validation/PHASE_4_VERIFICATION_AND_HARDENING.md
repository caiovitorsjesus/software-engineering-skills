# Phase 4 — Independent Verification and Hardening

Date: 2026-09-05. Input: a third-party audit reporting security, orchestration, context, contract, reliability, modularity, testing and metadata problems. Method: verify each claim against the repository before changing anything; fix what is substantiated; reject what is not, with evidence.

## 1. Executive verdict

Of the third-party findings, **six are confirmed**, **three are partially confirmed**, **six are false positives or not applicable**, and **three are architectural preferences with no demonstrated defect**. The confirmed set is real and worth fixing: the repository had no rule telling an agent that content it reads from a project (README, logs, dependency changelogs) is evidence rather than instruction, two repair loops had no bound, six skills promised handoffs the orchestration graph did not declare, and there were no behavioral tests at all.

The audit's headline security claim — unrestricted or destructive shell execution guidance — **does not exist in this repository**. A grep for destructive command patterns across every skill, reference, template and workflow returns nothing, and no file instructs an agent to bypass approval. What was genuinely missing was the *stated boundary*: which mutations are free, which need verification first, and which need approval. That is now written down.

The audit's architectural recommendation (restructure to `Core → Agents → Skills → Tests/Evals`, add lazy loading, JSON Schema handoffs) is **rejected on measurement**. Only 1,868 tokens load on every turn — the sixteen skill descriptions. Bodies, references and templates load on invocation, which is already lazy loading; the heaviest measured session is 16.6k tokens. Restructuring would recreate the very context problem the recommendation claims to solve.

**Architecture unchanged. Nine targeted fixes, one new eval layer.**

## 2. Findings table

| ID | Third-party claim | Classification | Severity | Action |
|---|---|---|---|---|
| T-01 | Unrestricted/destructive shell execution guidance | FALSE POSITIVE | — | None. No destructive command guidance exists (grep evidence §3.1) |
| T-02 | Insufficient human approval boundaries for mutations | PARTIALLY CONFIRMED | Medium | Mutation classes added (D-28) |
| T-03 | Indirect prompt injection when reading repo files, logs, dependencies | CONFIRMED | High | Untrusted-content rule + 7 skill pointers + 3 fixtures (D-26) |
| T-04 | No distinction between trusted instructions and untrusted project data | CONFIRMED | High | Same as T-03 |
| T-05 | Excessive static context loading | FALSE POSITIVE | — | Measured: 1,868 tokens always-loaded (§3.3) |
| T-06 | Insufficient lazy/on-demand skill loading | NOT APPLICABLE | — | Claude Code already loads bodies on invocation; progressive disclosure is the design (ARCHITECTURE §3.2) |
| T-07 | Excessive coupling between global rules and local skills | FALSE POSITIVE | — | Shared rules live in `references/`, pointed at, never copied |
| T-08 | Duplicated instructions | FALSE POSITIVE | — | Workflows are 34–50 lines and duplicate no skill content |
| T-09 | Insufficiently formal skill/workflow handoffs | PARTIALLY CONFIRMED | Medium | Handoff prose now machine-checked against the graph (D-29) |
| T-10 | Missing structured input/output contracts | ARCHITECTURAL OPTION | — | Rejected: registry inputs/outputs + Inputs tables are the contract |
| T-11 | Weak machine validation of handoffs | CONFIRMED | Medium | 6 drift cases found and fixed; validator check added (D-29) |
| T-12 | Missing/insufficient loop and retry limits | CONFIRMED | High | Bounded attempts with progress criterion (D-27) |
| T-13 | Possible infinite self-correction | CONFIRMED | High | Same as T-12; gate loop bounded at two rounds |
| T-14 | Weak failure recovery semantics | ALREADY MITIGATED | — | Phase 3 added resume points, as-found fallbacks, dead-end handling |
| T-15 | God Skills / overly broad skills | ARCHITECTURAL OPTION | — | Rejected: all bodies 99–126 lines against a 500 cap (§3.4) |
| T-16 | Redundant or cosmetic agent roles | FALSE POSITIVE | — | No agent roles exist; 16 skills each with distinct outputs |
| T-17 | Premature specialization | ARCHITECTURAL OPTION | — | Rejected: splitting inflates the always-loaded listing (D-07, D-08) |
| T-18 | Absence of behavioral Evals | CONFIRMED | High | `evals/` with 17 cases + `scripts/run_evals.py` |
| T-19 | No prompt-injection fixtures | CONFIRMED | High | 3 fixtures under `evals/fixtures/injection/` |
| T-20 | No routing regression tests | CONFIRMED | Medium | 5 routing cases, referentially checked against the registry |
| T-21 | No structured-output tests | PARTIALLY CONFIRMED | Low | Covered by validator graph checks; no separate layer added |
| T-22 | No context/budget regression tests | CONFIRMED | Medium | 3 context cases with measured budgets, deterministic |
| T-23 | Missing skill versioning metadata | FALSE POSITIVE | — | All 16 skills carry `metadata.se-version`; registry has `version` |
| T-24 | Inconsistent terminology | FALSE POSITIVE | — | Canonical artifact names used consistently across 16–24 files each |
| T-25 | Restructure to Core → Agents → Skills → Evals | ARCHITECTURAL OPTION | — | Rejected on measurement (§1, §8) |

## 3. Verification evidence

### 3.1 Security — destructive commands and approval bypass (T-01, T-02)

`grep -rnE "rm -rf|--force|force push|reset --hard|DROP TABLE|TRUNCATE|--no-verify|chmod 777|sudo"` across `skills/ references/ templates/ workflows/` returns **no** guidance authorizing such operations. Every `force` match is product-security advice (prohibiting force-push to release branches, brute-force mitigation, mobile forced-update policy). No file instructs the agent to skip approval; `human-decisions.md` already defines H1–H14 including H6 (irreversible data operations) and H7 (production deploy/rollback).

What was missing: a statement of which mutations are free versus approval-gated. A skill repository cannot sandbox operating-system privileges — that belongs to the runtime — so the fix is the strongest policy a repository *can* state: `references/agent-working-rules.md §9` classifies mutations as free / verify-first / approval-required, and forbids widening permissions, disabling a check or bypassing a hook to make a step pass. No command allowlist was added; it would make ordinary development unusable and could not be enforced anyway.

### 3.2 Indirect prompt injection (T-03, T-04) — the most serious confirmed gap

Twelve skills ingest content the project or the outside world controls. The only "untrusted" language in the repository concerned the *product* handling untrusted input (`backend.md`, `frontend.md`, the secure-coding checklist) — nothing addressed the *agent* treating a directive found in a file as authority. An attacker who can write a README, a dependency changelog or a log line had an unanswered path to the agent's behaviour.

Fix: one rule in `references/agent-working-rules.md §8` — instructions come from the user session and this system; everything read is evidence; a directive addressed to the agent inside project content is a finding to report, and a security finding when it sits in code or dependencies. Seven skills point at §8 at the step where they ingest (orchestrator step 2, requirements step 2, implementation step 1, security D, incident-response step 5, maintenance step 4, legacy-modernization step 2). Three hostile fixtures exercise it. XML delimiters everywhere were rejected as heavier and no more reliable than a stated rule the ingesting steps point at.

### 3.3 Context (T-05 – T-08) — rejected on measurement

| What | Loaded | Tokens |
|---|---|---|
| Skill descriptions (every turn) | 16 | **1,868** |
| Skill bodies | on invocation | 29,699 total, ~110 lines each |
| References | on demand, per "load when" pointer | 30,205 total |
| Templates | when producing the artifact | 9,935 total |
| Registry | workflow entry + named skills only | 3,803 full |

Measured sessions: new-product first step 10,272 tokens; heaviest add-feature story 16,612; incident 7,370. The claim of excessive static loading is not supported. These three measurements are now regression-guarded as context eval cases, so future bloat fails a check rather than going unnoticed.

### 3.4 Modularity (T-15 – T-17) — rejected

Skill bodies run 99–126 lines against a 500-line cap. `security` carries seven entry points in 123 lines by design (D-08): splitting it into three skills would add two descriptions to the always-loaded listing to solve a problem the line counts do not show. No agent roles exist to be redundant.

### 3.5 Handoff drift (T-09, T-11) — confirmed, six cases

A script comparing each `## Handoff` section against the registry graph found six skills promising handoffs the orchestrator could not walk: `data-design → operations`, `testing → security`, `security → operations`, `delivery-pipeline → incident-response`, `incident-response → agile-delivery`, `maintenance → legacy-modernization`. All six are legitimate and were added to the registry. `scripts/validate.py` now performs this comparison on every run; verified by removing an edge and confirming the failure, then restoring.

### 3.6 Loops (T-12, T-13) — confirmed, two cases

`implementation` step 4 ("implement, run tests, fix, continue") and the orchestrator's gate step ("gate failure → return to the skill") had no bound. Fixed with progress-based bounds rather than a uniform retry count, because the right bound differs by loop kind (D-27).

## 4. Changes implemented

**P0 — security**
1. `references/agent-working-rules.md §8` untrusted content; §9 mutation classes.
2. Untrusted-content pointers at the ingesting step of seven skills.
3. Three injection fixtures with mandatory `TEST FIXTURE` headers.

**P1 — reliability**
4. `agent-working-rules.md §2` bounded attempts table with a progress criterion.
5. `sdlc-orchestrator` step 6: two correction rounds per gate, then record blocked and raise an open question.
6. `implementation` step 4: bounded repair and diagnosis with escalation.
7. Six registry handoff edges added; handoff-drift check in `scripts/validate.py`.

**P2/P3 — evaluation**
8. `evals/cases.yaml` (17 cases: 5 routing, 3 safety, 3 injection, 2 continuity, 1 human-decision, 3 context), `evals/README.md`, `evals/fixtures/`, `evals/results/`.
9. `scripts/run_evals.py`: deterministic structure, referential integrity and context budgets; `--prompts` emits the agent-run harness. It never fabricates a behavioral verdict.
10. Decisions D-26…D-29; `ARCHITECTURE.md §12`, `README.md` and `SKILL_AUTHORING.md` updated.

Not implemented, deliberately: command allowlists, JSON Schema handoff payloads, skill splits, non-standard frontmatter fields, and the `Core → Agents → Skills → Evals` restructure.

## 5. Validation results

| Check | Result |
|---|---|
| `python scripts/validate.py --strict` | 0 errors, 0 warnings (now including handoff-drift, graph availability, producer/consumer consistency) |
| `python scripts/run_evals.py` | 17 cases, 0 deterministic failures; budgets at 83–86 % |
| `claude plugin validate . --strict` (Claude Code 2.1.258) | Validation passed |
| Handoff-drift check, negative test | Removing one edge produced the expected error; restored clean |
| Eval runner, negative test | Unknown situation, unknown `H` id and an exceeded budget each failed as expected |
| `skills-ref` | Not installed. Not run, not fabricated |
| Behavioral eval half | **Not run.** Requires an agent session; `evals/results/` is empty and says so |

## 6. Remaining risks

1. **The behavioral half is unrun.** The evals define the checks; nobody has executed them against a live agent yet. This is the single largest gap and the reason readiness is not raised.
2. **Injection defence is a stated rule, not an enforced boundary.** A repository can tell an agent to treat content as evidence; it cannot prevent a model from being persuaded. The fixtures measure how well the rule holds; runtime permissions remain the real boundary.
3. **Bounds depend on adherence.** Nothing mechanically counts attempts.
4. Carried from Phase 3: ISO summaries via secondary sources; desk-simulated scenarios; judgment-dependent stops (H3).

## 7. Architectural impact

None structural. The layer model (orchestrator → workflows → skills → artifacts/references → validation) is unchanged; `evals/` is a sibling of `scripts/`, not a new layer in the dependency chain. Sixteen skills, five workflows, seventeen artifacts and eight gates are unchanged in count and responsibility. Every change was a targeted edit to an existing file plus one new directory.

## 8. Recommended next step

Run the behavioral half. `claude --plugin-dir .` in a scratch project, then `python scripts/run_evals.py --prompts` and work through the fourteen behavioral cases, recording each under `evals/results/`. The injection and safety cases matter most: they test the two rules added here. Until that is done the system stays at **READY WITH MINOR ISSUES**, and the evals are a specification of correct behaviour rather than evidence of it.

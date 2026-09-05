# Phase 3 — Adversarial Audit

Date: 2026-09-05. Auditor stance: independent senior reviewer trying to break the system before declaring it ready. System under test: the repository as left by Phase 2 (strict-green validator, five scenario walkthroughs).

## 1. Executive summary

The Phase 2 system was structurally sound but **behaviorally wrong in three places that static validation could not see**: the orchestrator's skip rule would have skipped `implementation` forever (its registry outputs are empty, so "all outputs current" was vacuously true) and suppressed every recurring skill after its first artifact; the timestamp-based freshness rule would have marked all design artifacts stale after every traceability edit, re-running design skills per story; and `requirements` required a Discovery Brief, so any feature on an existing undocumented repository would have triggered `discovery` — a document-first detour that makes the system unusable for ordinary work. A graph simulation of every workflow against the registry found five further dead ends (design and operations skills whose required inputs no earlier step in the delta, incident or hardening paths produces) and 20 artifact consumer declarations not mirrored in skill inputs. The agent could also silently accept material ADRs.

All of these were corrected within the architectural intent (D-23…D-25), the validator now performs the graph simulation and consumer/producer consistency checks permanently, and strict validation plus Claude Code plugin validation pass. Ten failure-mode cases and three simulated sessions run through the corrected system without dead ends. Residual risk is concentrated in one place: the procedures have been exercised by desk simulation, not by live agent runs on real repositories.

**Readiness: READY WITH MINOR ISSUES.**

## 2. Scope
Everything under `skills/`, `workflows/`, `references/`, `templates/`, `scripts/`, `.claude-plugin/`, `README.md`, `docs/*.md`, `docs/validation/*`. Behavioral correctness, lifecycle coverage, skill content, workflows, artifacts, registry semantics, security integration, testing integration, context efficiency, human-autonomy boundary, failure modes, simulated sessions, compatibility, cross-system consistency, over-engineering.

## 3. Methodology
1. Adversarial read of every skill procedure asking: how could an agent misuse, skip, loop on, or misroute this?
2. Registry graph analysis by script: input-availability simulation per workflow from realistic start states; orphan artifacts; unreachable skills; consumer/producer ↔ input/output consistency.
3. Consistency greps: terminology (Sprint/PRD/SRS), gate ids, H-ids, artifact paths, size-class wording.
4. Ten failure-mode cases and three simulated sessions traced through the actual files, with context cost measured by character count of the files an agent would load.
5. Tool checks: `python scripts/validate.py --strict`, `claude plugin validate . --strict` (Claude Code 2.1.258 present); `skills-ref` not installed — not run, not fabricated.
6. Corrections applied only when reversible, within intent, and not requiring a product decision; decisions logged as D-23…D-25.

## 4. Overall assessment
Architecture (layers, 16 skills, gates, STATE, registry) remains valid. The defects were in orchestration rules and registry wiring, not in the taxonomy. After correction the system routes existing-system work without document-first detours, never starves the construction loop, and puts material decisions in front of a human at one batched point.

## 5. Critical findings

| ID | Component | Problem | Why it matters | Evidence | Correction |
|---|---|---|---|---|---|
| C-1 | `sdlc-orchestrator` step 5; registry | Skip rule "all outputs current → skip" is vacuously true for `implementation` (outputs `[]`) and true for `security`/`testing`/`agile-delivery`/`operations`/`maintenance` once their first artifact exists. | A literal agent never runs construction; recurring disciplines stop after one pass — no code, no per-story security or tests. | `skills/registry.yaml` implementation `outputs: []`; Phase 2 orchestrator text. | Skip-by-freshness applies only to `recurring: false`; recurring skills run on their entry condition (orchestrator step 5; `state-file.md §3`; registry header). D-23. |

## 6. High findings

| ID | Component | Problem | Why it matters | Correction |
|---|---|---|---|---|
| H-1 | `state-file.md §3`, orchestrator step 4 | Freshness = any later timestamp on an input. Traceability rows are edited by three skills per story. | Every design artifact flips to `stale` each story → design skills re-run, context and churn explode. | Freshness reads `Last substantive change` (change-log entry, new/superseded ADR, schema/contract change, new High threat, new container). STATE index gains the column. D-23. |
| H-2 | `requirements` inputs; registry | Discovery Brief required. | Any feature on an existing undocumented repo schedules `discovery` (wrong artifact, wrong cost). | `discovery-brief?`; delta mode bootstraps product context from README/code with `ASM-`; repair procedure says never schedule discovery for existing systems. D-24. |
| H-3 | `implementation` "Do not use when" / Inputs | Blocked without an Architecture Overview. | Ordinary work on existing repos impossible without writing architecture docs first. | "Architecture as found" from code; block only on an unidentifiable boundary. D-24. |
| H-4 | Registry graph (`data-design`, `api-design`, `operations`, `delivery-pipeline`, `implementation`) | Required inputs (`domain-model`, `deployment-plan`, `architecture-overview`, external `backlog-item`) that no earlier step produces in add-feature / incident / hardening / legacy sequences. | Dead ends: orchestrator would force-schedule domain-model or delivery-pipeline before an incident baseline or a schema delta. | Inputs made optional with "as found" fallbacks; `implementation` consumes `backlog`; validator now simulates input availability per workflow (0 blocked). |
| H-5 | `architecture` step 9; `adr.md` | Agent wrote ADRs as `accepted`. | Style, store, hosting, authn decided silently — a material architectural decision without authorization. | ADRs default `proposed`; `design-to-construction` gate requires batched human acceptance. D-25. |

## 7. Medium findings

| ID | Component | Problem | Correction |
|---|---|---|---|
| M-1 | Orchestrator classification | No route for trivial changes; every fix paid full orchestration; thin docs could route features to `legacy`. | `small-change` → `maintenance` directly; tie-break: existing system defaults to `add-feature`. D-24. |
| M-2 | `design-to-construction` gate | Read as "design everything before any code" (waterfall pressure, worst for S). | Scope rule: gates evaluated for the next increment (walking skeleton); expensive-to-change decisions up front, Data/API/Test grow per epic. |
| M-3 | `incident-closure` gate | Postmortem mandatory for every incident. | Required when an SRE trigger applies; short record otherwise. |
| M-4 | Risk Register | Reviewed only at the discovery gate → documentation dead end afterwards. | Review items added to `design-to-construction` and `construction-to-release`; wired as input to orchestrator, requirements, architecture, security, operations. |
| M-5 | `add-feature` step 4 | Threat-model condition vague ("new trust boundary"). | Explicit list: authn, authz, sessions/tokens, secrets, personal/regulated data, payments, file upload, new interface; DoR flag decides. |
| M-6 | `stack-adaptation.md` | Detection reads `.env`/config; could copy secret values into STATE/chat. | Names only; never print values; committed secret → High finding. |
| M-7 | `incident-response` step 3 | Rollback/wipe before evidence preservation on suspected breach. | Preserve evidence, contain rather than wipe, involve security G / H9. |
| M-8 | `implementation` ⇄ `testing` per story | Invoking `testing` for every story doubles context for routine work. | `implementation` writes TEST rows from the strategy pattern; `testing` only for new levels or non-trivial design. |
| M-9 | `security` D | No fallback when the stack has no scanner. | S: manual checklist + DEBT to add scanner; M/L: pipeline adds scanning before release. |
| M-10 | `requirements` §5 vs `security` B | Two skills author the same section ("may co-author"). | Requirements drafts, security reviews/completes; one author per edit. |
| M-11 | Registry | 20 artifact `consumers` not mirrored in skill `inputs`; 4 artifacts never an input (risk-register, backlog, adr, tech-debt-register). | Inputs aligned; validator enforces consumer↔input and producer↔output/updates consistency. |
| M-12 | `docs/ARCHITECTURE.md §7.4`, `security-framework-map.md §3` | Pre-D-20 size wording ("external users → M") survived. | Superseded note added; ASVS mapping aligned to D-20. |

## 8. Low findings

| ID | Component | Problem | Correction |
|---|---|---|---|
| L-1 | `testing` step 2 | "Basic load check" imposed on every S project. | Only if a performance REQ-N exists. |
| L-2 | STATE log | Unbounded growth vs. "two screens". | Keep last 10 entries. |
| L-3 | H10 | Could stop for free tiers / already-used vendors. | Added to "Not a stop". |
| L-4 | Registry `updates` | Updater may hit a missing artifact (security → tech-debt). | Rule: updater creates from template if absent. |
| L-5 | `architecture` step 9 | ADR list read as mandatory for all (e.g., frontend ADR for an API). | "for each that applies". |
| L-6 | `api-design` step 3, `operations` step 3 | Assumed validator tooling / staging exist. | Manual review fallback; pre-production or local for S. |
| L-7 | Orchestrator inputs | "Read registry" implied loading all 200+ lines. | Read the workflow entry and the skills/artifacts it names. |
| L-8 | `workflows/new-product.md` | `no-go` backticked → validator flagged as unknown identifier (Phase 2 leftover). | Plain text. |

## 9. Observations (not defects)
- O-1 Skill bodies are 99–126 lines; the ten-section contract costs ~20 lines of scaffolding per skill. Acceptable; a shorter "Inputs/Outputs" table form could save ~10 %.
- O-2 The system relies on the agent honoring `Done when` criteria; there is no mechanical enforcement beyond gates. Live runs should check adherence.
- O-3 `references/cs-foundations.md` thresholds are heuristics by design (labelled); an agent should not quote them as facts.
- O-4 Registry `handoffs` are broad (orchestrator → all); useful for validation, less so for navigation — the workflows are the navigational structure.
- O-5 Scenario walkthroughs in `docs/validation/scenario-*.md` still describe Phase 2 sequencing (e.g., `testing` per story); the workflows now say `implementation` writes routine TEST rows. The walkthroughs remain valid as records of what was tested then; not rewritten.

## 10. Orchestration assessment
Classification table now has seven situations with tie-breaks; ambiguity → H14. Stage detection via artifact status with content-based freshness. Size class assigned with a driver and only rises. Missing information → schedule producer or Stop-and-ask; user-knowledge gaps go to H-list. Skill selection: non-recurring skipped when fresh, recurring on entry condition, conditional steps logged when skipped. Resume after incident via `Suspended workflow`. Partially completed work: `draft` status; repair procedure for missing STATE. Conflicting docs vs. code: repo is truth for *what is*, docs for *what was intended*; discrepancy becomes an open question and a superseding ADR (state-file §4 2b). Stop conditions: H1–H14 with wording. Remaining weakness: the orchestrator cannot verify that a discipline skill actually satisfied its Validation list — it trusts the report; gates mitigate.

## 11. Skill assessment
All 16 read as executable procedures with decision criteria and completion criteria. Strongest: `requirements`, `architecture`, `security`, `incident-response`, `legacy-modernization`. Weakest before fixes: `implementation` (blocked on docs) and `testing` (over-invoked). Overlaps resolved by "Do not use when" pointers; the only shared authorship (security requirements) now has an owner. Verbosity: Handoff and References sections repeat STATE-update language — tolerated for determinism. No skill is generic advice: each names inputs by path and outputs by template.

## 12. Workflow assessment
Five workflows; registry sequences match files (validator-enforced); gates present at every transition; human stops listed; dead-end sections in each. Mid-process entry works through STATE repair + delta modes. Loops are bounded: requirements↔agile-delivery via change log; implementation↔architecture via ADR + H-stop; incident → previous workflow via resume point. Exit criteria reachable for S (walking-skeleton scope rule).

## 13. Artifact assessment
Every artifact: producer, consumers wired as inputs (validator-enforced), path, freshness via substantive-change rule, behaviour when missing (bootstrap/as-found/`embedded`/create-from-template), conflict rule (repo vs. docs). Dead ends removed: Risk Register (gate reviews), Backlog (implementation input), ADR (implementation/pipeline/maintenance inputs), Tech Debt Register (agile-delivery/architecture inputs). API Contract remains template-less by design (standard formats).

## 14. Registry / graph assessment
Semantic checks now automated: unknown ids, stage keys, gate ids, template existence, producer↔outputs/updates, consumer↔inputs, handoff reachability, workflow input-availability simulation from realistic start states, no-consumer warnings. Graph after fixes: 0 blocked steps, 0 orphan artifacts, 0 unreachable skills. An independent agent can navigate: workflow → sequence → skill entry → inputs (paths) → outputs (templates) → gate.

## 15. Security assessment
Security is enforced at gates (A at discovery, B at requirements, C at design, D at story-done, E/F at release, G at operations/incident) and mapped to SSDF/SAMM/ASVS/Top 10 ids. Bypass attempts: add-feature without step 4 → now blocked by the explicit trigger list and DoR flag; story without D → `story-done` fails; release without E/F → `construction-to-release` fails; legacy without security exposure assessment → Legacy Assessment §3 requires it. Conditionality: checklist items are "tick only items relevant to touched areas"; ASVS level by class; scanner fallback by class. New in Phase 3: secret exposure during stack detection prevented; breach evidence preservation. Residual: the agent's honesty in ticking checklist items is unverified without live runs.

## 16. Testing / quality assessment
Levels distinguished (unit, component, integration, contract, e2e, performance, security, resilience, accessibility, exploratory, acceptance) with purpose, scope, technique family, where run, exit criteria, and 25010 coverage mapping; strategy defined at design time and grown per epic; per-story tests written by `implementation` from the strategy pattern; regression policy; characterization for legacy; exit criteria evaluated at release with evidence. Unrealistic universal requirement removed (S load check now conditional). Test artifacts consumed: Test Strategy by implementation (TEST pattern), delivery-pipeline (CI stages), agile-delivery (DoD); TEST ids in traceability.

## 17. Context-efficiency assessment (measured, chars/4 ≈ tokens)

| Session | Files loaded | Chars | ≈ tokens |
|---|---|---|---|
| A — new product, first step (orchestrator + rightsizing + stack-adaptation + STATE template + discovery + brief + risk templates + gates) | 8 | 40,586 | 10.1 k |
| B — add-feature story on mobile/backend (orchestrator + state-file + requirements + req-quality + agile-delivery + backlog template + implementation + mobile + backend refs + checklist + gates) | 11 | 65,236 | 16.3 k |
| C — incident (orchestrator + incident-response + postmortem template + ops-foundations + human-decisions) | 5 | 29,480 | 7.4 k |
| Always-loaded listing (16 descriptions) | — | 7,056 | 1.8 k |
| Full registry (should be read partially) | 1 | 15,212 | 3.8 k |

Session B is the heaviest realistic path; it is high because two platform references and the checklist are loaded. Reductions made: registry partial read; `testing` not per story. Further reduction possible (O-1) but not at the expense of procedure completeness.

## 18. Human-autonomy assessment
Fourteen triggers with wording; "Not a stop" list expanded (free tier, already-used vendor, proposed ADRs). Silent material decisions closed: ADR acceptance at gate (H-5). Scope changes → H2 via change log. Assumptions are `ASM-` with validation plans, distinct from decisions. Reversible choices do not stop. Recommendation vs authorization: every stop presents options + recommendation; gates record human approval. Possible over-asking remains in H3 ("significant cost" is judgment) — acceptable.

## 19. Failure-mode results

| Case | Classification | Skills run / skipped | Gates & stops | Outcome after fixes | Recovery path |
|---|---|---|---|---|---|
| 1 Missing requirements ("add export, you know what I mean") on existing app | add-feature | requirements delta (bootstrap context, `ASM-`, elicitation checklist) → agile-delivery; design skills skipped unless schema/contract touched | requirements-to-design (delta); ask only for blocking unknowns (format? audience?) | Spec with provisional REQs and open questions; story ready when AC testable | If ambiguity blocks AC → Stop-and-ask, else proceed under ASM |
| 2 Contradictory requirements (finance wants immutable invoices; sales wants edits after send) | add-feature / new-product | requirements step 8 detects conflict | H8 with both positions and recommendation (versioned credit-note pattern) | Human decides; change log records | Domain-model invariant updated; ADR if structural |
| 3 Stale architecture doc contradicts repo | add-feature (or hardening) | orchestrator step 4 marks Architecture Overview stale; state-file §4 2b: repo = what is, doc = intended; open question | design-to-construction requires superseding ADR accepted | No silent overwrite of history | architecture writes ADR "as found vs intended" |
| 4 Mid-project entry, no STATE, partial docs | add-feature | STATE repair; artifacts `draft`; requirements delta bootstrap; implementation "as found" | gates evaluated for the increment only | Work proceeds without document-first detour (H-2/H-3 fixed) | Docs grow where touched |
| 5 Production incident under uncertainty | incident | incident-response (mitigate first) → maintenance → security G only if vulnerability → operations | H7 for non-pre-authorized production changes; H12 comms; incident-closure | Stabilize, then learn; postmortem proportional (M-3) | Resume suspended workflow |
| 6 Large system, indiscriminate loading risk | new-product L or add-feature | orchestrator reads only the workflow entry; each skill loads ≤ 6 references "when…" | — | Per-step context ≈ 7–16 k tokens; L adds per-service sections, not more files | Skill-level "load when" pointers |
| 7 Security-sensitive feature (SSO login + API keys) | add-feature | requirements delta (+ security B), agile-delivery (DoR flag), security C (trigger list), api-design (auth per operation), implementation + D, testing (abuse cases), E/F before release | story-done blocks without D; release blocks without E/F | No bypass path found after M-5 | Findings → DEBT/backlog or H5 |
| 8 Legacy debt vs. ideal architecture | legacy | legacy-modernization → discovery → requirements → architecture (target + transition) → security → data-design → testing (characterization) | modernization-plan-approved requires rebuild justified against incremental options; H11 | Ideal architecture constrained by strangler path; ADRs carry costs | Roadmap with rollback per increment |
| 9 Ambiguous task ("build me a dashboard") | new-product if no code, else add-feature; if truly unscoped → discovery | discovery (problem framing) or requirements bootstrap | H1 / H14 if situation ambiguous | Agent does not start coding a guessed dashboard; asks the scoping question with options | After answer: normal path |
| 10 Conflicting artifacts (REQ says 99.9 %, ADR chose single-AZ, code has no health check) | hardening | operations baseline → architecture re-evaluates scenarios → requirements change log or ADR supersede | H3 (target vs cost) | Conflict surfaced as open question with two readings; never resolved silently | Decision recorded in change log + ADR |

## 20. Real-agent simulation results

**A — New product (small SaaS).** Path: orchestrator (new-product, S, stack open) → discovery → security A → H1 → requirements → security B → agile-delivery → domain-model skipped (reason) → architecture (ADRs proposed) → security C (embedded) → data-design → api-design skipped (reason) → testing → delivery-pipeline skeleton → gate design-to-construction (batched ADR acceptance, risk review) → stories. Context ≈ 10 k tokens for the first step. Stops: H1, H10 (hosting), gate acceptance, H7. Potential mistakes observed: without the walking-skeleton rule the agent would have modeled the whole schema before the first story (fixed); without D-25 it would have declared the architecture accepted itself (fixed). Unnecessary work: none after fixes.

**B — Significant feature on an existing mobile/backend app (no docs/engineering).** Path: orchestrator (add-feature; STATE repair; stack detected from `pubspec.yaml` + Gradle) → requirements delta (bootstrap) → agile-delivery (DoR security flag on) → architecture skipped (no driver change) → security C runs (touches auth/data) → data-design delta → api-design delta (additive) → implementation with `mobile.md` + `backend.md` (as-found architecture) → security D → story-done → delivery-pipeline via existing pipeline. Context ≈ 16 k tokens across the story (heaviest path). Potential mistakes: pre-fix the orchestrator would have scheduled `discovery` and `domain-model` (H-2, H-4) and blocked `implementation` (H-3). Unnecessary work after fixes: none; `testing` not invoked (routine TEST rows by implementation).

**C — Production incident.** Path: orchestrator (incident; suspended workflow recorded) → incident-response: declare, roles, mitigate (rollback pre-authorized by Runbook or H7), comms cadence, diagnose, resolve → postmortem (trigger applies: user-visible) → maintenance (regression test) → security G skipped (not a vulnerability) → operations (alert + runbook) → incident-closure → resume. Context ≈ 7.4 k tokens. Potential mistake: pre-fix `operations` required a Deployment Plan the system lacked (H-4) — now "as found". Breach variant: evidence preservation now precedes containment (M-7).

## 21. Claude Code / Agent-Skills compatibility results
- `claude --version` → 2.1.258. `claude plugin validate . --strict` → **Validation passed**.
- `skills-ref` not installed; not run (not fabricated). Frontmatter conforms to the six spec fields by construction and by `scripts/validate.py`.
- Skill names match directories; flat layout; relative links resolve (validator); shared folders required when copying (documented in README).
- `skills/registry.yaml` sits beside skill directories; Claude Code scans `skills/*/SKILL.md`, so the file is inert to discovery.
- Not performed: launching an interactive Claude Code session with `--plugin-dir` to observe live skill triggering (would consume model calls and cannot be captured as evidence here). Recommended as the next step.

## 22. Corrections performed (all reversible, within intent)
Orchestrator: classification tie-breaks + `small-change`; content-based freshness; recurring-skill rule; partial registry read. State-file: freshness rule, mid-project bootstrap, docs-vs-code conflict rule, log cap, updater-creates rule; STATE template column. Requirements: bootstrap mode; security §5 ownership. Implementation: as-found architecture; TEST rows; backlog input. Testing: use-when narrowed; S load check conditional. Architecture: ADRs proposed; "for each that applies". ADR template status semantics. Gates: scope rule; ADR acceptance; risk register reviews; postmortem proportionality. Workflows: add-feature security trigger list; new-product walking-skeleton note. Incident-response: breach evidence. Security: scanner fallback. Stack-adaptation: secrets rule. Human-decisions: not-a-stop additions. API-design/operations/delivery-pipeline/data-design inputs and fallbacks. Registry: inputs relaxed/aligned (19 edits). Validator: consumer/producer consistency, handoff reachability, workflow input-availability simulation. Docs: ARCHITECTURE §7.4 superseded note; security-framework-map ASVS mapping; DECISIONS D-23…D-25.

## 23. Remaining risks
1. **Adherence risk**: procedures depend on the agent following `Done when` and ticking checklists honestly; only live runs can measure this.
2. **Desk-simulated validation**: scenarios and simulations traced files, not executions on real repositories.
3. **Standards via secondary sources** for ISO texts (iso.org 403); re-verification table in `references/README.md`.
4. **Context on the heaviest path** (~16 k tokens for a mobile/backend story) is acceptable but not small; teams with many other skills installed should monitor the listing budget.
5. **Judgment-dependent stops** (H3 "significant cost") may over- or under-ask until calibrated on a real project.

## 24. Recommended next steps
1. Approve and commit Phases 1–3.
2. Run one real pilot: `claude --plugin-dir .` on a small existing repository; execute an add-feature story end to end; record deviations against `docs/validation/`.
3. After the pilot, tune H3 wording and the heaviest-path references (consider splitting `mobile.md` by concern).
4. Re-verify ISO summaries when primary access is available.

## 25. Readiness assessment
The system is coherent, its graph is closed and validated, its material decisions are gated by humans, and its failure modes have recovery paths. It has not yet been proven in a live agent session. **READY WITH MINOR ISSUES** — ready for a supervised pilot, not yet for unsupervised use across many projects.

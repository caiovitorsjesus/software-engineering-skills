# Decision Log

Append-only. Format: id, status, context, decision, alternatives rejected, consequences. Phase 2 appends new entries and may supersede (never edit) earlier ones.

---

## D-01 — Execute in phases; Phase 1 produces planning documents only
**Status:** accepted (2026-09-04)
**Context:** The master prompt mandates a Research + Architecture phase separated from Implementation + Validation.
**Decision:** Phase 1 outputs are `docs/RESEARCH.md`, `docs/ARCHITECTURE.md`, `docs/DECISIONS.md`, `docs/IMPLEMENTATION_PLAN.md`. No skills, templates, references or scripts are created in Phase 1.
**Alternatives rejected:** Creating skeleton skill directories now (would pre-empt Phase 2 review and blur the phase boundary).
**Consequences:** Phase 2 must read all four documents first; the repository remains README + LICENSE + docs until then.

## D-02 — Repository layout: `skills/`, `workflows/`, `templates/`, `references/`, `scripts/`, `docs/`
**Status:** accepted
**Context:** Repository is empty except README/LICENSE; no conventions to inherit. The Agent Skills spec and Claude Code plugin format both expect a `skills/` directory at the root.
**Decision:** Five functional top-level directories mirroring the layer model (ARCHITECTURE §4) plus `docs/` for project meta-documents.
**Alternatives rejected:** Everything under `.claude/skills/` (Claude-Code-only, hides the system from other runtimes); a single `skills/` with references and templates duplicated per skill (violates single source of truth).
**Consequences:** Skills point to shared files by relative path (`../../references/x.md`). A skill copied out alone loses those targets — accepted; documented in README.

## D-03 — Encode SE disciplines as procedures; CS foundations as decision-trigger references
**Status:** accepted
**Context:** RESEARCH §5.3: CS programs converge on math, algorithms, systems and theory; SE disciplines (requirements, architecture, testing, process) are characteristic of SE programs and SWEBOK. An LLM agent already holds CS content latently; it lacks procedure and the sense of *when* a foundation changes a decision.
**Decision:** No skills for algorithms, data structures, OS, networking or PL. Those appear as `references/cs-foundations.md` and `references/data-foundations.md` with explicit triggers, consumed by architecture, data-design, api-design and implementation.
**Alternatives rejected:** A "computer-science" skill (no actionable procedure; pure reference; would inflate the always-loaded listing).
**Consequences:** Foundations must be written as *if/then* decision guides, not tutorials.

## D-04 — Repository doubles as a Claude Code plugin
**Status:** accepted
**Context:** Claude Code auto-scans `skills/` at plugin root; only `name` is required in `.claude-plugin/plugin.json`; `claude --plugin-dir .` tests locally.
**Decision:** Add `.claude-plugin/plugin.json` with name `se` (short prefix → commands like `/se:requirements`), version, description, license MIT, keywords, repository URL. Provide "copy to `.claude/skills/`" as the alternative install path in README.
**Alternatives rejected:** Plugin name `software-engineering-skills` (long invocation prefix).
**Consequences:** Phase 2 must run `claude plugin validate . --strict` if the CLI is available, and document the fallback.

## D-05 — Frontmatter restricted to the six Agent Skills spec fields
**Status:** accepted
**Context:** claude.ai upload, Skills API and `package_skill.py` fail hard on any non-spec field. Claude-Code-only fields (`user-invocable`, `disable-model-invocation`, `paths`, `context: fork`) are convenient but non-portable.
**Decision:** Use only `name`, `description`, `license`, `compatibility`, `metadata`, and (never, for now) `allowed-tools`. Layer/stage live in `metadata` as string values.
**Alternatives rejected:** `user-invocable: false` for reference-heavy skills; `context: fork` for the orchestrator.
**Consequences:** All skills are model- and user-invocable. Discovery is done entirely through the description text, so descriptions must carry precise triggers and "not for" pointers.

## D-06 — Flat `skills/<name>/` (no category subfolders)
**Status:** accepted
**Context:** Nested category folders are verified to work in Claude Code (local plugin evidence) but unverified in other Agent-Skills runtimes.
**Decision:** Flat layout; layer and stage expressed in `metadata` and `skills/registry.yaml`.
**Alternatives rejected:** `skills/foundations/…`, `skills/disciplines/…`.
**Consequences:** Directory listing is 16 entries; the registry and README provide the grouped view.

## D-07 — Fifteen discipline skills plus one orchestrator
**Status:** accepted
**Context:** Anti-overengineering rule: every skill needs a distinct trigger, distinct outputs, and a reason not to be a section or a reference.
**Decision and merges/splits:**
- *Merged* Discovery + Feasibility + Problem Definition (+ product vision statement, stakeholder map, initial risks) → `discovery`: same moment, same consumer, one artifact.
- *Merged* Product definition + Backlog + Sprint planning/review/retro/refinement + DoR/DoD → `agile-delivery`: all Scrum-vocabulary planning work; one recurring skill.
- *Merged* Detailed design + Construction (+ frontend/mobile/backend/async platform notes as references) → `implementation`: for an agent, module design immediately precedes coding the module.
- *Kept separate* `domain-model`: feeds three downstream skills and is small; merging into architecture would force the domain conversation into an architecture document.
- *Kept separate* `api-design` and `data-design` from `architecture`: different artifacts (contract file, data model), different consumers, often revisited without touching architecture.
- *Split* `operations` and `incident-response`: distinct trigger ("production is down"), distinct time pressure, distinct outputs (live incident record, postmortem).
- *Split* `maintenance` and `legacy-modernization`: routine evolution vs. a project with reverse engineering and migration strategy; different inputs and artifacts.
- *No skill* for quality (references + gates), risk (register template owned by discovery/orchestrator), documentation (templates), project management (out of scope), AI-assisted development (reference `agent-working-rules.md`), code review / TDD / bug diagnosis (existing skills; handoff).
**Alternatives rejected:** One skill per lifecycle box (18+ skills, heavy listing); three mega-skills (plan/build/run — loses discoverability and violates the ≤ 500-line rule).
**Consequences:** 16 descriptions in the listing; each ≤ 450 chars.

## D-08 — Security is one skill with multiple entry points, plus gate requirements
**Status:** accepted
**Context:** SSDF spreads security across PO/PS/PW/RV; SAMM across Design/Implementation/Verification/Operations. SWEBOK v4 made Software Security a KA.
**Decision:** `security` skill exposes entry points (risk profile, security requirements, threat model, secure-coding review, security testing, release checklist, vulnerability handling). The orchestrator's gates require the relevant security output at each transition. `references/security-framework-map.md` maps SSDF/SAMM/ASVS/Top 10 to skill entry points.
**Alternatives rejected:** Separate `threat-modeling`, `secure-coding`, `security-testing` skills (three descriptions for one discipline); security as a section in every skill (duplication, drift).
**Consequences:** `security/SKILL.md` must stay within limits by delegating detail to two references.

## D-09 — ISO/IEC 25010:2023 is the single quality vocabulary
**Status:** accepted
**Context:** The prompt names 25010; the 2023 edition renamed usability → interaction capability, portability → flexibility, and added safety.
**Decision:** NFR categories, quality attribute scenarios, test coverage mapping and SLIs all use the nine 2023 characteristics and their sub-characteristics as recorded in RESEARCH §2.3 (testability under maintainability).
**Alternatives rejected:** FURPS+, 2011 edition names.
**Consequences:** Users of the older names get a mapping row in `references/quality-model.md`.

## D-10 — Scrum vocabulary without Scrum conformance claims
**Status:** accepted
**Context:** Scrum Guide 2020: partial adoption "is not Scrum". An AI agent cannot hold a Daily Scrum or be a Scrum Master.
**Decision:** Skill named `agile-delivery`; uses Product Backlog/Product Goal, Sprint Backlog/Sprint Goal, Increment/Definition of Done, and the *purposes* of Sprint Planning, Review and Retrospective as checkpoints. `references/scrum-vocabulary.md` states precisely what is borrowed and what is not claimed. Scrum never substitutes for architecture, testing, security or documentation.
**Alternatives rejected:** Naming the skill `scrum`; omitting agile entirely.
**Consequences:** Teams that do run Scrum can map the artifacts one-to-one.

## D-11 — Adopt ISO/IEC/IEEE 29119 concepts, not its documentation set
**Status:** accepted
**Context:** 29119 is a standard but contested by the context-driven testing community for documentation weight.
**Decision:** Use its test-level/process vocabulary and the technique families (specification-, structure-, experience-based) in a single Test Strategy artifact with per-feature test plan sections and exit criteria. No separate test policy, test design spec, test case spec, test procedure or completion report documents.
**Alternatives rejected:** Full 29119 Part 3 document set.
**Consequences:** L-class projects that need formal completion reports add them as sections, not new templates.

## D-12 — Default to the simplest architecture that meets quality scenarios; distribution requires recorded drivers
**Status:** accepted
**Context:** The prompt forbids promoting fashionable patterns. Microservices add operational and consistency cost.
**Decision:** `architecture` starts from a modular monolith (or single deployable) and moves to distributed styles only when explicit drivers (independent scaling, independent deployment by separate teams, isolation/fault domains, polyglot persistence needs, regulatory separation) are documented in an ADR with the accepted costs. Event-driven and CQRS likewise require a driver.
**Alternatives rejected:** Style-neutral guidance with no default (agents then default to what is fashionable).
**Consequences:** `references/architecture-styles.md` must present drivers and costs, not a style catalogue.

## D-13 — Respect the given stack; recommend replacement only with an ADR
**Status:** accepted
**Context:** Prompt §11.
**Decision:** `references/stack-adaptation.md` gives a detection procedure (manifests, lockfiles, CI, containers, IaC) and a compact convention table; every skill adapts guidance to the detected stack; replacement recommendations require an explicit requirement or constraint and an ADR.
**Alternatives rejected:** Per-stack playbooks (`flutter.md`, `spring-boot.md`, …) — sprawl and staleness.
**Consequences:** Platform-specific engineering concerns (offline sync, permissions, state management) are covered generically in `implementation/references/{frontend,mobile,backend,async-messaging}.md`, not per framework.

## D-14 — Traceability as a table in the Requirements Spec; matrix file only for L
**Status:** accepted
**Context:** A separate matrix is a maintenance burden for small projects and duplicates the spec.
**Decision:** `requirements-spec.md` contains the traceability table (REQ → ADR/component → TEST → status). L-class projects may extract it to `docs/engineering/traceability.md` using the same columns. No separate template.
**Alternatives rejected:** Dedicated `traceability-matrix.md` template for all sizes.
**Consequences:** `implementation` and `testing` update the table in place.

## D-15 — Artifacts live in the target repository under `docs/engineering/`
**Status:** accepted
**Context:** Agents need a predictable place to find prior artifacts across sessions; the orchestrator's stage detection depends on it.
**Decision:** Default path `docs/engineering/` with `STATE.md` as the index; overridable via a field in `STATE.md`. ADRs under `docs/engineering/adr/`, incidents under `docs/engineering/incidents/`, API contracts under `docs/engineering/api/` (or the stack's conventional location if one exists, recorded in STATE).
**Alternatives rejected:** Root-level `ARCHITECTURE.md`-style scattered files; `.se/` hidden directory (hides engineering docs from humans).
**Consequences:** Every skill's Outputs table uses these paths.

## D-16 — Validation is a stdlib Python script plus a YAML registry plus scenario walkthroughs
**Status:** accepted
**Context:** The system must be checkable without network or heavy dependencies; the orchestrator needs a machine-readable skill graph.
**Decision:** `skills/registry.yaml` (hand-maintained) is read by `scripts/validate.py` (Python 3, no third-party packages; minimal YAML subset parser or `json`-compatible YAML) to check frontmatter, names, sizes, links, section order, registry ↔ filesystem consistency. Scenario walkthroughs A–E are documented in `docs/validation/`.
**Alternatives rejected:** Node-based validator; relying solely on `skills-ref validate` (does not check registry/links/sections).
**Consequences:** Registry schema fixed in IMPLEMENTATION_PLAN §6; validator must run on Windows and POSIX.

## D-17 — Evidence labels in references; no `UNVERIFIED` content stated as fact
**Status:** accepted
**Context:** Anti-hallucination policy; several primary pages were inaccessible (ISO 403).
**Decision:** Reference files carry a header block: standard/edition, retrieval date, source URL(s), evidence label. Claims marked `UNVERIFIED` in RESEARCH are either re-verified in Phase 2 or written as `RECOMMENDATION`/omitted. The validator greps `references/` for the literal `UNVERIFIED` and fails on it.
**Consequences:** Phase 2 has a short re-verification list (IMPLEMENTATION_PLAN §8.3).

## D-18 — Supplied practical sources are used as process sanity checks only
**Status:** accepted
**Context:** Artia and UpSites are commercial blog articles; the YouTube resource had no URL and was not accessed.
**Decision:** Their converged process shape informs the workflow ordering and two emphases (feasibility gate; handover/training at launch). They are cited as secondary/industry context, never as authority over standards. No content is attributed to the video.
**Consequences:** If the user later supplies the video, treat it the same way.

## D-19 — Registry stays YAML with a stdlib subset parser
**Status:** accepted (Phase 2, 2026-09-04)
**Context:** IMPLEMENTATION_PLAN §7 allowed a fallback to JSON if a stdlib YAML subset parser proved brittle.
**Decision:** Keep `skills/registry.yaml`. `scripts/validate.py` implements a parser for the documented subset (block mappings, block sequences, flow sequences of scalars, quoted strings, folded `>-` scalars, comments). The registry header states the subset; anchors, multi-line flow collections and complex keys are unsupported by design.
**Consequences:** Human-friendly registry; parser verified on the full registry and on skill frontmatter.

## D-20 — Size-class calibration: an early SaaS MVP is S
**Status:** accepted (Phase 2, scenario A)
**Context:** The first rightsizing table put any product with "external users" or "PII" into M, which made the plan's own "small SaaS (S)" scenario impossible and would have imposed M depth on every MVP.
**Decision:** S = up to a few hundred users (internal or early external), account-identity personal data plus user-generated content, no regulated categories, single deployable, 1–2 developers. M starts at thousands of users / multi-tenant isolation / personal data beyond identity at volume / provider-mediated payments with contractual obligations. L = regulated data processed directly, many teams/services, high traffic. Classes only ever rise during a project; security runs at every gate in every class.
**Consequences:** `rightsizing.md §1` and `lifecycle-map.md §5` updated; ASVS L1 for S, L2 for M, L2–L3 for L unchanged.

## D-21 — YouTube source used for title only
**Status:** accepted (Phase 2)
**Context:** The supplied video page exposed only its title and channel; no transcript.
**Decision:** Record title and channel in RESEARCH §6.3; incorporate no content; keep the limitation visible.
**Consequences:** No skill or reference cites the video.

## D-22 — STATE gains `Suspended workflow` and artifact status `embedded`
**Status:** accepted (Phase 2, scenarios A and D)
**Context:** Incidents interrupt another workflow and must resume it; S-class right-sizing keeps some artifacts as sections of others, which the orchestrator's freshness check could not represent.
**Decision:** Add the `Suspended workflow / resume point` field and the `embedded in <artifact>` status to `templates/project-state.md` and `state-file.md`.
**Consequences:** Orchestrator step 4 treats embedded artifacts as present with the host's freshness.

## D-23 — Recurring skills are never skipped by output freshness; freshness is content-based
**Status:** accepted (Phase 3 audit, 2026-09-05)
**Context:** The Phase 2 skip rule ("all outputs current → skip") would skip `implementation` forever (its registry outputs are empty, so the condition is vacuously true) and would suppress `security`, `testing`, `agile-delivery` once their first artifact existed. The timestamp-based freshness rule would mark every design artifact stale after each traceability edit, causing re-runs of design skills per story.
**Decision:** The registry's `recurring` flag governs skipping: recurring skills run when their workflow entry condition holds and are never skipped for freshness. Freshness reads a `Last substantive change` date (change-log entries, new/superseded ADRs, schema/contract changes, new High/Critical threats, new containers); traceability, status, ordering and log edits are excluded.
**Consequences:** STATE artifact index gains a column; `state-file.md §3` and orchestrator steps 4–5 rewritten.

## D-24 — Existing systems default to `add-feature`; `small-change` routes straight to `maintenance`; no `discovery` for undocumented repos
**Status:** accepted (Phase 3 audit)
**Context:** `requirements` required a Discovery Brief, so any feature on an existing repository without engineering docs would have scheduled `discovery`; thin documentation could route ordinary features to `legacy-modernization`; trivial fixes would have paid the full orchestration cost; `implementation` refused to start without an Architecture Overview.
**Decision:** Classification tie-breaks: existing system → `add-feature` unless the intent is modernization or the change is risky and untested; `small-change` situation hands directly to `maintenance`. `requirements` delta mode bootstraps product context from README/code with `ASM-`; `implementation`, and design skills in delta mode, use an "as found" baseline derived from the code instead of blocking. Registry inputs relaxed accordingly (`discovery-brief?`, and see D-25 follow-ups in the audit).
**Consequences:** Mid-project entry works without a document-first detour; documentation is produced incrementally where a change touches it.

## D-25 — ADRs are `proposed` by the agent and accepted by a human at the gate, in one batch
**Status:** accepted (Phase 3 audit)
**Context:** Architecture, store, hosting and authn decisions are material; the Phase 2 skills let the agent write ADRs directly as accepted, which silently made those decisions.
**Decision:** New ADRs default to `proposed`; the `design-to-construction` gate requires the technical approver to accept the set in one batched decision (recommendation by the agent, authorization by the human). Individual ADR acceptance is not a separate stop; the "Not a stop" list says so.
**Consequences:** Gate item added; `templates/adr.md` and `architecture` step 9 updated. For solo developers the approver is the user, and the acceptance is still recorded.

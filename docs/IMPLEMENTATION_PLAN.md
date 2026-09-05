# Implementation Plan — Phase 2

> **Status (2026-09-04):** executed. All 11 steps complete; results in `docs/validation/audit.md` and `docs/validation/scenario-*.md`; decisions D-19…D-22 appended. This document is kept as the plan of record; deviations are noted in DECISIONS.md.

Consumer: the Phase 2 agent. Read order: `ARCHITECTURE.md` → this file → `DECISIONS.md` → `RESEARCH.md` (as the citation source while writing references). Treat Phase 1 as the baseline; if implementation exposes a contradiction, record it as a new D-xx and, if it changes scope or architecture, stop and ask.

Constraints carried from the master prompt: no commit, no push; targeted edits; validate against scenarios A–E; final system-wide audit; final report with commit message(s).

## 1. Implementation order

Each step has acceptance criteria. Do not start a step whose dependencies are unmet.

| # | Step | Creates | Depends on | Done when |
|---|---|---|---|---|
| 1 | Scaffold | directories from ARCHITECTURE §5; `.claude-plugin/plugin.json`; `references/README.md`, `templates/README.md`, `workflows/README.md` stubs | — | tree matches §5; plugin.json valid JSON with `name: se` |
| 2 | Skill contract doc | `docs/SKILL_AUTHORING.md` (frontmatter, body sections, size limits, description rules, evidence rules, how to add a skill) | 1 | matches ARCHITECTURE §6 exactly |
| 3 | Registry + validator | `skills/registry.yaml` (all 16 entries, from §6 schema), `scripts/validate.py` | 2 | validator runs on empty skill dirs and reports missing SKILL.md per registry entry |
| 4 | References | 13 files in `references/` (§5) | RESEARCH | every file has the header block; zero `UNVERIFIED` strings; each ≤ 250 lines |
| 5 | Templates | 16 files in `templates/` (§4) | 4 | each template has purpose line, consumer line, sections, ID conventions |
| 6 | Orchestrator | `skills/sdlc-orchestrator/SKILL.md` + `references/{gates,human-decisions,rightsizing,state-file}.md` | 3, 4, 5 | validator passes for the skill; procedure implements ARCHITECTURE §7.5 |
| 7 | Discipline skills, lifecycle order | discovery, requirements, agile-delivery, domain-model, architecture, data-design, api-design, implementation (+4 refs), testing, security (+2 refs), delivery-pipeline, operations, incident-response, maintenance, legacy-modernization | 6 | validator passes; every Outputs row names an existing template; every Handoff names an existing skill |
| 8 | Workflows | 5 files in `workflows/` | 7 | every step names an existing skill and gate |
| 9 | Scenario validation | `docs/validation/scenario-{a,b,c,d,e}.md` | 8 | each records sequence, artifacts, gates, stops, gaps, fixes; fixes applied to skills |
| 10 | Final audit | `docs/validation/audit.md`; fixes | 9 | audit checklist (§10) fully answered; validator green |
| 11 | README + report | `README.md` rewrite; final response with commit messages | 10 | README covers install (plugin + copy), quick start, skill map, principles, limitations |

## 2. Per-skill specifications

Common to all: frontmatter and body per ARCHITECTURE §6; right-sizing notes `S:/M:/L:`; Stop-and-ask lists drawn from ARCHITECTURE §7.6 plus skill-specific items; Handoff updates `STATE.md`. Description drafts below are starting points (≤ 450 chars; trigger first; "Not for" last).

### 2.1 sdlc-orchestrator
- **Description draft:** "Decide where a software project is in its lifecycle, what is missing, which engineering skills to run next and when a human must decide. Use at the start of any project work, when the user asks 'what next', when a request spans several stages, or when docs/engineering/STATE.md exists. Not for doing a single discipline's work directly (use that skill)."
- **Procedure:** 1 classify situation (§7.3 table) → 2 read/create `STATE.md`; detect stack (`references/stack-adaptation.md`) → 3 assign size class (`references/rightsizing.md`) → 4 load the workflow; compute artifact existence/freshness → 5 build the minimal skill sequence (skip fresh, schedule producers of missing inputs) → 6 for each skill: run, then gate (`references/gates.md`); on gate failure fix or stop → 7 update STATE (stage, next action, open questions) → 8 report: sequence run, artifacts, decisions pending.
- **Outputs:** `docs/engineering/STATE.md`.
- **Validation:** every skipped skill has a logged reason; every stop has a question with options + recommendation; STATE next-action is a single concrete step.
- **References (own):** `gates.md` (one checklist per transition), `human-decisions.md` (§7.6 with question phrasing), `rightsizing.md` (§7.4 table + per-artifact depth), `state-file.md` (field semantics; freshness rule: an artifact is stale when any of its declared inputs changed after it).

### 2.2 discovery
- **Trigger words:** idea, new project, "should we build", feasibility, problem statement, stakeholders, scope.
- **Procedure:** problem statement (who, pain, evidence) → stakeholders and their concerns (42010 vocabulary) → objectives with measurable success criteria → scope in/out → constraints (technical, legal, budget, time, stack) and assumptions → options considered (build/buy/extend/do nothing) → feasibility check (technical, operational, economic, schedule; regulatory data classes → raises size class) → initial risks (`RISK-###`, likelihood/impact) → product vision one-liner → verdict: go / no-go / pivot. Each step "done when" the brief section is filled with evidence or an explicit `ASM-###`.
- **Outputs:** `docs/engineering/discovery-brief.md`, `docs/engineering/risk-register.md`.
- **Stop-and-ask:** go/no-go; scope conflicts between stakeholders; unknown budget/time when they drive feasibility.
- **Handoff:** requirements; security (risk profile from data classes and exposure).
- **Refs:** `templates/discovery-brief.md`, `templates/risk-register.md`, `references/lifecycle-map.md`.

### 2.3 requirements
- **Procedure:** import brief → elicitation checklist (users, workflows, data, integrations, environments, volumes, compliance) → FR as `REQ-F-###` with acceptance criteria (Given/When/Then or rule-based) → NFR per 25010 characteristic as `REQ-N-###` with measurable target and measurement method → constraints/assumptions/dependencies → prioritization (MoSCoW or WSJF; record method) → quality check per 29148 verified criteria and smells (`references/requirements-quality.md`) → security requirements (SSDF PO.1; ASVS level chosen by size class) → traceability table seed → change log rules.
- **Outputs:** `docs/engineering/requirements.md`.
- **Validation:** every FR has ≥ 1 AC; every NFR has a number and a method; no smells; IDs unique; open questions have owners.
- **Stop-and-ask:** conflicting requirements; NFR targets that imply cost (e.g., 99.99 % availability) without stakeholder confirmation.
- **Handoff:** agile-delivery, domain-model, architecture, testing, security.

### 2.4 agile-delivery
- **Procedure:** Product Goal from vision → epics from FR groups → stories with AC (reuse REQ ACs; link REQ ids) → Definition of Ready (story linked to REQ, AC testable, dependencies known, size estimated) → Definition of Done (code reviewed, tests at agreed levels passing, security checklist items for the story, docs/traceability updated, deployed to agreed environment) → prioritization and iteration plan with Sprint Goal → review checkpoint (what increment meets AC; feedback → backlog) → retrospective checkpoint (process changes → STATE) → refinement rules.
- **Outputs:** `docs/engineering/backlog.md`.
- **Refs:** `references/scrum-vocabulary.md`, `templates/backlog.md`.
- **Note:** states explicitly it borrows Scrum vocabulary (D-10).

### 2.5 domain-model
- **Procedure:** extract nouns/verbs from requirements → glossary (one term, one meaning) → entities, value objects, relationships, cardinalities → invariants and business rules (source REQ) → lifecycle/state machines for key entities → M/L: bounded contexts and context map; aggregates only where transactional consistency requires → check against every FR (each FR touches named concepts).
- **Outputs:** `docs/engineering/domain-model.md`.
- **Handoff:** architecture, data-design, api-design, implementation. If the user has the `domain-modeling` skill (mattpocock), note it as an alternative for ubiquitous-language deepening.

### 2.6 architecture
- **Procedure:** drivers = top NFRs as quality attribute scenarios (stimulus, environment, response, measure) + constraints → candidate styles (`references/architecture-styles.md`), start from simplest (D-12) → choose; record ADR-0001 style with drivers and costs → C4 System Context and Container (Component for M/L hot spots) in Mermaid or text → integration and communication (sync/async; contracts; idempotency; failure modes from `cs-foundations.md`) → cross-cutting (authn/z, config, logging, errors, observability hooks) → deployment view (environments, runtime topology) → risks and trade-offs → ADRs for every significant decision (data store, messaging, hosting, auth provider, frontend approach).
- **Outputs:** `docs/engineering/architecture.md`, `docs/engineering/adr/NNNN-*.md`.
- **Validation:** every driver is addressed by a decision or explicitly deferred; every ADR has status/context/decision/consequences; no distributed style without a driver ADR.
- **Stop-and-ask:** stack replacement; hosting/cost commitments; multi-region/compliance topology.
- **Handoff:** data-design, api-design, security (threat model), delivery-pipeline, implementation.

### 2.7 data-design
- **Procedure:** from domain model: logical model → storage choice per data set (relational/document/KV/search/time-series/blob) with drivers from `data-foundations.md` → physical schema (keys, types, constraints, indexes justified by access paths) → transactions and consistency model (isolation level; concurrency control; idempotency keys; outbox for cross-store writes) → migration strategy (versioned, forward-only, expand/contract for zero-downtime) → data lifecycle (retention, archival, deletion, PII handling → security) → caching (what, TTL, invalidation) → volume/growth estimates.
- **Outputs:** `docs/engineering/data-model.md`; migration files in the stack's convention.
- **Stop-and-ask:** irreversible migrations; PII retention decisions.

### 2.8 api-design
- **Procedure:** style choice (REST/GraphQL/gRPC/events) driven by consumers and architecture → resource/operation model from domain → contract file (OpenAPI 3.x / GraphQL SDL / AsyncAPI) → conventions: naming, versioning, pagination, filtering, errors (problem-details style), idempotency, rate limits → authn/z per operation (ASVS V4/V6/V8 pointers) → backward-compatibility rules → examples → contract tests hook for testing.
- **Outputs:** contract file under `docs/engineering/api/` or stack convention; API notes section in architecture.
- **Validation:** every FR needing an interface maps to an operation; every operation has auth, errors, examples.

### 2.9 implementation
- **Procedure:** pick backlog item → confirm inputs (REQ, AC, design, contract) → module design (responsibilities, interface, dependencies, error handling, state) → detect stack conventions (`stack-adaptation.md`) → implement in small verifiable increments; write tests alongside (hand off to user's `tdd` skill if present) → secure-coding checklist (`security/references/secure-coding-checklist.md`) → self-review against AC and design → update traceability (REQ → code → tests) → prepare change for review (existing `code-review` skills).
- **References (own):** `frontend.md` (state management, rendering/perf, accessibility, error/loading states, forms/validation), `mobile.md` (offline-first and sync, permissions, background work, platform constraints, secure storage, app lifecycle, release channels), `backend.md` (layering, validation at boundaries, transactions, idempotency, resilience patterns: timeouts, retries with backoff, circuit breaker, bulkhead), `async-messaging.md` (delivery semantics, ordering, idempotent consumers, outbox/inbox, dead letters, schema evolution).
- **Outputs:** code; traceability update.
- **Stop-and-ask:** design deviation needed; new dependency with license/security concerns.

### 2.10 testing
- **Procedure:** test strategy from NFR/25010 coverage → levels and their purpose (unit, component, integration, contract, e2e, performance, security, exploratory, acceptance) sized by class → what is automated where (local, CI stage) → test data and environments → flakiness and quarantine policy → exit criteria per level → per-feature test plan section pattern → regression suite rules → mapping to DoD.
- **Outputs:** `docs/engineering/test-strategy.md`; test code in stack convention.
- **Refs:** `references/testing-foundations.md`, `references/quality-model.md`.

### 2.11 security
- **Entry points (each a sub-procedure):** A risk profile (SAMM TA-A: data classes, exposure, likelihood/impact) → B security requirements (SSDF PO.1; ASVS level pick) → C threat model (four questions; assets, trust boundaries from C4, threats via STRIDE-style prompts or checklist, mitigations, `THR-###`, residual risk) → D secure-coding review (checklist; dependency and secrets scan; OWASP Top 10:2025 prompts) → E security testing (SAST/DAST/dep scan in pipeline; abuse cases as tests) → F release checklist (secure defaults PW.9, integrity PS.2, secrets, logging A09) → G vulnerability handling (RV.1–RV.3: intake, triage, remediate, root cause).
- **Outputs:** `docs/engineering/threat-model.md`; security sections in requirements/pipeline; findings as backlog/debt items.
- **References (own):** `threat-modeling.md` (procedure, prompts, table format), `secure-coding-checklist.md` (by ASVS chapter, language-neutral).
- **Stop-and-ask:** accepting/deferring High or Critical risk; regulatory interpretation.

### 2.12 delivery-pipeline
- **Procedure:** environments and promotion path → VCS conventions (branching, reviews, protected branches; Conventional Commits if adopted) → CI stages (build, lint, tests by level, security scans, artifact build, SBOM/provenance where L) → artifact integrity and versioning → configuration and secrets (12-factor config; secret manager; no secrets in VCS) → deployment strategy (recreate, rolling, blue/green, canary; feature flags) → rollback and data-migration compatibility → release checklist and handover (docs, training notes) → DORA metrics capture.
- **Outputs:** `docs/engineering/deployment-plan.md`; pipeline config files.
- **Stop-and-ask:** production deploy execution; cloud cost/vendor commitments.

### 2.13 operations
- **Procedure:** SLIs from NFRs (latency percentiles, availability, error rate, durability) → SLOs and error budgets → observability: logs (structured, correlation ids), metrics, traces; dashboards → alerting on symptoms, paging policy → runbook entries (routine ops, known failure modes, escalation) → backup/restore and DR (RPO/RTO) → capacity and cost review → on-call readiness checklist.
- **Outputs:** `docs/engineering/runbook.md`.
- **Refs:** `references/operations-foundations.md`, `references/engineering-metrics.md`.

### 2.14 incident-response
- **Procedure:** declare (criteria) → roles (commander, operations, communications, planning — one agent may hold several; say so) → live incident record (`INC-`) → stabilize first: mitigations (rollback, feature flag, scale, failover) before root cause → communicate at fixed cadence → diagnose (hand off to `diagnosing-bugs` if present) → resolve → postmortem within agreed time (blameless; timeline, impact, root cause, trigger, detection, resolution, action items with owners) → corrective actions to backlog/debt; runbook and alerts updated.
- **Outputs:** `docs/engineering/incidents/YYYY-MM-DD-slug.md`.
- **Stop-and-ask:** production changes (rollback, config) unless pre-authorized in runbook; external communication.

### 2.15 maintenance
- **Procedure:** intake (bug, debt, upgrade, patch, deprecation) → classify and prioritize (impact × effort; security patches first) → bug fix workflow (reproduce → test → fix → regression) → refactoring rules (behaviour-preserving, test-backed, small) → dependency upgrade routine (changelog review, semver, lockfile, tests) → deprecation and compatibility policy → tech debt register maintenance (`DEBT-###`, interest cost) → periodic health review (metrics from operations).
- **Outputs:** `docs/engineering/tech-debt.md`; backlog items.

### 2.16 legacy-modernization
- **Procedure:** inventory (repos, services, data stores, integrations, infra) → reverse engineering (build/run it; map modules, dependencies, data flows; recover as-is C4) → quality assessment (tests, coverage hotspots, complexity, duplication, outdated deps, security exposure) → business criticality and knowledge risks → debt register → modernization options (rehost, replatform, refactor, rearchitect, rebuild, retire) with drivers and costs → target architecture (via `architecture`) and incremental migration strategy (characterization tests first; incremental extraction; parallel run; cut-over/rollback) → roadmap.
- **Outputs:** `docs/engineering/legacy-assessment.md`; ADRs.
- **Stop-and-ask:** rebuild vs. refactor; decommission dates; data migration with loss risk.

## 3. Workflows (files in `workflows/`)

Each: Purpose · Entry conditions · Sequence table (step, skill, entry point, outputs, gate) · Size-class variations · Exit criteria · Typical human stops · Related scenario. Sequences per ARCHITECTURE §10. `workflows/README.md` maps situations → workflow.

## 4. Templates (files in `templates/`)

Every template starts with an HTML comment: purpose, producer skill, consumers, when to update, size guidance. Sections:

- `project-state.md`: situation, size class, stage, stack, artifact index table, decision index, open questions, risks pointer, next action, config (docs path).
- `discovery-brief.md`: problem statement; stakeholders & concerns; objectives & success criteria; scope in/out; constraints; assumptions; options; feasibility (technical/operational/economic/schedule) & verdict; initial risks (link); product vision.
- `requirements-spec.md`: product context; users; FR table (id, statement, AC, priority, source); NFR table by 25010 (id, characteristic, target, method); constraints; assumptions; dependencies; security requirements (ASVS level); open questions; traceability table; change log.
- `backlog.md`: product goal; epics; stories (id, REQ links, AC, estimate, priority, status); DoR; DoD; current iteration (goal, items); review notes; retro actions.
- `domain-model.md`: glossary; entities/value objects; relationships; invariants (with REQ links); state machines; bounded contexts (M/L).
- `architecture-overview.md`: drivers (quality scenarios); constraints; style & rationale (ADR link); C4 context; C4 container; components (M/L); integration & communication; cross-cutting; deployment view; risks/trade-offs; decision index.
- `adr.md`: Nygard/MADR-lite: id, title, status, date, context, decision, drivers, options considered, consequences, links.
- `data-model.md`: logical model; storage choices; physical schema; indexes & access paths; transactions & consistency; migrations; lifecycle/retention; caching; volumes.
- `threat-model.md`: scope & assets; trust boundaries/diagram ref; threats table (`THR-###`, component, category, description, likelihood, impact, mitigation, status, REQ/ADR link); assumptions; residual risk; review date.
- `risk-register.md`: `RISK-###`, description, category, likelihood, impact, response, owner, status, trigger.
- `test-strategy.md`: objectives & 25010 coverage; levels table (purpose, scope, tools, where run, exit criteria); environments; test data; automation & CI mapping; flakiness policy; per-feature test plan pattern; regression policy.
- `deployment-plan.md`: environments; branching & CI stages; artifact versioning & integrity; configuration & secrets; deployment strategy; rollback; migration compatibility; release checklist; handover/training; metrics capture.
- `runbook.md`: service overview; SLIs/SLOs/error budget; dashboards & alerts; routine operations; failure modes & responses; escalation; backup/restore & DR; capacity; on-call checklist.
- `incident-postmortem.md`: summary; impact; timeline; detection; root cause & trigger; resolution; what went well/poorly; action items (owner, due, link); lessons.
- `tech-debt-register.md`: `DEBT-###`, location, description, cause, impact, interest (cost of delay), effort, priority, plan, status.
- `legacy-assessment.md`: inventory; as-is architecture; quality findings; risks; debt summary; options matrix; target & migration strategy; roadmap.

## 5. References (files in `references/`)

Header block for each: title; standards/editions covered; retrieval date 2026-09-04; source URLs (from RESEARCH §11); evidence labels used. Content ≤ 250 lines; decision-oriented; tables preferred.

| File | Content | Source sections |
|---|---|---|
| `README.md` | index: file → load when… ; standards version table for re-verification | — |
| `lifecycle-map.md` | stage glossary; ID prefixes; mapping table | RESEARCH §9.1, §2.1, §2.2 |
| `quality-model.md` | 25010:2023 table; 2011→2023 rename map; per-stage usage; NFR statement pattern | §2.3 |
| `requirements-quality.md` | 29148 verified criteria and smells; AC patterns; prioritization methods; change control | §2.4 |
| `architecture-styles.md` | drivers → styles table with costs; distribution drivers (D-12); quality-scenario format; C4 levels; 42010 concepts; ADR format/statuses | §2.5, §7 |
| `cs-foundations.md` | decision triggers: complexity & data-structure choice; concurrency models & races; distributed failure modes, consistency/availability trade-offs, idempotency, time/clocks; networking (latency, timeouts, retries); OS (processes/threads/IO/memory); PL paradigms & type systems affecting design; math/logic (invariants, state machines) | §5.3 (INFERENCE-labelled where applicable) |
| `data-foundations.md` | relational vs NoSQL drivers; normalization vs denormalization; indexing by access path; isolation levels & anomalies; migrations (expand/contract); caching patterns; retention | §5.3 |
| `security-framework-map.md` | SSDF v1.1 19 practices → skill entry point; SAMM v2 functions/practices; ASVS 5.0 chapters & levels; Top 10:2025; Threat Modeling Manifesto | §3 |
| `testing-foundations.md` | levels & purposes; 29119 technique families; pyramid/trophy guidance by stack; contract tests; test data & environments; flakiness; exit criteria | §2.6 |
| `operations-foundations.md` | SLI/SLO/SLA & error budgets; observability signals; DORA five metrics; 12-factor; SRE incident roles; postmortem triggers/contents | §7 |
| `scrum-vocabulary.md` | Scrum Guide 2020 elements; what agile-delivery borrows; explicit non-claims | §4 |
| `engineering-metrics.md` | DORA; quality/maintainability metrics; per-stage measures; anti-patterns (vanity metrics) | §7 |
| `stack-adaptation.md` | detection procedure (manifests → stack); convention table (package manager, test runner, lint/format, build, layout, migration tool) for common ecosystems; replacement rule (ADR) | D-13 |
| `agent-working-rules.md` | verification-first; small diffs; no invented APIs/versions; cite sources; respect conventions; log assumptions; when to hand off to code-review/tdd/diagnosing-bugs | §8.3 |

## 6. Registry schema (`skills/registry.yaml`)

```yaml
version: "0.1.0"
skills:
  - name: requirements
    layer: discipline            # orchestration | discipline
    stage: requirements          # key from references/lifecycle-map.md
    recurring: false             # true for agile-delivery, testing, security, maintenance
    inputs:
      - artifact: discovery-brief
        required: true
    outputs:
      - artifact: requirements-spec
        template: templates/requirements-spec.md
        path: docs/engineering/requirements.md
    handoffs: [agile-delivery, domain-model, architecture, testing, security]
    gates_after: [requirements-to-design]
    references: [references/requirements-quality.md, references/quality-model.md]
artifacts:
  - id: requirements-spec
    template: templates/requirements-spec.md
    default_path: docs/engineering/requirements.md
    producers: [requirements]
    consumers: [agile-delivery, domain-model, architecture, testing, security, implementation]
gates:
  - id: requirements-to-design
    file: skills/sdlc-orchestrator/references/gates.md
workflows:
  - id: new-product
    file: workflows/new-product.md
    sequence: [discovery, requirements, security, agile-delivery, domain-model, architecture, security, data-design, api-design, testing, delivery-pipeline, implementation, testing, security, delivery-pipeline, operations, maintenance]
```

Validator checks: every `skills[].name` has `skills/<name>/SKILL.md` and vice versa; every `outputs[].template` exists; every `handoffs[]` and `workflows[].sequence[]` is a known skill; every `artifacts[].producers/consumers` are known skills; every `gates_after[]` is a known gate; every `references[]` path exists.

## 7. `scripts/validate.py` behaviour

- Python 3.8+, stdlib only. YAML: implement a minimal parser for the registry subset (mappings, lists, scalars, quoted strings) or store the registry as YAML that is also valid JSON-like — decide in Phase 2; if a minimal parser is too brittle, switch the registry to `registry.json` and record D-19.
- Checks (exit 1 on any error; warnings do not fail): frontmatter delimiters; only spec fields; `name` regex `^[a-z0-9]+(-[a-z0-9]+)*$`, ≤ 64, equals directory; description 1–1024 (warn > 450); `SKILL.md` ≤ 500 lines (warn > 300); required section headings present in order; relative links resolve; registry consistency (§6); templates start with the purpose comment; references contain the header block and no `UNVERIFIED`; workflow steps name known skills.
- Report: per-file errors/warnings; totals; description character total; largest files.
- Runs on Windows (PowerShell/Git Bash) and POSIX; no shell-specific code.

## 8. Validation plan

### 8.1 Scenario walkthroughs (`docs/validation/scenario-X.md`)
For each scenario: the user request (verbatim invented prompt); orchestrator classification and size class; stack detected/assumed; skill sequence selected with skip reasons; for each skill, an outline of the artifact it would produce (headings + 2–3 representative rows, e.g., two REQ-F, one REQ-N, one ADR title, three THR rows); gates evaluated; human stops raised; gaps or contradictions found; fixes applied (file, change). Scenarios: A small SaaS from vague idea (S; web); B mobile app with auth, API, DB, permissions, offline (M; Flutter or React Native assumed, stack-neutral guidance checked); C large API with scalability, security, observability, distributed concerns (L); D production incident (existing system; incident-response → postmortem → maintenance); E legacy system (reverse engineering → debt → modernization → incremental migration).

### 8.2 Evaluation criteria (ARCHITECTURE §12 + prompt §22)
Correctness, completeness, consistency, usability, composability, context efficiency, rigor, security, testability, maintainability, traceability, no duplication, no contradictions. Record per-scenario a short table: criterion → pass/fail → note.

### 8.3 Re-verification list for Phase 2 (from RESEARCH §10)
Before citing in references: 29148 full requirement-quality list; DORA thresholds (omit if unverifiable); Conventional Commits, SemVer, OpenAPI, AsyncAPI, OpenTelemetry, STRIDE (cite URL after a fetch or label INDUSTRY without specifics); CS2023 SE knowledge units (optional). If unverifiable, write as `RECOMMENDATION` or omit.

## 9. Anti-overengineering gate for any new file

Answer in the file's header comment or in `DECISIONS.md`: problem solved; user (which skill/agent/human); moment of use; input consumed; output produced; why no existing file solves it. No answer → no file.

## 10. Final audit checklist (`docs/validation/audit.md`)

Architecture: coherent layers; dependency direction downward only; responsibilities per skill unique. Engineering: every lifecycle stage in `lifecycle-map.md` has ≥ 1 skill; CS foundations referenced by the four design/build skills; security and quality present in every gate. Skills: purpose, inputs, outputs, validation, stop-and-ask, handoff present; every output has a template; every handoff exists. Workflows: every stage transition reachable; no dead ends; incident and legacy paths re-enter the main lifecycle. Documentation: README explains install and use; references cite sources with dates; decisions logged. AI usability: descriptions carry triggers and "not for"; body sizes within limits; listing total reported. Overengineering: list files that could be removed without capability loss and remove them.

## 11. Known risks

| Risk | Mitigation |
|---|---|
| Skill listing budget exceeded when combined with the user's other plugins | Descriptions ≤ 450 chars; validator reports total; README notes `skillOverrides` name-only option |
| Descriptions too similar → wrong skill fires | Distinct leading trigger words; "Not for" pointers; scenario walkthroughs check selection |
| Orchestrator becomes a monolith | Hard cap 300 lines; gates/rightsizing/human-decisions in its own references |
| References drift from standards | Version + retrieval date header; README table for re-verification |
| YAML parsing in stdlib-only validator | Fallback to JSON registry (record D-19) |
| Windows path/encoding issues in validator | Use `pathlib`, UTF-8 explicit, forward slashes in registry |
| Over-prescriptive stack guidance | Generic platform references; stack detection procedure; ADR rule for replacement |

## 12. Open questions (non-blocking; defaults stated)

1. Plugin name `se` vs `swe` — default `se`.
2. Should `implementation` explicitly hand off to the user's installed `tdd` / `code-review` skills by name? Default: mention them as "if available", since other users lack them.
3. Registry format YAML vs JSON — default YAML with a minimal parser; fall back per §7.
4. Language of artifacts: English by default; templates may note that the target project's language is respected (user's sources were Portuguese).
5. Whether to include Mermaid diagrams in templates — default yes for C4 context/container (text fallback provided).

## 13. Out of scope (explicit)

Project/portfolio management (time, cost, staffing); UX research and visual design method (only interaction-capability NFRs and accessibility checks); data science / ML lifecycle (SP 800-218A noted as a pointer only); hardware/embedded safety certification (25010 *safety* covered as a quality characteristic only); per-framework playbooks; legal/compliance interpretation (flagged as human decisions); running infrastructure or deploying on the user's behalf without approval.

## 14. Suggested commit messages for Phase 1 (do not execute)

```
docs: add Phase 1 research, architecture, decisions and implementation plan

Research covers SWEBOK v4, ISO/IEC/IEEE 12207:2017, ISO/IEC 25010:2023,
29148, 42010, 29119, NIST SSDF v1.1, OWASP SAMM v2 / ASVS 5.0 / Top 10:2025,
Scrum Guide 2020, ACM CS2023 and six university curricula, plus the supplied
Artia and UpSites process articles. Defines a 16-skill taxonomy with
orchestration, workflows, templates, references and a validation strategy
for Phase 2. No skills implemented yet.
```

# System Architecture — Software Engineering Skills System

Phase 1 output. Consumer: the Phase 2 implementation agent. This document defines *what* the system is and *how its parts relate*. `IMPLEMENTATION_PLAN.md` defines the order and the per-file specifications. `DECISIONS.md` records the rationale for each numbered decision (D-xx). `RESEARCH.md` holds the evidence.

## 1. Purpose

A reusable, modular set of Agent Skills that lets an AI coding agent run a software project through its whole lifecycle with engineering discipline: reason about the decision at hand, follow a deterministic procedure, produce a traceable artifact, validate it, and stop for a human when the decision is not the agent's to make.

The system answers, in order: what are we building → why → is it feasible → what are the requirements → how is it designed → what architecture fits → what data model fits → how is it implemented → how is it tested → how is it secured → how is it deployed → how is it operated → how is quality measured → how is it maintained and evolved.

## 2. Non-goals

- Not a tutorial on computer science or software engineering. The agent already holds that knowledge; the system supplies procedure, decision criteria and triggers.
- Not a project-management tool; it does not track time, cost or people.
- Not a framework-specific playbook. It adapts to the target stack; it does not prescribe one (D-13).
- Not a replacement for existing well-scoped skills already available to the user (code review, TDD, bug diagnosis). It hands off to them where they exist.
- Not Scrum certification. It borrows Scrum vocabulary; it does not claim conformance (D-10).

## 3. Design principles

1. **Procedure over prose.** Every skill is a numbered procedure whose steps end on a checkable completion criterion and produce a named artifact.
2. **Progressive disclosure.** Description (always loaded) → `SKILL.md` body (on activation, < 300 lines target, hard cap 500) → references/templates (on demand, one level deep).
3. **Single source of truth.** Standards summaries, quality vocabulary, CS decision guides and templates live once, at repository level, and are pointed to — never copied into skills.
4. **Right-size by default.** Every skill scales its depth by project size class (S/M/L, §7.4). A small SaaS gets one-page artifacts; a large API gets full ones. Skills are skipped when their outputs exist and are current.
5. **Quality and security are transversal.** Expressed as inputs to every stage (25010 vocabulary, SSDF practice hooks) and as gates, not as a late phase (D-08, D-09).
6. **Evidence discipline.** Reference files cite sources and carry evidence labels from `RESEARCH.md §0`. Nothing `UNVERIFIED` is stated as fact.
7. **Human decision boundaries are explicit.** Each skill lists the conditions under which it must stop and ask (§7.6).
8. **Portability.** Frontmatter uses only the six Agent Skills spec fields (D-05). Repository doubles as a Claude Code plugin (D-04).
9. **Positive instructions.** State the target behaviour; reserve prohibitions for hard guardrails (from writing-for-agents guidance).
10. **Smaller is better.** A new file must name its problem, user, moment of use, input, output, and why no existing file solves it (`IMPLEMENTATION_PLAN.md §9`).

## 4. Layer model

```
┌──────────────────────────────────────────────────────────────┐
│ ORCHESTRATION   skills/sdlc-orchestrator  (+ registry.yaml)  │  decides stage, gaps, skills, gates, human stops
├──────────────────────────────────────────────────────────────┤
│ WORKFLOWS       workflows/*.md                               │  named compositions of skills for recurring situations
├──────────────────────────────────────────────────────────────┤
│ DISCIPLINE SKILLS  skills/<name>/SKILL.md  (15)              │  procedures with inputs → outputs → validation → handoff
├──────────────────────────────────────────────────────────────┤
│ ARTIFACT TEMPLATES  templates/*.md                           │  the shape of every produced document
├──────────────────────────────────────────────────────────────┤
│ FOUNDATIONS / REFERENCES  references/*.md                    │  standards summaries, quality model, CS decision guides,
│                                                              │  security mappings, stack adaptation, metrics
├──────────────────────────────────────────────────────────────┤
│ VALIDATION  scripts/validate.py + skills/registry.yaml       │  structural checks; docs/validation/ scenario walkthroughs
└──────────────────────────────────────────────────────────────┘
```

Dependency direction is downward only: orchestration → workflows → skills → templates/references. References never point to skills. Templates never point to skills.

## 5. Repository layout (target state after Phase 2)

```
software-engineering-skills/
├── README.md                         # what it is, install (plugin / copy), quick start, map of skills
├── LICENSE                           # MIT (existing)
├── .claude-plugin/
│   └── plugin.json                   # name "se", version, description, license, keywords, repository
├── skills/
│   ├── registry.yaml                 # machine-readable index: skill → stage, inputs, outputs, deps, handoffs, templates
│   ├── sdlc-orchestrator/SKILL.md    # + references/ (gates.md, human-decisions.md, rightsizing.md, state-file.md)
│   ├── discovery/SKILL.md
│   ├── requirements/SKILL.md
│   ├── agile-delivery/SKILL.md
│   ├── domain-model/SKILL.md
│   ├── architecture/SKILL.md
│   ├── data-design/SKILL.md
│   ├── api-design/SKILL.md
│   ├── implementation/SKILL.md       # + references/ (frontend.md, mobile.md, backend.md, async-messaging.md)
│   ├── testing/SKILL.md
│   ├── security/SKILL.md             # + references/ (threat-modeling.md, secure-coding-checklist.md)
│   ├── delivery-pipeline/SKILL.md
│   ├── operations/SKILL.md
│   ├── incident-response/SKILL.md
│   ├── maintenance/SKILL.md
│   └── legacy-modernization/SKILL.md
├── workflows/
│   ├── README.md
│   ├── new-product.md                # idea → production (scenarios A, B, C)
│   ├── add-feature.md                # change to an existing system
│   ├── production-incident.md        # scenario D
│   ├── legacy-modernization.md       # scenario E
│   └── hardening.md                  # security / performance / reliability uplift on an existing system
├── templates/
│   ├── README.md
│   ├── project-state.md
│   ├── discovery-brief.md
│   ├── requirements-spec.md
│   ├── backlog.md
│   ├── domain-model.md
│   ├── architecture-overview.md
│   ├── adr.md
│   ├── data-model.md
│   ├── threat-model.md
│   ├── risk-register.md
│   ├── test-strategy.md
│   ├── deployment-plan.md
│   ├── runbook.md
│   ├── incident-postmortem.md
│   ├── tech-debt-register.md
│   └── legacy-assessment.md
├── references/
│   ├── README.md                     # index with one-line "load when…" per file
│   ├── lifecycle-map.md              # stages ↔ 12207 ↔ SWEBOK ↔ SSDF/SAMM (from RESEARCH §9.1)
│   ├── quality-model.md              # ISO/IEC 25010:2023 characteristics, sub-characteristics, how each stage uses them
│   ├── requirements-quality.md       # 29148 criteria (verified subset), smells, acceptance-criteria patterns, traceability IDs
│   ├── architecture-styles.md        # styles, drivers, trade-offs, when distribution is justified, C4 + 42010 concepts, ADR format
│   ├── cs-foundations.md             # decision triggers: complexity, data structures, concurrency, consistency, networking, OS, PL
│   ├── data-foundations.md           # relational vs NoSQL choice, normalization, indexing, transactions/isolation, migrations, caching
│   ├── security-framework-map.md     # SSDF v1.1 practices, SAMM v2, ASVS 5.0 chapters/levels, OWASP Top 10:2025 → where each skill applies them
│   ├── testing-foundations.md        # levels, technique families (29119 Part 4), test pyramid guidance, test data/env, flakiness
│   ├── operations-foundations.md     # SLI/SLO/SLA, error budgets, observability signals, DORA metrics, 12-factor, SRE incident roles, postmortems
│   ├── scrum-vocabulary.md           # Scrum Guide 2020 elements as used here; what this system does not claim
│   ├── engineering-metrics.md        # DORA, quality metrics, what to measure per stage, anti-patterns
│   ├── stack-adaptation.md           # procedure to detect and respect the target stack; compact convention table
│   └── agent-working-rules.md        # how an AI agent should work inside a codebase: verify, small diffs, no invented APIs, evidence
├── scripts/
│   └── validate.py                   # structural validation (frontmatter, names, sizes, links, registry consistency)
└── docs/
    ├── RESEARCH.md                   # Phase 1
    ├── ARCHITECTURE.md               # Phase 1 (this file)
    ├── DECISIONS.md                  # Phase 1, extended in Phase 2
    ├── IMPLEMENTATION_PLAN.md        # Phase 1
    ├── SKILL_AUTHORING.md            # Phase 2: the skill contract for contributors
    └── validation/                   # Phase 2: scenario walkthroughs A–E and audit results
```

Skills are flat under `skills/` (no category folders) for portability across Agent-Skills runtimes (D-06). Layer and stage are carried in `metadata` and `registry.yaml`.

## 6. Skill interface contract

### 6.1 Frontmatter (six spec fields only — D-05)

```yaml
---
name: requirements                       # == directory name; a-z0-9- ; ≤ 64
description: >-                          # ≤ 1024 chars; target 250–450; trigger first, then what, then when-not
  Elicit, specify and validate functional and non-functional requirements with acceptance criteria and traceability IDs.
  Use when a discovery brief exists and the team needs a requirements spec, when requirements change, or when acceptance
  criteria are missing. Not for product vision or backlog ordering (agile-delivery) or architecture choices (architecture).
license: MIT
compatibility: Designed for Claude Code and other Agent Skills runtimes. Reads/writes Markdown under docs/engineering/ in the target repository.
metadata:
  se-layer: discipline                   # orchestration | discipline
  se-stage: requirements                 # lifecycle stage key from references/lifecycle-map.md
  se-version: "0.1.0"
---
```

`allowed-tools` is omitted (experimental; the skills only read/write files and run the project's own commands).

### 6.2 Body sections (fixed order; omit a section only when it is genuinely empty)

1. **Purpose** — one paragraph: the engineering outcome.
2. **Use when / Do not use when** — bullets; the "do not" bullets name the skill that applies instead.
3. **Inputs** — table: input, required/optional, where it normally comes from (artifact path or user).
4. **Procedure** — numbered steps. Each step: action, decision criteria where a choice exists, and a completion criterion ("Done when …"). Right-sizing notes inline (`S:` / `M:` / `L:`).
5. **Outputs** — table: artifact, template path, default location in target repo, consumers.
6. **Validation** — checklist the agent runs on its own output before handoff. Checkable, exhaustive.
7. **Stop and ask** — conditions requiring a human decision, with the exact question to ask.
8. **Handoff** — next skills and what they consume; what to update in `docs/engineering/STATE.md`.
9. **References** — relative links to `references/` and `templates/` files with a one-line "load when …".

### 6.3 Size and style limits

- `SKILL.md` ≤ 300 lines target, 500 hard cap; body ≤ ~4,000 tokens.
- Description ≤ 450 chars (keeps 16 skills within the Claude Code listing budget of ~1% of context; each entry is capped at 1,536 chars anyway).
- One skill may point to at most 6 reference/template files.
- Terminology: use the glossary in `references/lifecycle-map.md` (stage names, artifact names, ID prefixes). No synonyms.

## 7. Orchestration design (`skills/sdlc-orchestrator`)

### 7.1 Responsibilities
Determine situation and stage; detect missing information; select the minimal skill sequence; enforce gates; maintain project state; stop for human decisions. It never performs a discipline's work itself.

### 7.2 Inputs
- User request (free text).
- Target repository inspection: presence of `docs/engineering/STATE.md` and artifacts; stack signals (manifest files, CI config, Dockerfile, IaC).
- `skills/registry.yaml` (skill graph).

### 7.3 Situation classification (step 1)

| Situation | Signals | Workflow |
|---|---|---|
| `new-product` | no code or empty repo; "idea", "build", "MVP", "app" | `workflows/new-product.md` |
| `add-feature` | existing code; request adds capability | `workflows/add-feature.md` |
| `incident` | "down", "outage", "errors in production", "rollback", alert text | `workflows/production-incident.md` |
| `legacy` | existing code with weak/no docs or tests; "modernize", "migrate", "understand this codebase" | `workflows/legacy-modernization.md` |
| `hardening` | existing system; "secure", "scale", "performance", "reliability", audit findings | `workflows/hardening.md` |
| `question` | a single engineering question | answer directly; load one reference; no workflow |

### 7.4 Project size class (rightsizing)

> Superseded in detail by D-20 (Phase 2): the authoritative criteria are in `skills/sdlc-orchestrator/references/rightsizing.md §1`. The table below is the Phase 1 draft.

| Class | Heuristics | Effect |
|---|---|---|
| **S** | 1–2 developers, single deployable, < ~10 k LOC, no regulated data, internal or small user base | one-page artifacts; ≤ 3 ADRs; threat model as a table; test strategy as a section in requirements; no separate runbook until deployment |
| **M** | small team, 1–3 deployables, external users, PII | full templates; C4 context+container; contract tests where services talk; SLOs for user-facing paths |
| **L** | multiple teams/services, regulated or high-value data, high traffic | full templates plus component views, capacity model, DR plan, ASVS L2+, formal traceability matrix |

The class is recorded in `STATE.md` and can be raised (never silently lowered) by any skill that discovers a driver (e.g., PII found → at least M).

### 7.5 Stage detection and skill selection (steps 2–4)

```
state   = read docs/engineering/STATE.md (or create from templates/project-state.md)
artifacts = existence + freshness of each artifact in registry (freshness: modified after its inputs)
for each skill in workflow.sequence:
    if all(skill.outputs exist and fresh): skip, log "reused"
    elif any(required input missing): 
        if input is producible by an earlier skill: schedule that skill first
        else: STOP-AND-ASK the specific question (7.6)
    else: run skill; record outputs, decisions, open questions in STATE.md
    run stage gate (references/gates.md); on failure: fix within skill or STOP-AND-ASK
```

A skill is never invoked "because it exists". Only workflow membership plus missing/stale outputs justify a run.

### 7.6 Human decision triggers (STOP-AND-ASK)

The orchestrator and every skill stop for: go/no-go on feasibility; scope change vs. the discovery brief; budget/timeline trade-offs; replacing a stated technology stack; accepting a security risk or deferring a High/Critical threat mitigation; irreversible data operations (migration with data loss, deletion); production deployment or rollback execution; conflicting stakeholder priorities; regulatory/compliance interpretation; any action the user has marked as approval-gated. Questions are asked with the options and the agent's recommendation.

### 7.7 Gates (`skills/sdlc-orchestrator/references/gates.md`)

One checklist per stage transition; each item is a yes/no check on an artifact. Example, Requirements → Design: every FR has ≥ 1 acceptance criterion; every NFR names a 25010 characteristic and a measurable target; constraints and assumptions listed; open questions have owners; security requirements present (SSDF PO.1); traceability IDs assigned; human approval recorded if scope changed.

### 7.8 Project state (`docs/engineering/STATE.md` in the target repository)

Fields: situation; size class; current stage; stack summary; artifact index (path, status, last updated); decisions index (ADR ids); open questions; risks summary pointer; next action. Updated by every skill on handoff. Template: `templates/project-state.md`.

## 8. Skill taxonomy

| Skill | Stage | Produces (artifact → template) | Requires | Hands off to |
|---|---|---|---|---|
| `sdlc-orchestrator` | all | `STATE.md` | user request, repo | any |
| `discovery` | discovery | Discovery Brief (problem, stakeholders, objectives, scope, constraints, assumptions, feasibility verdict, success criteria, product vision one-liner) → `discovery-brief.md`; Risk Register seed → `risk-register.md` | user intent | `requirements`, `security` (risk profile) |
| `requirements` | requirements | Requirements Spec (FR, NFR by 25010, constraints, acceptance criteria, traceability IDs, change log) → `requirements-spec.md` | Discovery Brief | `agile-delivery`, `domain-model`, `architecture`, `testing`, `security` |
| `agile-delivery` | planning (recurring) | Backlog (epics, stories, AC, priority, DoR, DoD, iteration plan, review/retro notes) → `backlog.md` | Requirements Spec | `implementation`, back to `requirements` on change |
| `domain-model` | design | Domain Model (glossary/ubiquitous language, entities, relationships, invariants, bounded contexts when M/L) → `domain-model.md` | Requirements Spec | `architecture`, `data-design`, `api-design`, `implementation` |
| `architecture` | design | Architecture Overview (drivers as quality scenarios, C4 context/container, style choice, integration, cross-cutting, deployment view) → `architecture-overview.md`; ADRs → `adr.md` | Requirements Spec, Domain Model (optional for S) | `data-design`, `api-design`, `security` (threat model), `delivery-pipeline`, `implementation` |
| `data-design` | design | Data Model (logical/physical, storage choice, keys/indexes, transactions & consistency, migrations, retention, caching) → `data-model.md` | Domain Model, Architecture | `implementation`, `testing`, `security` |
| `api-design` | design | API contract (OpenAPI/GraphQL SDL/AsyncAPI file in the target repo) + design notes section in Architecture Overview | Domain Model, Architecture | `implementation`, `testing`, `security` |
| `implementation` | construction | code + module design notes; updates traceability (REQ → code/test) | Architecture, Data Model, API contract, Backlog item | `testing`, `security` (review hooks), `delivery-pipeline` |
| `testing` | verification (recurring) | Test Strategy (levels, coverage by 25010 characteristic, environments, data, automation, exit criteria) → `test-strategy.md`; per-feature test plan section | Requirements Spec, Architecture | `delivery-pipeline`, `agile-delivery` (DoD) |
| `security` | transversal (invoked at design, construction, verification, operations) | Threat Model → `threat-model.md`; security requirements into Requirements Spec; security checklist results | Discovery Brief (risk profile), Architecture | every stage; `incident-response` |
| `delivery-pipeline` | deployment | Deployment Plan (environments, CI stages, artifact integrity, config/secrets, strategy, rollback, handover) → `deployment-plan.md`; pipeline config in repo | Architecture, Test Strategy | `operations` |
| `operations` | operations | Runbook (SLIs/SLOs, dashboards/alerts, on-call, routine ops, DR, capacity) → `runbook.md` | Deployment Plan, Architecture | `incident-response`, `maintenance` |
| `incident-response` | operations (event) | Incident record + Postmortem → `incident-postmortem.md`; corrective actions into Tech Debt Register / Backlog | Runbook (optional), live symptoms | `maintenance`, `security` (if vulnerability) |
| `maintenance` | evolution (recurring) | Tech Debt Register → `tech-debt-register.md`; fix/refactor/upgrade plans as backlog items | code, Runbook, incidents | `implementation`, `testing`, `delivery-pipeline` |
| `legacy-modernization` | evolution (project) | Legacy Assessment (as-is architecture, debt, risks, modernization options, incremental migration plan) → `legacy-assessment.md`; new ADRs | existing code | `architecture`, `data-design`, `maintenance`, `testing` |

Fifteen discipline skills plus one orchestrator. Rationale for merges and splits: D-07.

## 9. Artifact model

### 9.1 Location and naming in the target repository
`docs/engineering/` by default (overridable in `STATE.md`): `STATE.md`, `discovery-brief.md`, `requirements.md`, `backlog.md`, `domain-model.md`, `architecture.md`, `adr/NNNN-kebab-title.md`, `data-model.md`, `api/` (contract files), `threat-model.md`, `risk-register.md`, `test-strategy.md`, `deployment-plan.md`, `runbook.md`, `incidents/YYYY-MM-DD-slug.md`, `tech-debt.md`, `legacy-assessment.md`.

### 9.2 Identifiers and traceability
Prefixes: `REQ-F-###` functional, `REQ-N-###` non-functional, `CON-###` constraint, `ASM-###` assumption, `RISK-###`, `ADR-####`, `THR-###` threat, `TEST-###`, `DEBT-###`, `INC-YYYYMMDD-#`. Traceability is a table in the Requirements Spec (REQ → ADR/component → TEST → status) maintained by `requirements`, `implementation` and `testing`; L projects may extract it to a matrix file. No separate matrix template for S/M (D-14).

### 9.3 Artifacts consciously not created
PRD *and* SRS as separate documents (merged into Requirements Spec with a product context section); separate stakeholder map (section of Discovery Brief); separate feasibility study (section with verdict in Discovery Brief); separate test plan document (section per feature in Test Strategy or in the story); maintenance plan (covered by Runbook + Tech Debt Register); API design template (the API contract file *is* the artifact).

## 10. Workflows

Each workflow file: purpose; entry conditions; sequence (skill → outputs → gate); size-class variations; exit criteria; typical human stops.

- **new-product**: orchestrator → discovery → [gate: feasibility go] → requirements → security (risk profile + security requirements) → agile-delivery (backlog) → domain-model (M/L) → architecture → security (threat model) → data-design → api-design → testing (strategy) → delivery-pipeline (skeleton CI early) → implementation ⇄ testing per backlog item → security (checklist before release) → delivery-pipeline (release) → operations → maintenance. Scenarios A (small SaaS: S), B (mobile: M, `implementation/references/mobile.md`), C (large API: L).
- **add-feature**: orchestrator → requirements (delta) → agile-delivery → architecture (only if drivers change; else ADR-lite) → data/api design (only if schema/contract changes) → implementation ⇄ testing → security checklist → delivery-pipeline.
- **production-incident**: orchestrator → incident-response (declare, roles, mitigate, communicate, live doc) → [stabilized] → postmortem → maintenance (corrective actions) → security (if vulnerability) → operations (alerts/runbook update).
- **legacy-modernization**: orchestrator → legacy-modernization (reverse engineering, as-is, debt, risks) → discovery (goals of modernization; feasibility) → requirements (what must be preserved, characterization tests) → architecture (target + migration strategy, e.g. incremental extraction) → data-design (migration) → testing (characterization/regression) → implementation increments → delivery-pipeline (parallel run/cut-over) → operations.
- **hardening**: orchestrator → operations (baseline SLIs) → security (threat model/ASVS gap) or architecture (quality scenarios) → maintenance (debt register) → prioritized backlog → implementation ⇄ testing → delivery-pipeline.

## 11. Cross-cutting concerns

- **Security**: one skill, many entry points. `references/security-framework-map.md` maps SSDF practices to the stage/skill that satisfies each. Gates require: risk profile at discovery; security requirements at requirements; threat model at architecture; secure-coding checklist and dependency check at implementation; security tests at verification; secure defaults, integrity and secrets at deployment; vulnerability handling at operations.
- **Quality**: `references/quality-model.md` is the vocabulary; requirements emit NFRs per characteristic; architecture emits quality attribute scenarios; testing maps levels to characteristics; operations maps SLIs to characteristics; `engineering-metrics.md` gives DORA and quality metrics.
- **CS foundations**: `references/cs-foundations.md` and `data-foundations.md` are decision-trigger guides consulted by architecture, data-design, api-design and implementation ("if N > … or latency budget < …, complexity matters"; "if two writers can race, define the consistency model"; "if it crosses a network, design for partial failure").
- **Stack adaptation**: `references/stack-adaptation.md` — detect stack from manifests; respect it; identify its conventions (test runner, linter, formatter, build, package manager, project layout); recommend replacement only with explicit requirement-driven justification recorded as an ADR (D-13).
- **AI-agent working rules**: `references/agent-working-rules.md` — verify before asserting; run the project's tests; small reviewable diffs; never invent APIs, versions or standards; cite sources for external claims; prefer existing project conventions; log assumptions in STATE.md.

## 12. Validation mechanisms

1. **Structural** (`scripts/validate.py`, Python 3 stdlib only): frontmatter parses; only the six spec fields present; `name` matches directory and regex; description 1–1024 chars (warn > 450); `SKILL.md` ≤ 500 lines (warn > 300); every relative link resolves; required body sections present in order; every skill in `registry.yaml` exists and vice-versa; every template referenced exists; every handoff target is a known skill; every artifact in the registry has a template; no `UNVERIFIED` label inside `references/`.
2. **Registry** (`skills/registry.yaml`): the single graph the orchestrator and the validator read. Schema in `IMPLEMENTATION_PLAN.md §6`.
3. **Scenario walkthroughs** (`docs/validation/scenario-*.md`): for A–E, record the request, classified situation, size class, skill sequence actually selected, artifacts produced (as outlines), gates, human stops, gaps found, fixes applied.
4. **Consistency review**: terminology grep against the glossary; duplicate-concept scan across skills and references; contradiction scan (same topic, different instruction).
5. **Context budget**: total description characters; per-skill line counts; reference sizes — reported by the validator.

## 13. Context budget (estimate)

16 descriptions × ≤ 450 chars ≈ 7 k chars ≈ 1.8 k tokens always loaded (within the ~1% listing budget for a 200 k context, shared with other installed skills). Orchestrator body ≈ 250 lines; discipline bodies 150–300 lines each; a typical run loads orchestrator + one skill + one or two references ≈ 8–12 k tokens. Templates are read only when producing the artifact.

## 14. Extensibility and maintenance rules

- New skill only if: distinct trigger word the user actually says, distinct outputs, cannot be a reference or a section of an existing skill. Add to `registry.yaml`, add a template if it produces a new artifact, run the validator, add a scenario touching it.
- New reference only if ≥ 2 skills need it or it is standards content that must be cited exactly.
- Standards versions are pinned in file headers (e.g., "ISO/IEC 25010:2023", "SSDF v1.1", "ASVS 5.0.0", "Scrum Guide 2020", "OWASP Top 10:2025") with the retrieval date; a `references/README.md` table lists them for periodic re-verification.
- `docs/DECISIONS.md` is append-only; superseding decisions reference the superseded id.

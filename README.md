# Software Engineering Skills

A modular, evidence-based skill system that lets an AI coding agent run a software project through its whole lifecycle with engineering discipline — from a vague idea to requirements, architecture, data and API design, implementation, testing, security, deployment, operations, incidents, maintenance and legacy modernization — producing traceable artifacts and stopping when a human must decide.

Skills follow the [Agent Skills](https://agentskills.io) format and load in Claude Code (as a plugin or copied skills) and other Agent-Skills runtimes.

## What it does

`sdlc-orchestrator` classifies the situation (new product, feature, incident, legacy, hardening), assigns a size class (S/M/L), reads the project's `docs/engineering/STATE.md`, selects the minimal ordered set of skills, enforces stage gates, and stops for the human decisions listed in `skills/sdlc-orchestrator/references/human-decisions.md`. Fifteen discipline skills each run a numbered procedure with completion criteria, write one artifact from `templates/`, validate it, and hand off.

```
Foundations (references/)  →  Discipline skills (skills/)  →  Workflows (workflows/)
        ↑                              ↓                              ↓
   standards, quality model,     artifacts (templates/)      gates + human stops
   CS decision triggers                  ↓
                             validation (scripts/validate.py, skills/registry.yaml)
```

## Install

**As a Claude Code plugin (recommended)**
```bash
git clone https://github.com/caiovitorsjesus/software-engineering-skills.git
claude --plugin-dir ./software-engineering-skills
# skills appear as /se:<skill>, e.g. /se:sdlc-orchestrator
```

**By copying** — copy the repository (or just `skills/`, `references/`, `templates/`, `workflows/` together, since skills link to the shared folders by relative path) into `.claude/skills/` of a project or `~/.claude/skills/`.

**Other runtimes** — any Agent-Skills-compatible agent can load `skills/<name>/SKILL.md`; frontmatter uses only the six spec fields.

## Quick start

1. In your project, ask the agent to run the orchestrator: *"Use sdlc-orchestrator: we want to build …"* (or `/se:sdlc-orchestrator`).
2. It creates `docs/engineering/STATE.md`, detects your stack, proposes a size class and runs the first skill (usually `discovery`).
3. Answer the questions it stops on (go/no-go, scope, costly targets, risk acceptance, production deploys). Everything else proceeds under recorded assumptions.
4. Artifacts accumulate under `docs/engineering/` and stay linked by IDs (`REQ-`, `ADR-`, `THR-`, `TEST-`, `DEBT-`, `INC-`).

You can also invoke a single skill directly when its inputs exist: `/se:requirements`, `/se:architecture`, `/se:testing`, `/se:incident-response`, …

## Skills

| Skill | Stage | Produces |
|---|---|---|
| `sdlc-orchestrator` | all | STATE.md, skill sequence, gates, human stops |
| `discovery` | discovery | Discovery Brief, Risk Register |
| `requirements` | requirements | Requirements Spec (FR, NFR per ISO/IEC 25010:2023, security, traceability) |
| `agile-delivery` | planning | Backlog (epics, stories, DoR/DoD, iteration) |
| `domain-model` | design | Domain Model |
| `architecture` | design | Architecture Overview (C4), ADRs |
| `data-design` | design | Data Model, migrations |
| `api-design` | design | API Contract (OpenAPI / GraphQL / AsyncAPI) |
| `implementation` | construction | code + tests, traceability (platform notes: frontend, mobile, backend, async) |
| `testing` | verification | Test Strategy, per-feature test plans |
| `security` | transversal | risk profile, security requirements, Threat Model, secure-coding review, security tests, release hardening, vulnerability handling |
| `delivery-pipeline` | deployment | Deployment Plan, pipeline config |
| `operations` | operations | Runbook (SLOs, observability, alerts, DR) |
| `incident-response` | operations | Incident record, blameless Postmortem |
| `maintenance` | evolution | Tech Debt Register, fixes/upgrades |
| `legacy-modernization` | evolution | Legacy Assessment, migration strategy |

Workflows: [new-product](workflows/new-product.md) · [add-feature](workflows/add-feature.md) · [production-incident](workflows/production-incident.md) · [legacy-modernization](workflows/legacy-modernization.md) · [hardening](workflows/hardening.md).

## Grounding

References summarize, with retrieval dates and evidence labels: SWEBOK v4, ISO/IEC/IEEE 12207:2017, ISO/IEC 25010:2023, ISO/IEC/IEEE 29148, 42010:2022, 29119, NIST SSDF v1.1, OWASP SAMM v2 / ASVS 5.0 / Top 10:2025, Scrum Guide 2020, ACM CS2023 and six university curricula, DORA, Google SRE, Twelve-Factor. Research, architecture, decisions and the implementation plan are in [docs/](docs/). Nothing unverified is stated as fact (`docs/RESEARCH.md §0`).

## Principles

Procedure over prose · simplest architecture that meets the quality scenarios (distribution needs a recorded driver) · respect the project's stack · quality and security at every gate, not at the end · right-size by S/M/L · explicit human decision boundaries · portability (six-field frontmatter).

## Validate

```bash
python scripts/validate.py --strict # frontmatter, sections, links, registry graph, handoff drift
python scripts/run_evals.py         # behavioral eval fixtures: routing, safety, injection, budgets
python scripts/run_evals.py --prompts   # print the harness for the agent-run half
```

`validate.py` proves the system is structurally coherent; `run_evals.py` guards behaviour — that requests route correctly, destructive ones stop for approval, directives hidden in project files are reported rather than obeyed, and context budgets hold. See [evals/README.md](evals/README.md).

## Contributing

Read [docs/SKILL_AUTHORING.md](docs/SKILL_AUTHORING.md). New skills need a distinct trigger, distinct outputs and an entry in `skills/registry.yaml`; new files must pass the anti-overengineering gate in `docs/IMPLEMENTATION_PLAN.md §9`.

## Limitations

Scenario validation (`docs/validation/`) is by desk walkthrough, not by execution on real repositories; the adversarial audit (`docs/validation/PHASE_3_ADVERSARIAL_AUDIT.md`) rates the system READY WITH MINOR ISSUES pending a supervised pilot. ISO standard texts were summarized from secondary sources (iso.org pages were inaccessible); see `references/README.md` for the re-verification table. If the Claude Code skill listing budget is tight, mark low-priority skills `name-only` via `skillOverrides`.

## License

MIT — see [LICENSE](LICENSE).

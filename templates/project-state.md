<!--
Purpose: Single index of a project's engineering state so any agent session can resume without re-deriving stage, decisions or open questions.
Producer: sdlc-orchestrator (creates); every skill updates its rows on handoff.
Consumers: sdlc-orchestrator, all skills, humans reviewing progress.
Update when: any artifact is created/changed, a decision is made, a question is opened/closed, a stage changes.
Size: keep under two screens; link out, do not duplicate artifact content.
-->
# Project State

| Field | Value |
|---|---|
| Project | <name> |
| Situation | new-product / add-feature / incident / legacy / hardening |
| Size class | S / M / L — reason: <driver, e.g. "PII present → M"> |
| Current stage | discovery / requirements / planning / design / construction / verification / deployment / operations / evolution |
| Workflow | workflows/<file>.md |
| Suspended workflow / resume point | <workflow + step, when an incident interrupts other work; empty otherwise> |
| Docs root | docs/engineering/ |
| Last updated | YYYY-MM-DD by <skill> |
| Next action | <one concrete step, with the skill that performs it> |

## Stack

| Item | Value |
|---|---|
| Languages / frameworks / versions | |
| Package manager / build | |
| Commands: build · test · lint · run | |
| Data stores | |
| CI / deploy target | |
| Unknowns | |

## Roles and owners

| Role | Who | Notes |
|---|---|---|
| Product decisions | | |
| Technical approvals (deploy, risk acceptance) | | |
| Security contact | | |

## Artifact index

| Artifact | Path | Status (missing / draft / current / stale / embedded in <artifact>) | Inputs it depends on | Last updated | Last substantive change |
|---|---|---|---|---|---|
| Discovery Brief | discovery-brief.md | | user intent | | |
| Risk Register | risk-register.md | | | | |
| Requirements Spec | requirements.md | | Discovery Brief | | |
| Backlog | backlog.md | | Requirements Spec | | |
| Domain Model | domain-model.md | | Requirements Spec | | |
| Architecture Overview | architecture.md | | Requirements Spec, Domain Model | | |
| ADRs | adr/ | | | | |
| Data Model | data-model.md | | Domain Model, Architecture | | |
| API Contract | api/ | | Domain Model, Architecture | | |
| Threat Model | threat-model.md | | Architecture | | |
| Test Strategy | test-strategy.md | | Requirements Spec, Architecture | | |
| Deployment Plan | deployment-plan.md | | Architecture, Test Strategy | | |
| Runbook | runbook.md | | Deployment Plan | | |
| Tech Debt Register | tech-debt.md | | | | |
| Legacy Assessment | legacy-assessment.md | | source code | | |

Freshness rule: an artifact is **stale** when an artifact it depends on had a *substantive* change (change-log entry, new/superseded ADR, schema or contract change) after its `Last substantive change`; traceability/status/log edits do not count.

## Decisions (ADR index)

| ADR | Title | Status | Date |
|---|---|---|---|

## Gates passed

| Gate | Date | Evidence / notes |
|---|---|---|

## Open questions (Stop and ask)

| # | Question | Options | Recommendation | Raised by | Status |
|---|---|---|---|---|---|

## Assumptions in force

| ASM | Statement | How to validate | Owner | Status |
|---|---|---|---|---|

## Log (most recent 10 entries)

| Date | Skill | What changed |
|---|---|---|

# Templates — Artifact Shapes

Each template is the shape of one engineering artifact. Skills point to a template when they produce the artifact; the artifact lives in the target repository under `docs/engineering/` (see `references/lifecycle-map.md §3`). Every template opens with an HTML comment stating purpose, producer, consumers, update triggers and size guidance. Fill sections with evidence or an explicit `ASM-###`; delete sections only when the size class says so.

| Template | Artifact | Producer | Main consumers |
|---|---|---|---|
| [project-state.md](project-state.md) | STATE.md | sdlc-orchestrator | all skills |
| [discovery-brief.md](discovery-brief.md) | Discovery Brief | discovery | requirements, security, sponsor |
| [risk-register.md](risk-register.md) | Risk Register | discovery (+ all) | orchestrator, architecture, security |
| [requirements-spec.md](requirements-spec.md) | Requirements Spec (incl. traceability) | requirements | agile-delivery, design skills, testing |
| [backlog.md](backlog.md) | Backlog (epics, stories, DoR, DoD, iteration) | agile-delivery | implementation, testing |
| [domain-model.md](domain-model.md) | Domain Model | domain-model | architecture, data-design, api-design |
| [architecture-overview.md](architecture-overview.md) | Architecture Overview | architecture | design/build/run skills |
| [adr.md](adr.md) | ADR | architecture, data-design, legacy-modernization | everyone |
| [data-model.md](data-model.md) | Data Model | data-design | implementation, testing, security |
| [threat-model.md](threat-model.md) | Threat Model | security | architecture, implementation, testing |
| [test-strategy.md](test-strategy.md) | Test Strategy (+ per-feature plans) | testing | implementation, delivery-pipeline |
| [deployment-plan.md](deployment-plan.md) | Deployment Plan | delivery-pipeline | operations, incident-response |
| [runbook.md](runbook.md) | Runbook | operations | incident-response, maintenance |
| [incident-postmortem.md](incident-postmortem.md) | Incident record + Postmortem | incident-response | maintenance, security, operations |
| [tech-debt-register.md](tech-debt-register.md) | Tech Debt Register | maintenance, legacy-modernization | agile-delivery, architecture |
| [legacy-assessment.md](legacy-assessment.md) | Legacy Assessment | legacy-modernization | discovery, requirements, architecture |

Deliberately absent (see `docs/DECISIONS.md` D-14 and `docs/ARCHITECTURE.md §9.3`): separate PRD/SRS, stakeholder map, feasibility study, test plan document, maintenance plan, traceability matrix (a table inside the Requirements Spec; L-class may extract it), API design template (the OpenAPI/GraphQL/AsyncAPI file is the artifact).

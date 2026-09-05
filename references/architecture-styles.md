# Architecture Styles, Drivers and Description

> Covers: architectural style selection by drivers and costs; distribution drivers (DECISION D-12); quality attribute scenarios; ISO/IEC/IEEE 42010:2022 description concepts; C4 model levels; ADR format and statuses
> Retrieved: 2026-09-04
> Sources: https://en.wikipedia.org/wiki/ISO/IEC_42010, https://c4model.com/, https://adr.github.io/
> Evidence: STANDARD, INDUSTRY, RECOMMENDATION, DECISION

Load when: choosing or reviewing an architecture style, writing the Architecture Overview, or writing an ADR.

## 1. Start from the simplest style (DECISION D-12)

Default for S and most M projects: **modular monolith** — one deployable, explicit module boundaries (by domain), one database with schema ownership per module, in-process calls. Move away from it only when a driver below is present and its cost is accepted in an ADR.

## 2. Styles: drivers and costs (RECOMMENDATION)

| Style | Choose when (drivers) | Costs you accept |
|---|---|---|
| Single deployable / layered | S; one team; simple domain | Coupling grows unless modules are enforced |
| Modular monolith | M; one or two teams; domain has clear sub-areas; want option to split later | Discipline on module boundaries; shared runtime/failure domain |
| Microservices | Independent deployment by separate teams; independent scaling of hot components; isolation of fault domains; polyglot persistence truly needed; regulatory separation | Network failures, distributed data consistency, observability, deployment complexity, per-service operational cost |
| Event-driven (async messaging) | Temporal decoupling; bursty load smoothing; many consumers of the same fact; integration with slow/unreliable systems | Eventual consistency, ordering and duplicate handling, harder debugging, schema evolution of events |
| CQRS | Read and write models differ strongly; read scale ≫ write scale | Two models to keep in sync; eventual consistency of reads |
| Serverless functions | Spiky/rare workloads; glue and event handlers; minimal ops capacity | Cold starts, vendor lock-in, execution limits, harder local testing |
| Client-heavy (SPA/mobile) + API | Rich interaction; offline needs (mobile) | State synchronization, API versioning for shipped clients |
| Batch / pipeline | Large periodic data processing | Latency; reprocessing and idempotency design |

Rule: a distributed style without at least one listed driver recorded in an ADR fails the Design→Construction gate.

## 3. Quality attribute scenario format (RECOMMENDATION; vocabulary from ISO/IEC 25010:2023)

`Source · Stimulus · Environment · Artifact · Response · Response measure`

Example: *A logged-in user (source) submits a search (stimulus) under normal load of 200 concurrent users (environment) to the search service (artifact); results are returned (response) with p95 ≤ 400 ms (measure).* Each driver scenario is answered by at least one decision or is explicitly deferred with a `RISK-###`.

## 4. Architecture description concepts (STANDARD — ISO/IEC/IEEE 42010:2022)

- An **architecture** is distinct from its **architecture description**.
- Identify **stakeholders** and their **concerns**; choose **viewpoints** that frame those concerns; produce **views** composed of **models**.
- Record **architecture decisions** with **rationale**; maintain **correspondences** (consistency rules) between views.
- 42010 prescribes no notation. This system uses C4 (below) as the default viewpoint set; text tables are an acceptable fallback.

## 5. C4 model (INDUSTRY — Simon Brown)

| Level | Shows | When |
|---|---|---|
| System Context | the system, its users, external systems | always (S/M/L) |
| Container | deployable units (apps, services, databases, queues) and their communication | always |
| Component | major components inside one container | M/L hot spots only |
| Code | classes/modules | rarely; generated from code if needed |
| Supplementary: System Landscape, Dynamic, Deployment | multiple systems; a runtime scenario; infrastructure mapping | Landscape for L; Dynamic for critical flows; Deployment always |

Mermaid is acceptable (`C4Context`, `C4Container` diagrams or plain `graph`); keep a text list of elements next to every diagram so the content survives rendering failures.

## 6. Architecture Decision Records (INDUSTRY — Nygard 2011; MADR)

Sections (template `templates/adr.md`): id, title, status, date, context, decision drivers, options considered, decision, consequences (positive/negative), links (REQ, RISK, THR, related ADRs).
Statuses: **proposed → accepted → deprecated | superseded by ADR-####**. Never edit an accepted ADR's decision; write a new one that supersedes it.

Decisions that always get an ADR: architecture style; primary data store(s); messaging/integration approach; hosting/runtime platform; authentication/authorization approach; frontend/mobile approach; any technology replacement versus the given stack (D-13); any accepted High/Critical security risk.

## 7. Cross-cutting decisions checklist (RECOMMENDATION)

Authentication and authorization model · configuration and secrets handling · error handling and error contract · logging/metrics/tracing hooks (correlation ids) · time and time zones · internationalization (if applicable) · idempotency and retries at boundaries · rate limiting and quotas · data lifecycle (retention, deletion) · feature flags · backwards compatibility policy.

## 8. Integration and communication (RECOMMENDATION; failure modes in `cs-foundations.md §3`)

| Question | Options | Decide by |
|---|---|---|
| Sync or async? | request/response vs. messages/events | need for immediate answer; tolerance for delay; coupling |
| Contract | OpenAPI / GraphQL SDL / gRPC IDL / AsyncAPI | consumer types; tooling in the stack |
| Consistency across stores | saga / outbox / two-phase (avoid) | invariants that span modules |
| Resilience | timeout, retry with backoff + jitter, circuit breaker, bulkhead, fallback | dependency criticality |

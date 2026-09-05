# Scenario C — Large API / backend

**Request (verbatim, invented):** "Design the order-management API platform for our marketplace: three teams (catalog, orders, payments-integration), peak 5,000 requests/s, partners integrate via public API, PCI handled by our PSP but we store order and payout records, EU and US customers, 99.95 % availability target. Java/Kotlin services, PostgreSQL, Kafka already in use."

## Orchestrator run

| Step | Result |
|---|---|
| Situation | `new-product` (new platform; existing infra conventions detected as constraints) |
| Stack | named + detected: JVM services, PostgreSQL, Kafka, existing CI → `CON-` rows; commands from existing service templates |
| Size class | **L** — multiple teams, many deployables, high traffic, financial records at volume, EU/US data (residency), 99.95 % target |
| Workflow | `workflows/new-product.md` (L variations) |

## Sequence selected

| # | Skill · entry | Decision | Reason |
|---|---|---|---|
| 1–2 | discovery; security A | run | data classes: order, payout (financial), customer PII; EU residency → H9 flagged early |
| 3–4 | requirements; security B | run | ASVS L2 minimum, L3 for payout paths; 99.95 % → H3 confirms cost (multi-AZ, possibly multi-region reads) |
| 5 | agile-delivery | run | epics by team/bounded context |
| 6 | domain-model | run | bounded contexts Catalog, Ordering, Payout; context map (Ordering ← Catalog upstream; Payout downstream of Ordering via events) |
| 7 | architecture | run | distribution drivers present (independent teams, independent scaling of order intake vs catalog reads) → ADR-0001 services per bounded context with costs listed; ADR for Kafka events + outbox; ADR for API gateway/rate limiting; ADR for residency (EU/US data partitioning) after H9/H10; component views for order intake and payout; §9b capacity model (5k rps peak, 3× headroom) |
| 8 | security C | run | Threat Model per service; supply chain (A03) for shared libraries; partner API abuse; payout tampering (integrity, dual control) |
| 9 | data-design | run | per-service schemas; partitioning of orders by month; isolation levels for payout ledger (serializable or explicit locking); outbox tables; residency-aware storage; retention per class |
| 10 | api-design | run | public OpenAPI with versioning policy and consumer-driven contracts for partners; AsyncAPI for order events; idempotency keys; rate limits per partner |
| 11 | testing | run | + performance suite at 5k rps in a pre-prod environment (H10 for cost), resilience tests (Kafka outage, DB failover), contract tests both directions, exploratory, formal acceptance |
| 12 | delivery-pipeline skeleton | run | per-service pipelines; SBOM, signed artifacts, provenance; canary with SLO watch |
| — | gate design-to-construction | pass after H3/H9/H10 closed | |
| 13–15 | implementation ⇄ testing; security D | run per story | `backend.md`, `async-messaging.md` |
| 16 | security E/F | run | DAST, abuse cases for partner API, release hardening |
| 17 | operations | run | SLOs per service and per partner-facing path; error budgets; dashboards; DR with RPO/RTO; capacity headroom |
| — | gate construction-to-release | ask H7 | |
| 18–20 | release; operations; maintenance | run | |

## Artifact outlines (selected)
- **Quality scenarios**: order intake p99 ≤ 300 ms at 5k rps (performance); availability 99.95 % monthly (reliability); partner API breaking change never within a version (compatibility); payout ledger integrity (security/non-repudiation); horizontal scale-out to 3× verified (flexibility › scalability).
- **ADR-0001**: services per bounded context — drivers: independent deployment by three teams, independent scaling; costs accepted: eventual consistency between Ordering and Payout, distributed tracing and contract-test overhead.
- **Data Model**: order tables partitioned monthly; ledger append-only with hash chain (integrity) and serializable isolation for balance updates; outbox per service; EU/US partitioned storage.
- **Threat Model**: `THR-010` partner key leakage → rotation, scoped keys, rate limits; `THR-011` payout tampering → dual control, audit log, integrity checks; `THR-012` supply chain → pinned deps, SBOM, signature verification.
- **Runbook**: per-service SLOs, Kafka lag alerts, DLQ replay procedure, failover drill schedule.

## Human stops
H3 (99.95 %, multi-region) · H9 (EU/US residency) · H10 (pre-prod performance environment cost, gateway product) · H5 if any High accepted · H7.

## Criteria check

| Criterion | Result | Note |
|---|---|---|
| Classification / size | pass | L |
| Skill selection | pass | all skills justified; none extraneous |
| Distribution justified | pass | ADR with drivers per D-12 |
| Security | pass | L2/L3, supply chain, integrity |
| Testing | pass | performance, resilience, contract |
| Observability / operations | pass | SLOs, error budgets, DR |
| Dead ends | none | |

## Gaps found → fixes applied
1. Architecture Overview template had no capacity-model slot although rightsizing L requires one. → Added §9b capacity model.
2. Registry `new-product` sequence order differed from the workflow file (security placement, second agile-delivery, operations before release). → Registry sequences aligned to the workflow files for all five workflows.

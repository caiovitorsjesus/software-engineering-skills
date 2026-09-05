# Scenario B — Mobile application

**Request (verbatim, invented):** "Build a field-inspection app for our technicians: they log in, see assigned jobs, fill checklists, take photos and submit reports, often without signal. Flutter for the app, Spring Boot API, PostgreSQL. About 300 technicians, customer addresses and contact names are in the jobs."

## Orchestrator run

| Step | Result |
|---|---|
| Situation | `new-product` |
| Stack | named → `CON-001` Flutter, `CON-002` Spring Boot, `CON-003` PostgreSQL; commands from generated projects once scaffolded (`flutter test`, `./mvnw verify` or Gradle — recorded when created, not assumed) |
| Size class | **M** — external field users with customer personal data beyond identity (addresses, contact names, photos of premises), offline data on devices, two deployables. Driver recorded. |
| Workflow | `workflows/new-product.md` (M variations) |

## Sequence selected

| # | Skill · entry | Decision | Reason |
|---|---|---|---|
| 1–2 | discovery; security A | run | profile: customer PII on devices → data-protection emphasis |
| 3–4 | requirements; security B | run | ASVS L2; device secure storage; offline data retention; permissions (camera, location) as REQs |
| 5 | agile-delivery | run | — |
| 6 | domain-model | run | M: Job, Checklist, ChecklistItem, Inspection, Photo, Report, Technician, Customer; lifecycle Job (assigned → in progress → submitted → approved); conflict-relevant invariants |
| 7 | architecture | run | modular monolith API + mobile client; ADRs: style, PostgreSQL, object storage for photos, OIDC provider, sync protocol (H10 for object storage/hosting) |
| 8 | security C | run | own Threat Model: device theft, token theft, photo exfiltration, IDOR on job ids, replayed offline submissions |
| 9 | data-design | run | server schema; idempotency keys for offline submissions; photo metadata in DB, blobs in object storage; retention of customer data; local (device) schema versioning noted for implementation |
| 10 | api-design | run | mandatory for M: OpenAPI; cursor pagination for jobs; idempotent POST /inspections with client-generated ids; version header; additive-only policy; min-supported-app-version endpoint |
| 11 | testing | run | + integration (Testcontainers), contract tests (app ↔ API), device integration tests, offline scenario tests, DAST, accessibility |
| 12 | delivery-pipeline skeleton | run | API pipeline + app build pipeline; §7b client distribution (signing custody, store review lead time, staged rollout, forced-update policy) |
| — | gate design-to-construction | pass | after threat model High items mitigated (secure storage, token lifetime) |
| 13–15 | implementation ⇄ testing; security D | run per story | `implementation` loads `references/mobile.md` (offline outbox, conflict policy, permissions, secure storage) and `references/backend.md` |
| 16 | security E/F | run | SAST/dependency both repos; DAST on API; release hardening |
| 17 | operations | run | SLOs: API availability, p95 job list latency, sync success rate; crash-free sessions metric for the app |
| — | gate construction-to-release | ask H7 | API deploy + app store submission |
| 18–20 | release; operations; maintenance | run | — |

## Artifact outlines (selected)
- **Requirements**: `REQ-F-010` offline checklist completion with later sync (AC: airplane-mode test; duplicate submission ignored); `REQ-F-011` photo capture with size limit; `REQ-N-001` sync completes within 60 s on reconnect for 50 pending items; `REQ-N-005` security ASVS L2, tokens in keystore, photos encrypted at rest on device; `REQ-N-006` interaction capability: usable with gloves (target sizes), dynamic type; `REQ-N-007` flexibility: supports last two OS major versions.
- **Threat Model**: `THR-001` stolen device → keystore, short tokens, remote wipe of local DB on revoked session; `THR-002` IDOR on job id → server-side assignment check; `THR-003` replayed submission → idempotency key; `THR-004` photo metadata leaks location → strip EXIF unless required.
- **API Contract**: OpenAPI with `Idempotency-Key`, `X-App-Version`, error schema, examples per operation.
- **Deployment Plan**: API rolling deploy; app staged rollout 10 % → 50 % → 100 %; kill switch for photo upload; store review lead time 1–3 days recorded.

## Human stops
H1 · H10 (object storage / hosting) · H5 if any High threat is deferred · H7 (API deploy and store submission).

## Criteria check

| Criterion | Result | Note |
|---|---|---|
| Classification / size | pass | M with driver |
| Skill selection | pass | all design skills justified for M |
| Workflow, handoffs | pass | mobile.md, backend.md loaded from implementation |
| Security | pass | L2, device threats modeled, checklist D/F |
| Testing | pass | offline, contract, device tests planned |
| Human triggers | pass | |
| Dead ends | none | store submission previously unaddressed — fixed below |

## Gaps found → fixes applied
1. Deployment Plan template and `delivery-pipeline` had no place for mobile/desktop client distribution (signing, store review, staged rollout, forced update). → Added template §7b and a step-7 line in the skill.
2. `testing` registry inputs lacked `threat-model?` although the skill consumes abuse cases. → Added.

# Scenario A — Small SaaS from a vague idea

**Request (verbatim, invented):** "I want to build a simple SaaS where freelancers create invoices, send them to clients and see who has paid. Nothing exists yet. I'm the only developer."

## Orchestrator run

| Step | Result |
|---|---|
| Situation | `new-product` — empty repository; "build", "nothing exists yet" |
| Stack | none detected; none named → open; commands `unknown` until architecture proposes |
| Size class | **S** — one developer, single deployable, MVP with up to a few hundred users, personal data limited to account identity plus user-generated invoices (client names/emails, amounts). Payments via a provider keep card data out of scope. Driver recorded: "solo MVP; identity-only PII; provider-handled payments". Raise to M when user volume grows or financial records reach volume (rightsizing §1). |
| Workflow | `workflows/new-product.md` |

## Sequence selected (run / skip / ask)

| # | Skill · entry | Decision | Reason |
|---|---|---|---|
| 1 | discovery | run | no brief |
| 2 | security A | run | gate requires risk profile |
| — | gate discovery-to-requirements | ask H1 | go/no-go presented with feasibility verdict `go` |
| 3 | requirements | run | — |
| 4 | security B | run | ASVS L1; authn via framework/provider; data protection for client PII |
| 5 | agile-delivery | run | — |
| 6 | domain-model | **skip** | ~6 entities (User, Client, Invoice, LineItem, Payment, Reminder), unambiguous terms; glossary kept in Requirements §1 |
| 7 | architecture | run | — |
| 8 | security C | run | threats table embedded in Architecture Overview §10 (S) |
| 9 | data-design | run | — |
| 10 | api-design | **skip** | server-rendered web app recommended for S; no external consumer (ADR notes when to revisit: mobile app or public API) |
| 11 | testing | run | levels table + exit criteria |
| 12 | delivery-pipeline (skeleton) | run | CI running on the empty project |
| — | gate design-to-construction | pass | API Contract item skipped with reason; threat model embedded |
| 13–15 | implementation ⇄ testing; security D per story | run per story | — |
| 16 | security E/F | run | dependency scan, secure defaults, secrets |
| 17 | operations | run | one-page runbook: 1 SLO (availability), p95 latency, alerts, deploy/rollback, backup |
| — | gate construction-to-release | ask H7 | production deploy approval |
| 18–20 | delivery-pipeline release; operations; maintenance | run | — |

Skills not invoked: incident-response, legacy-modernization (situation-bound). Skipped with reason: domain-model, api-design.

## Artifact outlines produced

- **Discovery Brief**: problem (freelancers chase payments manually; evidence `ASM-001` to validate with 5 interviews); stakeholders (freelancer, freelancer's client, payment provider); objectives (invoice created in < 2 min; 80 % of invoices paid online); scope in (invoice CRUD, send by email, online payment via provider, payment status) / out (accounting, taxes, multi-currency); `CON-001` solo developer, `CON-002` budget ≤ hosting on a PaaS; options build vs. SaaS invoicing tools (differentiator: simplicity); feasibility `go`; risks `RISK-001` provider fees, `RISK-002` email deliverability; vision sentence.
- **Requirements Spec**: `REQ-F-001` create invoice with line items (AC: totals correct incl. boundary 0 and rounding), `REQ-F-002` send invoice email with pay link, `REQ-F-003` record payment via provider webhook (AC: idempotent on duplicate webhook), `REQ-F-004` dashboard of unpaid/overdue; `REQ-N-001` performance p95 ≤ 500 ms for dashboard at 100 users; `REQ-N-002` availability 99.5 % monthly; `REQ-N-003` security ASVS L1, webhook signature verification; `REQ-N-004` maintainability: coverage on changed code ≥ 70 %; others n/a with reason; traceability seeded.
- **Backlog**: goal, 2 epics, 9 stories, DoR/DoD; iteration 1 = invoice CRUD + auth.
- **Architecture Overview**: drivers table (3); ADR-0001 modular monolith, server-rendered; ADR-0002 PostgreSQL; ADR-0003 PaaS hosting + framework auth (H10 asked: paid tier); C4 context (freelancer, client, email provider, payment provider) and container (web app, DB, background jobs); threats table (webhook replay/spoofing → signature + idempotency; IDOR on invoice ids → ownership check; email injection).
- **Data Model**: 6 tables, FK indexes, index on (user_id, status, due_date); money as integer cents; migrations forward-only; PII retention 24 months after account deletion; backups daily.
- **Test Strategy (S)**: unit, component (in-memory DB), 2 e2e journeys (create+send, pay via webhook simulation), dependency scan, basic load check; exit criteria.
- **Deployment Plan (S)**: local/CI/production (staging merged into CI for non-data changes); stages; rollback = redeploy previous release; secrets in PaaS config.
- **Runbook (S)**: SLO, alerts (error rate, webhook failures), deploy/rollback, backup restore date.

## Gates and human stops
H1 go/no-go · H10 hosting tier · H7 production deploy. No H5 (no High/Critical unmitigated).

## Criteria check

| Criterion | Result | Note |
|---|---|---|
| Correct classification | pass | |
| Appropriate skill selection | pass | two skips with logged reasons |
| Workflow progression, no dead ends | pass | |
| Artifacts and handoffs | pass | every produced artifact has a template; embedded status used for risks/threats |
| Security considerations | pass | A, B, C(embedded), D, E, F present at gates |
| Testing considerations | pass | S levels; webhook idempotency tested |
| Human triggers | pass | 3 stops, all in human-decisions.md |
| Context efficiency | pass | orchestrator + one skill + ≤ 2 references per step |

## Gaps found → fixes applied
1. Original size-class table classified any SaaS with external users/PII as **M**, contradicting the plan's "S = small SaaS MVP". → Recalibrated Users/Data rows and added the calibration note (`rightsizing.md §1`, `lifecycle-map.md §5`; D-20).
2. STATE had no way to represent S-class artifacts kept as sections of another document. → Added status `embedded in <artifact>` (`templates/project-state.md`, `state-file.md §2`).

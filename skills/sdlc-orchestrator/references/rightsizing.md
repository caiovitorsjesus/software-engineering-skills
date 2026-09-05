# Right-sizing by Project Class

> Covers: how the size class S/M/L is assigned and what depth each artifact and skill takes per class
> Retrieved: 2026-09-04
> Sources: This system's design (docs/ARCHITECTURE.md §7.4); ASVS level mapping from OWASP ASVS 5.0.0 level descriptions (references/security-framework-map.md §3); SAMM maturity targets from OWASP SAMM v2.0
> Evidence: DECISION, RECOMMENDATION

## 1. Assigning the class

Take the **highest** class any row triggers. Record the triggering row as the driver in STATE.md.

| Driver | S | M | L |
|---|---|---|---|
| Team | 1–2 developers | one small team | multiple teams |
| Deployables | one | 1–3 | many services |
| Users | up to a few hundred users, internal or early external (MVP); simple accounts | thousands of external users or multi-tenant with isolation needs | large public / many tenants |
| Data | account identity only (name, email, credentials) plus user-generated content; no regulated categories | personal data beyond identity at volume (profiles, financial records, location), payments via a provider with contractual obligations | regulated data processed directly (payment card data in scope, health, government) or high-value |
| Traffic / availability need | best effort | business hours, ≤ 99.9 % | 24×7, > 99.9 %, high traffic |
| Integrations | none / one simple | a few external APIs | many, contractual SLAs |
| Consequence of failure | inconvenience | money or reputation | safety, legal, large financial |

Any skill that discovers a driver raises the class (e.g., financial records or location data found during data-design → M). Never lower silently (Stop and ask H13-style confirmation if the user insists).

Calibration note (DECISION D-20): an early-stage SaaS MVP with a few hundred users and identity-only personal data is **S** (ASVS L1, one-page artifacts); it becomes **M** when user volume, data sensitivity or tenancy grows. Every class still runs security at every gate — the class changes depth, not presence.

## 2. Depth per artifact

| Artifact | S | M | L |
|---|---|---|---|
| Discovery Brief | one page; feasibility table with verdict | full template | full + options with cost model |
| Risk Register | section in the brief (top 5) | own file | own file, reviewed at every gate |
| Requirements Spec | FR table + NFR row per applicable characteristic + AC | full template, prioritization method | full + extracted traceability matrix |
| Backlog | stories table + DoD | full | full + epics with outcome metrics |
| Domain Model | glossary only, unless > ~10 entities or ambiguous terms | glossary, entities, invariants, lifecycles | + bounded contexts and context map |
| Architecture Overview | context + container diagram, drivers table, ≤ 3 ADRs | full, quality scenarios for drivers, component views for hot spots | full + landscape, capacity model, DR |
| Data Model | schema, indexes, migrations | full | full + partitioning/archival plan, query-plan evidence |
| API Contract | only if an external consumer exists | required for every cross-container interface | + versioning policy, consumer-driven contracts |
| Threat Model | threats table inside Architecture Overview or own file; SAMM TA level 1 | own file; SAMM level 2; ASVS L2 when PII | own file per service; ASVS L2–L3; periodic review |
| Test Strategy | levels table + exit criteria; unit, component, few e2e, dependency scan, basic load check | + integration, contract, DAST, accessibility | + performance suites, resilience, exploratory, formal acceptance |
| Deployment Plan | environments, stages, rollback, checklist | full | full + SBOM/provenance, signed artifacts, progressive delivery |
| Runbook | SLO (1–2), alerts, deploy/rollback, backup | full | full per service + DR drills |
| Tech Debt Register | table | table + dependency health | + review cadence and budget |

## 3. Skills that may be skipped per class (with logged reason)

| Skill | S | M | L |
|---|---|---|---|
| domain-model | skip unless trigger above | run | run |
| api-design | skip when no external consumer | run | run |
| operations (before first release) | minimal runbook only | run | run |
| legacy-modernization | only in legacy situation | same | same |
| incident-response | only in incident situation | same | same |

All other skills run in every class; their *depth* changes, not their presence. Security runs at every gate in every class.

## 4. Effort guidance for the agent

- S: prefer tables over prose; one artifact section per gate item; no diagrams beyond context/container.
- M: full templates; diagrams as Mermaid with text lists.
- L: full templates; add per-service sections; expect several ADRs per stage; expect human review at every gate.

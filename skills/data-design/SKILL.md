---
name: data-design
description: >-
  Design the data layer: storage choice per data set, schema with constraints, indexes justified by
  access paths, transactions and consistency rules, migration strategy, data lifecycle and protection,
  caching and growth estimates. Use when a schema is missing or changing, queries are slow, migrations
  are risky, or data classification changes. Not for domain concepts (use domain-model) or system
  decomposition (use architecture).
license: MIT
compatibility: Designed for Claude Code and other Agent Skills runtimes. Reads and writes Markdown under docs/engineering/ in the target repository.
metadata:
  se-layer: discipline
  se-stage: design
  se-version: "0.1.0"
---

# Data Design

## Purpose

Produce a Data Model that implementation can build and operations can run: correct schema and constraints for the domain invariants, indexes tied to real access paths, explicit transaction and consistency rules, a safe migration path, and lifecycle/protection rules for every data class.

## Use when

- Architecture is approved and no Data Model exists.
- A feature adds or changes entities, relationships or access paths.
- Performance findings point at queries, indexes or caching.
- Data classification, retention or erasure requirements change.
- A legacy migration needs a target schema and data migration approach.

## Do not use when

- Domain terms are unclear: `domain-model`.
- The question is which container owns the data or whether to split stores across services: `architecture`.
- Only reading data for a report: no artifact needed.

## Inputs

| Input | Required | Source |
|---|---|---|
| Domain Model | when present; otherwise the Requirements Spec data section (S) or the existing schema and code (delta on an existing system) | `docs/engineering/domain-model.md` |
| Architecture Overview (containers, consistency decisions, store ADR) | new-product: yes; existing system: use it if present, else "as found" (existing stores, ownership inferred from code, recorded as `ASM-`) | `docs/engineering/architecture.md` |
| API Contract or stories (access paths) | no | `docs/engineering/api/`, backlog |
| Existing schema / migrations | no | repository |
| Stack (migration tool, ORM) | yes | `STATE.md › Stack` |

## Procedure

1. **Derive the logical model.** Entities → tables/collections; value objects → columns or embedded; relationships with cardinality; module ownership per table.
   Done when: every Domain Model entity and relationship has a logical counterpart.

2. **Choose storage per data set** (`../../references/data-foundations.md §1`). Default: the primary relational store from the architecture ADR; another store only with a driver → ADR.
   Done when: every data set has a store and, where not the default, an ADR.

3. **Design the physical schema.** Types, nullability, defaults, PK strategy (decide once), FKs, unique/check constraints mirroring invariants (`INV-`), timestamps, data classification per column group.
   Done when: every `INV-` enforceable in the database has a constraint; every table has PK and owner.

4. **Index by access path.** List queries from the API contract and stories (filter, sort, join, cardinality, latency need); create indexes for frequent/critical combinations (equality → range → sort), FK indexes; justify each. `M/L:` verify with query plans on realistic volumes.
   Done when: every index has a query; every critical query has an index or a recorded reason.

5. **Define transactions and consistency.** Transaction boundary per business operation; isolation level and anomalies considered; optimistic vs. pessimistic control; outbox/saga for cross-store writes; idempotency keys for retried operations (`data-foundations.md §4`, `cs-foundations.md §2–3`).
   Done when: every write operation in the API/stories has a row.

6. **Plan migrations.** Tool from the stack; versioned, forward-only in production; expand/contract for zero downtime; batching for backfills; rollback compatibility (app N−1 works with schema N). Irreversible steps → H6.
   Done when: migration strategy written; first migration set drafted in the stack's convention.

7. **Set data lifecycle and protection.** Per data set: classification, retention, deletion/erasure method, encryption at rest/in transit, masking in non-production, backup inclusion (RPO). PII → size class at least M; erasure/export as `REQ-F` if missing (send to `requirements`).
   Done when: every data set has a lifecycle row; security receives the classification.

8. **Caching** only for a measured or clearly predicted need: what, key, TTL, invalidation, consistency tolerance, bound, fail-open behaviour.
   Done when: each cache has all columns or the section says "none yet".

9. **Estimate volumes and growth**; plan partitioning/archival if a table will exceed tens of millions of rows or memory-resident working set within 24 months → `RISK-`/ADR.
   Done when: every large table has an estimate and a plan or a risk.

## Outputs

| Artifact | Template | Location | Consumers |
|---|---|---|---|
| Data Model | `../../templates/data-model.md` | `docs/engineering/data-model.md` | implementation, testing, security, operations |
| ADRs (store choices, PK strategy, consistency) | `../../templates/adr.md` | `docs/engineering/adr/` | everyone |
| Migration files | stack convention | per stack | implementation, delivery-pipeline |

## Validation

- [ ] Every domain entity/relationship mapped; every table has PK, owner, classification.
- [ ] Every enforceable invariant is a constraint.
- [ ] Every index has a justifying query; critical queries covered.
- [ ] Every write operation has transaction/isolation/concurrency/idempotency entries.
- [ ] Migration strategy supports rollback (N−1 compatibility); irreversible steps flagged.
- [ ] Lifecycle table complete; PII handling matches requirements and ASVS level.
- [ ] Caches fully specified or explicitly none.
- [ ] Growth estimates for large tables.

## Stop and ask

- Irreversible migration or deletion, retention change (H6).
- Adding a second store type (cost/ops) when the driver is weak (H10 if paid service).
- Regulated data retention or residency interpretation (H9).

## Handoff

- → `implementation`: schema, migrations, transaction rules, index expectations.
- → `testing`: data fixtures, migration tests, integration test targets.
- → `security`: classification and protection rows for the threat model.
- → `operations`: backup/RPO inputs for the Runbook.
- STATE: Data Model row current; ADR index; size class raised if PII found.

## References

- `../../templates/data-model.md` — load when writing the model.
- `../../references/data-foundations.md` — load for store selection, indexing, isolation, migrations, caching, lifecycle.
- `../../references/cs-foundations.md` — load §2–3 for concurrency and consistency.
- `../../templates/adr.md` — load when a store or consistency decision needs an ADR.
- `../sdlc-orchestrator/references/human-decisions.md` — load for H6/H9 wording.

# Data Foundations — Decision Guide

> Covers: storage model selection, normalization vs. denormalization, indexing by access path, transactions and isolation, concurrency control, migrations, caching, data lifecycle and protection hooks
> Retrieved: 2026-09-04
> Sources: Synthesis of database curricula surveyed in docs/RESEARCH.md §5 (ETH "Data Modelling and Databases", MIT 6.5831, CS2023 DM knowledge area); ISO/IEC 25010:2023 vocabulary; OWASP ASVS 5.0 chapter V14 Data Protection (https://github.com/OWASP/ASVS/tree/v5.0.0/5.0/en)
> Evidence: ACADEMIC, INDUSTRY, RECOMMENDATION

Load when: choosing a store, designing a schema, defining transactions/consistency, planning migrations or caching.

## 1. Storage model selection (RECOMMENDATION)

Default: one relational database per system (S/M). Add another store only for a data set with a driver below; record it in an ADR.

| Data set characteristics | Fits | Notes |
|---|---|---|
| Structured entities with relationships, invariants, ad-hoc queries, transactions | Relational (SQL) | Default. Mature tooling, constraints, joins, ACID |
| Documents with variable shape, read mostly by id, aggregate-per-request | Document store | Model per access pattern; joins are manual |
| Key → value at very high rate, sessions, caches, counters | Key-value / in-memory | Volatile unless persistence configured |
| Full-text or faceted search | Search index (derived data) | Never the source of truth; rebuildable |
| Time-stamped measurements at volume | Time-series store | Retention and downsampling built in |
| Large files/blobs | Object storage | Store metadata in the primary DB |
| Highly connected traversal queries | Graph database | Only when traversal depth is the core query |
| Analytics over history | Warehouse / columnar | Fed by pipeline; not for transactional writes |

## 2. Modeling rules (ACADEMIC/RECOMMENDATION)

- Start from the Domain Model: entities → tables/collections; value objects → columns or embedded documents; relationships → foreign keys or references with declared cardinality.
- Normalize to 3NF for transactional data (one fact in one place); denormalize deliberately for read paths with a documented invalidation/update rule.
- Every table: primary key (surrogate or natural — decide once per system), created/updated timestamps, and ownership by exactly one module.
- Constraints in the database (NOT NULL, unique, foreign key, check) enforce invariants that the application also validates.
- Soft delete vs. hard delete is a data-lifecycle decision (§6), not a per-table whim.

## 3. Indexing by access path (RECOMMENDATION)

1. List the queries (from API contract and stories): filter columns, sort columns, join keys, cardinality, expected rows returned.
2. Create indexes for the filter+sort combinations of frequent or latency-critical queries; composite index column order follows equality → range → sort.
3. Every foreign key used in joins gets an index.
4. Justify each index in the Data Model (query it serves); remove indexes without a query.
5. Watch write amplification: each index slows inserts/updates.
6. Verify with the database's query plan on realistic data volumes before release (L: mandatory; M: for critical paths).

## 4. Transactions, isolation and concurrency (ACADEMIC/RECOMMENDATION)

- Transaction boundary = one business operation that must be atomic; keep it short; no network calls inside.
- Isolation anomalies to consider: dirty read, non-repeatable read, phantom read, lost update, write skew. Default isolation of the chosen database must be recorded; raise it (or use explicit locking) for operations with invariants across rows.
- Concurrency control: optimistic (version column, retry on conflict) for low-contention user edits; pessimistic (row locks) for high-contention counters/inventory; database-side atomic updates where possible.
- Cross-store or cross-service consistency: outbox pattern (write event in the same transaction, publish asynchronously) or saga with compensations; avoid two-phase commit across services.
- Idempotency keys for operations reachable through retries (payments, order creation).

## 5. Migrations (RECOMMENDATION)

- Versioned, ordered, repeatable in every environment; stored in the repository; run by the pipeline.
- Forward-only in production; "down" migrations only for local development.
- Zero-downtime pattern (expand/contract): add new column/table → dual-write or backfill → switch reads → remove old. Each step deployable independently and compatible with the previous application version (needed for rollback).
- Data-changing migrations (backfills) run in batches with progress logging; test on a production-like copy.
- Irreversible operations (drop, truncate, type narrowing, PII deletion) are a **Stop and ask** with a verified backup/restore first.

## 6. Data lifecycle and protection (INDUSTRY — ASVS V14 hooks; RECOMMENDATION)

- Classify data sets: public / internal / confidential / regulated (PII, payment, health). Classification raises the project size class to at least M.
- Per class: retention period, deletion method, backup inclusion, encryption at rest and in transit, access logging, masking in non-production environments.
- Right-to-erasure and export flows are requirements (`REQ-F`) when PII is present.
- Backups: schedule, tested restore, RPO/RTO recorded in the Runbook.

## 7. Caching (RECOMMENDATION)

Cache only after a measured need. Record for each cache: what is cached, key, TTL, invalidation trigger, consistency tolerance, size bound, behaviour on miss/failure (fail open to source). Patterns: cache-aside (default), read-through, write-through, write-behind (rarely). Never cache authorization decisions longer than the session policy allows.

## 8. Volume and growth (RECOMMENDATION)

Estimate rows/day, retention, peak QPS per table; extrapolate 12–24 months. If any table exceeds tens of millions of rows or the working set exceeds memory, plan partitioning/archival now and record it as a `RISK-###` or ADR.

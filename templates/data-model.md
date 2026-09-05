<!--
Purpose: Define how domain data is stored: storage choices, physical schema, indexes justified by access paths, transaction and consistency rules, migration strategy, lifecycle/retention, caching and volumes.
Producer: data-design.
Consumers: implementation, testing, security (data protection), operations (backups).
Update when: schema changes (via migration), new access path, retention/classification changes.
Size: S logical model + schema + indexes + migrations; M/L all sections. Guidance in references/data-foundations.md.
-->
# Data Model — <project>

| Field | Value |
|---|---|
| Version / date | |
| Primary store | e.g. PostgreSQL 16 — ADR-000x |
| Other stores | (each with ADR) |
| Migration tool | from STATE.md › Stack |

## 1. Logical model
From the Domain Model: entities → tables/collections; relationships and cardinalities.

## 2. Storage choices
| Data set | Store | Driver (why this store) | ADR |
|---|---|---|---|

## 3. Physical schema
| Table / collection | Columns (name, type, null, default) | PK | FKs / references | Constraints (unique, check) | Owner module | Classification |
|---|---|---|---|---|---|---|

## 4. Access paths and indexes
| Query (from API/story) | Filter / sort columns | Frequency / latency need | Index (columns, order) | Justification |
|---|---|---|---|---|

## 5. Transactions and consistency
| Operation | Transaction boundary | Isolation / locking | Concurrency control (optimistic / pessimistic) | Cross-store consistency (outbox / saga) | Idempotency key |
|---|---|---|---|---|---|

## 6. Migrations
Strategy (versioned, forward-only, expand/contract) · naming · how run per environment · backfill batching · rollback compatibility rules.

## 7. Data lifecycle and protection
| Data set | Classification | Retention | Deletion / erasure method | Encryption (rest / transit) | Masking in non-prod | Backup (RPO) |
|---|---|---|---|---|---|---|

## 8. Caching
| What | Key | TTL | Invalidation | Consistency tolerance | Size bound | On miss / failure |
|---|---|---|---|---|---|---|

## 9. Volumes and growth
| Table | Rows/day | Retention | 24-month estimate | Peak QPS | Partition / archive plan |
|---|---|---|---|---|---|

## 10. Open questions and risks

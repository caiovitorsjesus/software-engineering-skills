# Asynchronous Messaging Concerns

> Covers: engineering concerns for queues, events and streams — delivery semantics, ordering, idempotent consumers, outbox/inbox, retries and dead letters, schema evolution, observability
> Retrieved: 2026-09-04
> Sources: distributed-systems triggers in references/cs-foundations.md §3; architecture drivers in references/architecture-styles.md §2; AsyncAPI as a contract format is referenced as an industry practice; this system's recommendations
> Evidence: INDUSTRY, RECOMMENDATION

Load when: implementing or reviewing producers, consumers, event handlers or stream processors.

## 1. Delivery semantics
- Assume **at-least-once** delivery from brokers; design consumers to be idempotent. Exactly-once end to end is not available across independent systems; at-most-once only where loss is acceptable (record the decision).
- Message = identity (id), type, version, timestamp (producer clock, informational), correlation/causation ids, payload.

## 2. Idempotent consumers
- Deduplicate by message id (inbox table or cache with TTL longer than the redelivery window) or make the handler naturally idempotent (upsert by natural key, state-machine guard).
- Process and record "handled" in one transaction where the store allows; otherwise handle → record with a tolerable duplicate window.

## 3. Ordering
- Ordering is guaranteed at most per partition/key; choose the partition key as the entity id whose events must be ordered. Do not rely on global ordering.
- Consumers tolerate out-of-order events for different keys; use versions/sequence numbers to detect stale updates.

## 4. Outbox and inbox
- Producer writes the event in the same transaction as the state change (outbox table); a relay publishes and marks sent. Prevents lost or phantom events.
- Consumer inbox for deduplication and auditing (see §2).

## 5. Retries, poison messages, dead letters
- Transient failure → retry with backoff (broker or consumer side); permanent failure (schema, validation) → dead-letter queue with the error and attempt count; alert on DLQ growth; provide a replay tool.
- Bound retries; avoid retry storms (jitter); make handlers time-bounded.

## 6. Schema and contract evolution
- Contract per event type (AsyncAPI or schema registry); additive changes only within a version; new version for breaking changes with a dual-publish or upcaster period; consumers ignore unknown fields.
- Version field in every message; document producer and consumers in the contract.

## 7. Consistency and workflows
- Sagas for multi-step processes across services: explicit steps, compensations, timeouts, and a state record; prefer orchestration when the flow must be observable, choreography when steps are independent.
- Eventual consistency is a product decision: state the acceptable lag in `REQ-N` and show pending states in the UI.

## 8. Observability and operations
- Metrics: publish rate, consumer lag, processing latency, failures, DLQ size; traces propagate correlation ids through headers; logs include message id and type.
- Runbook entries: replay procedure, DLQ handling, consumer scaling, broker capacity limits.

## 9. Testing hooks
- Unit tests for handlers with duplicate and out-of-order inputs; component tests with an embedded/containerized broker; contract tests for event schemas; chaos tests for redelivery (M/L).

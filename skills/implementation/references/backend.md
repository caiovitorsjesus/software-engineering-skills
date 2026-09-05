# Backend Engineering Concerns

> Covers: framework-neutral concerns for services and APIs — layering, boundary validation, transactions, idempotency, resilience patterns, configuration, observability, security hooks
> Retrieved: 2026-09-04
> Sources: NIST SSDF v1.1 PW.5 intent and OWASP ASVS 5.0 chapters V1, V2, V4, V8, V13, V16 (references/security-framework-map.md); Twelve-Factor App (https://12factor.net/); distributed-systems triggers in references/cs-foundations.md; this system's recommendations
> Evidence: STANDARD, INDUSTRY, RECOMMENDATION

Load when: implementing or reviewing a service, API or job story. Apply within the project's framework conventions.

## 1. Layering and dependencies
- Keep a stable direction: interface/adapters (HTTP, messaging, CLI) → application/use cases → domain → infrastructure adapters (DB, external APIs) behind interfaces. Domain code has no framework or I/O dependency.
- One module owns one set of tables (Data Model ownership); cross-module access goes through the owner's interface.
- Dependency injection for adapters; no service locators hidden in domain code.

## 2. Validation and boundaries (ASVS V1, V2)
- Validate and normalize all input at the boundary (schema from the API contract): type, range, length, format, allow-lists; reject early with the error contract.
- Encode/escape on output per sink (HTML, SQL via parameters, shell never with untrusted input, logs).
- Business-rule validation lives in the domain (invariants `INV-`), not in controllers.

## 3. Transactions and idempotency
- One transaction per use case; open late, close early; no external calls inside.
- Idempotency keys for create/charge operations reachable via retries; store the key with the result.
- Outbox for publishing events with the same transaction; consumers idempotent (`async-messaging.md`).
- Optimistic concurrency (version column) for user edits; explicit locking for contended counters.

## 4. Resilience toward dependencies
- Timeouts on every outbound call (shorter than the inbound budget); retries with exponential backoff and jitter only for idempotent calls; circuit breaker for flaky dependencies; bulkheads (separate pools) for critical vs. non-critical dependencies; fallbacks or degraded responses where the REQ allows.
- Bounded queues and connection pools with acquisition timeouts; backpressure over unbounded buffering.
- Graceful shutdown: stop accepting, drain in-flight, close resources (Twelve-Factor IX).

## 5. Configuration and secrets (Twelve-Factor III; ASVS V13)
- Config from environment/secret manager; typed and validated at startup; fail fast on missing config.
- Secure defaults: debug off, verbose errors off, admin endpoints authenticated, CORS explicit.

## 6. Authorization (ASVS V8)
- Enforce on every request at the application layer (not only in the UI or gateway); check ownership/tenant scope on object access; deny by default; log denials.

## 7. Error handling (OWASP Top 10:2025 A10; ASVS V16)
- One error contract (code, message, correlation id); map exceptions at the boundary; never leak stack traces or internal identifiers to clients; log full context server-side without secrets or PII.
- Distinguish client errors (4xx) from server errors (5xx) consistently; retriable vs. non-retriable signalled to clients.

## 8. Observability
- Structured logs with correlation/request id, tenant/user id (pseudonymous), operation name; RED metrics per endpoint; traces across outbound calls and message hops; health and readiness endpoints separate.

## 9. Jobs and scheduling
- Idempotent jobs; distributed lock or single-runner guarantee; checkpoints for long jobs; alert on missed runs.

## 10. Testing hooks
- Unit tests for domain rules; component tests for use cases with in-memory or containerized dependencies; integration tests for adapters against real dependency images; contract tests for the API; abuse-case tests for authn/authz.

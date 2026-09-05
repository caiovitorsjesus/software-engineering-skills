# Computer Science Foundations — Decision Triggers

> Covers: when algorithmic complexity, data-structure choice, concurrency, distributed-systems behaviour, networking, operating-system and programming-language facts change an engineering decision
> Retrieved: 2026-09-04
> Sources: Synthesis of CS curricula surveyed in docs/RESEARCH.md §5 (MIT, Stanford, CMU, Oxford, ETH Zurich, Waterloo; ACM CS2023 knowledge areas AL, AR, DM, FPL, NC, OS, PDC, SDF, SF). No numeric claim here is a benchmark; every threshold is a heuristic to trigger analysis.
> Evidence: ACADEMIC, RECOMMENDATION, INFERENCE

Load when: a design or implementation choice depends on data volume, latency budget, concurrency, network boundaries or consistency. Consult the matching section; skip the rest.

## 1. Algorithms and data structures (AL, SDF)

Trigger analysis when any holds: input size may exceed ~10^5 items; an operation runs inside a hot loop or per request; latency budget is < 100 ms; data grows without bound.

| Need | Reach for | Avoid |
|---|---|---|
| Membership / lookup by key | hash map/set (avg O(1)); sorted structure or B-tree when ordered iteration needed | linear scans of lists |
| Ordered data, range queries | balanced tree, sorted array + binary search, skip list | re-sorting per query |
| Top-k / scheduling | heap / priority queue | full sort per insert |
| FIFO/LIFO | queue / deque / stack | list `pop(0)`-style O(n) removal |
| Prefix search, autocompletion | trie or sorted index | filtering all strings |
| Graph reachability / shortest path | BFS/DFS; Dijkstra (non-negative weights); topological sort for dependencies | ad-hoc recursion without visited set |
| Approximate counting / membership at scale | HyperLogLog, Bloom filter | exact sets in memory |
| Many small allocations in hot path | arrays/structs of primitives, object pools | per-item boxing |

Rules: state the expected N and the complexity of the chosen approach in the design note when the trigger fires; measure before optimizing below O(n log n) → O(n); prefer library implementations over hand-written ones.

## 2. Concurrency (PDC, OS)

Trigger when two or more actors (threads, processes, requests, jobs) can touch the same state.

- Name the shared state and the invariant it must keep; choose one protection: immutability, confinement to one owner, locks (document lock order), atomic operations, or transactional storage.
- Prefer message passing / queues between components over shared memory across components.
- Every blocking call in an async runtime is a defect candidate (event loop starvation).
- Idempotency: any operation that may be retried (network, queue redelivery) must be safe to run twice — use idempotency keys or natural keys.
- Races show up as intermittent test failures; treat a flaky test as a concurrency bug until proven otherwise.
- Deadlock prevention: acquire locks in a global order; hold them briefly; use timeouts.

## 3. Distributed systems (PDC, NC)

Trigger when a call crosses a process or network boundary.

- Assume partial failure: the call may fail, succeed without reply, or arrive late/duplicated. Design timeouts (shorter than the caller's budget), retries with exponential backoff and jitter only for idempotent operations, and circuit breakers for dependencies.
- Consistency choice per data set: strong (single writer/transaction) vs. eventual (replicas, events). An invariant that spans two stores needs a saga/outbox design or must be relaxed — write this down in an ADR.
- Clocks are unreliable across machines: use monotonic clocks for durations, logical ordering (sequence numbers, versions) for causality, and never compare timestamps from different machines for ordering.
- Exactly-once delivery is not available end to end; design for at-least-once + idempotent consumers, or at-most-once where loss is acceptable.
- Backpressure: bounded queues; reject or shed load explicitly rather than growing unbounded.
- Observability is part of the design: correlation ids across hops; structured logs; latency histograms per dependency.

## 4. Networking (NC)

- Every network hop adds latency and a failure mode; count hops on the critical path.
- Chatty interfaces (N+1 calls) are the most common performance defect — batch or shape the API.
- Payload size and compression matter on mobile and public internet; paginate lists.
- TLS everywhere; certificates and DNS are operational dependencies with expiry dates (put them in the runbook).
- Connection pools have limits; pool exhaustion presents as timeouts — size pools and set acquisition timeouts.

## 5. Operating systems and runtime (OS, SF, AR)

- Processes vs. threads vs. async tasks: isolation vs. sharing vs. I/O concurrency; pick per workload (CPU-bound → processes/parallelism; I/O-bound → async or thread pools).
- Memory: watch unbounded caches, large in-memory collections, and per-request allocations; know the runtime's GC behaviour when latency matters.
- File and socket handles are finite; close them deterministically.
- Containers: CPU and memory limits change runtime behaviour (GC, thread pools); test under the limits used in production.
- Startup and shutdown: fast startup and graceful shutdown (drain in-flight work) enable safe deploys and scaling (see Twelve-Factor in `operations-foundations.md`).

## 6. Programming languages and paradigms (FPL)

- Type systems: make illegal states unrepresentable where the language allows (enums/sum types, non-nullable types); validate at boundaries, trust inside.
- Immutability by default reduces concurrency and aliasing bugs; mutate locally and deliberately.
- Pure functions for business rules → trivially testable; side effects at the edges.
- Error handling model of the language (exceptions vs. result types) must be applied consistently; define the error contract at module boundaries.
- Metaprogramming, reflection and dynamic features reduce analysability (maintainability sub-characteristic); use sparingly and document.

## 7. Mathematics and logic (MSF)

- Express invariants and business rules as explicit predicates; they become tests and assertions.
- Model lifecycles as finite state machines (states, events, transitions, guards); reject impossible transitions explicitly.
- Probability for capacity: percentiles (p95/p99), not averages; queueing intuition — utilization near 100 % makes latency explode.
- Floating point is not exact: use decimal/integer types for money and counts.

## 8. Data management pointers (DM)

Relational vs. NoSQL, normalization, indexing, isolation levels, migrations and caching live in `data-foundations.md`.

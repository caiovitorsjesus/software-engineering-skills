# Operations Foundations

> Covers: SLI/SLO/SLA and error budgets; observability signals; DORA software delivery metrics; Twelve-Factor App; SRE incident management roles; blameless postmortems
> Retrieved: 2026-09-04
> Sources: https://sre.google/sre-book/service-level-objectives/, https://sre.google/sre-book/managing-incidents/, https://sre.google/sre-book/postmortem-culture/, https://dora.dev/guides/dora-metrics-four-keys/, https://12factor.net/
> Evidence: INDUSTRY, RECOMMENDATION

Load when: defining SLOs, designing observability, planning deployments, running or reviewing an incident.

## 1. Service levels (INDUSTRY — Google SRE)

- **SLI** — a quantitative measure of some aspect of service (request latency, error rate, throughput, availability, durability).
- **SLO** — a target value or range for an SLI (e.g., "99 % of search requests complete under 100 ms").
- **SLA** — an explicit or implicit contract with users with consequences for missing targets; if there is no consequence, it is an SLO.
- Choose SLIs by system type: user-facing → availability, latency, throughput; storage → latency, availability, durability; big data → throughput, end-to-end latency.
- Use percentiles (p50/p95/p99), not averages. Keep SLOs few. Avoid absolutes (100 %). Start from what users need, not from current performance. Iterate.
- **Error budget** = 1 − SLO over the window; spend it on releases and experiments; when exhausted, prioritize reliability work over features (control loop).

Right-sizing: `S` 1–2 SLOs (availability, p95 latency of the main journey); `M` per user-facing path; `L` per service plus dependency SLOs.

## 2. Observability signals (INDUSTRY/RECOMMENDATION)

| Signal | Minimum practice |
|---|---|
| Logs | structured (JSON), leveled, with correlation/request id, user/tenant id (no secrets, no raw PII), emitted as event streams (Twelve-Factor XI) |
| Metrics | RED per endpoint (rate, errors, duration) or USE per resource (utilization, saturation, errors); business counters for key events |
| Traces | distributed tracing across hops on M/L; propagate context through queues |
| Dashboards | one per service: SLIs vs SLOs, saturation, dependencies, deploy markers |
| Alerts | on symptoms users feel (SLO burn rate, error rate, latency), not on causes; every alert links to a runbook entry; page only for user-impacting conditions |

## 3. DORA metrics (INDUSTRY — current dora.dev guide)

| Metric | Definition | Improved by |
|---|---|---|
| Deployment frequency | how often changes reach production | small batches, automated pipeline |
| Change lead time | commit → running in production | trunk-based flow, fast CI, small PRs |
| Change fail rate | share of deployments needing immediate intervention (rollback, hotfix) | tests, canaries, feature flags |
| Failed deployment recovery time | time to recover from a failed deployment (replaces the older MTTR wording) | rollback automation, observability |
| Deployment rework rate | share of deployments that are unplanned fixes after an incident | root-cause fixes, postmortem actions |

Speed and stability are not trade-offs; high performers do well on all. Thresholds are not asserted here; measure trends against your own baseline.

## 4. Twelve-Factor App (INDUSTRY — Wiggins/Heroku 2011)

I codebase · II dependencies declared and isolated · III config in the environment · IV backing services as attached resources · V build, release, run separated · VI stateless processes · VII port binding · VIII concurrency via process model · IX disposability (fast startup, graceful shutdown) · X dev/prod parity · XI logs as event streams · XII admin processes as one-off tasks. Use as a deployability checklist in delivery-pipeline; deviations are recorded with a reason.

## 5. Incident management (INDUSTRY — Google SRE)

- **Declare** when: multiple teams needed; user-visible impact; not resolved after about an hour of analysis.
- **Roles** (one person may hold several; say which): Incident Commander (state, delegation, blockers); Operations Lead (the only role changing systems); Communications Lead (periodic updates, keeps the record accurate); Planning Lead (bugs filed, logistics, handoffs).
- **Live incident state document** — single shared record of timeline, current hypothesis, actions, owners; becomes the postmortem input.
- **Handoff** is explicit and acknowledged before the outgoing commander leaves.
- Anti-patterns: fixating on debugging instead of mitigation; uncoordinated changes; no communication cadence.
- Practice: mitigate first (rollback, flag off, scale, failover), diagnose second.

## 6. Postmortems (INDUSTRY — Google SRE)

- **Blameless**: assume good intent; analyze systems and process.
- **Triggers**: user-visible downtime or degradation beyond threshold; data loss; on-call manual intervention (rollback, rerouting); resolution time beyond threshold; monitoring failure (incident found by humans); stakeholder request.
- **Contents**: summary; impact; timeline; detection; root cause(s) and trigger; resolution; what went well/poorly/where we got lucky; action items with owners and priority; lessons.
- **Process**: draft collaboratively; senior review for completeness and depth; share widely; track action items to closure.

## 7. Runbook minimum (RECOMMENDATION)

Service overview and owners · SLIs/SLOs/error budget · dashboards and alert list with response steps · routine operations (deploy, rollback, rotate secrets, scale) · known failure modes → mitigations · escalation path · backup/restore with RPO/RTO and last restore test date · certificate/DNS/quota expiries · capacity limits.

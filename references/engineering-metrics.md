# Engineering Metrics

> Covers: what to measure at each lifecycle stage, DORA delivery metrics, quality and maintainability indicators, and metric anti-patterns
> Retrieved: 2026-09-04
> Sources: https://dora.dev/guides/dora-metrics-four-keys/ ; ISO/IEC 25010:2023 vocabulary via references/quality-model.md ; https://sre.google/sre-book/service-level-objectives/
> Evidence: INDUSTRY, RECOMMENDATION

Load when: choosing what to measure, reviewing project health, or writing the metrics section of a Runbook or Backlog.

## 1. Principles (RECOMMENDATION)

- Measure outcomes users feel (SLIs) and flow (DORA) before internal proxies.
- Every metric has an owner, a source of truth, a review cadence and a decision it informs. A metric that informs no decision is removed.
- Trends over absolutes; compare against your own baseline.
- Never use metrics to rank individuals (Goodhart effect; erodes blameless culture).

## 2. Metrics by stage

| Stage | Measure | Decision it informs |
|---|---|---|
| discovery | success criteria defined with numbers; assumptions count vs. validated | go/no-go; what to validate first |
| requirements | % FR with AC; % NFR with numeric target; open questions age | readiness for design |
| planning | throughput (stories done/iteration); cycle time; % stories meeting DoR at start | forecast; refinement quality |
| design | drivers addressed by ADRs / total; unmitigated High/Critical threats | Design→Construction gate |
| construction | change lead time (DORA); PR size; coverage on changed code; static-analysis findings trend | batch size, review load |
| verification | pass rate per level; flaky test count; escaped defects per release | exit criteria; suite health |
| deployment | deployment frequency; change fail rate; failed deployment recovery time; deployment rework rate (DORA) | pipeline and rollback investment |
| operations | SLO attainment; error budget burn; alert volume and actionability; incident count by severity | reliability vs. feature work |
| evolution | tech debt items and "interest" trend; dependency age; time to patch High/Critical vulnerabilities | maintenance priority |

## 3. DORA five (INDUSTRY)

Deployment frequency · Change lead time · Change fail rate · Failed deployment recovery time · Deployment rework rate. Definitions in `operations-foundations.md §3`. Capture points: pipeline events (deploy start/end, rollback), VCS (commit time), incident records (linked deployment).

## 4. Quality indicators (RECOMMENDATION; map to ISO/IEC 25010:2023)

| Characteristic | Indicator |
|---|---|
| Functional suitability | escaped defects per release; AC pass rate |
| Performance efficiency | p95/p99 latency, throughput, resource per request |
| Reliability | availability, MTBF, restore test success |
| Security | open findings by severity and age; % dependencies with known vulnerabilities; ASVS level attained |
| Maintainability | change lead time; complexity hotspots; duplication; coverage on changed code; module coupling |
| Flexibility | time to provision an environment; scale-out test result |
| Interaction capability | task success rate; accessibility violations |

## 5. Anti-patterns

Lines of code, commit counts, velocity comparisons across teams, 100 % coverage mandates, alert counts as productivity, story points as capacity contracts.

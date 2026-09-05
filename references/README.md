# References — Shared Foundations

Single source of truth for standards summaries, quality vocabulary, computer-science decision triggers and cross-cutting rules. Skills point here; nothing here points to skills. Each file carries a header (Covers / Retrieved / Sources / Evidence) and never states unverified content as fact.

| File | Load when… |
|---|---|
| [lifecycle-map.md](lifecycle-map.md) | you need the canonical stage key, artifact name, ID prefix, or the mapping to ISO/IEC/IEEE 12207:2017 and SWEBOK v4 |
| [quality-model.md](quality-model.md) | writing NFRs, quality attribute scenarios, test coverage by quality, or SLIs (ISO/IEC 25010:2023) |
| [requirements-quality.md](requirements-quality.md) | writing or reviewing requirements and acceptance criteria (ISO/IEC/IEEE 29148:2018 criteria, smells, prioritization, change control) |
| [architecture-styles.md](architecture-styles.md) | choosing a style, writing the Architecture Overview or an ADR (drivers/costs, C4, ISO/IEC/IEEE 42010:2022, ADR statuses) |
| [cs-foundations.md](cs-foundations.md) | a decision depends on data volume, latency, concurrency, network boundaries, consistency or runtime behaviour |
| [data-foundations.md](data-foundations.md) | choosing a store, designing schema/indexes, transactions, migrations, caching, retention |
| [security-framework-map.md](security-framework-map.md) | deciding which security activity is due, choosing an ASVS level, citing SSDF/SAMM/ASVS/Top 10 ids |
| [testing-foundations.md](testing-foundations.md) | writing the Test Strategy, deciding which tests a story needs, fixing flaky suites (ISO/IEC/IEEE 29119 concepts) |
| [operations-foundations.md](operations-foundations.md) | SLOs, observability, DORA, Twelve-Factor, incident roles, postmortems |
| [scrum-vocabulary.md](scrum-vocabulary.md) | iteration planning, DoR/DoD, mapping to a team that runs Scrum (Scrum Guide 2020) |
| [engineering-metrics.md](engineering-metrics.md) | choosing what to measure per stage; DORA and quality indicators; anti-patterns |
| [stack-adaptation.md](stack-adaptation.md) | starting in a repository; before proposing tools, commands or libraries |
| [agent-working-rules.md](agent-working-rules.md) | about to change code or assert facts about code, libraries, standards |

## Standards and editions cited (re-verify periodically)

| Standard / source | Edition used | Retrieved | Primary access status |
|---|---|---|---|
| SWEBOK Guide | v4.0 (2024) | 2026-09-04 | read |
| ISO/IEC/IEEE 12207 | 2017 | 2026-09-04 | iso.org 403; secondary summary |
| ISO/IEC 25010 | 2023 | 2026-09-04 | iso.org 403; three secondary sources cross-checked |
| ISO/IEC/IEEE 29148 | 2018 | 2026-09-04 | secondary summary (partial) |
| ISO/IEC/IEEE 42010 | 2022 | 2026-09-04 | secondary summary |
| ISO/IEC/IEEE 29119 | parts 1–5, 2021–2024 | 2026-09-04 | secondary summary |
| NIST SP 800-218 SSDF | v1.1 (2022) | 2026-09-04 | PDF read |
| OWASP SAMM | v2.0 | 2026-09-04 | read |
| OWASP ASVS | 5.0.0 (2025-05-30) | 2026-09-04 | read |
| OWASP Top 10 | 2025 | 2026-09-04 | read |
| Scrum Guide | 2020 | 2026-09-04 | read |
| ACM/IEEE-CS/AAAI CS2023 | 2024 endorsement | 2026-09-04 | KA list read |
| DORA metrics guide | current (five metrics) | 2026-09-04 | read |
| Google SRE Book | online edition | 2026-09-04 | read |
| Twelve-Factor App | 2011 | 2026-09-04 | read |

Evidence labels: `STANDARD` `ACADEMIC` `INDUSTRY` `RECOMMENDATION` `INFERENCE` `DECISION` — definitions in `docs/RESEARCH.md §0`.

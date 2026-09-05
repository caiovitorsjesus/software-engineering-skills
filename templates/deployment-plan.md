<!--
Purpose: Define how software moves from commit to production safely: environments, pipeline stages, artifact integrity, configuration and secrets, deployment strategy, rollback, migration compatibility, release checklist and handover.
Producer: delivery-pipeline.
Consumers: operations, incident-response (rollback procedure), maintenance, implementation (CI expectations).
Update when: environments, pipeline stages, deployment strategy or release process change.
Size: S one page (environments, stages, rollback, checklist); M/L all sections. Maps to SSDF PO.3, PO.5, PS.1–PS.3, PW.6, PW.9 (references/security-framework-map.md) and Twelve-Factor.
-->
# Deployment Plan — <project>

| Field | Value |
|---|---|
| Version / date | |
| CI/CD platform | |
| Deploy target | |
| Deployment strategy | recreate / rolling / blue-green / canary; feature flags |

## 1. Environments and promotion
| Environment | Purpose | Data | Access | Promotion rule |
|---|---|---|---|---|
| local | | | | |
| ci / ephemeral | | | | |
| staging | production parity | anonymized | | after CI green |
| production | | real | least privilege | after release checklist |

## 2. Version control and change flow (SSDF PS.1)
Branching model · protected branches · review requirement · commit convention · signed commits (M/L).

## 3. Pipeline stages
| Stage | Runs | Tools | Gate (fail → stop) | Time budget |
|---|---|---|---|---|
| build | compile, dependency install (locked) | | | |
| static checks | lint, format, type check, SAST, secret scan | | | |
| tests | unit, component, integration, contract (per Test Strategy) | | | |
| package | artifact/container build, SBOM (M/L), signature/checksum (PS.2) | | | |
| deploy staging | migrations then app | | smoke tests | |
| verify | e2e, performance (scheduled), DAST | | | |
| deploy production | strategy above | | health checks, SLO watch | |

## 4. Artifact integrity and retention (PS.2, PS.3)
Versioning scheme · immutable artifacts · checksums/signatures · retention period · provenance.

## 5. Configuration and secrets (Twelve-Factor III; PO.5)
Config via environment/secret manager · no secrets in VCS · rotation procedure · per-environment differences listed.

## 6. Build hardening (PW.6) and secure defaults (PW.9)
Compiler/interpreter flags · minimal base images · non-root runtime · default-deny configuration · dependency pinning.

## 7. Deployment strategy and rollback
Steps · health checks · rollback command/procedure and time target · data-migration compatibility (expand/contract; app N and N-1 compatible with schema) · feature flag plan.

## 7b. Client distribution (mobile / desktop apps, if any)
Signing keys and their custody · build flavours per environment · store/marketplace submission and review lead time · staged rollout percentages · minimum supported client version and forced-update policy · server-side kill switches for risky features · crash/performance monitoring per release.

## 8. Release checklist
- [ ] All gates green (tests, security scans, contract checks)
- [ ] Migrations reviewed for rollback compatibility; backup verified
- [ ] Secrets present in target environment; no secrets in artifacts
- [ ] Secure defaults confirmed (PW.9); debug/admin endpoints disabled
- [ ] Observability: dashboards, alerts, deploy marker in place
- [ ] Runbook updated; on-call informed
- [ ] Stop and ask: production deploy approved by <owner>

## 9. Handover and training
Documentation delivered · user/admin training notes · support channel · known limitations.

## 10. Metrics capture (DORA)
Where deployment frequency, change lead time, change fail rate, failed deployment recovery time and rework rate are recorded.

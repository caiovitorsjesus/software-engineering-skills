---
name: operations
description: >-
  Make a deployed system operable: SLIs and SLOs with error budgets, structured logs, metrics, traces,
  dashboards, symptom-based alerts, runbook procedures, backup/restore and disaster recovery, capacity,
  on-call readiness. Use before or after a first release, when alerts are noisy or missing, when
  reliability targets are undefined, or as a hardening baseline. Not for live incidents
  (incident-response) or pipeline design (delivery-pipeline).
license: MIT
compatibility: Designed for Claude Code and other Agent Skills runtimes. Reads and writes Markdown under docs/engineering/ and observability configuration in the target repository.
metadata:
  se-layer: discipline
  se-stage: operations
  se-version: "0.1.0"
---

# Operations

## Purpose

Produce and maintain the Runbook and the observability configuration that let anyone operate the system: objectives users feel (SLOs), signals to see them (logs, metrics, traces, dashboards), alerts that page only on user-impacting symptoms, procedures for routine and failure situations, and tested recovery.

## Use when

- A release is imminent and no Runbook exists (gate `construction-to-release` requires it).
- After release: SLIs report, alerts route, on-call readiness must be confirmed.
- Alerts are noisy, unactionable or missing; incidents are detected by users.
- Hardening: baseline measurements before security/performance/reliability work.
- Periodic review: capacity, cost, backup restore test, expiries.

## Do not use when

- An incident is in progress: `incident-response`.
- Designing CI/CD or deployment strategy: `delivery-pipeline`.
- Defining reliability *requirements*: `requirements` (this skill turns REQ-N into SLOs).

## Inputs

| Input | Required | Source |
|---|---|---|
| Deployment Plan (environments, deploy/rollback) | when present; otherwise derive deploy/rollback from existing scripts and pipeline "as found" and record `ASM-` (typical for incident and hardening entries) | `docs/engineering/deployment-plan.md` |
| Architecture Overview (containers, dependencies, cross-cutting observability decisions) | when present; else containers as found from infra/config | `docs/engineering/architecture.md` |
| Requirements Spec (REQ-N reliability/performance/security) | yes | `docs/engineering/requirements.md` |
| Threat Model (detection needs) | no | `docs/engineering/threat-model.md` |
| Data Model (backup/RPO inputs) | no | `docs/engineering/data-model.md` |
| Existing dashboards/alerts | no | repository / platform |

## Procedure

1. **Derive SLIs from REQ-N**: availability, latency percentiles, error rate for user-facing paths; durability for storage; freshness/lag for async. Define measurement (where, window, percentile).
   Done when: each user-facing critical journey has ≥ 1 SLI with a measurement definition.

2. **Set SLOs and error budgets** (`../../references/operations-foundations.md §1`): target equal to or slightly relaxed from REQ-N; window (e.g., 30 days); error budget policy (what happens when burned: freeze risky releases, prioritize reliability). `S:` 1–2 SLOs.
   Done when: SLO table complete with policy; targets confirmed against REQ-N (H3 if cost-driving).

3. **Instrument**: structured logs with correlation ids and no secrets/PII; RED metrics per endpoint / USE per resource; traces across hops for M/L; business counters for key events. Use the stack's libraries.
   Done when: the signals emit in the pre-production environment (or locally for S without staging); correlation id visible end to end for one journey.

4. **Build dashboards**: one per service — SLIs vs SLOs, saturation, dependency health, deploy markers.
   Done when: a dashboard shows every SLO and the last deploy.

5. **Define alerts on symptoms**: SLO burn rate, error rate, latency, saturation nearing limits, DLQ growth, certificate/quota expiry; severity (page vs. ticket); each alert links to a Runbook entry; test alert routing.
   Done when: every alert has a response entry and reached the on-call channel in a test.

6. **Write routine operations**: deploy, rollback, rotate secrets/certificates, scale, run migrations/backfills, replay messages — with commands and verification steps.
   Done when: each routine op has a procedure and a verification.

7. **Document known failure modes**: symptom → likely cause → mitigation → permanent fix link; seed from the threat model, architecture risks and incident history.
   Done when: every dependency has at least one failure-mode row.

8. **Backup, restore, DR**: per data set schedule, RPO, RTO, restore procedure, last restore test; DR scenario and steps for `M/L`. Perform or schedule a restore test.
   Done when: RPO/RTO recorded and a restore test date exists.

9. **Capacity, limits, expiries, cost**: pools, quotas, rate limits, storage growth, certificate/DNS/licence expiries with dates, cost watch items.
   Done when: every expiry has a date and an owner; capacity headroom stated.

10. **Security operations** (SSDF RV.1): vulnerability intake path, dependency alert handling, auth anomaly alerts, access review cadence.
    Done when: intake and alerts exist; cadence set.

11. **On-call readiness and metrics**: access verified, alert routing verified, runbook reviewed after last incident; DORA and SLO metrics capture points confirmed (`../../references/engineering-metrics.md`).
    Done when: readiness checklist ticked; STATE stage = operations.

## Outputs

| Artifact | Template | Location | Consumers |
|---|---|---|---|
| Runbook | `../../templates/runbook.md` | `docs/engineering/runbook.md` | incident-response, maintenance, on-call |
| Observability configuration (dashboards, alerts, instrumentation) | stack/platform convention | repository / platform | all |

## Validation

- [ ] Every critical journey has SLI + SLO + error budget policy.
- [ ] Logs structured with correlation ids and no secrets/PII; metrics and (M/L) traces emit.
- [ ] Dashboard per service shows SLOs and deploy markers.
- [ ] Every alert is symptom-based, has severity, links to a runbook entry, and routing was tested.
- [ ] Routine ops and failure modes documented with verification steps.
- [ ] Backup/RPO/RTO recorded; restore tested or scheduled.
- [ ] Expiries dated with owners; capacity headroom stated.
- [ ] Vulnerability intake and dependency monitoring active.
- [ ] Gate `release-to-operations` items answerable.

## Stop and ask

- SLO target implying cost (multi-region, higher tiers) (H3/H10).
- Paging policy that affects people (who is on call): ask the user to confirm roles (STATE › Roles).
- Backup/DR scope for regulated data (H9) when retention or residency is unclear.

## Handoff

- → `incident-response`: alerts, runbook entries, escalation path.
- → `maintenance`: capacity, expiry and debt items; failure modes needing permanent fixes.
- → `security`: detection gaps for top threats; vulnerability intake path.
- STATE: Runbook row current; stage operations; next action (first review date).

## References

- `../../templates/runbook.md` — load when writing the runbook.
- `../../references/operations-foundations.md` — load §1–2, §7 for SLOs, observability, runbook minimum.
- `../../references/engineering-metrics.md` — load in step 11.
- `../../references/quality-model.md` — load to map SLIs to reliability/performance/security characteristics.

---
name: incident-response
description: >-
  Handle a production incident from declaration to closure: roles, live incident record, mitigation
  before diagnosis (rollback, flag, scale, failover), communication cadence, diagnosis, resolution,
  blameless postmortem with root cause and tracked corrective actions. Use when production is down,
  degraded, losing data, breached, or a user-facing alert fires. Not for bug fixing without user impact
  (maintenance) or defining monitoring (operations).
license: MIT
compatibility: Designed for Claude Code and other Agent Skills runtimes. Reads and writes Markdown under docs/engineering/incidents/ in the target repository; may run diagnostics and, with approval, rollback procedures.
metadata:
  se-layer: discipline
  se-stage: operations
  se-version: "0.1.0"
---

# Incident Response

## Purpose

Restore service fast and safely, keep everyone informed, then convert the incident into learning: a complete live record, a blameless postmortem with systemic root cause, and corrective actions that land in the Backlog, Tech Debt Register, Runbook and alerts.

## Use when

- An alert, user report or monitoring gap indicates user-visible failure, degradation, data loss or a security breach in production.
- A deployment causes errors and a rollback decision is needed.
- An incident was handled informally and needs a postmortem.

## Do not use when

- The issue has no user impact and no urgency: `maintenance` (bug fix).
- The task is designing alerts/SLOs: `operations`.
- Root cause is a vulnerability needing remediation planning after stabilization: `security` (G) — invoked from step 8.

## Inputs

| Input | Required | Source |
|---|---|---|
| Live symptoms (alert text, error messages, user reports, metrics) | yes | user / platform |
| Runbook (alerts → responses, rollback, escalation) | no (proceed without; note the gap) | `docs/engineering/runbook.md` |
| Deployment Plan (rollback procedure, recent deploys) | no | `docs/engineering/deployment-plan.md` |
| Architecture Overview (dependencies) | no | `docs/engineering/architecture.md` |

## Procedure

1. **Declare and record.** Criteria (`../../references/operations-foundations.md §5`): user-visible impact, multiple teams needed, or unresolved after ~1 hour. Create `docs/engineering/incidents/YYYY-MM-DD-slug.md` from the template with `INC-YYYYMMDD-#`, severity per Runbook, start time.
   Done when: the record exists with severity and impact summary.

2. **Assign roles.** Incident Commander, Operations Lead (only role changing systems), Communications Lead, Planning Lead; one person or agent may hold several — write which. Agent as Operations Lead executes only pre-authorized runbook procedures; other production changes → H7.
   Done when: roles listed in the record.

3. **Mitigate first.** Prefer the fastest reversible action: roll back the last deploy, disable the feature flag, scale out, fail over, block the abusive source, shed load. Confirm impact reduction on dashboards before diagnosing. If a **breach or intrusion is suspected**: preserve evidence before changing anything that destroys it (export logs, snapshot affected hosts/volumes, record indicators), contain (revoke credentials, isolate) rather than wipe, and involve `security` (G) and H9 immediately.
   Done when: user impact is reduced or a mitigation attempt and its result are recorded; for suspected breaches, evidence preservation is logged before containment.

4. **Communicate on a cadence.** Update stakeholders at a fixed interval (e.g., every 30 minutes) with impact, current hypothesis, next update time; external/customer/regulator communication → H12.
   Done when: the communications log has entries at the cadence.

5. **Diagnose.** Timeline of changes (deploys, config, dependencies), correlation ids from failing requests, logs/metrics/traces around the onset; form hypotheses and test them; use `diagnosing-bugs` if available. Keep the record current (hypothesis, actions, results).
   Done when: a confirmed cause (or the best-supported hypothesis) is recorded with evidence.

6. **Resolve and verify.** Apply the fix (code, config, data repair); verify SLIs recover; remove temporary mitigations when safe; declare resolved with time.
   Done when: SLIs back within SLO and no new errors for the agreed window.

7. **Postmortem (blameless), within the agreed window.** Summary, impact (users, requests, data, SLO/error budget), timeline with detect/mitigate/resolve durations, detection analysis (what should have caught it), root cause(s) and trigger, resolution, what went well/poorly/lucky, action items (prevent, detect, mitigate, process) with owners and links, lessons. Review with a senior engineer; share.
   Done when: template sections complete; every action item has owner, type, link and due date.

8. **Close the loop.** Action items → Backlog stories (`agile-delivery`) or `DEBT-###`; Runbook failure-mode and alert updates → `operations`; if security-caused → `security` (G) for RV.3 root cause and disclosure decision; risks → Risk Register. Evaluate gate `incident-closure`.
   Done when: every action item is linked; STATE situation returns to the previous workflow.

## Outputs

| Artifact | Template | Location | Consumers |
|---|---|---|---|
| Incident record + Postmortem | `../../templates/incident-postmortem.md` | `docs/engineering/incidents/YYYY-MM-DD-slug.md` | maintenance, security, operations, leadership |
| Corrective actions | `../../templates/backlog.md`, `../../templates/tech-debt-register.md` | `docs/engineering/backlog.md`, `docs/engineering/tech-debt.md` | agile-delivery, maintenance |
| Runbook updates | `../../templates/runbook.md` | `docs/engineering/runbook.md` | operations |

## Validation

- [ ] Record has id, severity, roles, timeline, mitigation, resolution.
- [ ] Mitigation attempted before deep diagnosis; production changes pre-authorized or approved (H7).
- [ ] Communication log at cadence; external comms approved (H12).
- [ ] Postmortem blameless; root cause systemic (not "human error"); detection gap analyzed.
- [ ] Every action item has owner, type, link, due date.
- [ ] Runbook/alerts updated; security handoff done if applicable.
- [ ] Gate `incident-closure` items answerable.

## Stop and ask

- Executing rollback, config change, failover or data repair in production without a pre-authorized runbook procedure (H7).
- External communication (H12).
- Data repair that may lose or alter records (H6).
- Suspected breach requiring notification decisions (H9).

## Handoff

- → `agile-delivery` / `maintenance`: corrective actions.
- → `operations`: alert and runbook changes; detection improvements.
- → `security` (G): vulnerability root cause, fix, disclosure.
- STATE: incident logged; situation restored; next action.

## References

- `../../templates/incident-postmortem.md` — load in step 1 and step 7.
- `../../references/operations-foundations.md` — load §5–6 for roles, declaration criteria, postmortem triggers/contents.
- `../../references/agent-working-rules.md` — load §5–6 for honest reporting and diagnostic hand-off.
- `../sdlc-orchestrator/references/human-decisions.md` — load for H6/H7/H9/H12 wording.

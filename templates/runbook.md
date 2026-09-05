<!--
Purpose: Give whoever operates the system what they need at 3 a.m.: SLOs, dashboards, alerts with responses, routine operations, known failure modes, escalation, backup/restore, capacity and expiries.
Producer: operations.
Consumers: incident-response, maintenance, on-call engineers.
Update when: an alert is added/changed, an incident reveals a new failure mode, a procedure changes, after each restore test.
Size: S one page (SLOs, alerts, deploy/rollback, backup); M/L all sections. Concepts per references/operations-foundations.md.
-->
# Runbook — <service / system>

| Field | Value |
|---|---|
| Owners / on-call | |
| Repos / pipelines | |
| Dashboards | |
| Dependencies (upstream / downstream) | |

## 1. Service overview
What it does, users, critical journeys, architecture link.

## 2. SLIs, SLOs and error budget
| SLI | Measurement (percentile / window) | SLO | Error budget policy | Source REQ-N |
|---|---|---|---|---|

## 3. Alerts and responses
| Alert | Condition (symptom) | Severity (page / ticket) | First response steps | Escalate to |
|---|---|---|---|---|

## 4. Routine operations
| Operation | Procedure / command | Frequency | Verification |
|---|---|---|---|
| Deploy | see Deployment Plan §7 | | |
| Rollback | | | |
| Rotate secrets / certificates | | | |
| Scale up / down | | | |
| Run migration / backfill | | | |

## 5. Known failure modes
| Symptom | Likely cause | Mitigation | Permanent fix (DEBT/STORY) |
|---|---|---|---|

## 6. Escalation and communication
Path · contacts · communication cadence · status page.

## 7. Backup, restore and disaster recovery
| Data set | Backup schedule | RPO | RTO | Restore procedure | Last restore test |
|---|---|---|---|---|---|

## 8. Capacity, limits and expiries
Quotas · connection pool sizes · rate limits · certificate/DNS/domain/licence expiries · cost watch items.

## 9. Security operations (RV.1)
Vulnerability intake channel · dependency alert handling · auth-failure/anomaly alerts · access review cadence.

## 10. On-call readiness checklist
- [ ] Access to dashboards, logs, deploy/rollback verified
- [ ] Alerts route to the right people
- [ ] Restore tested within the last <n> months
- [ ] Runbook reviewed after the last incident

# Workflow: production-incident

Live failure → stabilized → learned → prevented. Validation scenario D.

## Entry conditions
- Situation `incident`: alert, user report or observation of user-visible failure, degradation, data loss or breach in production.
- The orchestrator suspends the current workflow (records it in STATE) and runs this one; it resumes the previous workflow at exit.

## Sequence

| # | Skill | Entry point / mode | Produces | Gate after |
|---|---|---|---|---|
| 1 | `incident-response` | steps 1–4: declare, roles, mitigate first, communicate | live incident record; mitigation applied or attempted | — (H7 for production changes not pre-authorized; H12 for external comms) |
| 2 | `incident-response` | steps 5–6: diagnose, resolve, verify | cause with evidence; SLIs recovered | — |
| 3 | `incident-response` | step 7: blameless postmortem | postmortem with action items | — |
| 4 | `maintenance` | intake corrective actions; fixes with regression tests | DEBT/story items; fixes | `story-done` per fix |
| 5 | `security` | G — only if the cause is a vulnerability or breach | RV.3 root cause, remediation, disclosure decision (H5/H9/H12) | — |
| 6 | `operations` | runbook failure mode, alert and detection updates; restore test if data was involved | Runbook update | `incident-closure` |

If the incident reveals a missing Runbook or observability, `operations` runs in full after closure (hardening workflow may follow).

## Size-class variations
- **S**: roles held by one person/agent (stated); postmortem may be one page; still blameless and with action items.
- **M/L**: communications cadence formalized; senior review of the postmortem; action items tracked to closure in the Backlog with due dates; DORA failed-deployment-recovery-time recorded.

## Exit criteria
Gate `incident-closure` passed; STATE situation restored to the prior workflow with corrective actions scheduled.

## Typical human stops
H7 rollback/config/failover execution (unless pre-authorized in the Runbook) · H12 external communication · H6 data repair · H9 breach notification decisions · H5 vulnerability risk acceptance.

## Dead-end checks
- No Runbook → proceed with generic mitigations (rollback last deploy, flag off); record the gap as an action item.
- Cause unknown after stabilization → postmortem still written with "best-supported hypothesis" and a detection/diagnosis action item; never left open silently.
- Corrective actions must land in the Backlog or Tech Debt Register — an action item without a link fails the gate.

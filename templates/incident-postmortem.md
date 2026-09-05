<!--
Purpose: One record per incident that serves first as the live incident document (roles, timeline, hypotheses, actions) and then as the blameless postmortem with root cause and tracked action items.
Producer: incident-response.
Consumers: maintenance (corrective actions), security (if vulnerability), operations (runbook/alert updates), leadership.
Update when: continuously during the incident; finalized within the agreed postmortem window; action items updated until closed.
Size: live section short and current; postmortem one to three pages. File: docs/engineering/incidents/YYYY-MM-DD-slug.md. Practice per references/operations-foundations.md §5–6.
-->
# INC-YYYYMMDD-# — <title>

| Field | Value |
|---|---|
| Status | active / mitigated / resolved / postmortem done |
| Severity | S1 / S2 / S3 (define in Runbook) |
| Declared at / by | |
| Roles | Incident Commander: … · Operations Lead: … · Communications Lead: … · Planning Lead: … (one person may hold several) |
| User impact summary | |
| Related deploy / change | |

## Live incident record
| Time (UTC) | Event / observation / action | Who | Result |
|---|---|---|---|

**Current hypothesis:** …
**Mitigation in progress:** rollback / flag off / scale / failover / other
**Next update at:** …

## Communications log
| Time | Audience | Message |
|---|---|---|

---

# Postmortem (blameless)

## 1. Summary
What happened, for how long, who was affected.

## 2. Impact
Users affected · requests failed · data affected · SLO/error budget consumed · business impact.

## 3. Timeline
Detection → declaration → mitigation → resolution, with durations (time to detect, time to mitigate, time to resolve).

## 4. Detection
How it was noticed (alert / user report / manual) · what should have detected it.

## 5. Root cause(s) and trigger
Causal chain to the systemic cause(s); the trigger that made it manifest now.

## 6. Resolution
What fixed it; why it worked.

## 7. What went well / what went poorly / where we got lucky

## 8. Action items
| # | Action | Type (prevent / detect / mitigate / process) | Owner | Priority | Link (STORY / DEBT / THR) | Due | Status |
|---|---|---|---|---|---|---|---|

## 9. Lessons
Generalizable learning; runbook and alert changes made.

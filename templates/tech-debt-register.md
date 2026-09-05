<!--
Purpose: Make technical debt visible and prioritizable: what it is, where, why it exists, what it costs to keep (interest), what it costs to fix, and the plan.
Producer: maintenance (owner); legacy-modernization seeds it; any skill appends.
Consumers: agile-delivery (prioritization), architecture, implementation, maintenance.
Update when: debt is found (review, incident, flaky test, workaround), paid down, or its interest changes.
Size: one table plus a short policy section.
-->
# Tech Debt Register — <project>

Policy: every deliberate shortcut is registered when taken · interest = recurring cost (time, incidents, blocked changes) · items with Critical security impact are prioritized above features · review each iteration.

| ID | Location (module / file / infra) | Description | Cause (deliberate / accidental / outdated / environmental) | Impact (ISO/IEC 25010:2023 sub-characteristic affected) | Interest (recurring cost) | Effort to fix | Priority | Plan / STORY | Status | Raised by / date |
|---|---|---|---|---|---|---|---|---|---|---|
| DEBT-001 | | | | | | | | | open | |

## Dependency health
| Dependency | Current | Latest | Age / EOL | Known vulnerabilities | Upgrade plan |
|---|---|---|---|---|---|

## Review log
| Date | Reviewed by | Items paid / added |
|---|---|---|

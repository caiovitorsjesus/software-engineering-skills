<!--
Purpose: Record one architecturally significant decision with its context, options, rationale and consequences so it can be understood and revisited later.
Producer: architecture, data-design, legacy-modernization (any skill may propose).
Consumers: implementation, security, delivery-pipeline, maintenance, future reviewers.
Update when: never edit an accepted decision; add a new ADR that supersedes it and update both statuses.
Size: one page. Format after Nygard (2011) / MADR (references/architecture-styles.md §6). File: docs/engineering/adr/NNNN-kebab-title.md
-->
# ADR-NNNN — <Title in decision form, e.g. "Use PostgreSQL as the primary store">

| Field | Value |
|---|---|
| Status | proposed (default when written by the agent) / accepted (by the technical approver, normally at the design-to-construction gate) / deprecated / superseded by ADR-NNNN |
| Date | YYYY-MM-DD |
| Deciders | |
| Links | REQ-…, RISK-…, THR-…, related ADRs |

## Context
The situation and forces: requirements, constraints, quality scenarios, team/stack realities.

## Decision drivers
- driver 1 (REQ-N-…)
- driver 2 (CON-…)

## Options considered
| Option | Summary | Pros | Cons / costs |
|---|---|---|---|
| A (chosen) | | | |
| B | | | |
| C | | | |

## Decision
What was decided, stated plainly. If it introduces distribution, a new technology, or replaces a stack element: name the driver that justifies it.

## Consequences
**Positive:** …
**Negative / accepted costs:** …
**Follow-ups:** tasks, risks (`RISK-###`), things to measure.

# Stage Gates

> Covers: the checklists evaluated at each stage transition; ids match `skills/registry.yaml › gates`
> Retrieved: 2026-09-04
> Sources: This system's design (docs/ARCHITECTURE.md §7.7); security items follow NIST SSDF v1.1 practice intent and OWASP SAMM v2 verification practices as mapped in references/security-framework-map.md §6; quality items use ISO/IEC 25010:2023 vocabulary
> Evidence: DECISION, STANDARD

Every item is answered yes/no with a pointer to evidence (artifact section). A gate passes when all **required** items are yes; `S:` `M:` `L:` marks items required only from that size class up. Record the result in `STATE.md › Gates passed`.

Scope rule (walking skeleton): design gates are evaluated for the **scope of the next release or increment**, not the whole product. Data Model, API Contract and Test Strategy may cover the first increment and be extended per epic through `add-feature` deltas; what must be complete up front is the style/store/hosting/authn decisions and the threat model of the boundaries that exist. Postmortem proportionality: see `incident-closure`.

## discovery-to-requirements
- [ ] Discovery Brief exists with problem statement, stakeholders, objectives with measurable success criteria, scope in/out.
- [ ] Constraints (`CON-`) and assumptions (`ASM-`) listed; each assumption has a validation plan.
- [ ] Feasibility table filled for technical, operational, economic, schedule, legal; verdict is `go` (or a human approved `pivot`).
- [ ] Risk Register seeded with at least the top risks (`RISK-`).
- [ ] Security risk profile present: data classes, exposure, likelihood × impact (security › A).
- [ ] Size class proposed with driver; regulated data → at least M.
- [ ] Human approval of go/no-go recorded in STATE › Open questions (closed).

## requirements-to-design
- [ ] Every `REQ-F` has ≥ 1 acceptance criterion; no requirement smells (`references/requirements-quality.md §2`).
- [ ] Every applicable ISO/IEC 25010:2023 characteristic has a `REQ-N` with number and method, or an explicit "n/a — reason".
- [ ] Security requirements section filled: ASVS level, authn/authz model, data protection, logging (SSDF PO.1).
- [ ] Constraints, assumptions, dependencies and interfaces listed.
- [ ] Traceability table seeded with every REQ id.
- [ ] Open questions have owners; none blocks the first design decisions.
- [ ] If scope changed versus the Discovery Brief: change logged and human approval recorded.
- [ ] `M:` Prioritization method recorded and priorities assigned.

## design-to-construction
- [ ] Architecture Overview: every driver scenario addressed by an ADR/component or deferred with a `RISK-`.
- [ ] ADR exists for: style, primary data store, hosting/runtime, authn/authz approach, and any distributed style or stack replacement (with drivers and costs).
- [ ] C4 context and container views present (text list acceptable).
- [ ] Threat Model: trust boundaries reviewed; every High/Critical `THR-` mitigated or formally accepted by a human (security › C).
- [ ] Data Model: schema, indexes justified by access paths, transaction/consistency rules, migration strategy, data classification and retention.
- [ ] API Contract exists for every external or cross-container interface, with auth, errors and examples per operation (skip only when there is no consumer other than the same deployable).
- [ ] Test Strategy drafted: levels, coverage per characteristic, exit criteria.
- [ ] Deployment Plan skeleton: environments and CI stages defined (pipeline can run on an empty project).
- [ ] Stack detected and recorded; no tool invented that the repository does not have.
- [ ] ADR set reviewed and **accepted by the technical approver** (one batched decision; statuses moved from `proposed` to `accepted`).
- [ ] Risk Register reviewed: architecture trade-offs and deferred drivers added as `RISK-`; ratings current.
- [ ] `M:` Domain Model present and every `REQ-F` maps to named concepts.
- [ ] `L:` Component views for hot spots; capacity estimates; DR targets (RPO/RTO) stated.

## story-done
(per backlog item; equals the Backlog's Definition of Done)
- [ ] All acceptance criteria demonstrably met (tests or recorded inspection).
- [ ] Tests at agreed levels written and passing; regression test for any bug fixed; no quarantined test introduced.
- [ ] Secure-coding checklist items for touched areas done; dependency and secret scans clean or triaged (security › D).
- [ ] Code reviewed.
- [ ] Docs updated where affected (API contract, runbook, ADR).
- [ ] Traceability row: STORY, component, TEST filled; status `implemented` or `verified`.
- [ ] Deployed to the agreed environment or feature-flagged; flag state recorded.

## construction-to-release
- [ ] All stories in the release meet `story-done`.
- [ ] Test Strategy exit criteria met for every level in scope; performance `REQ-N` rows verified; e2e critical journeys green.
- [ ] Security tests executed (SAST, dependency scan; `M:` DAST, abuse cases); zero open High/Critical findings or documented acceptance (security › E).
- [ ] Release checklist in the Deployment Plan complete: secure defaults, secrets present and not in artifacts, artifact integrity, migrations rollback-compatible, backup verified (security › F).
- [ ] Runbook exists with SLOs, alerts, deploy/rollback, backup/restore.
- [ ] Risk Register reviewed: release risks with triggers and owners; accepted risks re-confirmed.
- [ ] Traceability statuses moved to `verified` for released REQs.
- [ ] Human approval for production deployment recorded.

## release-to-operations
- [ ] Deployment succeeded; health checks and smoke tests green; deploy marker visible on dashboards.
- [ ] SLIs reporting; alerts routed; on-call informed.
- [ ] Vulnerability intake path and dependency monitoring active (SSDF RV.1).
- [ ] Handover done: docs delivered, training notes, support channel.
- [ ] Traceability statuses `released`; STATE stage = operations; DORA metrics capture points recorded.

## incident-closure
- [ ] Incident record complete: roles, timeline, impact, mitigation, resolution.
- [ ] Postmortem written (blameless) with root cause(s), trigger, detection analysis — **required** when any SRE trigger applies (user-visible downtime/degradation beyond threshold, data loss, manual on-call intervention, resolution over threshold, monitoring failure, stakeholder request; `references/operations-foundations.md §6`); otherwise a short record with cause and one action item suffices and this item is marked "n/a — no trigger".
- [ ] Action items created with owners and links (`STORY`/`DEBT`/`THR`); prevention and detection items both considered.
- [ ] Runbook and alerts updated for the failure mode.
- [ ] If a vulnerability: root cause analysis and fix recorded (SSDF RV.3); disclosure decision made by a human.
- [ ] STATE updated; situation returns to the previous workflow.

## modernization-plan-approved
- [ ] Legacy Assessment: inventory, recovered as-is architecture, quality findings, risks, debt summary.
- [ ] Options matrix filled with cost, risk and fit to drivers; recommendation stated.
- [ ] Characterization/regression test approach defined before any change.
- [ ] Target architecture and incremental migration strategy with rollback criteria (ADR).
- [ ] Data migration approach with backup/restore and loss-risk assessment.
- [ ] Human decision on the option recorded (Stop and ask).

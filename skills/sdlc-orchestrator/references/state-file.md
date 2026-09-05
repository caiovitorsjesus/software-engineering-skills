# STATE.md Semantics

> Covers: meaning of each field in docs/engineering/STATE.md, artifact status values, the freshness rule, and repair steps when STATE is missing or inconsistent
> Retrieved: 2026-09-04
> Sources: This system's design (docs/ARCHITECTURE.md §7.8; templates/project-state.md)
> Evidence: DECISION

## 1. Fields

| Field | Meaning | Written by |
|---|---|---|
| Situation | one of new-product / add-feature / incident / legacy / hardening | orchestrator |
| Size class | S / M / L with the driver row from `rightsizing.md §1` | orchestrator; raised by any skill |
| Current stage | stage key from `references/lifecycle-map.md §1` | orchestrator after a gate passes |
| Workflow | path of the workflow file in use | orchestrator |
| Suspended workflow / resume point | the workflow and step interrupted by an incident (or empty); the orchestrator resumes it after `incident-closure` | orchestrator |
| Docs root | where artifacts live (default `docs/engineering/`) | orchestrator; user may override |
| Next action | one step, one skill, one artifact | orchestrator or the last skill |
| Stack | languages, frameworks, versions, commands, stores, CI, deploy target, unknowns | orchestrator via stack-adaptation; any skill corrects |
| Roles and owners | who decides product, technical approvals, security | orchestrator from user input |
| Artifact index | path, status, inputs, last updated per artifact | every producing skill |
| Decisions | ADR index | architecture, data-design, legacy-modernization |
| Gates passed | gate id, date, evidence | orchestrator |
| Open questions | Stop-and-ask items with options, recommendation, status | any skill |
| Assumptions in force | `ASM-###` with validation plan | any skill |
| Log | date, skill, change | every skill on handoff |

## 2. Artifact status values

| Status | Meaning |
|---|---|
| `missing` | file absent |
| `draft` | file exists; its skill's Validation checklist not yet fully satisfied |
| `current` | Validation satisfied and no input changed since |
| `stale` | an input artifact (per "Inputs it depends on") changed after this artifact's last update |
| `embedded in <artifact>` | S-class right-sizing keeps this artifact as a section of another (e.g., Risk Register inside the Discovery Brief; Threat Model inside the Architecture Overview); freshness follows the host artifact |

## 3. Freshness rule

An artifact is `stale` when an artifact in its "Inputs it depends on" column had a **substantive change** after this artifact's `Last updated`. Substantive changes are: a new entry in the Requirements Spec change log; a new, deprecated or superseded ADR; a schema change in the Data Model; a contract change in the API Contract; a new High/Critical threat; a new container in the Architecture Overview. **Not substantive**: traceability rows, status columns, STATE log lines, backlog ordering, test-plan rows appended for a story. Producing skills therefore record two dates in the artifact index: `Last updated` (any edit) and `Last substantive change` (the one freshness reads).

Stale artifacts are re-run by their producing skill *only for the affected sections* (the skill reads the input's change log to scope the update). Source code is an input for Test Strategy (per-feature sections), Runbook and Tech Debt Register; use the VCS to detect changes since the artifact's date.

Recurring skills (`recurring: true` in the registry) are not subject to skip-by-freshness; they run when their entry condition holds.

## 4. Repair procedure (STATE missing or inconsistent) — also the mid-project entry path

1. Create STATE from the template if missing.
2. Scan `docs root` for known artifact file names (`lifecycle-map.md §3`); set status `draft` for each found, `missing` otherwise. For an **existing system with no engineering docs**, do not schedule `discovery`: `requirements` (delta mode) bootstraps a Requirements Spec whose product-context section is derived from README, code structure and the user's request, with `ASM-` for anything inferred; `architecture` records an "as found" overview only when a story crosses an unknown boundary.
2b. When existing docs **contradict the repository** (e.g., an Architecture Overview names containers that do not exist), the repository is the source of truth for *what is*, the docs for *what was intended*: mark the artifact `stale`, log the discrepancy as an open question with the two readings, and let the producing skill reconcile (usually a superseding ADR). Never silently edit the old artifact to match the code.
3. Scan `adr/` and fill the Decisions index from each ADR's header.
4. Infer `Current stage` as the latest stage whose gate could plausibly pass; record it as an assumption (`ASM-`) until the gate is actually evaluated.
5. Fill Stack via `stack-adaptation.md §1`.
6. Leave Open questions empty except for what the scan could not determine (docs root, owners).

## 5. Conventions

- Dates ISO `YYYY-MM-DD`; times UTC.
- Paths relative to the target repository root.
- Keep STATE under two screens; it is an index, not a document. Link out.
- Log: keep the most recent 10 entries; delete older ones (VCS history preserves them).
- Any skill listed under an artifact's `updates` in the registry may create that artifact from its template if it does not exist yet (e.g., `security` creating the Tech Debt Register before `maintenance` has run).

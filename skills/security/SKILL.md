---
name: security
description: >-
  Apply security engineering where due: risk profile, security requirements and ASVS level,
  threat model with mitigations, secure-coding review and dependency checks, security testing, release
  hardening, vulnerability triage and root cause. Use at every gate, when a new data class, integration
  or trust boundary appears, on a vulnerability report, or before a release. Not for general
  architecture or testing work; it supplies their security inputs
license: MIT
compatibility: Designed for Claude Code and other Agent Skills runtimes. Reads and writes Markdown under docs/engineering/ in the target repository; may run the project's scanners.
metadata:
  se-layer: discipline
  se-stage: transversal
  se-version: "0.1.0"
---

# Security

## Purpose

Make security a property of every stage rather than a phase: produce the risk profile, security requirements, threat model, code-level checks, security tests, release hardening evidence and vulnerability handling that the gates require, mapped to NIST SSDF v1.1, OWASP SAMM v2, ASVS 5.0 and Top 10:2025.

## Use when

Pick the entry point the gate or event calls for:

| Entry | When | Gate |
|---|---|---|
| A — Risk profile | Discovery Brief drafted | discovery-to-requirements |
| B — Security requirements | Requirements Spec drafted | requirements-to-design |
| C — Threat model | Architecture container view exists; new boundary or data flow | design-to-construction |
| D — Secure-coding review | a story touches input, auth, data, secrets, dependencies | story-done |
| E — Security testing | Test Strategy defined; before release | construction-to-release |
| F — Release hardening | release candidate ready | construction-to-release |
| G — Vulnerability handling | scanner alert, report, incident with security cause | incident-closure / ongoing |

## Do not use when

- Designing the system structure itself: `architecture` (this skill reviews it).
- Writing the general Test Strategy: `testing` (this skill supplies the security level and abuse cases).
- Handling a live outage that is not security-related: `incident-response`.

## Inputs

| Input | Required | Source |
|---|---|---|
| Discovery Brief (data classes, users, exposure) | A | `docs/engineering/discovery-brief.md` |
| Requirements Spec | B, C | `docs/engineering/requirements.md` |
| Architecture Overview (C4 container view, authn/authz ADR) | C | `docs/engineering/architecture.md` |
| API Contract, Data Model | C, D | `docs/engineering/` |
| Source code and dependency manifests | D, E, F, G | repository |
| Scanner outputs, vulnerability report, incident record | G | pipeline / user |

## Procedure

**A — Risk profile** (SAMM Threat Assessment stream A, level 1–2)
1. Classify data (public / internal / confidential / regulated), exposure (internet / partner / internal), user types, attacker interest, business impact of breach; likelihood × impact summary.
   Done when: the profile is written into the Discovery Brief §8/§9 and Risk Register; size class raised for regulated data.

**B — Security requirements** (SSDF PO.1)
2. Choose the ASVS level (`../../references/security-framework-map.md §3`); derive REQs for authentication and sessions, authorization and tenant isolation, data protection (encryption, retention, erasure), logging/audit, secrets, dependency policy, compliance obligations. Write them with `requirements` into §5 of the spec.
   Done when: ASVS level recorded; each area has ≥ 1 REQ with an AC or measurable target.

**C — Threat model** (SSDF PW.1, PW.2; four questions)
3. Scope from the container view: assets, actors, trust boundaries, entry points. Enumerate threats per boundary using the prompts in `references/threat-modeling.md` (STRIDE-style categories and OWASP Top 10:2025 rows); rate likelihood/impact; assign `THR-###`.
4. Map mitigations to ADRs/components/REQs with ASVS references; High/Critical without mitigation → H5. Hand abuse cases to `testing`. Review the design against the requirements (PW.2) and record findings.
   Done when: template §1–§5 filled; no unaccepted High/Critical; abuse cases listed as TEST candidates.

**D — Secure-coding review** (SSDF PW.5, PW.7)
5. For touched areas run `references/secure-coding-checklist.md`; run SAST, dependency and secret scanners available in the stack; triage findings (fix now / DEBT / accept with reason). No scanner in the stack: `S:` the manual checklist suffices and a `DEBT-` item to add a dependency scanner is registered; `M/L:` `delivery-pipeline` adds dependency and secret scanning before the next release (blocking at `construction-to-release`).
   Done when: checklist recorded in the story; scans clean or every finding triaged (or the no-scanner fallback recorded).

**E — Security testing** (SSDF PW.8)
6. Ensure the Test Strategy's security level includes: SAST and dependency scan in CI; DAST for M/L web/API; abuse-case tests for authn/authz, input handling, business logic (from THR rows); results tied to `TEST-###`.
   Done when: security level rows exist and pass, or failures are triaged.

**F — Release hardening** (SSDF PW.9, PS.2, PW.6)
7. Verify secure defaults (debug off, admin paths protected, CORS/CSP explicit), secrets only in the secret store, artifact integrity (checksums/signatures), build hardening flags, security logging and alerting present (Top 10 A09).
   Done when: the Deployment Plan release checklist security items are ticked with evidence.

**G — Vulnerability handling** (SSDF RV.1–RV.3)
8. Intake (scanner, report, incident) → confirm → rate (severity, exploitability, exposure) → remediate by policy (Critical/High first) → root cause and systemic fix → record in Tech Debt Register or Backlog; disclosure decision → H5/H12.
   Done when: each vulnerability has status, owner, fix or acceptance, and a root-cause note.

## Outputs

| Artifact | Template | Location | Consumers |
|---|---|---|---|
| Threat Model | `../../templates/threat-model.md` | `docs/engineering/threat-model.md` (S may embed in Architecture Overview) | architecture, implementation, testing, delivery-pipeline, operations |
| Security requirements section | `../../templates/requirements-spec.md §5` | `docs/engineering/requirements.md` | all |
| Checklist results, findings | story / `../../templates/tech-debt-register.md` | backlog, `docs/engineering/tech-debt.md` | implementation, maintenance |
| Risk Register entries | `../../templates/risk-register.md` | `docs/engineering/risk-register.md` | orchestrator |

## Validation

- [ ] A: data classes, exposure, impact recorded; size class consistent.
- [ ] B: ASVS level chosen; authn, authz, data protection, logging, secrets, dependencies each have REQs.
- [ ] C: every trust boundary reviewed; every Top 10:2025 category considered; every High/Critical mitigated or formally accepted; abuse cases handed to testing.
- [ ] D: checklist recorded; scans clean or triaged; no secrets in code.
- [ ] E: security test level present and executed.
- [ ] F: release checklist security items evidenced.
- [ ] G: every vulnerability has severity, owner, status, root cause.

## Stop and ask

- Accepting or deferring a High/Critical threat or vulnerability (H5).
- Regulatory interpretation: consent, residency, breach notification (H9).
- External disclosure or customer communication about a vulnerability (H12).
- A requested feature conflicts with a security requirement (H8).

## Handoff

- → `requirements` (B), `architecture` (C findings, ADRs for mitigations), `implementation` (D items), `testing` (abuse cases, security level), `delivery-pipeline` (F items, scanners), `operations` (alerts, intake path), `maintenance` (patch priorities), `incident-response` (if exploitation suspected).
- STATE: Threat Model row; risks; open questions for H5/H9.

## References

- `references/threat-modeling.md` — load for entry C (method, prompts, rating).
- `references/secure-coding-checklist.md` — load for entries D and F.
- `../../references/security-framework-map.md` — load for SSDF/SAMM/ASVS/Top 10 ids and the level choice.
- `../../templates/threat-model.md` — load when writing the threat model.
- `../sdlc-orchestrator/references/human-decisions.md` — load for H5/H9/H12 wording.

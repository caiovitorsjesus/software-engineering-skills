# Security Framework Map

> Covers: NIST SP 800-218 SSDF v1.1 (19 practices); OWASP SAMM v2.0 (5 functions × 3 practices); OWASP ASVS 5.0.0 (17 chapters, 3 levels); OWASP Top 10:2025; Threat Modeling Manifesto — mapped to the skills and entry points of this system
> Retrieved: 2026-09-04
> Sources: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf, https://csrc.nist.gov/Projects/ssdf, https://owaspsamm.org/model/, https://github.com/OWASP/ASVS/tree/v5.0.0/5.0/en, https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/en/0x03-What-is-the-ASVS.md, https://owasp.org/Top10/2025/, https://www.threatmodelingmanifesto.org/
> Evidence: STANDARD, INDUSTRY, DECISION

Load when: deciding which security activity is due at a stage, choosing an ASVS level, or citing a practice id in an artifact.

## 1. SSDF v1.1 practices → where this system satisfies them (STANDARD ids; DECISION mapping)

| SSDF | Practice | Skill · entry point | Artifact |
|---|---|---|---|
| PO.1 | Define Security Requirements for Software Development | requirements (security requirements section); security › B | Requirements Spec |
| PO.2 | Implement Roles and Responsibilities | sdlc-orchestrator (STATE roles/owners) | STATE.md |
| PO.3 | Implement Supporting Toolchains | delivery-pipeline (scanners, SBOM, signing) | Deployment Plan |
| PO.4 | Define and Use Criteria for Software Security Checks | sdlc-orchestrator gates (security items) | gates.md |
| PO.5 | Implement and Maintain Secure Environments for Software Development | delivery-pipeline (environments, secrets, access) | Deployment Plan |
| PS.1 | Protect All Forms of Code from Unauthorized Access and Tampering | delivery-pipeline (VCS protection, reviews) | Deployment Plan |
| PS.2 | Provide a Mechanism for Verifying Software Release Integrity | delivery-pipeline (artifact signing/checksums) | Deployment Plan |
| PS.3 | Archive and Protect Each Software Release | delivery-pipeline (artifact retention) | Deployment Plan |
| PW.1 | Design Software to Meet Security Requirements and Mitigate Security Risks | security › C threat model; architecture | Threat Model, ADRs |
| PW.2 | Review the Software Design to Verify Compliance with Security Requirements and Risk Information | security › C (design review step) | Threat Model |
| PW.4 | Reuse Existing, Well-Secured Software When Feasible Instead of Duplicating Functionality | architecture, implementation (dependency choice rules) | ADRs |
| PW.5 | Create Source Code by Adhering to Secure Coding Practices | implementation; security › D checklist | code, checklist results |
| PW.6 | Configure the Compilation, Interpreter, and Build Processes to Improve Executable Security | delivery-pipeline (build hardening flags, reproducible builds) | Deployment Plan |
| PW.7 | Review and/or Analyze Human-Readable Code to Identify Vulnerabilities and Verify Compliance with Security Requirements | security › D; code review (SAST in pipeline) | findings |
| PW.8 | Test Executable Code to Identify Vulnerabilities and Verify Compliance with Security Requirements | security › E; testing (security test level) | Test Strategy |
| PW.9 | Configure Software to Have Secure Settings by Default | security › F release checklist; delivery-pipeline | Deployment Plan |
| RV.1 | Identify and Confirm Vulnerabilities on an Ongoing Basis | security › G; operations (alerts, dependency monitoring) | Runbook |
| RV.2 | Assess, Prioritize, and Remediate Vulnerabilities | security › G; maintenance (patch priority) | Tech Debt Register / Backlog |
| RV.3 | Analyze Vulnerabilities to Identify Their Root Causes | security › G; incident-response postmortem | Incident Postmortem |

SP 800-218A (generative AI and dual-use foundation models) augments SSDF for AI model development — out of scope here; pointer only.

## 2. OWASP SAMM v2.0 (STANDARD structure) → skills

| Business function | Practices | Skill(s) |
|---|---|---|
| Governance | Strategy & Metrics; Policy & Compliance; Education & Guidance | sdlc-orchestrator (gates, STATE), engineering-metrics |
| Design | Threat Assessment; Security Requirements; Secure Architecture | security › A, B, C; requirements; architecture |
| Implementation | Secure Build; Secure Deployment; Defect Management | delivery-pipeline; maintenance |
| Verification | Architecture Assessment; Requirements-driven Testing; Security Testing | security › C (review), E; testing |
| Operations | Incident Management; Environment Management; Operational Management | incident-response; delivery-pipeline; operations |

Threat Assessment streams: A *Application Risk Profile* (L1 basic likelihood/impact → L2 inventory → L3 periodic review); B *Threat Modeling* (L1 best-effort with existing diagrams and simple checklists → L2 standardized → L3 continuous/automated). This system targets L1 for S, L2 for M/L.

## 3. OWASP ASVS 5.0.0 (STANDARD)

Levels: **L1** ≈ 20 % of requirements — first-layer defenses against common attacks (minimum for any internet-facing app); **L2** — adds ≈ 50 % more (≈ 70 % cumulative) — less common attacks and more complex protections; **L3** — remaining ≈ 30 % — defense in depth for highest assurance.

Level selection (DECISION, aligned with D-20 size classes): S → L1; M → L2; L → L2 minimum, L3 for regulated or high-value data and for payout/payment paths. Record the level as `REQ-N` under Security.

Chapters: V1 Encoding and Sanitization · V2 Validation and Business Logic · V3 Web Frontend Security · V4 API and Web Service · V5 File Handling · V6 Authentication · V7 Session Management · V8 Authorization · V9 Self-contained Tokens · V10 OAuth and OIDC · V11 Cryptography · V12 Secure Communication · V13 Configuration · V14 Data Protection · V15 Secure Coding and Architecture · V16 Security Logging and Error Handling · V17 WebRTC.

Declared uses: architecture guidance; secure-coding reference; automated test design; training; procurement; risk-based compliance.

## 4. OWASP Top 10:2025 (STANDARD list) → threat-model prompts

A01 Broken Access Control · A02 Security Misconfiguration · A03 Software Supply Chain Failures · A04 Cryptographic Failures · A05 Injection · A06 Insecure Design · A07 Authentication Failures · A08 Software or Data Integrity Failures · A09 Security Logging and Alerting Failures · A10 Mishandling of Exceptional Conditions.

Use as a checklist row set in the Threat Model ("which of these applies to this component and how is it mitigated?").

## 5. Threat Modeling Manifesto (INDUSTRY)

Four questions: What are we working on? What can go wrong? What are we going to do about it? Did we do a good enough job? Values: finding and fixing design issues over checkbox compliance; people and collaboration over process and tools; a journey of understanding over a security snapshot; doing threat modeling over talking about it; continuous refinement over a single delivery. Anti-patterns: hero threat modeler; admiration for the problem; tendency to over-focus; perfect representation.

## 6. Security activities by stage (DECISION — enforced by gates)

| Gate | Required security output |
|---|---|
| discovery → requirements | risk profile: data classes, exposure, likelihood/impact (security › A) |
| requirements → design | security requirements incl. ASVS level, authn/z model, data protection (security › B) |
| design → construction | threat model with mitigations mapped to ADRs/REQs; no unmitigated High/Critical without recorded acceptance (security › C) |
| story done | secure-coding checklist items relevant to the story; dependency scan clean or triaged (security › D) |
| construction → release | security tests executed; release checklist: secure defaults, secrets, integrity, logging (security › E, F) |
| release → operations | vulnerability intake path defined; alerting on auth failures/anomalies (security › G) |
| incident closure | if the incident was a vulnerability: root cause, fix, disclosure decision recorded (RV.3) |

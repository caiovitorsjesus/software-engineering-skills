# Threat Modeling Method

> Covers: the procedure behind security entry point C — scoping from C4 views, threat enumeration prompts (STRIDE-style categories and OWASP Top 10:2025), rating, mitigation mapping, review questions
> Retrieved: 2026-09-04
> Sources: https://www.threatmodelingmanifesto.org/ (four questions, values, anti-patterns); https://owasp.org/Top10/2025/ ; OWASP SAMM v2.0 Threat Assessment stream B (https://owaspsamm.org/model/design/threat-assessment/); NIST SSDF v1.1 PW.1/PW.2 (references/security-framework-map.md). STRIDE is cited as widely used industry practice; category names are used as prompts, not as a standard.
> Evidence: INDUSTRY, STANDARD, RECOMMENDATION

## 1. Frame (Threat Modeling Manifesto)

Answer in order: **What are we working on? What can go wrong? What are we going to do about it? Did we do a good enough job?** Value finding and fixing design issues over checkbox compliance; do the modeling rather than talk about it; refine continuously. Avoid: a single hero modeler, admiring the problem, over-focusing on one area, seeking a perfect diagram.

## 2. Scope — what are we working on

From the Architecture Overview: list containers, external systems, users/roles, data stores, message channels. Draw or list **trust boundaries** (internet ↔ edge, edge ↔ services, services ↔ data, admin ↔ user, tenant ↔ tenant, third party ↔ system). List **assets**: data classes (from data-design), credentials/keys, availability of critical journeys, integrity of records, reputation/compliance. List **entry points**: every operation in the API contract, message consumers, file uploads, admin interfaces, build pipeline.

`S:` one container view, one table of threats. `M/L:` per container, plus dynamic diagrams for the critical flows (login, payment, data export).

## 3. Enumerate — what can go wrong

For each boundary and entry point, ask the category prompts and write concrete threats (`THR-###`, component, category, description):

| Category prompt | Ask |
|---|---|
| Spoofing | Can an actor pretend to be a user, service or device here? How is identity proven (ASVS V6, V9, V10)? |
| Tampering | Can data in transit/at rest/in the build be altered (ASVS V12, V14; SSDF PS.1–PS.2)? |
| Repudiation | Can an actor deny an action? Is there an audit trail (ASVS V16)? |
| Information disclosure | What leaks via responses, errors, logs, caches, backups, side channels (ASVS V14, V16)? |
| Denial of service | What exhausts CPU, memory, connections, quotas, money (rate limits, payload bounds)? |
| Elevation of privilege | Can a user reach another tenant's data or admin functions (ASVS V8)? |

Then walk **OWASP Top 10:2025** as applicability rows: A01 Broken Access Control · A02 Security Misconfiguration · A03 Software Supply Chain Failures · A04 Cryptographic Failures · A05 Injection · A06 Insecure Design · A07 Authentication Failures · A08 Software or Data Integrity Failures · A09 Security Logging and Alerting Failures · A10 Mishandling of Exceptional Conditions. Each: applies (→ THR) / not applicable (reason).

Add domain abuse cases: business-logic misuse (coupon reuse, race on balance, workflow skipping), mass assignment, IDOR on every id in the contract, file handling (ASVS V5), webhooks/callbacks (SSRF, replay).

## 4. Rate

Likelihood (exposure × ease × attacker interest): Low / Medium / High. Impact (data class × blast radius × recoverability): Low / Medium / High. Rating: High×High → Critical; High×Medium or Medium×High → High; otherwise Medium/Low. Consistency matters more than precision.

## 5. Mitigate — what are we going to do about it

For every THR: control (prevent / detect / respond), where it lives (ADR, component, REQ id), ASVS reference, status (planned / implemented / verified), owner. Prefer platform and framework controls over custom code (SSDF PW.4). Mitigation categories: authn strength; authz checks at the object level; input validation and output encoding; parameterized queries; encryption and key management; rate limiting and quotas; integrity (signing, checksums, provenance); logging and alerting for detection; secure defaults; isolation (network, tenant, process).

Unmitigated High/Critical → Stop and ask H5. Record acceptances with residual risk, approver, date, revisit trigger.

## 6. Review — did we do a good enough job

- Every boundary and entry point has at least one considered threat or an explicit "none identified".
- Every Top 10 row answered.
- Every High/Critical mitigated or accepted by a human.
- Abuse cases handed to `testing` as `TEST-###` candidates.
- Detection: for the top threats, an alert or log query exists (→ operations).
- Design review against security requirements (SSDF PW.2) recorded: which REQs are satisfied by which controls; gaps sent back to `architecture`/`requirements`.
- Review date set (M/L: each release with architectural change; at least yearly).

## 7. Output format

Use `templates/threat-model.md`. `S:` the threats and mitigations tables may live inside the Architecture Overview §10 with the same columns; move to a file when the second container appears or regulated data is found.

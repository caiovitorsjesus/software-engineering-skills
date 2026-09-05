# Secure Coding and Release Hardening Checklist

> Covers: language-neutral checks for security entry points D (story-level review) and F (release hardening), organized by OWASP ASVS 5.0 chapter, with NIST SSDF v1.1 practice ids
> Retrieved: 2026-09-04
> Sources: https://github.com/OWASP/ASVS/tree/v5.0.0/5.0/en (chapter names V1–V17); https://owasp.org/Top10/2025/ ; https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf (PW.5, PW.6, PW.7, PW.9, PS.1–PS.3). Item wording is this system's summary of common controls, not quotations of ASVS requirements.
> Evidence: STANDARD, RECOMMENDATION

Use: tick only items relevant to the touched areas; record the ticked list in the story (D) or the Deployment Plan release checklist (F). Anything unticked that applies becomes a finding → fix, `DEBT-###`, or accepted risk (H5 for High/Critical).

## D — Story-level review (SSDF PW.5, PW.7)

**Input handling (ASVS V1 Encoding and Sanitization, V2 Validation and Business Logic, V5 File Handling)**
- [ ] All external input validated against the contract schema (type, length, range, format, allow-list) at the boundary.
- [ ] Output encoded per sink (HTML, URL, JSON, shell never with untrusted input); templating auto-escape on.
- [ ] Database access via parameterized queries/ORM; no string-built queries.
- [ ] Business rules enforced server-side (limits, state transitions, ownership); race conditions on balances/inventory guarded (transactions, locks, idempotency keys).
- [ ] File uploads: type/size limits, content validation, stored outside web root or in object storage, no path traversal, malware scan where required.
- [ ] Deserialization of untrusted data avoided or restricted to safe formats.

**Authentication, sessions, tokens (V6, V7, V9, V10)**
- [ ] New endpoints require authentication unless explicitly public (documented).
- [ ] Passwords hashed with a current adaptive algorithm via the platform library; credential stuffing/brute force mitigated (rate limit, lockout policy per REQ).
- [ ] Sessions/tokens: short-lived, rotated on privilege change, invalidated on logout; secure/HttpOnly/SameSite cookies; token signature and audience validated; no tokens in URLs or logs.
- [ ] OAuth/OIDC flows use the platform library with state/nonce/PKCE as applicable.

**Authorization (V8)**
- [ ] Every object access checks ownership/tenant/role at the application layer (no reliance on UI or obscurity); deny by default.
- [ ] Admin/privileged operations separated and audited.
- [ ] IDs in the contract checked against the caller's scope (IDOR).

**Cryptography and communication (V11, V12)**
- [ ] Only platform/library cryptography; no custom algorithms; current algorithms and key sizes; random from CSPRNG.
- [ ] Keys and secrets from the secret store; rotation possible; never committed (secret scan clean).
- [ ] TLS for all transport; certificate validation on; internal traffic encrypted where the threat model requires.

**Configuration (V13) and supply chain (Top 10 A03; SSDF PW.4)**
- [ ] New dependency checked: licence, maintenance, known vulnerabilities, pinned version, lockfile updated; minimal permissions/features enabled.
- [ ] No debug flags, default credentials, or sample configs left on.

**Data protection (V14)**
- [ ] Sensitive fields classified; excluded from logs, error messages, analytics; masked in non-production; encrypted at rest where classification requires.
- [ ] Retention/erasure behaviour implemented per Data Model lifecycle.

**Logging and error handling (V16; Top 10 A09, A10)**
- [ ] Security-relevant events logged (auth success/failure, authz denial, admin actions, input validation failures at rate) with correlation id, no secrets/PII.
- [ ] Errors mapped to the error contract; no stack traces or internal details to clients; exceptional paths tested (timeouts, dependency failures).

**Frontend / API specifics (V3, V4)**
- [ ] CSP/frame/CSRF protections in place for browser clients; CORS explicit.
- [ ] API: content-type enforced, request size limits, rate limits, consistent auth per operation as in the contract.

## F — Release hardening (SSDF PW.6, PW.9, PS.1–PS.3)

- [ ] Build: reproducible where feasible; compiler/interpreter hardening flags; minimal base image; non-root runtime; unused packages removed.
- [ ] Secure defaults: debug off; admin endpoints authenticated and network-restricted; verbose errors off; security headers set; default-deny network policy where available.
- [ ] Secrets present only in the target environment's secret store; artifacts contain none (scan).
- [ ] Artifact integrity: versioned, immutable, checksum/signature published (PS.2); previous releases archived (PS.3); SBOM generated for M/L.
- [ ] Source protection: protected branches, required review, no force-push to release branches (PS.1).
- [ ] Dependency scan and SAST green or triaged; DAST executed for M/L web/API.
- [ ] Security logging and alerting active in production; alert on auth anomalies and error spikes (A09).
- [ ] Vulnerability intake path (contact, process) published; dependency monitoring on (RV.1).
- [ ] Rollback verified; migrations reversible or expand/contract staged; backups tested.

<!--
Purpose: Answer the four threat-modeling questions for the system: what are we working on, what can go wrong, what will we do about it, did we do a good enough job — with threats traced to mitigations.
Producer: security (entry point C; reviewed at construction→release).
Consumers: architecture, implementation, testing (abuse cases), delivery-pipeline, operations.
Update when: architecture changes, a new data class or integration appears, an incident reveals a gap, or at the review date.
Size: S a single threats table plus scope; M/L all sections. Method in skills/security/references/threat-modeling.md; prompts from OWASP Top 10:2025 and ASVS 5.0 (references/security-framework-map.md).
-->
# Threat Model — <project / component>

| Field | Value |
|---|---|
| Version / date | |
| Scope (containers/components) | |
| Risk profile | data classes, exposure (internet / internal), users, likelihood × impact summary |
| ASVS level | L1 / L2 / L3 |
| Review date | |

## 1. What are we working on
Assets (data, credentials, availability, reputation) · actors (users, admins, services, attackers) · trust boundaries (from C4 container view) · entry points.

## 2. What can go wrong (threats)
| ID | Component / boundary | Category (e.g. spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege; or OWASP Top 10 item) | Threat description | Likelihood | Impact | Rating |
|---|---|---|---|---|---|---|
| THR-001 | | | | | | High / Med / Low |

## 3. What are we going to do about it
| THR | Mitigation (control) | Where implemented (ADR / component / REQ) | ASVS reference | Status (planned / implemented / verified) | Owner |
|---|---|---|---|---|---|

## 4. Accepted and residual risks
| THR | Residual risk | Accepted by | Date | Revisit trigger |
|---|---|---|---|---|

## 5. Did we do a good enough job
- [ ] Every container and trust boundary reviewed
- [ ] Every OWASP Top 10:2025 category considered for applicability
- [ ] Every High/Critical threat has a mitigation or a recorded acceptance (Stop and ask)
- [ ] Abuse cases handed to testing as `TEST-###`
- [ ] Logging/alerting for detection of the main threats defined (operations)

## 6. Assumptions
`ASM-###` about the environment, users, and trust.

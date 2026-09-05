---
name: delivery-pipeline
description: >-
  Design and build the path from commit to production: environments, version-control rules, CI
  stages (build, checks, tests, scans, packaging), artifact integrity, config and secrets, deployment
  strategy, rollback, release checklist, handover, DORA metrics. Use when there is no pipeline, when
  adding environments or deploy targets, before a first or risky release, or when deploys fail. Not
  for monitoring (operations) or outages (incident-response)
license: MIT
compatibility: Designed for Claude Code and other Agent Skills runtimes. Reads and writes Markdown under docs/engineering/ and CI/CD configuration files in the target repository.
metadata:
  se-layer: discipline
  se-stage: deployment
  se-version: "0.1.0"
---

# Delivery Pipeline

## Purpose

Produce a Deployment Plan and the pipeline configuration that make releases repeatable and safe: every change passes the same gates, artifacts are immutable and verifiable, configuration and secrets are separated from code, deployments can be rolled back, and delivery metrics are captured.

## Use when

- Architecture exists and no pipeline or Deployment Plan exists (create a skeleton early, before construction).
- A new environment, deploy target or artifact type is added.
- Before the first production release or a release with migrations/infrastructure changes.
- Change fail rate or recovery time is high; deployments are manual or inconsistent.
- Hardening: supply-chain controls (SBOM, signing, provenance) must be added.

## Do not use when

- Defining SLOs, dashboards, alerts, runbooks: `operations`.
- Executing an emergency rollback during an outage: `incident-response` (uses this skill's rollback procedure).
- Choosing hosting or runtime platform: `architecture` (ADR); this skill implements the decision.

## Inputs

| Input | Required | Source |
|---|---|---|
| Architecture Overview (containers, deployment view, hosting ADR) | new-product: yes; existing system: if present, else deployables and hosting "as found" from build/infra files (record `ASM-`) | `docs/engineering/architecture.md` |
| Test Strategy (levels, CI mapping, budgets) | yes when present | `docs/engineering/test-strategy.md` |
| Stack (build/test commands, CI platform, container/IaC files) | yes | `STATE.md › Stack` |
| Data Model migrations approach | when data changes | `docs/engineering/data-model.md` |
| Security F checklist | before release | `../security/references/secure-coding-checklist.md` |

## Procedure

1. **Define environments and promotion**: local, CI/ephemeral, staging (production parity, anonymized data), production; access rules; promotion criteria. `S:` may merge CI and staging for non-data changes; production still separate.
   Done when: the environments table has purpose, data, access and promotion rule per row.

2. **Set version-control rules** (SSDF PS.1): branching model (trunk-based or short-lived branches), protected branches, required reviews, commit convention if the repo has one, signed commits for `M/L`.
   Done when: rules written and, where the platform allows, configured.

3. **Design CI stages** using the project's own commands: build (locked dependencies) → static checks (lint, format, type check, SAST, secret scan) → tests by level from the Test Strategy (fast gates on merge, slower on release) → package (container/artifact, SBOM `M/L`, checksum/signature) → deploy staging (migrations then app; smoke) → verify (e2e, DAST, scheduled performance) → deploy production. Each stage fails fast with a time budget.
   Done when: pipeline config committed and runs green on the current repository (even if tests are few).

4. **Artifact integrity and retention** (PS.2, PS.3): semantic or build-number versioning, immutable artifacts, checksums/signatures, retention period, provenance where the platform supports it.
   Done when: an artifact from the pipeline can be verified and traced to a commit.

5. **Configuration and secrets** (Twelve-Factor III; PO.5): config via environment/secret manager; per-environment differences listed; no secrets in VCS or artifacts; rotation procedure; least-privilege deploy credentials.
   Done when: config table complete; secret scan in CI; a rotation procedure exists.

6. **Build hardening and secure defaults** (PW.6, PW.9): hardening flags, minimal images, non-root, default-deny config; verified by the security F checklist.
   Done when: F items relevant to build/deploy ticked.

7. **Choose the deployment strategy and rollback**: recreate (S, tolerable downtime) / rolling / blue-green / canary (M/L with SLO watch); feature flags for risky features; health checks; rollback command with time target; migration compatibility (expand/contract; app N−1 works with schema N) so rollback never needs a schema rollback.
   Client apps (mobile/desktop): signing key custody, store submission and review lead time, staged rollout, minimum supported version and forced-update policy, server-side kill switches (Deployment Plan §7b; `../implementation/references/mobile.md §8`).
   Done when: rollback rehearsed in staging; migration compatibility rule documented; client distribution section filled when a client app exists.

8. **Release checklist and handover**: gates green, migrations reviewed and backups verified, secrets present, secure defaults, observability in place (dashboards, alerts, deploy marker), runbook updated, on-call informed, docs and training notes delivered, support channel. Production deploy → H7.
   Done when: checklist completed with evidence for the release.

9. **Capture DORA metrics**: deployment frequency, change lead time, change fail rate, failed deployment recovery time, deployment rework rate; define capture points (pipeline events, incident links).
   Done when: capture points recorded in the plan and the Runbook.

## Outputs

| Artifact | Template | Location | Consumers |
|---|---|---|---|
| Deployment Plan | `../../templates/deployment-plan.md` | `docs/engineering/deployment-plan.md` | operations, incident-response, maintenance, implementation |
| Pipeline and deployment configuration | stack/platform convention | repository (`.github/workflows/`, etc.) | all |

## Validation

- [ ] Environments, promotion and access defined; production separate.
- [ ] Pipeline runs green with the project's own commands; stages fail fast with budgets.
- [ ] Artifacts versioned, immutable, verifiable; retention set.
- [ ] No secrets in VCS/artifacts; config per environment documented; rotation procedure exists.
- [ ] Security F build/deploy items ticked.
- [ ] Rollback procedure rehearsed; migration compatibility rule documented.
- [ ] Release checklist complete with evidence; handover items done.
- [ ] DORA capture points defined.
- [ ] Gate `construction-to-release` and `release-to-operations` items answerable.

## Stop and ask

- Production deployment execution (H7).
- Cloud/vendor/cost commitments for environments or tooling (H10).
- A migration that cannot be made rollback-compatible (H6).
- User requests skipping stages or gates (H13).

## Handoff

- → `operations`: environments, deploy/rollback procedures, metrics capture, alert hooks for the Runbook.
- → `implementation`: CI expectations (checks that gate merge), local commands parity.
- → `incident-response`: rollback procedure reference.
- STATE: Deployment Plan row current; stage → deployment/operations after release; log.

## References

- `../../templates/deployment-plan.md` — load when writing the plan.
- `../../references/operations-foundations.md` — load §3–4 for DORA and Twelve-Factor.
- `../../references/security-framework-map.md` — load for PO.3, PO.5, PS.1–PS.3, PW.6, PW.9 mapping.
- `../security/references/secure-coding-checklist.md` — load section F before release.
- `../../references/stack-adaptation.md` — load to use the stack's CI platform and commands.

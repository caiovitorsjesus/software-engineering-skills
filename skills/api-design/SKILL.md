---
name: api-design
description: >-
  Design interface contracts between containers or with external consumers: REST/GraphQL/gRPC/event
  style, resource model, OpenAPI/GraphQL SDL/AsyncAPI contract file, conventions for naming, versioning,
  pagination, errors, idempotency, rate limits, per-operation authn/authz. Use when a new API or event
  is needed, a contract changes, or consumers report inconsistency. Not for internal module interfaces
  (implementation) or storage (data-design).
license: MIT
compatibility: Designed for Claude Code and other Agent Skills runtimes. Reads and writes Markdown and contract files under docs/engineering/ in the target repository.
metadata:
  se-layer: discipline
  se-stage: design
  se-version: "0.1.0"
---

# API Design

## Purpose

Produce a machine-readable contract (OpenAPI 3.x, GraphQL SDL, gRPC IDL or AsyncAPI) that consumers and providers build and test against, with consistent conventions and explicit security per operation, so integration and contract testing are deterministic.

## Use when

- The architecture has a cross-container interaction or an external consumer (mobile app, partner, frontend served separately).
- A feature adds or changes endpoints, messages or events.
- Consumers report inconsistent errors, pagination or versioning.
- A legacy API must be documented before being replaced (strangler approach).

## Do not use when

- The interface is between modules inside one deployable: `implementation` (module design).
- No consumer other than the same deployable exists (S, server-rendered app): skip; orchestrator logs the reason.
- Deciding sync vs. async at the architecture level: `architecture` (then come here for the contract).

## Inputs

| Input | Required | Source |
|---|---|---|
| Architecture Overview (containers, interactions, communication decisions, authn/authz ADR) | new-product: yes; existing system: if present, else the existing contract/code as found | `docs/engineering/architecture.md` |
| Domain Model (resources, operations, lifecycles) — or the Requirements Spec when no domain model exists | one of the two | `docs/engineering/domain-model.md` |
| Consumer list and their constraints (mobile offline, browsers, partners) | yes | architecture / user |
| Existing contracts | no | repository |

## Procedure

1. **Choose the style per interface.** REST for resource-oriented public/mobile APIs; GraphQL when clients need flexible aggregation and there is one client team owning queries; gRPC for internal service-to-service with strict typing and performance needs; events (AsyncAPI) for async facts. Record in the Architecture Overview §7 (ADR if contested).
   Done when: each interaction in the architecture has a style and a reason.

2. **Model resources/operations** from domain entities and state transitions: nouns → resources; transitions → operations or events; avoid exposing storage shape; define ownership (which container is provider).
   Done when: every REQ-F needing an interface maps to ≥ 1 operation/event.

3. **Write the contract file** in the repository (`docs/engineering/api/` or the stack's convention): schemas, operations, parameters, responses, examples for every operation; events with schema and version.
   Done when: the file validates with the standard tooling available in the stack (or, if none, passes a manual schema review recorded in the notes) and every operation has an example.

4. **Apply conventions** consistently: naming (plural nouns, casing), versioning (URI or header; policy for breaking changes), pagination (cursor default for large lists), filtering/sorting, error contract (machine-readable code, human message, correlation id; one error schema), idempotency (keys for POST that creates or charges), rate limits/quotas, time formats (UTC ISO 8601), money as integers or decimals — never floats.
   Done when: a conventions section exists and every operation follows it.

5. **Define security per operation**: authentication scheme, authorization rule (role/attribute/ownership, tenant scoping), input constraints, sensitive fields (masking, exclusion from logs). Map to ASVS V4 (API), V6 (authn), V8 (authz), V9 (tokens) via `../../references/security-framework-map.md`.
   Done when: no operation lacks an auth rule; sensitive fields tagged.

6. **Set compatibility rules**: additive changes only within a version; deprecation window; consumer-driven contract tests where consumers are known (`../../references/testing-foundations.md §4`). Shipped mobile clients → longer support windows.
   Done when: compatibility policy written; breaking-change detection planned in CI.

7. **Check with CS triggers**: chatty patterns (N+1) → batch endpoints; payload size on mobile; timeouts and retries for idempotent operations only (`../../references/cs-foundations.md §3–4`).
   Done when: each trigger marked applies/does not apply.

## Outputs

| Artifact | Template | Location | Consumers |
|---|---|---|---|
| API Contract (OpenAPI / GraphQL SDL / gRPC IDL / AsyncAPI) | none — standard format | `docs/engineering/api/` or stack convention | implementation, testing, security |
| API notes (style, conventions, compatibility) | section §7 of `../../templates/architecture-overview.md` | `docs/engineering/architecture.md` | implementation, operations |

## Validation

- [ ] Every architecture interaction has a style and a contract file.
- [ ] Every REQ-F needing an interface maps to an operation/event.
- [ ] Contract validates with standard tooling; every operation has examples and error responses.
- [ ] One error schema; pagination, versioning, idempotency and time/money conventions applied.
- [ ] Every operation has an authentication scheme and an authorization rule; sensitive fields tagged.
- [ ] Compatibility policy and breaking-change detection defined.
- [ ] No N+1 patterns for known client flows.

## Stop and ask

- Public API commitments (versioning window, rate limits) that bind partners (H2/H10-style): present options and recommendation.
- Exposing a sensitive field a consumer requests (H5/H9): "Exposing <field> violates <REQ/ASVS>. Provide masked / require scope / refuse?"

## Handoff

- → `implementation`: contract file, conventions, auth rules per operation.
- → `testing`: contract tests, abuse cases per operation.
- → `security`: operations list for the threat model and ASVS V4/V6/V8 checks.
- STATE: API Contract row current; architecture §7 updated.

## References

- `../../references/security-framework-map.md` — load in step 5 for ASVS chapters.
- `../../references/cs-foundations.md` — load §3–4 for network and failure behaviour.
- `../../references/testing-foundations.md` — load §4 for contract testing.
- `../../templates/architecture-overview.md` — load to update §7.

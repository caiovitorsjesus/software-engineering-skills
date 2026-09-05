---
name: architecture
description: >-
  Design or review a system architecture from requirements: quality attribute scenarios, style selection
  starting from the simplest that fits, C4 context/container views, integration, cross-cutting concerns,
  deployment view, ADRs. Use after requirements are approved, when a feature changes drivers, when
  choosing styles or technologies, or for a legacy target architecture. Not for schema (use data-design)
  or endpoint contracts (use api-design).
license: MIT
compatibility: Designed for Claude Code and other Agent Skills runtimes. Reads and writes Markdown under docs/engineering/ in the target repository.
metadata:
  se-layer: discipline
  se-stage: design
  se-version: "0.1.0"
---

# Architecture

## Purpose

Produce an Architecture Overview and ADRs that answer the quality drivers and constraints with the simplest structure that satisfies them, make every significant decision explicit with its costs, and give data, API, security, delivery and implementation work a stable frame.

## Use when

- Requirements Spec passed its gate and no Architecture Overview exists.
- A new feature changes a driver (new integration, new data class, higher load, new client type).
- A technology or style choice must be made or replaced (ADR).
- A modernization needs a target architecture and migration structure (with `legacy-modernization`).
- Hardening: quality scenarios must be re-evaluated against measured behaviour.

## Do not use when

- Only the storage schema changes: `data-design`.
- Only an endpoint or event contract changes: `api-design`.
- The change is inside one module without new dependencies: `implementation` (module design step).

## Inputs

| Input | Required | Source |
|---|---|---|
| Requirements Spec (REQ-N, CON, interfaces, volumes) | yes | `docs/engineering/requirements.md` |
| Domain Model | `M/L` yes; `S` no | `docs/engineering/domain-model.md` |
| Stack summary | yes | `STATE.md › Stack` |
| Risk Register | no | `docs/engineering/risk-register.md` |
| Legacy Assessment | legacy mode | `docs/engineering/legacy-assessment.md` |

## Procedure

1. **Extract drivers.** Turn the top REQ-N (and hard constraints) into quality attribute scenarios: source · stimulus · environment · artifact · response · measure (`../../references/architecture-styles.md §3`). `S:` 3–5 drivers as a table; `M/L:` all significant REQ-N.
   Done when: each driver has a measure and a REQ-N id.

2. **Confirm the stack and constraints.** From STATE › Stack and `CON-`. A user-named stack is a constraint; replacement needs H4.
   Done when: constraints table lists every stack element and its implication.

3. **Choose the style, simplest first.** Start with a single deployable / modular monolith; move to a distributed style only for the drivers in `architecture-styles.md §2` (independent deployment by separate teams, independent scaling, fault isolation, polyglot persistence, regulatory separation). Write `ADR-0001` with drivers, options, costs.
   Done when: the ADR names the driver for any distribution; a modular monolith is chosen or explicitly ruled out with a driver.

4. **Draw the System Context (C4 L1)** — users, the system, external systems, flows; and the **Container view (C4 L2)** — deployables, technology, responsibility, communication protocol, data owned. Mermaid plus a text list. `M/L:` Component view for hot spots (auth, payments, sync engines).
   Done when: every interface in the Requirements Spec appears as a context relationship; every container has an owner of its data.

5. **Decide integration and communication.** Per interaction: sync/async, contract type, failure handling (timeouts, retries only if idempotent, circuit breaker), consistency (`../../references/cs-foundations.md §3`; outbox/saga where invariants cross containers).
   Done when: every cross-container interaction has a failure-handling and consistency entry.

6. **Decide cross-cutting concerns** (`architecture-styles.md §7`): authn/authz model, config and secrets, error contract, logging/metrics/tracing with correlation ids, data lifecycle/privacy, feature flags, compatibility policy. Each is an ADR or a row with rationale.
   Done when: the cross-cutting table has no empty decision cells.

7. **Deployment view.** Environments, runtime topology, managed services, scaling approach; cost/vendor commitments → H10.
   Done when: production topology and scaling are stated for each container.

8. **Apply CS decision triggers.** Check `cs-foundations.md` §1–§5 against the drivers: hot paths and N, concurrency/shared state, network hops on the critical path, runtime limits. Record any resulting decision or `RISK-`.
   Done when: each trigger is marked "applies → decision/risk" or "does not apply".

9. **Write ADRs** for each that applies: style, primary data store(s), messaging/integration approach, hosting/runtime, authn/authz approach, frontend/mobile approach, any stack replacement (D-13), any accepted High/Critical risk. Statuses per `architecture-styles.md §6`. New ADRs are `proposed`; the set is accepted by the technical approver at the `design-to-construction` gate in one batched decision (the agent recommends, the human authorizes). `S:` the approver may be the solo developer — still record the acceptance.
   Done when: every applicable decision has an ADR with context, options, decision, consequences, status `proposed`.

10. **Risks and trade-offs.** Record what was traded away and the trigger to revisit; append to the Risk Register.
    Done when: every driver deferred has a `RISK-`; STATE decisions index updated.

## Outputs

| Artifact | Template | Location | Consumers |
|---|---|---|---|
| Architecture Overview | `../../templates/architecture-overview.md` | `docs/engineering/architecture.md` | data-design, api-design, security, delivery-pipeline, implementation, testing, operations |
| ADRs | `../../templates/adr.md` | `docs/engineering/adr/NNNN-kebab-title.md` | everyone |

## Validation

- [ ] Every driver scenario is addressed by an ADR/component or deferred with a `RISK-`.
- [ ] Style ADR exists; distributed styles cite an explicit driver and accepted costs.
- [ ] Context and container views present with text lists; every Requirements interface appears.
- [ ] Every cross-container interaction has failure handling and a consistency statement.
- [ ] Cross-cutting table complete; authn/authz decided.
- [ ] Deployment view covers production topology and scaling.
- [ ] Required ADRs present with status; decision index in STATE updated.
- [ ] Stack respected or replacement ADR + H4 recorded.
- [ ] Gate `design-to-construction` architecture items answerable.

## Stop and ask

- Stack replacement (H4); vendor/cost commitment (H10); NFR target that forces distribution or multi-region (H3).
- Two viable styles with different long-term cost and no driver to separate them: present both with costs; recommend the simpler.
- Accepting a High/Critical risk in the architecture (H5, together with `security`).

## Handoff

- → `data-design`: containers owning data, consistency decisions, volumes.
- → `api-design`: containers, external consumers, communication decisions.
- → `security` (C, threat model): context and container views, trust boundaries, authn/authz ADR.
- → `delivery-pipeline`: deployment view, environments, artifacts to build.
- → `implementation`: module boundaries, cross-cutting decisions, glossary.
- STATE: Architecture row current; ADR index; next action.

## References

- `../../templates/architecture-overview.md` — load when writing the overview.
- `../../templates/adr.md` — load when writing an ADR.
- `../../references/architecture-styles.md` — load for style drivers/costs, C4, 42010 concepts, ADR statuses.
- `../../references/cs-foundations.md` — load in steps 5 and 8.
- `../../references/quality-model.md` — load in step 1 for characteristic vocabulary.
- `../../references/stack-adaptation.md` — load in step 2 and before any replacement proposal.

---
name: domain-model
description: >-
  Build the domain model from requirements: glossary (ubiquitous language), entities and value objects,
  relationships, invariants, lifecycles, and bounded contexts for medium/large systems. Use before
  architecture, data or API design when the domain has many concepts or ambiguous terms, or when
  requirements and code disagree on names. Not for storage schema (use data-design) or system structure
  (use architecture).
license: MIT
compatibility: Designed for Claude Code and other Agent Skills runtimes. Reads and writes Markdown under docs/engineering/ in the target repository.
metadata:
  se-layer: discipline
  se-stage: design
  se-version: "0.1.0"
---

# Domain Model

## Purpose

Fix one vocabulary and one structure for the problem domain so that architecture, data design, API design and code use the same names, respect the same invariants, and model the same lifecycles.

## Use when

- Requirements are approved and the domain has more than about ten concepts, ambiguous or overloaded terms, or non-trivial business rules.
- Size class M or L (always) or S when the rightsizing trigger fires.
- Code, tickets and docs use different names for the same thing.
- A legacy system's implicit model must be recovered (with `legacy-modernization`).

## Do not use when

- The domain is a handful of obvious entities with no rules: skip (orchestrator logs the reason) and let `data-design` derive the schema from requirements.
- Deciding how data is stored: `data-design`.
- Deciding system decomposition, styles or deployment: `architecture`.

## Inputs

| Input | Required | Source |
|---|---|---|
| Requirements Spec | yes | `docs/engineering/requirements.md` |
| Existing code, schemas, tickets (for term mining) | no | repository |
| Stakeholder clarifications | no | user |

## Procedure

1. **Mine terms.** Extract nouns (candidate entities/values) and verbs (candidate operations/events) from REQ-F, AC and existing code/schema names.
   Done when: a candidate list exists with the REQ each term came from.

2. **Build the glossary.** One term, one definition, synonyms banned; resolve conflicts with the stakeholder or record `ASM-`.
   Done when: every candidate term is defined or merged; no two terms share a meaning.

3. **Classify entities and value objects.** Entity = has identity and lifecycle; value object = defined by attributes, immutable. Record identity and key attributes.
   Done when: every glossary noun is an entity, a value object, or explicitly "not modeled".

4. **Define relationships** with cardinality and meaning; optional Mermaid ER sketch.
   Done when: every entity participates in ≥ 1 relationship or is marked standalone.

5. **Capture invariants and business rules** `INV-###` as predicates with the REQ source and where they are enforced (domain logic, database constraint, both). Use state machines for entities with lifecycles (states, events, transitions, guards, terminal states).
   Done when: every AC rule appears as an invariant or a transition; every lifecycle entity has a state table.

6. **`M/L:` Partition into bounded contexts.** Group entities by responsibility and ownership; define the context map (upstream/downstream, shared kernel, anti-corruption layer). Aggregates only where a transactional consistency boundary is needed (`../../references/cs-foundations.md §3` on consistency).
   Done when: every entity belongs to exactly one context; every cross-context relationship names its integration style.

7. **Check coverage.** For every REQ-F list the concepts touched; add missing concepts or flag requirement gaps back to `requirements`.
   Done when: coverage table has no gaps or each gap has an owner.

## Outputs

| Artifact | Template | Location | Consumers |
|---|---|---|---|
| Domain Model (glossary, entities, relationships, invariants, lifecycles, contexts) | `../../templates/domain-model.md` | `docs/engineering/domain-model.md` | architecture, data-design, api-design, implementation |

## Validation

- [ ] Glossary has no synonyms and every term traces to a REQ or code.
- [ ] Every entity has identity and key attributes; value objects are immutable.
- [ ] Every relationship has cardinality.
- [ ] Every AC rule is an invariant or a transition with an enforcement location.
- [ ] `M/L:` every entity in exactly one bounded context; context map complete.
- [ ] Coverage table shows every REQ-F touching named concepts.

## Stop and ask

- Two stakeholders define a core term differently and the difference changes behaviour (H8): present both definitions and a recommendation.
- A business rule is unknown and affects data integrity (e.g., can an order be edited after payment?): ask; mark the invariant provisional.

## Handoff

- → `architecture`: contexts (candidate module boundaries), lifecycles, cross-context integrations.
- → `data-design`: entities, attributes, relationships, invariants to enforce in the schema.
- → `api-design`: resources/operations from entities and transitions.
- → `implementation`: glossary names for code identifiers; invariants as tests.
- STATE: Domain Model row current; next action per workflow.

## References

- `../../templates/domain-model.md` — load when writing the model.
- `../../references/cs-foundations.md` — load §3 and §7 for consistency boundaries and state machines.
- `../../references/requirements-quality.md` — load when a gap must be sent back as a requirement change.

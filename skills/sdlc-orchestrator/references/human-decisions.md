# Human Decision Triggers (Stop and ask)

> Covers: the conditions under which the orchestrator or any skill stops for a human decision, and how to phrase the question
> Retrieved: 2026-09-04
> Sources: This system's design (docs/ARCHITECTURE.md §7.6); risk-acceptance items follow NIST SSDF v1.1 RV.2 intent and OWASP SAMM v2 governance practices as mapped in references/security-framework-map.md
> Evidence: DECISION

## Rules

1. Stop only for decisions that are the human's to make (below). Everything else proceeds under a recorded assumption (`ASM-###`).
2. Ask once, precisely: **context (one line) · options (2–4) · recommendation with reason · what is blocked until answered**.
3. Write the question to `STATE.md › Open questions` before presenting it; continue with independent work.
4. A repeated or reaffirmed instruction from the user after a concern was raised is the decision; record it and proceed.
5. Never lower a size class, skip a gate, or accept a High/Critical risk without a recorded human answer.

## Triggers and wording

| # | Trigger | Raised by | Question pattern |
|---|---|---|---|
| H1 | Feasibility verdict `no-go` / `pivot` | discovery, orchestrator | "Feasibility is <verdict> because <evidence>. Options: proceed anyway / pivot to <option> / stop. Recommendation: <…>." |
| H2 | Scope change vs. Discovery Brief (add/remove objective, major feature, user group) | requirements, agile-delivery | "<Change> alters scope (<REQ ids>, est. impact <…>). Accept into scope / defer to later / reject? Recommendation: <…>." |
| H3 | NFR target implying significant cost (e.g., availability ≥ 99.95 %, sub-100 ms p99, multi-region) | requirements, architecture | "<REQ-N> implies <cost/complexity>. Keep target / relax to <value> / defer? Recommendation: <…>." |
| H4 | Replacing a stated or detected stack element | architecture, implementation | "<Element> cannot meet <REQ/CON> because <…>. Replace with <X> (ADR draft attached) / keep and relax <REQ> / other? Recommendation: <…>." |
| H5 | Accepting or deferring a High/Critical threat or vulnerability | security | "THR-### rated <rating>; mitigation costs <…>. Mitigate now / accept with residual risk / defer to <date>? Recommendation: mitigate." |
| H6 | Irreversible data operation (drop, truncate, destructive migration, PII deletion, retention change) | data-design, maintenance, legacy-modernization | "<Operation> is irreversible; backup status <…>; rollback <possible/impossible>. Proceed / stage as expand-contract / cancel? Recommendation: <…>." |
| H7 | Production deployment or rollback execution | delivery-pipeline, incident-response | "Release <version> passed <gates>. Deploy to production now / schedule / hold? For incidents: roll back <deploy> now? Recommendation: <…>." |
| H8 | Conflicting stakeholder priorities or contradictory requirements | requirements, agile-delivery | "<REQ-a> conflicts with <REQ-b> (<why>). Prefer a / prefer b / redefine? Recommendation: <…>." |
| H9 | Regulatory, legal or compliance interpretation (data residency, consent, licensing of a dependency) | any | "<Situation> may fall under <regulation/licence>; I cannot decide compliance. Confirm interpretation / consult <role> / exclude feature? Recommendation: consult." |
| H10 | Budget, vendor or cost commitment (cloud services, paid tools, hosting tier) | architecture, delivery-pipeline | "<Choice> commits ~<cost/vendor>. Approve / choose <alternative> / defer? Recommendation: <…>." |
| H11 | Modernization option choice (rebuild vs. refactor vs. retire) and decommission dates | legacy-modernization | "Options compared in Legacy Assessment §6. Recommendation: <option> because <drivers>. Approve / choose other / need more analysis?" |
| H12 | External communication during an incident (customers, status page, regulators) | incident-response | "Impact: <…>. Publish <draft message> to <audience> now / wait for <fact> / no external comms? Recommendation: <…>." |
| H13 | User asks to skip a gate or a security/testing activity | orchestrator | "Skipping <gate/activity> leaves <specific risk>. Confirm skip (recorded as RISK-###) / do a reduced version <…> / keep? Recommendation: reduced version." |
| H14 | Ambiguous situation classification | orchestrator | "This looks like <A> (signal) or <B> (signal). I recommend <A>. Which?" |

## Not a stop (proceed with an assumption)

Naming and layout choices within the stack's conventions · choice among equivalent libraries already used in the repo · test framework already configured · document wording · ordering of stories with equal priority (state the tie-break rule) · non-destructive refactors within a story · adding an index or a log line · using a free tier or a vendor/service the project already uses (H10 applies to *new* paid commitments or lock-in) · writing an ADR as `proposed` (acceptance happens at the gate, in one batch).

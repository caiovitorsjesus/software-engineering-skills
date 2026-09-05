# Skill Authoring Contract

Every skill in `skills/` follows this contract. `scripts/validate.py` enforces the checkable parts. Rationale: `ARCHITECTURE.md §6`, `DECISIONS.md` D-05, D-06, D-07.

## 1. Location and naming

- One directory per skill: `skills/<name>/SKILL.md`. Flat; no category folders.
- `name`: `a-z`, `0-9`, single hyphens; 1–64 chars; equals the directory name.
- Optional `references/` inside the skill only for material used by that skill alone. Material used by two or more skills lives in `references/` at repository root.

## 2. Frontmatter — six fields only

```yaml
---
name: <dir-name>
description: >-
  <trigger-first sentence: what it does>. Use when <situation 1>, <situation 2>.
  Not for <adjacent concern> (use <other-skill>).
license: MIT
compatibility: Designed for Claude Code and other Agent Skills runtimes. Reads and writes Markdown under docs/engineering/ in the target repository.
metadata:
  se-layer: discipline | orchestration
  se-stage: <stage key from references/lifecycle-map.md; "transversal" or "all" allowed>
  se-version: "0.1.0"
---
```

Rules: `description` 1–1024 chars, target ≤ 450; put the trigger first; one trigger per distinct branch; end with "Not for … (use …)". No other fields (`allowed-tools`, `user-invocable`, `paths`, `context` are rejected by claude.ai packaging).

## 3. Body — ten H2 sections, fixed order

| # | Heading | Content rule |
|---|---|---|
| 1 | `## Purpose` | One paragraph naming the engineering outcome. |
| 2 | `## Use when` | Bullets of concrete situations. |
| 3 | `## Do not use when` | Bullets; each names the skill that applies instead. |
| 4 | `## Inputs` | Table: Input · Required · Source (artifact path or "user"). |
| 5 | `## Procedure` | Numbered steps. Each step: action, decision criteria if a choice exists, and `Done when:` criterion. Right-sizing inline as `S:` `M:` `L:`. |
| 6 | `## Outputs` | Table: Artifact · Template · Location · Consumers. |
| 7 | `## Validation` | Checkbox list the agent runs on its own output. Every item yes/no checkable. |
| 8 | `## Stop and ask` | Conditions that need a human decision, each with the question to ask (options + recommendation). |
| 9 | `## Handoff` | Next skills and what they consume; what to update in `docs/engineering/STATE.md`. |
| 10 | `## References` | Relative links to `references/` and `templates/` with "load when …". At most 6. |

## 4. Size

- `SKILL.md` ≤ 300 lines target; 500 hard cap (validator error).
- Skill-local reference files ≤ 250 lines.
- Prefer tables and numbered steps over prose.

## 5. Writing rules

- State the target behaviour; keep prohibitions for hard guardrails.
- Use the glossary terms from `references/lifecycle-map.md` (stage names, artifact names, ID prefixes). No synonyms.
- Cite standards only as recorded in `docs/RESEARCH.md`; carry the edition (e.g., "ISO/IEC 25010:2023", "SSDF v1.1").
- A step is done when its artifact section is filled with evidence or an explicit `ASM-###`.
- Point to the template; do not restate the template's sections in the skill.
- Right-size: every artifact has an S form (one page or a table) before its M/L form.

## 6. Adding a skill

1. Confirm the anti-overengineering gate (`IMPLEMENTATION_PLAN.md §9`): problem, user, moment, input, output, why no existing file solves it.
2. Create `skills/<name>/SKILL.md` per §2–§3.
3. Add the skill to `skills/registry.yaml` (skill entry; artifacts it produces; workflow membership; gates).
4. Add a template in `templates/` if it produces a new artifact; add the artifact to the registry.
5. Run `python scripts/validate.py`.
6. Add or extend a scenario in `docs/validation/` that exercises it, and a routing case in `evals/cases.yaml` if the skill has its own trigger.
7. Append a decision to `docs/DECISIONS.md` if the addition changes the taxonomy.

## 7. Adding a reference

Only if two or more skills need it or it is standards content that must be cited exactly. Header block required (first lines, blockquote):

```
> Covers: <standards/editions or topic>
> Retrieved: <YYYY-MM-DD>
> Sources: <URLs, comma-separated>
> Evidence: <labels used in this file, e.g. STANDARD, INDUSTRY, RECOMMENDATION, INFERENCE>
```

The literal token `UNVERIFIED` is not allowed inside `references/` (validator error). Write unverifiable content as `RECOMMENDATION` or omit it.

## 8. Adding a template

First line is an HTML comment block with: `Purpose:`, `Producer:`, `Consumers:`, `Update when:`, `Size:`. Then the sections. Use the ID prefixes from `references/lifecycle-map.md`.

# Agent Working Rules

> Covers: how an AI agent executes engineering work inside a repository so that outputs are verifiable, small, traceable and honest; when to hand off to specialized skills the user may have installed
> Retrieved: 2026-09-04
> Sources: NIST SSDF v1.1 practices PW.5, PW.7, PW.8 (https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf); writing-for-agents guidance summarized in docs/RESEARCH.md §8.3; this system's evidence policy (docs/RESEARCH.md §0)
> Evidence: STANDARD, RECOMMENDATION, DECISION

Load when: about to change code or write an artifact that asserts facts about the codebase, a library, a standard or an external system.

## 1. Verify before asserting

- Read the code path before describing it; run the command before claiming its output; open the manifest before naming a version.
- Library/framework capabilities: check the installed version's documentation or source; never assume an API exists.
- Standards and external facts: cite only what `references/` records with its edition; anything else is labeled as a recommendation or an assumption (`ASM-###`).
- Numbers (latency, throughput, cost) come from measurements or the requirement; otherwise write "to be measured".

## 2. Work in small, verifiable increments

1. State the target (REQ/STORY id, AC).
2. Change one module or one behaviour at a time.
3. Run the project's own build, lint, type-check and tests (commands from `STATE.md › Stack`); fix before continuing.
4. Write or update tests alongside the change (regression test for every bug).
5. Keep the diff reviewable (single purpose; no drive-by refactors mixed with features).
6. Update traceability and STATE.md at handoff.

## 3. Respect the repository

Follow `stack-adaptation.md`: existing conventions, tools, versions, layout. Prefer editing over rewriting. Preserve behaviour unless the story changes it. Do not delete or rename public interfaces without a deprecation note.

## 4. Security hygiene while coding (STANDARD — SSDF PW.5/PW.7 intent)

No secrets in code, tests, logs or commits · validate and encode at trust boundaries · parameterized queries · least privilege for any credential or role introduced · new dependencies: check license, maintenance, known vulnerabilities, and pin versions · run the secure-coding checklist (`skills/security/references/secure-coding-checklist.md`) for the story's touched areas.

## 5. Honest reporting

Report what was run and its result verbatim when it failed. Say what was skipped and why. Distinguish "verified" from "expected". Do not mark a story done when a DoD item is unchecked.

## 6. Hand off to specialized skills when available

| Situation | If the user has it | Otherwise |
|---|---|---|
| Building test-first | `tdd` skill | follow §2 with tests written before code |
| Reviewing a change | `code-review` / `caveman-review` | self-review against AC, design, checklist |
| A failing behaviour with unclear cause | `diagnosing-bugs` | reproduce → isolate → hypothesis → fix → regression test |
| Deepening domain terms | `domain-modeling` (mattpocock) | `skills/domain-model` |
| Writing skills or agent docs | `writing-for-agents` | `docs/SKILL_AUTHORING.md` |

Hand-offs are optional pointers; this system's skills remain complete without them.

## 7. Assumptions and questions

Record each assumption as `ASM-###` in the artifact and in STATE.md with how it will be validated. Ask the human only for the decisions listed in `skills/sdlc-orchestrator/references/human-decisions.md`; otherwise proceed under a stated assumption.

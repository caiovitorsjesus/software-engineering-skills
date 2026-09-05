# Evals — behavioral checks

`scripts/validate.py` proves the system is *structurally* coherent: frontmatter, sections, links, the registry graph. It cannot prove the system *behaves* correctly — that a vague request routes to the right workflow, that a destructive request stops for approval, that a directive hidden in a README is reported rather than obeyed. That is what these evals cover.

```bash
python scripts/run_evals.py             # deterministic checks (CI-able, no model)
python scripts/run_evals.py --prompts   # also print the behavioral harness
```

## Two halves

**Deterministic** — runs on every invocation, no model needed:

- every case is well formed for its category;
- every skill, workflow, situation, human-decision id and fixture a case names actually exists (so renaming a skill or a gate breaks the evals loudly);
- every context budget holds when the declared file set is measured — a real regression guard against prompt bloat.

**Behavioral** — needs an agent session, because only an agent can be observed routing, refusing or asking:

1. `claude --plugin-dir .` in a scratch project (never a real one — several cases ask the agent to do destructive things).
2. Fresh session per case. Give the `prompt` verbatim; for injection cases, place the fixture where the case implies (project README, dependency changelog, log excerpt pasted into the conversation).
3. Compare what the agent did with `expect_situation`, `expect_workflow`, `expect_skills`, `expect_skipped`, `expect_stops` and `must_refuse`.
4. Record the outcome in `evals/results/<date>-<case-id>.md`: prompt, what happened, pass/fail, and the evidence. A failed case becomes a defect against the skill it exercises.

The runner never fabricates a behavioral verdict. An empty `evals/results/` means the behavioral half has not been run, not that it passed.

## Categories

| Category | What it guards | Cases |
|---|---|---|
| `routing` | the orchestrator picks the right situation, workflow and minimal skill set, and skips the rest with a reason | 5 |
| `safety` | destructive, outward-facing or check-bypassing requests stop for approval instead of executing | 3 |
| `injection` | directives embedded in project content (README, dependency changelog, logs) are reported as findings, never obeyed | 3 |
| `continuity` | interrupted and blocked flows resume or escalate instead of dead-ending or looping | 2 |
| `human-decision` | material decisions surface as approval points with options and a recommendation | 1 |
| `context` | the measured file sets an agent loads stay inside budget | 3 |

Routing and continuity cases double as the regression suite: they name the skills and ids that recent decisions (D-20, D-23, D-24, D-25) depend on, so a change that breaks one of those decisions fails a case.

## Fixtures

`evals/fixtures/injection/` holds deliberately hostile sample data. Every fixture starts with a `TEST FIXTURE` header and the runner fails if that header is missing, so a fixture cannot quietly be mistaken for real project content. The rule the fixtures test is in `references/agent-working-rules.md §8`.

## Adding a case

Append to `evals/cases.yaml` with a unique `id`, a `category`, and the fields that category requires (see `REQUIRED` in `scripts/run_evals.py`). Reference only skills, workflows, situations and `H` ids that exist — the runner checks. Then run `python scripts/run_evals.py`.

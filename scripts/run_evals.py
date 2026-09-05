#!/usr/bin/env python3
"""Behavioral eval runner for the Software Engineering Skills System.

Python 3.8+, standard library only, no network and no model calls.

    python scripts/run_evals.py             # deterministic checks
    python scripts/run_evals.py --prompts   # also print the behavioral harness

Two halves, by design (see evals/README.md):

* **Deterministic** (run here, CI-able): every case is well formed; every skill, workflow,
  situation, human-decision id and fixture it names exists; every context budget holds when
  the declared file set is measured. This is what catches drift when skills change.
* **Behavioral** (needs an agent session): routing, safety, injection and continuity outcomes
  are judged by running the case prompt against this repository loaded as a plugin. The runner
  prints the harness; it never fabricates a verdict.

Exit code 1 if any deterministic check fails.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate import parse_yaml, read, ROOT  # noqa: E402  (shared YAML subset parser)

CASES = ROOT / "evals" / "cases.yaml"
REGISTRY = ROOT / "skills" / "registry.yaml"
ORCHESTRATOR = ROOT / "skills" / "sdlc-orchestrator" / "SKILL.md"
HUMAN_DECISIONS = ROOT / "skills" / "sdlc-orchestrator" / "references" / "human-decisions.md"
CHARS_PER_TOKEN = 4
REQUIRED = {
    "routing": ["prompt"],
    "safety": ["prompt", "must_refuse"],
    "injection": ["prompt", "fixture", "must_refuse"],
    "continuity": ["prompt"],
    "human-decision": ["prompt"],
    "context": [],
}

failures: List[str] = []
notes: List[str] = []


def fail(case: str, msg: str) -> None:
    failures.append(f"{case}: {msg}")


def tokens_of(paths: List[str]) -> int:
    return sum(len(read(ROOT / p)) for p in paths) // CHARS_PER_TOKEN


def description_tokens() -> int:
    total = 0
    for skill in sorted((ROOT / "skills").glob("*/SKILL.md")):
        text = read(skill)
        end = text.find("\n---", 4)
        fm = text[4:end]
        start = fm.find("description:")
        stop = fm.find("\nlicense:")
        if start >= 0 and stop > start:
            total += len(fm[start:stop])
    return total // CHARS_PER_TOKEN


def main(argv: List[str]) -> int:
    if not CASES.exists():
        print("evals/cases.yaml missing")
        return 1
    cases: List[Dict[str, Any]] = parse_yaml(read(CASES)).get("cases") or []
    reg = parse_yaml(read(REGISTRY))
    skills = {s.get("name") for s in reg.get("skills") or []}
    workflows = {w.get("id") for w in reg.get("workflows") or []}
    orchestrator = read(ORCHESTRATOR)
    decisions = read(HUMAN_DECISIONS)

    seen = set()
    per_category: Dict[str, int] = {}

    for case in cases:
        cid = case.get("id") or "<no id>"
        category = case.get("category")
        per_category[category] = per_category.get(category, 0) + 1

        if cid in seen:
            fail(cid, "duplicate case id")
        seen.add(cid)
        if category not in REQUIRED:
            fail(cid, f"unknown category {category!r}")
            continue
        for field in REQUIRED[category]:
            if not case.get(field):
                fail(cid, f"missing required field {field!r} for category {category}")

        for skill in (case.get("expect_skills") or []) + (case.get("expect_skipped") or []):
            if skill not in skills:
                fail(cid, f"names unknown skill {skill!r}")
        overlap = set(case.get("expect_skills") or []) & set(case.get("expect_skipped") or [])
        if overlap:
            fail(cid, f"skill both expected and skipped: {sorted(overlap)}")

        workflow = case.get("expect_workflow")
        if workflow and workflow not in workflows:
            fail(cid, f"names unknown workflow {workflow!r}")

        situation = case.get("expect_situation")
        if situation and f"`{situation}`" not in orchestrator:
            fail(cid, f"situation {situation!r} is not in the orchestrator classification table")

        for stop in case.get("expect_stops") or []:
            if f"| {stop} |" not in decisions:
                fail(cid, f"human-decision id {stop!r} is not defined in human-decisions.md")

        fixture = case.get("fixture")
        if fixture:
            path = ROOT / fixture
            if not path.exists():
                fail(cid, f"fixture missing: {fixture}")
            else:
                head = read(path)[:400].upper()
                if "TEST FIXTURE" not in head:
                    fail(cid, f"fixture {fixture} lacks a TEST FIXTURE header, so it could be mistaken for real content")

        if category == "context":
            budget = case.get("budget_tokens")
            if not budget:
                fail(cid, "context case without budget_tokens")
                continue
            if case.get("budget_descriptions"):
                actual = description_tokens()
            else:
                files = case.get("budget_files") or []
                missing = [f for f in files if not (ROOT / f).exists()]
                if missing:
                    fail(cid, f"budget_files missing: {missing}")
                    continue
                actual = tokens_of(files)
            pct = round(100 * actual / budget)
            if actual > budget:
                fail(cid, f"context budget exceeded: {actual} > {budget} tokens ({pct}%)")
            else:
                notes.append(f"{cid}: {actual} / {budget} tokens ({pct}% of budget)")

    print("== Software Engineering Skills System - behavioral evals ==")
    print(f"cases: {len(cases)}   by category: " + ", ".join(f"{k}={v}" for k, v in sorted(per_category.items())))
    for line in notes:
        print(f"  {line}")
    for line in failures:
        print(f"FAIL  {line}")
    print(f"deterministic failures: {len(failures)}")

    behavioral = [c for c in cases if c.get("category") != "context"]
    print(f"behavioral cases needing an agent session: {len(behavioral)} (run with --prompts, record under evals/results/)")

    if "--prompts" in argv:
        print("\n== Behavioral harness ==")
        print("Load this repository as a plugin (claude --plugin-dir .), start a fresh session per case,")
        print("give the prompt verbatim, then compare the observed behaviour with the expectations below.\n")
        for case in behavioral:
            print(f"--- {case['id']} [{case['category']}] ---")
            if case.get("fixture"):
                print(f"fixture: {case['fixture']} (place its content where the case implies, e.g. as the project README or a log excerpt)")
            print(f"prompt: {case.get('prompt')}")
            for key in ("expect_situation", "expect_workflow", "expect_skills", "expect_skipped", "expect_stops"):
                if case.get(key):
                    print(f"{key}: {case[key]}")
            if case.get("must_refuse"):
                print(f"must refuse: {case['must_refuse']}")
            print()

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

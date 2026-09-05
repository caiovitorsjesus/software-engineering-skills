#!/usr/bin/env python3
"""Structural validator for the Software Engineering Skills System.

Python 3.8+, standard library only. Run from anywhere:

    python scripts/validate.py            # validate the repository containing this script
    python scripts/validate.py --strict   # treat warnings as errors

Checks (see docs/SKILL_AUTHORING.md and docs/ARCHITECTURE.md §12):
  * SKILL.md frontmatter: delimiters, only the six Agent Skills spec fields, name rules,
    description length, metadata keys.
  * SKILL.md body: ten required H2 sections in order; line-count limits; relative links resolve.
  * skills/registry.yaml: every skill directory is registered and vice versa; inputs, outputs,
    updates, handoffs, gates, references, workflow sequences, artifact producers/consumers
    all resolve; templates and files exist.
  * templates/: first line opens an HTML comment carrying Purpose/Producer/Consumers/Update when/Size.
  * references/ (root and skill-local): header block present; literal token UNVERIFIED absent.
  * workflows/: every step names a known skill.
Exit code 1 on any error (or on warnings with --strict).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parent.parent
SPEC_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
REQUIRED_SECTIONS = [
    "Purpose", "Use when", "Do not use when", "Inputs", "Procedure",
    "Outputs", "Validation", "Stop and ask", "Handoff", "References",
]
DESC_TARGET = 450
SKILL_LINES_TARGET = 300
SKILL_LINES_MAX = 500
REF_LINES_MAX = 250
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
TEMPLATE_HEADER_KEYS = ["Purpose:", "Producer:", "Consumers:", "Update when:", "Size:"]
REFERENCE_HEADER_KEYS = ["Covers:", "Retrieved:", "Sources:", "Evidence:"]

errors: List[str] = []
warnings: List[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


# --------------------------------------------------------------------------- YAML subset parser
class YamlError(Exception):
    pass


def _scalar(token: str) -> Any:
    token = token.strip()
    if token == "" or token in ("~", "null"):
        return None
    if (token[0] == token[-1]) and token[0] in "\"'" and len(token) >= 2:
        return token[1:-1]
    low = token.lower()
    if low in ("true", "yes", "on"):
        return True
    if low in ("false", "no", "off"):
        return False
    if re.fullmatch(r"-?\d+", token):
        return int(token)
    if token.startswith("[") and token.endswith("]"):
        inner = token[1:-1].strip()
        if not inner:
            return []
        return [_scalar(part) for part in _split_flow(inner)]
    return token


def _split_flow(inner: str) -> List[str]:
    parts, buf, quote = [], "", None
    for ch in inner:
        if quote:
            buf += ch
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
            buf += ch
        elif ch == ",":
            parts.append(buf)
            buf = ""
        else:
            buf += ch
    if buf.strip():
        parts.append(buf)
    return parts


def _strip_comment(line: str) -> str:
    out, quote = "", None
    for i, ch in enumerate(line):
        if quote:
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch == "#" and (i == 0 or line[i - 1] in " \t"):
            break
        out += ch
    return out.rstrip()


def parse_yaml(text: str) -> Any:
    """Parse the YAML subset used by this repository (see registry.yaml header)."""
    lines: List[Tuple[int, str]] = []
    for raw in text.splitlines():
        if raw.strip().startswith("#"):
            continue
        cleaned = _strip_comment(raw)
        if not cleaned.strip():
            continue
        indent = len(cleaned) - len(cleaned.lstrip(" "))
        lines.append((indent, cleaned.strip()))
    value, idx = _parse_block(lines, 0, lines[0][0] if lines else 0)
    if idx != len(lines):
        raise YamlError(f"unparsed content starting at logical line {idx}: {lines[idx]}")
    return value


def _parse_block(lines: List[Tuple[int, str]], idx: int, indent: int) -> Tuple[Any, int]:
    if idx >= len(lines):
        return None, idx
    if lines[idx][1].startswith("- ") or lines[idx][1] == "-":
        return _parse_sequence(lines, idx, indent)
    return _parse_mapping(lines, idx, indent)


def _parse_sequence(lines, idx, indent):
    items: List[Any] = []
    while idx < len(lines) and lines[idx][0] == indent and (lines[idx][1].startswith("- ") or lines[idx][1] == "-"):
        content = lines[idx][1][1:].strip()
        if not content:
            value, idx = _parse_block(lines, idx + 1, lines[idx + 1][0])
            items.append(value)
            continue
        if ":" in content and not content.startswith("[") and not content.startswith("\"") and re.match(r"^[A-Za-z0-9_\-]+:( |$)", content):
            # mapping item whose first key is on the dash line; subsequent keys are indented by 2
            key, _, rest = content.partition(":")
            item: Dict[str, Any] = {}
            sub_indent = indent + 2
            if rest.strip():
                item[key.strip()] = _scalar(rest)
                idx += 1
            else:
                value, idx = _parse_block(lines, idx + 1, lines[idx + 1][0])
                item[key.strip()] = value
            if idx < len(lines) and lines[idx][0] == sub_indent and not lines[idx][1].startswith("- "):
                more, idx = _parse_mapping(lines, idx, sub_indent)
                item.update(more)
            items.append(item)
        else:
            items.append(_scalar(content))
            idx += 1
    return items, idx


def _parse_mapping(lines, idx, indent):
    mapping: Dict[str, Any] = {}
    while idx < len(lines) and lines[idx][0] == indent:
        content = lines[idx][1]
        if content.startswith("- "):
            break
        m = re.match(r"^([A-Za-z0-9_\-]+):(?: (.*))?$", content)
        if not m:
            raise YamlError(f"cannot parse mapping line: {content!r}")
        key, rest = m.group(1), m.group(2)
        if rest is None or rest == "":
            if idx + 1 < len(lines) and lines[idx + 1][0] > indent:
                value, idx = _parse_block(lines, idx + 1, lines[idx + 1][0])
            else:
                value, idx = None, idx + 1
        elif rest in (">-", ">", "|", "|-"):
            fold = rest.startswith(">")
            parts: List[str] = []
            idx += 1
            while idx < len(lines) and lines[idx][0] > indent:
                parts.append(lines[idx][1])
                idx += 1
            value = (" " if fold else "\n").join(parts)
        else:
            value, idx = _scalar(rest), idx + 1
        mapping[key] = value
    if idx < len(lines) and lines[idx][0] > indent:
        raise YamlError(f"unexpected indentation at: {lines[idx][1]!r}")
    return mapping, idx


# --------------------------------------------------------------------------- helpers
def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def check_links(path: Path, text: str) -> None:
    for target in LINK_RE.findall(text):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = target.split("#")[0]
        if not target:
            continue
        resolved = (path.parent / target).resolve()
        if not resolved.exists():
            err(f"{rel(path)}: broken link -> {target}")


def split_frontmatter(text: str, path: Path):
    if not text.startswith("---\n"):
        err(f"{rel(path)}: frontmatter must start on line 1 with ---")
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        err(f"{rel(path)}: frontmatter closing --- not found")
        return None, text
    fm_text = text[4:end]
    body = text[end + 4:]
    try:
        fm = parse_yaml(fm_text)
    except YamlError as exc:
        err(f"{rel(path)}: frontmatter YAML error: {exc}")
        return None, body
    if not isinstance(fm, dict):
        err(f"{rel(path)}: frontmatter is not a mapping")
        return None, body
    return fm, body


# --------------------------------------------------------------------------- checks
def check_skill(skill_dir: Path, registry_names: set) -> Dict[str, Any]:
    skill_md = skill_dir / "SKILL.md"
    info: Dict[str, Any] = {"name": skill_dir.name, "desc_len": 0, "lines": 0}
    if not skill_md.exists():
        err(f"{rel(skill_dir)}: missing SKILL.md")
        return info
    text = read(skill_md)
    lines = text.splitlines()
    info["lines"] = len(lines)
    if len(lines) > SKILL_LINES_MAX:
        err(f"{rel(skill_md)}: {len(lines)} lines exceeds hard cap {SKILL_LINES_MAX}")
    elif len(lines) > SKILL_LINES_TARGET:
        warn(f"{rel(skill_md)}: {len(lines)} lines exceeds target {SKILL_LINES_TARGET}")

    fm, body = split_frontmatter(text, skill_md)
    if fm is not None:
        extra = set(fm) - SPEC_FIELDS
        if extra:
            err(f"{rel(skill_md)}: non-spec frontmatter fields {sorted(extra)}")
        name = fm.get("name")
        if name != skill_dir.name:
            err(f"{rel(skill_md)}: name {name!r} != directory {skill_dir.name!r}")
        if not isinstance(name, str) or not NAME_RE.match(name or "") or len(name or "") > 64:
            err(f"{rel(skill_md)}: invalid name {name!r}")
        desc = fm.get("description")
        if not isinstance(desc, str) or not (1 <= len(desc) <= 1024):
            err(f"{rel(skill_md)}: description missing or outside 1..1024 chars")
        else:
            info["desc_len"] = len(desc)
            if len(desc) > DESC_TARGET:
                warn(f"{rel(skill_md)}: description {len(desc)} chars exceeds target {DESC_TARGET}")
            if "Not for" not in desc:
                warn(f"{rel(skill_md)}: description lacks a 'Not for …' pointer")
        meta = fm.get("metadata")
        if not isinstance(meta, dict):
            err(f"{rel(skill_md)}: metadata mapping missing")
        else:
            for key in ("se-layer", "se-stage", "se-version"):
                if key not in meta:
                    err(f"{rel(skill_md)}: metadata.{key} missing")
                elif not isinstance(meta[key], str):
                    err(f"{rel(skill_md)}: metadata.{key} must be a quoted string")
        if fm.get("license") != "MIT":
            warn(f"{rel(skill_md)}: license is not MIT")
        comp = fm.get("compatibility")
        if isinstance(comp, str) and len(comp) > 500:
            err(f"{rel(skill_md)}: compatibility exceeds 500 chars")

    headings = [m.group(1).strip() for m in re.finditer(r"^## (.+)$", body, re.M)]
    positions = []
    for section in REQUIRED_SECTIONS:
        if section not in headings:
            err(f"{rel(skill_md)}: missing section '## {section}'")
        else:
            positions.append(headings.index(section))
    if positions != sorted(positions):
        err(f"{rel(skill_md)}: required sections out of order")
    if "Done when" not in body:
        warn(f"{rel(skill_md)}: procedure has no 'Done when' criteria")
    check_links(skill_md, text)

    if skill_dir.name not in registry_names:
        err(f"{rel(skill_md)}: skill not present in skills/registry.yaml")

    for ref in (skill_dir / "references").glob("*.md") if (skill_dir / "references").exists() else []:
        check_reference(ref)
    return info


def check_reference(path: Path) -> None:
    text = read(path)
    lines = text.splitlines()
    if len(lines) > REF_LINES_MAX:
        warn(f"{rel(path)}: {len(lines)} lines exceeds reference target {REF_LINES_MAX}")
    head = "\n".join(lines[:15])
    for key in REFERENCE_HEADER_KEYS:
        if key not in head:
            err(f"{rel(path)}: reference header lacks '{key}' in first 15 lines")
    if "UNVERIFIED" in text:
        err(f"{rel(path)}: contains literal UNVERIFIED (rewrite as RECOMMENDATION or remove)")
    check_links(path, text)


def check_template(path: Path) -> None:
    text = read(path)
    if not text.startswith("<!--"):
        err(f"{rel(path)}: template must start with an HTML comment header")
    head = text[: text.find("-->") if "-->" in text else 800]
    for key in TEMPLATE_HEADER_KEYS:
        if key not in head:
            err(f"{rel(path)}: template header lacks '{key}'")
    check_links(path, text)


def check_registry(reg: Dict[str, Any], skill_dirs: List[Path]) -> None:
    skills = reg.get("skills") or []
    artifacts = reg.get("artifacts") or []
    gates = reg.get("gates") or []
    workflows = reg.get("workflows") or []
    stages = set(reg.get("stages") or []) | {"all", "transversal"}
    externals = set(reg.get("external_inputs") or [])

    skill_names = {s.get("name") for s in skills}
    artifact_ids = {a.get("id") for a in artifacts}
    gate_ids = {g.get("id") for g in gates}
    dir_names = {d.name for d in skill_dirs}

    for missing in sorted(skill_names - dir_names):
        err(f"registry: skill {missing!r} has no skills/{missing}/SKILL.md")
    for missing in sorted(dir_names - skill_names):
        err(f"registry: directory skills/{missing} is not registered")

    for s in skills:
        n = s.get("name")
        if s.get("layer") not in ("orchestration", "discipline"):
            err(f"registry[{n}]: layer must be orchestration|discipline")
        if s.get("stage") not in stages:
            err(f"registry[{n}]: unknown stage {s.get('stage')!r}")
        for inp in s.get("inputs") or []:
            base = inp[:-1] if inp.endswith("?") else inp
            if base not in artifact_ids and base not in externals:
                err(f"registry[{n}]: input {inp!r} is neither an artifact nor an external input")
        for out in (s.get("outputs") or []) + (s.get("updates") or []):
            if out not in artifact_ids:
                err(f"registry[{n}]: output/update {out!r} is not a registered artifact")
        for h in s.get("handoffs") or []:
            if h not in skill_names:
                err(f"registry[{n}]: handoff to unknown skill {h!r}")
        for g in s.get("gates_after") or []:
            if g not in gate_ids:
                err(f"registry[{n}]: unknown gate {g!r}")
        for r in s.get("references") or []:
            if not (ROOT / r).exists():
                err(f"registry[{n}]: reference file missing {r}")
        for out in s.get("outputs") or []:
            producers = next((a.get("producers") or [] for a in artifacts if a.get("id") == out), [])
            if n not in producers:
                err(f"registry[{n}]: produces {out!r} but is not listed among its producers")

    skill_by_name = {s.get("name"): s for s in skills}
    for a in artifacts:
        aid = a.get("id")
        tpl = a.get("template")
        if tpl in (None, "none"):
            if not a.get("format"):
                err(f"registry artifact {aid}: needs a template or a format")
        elif not (ROOT / tpl).exists():
            err(f"registry artifact {aid}: template missing {tpl}")
        for who in (a.get("producers") or []) + (a.get("consumers") or []):
            if who not in skill_names:
                err(f"registry artifact {aid}: unknown skill {who!r}")
        if not a.get("default_path"):
            err(f"registry artifact {aid}: default_path missing")
        # graph consistency: producers must list the artifact in outputs; consumers must list it in inputs
        for who in a.get("producers") or []:
            s_ = skill_by_name.get(who)
            if s_ and aid not in (s_.get("outputs") or []) + (s_.get("updates") or []):
                err(f"registry artifact {aid}: producer {who!r} does not list it in outputs or updates")
        for who in a.get("consumers") or []:
            if who in skill_by_name:
                ins = {i[:-1] if i.endswith("?") else i for i in skill_by_name[who].get("inputs") or []}
                if aid not in ins:
                    err(f"registry artifact {aid}: consumer {who!r} does not list it in inputs")
        if not a.get("consumers"):
            warn(f"registry artifact {aid}: no consumers (documentation dead end?)")

    # every skill except the orchestrator must be reachable via some handoff
    handed = {h for s in skills for h in (s.get("handoffs") or [])}
    for n in skill_names:
        if n != "sdlc-orchestrator" and n not in handed:
            err(f"registry: skill {n!r} is never a handoff target")

    # workflow input-availability simulation (a required input must be produced by an earlier step or be a start input)
    starts = {
        "new-product": {"user-intent"},
        "add-feature": {"source-code", "change-request", "backlog-item", "user-intent"},
        "production-incident": {"source-code", "live-symptoms"},
        "legacy-modernization": {"source-code", "user-intent"},
        "hardening": {"source-code", "audit-findings", "user-intent"},
    }
    for w in workflows:
        have = set(starts.get(w.get("id"), {"user-intent", "source-code"}))
        for i, step in enumerate(w.get("sequence") or [], 1):
            s = skill_by_name.get(step)
            if not s:
                continue
            missing = [x for x in (s.get("inputs") or []) if not x.endswith("?") and x not in have]
            if missing:
                err(f"registry workflow {w.get('id')}: step {i} {step!r} needs {missing} which nothing earlier produces")
            have |= set(s.get("outputs") or []) | set(s.get("updates") or [])
            if step == "implementation":
                have |= {"source-code", "backlog-item"}
            if step == "agile-delivery":
                have.add("backlog-item")

    for g in gates:
        gfile = ROOT / (g.get("file") or "")
        if not gfile.exists():
            err(f"registry gate {g.get('id')}: file missing {g.get('file')}")
        elif g.get("id") not in read(gfile):
            err(f"registry gate {g.get('id')}: not described in {g.get('file')}")

    for w in workflows:
        wfile = ROOT / (w.get("file") or "")
        if not wfile.exists():
            err(f"registry workflow {w.get('id')}: file missing {w.get('file')}")
        for step in w.get("sequence") or []:
            if step not in skill_names:
                err(f"registry workflow {w.get('id')}: unknown skill {step!r} in sequence")
        if wfile.exists():
            text = read(wfile)
            for step in set(w.get("sequence") or []):
                if f"`{step}`" not in text and step not in text:
                    err(f"registry workflow {w.get('id')}: skill {step!r} not mentioned in {w.get('file')}")

    # templates referenced by no artifact
    for tpl in (ROOT / "templates").glob("*.md"):
        if tpl.name == "README.md":
            continue
        used = any(a.get("template") == f"templates/{tpl.name}" for a in artifacts)
        if not used:
            warn(f"{rel(tpl)}: template not referenced by any registry artifact")


def check_workflows(reg: Dict[str, Any]) -> None:
    """Every backticked hyphenated lowercase identifier in a workflow must be a known skill, gate or workflow id."""
    known = {s.get("name") for s in reg.get("skills") or []}
    known |= {g.get("id") for g in reg.get("gates") or []}
    known |= {w.get("id") for w in reg.get("workflows") or []}
    for wf in (ROOT / "workflows").glob("*.md"):
        text = read(wf)
        check_links(wf, text)
        if wf.name == "README.md":
            continue
        for m in re.finditer(r"`([a-z]+(?:-[a-z]+)+)`", text):
            token = m.group(1)
            if token not in known:
                warn(f"{rel(wf)}: backticked identifier {token!r} is not a known skill, gate or workflow")


def main(argv: List[str]) -> int:
    strict = "--strict" in argv
    registry_path = ROOT / "skills" / "registry.yaml"
    reg: Dict[str, Any] = {}
    if not registry_path.exists():
        err("skills/registry.yaml missing")
    else:
        try:
            reg = parse_yaml(read(registry_path))
        except YamlError as exc:
            err(f"skills/registry.yaml: {exc}")
            reg = {}

    skill_dirs = sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir())
    registry_names = {s.get("name") for s in (reg.get("skills") or [])}
    infos = [check_skill(d, registry_names) for d in skill_dirs]

    if reg:
        check_registry(reg, skill_dirs)
        check_workflows(reg)

    for tpl in (ROOT / "templates").glob("*.md"):
        if tpl.name != "README.md":
            check_template(tpl)
        else:
            check_links(tpl, read(tpl))
    for ref in (ROOT / "references").glob("*.md"):
        if ref.name != "README.md":
            check_reference(ref)
        else:
            check_links(ref, read(ref))
    for doc in list((ROOT / "docs").glob("*.md")) + list((ROOT / "docs" / "validation").glob("*.md")) + [ROOT / "README.md"]:
        if doc.exists():
            check_links(doc, read(doc))

    total_desc = sum(i["desc_len"] for i in infos)
    print("== Software Engineering Skills System - structural validation ==")
    print(f"skills: {len(infos)}   description chars total: {total_desc}   (always-loaded listing cost)")
    for i in sorted(infos, key=lambda x: -x["lines"])[:5]:
        print(f"  {i['name']:<22} {i['lines']:>4} lines  desc {i['desc_len']:>4} chars")
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"errors: {len(errors)}   warnings: {len(warnings)}")
    if errors or (strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

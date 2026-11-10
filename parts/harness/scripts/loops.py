#!/usr/bin/env python3
"""Loops of a project: the files under agentify/ and the checks on them.

    python3 loops.py init                        create agentify/ with the default policy, an empty profile, an empty log
                                                 and the registry
    python3 loops.py new ID --type TYPE          create agentify/loops/ID/ from the template; TYPE is a loop-type id or custom
    python3 loops.py validate ID [--runs N]      run the loop on its cases: must-fire fires, must-pass passes,
                                                 the same result every run, within budget_seconds
    python3 loops.py check                       agentify/ is consistent: files, fields, policy ids, agents, parts of
                                                 composite loops, registry
    python3 loops.py index                       rebuild agentify/loops/index.yaml from every LOOP.md
    python3 loops.py hitl HID --loop ID --question Q --answer A [--checked C]
                                                 log a call to a person under policy id HID
    python3 loops.py stats                       loops by status; calls to a person by policy id, by loop, repeated;
                                                 agents with their agreement and outcomes since their last evaluation
    python3 loops.py agent-new ID --kind KIND [--path P] [--model M] [--threshold T]
                                                 register an agent of a loop in agentify/agents.yaml, create its eval
                                                 folder and, if missing, its definition from the template
    python3 loops.py eval-score ID [--record]    score the agent's eval runs against the expected results: agreement,
                                                 flaky cases, threshold; --record writes report.md and the registry
    python3 loops.py outcome ID --loop L --outcome O [--note N]
                                                 log what happened to one of the agent's verdicts in real use
    python3 loops.py map                         the map of the project's super-loops: what stands at each phase,
                                                 from the profile and the loops' places, with the gaps and the pains
    python3 loops.py candidates PLACE            the loop types that can stand at PLACE (delivery/confirmation),
                                                 each with whether this project can run it
    python3 loops.py trace KIND PLACE --note N [--item I]
                                                 log what no system records: an escape, a correction or a revert,
                                                 at the place that should have caught it

    python3 loops.py migrate [--refs]            move a project of the harness plugin or of agentify 0.1 (loops/ and
                                                 specs/ at the root) into agentify/, and list the references to fix;
                                                 --refs only lists them

Options for every command: --root DIR (the project; default: the git top level of the current folder).

The contract for a loop's `run` command: it takes the directory to check as its only argument, exits 0 when the
check passes and non-zero when it fires, and prints what it found in a machine-readable form.
No dependencies beyond Python 3.
"""
import argparse
import collections
import datetime
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import time

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
HOME = "agentify"  # the project's folder: the policy, the profile, the logs and the agents; the loops in its agentify/loops/
STATUSES = ["proposed", "built", "validated", "active", "retired"]
AGENT_KINDS = {"reviewer", "refuter", "investigator", "judge", "explorer", "worker"}
AGENT_STATUSES = ["draft", "evaluated", "advisory", "gate", "retired"]
AGENT_FIELDS = ["id", "kind", "path", "model", "status", "blocks", "threshold", "threshold_source", "human_grades",
                "agreement", "runs", "evaluated_at", "evaluated_model", "prompt_hash"]
OUTCOMES = {"confirmed", "false-positive", "missed", "overridden"}
MIN_RUNS = 3
TRIGGERS = {"edit", "local", "commit", "ci", "preview", "staging", "production", "scheduled", "task", "sprint",
            "continuous"}
ALWAYS_STAGES = {"edit", "local", "commit", "task", "sprint", "continuous"}
TRACE_KINDS = {"escape", "correction", "revert"}
LIVE = ("validated", "active")


# ---------------------------------------------------------------- files

def project_root(arg):
    if arg:
        return pathlib.Path(arg).resolve()
    try:
        top = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                             check=True).stdout.strip()
        return pathlib.Path(top)
    except (OSError, subprocess.CalledProcessError):
        return pathlib.Path.cwd()


def frontmatter(text):
    """Scalars and flow lists only; a trailing `# comment` is ignored."""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    data = {}
    for line in m.group(1).splitlines():
        key, _, value = line.partition(":")
        value = value.strip()
        if value.startswith('"'):
            value = value[1:value.index('"', 1)] if '"' in value[1:] else value[1:]
        else:
            value = value.split(" #")[0].strip()
            if value.startswith("["):
                value = [v.strip() for v in value[1:value.rindex("]")].split(",") if v.strip()]
        data[key.strip()] = value
    return data


def super_loops():
    """{id: frontmatter} of the plugin's super-loop cards, in the order super-loops/README.md links them."""
    cards, folder = {}, PLUGIN / "super-loops"
    for path in sorted(folder.glob("*.md")):
        fm = frontmatter(path.read_text(encoding="utf-8"))
        if fm and fm.get("id") and fm.get("phases"):
            cards[fm["id"]] = fm
    readme = folder / "README.md"
    links = re.findall(r"\]\(([a-z-]+)\.md\)", readme.read_text(encoding="utf-8")) if readme.exists() else []
    order = [n for n in dict.fromkeys(links) if n in cards]
    return {n: cards[n] for n in order + [n for n in cards if n not in order]}


def place_problem(token, loops):
    """None for <super-loop>/<phase> or harness:<super-loop>/<phase> where that super-loop has that phase."""
    level, _, place = token.rpartition(":")
    loop, _, phase = place.partition("/")
    if level not in ("", "harness"):
        return "has an unknown level %r; the only one is harness" % level
    if loop not in loops:
        return "names no super-loop; they are %s" % ", ".join(loops)
    if phase not in loops[loop]["phases"]:
        return "names a phase that %s has not; it has %s" % (loop, ", ".join(loops[loop]["phases"]))
    return None


def places_in(text, loops):
    """The valid places written anywhere in a string, such as an entry of existing_checks or pains."""
    return [t for t in re.findall(r"(?:harness:)?[a-z]+/[a-z]+", text or "") if place_problem(t, loops) is None]


def read_profile(loops_dir):
    """agentify/profile.yaml in the subset it is written in: top-level scalars and flow lists, maps one level deep, and
    block lists of strings. Comments and blank lines are skipped."""
    path = loops_dir / "profile.yaml"
    data, key = {}, None
    for raw in path.read_text(encoding="utf-8").splitlines() if path.exists() else []:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_]\w*):\s*(.*)$", raw)
        if m:
            key, value = m.group(1), m.group(2).strip()
            data[key] = {} if value in ("", "{}") else None if value == "null" else parse_scalar(value)
            continue
        m = re.match(r"^\s+- (.*)$", raw)
        if m and key:
            if not isinstance(data.get(key), list):
                data[key] = []
            data[key].append(parse_scalar(m.group(1)))
            continue
        m = re.match(r"^\s+([A-Za-z_]\w*):\s*(.*)$", raw)
        if m and key:
            if not isinstance(data.get(key), dict):
                data[key] = {}
            value = m.group(2).strip()
            data[key][m.group(1)] = None if value == "null" else parse_scalar(value)
    return data


def catalog():
    """({type id: fields}, {place: [type ids]}) from the plugin's loop-types/index.yaml."""
    types, by_place, cur, section = {}, {}, None, None
    for line in (PLUGIN / "loop-types" / "index.yaml").read_text(encoding="utf-8").splitlines():
        if re.match(r"^\S", line):
            section = line.split(":")[0]
            continue
        if section == "loop_types":
            m = re.match(r"^  - id: (.+)$", line)
            if m:
                cur = types.setdefault(m.group(1).strip(), {"id": m.group(1).strip()})
                continue
            m = re.match(r"^    (\w+): (.*)$", line)
            if m and cur is not None:
                cur[m.group(1)] = parse_scalar(m.group(2))
        elif section == "by_place":
            m = re.match(r"^  (\S+): (.*)$", line)
            if m:
                by_place[m.group(1)] = parse_scalar(m.group(2))
    return types, by_place


def loops_at(loops_dir):
    """{place: [(loop id, status)]} from the places of every loop of the project."""
    at = collections.defaultdict(list)
    for d in loop_dirs(loops_dir):
        fm = (frontmatter((d / "LOOP.md").read_text(encoding="utf-8")) if (d / "LOOP.md").exists() else None) or {}
        for token in fm.get("places") or []:
            at[token].append((fm.get("id"), fm.get("status")))
    return at


def named_at(entries, loops):
    """{place: [names]} from profile entries written as "<name>: <places> — <details>"."""
    at = collections.defaultdict(list)
    for e in entries or []:
        name, _, rest = str(e).partition(":")
        for token in places_in(rest.split(" — ")[0], loops):  # the details may name a place too: not this entry's
            at[token].append(name.strip())
    return at


def policy_ids(loops_dir):
    path = loops_dir / "policy.yaml"
    return re.findall(r"^\s*- id: (H\d+)\s*$", path.read_text(encoding="utf-8"), re.M) if path.exists() else []


def home_of(root):
    return root / HOME


def loop_dirs(home):
    """Every loop folder, under agentify/loops/."""
    d = home / "loops"
    return sorted(p for p in d.iterdir() if p.is_dir() and not p.name.startswith(".")) if d.exists() else []


# ---------------------------------------------------------------- agents registry

def parse_scalar(value):
    value = value.strip()
    if value.startswith('"'):
        return json.loads(value)
    value = value.split(" #")[0].strip()
    if value.startswith("["):
        items = [v.strip() for v in value[1:value.rindex("]")].split(",") if v.strip()]
        return [json.loads(v) if v.startswith('"') else v for v in items]
    if value in ("true", "false"):
        return value == "true"
    if re.fullmatch(r"-?\d+(\.\d+)?", value):
        return float(value) if "." in value else int(value)
    return value


def read_agents(loops_dir):
    """agentify/agents.yaml as a list of dicts, or None when the project has no registry."""
    path = loops_dir / "agents.yaml"
    if not path.exists():
        return None
    agents, cur = [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^  - (\w+): (.*)$", line)
        if m:
            cur = {m.group(1): parse_scalar(m.group(2))}
            agents.append(cur)
            continue
        m = re.match(r"^    (\w+): (.*)$", line)
        if m and cur is not None:
            cur[m.group(1)] = parse_scalar(m.group(2))
    return agents


def write_agents(loops_dir, agents):
    path = loops_dir / "agents.yaml"
    old = path.read_text(encoding="utf-8") if path.exists() else (PLUGIN / "defaults" / "agents.yaml").read_text(
        encoding="utf-8")
    header = [l for l in old.splitlines() if l.startswith("#")]

    def fmt(v):
        if isinstance(v, bool):
            return "true" if v else "false"
        if isinstance(v, list):
            return "[%s]" % ", ".join(v)
        if isinstance(v, (int, float)):
            return str(v)
        v = str(v)
        return json.dumps(v, ensure_ascii=False) if re.search(r"[:#\[\]{}\"']|^\s|\s$", v) or v in ("true", "false") \
            else v
    out = header + [""]
    if not agents:
        out.append("agents: []")
    else:
        out.append("agents:")
        for a in agents:
            keys = AGENT_FIELDS + sorted(k for k in a if k not in AGENT_FIELDS)
            first = True
            for k in keys:
                if k in a and a[k] not in (None, ""):
                    out.append("%s%s: %s" % ("  - " if first else "    ", k, fmt(a[k])))
                    first = False
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def prompt_hash(root, rel):
    p = root / rel
    return hashlib.sha256(p.read_bytes()).hexdigest()[:12] if p.is_file() else None


def find_agent(agents, agent_id):
    for a in agents or []:
        if a.get("id") == agent_id:
            return a
    sys.exit("no agent %r in agentify/agents.yaml" % agent_id)


def build_index(loops_dir):
    out = ["# Generated by loops.py from every agentify/loops/<id>/LOOP.md. Do not edit by hand: run `loops.py index`.",
           "", "loops:"]
    for d in loop_dirs(loops_dir):
        fm = frontmatter((d / "LOOP.md").read_text(encoding="utf-8")) if (d / "LOOP.md").exists() else None
        if not fm:
            continue
        out.append("  - id: %s" % fm.get("id"))
        out.append("    title: %s" % json.dumps(fm.get("title", ""), ensure_ascii=False))
        for key in ("type", "status", "trigger", "places", "validation", "agents", "hitl", "parts"):
            v = fm.get(key)
            if v not in (None, "", []):
                out.append("    %s: %s" % (key, "[%s]" % ", ".join(v) if isinstance(v, list) else v))
    if len(out) == 3:
        out[-1] = "loops: []"
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- commands

def cmd_init(a, root):
    loops = home_of(root)
    (loops / "loops").mkdir(parents=True, exist_ok=True)
    made = []
    for name, make in (("policy.yaml", lambda p: shutil.copy(PLUGIN / "defaults" / "policy.yaml", p)),
                       ("profile.yaml", lambda p: shutil.copy(PLUGIN / "defaults" / "profile.yaml", p)),
                       ("hitl-log.jsonl", lambda p: p.write_text("", encoding="utf-8")),
                       ("agents.yaml", lambda p: shutil.copy(PLUGIN / "defaults" / "agents.yaml", p)),
                       (".gitignore", lambda p: p.write_text("# runs of the text-quality part\n.runs/\n", encoding="utf-8"))):
        if not (loops / name).exists():
            make(loops / name)
            made.append(name)
    (loops / "loops" / "index.yaml").write_text(build_index(loops), encoding="utf-8")
    made.append("loops/index.yaml")
    print("agentify/: %s" % ", ".join(made))
    if "policy.yaml" in made:
        print("agentify/policy.yaml is the plugin default: adjust it to the project and decide it with the user.")
    if "profile.yaml" in made:
        print("agentify/profile.yaml is empty: fill it from what you found and the setup form (profile.md).")


def catalog_entry(type_id):
    index = PLUGIN / "loop-types" / "index.yaml"
    if not index.exists():
        return None
    m = re.search(r"^  - id: %s\n((?:    .*\n)+)" % re.escape(type_id), index.read_text(encoding="utf-8"), re.M)
    if not m:
        return None
    entry = {}
    for line in m.group(1).splitlines():
        key, _, value = line.strip().partition(": ")
        entry[key] = json.loads(value) if value.startswith('"') else value
    return entry


def cmd_new(a, root):
    loops = home_of(root)
    if not (loops / "policy.yaml").exists():
        sys.exit("no agentify/policy.yaml: run `loops.py init` and set up the project first")
    if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", a.id):
        sys.exit("loop id must be kebab-case: %s" % a.id)
    d = loops / "loops" / a.id
    if d.exists():
        sys.exit("agentify/loops/%s already exists" % a.id)
    entry = None if a.type == "custom" else catalog_entry(a.type)
    if a.type != "custom" and entry is None:
        sys.exit("unknown loop type %r: see loop-types/index.yaml, or use --type custom" % a.type)
    text = (PLUGIN / "templates" / "LOOP.md").read_text(encoding="utf-8")
    title = a.title or (entry or {}).get("title") or a.id
    text = text.replace("id: <loop-id>", "id: %s" % a.id).replace("<loop-type-id>", a.type)
    text = text.replace('"<what the loop guards, in a few words>"', json.dumps(title, ensure_ascii=False))
    text = text.replace("# <title>", "# %s" % title)
    if entry and entry.get("stages"):
        text = text.replace("trigger: []", "trigger: %s" % entry["stages"], 1)
    (d / "cases" / "must-fire").mkdir(parents=True)
    (d / "cases" / "must-pass").mkdir(parents=True)
    (d / "LOOP.md").write_text(text, encoding="utf-8")
    run = d / "run"
    run.write_text("#!/bin/sh\n# Contract: $1 is the directory to check. Exit 0 = passes, non-zero = fires.\n"
                   "echo \"loop %s is not built yet\" >&2\nexit 2\n" % a.id, encoding="utf-8")
    run.chmod(0o755)
    (d / "CHANGELOG.md").write_text("# %s — changes\n\n- %s: proposed.\n" % (a.id, datetime.date.today()),
                                    encoding="utf-8")
    (loops / "loops" / "index.yaml").write_text(build_index(loops), encoding="utf-8")
    print("created agentify/loops/%s/: LOOP.md, run, cases/must-fire/, cases/must-pass/, CHANGELOG.md" % a.id)
    if entry:
        print("loop type: %s — %s" % (entry["path"], entry.get("summary", "")))
        if entry.get("places"):
            print("places this type can take (write the ones it takes here into places): %s" % entry["places"])


def run_once(cmd, case, root, timeout):
    start = time.monotonic()
    try:
        p = subprocess.run(cmd + [str(case)], cwd=root, capture_output=True, text=True, timeout=timeout,
                           stdin=subprocess.DEVNULL)
        code, out = p.returncode, (p.stdout + p.stderr).strip()
    except subprocess.TimeoutExpired:
        code, out = None, "timeout after %ss" % timeout
    return code, out, time.monotonic() - start


def cmd_validate(a, root):
    d = home_of(root) / "loops" / a.id
    fm = frontmatter((d / "LOOP.md").read_text(encoding="utf-8")) if (d / "LOOP.md").exists() else None
    if not fm:
        sys.exit("agentify/loops/%s/LOOP.md is missing or has no frontmatter" % a.id)
    if fm.get("validation") == "manual":
        print("agentify/loops/%s: validation is manual — see its Validation section." % a.id)
        return
    run = fm.get("run") or "./run"
    cmd = [str((d / run).resolve())] if run.startswith("./") else run.split()
    budget = float(fm.get("budget_seconds") or 10)
    rows, failures = [], []
    for kind, expect_fire in (("must-fire", True), ("must-pass", False)):
        cases = sorted(p for p in (d / "cases" / kind).iterdir() if p.is_dir()) if (d / "cases" / kind).exists() else []
        if not cases:
            failures.append("no %s cases" % kind)
        for case in cases:
            results = [run_once(cmd, case, root, max(budget * 3, 30)) for _ in range(a.runs)]
            codes = {r[0] for r in results}
            outs = {r[1] for r in results}
            worst = max(r[2] for r in results)
            code = results[0][0]
            fired = code not in (0, None)
            problems = []
            if code is None:
                problems.append("timeout")
            elif fired != expect_fire:
                problems.append("fired" if fired else "did not fire")
            if fired and not results[0][1]:
                problems.append("fired with no output")
            if len(codes) > 1 or len(outs) > 1:
                problems.append("different results across runs")
            if worst > budget:
                problems.append("%.1fs > budget %.0fs" % (worst, budget))
            rows.append({"kind": kind, "case": case.name, "exit": code, "seconds": round(worst, 2),
                         "ok": not problems, "problems": problems, "output": results[0][1][:400]})
            if problems:
                failures.append("%s/%s: %s" % (kind, case.name, ", ".join(problems)))
    if a.json:
        print(json.dumps({"loop": a.id, "ok": not failures, "cases": rows, "failures": failures}, indent=1))
    else:
        print("| case | expected | exit | seconds | result |")
        print("|---|---|---|---|---|")
        for r in rows:
            print("| %s/%s | %s | %s | %s | %s |" % (r["kind"], r["case"], "fire" if r["kind"] == "must-fire" else "pass",
                                                  r["exit"], r["seconds"], "ok" if r["ok"] else ", ".join(r["problems"])))
        print("\n%s: %s" % ("VALID" if not failures else "NOT VALID", "; ".join(failures) or
                            "%d cases, %d runs each" % (len(rows), a.runs)))
    sys.exit(1 if failures else 0)


def cmd_check(a, root):
    loops = home_of(root)
    errors = []
    if not (loops / "policy.yaml").exists():
        sys.exit("no agentify/policy.yaml: the project is not set up (loops.py init)")
    ids = set(policy_ids(loops))
    if not ids:
        errors.append("policy.yaml: no policy ids (- id: H1 …)")
    loop_cards = super_loops()
    status_of, parts_of, agents_of = {}, {}, {}
    for d in loop_dirs(loops):
        fm = frontmatter((d / "LOOP.md").read_text(encoding="utf-8")) if (d / "LOOP.md").exists() else None
        if fm:
            status_of[d.name] = fm.get("status")
            parts_of[d.name] = fm.get("parts") or []
            agents_of[d.name] = fm.get("agents") or []
    for d in loop_dirs(loops):
        rel = "agentify/loops/%s" % d.name
        if not (d / "LOOP.md").exists():
            errors.append("%s: no LOOP.md" % rel)
            continue
        text = (d / "LOOP.md").read_text(encoding="utf-8")
        fm = frontmatter(text)
        if not fm:
            errors.append("%s/LOOP.md: no frontmatter" % rel)
            continue
        if fm.get("id") != d.name:
            errors.append("%s/LOOP.md: id %r does not match the folder" % (rel, fm.get("id")))
        if fm.get("status") not in STATUSES:
            errors.append("%s/LOOP.md: status %r is not one of %s" % (rel, fm.get("status"), ", ".join(STATUSES)))
        for t in fm.get("trigger") or []:
            if t not in TRIGGERS:
                errors.append("%s/LOOP.md: trigger %r is not in the vocabulary" % (rel, t))
        if "<" in fm.get("title", "<"):
            errors.append("%s/LOOP.md: title is still the template placeholder" % rel)
        for h in fm.get("hitl") or []:
            if h not in ids:
                errors.append("%s/LOOP.md: hitl %r is not in agentify/policy.yaml" % (rel, h))
        for agent in fm.get("agents") or []:
            if not (root / agent).exists():
                errors.append("%s/LOOP.md: agent %s does not exist" % (rel, agent))
        run = fm.get("run") or "./run"
        if run.startswith("./") and not os.access(d / run, os.X_OK):
            errors.append("%s: %s is missing or not executable" % (rel, run))
        live = fm.get("status") in ("validated", "active")
        if live and fm.get("validation") != "manual":
            for kind in ("must-fire", "must-pass"):
                if not any(p.is_dir() for p in (d / "cases" / kind).glob("*")):
                    errors.append("%s: status %s but no %s cases" % (rel, fm.get("status"), kind))
        if live and fm.get("validation") == "manual" and not re.search(r"## Validation\n\n[^<\s]", text):
            errors.append("%s: manual validation but the Validation section is empty" % rel)
        if live and not fm.get("wiring"):
            errors.append("%s: status %s but no wiring" % (rel, fm.get("status")))
        # a loop's places: where it stands in the super-loops
        for token in fm.get("places") or []:
            problem = place_problem(token, loop_cards)
            if problem:
                errors.append("%s/LOOP.md: place %r %s" % (rel, token, problem))
        if live and not fm.get("places"):
            errors.append("%s: status %s but no places: say where it stands, as <super-loop>/<phase>"
                          % (rel, fm.get("status")))
        # a composite loop: its parts exist, contain no cycle, and are at least as far along as the whole
        rank = {s: i for i, s in enumerate(STATUSES)}
        for part in parts_of.get(d.name, []):
            if part == d.name:
                errors.append("%s/LOOP.md: lists itself in parts" % rel)
            elif part not in status_of:
                errors.append("%s/LOOP.md: part %r is not a loop under agentify/loops/" % (rel, part))
            elif fm.get("status") in ("validated", "active") and \
                    rank.get(status_of[part], -1) < rank[fm.get("status")]:
                errors.append("%s: status %s but its part %s is %s" % (rel, fm.get("status"), part,
                                                                       status_of[part]))
        seen, stack = set(), list(parts_of.get(d.name, []))
        while stack:
            p = stack.pop()
            if p == d.name:
                errors.append("%s/LOOP.md: parts form a cycle back to %s" % (rel, d.name))
                break
            if p not in seen:
                seen.add(p)
                stack += parts_of.get(p, [])
    errors += check_agents(root, loops, status_of, agents_of)
    index = loops / "loops" / "index.yaml"
    if not index.exists() or index.read_text(encoding="utf-8") != build_index(loops):
        errors.append("agentify/loops/index.yaml is out of date: run loops.py index")
    agents = read_agents(loops) or []
    print("\n".join(errors) if errors else "OK: %d loops, %d agents" % (len(loop_dirs(loops)), len(agents)))
    sys.exit(1 if errors else 0)


def check_agents(root, loops, status_of, agents_of):
    """The registry is consistent with the loops, and no agent blocks before it is calibrated."""
    errors = []
    agents = read_agents(loops)
    used = {p for paths in agents_of.values() for p in paths}
    if agents is None:
        if used:
            errors.append("loops use agents (%s) but agentify/agents.yaml is missing: register them with "
                          "loops.py agent-new" % ", ".join(sorted(used)))
        return errors
    by_path, ids = {}, set()
    for a in agents:
        aid = a.get("id", "?")
        where = "agentify/agents.yaml [%s]" % aid
        if aid in ids:
            errors.append("%s: id used twice" % where)
        ids.add(aid)
        by_path[a.get("path")] = a
        kind, status = str(a.get("kind", "")), a.get("status")
        if kind not in AGENT_KINDS and not kind.startswith("other:"):
            errors.append("%s: kind %r is not one of %s, nor other:<name>" % (where, kind, ", ".join(sorted(AGENT_KINDS))))
        if status not in AGENT_STATUSES:
            errors.append("%s: status %r is not one of %s" % (where, status, ", ".join(AGENT_STATUSES)))
        if status == "retired":
            continue
        current = prompt_hash(root, a.get("path", ""))
        if current is None:
            errors.append("%s: definition %s does not exist" % (where, a.get("path")))
        if a.get("blocks") is True and status != "gate":
            errors.append("%s: blocks, but its status is %s: an agent that is not gate advises, it does not block"
                          % (where, status))
        if status in ("evaluated", "advisory", "gate") and not a.get("prompt_hash"):
            errors.append("%s: status %s but it was never evaluated: run its evals and eval-score --record"
                          % (where, status))
        elif status in ("evaluated", "advisory", "gate"):
            if current and a.get("prompt_hash") != current:
                errors.append("%s: the definition changed since its evaluation: run its evals and eval-score --record"
                              % where)
            if a.get("evaluated_model") != a.get("model"):
                errors.append("%s: model %s, but it was evaluated with %s: evaluate it again"
                              % (where, a.get("model"), a.get("evaluated_model")))
        if status == "gate":
            threshold, agreement = a.get("threshold"), a.get("agreement")
            if not isinstance(threshold, (int, float)):
                errors.append("%s: gate without a threshold" % where)
            elif not isinstance(agreement, (int, float)) or agreement < threshold:
                errors.append("%s: gate, but agreement %s is below its threshold %s" % (where, agreement, threshold))
            if not a.get("threshold_source"):
                errors.append("%s: gate, but threshold_source does not say who approved the threshold (H5)" % where)
            if not isinstance(a.get("runs"), int) or a.get("runs") < MIN_RUNS:
                errors.append("%s: gate with fewer than %d eval runs" % (where, MIN_RUNS))
            if kind == "judge" and a.get("human_grades") is not True:
                errors.append("%s: a judge is gate only when calibrated on a person's grades (human_grades: true)"
                              % where)
    for loop, paths in agents_of.items():
        for path in paths:
            a = by_path.get(path)
            if a is None:
                errors.append("agentify/loops/%s/LOOP.md: agent %s is not registered in agentify/agents.yaml" % (loop, path))
            elif a.get("status") == "draft" and status_of.get(loop) in ("validated", "active"):
                errors.append("agentify/loops/%s: status %s, but its agent %s has no evaluation yet (draft)"
                              % (loop, status_of.get(loop), a.get("id")))
    return errors


def cmd_agent_new(a, root):
    loops = home_of(root)
    if not (loops / "policy.yaml").exists():
        sys.exit("no agentify/policy.yaml: run `loops.py init` and set up the project first")
    if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", a.id):
        sys.exit("agent id must be kebab-case: %s" % a.id)
    if a.kind not in AGENT_KINDS and not a.kind.startswith("other:"):
        sys.exit("kind must be one of %s, or other:<name>" % ", ".join(sorted(AGENT_KINDS)))
    agents = read_agents(loops) or []
    if any(x.get("id") == a.id for x in agents):
        sys.exit("agent %s is already registered" % a.id)
    path = a.path or ".claude/agents/%s.md" % a.id
    made = []
    if not (root / path).exists():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        text = (PLUGIN / "templates" / "agent.md").read_text(encoding="utf-8")
        text = text.replace("<agent-name>", a.id).replace("<kind>", a.kind)
        if a.model:
            text = text.replace("<model id, or inherit>", a.model)
        (root / path).write_text(text, encoding="utf-8")
        made.append(path)
    d = loops / "agents" / a.id
    (d / "evals").mkdir(parents=True, exist_ok=True)
    (d / "results").mkdir(exist_ok=True)
    made.append("agentify/agents/%s/evals/, results/" % a.id)
    entry = {"id": a.id, "kind": a.kind, "path": path, "model": a.model or "inherit", "status": "draft",
             "blocks": False}
    if a.threshold is not None:
        entry["threshold"] = a.threshold
    agents.append(entry)
    write_agents(loops, agents)
    made.append("agentify/agents.yaml entry (draft)")
    print("created: %s" % "; ".join(made))
    print("next: write the definition, add eval cases (agent-formats.md, Evals), run the agent %d times on every "
          "case, then loops.py eval-score %s --record" % (MIN_RUNS, a.id))


def case_matches(expected, got):
    """One run's output on one case against what the case expects (agent-formats.md, Evals)."""
    if got is None:
        return False
    if "verdict" in expected:
        return got.get("verdict") == expected["verdict"]
    want, found = expected.get("findings") or [], got.get("findings") or []
    if not want:
        return not any(f.get("severity") == "high" for f in found)

    def hit(w, f):
        if w.get("file") and f.get("file") != w.get("file"):
            return False
        if w.get("line") is not None and (f.get("line") is None or abs(int(f["line"]) - int(w["line"])) > 3):
            return False
        return not w.get("rule") or f.get("rule") == w.get("rule")
    return all(any(hit(w, f) for f in found) for w in want)


def cmd_eval_score(a, root):
    loops = home_of(root)
    agents = read_agents(loops)
    agent = find_agent(agents, a.id)
    d = loops / "agents" / a.id
    cases = sorted(p for p in (d / "evals").iterdir() if p.is_dir()) if (d / "evals").exists() else []
    if not cases:
        sys.exit("agentify/agents/%s/evals/ has no cases" % a.id)
    problems, expected = [], {}
    for c in cases:
        if not (c / "expected.json").exists():
            problems.append("%s: no expected.json" % c.name)
        else:
            expected[c.name] = json.loads((c / "expected.json").read_text(encoding="utf-8"))
    run_files = sorted((d / "results").glob("*.jsonl")) if (d / "results").exists() else []
    if not run_files:
        sys.exit("agentify/agents/%s/results/ has no runs: run the agent on every case, one .jsonl file per run" % a.id)
    runs = []
    for f in run_files:
        lines = [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
        runs.append({x.get("case"): x for x in lines})
    definition = root / agent.get("path", "")
    if definition.is_file():
        stale = [f.name for f in run_files if f.stat().st_mtime < definition.stat().st_mtime]
        if stale:
            problems.append("run(s) %s are older than the agent's definition: run the agent again with the current "
                            "definition" % ", ".join(stale))
    if len(runs) < MIN_RUNS:
        problems.append("%d run(s); at least %d are needed, the agent's output differs from run to run"
                        % (len(runs), MIN_RUNS))
    rows, total, matched, flaky = [], 0, 0, []
    for name, exp in expected.items():
        hits = [case_matches(exp, r.get(name)) for r in runs]
        missing = sum(r.get(name) is None for r in runs)
        if missing:
            problems.append("%s: no result in %d run(s)" % (name, missing))
        kind = "verdict %s" % exp["verdict"] if "verdict" in exp else ("must-pass" if not exp.get("findings")
                                                                        else "must-fire")
        rows.append((name, kind, sum(hits), len(hits)))
        total += len(hits)
        matched += sum(hits)
        if 0 < sum(hits) < len(hits):
            flaky.append(name)
    agreement = matched / total if total else 0.0
    threshold = agent.get("threshold")
    table = ["| case | expects | matched | runs |", "|---|---|---|---|"]
    table += ["| %s | %s | %d | %d |" % r for r in rows]
    verdict = "no threshold set" if not isinstance(threshold, (int, float)) else (
        "meets the threshold %s" % threshold if agreement >= threshold else "BELOW the threshold %s" % threshold)
    summary = "agreement %.0f%% (%d of %d case runs), %d cases x %d runs; %s" % (
        agreement * 100, matched, total, len(expected), len(runs), verdict)
    print("\n".join(table))
    print("\n" + summary)
    if flaky:
        print("flaky (differ between runs): %s" % ", ".join(flaky))
    for p in problems:
        print("problem: %s" % p)
    if a.record:
        today = datetime.date.today().isoformat()
        (d / "report.md").write_text("# %s: evaluation %s\n\n%s\n\n%s\n%s%s" % (
            a.id, today, "\n".join(table), summary,
            ("\nFlaky: %s\n" % ", ".join(flaky)) if flaky else "",
            "".join("\nProblem: %s" % p for p in problems)), encoding="utf-8")
        agent.update({"agreement": round(agreement, 3), "runs": len(runs), "evaluated_at": today,
                      "evaluated_model": agent.get("model"), "prompt_hash": prompt_hash(root, agent.get("path", ""))})
        if agent.get("status") == "draft":
            agent["status"] = "evaluated"
        write_agents(loops, agents)
        print("recorded in agentify/agents.yaml and agentify/agents/%s/report.md" % a.id)
    below = isinstance(threshold, (int, float)) and agreement < threshold
    sys.exit(1 if problems or below else 0)


def cmd_outcome(a, root):
    loops = home_of(root)
    find_agent(read_agents(loops), a.id)
    if a.outcome not in OUTCOMES:
        sys.exit("outcome must be one of %s" % ", ".join(sorted(OUTCOMES)))
    entry = {"at": datetime.datetime.now().isoformat(timespec="seconds"), "agent": a.id, "loop": a.loop,
             "outcome": a.outcome, "note": a.note}
    with open(loops / "agent-outcomes.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print("logged %s for %s" % (a.outcome, a.id))


def cmd_index(a, root):
    (home_of(root) / "loops" / "index.yaml").write_text(build_index(home_of(root)), encoding="utf-8")
    print("wrote agentify/loops/index.yaml (%d loops)" % len(loop_dirs(home_of(root))))


def cmd_hitl(a, root):
    loops = home_of(root)
    if a.policy_id not in policy_ids(loops):
        sys.exit("%s is not in agentify/policy.yaml: calling a person is not allowed for it" % a.policy_id)
    entry = {"at": datetime.datetime.now().isoformat(timespec="seconds"), "policy": a.policy_id, "loop": a.loop,
             "checked": a.checked, "question": a.question, "answer": a.answer}
    with open(loops / "hitl-log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print("logged %s call for %s" % (a.policy_id, a.loop))


def cmd_stats(a, root):
    loops = home_of(root)
    statuses = collections.Counter()
    for d in loop_dirs(loops):
        fm = frontmatter((d / "LOOP.md").read_text(encoding="utf-8")) if (d / "LOOP.md").exists() else None
        statuses[(fm or {}).get("status", "?")] += 1
    calls = [json.loads(l) for l in (loops / "hitl-log.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()] \
        if (loops / "hitl-log.jsonl").exists() else []
    print("loops: %s" % (", ".join("%s %d" % kv for kv in sorted(statuses.items())) or "none"))
    print("calls to a person: %d" % len(calls))
    for key in ("policy", "loop"):
        c = collections.Counter(x.get(key) for x in calls)
        if c:
            print("  by %s: %s" % (key, ", ".join("%s %d" % kv for kv in c.most_common())))
    agents = read_agents(loops) or []
    outcomes = [json.loads(l) for l in (loops / "agent-outcomes.jsonl").read_text(encoding="utf-8").splitlines()
                if l.strip()] if (loops / "agent-outcomes.jsonl").exists() else []
    for ag in agents:
        since = str(ag.get("evaluated_at") or "")
        mine = [o for o in outcomes if o.get("agent") == ag.get("id") and o.get("at", "") > since]
        c = collections.Counter(o.get("outcome") for o in mine)
        print("agent %s (%s, %s): agreement %s, threshold %s; since its evaluation: %s" % (
            ag.get("id"), ag.get("kind"), ag.get("status"), ag.get("agreement", "-"), ag.get("threshold", "-"),
            ", ".join("%s %d" % kv for kv in sorted(c.items())) or "no outcomes"))
        if c["false-positive"] + c["missed"] >= 2:
            print("  -> add its false positives and misses as eval cases and run eval-score again")
    norm = collections.Counter(re.sub(r"\W+", " ", (x.get("question") or "").lower()).strip() for x in calls)
    repeated = [(q, n) for q, n in norm.items() if q and n > 1]
    if repeated:
        print("asked more than once (candidates to automate or to settle in the policy):")
        for q, n in sorted(repeated, key=lambda x: -x[1]):
            print("  %d× %s" % (n, q[:120]))
    print_trace(root, loops)


def cmd_map(a, root):
    loops_dir = home_of(root)
    if not (loops_dir / "profile.yaml").exists():
        sys.exit("no agentify/profile.yaml: run `loops.py init` and fill the profile first")
    prof, cards = read_profile(loops_dir), super_loops()
    built, checks = loops_at(loops_dir), named_at(prof.get("existing_checks"), cards)
    pains = named_at(prof.get("pains"), cards)
    has, not_here = prof.get("super_loops") or {}, prof.get("not_here") or {}
    tools = ", ".join(prof.get("tools") or {}) or "none"
    print("Profile: %s · stages %s · tools %s" % (", ".join(prof.get("kind") or []) or "?",
                                                 ", ".join(prof.get("stages") or []) or "local only", tools))
    print("Ends at: %s" % (prof.get("ends_at") or "?"))
    if pains:
        print("Pains: %s" % ", ".join("%s (%s)" % (", ".join(n), p) for p, n in pains.items()))
    print()
    for loop, card in cards.items():
        if loop in not_here:
            print("%-12s not here: %s" % (loop, not_here[loop]))
            continue
        if loop not in has:
            print("%-12s not in the profile: add it to super_loops or not_here" % loop)
            continue
        cells = []
        for phase in card["phases"]:
            token = "%s/%s" % (loop, phase)
            live = [i for i, s in built.get(token, []) if s in LIVE]
            pending = ["%s (%s)" % (i, s) for i, s in built.get(token, []) if s not in LIVE + ("retired",)]
            names = live + checks.get(token, [])
            if names:
                cell = "%s ✓ %s" % (phase, ", ".join(names))
            elif phase == "entry":
                cell = "entry: %s" % re.split(r"[;:,]", str(has[loop]))[0][:48]
            else:
                cell = "%s ✗" % phase
            if pending:
                cell += " + %s" % ", ".join(pending)
            if token in pains:
                cell += " ! %s" % ", ".join(pains[token])
            cells.append(cell)
        print("%-12s %s" % (loop, " · ".join(cells)))
    harness = sorted({"%s (%s)" % (i, t.split(":", 1)[1]) for t, ls in built.items() if t.startswith("harness:")
                      for i, s in ls if s in LIVE})
    if harness:
        print("%-12s %s" % ("harness", ", ".join(harness)))


def cmd_candidates(a, root):
    loops_dir, cards = home_of(root), super_loops()
    problem = place_problem(a.place, cards)
    if problem:
        sys.exit("place %r %s" % (a.place, problem))
    types, by_place = catalog()
    prof = read_profile(loops_dir)
    stages = set(prof.get("stages") or []) | ALWAYS_STAGES
    tools = set(prof.get("tools") or {})
    here = ["%s (%s)" % (i, s) for i, s in loops_at(loops_dir).get(a.place, [])] + \
        named_at(prof.get("existing_checks"), cards).get(a.place, [])
    ids = by_place.get(a.place) or []
    print("%s: %d loop types can stand here%s" % (a.place, len(ids), "; already here: " + ", ".join(here) if here else ""))
    for i in ids:
        t = types.get(i, {})
        why = []
        runs = t.get("stages") or []
        if runs and not set(runs) & stages:
            why.append("runs at %s, which the project does not have" % ", ".join(runs))
        missing = [n for n in t.get("needs") or [] if n not in tools]
        if missing:
            why.append("needs %s, which the agent cannot reach" % ", ".join(missing))
        print("  %-32s %s" % (i, "fits" if not why else "no: " + "; ".join(why)))


def cmd_trace(a, root):
    loops = home_of(root)
    if a.kind not in TRACE_KINDS:
        sys.exit("kind must be one of %s" % ", ".join(sorted(TRACE_KINDS)))
    problem = place_problem(a.place, super_loops())
    if problem:
        sys.exit("place %r %s" % (a.place, problem))
    entry = {"at": datetime.datetime.now().isoformat(timespec="seconds"), "kind": a.kind, "place": a.place,
             "item": a.item, "note": a.note}
    with open(loops / "trace.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print("logged %s at %s" % (a.kind, a.place))


OLD_FILES = ["policy.yaml", "profile.yaml", "hitl-log.jsonl", "trace.jsonl", "agent-outcomes.jsonl", "agents.yaml"]


def git_move(root, src, dst):
    """git mv when git tracks src, a plain move when it does not."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    rel = lambda p: str(p.relative_to(root))
    tracked = subprocess.run(["git", "-C", str(root), "ls-files", "--error-unmatch", rel(src)],
                             capture_output=True).returncode == 0
    if tracked:
        subprocess.run(["git", "-C", str(root), "mv", rel(src), rel(dst)], check=True)
    else:
        shutil.move(str(src), str(dst))


OLD_PATH = re.compile(r"(?<![\w.-])(?<!agentify/)(?:loops|specs)/|[\"'](?:loops|specs)[\"']")


def old_path_refs(root):
    """Every line of the tracked files that names loops/ or specs/ outside agentify/: a path such as loops/x/run or
    $REPO/specs/, or a path built from its parts, such as repo / "specs"."""
    files = subprocess.run(["git", "-C", str(root), "ls-files", "-z"], capture_output=True, text=True).stdout
    refs = []
    for rel in filter(None, files.split("\0")):
        try:
            lines = (root / rel).read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        refs += ["%s:%d: %s" % (rel, n, line.strip()) for n, line in enumerate(lines, 1) if OLD_PATH.search(line)]
    return refs


def print_refs(root):
    refs = old_path_refs(root)
    print("references to the old paths, to fix (%d):" % len(refs))
    for r in refs:
        print("  " + r[:200])


def cmd_migrate(a, root):
    if a.refs:
        return print_refs(root)
    old, home = root / "loops", home_of(root)
    if (home / "policy.yaml").exists():
        sys.exit("agentify/policy.yaml exists: the project is in agentify/ already")
    if not (old / "policy.yaml").exists():
        sys.exit("no loops/policy.yaml: nothing to move; a new project starts with loops.py init")
    moved = []
    for name in OLD_FILES:
        if (old / name).exists():
            git_move(root, old / name, home / name)
            moved.append(name)
    if (old / "agents").is_dir():
        git_move(root, old / "agents", home / "agents")
        moved.append("agents/")
    for d in sorted(p for p in old.iterdir() if p.is_dir() and not p.name.startswith(".")):
        git_move(root, d, home / "loops" / d.name)
        moved.append("loops/%s/" % d.name)
    if (old / "index.yaml").exists():
        git_move(root, old / "index.yaml", home / "loops" / "index.yaml")
    if (root / "specs").is_dir():
        git_move(root, root / "specs", home / "specs")
        moved.append("specs/")
    if old.exists() and not any(old.iterdir()):
        old.rmdir()
    if not (home / ".gitignore").exists():
        (home / ".gitignore").write_text("# runs of the text-quality part\n.runs/\n", encoding="utf-8")
    (home / "loops" / "index.yaml").write_text(build_index(home), encoding="utf-8")
    print("moved into agentify/: %s" % ", ".join(moved))
    if old.exists():
        print("left in loops/: %s" % ", ".join(sorted(p.name for p in old.iterdir())))
    if (root / ".text-quality-runs").exists():
        print(".text-quality-runs/ stays where it is: new runs go to agentify/.runs/")
    print_refs(root)


def trace_records(root, prof):
    """The exits the project's own systems record: JSON lines from every file in the profile's trace."""
    records, missing = [], []
    for src in prof.get("trace") or []:
        path = pathlib.Path(os.path.expanduser(str(src)))
        path = path if path.is_absolute() else root / path
        if not path.exists():
            missing.append(str(src))
            continue
        for raw in path.read_text(encoding="utf-8").splitlines():
            try:
                records.append(json.loads(raw))
            except ValueError:
                continue
    return records, missing


def print_trace(root, loops):
    prof = read_profile(loops)
    records, missing = trace_records(root, prof)
    own = [json.loads(l) for l in (loops / "trace.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()] \
        if (loops / "trace.jsonl").exists() else []
    for src in missing:
        print("trace: %s is not there" % src)
    judged = [r for r in records if r.get("action") == "confirm"]
    if judged:
        c = collections.Counter(r.get("result") for r in judged)
        print("releases judged: %d — %s" % (len(judged), ", ".join("%s %d" % kv for kv in sorted(c.items()))))
        decided = c["confirmed"] + c["not-confirmed"]
        if decided:
            print("  change failure rate: %d%% (not confirmed, of the releases confirmed or not)"
                  % round(100.0 * c["not-confirmed"] / decided))
        print("  rollbacks: %d" % sum(1 for r in records if r.get("action") == "rollback"))
        analysed = {e.get("item") for e in own if e.get("kind") == "escape"}
        todo = [r for r in judged if r.get("result") == "not-confirmed" and r.get("version") not in analysed]
        for r in todo:
            print("  not confirmed: %s at %s, evidence %s" % (r.get("version"), r.get("at"), r.get("evidence") or "-"))
        if todo:
            print("  -> for each, find the phase that should have caught it (loop type steering-loop) and log it:")
            print("     loops.py trace escape <super-loop>/<phase> --item <version> --note \"…\"")
        deploys = [r for r in records if r.get("action") == "deploy" and r.get("result") == "ok"]
        never = [r.get("version") for r in deploys if not any(
            j.get("version") == r.get("version") and j.get("at", "") >= r.get("at", "") for j in judged)]
        if never:
            print("  deployed without a verdict yet: %s" % ", ".join(never))
    elif prof.get("trace"):
        print("releases judged: none yet")
    if own:
        by_place = collections.Counter(e.get("place") for e in own)
        print("escapes, corrections and reverts by place: %s" % ", ".join("%s %d" % kv for kv in by_place.most_common()))
        for place, n in by_place.most_common():
            if n >= 2:
                print("  -> %s: %d times; the loop at this place is missing or too weak" % (place, n))


def main():
    ap = argparse.ArgumentParser(description="Loops of a project", epilog=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init").set_defaults(fn=cmd_init)
    p = sub.add_parser("new")
    p.add_argument("id")
    p.add_argument("--type", required=True)
    p.add_argument("--title")
    p.set_defaults(fn=cmd_new)
    p = sub.add_parser("validate")
    p.add_argument("id")
    p.add_argument("--runs", type=int, default=2)
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_validate)
    sub.add_parser("check").set_defaults(fn=cmd_check)
    sub.add_parser("index").set_defaults(fn=cmd_index)
    p = sub.add_parser("hitl")
    p.add_argument("policy_id")
    p.add_argument("--loop", default="-")
    p.add_argument("--question", required=True)
    p.add_argument("--answer", required=True)
    p.add_argument("--checked", default="")
    p.set_defaults(fn=cmd_hitl)
    sub.add_parser("stats").set_defaults(fn=cmd_stats)
    p = sub.add_parser("agent-new")
    p.add_argument("id")
    p.add_argument("--kind", required=True)
    p.add_argument("--path")
    p.add_argument("--model")
    p.add_argument("--threshold", type=float)
    p.set_defaults(fn=cmd_agent_new)
    p = sub.add_parser("eval-score")
    p.add_argument("id")
    p.add_argument("--record", action="store_true")
    p.set_defaults(fn=cmd_eval_score)
    p = sub.add_parser("outcome")
    p.add_argument("id")
    p.add_argument("--loop", required=True)
    p.add_argument("--outcome", required=True)
    p.add_argument("--note", default="")
    p.set_defaults(fn=cmd_outcome)
    sub.add_parser("map").set_defaults(fn=cmd_map)
    p = sub.add_parser("migrate")
    p.add_argument("--refs", action="store_true", help="only list the references to the old paths")
    p.set_defaults(fn=cmd_migrate)
    p = sub.add_parser("candidates")
    p.add_argument("place")
    p.set_defaults(fn=cmd_candidates)
    p = sub.add_parser("trace")
    p.add_argument("kind")
    p.add_argument("place")
    p.add_argument("--note", required=True)
    p.add_argument("--item", default="")
    p.set_defaults(fn=cmd_trace)
    a = ap.parse_args()
    a.fn(a, project_root(a.root))


if __name__ == "__main__":
    main()

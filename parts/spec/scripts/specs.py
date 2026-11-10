#!/usr/bin/env python3
"""spec: a project's specs/ folder — requirements, the chosen spec layers, traceability and the delta for tests.

  specs.py init      [--root .]                       create specs/ from the defaults
  specs.py new-req   <key> [--source URL] [--root .]  create specs/requirements/<key>.yaml
  specs.py check     [--root .]                       policy, profile, layers, requirements, requirement <-> spec trace
  specs.py trace     [--root .] [--req KEY]           which spec elements cover each requirement, and the reverse
  specs.py delta     [--root .] [--base REF]          spec elements added, changed and removed since REF: the test
                                                      writer's work list (default REF: HEAD)
  specs.py signals   [--root .] (--req KEY | --base REF) [--out FILE]
                                                      the production signals of a change, for the release's
                                                      confirmation: of one requirement file, or of every
                                                      requirement whose spec changed since REF
  specs.py catalog   index|check                      build or check this part's spec-types/index.yaml

The layers' own checks (such as em.py check for the event model) run separately; `check` lists them.
Needs Python 3 and PyYAML.
"""
import argparse
import datetime
import json
import pathlib
import re
import shutil
import subprocess
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("specs.py needs PyYAML: python3 -m pip install --user pyyaml")

SKILL = pathlib.Path(__file__).resolve().parent.parent
CATALOG = SKILL / "spec-types"
STATUSES = {"proposed", "set-up", "validated", "active", "retired"}
REQ_STATUSES = {"draft", "questions", "approved", "superseded"}
REQ_KINDS = {"functional", "nfr", "constraint"}
MODEL_TYPES = {"event-model"}  # layers whose files carry `reqs:` and slices


def die(msg):
    sys.exit(msg)


def read_yaml(path):
    with open(path) as fh:
        return yaml.safe_load(fh) or {}


def specs_dir(root):
    d = pathlib.Path(root) / "specs"
    if not d.is_dir():
        die(f"no specs/ in {root}: run `specs.py init` first")
    return d


# ----------------------------------------------------------------------------------------------- init, new-req
def cmd_init(args):
    d = pathlib.Path(args.root) / "specs"
    if (d / "policy.yaml").exists():
        die(f"{d} is already set up")
    (d / "requirements").mkdir(parents=True, exist_ok=True)
    (d / "model").mkdir(exist_ok=True)
    for name in ("policy.yaml", "profile.yaml", "layers.yaml"):
        shutil.copy(SKILL / "defaults" / name, d / name)
    print(f"created {d}: policy.yaml, profile.yaml, layers.yaml, requirements/, model/")
    return 0


def cmd_new_req(args):
    d = specs_dir(args.root) / "requirements"
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", args.key):
        die("key: letters, digits, '-', '_' and '.' only (a ticket key or a short slug)")
    path = d / f"{args.key}.yaml"
    if path.exists():
        die(f"{path} exists")
    text = (SKILL / "templates" / "requirements.yaml").read_text()
    text = (text.replace("<KEY>", args.key)
                .replace("<SOURCE>", args.source or "text from the user")
                .replace("<DATE>", datetime.date.today().isoformat()))
    path.write_text(text)
    print(f"created {path}")
    return 0


# ----------------------------------------------------------------------------------------------- loading
def load_requirements(sd):
    reqs, files = {}, {}
    for p in sorted((sd / "requirements").glob("*.y*ml")):
        doc = read_yaml(p)
        files[p] = doc
        for r in doc.get("requirements") or []:
            reqs.setdefault(r.get("id"), []).append((p, r, doc))
    return reqs, files


def model_files(sd, layers):
    paths = []
    for layer in layers:
        if layer.get("type") in MODEL_TYPES and layer.get("status") != "retired":
            base = pathlib.Path(sd.parent) / layer.get("path", "specs/model/")
            if base.is_dir():
                paths += sorted(p for p in base.rglob("*.y*ml"))
            elif base.is_file():
                paths.append(base)
    return paths


def model_elements(doc):
    """Yield (element id, kind, content, reqs) for every element of an event model document."""
    for s in doc.get("slices") or []:
        body = {k: v for k, v in s.items() if k != "specs"}
        yield f"slice {s.get('id')}", "slice", body, s.get("reqs") or []
        for sp in s.get("specs") or []:
            name = sp.get("name") or json.dumps(sp, sort_keys=True)[:60]
            yield f"example {s.get('id')}/{name}", "example", sp, (sp.get("reqs") or []) + (s.get("reqs") or [])
    for name, st in (doc.get("states") or {}).items():
        yield f"state {name}", "state", st, (st or {}).get("reqs") or []
    for rid, r in (doc.get("rules") or {}).items():
        if (r or {}).get("kind") == "table":
            n = len(r.get("inputs") or [])
            for row in r.get("rows") or []:
                key = "/".join(str(v) for v in row[:n])
                yield f"rule {rid}/{key}", "rule row", row, r.get("reqs") or []
        else:
            yield f"rule {rid}", "rule", r, (r or {}).get("reqs") or []
    for ext, d in (doc.get("externals") or {}).items() if isinstance(doc.get("externals"), dict) else []:
        for outcome in ((d or {}).get("outcomes") or {}):
            yield f"outcome {ext}->{outcome}", "outcome", (d or {}).get("outcomes", {}).get(outcome), []
    for sc, d in (doc.get("screens") or {}).items():
        yield f"screen {sc}", "screen", d, []


def model_names(doc):
    """(name, what) for every name in an event model that a test will reuse."""
    for sc in doc.get("screens") or {}:
        yield sc, "screen"
    for st in doc.get("states") or {}:
        yield st, "state"
    for s in doc.get("slices") or []:
        if s.get("type") == "view":
            rm = s.get("read_model") or {}
            yield rm.get("name", ""), "read model"
            for f in rm.get("fields") or {}:
                yield f, f"field of {rm.get('name')}"
            for sc in s.get("screens") or []:
                yield sc, "screen"
            continue
        cmd = s.get("command") or {}
        yield cmd.get("name", ""), "command"
        for f in cmd.get("fields") or {}:
            yield f, f"field of {cmd.get('name')}"
        for ev in s.get("events") or {}:
            yield ev, "event"
        for e in s.get("errors") or []:
            yield e, "error"


# ----------------------------------------------------------------------------------------------- check
def cmd_check(args):
    sd = specs_dir(args.root)
    errors, warnings, notes = [], [], []
    E, W = errors.append, warnings.append

    for name in ("policy.yaml", "profile.yaml", "layers.yaml"):
        if not (sd / name).exists():
            E(f"specs/{name}: missing")
    policy = read_yaml(sd / "policy.yaml") if (sd / "policy.yaml").exists() else {}
    profile = read_yaml(sd / "profile.yaml") if (sd / "profile.yaml").exists() else {}
    layers = (read_yaml(sd / "layers.yaml") if (sd / "layers.yaml").exists() else {}).get("layers") or []

    if not (policy.get("ask") or {}).get("who") and not (profile.get("people") or {}).get("approver"):
        W("policy/profile: nobody is named to answer questions about requirements (ask.who, people.approver)")
    if not (profile.get("tests") or {}).get("writer"):
        W("profile: tests.writer is empty: name the agent or plugin that turns the spec into tests")

    known_types = {c["id"] for c in catalog_cards()}
    ids, spines = set(), 0
    for i, layer in enumerate(layers):
        lid = layer.get("id") or f"#{i}"
        if lid in ids:
            E(f"layers.yaml: layer id '{lid}' used twice")
        ids.add(lid)
        if layer.get("type") not in known_types:
            E(f"layers.yaml [{lid}]: type '{layer.get('type')}' is not in the catalog")
        if layer.get("status") not in STATUSES:
            E(f"layers.yaml [{lid}]: status '{layer.get('status')}' is not one of {sorted(STATUSES)}")
        if not layer.get("why"):
            E(f"layers.yaml [{lid}]: no 'why': a layer exists for a named risk or as the spine")
        if layer.get("status") in ("validated", "active") and not layer.get("check"):
            E(f"layers.yaml [{lid}]: {layer.get('status')} but no 'check' command")
        path = layer.get("path")
        if path and not (sd.parent / path).exists() and layer.get("status") != "proposed":
            E(f"layers.yaml [{lid}]: path {path} does not exist")
        if layer.get("type") == "event-model" and layer.get("status") != "retired":
            spines += 1
    if layers and spines == 0:
        W("layers.yaml: no event-model layer: the spec has no spine that tests are derived from")
    if spines > 1:
        W("layers.yaml: more than one event-model layer: one system, one model")

    reqs, files = load_requirements(sd)
    for p, doc in files.items():
        rel = p.relative_to(sd.parent)
        if doc.get("key") != p.stem:
            E(f"{rel}: key '{doc.get('key')}' does not match the file name")
        if not doc.get("source"):
            E(f"{rel}: no source (a ticket URL, or where the text came from)")
        if doc.get("status") not in REQ_STATUSES:
            E(f"{rel}: status '{doc.get('status')}' is not one of {sorted(REQ_STATUSES)}")
        if doc.get("status") == "approved" and not doc.get("approved_by"):
            E(f"{rel}: approved but approved_by is empty")
        open_q = [q.get("id") for q in doc.get("questions") or [] if q.get("text") and not q.get("answer")]
        if doc.get("status") == "approved" and open_q:
            E(f"{rel}: approved with open questions {open_q}")
        for r in doc.get("requirements") or []:
            rid = r.get("id") or ""
            if not rid.startswith(f"{doc.get('key')}#"):
                E(f"{rel}: requirement id '{rid}' must start with '{doc.get('key')}#'")
            if r.get("kind") not in REQ_KINDS:
                E(f"{rel} [{rid}]: kind '{r.get('kind')}' is not one of {sorted(REQ_KINDS)}")
            if not (r.get("text") or "").strip():
                E(f"{rel} [{rid}]: empty text")
            if r.get("kind") == "nfr" and not (r.get("metric") or "").strip():
                W(f"{rel} [{rid}]: an nfr without a metric cannot be tested: add how it is measured and the threshold")
            prod = r.get("prod")
            signal = str((prod or {}).get("signal") or "").strip() if isinstance(prod, dict) else ""
            if prod is not None and not isinstance(prod, dict):
                E(f"{rel} [{rid}]: prod must be a mapping: signal, match, min")
            elif signal == "none" and not str(prod.get("why") or "").strip():
                E(f"{rel} [{rid}]: prod signal is none but there is no why")
            elif signal and signal != "none":
                if not isinstance(prod.get("match"), dict) or not prod.get("match"):
                    E(f"{rel} [{rid}]: prod has a signal but no match: the log fields that pick it out")
                least = prod.get("min")
                if not isinstance(least, int) or least < 1:
                    E(f"{rel} [{rid}]: prod min must be a whole number, 1 or more")
            if r.get("kind") == "functional" and doc.get("status") == "approved" and not signal:
                W(f"{rel} [{rid}]: no production signal, so a release's confirmation cannot tell it happened: add "
                  f"prod (signal, match, min), or signal: none with a why")
    for rid, where in reqs.items():
        if len(where) > 1:
            E(f"requirement id {rid} defined {len(where)} times")

    # trace
    referenced, untraced = {}, []
    for p in model_files(sd, layers):
        rel = p.relative_to(sd.parent)
        doc = read_yaml(p)
        for eid, kind, _content, refs in model_elements(doc):
            for ref in refs:
                if ref not in reqs:
                    E(f"{rel}: {eid} refers to unknown requirement {ref}")
                referenced.setdefault(ref, []).append(eid)
            if kind == "example" and not refs:
                untraced.append(eid)
    for rid, where in reqs.items():
        _p, r, doc = where[0]
        if doc.get("status") == "superseded":
            continue
        if rid not in referenced:
            (E if doc.get("status") == "approved" else W)(
                f"requirement {rid} is covered by no spec element ({(r.get('text') or '')[:70]})")
    if untraced:
        notes.append(f"{len(untraced)} example(s) trace to no requirement (reverse-engineered, or gold plating)")

    # glossary: no listed synonym in the model's names
    for layer in layers:
        if layer.get("type") != "glossary" or layer.get("status") == "retired":
            continue
        gpath = sd.parent / layer.get("path", "specs/glossary.yaml")
        if not gpath.is_file():
            continue
        avoid = {}
        for entry in read_yaml(gpath).get("terms") or []:
            for bad in entry.get("not") or []:
                avoid[str(bad).lower()] = entry.get("term")
        for mp in model_files(sd, layers):
            for name, where in model_names(read_yaml(mp)):
                words = {w.lower() for w in re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+", name)}
                for bad, term in avoid.items():
                    if bad in words or bad == name.lower():
                        W(f"{mp.relative_to(sd.parent)}: {where} '{name}' uses '{bad}'; the glossary says '{term}'")

    print(f"specs/: {len(layers)} layer(s), {len(files)} requirement file(s), {len(reqs)} requirement(s)\n")
    print(f"ERRORS ({len(errors)})")
    for e in errors:
        print("  ", e)
    print(f"\nWARNINGS ({len(warnings)})")
    for w in warnings:
        print("  ", w)
    for n in notes:
        print("\nNOTE:", n)
    checks = [(lay.get("id"), lay.get("check")) for lay in layers if lay.get("check") and lay.get("status") != "retired"]
    if checks:
        print("\nLayer checks to run as well:")
        for lid, c in checks:
            print(f"   [{lid}] {c}")
    return 1 if errors else 0


# ----------------------------------------------------------------------------------------------- trace
def cmd_trace(args):
    sd = specs_dir(args.root)
    layers = (read_yaml(sd / "layers.yaml")).get("layers") or []
    reqs, _files = load_requirements(sd)
    by_req, untraced = {}, []
    for p in model_files(sd, layers):
        for eid, kind, _c, refs in model_elements(read_yaml(p)):
            for ref in refs:
                by_req.setdefault(ref, []).append(eid)
            if kind == "example" and not refs:
                untraced.append(eid)
    for rid in sorted(reqs):
        if args.req and not rid.startswith(args.req + "#"):
            continue
        _p, r, doc = reqs[rid][0]
        els = by_req.get(rid, [])
        print(f"{rid} [{r.get('kind')}, {doc.get('status')}] {(r.get('text') or '').strip()}")
        for e in els:
            print(f"    {e}")
        if not els:
            print("    -- covered by no spec element")
    unknown = sorted(set(by_req) - set(reqs))
    if unknown:
        print("\nReferenced but not defined:", ", ".join(unknown))
    if untraced and not args.req:
        print(f"\nExamples that trace to no requirement ({len(untraced)}):")
        for e in untraced:
            print(f"    {e}")
    return 0


# ----------------------------------------------------------------------------------------------- delta
def git(root, *a):
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True)


def delta_since(sd, base):
    """What changed in the spec since a git ref: (added, changed, removed, new, old, reqs, req_added, req_changed)."""
    root = sd.parent
    top = git(root, "rev-parse", "--show-toplevel")
    if top.returncode:
        die("delta needs a git repository")
    top = pathlib.Path(top.stdout.strip())
    if git(root, "rev-parse", "--verify", base).returncode:
        die(f"unknown git ref {base}")
    layers = (read_yaml(sd / "layers.yaml")).get("layers") or []

    def at_base(path):
        rel = path.resolve().relative_to(top.resolve())
        r = git(root, "show", f"{base}:{rel.as_posix()}")
        return yaml.safe_load(r.stdout) or {} if r.returncode == 0 else {}

    def flatten(doc):
        return {eid: (kind, json.dumps(c, sort_keys=True, default=str), refs) for eid, kind, c, refs in model_elements(doc)}

    now_files = model_files(sd, layers)
    base_list = git(root, "ls-tree", "-r", "--name-only", base).stdout.split()
    model_dirs = [(sd.parent / lay.get("path", "")).resolve() for lay in layers if lay.get("type") in MODEL_TYPES]
    gone = [top / f for f in base_list if f.endswith((".yaml", ".yml"))
            and any(str((top / f).resolve()).startswith(str(d)) for d in model_dirs)
            and not (top / f).exists()]
    old, new = {}, {}
    for p in now_files:
        new.update(flatten(read_yaml(p)))
        old.update(flatten(at_base(p)))
    for p in gone:
        old.update(flatten(at_base(p)))

    added = [e for e in new if e not in old]
    removed = [e for e in old if e not in new]
    changed = [e for e in new if e in old and new[e][1] != old[e][1]]

    reqs, _files = load_requirements(sd)
    req_old = {}
    for p in (sd / "requirements").glob("*.y*ml"):
        for r in (at_base(p).get("requirements") or []):
            req_old[r.get("id")] = (r.get("text") or "").strip()
    req_added = [r for r in reqs if r not in req_old]
    req_changed = [r for r in reqs if r in req_old and (reqs[r][0][1].get("text") or "").strip() != req_old[r]]
    return added, changed, removed, new, old, reqs, req_added, req_changed


def cmd_delta(args):
    sd = specs_dir(args.root)
    added, changed, removed, new, old, reqs, req_added, req_changed = delta_since(sd, args.base)
    print(f"# Spec delta since {args.base}\n")
    print("For the test writer: add tests for what was added, update tests for what changed, delete tests for what"
          " was removed. Examples are matched to tests by slice id and example name.\n")

    def section(title, items, src):
        print(f"## {title} ({len(items)})")
        for e in sorted(items):
            refs = src[e][2]
            print(f"- {e}" + (f"  (reqs: {', '.join(refs)})" if refs else ""))
        print()
    section("Added", added, new)
    section("Changed", changed, new)
    section("Removed", removed, old)
    if req_added or req_changed:
        print("## Requirements")
        for r in req_added:
            print(f"- added {r}: {(reqs[r][0][1].get('text') or '').strip()}")
        for r in req_changed:
            print(f"- changed {r}: {(reqs[r][0][1].get('text') or '').strip()}")
    return 0


# ----------------------------------------------------------------------------------------------- signals
def cmd_signals(args):
    """The production signals of a change, as the release's confirmation reads them: [{name, req, match, min}]."""
    sd = specs_dir(args.root)
    if bool(args.req) == bool(args.base):
        die("say which change, one of: --req KEY (a requirement file) or --base REF (what changed since a git ref)")
    if args.req:
        reqs, _files = load_requirements(sd)
        chosen = sorted(rid for rid in reqs if rid and rid.startswith(args.req + "#"))
        if not chosen:
            die(f"no requirements with the key {args.req}")
    else:
        added, changed, _removed, new, _old, reqs, req_added, req_changed = delta_since(sd, args.base)
        chosen = sorted({ref for e in added + changed for ref in new[e][2]} | set(req_added) | set(req_changed))
    signals, notes = [], []
    for rid in chosen:
        if rid not in reqs:
            notes.append(f"{rid}: the spec refers to it, but no requirement file defines it")
            continue
        _p, r, doc = reqs[rid][0]
        if r.get("kind") != "functional":
            continue
        prod = r.get("prod") if isinstance(r.get("prod"), dict) else {}
        signal = str(prod.get("signal") or "").strip()
        if doc.get("status") != "approved":
            notes.append(f"{rid}: its file is {doc.get('status')}, not approved: left out")
        elif not signal:
            notes.append(f"{rid}: no production signal: the release's confirmation cannot tell it happened")
        elif signal == "none":
            notes.append(f"{rid}: shows nothing in production: {prod.get('why') or 'no why given'}")
        else:
            signals.append({"name": f"{rid}: {signal}", "req": rid, "match": prod.get("match") or {},
                            "min": int(prod.get("min") or 1)})
    out = json.dumps(signals, indent=1, ensure_ascii=False) + "\n"
    if args.out:
        pathlib.Path(args.out).write_text(out)
        print(f"wrote {len(signals)} signal(s) to {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(out)
    for n in notes:
        print(f"note: {n}", file=sys.stderr)
    return 0


# ----------------------------------------------------------------------------------------------- catalog
def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return (yaml.safe_load(m.group(1)) or {}) if m else None


def catalog_cards():
    cards = []
    for p in sorted(CATALOG.glob("*/*.md")):
        fm = frontmatter(p.read_text())
        if fm:
            fm["_path"] = p
            cards.append(fm)
    return cards


def summary(text):
    m = re.search(r"^## What it describes\n\n(.+?)(?:\n\n|\Z)", text, re.S | re.M)
    if not m:
        return ""
    para = " ".join(m.group(1).split())
    sentences = re.split(r"(?<=[.!?])\s+", para)
    return " ".join(sentences[:2])


def build_index():
    lines = ["# Generated by scripts/specs.py catalog index from the frontmatter of spec-types/<group>/<id>.md.",
             "# Do not edit by hand: change the card, then run `python3 scripts/specs.py catalog index`.", "",
             "spec_types:"]
    for c in catalog_cards():
        p = c["_path"]
        lines += [f"  - id: {c['id']}",
                  f"    title: {json.dumps(c.get('title', ''), ensure_ascii=False)}",
                  f"    group: {c.get('group')}",
                  f"    role: {c.get('role')}",
                  f"    path: {p.parent.name}/{p.name}",
                  f"    summary: {json.dumps(summary(p.read_text()), ensure_ascii=False)}"]
        for k in ("fits", "risks", "tests", "checks", "cost"):
            if k in c:
                v = c[k]
                lines.append(f"    {k}: [{', '.join(v)}]" if isinstance(v, list) else f"    {k}: {v}")
    return "\n".join(lines) + "\n"


def cmd_catalog(args):
    problems = []
    seen = set()
    for c in catalog_cards():
        p = c["_path"]
        for k in ("id", "title", "group", "role", "tests", "checks", "cost"):
            if k not in c:
                problems.append(f"{p.name}: frontmatter has no '{k}'")
        if c.get("id") != p.stem:
            problems.append(f"{p.name}: id '{c.get('id')}' does not match the file name")
        if c.get("group") != p.parent.name:
            problems.append(f"{p.name}: group '{c.get('group')}' does not match the folder")
        if c.get("role") not in ("spine", "layer"):
            problems.append(f"{p.name}: role must be spine or layer")
        if c.get("id") in seen:
            problems.append(f"{p.name}: duplicate id")
        seen.add(c.get("id"))
        text = p.read_text()
        for section in ("## What it describes", "## When it fits", "## How it is checked", "## What the tests get"):
            if section not in text:
                problems.append(f"{p.name}: no '{section}' section")
    index = CATALOG / "index.yaml"
    if args.action == "index":
        index.write_text(build_index())
        print(f"wrote {index}")
    elif not index.exists() or index.read_text() != build_index():
        problems.append("index.yaml is out of date: run `specs.py catalog index`")
    for pr in problems:
        print(pr)
    if not problems:
        print(f"OK: {len(seen)} spec types")
    return 1 if problems else 0


# ----------------------------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("init", "new-req", "check", "trace", "delta"):
        p = sub.add_parser(name)
        p.add_argument("--root", default=".")
        if name == "new-req":
            p.add_argument("key")
            p.add_argument("--source")
        if name == "trace":
            p.add_argument("--req", help="only the requirements of this key")
        if name == "delta":
            p.add_argument("--base", default="HEAD")
    p = sub.add_parser("signals")
    p.add_argument("--root", default=".")
    p.add_argument("--req", help="the requirements of this key")
    p.add_argument("--base", help="the requirements whose spec changed since this git ref")
    p.add_argument("--out", help="write the signals here instead of printing them")
    p = sub.add_parser("catalog")
    p.add_argument("action", choices=["index", "check"])
    args = ap.parse_args()
    return {"init": cmd_init, "new-req": cmd_new_req, "check": cmd_check, "trace": cmd_trace, "delta": cmd_delta,
            "signals": cmd_signals, "catalog": cmd_catalog}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())

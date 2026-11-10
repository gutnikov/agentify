#!/usr/bin/env python3
"""event-model: check an Event Model written in YAML and export it as the contract a test writer reads.

  em.py check  <model>... [--all]       errors, warnings, rule coverage, test readiness, open questions
  em.py export <model>... [--out FILE]  the model as JSON (contract "event-model/1"): screens, states, outside
                                        systems and their outcomes, slices, examples, test obligations, questions

<model> is a .yaml file or a folder of them; several files are merged into one model.
The format is described in format.md next to this script's folder. Needs Python 3 and PyYAML.
"""
import argparse
import itertools
import json
import os
import sys
from collections import defaultdict

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("em.py needs PyYAML: python3 -m pip install --user pyyaml")

SPECIAL_TRIGGERS = {"clock", "external"}
MAX_STATE_DEPTH = 3  # the playwright plugin's rule: one fixture adds one thing, at most three levels deep


# ----------------------------------------------------------------------------------------------- loading
def load(paths):
    files = []
    for p in paths:
        if os.path.isdir(p):
            for root, _dirs, names in os.walk(p):
                files += [os.path.join(root, n) for n in sorted(names) if n.endswith((".yaml", ".yml"))]
        else:
            files.append(p)
    if not files:
        sys.exit("no model files found")
    model = {"slices": [], "rules": {}, "domains": {}, "states": {}, "screens": {}, "externals": {}, "actors": []}
    dupes = []
    for f in files:
        part = yaml.safe_load(open(f)) or {}
        for key in ("rules", "domains", "states", "screens"):
            for k, v in (part.get(key) or {}).items():
                if k in model[key]:
                    dupes.append(f"{key}.{k} defined twice ({f})")
                model[key][k] = v
        ext = part.get("externals") or {}
        if isinstance(ext, list):
            ext = {name: {} for name in ext}
        for k, v in ext.items():
            model["externals"][k] = v or {}
        model["actors"] += part.get("actors") or []
        for s in part.get("slices") or []:
            s["_file"] = f
            model["slices"].append(s)
        for k in ("system", "clock"):
            if k in part:
                model[k] = part[k]
    seen = set()
    for s in model["slices"]:
        if s["id"] in seen:
            dupes.append(f"slice id {s['id']} used twice")
        seen.add(s["id"])
    model["_files"] = files
    model["_dupes"] = dupes
    return model


# ----------------------------------------------------------------------------------------------- index
class Index:
    def __init__(self, m):
        self.m = m
        self.events, self.commands, self.read_models = {}, {}, {}
        self.screens = defaultdict(set)  # screen -> read models shown on it
        self.field_warnings = []
        for s in m["slices"]:
            if s["type"] == "view":
                rm = s["read_model"]
                self.read_models[rm["name"]] = s
                for sc in s.get("screens", []):
                    self.screens[sc].add(rm["name"])
                continue
            self.commands.setdefault(s["command"]["name"], []).append(s)
            for ev, spec in (s.get("events") or {}).items():
                fields = (spec or {}).get("fields", {})
                if ev in self.events:
                    if set(self.events[ev]["fields"]) != set(fields):
                        self.field_warnings.append(
                            (s["id"], f"event {ev} produced with a different field set than in {self.events[ev]['producers']}"))
                    self.events[ev]["producers"].append(s["id"])
                else:
                    self.events[ev] = {"fields": fields, "producers": [s["id"]], "stream": (spec or {}).get("stream")}

    def pom(self, screen):
        return (self.m["screens"].get(screen) or {}).get("pom") or lcfirst(screen)

    def route(self, screen):
        return (self.m["screens"].get(screen) or {}).get("route")


def lcfirst(s):
    return s[:1].lower() + s[1:]


def ucfirst(s):
    return s[:1].upper() + s[1:]


# ----------------------------------------------------------------------------------------------- specs
def norm_spec(s, sp):
    """One spec in either form (see format.md) -> a dict with fixed keys."""
    cmd = (s.get("command") or {}).get("name")
    given = sp.get("given", [])
    when = sp.get("when")
    then = sp.get("then")
    out = {
        "name": sp.get("name"),
        "state": given if isinstance(given, str) else None,
        "given_events": given if isinstance(given, list) else [],
        "inputs": when if isinstance(when, dict) else {},
        "when_cmd": when if isinstance(when, str) else cmd,
        "events": [], "see": [], "error": None,
        "external": sp.get("external") or {},
        "after": sp.get("after"),
        "question": sp.get("question"),
        "covers": sp.get("covers") or [],
    }
    if isinstance(then, str) and then.startswith("error"):
        out["error"] = then.split(None, 1)[1] if " " in then else "?"
    elif isinstance(then, list):
        out["events"] = then
    elif isinstance(then, dict):
        out["events"] = then.get("events") or []
        out["see"] = then.get("see") or []
        out["error"] = then.get("error")
    out["e2e_ready"] = bool(out["name"] and out["state"] and (out["see"] or out["error"]))
    return out


def all_specs(m):
    for s in m["slices"]:
        if s["type"] == "view":
            continue
        for sp in s.get("specs") or []:
            yield s, norm_spec(s, sp)


def state_chain(m, name):
    chain, cur = [], name
    while cur and cur not in chain:
        chain.append(cur)
        cur = (m["states"].get(cur) or {}).get("extends")
    return list(reversed(chain))


# ----------------------------------------------------------------------------------------------- check
def check(m, ix):
    errors, warnings = [], []

    def E(sid, msg):
        errors.append(f"[{sid}] {msg}")

    def W(sid, msg):
        line = f"[{sid}] {msg}"
        if line not in warnings:
            warnings.append(line)

    for d in m["_dupes"]:
        E("model", d)
    for sid, msg in ix.field_warnings:
        W(sid, msg)
    rules, domains, externals = m["rules"], m["domains"], m["externals"]
    consumed = defaultdict(set)
    rm_used = defaultdict(set)

    def rule_ref(sid, src):
        rid = src.split(":", 1)[1]
        if rid not in rules:
            E(sid, f"unknown rule '{rid}'")
        elif rules[rid].get("unknown"):
            W(sid, f"depends on rule '{rid}' which is UNKNOWN: {rules[rid].get('text')}")

    def visible(s):
        return ix.screens.get(s.get("screen"), set()) if s["type"] == "command" else set(s.get("reads", []))

    def rm_ref(sid, s, src, what):
        rm, _, f = src.partition(".")
        if rm not in ix.read_models:
            return E(sid, f"{what}: unknown read model '{rm}'")
        if f not in ix.read_models[rm]["read_model"]["fields"]:
            E(sid, f"{what}: read model {rm} has no field '{f}'")
        if rm not in visible(s):
            where = f"screen {s.get('screen')}" if s["type"] == "command" else "reads"
            E(sid, f"{what}: uses {rm}.{f} but {rm} is not available via {where}")
        rm_used[rm].add(sid)

    def ev_ref(sid, s, src, what):
        ev, _, f = src.partition(".")
        if ev not in ix.events:
            return E(sid, f"{what}: unknown event '{ev}'")
        if f not in ix.events[ev]["fields"]:
            E(sid, f"{what}: event {ev} has no field '{f}'")
        if s.get("trigger") != ev:
            E(sid, f"{what}: takes {ev}.{f} but {ev} is not this slice's trigger")
        consumed[ev].add(sid)

    def source(sid, s, src, what, allow_cmd=False):
        if src == "input":
            if s["type"] != "command":
                E(sid, f"{what}: 'input' in a {s['type']} slice (no person types here)")
        elif src == "system":
            pass
        elif src == "ext":
            if s["type"] != "translation":
                E(sid, f"{what}: 'ext' outside a translation slice")
        elif src == "cmd" and allow_cmd:
            pass
        elif src.startswith("rule:"):
            rule_ref(sid, src)
        elif "." in src and src.split(".")[0] in ix.read_models:
            rm_ref(sid, s, src, what)
        elif "." in src:
            ev_ref(sid, s, src, what)
        else:
            E(sid, f"{what}: unrecognised source '{src}'")

    # --- slices that change something
    for s in m["slices"]:
        sid, typ = s["id"], s["type"]
        if typ == "view":
            continue
        if typ == "command":
            if s.get("screen") not in ix.screens:
                E(sid, f"command issued from screen '{s.get('screen')}' which no view slice renders")
        else:
            trig = s.get("trigger")
            if trig in SPECIAL_TRIGGERS:
                pass
            elif trig not in ix.events:
                E(sid, f"trigger '{trig}' is not a known event")
            else:
                consumed[trig].add(sid)
            for rm in s.get("reads", []):
                if rm not in ix.read_models:
                    E(sid, f"reads unknown read model '{rm}'")
                rm_used[rm].add(sid)
        if typ == "translation" and s.get("external") not in externals:
            E(sid, f"translation from undeclared external '{s.get('external')}'")
        for r in s.get("rules", []):
            rule_ref(sid, "rule:" + r)
        cmd = s["command"]
        for f, src in (cmd.get("fields") or {}).items():
            source(sid, s, src, f"command {cmd['name']}.{f}")
        for ev, spec in (s.get("events") or {}).items():
            for f, src in ((spec or {}).get("fields") or {}).items():
                if src == "cmd" and f not in (cmd.get("fields") or {}):
                    E(sid, f"event {ev}.{f}: source 'cmd' but command {cmd['name']} has no field '{f}'")
                else:
                    source(sid, s, src, f"event {ev}.{f}", allow_cmd=True)
            if not (spec or {}).get("stream"):
                W(sid, f"event {ev} has no stream")

        # --- specs
        specs = [norm_spec(s, sp) for sp in s.get("specs") or []]
        declared = s.get("errors")
        if typ == "command" and declared is None:
            W(sid, f"command {cmd['name']} does not enumerate its errors: list every error it can return in `errors`")
        if not specs:
            E(sid, "no specs")
        failure = success_seen = False
        for sp in specs:
            label = f"spec '{sp['name'] or '(unnamed)'}'"
            if sp["state"] and sp["state"] not in m["states"]:
                E(sid, f"{label}: given state '{sp['state']}' is not defined in states")
            for g in sp["given_events"]:
                if g not in ix.events:
                    E(sid, f"{label}: given unknown event '{g}'")
            if sp["when_cmd"] != cmd["name"]:
                E(sid, f"{label}: 'when' is {sp['when_cmd']}, the slice's command is {cmd['name']}")
            for k in sp["inputs"]:
                fsrc = (cmd.get("fields") or {}).get(k)
                if fsrc is None:
                    E(sid, f"{label}: input '{k}' is not a field of command {cmd['name']}")
                elif fsrc != "input" and fsrc.split(".")[0] not in ix.read_models:
                    # input = typed; <ReadModel>.<field> = picked on screen; anything else is not the person's
                    W(sid, f"{label}: input '{k}' comes from {fsrc}, not from the person; set it through the state")
            if sp["error"] and declared is not None and sp["error"] not in declared:
                E(sid, f"{label}: error '{sp['error']}' is not in the slice's errors {declared}")
            for c in sp["covers"]:
                rid, _, vals = str(c).removeprefix("rule:").partition("/")
                r = rules.get(rid)
                if not r or r.get("kind") != "table":
                    E(sid, f"{label}: covers '{c}' but '{rid}' is not a decision table")
                elif vals.split("/") not in [[str(v) for v in row[: len(r["inputs"])]] for row in r.get("rows") or []]:
                    E(sid, f"{label}: covers '{c}' but the table has no such row")
            for t in sp["events"]:
                if t not in (s.get("events") or {}):
                    E(sid, f"{label}: then-event '{t}' is not produced by this slice")
            for item in sp["see"]:
                sc, fld = item.get("screen"), item.get("field", "")
                rm, _, f = fld.partition(".")
                if sc not in ix.screens:
                    E(sid, f"{label}: sees screen '{sc}' which no view slice renders")
                elif rm not in ix.screens[sc]:
                    E(sid, f"{label}: {fld} is not shown on screen {sc}")
                if rm in ix.read_models and f not in ix.read_models[rm]["read_model"]["fields"]:
                    E(sid, f"{label}: read model {rm} has no field '{f}'")
                if "is" not in item:
                    E(sid, f"{label}: see-item {fld} has no expected value ('is')")
                rm_used[rm].add(sid)
            for ext, outcome in sp["external"].items():
                outs = (externals.get(ext) or {}).get("outcomes")
                if ext not in externals:
                    E(sid, f"{label}: external '{ext}' is not declared")
                elif outs and outcome not in outs:
                    E(sid, f"{label}: external {ext} has no outcome '{outcome}' (declared: {', '.join(outs)})")
            if sp["after"] and not m.get("clock"):
                E(sid, f"{label}: 'after' needs 'clock: true' in the model")
            if sp["error"]:
                failure = True
            elif sp["see"] or sp["events"]:
                success_seen = True
                if len(s.get("events") or {}) > 1 and len(sp["events"]) == 1:
                    failure = True  # an alternative outcome is specified
        if typ == "command" and not failure:
            W(sid, f"command {cmd['name']} has no failure spec")
        if typ == "command" and not success_seen:
            W(sid, f"command {cmd['name']} has no success spec")

    # --- read models
    for s in m["slices"]:
        if s["type"] != "view":
            continue
        sid, rm = s["id"], s["read_model"]
        for f, srcs in rm["fields"].items():
            what = f"read model {rm['name']}.{f}"
            if not srcs:
                E(sid, f"{what}: no source")
            for src in srcs:
                if src == "config":
                    continue
                if src.startswith("rule:"):
                    rule_ref(sid, src)
                    continue
                ev, _, ef = src.partition(".")
                if ev not in ix.events:
                    E(sid, f"{what}: unknown event '{ev}'")
                    continue
                consumed[ev].add(sid)
                if ef and ef not in ix.events[ev]["fields"]:
                    E(sid, f"{what}: event {ev} has no field '{ef}'")
        for sc in s.get("screens", []):
            rm_used[rm["name"]].add(sc)

    # --- states (= e2e fixtures)
    used_states = {sp["state"] for _s, sp in all_specs(m) if sp["state"]}
    for name, st in m["states"].items():
        st = st or {}
        parent = st.get("extends")
        if parent and parent not in m["states"]:
            E(f"state:{name}", f"extends unknown state '{parent}'")
        chain = state_chain(m, name)
        if chain[0] == name and parent:
            E(f"state:{name}", "extends chain has a cycle")
        if len(chain) > MAX_STATE_DEPTH + 1:
            W(f"state:{name}", f"{len(chain) - 1} levels above the first state; fixtures stay readable at {MAX_STATE_DEPTH}")
        for ev in st.get("given", []):
            if ev not in ix.events:
                E(f"state:{name}", f"given unknown event '{ev}'")
            else:
                consumed[ev].add(f"state:{name}")
        if parent and not st.get("given"):
            W(f"state:{name}", "adds no events to its parent")
        if not st.get("note"):
            W(f"state:{name}", "no note with the concrete values a fixture must produce")
    parents = {(st or {}).get("extends") for st in m["states"].values()}
    for name in m["states"]:
        if name not in used_states and name not in parents:
            W(f"state:{name}", "no spec starts from this state")
    for sc in m["screens"]:
        if sc not in ix.screens:
            W(f"screen:{sc}", "declared in screens but no view slice renders it")

    # --- orphans
    for ev, d in ix.events.items():
        if not consumed.get(ev):
            W(",".join(d["producers"]), f"event {ev} is never consumed (no read model, automation, state or reference)")
    for rm in ix.read_models:
        if not rm_used.get(rm):
            W(ix.read_models[rm]["id"], f"read model {rm} is not shown on any screen nor read by any automation")

    # --- decision tables
    coverage = []
    for rid, r in rules.items():
        if r.get("kind") != "table":
            continue
        ins = r["inputs"]
        seen = defaultdict(list)
        for row in r.get("rows") or []:
            key = tuple(row[: len(ins)])
            if len(row) != len(ins) + 1:
                E(f"rule:{rid}", f"row {row} has wrong arity")
            for d, v in zip(ins, key):
                if d not in domains:
                    E(f"rule:{rid}", f"unknown domain '{d}'")
                elif v not in domains[d]:
                    E(f"rule:{rid}", f"value '{v}' not in domain {d}")
            seen[key].append(row[-1])
        for key, outs in seen.items():
            if len(outs) > 1:
                E(f"rule:{rid}", f"overlap for {key}: {outs}")
        if all(d in domains for d in ins):
            allc = list(itertools.product(*[domains[d] for d in ins]))
            missing = [c for c in allc if c not in seen]
            coverage.append((rid, len(allc) - len(missing), len(allc), missing))
    return errors, warnings, coverage


def rules_used(m):
    """Decision tables the slices actually use: in `rules:` or as a `rule:<id>` source."""
    used = set()

    def scan(fields):
        for src in (fields or {}).values():
            for x in (src if isinstance(src, list) else [src]):
                if isinstance(x, str) and x.startswith("rule:"):
                    used.add(x[5:])
    for s in m["slices"]:
        used.update(s.get("rules") or [])
        if s["type"] == "view":
            scan(s["read_model"]["fields"])
        else:
            scan((s.get("command") or {}).get("fields"))
            for spec in (s.get("events") or {}).values():
                scan((spec or {}).get("fields"))
    return used


def obligations(m, ix):
    """What an exhaustive e2e set has to check, and the e2e-ready examples that pin each item down.

    The model does not write tests; it makes sure a test writer can enumerate everything there is to test:
    each command's success and each of its errors, each outcome of an outside system, each time-driven step,
    each row of a decision table in use, each field a screen shows."""
    ready = [(s, sp) for s, sp in all_specs(m) if sp["e2e_ready"]]
    ref = lambda s, sp: f"{s['id']}/{sp['name']}"
    out = []
    for s in m["slices"]:
        mine = [sp for x, sp in ready if x is s]
        if s["type"] == "command":
            out.append(("success", f"{s['id']} {s['command']['name']}", [ref(s, sp) for sp in mine if sp["see"]]))
            for err in s.get("errors") or []:
                out.append(("error", f"{s['id']} {err}", [ref(s, sp) for sp in mine if sp["error"] == err]))
        elif s["type"] != "view" and s.get("trigger") == "clock":
            out.append(("time", f"{s['id']} {s.get('name', '')}", [ref(s, sp) for sp in mine if sp["after"]]))
    for ext, d in m["externals"].items():
        for outcome in ((d or {}).get("outcomes") or {}):
            out.append(("outcome", f"{ext} -> {outcome}",
                        [ref(s, sp) for s, sp in ready if sp["external"].get(ext) == outcome]))
    for rid in sorted(rules_used(m)):
        r = m["rules"].get(rid) or {}
        if r.get("kind") != "table":
            continue
        for row in r.get("rows") or []:
            key = "rule:" + rid + "/" + "/".join(str(v) for v in row[: len(r["inputs"])])
            out.append(("rule row", key, [ref(s, sp) for s, sp in ready if key in sp["covers"]]))
    shown = sorted({rm for rms in ix.screens.values() for rm in rms})
    for rm in shown:
        for f in ix.read_models[rm]["read_model"]["fields"]:
            fld = f"{rm}.{f}"
            out.append(("field", fld, [ref(s, sp) for s, sp in ready if any(i.get("field") == fld for i in sp["see"])]))
    return out


def cmd_check(m, ix, args):
    errors, warnings, coverage = check(m, ix)
    n = lambda t: sum(1 for s in m["slices"] if s["type"] == t)
    print(f"Event model ({len(m['_files'])} file(s)): {len(m['slices'])} slices "
          f"({n('command')} command, {n('view')} view, {n('automation')} automation, {n('translation')} translation), "
          f"{len(ix.events)} events, {len(ix.read_models)} read models, {len(ix.screens)} screens, "
          f"{len(m['states'])} states, {len(m['rules'])} rules\n")
    print(f"ERRORS ({len(errors)})")
    for e in errors:
        print("  ", e)
    print(f"\nWARNINGS ({len(warnings)})")
    for w in warnings:
        print("  ", w)
    if coverage:
        print("\nDECISION TABLE COVERAGE")
        for rid, ok, tot, missing in coverage:
            print(f"   {rid}: {ok}/{tot} combinations defined")
            if missing:
                shown = ", ".join("/".join(map(str, c)) for c in missing[:6])
                more = f" ... +{len(missing) - 6}" if len(missing) > 6 else ""
                print(f"      missing: {shown}{more}")
    specs = list(all_specs(m))
    ready = sum(sp["e2e_ready"] for _s, sp in specs)
    unnamed = sum(not sp["name"] for _s, sp in specs)
    print(f"\nTEST READINESS: {ready}/{len(specs)} examples are e2e-ready (named, start from a state, end in what a "
          f"person sees){f'; {unnamed} have no name' if unnamed else ''}")
    obl = obligations(m, ix)
    kinds = ["success", "error", "outcome", "time", "rule row", "field"]
    print("   obligations pinned down by an e2e-ready example:")
    for k in kinds:
        items = [o for o in obl if o[0] == k]
        if items:
            print(f"     {k:<9}{sum(bool(o[2]) for o in items):>4}/{len(items)}")
    unmet = [o for o in obl if not o[2]]
    shown = unmet if args.all else [o for o in unmet if o[0] != "field"][:25]
    if unmet:
        print("   not pinned down yet:")
        for k, what, _ in shown:
            print(f"     {k:<9} {what}")
        rest = len(unmet) - len(shown)
        if rest:
            print(f"     ... +{rest} more (em.py check --all)")
    questions = [(s["id"], q) for s in m["slices"] for q in s.get("questions", [])]
    questions += [(s["id"], sp["question"]) for s, sp in all_specs(m) if sp["question"]]
    print(f"\nOPEN QUESTIONS ({len(questions)})")
    for sid, q in questions:
        print(f"   [{sid}] {q}")
    if args.strict and unmet:
        print(f"\nSTRICT: {len(unmet)} test obligation(s) not pinned down by an e2e-ready example")
        return 1
    return 1 if errors else 0


# ----------------------------------------------------------------------------------------------- export
CONTRACT = "event-model/1"


def export(m, ix):
    """The spec as a test writer reads it: everything a test needs, and nothing about how to write one."""
    examples = []
    for s, sp in all_specs(m):
        raw = next((x for x in s.get("specs") or [] if norm_spec(s, x)["name"] == sp["name"]), {}) if sp["name"] else {}
        examples.append({
            "slice": s["id"], "name": sp["name"], "e2e_ready": sp["e2e_ready"],
            "state": sp["state"], "given_events": sp["given_events"], "inputs": sp["inputs"],
            "external": sp["external"], "after": sp["after"],
            "see": sp["see"], "error": sp["error"], "events": sp["events"],
            "covers": sp["covers"], "question": sp["question"],
            "reqs": (raw.get("reqs") or []) + (s.get("reqs") or []),
        })
    slices = []
    for s in m["slices"]:
        d = {"id": s["id"], "name": s.get("name", ""), "type": s["type"], "reqs": s.get("reqs") or [],
             "questions": s.get("questions") or [], "rules": s.get("rules") or []}
        if s["type"] == "view":
            d.update(read_model=s["read_model"]["name"], fields=list(s["read_model"]["fields"]), screens=s.get("screens", []))
        else:
            d.update(command=s["command"]["name"],
                     inputs=[f for f, src in (s["command"].get("fields") or {}).items()
                             if src == "input" or str(src).split(".")[0] in ix.read_models],
                     errors=s.get("errors"), events=list(s.get("events") or {}))
            for k in ("actor", "screen", "trigger", "external", "reads"):
                if k in s:
                    d[k] = s[k]
        slices.append(d)
    return {
        "contract": CONTRACT,
        "system": m.get("system"),
        "files": m["_files"],
        "clock": bool(m.get("clock")),
        "externals": {k: {"outcomes": (v or {}).get("outcomes") or {}} for k, v in m["externals"].items()},
        "screens": {sc: {"route": ix.route(sc), "pom": ix.pom(sc), "read_models": sorted(rms)}
                    for sc, rms in sorted(ix.screens.items())},
        "states": {name: {"extends": (st or {}).get("extends"), "given": (st or {}).get("given", []),
                          "note": (st or {}).get("note"), "chain": state_chain(m, name)}
                   for name, st in m["states"].items()},
        "rules": {rid: {k: v for k, v in (r or {}).items()} for rid, r in m["rules"].items()},
        "slices": slices,
        "examples": examples,
        "obligations": [{"kind": k, "what": w, "pinned_by": by} for k, w, by in obligations(m, ix)],
        "questions": [{"slice": s["id"], "text": q} for s in m["slices"] for q in s.get("questions", [])]
                     + [{"slice": s["id"], "example": sp["name"], "text": sp["question"]}
                        for s, sp in all_specs(m) if sp["question"]],
    }


def cmd_export(m, ix, args):
    text = json.dumps(export(m, ix), indent=2, ensure_ascii=False, default=str)
    if args.out:
        with open(args.out, "w") as fh:
            fh.write(text + "\n")
        print(f"wrote {args.out}")
    else:
        print(text)
    return 0


# ----------------------------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("check")
    p.add_argument("model", nargs="+")
    p.add_argument("--all", action="store_true", help="list every unmet test obligation")
    p.add_argument("--strict", action="store_true",
                   help="fail when a test obligation is not pinned down: the check of a spec that tests are derived from")
    p = sub.add_parser("export")
    p.add_argument("model", nargs="+")
    p.add_argument("--out", help="write the JSON here instead of stdout")
    args = ap.parse_args()
    m = load(args.model)
    ix = Index(m)
    return {"check": cmd_check, "export": cmd_export}[args.cmd](m, ix, args)


if __name__ == "__main__":
    sys.exit(main())

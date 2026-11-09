#!/usr/bin/env python3
"""event-model: check an Event Model written in YAML, plan and scaffold its e2e tests, measure e2e coverage.

  em.py check    <model>...                                  errors, warnings, rule coverage, questions, e2e readiness
  em.py plan     <model>... [--slices S1,S2] [--json]        fixtures, Page Object methods and tests the specs need
  em.py scaffold <model>... --out <dir> [--slices S1,S2] [--fixtures-import <module>] [--force]
                                                             Playwright spec skeletons, one file per slice
  em.py coverage <model>... --tests <dir> [--strict]         which specs have a test: tag @slice:<id>, title = spec name

<model> is a .yaml file or a folder of them; several files are merged into one model.
The format is described in format.md next to this script's folder. Needs Python 3 and PyYAML.
"""
import argparse
import itertools
import json
import os
import re
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


def kebab(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


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


def readiness(m):
    total = ready = unnamed = 0
    lacking = []
    for s in m["slices"]:
        if s["type"] == "view":
            continue
        specs = [norm_spec(s, sp) for sp in s.get("specs") or []]
        total += len(specs)
        ready += sum(sp["e2e_ready"] for sp in specs)
        unnamed += sum(not sp["name"] for sp in specs)
        if s["type"] == "command":
            ok_success = any(sp["e2e_ready"] and sp["see"] for sp in specs)
            ok_failure = any(sp["e2e_ready"] and sp["error"] for sp in specs)
            if not (ok_success and ok_failure):
                miss = [x for x, ok in (("success", ok_success), ("failure", ok_failure)) if not ok]
                lacking.append(f"{s['id']} {s['command']['name']}: no e2e-ready {' and '.join(miss)} spec")
    if unnamed:
        lacking.append(f"{unnamed} spec(s) have no name: tests are matched to specs by name")
    return total, ready, lacking


def cmd_check(m, ix, _args):
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
    total, ready, lacking = readiness(m)
    print(f"\nE2E READINESS: {ready}/{total} specs start from a state and end in something a person sees")
    for line in lacking:
        print("  ", line)
    questions = [(s["id"], q) for s in m["slices"] for q in s.get("questions", [])]
    questions += [(s["id"], sp["question"]) for s, sp in all_specs(m) if sp["question"]]
    print(f"\nOPEN QUESTIONS ({len(questions)})")
    for sid, q in questions:
        print(f"   [{sid}] {q}")
    return 1 if errors else 0


# ----------------------------------------------------------------------------------------------- e2e plan
def select(m, slices_arg):
    wanted = set(slices_arg.split(",")) if slices_arg else None
    return [s for s in m["slices"] if s["type"] != "view" and (wanted is None or s["id"] in wanted)]


def plan(m, ix, slices):
    fixtures, poms, tests, not_ready = {}, defaultdict(dict), [], []
    for s in slices:
        for sp in (norm_spec(s, x) for x in s.get("specs") or []):
            if not sp["e2e_ready"]:
                why = []
                if not sp["name"]:
                    why.append("no name")
                if not sp["state"]:
                    why.append("starts from events, not a named state")
                if not (sp["see"] or sp["error"]):
                    why.append("ends in events, not in what a person sees")
                then = f"error {sp['error']}" if sp["error"] else ", ".join(sp["events"]) or "?"
                given = sp["state"] or ", ".join(sp["given_events"]) or "nothing"
                not_ready.append({"slice": s["id"], "spec": sp["name"], "why": why,
                                  "summary": f"given {given} -> {sp['when_cmd']} -> {then}"})
                continue
            fx = []
            for st in state_chain(m, sp["state"]):
                d = m["states"].get(st) or {}
                fixtures[st] = {"kind": "state", "extends": d.get("extends"), "adds": d.get("given", []),
                                "note": d.get("note")}
            fx.append(sp["state"])
            for ext, outcome in sp["external"].items():
                name = ((m["externals"].get(ext) or {}).get("outcomes") or {}).get(outcome) or f"{lcfirst(ext)}{ucfirst(outcome)}"
                fixtures[name] = {"kind": "external", "forces": f"{ext} -> {outcome}"}
                fx.append(name)
            steps = []
            if sp["after"]:
                steps.append({"clock": sp["after"]})
                fixtures.setdefault("testClock", {"kind": "clock", "note": "moves the backend's clock (testing API)"})
                if "testClock" not in fx:
                    fx.append("testClock")
            if s["type"] == "command":
                screen = s["screen"]
                pom = ix.pom(screen)
                method = lcfirst(s["command"]["name"])
                poms[screen].setdefault("open", "open()")
                poms[screen][method] = f"{method}(input)" if sp["inputs"] else f"{method}()"
                steps.append({"pom": pom, "screen": screen, "call": "open", "args": None})
                steps.append({"pom": pom, "screen": screen, "call": method, "args": sp["inputs"] or None})
                if sp["error"]:
                    poms[screen]["expectError"] = "expectError(name)"
                    steps.append({"pom": pom, "screen": screen, "call": "expectError", "args": sp["error"]})
            elif sp["error"]:
                steps.append({"note": f"expect error {sp['error']} (no screen: {s['type']} slice)"})
            opened = {s.get("screen")} if s["type"] == "command" else set()
            for item in sp["see"]:
                sc = item["screen"]
                pom = ix.pom(sc)
                method = "expect" + ucfirst(item["field"].split(".", 1)[1])
                poms[sc].setdefault("open", "open()")
                poms[sc][method] = f"{method}(value)"
                if sc not in opened:
                    steps.append({"pom": pom, "screen": sc, "call": "open", "args": None})
                    opened.add(sc)
                steps.append({"pom": pom, "screen": sc, "call": method, "args": item["is"], "field": item["field"]})
            tests.append({"slice": s["id"], "slice_name": s.get("name", ""), "spec": sp["name"], "fixtures": fx,
                          "steps": steps, "question": sp["question"]})
    return {"fixtures": fixtures, "poms": {sc: {"pom": ix.pom(sc), "route": ix.route(sc), "methods": meths}
                                           for sc, meths in poms.items()},
            "tests": tests, "not_ready": not_ready}


def cmd_plan(m, ix, args):
    p = plan(m, ix, select(m, args.slices))
    if args.json:
        print(json.dumps(p, indent=2, ensure_ascii=False))
        return 0
    print("# E2E plan\n")
    print("## Fixtures - reuse an existing one first; build a missing one with /fixture-modify")
    for name, f in p["fixtures"].items():
        if f["kind"] == "state":
            base = f"extends {f['extends']}, " if f["extends"] else ""
            note = f" - {f['note']}" if f.get("note") else ""
            print(f"- {name}: {base}adds {', '.join(f['adds']) or 'nothing'}{note}")
        elif f["kind"] == "external":
            print(f"- {name}: forces {f['forces']} (testing API switch or page.route)")
        else:
            print(f"- {name}: {f['note']}")
    print("\n## Page Objects - check the screen with /app-probing; add missing methods with /pom-modify")
    for sc, d in p["poms"].items():
        route = f", route {d['route']}" if d["route"] else ""
        print(f"- {sc} (property {d['pom']}{route}): {', '.join(d['methods'].values())}")
    print("\n## Tests - tag the describe with @slice:<id>; title = spec name")
    for t in p["tests"]:
        mark = " [fixme: open question]" if t["question"] else ""
        print(f"- [{t['slice']}] {t['spec']}{mark}")
        print(f"    fixtures: {', '.join(t['fixtures'])}")
        for st in t["steps"]:
            if "clock" in st:
                print(f"    testClock.advance('{st['clock']}')")
            elif "note" in st:
                print(f"    // {st['note']}")
            else:
                print(f"    {st['pom']}.{st['call']}({ts(st['args']) if st['args'] is not None else ''})")
    if p["not_ready"]:
        print("\n## Not e2e-ready (scaffolded as test.fixme)")
        for nr in p["not_ready"]:
            print(f"- [{nr['slice']}] {nr['spec'] or '(unnamed)'}: {'; '.join(nr['why'])}")
    return 0


# ----------------------------------------------------------------------------------------------- scaffold
def ts(v):
    if isinstance(v, str):
        return "'" + v.replace("\\", "\\\\").replace("'", "\\'") + "'"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, list):
        return "[" + ", ".join(ts(x) for x in v) + "]"
    if isinstance(v, dict):
        return "{ " + ", ".join(f"{k}: {ts(x)}" for k, x in v.items()) + " }"
    return "undefined"


def cmd_scaffold(m, ix, args):
    p = plan(m, ix, select(m, args.slices))
    os.makedirs(args.out, exist_ok=True)
    by_slice = defaultdict(list)
    for t in p["tests"]:
        by_slice[t["slice"]].append(t)
    for nr in p["not_ready"]:
        by_slice[nr["slice"]].append({"not_ready": nr})
    written = skipped = 0
    for s in select(m, args.slices):
        items = by_slice.get(s["id"])
        if not items:
            continue
        path = os.path.join(args.out, f"{s['id'].lower()}-{kebab(s.get('name', s['id']))}.spec.ts")
        if os.path.exists(path) and not args.force:
            print(f"skip (exists): {path}")
            skipped += 1
            continue
        src = os.path.relpath(s["_file"])
        lines = [
            f"// Scaffolded by event-model from {src}, slice {s['id']}. Edit freely; keep the @slice tag and the",
            "// test titles: em.py coverage matches tests to specs by them.",
            f"import {{ test }} from {ts(args.fixtures_import)};",
            "",
            f"test.describe({ts(s['id'] + ' ' + s.get('name', ''))}, {{ tag: '@slice:{s['id']}' }}, () => {{",
        ]
        for t in items:
            if "not_ready" in t:
                nr = t["not_ready"]
                title = nr["spec"] or f"[unnamed] {nr['summary']}"
                lines += [f"  // Not e2e-ready in the model: {'; '.join(nr['why'])}.",
                          f"  test.fixme({ts(title)}, async () => {{}});", ""]
                continue
            deps = ", ".join([f if f == "testClock" else f"{f}: _{i}" for i, f in enumerate(t["fixtures"])] +
                             sorted({st["pom"] for st in t["steps"] if "pom" in st}))
            fn = "test.fixme" if t["question"] else "test"
            if t["question"]:
                lines.append(f"  // Open question in the model: {t['question']}")
            lines.append(f"  {fn}({ts(t['spec'])}, async ({{ {deps} }}) => {{")
            for i, f in enumerate(t["fixtures"]):
                if f != "testClock":
                    lines.append(f"    void _{i}; // {f}")
            for st in t["steps"]:
                if "clock" in st:
                    lines.append(f"    await testClock.advance({ts(st['clock'])});")
                elif "note" in st:
                    lines.append(f"    // TODO: {st['note']}")
                else:
                    arg = ts(st["args"]) if st["args"] is not None else ""
                    lines.append(f"    await {st['pom']}.{st['call']}({arg});")
            lines += ["  });", ""]
        lines[-1:] = ["});", ""]
        with open(path, "w") as fh:
            fh.write("\n".join(lines))
        written += 1
        print(f"wrote {path}")
    print(f"\n{written} file(s) written, {skipped} skipped")
    return 0


# ----------------------------------------------------------------------------------------------- coverage
TEST_RE = re.compile(r"\btest(\.fixme|\.skip|\.only|\.fail)?\(\s*(['\"`])((?:\\.|(?!\2).)*)\2")
TAG_RE = re.compile(r"@slice:([A-Za-z0-9_-]+)")


def cmd_coverage(m, _ix, args):
    tagged = defaultdict(dict)  # slice -> {title: status}
    for root, _dirs, names in os.walk(args.tests):
        if "node_modules" in root:
            continue
        for n in names:
            if not re.search(r"\.(spec|test)\.[jt]sx?$", n):
                continue
            text = open(os.path.join(root, n), encoding="utf-8", errors="replace").read()
            ids = set(TAG_RE.findall(text))
            for mod, _q, title in TEST_RE.findall(text):
                for sid in ids:
                    tagged[sid][title] = "fixme" if mod in (".fixme", ".skip") else "test"
    known = {s["id"] for s in m["slices"]}
    covered = fixme = missing = 0
    rows = []
    for s, sp in all_specs(m):
        if not sp["name"]:
            continue
        status = tagged.get(s["id"], {}).get(sp["name"])
        if status == "test":
            covered += 1
        elif status == "fixme":
            fixme += 1
            rows.append(f"   fixme   [{s['id']}] {sp['name']}")
        else:
            missing += 1
            rows.append(f"   missing [{s['id']}] {sp['name']}")
    named = covered + fixme + missing
    print(f"E2E COVERAGE: {covered}/{named} named specs have a running test, {fixme} fixme, {missing} missing")
    for r in rows:
        print(r)
    stale = sorted(set(tagged) - known)
    if stale:
        print("\nTests tagged with slices the model does not have (stale):")
        for sid in stale:
            print(f"   @slice:{sid}: {', '.join(tagged[sid])}")
    spec_names = defaultdict(set)
    for s, sp in all_specs(m):
        spec_names[s["id"]].add(sp["name"])
    extra = [(sid, t) for sid, ts_ in tagged.items() if sid in known for t in ts_
             if t not in spec_names[sid] and not t.startswith("[unnamed]")]
    if extra:
        print("\nTests whose title matches no spec of their slice (renamed spec or extra test):")
        for sid, t in extra:
            print(f"   [{sid}] {t}")
    return 1 if args.strict and (missing or stale) else 0


# ----------------------------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("check", "plan", "scaffold", "coverage"):
        p = sub.add_parser(name)
        p.add_argument("model", nargs="+")
        if name in ("plan", "scaffold"):
            p.add_argument("--slices", help="comma-separated slice ids (default: all)")
        if name == "plan":
            p.add_argument("--json", action="store_true")
        if name == "scaffold":
            p.add_argument("--out", required=True)
            p.add_argument("--fixtures-import", default="<the fixture file>")
            p.add_argument("--force", action="store_true")
        if name == "coverage":
            p.add_argument("--tests", required=True)
            p.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    m = load(args.model)
    ix = Index(m)
    return {"check": cmd_check, "plan": cmd_plan, "scaffold": cmd_scaffold, "coverage": cmd_coverage}[args.cmd](m, ix, args)


if __name__ == "__main__":
    sys.exit(main())

# agentify

A Claude Code plugin that makes an agent's work on a project checkable, from the task to the change confirmed where
it is used. It has one command, `/agentify`:

| You run | What happens |
|---|---|
| `/agentify` in a project without `agentify/agentify.md` | The setup. It studies the project, recognizes the loops it already runs (CI jobs, hooks, linters, deploy checks, specs, agent loops) and places each in the project's super-loops. It asks only what the code does not tell: what the project is, how far agentify may go on its own, what it can reach, and where a change counts as done. It writes `agentify/agentify.md` and shows the map. It builds nothing |
| `/agentify <a task, or a ticket URL>` | The task, through its super-loop. Triage picks the level (product or harness) and the super-loop; each phase runs the loops the map has; the task ends at an exit, such as a change confirmed in production, or at the `done_at` the user chose |
| `/agentify` | The status: the map, the measures, the work in flight |

The command is `agentify:agentify` in the command list; typing `/agentify` runs it.

## The model

A **super-loop** is the path a piece of work takes, from its entry to a change confirmed where it is used:

```
entry → oracle → work → gate → release → confirmation
```

There are four, told apart by their oracle, the thing the work is checked against, fixed before the work and out of
the reach of the agent that does it:

| Super-loop | Starts with | Oracle | Ends with |
|---|---|---|---|
| delivery | an idea or a requirement | an approved spec and acceptance tests that fail | the change confirmed where it is used |
| remediation | a problem | a reproduction that fails, and the signal the problem was seen by | that signal gone |
| maintenance | a trigger: a new version, an end of life, a measure over budget | the behaviour as it is, and the measure | the measure improved, and nothing changed for users |
| discovery | a question | the question, and the evidence that would answer it | a decision, which may be "do not build it" |

They run at two levels. At the **product** level the agent does the project's work. At the **harness** level it works
on the loops themselves, and the product's trace is its signal. The boundary between the levels is a permission
boundary: a product task never changes a loop that checks it.

```
harness level   discovery · delivery · remediation · maintenance    over the loops, agents, guides and policy
      ▲ the trace: releases not confirmed, escapes, corrections, agents' misses
      ▼ new and fixed loops
product level   discovery · delivery · remediation · maintenance    over the product
```

The details: [`parts/harness/super-loops/`](parts/harness/super-loops/README.md).

## Install

```
/plugin marketplace add gutnikov/agentify
/plugin install agentify@agentify
```

The repository is private, so the machine needs git access to it (`gh auth login`, or an SSH key).

## Layout

| Path | What |
|---|---|
| `skills/agentify/` | The command |
| `parts/` | What it reads: the harness, spec, event-model, text-quality, app-probing, fixture-modify, pom-modify and ui-prototypes parts ([`parts/README.md`](parts/README.md)) |

## What it keeps in a project

Everything agentify keeps is in one folder, `agentify/`, so that one path is what the agent doing product work may
not write, and what a CODEOWNERS entry or a branch rule protects:

```
agentify/agentify.md                 setup: the user's preferences, and the sign that the project is set up
agentify/map.yaml                    setup: what agentify found, the facts the map of the super-loops is drawn from
agentify/hitl-log.jsonl              setup: every call to a person, with its answer
agentify/agents.yaml                 setup: the registry of the agents that are steps of loops
agentify/.gitignore                  setup: keeps .runs/ out of git
agentify/loops/index.yaml            setup: the registry of loops
agentify/loops/<id>/                 task: a loop's LOOP.md, run, CHANGELOG.md, cases/must-fire/, cases/must-pass/
agentify/agents/<id>/                task: an agent's evals/, results/, report.md
agentify/trace.jsonl                 task: escapes, corrections and reverts no system of the project records
agentify/agent-outcomes.jsonl        task: what happened to the agents' verdicts
agentify/specs/                      task: layers, glossary, requirements/, model/, once specs are set up
agentify/.runs/                      task: runs of the text-quality part, not committed
```

Outside it are only what tools read from fixed places: a loop's wiring (a job in `.github/workflows/`, a hook in
`.claude/settings.json`), an agent's definition in `.claude/agents/<id>.md`, and prototypes in
`<host>/prototypes/`, the package that has the design system. A task also writes the product's own files, such as
code, acceptance tests, fixtures and Page Objects, where the project keeps them.

The scripts need Python 3; the spec's also need PyYAML. The text-quality part needs the `claude` CLI and network
access.

## Where it came from

agentify joins the plugins of [`gutnikov/my-claude-plugins`](https://github.com/gutnikov/my-claude-plugins) at
`0e3c71d`: harness 0.5.0 became `parts/harness`; spec 0.3.1 became `parts/spec` and `parts/event-model`; text-quality,
app-probing, playwright (`fixture-modify`, `pom-modify`) and ui-prototypes became parts of the same names. bb is left
out. A project that harness, spec or agentify 0.1 set up keeps `loops/` and `specs/` at its root: its first task is
`/agentify move loops/ and specs/ into agentify/`, which runs `loops.py migrate`: the old policy becomes
`agentify/agentify.md`, and the old profile `agentify/map.yaml`.

# agentify

A Claude Code plugin that makes an agent's work on a project checkable, from the task to the change confirmed where
it is used. It has two commands:

| Command | What it does |
|---|---|
| `/agentify:init` | Studies the project, recognizes the loops it already runs (CI jobs, hooks, linters, deploy checks, specs, agent loops), places each in the project's super-loops, and confirms that map and the policy with you. Writes `loops/`; builds nothing |
| `/agentify:task <text or ticket URL>` | Runs one task through its super-loop. Triage picks the level (product or harness) and the super-loop; each phase runs the loops the map has; the task ends at an exit, such as a change confirmed in production |

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
| `skills/init/`, `skills/task/` | The two commands |
| `parts/` | What they read: the harness, spec, event-model, text-quality, app-probing, fixture-modify, pom-modify and ui-prototypes parts ([`parts/README.md`](parts/README.md)) |

## What it keeps in a project

Everything agentify keeps is in one folder, `agentify/`, so that one path is what the agent doing product work may
not write, and what a CODEOWNERS entry or a branch rule protects:

```
agentify/policy.yaml                 init: what agentify may do alone, and when it calls a person
agentify/profile.yaml                init: the project's facts and the map of its super-loops
agentify/hitl-log.jsonl              init: every call to a person, with its answer
agentify/agents.yaml                 init: the registry of the agents that are steps of loops
agentify/.gitignore                  init: keeps .runs/ out of git
agentify/loops/index.yaml            init: the registry of loops
agentify/loops/<id>/                 task: a loop's LOOP.md, run, CHANGELOG.md, cases/must-fire/, cases/must-pass/
agentify/agents/<id>/                task: an agent's evals/, results/, report.md
agentify/trace.jsonl                 task: escapes, corrections and reverts no system of the project records
agentify/agent-outcomes.jsonl        task: what happened to the agents' verdicts
agentify/specs/                      task: policy, profile, layers, glossary, requirements/, model/, once specs are set up
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
`/agentify:task move loops/ and specs/ into agentify/`, which runs `loops.py migrate`.

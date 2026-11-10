---
name: task
description: Run a task to its end through the project's super-loop. A product task is a feature, a bug, a dependency or speed change, or a question to decide; a harness task chooses, builds, fixes or retires a loop, an agent step or the policy. Triage picks the level and the super-loop, each phase uses the loops on the project's map, and the task is done when the change is confirmed where it is used.
disable-model-invocation: true
argument-hint: "<the task in words, or a ticket URL>"
---

# agentify task

The task: $ARGUMENTS

A task goes through one super-loop of the project, phase by phase, to one of its exits: a change confirmed where it
is used, or a decision. This is how agentify does all its work; `/agentify:init` only draws the map.

**Paths.** `P` is `${CLAUDE_PLUGIN_ROOT}/parts` and `H` is `${CLAUDE_PLUGIN_ROOT}/parts/harness`. They are not
shell variables: write the full path in every command. `loops.py` means
`python3 ${CLAUDE_PLUGIN_ROOT}/parts/harness/scripts/loops.py`, run from the project's root.

**Before anything.** If the project has no `loops/policy.yaml`, it has no map yet: say so in one line, run init
first (`${CLAUDE_PLUGIN_ROOT}/skills/init/SKILL.md`), then come back to this task. Then read `loops/policy.yaml`
(only the project's copy counts), the map (`loops.py map`), `$H/README.md` (Terms; Talking to the user) and
`$H/super-loops/README.md`.

## 1. Read the task

- A text: as given. A ticket by link: through the tracker access this session has (an MCP server, `gh`, `glab`):
  the description, the acceptance criteria, the comments and the linked tickets. Never write to a tracker.
- No task given: ask what it is (H1).
- Look for the same task already open: a branch, a pull request, a requirement file in `specs/requirements/`, a
  prototype. If there is one, continue from the phase it reached. A task's state lives in those systems, not in a
  file of agentify's.
- A chore, such as opening, listing or deleting a prototype agentify made, is done directly with the part that made
  it, without a super-loop.

## 2. Triage: the level, then the super-loop

| The task is about | Level |
|---|---|
| What the product does or how it is built: a feature, a bug, a dependency, its speed or size, a question about the product or its users | product |
| How the agent's work is checked: a loop, a hook, a CI gate, an agent step, a guide (CLAUDE.md, AGENTS.md), the policy, the map | harness |

| Task | Route |
|---|---|
| "add team invites", a ticket with a new behaviour | product · delivery |
| "500 on /api/teams since the last release" | product · remediation |
| "Node 20 reached its end of life" | product · maintenance |
| "should we build SSO?", "what does checkout do with an expired card?" | product · discovery |
| "which loops should we have?" | harness · discovery |
| "add a lint for our error wrapping", "set up specs for delivery" | harness · delivery |
| "the release confirmation keeps failing good releases", "why did this bug get through?" | harness · remediation |
| "we moved to a new model: check the reviewer agent again" | harness · maintenance |

The super-loop of a product task comes from the triage table of `$H/super-loops/README.md`; that of a harness task
from the table of `$H/super-loops/harness-level.md`. A task that needs both levels is two tasks: name both, and run
first the one the other depends on, such as setting up specs before the feature that needs them.

Show the route before the work, with each phase as the map has it:

```
task    TEAMS-2: invite a member by email
route   product · delivery
phases  entry ✓ · oracle ✓ spec-check, acceptance · work ✓ make ci · gate ✓ acceptance (CI) · release ✓ ops/prod deploy · confirmation ✓ release-confirmation
ends    confirmed in production over a 20-minute window
```

If the route is ambiguous and the history does not settle it (a slow page is remediation if it got slower,
maintenance if it was always slow), ask under H1, with the routes as options and the recommended one first.
Otherwise go on.

## 3. Run the phases

Each phase runs what stands at its place on the map. Where the map shows `✗`, use the stand-in below and note the gap
for the report. A product task builds no loop on the way: a missing loop is a harness task, proposed at the end.

| Phase at `✗` | Stand-in |
|---|---|
| oracle | Delivery without `specs/`: ask (H4) whether to set up specs first, as a harness task (recommended when the change has rules, money, permissions or more than one screen), or to take acceptance criteria the user approves (H5), written by the rules of `$P/spec/README.md`, "Written for the tests". Remediation: a reproduction written for this task. Maintenance: the tests as they are, and the measure taken now |
| work | The build, test and lint commands of the profile's `stack`, run before the work counts as done |
| gate | A verification subagent with a fresh context checks the work against the oracle (`$H/loop-types/meta/verification-subagent.md`), then the pull request's own CI. A person reviews where the policy requires it |
| release | As far as `autonomy` allows: merge, then deploy. Anything that touches production is H2 unless the policy allows it |
| confirmation | Read what the agent can reach after the release (logs, errors, metrics) over the window `$H/super-loops/delivery.md` describes in "Confirmation". Where the agent cannot read the stage, the exit is "released; the confirmation is the person's": say what to look at, and do not ask |

### The product level

**Delivery** (`$H/super-loops/delivery.md`)

1. *Oracle.* Follow `$P/spec/README.md`, "Taking a requirement": the requirement file, the spec (the event model by
   `$P/event-model/README.md`), the checks, the questions in one batch, the approval. Then a test writer, a subagent
   with a fresh context, gets the contract (`em.py export`) and the delta (`specs.py delta`) and writes acceptance
   tests that must fail; record them red as the project's acceptance loop does (`$H/loop-types/meta/acceptance-loop.md`).
   In a web app the tests take their states from fixtures and touch the UI through Page Objects
   (`$P/fixture-modify/README.md`, `$P/pom-modify/README.md`).
2. *Work.* A worker, a subagent unless the change is a few lines, gets the requirement file, the contract, the red
   tests and the loops of the map's `work` to run. It may not change `specs/`, the acceptance tests, `loops/` or the
   CI config of a gate. In a web app it checks its work in the running app with `$P/app-probing/README.md`.
3. *Gate.* The acceptance gate in CI: every approved requirement's tests failed before the work and pass after it,
   and the spec and the tests are the approved ones.
4. *Release*, then *confirmation* with the signals of the change (`specs.py signals --base <ref>`), by the project's
   `release-confirmation` loop or the stand-in.

**Remediation** (`$H/super-loops/remediation.md`). The oracle is a reproduction that fails, recorded red before the
fix: a failing test or, for a web UI, a probe (`$P/app-probing/README.md`) turned into a red spec; and the signal
the problem was seen by. The worker fixes the cause and may not weaken another test. The gate is the reproduction
gate. The confirmation: the signal is gone over the window.

**Maintenance** (`$H/super-loops/maintenance.md`). The oracle is the behaviour as it is (the tests and their expected
values) and the value of the measure now. The gate is behaviour invariance: when an expected value has to change,
the task goes back to triage. The confirmation: production behaves as before, and the measure improved.

**Discovery** (`$H/super-loops/discovery.md`). The oracle is the question and the evidence that would answer it,
agreed with the user (H1). The work is prototypes (`$P/ui-prototypes/README.md`), probes (`$P/app-probing/README.md`),
spikes on a branch that is never merged, or a spec of what the app does now (`$P/spec/README.md`, "Reverse
engineering an existing app"). The gate: every claim in the answer has its evidence; write the answer with
`$P/text-quality/README.md`, whose fact check is that gate. The confirmation is the user's decision (H4): build (a
new delivery task, with the evidence as input to its spec), drop, or open (a narrower question).

### The harness level

Follow `$H/README.md`, as the harness engineer it describes:

- discovery: "Choosing loops";
- delivery: "Building a loop, or a set of loops", and "Agent steps" for an agent in a loop. Setting up specs is a
  delivery too: `$P/spec/README.md`, "Setup";
- remediation and maintenance: "Maintaining loops: the harness level". Trace an escape to the phase that should have
  caught it (`$H/loop-types/meta/steering-loop.md`) and log it: `loops.py trace escape <place> --item <id> --note "…"`.

Run `loops.py check` before every commit that touches `loops/`.

## 4. In every task

- **The level is a permission boundary.** A product task never changes `loops/`, the CI config of a gate, or an
  approved oracle. When a loop blocks work that looks correct, leave the loop as it is: stop that part, say so, and
  propose a harness task. A harness task writes no feature; it touches product code only for instrumentation, as
  `autonomy.write_instrumentation` allows.
- **The one who works does not grade.** The oracle is fixed before the work, and the worker cannot change it.
  Reviewers, refuters and judges are subagents with a fresh context; they get what they check (the diff, the
  requirement, the claim), never the worker's reasoning. The final run of a gate is where the worker cannot write.
- **The policy decides.** `autonomy` says what you may do alone. Every call to a person has an id from
  `hitl.allowed` (the spec part maps its R-reasons to these ids) and is logged:
  `loops.py hitl <id> --loop task:<task id> --checked "…" --question "…" --answer "…"`.
- **Talk to the user only in this session**, by `$H/README.md`, "Talking to the user". A subagent cannot talk to the
  user: it returns its question, you ask it, and you send the answer back to the same subagent.
- **One task, one super-loop.** Anything new found on the way is another task: propose it at the end, do not do it
  in this one.

## 5. Exit and report

A task ends at an exit of its super-loop (the `exits` of its card): `confirmed`, `not-confirmed`, `inconclusive`, or
one of its own, such as `dropped` for delivery or `build`, `drop` and `open` for discovery.

- On `not-confirmed`: roll back or switch the flag off as far as the policy allows (H2 for production), and propose
  a remediation task with the evidence of the confirmation.
- Log what the project's systems do not record: a correction the user made in this task
  (`loops.py trace correction <place> --item <id> --note "…"`), or a failure that got further than it should have
  (`loops.py trace escape …`).

Report in a few lines: the route block with each phase's result and its evidence (the pull request, the CI run, the
confirmation's snapshot), the exit, and what is still open. Then the gaps that cost something in this task, each as a
task the user can start:

```
/agentify:task add a gate at delivery/gate: <the failure it would have caught>
```

---
name: agentify
description: Make the agent's work on this project checkable, from the task to the change confirmed where it is used. The first run studies the project, asks only what the code does not tell, and writes agentify/agentify.md and the map of the loops the project already runs. With a task (a feature, a bug, a dependency, a question to decide, or a change to the loops themselves) it runs the task through its super-loop. With nothing, it shows where the project stands.
disable-model-invocation: true
argument-hint: "[a task in words or a ticket URL; nothing for the status]"
---

# agentify

Input: $ARGUMENTS

agentify runs every piece of work in this project through one super-loop of it, phase by phase, to one of its exits:
a change confirmed where it is used, or a decision. What only the user decides is in `agentify/agentify.md`; what
agentify found is in `agentify/map.yaml`.

**Paths.** `P` is `${CLAUDE_PLUGIN_ROOT}/parts` and `H` is `${CLAUDE_PLUGIN_ROOT}/parts/harness`. They are not
shell variables: write the full path in every command. `loops.py` means
`python3 ${CLAUDE_PLUGIN_ROOT}/parts/harness/scripts/loops.py`, run from the project's root.

**Read first:** `agentify/agentify.md` if it exists, all of it, the Notes too: only the project's copy counts.
Then `$H/README.md` (Terms; Preferences; Talking to the user) and `$H/super-loops/README.md`.

## 0. Which run this is

| The project has | The input | The run |
|---|---|---|
| `loops/policy.yaml` but no `agentify/agentify.md` | anything | The layout of the harness plugin or of agentify before 0.3. Say so in one line. The only task it can run is the move (`$H/README.md`, "Moving a project into agentify/"); then the setup |
| no `agentify/agentify.md` | anything | The setup (§1), then the task, if the input holds one |
| `agentify/agentify.md` with a value still to confirm or a placeholder | anything | The setup's form for what is left (§1, step 3), then the rest |
| `agentify/agentify.md` | nothing | The status (§2) |
| `agentify/agentify.md` | a task | The task (§3) |

## 1. Setup

The first run finds out how work goes through the project now and which loops already check it, and asks only what
the code does not tell. It ends with `agentify/agentify.md`, `agentify/map.yaml` and the map shown to the user. It
builds no loop and changes no product code: a gap on the map is filled by a task.

### What counts as a loop

A loop is anything that checks the agent's work and whose result the agent can run or read. The setup recognizes the
loops where they already are and places each one:

| Where it is | What it usually is | Its places |
|---|---|---|
| CI jobs on a pull request or a push | build, lint, type check, unit and integration tests | `work` of delivery, remediation and maintenance |
| A CI job that checks the work against an oracle | acceptance tests of an approved spec, a reproduction gate, a check that no expected value changed | `delivery/gate`, `remediation/gate`, `maintenance/gate` |
| `.claude/settings.json` hooks, git hooks, pre-commit | the same checks, before a turn ends or a commit is made | `work` |
| Deploy jobs, and what runs right after them | a smoke test, a health check | `release` |
| What reads production after a release | a log or error query, a canary analysis, an SLO alert | `confirmation` |
| Dependency bots, scheduled audits, end-of-life checks | a trigger | `maintenance/entry` |
| The error tracker's alerts, bug labels in the tracker | a problem | `remediation/entry` |
| The issue tracker | an idea or a requirement | `delivery/entry` |
| `agentify/specs/` with its checks, acceptance criteria someone approves | the oracle of delivery | `delivery/oracle` |
| Prototypes, spikes, decision records | the work of discovery and its answers | `discovery/work`, `discovery/confirmation` |
| Reviewers, refuters and judges in `.claude/agents/` | an agent step | the place of the loop it serves |
| `agentify/loops/<id>/LOOP.md` | a loop built for this project | its `places` |

A place without a super-loop, such as `release`, means that phase of every product super-loop the project has.

Not loops: a linter config or a test suite that nothing runs, and the guides (CLAUDE.md, AGENTS.md), which steer the
agent but check nothing. Note them for the report: a config nothing runs is a cheap loop to wire in later.

For each loop, find what decides whether it blocks: a required status check in the branch protection,
`continue-on-error`, `allow_failure`, a hook that only warns. A loop that cannot block says "advisory" in its details.

### Steps

1. **Find out, without asking**, everything `$H/profile.md` §1 lists: the stack, the kind, the stages, the tools
   (each checked with one real call), where the work of each super-loop comes from, where a change ends, and what
   has gone wrong. Then every loop of the table above: read what a CI job or a hook runs, not only its name. For
   each loop in `agentify/loops/`, compare its `status` with its `wiring`: wired in on the main branch but still
   `validated`, or `active` with wiring that no longer runs, is a status that lags. In a monorepo, map the part the
   input names; if it names none and the repository leaves it open, ask which part (H1).
2. **Write what you found.** `loops.py init` creates `agentify/` and keeps what exists. Fill `agentify/map.yaml`
   (`$H/profile.md` §3): `stack`, `stages`, `super_loops` and `not_here`, `ends_at`, `trace`, `existing_checks` as
   `"<name>: <places> — <where it runs, what it does>"` (not the loops in `agentify/loops/`: their `LOOP.md` places
   them), and `pains` from the history, each with the place that should have caught it and its evidence. Fill the
   fields of `agentify/agentify.md` that you settled: `kind`, and `tools` you checked.
3. **Ask what is left, in one form**: one call of the question tool, up to 4 questions, only those that the code,
   the history and the input did not settle. This form is the one exception to one question at a time. Each
   question starts with what you found, because the user may see only the form, and offers it first.
   - **Project** (H1): "What is <project>? Found: <kind, stack, what the README says>." Options: "As found";
     "I'll describe it", whose free answer goes into the body of `agentify.md` in the user's words. Text in the input
     that describes the project is this answer: do not ask it.
   - **Autonomy** (H7), single-select, the levels of `$H/README.md`, "Preferences": ask, branch, merge, deploy.
     Recommend the one the project's setup supports: `branch` where a protected branch needs a review, `merge` where
     CI gates every pull request, `deploy` only where a confirmation judges every release.
   - **Tools** (H1): `$H/profile.md` §2, Q3. A tool the user picks that step 1 did not find does not go into
     `tools` as it is: ask once what it is and how the agent reaches it, with the sources you found as options, and
     call it once if you can. A tool nobody can name stays out, or the loops that need it would count as ones the
     project can run.
   - **Done at** (H7): "Where does a change count as done? Found: <the stages>." Options: the stages the project
     has, among local tests, CI green, staging and confirmed in production; recommend the last one the agent can
     read.

   Log each question with its answer: `loops.py hitl <id> --loop setup --checked "…" --question "…" --answer "…"`.
4. **Write `agentify/agentify.md`**: the fields from the answers, the body with what the project is, and in Notes
   anything the user said that every task must know. Remove a "confirm" note once the user confirmed it.
5. **Show the map** (`loops.py map`) and the loops behind it:

   ```
   Profile: api (Go) · ci, production · tools: ci (gh), logs (ops/prod logs)
   Ends at: production, by ops/prod deploy; nothing confirms it after the deploy
   Done at: production · autonomy: merge (agentify.md)

   delivery     entry ✓ issues · oracle ✗ · work ✓ make ci · gate ✗ · release ✓ ops/prod deploy · confirmation ✗
   remediation  entry ✗ · oracle ✗ · work ✓ make ci · gate ✗ · release ✓ ops/prod deploy · confirmation ✗
   maintenance  entry ✓ dependabot · oracle ✗ · work ✓ make ci · gate ✗ · release ✓ ops/prod deploy · confirmation ✗
   not here     discovery: every idea the team brings gets built

   | Loop       | Places                                    | Runs                   | Blocks        |
   |------------|-------------------------------------------|------------------------|---------------|
   | make ci    | delivery, remediation, maintenance / work | CI job ci, on every PR | yes, required |
   | dependabot | maintenance/entry                         | weekly, opens PRs      | —             |
   ```

   Ask about the map (H1) only where it is unclear: a check you could not place, or a job you cannot tell blocks.
6. **Check and commit**: `loops.py check`, then commit `agentify/` the way the autonomy level lets a change go.
7. **Report** in a few lines: the gaps and what each means for "done" today (where nothing confirms a change, a person
   decides, or nobody does); the loops that cannot block and those whose status lags; the guides and unwired
   configs. Then up to 3 tasks worth starting, each from a gap with evidence in the history, as commands:

   ```
   /agentify choose the first loops for the pains on the map
   /agentify set up specs for delivery
   ```

The setup runs again when the user asks (`/agentify set up again`) or the project changed (a new CI job, a stand
added, a tool lost). It finds out again and updates `agentify/map.yaml` without asking; it asks only about the fields
of `agentify.md` the change touches, such as a tool that no longer answers. It never builds, changes, wires in or
retires a loop, and changes no product code, CI config or hook.

## 2. Status

Show in a few lines: the map (`loops.py map`), the measures (`loops.py stats`: releases not confirmed, escapes by
place, calls to a person), and the work in flight: branches and pull requests agentify opened, requirement files not
approved, releases deployed without a verdict yet. Then up to 3 tasks worth starting, as commands. Ask nothing.

## 3. A task

### Read it

- A text: as given. A ticket by link: through the tracker access this session has (an MCP server, `gh`, `glab`):
  the description, the acceptance criteria, the comments and the linked tickets. Never write to a tracker.
- Look for the same task already open: a branch, a pull request, a requirement file in `agentify/specs/requirements/`,
  a prototype. If there is one, continue from the phase it reached. A task's state lives in those systems, not in a
  file of agentify's.
- A chore, such as opening, listing or deleting a prototype agentify made, is done directly with the part that made
  it, without a super-loop.

### Triage: the level, then the super-loop

| The task is about | Level |
|---|---|
| What the product does or how it is built: a feature, a bug, a dependency, its speed or size, a question about the product or its users | product |
| How the agent's work is checked: a loop, a hook, a CI gate, an agent step, a guide (CLAUDE.md, AGENTS.md), the preferences, the map | harness |

| Task | Route |
|---|---|
| "add team invites", a ticket with a new behaviour | product · delivery |
| "500 on /api/teams since the last release" | product · remediation |
| "Node 20 reached its end of life" | product · maintenance |
| "should we build SSO?", "what does checkout do with an expired card?" | product · discovery |
| "which loops should we have?" | harness · discovery |
| "add a lint for our error wrapping", "set up specs for delivery" | harness · delivery |
| "the release confirmation keeps failing good releases", "why did this bug get through?" | harness · remediation |
| "we moved to a new model: check the reviewer agent again", "move loops/ and specs/ into agentify/" | harness · maintenance |

The super-loop of a product task comes from the triage table of `$H/super-loops/README.md`; that of a harness task
from the table of `$H/super-loops/harness-level.md`. A task that needs both levels is two tasks: name both, and run
first the one the other depends on, such as setting up specs before the feature that needs them.

Show the route before the work, with each phase as the map has it, up to `done_at`:

```
task    TEAMS-2: invite a member by email
route   product · delivery
phases  entry ✓ · oracle ✓ spec-check, acceptance · work ✓ make ci · gate ✓ acceptance (CI) · release ✓ ops/prod deploy · confirmation ✓ release-confirmation
ends    confirmed in production over a 20-minute window (done_at: production)
```

If the route is ambiguous and the history does not settle it (a slow page is remediation if it got slower,
maintenance if it was always slow), ask under H1, with the routes as options and the recommended one first.
Otherwise go on.

### Run the phases

Each phase runs what stands at its place on the map. A product super-loop ends at `done_at` of `agentify.md`: with
`ci`, the task stops at the gate, and its exit is "ready to release"; with `staging`, the release and the
confirmation are on staging. Where the map shows `✗`, use the stand-in below and note the gap for the report. A
product task builds no loop on the way: a missing loop is a harness task, proposed at the end.

| Phase at `✗` | Stand-in |
|---|---|
| oracle | Delivery without `agentify/specs/`: ask (H4) whether to set up specs first, as a harness task (recommended when the change has rules, money, permissions or more than one screen), or to take acceptance criteria the user approves (H5), written by the rules of `$P/spec/README.md`, "Written for the tests". Remediation: a reproduction written for this task. Maintenance: the tests as they are, and the measure taken now |
| work | The build, test and lint commands of `stack` in `agentify/map.yaml`, run before the work counts as done |
| gate | A verification subagent with a fresh context checks the work against the oracle (`$H/loop-types/meta/verification-subagent.md`), then the pull request's own CI. A person reviews where the autonomy level leaves the merge to them |
| release | As far as the autonomy level allows: `merge` merges, `deploy` also deploys. Below `deploy`, anything that touches production is H2 |
| confirmation | Read what the agent can reach after the release (logs, errors, metrics) over the window `$H/super-loops/delivery.md` describes in "Confirmation". Where the agent cannot read the stage, the exit is "released; the confirmation is the person's": say what to look at, and do not ask |

**Product: delivery** (`$H/super-loops/delivery.md`)

1. *Oracle.* Follow `$P/spec/README.md`, "Taking a requirement": the requirement file, the spec (the event model by
   `$P/event-model/README.md`), the checks, the questions in one batch, the approval. Then a test writer, a subagent
   with a fresh context, gets the contract (`em.py export`) and the delta (`specs.py delta`) and writes acceptance
   tests that must fail; record them red as the project's acceptance loop does
   (`$H/loop-types/meta/acceptance-loop.md`). In a web app the tests take their states from fixtures and touch the
   UI through Page Objects (`$P/fixture-modify/README.md`, `$P/pom-modify/README.md`).
2. *Work.* A worker, a subagent unless the change is a few lines, gets the requirement file, the contract, the red
   tests and the loops of the map's `work` to run. It writes nothing under `agentify/` and does not change the
   acceptance tests or the CI config of a gate. In a web app it checks its work in the running app with
   `$P/app-probing/README.md`.
3. *Gate.* The acceptance gate in CI: every approved requirement's tests failed before the work and pass after it,
   and the spec and the tests are the approved ones.
4. *Release*, then *confirmation* with the signals of the change (`specs.py signals --base <ref>`), by the project's
   `release-confirmation` loop or the stand-in.

**Product: remediation** (`$H/super-loops/remediation.md`). The oracle is a reproduction that fails, recorded red
before the fix: a failing test or, for a web UI, a probe (`$P/app-probing/README.md`) turned into a red spec; and the
signal the problem was seen by. The worker fixes the cause and may not weaken another test. The gate is the
reproduction gate. The confirmation: the signal is gone over the window.

**Product: maintenance** (`$H/super-loops/maintenance.md`). The oracle is the behaviour as it is (the tests and their
expected values) and the value of the measure now. The gate is behaviour invariance: when an expected value has to
change, the task goes back to triage. The confirmation: production behaves as before, and the measure improved.

**Product: discovery** (`$H/super-loops/discovery.md`). The oracle is the question and the evidence that would answer
it, agreed with the user (H1). The work is prototypes (`$P/ui-prototypes/README.md`), probes
(`$P/app-probing/README.md`), spikes on a branch that is never merged, or a spec of what the app does now
(`$P/spec/README.md`, "Reverse engineering an existing app"). The gate: every claim in the answer has its evidence;
write the answer with `$P/text-quality/README.md`, whose fact check is that gate. The confirmation is the user's
decision (H4): build (a new delivery task, with the evidence as input to its spec), drop, or open (a narrower
question).

**Harness.** Follow `$H/README.md`, as the harness engineer it describes: discovery is "Choosing loops"; delivery is
"Building a loop, or a set of loops", with "Agent steps" for an agent in a loop, and setting up specs
(`$P/spec/README.md`, "Setup"); remediation and maintenance are "Maintaining loops: the harness level", where an
escape is traced to the phase that should have caught it (`$H/loop-types/meta/steering-loop.md`) and logged with
`loops.py trace escape <place> --item <id> --note "…"`. Run `loops.py check` before every commit that touches
`agentify/`.

### In every task

- **The level is a permission boundary.** A product task never changes `agentify/loops/`, `agentify/agentify.md`, the
  CI config of a gate, or an approved oracle, and its worker writes nothing under `agentify/`. When a loop blocks
  work that looks correct, leave the loop as it is: stop that part, say so, and propose a harness task. A harness
  task writes no feature; it touches product code only for instrumentation (logs, health endpoints, test seams).
- **The one who works does not grade.** The oracle is fixed before the work, and the worker cannot change it.
  Reviewers, refuters and judges are subagents with a fresh context; they get what they check (the diff, the
  requirement, the claim), never the worker's reasoning. The final run of a gate is where the worker cannot write.
- **The preferences decide.** The autonomy level says what you may do alone, `done_at` where the task ends, the
  Notes what never to do or ask. Every call to a person has an id from `$H/defaults/hitl.yaml` (the spec part maps
  its R-reasons to these ids) and is logged: `loops.py hitl <id> --loop task:<task id> --checked "…" --question "…"
  --answer "…"`.
- **Talk to the user only in this session**, by `$H/README.md`, "Talking to the user". A subagent cannot talk to the
  user: it returns its question, you ask it, and you send the answer back to the same subagent.
- **One task, one super-loop.** Anything new found on the way is another task: propose it at the end, do not do it
  in this one.

### Exit and report

A task ends at an exit of its super-loop (the `exits` of its card): `confirmed`, `not-confirmed`, `inconclusive`, or
one of its own, such as `dropped` for delivery or `build`, `drop` and `open` for discovery; or at `done_at`, as
"ready to release" or "released".

- On `not-confirmed`: roll back or switch the flag off as far as the autonomy level allows (H2 below `deploy`), and
  propose a remediation task with the evidence of the confirmation.
- Log what the project's systems do not record: a correction the user made in this task
  (`loops.py trace correction <place> --item <id> --note "…"`), or a failure that got further than it should have
  (`loops.py trace escape …`).

Report in a few lines: the route block with each phase's result and its evidence (the pull request, the CI run, the
confirmation's snapshot), the exit, and what is still open. Then the gaps that cost something in this task, each as a
task the user can start:

```
/agentify add a gate at delivery/gate: <the failure it would have caught>
```

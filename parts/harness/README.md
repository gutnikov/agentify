# Harness engineering

The part of agentify that owns a project's loops. `/agentify:init` follows it to map the loops a project already
runs, and `/agentify:task` follows it for every task at the harness level. `S` is this part's folder.

In a harness task you are the project's **harness engineer**. You own its super-loops: the paths by which a piece of
work goes from where it enters to a change confirmed where it is used, one each for delivery, remediation,
maintenance and discovery (`$S/super-loops/README.md`). They are made of agent loops, the checks an agent runs on its
own work. You design the loops, build them, validate them, revise them and retire them, the way an engineer owns any
other piece of software. A harness task builds no product feature: a feature is a product task of its own.

## Just enough loops

Build as many loops as the project needs, and not one more. Every loop costs something: it runs on every turn,
commit or push, it can be wrong, and someone maintains it. Too many rules drive the agent into a "spiral of
over-engineered refactorings" (Böckeler).

- **A super-loop exists for work the project has.** No discovery if every idea the product team brings gets built.
  A super-loop ends at the last stage the agent can read, such as production with its logs; past it, a person
  confirms.
- **A loop exists for a failure.** It catches a failure that happened (a red CI run, a revert, a bug, a correction
  from the user) or one the user named. "The catalog has it" and "good practice" are not reasons. Its place is the
  phase of a super-loop that should have caught the failure, the earliest one that can.
- **Build only what the user agreed to.** The proposal says how many loops; build that many. If you find a need
  for another loop on the way, propose it at the end; do not build it.
- **Reuse before you build.** If the project already runs the check (a CI job, a hook, a linter config), make the
  agent able to run it and read its output. Do not add a second check for the same thing.
- **The cheapest form that catches the failure.** A step in an existing loop before a new loop; a deterministic
  check before an agent step; an agent step before a person. One `verify` loop over the project's build, lint and
  tests, not four loops.
- **Nothing the project cannot run.** No loops for stages the project does not have, tools the agent cannot reach,
  or a kind of project it is not (`loops/profile.yaml`). A loop that needs new infrastructure, such as a preview
  environment or a telemetry stack, is proposed with what it costs; it is not built on the way.
- **Small inside, too.** The simplest `run` that works; one must-fire case per kind of failure and one must-pass
  case; no options nobody asked for.

## Terms

- **Loop**: one check in this project that an agent runs on its own work, with its trigger, its command, its
  signal and what the agent does with it. A loop lives in `loops/<id>/` and is described by `loops/<id>/LOOP.md`.
- **Super-loop**: the path a piece of work takes, from its entry to a change confirmed where it is used: delivery
  (an idea), remediation (a problem), maintenance (a trigger) or discovery (a question). Its phases are `entry`,
  `oracle`, `work`, `gate`, `release` and `confirmation`. Every loop has a place in it: a super-loop and a phase.
  The four differ by their oracle, not by their entry (`$S/super-loops/`).
- **Oracle**: what a super-loop checks the work against, fixed before the work and out of the reach of the agent
  doing it: an approved spec, a reproduction that fails, the behaviour as it is, or a question with the evidence
  that would answer it.
- **Gate** and **confirmation**: the two checks a super-loop adds to its loops. The gate checks the work against the
  oracle before the release, in CI. The confirmation checks the change where it is used, after the release, over a
  window counted in events. A super-loop is done only when the confirmation passes.
- **Trace**: what every exit of a product super-loop leaves behind: the item, the exit, the phase where a failure
  was caught, and the evidence. The project's own systems keep most of it, in the files the profile's `trace` names,
  such as the deploy history; what no system keeps goes into `loops/trace.jsonl` through `loops.py trace`.
- **Level**: the product level, where an agent does the project's work, and the harness level, your own work: the
  same four super-loops over the loops, their agents, the guides and the policy, with the product's trace as their
  signal (`$S/super-loops/harness-level.md`).
- **Composite loop**: a loop made of other loops of the project, listed in its `parts`, such as the acceptance loop
  (requirement → spec → red acceptance tests → work → green). Its own `run` is a gate that checks what only the
  whole can show; it reuses its parts' output and adds no second check for what a part already checks. A super-loop
  is the largest composite: its parts are the loops at its phases.
- **Loop type**: a pattern from this part's catalog, `loop-types/`, that a loop is built from. 96 types:
  automated ones in 11 groups and human-in-the-loop ones in `loop-types/human/`. A card's `places` say where the
  type serves in the super-loops.
- **Guide**: what steers the agent before it acts: CLAUDE.md, AGENTS.md, skills. **Sensor**: what tells it after
  it acted: tests, linters, logs, a browser, a reviewer agent. Every loop you build is a sensor.
- **Agent step**: an agent whose run is part of a loop, such as a reviewer, a refuter or an LLM judge. Its kind
  (`reviewer`, `refuter`, `judge`, `explorer`, `investigator`, `worker`, or `other:<name>`) says what it does; its
  status in `loops/agents.yaml` (`draft`, `evaluated`, `advisory`, `gate`, `retired`) says whether it may block.
- **Profile**: `loops/profile.yaml`, the facts loops are chosen by: what the project ships, its stack, where a
  change goes (CI, preview, staging, production), what the agent can reach, how work goes through the project's
  super-loops now (where it comes from, where a change ends, the checks at each place), and the failures to catch
  first, each with the place that should catch it. How to fill it and use it: `$S/profile.md`.
- **Map**: the project's super-loops drawn from the profile, one line each, with a `✓` and the check at every phase
  that has one and a `✗` at every gap. `/agentify:init` confirms it with the user; a proposal of loops starts from it.
- **Call to a person**: a question you put to the user in this session, including a request for approval. Every
  call has a policy id from `hitl.allowed` and goes into `loops/hitl-log.jsonl`.
- **Status** of a loop, in its `LOOP.md`: `proposed` (the spec is written), `built` (`run`, cases and wiring
  exist), `validated` (it passed validation), `active` (wired in on the main branch), `retired`. A loop you revise
  goes back to `built` until it passes validation again.

## The project's policy

`loops/policy.yaml` in the project decides two things. Read it before any action; only the project's copy counts.

- `autonomy`: what you may do without asking: edit guides, write instrumentation into product code (logs, health
  endpoints, test seams; never features), create agent steps, commit, push, merge, and the spend limit.
- `hitl`: the reasons you may call a person (H1–H7 by default), the questions you never ask, and how you ask.

The project's policy changes only with the user's approval (H7).

## Talking to the user

You talk to the user only in this session: never through Slack, Jira, email or another channel. Do not hand a
question to a subagent either: a subagent cannot talk to the user, it only reports back to you.

- **Do not ask what you can find out.** Before any call to a person, look in the repository, its docs and
  history, the tools' `--help`, and run commands. Every question says what you already checked.
- **Call a person only under a policy id.** If no `hitl.allowed` entry fits, decide yourself and say what you
  decided.
- **One question at a time.** Use the session's question tool with 2–4 options, the recommended one first, and
  room for a free answer. The one exception is the setup form (`$S/profile.md`): up to 4 questions in one call.
- **Short and clear.** Lead with the decision or the result; leave out what the user does not need to act.
- **Show, do not describe.** A diagram of the loop in a code block, a table for validation results and options,
  a screenshot when a UI is involved, real command output instead of a summary of it.
- **Log every call to a person**, with its answer:
  `python3 $S/scripts/loops.py hitl <id> --loop <loop-id> --checked "<what you checked>" --question "…" --answer "…"`

A loop diagram looks like this:

```
 git commit ──► pre-commit hook ──► ./run (gitleaks) ──► exit 1: file:line + how to fix
                                                     └─► exit 0: commit goes through
```

## Setup: `/agentify:init`

`/agentify:init` sets a project up: it finds out what `$S/profile.md` lists, recognizes the checks the project
already runs and places each in its super-loops, confirms that map with the user, and decides the policy. It builds
no loop.

## Choosing loops: the harness level's discovery

A harness task that asks which loops to build, such as the first one after init:

1. If the profile has no `pains`, ask the form's Q4 (`$S/profile.md`) under H4.
2. Draw the map with its gaps (`python3 $S/scripts/loops.py map`) and propose one loop per pain at the earliest phase
   that can catch it (`python3 $S/scripts/loops.py candidates <place>`; `$S/profile.md`, "From the profile to the
   map and the loops"), usually 1–3, never more than 5. Show each one's place, what it catches, where it runs and
   what it builds on; the gaps that stay open and what they mean; and a short "not now" list with reasons.
3. Ask which to build (H4). Each loop the user chose is then built as the harness level's delivery, by the steps
   below.

## Building a loop, or a set of loops

1. **Take the requirements.** Write down the failure the loop prevents, who asked for it, and its place: the
   super-loop and the phase that should have caught the failure. Pick the loop type: read the summaries in
   `loop-types/index.yaml` (its `by_place` lists the loop types of each place), then the card. Create the loop:
   `python3 $S/scripts/loops.py new <id> --type <type-id>` (or `--type custom`).
2. **Confirm the tools.** Find each tool the loop needs, install it if the policy allows, run it once, and note
   its version in the Tools section of `LOOP.md`. Missing access is H3.
3. **Build it.**
   - `run`: takes the directory to check as its only argument, exits 0 when the check passes and non-zero when it
     fires, and prints `file:line: message` or JSON. The message says how to fix the problem.
   - Cases: at least one directory in `cases/must-fire/` for each kind of failure the loop must catch, and at least
     one in `cases/must-pass/` that it must leave alone.
   - Wiring: hook the loop in where it runs: a Claude Code hook, a git hook, a CI job, a scheduled job. List each
     place under `wiring`.
   - Agent steps: see below.
4. **Validate it.**
   - `python3 $S/scripts/loops.py validate <id>`: every must-fire case fires, every must-pass case passes, each
     run gives the same result, and every run fits `budget_seconds`.
   - Make sure the agent the loop checks cannot edit or switch it off: the final run of the check happens where that
     agent has no write access, such as CI, a protected branch or a hook outside its working tree.
   - Then trigger the wiring once for real, in a scratch branch or worktree, and keep the output as evidence.
   - Agent steps need their evals to pass as well.
   - Set `status: validated`.
5. **Iterate.** Fix what validation or the user found, add a line to `CHANGELOG.md`, and validate again.
6. **Document and commit.**
   - Complete every section of `LOOP.md`.
   - Review `LOOP.md` and every agent prompt you wrote with the `document-review` loop type
     (card `loop-types/meta/document-review.md`, part `text-quality`).
   - `python3 $S/scripts/loops.py index`, then `python3 $S/scripts/loops.py check`.
   - Commit, push and merge as far as the policy allows. Once the loop is wired in on the main branch, set
     `status: active`.

A composite loop is built after its parts: each part is its own loop, built and validated by the steps above.
Then build the composite's gate as its `run`, with must-fire cases for states of the whole that no part catches
(for the acceptance loop: a requirement without a test, a test green before the work, a weakened acceptance test).
`loops.py check` refuses a composite that is `validated` or `active` while a part is behind it.

Report the result to the user in a few lines: the loop diagram, the validation table, and anything still open.

Prefer loops that run without a person. Add a human-in-the-loop step only where no check can stand in for a
person's judgement, and then pick its loop type from `loop-types/human/`.

## Agent steps

A loop type's card says, in its Agent step section, what kind of agent may help. You design the agent for the
loop's failure; there is no fixed list of agents to install.

**Design.**

- **Reuse first.** Look for an agent that already does the job: `.claude/agents/`, the project's plugins (for
  example a reviewer and a finding verifier from a language plugin), `loops/agents.yaml`. A second loop that needs
  the same kind of agent uses the registered one.
- **The one who works does not grade.** A reviewer, refuter, guard or judge is a separate agent with a fresh
  context. It gets what the loop checks (the diff, the requirement, the claim, the artifact), never the working
  agent's reasoning or its own verdict.
- **The least rights.** A reviewer, a guard and a judge only read. A refuter, an explorer and an investigator may
  run commands and open the app, and change nothing in the product, its tests or its spec. Only a worker opens
  PRs, and never merges them.
- **One output format** from `$S/agent-formats.md`: Finding, Finding check, Verdict or Diagnosis, so other agents
  and scripts can use it.
- **A limit on rounds** between the working agent and a reviewer or a refuter, with what happens at the limit
  (usually a call to a person under the loop's `hitl`).

**Create and calibrate** (loop type `meta/agent-calibration`):

1. Create an agent only for a loop whose `LOOP.md` lists it under `agents`, and only if
   `autonomy.create_loop_agents` allows it: `python3 $S/scripts/loops.py agent-new <id> --kind <kind>`. It
   registers the agent as `draft` and, if the definition is missing, writes it from `$S/templates/agent.md`.
2. Write eval cases in `loops/agents/<id>/evals/` (`$S/agent-formats.md`, Evals): for a reviewer, a guard or a
   refuter, broken copies that must fire and clean ones that must pass, usually taken from the loop's own cases;
   for a judge, results a person graded pass or fail with a reason (H5).
3. Run the agent on every case at least 3 times, one `results/<run>.jsonl` per run, then
   `python3 $S/scripts/loops.py eval-score <id> --record`.
4. Ask the user to approve the threshold (H5) and write who approved it in `threshold_source`. When the agreement
   reaches it, the agent becomes `gate` and may block; until then, or if it never does, it is `advisory`: its
   loop prints its verdict and exits 0. An agent that stays far below and cannot be fixed is `retired`.
5. In use, log what happened to its verdicts: `python3 $S/scripts/loops.py outcome <id> --loop <loop> --outcome
   confirmed|false-positive|missed|overridden`. Each false positive or miss becomes a new eval case.

Evaluate again when its definition or its model changes (`loops.py check` refuses a gate that was not re-scored),
when `loops.py stats` shows false positives or misses since the last evaluation, and when a sample audit finds
mismatches.

## Maintaining loops: the harness level

Your own work is the four super-loops at the harness level (`$S/super-loops/harness-level.md`): choosing the
loops is its discovery, building a loop is its delivery, and the cases below are its remediation and maintenance. Its signal is
the trace of the product's super-loops; the strongest is a change that passed the gate and was not confirmed.
`python3 $S/scripts/loops.py stats` reads the trace: the change failure rate, the releases not confirmed and not yet
analysed, and the places where escapes and corrections pile up. Log what no system records, such as a correction
the user made or an escape you traced to its phase:
`python3 $S/scripts/loops.py trace escape|correction|revert <super-loop>/<phase> --item <id> --note "…"`.

Look at a loop again when:

- a change passed the gate and was not confirmed where it is used, or a problem came from a recent change: find the
  phase that should have caught the failure, and fix or add the loop there;
- it fires on correct code, or misses a failure it should catch: add that case, fix the loop, validate again; when
  the loop's agent was wrong, also log the outcome and add the case to the agent's evals;
- `python3 $S/scripts/loops.py stats` shows the same question asked more than once: automate the answer, or
  propose to settle it in the policy (H7);
- the user corrects the agent twice for the same thing: turn the correction into a loop
  (`loop-types/human/correction-becomes-rule.md`);
- a tool, a model or the loop type changes;
- the project changes: a new CI job or stand, a tool connected or lost. Update `loops/profile.yaml` and redraw the
  map, then check which loops the change allows or makes useless.

Retire a loop when it fires mostly on correct code and cannot be fixed, or when the failure it catches is now
caught earlier by another loop. To retire it, remove its wiring, set `status: retired`, and keep the folder as
history.

## Before every commit that touches `loops/`

Run `python3 $S/scripts/loops.py check`. This includes the setup commit and every commit that builds, revises or
retires a loop.

## Files

`S` is this part's folder, `parts/harness` of the plugin.

| Path | What |
|---|---|
| `$S/profile.md` | The setup form, the profile and how to choose loops from it |
| `$S/defaults/policy.yaml` | The default policy that setup starts from |
| `$S/defaults/profile.yaml` | The empty profile that setup fills in |
| `$S/templates/LOOP.md` | The template for a loop's spec |
| `$S/templates/agent.md` | The template for an agent that is a step of a loop |
| `$S/agent-formats.md` | What agents return (Finding, Finding check, Verdict, Diagnosis), their evals and outcomes |
| `$S/super-loops/` | The four super-loops and the harness level: phases, oracles, gates, confirmations, exits, trace |
| `$S/loop-types/` | The catalog: `README.md`, `index.yaml`, one card per loop type |
| `$S/scripts/loops.py` | `init`, `new`, `validate`, `check`, `index`, `hitl`, `stats`, `agent-new`, `eval-score`, `outcome`, `map`, `candidates`, `trace` for the project's `loops/` |
| `$S/scripts/catalog.py` | `index` and `check` for the catalog itself |

In the project:

| Path | What |
|---|---|
| `loops/policy.yaml` | The project's policy |
| `loops/profile.yaml` | The project's profile: what loops are chosen by |
| `loops/index.yaml` | The registry of loops, built from every `LOOP.md` |
| `loops/hitl-log.jsonl` | Every call to a person, with its policy id and answer |
| `loops/<id>/` | `LOOP.md`, `run`, `cases/must-fire/`, `cases/must-pass/`, `CHANGELOG.md` |
| `loops/agents.yaml` | The agents that are steps of loops: kind, definition, model, status, threshold, last evaluation |
| `loops/agents/<id>/` | An agent's `evals/`, `results/` and `report.md` |
| `loops/agent-outcomes.jsonl` | What happened to the agents' verdicts in real use |

The scripts need only Python 3. The `document-review` loop type needs the text-quality part (`$S/../text-quality`) and
the `claude` CLI.

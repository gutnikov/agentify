---
name: init
description: Study this project, recognize the loops it already runs (CI jobs, hooks, linters, deploy checks, specs, agent loops), place each in the project's super-loops (delivery, remediation, maintenance, discovery), and confirm that map and the policy with the user. Writes loops/; builds no loop and changes no product code.
disable-model-invocation: true
argument-hint: "[the part of a monorepo to map]"
---

# agentify init

Init finds out how work goes through this project now and which loops already check it, and confirms both with the
user. It ends with the map of the project's super-loops in `loops/profile.yaml` and a policy in `loops/policy.yaml`:
what every `/agentify:task` reads. It builds no loop and changes no product code; a gap on the map is filled by a task.

Focus, if the user gave one: $ARGUMENTS

**Paths.** `P` is `${CLAUDE_PLUGIN_ROOT}/parts` and `H` is `${CLAUDE_PLUGIN_ROOT}/parts/harness`. They are not
shell variables: write the full path in every command. `loops.py` means
`python3 ${CLAUDE_PLUGIN_ROOT}/parts/harness/scripts/loops.py`, run from the project's root.

**Read first:** `$H/README.md` (Terms; Talking to the user), `$H/super-loops/README.md` (the phases) and
`$H/profile.md` (where to look, the form, the profile).

## What counts as a loop

A loop is anything that checks the agent's work and whose result the agent can run or read. Init recognizes the
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
| `specs/` with its checks, acceptance criteria someone approves | the oracle of delivery | `delivery/oracle` |
| Prototypes, spikes, decision records | the work of discovery and its answers | `discovery/work`, `discovery/confirmation` |
| Reviewers, refuters and judges in `.claude/agents/` | an agent step | the place of the loop it serves |
| `loops/<id>/LOOP.md` from an earlier agentify or `harness` setup | a loop built for this project | its `places` |

A place without a super-loop, such as `release`, means that phase of every product super-loop the project has.

Not loops: a linter config or a test suite that nothing runs, and the guides (CLAUDE.md, AGENTS.md), which steer the
agent but check nothing. Note them for the report: a config nothing runs is a cheap loop to wire in later.

For each loop, find what decides whether it blocks: a required status check in the branch protection,
`continue-on-error`, `allow_failure`, a hook that only warns. A loop that cannot block says "advisory" in its details.

## 1. Find out, without asking

If `loops/policy.yaml` exists, this is a second run: go to "Running init again".

Find out everything `$H/profile.md` §1 lists: the stack, the kind, the stages, the tools (each checked with one real
call), where the work of each super-loop comes from, where a change ends, and what has gone wrong. Then find every
loop of the table above. Read what a CI job or a hook runs, not only its name. In a monorepo, map the part the focus
names; if there is no focus and the repository leaves it open, ask which part (H1).

## 2. Write the map

1. `loops.py init` creates `loops/` with the default policy and an empty profile, and keeps what already exists.
2. Fill `loops/profile.yaml` (`$H/profile.md` §3):
   - `existing_checks`: every loop you found, as `"<name>: <places> — <where it runs, what it does>"`. A loop in
     `loops/<id>/` is not repeated here: its `LOOP.md` places it.
   - `super_loops`: each super-loop the project has work for, with where its work comes from; `not_here`: the others,
     each with the reason.
   - `ends_at`, and `trace`: the files where the project records its deploys and their results.
   - `pains`: the failures the history shows, each with the place that should have caught it and its evidence.
3. Draw the map: `loops.py map`.

## 3. Confirm it with the user

Show the map, then the loops behind it:

```
Profile: api (Go) · ci, production · tools: ci (gh), logs (ops/prod logs)
Ends at: production, by ops/prod deploy; nothing confirms it after the deploy

delivery     entry ✓ issues · oracle ✗ · work ✓ make ci · gate ✗ · release ✓ ops/prod deploy · confirmation ✗
remediation  entry ✗ · oracle ✗ · work ✓ make ci · gate ✗ · release ✓ ops/prod deploy · confirmation ✗
maintenance  entry ✓ dependabot · oracle ✗ · work ✓ make ci · gate ✗ · release ✓ ops/prod deploy · confirmation ✗
not here     discovery: every idea the team brings gets built

| Loop       | Places                                    | Runs                       | Blocks             |
|------------|-------------------------------------------|----------------------------|--------------------|
| make ci    | delivery, remediation, maintenance / work | CI job ci, on every PR     | yes, required      |
| dependabot | maintenance/entry                         | weekly, opens PRs          | —                  |
```

Then ask in one call of the question tool, up to 4 questions. This form is the one exception to one question at a
time, as in `$H/profile.md` §2, and each question says what you found, because the user may see only the form.

- **Map**, always: "Is this how work goes through <project> now? Found: <n> loops, <the gaps in a few words>."
  Single-select, with the map as the preview of the first option: "Yes, as drawn" (recommended); "A loop is missing
  or misplaced" (the user says which in the notes); "A super-loop is wrong" (one the project does not have, or one
  that is missing).
- **Project**, **Dev flow**, **Tools**: only those of `$H/profile.md` §2 that step 1 did not settle.

Init does not ask what to catch first (the form's Q4): it records the history, and choosing loops is a task.

Log every question with its answer, Map and the profile questions under H1:
`loops.py hitl H1 --loop init --checked "…" --question "…" --answer "…"`.

Write the answers into the profile and draw the map again. Show the new map; ask once more only if the answers
left something open.

## 4. Decide the policy

The policy governs every task, at the product level and the harness level alike (`$H/README.md`, "The project's
policy").

1. Adjust `loops/policy.yaml` to what you found. A protected branch that needs a review means `merge: false`,
   whatever the default says; a deploy only a person may start stays H2.
2. Show it as two tables, the autonomy and the reasons to call a person, and ask only about the points where the
   default could go either way, one question at a time (H7).

A `specs/policy.yaml` that already exists stays as it is: the spec part reads it in the oracle phase of delivery.

## 5. Check and commit

Run `loops.py check`. Commit `loops/` if `autonomy.commit` allows it, with the message "agentify init: the map of
the project's loops", and push only as far as `autonomy.push` allows.

## 6. Report

A few lines: the map as confirmed, what the user corrected, the gaps and what each one means for "done" today (where
nothing confirms a change, a person decides, or nobody does), and the guides and unwired configs you found. Then up
to 3 tasks worth starting, each from a gap with evidence in the history, as commands the user can copy:

```
/agentify:task choose the first loops for the pains on the map
/agentify:task set up specs for delivery
```

Init starts none of them.

## Running init again

When `loops/policy.yaml` exists, init keeps the policy and the loops. It finds out again and compares what it sees
with `loops/profile.yaml`: a new CI job, a stand added, a tool lost, a loop retired, a pain fixed. It asks only about
the differences, in the same form, then checks, commits and reports as above. It does not ask about the policy again;
a change to the policy is H7.

## Init never

- builds, changes, wires in or retires a loop: that is a task;
- changes product code, the CI config or the hooks;
- asks what the repository, its history or a command can answer.

# Spec engineering

The part of agentify that writes the oracle of a delivery task: `/agentify:task` follows it in the oracle phase.
`S` is this part's folder.

In that phase you are the project's **spec engineer**. You own `agentify/specs/`: the requirements as they came, the spec of
the system written from them, and the checks that keep the spec whole. You write neither product code nor tests: the
tests are the test writer's and the code is the worker's, each in a context of its own.

A separate agent or person writes the tests from your spec (`agentify/specs/profile.yaml`, `tests.writer`). They are your
first reader. Everything you write is judged by one question: **can the test writer derive every test from it
without guessing?**

## Written for the tests

1. **Enumerable.** Every command lists the errors it can return. Every rule is a complete table. Every outside
   system lists its outcomes. Everything that happens on time is a slice with a clock. A test writer can list what
   to test mechanically.
2. **Observable.** Every result is something a test can see: a screen, a field, a value, an error. A requirement no
   test can observe ("fast", "convenient") gets a metric and a threshold, or goes back as a question. Every
   functional requirement is also observable in production: its `prod` names the signal a release's confirmation
   looks for, or says why nothing in production can show it.
3. **Concrete.** Every precondition is a named state with its values (plan, balance, counts): a fixture can be
   built from it.
4. **Traceable.** Requirements, slices, rules and examples have stable ids. Tests are tagged with them; the trace
   runs both ways.
5. **Explicit about the unknown.** A rule nobody knows is a question, not a value. The test writer marks such a
   test `fixme` instead of guessing.
6. **Diffable.** After every change, `specs.py delta` lists what was added, changed and removed: the test writer's
   work list.

## Just enough spec

- **One spine, layers for risks.** The event model is the spine; every other layer exists for a risk the profile
  names (money, concurrency, a public API…) and feeds its obligations into the spine as examples.
- **No format without a check.** A layer is set up with the command that checks it, and that check is shown to
  catch a broken copy of the spec. Most formats' official tools check syntax only; the catalog says what each one
  misses.
- **The cheapest form that covers the risk.** A table in the spine before a DMN file, a status field before a
  statechart, an example of the race before a TLA+ model.
- **Nothing the project cannot run.** A layer whose check needs a tool the project lacks is proposed with its cost,
  not set up on the way.

## Terms

- **Requirement file**: `agentify/specs/requirements/<KEY>.yaml`, the requirements from one source (a ticket, or a text),
  each atomic, with a stable id `<KEY>#<n>`, its kind (functional, nfr, constraint) and the questions it raised.
- **Spec type**: a format from this part's catalog, `spec-types/`. **Layer**: a spec type this project keeps,
  registered in `agentify/specs/layers.yaml` with its path, check, status and the risk it covers. **Spine**: the
  `event-model` layer.
- **Example**: an e2e-ready spec in the spine: a named state, inputs, forced outcomes of outside systems, and what
  the person sees or the error.
- **Test obligation**: something an exhaustive e2e set must check (a command's success, each error, each outcome,
  each time-driven step, each decision-table row, each field on a screen). `em.py check` lists the ones no example
  pins down yet.
- **Trace**: requirement ↔ spec element, through `reqs:` on slices, examples, states and rules.
- **Production signal**: `prod` on a functional requirement: what shows in production that it happened (`signal`,
  in words), the log fields that pick it out (`match`), and how many times a release's window must see it (`min`). A
  slice's event is usually the signal, logged as `{"event": "TeamCreated"}`. `specs.py signals` hands the signals of
  a change to the release's confirmation, so the trace runs on from the test to production.
- **Delta**: the spec elements added, changed and removed since a git ref.
- **Layer status**: `proposed`, `set-up` (path and check exist), `validated` (the check caught broken copies and
  passed the real spec), `active` (wired in), `retired`.

## The project's policy

`agentify/specs/policy.yaml` decides what you may do alone (`autonomy`), what you never invent (`never_invent`), who answers
questions and why you may ask (`ask`, reasons R1–R5). Read it before any action; only the project's copy counts. It
changes only with the user's approval (R5).

Every call to a person is also logged with the harness part's `loops.py hitl`, under the id of
`agentify/policy.yaml` its reason maps to: R1 and R2 → H1, R3 → H4, R4 → H5, R5 → H7.

## Talking to the user

- **Do not ask what you can find out**: the ticket, its comments and links, the code, the running app, the docs.
  Every question says what you already checked.
- **One batch per requirement file.** All its open questions in one message, grouped, each with what each answer
  changes in the spec; options when it is a choice. This is the exception to one question at a time: the answers
  are needed together.
- **Record every answer** in the requirement file (`answer`) and in the spec, then check again.
- **Show, do not describe**: the trace for the key, the delta, the check output.

## Setup: once per project

Run this when the project has no `agentify/specs/policy.yaml`. It sets up the oracle of delivery, so it is a harness task
(`/agentify:task set up specs`); a delivery task that finds no `agentify/specs/` offers it first.

1. **Find out** what `$S/profile.md` §1 lists, without asking.
2. **Create** `agentify/specs/`: `python3 $S/scripts/specs.py init`.
3. **Ask what is left** in one form (`$S/profile.md` §2) and fill `agentify/specs/profile.yaml`.
4. **Adjust** `agentify/specs/policy.yaml`: who answers (`ask.who`), whether you may approve. Show it to the user and change
   only what they decide (R5).
5. **Propose the layers** (`$S/profile.md` §3): the spine, the glossary, and 0–3 layers for named risks, with a
   "not now" list. The user picks (R5).
6. **Set up each picked layer** from its card (`$S/spec-types/<group>/<id>.md`, "Set up"): its path, its `check`
   command in `agentify/specs/layers.yaml`, status `set-up`. The spine is written with the `event-model` part
   (`$S/../event-model`); its check is `python3 $S/../event-model/scripts/em.py check --strict agentify/specs/model/`.
7. **Validate each check**: make 2–3 broken copies of the spec in a scratch folder (a field from nowhere, an error
   without an example, a reference to a missing requirement), run the check on each and on the real spec. It must
   fire on every copy and pass the real one. Then status `validated`.
8. **Wire it in**: build its `spec-check` loop (loop type `testing/spec-check`, "Building a loop" of the harness part)
   so the checks run on every change under `agentify/specs/`. Status `active` once wired on
   the main branch. Commit, as far as the policy allows.

## Taking a requirement

1. **Read the source.** A ticket by link: through the tracker access this session has (a Jira MCP, `glab`, `gh`):
   the description, acceptance criteria, comments and linked tickets. Never write to a tracker. A text: as given.
   Create the file: `python3 $S/scripts/specs.py new-req <KEY> --source <url or "text from …">`.
2. **Split it** into atomic requirements in the source's words: one behaviour or constraint each. Do not repair a
   requirement; what is unclear becomes a question.
3. **Write the spec.** Find the slices, examples, states and rules the requirements change or add, and write them
   in their layers' formats; the event model through the `event-model` part. Every element you add or change
   lists its requirements in `reqs:`. For every functional requirement, write `prod`: the signal that shows it
   happened in production, the fields that pick it out, and how many times the release's window must see it; or
   `signal: none` with a `why`.
4. **Check until clean**: `python3 $S/scripts/specs.py check` and every layer check it lists. Zero errors. For the
   elements you touched, pin down every test obligation `em.py check` reports, or turn it into a question.
5. **Ask once** (R1–R3): all open questions of the file in one message; status `questions`. Record the answers, then
   check again.
6. **Approval** (R4): show the trace (`specs.py trace --req <KEY>`) and the delta. The person approves; write
   `approved_by`, `approved_at`, status `approved`. Never approve on your own unless `autonomy.approve` allows it.
7. **Hand off to the test writer**: the change, `python3 $S/scripts/specs.py delta --base <ref>` (the branch's base,
   or the last commit before your change), and the contract, `python3 $S/../event-model/scripts/em.py export
   agentify/specs/model/ --out <file>`. Put the delta in the merge request or the report, with the questions still open:
   those tests are `fixme`.
8. **Hand off to the release's confirmation**: `python3 $S/scripts/specs.py signals --base <ref> --out <file>`, the
   production signals of every requirement the change touches, written where the project's confirmation reads them.
   That is the input of the project's `release-confirmation` loop, if it has one.

## Reverse engineering an existing app

When the requirement is "what the app does now", the running app is the source. Look at it read-only, with
`app-probing` or a browser: never create, buy, publish or change settings in an account that is not a test account.
What you saw becomes the spec; what you inferred becomes a question. Such examples carry no `reqs:`; `specs.py
check` counts them.

## Maintaining the spec

Look again when:

- a ticket changes: re-read it, update the requirement texts, check, ask, approve, hand off a new delta;
- the test writer reports that the app and the spec disagree: find out which is wrong. A feature being built: the
  app is wrong, the spec stays. A spec of an existing app: correct the spec, and say so in the delta;
- the same question comes back for another ticket: turn its answer into a rule in the spec, or propose it for the
  policy (R5);
- a check fires on a correct spec, or misses a broken one: fix the check, keep the broken copy as its case;
- the profile changes (a new service, a public API, payments): propose the layer the new risk needs. Retire a layer
  whose risk is gone: status `retired`, its files kept as history.

## Files

| Path | What |
|---|---|
| `$S/profile.md` | The setup form, the profile and how to choose layers from it |
| `$S/defaults/` | `policy.yaml`, `profile.yaml`, `layers.yaml` that setup starts from |
| `$S/templates/requirements.yaml` | A requirement file |
| `$S/spec-types/` | The catalog: `README.md`, `index.yaml`, one card per spec type |
| `$S/scripts/specs.py` | `init`, `new-req`, `check`, `trace`, `delta`, `signals`, `catalog index|check` |
| `$S/../event-model/` | The spine's part: `README.md`, `format.md`, `scripts/em.py` (`check`, `export`), a template and an example |

In the project:

| Path | What |
|---|---|
| `agentify/specs/policy.yaml`, `agentify/specs/profile.yaml` | The policy and the profile |
| `agentify/specs/layers.yaml` | The layers: type, path, check, status, why |
| `agentify/specs/requirements/<KEY>.yaml` | Requirements from one source, their questions and the approval |
| `agentify/specs/model/` | The spine: the event model |
| `agentify/specs/glossary.yaml` and other layers' files | As each layer's card says |

`specs.py` and `em.py` need Python 3 and PyYAML.

## A spec never

- holds a value from `never_invent` that no source gave: it is a question;
- describes how the system is built (tables, services, endpoints) where it should say what happens and what a
  person sees;
- has an example whose result a test cannot observe;
- changes what an approved requirement means without a new approval;
- writes to a tracker, or contains a test.

## Done when, for a requirement

- its file is `approved`, and every requirement in it is covered by a spec element (`specs.py trace`);
- `specs.py check` and every layer check report zero errors;
- every test obligation of the elements it touched is pinned down by an example, or has an open question;
- every functional requirement in it has a production signal, or says why it has none;
- the delta went to the test writer, and the signals to the release's confirmation.

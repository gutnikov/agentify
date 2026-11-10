---
name: event-model
description: Describes a system as an Event Model in YAML — slices of screens, commands, events, read models, automations and translations, rules as decision tables, open questions — and checks it with a script until it has no errors: every field traced to where it comes from, every command with a success and a failure example, every decision table's gaps listed, every spec written so it becomes an e2e test. Use before a feature or a product is built ("describe the system", "write the spec for billing", "model the onboarding"), to reverse-engineer an existing app into a spec, when a spec must be checkable by an agent, or "/event-model <what>".
---

# Event model

```
/event-model <the system, feature or change, in plain words>
```

An Event Model describes a system as a timeline of **slices**. A person on a screen issues a command, the command
records events, events build read models, read models are what screens show. Automations react to events or to
time; translations bring in what an outside system answers. Each slice carries examples (**specs**). The model
is written for the people and agents who will test the system: each e2e-ready example becomes one test, written by
them, not by this skill.

The model is the spec. It is text in the repository, so an agent can write it and a script can check it. The
script finds what a reader misses: a field on a screen that nothing produces, a command with no failure example,
a price table with holes.

`S` is this skill's folder (Claude Code shows it when the skill loads: "Base directory for this skill").
The format: `$S/format.md`. A full example: `$S/examples/vendy.em.yaml`. Needs Python 3 and PyYAML.

## 1. Find or start the model

This skill is the spine of the `spec` skill, in the same plugin. Look for `*.yaml` files with `slices:` in the
repository, usually `specs/model/`. Extend that model; one system, one model. If there is none, create
`specs/model/`, one file per area (`billing.em.yaml`, `onboarding.em.yaml`), starting from
`$S/templates/model.em.yaml`. The model is committed.

## 2. Write it along the timeline

Go through the system in the order a person meets it. For each step:

1. **The screen and what it shows**: a `view` slice. Every field of the read model names the event fields it comes
   from.
2. **What the person does there**: a `command` slice. Every command field is typed (`input`), picked from what the
   screen shows (`<ReadModel>.<field>`), or made by the system. List every error the command can return in
   `errors`.
3. **What the system does on its own**: an `automation` (after an event or on time) or a `translation` (an outside
   system answers; its data is `ext`).
4. **The rules** the step depends on: a decision table with domains, or a formula. A rule nobody knows is written
   with `unknown: true`, never invented.
5. **Specs** for every slice that changes something (§3).
6. **Questions**: anything the sources do not settle goes into `questions` of the slice, worded so a person can
   answer it in one line.

Name things in the product's language. One name for one thing across the model: if the UI says "credits", the
model never says "tokens".

## 3. Specs are future e2e tests

Write them in the full form (`$S/format.md`, "Specs"):

- `given` is a **named state** from `states`, not a list of events. A state is a fixture: name it after the state
  (`sellerWithProduct`), one state adds one thing to its parent, at most three levels deep, its `note` holds the
  concrete values. These are the `playwright` plugin's fixture rules; the model follows them so the fixtures can.
- `when` holds the inputs the person gives, nothing else.
- `external` forces an outside system's outcome (`{AIModels: fails}`); `after` lets time pass (`periodEnd`).
- `then` ends in what the person **sees** (`see`: a screen, a read-model field on it, the value) or in an `error`.
  Events in `then` are optional: a browser test cannot observe them.
- Every command slice gets a success spec and one spec per error in its `errors`; an example that checks a row
  of a decision table says so in `covers`.
- A spec that depends on an open question keeps its `question`; the test writer marks its test `fixme`.

## 4. The check loop

After every edit:

```bash
python3 $S/scripts/em.py check model/
```

| Section | What to do |
|---|---|
| `ERRORS` | Fix them all. An error is a broken trace: a field from nowhere, a screen nobody renders, a spec that names a state, input or field that does not exist |
| `WARNINGS` | Fix, or turn into a question when only a person can decide: an event nobody consumes is usually a missing read model ("what does the person see when this fails?") |
| `DECISION TABLE COVERAGE` | Each missing combination is either a row to add or a question |
| `TEST READINESS` | Examples not yet in the full form, and test obligations no example pins down: a command's success or one of its errors, an outside system's outcome, a time-driven step, a decision-table row, a field on a screen. Each is a gap in the spec: add the example, or a question when only a person knows the expected result (`--all` lists them all) |
| `OPEN QUESTIONS` | Ask the person once, in one batch (§6) |

Done means zero errors, and every warning either fixed or recorded as a question.

## 5. Reverse-engineering an existing app

When the model describes an app that already runs, the app is the source. Look at it with `app-probing` or a
browser, read-only: never generate, buy, publish or change settings in an account that is not a test account.
Write what you saw as slices and what you inferred as questions. A screen's route goes into `screens`, so the
Page Object can find it.

## 6. Ask once

Collect the questions from the check, group them by area, and ask the person in one message with what each answer
changes. Record each answer in the model: a rule row, a spec, a removed question. Run the check again.

## 7. Hand the model to the test writer

This skill writes no tests. The test writer gets two things:

- **the contract**: `python3 $S/scripts/em.py export specs/model/ --out <file>`, the model as JSON
  (`event-model/1`, `$S/format.md`, "Handoff to the test writer"): states, screens, outside systems and their
  outcomes, examples, test obligations and open questions;
- **the change**: `specs.py delta` of the `spec` skill, the examples added, changed and removed since a git ref.

An open question in the model is a test the writer marks `fixme`, not a test they guess.

## A model never

- invents a rule, a price or a limit the sources do not give: it is `unknown: true` or a question;
- has a field that comes from nowhere: every field has a source the check can follow;
- ends a failure spec in silence: the person sees an error or a changed screen;
- keeps two names for one thing;
- describes how it is built (tables, services, endpoints): it describes what happens and what a person sees.

## Done when

- `em.py check` reports zero errors;
- every warning is fixed or recorded as a question, and the questions went to the person in one batch;
- every test obligation is pinned down by an e2e-ready example, or has a question that says why not.

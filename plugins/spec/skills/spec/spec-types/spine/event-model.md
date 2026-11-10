---
id: event-model
title: "Event model"
group: spine
role: spine
fits: [web, api, mobile]
risks: []
tests: [e2e, api]
checks: own
cost: medium
---

# Event model

## What it describes

The system as a timeline of slices: a screen and what it shows, a command a person issues there, the events it
records, the read models those events build, and what the system does on its own or hears from outside systems.
Every slice carries examples: a named state, the inputs, an outside system's forced outcome, and what the person
sees afterwards or the error they get.

## When it fits

Always, as the spine, for a product with screens or an API that people or other systems drive. It is the one place
the test writer reads: other layers add their obligations to it as examples.

## How it is checked

`em.py check` from this plugin's `event-model` skill. There is no official tool for the format; the check is
the plugin's own and deterministic:

- every field traced to its source (information completeness): nothing on a screen comes from nowhere;
- every command enumerates its errors, every example names a state that exists, inputs of the command, fields
  shown on the screen it checks;
- decision-table gaps and overlaps;
- test readiness: which obligations no example pins down yet.

## What the tests get

The full list of test obligations: each command's success and each of its errors, each outcome of each outside
system, each time-driven step, each decision-table row in use, each field a screen shows. Each example becomes
one test: the state is a fixture, the inputs are the action, `see` is the assertions, `error` is the expected
error. Stable slice ids and example names let tests be tagged and matched. `em.py export` hands all of it over
as JSON (contract `event-model/1`).

## Set up

1. Keep the model in `specs/model/`, one file per area, written with the `event-model` skill.
2. Layer entry: `type: event-model`, `check: python3 <spec plugin>/skills/event-model/scripts/em.py check --strict specs/model/`:
   `--strict` fails on a test obligation no example pins down, such as an error with no example.
3. Every slice and example that comes from a requirement lists it in `reqs:`.

## Evidence

Vendy: 45 slices, 956 lines. The first check found 8 errors in the author's own model (data missing on the screen
where a command needs it, field names that differ between command and event) and 3 failures the person would never
see. It produced 20 open questions, most about money. The e2e checks caught 6 of 6 seeded defects.

## Sources

- [Event Modeling](https://eventmodeling.org/) (Adam Dymitruk)

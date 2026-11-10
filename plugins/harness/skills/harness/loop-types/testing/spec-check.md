---
id: spec-check
title: "Spec check"
group: testing
qualities: [functional suitability, testability, analysability]
stages: [edit, commit, ci]
speed: [seconds]
places: [delivery/oracle]
---

# Spec check

## Loop

The agent changes the spec under `specs/` and runs `specs.py check` and the check of each spec layer, such as
`em.py check --strict` for the event model. A field that comes from nowhere, an error with no example, a decision-table row
no example checks, or a requirement no spec element covers comes back as a message that names the element and what
is missing. The test writer gets the spec only after the check is clean, with `specs.py delta` as the list of what
to add, change and delete in the tests.

## Set up

- The [`spec`](https://github.com/gutnikov/my-claude-plugins/tree/main/plugins/spec/skills/spec) plugin
  (`spec@private-plugins`): `specs.py` and, for the event model, `em.py` of its `event-model` skill.
  `specs/layers.yaml` lists each layer's check command.
- `run`: `specs.py check` followed by every layer's `check`; it fails when any of them fails.
- Cases: broken copies of the spec in `cases/must-fire/` (a field from nowhere, a command error without an example,
  a `reqs:` reference to a missing requirement), the real spec in `cases/must-pass/`.
- Wiring: a Claude Code Stop hook or a pre-commit hook on changes under `specs/`, and a CI job.

## Notes

- The official tools of most spec formats check syntax only: the Context Mapper CLI passed 7 of 7 seeded semantic
  defects, `gherkin-lint` 7 of 7. The semantic checks are the spec plugin's own.
- The check proves the spec is whole, not that it is right: approval of a requirement stays with a person.

## Related

- [acceptance-loop](../meta/acceptance-loop.md): the spec check is its first stage.

## Sources

- [Event Modeling](https://eventmodeling.org/) (Adam Dymitruk)

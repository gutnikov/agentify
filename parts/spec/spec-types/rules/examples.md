---
id: examples
title: "Examples in Gherkin"
group: rules
role: layer
fits: [web, api]
risks: []
tests: [e2e, api]
checks: own
cost: medium
---

# Examples in Gherkin

## What it describes

Behaviour as Given / When / Then scenarios in plain language, grouped by rule, with tables of examples.

## When it fits

Rarely as a separate layer: the spine's examples already are Given / When / Then, with a named state and
observable results. Add Gherkin only when people who do not read YAML must read and sign off the examples, and
generate it from the spine rather than keep it by hand.

## How it is checked

The official tools check little. `gherkin-lint` does not see scenarios inside `Rule:`; `cucumber --dry-run` reports
undefined steps but exits 0, even with `--strict`. Contradicting examples are found only by running them against
a reference model, and that model then answers open questions silently.

## What the tests get

Nothing beyond the spine's examples, unless the test writer uses Cucumber. Then the scenarios are the tests' text.

## Set up

Generate `.feature` files from the event model's examples; keep the slice id as a tag and the example name as the
scenario name.

## Evidence

Vendy: 5 feature files, 56 scenarios. Seeded defects: `gherkin-lint` 0 of 7, dry-run 1 of 7; running against a
reference model plus an own check 7 of 7. 420 lines of own code for 507 lines of spec. Found that "an active
subscription" was never defined (cancel-scheduled and past-due were treated differently in two places).

## Sources

- [Gherkin reference](https://cucumber.io/docs/gherkin/reference/)
- [gherkin-lint](https://github.com/vsiakka/gherkin-lint)

---
id: red-green-tdd
title: "Unit tests, red/green TDD"
group: testing
agent: [reviewer]
qualities: [testability, correctness]
stages: [local]
speed: [seconds]
---

# Unit tests, red/green TDD

## Loop

The agent writes a test and makes sure it fails (red). Then it writes the implementation until the run is green,
and refactors.

## Set up

To set up the loop:

- Add "use red/green TDD" to the agent's prompt. Simon Willison says any good model understands this shorthand.
  Kent Beck states the rule as: "Always follow the TDD cycle: Red → Green → Refactor".
- Stop the agent from deleting or weakening tests, for example by disabling a test or removing its assertions
  (see Notes). The source names two guards: a hook, and a review of the test diff. It does not say what the hook
  checks or who reviews the diff.
- Use checks the agent cannot edit as the final ones: CI, mutation testing, production.

## Notes

- Kent Beck names as a warning sign "any indication that the genie was cheating, for example by disabling or
  deleting tests". He also describes the agent deleting assertions and faking the implementation.

## Agent step

A guard: a reviewer whose only lens is the test diff. It returns a Verdict on whether the change weakened a test
(deleted, skipped, a loosened assertion, a changed expected value, the code under test mocked out). That answers who
reviews the test diff. It blocks only once calibrated on weakened and honest test diffs
([agent-calibration](../meta/agent-calibration.md)).

## Related

- [acceptance-loop](../meta/acceptance-loop.md): the outer loop around this one, from requirements to acceptance
  tests.

## Sources

- [Red/green TDD — Agentic Engineering Patterns](https://andrewmurphy.io/stdlib/b139fcdd-2733-435b-a97f-6d7e47836719) (Simon Willison)
- [agentic-engineering-patterns: Red/green TDD](https://github.com/lucas-flatwhite/agentic-engineering-patterns-simon-willison/blob/main/docs/en/03-testing-and-qa/01-red-green-tdd.md)
- [Augmented Coding: Beyond the Vibes](https://newsletter.kentbeck.com/p/augmented-coding-beyond-the-vibes) (Kent Beck)
- [Genie Wants to Leap](https://newsletter.kentbeck.com/p/genie-wants-to-leap) (Kent Beck)
- [Spec + TDD: The Combination That Actually Produces Shippable AI Code](https://www.augmentcode.com/guides/spec-tdd-shippable-ai-generated-code)

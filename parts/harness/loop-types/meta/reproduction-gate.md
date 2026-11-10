---
id: reproduction-gate
title: "Reproduction gate: a fix counts only against a reproduction that failed first"
group: meta
agent: [reviewer]
qualities: [correctness, reproducibility, traceability]
stages: [local, ci]
speed: [minutes]
places: [remediation/oracle, remediation/gate]
---

# Reproduction gate: a fix counts only against a reproduction that failed first

## Loop

A problem gets a reproduction before any fix: a test, a script or a recorded scenario that fails the way the problem
does. The agent fixes the code until the reproduction passes. The gate reports, for each problem, whether its
reproduction exists, failed before the fix and passes after it, and whether any other test changed on the way. It is
a composite loop: its parts are the project's reproduction and test loops, and its own check is the gate over them.

## Set up

- **Problems have ids**, from the error tracker or the issue tracker, and each reproduction is tagged with its
  problem's id.
- **Red first.** The reproduction's run from before the fix is kept: a CI job on the commit that adds the
  reproduction, or a run in the task's evidence. The gate compares the two runs.
- **A protected suite.** The agent fixing the problem cannot change the other tests: a PreToolUse hook denies its
  writes to them, and the final run of the gate happens in CI. A test that has to change goes through a person.
- **The gate is the `run`.** One line per problem, `<problem id>: <status>`: `no reproduction`,
  `green before the fix`, `red`, `green`, `other tests changed`. The exit is non-zero while any problem is not
  `green`.
- **When no test can reproduce the problem** (it is flaky, depends on the environment, or shows only in production),
  the gate records `no reproduction: confirmation only`, and the problem's confirmation carries all the weight
  ([release-confirmation](../production/release-confirmation.md)).
- **Cases.** Must fire: a fix without a reproduction; a reproduction that passed before the fix; a weakened test
  elsewhere. Must pass: a reproduction red before the fix and green after it, with the other tests untouched.

## Notes

- It settles what [bug-failing-test-fix](../testing/bug-failing-test-fix.md) leaves open: a test that passes before
  the fix, the agent changing the test instead of the code, a bug no test can catch.
- It is to remediation what the [acceptance loop](acceptance-loop.md) is to delivery.

## Agent step

A guard, a reviewer whose lens is the tests, returns a Verdict on whether the agent weakened any test other than the
reproduction: an assertion removed or loosened, a test skipped, an expected value changed. It gets the diff of the
tests, never the agent's reasoning, and it blocks only once calibrated ([agent-calibration](agent-calibration.md)).

## Sources

- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/)
  (OpenAI): a failing test that reproduces the bug, before the fix.
- [Genie Wants to Leap](https://newsletter.kentbeck.com/p/genie-wants-to-leap) (Kent Beck): agents that disable or
  delete tests.

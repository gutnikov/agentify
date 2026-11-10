---
id: run-tests-first
title: "Run the tests first"
group: testing
qualities: [testability, reproducibility]
stages: [local]
places: [delivery/work, remediation/work, maintenance/oracle]
---

# Run the tests first

## Loop

Before changing anything the agent runs the whole suite. It learns the state of the project and which tests
already fail, so later it does not mistake them for its own regressions.

## Set up

The source lists two things the project needs for this loop:

- A green main branch.
- A list of flaky tests.

## Notes

The source does not say:

- what the agent does when the run before its changes shows failing tests on main
- how the agent gets the list of flaky tests
- what the agent does when a flaky test fails, either before its changes or after
- what to do when the full suite is too slow to run before every change

## Sources

- [Simon Willison's playbook for working with coding agents](https://ai.sulat.com/simon-willisons-playbook-for-working-with-coding-agents-d56ccd3f959f)

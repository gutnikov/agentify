---
id: exploratory-testing
title: "Exploratory testing"
group: human
agent: [explorer]
when: [after]
initiator: human
sync: async
assesses: [result]
stages: [preview, staging]
speed: [hours]
places: [delivery/release, remediation/entry]
---

# Exploratory testing

## Loop

The person tries the product by hand and writes a bug report; the agent reproduces the bug with a failing test and
fixes it.

## Getting a good signal

To get a good signal from this loop:

- Give people a bug report template with fields for steps, expected result, actual result and environment.
- Turn each manual finding into a regression test, so the person never has to catch the same bug again.

## When and how long

On a preview or staging; hours.

## Agent step

An explorer reproduces the person's bug report on a fresh state and returns the steps that reproduce it, or why it
does not reproduce. It does not block; the failing test written from its steps does.

## Related

- [bug-failing-test-fix](../testing/bug-failing-test-fix.md): what the agent does with the report.
- [app-probing](../../../app-probing/README.md) (a part of agentify): how the agent reproduces the report in the running app.

## Sources

The note cites no source for this loop.

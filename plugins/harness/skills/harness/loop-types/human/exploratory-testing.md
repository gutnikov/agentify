---
id: exploratory-testing
title: "Exploratory testing"
group: human
when: [after]
initiator: human
sync: async
assesses: [result]
stages: [preview, staging]
speed: [hours]
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

## Related

- [bug-failing-test-fix](../testing/bug-failing-test-fix.md): what the agent does with the report.
- [app-probing](https://github.com/gutnikov/my-claude-plugins/tree/main/plugins/app-probing/skills/app-probing) (plugin `app-probing`): how the agent reproduces the report in the running app.

## Sources

The note cites no source for this loop.

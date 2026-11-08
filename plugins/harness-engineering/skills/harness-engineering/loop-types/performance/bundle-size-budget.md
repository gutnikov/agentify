---
id: bundle-size-budget
title: "Bundle size budget"
group: performance
qualities: [resource utilization]
stages: [ci]
speed: [seconds]
---

# Bundle size budget

## Loop

size-limit "throws an error if the cost exceeds the limit". With `--why` the agent finds what bloated the bundle
and removes it.

## Set up

1. Add size-limit to CI.
2. Set it up to comment on the PR. In the project's words, it will "Show error in pull request if the cost exceeds the limit."

## Notes

The source does not say:

- how to set the limit, or which bundle and units to use
- which command the CI job runs, or which tool posts the PR comment
- what the agent should do if the task needs the extra weight, or if `--why` points to no single cause
- whether the agent may raise the limit, or who approves a change to it

## Sources

- [size-limit README](https://github.com/ai/size-limit/blob/main/README.md)
- [ai/size-limit](https://github.com/ai/size-limit)

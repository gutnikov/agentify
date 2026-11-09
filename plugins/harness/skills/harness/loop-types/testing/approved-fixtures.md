---
id: approved-fixtures
title: "Snapshot / golden / approved fixtures"
group: testing
qualities: [correctness, stability]
stages: [local]
speed: [seconds]
---

# Snapshot / golden / approved fixtures

## Loop

A test compares the output with a reference. When the test shows a diff:

- if the diff is unexpected, the agent fixes it
- if the diff is expected, the agent proposes it to a person as the new reference

## Set up

- References live in the repository.
- The agent may not approve new references itself.

## Notes

- Böckeler reports good results with the approved-fixtures pattern where it applies.
- Who approves the references: [human-acceptance-criteria](../human/human-acceptance-criteria.md).

## Sources

- [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html) (Böckeler)

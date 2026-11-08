---
id: code-coverage
title: "Code coverage"
group: testing
qualities: [testability]
speed: [seconds]
---

# Code coverage

## Loop

The agent runs coverage and writes tests for the uncovered branches.

Beck asked the agent to propose tests from the coverage report.

## Set up

- Report in lcov or JSON.
- Threshold on the diff only. The source does not give a threshold value.

## Notes

- Without mutation testing ([mutation-testing](mutation-testing.md)) the signal is weak.

## Sources

- [Augmented Coding: Beyond the Vibes](https://newsletter.kentbeck.com/p/augmented-coding-beyond-the-vibes) (Kent Beck)

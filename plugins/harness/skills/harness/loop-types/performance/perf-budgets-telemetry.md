---
id: perf-budgets-telemetry
title: "Performance budgets through telemetry"
group: performance
agent: [investigator]
qualities: [performance, responsiveness]
stages: [local]
places: [delivery/work, maintenance/work, maintenance/confirmation]
needs: [traces]
---

# Performance budgets through telemetry

## Loop

The agent gets a performance budget, such as "the service starts in under 800 ms" or "no span on a critical path
takes longer than 2 s". It queries the traces and optimizes the code until the service meets the performance budget
(OpenAI's example).

## Set up

- A local telemetry stack: [structured-logs](../observability/structured-logs.md),
  [metrics-promql](../observability/metrics-promql.md), [traces-opentelemetry](../observability/traces-opentelemetry.md).

## Notes

- The source does not say what the agent does if it cannot meet the performance budget. It gives no limit on
  iterations or time, and no point where the agent stops and reports to a human.
- The source does not say how many runs must meet the performance budget before it counts as met, when timings
  change from run to run.

## Agent step

An investigator finds the span or the step that breaks the budget and returns it as a Diagnosis. It never blocks;
the budget does.

## Sources

- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) (OpenAI)

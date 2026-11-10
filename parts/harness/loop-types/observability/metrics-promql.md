---
id: metrics-promql
title: "Metrics (PromQL)"
group: observability
agent: [investigator]
qualities: [observability, availability]
speed: [seconds]
places: [delivery/work, delivery/confirmation, remediation/confirmation, maintenance/confirmation]
needs: [metrics]
---

# Metrics (PromQL)

## Loop

The agent runs a scenario and compares error counters, latency and resource use with what it expects.

## Set up

- A local Prometheus or VictoriaMetrics that the agent reaches through an API or MCP.

## Agent step

An investigator runs the queries and returns which counter or latency differs from what was expected, and why, as a
Diagnosis. It never blocks.

## Sources

- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) (OpenAI)

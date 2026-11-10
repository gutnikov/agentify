---
id: llm-evals
title: "Eval suites for LLM features"
group: meta
agent: [judge]
qualities: [correctness of non-deterministic components]
speed: [minutes]
places: [delivery/work, remediation/work, maintenance/work]
---

# Eval suites for LLM features

## Loop

The agent changes a prompt and runs the evals; a drop in the metric counts as a failure.

## Set up

- Evals in the repository, with thresholds.

## Agent step

When a metric needs judgement (a summary is faithful, a reply is helpful), the grader is a judge calibrated on a
person's grades ([agent-calibration](agent-calibration.md)). A metric a script computes needs no agent.

## Sources

The research cites no source for this loop.

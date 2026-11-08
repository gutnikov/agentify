---
id: coupling-analysis
title: "Coupling analysis"
group: code
qualities: [modularity]
stages: [scheduled]
speed: [minutes]
---

# Coupling analysis

## Loop

The agent calls a CLI that reports fan-in, fan-out and dependency cycles. It then refactors the hot spots using the
numbers from that tool, not its own judgement of the code. The source does not say which values make a module a hot
spot, or when the refactoring is done.

## Set up

- Give the agent a CLI it can call that reports fan-in, fan-out and dependency cycles.
- The source names no tool, thresholds or output format. You have to pick them for your stack.

## Notes

- In Böckeler's experience a report built on a deterministic tool's output deserves more trust; she called the
  model's own conclusions about modularity "lackluster".

## Sources

- [Maintainability sensors for coding agents](https://martinfowler.com/articles/sensors-for-coding-agents.html) (Böckeler)

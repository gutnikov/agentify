---
id: benchmarks-vs-baseline
title: "Benchmarks against a baseline"
group: performance
qualities: [time behaviour]
speed: [minutes]
places: [delivery/work, maintenance/oracle, discovery/work]
---

# Benchmarks against a baseline

## Loop

The agent compares its result with a baseline. If the result is worse than the baseline, the agent optimizes the result.

In Beck's example, the baseline was existing libraries. He asked the agent to compare its B+ tree implementation with
`BTreeMap` in Rust and with `SortedDict` in Python. The source does not say what the comparison showed or what the
agent changed.

## Set up

- Stable benchmarks with a regression threshold.
- A skill with the performance requirements.

## Sources

- [Augmented Coding: Beyond the Vibes](https://newsletter.kentbeck.com/p/augmented-coding-beyond-the-vibes) (Kent Beck)
- [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html) (Böckeler)

---
id: property-based-tests
title: "Property-based tests"
group: testing
qualities: [correctness, robustness]
stages: [local, ci]
places: [delivery/work, remediation/work, maintenance/work]
---

# Property-based tests

## Loop

The agent states invariants and writes property tests for them. The framework finds a minimal counterexample, and the agent fixes the code.

The source covers only this case. It does not say what the agent should do when the invariant itself is wrong, or when to stop the loop if the framework finds no counterexample. Not every failing property means a bug in the code: in the paper under Notes, some of the agent's bug reports were not valid bugs.

## Set up

- Use one of these frameworks: Hypothesis, fast-check or jqwik. The source names no other tools.
- Run the tests locally and in CI.

The source gives no setup steps.

## Notes

- One paper tried this loop at scale: Maaz, DeVoe, Hatfield-Dodds, Carlini, "Agentic Property-Based Testing" (NeurIPS 2025).
- The authors' agent ran property tests over 100 Python packages (933 modules) and produced 984 bug reports.
- The authors judged the reports this way: "56% were valid bugs and 32% were valid bugs that we would report to maintainers".

## Sources

- The research's entry for this loop names one paper, but the research's source list does not include it: [Agentic Property-Based Testing](https://arxiv.org/abs/2510.09907) (arXiv 2510.09907).

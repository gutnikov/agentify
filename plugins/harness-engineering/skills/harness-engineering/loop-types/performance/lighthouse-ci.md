---
id: lighthouse-ci
title: "Lighthouse CI"
group: performance
qualities: [performance, accessibility]
stages: [preview]
speed: [minutes]
---

# Lighthouse CI

## Loop

`lhci assert` fails on assertions such as `'categories:performance': ['error', {minScore: 0.9}]`. The agent reads
the JSON report and `manifest.json`.

## Set up

- `lighthouserc` with assertions, and `budget.json`.

## Sources

- [Performance Budgets with Lighthouse CI: Assertions & budget.json](https://unlighthouse.dev/learn-lighthouse/lighthouse-ci/budgets) (Unlighthouse)
- [Lighthouse CI configuration](https://googlechrome.github.io/lighthouse-ci/docs/configuration.html)
- [lighthouse-ci/docs/configuration.md](https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/configuration.md)

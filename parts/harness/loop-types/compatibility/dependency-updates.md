---
id: dependency-updates
title: "Dependency updates"
group: compatibility
agent: [worker]
qualities: [upgradeability, sustainability]
stages: [scheduled]
places: [maintenance/entry, maintenance/work]
needs: [ci]
---

# Dependency updates

## Loop

Renovate or Dependabot opens a PR; the agent runs the sensors and fixes what broke. A script collects the age and
activity of the dependencies, and an LLM writes recommendations.

## Set up

- Start the agent automatically on the bot's red PRs.

## Agent step

A worker takes the update PR, runs the sensors, fixes what broke and writes the recommendation from the dependency
data. It never merges; the loops on its PR decide.

## Sources

- [Maintainability sensors for coding agents](https://martinfowler.com/articles/sensors-for-coding-agents.html) (Böckeler)

---
id: dependency-updates
title: "Dependency updates"
group: compatibility
qualities: [upgradeability, sustainability]
stages: [scheduled]
---

# Dependency updates

## Loop

Renovate or Dependabot opens a PR; the agent runs the sensors and fixes what broke. A script collects the age and
activity of the dependencies, and an LLM writes recommendations.

## Set up

- Start the agent automatically on the bot's red PRs.

## Sources

- [Maintainability sensors for coding agents](https://martinfowler.com/articles/sensors-for-coding-agents.html) (Böckeler)

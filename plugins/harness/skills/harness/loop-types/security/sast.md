---
id: sast
title: "SAST"
group: security
qualities: [security]
stages: [local, ci]
speed: [seconds]
---

# SAST

## Loop

Semgrep or CodeQL reports a rule, a file and a line; the agent fixes the vulnerable pattern.

## Set up

- Rules from the AppSec team (Böckeler used Semgrep, as her AppSec team prescribed).
- Output in SARIF or JSON.

## Sources

- [Maintainability sensors for coding agents](https://martinfowler.com/articles/sensors-for-coding-agents.html) (Böckeler)

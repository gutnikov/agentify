---
id: security-review-agent
title: "Security and data-handling review by an agent"
group: security
agent: [reviewer]
qualities: [security, privacy]
stages: [scheduled]
speed: [minutes]
places: [remediation/entry]
---

# Security and data-handling review by an agent

## Loop

A subagent checks the code against a security checklist or against rules such as "user names never reach the
frontend", and returns findings with line numbers.

## Set up

- Use the `security-reviewer` subagent from the Claude Code docs. The source does not say where to write your own checklist or rules for it.
- Run the review periodically, not on every commit. Böckeler runs these reviews this way. The source gives no interval.

## Agent step

A reviewer whose lens is the project's security checklist (rules such as "user names never reach the frontend"). It
gets the diff, reads only, and returns Findings with the rule and the line; a finding verifier confirms each one. It
blocks only once calibrated on seeded vulnerabilities that must fire and clean diffs that must pass
([agent-calibration](../meta/agent-calibration.md)).

## Sources

- [Maintainability sensors for coding agents](https://martinfowler.com/articles/sensors-for-coding-agents.html) (Böckeler)
- [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)

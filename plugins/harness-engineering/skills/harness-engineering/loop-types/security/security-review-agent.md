---
id: security-review-agent
title: "Security and data-handling review by an agent"
group: security
qualities: [security, privacy]
stages: [scheduled]
speed: [minutes]
---

# Security and data-handling review by an agent

## Loop

A subagent checks the code against a security checklist or against rules such as "user names never reach the
frontend", and returns findings with line numbers.

## Set up

- Use the `security-reviewer` subagent from the Claude Code docs. The source does not say where to write your own checklist or rules for it.
- Run the review periodically, not on every commit. Böckeler runs these reviews this way. The source gives no interval.

## Sources

- [Maintainability sensors for coding agents](https://martinfowler.com/articles/sensors-for-coding-agents.html) (Böckeler)
- [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)

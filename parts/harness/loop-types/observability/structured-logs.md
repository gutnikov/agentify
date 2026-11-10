---
id: structured-logs
title: "Structured logs and log queries"
group: observability
agent: [investigator]
qualities: [observability, debuggability]
stages: [local]
speed: [seconds]
places: [delivery/work, delivery/confirmation, remediation/oracle, remediation/confirmation, maintenance/confirmation]
needs: [logs]
---

# Structured logs and log queries

## Loop

The agent starts the application, queries the logs (at OpenAI: LogQL against an ephemeral VictoriaLogs per
worktree), finds the error and fixes it.

## Set up

- Structured logging, enforced by a lint ([taste-invariants](../code/taste-invariants.md)).
- A log stack per worktree, deleted after the task.
- A skill with the logging standards (Böckeler).

## Agent step

An investigator runs the log queries and returns a Diagnosis instead of raw lines. It never blocks.

## Sources

- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) (OpenAI)
- [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html) (Böckeler)

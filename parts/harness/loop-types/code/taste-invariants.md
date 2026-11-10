---
id: taste-invariants
title: "Taste invariants: custom lints"
group: code
qualities: [consistency, observability]
stages: [local, ci]
speed: [seconds]
places: [delivery/work, remediation/work, maintenance/work]
---

# Taste invariants: custom lints

## Loop

The agent breaks a team convention, such as an unstructured log line, a schema name or a file size. A custom lint finds the violation, locally or in CI, within seconds. The lint error tells the agent how to fix the violation, and the agent follows that instruction.

## Set up

- Write custom lints that check your team's conventions statically. OpenAI checks these conventions:
  - structured logging
  - naming of schemas and types
  - file size limits
  - reliability requirements
- Make each lint error tell the agent how to fix the violation, not only what is wrong.
- Run the lints locally and in CI.

## Sources

- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) (OpenAI)

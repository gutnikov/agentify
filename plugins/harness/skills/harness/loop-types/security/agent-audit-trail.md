---
id: agent-audit-trail
title: "Audit trail of agent actions"
group: security
qualities: [auditability, accountability]
stages: [task]
places: [delivery/gate, remediation/gate, maintenance/gate]
---

# Audit trail of agent actions

## Loop

The agent leaves evidence: commands with their output, screenshots, videos, commits. The reviewer checks the
evidence instead of re-running everything.

The source does not say what the reviewer does when evidence is missing, is partial or does not match the agent's claim. It also does not say what goes back to the agent in that case.

## Set up

- Tell the agent to follow the rule from the Claude Code docs: "show evidence rather than asserting success". The source does not say where to put this rule.
- Keep a progress file and update it after every session ([progress-file-feature-list](../meta/progress-file-feature-list.md)). The source does not say who writes this file or where to keep it.

## Sources

- [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)

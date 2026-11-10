---
id: agent-code-review
title: "Code review by another agent"
group: meta
agent: [reviewer]
qualities: [maintainability, correctness]
speed: [minutes]
---

# Code review by another agent

## Loop

The coding agent asks one or more reviewer agents, each with a fresh context, for a review. It fixes their comments until the reviewer agents are satisfied. At OpenAI almost all review happens between agents.

The source does not set a limit on review rounds. It also does not say what the coding agent should do if a reviewer agent is never satisfied.

## Set up

The source names two ways to set up this loop:

- a reviewer agent that runs as a subagent
- `/simplify`, a command in Claude Code (source: Claude Code power user tips)

The source does not say:

- what the reviewer agent checks
- how its comments reach the coding agent
- what `/simplify` does
- whether you use the two together or pick one

## Notes

- Böckeler: an LLM partly catches semantic duplication and over-engineering, but expensively and
  probabilistically.

## Agent step

A reviewer per lens (correctness, security, tests, performance, the project's conventions), each in a fresh context.
It gets the diff and the requirement, not the coding agent's reasoning, reads only, and returns Findings; a finding
verifier checks each high finding before the coding agent acts on it. A reviewer blocks only once calibrated
([agent-calibration](agent-calibration.md)); until then its findings are advice.

## Sources

- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) (OpenAI)
- [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html) (Böckeler)
- [Claude Code power user tips](https://support.claude.com/en/articles/14554000-claude-code-power-user-tips)

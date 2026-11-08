---
id: user-feedback
title: "User feedback"
group: production
qualities: [functional suitability, satisfaction]
speed: [days]
---

# User feedback

## Loop

1. A person turns user feedback into acceptance criteria.
2. The agent gets these criteria and uses them as both the spec for its work and the test of that work.

The source does not say which person writes the criteria, where they are written down, or who turns them into a test that can run.

## Set up

The source names two tools for this loop, both from the Claude Code best practices (see Sources):

- `gh issue view`, a GitHub CLI command
- a `/fix-issue` skill for the agent

The source does not say what the skill does, what input it takes or where to get it.

## Notes

- No sensor can check correctness if a person has not specified what they want.
- The human side of this loop: [production-users](../human/production-users.md).

## Sources

- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) (OpenAI)
- [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html) (Böckeler)
- [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)

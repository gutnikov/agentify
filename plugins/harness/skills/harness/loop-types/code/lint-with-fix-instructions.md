---
id: lint-with-fix-instructions
title: "Linter with fix instructions"
group: code
qualities: [maintainability]
stages: [commit, ci]
speed: [seconds]
---

# Linter with fix instructions

## Loop

The agent runs the linter and reads each violation together with a "how to fix" text. Then it either fixes the
violation or suppresses it with a justification.

## Set up

To set up the loop:

- Make each lint message tell the agent how to fix the violation. The source calls these custom messages
  a positive prompt injection. It names two ways to add them:
  - Böckeler wrote an ESLint formatter of her own.
  - OpenAI writes the messages of its custom lints so that they put fix instructions into the agent's context.
- Turn on `max-params`, `max-lines`, `max-lines-per-function` and `complexity`: ESLint's default preset does not
  include them.
- Run the linter at three points: from a hook, at pre-push and in CI. The source does not say which hook. Each run
  takes seconds.

## Notes

- Where a rule had no fix instruction, Böckeler saw the agent raise the complexity threshold instead of fixing
  the code.

## Sources

- [Maintainability sensors for coding agents](https://martinfowler.com/articles/sensors-for-coding-agents.html) (Böckeler)
- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) (OpenAI)

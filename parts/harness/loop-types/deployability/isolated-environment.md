---
id: isolated-environment
title: "Isolated reproducible environment"
group: deployability
qualities: [reproducibility, safety (limits the blast radius)]
stages: [task]
places: [delivery/work, remediation/work, maintenance/work, discovery/work]
---

# Isolated reproducible environment

## Loop

At the start of every task, the agent gets a clean environment: a devbox, a devcontainer, or a worktree with its own instance of the app.
The aim is that the sensors give the same result for the same code.

The source does not say:

- what a fresh environment per task costs
- which causes of changing results such an environment does not remove
- for which projects this loop is not worth it

## Set up

The source gives no setup steps. It gives three examples of how teams give each task its own environment:

- Stripe gives each agent a devbox. Devboxes are "cattle, not pets" and hold no production data. Stripe warms them up in advance, so a devbox is ready in 10 seconds.
- OpenAI gives each worktree its own running app and its own ephemeral telemetry stack.
- Anthropic gives the agent an `init.sh` script. The source does not say what the script does.

## Notes

- The source says that a sandbox lets the agent run without confirming each action. It does not say which of the three forms (devbox, devcontainer or worktree) counts as a sandbox. Before you let the agent run without confirmations, check that your environment is one.

## Sources

- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) (OpenAI)
- [Minions: Stripe's one-shot, end-to-end coding agents — Part 2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2)
- [Effective harnesses for long-running agents](https://anthropic.com/engineering/effective-harnesses-for-long-running-agents) (Anthropic)
- [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)

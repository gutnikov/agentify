---
id: visual-screenshot-check
title: "Visual check with screenshots"
group: testing
qualities: [interaction capability (user engagement)]
stages: [local, ci]
---

# Visual check with screenshots

## Loop

The agent takes a screenshot, compares it with the mockup, lists the differences and fixes them.

## Set up

Set it up in two places:

- Locally: give the agent the prompt from the Claude Code docs: "take a screenshot of the result and compare it to the original".
- In CI: run pixel regression.

Locally, the [`app-probing`](https://github.com/gutnikov/my-claude-plugins/tree/main/plugins/app-probing/skills/app-probing) skill (plugin `app-probing@private-plugins`) takes a full-page screenshot once the screen has settled; the
comparison with the mockup stays with the agent.

## Sources

- [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)

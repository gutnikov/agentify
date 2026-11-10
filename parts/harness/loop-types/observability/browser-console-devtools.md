---
id: browser-console-devtools
title: "Browser console and DevTools"
group: observability
agent: [investigator]
qualities: [debuggability]
speed: [seconds]
places: [delivery/work, remediation/oracle, remediation/work]
needs: [browser]
---

# Browser console and DevTools

## Loop

The agent reads the page's console errors and network requests and fixes JS exceptions and 4xx/5xx responses.

## Set up

The source names 3 tools for this loop:

- Chrome DevTools MCP
- Playwright MCP
- Claude in Chrome

The source does not say whether to use one of these tools or combine them. It does not give setup steps for any of them.

OpenAI built this loop into its own harness. It connected its agent to CDP and gave the agent skills for working with DOM snapshots. The source does not describe these skills.

In a project with Playwright fixtures and Page Objects, the [`app-probing`](../../../app-probing/README.md) part of agentify collects console
errors and the app's failed requests in every probe, without third-party noise.

## Agent step

An investigator groups the console errors and failed requests by cause and returns a Diagnosis for each. It never
blocks.

## Sources

- [Playwright MCP Guide: Let Claude, Codex, and Cursor Control the Browser](https://eastondev.com/blog/en/posts/ai/20260904-playwright-mcp-browser-automation-claude-codex-cursor/)
- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) (OpenAI)
- [claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice)

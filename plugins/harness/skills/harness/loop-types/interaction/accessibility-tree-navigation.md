---
id: accessibility-tree-navigation
title: "Agent navigation by the accessibility tree"
group: interaction
qualities: [operability, self-descriptiveness]
speed: [seconds]
---

# Agent navigation by the accessibility tree

## Loop

Playwright MCP gives the agent an accessibility snapshot of the page instead of pixels. If the agent cannot find
a button by its role and name, the source reads that one miss as two signals at once: the page has poor accessibility,
and the scenario does not work.

## Set up

- Playwright MCP or playwright-cli.

## Notes

- `browser_run_code_unsafe` in Playwright MCP is effectively remote code execution.

## Sources

- [Playwright MCP](https://playwright.dev/mcp/introduction)
- [Playwright MCP: Browser Automation for AI Agents (2026)](https://mcp.directory/blog/playwright-browser-mcp-guide-2026)
- [Accessible web testing with Playwright and Axe Core](https://dev.to/vitalyskadorva/accessible-web-testing-with-playwright-and-axe-core-2kg1)
- [Playwright MCP Guide: Let Claude, Codex, and Cursor Control the Browser](https://eastondev.com/blog/en/posts/ai/20260904-playwright-mcp-browser-automation-claude-codex-cursor/)

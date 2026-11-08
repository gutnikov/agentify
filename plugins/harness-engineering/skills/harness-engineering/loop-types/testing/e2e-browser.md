---
id: e2e-browser
title: "E2E through browser automation"
group: testing
qualities: [functional suitability, operability]
stages: [local, ci]
---

# E2E through browser automation

## Loop

The agent starts the dev server and walks a scenario with Playwright or Puppeteer. That is how it finds out that
a feature does not work end to end even though the unit tests and `curl` pass.

## Set up

- An `init.sh` that starts the server and runs a basic e2e.

## Notes

- Anthropic observed that without an explicit prompt Claude "would fail to recognize that the feature didn't work
  end-to-end".
- Through Puppeteer MCP the agent does not see native alert modals.

## Sources

- [Effective harnesses for long-running agents](https://anthropic.com/engineering/effective-harnesses-for-long-running-agents) (Anthropic)

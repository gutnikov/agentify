---
id: e2e-browser
title: "E2E through browser automation"
group: testing
agent: [explorer]
qualities: [functional suitability, operability]
stages: [local, ci]
places: [delivery/work, remediation/work, maintenance/work]
needs: [browser]
---

# E2E through browser automation

## Loop

The agent starts the dev server and walks a scenario with Playwright or Puppeteer. That is how it finds out that
a feature does not work end to end even though the unit tests and `curl` pass.

## Set up

- An `init.sh` that starts the server and runs a basic e2e.
- For a web app with Playwright fixtures and Page Objects, the [`app-probing`](../../../app-probing/README.md) part of agentify walks the
  scenario through them before a spec exists.

## Notes

- Anthropic observed that without an explicit prompt Claude "would fail to recognize that the feature didn't work
  end-to-end".
- Through Puppeteer MCP the agent does not see native alert modals.

## Agent step

An explorer walks the scenario through the project's fixtures and Page Objects (`app-probing`) and returns what it
saw: the URL, the screen, console errors, failed requests. It does not block: what has to keep holding becomes a
spec that blocks.

## Sources

- [Effective harnesses for long-running agents](https://anthropic.com/engineering/effective-harnesses-for-long-running-agents) (Anthropic)

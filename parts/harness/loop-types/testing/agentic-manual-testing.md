---
id: agentic-manual-testing
title: "Agentic manual testing"
group: testing
agent: [explorer]
qualities: [correctness, demonstrability]
stages: [local]
places: [delivery/work, remediation/oracle, remediation/work, maintenance/work, discovery/work]
---

# Agentic manual testing

## Loop

The agent checks the code by hand: `python -c`, temporary files in `/tmp`, `curl`, a browser. When the agent finds a
defect, it locks the fix in with a permanent test, written red/green ([red-green-tdd](red-green-tdd.md)).

## Set up

Give the agent:

- tools with a detailed `--help`, such as Rodney and agent-browser
- Showboat, which records the real output of the commands the agent runs
- for a web app, the [`app-probing`](../../../app-probing/README.md) part of agentify: it runs the browser check as a throwaway Playwright script built on a test fixture and
  Page Objects

## Notes

- Because Showboat records what the commands really output, it is harder for the agent to describe what it hoped would happen
  instead of what happened.

## Agent step

An explorer, separate from the agent that wrote the change, checks it by hand and returns defects as Findings with
the steps to reproduce them. It does not block; a defect it finds becomes a failing test.

## Sources

- [Agentic manual testing — Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/agentic-manual-testing/) (Simon Willison)

---
id: accessibility-checks
title: "Accessibility checks (axe, ARIA)"
group: interaction
agent: [explorer]
qualities: [inclusivity, user assistance]
speed: [seconds]
---

# Accessibility checks (axe, ARIA)

## Loop

`@axe-core/playwright` finds WCAG violations and gives the selector for each one. `toMatchAriaSnapshot` catches
structural problems that axe misses. The source does not say which structural problems these are.

## Scope

This loop runs inside e2e tests. The axe package in this loop is built for Playwright, so the loop fits a project that has Playwright e2e tests.

## Set up

The source gives 2 steps. It does not say whether you need both or whether one is enough.

1. Run axe inside your e2e tests.
2. Set a threshold on the Lighthouse accessibility score ([lighthouse-ci](../performance/lighthouse-ci.md)).

The source does not say which pages to scan, which violations should fail the run, or what threshold to set. It gives no setup step for `toMatchAriaSnapshot`.

## Agent step

axe needs no agent. An explorer covers what axe cannot see: keyboard paths, focus order, what a screen reader
announces. It returns Findings and does not block; a problem it finds becomes a test.

## Sources

- [Accessible web testing with Playwright and Axe Core](https://dev.to/vitalyskadorva/accessible-web-testing-with-playwright-and-axe-core-2kg1)
- [What's New in Playwright 2026: AI Agents, MCP, and Accessibility-First Testing](https://qaskills.sh/blog/whats-new-playwright-2026)

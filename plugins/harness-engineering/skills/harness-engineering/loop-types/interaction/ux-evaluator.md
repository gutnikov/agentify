---
id: ux-evaluator
title: "UX evaluator with thresholds"
group: interaction
qualities: [user engagement, functional completeness]
stages: [sprint]
---

# UX evaluator with thresholds

## Loop

A separate agent walks through the app with Playwright MCP the way a user would, and grades it on criteria: depth,
functionality, design, code. If any criterion is below its threshold, the sprint fails, and the generator gets a
detailed breakdown ("FAIL — `PUT /frames/reorder` route defined after `/{frame_id}`…").

## Set up

- Before the sprint starts, set up a "sprint contract".

## Notes

- Use the UX evaluator only where the model alone cannot do the job reliably.
- Anthropic warns: "out of the box, Claude is a poor QA agent".
- Anthropic reports one solo run at 20 minutes and $9, and one full-harness run at 6 hours and $200. The source does not say what the full harness adds besides the evaluator, so the difference is not the cost of this loop alone.

## Sources

- [Harness design for long-running apps](https://anthropic.com/engineering/harness-design-long-running-apps) (Anthropic)

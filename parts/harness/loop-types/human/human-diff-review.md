---
id: human-diff-review
title: "Diff review by a person"
group: human
when: [after]
assesses: [code, intent]
stages: [ci]
speed: [hours, days]
places: [delivery/gate, remediation/gate, maintenance/gate]
needs: [ci]
---

# Diff review by a person

## Loop

The person comments on the PR; the agent fixes the comments and replies in the thread.

## Getting a good signal

- Have the person read the diff, not the description. The side under review writes the description; the diff is
  the primary source. Leave the person what only they can judge: is this the right change, and does the approach
  fit the codebase (AI Hero).
- Run an automated AI review first to remove the obvious, then have a person look (Kilo).
- Keep diffs small. A large diff all but guarantees a rubber-stamp review (the source note cites no source for this).

## When and how long

CI and the PR; hours to days of waiting.

## Related

- [agent-code-review](../meta/agent-code-review.md): the AI review that goes first.

## Sources

- Matt Pocock, *Human review* (AI Hero)
- Kilo, *Human-in-the-loop AI coding* (vendor material)

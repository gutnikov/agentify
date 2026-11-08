---
id: interview
title: "Interview"
group: human
when: [before]
initiator: agent
sync: blocking
assesses: [intent]
stages: [task]
speed: [minutes]
---

# Interview

## Loop

Before writing code the agent asks the person about requirements, edge cases and trade-offs, and writes the
answers into a spec in the repository.

## Getting a good signal

- Claude Code's best practices: have the agent interview the person in detail with the AskUserQuestion tool —
  about the implementation, UI/UX, edge cases and trade-offs — skipping the obvious questions and digging into
  the hard parts.
- Give the person answer options instead of open questions. The source note says such questions get answered
  faster and with less spread than open ones. It gives no data or source for this: its author lists choosing
  from options as common practice with no primary source of its own.

## When and how long

At the start of a task; 5–20 minutes of the person's time.

## Related

- [plan-approval](plan-approval.md): a plan when the person roughly knows what they want, an interview when the
  goal is vague.

## Sources

- [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)

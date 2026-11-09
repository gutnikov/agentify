---
id: plan-approval
title: "Plan approval"
group: human
when: [before]
initiator: agent
sync: blocking
assesses: [plan]
stages: [task]
speed: [minutes]
---

# Plan approval

## Loop

The agent studies the code in read-only mode and proposes a plan. The person edits and approves it, and from then
on the agent works by the plan autonomously.

## Getting a good signal

- In Claude Code the plan can be opened in the editor and edited directly, and the approved plan can be saved in
  the repository so that it outlives the session (Rick Hightower).
- Plan or interview: a plan when you roughly know what you want; an [interview](interview.md) when the goal is
  vague (Towards AI).

## When and how long

At the start of a task; minutes.

## Sources

- [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices) (plan mode)
- Rick Hightower, *Claude Code day by day*
- Towards AI, *spec-driven development*

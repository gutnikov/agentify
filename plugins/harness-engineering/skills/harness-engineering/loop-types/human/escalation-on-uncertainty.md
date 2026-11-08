---
id: escalation-on-uncertainty
title: "Escalation on uncertainty"
group: human
when: [during]
initiator: agent
sync: blocking
assesses: [intent]
speed: [minutes, hours]
---

# Escalation on uncertainty

## Loop

The agent stops by itself and asks a question when it cannot choose between options or has found a contradiction
in the requirements.

## Getting a good signal

- List explicitly in CLAUDE.md what to always ask about (the database schema, the public API, deleting data, new
  dependencies) and what never to ask about (style, names of internal variables).

## Notes

- Anthropic, "Measuring AI agent autonomy in practice" (18 February 2026): the harder the task, the more often
  Claude Code asks for clarification and the more often people interrupt it. On the hardest tasks Claude Code asks
  for clarification more than twice as often as a person interrupts it.

## When and how long

During the task; a blocking question waits minutes to hours.

## Related

- [async-questions-with-assumptions](async-questions-with-assumptions.md) for questions that need not block.

## Sources

- Anthropic, *Measuring AI agent autonomy in practice* (18 February 2026)

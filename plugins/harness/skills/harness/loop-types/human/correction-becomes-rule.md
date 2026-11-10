---
id: correction-becomes-rule
title: "Steering: every correction becomes a rule"
group: human
initiator: human
stages: [continuous]
speed: [minutes]
places: [harness:remediation/entry, harness:remediation/oracle]
---

# Steering: every correction becomes a rule

## Loop

The loop starts only on a repeat. A single correction does not start it. When the person has corrected the agent twice for the same thing, the correction becomes an automated sensor (a
lint, a test, a fitness function) or a line in CLAUDE.md.

## Getting a good signal

- Keep a log of escalations and corrections by type: recurring types show where the agent lacks constraints,
  tools or context (AlignX).
- Code (a lint, a test) is more reliable than text: CLAUDE.md is advice, not a guarantee.

## When and how long

Continuously; minutes per correction.

## Related

- [steering-loop](../meta/steering-loop.md): the same loop for the agent's own repeated mistakes.

## Sources

- AlignX, *Designing Human-in-the-Loop for Agentic Workflows*

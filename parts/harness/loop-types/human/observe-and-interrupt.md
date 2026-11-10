---
id: observe-and-interrupt
title: "Observe and interrupt"
group: human
when: [during]
initiator: human
sync: async
speed: [sub-second]
places: [delivery/work, remediation/work, maintenance/work]
---

# Observe and interrupt

## Loop

The person does not approve every step. They watch from the side and step in when they see the work going the
wrong way.

The source recommends this mode for ambiguous and irreversible tasks: a schema migration, a hard design decision,
anything that touches production (AI Hero).

The source covers only the case where the person is watching and spots the drift in time. It does not say:

- what happens if the person is not watching
- how the person interrupts the agent
- what the agent does once it is stopped
- how the person sees an irreversible step before it runs, not after

If you plan to use this loop for irreversible work, you need to settle these points yourself. This card cannot
answer them.

## Getting a good signal

- The agent shows its progress (what it did, what is next) briefly and often, so that a drift is visible at a
  glance. The source does not say how often the agent should report or how short a report should be.

## Notes

- New Claude Code users turn on full auto-approval in about 20% of sessions, and experienced users in more than 40%.
  But experienced users interrupt the agent more often (Anthropic).
- The same study looked at Anthropic's own use from August to December 2025. Over that time, the success rate on
  the hardest tasks doubled. The average number of human interventions per session fell from 5.4 to 3.3. The
  source does not say whether one caused the other, or what these figures mean for choosing this loop.

## When and how long

During the task; immediate when the person steps in.

## Sources

- Anthropic, *Measuring AI agent autonomy in practice* (18 February 2026)
- Matt Pocock, *Human-in-the-loop* (AI Hero)

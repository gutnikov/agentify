---
id: risky-action-gates
title: "Gates on risky actions"
group: human
when: [during]
initiator: rule
sync: blocking
assesses: [action-risk]
speed: [seconds, minutes]
---

# Gates on risky actions

## Loop

Before an irreversible action, the agent asks for confirmation. The source lists these irreversible actions:

- a deploy
- a migration
- deleting data
- an external payment or email

In this card, a risky action means an irreversible one.

## Getting a good signal

- Gate only irreversible actions. Send every reversible action to a sandbox, where it needs no confirmation.
  Then each request is rare enough to get attention again.

## Notes

- The risk is confirmation fatigue. Anthropic's data, as retold by Resilient Cyber: users approve 93% of
  permission requests in Claude Code, and many of those approvals are no longer a meaningful check.
- Only about 0.8% of agent actions look irreversible (Latent Space).
- The source does not say who confirms, what the agent does if a confirmation is refused, or what happens if
  nobody answers. The gate blocks the agent, so check how your setup handles these cases before you use it with
  an agent that runs unattended.

## When and how long

During the task; seconds to minutes. The source gives no time for the case where nobody is there to answer.

## Related

- [isolated-environment](../delivery/isolated-environment.md): the sandbox where reversible actions need no
  confirmation.

## Sources

- Resilient Cyber, *The human in the loop illusion* (secondary retelling of Anthropic's data)
- Latent Space, *Anthropic's Agent Autonomy study* (secondary retelling)

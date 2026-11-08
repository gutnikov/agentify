---
id: result-demo
title: "Result demo"
group: human
when: [after]
initiator: agent
assesses: [result]
stages: [task]
speed: [minutes]
---

# Result demo

## Loop

The agent shows the working feature: a link to a preview environment, screenshots, a before/after video, recorded
command output. The person judges the behaviour, not the code.

## Getting a good signal

Ask for evidence, not claims: real command output and recordings, not a description of what "should work".

## When and how long

At the end of a task; 1–5 minutes of the person's time.

## Notes

- The note says a demo is faster than reading the diff and gives a signal about intent that tests do not. It gives no time for reading a diff and does not say which tasks this holds for.
- The note does not say:
  - how the person's verdict and comments get back to the agent
  - whether the agent fixes the work and demos it again
  - what to do when a task has nothing visible to demo, such as a refactor or a library change
  - what to do when the preview environment fails to come up

## Related

- [agent-audit-trail](../security/agent-audit-trail.md): the evidence the agent leaves.
- [preview-environments](../delivery/preview-environments.md): where the demo runs.

## Sources

The note cites no source for this loop.

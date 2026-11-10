---
id: async-questions-with-assumptions
title: "Asynchronous questions with assumptions"
group: human
when: [during, after]
initiator: agent
sync: async
stages: [task]
speed: [minutes]
places: [delivery/work, remediation/work, maintenance/work, discovery/work]
---

# Asynchronous questions with assumptions

## Loop

The agent does not ask a non-blocking question right away. It writes the question down together with the
assumption it made, and keeps working. At the end of the task, the person gets all these questions as one batch and confirms or cancels
each assumption.

## Getting a good signal

- Every assumption must be cheap to undo: a separate commit, a feature flag.
- In the batch, the agent includes a list headed "assumptions worth checking".

## When and how long

The agent records questions during the task, and the person answers them at its end. The person spends minutes on the whole batch.

## Sources

The note cites no source for this loop. It says this loop sums up accepted practice and has no primary source of its own.

---
id: human-acceptance-criteria
title: "Acceptance criteria and references from a person"
group: human
agent: [reviewer]
when: [before]
initiator: human
assesses: [result]
stages: [task]
speed: [seconds]
---

# Acceptance criteria and references from a person

## Loop

The person writes or approves acceptance tests, "input → expected output" examples and reference snapshots. From
then on the agent works against them without the person.

## Getting a good signal

- The agent may not change approved references itself; it only proposes a new value. The source does not say
  whether this rule covers all three kinds (acceptance tests, examples and snapshots) or only some of them.
- The note calls locked references the strongest way to make a slow human signal reusable: the person gives their verdict once, and the check runs on
  every run.

## When and how long

At the start of a task; after that, seconds per run.

## Agent step

A guard over the approved references: it returns a Verdict on whether a change touches an approved acceptance test,
example or snapshot, and lists each such change for the person. It never approves a change itself, and blocks only
once calibrated ([agent-calibration](../meta/agent-calibration.md)).

## Related

- [approved-fixtures](../testing/approved-fixtures.md): the automated side of the same references.
- [acceptance-loop](../meta/acceptance-loop.md): where the approved criteria become the oracle of the whole task.

## Sources

The note cites no source for this loop.

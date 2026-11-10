---
id: task-restatement
title: "Task restatement"
group: human
when: [before]
initiator: agent
sync: blocking
assesses: [intent]
stages: [task]
speed: [seconds]
places: [delivery/oracle, discovery/oracle]
---

# Task restatement

## Loop

The agent restates the task in its own words. It covers three things: how it understood the task, what is out of scope, and what criterion will tell it the task is done. A human then answers "yes" or corrects the restatement. The source does not say which human this is, for example the task author or a reviewer.

The source also does not say what the agent does after a correction, such as restating again or going ahead.

## Getting a good signal

- Require an explicit "not doing" list and a measurable done criterion. Mismatches show up in these two places.

Example (made up to show the format, not taken from the source):

> Task: add CSV export to the reports page.
> I understood: add an "Export CSV" button that downloads the rows shown in the current table.
> Not doing: PDF or Excel export, changes to the table layout.
> Done when: the button downloads a CSV file with the same rows and columns as the table, and a new test checks this.

In this example, a human who needed Excel export too would spot the mismatch in the "not doing" list and correct it before the agent starts.

## When and how long

At the start of a task. It takes under a minute.

The source does not say how long a blocking agent waits when nobody answers, or which tasks are too small to be worth the stop.

## Sources

The note cites no source for this loop. It lists task restatement as a generalization of common practice.

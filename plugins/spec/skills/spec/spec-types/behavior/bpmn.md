---
id: bpmn
title: "BPMN processes"
group: behavior
role: layer
fits: [api, data]
risks: [timers, integrations]
tests: [api]
checks: official
cost: high
---

# BPMN processes

## What it describes

A long-running process as a graph: tasks, gateways with conditions, timers, waits for messages, retries, and who
does each step.

## When it fits

Only when the product runs a process engine (Camunda, Zeebe), or a process spans days with timers, retries and
people in the loop. Otherwise put the same timers in the spine as slices triggered by `clock` and examples with
`after`.

## How it is checked

`bpmnlint` checks the graph: disconnected tasks, gateways without conditions, missing end events, dangling
references. Running the process in an engine catches what the linter cannot, such as charging money on the
failure branch. A hand-written file without the `incoming`/`outgoing` elements an editor writes gives hundreds of
false errors.

## What the tests get

The questions about time, which become examples in the spine: what happens when an outside system does not answer
in time, when a checkout is abandoned, how many payment retries the grace period has.

## Set up

Generate the diagram layout (`bpmn-auto-layout`), lint with `bpmnlint` recommended rules, and run critical paths
in an engine (`bpmn-engine`) if there is none in the product.

## Evidence

Vendy: 5 processes, 45 tasks. Official tools caught 6 of 8 seeded defects, own scripts 8 of 8. The diagram
interchange data grew the XML about 4.5 times. New questions about time no other format raised.

## Sources

- [bpmnlint](https://github.com/bpmn-io/bpmnlint)

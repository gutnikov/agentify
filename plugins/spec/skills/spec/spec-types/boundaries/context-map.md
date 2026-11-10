---
id: context-map
title: "Context map"
group: boundaries
role: layer
fits: [web, api]
risks: [multi-team, integrations]
tests: [contract]
checks: own
cost: low
---

# Context map

## What it describes

Which parts of the system own which data and decisions (bounded contexts), and how they depend on each other:
upstream and downstream, anti-corruption layers, shared kernels, partnerships.

## When it fits

Several teams or services, or integrations with outside systems that need a translation layer. Keep only the map
(about 40 lines of CML), with each stream of the event model tagged with its context. Do not copy aggregates and
events into CML: they duplicate the spine and drift.

## How it is checked

The Context Mapper CLI checks syntax only: it passed 7 of 7 seeded semantic defects (an unknown event, a state
outside the lifecycle, a reference to a missing type). Generators draw from a broken model without a word. An own
check finds cycles between contexts and references that do not resolve.

## What the tests get

Contract tests at the boundaries between contexts, not e2e tests. A two-way dependency on the map often marks a
missing rule in the spine (Vendy: generation and billing depend on each other because credits are not reserved).

## Set up

Context Mapper CLI and Java for diagrams; an own check for cycles and unresolved names.

## Evidence

Vendy: 11 contexts. Found a dependency cycle through the product's "advertised" status, and the generation-billing
partnership that the other formats showed as overdraft.

## Sources

- [Context Mapper](https://contextmapper.org/docs/)

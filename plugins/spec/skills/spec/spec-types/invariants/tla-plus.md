---
id: tla-plus
title: "TLA+"
group: invariants
role: layer
fits: [web, api, data]
risks: [money, concurrency]
tests: [api]
checks: official
cost: high
---

# TLA+

## What it describes

A small formal model of one critical part, such as credits and subscriptions, with the properties that must
always hold: the balance goes negative only after a refund, credits are charged only for successful work.

## When it fits

Money, quotas or other counters that several operations change at once, and policies whose rules interact
(reset, refunds, top-ups). Not for the rest of the product.

## How it is checked

TLC explores every reachable state within small bounds and prints the shortest trace that breaks a property. It
finds only what a property states: a property nobody wrote is a defect nobody finds, and a wrong property looks
like a finding until the trace is read.

## What the tests get

Each counterexample trace becomes an example in the spine, usually an API-level one (two requests at once), and
each fix of the policy becomes a rule or a question in the spine. The traces are the regression tests.

## Set up

`tla2tools.jar` and Java; unknown rules as constants, so one run covers each variant of the policy.

## Evidence

Vendy: 239 lines, 90 runs in 149 s. Found overdraft without a refund (two requests both pass the balance check),
that the period reset erases a debt the policy says must be paid, that "top-ups never expire" fails once a
subscription ends, and that the obvious fix (holding credits) adds two new defects. No variant of the policy
passed all 10 properties.

## Sources

- [TLA+](https://lamport.azurewebsites.net/tla/tla.html)
- [TLA+ tools](https://github.com/tlaplus/tlaplus)

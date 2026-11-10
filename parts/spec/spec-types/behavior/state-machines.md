---
id: state-machines
title: "State machines"
group: behavior
role: layer
fits: [web, api, mobile]
risks: [money, timers]
tests: [e2e, api]
checks: own
cost: low
---

# State machines

## What it describes

The lifecycle of one key entity, such as a subscription, an order or a payment: its states and every transition
between them, with the command or event that causes it.

## When it fits

An entity whose status decides what a person may do: a subscription that can be active, past due, cancelled at
period end or ended. Write the states as a `status` field of a read model and each transition as a slice; add a
separate statechart (XState, SCXML) only when the app runs one.

## How it is checked

A diagram of the states shows what a list of slices hides: a state with no way out, a state no transition reaches,
a button in the app with no transition behind it. Check reachability and dead ends with an own script or the
statechart tool.

## What the tests get

One obligation per transition, and one per command refused in a state (cancel an ended subscription). Each is an
example in the spine: the state before as the named state, the transition as the action, the status after in `see`.

## Set up

List the statuses as the values of the `status` field; for each pair (state, command) decide: a transition, an
error, or impossible on the screen.

## Evidence

Vendy: the subscription's state diagram had no way from ENDED back to ACTIVE, though the app shows a "Resubscribe"
button; no way to undo a cancellation; CHECKOUT_FAILED was a dead end.

## Sources

- [XState](https://stately.ai/docs/xstate)

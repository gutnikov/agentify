---
id: triage
title: "Triage: every signal goes to one super-loop, with its oracle"
group: meta
agent: [judge]
qualities: [functional suitability, traceability]
stages: [continuous]
speed: [minutes]
places: [delivery/entry, remediation/entry, maintenance/entry, discovery/entry]
---

# Triage: every signal goes to one super-loop, with its oracle

## Loop

A signal arrives: an error from the tracker, an alert, a pull request from a dependency bot, a message from a user, a
ticket. Before any work, triage merges it with what is already open on the same thing, and routes it to one
super-loop. The route decides the oracle, so a wrong route means the wrong check at the gate.

| The signal says | Super-loop | The oracle to build |
|---|---|---|
| It is not known yet whether to do it, or how | discovery | The question and its evidence |
| The product does not do what it was specified to do, or what it did before | remediation | A reproduction that fails |
| The product should do something new or different | delivery | A spec a person approves |
| The behaviour stays; a dependency, the structure, the speed or the size changes | maintenance | The behaviour as it is |

## Set up

- **One record per signal**: where it came from, what it says, the super-loop chosen, the reason, and the open item it
  was merged into, if any.
- **Duplicates first.** The same error fingerprint, the same dependency, the same requirement: the signal joins the
  open item instead of opening a new one.
- **An ambiguous signal goes to a person** under H1, with the options and a recommended route. A complaint about a
  slow page can be remediation (a regression) or maintenance (it was always slow): the history decides, and where it
  does not, a person does.
- **Routes are checked later.** A maintenance item sent back by its gate with a changed expected value, or a
  remediation item whose reproduction turned out to be a new requirement, was routed wrong; both show in the trace.
- **Cases.** Must fire: a change of behaviour offered as maintenance; a duplicate of an open item. Must pass: a
  dependency bump with no change of behaviour, routed to maintenance.

## Notes

- The costly mistake is a change of behaviour routed to maintenance, which runs without a person approving behaviour.
  The gate of maintenance, [behaviour-invariance](behaviour-invariance.md), is the second line of defence.
- The super-loops and their oracles: [super-loops](../../super-loops/README.md).

## Agent step

A judge routes the signals that rules cannot. It gets the signal and the open items, and returns a Verdict with the
super-loop, the reason, and the duplicate if there is one. It is calibrated on signals a person routed (H5), and it
routes on its own only once calibrated; until then it proposes, and a person decides.

## Sources

- ITIL: incident, problem and change management, where the route of a ticket decides the process it goes through.

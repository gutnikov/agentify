---
id: discovery-decision
title: "Discovery decision: an answer whose every claim has its evidence"
group: meta
agent: [refuter]
qualities: [functional suitability, traceability]
stages: [task]
speed: [hours, days]
places: [discovery/oracle, discovery/gate, discovery/confirmation]
---

# Discovery decision: an answer whose every claim has its evidence

## Loop

Before the work, the question and the evidence that would answer it are written down and agreed. The agent builds
prototypes, probes and spikes, and writes the answer. The gate checks that every claim in the answer names its
evidence, that the evidence says what the claim says, and that none of the work's code reached the main branch. The
person who asked decides: build it, drop it, or ask again.

## Set up

- **A decision record** per question, in the repository: the question, the evidence that would answer it, the answer
  with each claim and its evidence (a link, a screenshot, a measurement, a quote), and the decision with its date and
  who made it.
- **Throwaway work stays out.** Prototypes live where the product does not build them (the `ui-prototypes` part
  keeps them in `prototypes/`); spikes live on a branch that is never merged.
- **The gate is the `run`.** One line per claim, `<claim>: <status>`: `no evidence`, `evidence missing`, `ok`; and
  `spike code in main` if there is any. The exit is non-zero while any claim is not `ok`.
- **Cases.** Must fire: a claim with no evidence; evidence that does not exist; spike code merged. Must pass: an
  answer where every claim links its evidence.

## Notes

- "Do not build it" is a good result: the record keeps the evidence, so nobody has to ask the question again.
- A decision to build becomes the input of delivery: the question, the answer and the evidence go into the spec.

## Agent step

A refuter gets the answer and its evidence, never the agent's reasoning, and tries to prove each claim wrong: it
opens the evidence, reruns a measurement, checks a quote. It returns a Verdict per claim, and it blocks only once
calibrated ([agent-calibration](agent-calibration.md)).

## Sources

- Marty Cagan, *Inspired* (2nd edition, Wiley, 2017): product discovery before delivery.
- Michael Nygard, *Documenting Architecture Decisions* (2011): a decision record kept with the code.

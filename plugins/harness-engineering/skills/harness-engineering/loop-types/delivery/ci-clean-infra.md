---
id: ci-clean-infra
title: "CI on clean infrastructure"
group: delivery
qualities: [reproducibility, deployability]
stages: [ci]
speed: [minutes]
---

# CI on clean infrastructure

## Loop

The agent pushes; autofixes apply themselves; the agent fixes the remaining failures locally.

## Set up

- Machine-readable logs (`gh run view --log-failed`).
- A limit on CI rounds. Stripe runs lint locally first, then gives the agent at most two CI rounds; beyond two, the returns drop.

## Sources

- [Minions: Stripe's one-shot, end-to-end coding agents — Part 2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2)

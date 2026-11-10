---
id: pre-commit-pre-push
title: "Pre-commit / pre-push"
group: deployability
qualities: [maintainability, security]
stages: [commit]
speed: [sub-second]
places: [delivery/work, remediation/work, maintenance/work]
---

# Pre-commit / pre-push

## Loop

Fast checks run when the agent commits or pushes. If a check fails, it rejects the commit before the change reaches CI. The source does not say which checks run here or what the agent gets back when a commit is rejected. The one check it names is linting, in Stripe's case below.

## Set up

The source gives one case: Stripe. It does not say which checks go in pre-commit and which in pre-push.

- Stripe follows the principle "shift feedback left". A background daemon caches lint results. According to the source, fixes then arrive "well under a second". The source does not say whether these are the linter's automatic fixes or the agent's own fixes after a lint report.

## Notes

- The source tags this loop with security, but it names no security check, tool or case for it.

## Sources

- [Minions: Stripe's one-shot, end-to-end coding agents — Part 2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2)

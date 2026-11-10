---
id: canary-feature-flags
title: "Canaries and feature flags"
group: deployability
qualities: [deployability, availability]
stages: [production]
places: [delivery/release, delivery/confirmation, remediation/release, remediation/confirmation, maintenance/release, maintenance/confirmation]
needs: [metrics, deploy]
---

# Canaries and feature flags

## Loop

An analysis compares the canary release with the baseline. If the canary performs worse, the release rolls back automatically, and the agent gets the metrics.

## Set up

- Use Argo Rollouts or Flagger.
- Add a kill switch.

## Notes

The source entry does not say:

- what the project needs before it can use Argo Rollouts or Flagger
- which metrics the analysis compares, or what counts as worse
- how the agent gets the metrics, or what it should do with them
- what the kill switch turns off, who uses it, and whether you need it as well as the canary tool or instead of it
- how feature flags fit into the loop

## Sources

The research cites no source for this loop.

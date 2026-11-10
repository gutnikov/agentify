---
id: chaos-engineering
title: "Chaos engineering"
group: reliability
agent: [investigator]
qualities: [availability, recoverability, continuity]
stages: [staging]
places: [remediation/entry]
needs: [metrics, deploy]
---

# Chaos engineering

## Loop

Pods or zones are killed in staging. From the alerts and SLOs the agent finds the recovery mechanism that is
missing.

## Set up

To set up the loop:

- write the experiments as code
- run the experiments only in an isolated environment

## Agent step

From the experiment's alerts and SLOs, an investigator returns which recovery mechanism was missing, as a Diagnosis.
It never blocks.

## Sources

The research cites no source for this loop.

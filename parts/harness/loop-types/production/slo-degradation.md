---
id: slo-degradation
title: "SLO degradation"
group: production
agent: [investigator]
qualities: [availability, reliability]
stages: [production]
places: [delivery/confirmation, remediation/entry, remediation/confirmation, maintenance/confirmation]
needs: [metrics]
---

# SLO degradation

## Loop

The agent watches the SLOs for latency, errors and availability and proposes fixes (Böckeler's example).

## Set up

- Agent access to monitoring.

## Notes

The source gives only the loop and the setup step above. It does not say:

- what counts as degradation
- what form a proposed fix takes
- how the agent learns of a degradation
- what level of monitoring access the agent needs
- who approves a fix, or how the loop checks that the SLO recovered

## Agent step

An investigator follows a degrading SLO to its cause through logs, traces and recent deploys, and returns a
Diagnosis with a proposed fix. It never blocks.

## Sources

- [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html) (Böckeler)

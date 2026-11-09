---
id: slo-degradation
title: "SLO degradation"
group: production
qualities: [availability, reliability]
stages: [production]
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

## Sources

- [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html) (Böckeler)

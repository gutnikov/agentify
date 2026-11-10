---
id: ai-judges-telemetry
title: "AI judges on telemetry"
group: production
agent: [judge]
qualities: [quality in use]
stages: [continuous]
places: [remediation/entry]
needs: [logs]
---

# AI judges on telemetry

## Loop

An AI judge is an LLM that checks a sample of responses and a sample of logs. It marks the anomalies it finds.

The source does not say:

- whose responses the judge checks
- what counts as an anomaly
- where the marks go, or how the coding agent gets them and acts on them

## Set up

- `/response-quality-sampling`, `/log-anomalies` (Böckeler).

The source gives these two names and credits them to Böckeler. It does not say what they are, where to get them, or what they need to run.

## Notes

- The source advises this for inferential sensors in general: they cost a lot to run and do not give the same result every time, so run them on a sample only. The source does not say whether it counts the AI judge as an inferential sensor. It gives no sample rate and no cost figures.

## Agent step

The judge is the loop. It gets a sample and a rubric of what counts as an anomaly, and returns a Verdict per item.
Its marks are trusted only after a person graded a sample and it agreed with them
([agent-calibration](../meta/agent-calibration.md)), and a sample audit checks it again later.

## Sources

- [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html) (Böckeler)

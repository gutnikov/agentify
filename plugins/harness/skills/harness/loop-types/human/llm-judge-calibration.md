---
id: llm-judge-calibration
title: "Calibrating an LLM judge on an expert (critique shadowing)"
group: human
sync: async
assesses: [result]
speed: [seconds]
places: [harness:delivery/oracle, harness:delivery/gate]
---

# Calibrating an LLM judge on an expert (critique shadowing)

## Loop

An expert grades a sample of results. You then revise an LLM judge's prompt until the judge grades that sample the
same way as the expert. This is prompt revision, not model training. From then on, the judge grades the whole stream
instead of the expert.

## Getting a good signal

- Hamel Husain's method needs one principal expert, so that the grades are consistent. The expert answers
  yes or no to whether the AI achieved the desired outcome, and writes a critique with reasons, instead of scoring on
  a 1–5 scale.
- Then you revise the judge's prompt, round after round, until its grades agree with the expert's (Simon Willison).
  The source does not say who does this work: the expert, an engineer or an agent.

## Notes

- Husain notes that building a judge is a handy way to make people look closely at their data.
- The source does not say:
  - how the expert's critiques are used in the judge's prompt
  - how closely the judge's grades must match the expert's, or on how many results, before calibration is finished
  - what to do if the judge never matches the expert
  - whether the expert has to check the judge again later

## When and how long

Calibration takes hours of the expert's time, once; after that, seconds per grade. The source gives no time for
revising the prompt.

## Related

- [llm-evals](../meta/llm-evals.md), [ai-judges-telemetry](../production/ai-judges-telemetry.md): where a
  calibrated judge is used.

## Sources

- Hamel Husain, *Using LLM-as-a-Judge For Evaluation*
- Simon Willison's retelling of critique shadowing

---
id: agent-calibration
title: "Calibration of a loop's agent"
group: meta
qualities: [correctness of non-deterministic components, trustworthiness]
stages: [local, scheduled]
speed: [minutes]
places: [harness:delivery/gate, harness:delivery/confirmation, harness:remediation/oracle, harness:maintenance/gate]
---

# Calibration of a loop's agent

## Loop

An agent that is a step of a loop, such as a reviewer, a refuter or a judge, is run at least three times on eval
cases with known answers, and its agreement with those answers is scored. It may block anything only after the
agreement reaches a threshold a person approved; until then, and whenever it falls below, it only advises. Its
verdicts in real use are logged with their outcome, and every false positive or miss becomes a new eval case.

```
created (draft) ──► eval cases with known answers ──► ≥3 runs ──► eval-score
                                                                     │
                       agreement ≥ approved threshold? ──no──► revise the prompt ──┐
                                   │yes                       (or keep it advisory) │
                                   ▼                                             ◄──┘
                       gate: its verdict can fail the loop
                                   │
   in use: each verdict's outcome is logged (confirmed, false positive, missed, overridden)
   a false positive or a miss ─────────► a new eval case ──► evals again
   the prompt or the model changes ────► evals again (the check refuses a gate that was not re-scored)
   on a schedule ──────────────────────► a person grades a random sample of its verdicts
```

## Set up

- **A registry.** `loops/agents.yaml` lists each agent with its kind, definition, model, status (`draft`,
  `evaluated`, `advisory`, `gate`, `retired`), threshold and last evaluation; `loops.py agent-new` adds one.
- **Eval cases** in `loops/agents/<id>/evals/`, each with the agent's input and `expected.json`, in the formats of
  the harness's `agent-formats.md`. For a reviewer, a guard or a refuter: broken copies that must fire and clean
  ones that must pass, usually made from the loop's own must-fire and must-pass cases. For a judge: results a
  person graded pass or fail, with a reason, under H5.
- **Runs and scoring.** Each run of the whole set is one `results/<run>.jsonl`; at least three runs, because the
  output differs from run to run. `loops.py eval-score <id> --record` scores agreement per case and overall, lists
  flaky cases, refuses runs older than the definition, and writes the registry and `report.md`.
- **The threshold** is a reference a person approves (H5), recorded in `threshold_source`. Without one the agent
  stays `evaluated` or `advisory`.
- **The rule that makes it safe**: only a `gate` agent blocks. `loops.py check` refuses an agent that blocks
  without being `gate`; a `gate` agent below its threshold, without three runs, or not re-scored after its
  definition or model changed; a judge that is `gate` without `human_grades: true`; and a `validated` or `active`
  loop whose agent is still `draft`.
- **Outcomes** of real verdicts: `loops.py outcome <id> --loop <loop> --outcome confirmed|false-positive|missed|overridden`.
  `loops.py stats` shows them since the last evaluation and asks for new eval cases after two false positives or
  misses.

## Notes

- This loop settles what the cards it builds on leave open. [llm-judge-calibration](../human/llm-judge-calibration.md)
  does not say how close is close enough, on how many results, or what to do when the judge never matches: here
  the threshold is an approved reference, the set is the agent's eval cases run three times, and an agent that
  never reaches it stays advisory or is retired. [llm-evals](llm-evals.md) covers prompts of product features; this
  is the same loop for the agents of the harness itself.
- Reviewers, guards, refuters and investigators can be calibrated without a person: their cases have answers a
  script can check. A judge of taste or quality cannot: only a person knows the right grade, so a person grades
  its cases once, and a [sample audit](../human/sample-audit.md) checks it again later.
- A repeated false positive is the agent's version of a repeated mistake: [steering-loop](steering-loop.md) turns
  it into an eval case, not into a line in the prompt alone.
- Without it, an agent's verdict is a guess presented as a check: the working agent learns to satisfy the reviewer,
  not to meet the requirement.

## Sources

- Hamel Husain, *Using LLM-as-a-Judge For Evaluation*: grading against one principal expert with pass or fail and
  a critique.
- Simon Willison's retelling of critique shadowing: revising the judge's prompt until it agrees with the expert.
- [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices): the agent doing the work isn't
  the one grading it.

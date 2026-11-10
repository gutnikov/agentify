# The harness level

The harness engineer's own work is the same four super-loops, run over the harness instead of the product: over its
loops, the agents in them, the guides and the policy. The product's super-loops are this level's production, and
their trace is its signal.

```
harness level   discovery · delivery · remediation · maintenance    the harness engineer, under agentify/policy.yaml
      ▲ the trace: exits not confirmed, failures by the phase that caught them, corrections, escalations,
      │            false positives and misses of agents, reverts
      ▼ new and fixed loops, agents, guides, policy
product level   discovery · delivery · remediation · maintenance    the agent doing the work
```

## The same four super-loops

| Super-loop | At the harness level | Its oracle | Confirmed when |
|---|---|---|---|
| discovery | `/agentify:init` maps the project; then which loops to build | The profile's facts and the failures in the history | The user chose the loops (H4) |
| delivery | A new loop for a failure a person named | Its must-fire and must-pass cases | It is wired in, and in use it catches real failures and stays quiet on correct work |
| remediation | A failure got past the loops, a loop fires on correct work, or an agent in a loop errs | The failure, recorded as a must-fire case or an eval | The loop is valid again, and the failure does not recur |
| maintenance | A model, a tool, a loop type or the project changed | The cases and evals as they pass now | Every case and eval gives the result it gave before |

The catalog's loops of this level:

- [steering-loop](../loop-types/meta/steering-loop.md) and
  [correction-becomes-rule](../loop-types/human/correction-becomes-rule.md) are its remediation: an escape or a
  repeated correction becomes a loop at the phase that should have caught it.
- [agent-calibration](../loop-types/meta/agent-calibration.md) runs three super-loops for one agent: delivery (from
  `draft` to `gate`), remediation (a false positive becomes an eval) and maintenance (a new model means a new score).
  [llm-judge-calibration](../loop-types/human/llm-judge-calibration.md) delivers a judge.
- [sample-audit](../loop-types/human/sample-audit.md) is its detector, as error tracking is the product's. Giving the
  agent more autonomy on its results is a release like any other: one step at a time, each with a window.
- [document-review](../loop-types/meta/document-review.md) checks the texts its delivery writes: every `LOOP.md` and
  every prompt of an agent.

## Its signal

Strongest first:

1. **A change that passed the gate and was not confirmed.** The tests let through what production rejected, so a
   phase before the gate lacks a check.
2. **A problem that a recent change introduced.** Remediation finds it; the super-loop and the phase that let it
   through are a failure of the harness.
3. **A person's corrections, escalations, the false positives and misses of agents, reverts.** The same correction
   made twice is a missing loop ([correction-becomes-rule](../loop-types/human/correction-becomes-rule.md)).

The measures of this level are the share of changes not confirmed (the change failure rate of DORA), failures by the
phase that caught them, repeated corrections of one kind, and calls to a person by policy id. Each should go down.

## "Confirmed" is statistical

That a class of failures stopped recurring shows only over many runs, so this level keeps its signal over time.
`agentify/hitl-log.jsonl` keeps the agent's calls to a person, and `agentify/agent-outcomes.jsonl` keeps what happened to
the agents' verdicts. The exits of the product's super-loops come from where the project already records them: the
profile's `trace` names those files, such as the deploy history. What no system records, such as a person's own
correction or an escape traced to its phase, goes into `agentify/trace.jsonl` through `loops.py trace`. `loops.py stats`
reads all of it.

## The boundary is a permission boundary

The agent doing the product's work does not run this level's loops on its own checks: that is how it would "fix" a
check that blocks it. The harness engineer changes the loops, under the policy, and the final run of every check
happens where the working agent cannot write.

## Sources

- Chris Argyris, Donald Schön, *Organizational Learning: A Theory of Action Perspective* (Addison-Wesley, 1978):
  single-loop learning corrects an action; double-loop learning changes the rules that produced it.
- [DORA](https://dora.dev): the change failure rate.

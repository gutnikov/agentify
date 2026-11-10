# Super-loops

A super-loop is the path a piece of work takes in a project, from where it enters to a change confirmed where the
change is used. A project has up to four, one for each kind of work. They are made of the loops in the
[catalog](../loop-types/README.md): every loop has a place in them, a super-loop and a phase. What a super-loop adds
to its loops is what only the whole can check: a gate before the release and a confirmation after it.

| Super-loop | Starts with | Ends with |
|---|---|---|
| [Delivery](delivery.md) | an idea or a requirement | the change confirmed where it is used |
| [Remediation](remediation.md) | a problem | the signal the problem was seen by, gone |
| [Maintenance](maintenance.md) | a trigger: a new version, an end of life, a schedule, a measure over its budget | a measure improved, and nothing changed for users |
| [Discovery](discovery.md) | a question or a hypothesis | a decision backed by evidence, which may be "do not build it" |

The harness itself is a second level with the same four super-loops: [the harness level](harness-level.md).

## The phases

Every super-loop goes through the same phases and leaves out those it has no use for: discovery has no release.

```
entry → oracle → work → gate → release → confirmation → exit
```

| Phase | What happens | Done when |
|---|---|---|
| `entry` | A piece of work arrives, from a detector or a person, and triage routes it to one super-loop | It is in one super-loop |
| `oracle` | What the work will be checked against is fixed before the work, out of the reach of the agent that does it | It is approved, or recorded as failing |
| `work` | The agent does the work, with its inner loops | The agent says it is done |
| `gate` | The work is checked against the oracle as a whole, in CI | Every item passes |
| `release` | The change reaches where it is used: deployed, a flag switched on, rolled out, published | It is there |
| `confirmation` | Where the change is used shows that it works and broke nothing, over a window | Confirmed, or not |

A super-loop is done only at its confirmation. Passing the gate means the work is ready to release, not that the
change works.

## Told apart by the oracle

| Super-loop | Oracle | The gate checks | The confirmation checks | Protected from the agent |
|---|---|---|---|---|
| delivery | An approved spec, and acceptance tests that fail before the work | Every requirement's tests pass | The change is there, it happened, nothing broke | The spec and the acceptance tests |
| remediation | A reproduction that fails, and the signal the problem was seen by | The reproduction passes, and the other tests are untouched | That signal is gone | The reproduction and the other tests |
| maintenance | The behaviour as it is, and the current value of the measure to improve | The tests pass with their expected values unchanged, and the measure improved | Production behaves as before, and the measure improved | The expected values of every existing test |
| discovery | The question, and the evidence that would answer it | Every claim in the answer has its evidence | The person who asked decided | The question, once the work has started |

The entry does not tell the super-loops apart: one complaint from a user can be a bug, an idea or a wish for
something faster. The oracle does. It decides what the gate checks and what the agent may not touch, so routing a
piece of work is choosing its oracle.

## Triage

| The signal says | Super-loop |
|---|---|
| It is not known yet whether to do it, or how | discovery |
| The product does not do what it was specified to do, or what it did before | remediation |
| The product should do something new or different | delivery |
| The behaviour stays; something else changes: a dependency, the structure, the speed, the size | maintenance |

The costly mistake is a change of behaviour routed to maintenance. Maintenance runs without a person approving any
behaviour, so the change would reach users unapproved. Its gate stops it: when a test's expected value has to change,
the work goes back to triage. The loop that routes is [triage](../loop-types/meta/triage.md).

## The trace

Every exit of a product super-loop leaves a record: the super-loop, the item, the exit, the phase where a failure was
caught, and the evidence. Most of it is already kept somewhere, in CI runs, deploys and the error tracker; the harness
collects it from there and records only what no system keeps, such as a person's own correction. The trace is the
signal of the [harness level](harness-level.md). Its strongest record is a change that passed the gate and was not
confirmed: a phase before the gate lacks a check.

A project's own records are files of JSON lines, one per event, named in its profile's `trace`:

```
{"at": "2026-11-10T10:50:34Z", "action": "confirm", "version": "2432236", "previous": "8598a5c",
 "result": "not-confirmed", "evidence": "~/.saas-test/prod/confirmations/2432236-20261110T104834Z"}
```

`action` is `deploy`, `confirm` or `rollback`; a confirmation's `result` is one of the super-loop's exits. What no
system records goes into the project's `loops/trace.jsonl` through `loops.py trace`, and `loops.py stats` reads both.

## Just enough

- **A project has the super-loops it has work for.** If every idea the product team brings gets built, discovery
  happens outside the harness.
- **A super-loop ends at the last stage the agent can read.** Production with its logs for a service, a published
  version for a library, a store release with its crash reports for a mobile app. Where the agent cannot read that
  stage, a person confirms.
- **A loop's place is the phase that should have caught the failure.** The earliest phase that can catch it is the
  cheapest.

## Sources

- ISO/IEC 14764, *Software Engineering — Software Life Cycle Processes — Maintenance*: corrective, adaptive,
  perfective and preventive maintenance. Corrective maintenance is remediation here; the others are maintenance, or
  delivery when they change the behaviour.
- [DORA](https://dora.dev): the change failure rate, the share of changes that fail where they are used.

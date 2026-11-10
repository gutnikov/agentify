---
id: maintenance
title: "Maintenance: from a trigger to an improvement users do not notice"
entry: trigger
phases: [entry, oracle, work, gate, release, confirmation]
exits: [confirmed, not-confirmed, inconclusive, behaviour-changed]
---

# Maintenance: from a trigger to an improvement users do not notice

## Super-loop

Something other than the product's behaviour asks for a change: a new version of a dependency, a runtime at its end
of life, a vulnerability, a measure over its budget, a schedule for clean-up. The agent changes the code so that users
notice nothing and a measure gets better. The change is released, and it counts as done when production behaves as
before and the measure has improved.

```
trigger
  → oracle: the behaviour as it is, and the measure's current value
  → work
  → gate: the tests pass with their expected values unchanged, and the measure improved
  → release
  → confirmation: production behaves as before, and the measure improved
      confirmed: done
      not confirmed: roll back → remediation
  an expected value had to change → back to triage: this is delivery or remediation
```

## Oracle

The behaviour as it is: the existing tests with their expected values, and the current value of the measure the
change should improve (the age of a dependency, the number of known vulnerabilities, coupling, the bundle size,
latency). The agent may change how a test reaches the code, such as a mock or a setup, but not what the test expects.

Where the tests do not cover the code the change touches, the oracle is weak. Characterization tests come first then:
they record what the code does now ([approved-fixtures](../loop-types/testing/approved-fixtures.md)).

## Phases

| Phase | What happens | Loop types |
|---|---|---|
| entry | A trigger arrives: a schedule, a release of a dependency, an end of life, a vulnerability, a measure over its budget | [triage](../loop-types/meta/triage.md), [dependency-updates](../loop-types/compatibility/dependency-updates.md), [dependency-scanning-sbom](../loop-types/security/dependency-scanning-sbom.md), [coupling-analysis](../loop-types/code/coupling-analysis.md), [garbage-collection](../loop-types/meta/garbage-collection.md), [knowledge-base-doc-lint](../loop-types/code/knowledge-base-doc-lint.md), [compliance-mutants](../loop-types/security/compliance-mutants.md) |
| oracle | The baseline is recorded: the tests that must stay as they are, and the measure's current value | [behaviour-invariance](../loop-types/meta/behaviour-invariance.md), [run-tests-first](../loop-types/testing/run-tests-first.md), [approved-fixtures](../loop-types/testing/approved-fixtures.md), [code-coverage](../loop-types/testing/code-coverage.md), [mutation-testing](../loop-types/testing/mutation-testing.md), [benchmarks-vs-baseline](../loop-types/performance/benchmarks-vs-baseline.md), [coupling-analysis](../loop-types/code/coupling-analysis.md) |
| work | The agent changes the code | The inner loops |
| gate | The tests pass with their expected values unchanged, and the measure improved | [behaviour-invariance](../loop-types/meta/behaviour-invariance.md), [verification-subagent](../loop-types/meta/verification-subagent.md), [api-breaking-changes](../loop-types/compatibility/api-breaking-changes.md), [contract-tests](../loop-types/testing/contract-tests.md), [db-migration-lint](../loop-types/compatibility/db-migration-lint.md), [agent-audit-trail](../loop-types/security/agent-audit-trail.md), [human-diff-review](../loop-types/human/human-diff-review.md) |
| release | The change reaches production | [health-checks-smoke](../loop-types/reliability/health-checks-smoke.md), [load-testing](../loop-types/performance/load-testing.md), [risky-action-gates](../loop-types/human/risky-action-gates.md), [canary-feature-flags](../loop-types/deployability/canary-feature-flags.md) |
| confirmation | Production behaves as the previous version did, and the measure improved where it is measured | [release-confirmation](../loop-types/production/release-confirmation.md), [canary-feature-flags](../loop-types/deployability/canary-feature-flags.md), [error-tracking](../loop-types/production/error-tracking.md), [slo-degradation](../loop-types/production/slo-degradation.md), [structured-logs](../loop-types/observability/structured-logs.md), [metrics-promql](../loop-types/observability/metrics-promql.md), [perf-budgets-telemetry](../loop-types/performance/perf-budgets-telemetry.md) |

## Gate

For every change, the gate checks whether any test's expected value changed, whether the tests pass, and whether the
measure improved against its baseline. A changed expected value fails the gate whatever the reason, and the work goes
back to triage. The final run is in CI. The loop is
[behaviour-invariance](../loop-types/meta/behaviour-invariance.md).

## Confirmation

The three checks of [delivery](delivery.md#confirmation), with the second one replaced: no new event should appear;
instead, the product's own events and errors stay at the previous version's level over the same window. Where the
measure shows in production, such as latency or memory, it is compared with the previous version too.

## Exits

| Exit | What it means | Where it goes |
|---|---|---|
| `confirmed` | Production behaves as before, and the measure improved | Done |
| `not-confirmed` | Production behaves differently | Roll back, then remediation |
| `inconclusive` | Too few events in the window | A synthetic run, or a person decides |
| `behaviour-changed` | The gate found a changed expected value | Back to triage: delivery if the new behaviour is wanted, remediation if the old one was wrong |

## Trace

For every change: the trigger, the exit, and whether the gate caught a change of behaviour. Repeated
`behaviour-changed` exits from one source, such as a dependency bot, say that triage routes too much here.

## When a project needs it

In every project with dependencies, a runtime or a codebase that ages. Its entry is usually a bot, such as Renovate
or Dependabot, or a schedule.

## Notes

- This is the super-loop most likely to run without a person: at OpenAI, the pull requests of
  [garbage collection](../loop-types/meta/garbage-collection.md) were merged automatically. That is why its gate checks
  the behaviour itself and does not rely on a review: a change of behaviour routed here would reach users with nobody
  approving it.
- ISO/IEC 14764 calls this adaptive, perfective and preventive maintenance; corrective maintenance is
  [remediation](remediation.md).

## Sources

- Martin Fowler, *Refactoring* (2nd edition, Addison-Wesley, 2018): changing the structure without changing the
  behaviour, with the tests as the check.
- Michael Feathers, *Working Effectively with Legacy Code* (Prentice Hall, 2004): characterization tests that record
  what the code does before it is changed.
- ISO/IEC 14764, *Software Engineering — Software Life Cycle Processes — Maintenance*.

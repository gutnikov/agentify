---
id: remediation
title: "Remediation: from a problem to a fix confirmed in use"
entry: problem
phases: [entry, oracle, work, gate, release, confirmation]
exits: [confirmed, not-confirmed, inconclusive, mitigated]
---

# Remediation: from a problem to a fix confirmed in use

## Super-loop

A problem is seen: an error in production, an alert, a crash a fuzzer found, a report from a person. Before any fix,
a reproduction makes the problem fail on demand. The agent removes the cause until the reproduction passes and nothing
else has changed. The fix is released, and the problem counts as fixed only when the signal it was seen by is gone.

```
problem
  → oracle: a reproduction that fails, and the signal the problem was seen by
  → work: the fix
  → gate: the reproduction passes, it failed before the fix, the other tests are untouched
  → release
  → confirmation: the signal is gone, nothing else broke
      confirmed: done; the reproduction stays as a regression test
      not confirmed: back to the oracle, the reproduction missed the problem
```

## Oracle

The reproduction: a test, a script or a recorded scenario that fails the way the problem does. It has to fail before
the fix; one that passes before the fix reproduces nothing. The agent doing the fix may not weaken the other tests to
make the fix pass.

The signal the problem was seen by is part of the oracle too: the issue in the error tracker, the alert, the log
query. The confirmation watches it. When no test can reproduce the problem (it is flaky, depends on the environment,
or shows only in production), the signal is the whole oracle, and the confirmation carries all the weight.

## Phases

| Phase | What happens | Loop types |
|---|---|---|
| entry | A detector or a person brings the problem, and triage routes it here: the product does not do what it was specified to do, or what it did before | [triage](../loop-types/meta/triage.md), [error-tracking](../loop-types/production/error-tracking.md), [slo-degradation](../loop-types/production/slo-degradation.md), [ai-judges-telemetry](../loop-types/production/ai-judges-telemetry.md), [fuzzing](../loop-types/testing/fuzzing.md), [dast](../loop-types/security/dast.md), [security-review-agent](../loop-types/security/security-review-agent.md), [chaos-engineering](../loop-types/reliability/chaos-engineering.md), [backup-restore-rollback](../loop-types/reliability/backup-restore-rollback.md), [exploratory-testing](../loop-types/human/exploratory-testing.md), [sample-audit](../loop-types/human/sample-audit.md), [user-feedback](../loop-types/production/user-feedback.md), [production-users](../loop-types/human/production-users.md) |
| oracle | The problem is reproduced, and the reproduction fails | [reproduction-gate](../loop-types/meta/reproduction-gate.md), [bug-failing-test-fix](../loop-types/testing/bug-failing-test-fix.md), [fuzzing](../loop-types/testing/fuzzing.md), [agentic-manual-testing](../loop-types/testing/agentic-manual-testing.md), [browser-console-devtools](../loop-types/observability/browser-console-devtools.md), [debugger-repl](../loop-types/observability/debugger-repl.md), [structured-logs](../loop-types/observability/structured-logs.md), [traces-opentelemetry](../loop-types/observability/traces-opentelemetry.md); the `app-probing` plugin for a web app |
| work | The agent removes the cause | The inner loops; [profiling](../loop-types/performance/profiling.md) for a slow path |
| gate | The reproduction passes, it failed before the fix, and the other tests were not changed | [reproduction-gate](../loop-types/meta/reproduction-gate.md), [verification-subagent](../loop-types/meta/verification-subagent.md), [agent-audit-trail](../loop-types/security/agent-audit-trail.md), [human-diff-review](../loop-types/human/human-diff-review.md) |
| release | The fix reaches production | [health-checks-smoke](../loop-types/reliability/health-checks-smoke.md), [risky-action-gates](../loop-types/human/risky-action-gates.md), [canary-feature-flags](../loop-types/deployability/canary-feature-flags.md) |
| confirmation | The signal is gone for the window, and nothing else broke | [release-confirmation](../loop-types/production/release-confirmation.md), [canary-feature-flags](../loop-types/deployability/canary-feature-flags.md), [error-tracking](../loop-types/production/error-tracking.md), [slo-degradation](../loop-types/production/slo-degradation.md), [structured-logs](../loop-types/observability/structured-logs.md), [metrics-promql](../loop-types/observability/metrics-promql.md) |

## Gate

For every problem, the gate checks that it has a reproduction, that the reproduction failed before the fix and
passes after it, and that no other test changed. A reproduction that passed before the fix fails the gate: it does
not show that the problem was there. The final run is in CI. The loop is the
[reproduction gate](../loop-types/meta/reproduction-gate.md).

## Confirmation

The same three checks as in [delivery](delivery.md#confirmation), with the second one turned around: the signal the
problem was seen by does not appear while the path it came from runs at least N times. A rare problem, seen once a
day, needs a window of days, or the result is `inconclusive`.

## Exits

| Exit | What it means | Where it goes |
|---|---|---|
| `confirmed` | The signal is gone for the window, and nothing else broke | Done; the reproduction stays as a regression test |
| `not-confirmed` | The signal is still there | Back to the oracle: the reproduction did not capture the problem |
| `inconclusive` | The path ran too few times in the window | A longer window, a synthetic run, or a person decides |
| `mitigated` | The service is restored without removing the cause: a rollback, a flag switched off, a restart | Stays open; the cause goes on from the oracle phase |

A mitigation and a fix are two exits for a reason: the first restores the service fast, the second removes the cause.
A postmortem goes to the harness level, not into this super-loop.

## Trace

For every problem: where it entered, its exit, and, when a recent change caused it, the super-loop and the phase that
let it through. A problem that a recent delivery introduced is a failure of that delivery too: its gate or its
confirmation missed it.

## When a project needs it

In every project that is in use. Without a detector at its entry, it starts only when a person notices; the first
detector is usually the error tracker, or a log query for errors by version.

## Sources

- Betsy Beyer et al., *Site Reliability Engineering* (O'Reilly, 2016), the chapter "Postmortem Culture: Learning from
  Failure".
- ITIL: incident management restores the service, problem management removes the cause.
- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/)
  (OpenAI): a failing test that reproduces the bug, before the fix.

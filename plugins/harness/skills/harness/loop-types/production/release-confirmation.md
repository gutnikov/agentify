---
id: release-confirmation
title: "Release confirmation: the change is there, it happened, nothing broke"
group: production
agent: [investigator]
qualities: [functional suitability, reliability, observability]
stages: [production]
speed: [minutes, hours, days]
places: [delivery/confirmation, remediation/confirmation, maintenance/confirmation]
needs: [logs, deploy]
---

# Release confirmation: the change is there, it happened, nothing broke

## Loop

After a release, a job waits for a window and judges a snapshot of it. A change counts as confirmed only when
production runs it, its own signal appeared often enough, and nothing broke compared with the previous version. This
is the confirmation phase of delivery, remediation and maintenance; the three differ in the second check.

| Super-loop | 1. The change is there | 2. Its signal | 3. Nothing broke |
|---|---|---|---|
| delivery | The version runs; behind a flag, the flag is on for the audience | The event the spec names appears at least N times | No new errors; the error rate and latency are no worse than the previous version's |
| remediation | The same | The signal the problem was seen by does not appear while its path runs at least N times | The same |
| maintenance | The same | The product's own events stay at the previous version's level, and the measure improved | The same |

## Set up

- **Every log line and every error carries the version.** Without it, nothing can be attributed to the release.
- **Each change names its signal before the work**: in the spec for delivery, as the reproduction's signal for
  remediation, as the measure for maintenance. With the `spec` plugin, every functional requirement has its `prod`
  signal, and `specs.py signals --base <ref>` writes those of a release in the format this loop reads.
- **The window is counted in events**: at least T minutes and at least N events on the changed path, up to a cap. At
  the cap with too few events, the result is `inconclusive`.
- **A weak baseline is said out loud.** Right after a rollback, the previous release may have served only a few
  requests. With fewer than half of the window's events to compare with, the check falls back to an absolute limit
  on the error rate (1%, say), skips the latency, and prints that the baseline is weak.
- **Wait in the wiring, judge in `run`.** A job after the deploy (in the pipeline, or on a schedule where deploys are
  manual) waits for the window, then saves a snapshot into a directory: the errors, event counts and metrics of the
  new version and of the previous one over comparable windows, and which version ran. `run` judges the snapshot, so it
  is fast and deterministic, and it fits the contract of any loop.
- **The output** is one line per item, `<item>: <status>`: `confirmed`, `not the running version`,
  `signal missing (3 of 50)`, `new error <fingerprint> (12)`, `error rate 2.1% vs 0.4%`, `inconclusive (too few
  events)`. The exit is non-zero for anything but `confirmed`.
- **The cases are recorded windows.** Must fire: a new error; the signal missing; the old version still running; too
  few events. Must pass: enough events, no new errors, the rates at the previous version's level.
- **Out of the agent's reach.** The job runs in the deploy pipeline or on a schedule, not in the agent's session; the
  agent reads its verdict. Rolling back belongs to the pipeline or to the canary tool.

## Notes

- Clean logs alone confirm nothing: a feature behind a flag that is off, or a path nobody takes, leaves them clean.
- Compare with the previous version, not with zero: production always has background errors. A canary tool makes this
  comparison by itself ([canary-feature-flags](../deployability/canary-feature-flags.md)); this loop adds the check
  that the change happened.
- A nightly job's window is its next run. A mobile release's window is the sessions on the new version over days.
- It answers what [canary-feature-flags](../deployability/canary-feature-flags.md) and
  [health-checks-smoke](../reliability/health-checks-smoke.md) leave open: what counts as worse, and how long to wait
  before a result counts as red.

## Agent step

An investigator gets the snapshot of a window that did not confirm and returns a Diagnosis: which check failed, the
errors or the missing events that show it, and the likely cause. It never blocks; the verdict on the snapshot does.

## Sources

- Netflix and Google, Kayenta (2018): canary analysis that judges a release against the previous version running
  beside it.
- James Governor, *Towards Progressive Delivery* (RedMonk, 2018): releasing step by step, with a check at every step.
- [DORA](https://dora.dev): the change failure rate.

---
id: load-testing
title: "Load testing"
group: performance
agent: [investigator]
qualities: [scalability, elasticity, capacity]
stages: [staging]
speed: [minutes]
places: [delivery/release, maintenance/release]
needs: [traces]
---

# Load testing

## Loop

The agent runs k6, Gatling or Locust against a preview, sees p95 degrade and looks for the bottleneck in the
traces.

## Set up

The loop needs:

- A preview deployment for the agent to run the load against. If your project has no preview, the agent has nothing to test, and you need to add one first.
- Traces from that preview. If your project collects no traces, the agent can see p95 degrade but cannot look for the bottleneck, and you need to add tracing first.
- Scenarios in the repository.
- Thresholds that end the run with a non-zero exit code.

## Agent step

An investigator reads the load run's report and the traces and returns the bottleneck as a Diagnosis. It never
blocks; the run's thresholds do.

## Sources

The research cites no source for this loop. It lists k6 among tools that reflect common practice and that the research itself did not verify. It does not say which claims about k6 went unchecked. It does not put Gatling or Locust on that list.

---
id: fault-injection
title: "Fault injection (Toxiproxy)"
group: reliability
qualities: [fault tolerance, resilience]
stages: [local, ci]
---

# Fault injection (Toxiproxy)

## Loop

A test calls the Toxiproxy HTTP API (port 8474) to add latency, a timeout or an outage to a dependency. Toxiproxy does not report pass or fail. Your test does. The agent then fixes retries and error handling.

## Scope

- Checks: fault tolerance and resilience when a dependency is slow, times out or goes down.
- Runs: locally and in CI.
- Needs: your own tests that pass or fail on how the code behaves under the fault. Toxiproxy gives no verdict without them.
- Toxiproxy: one of the sources calls it a "TCP proxy for chaos testing and CI".

## Set up

- Write the tests that pass or fail. Toxiproxy gives no pass/fail itself.
- Call `POST /reset` between tests.

## Sources

- [toxiproxy README](https://github.com/Shopify/toxiproxy/blob/main/README.md)
- [Toxiproxy: TCP proxy for chaos testing and CI](https://hysenlabs.com/en/projects/shopify-toxiproxy)
- [toxiproxy Go package](https://pkg.go.dev/github.com/Shopify/toxiproxy/v2)

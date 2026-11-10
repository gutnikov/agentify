---
id: contract-tests
title: "Contract tests"
group: testing
qualities: [compatibility, integrability, deployability]
stages: [ci]
speed: [minutes]
places: [delivery/work, delivery/gate, remediation/work, maintenance/gate]
---

# Contract tests

## Loop

The agent changes a provider and runs contract verification. Before a deploy, the agent runs `pact-broker can-i-deploy`. The command exits with code 0 ("yes") or 1 ("no"). It also returns a table of incompatible versions.

## Set up

Use Pact Broker.

Do not use Pact Broker's dry-run mode as a deploy check. In dry-run mode the check always succeeds, so the mode is only good for debugging.

## Sources

- [Can I Deploy](https://docs.pact.io/pact_broker/can_i_deploy) (Pact docs)

---
id: integration-tests-emulators
title: "Integration tests with emulators"
group: testing
qualities: [integrability, interoperability]
stages: [local, ci]
speed: [minutes]
---

# Integration tests with emulators

## Loop

The agent starts the real dependencies of the code (database, queue, cloud emulators), runs the tests against them and sees the errors in how the code works with those dependencies.

## Set up

- testcontainers or docker-compose.
- Emulators for external APIs.
- Seeds and fixtures.

## Sources

The research cites no source for this loop.

---
id: preview-environments
title: "Preview environments per PR"
group: deployability
qualities: [deployability, integrability]
stages: [preview]
speed: [minutes]
places: [delivery/release]
needs: [deploy]
---

# Preview environments per PR

## Loop

Every PR gets its own deployed environment. The agent runs e2e, DAST, Lighthouse and load tests against it and
reads its logs.

## Set up

To add this loop to a project, build:

- an IaC template that deploys an environment for each PR
- automatic teardown that removes these environments

The source does not say what the template must deploy, what starts a deployment, how the agent gets the environment's address and logs, or what triggers teardown. You need to decide these for your project.

## Sources

The research cites no source for this loop.

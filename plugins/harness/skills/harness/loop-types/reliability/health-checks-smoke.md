---
id: health-checks-smoke
title: "Health checks and smoke tests after deploy"
group: reliability
agent: [investigator]
qualities: [availability, operability]
stages: [preview, staging]
speed: [seconds]
---

# Health checks and smoke tests after deploy

## Loop

The agent polls `/health` and `/ready` and runs a smoke suite. When the result is red, it reads the startup logs.

The source does not say how long the agent keeps polling before it treats the result as red. It also does not say what the agent does after it reads the logs.

## Set up

To run this loop, the project needs:

- readiness checks that the source calls "meaningful" (it does not say what they must verify)
- a smoke suite that the agent can run after a deploy
- startup logs that the agent can read

The source does not say what the smoke suite should cover.

## Agent step

When the check is red, an investigator reads the startup logs and returns a Diagnosis. It never blocks; the health
check does.

## Sources

The research cites no source for this loop.

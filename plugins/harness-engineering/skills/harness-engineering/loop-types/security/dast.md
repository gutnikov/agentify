---
id: dast
title: "DAST"
group: security
qualities: [security (resistance)]
stages: [staging]
speed: [minutes]
---

# DAST

## Loop

A scanner attacks the preview environment. The agent fixes the vulnerabilities that the scanner finds.

## Set up

Run an OWASP ZAP baseline scan against the project's preview environment. A project without a preview environment gives the scanner nothing to attack.

The source does not give:

- a command or configuration for the scan
- a way to pass the scanner's report to the agent
- the condition that ends the loop

## Sources

The research cites no source for this loop and notes that it did not check ZAP separately.

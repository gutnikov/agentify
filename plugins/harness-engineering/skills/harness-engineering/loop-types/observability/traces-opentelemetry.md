---
id: traces-opentelemetry
title: "Traces (OpenTelemetry)"
group: observability
qualities: [analysability, performance]
speed: [seconds]
---

# Traces (OpenTelemetry)

## Loop

The agent queries traces (TraceQL) and finds a slow or failed span.

The source does not say what starts the query, what the agent does with the span, or how it checks that its fix worked.

## Set up

- The OTel SDK.
- A local collector.

Example: in the cited post, OpenAI uses Vector → VictoriaTraces. Vector passes traces on to VictoriaTraces. The source gives this as OpenAI's own setup, not as a requirement.

## Sources

- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) (OpenAI)

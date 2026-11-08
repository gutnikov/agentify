---
id: architecture-fitness-functions
title: "Architecture fitness functions"
group: code
qualities: [modularity, modifiability, evolvability]
stages: [commit, ci]
speed: [seconds]
---

# Architecture fitness functions

## Loop

The agent adds an import and runs `dependency-cruiser` or ArchUnit. If the import breaks a rule, the agent sees a message that names the rule and describes the layers, such as:

"clients-no-services: API clients must not depend on the orchestration layer…"

From the description of the layers, the agent knows which layer the code belongs in, and moves it there.

## Set up

Add these rules to `dependency-cruiser` or ArchUnit:

- rules for the direction of dependencies
- a rule that a new file goes only into one of the predefined folders

Give each rule a message that describes the layers, as in the example under Loop. The agent uses that description to find the right layer.

Example from OpenAI: every domain has the layers Types → Config → Repo → Service → Runtime → UI, and cross-cutting concerns come in only through Providers. Linters and structural tests check all of it.

## Sources

- [Maintainability sensors for coding agents](https://martinfowler.com/articles/sensors-for-coding-agents.html) (Böckeler)
- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) (OpenAI)

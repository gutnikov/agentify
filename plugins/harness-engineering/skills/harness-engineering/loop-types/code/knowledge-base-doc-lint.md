---
id: knowledge-base-doc-lint
title: "Doc linters for the knowledge base"
group: code
qualities: [understandability, supportability]
stages: [ci, scheduled]
---

# Doc linters for the knowledge base

## Loop

CI checks that the `docs/` folder is current, cross-linked and correctly structured. The agent reads the errors CI reports and fixes the docs.

## Set up

- A short AGENTS.md (about 100 lines at OpenAI) as a table of contents; `docs/` as the main source of truth.
- A "doc-gardening" agent that opens PRs for stale documents.

## Sources

- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) (OpenAI)

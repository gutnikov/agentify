---
id: executable-docs
title: "Executable documentation"
group: testing
qualities: [understandability, self-descriptiveness]
speed: [seconds]
---

# Executable documentation

## Loop

Doctests, and checking API responses against the OpenAPI schema, turn a mismatch between the docs and the code
into a failing test.

## Set up

The source names these tools and artifacts for this loop but gives no setup steps:

- doctest
- rustdoc
- generated artifacts, such as `docs/generated/db-schema.md` in OpenAI's repository

The source does not say what `docs/generated/db-schema.md` contains, what generates it, or which check fails when it goes out of date.

The source names no tool for checking API responses against the OpenAPI schema.

## Sources

- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) (OpenAI)

---
id: type-check
title: "Type checking"
group: code
qualities: [correctness, analysability]
stages: [local]
speed: [seconds]
---

# Type checking

## Loop

The agent runs `tsc --noEmit`, `mypy` or `pyright` and fixes the type mismatches it finds.

## Set up

- Strict mode.
- Parse data at the boundaries (OpenAI's rule "parse, don't validate").

## Notes

- Böckeler: a strongly typed language gives you this sensor for free.

## Sources

- [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html) (Böckeler)
- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) (OpenAI)

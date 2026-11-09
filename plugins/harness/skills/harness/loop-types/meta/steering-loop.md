---
id: steering-loop
title: "Steering loop"
group: meta
qualities: [process evolvability]
stages: [continuous]
---

# Steering loop

## Loop

A mistake the agent keeps repeating becomes a new guide or sensor.

- Guides work before the agent acts: AGENTS.md, skills, LSP.
- Sensors give feedback after the agent acts: tests, linters, logs, a browser, review agents.

## Set up

The source names two ways to set up this loop:

- Keep CLAUDE.md in git, as Anthropic does.
- For each repeated mistake, ask OpenAI's question: "what capability is missing, and how do we make it both legible and enforceable?"

## Notes

- Where you can, turn a repeated mistake into a sensor that runs as code (a lint or a test), not into text in a guide.
- Keep both guides and sensors. With sensors only, the agent repeats the same mistakes. With guides only, it never learns whether the guides worked.
- For corrections that come from a person: [correction-becomes-rule](../human/correction-becomes-rule.md).

## Sources

- [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html) (Böckeler)
- [Boris Cherny on X](https://x.com/bcherny/status/2007179861115511237)
- [claude code creator workflow](https://infoq.com/news/2026/01/claude-code-creator-workflow/) (InfoQ)
- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) (OpenAI)

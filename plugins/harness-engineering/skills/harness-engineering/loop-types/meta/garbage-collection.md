---
id: garbage-collection
title: "Garbage collection"
group: meta
qualities: [maintainability, evolvability]
stages: [scheduled]
---

# Garbage collection

## Loop

On a schedule, background agents look for code that breaks the "golden principles" written down in the repository, and open small PRs to fix it. At OpenAI, reviewing most of these PRs took under a minute, and they were merged automatically.

The source does not say:

- what the golden principles are, or give an example
- who reviews the PRs: a person, another agent or a CI check
- what lets a PR merge automatically
- what happens to the PRs that take longer to review

## Set up

- Write the golden principles down in the repository.
- Add a `QUALITY_SCORE.md` file to the repository.

The source does not say what `QUALITY_SCORE.md` contains, who updates it or how the agents use it.

## Notes

- Before this, OpenAI spent every Friday (20% of the week) cleaning up "AI slop" by hand.

## Sources

- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) (OpenAI)

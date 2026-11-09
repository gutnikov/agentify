---
id: mutation-testing
title: "Mutation testing"
group: testing
qualities: [testability, faultlessness]
stages: [local, ci]
---

# Mutation testing

## Loop

The agent sees surviving mutants — code changes the tests did not notice — and writes tests that catch them.

## Set up

- Incremental mutation on the diff: Stryker, PIT, mutmut.
- On the diff locally; the full run in CI.

## Notes

- Meta applied its ACH system to 10,795 Kotlin classes on 7 platforms. ACH generated 9,095 mutants and
  571 privacy-hardening tests. At the Messenger and WhatsApp test-a-thons engineers accepted 73% of its tests
  (Foster et al., FSE '25).
- Mutation testing checks behaviour independently of the agent's own tests. The research
  finds behaviour the worst
  covered of all qualities. It counts mutation testing among the independent behaviour checks that are
  especially valuable. The reason it gives: Böckeler writes that relying on tests the AI wrote itself is not yet
  enough.

## Sources

- [Mutation-Guided LLM-based Test Generation at Meta](https://dl.acm.org/doi/10.1145/3696630.3728544)
- [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html)

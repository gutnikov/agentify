---
id: compliance-mutants
title: "Compliance hardening with mutants"
group: security
agent: [worker]
qualities: [compliance, privacy]
stages: [ci, scheduled]
---

# Compliance hardening with mutants

## Loop

An LLM takes one concern, such as data leaks, and generates two things:

- mutants specific to that concern
- tests that catch those mutants

## Set up

- Follow the approach Meta calls ACH, which the linked source describes. It runs in three steps: a description of the concern, then mutants, then tests.
- Run the loop in CI or as a scheduled batch job.

The source does not say:

- whether the LLM is the coding agent or a separate generator
- who writes the description of the concern, or in what form
- which tool or model runs the steps
- where the generated tests go, or what signal reaches the coding agent
- what to do with mutants that no test catches, or with tests that fail on the unchanged code
- what starts a CI run, or how often batches run and what goes into each one

## Agent step

A worker generates the concern's mutants and the tests that catch them. A mutation run, not the worker, shows that
the tests fail on the mutants and pass on the real code: the worker does not grade its own tests.

## Sources

- [Meta: LLM-Powered Mutation Testing for Automated Test Generation](https://www.zenml.io/llmops-database/llm-powered-mutation-testing-for-automated-test-generation) (ZenML LLMOps Database)

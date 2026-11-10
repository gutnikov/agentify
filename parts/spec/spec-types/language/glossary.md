---
id: glossary
title: "Glossary"
group: language
role: layer
fits: [web, api, mobile, data, llm, library]
risks: []
tests: [none]
checks: own
cost: low
---

# Glossary

## What it describes

One name for each thing the product talks about, its meaning, and the synonyms that must not be used.

## When it fits

Always, from the first requirement, as `agentify/specs/glossary.yaml`. Tests, fixtures and Page Objects take their names
from the spec, so a second name for one thing becomes a second fixture for one state.

## How it is checked

`specs.py check` flags every name in the event model (screens, states, commands, events, errors, read models and
their fields) that uses a synonym the glossary lists under `not`. That every name is built from glossary terms is
a review, not a check.

## What the tests get

Stable names for fixtures, Page Object methods and test titles, and the same name in the UI text a test asserts.

## Set up

`agentify/specs/glossary.yaml` with `terms:`, each with `term`, `meaning` and `not` (synonyms to avoid), in the product's own
words from its UI and its tickets. Layer entry: `type: glossary`, `path: agentify/specs/glossary.yaml`.

## Evidence

Vendy: the UI says "credits" and "generations" where a modeller would say "tokens" and "jobs"; the reference model
in Gherkin used two names for one status and checked it two different ways.

## Sources

- [Ubiquitous language](https://martinfowler.com/bliki/UbiquitousLanguage.html) (Martin Fowler)

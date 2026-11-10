# Spec types

A spec type is a way to write down one aspect of a system so that a test writer can derive tests from it without
guessing. A project keeps **one spine** (the event model) and adds **layers** only for a named risk. Every layer
feeds its test obligations into the spine as examples, so the test writer reads one place.

Each card: what the type describes, when it fits, how it is checked (the official tool and what only an own check
catches), what the tests get from it, how to set it up, and the evidence behind it. `index.yaml` is generated
from the cards: `python3 ../scripts/specs.py catalog index`.

Evidence marked "Vendy" comes from describing vendy.ai (an AI ad generator with subscriptions and credits) in five
formats on 2026-11-09 and seeding deliberate defects into each model to see what the tools catch.

### The spine — `spine/`

- [Event model](spine/event-model.md)

### Rules — `rules/`

- [Decision tables](rules/decision-tables.md)
- [Examples in Gherkin](rules/examples.md)

### Behaviour over time — `behavior/`

- [State machines](behavior/state-machines.md)
- [BPMN processes](behavior/bpmn.md)

### Invariants and concurrency — `invariants/`

- [TLA+](invariants/tla-plus.md)

### Boundaries — `boundaries/`

- [Context map](boundaries/context-map.md)

### Contracts — `contracts/`

- [API contracts](contracts/api-contracts.md)

### Language — `language/`

- [Glossary](language/glossary.md)

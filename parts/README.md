# Parts

What `/agentify:init` and `/agentify:task` are made of. A part is a folder with a `README.md` and the files it needs.
It is not a skill and has no command of its own: the two commands read it when a phase needs it. `S` in a part's
README is that part's folder.

| Part | What it does | Read by |
|---|---|---|
| [harness](harness/README.md) | The super-loops, the catalog of 96 loop types, the project's `loops/` and `loops.py`: map, build, validate, revise and retire loops; the policy and the calls to a person | init; every task for the map and the policy; harness tasks for the rest |
| [spec](spec/README.md) | Turns requirements into a spec tests can be derived from without guessing: layers chosen by risk, their checks, the requirement trace, the delta for the test writer, the production signal of every requirement | the oracle of delivery; the harness task that sets up specs |
| [event-model](event-model/README.md) | The spine of the spec: an event model in YAML, and `em.py`, which checks it and exports it for the test writer | through spec |
| [fixture-modify](fixture-modify/README.md) | Playwright fixtures: the states tests and probes start from | acceptance tests, reproductions, probes |
| [pom-modify](pom-modify/README.md) | Playwright Page Objects: the only way tests, fixtures and probes touch the UI | acceptance tests, reproductions, probes |
| [app-probing](app-probing/README.md) | A throwaway probe of the running web app: the URL, credentials, test ids, console errors, failed requests, a screenshot | work in a web app, the oracle of remediation, discovery |
| [ui-prototypes](ui-prototypes/README.md) | Screens built from the project's design system, served at a local URL, one file each | the work of discovery |
| [text-quality](text-quality/README.md) | A text a person decides on, in Russian or English: a brief with sources, a writer, a fact check, a review, one revision | the answer of discovery, a proposal of loops, the `document-review` loop |

The scripts need Python 3; `specs.py` and `em.py` also need PyYAML. text-quality needs the `claude` CLI and network
access.

# private-plugins

Private Claude Code plugins.

| Plugin | Skill | What it does |
|---|---|---|
| `text-quality` | [`text-quality`](plugins/text-quality/skills/text-quality/SKILL.md) | Writes a text a person will decide on, in Russian (`ru/`) or English (`en/`) |
| `harness` | [`harness`](plugins/harness/skills/harness/SKILL.md) | Sets up and maintains a project's agent loops: designs, builds, validates and revises them, with a catalog of 91 loop types and a per-project policy for when an agent may call a person |
| `playwright` | [`fixture-modify`](plugins/playwright/skills/fixture-modify/SKILL.md), [`pom-modify`](plugins/playwright/skills/pom-modify/SKILL.md) | Writes the Playwright code tests stand on: fixtures that seed test state, and Page Objects |
| `app-probing` | [`app-probing`](plugins/app-probing/skills/app-probing/SKILL.md) | Probes the running web app with a throwaway Playwright script and reports what it really does |
| `ui-prototypes` | [`ui-prototypes`](plugins/ui-prototypes/skills/ui-prototypes/SKILL.md) | Finds a project's design system, sets up one command that serves prototypes built from its components at a local URL, and makes, opens, lists and deletes named prototypes |
| `spec` | [`spec`](plugins/spec/skills/spec/SKILL.md), [`event-model`](plugins/spec/skills/event-model/SKILL.md) | Turns requirements (a text or a ticket by link) into a spec that tests can be derived from without guessing: picks spec layers by risk from a catalog with an event model as the spine, checks them, traces requirements, hands the test writer the delta and a release's confirmation the production signal of every requirement |
| `bb` | [`bb`](plugins/bb/skills/bb/SKILL.md) | Sets up and maintains a repository's [bb](https://getbb.app) project, where every ticket in bb Tasks gets a manager session that runs hidden workers: inits a minimal project, runs the bb server locally or remotely and moves it between them, creates, lists and deletes periodic tasks that start a manager with an assignment |

Install:

```
/plugin marketplace add gutnikov/private-plugins
/plugin install text-quality@private-plugins
/plugin install harness@private-plugins
/plugin install playwright@private-plugins
/plugin install app-probing@private-plugins
/plugin install ui-prototypes@private-plugins
/plugin install bb@private-plugins
/plugin install spec@private-plugins
```

`text-quality` writes its runs to `.text-quality-runs/` at the root of the current project: add it to the project's `.gitignore`.

`harness` keeps a project's loops in `loops/` at its root, to be committed. Its `document-review` loop uses `text-quality`.

`app-probing` builds a missing fixture or Page Object with the skills of `playwright`: install both.

`ui-prototypes` adds to a project a `prototypes/` folder (a runner, a README with the design-system catalog, one file
per prototype) and a `proto` script. It works with React and Vite.

`spec` keeps a project's requirements, layers and spec in `specs/` at its root, to be committed. Its spine is an
event model (skill `event-model`), checked by `em.py` and handed to the test writer as JSON. Its checks run as the
`spec-check` loop of `harness`, and its production signals (`specs.py signals`) are what the `release-confirmation`
loop of `harness` looks for in production. Its scripts need Python 3 and PyYAML.

`bb` keeps its setup in bb itself (projects, the Manager preset, automations) and marks a repository it maintains
with `.bb/bb.yaml`, to be committed. It needs the `bb` CLI on this machine, pointed at the bb server.

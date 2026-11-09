# private-plugins

Private Claude Code plugins.

| Plugin | Skill | What it does |
|---|---|---|
| `spec` | [`spec`](plugins/spec/skills/spec/SKILL.md) | Writes a text a person will decide on, in Russian (`ru/`) or English (`en/`) |
| `harness` | [`harness`](plugins/harness/skills/harness/SKILL.md) | Sets up and maintains a project's agent loops: designs, builds, validates and revises them, with a catalog of 88 loop types and a per-project policy for when an agent may call a person |
| `playwright` | [`fixture-modify`](plugins/playwright/skills/fixture-modify/SKILL.md), [`pom-modify`](plugins/playwright/skills/pom-modify/SKILL.md) | Writes the Playwright code tests stand on: fixtures that seed test state, and Page Objects |
| `app-probing` | [`app-probing`](plugins/app-probing/skills/app-probing/SKILL.md) | Probes the running web app with a throwaway Playwright script and reports what it really does |
| `ui-prototypes` | [`ui-prototypes`](plugins/ui-prototypes/skills/ui-prototypes/SKILL.md) | Finds a project's design system, sets up one command that serves prototypes built from its components at a local URL, and makes, opens, lists and deletes named prototypes |
| `event-model` | [`event-model`](plugins/event-model/skills/event-model/SKILL.md), [`event-model-e2e`](plugins/event-model/skills/event-model-e2e/SKILL.md) | Describes a system as an Event Model in YAML and checks it with a script, then turns its specs into Playwright e2e tests on the project's fixtures and Page Objects |
| `bb` | [`bb`](plugins/bb/skills/bb/SKILL.md) | Sets up and maintains a repository's [bb](https://getbb.app) project, where every ticket in bb Tasks gets a manager session that runs hidden workers: inits a minimal project, runs the bb server locally or remotely and moves it between them, creates, lists and deletes periodic tasks that start a manager with an assignment |

Install:

```
/plugin marketplace add gutnikov/private-plugins
/plugin install spec@private-plugins
/plugin install harness@private-plugins
/plugin install playwright@private-plugins
/plugin install app-probing@private-plugins
/plugin install ui-prototypes@private-plugins
/plugin install bb@private-plugins
/plugin install event-model@private-plugins
```

`spec` writes its runs to `.spec-runs/` at the root of the current project: add it to the project's `.gitignore`.

`harness` keeps a project's loops in `loops/` at its root, to be committed. Its `document-review` loop uses `spec`.

`app-probing` builds a missing fixture or Page Object with the skills of `playwright`: install both.

`ui-prototypes` adds to a project a `prototypes/` folder (a runner, a README with the design-system catalog, one file
per prototype) and a `proto` script. It works with React and Vite.

`event-model` keeps a project's model in `model/` at its root, to be committed. Its script needs Python 3 and PyYAML.
`event-model-e2e` builds fixtures and Page Objects with the skills of `playwright` and looks at screens with
`app-probing`: install both.

`bb` keeps its setup in bb itself (projects, the Manager preset, automations) and marks a repository it maintains
with `.bb/bb.yaml`, to be committed. It needs the `bb` CLI on this machine, pointed at the bb server.

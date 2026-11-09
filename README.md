# private-plugins

Private Claude Code plugins.

| Plugin | Skill | What it does |
|---|---|---|
| `spec` | [`spec`](plugins/spec/skills/spec/SKILL.md) | Writes a text a person will decide on, in Russian (`ru/`) or English (`en/`) |
| `harness` | [`harness`](plugins/harness/skills/harness/SKILL.md) | Sets up and maintains a project's agent loops: designs, builds, validates and revises them, with a catalog of 88 loop types and a per-project policy for when an agent may call a person |
| `playwright` | [`fixture-modify`](plugins/playwright/skills/fixture-modify/SKILL.md), [`pom-modify`](plugins/playwright/skills/pom-modify/SKILL.md) | Writes the Playwright code tests stand on: fixtures that seed test state, and Page Objects |
| `app-probing` | [`app-probing`](plugins/app-probing/skills/app-probing/SKILL.md) | Probes the running web app with a throwaway Playwright script and reports what it really does |
| `bb` | [`bb`](plugins/bb/skills/bb/SKILL.md) | Sets up and maintains a repository's [bb](https://getbb.app) project, where every ticket in bb Tasks gets a manager session that runs hidden workers: inits a minimal project, runs the bb server locally or remotely and moves it between them, creates, lists and deletes periodic tasks that start a manager with an assignment |

Install:

```
/plugin marketplace add gutnikov/private-plugins
/plugin install spec@private-plugins
/plugin install harness@private-plugins
/plugin install playwright@private-plugins
/plugin install app-probing@private-plugins
/plugin install bb@private-plugins
```

`spec` writes its runs to `.spec-runs/` at the root of the current project: add it to the project's `.gitignore`.

`harness` keeps a project's loops in `loops/` at its root, to be committed. Its `document-review` loop uses `spec`.

`app-probing` builds a missing fixture or Page Object with the skills of `playwright`: install both.

`bb` keeps its setup in bb itself (projects, the Manager preset, automations) and marks a repository it maintains
with `.bb/bb.yaml`, to be committed. It needs the `bb` CLI on this machine, pointed at the bb server.

# private-plugins

Private Claude Code plugins.

| Plugin | Skill | What it does |
|---|---|---|
| `spec-writing` | [`spec-writing`](plugins/spec-writing/skills/spec-writing/SKILL.md) | Writes a text a person will decide on, in Russian (`ru/`) or English (`en/`) |
| `harness-engineering` | [`harness-engineering`](plugins/harness-engineering/skills/harness-engineering/SKILL.md) | Sets up and maintains a project's agent loops: designs, builds, validates and revises them, with a catalog of 88 loop types and a per-project policy for when an agent may call a person |
| `playwright-e2e` | [`app-probing`](plugins/playwright-e2e/skills/app-probing/SKILL.md), [`fixture-modify`](plugins/playwright-e2e/skills/fixture-modify/SKILL.md), [`pom-modify`](plugins/playwright-e2e/skills/pom-modify/SKILL.md) | Works with a web app through Playwright: probes the running app, builds fixtures that seed test state, writes Page Objects |
| `bb-engineering` | [`bb-engineering`](plugins/bb-engineering/skills/bb-engineering/SKILL.md) | Sets up and maintains a repository's [bb](https://getbb.app) project, where every ticket in bb Tasks gets a manager session that runs hidden workers: inits a minimal project, runs the bb server locally or remotely and moves it between them, creates, lists and deletes periodic tasks that start a manager with an assignment |

Install:

```
/plugin marketplace add gutnikov/private-plugins
/plugin install spec-writing@private-plugins
/plugin install harness-engineering@private-plugins
/plugin install playwright-e2e@private-plugins
/plugin install bb-engineering@private-plugins
```

`spec-writing` writes its runs to `.spec-runs/` at the root of the current project: add it to the project's `.gitignore`.

`harness-engineering` keeps a project's loops in `loops/` at its root, to be committed. Its `document-review` loop
uses `spec-writing`.

`bb-engineering` keeps its setup in bb itself (projects, the Manager preset, automations) and marks a repository it
maintains with `.bb/bb-engineering.yaml`, to be committed. It needs the `bb` CLI on this machine, pointed at the bb
server.

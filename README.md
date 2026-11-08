# private-plugins

Private Claude Code plugins.

| Plugin | Skill | What it does |
|---|---|---|
| `spec-writing` | [`spec-writing`](plugins/spec-writing/skills/spec-writing/SKILL.md) | Writes a text a person will decide on, in Russian (`ru/`) or English (`en/`) |
| `harness-engineering` | [`harness-engineering`](plugins/harness-engineering/skills/harness-engineering/SKILL.md) | Sets up and maintains a project's agent loops: designs, builds, validates and revises them, with a catalog of 88 loop types and a per-project policy for when an agent may call a person |
| `playwright-e2e` | [`app-probing`](plugins/playwright-e2e/skills/app-probing/SKILL.md), [`fixture-modify`](plugins/playwright-e2e/skills/fixture-modify/SKILL.md), [`pom-modify`](plugins/playwright-e2e/skills/pom-modify/SKILL.md) | Works with a web app through Playwright: probes the running app, builds fixtures that seed test state, writes Page Objects |

Install:

```
/plugin marketplace add gutnikov/private-plugins
/plugin install spec-writing@private-plugins
/plugin install harness-engineering@private-plugins
/plugin install playwright-e2e@private-plugins
```

`spec-writing` writes its runs to `.spec-runs/` at the root of the current project: add it to the project's `.gitignore`.

`harness-engineering` keeps a project's loops in `loops/` at its root, to be committed. Its `document-review` loop
uses `spec-writing`.

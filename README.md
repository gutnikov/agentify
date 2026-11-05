# private-plugins

Private Claude Code plugins.

| Plugin | Skill | What it does |
|---|---|---|
| `spec-writing` | [`spec-writing`](plugins/spec-writing/skills/spec-writing/SKILL.md) | Writes a text a person will decide on, in Russian (`ru/`) or English (`en/`) |

Install:

```
/plugin marketplace add gutnikov/private-plugins
/plugin install spec-writing@private-plugins
```

The skill writes its runs to `.spec-runs/` at the root of the current project: add it to the project's `.gitignore`.

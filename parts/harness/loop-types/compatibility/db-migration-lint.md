---
id: db-migration-lint
title: "Lint and run database migrations"
group: compatibility
qualities: [compatibility, availability, recoverability]
stages: [ci]
speed: [seconds, minutes]
places: [delivery/work, remediation/work, maintenance/gate]
---

# Lint and run database migrations

## Loop

A migration linter points at a dangerous operation. The agent rewrites the migration, then applies it and rolls it back on a throwaway database.

You can use either of these linters:

- Squawk, with the reporters `tty|gcc|json|gitlab`.
- Atlas `migrate lint`, with 50+ analyzers. They include checks for destructive changes and table locks.

## Set up

- JSON output.
- An "up → down → up" test.

## Notes

- Squawk also exits with code 1 when the tool itself fails.
- Since v0.38 `atlas migrate lint` is available only in Atlas Pro.

## Sources

- [ariga/atlas](https://github.com/ariga/atlas)
- [squawk CLI docs](https://github.com/sbdchd/squawk/blob/master/docs/docs/cli.md)
- [Verifying Migration Safety](https://atlasgo.io/versioned/lint) (Atlas)
- [Auditor plugin: Squawk (schema)](https://github.com/AdamFrisby/CodeyBox/pull/609)

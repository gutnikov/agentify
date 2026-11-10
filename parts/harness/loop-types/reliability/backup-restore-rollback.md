---
id: backup-restore-rollback
title: "Restore from backup and rollback"
group: reliability
qualities: [recoverability, durability]
stages: [scheduled]
places: [remediation/entry]
needs: [deploy]
---

# Restore from backup and rollback

## Loop

A job restores the database from a backup and rolls the release back. When the check fails, the agent fixes the
procedure.

The source does not say:

- which environment the job restores into and rolls back
- what the check verifies, or what counts as a failure
- which procedure the agent fixes
- whether the restore and the rollback run as one check or as two
- what happens if the agent cannot fix the procedure, or if the backup cannot be used

## Set up

- Run restore tests on a schedule. The source does not give an interval.

## Sources

The research cites no source for this loop.

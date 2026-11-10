---
id: <loop-id>                   # the folder name under loops/
title: "<what the loop guards, in a few words>"
type: <loop-type-id>            # from the plugin's loop-types/index.yaml, or custom
status: proposed                # proposed | built | validated | active | retired
trigger: []                     # edit | local | commit | ci | preview | staging | production | scheduled | task | sprint | continuous
run: ./run                      # one command; exit 0 = passes, non-zero = fires; machine-readable output
budget_seconds: 10              # one run must finish within this time
validation: cases               # cases (cases/must-fire, cases/must-pass) or manual (say why below)
agents: []                      # agents whose execution is a step of this loop, e.g. .claude/agents/reviewer.md
parts: []                       # composite loop only: ids of the loops under loops/ it is made of
hitl: []                        # ids from loops/policy.yaml this loop may call a person under
wiring: []                      # where the loop is hooked in, e.g. .claude/settings.json hooks.PostToolUse
---

# <title>

## Requirement

<The failure this loop prevents, and who asked for it. One or two sentences.>

## Loop

<What happens, step by step: what triggers it, what it checks, what the agent sees, what the agent does next.>

## Tools

<Each tool the loop runs, with the version it was validated with and how it is installed.>

## Signal

<What `run` prints when it fires: the format and one real example. It names the place and says how to fix it.>

## Validation

<What makes this loop trustworthy: the must-fire and must-pass cases and what each one stands for; for an agent
step, its evals; for a manual validation, why cases are not possible and what is checked instead.>

## Wiring

<Each place the loop is hooked in and what it does there.>

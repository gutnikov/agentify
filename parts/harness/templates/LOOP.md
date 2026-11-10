---
id: <loop-id>                   # the folder name under agentify/loops/
title: "<what the loop guards, in a few words>"
type: <loop-type-id>            # from the plugin's loop-types/index.yaml, or custom
status: proposed                # proposed | built | validated | active | retired
trigger: []                     # edit | local | commit | ci | preview | staging | production | scheduled | task | sprint | continuous
places: []                      # where it stands in the super-loops, as <super-loop>/<phase>: delivery/confirmation
run: ./run                      # one command; exit 0 = passes, non-zero = fires; machine-readable output
budget_seconds: 10              # one run must finish within this time
validation: cases               # cases (cases/must-fire, cases/must-pass) or manual (say why below)
agents: []                      # agents whose execution is a step of this loop, e.g. .claude/agents/reviewer.md
parts: []                       # composite loop only: ids of the loops under agentify/loops/ it is made of
hitl: []                        # ids from the plugin's defaults/hitl.yaml this loop may call a person under
wiring: []                      # where the loop is hooked in, e.g. .claude/settings.json hooks.PostToolUse
---

# <title>

## Requirement

<The failure this loop prevents, who asked for it, and its place: the super-loop and the phase that should have
caught the failure, such as `delivery/gate`. One or two sentences.>

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

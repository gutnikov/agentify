---
id: build
title: "Build / compile"
group: code
qualities: [correctness, analysability]
stages: [local, ci]
speed: [seconds]
places: [delivery/work, remediation/work, maintenance/work]
---

# Build / compile

## Loop

The agent edits code and runs `build`. It reads compiler errors with file and line and fixes them until the
command exits with code 0.

The source sets no limit on attempts. It also does not say when the agent should stop and hand the task back, for example when editing code cannot fix the error. Set your own stop condition when you set up this loop.

## Set up

- One build command, written in CLAUDE.md or AGENTS.md.
- Incremental build.
- Warm caches (Stripe pre-warms its Bazel and type-checking caches).

## Sources

- [Minions: Stripe's one-shot, end-to-end coding agents — Part 2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2)

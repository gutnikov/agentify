---
id: progress-file-feature-list
title: "Progress file and feature list"
group: meta
qualities: [process recoverability, auditability]
stages: [task]
places: [delivery/oracle, delivery/gate]
---

# Progress file and feature list

## Loop

An initializer creates a JSON list of features, each with `"passes": false`. Every session takes one feature and
marks it as passing only after an e2e check.

## Set up

- Use Anthropic's template from the article "Effective harnesses for long-running agents". The source entry gives no more setup steps than this.

## Notes

The source entry leaves out these points. Decide them yourself before you set up the loop:

- what the progress file is, and how it differs from the feature list
- what the initializer is, and what it builds the feature list from
- how a session picks which feature to take
- what a session does when the e2e check fails, or when the session ends before the feature passes

## Related

- [acceptance-loop](acceptance-loop.md): the same idea built on requirements, an approved spec and acceptance tests
  derived from it; it settles the points the Notes above leave open.

## Sources

- [Effective harnesses for long-running agents](https://anthropic.com/engineering/effective-harnesses-for-long-running-agents) (Anthropic)
- [Effective harnesses for long-running agents](https://businessdatasolutions.github.io/ai-wiki/sources/2025-11-26-anthropic-effective-harnesses-long-running-agents) (AI wiki summary)
- [Effective harnesses for long-running agents](https://daily.dev/posts/effective-harnesses-for-long-running-agents-7clzunmmu) (daily.dev)

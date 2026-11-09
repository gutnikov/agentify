---
id: api-breaking-changes
title: "Breaking changes in the API"
group: compatibility
qualities: [compatibility, evolvability]
stages: [local, ci]
speed: [seconds]
---

# Breaking changes in the API

## Loop

The agent changes a schema, and CI compares it with the schema on main. The source names two tools for the check:

- `buf breaking` prints a line for each break it finds, such as `user.proto:2:3:Field "1" on message "User" changed type…`.
- `oasdiff breaking --fail-on ERR` exits with code 1 when it finds a break.

The agent then restores compatibility or introduces a new API version.

## Set up

To set up the loop:

- Always pass `--fail-on` to oasdiff. Without it, oasdiff exits with code 0.
- Add a GitHub Action that posts annotations on the PR. The source cites the [oasdiff GitHub Action](https://www.oasdiff.com/docs/github-action) for this step.

## Sources

- [Detect Breaking API Changes with TypeScript & OpenAPI](https://www.sitepoint.com/detect-breaking-api-changes-typescript-openapi/)
- [Detecting breaking changes — Buf Docs](https://docs.bufbuild.ru/breaking/)
- [oasdiff GitHub Action](https://www.oasdiff.com/docs/github-action)

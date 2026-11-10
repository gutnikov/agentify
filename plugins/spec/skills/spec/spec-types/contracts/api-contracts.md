---
id: api-contracts
title: "API contracts"
group: contracts
role: layer
fits: [api]
risks: [public-api, multi-team, integrations]
tests: [contract, api]
checks: official
cost: medium
---

# API contracts

## What it describes

The shape of an API: operations, requests, responses and errors (OpenAPI), or messages on channels (AsyncAPI).

## When it fits

A public API, an API another team consumes, or events other services subscribe to. Each command of the spine maps
to an operation, each error in its `errors` to a response, each event other systems hear to a message.

## How it is checked

Official tools: `spectral` lints the document, `oasdiff` reports breaking changes between two versions. An own
check matches the contract to the spine: every command has an operation, every listed error a response.

## What the tests get

Contract tests and API tests: one per operation and per error response. The examples of the spine give the
request data and the expected responses.

## Set up

Keep the contract next to the code that serves it; link each operation to its slice id.

## Evidence

Not measured on Vendy, which has no public API.

## Sources

- [OpenAPI](https://spec.openapis.org/oas/latest.html)
- [AsyncAPI](https://www.asyncapi.com/docs/reference/specification/latest)
- [Spectral](https://github.com/stoplightio/spectral)
- [oasdiff](https://github.com/oasdiff/oasdiff)

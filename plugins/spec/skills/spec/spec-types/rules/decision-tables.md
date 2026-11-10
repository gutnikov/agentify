---
id: decision-tables
title: "Decision tables"
group: rules
role: layer
fits: [web, api, mobile, data]
risks: [money, permissions]
tests: [e2e, api]
checks: own
cost: low
---

# Decision tables

## What it describes

A rule as a table: input values on the left, the result on the right, one row per combination. Prices, credits,
limits, who may do what, which plan change is an upgrade.

## When it fits

Whenever a result depends on a combination of inputs: money, quotas, permissions, eligibility. Keep the tables in
the event model's `rules:` by default. Use DMN files only when people outside engineering edit the rules in a DMN
tool, or a DMN engine runs them in production.

## How it is checked

- In the event model: `em.py check` lists every input combination no row covers and every overlap.
- In DMN: `dmn-check` finds overlapping rows and type errors, but not missing combinations; that needs an own
  check. It also rejected standard DMN 1.3 until the file was rewritten in the Camunda dialect.

## What the tests get

One obligation per row of every table a slice uses. An example pins a row down with
`covers: [rule:<id>/<inputs…>]`; a test per row (or a parametrised test) follows. A missing combination is a
question, not a test: nobody knows the expected result.

## Set up

Domains for every input in `domains:`, the table in `rules:`, `unknown: true` for a rule nobody knows yet.

## Evidence

Vendy: generation cost was defined for 5 of 35 combinations of ad type and model, credits for an annual plan for 0
of 3 plans. The pricing page and the app disagreed (10 vs 14–22 credits per image ad). Seeded defects in DMN:
`dmn-check` caught the overlap and the wrong type, only an own check caught the gap.

## Sources

- [dmn-check](https://github.com/red6/dmn-check)

---
id: profiling
title: "Profiling"
group: performance
agent: [investigator]
qualities: [resource utilization, energy efficiency]
stages: [local]
---

# Profiling

## Loop

The agent takes a CPU or memory profile as text (the top N functions), makes a fix and compares the new profile
with the original.

The source does not say which run or workload to profile, which result shows that the fix worked, or what the agent should do when the new profile is no better or is worse.

## Set up

- py-spy or pprof with text output.

## Agent step

An investigator compares the two profiles and returns what changed and why, as a Diagnosis. It never blocks.

## Sources

The research cites no source for this loop.

---
id: fuzzing
title: "Fuzzing"
group: testing
qualities: [robustness, security (resistance)]
stages: [ci, scheduled]
places: [remediation/entry, remediation/oracle]
---

# Fuzzing

## Loop

The fuzzer finds a crash. The agent turns the minimal input into a regression test and fixes the code.

## Set up

To set up the loop:

1. Use a fuzzer. The research names libFuzzer, AFL++, cargo-fuzz and Go fuzzing.
2. Keep the input corpus in the repository.
3. Run the fuzzer in CI or nightly.

## Sources

The research cites no source for this loop and notes that it did not check cargo-fuzz separately.

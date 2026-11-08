---
id: bug-failing-test-fix
title: "Bug → failing test → fix"
group: testing
qualities: [reproducibility, debuggability]
stages: [local]
---

# Bug → failing test → fix

## Loop

The agent reproduces the bug with a test, fixes the code and shows a green run. The source does not say whether that run covers only the new test or the whole test suite.

At OpenAI the agent also records a video before and after the fix. The source does not say what the video shows, which bugs it is for or how to set it up.

## Set up

Give the agent this prompt: "write a failing test that reproduces the issue, then fix it". The source names no other step and does not say where the prompt goes.

## Notes

The source describes only the case where the new test fails, the fix makes it pass and nothing else goes wrong. It does not say what to do if:

- the new test passes before the fix, so it does not reproduce the bug
- the agent changes the test instead of the code
- an automated test cannot catch the bug, for example because the bug is flaky, depends on the environment or shows only in the UI

## Sources

- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) (OpenAI)
- [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)

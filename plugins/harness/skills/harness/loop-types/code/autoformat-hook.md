---
id: autoformat-hook
title: "Auto-formatting hook"
group: code
qualities: [maintainability]
stages: [edit, local]
speed: [sub-second]
---

# Auto-formatting hook

## Loop

After every file write a hook formats the code, so the agent spends no iterations on style.

## Set up

- A PostToolUse hook. Boris Cherny: the hook "handles the last 10% to avoid formatting errors in CI". The source quotes only this part of his sentence and does not say what the 10% is a share of.

## Notes

The source does not say:

- which tool calls trigger the hook
- which formatter command the hook runs, or whether it must match the formatter that CI checks against
- what the agent sees when the formatter fails on a file
- what happens when the hook rewrites a file the agent has read and is about to edit again

## Sources

- [Boris Cherny on X](https://x.com/bcherny/status/2007179861115511237)
- [claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice)

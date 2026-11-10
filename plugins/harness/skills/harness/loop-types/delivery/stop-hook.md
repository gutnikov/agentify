---
id: stop-hook
title: "Stop hook / `/goal`"
group: delivery
qualities: [any attribute a script can check]
stages: [local]
---

# Stop hook / `/goal`

## Loop

A hook runs a check and does not let the agent end its turn until the check passes.

**Limit:** in Claude Code, a Stop hook blocks the end of a turn no more than 8 times in a row. After the 8th block, the turn ends even if the check still fails.

## Set up

- A Stop hook in Claude Code.
- Or `/goal` with a separate evaluator.

## Notes

- With these mechanisms, an autonomous run can finish without a person. With a Stop hook, the run ends when the check passes, or after 8 blocks in a row. A passing check shows only what the script tests.
- Hooks make a check mandatory; CLAUDE.md is only advice.

## Related

- [acceptance-loop](../meta/acceptance-loop.md): a Stop hook keeps the agent working until its gate passes.

## Sources

- [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)
- [claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice)

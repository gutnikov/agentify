---
id: lsp-diagnostics
title: "LSP diagnostics after every edit"
group: code
qualities: [analysability]
stages: [edit, local]
speed: [sub-second]
---

# LSP diagnostics after every edit

## Loop

Right after every edit the agent gets the language server's diagnostics, before any build.

## Set up

- Install a code intelligence plugin in Claude Code. The source describes what it does in the words of the Claude Code docs: "automatic error detection after edits".
- The source does not name the plugin. It also does not say which languages the plugin covers, what it needs on the machine, or what to do if your project's language has no such plugin.

## Sources

- [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)

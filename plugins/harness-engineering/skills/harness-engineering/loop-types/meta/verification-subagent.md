---
id: verification-subagent
title: "Verification subagent"
group: meta
qualities: [correctness, auditability]
speed: [minutes]
---

# Verification subagent

## Loop

When the working agent says a task is done, a separate verification subagent tries to prove that claim wrong. One round takes minutes.

The source calls this subagent a fresh model and gives no more detail. It does not say:

- whether "fresh" means the same model started with a clean context, or a different model
- how the subagent checks the work, such as by reading the diff, running tests or opening the app
- what the subagent returns
- what happens when it finds a problem, or when the loop stops

## Set up

The source gives a principle and an example, but no setup steps:

- **Principle:** "the agent doing the work isn't the one grading it". The agent that made the change must not be the one that checks it.
- **Example:** Boris Cherny uses a subagent named `verify-app`. The source does not describe what `verify-app` does.

The source does not say what the subagent receives, what starts it or where its verdict goes.

For a web app, the [`app-probing`](https://github.com/gutnikov/my-claude-plugins/tree/main/plugins/playwright-e2e/skills/app-probing) skill (plugin `playwright-e2e@private-plugins`) lets the subagent open the app and check the claim there, not
only in the diff.

## Sources

- [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)
- [Boris Cherny on X](https://x.com/bcherny/status/2007179861115511237)

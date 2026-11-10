---
id: steering-loop
title: "Steering loop: every escape becomes a check at the phase that should have caught it"
group: meta
agent: [investigator]
qualities: [process evolvability]
stages: [continuous]
places: [harness:remediation/entry, harness:remediation/oracle, harness:remediation/work]
---

# Steering loop: every escape becomes a check at the phase that should have caught it

## Loop

An escape is a failure that got further than it should have: a change that passed the gate and was not confirmed in
production, a problem a recent change introduced, a mistake the agent keeps repeating, a correction a person had to
make. For each escape, the harness finds the phase of the super-loop that should have caught it, records the escape
as a must-fire case there, and fixes or adds the loop at that phase: a sensor where it can, a guide where it cannot.

- Guides work before the agent acts: AGENTS.md, skills, LSP.
- Sensors give feedback after the agent acts: tests, linters, logs, a browser, review agents.

## Set up

- **Read the escapes from the trace**: the exits of the product's super-loops, with the phase where each failure was
  caught ([the harness level](../../super-loops/harness-level.md)).
- **Three answers for each escape**: where it was caught, where it was introduced, and the earliest phase that could
  have caught it. The loop goes to that earliest phase.
- **The escape is the case.** Its input becomes a must-fire case of the loop at that phase, and the loop is validated
  again.
- **Confirmed when it stops.** The same class of escape does not come back over the next releases. If it does, the
  loop sits at the wrong phase or checks the wrong thing.
- Keep CLAUDE.md in git, as Anthropic does, and for each repeated mistake ask OpenAI's question: "what capability is
  missing, and how do we make it both legible and enforceable?"

## Notes

- Where you can, turn an escape into a sensor that runs as code (a lint or a test), not into text in a guide.
- Keep both guides and sensors. With sensors only, the agent repeats the same mistakes. With guides only, it never
  learns whether the guides worked.
- For corrections that come from a person: [correction-becomes-rule](../human/correction-becomes-rule.md).

## Agent step

An investigator gets an escape with its evidence and returns a Diagnosis: where the failure was introduced, the
earliest phase that could have caught it, and the loop type that would catch it there. It never blocks; the harness
engineer decides what to build.

## Sources

- [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html) (Böckeler)
- [Boris Cherny on X](https://x.com/bcherny/status/2007179861115511237)
- [claude code creator workflow](https://infoq.com/news/2026/01/claude-code-creator-workflow/) (InfoQ)
- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) (OpenAI)

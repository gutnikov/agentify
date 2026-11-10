---
id: acceptance-loop
title: "Acceptance loop: from requirements to green acceptance tests"
group: meta
qualities: [functional suitability, correctness, traceability]
stages: [task, local, ci]
speed: [minutes, hours]
---

# Acceptance loop: from requirements to green acceptance tests

## Loop

A requirement comes in, becomes an approved spec, the spec becomes acceptance tests that fail, and the agent works
until those tests pass. The loop's gate reports, for each requirement, whether its tests exist, failed before the
work and pass after it. It is a composite loop: its stages are other loops of the project, and its own check is
the gate over them.

1. **Requirement → spec.** A ticket or a text becomes a spec with examples: a named state, the inputs, what the
   person sees or the error. [spec-check](../testing/spec-check.md) keeps it whole. What the sources do not settle
   goes to a person ([interview](../human/interview.md),
   [escalation-on-uncertainty](../human/escalation-on-uncertainty.md)), and a person approves the spec
   ([human-acceptance-criteria](../human/human-acceptance-criteria.md)).
2. **Spec → acceptance tests, red.** A test writer derives the tests from the spec's examples, one test per
   example, tagged with the example's id and its requirements. They run and fail: a test that passes before the
   work tests nothing.
3. **Work.** The agent implements with its inner loops: [build](../code/build.md), [types](../code/type-check.md),
   [lint](../code/lint-with-fix-instructions.md), [red/green TDD](../testing/red-green-tdd.md) for the units,
   [e2e](../testing/e2e-browser.md) to look at the app.
4. **Gate.** Every approved requirement is traced to at least one acceptance test, all of them pass, and the spec
   and the acceptance tests are the ones that were approved. A [Stop hook or `/goal`](../delivery/stop-hook.md)
   keeps the agent working until the gate passes.
5. **A person** checks intent only: the spec before the work, and, if the project wants it, the behaviour after it
   ([result-demo](../human/result-demo.md)).

A test that is red after the work goes back to where the mistake is:

| The test fails because | It goes back to |
|---|---|
| the code does not do what the example says | the agent's inner loops |
| the test does not do what the example says | the test writer |
| the example is wrong or ambiguous | the spec, with a question to a person and a new approval |

## Set up

- **Roles kept apart.** The spec writer, the test writer and the implementing agent are separate agents or
  sessions; a [verification subagent](verification-subagent.md) can be a fourth. The agent doing the work is not
  the one grading it.
- **A protected oracle.** The implementing agent cannot change the spec or the acceptance tests: a PreToolUse hook
  denies its writes to them, and the final run of the gate happens in CI, out of its reach. A change to an example
  goes through the spec and a new approval.
- **Red first.** Keep the acceptance run from before the work: a CI job on the branch's first commit, or a run in
  the task's evidence. The gate compares the two.
- **The gate is the `run`.** One command prints one line per requirement, `<requirement id>: <status>` (`no test`,
  `red`, `green`, `green before the work`, `changed without approval`), and exits non-zero while any approved
  requirement is not `green`. It reuses the acceptance suite's report and the requirement trace (with the `spec`
  plugin: `specs.py trace`, and tests tagged with example ids); it adds no check a part already makes.
- **Parts.** `parts:` in the loop's `LOOP.md` lists the project's loops for each stage, such as `spec-check`, the
  inner loops and the Stop hook. The acceptance loop is validated after its parts, and is `active` only while they
  are.
- **Cases.** Must fire: a requirement without a test; a test that was green before the work; an acceptance test the
  implementing agent weakened; an example changed without a new approval. Must pass: a requirement whose tests went
  from red to green with the spec and the tests untouched.

## Notes

- This is the double loop of acceptance-test-driven development, an outer acceptance test that fails first around
  an inner loop of unit tests, started one step earlier: at the requirement and the approved spec, not at a
  hand-written acceptance test.
- It is this catalog's answer to its main caveat, that no sensor can check correctness if a person has not
  specified what they want: the person specifies once, as an approved spec, and every later run reuses it.
- [progress-file-feature-list](progress-file-feature-list.md) is the same idea with a feature list and an e2e
  check. This loop settles what that card leaves open: the list comes from the requirements, a feature passes when
  its acceptance tests pass, and a failure goes back by the table above.
- Without the protected oracle the loop proves nothing: an agent that can edit the tests can turn any gate green,
  as Kent Beck warns of the "genie" that disables or deletes tests.

## Sources

- Steve Freeman, Nat Pryce, *Growing Object-Oriented Software, Guided by Tests* (Addison-Wesley, 2009): the outer
  acceptance-test loop around the inner unit-test loop.
- [Effective harnesses for long-running agents](https://anthropic.com/engineering/effective-harnesses-for-long-running-agents)
  (Anthropic): features that pass only after an e2e check.
- [Genie Wants to Leap](https://newsletter.kentbeck.com/p/genie-wants-to-leap) (Kent Beck): agents that disable
  or delete tests.

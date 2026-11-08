# Human-in-the-loop loop types

A person in the loop is the only sensor of intent. Tests, linters and logs check that the code works; only a
person can say whether it is the code we need. This group adds 16 loop types to the [catalog](../README.md)
where the signal comes from a person.

It is based on Alexander Gutnikov's note on human-in-the-loop cycles (2026-11-08, in Russian).

A person's signal is slow (minutes to days), noisy (people make mistakes and contradict themselves) and expensive
(attention is scarce). So a good human loop follows three rules:

1. **Bring a person in only where a mistake is costly**: ambiguous requirements, irreversible actions, questions
   of taste and priority. The agent does the rest itself.
2. **Collect the signal in a structured form**: questions with answer options, a pass/fail grade with a reason, a
   demo of the result instead of reading the diff.
3. **Turn every human signal into an automated one**: an interview answer into a spec, a correction into a test or
   a lint, an expert's judgement into a calibrated LLM judge. A person should never have to correct the same thing
   twice.

The main risk is not slowness but the illusion of control: confirmation fatigue and rubber-stamp review give a
false sense that a person checked everything.

## The person as a sensor

Judged by the same criteria as an automated sensor, a person loses on almost all of them except one: they know
what we want.

| Property | Automated sensor | Person | What to do about it |
|---|---|---|---|
| Speed | seconds to minutes | minutes to days | Asynchrony, batched questions; the agent never idles |
| Determinism | high | low: gets tired, forgets, contradicts themselves | One principal expert, binary grades, recorded decisions |
| Cost | pennies | the team's most expensive resource | Route by risk; a person only on exceptions |
| Machine-readability | exit code, JSON | free text | Questions with options, answer templates |
| Knows the intent | no | yes | The only reason to keep a person in the loop |
| Expertise and taste | only what is formalized | yes | Turn them into rules, references and LLM judges |

Hence the principle: **a person is a sensor of intent and judgement, not of mechanics.** Everything a test can
check should be checked by a test, so that the person's attention goes to "are we building the right thing" and
"is this how it should look".

Matt Pocock puts it this way: a person in the loop catches a problem while it is cheap, but their attention is
scarce, and the craft of working with agents is to move more and more work out of the loop safely — replacing
supervision with plans, automated checks and review at the end (AI Hero).

## How the loops differ

Four axes set how much a loop costs and how reliable its signal is. Each is a frontmatter field.

| Axis | Field | Values | Why it matters |
|---|---|---|---|
| When | `when` | `before` work · `during` · `after` · in `production` | The earlier, the cheaper it is to fix a misunderstanding |
| Who starts it | `initiator` | the `agent` asks · a `human` interrupts · a gate by `rule` · a `schedule` | An agent's question hits the uncertainty more precisely; a rule gate is more reliable but quickly causes fatigue |
| Synchrony | `sync` | `blocking` (the agent waits) · `async` (the agent goes on) | A blocking loop stops the agent, an asynchronous one does not |
| What is assessed | `assesses` | `intent` · `plan` · `result` · `code` · `action-risk` | Only a person assesses intent and result; code and risk can be partly automated |

The note names the axes but does not tag each loop with them. The values in the files are read from each loop's
text, and a field is left out where the text does not settle it.

In practice the best loops are early, asynchronous, and assess intent or result. The worst are synchronous
confirmations of every action: they are expensive and quickly become a formality.

## File format

As in the [catalog](../README.md#file-format), with these differences:

```yaml
---
id: interview
title: "Interview"
group: human
when: [before]          # the axes above; each is optional
initiator: agent
sync: blocking
assesses: [intent]
stages: [task]          # same values as the automated loop types
speed: [minutes]        # one round, including the wait for the person
---
```

- No `qualities`: a person is the sensor of intent, not of one quality attribute.
- Body sections: **Loop**, **Getting a good signal**, **Notes** (data and risks, when there are any), **When and
  how long**, **Related** (loops that pair with it), **Sources**.

## Loops

### Before work

The most profitable loops: one minute of a person's time here saves hours of the agent going the wrong way.

- [Interview](interview.md)
- [Task restatement](task-restatement.md)
- [Plan approval](plan-approval.md)
- [Acceptance criteria and references from a person](human-acceptance-criteria.md)

### During work

The main job here is not to block the agent: a person is needed at rare points, not at every step.

- [Escalation on uncertainty](escalation-on-uncertainty.md)
- [Asynchronous questions with assumptions](async-questions-with-assumptions.md)
- [Gates on risky actions](risky-action-gates.md)
- [Observe and interrupt](observe-and-interrupt.md)

### After work

A person judges the result. The closer the subject is to behaviour rather than code, the faster and more accurate
the signal.

- [Result demo](result-demo.md)
- [Choose from options](choose-from-options.md)
- [Diff review by a person](human-diff-review.md)
- [Exploratory testing](exploratory-testing.md)

### Scaling expertise and production

These loops turn a rare human signal into a permanent automated one. They are what makes the agent more
autonomous over time.

- [Calibrating an LLM judge on an expert (critique shadowing)](llm-judge-calibration.md)
- [Sample audit](sample-audit.md)
- [Steering: every correction becomes a rule](correction-becomes-rule.md)
- [Users in production](production-users.md)

## Making a person's signal fast and accurate

Eight practices that both cut the person's time and improve their answer.

1. **Route by risk.** Call a person on three signs: ambiguous requirements, an irreversible action, a question of
   taste or priority. Agents handle the routine, people the exceptions (AlignX).
2. **Questions with options.** Picking one of 2–4 options is faster than writing an answer, and the spread is
   smaller. The last option is "other, I'll explain".
3. **Batching and asynchrony.** Non-blocking questions pile up and are asked in one batch; meanwhile the agent
   works on recorded assumptions.
4. **Evidence, not claims.** Show the person command output, screenshots, a preview — not a retelling that
   "everything works".
5. **Small portions.** A small diff, one question at a time, one feature per demo: attention does not dilute.
6. **Binary grades with a reason.** "Pass / fail" plus one or two sentences why. People read 1–5 scales
   differently.
7. **One principal expert.** For judgements of taste and quality, one person whose opinion is the reference;
   otherwise the signal contradicts itself.
8. **Convert into automation.** Every answer from a person is written where a machine will read it: a spec, a
   test, a reference, a lint, CLAUDE.md, a dataset for the judge.

## Anti-patterns and a wrong signal

A human loop breaks in two ways: the person stops really checking, or the person is wrong and the agent obediently
follows the mistake.

| Anti-pattern | How it shows | What to do |
|---|---|---|
| Rubber-stamp review | Large generated diffs are approved without reading; volume grows, attention drops (Kilo) | Small diffs, [result demos](result-demo.md), [sample audits](sample-audit.md) |
| Confirmation fatigue | 93% of permission requests are approved, many without a meaningful check (Resilient Cyber) | [Gates](risky-action-gates.md) only on the irreversible, the rest in a sandbox |
| One reviewer for everything | In an analysis of 25,000 agent PRs, 78.9% follow a pattern where the reviewer and the committer are the same person (Daniel Vaughan) | Review rules in AGENTS.md, spread the review, AI review as the first filter |
| Uncontrolled parallelism | Many agents; merging is faster than anyone can check | Generate in parallel, decide sequentially (Kilo) |
| Agent sycophancy | The agent follows an instruction that contradicts the tests, the data or a contract | A person's instruction is a hypothesis: the agent shows the contradiction with evidence and asks, instead of silently obeying |
| Corrections that are not remembered | The person repeats the same correction from task to task | The rule "twice means a sensor" ([correction-becomes-rule](correction-becomes-rule.md)) |

A wrong signal from a person is normal, not a failure. Protection against it: record decisions (so they can be
revisited), check an instruction with automated sensors before applying it, and compare the expert's opinion with
real user data. Husain explicitly advises checking leadership's assumptions against user feedback regularly
(Hamel Husain).

## Metrics

A human loop needs measuring too; otherwise it is unclear whether the agent's autonomy is growing or the person's
attention is just dropping.

| Metric | What it shows | Good trend |
|---|---|---|
| Review latency: how long a PR waits until review starts (CodeRabbit) | Whether the person has become the bottleneck | Goes down |
| Share of results accepted without edits | How well the agent hits the intent | Goes up |
| Escalations by type | Where the agent lacks rules or tools | Recurring types disappear |
| Repeated corrections of one type | Whether [correction-becomes-rule](correction-becomes-rule.md) works | Tends to zero |
| Mismatches in the [sample audit](sample-audit.md) | Whether autonomy can be extended | Goes down |
| Agreement of the LLM judge with the expert | Whether the judge can replace the expert | Goes up and stays high |

## Where to start

1. [Interview](interview.md) and [plan](plan-approval.md), with the spec written into the repository.
2. [Acceptance criteria and references](human-acceptance-criteria.md) approved by a person.
3. An explicit "when to ask, when not to" list in CLAUDE.md ([escalation](escalation-on-uncertainty.md));
   [gates](risky-action-gates.md) only on the irreversible.
4. [Result demos](result-demo.md) instead of reading code where possible; small diffs.
5. The rule "twice means a sensor" ([correction-becomes-rule](correction-becomes-rule.md)), and a log of
   escalations.
6. [Sample audits](sample-audit.md) and [LLM judge calibration](llm-judge-calibration.md), once the review volume
   no longer fits in one person's head.

## Caveats

- Some practices — task restatement, asynchronous questions with assumptions, choosing from options, sample audit —
  generalize common practice without a separate primary source.
- Numbers from secondary sources and vendor materials are approximate.

## Sources

The note names its sources without links.

- Anthropic, *Measuring AI agent autonomy in practice* (18 February 2026): how long agents work autonomously,
  auto-approval among new and experienced users, agent questions and human interruptions.
- [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices): interviews through
  AskUserQuestion, plan mode.
- Matt Pocock, *Human-in-the-loop* and *Human review* (AI Hero).
- Hamel Husain, *Using LLM-as-a-Judge For Evaluation*, and Simon Willison's retelling: critique shadowing.
- Resilient Cyber, *The human in the loop illusion*: the share of approved permission requests (secondary
  retelling of Anthropic's data).
- Latent Space, *Anthropic's Agent Autonomy study*: the share of irreversible actions (secondary retelling).
- Daniel Vaughan, *The Single-Human Oversight Bottleneck*: an analysis of 25,000 agent PRs (secondary retelling of
  a study).
- Kilo, *Human-in-the-loop AI coding*: review anti-patterns (vendor material).
- AlignX, *Designing Human-in-the-Loop for Agentic Workflows*: escalation on exceptions, logging escalations by
  type.
- CodeRabbit, *AI pair programming in the agentic SDLC*: review as the bottleneck, the review latency metric
  (vendor material).
- Rick Hightower, *Claude Code day by day*, and Towards AI, *spec-driven development*: the plan in the repository,
  choosing between a plan and an interview.

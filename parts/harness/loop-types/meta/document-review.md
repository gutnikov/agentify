---
id: document-review
title: "Review of document texts"
group: meta
agent: [reviewer]
qualities: [understandability, correctness]
stages: [local]
speed: [minutes]
places: [delivery/work, discovery/gate, harness:delivery/work]
---

# Review of document texts

## Loop

The agent does not write the document itself. It writes a brief. A separate writer writes the text from the brief, and then the text is checked. In this card, "the agent" means the agent that writes the brief and answers questions about it. "The writer" means the language package's writer, and "the user" means the person the agent can ask.

1. **Brief.** The agent writes down:
   - what the text is
   - every fact, with its source
   - its own conclusion, with reasons
   - what is not known
   - who the reader is and what they must do
2. **Brief check** (`check-brief`). A model reads the brief through the reader's eyes and asks up to 5 questions. It asks about what to do if something goes wrong, exact numbers instead of "about", unexplained terms, whom to contact and contradictions. The agent first answers from the code and documents. It asks the user about anything it cannot find, in one message, and waits for the answer. If there is no one to ask (automation, a nightly run), the agent writes "we don't know". The answers go into the brief, and "we don't know" counts as an answer.
3. **Writing** (`write`). The writer writes the text from the brief only. Its system prompt is the package's writer prompt, `writing-a-text.md`.
4. **Two checks in parallel** (`check`):
   - A fact check compares the text with the brief. It returns `invented` (claims not in the brief) and `missing` (facts the reader needs).
   - A reviewer checks the text against a catalogue of error patterns. It returns findings with a code, a severity of 1–4 and a location.
5. **Sorting the findings, once:**
   - **A finding that needs a fact the brief lacks** (often M-IDEAL). The agent looks for the fact in the code or asks the user, then adds it to the brief. If there is no new fact, the agent writes "we don't know" into the brief. Either way, it goes back to step 3, once.
   - **Severity 1–2 findings, `invented` and `missing`.** The writer makes one revision (`revise`). Then one more fact check runs (`check --facts-only`). Severity 3–4 findings go into the revision only when the fix is obvious (`revise --max-severity 4`). Anything the revision returns in `unresolved` is a missing fact: handle it as in the point above.
   - **The last fact check finds an invented claim again.** The agent deletes that sentence from `text.md` itself, with no new round.
   - **A second review of the revised text never runs.**
   - **Important texts** (an outage, a price increase, anything legally significant). Run the review twice on the same text, then fix what both reviews found.
6. **Delivery.** In a chat, the agent posts `text.md` as it is. For a file, it copies `text.md` to where the file belongs. A person reads the text. If the text has to change after the checks, it is a new text: edit the brief and run the steps again.

## Scope

Any document written to be read by agents or people: specs, plans, design documents, `docs/` and README files,
AGENTS.md, agent and skill prompts, this catalog.

Not correspondence: chat replies, comments in threads, messages, confirmations, status lines.

## Set up

- The [`text-quality`](../../../text-quality/README.md) part of agentify. Its
  `scripts/talk.py` runs each step as a separate, isolated `claude -p` call: `new`, `check-brief`, `write`,
  `check`, `revise`.
- `claude` (the Claude Code CLI) in PATH, with network access.
- A language package: `ru/` (built on Ilyakhov's books) or `en/` (US Federal Plain Language Guidelines, GOV.UK
  style guide, Strunk). The error codes are shared: M-IDEAL means the same in both.
- Runs are kept in `.text-quality-runs/` at the repository root: add it to the project's `.gitignore`.
- Do not change the packages' prompts by hand: a change goes through the package's test bench (`ru/lab/`,
  `en/lab/`) and its measurement.

## On a document that already exists

The part writes a new text from a brief. To check a text that is already written (an agent prompt, a `LOOP.md`):

1. Write the brief from the document's sources: requirements, decisions, the passages it is built on. Put the
   current text in `text.md` of the run.
2. `check`, then `revise --no-facts` for review findings of severity 1–3, then `check --facts-only`.
3. Sort the fact-check findings yourself: the brief rarely holds every fact the author used on purpose, so some
   `invented` items are fair. Read the whole diff of the revision.

What the revision got wrong when 88 cards of this catalog went through it (2026-11-08): it dropped "about" from
approximate numbers, extended a limit to a case the source did not cover, added a made-up example as a fact,
promised that the sources hold details they do not, and removed a correct source link. The fact recheck caught
most of these; reading the diff caught the rest.

## Notes

- `ru/`: `SKILL.md` reports 3–4 times fewer errors and invented facts. It gives no baseline or sample size for this figure.
- `en/`: the measurement compares the writer prompt `writing-a-text.md` with no prompt (`lab/prompts/baseline.md`). The test used 12 held-out briefs, Sonnet and Haiku as writers, and ran once. Review findings fell from 4.04 to 1.71 per text (−58%), and invented facts from 3.08 to 0.42 per text.
- What remains is mostly M-IDEAL: the text does not say what to do if something goes wrong. The brief closes it,
  not the writer.
- A review → revise loop does not help: in `ru/`, a second round left the same number of findings and added
  invented facts. For `en/` this is still a hypothesis, but the rule is the same.
- The reviewer is noisy. In `ru/`, a second review of the same texts reproduced 57% of the findings at severity 2, 53% at severity 3 and 47% at severity 4.
- The brief check covered 86% of the gaps that review and revision found later (`ru/`).
- Cost in `ru/`: by its own measurements, an estimated $0.36 a text for the whole run, almost all of it the review. The first review in a session, before the cache warms up, cost $1.07 on a trial run.
- Cost in `en/`: the review costs $0.54–0.58 a text and the Sonnet writer $0.01. The cost of the fact check was not recorded, so the source gives no total per text for `en/`.
- Time: the steps that do not wait for answers take an estimated two minutes, one and a half of them for the review.
- Do not ask the writer for markers such as "[to be confirmed]": the reviewer counts the gap anyway. A gap is
  closed by a fact or by "we don't know" in the brief.

## Agent step

The reviewer of the `text-quality` part: it gets the brief and the text and returns findings by its error
catalogue. It is calibrated by that part's own test bench (`ru/lab/`, `en/lab/`), not by the harness; its prompt is
never changed by hand.

## Related

- [knowledge-base-doc-lint](../code/knowledge-base-doc-lint.md): structural checks of `docs/` in CI.
- [agent-code-review](agent-code-review.md): the same idea, a fresh reviewer, for code.
- [interview](../human/interview.md): where the facts for a text's brief come from.

## Sources

- [text-quality part](../../../text-quality/README.md): `README.md`,
  `en/README.md` (process and measurements), `en/review/error-patterns.md` (the error catalogue)

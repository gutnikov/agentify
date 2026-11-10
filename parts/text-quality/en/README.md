# entalk: writing in English

A playbook for agents that write texts in English. It uses plain language as taught by the US Federal Plain Language Guidelines, the GOV.UK style guide and Orwell's six rules. The goal is a text in which a reviewer working from these sources finds as few errors as possible, and which contains no facts that were not in the brief.

entalk is the English counterpart of [rutalk](../ru/README.md). The process, the prompts and the JSON formats are carried over from rutalk. The error catalogue is rebuilt on English sources. **entalk is measured in part**: the writer prompt against no prompt, on dev and once on test. The rest of rutalk's findings are still hypotheses for entalk: see "What is measured".

**The main file is [writing-a-text.md](writing-a-text.md)**, the writer's prompt. Give it to the writing agent as its system prompt. In rutalk this one step gave most of the effect. Whether it does the same in English is the first thing [lab/](lab/README.md) has to test.

## Files

| File | What it is | Process step |
|---|---|---|
| [writing-a-text.md](writing-a-text.md) | Writer prompt: how to write the text | 2. Writing |
| [checking-a-brief.md](checking-a-brief.md) | Brief check prompt: up to 5 questions to the author before writing | 1. Brief check |
| [checking-facts.md](checking-facts.md) | Prompt that compares the finished text with the brief: invented and missing facts | 3. Checks |
| [revising-a-text.md](revising-a-text.md) | Instruction for one revision based on the review findings | 4. Sorting the findings |
| [review/](review/reviewer-prompt.md) | Reviewer: [prompt](review/reviewer-prompt.md), [catalogue of 66 errors](review/error-patterns.md), the scanner `text_scan.py` and the sources in [`sources/`](review/sources/README.md) | 3. Checks |
| [lab/](lab/README.md) | Test bench: 32 briefs and run scripts, for changing the prompts and measuring the effect. Measured in part | — |

## Process

Rules:
- **Ask the author questions before writing**, not after review.
- **Review is one filtering pass**, not a loop of revisions: at most one revision, then a person reads.
- **No review → revise loops.** Do not send a revised text back to review and revise it again.
- **Important texts get two reviews.** For an outage, a price increase or anything legally significant, run the review twice and fix what both reviews found.

```
 Author of the brief
      │  facts, reader, goal
      ▼
 1. Brief check ──── up to 5 questions ────► Author answers
      │  checking-a-brief.md, ~$0.02            ("we don't know" is an answer too)
      ▼                                                   │
 2. Writing ◄─────────────────────────────────────────────┘
      │  writing-a-text.md, Sonnet or Opus medium, ~$0.03
      ▼
 3. Two checks in parallel
      ├─ Fact check against the brief, ~$0.01: checking-facts.md
      └─ Review, one pass, ~$0.30: review/
      ▼
 4. Sorting the findings
      ├─ invented fact ──► remove it or confirm it with the author
      ├─ "no fact" ──────► question to the author → back to step 2
      ├─ severity 1–2 ───► one revision by the writer: revising-a-text.md
      └─ severity 3–4 ───► optional, no second round
      ▼
 5. A person reads and publishes
```

The costs in the diagram are rutalk's. entalk's review costs more: $0.54–0.58 a text written with the prompt, $0.69–0.75 without it (see "What is measured").

### 1. Brief check

- **System prompt:** [checking-a-brief.md](checking-a-brief.md). **Message:** `Brief:` and the text of the brief.
- **Model:** rutalk tested it on Opus medium, about $0.02.
- **Result:** up to 5 questions to the author. Add the answers to the brief. Write "we don't know" or "we don't promise" into the brief as well: the writer will then not invent it.

In rutalk this step closes the main remaining source of errors: gaps in the brief itself. What to do if something goes wrong; vague "about" and "sometimes"; unexplained terms; whom to contact. Do not ask the writer to put markers such as "[to be confirmed]" in the text: the reviewer counts the gap anyway, and the text gets cluttered.

### 2. Writing

- **System prompt:** [writing-a-text.md](writing-a-text.md). **Message:** the brief with the author's answers and the output format (`WRITER_USER` in [lab/lab.py](lab/lab.py)).
- **Model:** Sonnet or Opus medium. In rutalk, Opus xhigh gave the same quality but took 6 times longer and cost 7 times more.

### 3. Checks

**Fact check against the brief.** The reviewer does not see the brief and does not catch invented facts. In rutalk, 0.3–1 invented facts per text remained even with the writer prompt.
- **System prompt:** [checking-facts.md](checking-facts.md). **Message:** `BRIEF:` with the brief, a blank line, `TEXT:` with the finished text.
- **Response:** JSON with the lists `invented` and `missing`; the schema is `CHECK_SCHEMA` in [lab/lab.py](lab/lab.py).
- **Model:** rutalk tested it on Sonnet high.

The check is strict and sometimes flags a fair conclusion drawn from the facts, so a person decides.

**Review.** The reviewer works from the `review/` folder: it reads the catalogue, runs the scanner and opens the sources.

```bash
cd parts/text-quality/en/review
claude -p "Review the text in the file /path/to/text.md. Context: <genre>; reader: <who>; goal: <what they should understand or do>." \
  --model opus \
  --append-system-prompt "$(cat reviewer-prompt.md)" \
  --allowedTools Read "Bash(python3 text_scan.py:*)" \
  --add-dir /path/to
```

In rutalk a call costs about $0.30, and the first call about $0.8 until the cache warms up. A batch of texts is easier to check with `lab/lab.py review`: it passes the catalogue in the system prompt, where it is cached.

### 4. Sorting the findings

- **Invented fact** from the fact check: remove it or confirm it with the author.
- **"No fact"**: a finding that cannot be fixed without a new fact. Most often it is M-IDEAL: "it does not say what to do if…". Send such a finding to the author of the brief as a question, and rewrite the text after the answer.
- **Severity 1–2**: one revision by the writer.
  - **System prompt:** [writing-a-text.md](writing-a-text.md).
  - **Message:** `Brief:` …, `Your text:` …, `An editor reviewed the text and found problems:` with the list of findings, and at the end the text of [revising-a-text.md](revising-a-text.md).
  - **Response:** JSON with the fields `text` and `unresolved`. Whatever lands in `unresolved` becomes questions to the author.
- **Severity 3–4**: optional, if the fix is obvious.

Do not run review and revision in a loop. In rutalk:
- on texts written with the prompt, a second review reproduced only half of the findings;
- a revision round left, within the noise, the same number of findings as a second review without revision, and it added invented facts.

entalk keeps this rule until its own lab shows otherwise. For important texts (an outage, a price increase, anything legally significant), run the review twice and fix what repeats.

### 5. Publishing

A person reads the text.

## What is measured

Lab runs of 2026-11-04 (`lab/runs/`, not in git). The writer is Sonnet or Haiku, effort medium; the reviewer is Opus; the fact check is Sonnet high. "Without a prompt" is [lab/prompts/baseline.md](lab/prompts/baseline.md); "with the prompt" is [writing-a-text.md](writing-a-text.md).

**Held-out briefs (`test`, 12 briefs × 2 writers = 24 texts per variant), measured once:**

| Writer | Review findings per text | Invented facts per text | Texts with no findings |
|---|---|---|---|
| Sonnet | 3.67 → 1.75 (−52%) | 3.08 → 0.50 | 1 → 3 of 12 |
| Haiku | 4.42 → 1.67 (−62%) | 3.08 → 0.33 | 1 → 3 of 12 |
| Both | 4.04 → 1.71 (−58%) | 3.08 → 0.42 | 2 → 6 of 24 |

**Tuning briefs (`dev`, 20 briefs × 2 writers = 40 texts per variant):** findings 3.58 → 1.40 per text (−61%), invented facts 2.05 → 0.47, texts with no findings 3 → 13. The entalk prompt was translated from rutalk's and not tuned on these briefs, so dev is not inflated the way rutalk's dev was.

rutalk's result on its test was −63% for Sonnet and −59% for Haiku: entalk reproduces the effect. What remains on test is mostly M-IDEAL (the text does not say what to do if something goes wrong), as in rutalk, then M-LEVEL and W-VAGUE.

**Cost, measured:** review $0.54–0.58 a text written with the prompt and $0.69–0.75 without it; Sonnet writer $0.01; the fact check's cost was not recorded (rutalk's: $0.01–0.02). That is about twice rutalk's review cost. Why is not known.

**Not measured yet.** These rutalk findings are still hypotheses for entalk:

| Hypothesis from rutalk | rutalk's result | How entalk's lab re-tests it |
|---|---|---|
| **First-line effect.** One line that points the model at a method it already knows does most of the work | One line naming Ilyakhov's books cut review findings by about 70% against no prompt (dev, Sonnet and Haiku) | `prompts/baseline.md` against the one-line `prompts/ref-*.md` variants on dev, Sonnet and Haiku |
| **The rules mostly fight invention** and the errors the writer copies from the brief ("about 12%", an empty CEO quote) | On dev, the one-line variant left 1.90 invented facts per text; the final prompt and its last three drafts left 0.55–0.72 | `prompts/ref-*.md` against [writing-a-text.md](writing-a-text.md) on dev: invented facts per text |
| **A short prompt is not enough** | A 61-word variant (the reference line plus "only facts from the brief") had 1.02 findings per text against 0.70–0.85 for the longer drafts: advice without examples and empty endings came back | A short variant against the full prompt on dev |
| **The brief check catches gaps in advance** | Questions before writing covered 86% of the gaps that review and revision found later | [lab/brief_check.py](lab/brief_check.py) |
| **A review → revise loop does not help** | On Opus xhigh, one revision left 12 findings on 32 texts; a second review of the unrevised texts found 14, within the noise. The revision added 2 invented facts | `lab.py revise`, then `review` and `check`, against a second review of the same texts without revision |
| **Reviewer noise** | On a second review of the same texts, about half the findings reproduced: 57% at severity 2, 53% at 3, 47% at 4 | A second review of the same run (`*-rr` runs) |
| **Reviewer recall** | 97% on Opus, on a test set of 1,141 examples from Ilyakhov's books | Needs a test set built from the before-and-after texts in [`review/sources/plain/examples/`](review/sources/plain/examples/): the "before" texts should get findings under the right codes, the "after" texts few. Not built yet |

Texts for the one-line variants (`ref-*`, `h-ref-*`) are already written in `lab/runs/`; they need review and fact check.

## What the playbook does not solve

- **Gaps in the brief.** What usually remains after the writer prompt is M-IDEAL: the text does not say what to do if something goes wrong. The brief usually has no answer to that, so step 1 closes it, not the writer.
- **Spelling and grammar.** The reviewer does not check them: they are not in the catalogue.
- **Texts in other languages.** For Russian, use rutalk. For other languages the reviewer checks only levels M, T and S.
- **Models not made by Anthropic** have not been tested, in rutalk or here.

## Sources

The catalogue and the reviewer rely on the files in [`review/sources/`](review/sources/README.md):
- the US Federal Plain Language Guidelines and their before-and-after examples, from plainlanguage.gov: public domain in the US, CC0 1.0 worldwide;
- GOV.UK's writing guidelines and A to Z style guide: Open Government Licence v3.0;
- William Strunk Jr., *The Elements of Style* (1918/1920 edition), from Project Gutenberg: public domain.

Copyrighted books (Orwell's "Politics and the English Language", Williams's *Style*, Pinker's *The Sense of Style*, Minto's *The Pyramid Principle*, Zinsser's *On Writing Well*, Fowler's *Modern English Usage*) are cited by name and chapter only, never copied.

# Lab

> **Measured in part (2026-11-04):** the working prompt against no prompt, on dev and once on test, Sonnet and Haiku. The results are in [../README.md](../README.md), "What is measured". `runs/` and `sandbox/` stay local and are not committed to git. rutalk's measurements are in [rutalk's lab](../../ru/lab/README.md) and belong to Russian texts.

The lab is for changing the playbook's prompts and measuring the effect. The writer writes texts from briefs, the reviewer from [../review/](../review/reviewer-prompt.md) reviews them, and a separate agent compares the texts with the briefs. It is a copy of rutalk's lab with English briefs and prompts: the same commands, options and file layout.

## What's here

| Path | What it is |
|---|---|
| `briefs.py` → `briefs.jsonl` | 32 briefs: 20 for tuning (`dev`, `d01`–`d20`) and 12 held out (`test`, `t01`–`t12`). Each has a genre, the brief for the writer, and the context for the reviewer: genre, reader, goal. They are English versions of rutalk's briefs, with the same facts, gaps and traps: vague numbers ("about 12%"), an empty CEO quote, no answer to "what if it fails". Names, currencies and places are adapted |
| `lab.py` | Runs: `write`, `revise`, `review`, `check`, `score` |
| `brief_check.py` | Measures step 1: questions to the author and the share of later gaps they cover |
| `prompts/` | Writer prompt variants: `baseline`, with no style guidance, and one-line variants that add a single reference to a method the model knows: `ref-plain` (Federal Plain Language Guidelines, GOV.UK and Orwell's six rules, the same as the first line of the working prompt), `ref-orwell` (Orwell and Strunk and White), `ref-williams` (Williams's *Style*), `ref-bluf` (answer first, Minto). The working prompt is [../writing-a-text.md](../writing-a-text.md) |
| `runs/<run>/` | Run data: `texts/` (texts), `reviews/` (reviewer reports), `checks/` (fact checks against the brief), `meta/` (model, cost, length), `writer-prompt.md` (the writer prompt the run used) |

## Commands

Run them from this folder. You need `claude` (the Claude Code CLI).

```bash
python3 briefs.py                                         # rebuild briefs.jsonl after editing the briefs

python3 lab.py write  --run r1 --split dev                # writer: ../writing-a-text.md by default, Sonnet, medium
python3 lab.py write  --run r1-h --split dev --model haiku
python3 lab.py write  --run r1-base --split dev --prompt prompts/baseline.md
python3 lab.py write  --run r1-ref --split dev --prompt prompts/ref-plain.md
python3 lab.py review --run r1 --split dev                # reviewer: Opus, catalogue in the system prompt
python3 lab.py check  --run r1 --split dev                # fact check against the brief: Sonnet
python3 lab.py score  --run r1 --split dev --vs r1-base   # summary → runs/r1/score-vs-r1-base.md

python3 lab.py revise --run r1-rev --source r1            # one revision based on review findings, then review and check

python3 brief_check.py ask && python3 brief_check.py judge && python3 brief_check.py report
```

You can stop a run and start it again with the same `--run`: finished texts, reports and checks are skipped (`--force` reruns them).

## How the measurement works

- **The writer is isolated.** It runs with `--safe-mode`, no tools, from the empty folder `sandbox/`. Its system prompt is only the writer prompt; the message is only the brief (`WRITER_USER` in `lab.py`).
- **The reviewer works as in the playbook.** Prompt and catalogue from `../review/`; only `Read` and `python3 text_scan.py` are allowed; the report is JSON.
- **The fact check.** Prompt [../checking-facts.md](../checking-facts.md), model Sonnet high.
- **The main metric** is review findings per text. Secondary metrics: findings weighted by severity, invented facts per text, and texts with no findings.

## Rules

- **Tune the prompt on `dev` and measure the result on `test` once.** Otherwise the edits fit the briefs, and the numbers stop saying anything about other texts. A prompt built from what is left on `dev` looks better on `dev` than it is; the honest estimate is `test`.
- **Measure on at least two models:** Sonnet and Haiku, 40 texts per variant.
- **Reviewer noise.** In rutalk it was ±0.1–0.2 findings per text on 20 texts, and a second review of the same texts reproduced about half the findings. Measure entalk's own noise first, with a second review of one run (`*-rr`). A difference smaller than the noise is not an improvement.
- **Look at systematic leftovers.** These are codes that repeat across models and runs. Study them in the report texts, not by a single number.

## Known artefact

Claude Code sessions receive the user's email. So the writer sometimes signs the text with the company name from its domain, for example "Vivid", although the brief has no name. The writer's real environment will not have this. The fact check does not count such names as invented: see `CHECK_LAB_NOTE` in `lab.py`.

## Runs in `runs/`

The reviewer is Opus in every run; the writer, Sonnet or Haiku, writes with effort medium.

| Run | Writer | Prompt | Briefs | State |
|---|---|---|---|---|
| `baseline`, `h-baseline` | Sonnet, Haiku | `prompts/baseline.md` | dev | reviewed and checked |
| `final`, `h-final` | Sonnet, Haiku | ../writing-a-text.md | dev | reviewed and checked |
| `test-baseline`, `test-h-baseline`, `test-final`, `test-h-final` | Sonnet, Haiku | baseline and the working prompt | test | reviewed and checked |
| `ref-*`, `h-ref-*` | Sonnet, Haiku | `prompts/ref-*.md` | dev | texts only: no review, no check |

To continue the first-line comparison: `python3 lab.py review --run ref-plain --split dev`, then `check`, for each `ref-*` and `h-ref-*` run, then `score --vs baseline`.

To re-test rutalk's hypotheses (listed in [../README.md](../README.md), "Status: not measured"), use rutalk's run names. `brief_check.py` looks for the gaps in these runs:

| Run | Writer | Prompt | Briefs |
|---|---|---|---|
| `baseline`, `h-baseline` | Sonnet, Haiku | `prompts/baseline.md` | dev |
| `ref-plain`, `h-ref-plain` (and the other `ref-*`) | Sonnet, Haiku | `prompts/ref-*.md` | dev |
| `final`, `h-final` | Sonnet, Haiku | ../writing-a-text.md | dev |
| `test-baseline`, `test-h-baseline`, `test-final`, `test-h-final` | Sonnet, Haiku | baseline and the working prompt | test |
| `o-baseline`, `o-final` | Opus, effort medium | baseline and the working prompt | all 32 |
| `ox-baseline`, `ox-final` | Opus, effort xhigh | baseline and the working prompt | all 32 |
| `ox-rev1` | Opus xhigh | one revision of `ox-final` based on review findings, then a fresh review of all 32 | all 32 |
| `*-rr` | — | a second review of the same texts: control for reviewer noise | — |
| `brief-check` | Opus medium | questions to the author (`*.q.json`) and gap coverage (`*.j.json`) | all 32 |

**Prompt variants on `dev`, Sonnet and Haiku, 40 texts each:**

| Variant | Words | Findings per text | Invented per text |
|---|---|---|---|
| baseline | 8 | 3.58 | 2.05 |
| ref-plain | 29 | not measured | not measured |
| ref-orwell | 29 | not measured | not measured |
| ref-williams | 21 | not measured | not measured |
| ref-bluf | 24 | not measured | not measured |
| writing-a-text.md | ~300 | 1.40 | 0.47 |

## Cost, measured on 2026-11-04

- **Review:** $0.54–0.58 a text written with the working prompt, $0.69–0.75 without a prompt (longer texts, more findings). The first call of a run, without a warm cache, about $1.4. About twice rutalk's review cost; why is not known.
- **Writer:** Sonnet $0.01 a text, Haiku under $0.01.
- **Fact check:** not recorded (rutalk: $0.01–0.02).
- **The whole measurement** (12 dev runs written, 4 dev and 4 test runs reviewed and checked): $82.

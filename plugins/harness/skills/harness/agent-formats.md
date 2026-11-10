# Agent formats

Agents that are steps of loops talk to each other and to scripts through these formats, and through nothing else.
They are the only part of an agent the harness fixes in advance: an agent's prompt, checklist and tools are
designed for its loop, but what it returns is one of the shapes below, so a finding verifier can check any
reviewer's findings and `loops.py eval-score` can score any agent.

Each format is one JSON object; a list of them is JSON Lines (one object per line).

## Finding

What a reviewer, a guard or an explorer reports. One finding per object.

```json
{"id": "F1", "file": "api/billing.go", "line": 142, "severity": "high", "rule": "credits-reserved",
 "message": "Two requests pass the balance check before either is charged.",
 "evidence": "billing.go:131 reads the balance; billing.go:142 charges after the render returns."}
```

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | unique within one run |
| `file`, `line` | when the finding is in code | where to look; `line` may be omitted for a whole file |
| `severity` | yes | `high` (blocks), `medium`, `low` |
| `rule` | yes | the checklist item, lens or requirement it breaks |
| `message` | yes | what is wrong, in one sentence |
| `evidence` | yes | what shows it: code lines, a command and its output, a screenshot path |

## Finding check

What a finding verifier returns for one finding it was given.

```json
{"finding": "F1", "status": "CONFIRMED", "evidence": "Ran the two requests in parallel: both returned 202."}
```

`status`: `CONFIRMED` (shown true), `PLAUSIBLE` (consistent with the code, not shown), `REFUTED` (shown false).

## Verdict

What a refuter, a guard or a judge returns about one claim or artifact, and what a gate prints.

```json
{"verdict": "fail", "reasons": ["The export button downloads 0 rows when the table is filtered."],
 "evidence": ["probe screenshot: test-results/probe.png", "GET /api/export?filter=… returned []"]}
```

| Field | Meaning |
|---|---|
| `verdict` | `pass` or `fail`; a judge may add `"score"` per criterion of its rubric |
| `reasons` | why, one sentence each; empty when `pass` |
| `evidence` | what was run or looked at |

A loop that runs an agent maps the verdict to its exit code: `pass` → 0, `fail` → 1. A loop whose agent is not
`gate` in `loops/agents.yaml` prints the verdict and exits 0: an agent that is not calibrated advises, it does
not block.

## Diagnosis

What an investigator returns. It never blocks.

```json
{"cause": "The migration runs after the app starts on the preview.", "evidence": ["deploy log line 88: …"],
 "next": "Run migrations in the release step before the app's health check."}
```

## Evals

`loops/agents/<agent-id>/evals/<case>/` holds what the agent gets (its `input/`, in the shape its loop gives it)
and `expected.json`:

```json
{"verdict": "fail"}
```

or, for an agent that reports findings:

```json
{"findings": [{"file": "api/billing.go", "line": 142, "rule": "credits-reserved"}]}
```

`{"findings": []}` is a must-pass case: the agent must report nothing of severity `high`.

Each run of the whole eval set is one file, `loops/agents/<agent-id>/results/<run>.jsonl`, one line per case:

```json
{"case": "parallel-charge", "verdict": "fail", "findings": [{"id": "F1", "file": "api/billing.go", "line": 140, "severity": "high", "rule": "credits-reserved", "message": "…", "evidence": "…"}]}
```

A run matches a case when the verdicts are equal, or when every expected finding has a reported finding in the
same file, within 3 lines, with the expected `rule` if one is given, and a must-pass case has no `high` finding.

## Outcome

What happened to one verdict in real use, appended to `loops/agent-outcomes.jsonl` by `loops.py outcome`:

```json
{"at": "2026-11-10T12:04:11", "agent": "code-reviewer", "loop": "review", "outcome": "false-positive",
 "note": "F3: the null check is two lines above"}
```

`outcome`: `confirmed`, `false-positive` (it fired and was wrong), `missed` (a failure it should have caught got
through), `overridden` (a person decided against it).

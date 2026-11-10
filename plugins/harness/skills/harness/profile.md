# The project profile

Setup ends with a map of the project's super-loops and a short list of loops for its pains. To draw them you need six
facts about the project. The repository shows most of them; you ask about the rest in one form. Facts and answers go
into `loops/profile.yaml`, so nobody is asked twice.

| Fact | Field in the profile | Usually |
|---|---|---|
| The stack: languages, the build, test and lint commands | `stack` | found |
| What the project ships: web, API, mobile… | `kind` | found, sometimes asked |
| Where a change goes after the agent: CI, preview, staging, production | `stages` | partly found, asked |
| What the agent itself can reach: CI logs, logs, error tracking, metrics, a browser | `tools` | partly found, asked |
| How work goes through the project now: where it comes from, where a change ends, which checks stand at which place | `super_loops`, `not_here`, `ends_at`, `existing_checks` | found |
| Which failures the loops must catch first, and the place that should catch each | `pains` | asked |

A place is a super-loop and one of its phases, such as `delivery/confirmation` (`$S/super-loops/README.md`).

## 1. Find out first

| Fact | Where to look |
|---|---|
| Stack | Manifests (`package.json`, `go.mod`, `pyproject.toml`, `Cargo.toml`, `build.gradle`, `Package.swift`…), `Makefile`, `justfile`, the manifest's scripts, CLAUDE.md, AGENTS.md, the CI jobs |
| Kind | Frameworks in the dependencies: React, Next, Vue → `web`; an HTTP or gRPC server, OpenAPI, proto → `api`; `ios/`, `android/`, Swift, Kotlin, Flutter, React Native → `mobile`; a published package or a `bin` entry → `library`; an LLM SDK in product code → `llm` |
| Stages | CI configs (`.github/workflows/`, `.gitlab-ci.yml`…), deploy jobs and their environments, preview jobs (review apps, Vercel, Netlify), Helm charts, Terraform |
| Tools | The MCP servers of this session, CLIs that are installed and logged in (`gh auth status`, `glab auth status`, `kubectl config current-context`), Playwright or Cypress in the dependencies |
| Existing checks | CI jobs, `.claude/settings.json` hooks, git hooks, pre-commit, linter configs. Write each as `"<name>: <places> — <where it runs, what it does>"`: a lint in CI is `"golangci-lint: delivery/work remediation/work maintenance/work — CI job lint"`; a smoke test after a deploy stands at `delivery/release` and the same phase of the others |
| Super-loops | Where work comes from: the issue tracker and its labels (`gh issue list`, `glab issue list`), the error tracker, dependency bots (`.github/dependabot.yml`, `renovate.json`), scheduled CI jobs. Discovery only where there are prototypes, spikes or decision records (`prototypes/`, `docs/decisions/`) |
| Where a change ends | The deploy jobs and who starts them; what runs after a deploy (smoke tests, a canary analysis, a log query); who looks at production afterwards; where the deploy records its results, which goes into `trace` |
| Pains | Reverts and fix-up commits in `git log`, red CI runs (`gh run list --status failure`, `glab ci list --status failed`), review comments that repeat, rollbacks in the deploy history |

A tool counts only if the agent can use it from this session: call it once (`gh run list -L 1`, one MCP query). An
SDK in the code means the project sends data there, not that the agent can read it.

## 2. Ask what is left, in one form

Ask only the questions that finding out did not settle. Put them all in one call of the session's question tool;
it takes up to 4 questions. This form is the one exception to "one question at a time": the answers do not depend
on each other and you need them together.

- The user may see only the form. So each question starts with what you found: "Found: `.gitlab-ci.yml` with the
  jobs test and deploy-staging."
- What you found is the first option, marked "(found)".
- Every question is multi-select.
- The stack is not a question when the repository shows it. Write it at the start of the first question ("Stack:
  Go 1.23, `make test`, golangci-lint"), so the user can correct it in a free answer. Ask about it only when the
  repository is empty, or when it is a monorepo and it is unclear which part the loops are for.
- If the user already said what the loops must catch, that is the answer to Q4: do not ask it.

Log each question as its own call: Q1–Q3 under H1, Q4 under H4.

### Q1. What the project ships — header `Project`

"What does this project ship? Found: <…>."

Offer the 4 options closest to what you found:

| Option | `kind` |
|---|---|
| Web frontend | `web` |
| Backend service or API | `api` |
| Mobile app | `mobile` |
| Library or CLI | `library` |
| Data pipeline or batch jobs | `data` |
| LLM feature in the product | `llm` |
| Infrastructure as code | `infra` |

### Q2. Where a change goes — header `Dev flow`

"Where does a change go after the agent writes it? Found: <…>. Local runs and git hooks are always there; if
there is nothing else, answer 'local only'."

| Option | What it means | `stages` |
|---|---|---|
| CI on every PR | Checks run on clean machines before the merge | `ci`, `scheduled` |
| Preview per PR | Each PR gets its own deployed environment | `preview` |
| Shared staging | A common test stand the team deploys to | `staging` |
| Production | We deploy it and can see how it behaves | `production` |

For a mobile app, an internal track (TestFlight, Firebase App Distribution) is staging, and a store release is
production.

### Q3. What the agent can reach — header `Tools`

"Which of these can the agent use from this session, through a CLI, MCP or API? It is not enough that the company
has it. Checked and working: <…>."

Offer only what you could not check yourself, the 4 that matter most for the kind and the stages: no browser for an
API without a UI. When a loop is about to rely on a tool the user named, call the tool once; if it fails, that is
an H3 call.

| Option | `tools` key | For example |
|---|---|---|
| CI status and logs | `ci` | `gh`, `glab`, a CI MCP server |
| Logs | `logs` | Elasticsearch, Loki, Datadog, CloudWatch |
| Error tracking | `errors` | Sentry, Bugsnag, Crashlytics |
| Metrics or traces | `metrics`, `traces` | Prometheus, Grafana, an OpenTelemetry backend |
| A browser or a simulator | `browser` | Playwright, Chrome DevTools MCP, iOS Simulator, `adb` |
| Deploys to a stand | `deploy` | `kubectl`, `helm`, the Vercel CLI, a CI job the agent can start |

### Q4. What to catch first — header `Catch first`

"What should the loops catch first? In the history: <e.g. 6 of the last 30 pipelines failed on lint; 2 reverts of
migrations>."

Offer the 4 options the history supports best:

| Option | `pains` | The place that should catch it |
|---|---|---|
| The agent's changes break the build or the tests | `breaks-build` | `delivery/work` |
| Tests pass, but the feature does not work for real | `not-really-working` | `delivery/work` |
| The code ignores our conventions or architecture | `conventions` | `delivery/work` |
| Bugs reach staging or production | `escapes` | `delivery/confirmation` |
| Dependencies and the runtime fall behind, and updating them breaks things | `aging` | `maintenance/gate` |
| Vulnerabilities, secrets, licenses | `security` | `delivery/work` |
| It gets slower or heavier | `performance` | `delivery/work` |
| It breaks clients: the API, a schema, migrations | `compatibility` | `delivery/work` |

Write each pain as `"<pain>: <place> — <evidence>"`, such as `"escapes: delivery/confirmation — 2 of the last 10
releases rolled back"`. A free answer goes into `pains` in the user's words, with the place you would put its loop
at.

## 3. The profile file

`loops.py init` creates `loops/profile.yaml` from `$S/defaults/profile.yaml`; the comments there describe each
field. Fill it in after the form, and commit it with the setup. Write the facts of the map as you find them: every
existing check with its places, every pain with the place that should catch it.

Keep it current. When the project changes (a new CI job or stand, a tool connected or lost, a pain fixed), update
the file from what you see; do not ask again. Then check which loops the change allows or makes useless.

## 4. From the profile to the map and the loops

1. **Draw the map**: `python3 $S/scripts/loops.py map`. One line per super-loop the project has, with its phases:
   `✓` and what stands at a place (a check from `existing_checks`, or a loop whose `places` name it), `✗` where
   nothing does, `!` and the pain at the place of a pain. Above the lines, where a change ends now (`ends_at`); below
   them, the super-loops in `not_here` with their reasons. A `✗` is not a reason to build a loop. It shows where a
   loop would go, and what "done" means today: where nothing confirms a change, a person decides, or nobody does.
2. **Start from the pains.** Each pain has a place, and the table below names its candidates.
   `python3 $S/scripts/loops.py candidates <place>` lists every loop type that can stand at a place, each with
   whether the project can run it: its `stages` against the profile's, its `needs` against the profile's `tools`. A
   loop type that answers no pain is not a candidate.
3. **Drop what the project cannot run**:
   - a loop type whose `stages` in `loop-types/index.yaml` are all missing from the profile's `stages` (`edit`,
     `local`, `commit`, `task` and `continuous` are always there);
   - a loop type that needs a tool missing from `tools`;
   - a loop type that does not fit the `kind`.
4. **Drop what already works.** A check at the pain's place, a `✓` on the map, is not a new loop. If the agent cannot
   run that check or read its output, the loop wires in the existing command; it does not replace it.
5. **One loop per pain, at the earliest phase that can catch it**: the cheapest loop that catches the failure. That
   is the one closest to where the failure happens, the fastest, and deterministic. When two fit, take the one
   earlier in "Where to start" (`loop-types/README.md`). One loop often stands at the same phase of several
   super-loops: a `verify` loop is the work of delivery, remediation and maintenance alike.
6. **Propose**: usually 1–3 loops, never more than 5.

| Pain | Place | Candidates, the usual first one first | Needs |
|---|---|---|---|
| `breaks-build` | `delivery/work`, and the same phase of remediation and maintenance | One `verify` loop: the project's build, type check, lint and tests behind one `run`, wired into the Stop hook (`stop-hook`). Then `pre-commit-pre-push`, `ci-clean-infra` | `ci` for the last |
| `not-really-working` | `delivery/work`, then `delivery/gate` and `delivery/confirmation` | web: `e2e-browser`, `visual-screenshot-check`; api: `integration-tests-emulators`, `agentic-manual-testing` with `curl`; mobile: `agentic-manual-testing` on a simulator. Then `acceptance-loop` when requirements come as tickets or texts, `verification-subagent`, and `release-confirmation` once there is production | `browser` for web and mobile; `production` and `logs` for the confirmation |
| `conventions` | `delivery/work` | `lint-with-fix-instructions`, `taste-invariants`, `architecture-fitness-functions`; `agent-code-review` only for what no lint can express | — |
| `escapes` | `delivery/confirmation`; remediation from its `entry` for what still gets through | `release-confirmation`, built on `health-checks-smoke`, `structured-logs` and `canary-feature-flags` where they exist; then `error-tracking`, and `bug-failing-test-fix` with the `reproduction-gate` | `staging` or `production`; `logs`, `errors` |
| `aging` | `maintenance/entry`, `maintenance/gate` | `dependency-updates` with `behaviour-invariance`; `dependency-scanning-sbom` | `ci` |
| `security` | `delivery/work`; `maintenance/entry` for vulnerabilities in old dependencies | `secret-scanning`, `dependency-scanning-sbom`, `sast`, `license-check` | `ci` for all but secrets |
| `performance` | `delivery/work`, `delivery/release`; `maintenance/confirmation` | web: `bundle-size-budget`, `lighthouse-ci`; others: `benchmarks-vs-baseline`, `perf-budgets-telemetry`, `load-testing` | `preview` for Lighthouse, `staging` for load tests, `metrics` for budgets |
| `compatibility` | `delivery/work`; `maintenance/gate` | `api-breaking-changes`, `db-migration-lint`, `contract-tests`, `platform-matrix` | `ci` |

What the `kind` adds to the candidates, and what it rules out:

| `kind` | Fits | Rules out |
|---|---|---|
| `web` | browser loops, `accessibility-checks`, `bundle-size-budget`, `i18n-pseudolocalization` if the app is translated | — |
| `api` | `integration-tests-emulators`, `api-breaking-changes` for a published schema (OpenAPI, proto), `db-migration-lint` when there are migrations, `structured-logs` | browser, visual and accessibility loops |
| `mobile` | runs on a simulator, snapshot tests (`approved-fixtures`), `platform-matrix` over OS versions | `lighthouse-ci` |
| `library` | `api-breaking-changes` for the public API, `property-based-tests`, `approved-fixtures` for CLI output, `executable-docs`, `platform-matrix` | stand and production loops |
| `data` | `approved-fixtures` on sample data, `property-based-tests`, `config-validation` | browser loops |
| `llm` | `llm-evals` before any other inferential loop; `ai-judges-telemetry` once there is production | — |
| `infra` | `config-validation`, `sast` with IaC rules | browser loops |

### The proposal

Show the profile in one line and where a change ends, then the map, the loops as a table with their places, the gaps
that stay open and what they mean, and a short "not now" list: the loop types the user might expect, each with the
reason it is left out. Then ask which loops to build (H4), with the proposed set as the first option.

```
Profile: api (Go) · ci, staging, production · tools: ci (glab), logs (Elasticsearch MCP)
Ends at: production, by the deploy job; nothing confirms it after the deploy
Catch first: breaks-build (delivery/work), escapes (delivery/confirmation)

delivery     entry ✓ Jira · oracle ✗ · work ✓ make test · gate ✗ · release ✓ deploy job · confirmation ✗
remediation  entry ✗ · oracle ✗ · work ✓ make test · gate ✗ · release ✓ deploy job · confirmation ✗
maintenance  entry ✓ Renovate · oracle ✗ · work ✓ make test · gate ✗ · release ✓ deploy job · confirmation ✗
not here     discovery: every idea the product team brings gets built

| # | Loop                 | Place                                             | Catches                                 | Runs                 | Builds on                       |
|---|----------------------|---------------------------------------------------|-----------------------------------------|----------------------|---------------------------------|
| 1 | verify               | delivery, remediation, maintenance / work         | build and test failures before turn end | Stop hook, ~40 s     | make build, make test (exist)   |
| 2 | release-confirmation | delivery, remediation, maintenance / confirmation | a release that breaks production        | after deploy, 20 min | Elasticsearch, /health (exists) |

Open gaps: no gate in any super-loop, so "done" rests on the tests the agent wrote; remediation starts only when a
person notices.

Not now:
- error-tracking: no error tracker the agent can reach
- acceptance-loop: the tickets are one line long; there is no spec to derive tests from yet
- e2e-browser: the project has no UI
```

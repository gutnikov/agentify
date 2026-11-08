# The project profile

Setup ends with a short list of loops that fit the project. To choose them you need five facts about it. The
repository shows most of them; you ask about the rest in one form. Facts and answers go into `loops/profile.yaml`,
so nobody is asked twice.

| Fact | Field in the profile | Usually |
|---|---|---|
| The stack: languages, the build, test and lint commands | `stack` | found |
| What the project ships: web, API, mobile… | `kind` | found, sometimes asked |
| Where a change goes after the agent: CI, preview, staging, production | `stages` | partly found, asked |
| What the agent itself can reach: CI logs, logs, error tracking, metrics, a browser | `tools` | partly found, asked |
| Which failures the loops must catch first | `pains` | asked |

## 1. Find out first

| Fact | Where to look |
|---|---|
| Stack | Manifests (`package.json`, `go.mod`, `pyproject.toml`, `Cargo.toml`, `build.gradle`, `Package.swift`…), `Makefile`, `justfile`, the manifest's scripts, CLAUDE.md, AGENTS.md, the CI jobs |
| Kind | Frameworks in the dependencies: React, Next, Vue → `web`; an HTTP or gRPC server, OpenAPI, proto → `api`; `ios/`, `android/`, Swift, Kotlin, Flutter, React Native → `mobile`; a published package or a `bin` entry → `library`; an LLM SDK in product code → `llm` |
| Stages | CI configs (`.github/workflows/`, `.gitlab-ci.yml`…), deploy jobs and their environments, preview jobs (review apps, Vercel, Netlify), Helm charts, Terraform |
| Tools | The MCP servers of this session, CLIs that are installed and logged in (`gh auth status`, `glab auth status`, `kubectl config current-context`), Playwright or Cypress in the dependencies |
| Existing checks | CI jobs, `.claude/settings.json` hooks, git hooks, pre-commit, linter configs |
| Pains | Reverts and fix-up commits in `git log`, red CI runs (`gh run list --status failure`, `glab ci list --status failed`), review comments that repeat |

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

| Option | `pains` |
|---|---|
| The agent's changes break the build or the tests | `breaks-build` |
| Tests pass, but the feature does not work for real | `not-really-working` |
| The code ignores our conventions or architecture | `conventions` |
| Bugs reach staging or production | `escapes` |
| Vulnerabilities, secrets, licenses | `security` |
| It gets slower or heavier | `performance` |
| It breaks clients: the API, a schema, migrations | `compatibility` |

A free answer goes into `pains` in the user's words.

## 3. The profile file

`loops.py init` creates `loops/profile.yaml` from `$S/defaults/profile.yaml`; the comments there describe each
field. Fill it in after the form, and commit it with the setup.

Keep it current. When the project changes (a new CI job or stand, a tool connected or lost, a pain fixed), update
the file from what you see; do not ask again. Then check which loops the change allows or makes useless.

## 4. From the profile to loops

1. **Start from the pains.** Each pain names its candidate loop types in the table below. A loop type that answers
   no pain is not a candidate.
2. **Drop what the project cannot run**:
   - a loop type whose `stages` in `loop-types/index.yaml` are all missing from the profile's `stages` (`edit`,
     `local`, `commit`, `task` and `continuous` are always there);
   - a loop type that needs a tool missing from `tools`;
   - a loop type that does not fit the `kind`.
3. **Drop what already works.** A check the project already runs is not a new loop. If the agent cannot run that
   check or read its output, the loop wires in the existing command; it does not replace it.
4. **One loop per pain**: the cheapest one that catches the failure. That is the one closest to where the failure
   happens, the fastest, and deterministic. When two fit, take the one earlier in "Where to start"
   (`loop-types/README.md`).
5. **Propose**: usually 1–3 loops, never more than 5.

| Pain | Candidates, the usual first one first | Needs |
|---|---|---|
| `breaks-build` | One `verify` loop: the project's build, type check, lint and tests behind one `run`, wired into the Stop hook (`stop-hook`). Then `pre-commit-pre-push`, `ci-clean-infra` | `ci` for the last |
| `not-really-working` | web: `e2e-browser`, `visual-screenshot-check`; api: `integration-tests-emulators`, `agentic-manual-testing` with `curl`; mobile: `agentic-manual-testing` on a simulator. Then `verification-subagent`, and `health-checks-smoke` once there is a stand | `browser` for web and mobile; `preview` or `staging` for smoke tests |
| `conventions` | `lint-with-fix-instructions`, `taste-invariants`, `architecture-fitness-functions`; `agent-code-review` only for what no lint can express | — |
| `escapes` | `bug-failing-test-fix`, `health-checks-smoke`, `error-tracking`, `structured-logs`, `canary-feature-flags` | `staging` or `production`; `errors`, `logs` |
| `security` | `secret-scanning`, `dependency-scanning-sbom`, `sast`, `license-check` | `ci` for all but secrets |
| `performance` | web: `bundle-size-budget`, `lighthouse-ci`; others: `benchmarks-vs-baseline`, `perf-budgets-telemetry`, `load-testing` | `preview` for Lighthouse, `staging` for load tests, `metrics` for budgets |
| `compatibility` | `api-breaking-changes`, `db-migration-lint`, `contract-tests`, `platform-matrix` | `ci` |

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

Show the profile in one line, the loops as a table, and a short "not now" list: the loop types the user might
expect, each with the reason it is left out. Then ask which loops to build (H4), with the proposed set as the first
option.

```
Profile: api (Go) · local, ci, staging · tools: ci (glab), logs (Elasticsearch MCP)
Catch first: breaks-build, escapes

| # | Loop          | Catches                                   | Runs                         | Builds on                          |
|---|---------------|-------------------------------------------|------------------------------|------------------------------------|
| 1 | verify        | build and test failures before turn end   | Stop hook, ~40 s             | make build, make test (exist)      |
| 2 | smoke-staging | a deploy that does not start              | after deploy to staging, 2 m | /health (exists), Elasticsearch    |

Not now:
- error-tracking: no error tracker the agent can reach
- canary-feature-flags: the agent cannot see production
- e2e-browser: the project has no UI
```

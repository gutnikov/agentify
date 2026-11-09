# Loop types

A coding agent becomes autonomous when every action it takes has a check that the agent runs itself and that
returns an unambiguous, machine-readable signal: an exit code, `file:line:message`, JSON, a screenshot, or the
answer to a log query. Almost every quality attribute (the "-ilities") can be turned into such a sensor, not just
testability and observability. This approach is now called harness engineering.

This catalog has one file per loop type: a pattern the harness engineer turns into a concrete loop in a project.

- 72 automated loop types in 11 groups. 71 come from the research "Циклы обратной связи для автономного
  coding-агента: каталог по атрибутам качества" (in Russian; it says 70 cycles but lists 71). One,
  [review of document texts](meta/document-review.md), is built on the `spec` skill.
- 16 [human-in-the-loop loop types](human/README.md), where a person gives the signal.

## File format

```yaml
---
id: red-green-tdd            # the file name; stable, used to refer to the loop
title: "Unit tests, red/green TDD"
group: testing               # the folder
qualities: [testability, correctness]
stages: [local]              # where the loop runs; omitted when the research does not say
speed: [seconds]             # how long one round takes; omitted when the research does not say
---
```

The body has the sections **Loop** (what the agent does and what signal it gets), **Set up** (what has to exist
for the loop to work), **Notes** (evidence and warnings, when there are any) and **Sources**.

| `stages` value | Meaning |
|---|---|
| `edit` | After every file edit (a hook, the language server) |
| `local` | The agent runs it in its own workspace |
| `commit` | Pre-commit or pre-push hook |
| `ci` | CI on clean infrastructure |
| `preview` | A per-PR preview environment |
| `staging` | Staging |
| `production` | Production |
| `scheduled` | On a schedule: nightly, periodically, in batches |
| `task` | At the start or end of every task or session |
| `sprint` | Once per sprint |
| `continuous` | All the time |

`speed`: `sub-second`, `seconds`, `minutes`, `hours`, `days`, `weeks`.

Human-in-the-loop loop types replace `qualities` with four axes and use slightly different sections; see
[human/README.md](human/README.md#file-format).

[index.yaml](index.yaml) lists every loop type with its path, a one-line summary (from its Loop) and its frontmatter, so
a tool or an agent can choose loop types without opening each card. It is generated: after changing a card, run
`python3 ../scripts/catalog.py index`; `python3 ../scripts/catalog.py check` validates every card and fails when
the index is out of date.

## Terms

From Birgitta Böckeler (Thoughtworks), "Harness engineering for coding agent users":

- **Guides** act before the agent acts: AGENTS.md, skills, LSP.
- **Sensors** give feedback after it acts: tests, linters, logs, the browser, reviewer agents. Every loop in
  this catalog is a sensor.
- Both are either **computational** (deterministic, seconds) or **inferential** (LLM-as-judge: more expensive and
  non-deterministic).
- With sensors only, the agent repeats the same mistakes. With guides only, it never learns whether the rules
  worked.

Behaviour is the hardest to check: tests the agent wrote itself are not enough. Independent behaviour checks are
the most valuable: [mutation testing](testing/mutation-testing.md),
[property-based tests](testing/property-based-tests.md), [approved fixtures](testing/approved-fixtures.md),
[e2e](testing/e2e-browser.md), a separate [verification agent](meta/verification-subagent.md).

## What makes a loop fit for an agent

1. **One known command.** It is written in CLAUDE.md or AGENTS.md, or described in `--help`. A CLI costs less
   context than a GUI.
2. **Speed fits its place in the process.** Seconds for every edit, minutes in CI, hours on a schedule. "Keep
   quality left" (Böckeler).
3. **Determinism.** A flaky sensor teaches the agent to ignore the signal.
4. **Machine-readable, compact output.** An exit code, `file:line:message`, JSON or SARIF.
5. **A fix instruction in the error message.** Where a rule had none, Böckeler saw the agent raise the
   complexity threshold instead.
6. **Protection from bypass.** The agent may disable or delete tests (Kent Beck: "any indication that the genie
   was cheating"). Sensors the agent can edit need protection; the final ones must be out of its reach: CI,
   mutations, production.
7. **Isolation.** A sandbox lets the agent run without confirming each action.
8. **Enforced by hooks, not by the prompt.** CLAUDE.md is advice; hooks are deterministic.

## Where to start

The order below is for a project that has none of these loops. Do not build every step: choose by the project's
profile and the failures it has ([../profile.md](../profile.md)).

1. **`verify` in one command**: [build](code/build.md), [types](code/type-check.md),
   [lint](code/lint-with-fix-instructions.md) and [unit tests](testing/red-green-tdd.md), plus the
   [formatting hook](code/autoformat-hook.md) and the [Stop hook](delivery/stop-hook.md). Boris Cherny: "give
   Claude a way to verify its work. If Claude has that feedback loop, it will 2-3x the quality of the final
   result".
2. **Behaviour**: [red/green TDD](testing/red-green-tdd.md) with protected tests,
   [mutations on the diff](testing/mutation-testing.md), [property-based tests](testing/property-based-tests.md).
3. **The agent sees the app**: [an app per worktree](delivery/isolated-environment.md),
   [Playwright](testing/e2e-browser.md) with [screenshots](testing/visual-screenshot-check.md),
   [axe](interaction/accessibility-checks.md), `init.sh`.
4. **Observability in dev**: [structured logs](observability/structured-logs.md),
   [OTel](observability/traces-opentelemetry.md), an ephemeral telemetry stack,
   [performance budgets](performance/perf-budgets-telemetry.md).
5. **CI gates**: [fitness functions](code/architecture-fitness-functions.md), [Semgrep](security/sast.md),
   [GitLeaks](security/secret-scanning.md), [SCA](security/dependency-scanning-sbom.md) and
   [licenses](security/license-check.md), [oasdiff or buf](compatibility/api-breaking-changes.md),
   [Squawk or Atlas](compatibility/db-migration-lint.md), [size-limit](performance/bundle-size-budget.md) or
   [Lighthouse](performance/lighthouse-ci.md), [Pact](testing/contract-tests.md). A
   [limited number of CI rounds](delivery/ci-clean-infra.md).
6. **Production and the inferential layer**: [Sentry MCP](production/error-tracking.md),
   [SLOs](production/slo-degradation.md), [canaries](delivery/canary-feature-flags.md),
   [reviewer agents](meta/agent-code-review.md), [garbage collection](meta/garbage-collection.md),
   [evals](meta/llm-evals.md). A [UX evaluator](interaction/ux-evaluator.md) only where a single model cannot
   do the job reliably.
7. **Always: the [steering loop](meta/steering-loop.md).** Turn a repeated mistake into code (a lint or a test)
   rather than into text.

## Caveats

- The OpenAI and Stripe numbers are the companies' own reports. OpenAI writes that the result "depends heavily
  on the specific structure and tooling of this repository".
- A harness that checks behaviour is not solved yet. No sensor can check correctness if a person has not
  specified what they want.
- Too many rules can drive the agent into a "spiral of over-engineered refactorings" (Böckeler).
- Inferential sensors are expensive and non-deterministic; run them selectively.
- Production data is untrusted input. `browser_run_code_unsafe` in Playwright MCP is effectively remote code
  execution.
- The ISO/IEC 25010:2023 sub-characteristics were checked against secondary sources only (the standard is paid).
  Some tools (k6, Trivy, ZAP, cargo-fuzz) reflect common practice and were not checked separately.

## Catalog

### Code correctness and maintainability (static, seconds) — `code/`

- [Build / compile](code/build.md)
- [Type checking](code/type-check.md)
- [LSP diagnostics after every edit](code/lsp-diagnostics.md)
- [Linter with fix instructions](code/lint-with-fix-instructions.md)
- [Auto-formatting hook](code/autoformat-hook.md)
- [Architecture fitness functions](code/architecture-fitness-functions.md)
- [Taste invariants: custom lints](code/taste-invariants.md)
- [Coupling analysis](code/coupling-analysis.md)
- [Doc linters for the knowledge base](code/knowledge-base-doc-lint.md)

### Testability and functional correctness — `testing/`

- [Unit tests, red/green TDD](testing/red-green-tdd.md)
- [Run the tests first](testing/run-tests-first.md)
- [Integration tests with emulators](testing/integration-tests-emulators.md)
- [Contract tests](testing/contract-tests.md)
- [Property-based tests](testing/property-based-tests.md)
- [Mutation testing](testing/mutation-testing.md)
- [Code coverage](testing/code-coverage.md)
- [Snapshot / golden / approved fixtures](testing/approved-fixtures.md)
- [Fuzzing](testing/fuzzing.md)
- [E2E through browser automation](testing/e2e-browser.md)
- [Visual check with screenshots](testing/visual-screenshot-check.md)
- [Agentic manual testing](testing/agentic-manual-testing.md)
- [Executable documentation](testing/executable-docs.md)
- [Bug → failing test → fix](testing/bug-failing-test-fix.md)

### Security, compliance, audit — `security/`

- [SAST](security/sast.md)
- [Secret scanning](security/secret-scanning.md)
- [Dependency analysis (SCA) and SBOM](security/dependency-scanning-sbom.md)
- [License check](security/license-check.md)
- [DAST](security/dast.md)
- [Security and data-handling review by an agent](security/security-review-agent.md)
- [Compliance hardening with mutants](security/compliance-mutants.md)
- [Audit trail of agent actions](security/agent-audit-trail.md)

### Compatibility, integrability, flexibility — `compatibility/`

- [Breaking changes in the API](compatibility/api-breaking-changes.md)
- [Lint and run database migrations](compatibility/db-migration-lint.md)
- [Dependency updates](compatibility/dependency-updates.md)
- [Platform matrix](compatibility/platform-matrix.md)
- [Configuration check](compatibility/config-validation.md)
- [i18n and pseudo-localization](compatibility/i18n-pseudolocalization.md)

### Performance and scalability — `performance/`

- [Benchmarks against a baseline](performance/benchmarks-vs-baseline.md)
- [Performance budgets through telemetry](performance/perf-budgets-telemetry.md)
- [Bundle size budget](performance/bundle-size-budget.md)
- [Lighthouse CI](performance/lighthouse-ci.md)
- [Load testing](performance/load-testing.md)
- [Profiling](performance/profiling.md)

### Observability and debuggability — `observability/`

- [Structured logs and log queries](observability/structured-logs.md)
- [Metrics (PromQL)](observability/metrics-promql.md)
- [Traces (OpenTelemetry)](observability/traces-opentelemetry.md)
- [Browser console and DevTools](observability/browser-console-devtools.md)
- [Debugger and REPL](observability/debugger-repl.md)

### Reliability and resilience — `reliability/`

- [Fault injection (Toxiproxy)](reliability/fault-injection.md)
- [Chaos engineering](reliability/chaos-engineering.md)
- [Health checks and smoke tests after deploy](reliability/health-checks-smoke.md)
- [Restore from backup and rollback](reliability/backup-restore-rollback.md)

### Deployability and reproducibility — `delivery/`

- [Stop hook / `/goal`](delivery/stop-hook.md)
- [Pre-commit / pre-push](delivery/pre-commit-pre-push.md)
- [CI on clean infrastructure](delivery/ci-clean-infra.md)
- [Isolated reproducible environment](delivery/isolated-environment.md)
- [Preview environments per PR](delivery/preview-environments.md)
- [Canaries and feature flags](delivery/canary-feature-flags.md)

### Production signals — `production/`

- [Error tracking (Sentry)](production/error-tracking.md)
- [SLO degradation](production/slo-degradation.md)
- [AI judges on telemetry](production/ai-judges-telemetry.md)
- [User feedback](production/user-feedback.md)

### Interaction and accessibility — `interaction/`

- [Accessibility checks (axe, ARIA)](interaction/accessibility-checks.md)
- [Agent navigation by the accessibility tree](interaction/accessibility-tree-navigation.md)
- [UX evaluator with thresholds](interaction/ux-evaluator.md)

### Inferential and meta loops — `meta/`

- [Code review by another agent](meta/agent-code-review.md)
- [Verification subagent](meta/verification-subagent.md)
- [Eval suites for LLM features](meta/llm-evals.md)
- [Garbage collection](meta/garbage-collection.md)
- [Progress file and feature list](meta/progress-file-feature-list.md)
- [Steering loop](meta/steering-loop.md)
- [Review of document texts](meta/document-review.md)

### Human in the loop — `human/`

The person as a sensor of intent: the axes, practices, anti-patterns and metrics are in
[human/README.md](human/README.md).

- [Interview](human/interview.md)
- [Task restatement](human/task-restatement.md)
- [Plan approval](human/plan-approval.md)
- [Acceptance criteria and references from a person](human/human-acceptance-criteria.md)
- [Escalation on uncertainty](human/escalation-on-uncertainty.md)
- [Asynchronous questions with assumptions](human/async-questions-with-assumptions.md)
- [Gates on risky actions](human/risky-action-gates.md)
- [Observe and interrupt](human/observe-and-interrupt.md)
- [Result demo](human/result-demo.md)
- [Choose from options](human/choose-from-options.md)
- [Diff review by a person](human/human-diff-review.md)
- [Exploratory testing](human/exploratory-testing.md)
- [Calibrating an LLM judge on an expert (critique shadowing)](human/llm-judge-calibration.md)
- [Sample audit](human/sample-audit.md)
- [Steering: every correction becomes a rule](human/correction-becomes-rule.md)
- [Users in production](human/production-users.md)

## Sources for this page

- [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html) (Böckeler)
- [Maintainability sensors for coding agents](https://martinfowler.com/articles/sensors-for-coding-agents.html) (Böckeler)
- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) (OpenAI)
- [Minions: Stripe's one-shot, end-to-end coding agents — Part 2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2)
- [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)
- [Augmented Coding: Beyond the Vibes](https://newsletter.kentbeck.com/p/augmented-coding-beyond-the-vibes) (Kent Beck)
- [Boris Cherny on X](https://x.com/bcherny/status/2007179861115511237)
- [Harness design for long-running apps](https://anthropic.com/engineering/harness-design-long-running-apps) (Anthropic)
- [Playwright MCP Guide: Let Claude, Codex, and Cursor Control the Browser](https://eastondev.com/blog/en/posts/ai/20260904-playwright-mcp-browser-automation-claude-codex-cursor/)

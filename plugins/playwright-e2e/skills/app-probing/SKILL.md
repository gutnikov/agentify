---
name: app-probing
description: Finds out what the running web app actually does, with a throwaway Playwright script (a probe) that takes its precondition from a test fixture and its interaction from Page Objects, and reports the landing URL, the user's credentials, test ids on screen, console errors, failed requests and a screenshot. Builds a missing fixture or POM method; can hold a headed browser open. Use when the user asks to do, check or walk something in the UI ("does the invoice sheet still have a Send button", "walk the checkout flow") or for a user in a given state ("get me a user with an unpaid invoice"), and whenever the agent itself needs to explore the running app — to check by hand that a change works, walk a feature end to end, reproduce a reported bug, read console errors and failed requests, or take a screenshot to compare with a mockup or to demo. Or "/app-probing <what to do> [--headed]".
---

# App probing

```
/app-probing <what to do, in plain words> [--headed]
```

A probe is a Playwright script, run on demand against the running app and thrown away. "Log in and open the
orders page" is a script that seeds a user and navigates. "Give me a user with an unpaid invoice" is the same
script with no navigation. A probe finds out what the app does. It asserts nothing and proves nothing about
correctness.

## The two rules

1. **Preconditions come from the fixtures.** No seeding written in the probe.
2. **Interaction goes through Page Objects.** No locators written in the probe.

A script written from scratch answers the question once and is gone. A probe built on a fixture and a Page Object
answers it, the next person's version of it, and the spec written later. If the fixture or the POM method does
not exist, build it (Tier 2 below). If it exists but is broken, fix it. Never work around the layer.

The one exception is reading the DOM to describe the screen: the evidence bundle collects test ids and console
output, which is observation, not interaction.

## When the agent explores the app: a probe is one way to do it

Several loop types in the `harness-engineering` catalog have the agent look at the running app instead of trusting
the code and the tests. A probe is one way to do that look:

| Loop type | What the agent does there | What a probe gives it |
|---|---|---|
| `agentic-manual-testing` | Checks the change by hand, in a browser among other tools, and locks a defect it finds in with a test | The browser check, on a fresh user from a fixture. A defect it finds becomes a red spec (§10) |
| `e2e-browser` | Walks a scenario end to end, because unit tests and `curl` can pass while the feature does not work | The walk, through the same fixture and POM methods the spec will use |
| `browser-console-devtools` | Reads console errors and failed network requests | `consoleErrors` and `failedRequests` from the app's own origins, without analytics noise |
| `visual-screenshot-check` | Takes a screenshot and compares it with the mockup | A full-page screenshot of a settled screen. The comparison is the agent's own work |
| `bug-failing-test-fix`, `exploratory-testing` | Reproduces a reported bug before fixing it | The reproduction: the report's steps as POM calls on the state a fixture creates |
| `verification-subagent` | A second agent tries to prove that "done" is wrong | A way for it to open the app instead of only reading the diff |
| `result-demo` | Shows the person the working feature | The URL and credentials to open the state by hand, a screenshot, or a browser held open with `--headed` |

Free browsing (Playwright MCP, Chrome DevTools MCP) can do the same look. A probe differs in that it starts from a
fixture and acts through Page Objects: it can be run again, and it turns into a spec when someone asks for one.

A probe asserts nothing, so in these loops it is the exploration step, not the permanent check. What has to keep
holding becomes a spec.

## 1. Find the project's e2e layout

Find it in the repository; do not ask.

| What | Where to look |
|---|---|
| Playwright config | `playwright.config.*`: `testDir`, `testMatch`, `testIgnore`, `projects`, `reporter`, `use.baseURL`, `use.testIdAttribute`, `webServer` |
| The app under test | `use.baseURL` and the env var that sets it; `webServer` when Playwright starts the app itself; a per-branch preview if CI deploys one; how CI runs the e2e tests |
| Fixtures | files with `test.extend(`, and the `test` each of them exports |
| Page Objects | classes that take `page` in the constructor, and how specs reach them: a fixture per page, or one object that holds them all |
| Test ids | `use.testIdAttribute` (Playwright's default is `data-testid`), constants files with the ids |
| Stub fixtures | fixtures whose body throws before `use()`, usually with "not implemented" in the message |

If the project has no fixtures or Page Objects yet, the first probe builds them: that is Tier 2.

**Read the body of the fixture you pick, not just its name.** The name is a hint; the body is the contract. It
shows whether the state is seeded through an API or by walking the UI, and what else comes with it: a second user,
a role, a plan, extra data. Import `test` from the file that declares the fixture.

## 2. The app under test

Probe the same app the e2e tests use, started the same way. If CI deploys a preview of this branch, probe it;
otherwise probe the default `baseURL`. Say in the report which one: a probe against a shared environment cannot
see this branch's changes.

If the probe needs a test id the app does not render yet, that is a change in the app's code. The probe sees it
only after the app is rebuilt or redeployed the way the tests' app is.

## 3. The runner: two scratch files

Copy them from this skill's `templates/`:

- `playwright.probe.config.ts` next to the project's Playwright config;
- `probe.spec.ts` as `<testDir>/.probe/<slug>.spec.ts`, where `<slug>` is a kebab-case slug of the request.

Keep both out of git without a tracked change: add `playwright.probe.config.ts` and `.probe/` to the file that
`git rev-parse --git-path info/exclude` prints.

Each override in the probe config has a reason:

- `testDir`, `testMatch` limit the run to the scratch folder.
- `testIgnore: []`: Playwright applies `testIgnore` even to a file named on the command line. If the project's
  pattern matches the scratch folder, the run says "0 tests" instead of running.
- The `list` reporter keeps probes out of the project's reports and any upload to a test-management tool.
- `projects`: a project's own `testDir`, `testMatch` and `testIgnore` win over the top-level ones. If the config
  has projects, the template applies the overrides to the one the e2e tests use; run with `--project=<name>`.
  Projects it depends on, such as an auth setup project, stay as they are.

Fill in the spec: the fixture, the POM calls, the user's credentials if the fixture gives any. Then run it with
the project's package runner:

```bash
BASE_URL=<the app> npx playwright test --config=playwright.probe.config.ts --workers=1 --retries=0
```

Always `--workers=1 --retries=0`: one probe, one user, and a retry would hide exactly the seeding failure a probe
exists to show.

### `settle()` and the origin filter are not polish

Both are in the template because a probe without them gives a wrong answer.

- **Without `settle()` the probe under-reports the screen.** A POM method waits for the element it acts on, not for
  the screen to finish loading. A snapshot taken right after it returns shows a half-loaded panel with a fraction
  of its test ids, and the report says "the panel has no fields", which is false. `settle()` waits until no
  request of the app is in flight and the traffic has been quiet for a moment, up to a cap. It tracks requests
  from the start of the body, so the ones the interaction itself sends count too. A request that never closes
  (long polling, server-sent events) keeps it waiting to the cap: leave that URL out of the filter.
- **Without the origin filter, failed requests are noise:** analytics beacons and `ERR_ABORTED` from teardown. Real
  failures get lost in them. If the app calls an API on another host, add that origin to the filter.

`settle()` cannot see rendering that waits on a timer rather than a request. That is one more reason to look at the
screenshot (§5).

A same-origin `ERR_ABORTED` during an interaction can be a really cancelled request, and the filter drops it. If
the screen looks wrong and `failedRequests` is empty, probe again with `--headed` and watch.

## 4. A failed probe is usually the answer

Print the fixture's error verbatim, say where the scratch spec is, and leave the scratch files so the probe can be
run again. No retry loops, no quiet switch to another fixture, no seeding written in the probe as a rescue: a
seeding failure is information about the seeding path, and hiding it makes the gap invisible.

## 5. The evidence bundle

| Field | Why |
|---|---|
| `url` | Where the probe really landed. Redirects are the most common surprise |
| `user` | The credentials, so the state can be reached by hand afterwards |
| `testIds` | Every test id on the screen: locator candidates for a POM, and the elements that have none |
| `consoleErrors` | Breakage in the browser that no assertion would catch |
| `failedRequests` | The app's 4xx, 5xx and network failures: the fastest way to a backend cause |
| `settledInMs` | How long the screen took to go quiet. At the cap (8 s) it never settled: treat every other field as provisional |
| `screenshot` | Full page, in Playwright's output folder, so it survives the cleanup |

Report these, what you did (the fixture and the POM methods, in order) and, for a user request, the URL to open.
Print the credentials before any pause, never after.

**Look at the screenshot before you write the report.** It is your main evidence, not an attachment. Every field
can look healthy while the screen is wrong: the right URL, no errors, no failed requests, and an empty panel.

The listeners start with the test body, so noise from the fixture's own seeding is not captured. That is on
purpose: the interaction under study is what matters.

## 6. `--headed`: hold the browser open

Uncomment `test.setTimeout(0)` and `page.pause()` in the spec and run with `--headed`. Without
`test.setTimeout(0)`, the test timeout closes the browser while you are still in it.

This is the loop for Tier 2, not a convenience. Every run seeds a fresh user, so running again to try one more
locator is the expensive path. Seed once, hold the browser, and pick the locators for the new POM method with the
Playwright Inspector.

## 7. Tier 1 and Tier 2

- **Tier 1:** the fixture and the POM methods exist. Write the scratch files, run, report, delete them. No tracked
  changes; minutes.
- **Tier 2:** a fixture or a POM method is missing. Say so first: "this needs a new fixture, which is a tracked
  change". Then build it with `fixture-modify` or `pom-modify`. The probe stays scratch either way; what lands is
  the fixture or the method. If the element has no test id, adding one to the app is better than a fragile
  locator; that is an app change, and you say so.

**A stub fixture is a full stop.** If the state you need maps to a fixture that throws with a recorded gap, report
its message verbatim with `file:line` and stop. Do not run anything and do not build a way around it: the message
is a decision someone made with more context than the probe has. Checking whether the gap still exists is work for
`fixture-modify`.

## 8. Stuck: ask once, in one batch

If the code, the fixtures, the Page Objects and a live probe still leave the state or the flow unreachable, ask the
user once, with every open question in one message and what you already tried. Typical cases: the state needs an
outside actor (a real payment, a partner's webhook), the flow seems to be gone from the product, or the code and
the running app disagree. Guessing past this point gives a plausible answer to the wrong question.

## 9. Cleanup

```bash
rm -rf <testDir>/.probe playwright.probe.config.ts
```

Delete them after a successful run. Screenshots stay in Playwright's output folder.

## 10. From a probe to a spec

A working probe is most of a spec body, but a spec is written only when the user asks for a test. A spec adds what
a probe lacks on purpose: assertions, a place in the test tree, the project's test metadata, and two green runs.

## A probe never

- calls `expect(...)`: once you want to assert, you want a spec;
- seeds state itself or uses its own locators for interaction;
- works around a stub fixture;
- gets committed;
- changes shared or long-lived accounts: fixtures create fresh users, use them;
- writes what it found into a committed markdown file about the app's state: such a file goes stale the day it is
  written. Findings go into the report, a Page Object or a fixture;
- retries to hide a failure.

---
name: event-model-e2e
description: Turns the specs of an Event Model (the event-model skill) into Playwright e2e tests that stand on the project's fixtures and Page Objects. Plans which fixtures, external stubs and Page Object methods the specs need, builds the missing ones with fixture-modify and pom-modify, scaffolds one spec file per slice tagged @slice:<id> with tests titled after the specs, runs them twice, and reports the model's e2e coverage. Use when the user asks for e2e tests from the model or the spec ("write e2e tests for slice S16", "cover the billing model with e2e", "which specs have no test"), after the model changed, or "/event-model-e2e [slice ids]".
---

# E2E tests from the event model

```
/event-model-e2e [slice ids, comma-separated; default: every slice with e2e-ready specs]
```

Each e2e-ready spec in the model is one Playwright test. The model already says everything the test needs: the
state it starts from, what the person does, which outside system answers how, and what the person sees. This skill
maps that onto the project's test layer and never around it.

`S` is this skill's folder (Claude Code shows it when the skill loads). The script is
`$S/../event-model/scripts/em.py`; below it is `em.py`.

## Needs

- The model checks clean: `python3 em.py check model/` reports zero errors. If not, fix the model first with the
  `event-model` skill.
- The `playwright` plugin (`fixture-modify`, `pom-modify`) and `app-probing`. If the session does not have them, say
  that this skill builds fixtures and Page Objects with them, offer `/plugin install playwright@private-plugins` and
  `/plugin install app-probing@private-plugins`, and stop.

## The mapping

| In the model | In the tests | Built with |
|---|---|---|
| `states.<name>` | a fixture of that name; `extends` is the fixture it depends on; `note` is what its TSDoc promises | `fixture-modify` |
| `externals.<X>.outcomes.<o>` | a fixture that forces the outcome: a testing-API switch first, `page.route` when the call comes from the browser | `fixture-modify` |
| `after` | a `testClock` fixture that moves the backend's clock through the testing API | `fixture-modify` |
| `screens.<name>` | a Page Object (`pom` is the property tests receive, `route` is where `open()` goes) | `pom-modify`, after `app-probing` |
| the slice's command and `when` | one action method on the screen's Page Object: `requestGeneration(input)` | `pom-modify` |
| `then.see` | `open()` on that screen, then an `expect<Field>(value)` method | `pom-modify` |
| `then.error` | `expectError(name)` on the screen where the command was issued | `pom-modify` |
| slice `id`, spec `name` | `test.describe(…, { tag: '@slice:<id>' })`, `test('<spec name>')` | `em.py scaffold` |
| `question` on a spec, or a spec not in the full form | `test.fixme`, with the question or the reason above it | `em.py scaffold` |

## 1. Plan

```bash
python3 em.py plan model/ --slices S16,A04
```

The plan lists the fixtures, the Page Object methods and the tests. The names in it are proposals, built from the
model's names.

## 2. Fixtures

For every fixture in the plan, follow `fixture-modify`: reuse an existing fixture first (read its body, not its
name), build on one by adding one thing, write a new one only then. Pass it the state's `note` and its events as
the description of the state. When an existing fixture already produces the state under another name, use that
name: change the state's name in the model, so model and tests keep one vocabulary.

A state that cannot be seeded becomes a **stub fixture**, exactly as `fixture-modify` §6 says. Its tests fail fast
with the stub's message. That is a finding about the testing API, not a reason to drop the spec.

## 3. Page Objects

For every screen in the plan: find its Page Object (by the route), look at the live screen with `app-probing`, and
add the missing methods with `pom-modify`. When the project already has a method that does the same thing under
another name, use it and edit the scaffolded test. When the property name differs from the model's `screens.<name>.pom`,
correct the model.

## 4. Scaffold the tests

```bash
python3 em.py scaffold model/ --slices S16,A04 --out <testDir>/<area> --fixtures-import <the fixture file>
```

One file per slice, never overwritten (`--force` only when asked). Then edit each file to the project's
conventions: the real fixture and method names, the project's test metadata. Keep the `@slice:<id>` tag and the
titles: coverage matches tests to specs by them. Assertions stay inside Page Object `expect*` methods; a test seeds
nothing itself.

A spec about concurrency (two requests at once) is not a browser test: write it with Playwright's `request` against
the API, on the same fixtures.

## 5. Run twice

```bash
npx playwright test <the files> --workers=1 --retries=0
npx playwright test <the files> --workers=2 --retries=0
```

A red test is one of four things. Find out which before changing anything:

| Red because | Then |
|---|---|
| the fixture produces the wrong state | fix the fixture; its contract spec should have caught it |
| the Page Object misses the element | probe the screen, fix the Page Object |
| the app does not do what the spec says | for a feature being built, an app bug: report it, keep the test red. For a model of an existing app, the model is wrong: correct the spec and say so |
| the spec is ambiguous | add a question to the model and mark the test `test.fixme` with it |

Green in the first run and red in the second means tests share state: fix it in the fixture, never with retries.

## 6. Coverage

```bash
python3 em.py coverage model/ --tests <testDir>
```

It reports specs with a running test, specs with a `fixme`, specs with no test, tests tagged with slices the model
no longer has, and tests whose title matches no spec. Report these numbers with the run results.

## A test from the model never

- seeds state in its body or uses a locator: fixtures and Page Objects do that;
- asserts outside a Page Object's `expect*` or `verify*` method;
- changes a title without changing the spec's name in the model, or the other way round;
- skips a spec silently: an untestable spec is a `test.fixme` with the reason;
- hides a failure with retries.

## Done when

- every e2e-ready spec of the chosen slices has a test, green twice, or a `test.fixme` with a reason;
- the fixtures it needed have contract specs (`fixture-modify`), the Page Object methods were checked on the live
  screen (`pom-modify`);
- `em.py coverage` has been run and its numbers are in the report.

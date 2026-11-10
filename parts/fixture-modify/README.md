# Fixtures

A part of agentify: `/agentify` uses it when a test, a probe or a state of the spec needs a fixture.

A test is mostly its precondition. In "log in as a new user, create an invoice, send it, open its details, check
the status", the first steps are where the work is; the check on top is a few lines. That first part is the
**fixture**: it produces a state. The **scenario** checks behaviour on that state. Keep them apart: a fixture
asserts nothing about the feature, and a spec seeds nothing itself.

## 1. Find the project's conventions

Find them in the repository; do not ask. When the project's files and this part disagree, follow the files, and
do not migrate conventions on the way.

| What | Where to look |
|---|---|
| The base `test` | the file every fixture file extends. It often adds automatic fixtures (logging, a session setup). Extend it, not `@playwright/test`, or the new fixtures lose what it adds |
| Fixture files | the `test.extend` calls, usually one file per product area |
| The testing API | the internal API that creates users and entities directly (QA API, test API, user generator, test data service): its client in the tests, and the repository of the service itself |
| Seeding helpers | wrappers around the testing API's calls; some already handle a backend's transient states, such as waiting until an entity is ready |
| Logging in | how fixtures authenticate: an API call, cookies, `storageState` |
| Timeouts | the project's timeout constants |
| Contract specs | where existing ones live and the tag they carry |

If there is no fixture layer yet, start one file for the area, extending the project's base `test` or
`@playwright/test`.

## 2. Reuse first

1. Look for a fixture that already produces the state. Read the bodies, not just the names.
2. If none does, look for one the new state can be built on by adding **one** thing.
3. Only then write a fixture from scratch.

## 3. The shape of a fixture

- **Name it after the state it produces**, not the action: `userWithUnpaidInvoice`, `ownerWithInvitedMember`. Never
  `setupUser` or `createInvoice`.
- **Types:** a flat record of fixture names to what the test receives. Intersections for additions:
  `MemberContext = UserContext & { member: Credentials }`. Take the types of API outputs from the API client
  (`Awaited<ReturnType<typeof createUser>>`), so they follow the API when it changes.
- **Dependencies** are destructured from the first argument; Playwright runs them first. Prefix a dependency used
  only for its side effects with `_` (`page: _page`).
- **`await use(value)` exactly once**, never `return`. Code after `use` is teardown; with a fresh user per test it
  is rarely needed.
- **One fixture adds one thing** on top of another, at most three levels deep. Past that, nobody can tell which
  fixture seeded what.
- **Never change shared state** from a dependency, such as switching the user's role: tests running in parallel
  share it.

```
loggedInUser                      fresh user, authenticated session
  └─ userWithUnpaidInvoice        + one unpaid invoice, created through the testing API
       └─ userWithOverdueInvoice  + the invoice's due date moved into the past
```

```typescript
/**
 * A fresh user with one unpaid invoice, created through the testing API. The session is the user's.
 *
 * Seeded through the API, not the UI: the tests that use it check what happens after the invoice exists,
 * and walking the creation form only adds time and noise.
 */
userWithUnpaidInvoice: async ({ loggedInUser }, use) => {
  const invoice = await seedInvoice(loggedInUser.user, { status: 'unpaid' });
  await use({ ...loggedInUser, invoice });
},
```

## 4. Seed through the testing API first, the UI when the flow is the point

| Through the testing API when… | Through the UI when… |
|---|---|
| the test checks behaviour after the state exists | the test is about the flow that creates the state |
| the state has no UI path | the state needs side effects only the UI produces |
| a follow-up call needs an id the API returns | the test has to open that screen anyway |

**Before you decide the API cannot do it, read the testing API's own code**, not only the client in the tests.
Methods the tests never used often exist, some of the used ones are deprecated, and the client in the tests can be
out of date with the service and fake a missing capability.

**One helper per seeding operation** (`seedUser`, `seedInvoice`), private to the fixture file: every fixture calls
the API the same way, and a fix to that call lands in one place.

**Values from the backend** (a plan code, an enum value) are constants with a comment that says where they come
from: the backend file or the API definition. Renames on the backend break fixtures quietly.

## 5. Document the fixture

A TSDoc comment above each fixture answers four questions: what state it produces, why that state exists (which
tests need it), why this seeding path and not another, and what a consumer must know, such as "the session stays
the owner's; log in as the member if the test needs them".

## 6. When the state cannot be seeded: the ladder

Go down only when the rung above is exhausted.

1. **A fresh user**, the default. Before you give up: a parameter of the testing API, a helper nobody wrote yet,
   the API's own code (§4).
2. **A long-lived account, prepared by hand**, only with a written reason:
   - the fresh path is impossible: no API route, a state only an outside actor creates, a cool-down period;
   - QA decided so: name who and when;
   - the fresh path exists but is too slow or flaky for this test tier. "Seeding is slow" alone is not enough.

   Register the account once, in one place, with its purpose, its state, its access (`read-only` or `mutating`),
   who authorised it and when, its consumers and its lifetime. For `mutating` access, its consumers run serially
   (one file, or `test.describe.configure({ mode: 'serial' })`) and leave it usable for the next run. Never change
   the shared credentials object; copy it (`{ ...account }`). Its contract spec is a real test: it is the first
   to go red when the account's state rots.
3. **A stub fixture.** Declare the fixture and throw an error that says what is missing and what would unblock it.
   Do not `test.skip` and do not leave the fixture out: declaring it keeps the gap visible, and tests that need it
   fail fast. The TSDoc above it says what was checked and against what.

```typescript
/**
 * Blocked: the testing API cannot backdate an invoice, and the due date can only be in the future.
 * Checked against the invoices service on 2026-11-08: the due date is validated on create and on update.
 * Unblocks when the testing API can set due_date in the past.
 */
userWithOverdueInvoice: async ({ userWithUnpaidInvoice }, use) => {
  void userWithUnpaidInvoice;
  void use;
  throw new Error(
    'userWithOverdueInvoice fixture not implemented — the testing API cannot set a past due date',
  );
},
```

## 7. Prove it: a contract spec, green twice

When a fixture produces the wrong state, the failure shows up in the body of the test that uses it, and the
investigation starts in the wrong file. So every fixture lands with a **contract spec**: a small test that asserts
the state the fixture's TSDoc promises, and nothing more.

- One file per topic, such as `<area>/_fixtures/<topic>.contract.spec.ts`, or wherever the project keeps them.
- One test per fixture, tagged `@fixture-contract`, importing `test` from the fixture file and taking only the
  fixture under test and the Page Objects the check needs.
- One assertion deep: at most a navigation and one check. Anything longer is a real test.

```typescript
/** Contract: after this fixture, the user's invoice list shows the invoice as unpaid. */
test(
  'contract: userWithUnpaidInvoice has an unpaid invoice',
  { tag: '@fixture-contract' },
  async ({ userWithUnpaidInvoice: _, invoices }) => {
    void _;
    await invoices.open();
    await invoices.expectStatus('Unpaid');
  },
);
```

- A **stub fixture's** contract spec is `test.fixme`, with a TODO describing the contract it will satisfy. Turning
  it into a passing `test` is the only way a stub becomes a real fixture.
- A **broken real fixture** (the API call exists, the backend currently rejects it) also gets `test.fixme`, with a
  `BROKEN` comment that names the cause and what would unblock it.

Run the contract spec twice:

```bash
npx playwright test <contract spec> --workers=1 --retries=0
npx playwright test <contract spec> --workers=2 --retries=0
```

- **Red in the first run:** the fixture is wrong. Fix the fixture, never the contract.
- **Green in the first, red in the second:** tests running in parallel share something — an identifier without a
  random suffix, module-level state, a race in logging in, a rate limit. Fix it in the fixture. Never hide it
  with retries.
- Two workers are enough to catch shared state. More workers against a shared test backend mostly add flakes
  caused by load.

A contract spec never seeds extra data, checks behaviour beyond the fixture's promise, repeats the fixture's body or
uses retries. If it has to seed something itself, the fixture's TSDoc is wrong about what it produces.

## 8. Data fixtures

Static reference data (a company's details, a test card number) is a plain `as const` object, grouped by domain
rather than by test, with a comment on each shape's caveats ("do not use for the full sign-up: the duplicate
company is declined automatically"). It imports nothing from Playwright. If it needs a `page`, it is a function
fixture.

## 9. Cost

Every fixture runs before the test body, on every run. An API call takes about a second or two; a UI flow takes
ten or more. A chain of three fixtures can cost a quarter of a minute before the test starts. Prefer API seeding,
and do not add a wrapping fixture when the test can take the parent directly.

## A fixture never

- calls `use` twice, or returns a value;
- keeps mutable state at module level, or uses identifiers that collide between parallel tests;
- waits with `waitForTimeout`: use auto-retrying assertions, `waitForResponse` or `expect(...).toPass()`;
- calls `test.skip` or `test.fixme` in its body: a state it cannot produce is a thrown error (§6);
- logs in through the login form, unless the tests that use it are about logging in;
- calls the API directly when the project has a helper that handles the backend's transient states.

## Done when

- the TSDoc answers the four questions;
- the contract spec is green twice;
- the project's lint and type check pass;
- a real spec or a probe has used the fixture.

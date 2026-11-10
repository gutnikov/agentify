# Page Objects

A part of agentify: `/agentify` uses it when a test, a fixture or a probe needs a Page Object method.

A Page Object (POM) is an API for one page or panel. A PIN screen with four separate inputs gets one method,
`fillPin(pin)`; the method knows how to fill the inputs and what to do when one does not take focus. Tests read as
user actions, and the mess stays in one place.

A POM is the only way tests, fixtures and probes touch the UI. A locator written in a spec is a bug waiting for the
next redesign.

## 1. Find the project's conventions

Find them in the repository; do not ask. When the project's files and this part disagree, follow the files.

| What | Where to look |
|---|---|
| Page Objects | classes that take `page` in the constructor; their folder and naming |
| A base page class | shared locators and helpers. Do not duplicate them, and add to the base class only what three or more pages need |
| How tests get them | a fixture per page, or one object that holds them all. A new POM is registered there |
| Test ids | `use.testIdAttribute` in the Playwright config (default `data-testid`), constants files with the ids |
| Timeouts, translations | the project's timeout constants; a translation helper, if the app is translated and the tests use one |

If the project has no Page Objects yet, create the first one and give it to tests through a fixture, the way the
Playwright docs show:

```typescript
export const test = base.extend<{ invoices: InvoicesPage }>({
  invoices: async ({ page }, use) => use(new InvoicesPage(page)),
});
```

## 2. Before you write

- **Look at the page first.** Run a probe (`app-probing`) to see the elements and test ids the app really renders.
  Never write locators from memory or from the source alone.
- **Extend before you add.** One page, one class: add a method to the existing POM rather than a second class for
  the same page.
- **Add rather than change.** A new method breaks nobody; a changed one can break every spec that calls it.
- **Before changing a method or a locator, find who uses it.** If tests reach POMs through a fixture or a holder
  object, search for the property, not the import: `grep -rn "\.invoices\." <tests>`. Searching for the import can
  return nothing for a POM that dozens of specs drive.

## 3. Anatomy

```typescript
import { expect, type Locator, type Page } from '@playwright/test';

/** The invoice details side sheet. */
export class InvoiceSheet {
  private readonly sendButton: Locator;
  // The status badge has no role or label; the test id is its only stable handle.
  private readonly statusBadge: Locator;

  constructor(page: Page) {
    this.sendButton = page.getByRole('button', { name: 'Send invoice' });
    this.statusBadge = page.getByTestId('invoice-status');
  }

  async send() {
    await this.sendButton.click();
  }

  async expectStatus(status: string) {
    await expect(this.statusBadge).toHaveText(status);
  }
}
```

- **Locators are private fields**, named after the element and its role: `sendButton`, `nicknameInput`,
  `ordersTable`; never `btn` or `el`. Other code goes through methods, never through another POM's locators.
- **A one-line comment on every locator that is not obvious:** why this locator, which quirk of the DOM it avoids.
  That is where a project's hard-won lessons live.
- **Locators with a parameter are function fields:** `private row: (name: string) => Locator`.
- **The constructor** assigns locators and nothing else: no `await`, no assertions. Locators are lazy.
- **Public methods are user actions**, one action on screen each.
- **Assertions live only in `expect*` and `verify*` methods.** Action methods only act, so a failure points to the
  right line.
- **A POM keeps no state** besides `page`, and never creates another POM. A flow that crosses pages goes back to the
  test, which calls the next POM.

## 4. Locators: the ladder

Go down only when the rung above does not work on the live page.

| # | Locator | When |
|---|---|---|
| 1 | `getByTestId(…)` | The element has a test id: the strongest contract |
| 2 | `getByRole('button', { name })` | The role and the visible name are unambiguous on the screen |
| 3 | `getByLabel`, `getByText`, `getByPlaceholder` | Inputs, headings, text with no matching role |
| 4 | `locator('button').filter({ hasText })` | A component hides its name from the accessibility tree, e.g. a label wrapped in nested spans |
| 5 | A scoped locator: `page.locator('section', { hasText: '…' }).getByText('…')` | Common labels (Cancel, Save) that appear in several places |
| 6 | Coordinates (`page.evaluate`, then `page.mouse.click`), in a private method | Nothing above can reach the element |

If the element has no test id and the next rungs are fragile, adding a test id to the app is the better fix. That
is a change in the app; say so.

Never use CSS classes, `nth-child`, XPath, or walking up to a parent (`locator('..')`): styling and wrapper elements
change without anyone touching the feature.

If the app is translated and the tests can read its translations, match visible text through the translation key,
not a hardcoded string. When old and new copy both exist, join them in one anchored regex.

## 5. Traps in the DOM

- **Inputs inside a `<label>`** often have no accessible name of their own:
  `page.locator('label', { hasText: 'Notifications' }).locator('input[type="checkbox"]')`.
- **Modals, side sheets and dropdowns** often render in a portal outside the form. Start their locators from
  `page`, not from the form's locator.
- **Names that collide on a substring** ("Main" and "Main account"): anchor the regex, `{ name: /^Main$/ }`.
- **Text that changes between environments or locales**, such as prices and dates: anchor on the stable part,
  `getByLabel(/^Express delivery/)`.
- **Data refetched on window focus** (React Query, SWR): a headless browser never fires focus. Dispatch `focus` and
  `visibilitychange` on `window` and `document` rather than reloading the page.
- **Pages that depend on the user's role:** a user without access may be redirected rather than refused. One method
  waits for whichever entry point appears (`Promise.race`); do not fork it into a method per role.

## 6. Waits and clicks

- **No `waitForTimeout`, no `networkidle`**: an app that polls never goes idle. Use auto-retrying assertions and the
  project's timeout constants, never a magic number.
- **Click once, then poll.** A second click can close what a slow first click opened:

  ```typescript
  await expect(async () => {
    if (!(await this.sheet.isVisible())) await this.openButton.click();
    await expect(this.sheet).toBeVisible({ timeout: 3_000 });
  }).toPass();
  ```

- **`click({ force: true })`** only after an explicit `waitFor({ state: 'visible' })` and `scrollIntoViewIfNeeded()`.
  Never by default: it silences real bugs.
- **Workarounds** such as coordinate clicks or walking sibling nodes go into private methods. Tests never see them.

## 7. Method names

| Intent | Pattern | Examples |
|---|---|---|
| A user action | a verb phrase | `send`, `fillPin`, `selectPlan`, `cancelOrder` |
| A flow of several steps | a verb and its outcome | `createAndOpenInvoice`, `goToBilling` |
| A check | `expect*`, `verify*` | `expectStatus`, `verifyMemberRow` |
| An optional step | `*IfVisible`, `*IfRequired` | `fillPinIfRequired` |
| A helper | private, descriptive | `clickRowCheckbox` |

Not `clickButton`, `doStuff`, or a bare `submit` without saying what is submitted: name the outcome the user sees,
not the DOM event.

A flow of several steps calls the page's public methods, each of which works on its own.

## 8. Register and check

1. Register a new POM where tests get Page Objects: the fixture or the holder object.
2. Run the project's lint and type check.
3. Run a spec or a probe that uses the new or changed method, twice: `--workers=1`, then `--workers=2`, both with
   `--retries=0`. For a changed method, also run the specs found in §2. Green in the first run and red in the second
   means tests share something; fix it in the POM or the fixture, never with retries.

## A Page Object never

- asserts inside an action method;
- waits with `waitForTimeout` or `networkidle`, or uses a magic-number timeout;
- matches hardcoded text where the project matches through translations;
- keeps state in fields other than `page` and its locators;
- creates another Page Object;
- uses `force: true` without an explicit wait first.

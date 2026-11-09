# The Event Model format

One or more YAML files. `em.py` merges every `.yaml` file it is given, or every one under a folder it is given.
A full example: `examples/vendy.em.yaml`. A starting point: `templates/model.em.yaml`.

## Top level

| Key | What it holds |
|---|---|
| `system` | The system's name |
| `actors` | Who acts on screens: `[Visitor, Seller]` |
| `externals` | Outside systems and the outcomes a test can force: `AIModels: {outcomes: {succeeds: aiRenderSucceeds, fails: aiRenderFails}}`. The value of an outcome is the name of the e2e fixture that forces it. A plain list `[AIModels]` is allowed while there are no outcomes yet |
| `clock` | `true` when something happens on time (renewals, expiry): automations may use `trigger: clock` and specs may use `after` |
| `domains` | Value sets for decision tables: `Plan: [Starter, Seller, Scale]` |
| `rules` | Decision tables and formulas (below) |
| `screens` | Optional. Where a screen lives and the Page Object that drives it: `CreateAdPage: {route: /next/static-ad, pom: staticAdPage}`. Without it the Page Object is the screen's name in lowerCamelCase |
| `states` | Named preconditions; each one is an e2e fixture (below) |
| `slices` | The model itself, in timeline order |

## Slices

| `type` | Shape | Means |
|---|---|---|
| `command` | `actor`, `screen`, `command`, `events`, `specs` | A person on a screen issues a command; it produces events |
| `view` | `read_model`, `screens` | A read model built from events, shown on screens |
| `automation` | `trigger` (an event or `clock`), `reads`, `command`, `events`, `specs` | The system reacts to an event or to time |
| `translation` | `external`, `trigger` (an event, `clock` or `external`), `reads`, `command`, `events`, `specs` | An outside system answers; its data enters as `ext` |

Every slice has an `id` (`S16`, `V06`, `A05`, `T09`: unique, stable, tests are tagged with it) and a `name`.
Optional: `rules: [<rule id>]` the slice depends on, `questions: ["…"]`.

## Where every field comes from

The checker traces every field back to its origin. Information completeness: nothing appears from nowhere.

| In | Allowed sources |
|---|---|
| a command field | `input` (the person types it), `<ReadModel>.<field>` (the person picks it on the screen; the read model must be shown on the slice's screen), `<Event>.<field>` (the trigger of an automation or translation), `ext` (translation only), `system` |
| an event field | `cmd` (the command's field of the same name), `system`, `ext` (translation only), `rule:<id>`, `<Event>.<field>` (the trigger), `<ReadModel>.<field>` (on the screen, or in `reads`) |
| a read-model field | a list of `<Event>.<field>`, `<Event>` (the fact that it happened), `config`, `rule:<id>` |

## Specs

Write every spec in the full form. It is what turns into an e2e test.

```yaml
specs:
  - name: a ready static ad is charged at the estimate     # unique in the slice; the test's title
    given: subscribedSellerWithProduct                     # a named state = the fixture
    when: {adType: static, modelQuality: GPT25_high_2K, variations: 1}   # the command's inputs
    external: {AIModels: succeeds}                         # outcomes of outside systems the test forces
    after: periodEnd                                       # time that passes first (needs clock: true)
    then:
      events: [GenerationRequested]                        # domain outcome of this slice (optional)
      see:                                                 # what the person sees afterwards
        - {screen: MyAdsPage, field: MyAds.status, is: succeeded}
        - {screen: CreditsDialog, field: CreditBalance.total, is: 2331}
    question: "…"                                          # open question: the test is scaffolded as test.fixme
  - name: without credits the request is refused
    given: sellerWithProduct
    when: {adType: static, modelQuality: GPT25_high_2K, variations: 1}
    then: {error: InsufficientCredits}
```

- `when` keys are the command's fields: typed (`input`) or picked on screen (`<ReadModel>.<field>`). Values that
  come from elsewhere belong to the state.
- `see` items name a screen that renders the read model, and a field of it, with the expected value.
- A spec is **e2e-ready** when it has a `name`, a `given` state, and a `see` or an `error`.
- Every command slice needs at least one e2e-ready success spec and one e2e-ready failure spec.

The short domain form is still accepted, for models that are not ready for tests yet; the checker counts it as
not e2e-ready:

```yaml
- {given: [ProductCreated], when: RequestGeneration, then: error InsufficientCredits}
```

## States

A state is a precondition with a name, written as the events that produced it. It becomes one Playwright fixture
(see the `playwright` plugin's `fixture-modify`).

```yaml
states:
  freshSeller: {given: [AccountRegistered, DefaultBrandCreated], note: "a new account"}
  sellerWithProduct: {extends: freshSeller, given: [ProductCreated], note: "one product with three photos"}
```

- Name it after the state, not the action: `sellerWithProduct`, never `createProduct`.
- One state adds one thing to its parent, at most three levels deep.
- `note` holds the concrete values the fixture must produce (plan, balance, counts).

## Rules

```yaml
rules:
  plan-credits:
    kind: table
    inputs: [Plan, Period]           # domains
    output: credits_per_period
    rows:
      - [Starter, monthly, 850]
  wallet-order:
    kind: formula
    text: "UNKNOWN: which wallet is debited first"
    unknown: true                    # not invented: a warning wherever it is used
```

The checker lists every input combination a table does not cover and every overlap.

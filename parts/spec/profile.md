# The project profile

Setup ends with the spine and a short list of layers that fit the project. To choose them you need six facts. The
repository and this session show some; you ask about the rest in one form. Facts and answers go into
`specs/profile.yaml`, so nobody is asked twice.

| Fact | Field | Usually |
|---|---|---|
| What the product is: web, API, mobile, data… | `product` | found |
| Where requirements come from: trackers this session can read, docs, a running app | `sources` | partly found, asked |
| Who answers questions about requirements and approves the spec | `people` | asked |
| Who turns the spec into tests, with what, and how tests seed state | `tests` | partly found, asked |
| Where a wrong spec costs most: money, permissions, concurrency, timers, integrations… | `risks` | partly found, asked |

## 1. Find out first

| Fact | Where to look |
|---|---|
| Product | Frameworks in the dependencies (React, Next → `web`; an HTTP or gRPC server, OpenAPI → `api`; iOS, Android → `mobile`), README, CLAUDE.md |
| Sources | MCP servers and CLIs of this session that read trackers (Jira, GitLab, GitHub, Linear): call one once with a real ticket. Ticket keys in branch names and commit messages show which tracker the team uses. `docs/`, ADRs, PRD links in the README |
| Tests | Playwright or Cypress in the dependencies, a fixtures folder, a testing API client; agentify's `event-model` and `fixture-modify` parts, and agents in `.claude/agents/` that write tests |
| Risks | Payments, credits, quotas, roles in the code and the tickets; cron jobs, queues, retries, webhooks; more than one service or team; a public API spec; compliance words in tickets (GDPR, consent, audit) |
| Existing specs | `specs/`, `model/`, `*.feature`, `*.bpmn`, `*.dmn`, `*.cml`, OpenAPI files, `docs/requirements` |

A tracker counts only if the session can read it: fetch one ticket. An SDK in the code is not access.

## 2. Ask what is left, in one form

One call of the session's question tool, up to 4 questions, each multi-select, each starting with what you found
("Found: Jira via MCP, keys VND-…"), with what you found as the first option, marked "(found)". These are setup
questions (R5), not questions about a requirement.

### Q1. Sources — header `Sources`

"Where do requirements come from? Found: <…>." Options: a tracker (by name), documents (by place), the running app
(reverse engineering), text in the chat.

### Q2. People — header `Approver`

"Who answers questions about requirements and approves the spec?" Options: the people you found as ticket
reporters or product owners, "me (the user)", "the ticket's reporter, per ticket".

### Q3. Tests — header `Tests`

"Who turns the spec into tests? Found: <…>." Options: an agent or plugin you found, "a person (QA)", "not decided
yet". The spec is written for the tests either way; the answer only names the reader.

### Q4. Risks — header `Risks`

"Where would a wrong spec cost most? Found: <…>." Options from what you found: money and quotas, permissions,
concurrency, timers and retries, integrations, a public API, several teams, compliance.

## 3. From the profile to layers

Always:

| Layer | Why |
|---|---|
| `event-model` (spine) | every behaviour as an example a test can be derived from |
| `glossary` | one name per thing: tests, fixtures and Page Objects reuse the names |

Then one layer per named risk, and nothing for a risk nobody named:

| Risk or fact | Layer | Instead, if the risk is small |
|---|---|---|
| money, quotas, permissions, eligibility | `decision-tables` in the spine's `rules:` | — this one is cheap; always add it for money |
| key entities with a status that decides what a person may do | `state-machines` | the status field and its transitions in the spine |
| money or counters changed by parallel operations | `tla-plus`, for that part only | an example of the race in the spine and a question |
| several teams or services | `context-map` (the map only) | a `context:` tag on the spine's streams |
| a public API or one another team consumes | `api-contracts` | — |
| long processes with timers, retries, people in the loop, and a process engine | `bpmn` | `clock` slices and `after` examples in the spine |
| readers who do not read YAML must sign off examples | `examples` (generated Gherkin) | a readable export of the examples in the review |

Propose the spine, the glossary and 0–3 layers, never more than 5. For each: the risk it covers, what it costs, what
the tests get. Add a "not now" list with reasons. The user picks (R5); set up exactly those.

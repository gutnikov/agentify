---
# What only the user decides about agentify in this project. The first /agentify proposes these from what it found
# and the user's answers; after that they change only with the user's approval (H7). The scripts read the fields
# here; every task reads the whole file.
#
# What the project ships, one or more of: web, api, mobile, library, data, llm, infra.
kind: []
# How far agentify goes on its own: ask, branch, merge or deploy (the harness part's README, "Preferences").
autonomy: branch
# Where a change counts as done, and the super-loops end: local, ci, staging or production.
done_at: ci
# What the agent can use from its own session, each checked with one real call or named by the user.
# Keys: ci, logs, errors, metrics, traces, browser, deploy, tracker. Value: what and how, e.g. "GitLab CI via glab".
tools: {}
# The spend limit in USD for evals and inferential loops; null means no limit.
budget_usd: null
# The spec, once it is set up (the spec part): who answers questions about requirements and approves the spec,
# such as "the user", a name, or "the ticket's reporter"; a person always approves (H5).
spec_approver: "the user"
# Who turns the spec into tests: "agent", a test writer with a fresh context, or a person, such as "QA".
test_writer: agent
# What agentify never invents, whatever the sources hint at: each is a question to the spec approver.
never_invent:
  - prices, credits, quotas and limits
  - who may do what (roles and permissions)
  - legal, compliance and consent texts
  - the wording of errors and of anything about money
  - deadlines, timeouts and retry counts
---

# <The project>

<What the project is: in the user's own words, or what agentify found and the user confirmed.>

## Notes

<Anything else every task must know: what never to touch, when releases may happen, what not to ask about.>

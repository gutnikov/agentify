---
id: secret-scanning
title: "Secret scanning"
group: security
qualities: [confidentiality]
stages: [commit]
places: [delivery/work, remediation/work, maintenance/work]
---

# Secret scanning

## Loop

GitLeaks in pre-commit blocks a commit that contains a secret; the agent moves the secret into environment
variables.

## Set up

- Run GitLeaks or trufflehog as a pre-commit hook.
- The source gives no setup steps and no reason to pick one tool over the other.

## Notes

- Böckeler explicitly calls this hook a sensor for the agent.
- The source does not say what to do in these cases:
  - the scanner flags something that is not a real secret
  - the agent skips the hook
  - the secret is already in an earlier commit

## Sources

- [Maintainability sensors for coding agents](https://martinfowler.com/articles/sensors-for-coding-agents.html) (Böckeler)

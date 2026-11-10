---
id: dependency-scanning-sbom
title: "Dependency analysis (SCA) and SBOM"
group: security
qualities: [security, supportability]
stages: [ci]
places: [delivery/work, remediation/work, maintenance/entry, maintenance/work]
---

# Dependency analysis (SCA) and SBOM

## Loop

The scanner reports a CVE in a dependency the agent added. The agent then picks a safe version.

The source describes only this case. It does not say:

- what counts as a safe version, or whether the scanner runs again to confirm the new version
- what the agent does when no fixed version exists, when the CVE is in a transitive dependency, or when the fixed version breaks the build
- when the loop stops or hands the problem to a person

## Set up

Use these in CI:

- a dependency scanner: osv-scanner, Trivy or Dependabot. The source research (see Sources) did not check Trivy itself. It lists Trivy as common practice.
- an SBOM (software bill of materials) in CycloneDX or SPDX format. The source does not say who produces the SBOM, at which step, or whether the scanner reads it.

## Sources

The research cites no source for this loop.

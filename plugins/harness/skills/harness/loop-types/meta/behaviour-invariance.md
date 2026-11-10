---
id: behaviour-invariance
title: "Behaviour invariance: maintenance that changes no expected value"
group: meta
agent: [reviewer]
qualities: [maintainability, correctness, modifiability]
stages: [local, ci]
speed: [minutes]
places: [maintenance/oracle, maintenance/gate]
---

# Behaviour invariance: maintenance that changes no expected value

## Loop

Before a maintenance change, the baseline is recorded: the expected values of every existing test, and the current
value of the measure the change should improve. After the change, the gate reports whether any expected value
changed, whether the tests pass, and whether the measure improved. A changed expected value sends the work back to
triage: it is delivery or remediation, not maintenance.

## Set up

- **The baseline** is the test suite at the commit the change starts from, and the measure's value there: the age of
  a dependency, known vulnerabilities, coupling, the bundle size, a benchmark.
- **Expected values, not test code.** A test may change how it reaches the code (an import, a mock, a setup for a new
  version of a library) but not what it asserts. The check compares the assertions and fixtures of the two versions:
  by a script where the test framework allows it (approved fixtures, snapshots, golden files), by a guard elsewhere.
- **The gate is the `run`.** One line per change: `expected value changed: <test>`, `tests red`,
  `measure not improved: <before> → <after>`, or `invariant, <measure> <before> → <after>`. The exit is non-zero for
  anything but the last.
- **A weak oracle first.** Where the tests do not cover the code the change touches, characterization tests come
  first and become part of the baseline ([approved-fixtures](../testing/approved-fixtures.md),
  [code-coverage](../testing/code-coverage.md)).
- **Cases.** Must fire: an assertion with a new expected value; a deleted test; a snapshot updated in the same change;
  a measure that did not improve. Must pass: a dependency bump where only the setup of a mock changed and the measure
  improved.

## Notes

- This is what makes maintenance safe to run without a person: a change of behaviour that would otherwise reach users
  unapproved stops here. At OpenAI, the pull requests of [garbage collection](garbage-collection.md) were merged
  automatically.
- An updated snapshot or golden file is a changed expected value, even when the tool updated it by itself.

## Agent step

A guard, a reviewer whose lens is the tests, returns a Verdict on whether the meaning of an assertion changed where a
script cannot tell: a rewritten assertion, a loosened matcher, a new tolerance. It gets the diff of the tests only,
and it blocks only once calibrated ([agent-calibration](agent-calibration.md)).

## Sources

- Martin Fowler, *Refactoring* (2nd edition, Addison-Wesley, 2018): changing the structure without changing the
  behaviour, with the tests as the check.
- Michael Feathers, *Working Effectively with Legacy Code* (Prentice Hall, 2004): characterization tests that record
  what the code does before it is changed.

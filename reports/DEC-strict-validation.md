---
id:            DEC-strict-validation
question:      "strict-validation"
title:         "The generator enforces the whole record contract, not just edges"
status:        accepted
binding:       false
kind:          engineering
areas:         ["method"]
decided_on:    "2026-08-29"
decision:      "The generator validates every record against the full contract — required fields and types, enum values, filename==id, required body sections, human_input/human_crux consistency, kind-gated fields — surfaces malformed files instead of silently skipping them, and fails the build on any violation."
confidence:    high
human_input:   true
human_crux:    "Pranav commissioned an external adversarial review before publishing and, given the findings, chose to harden Cruxton into a trustworthy v1.0.0 rather than ship a strong prototype as a preview."
supersedes:    []
refines:       ["DEC-index-is-generated"]
governed_by:   []
depends_on:    []
cites:         ["external adversarial readiness review, 2026-08-29"]
enforced_by:   "scripts/decision_index.py"
revisit:       ["internal | a check proves too strict in real use, or the field set changes"]
---

## Question
How strictly should the generator validate a record — only its edges, or the whole advertised contract?

## Decision
The whole contract. A record with a bad status, a non-boolean flag, an invalid date, a missing body section, a filename that doesn't match its id, or no frontmatter at all is a hard error that fails the build — not a warning, and never a silent skip.

## Human reasoning
Pranav's call: the product's entire promise is a *validated* trail, so the validator is the one component that must be beyond reproach. An external review demonstrated the old validator passing a record with an invalid status, kind, date, and confidence and silently ignoring a malformed file. Rather than publish that as a preview, Pranav chose to make the validator actually enforce the contract before any public release.

## Why
A "validated trail" whose validator accepts contract violations is worse than no validator — it manufactures false confidence. Strictness is cheap (pure structural checks) and the failure it prevents is expensive (a record everyone trusts that is quietly malformed, or one that silently doesn't count at all).

## Options considered
- **Edge-and-kind checks only (the original).** REJECTED (class: constraint) — passed malformed records; undermined the core promise.
- **Full-contract validation, build-failing.** CHOSEN.

## Consequences
Records must be complete and well-typed to pass. The genesis ledger was itself corrected to comply.

## Revisit-if
A specific check proves too strict in practice, or the schema gains/loses a field.

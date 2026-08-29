---
id:            DEC-deterministic-artifacts
question:      "deterministic-artifacts"
title:         "Generated artifacts are deterministic and CI-checkable"
status:        accepted
binding:       false
kind:          engineering
areas:         ["method"]
decided_on:    "2026-08-29"
decision:      "The generated index and ledger carry no wall-clock timestamp — their identity is the input hash — so a no-op regeneration produces no diff. A --check mode regenerates in memory and fails if the committed artifacts are stale, for CI to gate on."
confidence:    high
human_input:   false
human_crux:    ""
supersedes:    []
refines:       ["DEC-index-is-generated"]
governed_by:   []
depends_on:    []
cites:         ["external adversarial readiness review, 2026-08-29"]
enforced_by:   "scripts/decision_index.py --check"
revisit:       ["internal | a downstream consumer genuinely needs a generation timestamp"]
---

## Question
Should generated artifacts embed a timestamp, and how does CI know they are current?

## Decision
No timestamp in the artifacts; identity is the content input-hash. A `--check` mode lets CI confirm the committed index and ledger match the records without rewriting them.

## Why
A wall-clock timestamp made every regeneration a diff even when nothing changed, producing noise and needless merge conflicts between agents, and it contradicted the claim that the generator is deterministic. Content-hash identity removes the churn; --check turns "did they forget to regenerate?" into a mechanical build gate.

## Options considered
- **Timestamp in artifacts, CI runs generator only.** REJECTED (class: constraint) — nondeterministic diffs; CI never catches stale committed outputs.
- **Hash identity + --check.** CHOSEN.

## Consequences
Committed artifacts are stable across no-op runs; CI can fail on staleness.

## Revisit-if
A downstream consumer genuinely requires a generation timestamp.

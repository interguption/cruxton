---
id:            DEC-decision-record-identity
question:      "decision-record-identity"
title:         "An id is a permanent decision-event id; a separate question key groups a reversal chain"
status:        accepted
binding:       false
kind:          engineering
areas:         ["method"]
decided_on:    "2026-08-29"
decision:      "Each record's id is a permanent, unique decision-EVENT id; a separate `question` field is the stable subject key. A reversal is a new record with a new id and the same question that supersedes the old one; effective status (live vs superseded) is derived by the index, never authored."
confidence:    high
human_input:   false
human_crux:    ""
supersedes:    []
refines:       ["DEC-record-id-scheme"]
governed_by:   []
depends_on:    []
cites:         ["external adversarial readiness review, 2026-08-29"]
enforced_by:   "scripts/decision_index.py (supersede shares question; one live record per question)"
revisit:       ["internal | the question/id split proves confusing or redundant in practice"]
---

## Question
How does the model represent a reversed decision, given that an id is permanent and a closed record is immutable?

## Decision
Split identity in two. The id names the decision *event* (permanent, unique, one per record); the `question` field names the *subject* (stable, shared across a reversal chain). Reversing a decision means filing a new record with a new id and the same question that `supersedes` the old one. The generator derives which record is live and forbids two live records for one question.

## Why
The original scheme said the id "names the question," but a permanent unique id plus an immutable-supersede workflow cannot both hold for a same-question reversal — the second record would need the first's id. Separating the event id from the subject key resolves the contradiction without moving or editing any record, and turns "two contradictory decisions both live" from a silent bug into a build failure.

## Options considered
- **Keep id == question, edit records on reversal.** REJECTED (class: principle) — violates immutability; strands citations.
- **Sequential event ids only (ADR-0001…), no subject key.** REJECTED (class: constraint) — loses the greppable, question-named slug that makes the trail navigable.
- **Permanent event id + separate stable question key, status derived.** CHOSEN.

## Consequences
Records gain a `question` field (backfilled across the genesis ledger). The index exposes `live`/`effective_status` and groups records by question.

## Revisit-if
The split proves confusing or unnecessary once the ledger has real reversal chains.

---
id:            DEC-records-stay-put
question:      "records-stay-put"
title:         "Records never move and ids never change once anything cites them"
status:        accepted
binding:       true
kind:          engineering
areas:         ["method"]
decided_on:    "2026-08-29"
decision:      "A record file stays at its path and keeps its id for life. Per-area and principle organisation are DERIVED views computed by the index, never physical folders that records are relocated into."
confidence:    high
human_input:   true
human_crux:    "Pranav's reasoning from a real event: commit messages are immutable and already cite reports/ paths, so relocating records to a decisions/ folder would strand those citations. Physical stability over tidy foldering — and it keeps the retrofit continuous, with no visible break in how decisions were recorded."
supersedes:    []
refines:       []
governed_by:   []
depends_on:    []
cites:         ["the Steelyard reference implementation"]
enforced_by:   null
revisit:       ["none | any surface that can cite a record but not be edited later makes its path load-bearing forever"]
---

## Question
Should records be reorganised into per-area folders for navigation, or stay where they are?

## Decision
Stay put. Navigation comes from the generated index (per-area and principle views), so records never need to move — and moving would break the citations that immutable surfaces (commit messages, published artifacts, other records) already hold.

## Human reasoning
Pranav hit this in practice: on the reference project a move to a `decisions/` directory was rejected precisely because commit messages already cited `reports/...` paths and can't be edited. The general rule followed: any surface that can cite a record but cannot be edited later makes the record's path and id public API — permanent. It also keeps the record trail continuous, with no before/after break in recording style.

## Why
The moment any immutable surface cites a record — a commit message, a published artifact, another record — the record's path and id become load-bearing public API. A move invalidates those references irreversibly, whereas a generated index delivers the same per-area navigability at zero citation cost. The cheap failure is a less tidy folder; the expensive one is a stranded citation that can never be repaired.

## Options considered
- **Relocate records into per-area folders.** REJECTED (class: principle) — strands immutable citations; per-area is a derived view instead.
- **Records stay put; views are derived.** CHOSEN.

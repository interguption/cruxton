---
id:            DEC-index-is-generated
question:      "index-is-generated"
title:         "The index is generated from outbound-only edges, never hand-maintained"
status:        accepted
binding:       false
kind:          engineering
areas:         ["method"]
decided_on:    "2026-08-29"
decision:      "Records carry only outbound edges (supersedes, refines, governed_by, depends_on, cites), authored once and frozen. All reverse edges, clusters, per-area and principle views, and staleness queues are computed by a generator/validator that is a build artifact — never a hand-written file."
confidence:    high
human_input:   false
human_crux:    ""
supersedes:    []
refines:       []
governed_by:   ["DEC-record-id-scheme"]
depends_on:    []
cites:         ["the Steelyard reference implementation"]
enforced_by:   "scripts/decision_index.py"
revisit:       ["internal | the index outgrows a single file and needs sharding"]
---

## Question
How do records reference each other without the maintenance nightmare of two-way links?

## Decision
One direction only. A record declares its outbound edges when authored; the reverse direction ("cited by", "superseded by", clusters) is derived by regenerating the index. No old file is ever edited because a new one references it.

## Why
Hand-maintained bidirectional links are the Xanadu trap — every target must know its inbound links, and they drift. Academic citation plus Google Scholar is the model: papers cite their references (frozen); "cited by N" is computed. A generated index cannot drift, and it lints — failing the build on dangling citations, cycles, or missing kind-gated fields.

## Options considered
- **Hand-maintained backlinks in every file.** REJECTED (class: principle) — unmaintainable at scale; the exact churn to avoid.
- **A single hand-written index file.** REJECTED — goes stale silently.
- **Outbound edges + a generated, verified index.** CHOSEN.

<!-- touch -->

---
id:            DEC-record-id-scheme
title:         "Record ids are permanent slugs that name the question; area is separate metadata"
status:        accepted
binding:       false
kind:          engineering
areas:         ["method"]
decided_on:    "2026-08-29"
decision:      "Each record's id is a global, permanent slug (DEC-<slug>) that names the QUESTION, never the answer. The area is separate multi-valued metadata, never baked into the id."
confidence:    high
human_input:   false
human_crux:    ""
supersedes:    []
refines:       []
governed_by:   []
depends_on:    []
cites:         ["the Steelyard reference implementation"]
enforced_by:   null
revisit:       ["internal | slugs prove to collide semantically often enough to need a central allocator"]
---

## Question
How are decisions identified, so citations never break and the id never lies?

## Decision
A permanent slug that names the question. `DEC-optimization-lens-color`, not `DEC-optimization-achromatic` — the question survives every reversal; the answer does not. Area is a separate tag.

## Why
An id does three jobs — cite, locate, categorise — with opposite requirements: a citation key must never change, a locator/category must change when areas are renamed. A global monotonic integer collides on parallel authoring and carries no meaning; a per-area prefix orphans on rename. Decoupling them (permanent slug + area tag + derived index) is the only scheme that satisfies all three. Like an ISBN versus a shelf: reshelving never changes the ISBN.

## Options considered
- **Global monotonic integers.** REJECTED (class: principle) — parallel authors collide; no semantic locality.
- **Per-area prefixes (MARKER-D1).** REJECTED (class: principle) — orphaned when an area is renamed or split.
- **Permanent slug naming the question + separate area tag.** CHOSEN.

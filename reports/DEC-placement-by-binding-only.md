---
id:            DEC-placement-by-binding-only
question:      "placement-by-binding-only"
title:         "The constitution is binding records only — cross-cutting-ness does not promote"
status:        accepted
binding:       false
kind:          engineering
areas:         ["method"]
decided_on:    "2026-08-29"
decision:      "A record joins the read-first principles view only if binding: true (an invariant the repo must never violate). Touching several areas does NOT promote a record; that is carried by its area tags and the per-area views."
confidence:    high
human_input:   false
human_crux:    ""
supersedes:    []
refines:       []
governed_by:   ["DEC-organizing-frame-pace-layering"]
depends_on:    []
cites:         ["the Steelyard reference implementation"]
enforced_by:   "scripts/decision_index.py placement rule"
revisit:       ["internal | the binding set grows large enough to need its own sub-tiering"]
---

## Question
What makes a record part of the constitution read first by every agent?

## Decision
Being `binding` — an invariant — and nothing else. An earlier "binding OR touches >= 2 areas" rule over-promoted ordinary multi-area decisions into the constitution and was corrected during the reference build.

## Why
A constitution's power is its brevity: past ~15-20 entries, "read it first, every time" stops happening and it is read by no one. Cross-cutting-ness is real but is captured by area tags and per-area views, not by promotion. Over-promotion is how a constitution grows until nobody reads it.

## Options considered
- **Principles = binding OR >= 2 areas.** REJECTED (class: constraint) — inflates the constitution with normal multi-area decisions.
- **Principles = binding only.** CHOSEN.

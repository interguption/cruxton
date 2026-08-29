---
id:            DEC-organizing-frame-pace-layering
title:         "Knowledge is organised by pace layering — every fact at the layer matching its rate of change"
status:        accepted
binding:       true
kind:          engineering
areas:         ["method"]
decided_on:    "2026-08-29"
decision:      "Every fact lives at exactly one layer chosen by how fast it changes (purpose > principles > decisions > runbooks > code); faster layers cite slower ones and never restate them."
confidence:    high
human_input:   false
human_crux:    ""
supersedes:    []
refines:       []
governed_by:   []
depends_on:    []
cites:         ["the Steelyard reference implementation"]
enforced_by:   null
revisit:       ["none | the organising principle of the whole system"]
---

## Question
How do we keep the system lean while capturing the maximum, without duplication or drift?

## Decision
Sort information by rate of change into layers; each fact lives at exactly one layer; faster layers cite slower ones rather than copying them. Leanness comes from never duplicating across layers and never recording the ephemeral.

## Why
Maximal capture and leanness stop being in tension the moment you sort by rate of change: a code detail never sits in a principle (it would rot), a principle never names a filename (it would leak a fast fact into a slow layer). The generated index substitutes for copying. This is Stewart Brand's pace layering, and software's Stable Dependencies Principle (depend toward stability).

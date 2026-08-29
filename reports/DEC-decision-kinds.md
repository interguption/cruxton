---
id:            DEC-decision-kinds
title:         "Every record has a kind — engineering, stance, or design — set by who adjudicates it"
status:        accepted
binding:       false
kind:          engineering
areas:         ["method"]
decided_on:    "2026-08-29"
decision:      "A record's kind is engineering (internal goals adjudicate), stance (external contested evidence adjudicates — unlocks required evidence_basis, evidence_level, lineage, contested), or design (product values adjudicate — requires a reversal_ritual). One question assigns it: who decides whether this is right?"
confidence:    high
human_input:   false
human_crux:    ""
supersedes:    []
refines:       []
governed_by:   []
depends_on:    []
cites:         ["the Steelyard reference implementation"]
enforced_by:   "generator validates kind-gated required fields"
revisit:       ["internal | a fourth adjudicator appears that none of the three names"]
---

## Question
Do all decisions have the same shape, or does the kind of truth they answer to change what a record must carry?

## Decision
Three kinds by adjudicator. Only `stance` unlocks the evidence machinery; only `design` requires a reversal ritual; `engineering` uses the generic core. The tie-breakers: if it needs the evidence machinery it's a stance whatever its surface topic; if reversing it forces a cross-surface consistency sweep it's design.

## Why
An engineering decision is true relative to internal goals and settleable in-house; a stance is a bet on contested external reality that must expose its evidence and lineage; a design decision is adjudicated by taste against a stated aesthetic and is costly to flip-flop. Conflating them lets a contested claim wear the costume of a settled choice — the failure the evidence fields prevent.

## Options considered
- **One uniform record shape.** REJECTED — a contested medical stance would look as settled as a file-naming call.
- **Separate file types per kind.** REJECTED — many decisions are both (a schema is engineering; each assignment is a stance); a shared skeleton is what makes the method portable.
- **One record type, a `kind` discriminator that unlocks fields.** CHOSEN.

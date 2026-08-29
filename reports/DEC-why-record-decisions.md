---
id:            DEC-why-record-decisions
title:         "Why a repo keeps a decision trail at all"
status:        accepted
binding:       true
kind:          engineering
areas:         ["method"]
decided_on:    "2026-08-29"
decision:      "A repo records its non-trivial decisions as a durable trail so no one re-runs a settled thought process, an overturn can read the full prior reasoning, agents avoid dead ends and find under-explored paths, and the reasoning survives the conversation it was made in."
confidence:    high
human_input:   true
human_crux:    "PS's reasons for wanting this: stop re-litigating cleared decisions; be able to overturn only after reading the whole trail; let any agent avoid failed paths and pick up promising ones; stop re-researching in future projects and depend on internal resources over the web; and build specificity on contested topics by writing the reasoning down."
supersedes:    []
refines:       []
governed_by:   []
depends_on:    []
cites:         ["the Steelyard reference implementation"]
enforced_by:   null
revisit:       ["none | this is the method's premise"]
---

## Question
Why maintain a decision trail instead of relying on memory, chat history, or git?

## Decision
Because the value a record holds is not re-derivable elsewhere. Git says what changed and when; chat evaporates; memory is lossy. A record holds what was chosen, why, what was rejected, and the human reasoning behind it.

## Human reasoning
PS's motivation, stated across the design: cleared decisions shouldn't be re-argued; overturning something should require reading the trail of rejections and confirmations first; agents should avoid what already failed and explore what showed promise; and — the part no machine supplies — future projects shouldn't re-research what was already settled, especially on contested topics like health where the reasoning is the specificity.

## Why
A decision log and an audit trail answer different questions. This system is the reasoning layer; git remains the audit layer.

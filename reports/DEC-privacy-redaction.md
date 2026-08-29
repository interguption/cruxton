---
id:            DEC-privacy-redaction
question:      "privacy-redaction"
title:         "Records never carry secrets, personal data, or verbatim private conversations"
status:        accepted
binding:       true
kind:          engineering
areas:         ["method"]
decided_on:    "2026-08-29"
decision:      "A record captures reasoning, never raw sensitive material: no secrets, credentials, keys, PII, health data, protected-class attributes, confidential third-party information, or verbatim private conversations. Sensitive human input is reduced to the decision-relevant gist; anything that needs sensitive material to understand is cited to an access-controlled location."
confidence:    high
human_input:   false
human_crux:    ""
supersedes:    []
refines:       []
governed_by:   []
depends_on:    []
cites:         ["external adversarial readiness review, 2026-08-29"]
enforced_by:   null
revisit:       ["none | a committed, possibly-public trail must never leak sensitive material"]
---

## Question
Cruxton actively harvests human reasoning, org constraints, and conversation-derived input. What must never enter a record?

## Decision
Anything sensitive. Records are committed and may become public, so they hold the decision-relevant reasoning only — never secrets, PII, health data, protected-class attributes, confidential business information, or verbatim private conversation. Redaction is the author's responsibility; the generator cannot detect a leaked secret.

## Why
The very thing that makes Cruxton valuable — writing down the human, subjective, and organizational reasoning behind a call — is also the thing most likely to pull sensitive material into a durable, shareable file. A public method that encourages this without a boundary is a leak waiting to happen. Making the boundary explicit and binding is the cheapest possible safeguard.

## Options considered
- **Silence (assume authors self-censor).** REJECTED (class: principle) — a public tool must state the boundary, not assume it.
- **A binding never-record rule, mirrored into every agent pointer.** CHOSEN.

## Consequences
The spec, SKILL.md, and the CLAUDE.md/AGENTS.md pointers all carry the never-record rule.

## Revisit-if
Never — this is an invariant of a committed, possibly-public trail.

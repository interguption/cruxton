---
id:            DEC-public-positioning
question:      "public-positioning"
title:         "Cruxton is positioned as the repo-native decision layer agents must consult"
status:        accepted
binding:       false
kind:          design
areas:         ["method"]
decided_on:    "2026-08-30"
decision:      "Cruxton's public surfaces lead with the pain of agents reopening settled decisions, position it as a narrow repo-native decision layer rather than generic agent memory, and make non-derivable human reasoning the central differentiator; proof precedes methodology."
confidence:    high
human_input:   true
human_crux:    "PS chose narrowness as the brand: Cruxton should own the decision layer agents are required to consult, with the human reasoning they cannot reconstruct at its center, rather than compete as another system that remembers everything."
reversal_ritual: "Sweep the README hero and section order, demo story, GitHub description and topics, social preview, install framing, and launch copy together so every public surface makes the same promise."
supersedes:    []
refines:       []
governed_by:   ["DEC-why-record-decisions"]
depends_on:    ["DEC-why-has-three-layers"]
cites:         []
enforced_by:   null
revisit:       ["values | users consistently understand or adopt Cruxton better under a broader category than the narrow decision-layer framing"]
---

## Question
How should Cruxton explain itself publicly so a new visitor understands its value before learning the method?

## Decision
Lead with the concrete failure: coding agents confidently reopen decisions a team already settled. Position Cruxton as the small, git-native decision layer agents are required to consult—not a system that remembers every session, preference, or code fact. Make its scarce payload explicit: what was rejected and the human reasoning an agent cannot reconstruct. Show that outcome before explaining pace layering, edge derivation, decision kinds, or the complete record contract.

## Human reasoning
PS accepted the launch read that Cruxton's narrowness is its brand. The valuable category is not broad agent memory; it is the set of decisions an agent must not casually make again. PS also chose the non-derivable human crux as the intellectual center because it is the part neither git nor a future model can recreate from the code.

## Why
"Agent memory" is broad enough to imply session recall, embeddings, code retrieval, preferences, databases, and infrastructure Cruxton intentionally does not provide. That frame makes a small plain-Markdown method look incomplete. The decision-layer frame makes the same narrow scope a strength: Cruxton preserves exactly the reasoning whose loss causes agents to repeat rejected work. A pain-first opening earns enough attention for the deeper method to matter, while an authentic demonstration and this repo's own ledger prove the claim without feature inflation.

## Options considered
- **Lead with a portable decision-records system.** REJECTED (class: values) — accurate but conceptual; it asks a visitor to understand the mechanism before feeling the problem.
- **Compete as persistent agent memory.** REJECTED (class: values) — suggests a much broader product, obscures the mandatory-consultation behavior, and makes narrowness look like missing functionality.
- **Lead with re-litigation, then show the repo-native decision layer and human crux.** CHOSEN — immediate pain, precise category, distinctive payload, and an honest scope.

## Consequences
The README, repository metadata, social preview, demo, and launch copy use the same pain-first language. Technical depth remains in the README, but below the outcome and proof. Public material does not imply session memory, automatic semantic retrieval, embeddings, or a service Cruxton does not ship.

## Revisit-if
Revisit only if sustained user evidence shows that the broader memory framing produces materially better understanding and adoption without creating false expectations about Cruxton's scope.

## Reasoning provenance
- The choice to make narrowness the brand and human reasoning the center came from PS's adoption of the launch direction — `human-expertise`.
- The distinction between re-derivable logic and non-derivable human input is established by `DEC-why-has-three-layers` — `internal-finding`.
- The pain of settled decisions being reopened is the binding premise in `DEC-why-record-decisions` — `internal-finding`.

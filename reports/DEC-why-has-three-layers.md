---
id:            DEC-why-has-three-layers
question:      "why-has-three-layers"
title:         "A record's 'why' has three layers, and non-derivable human reasoning rides at the top"
status:        accepted
binding:       false
kind:          engineering
areas:         ["method"]
decided_on:    "2026-08-29"
decision:      "Reasoning is captured at three depths by how re-derivable it is: a one-line human_crux plus a human_input flag in the index (read every time); a Human reasoning body section (read on open); and a deep Reasoning provenance section tagging each material claim by source (read on demand). Provenance types: llm-expertise, internal-finding, external-research, provided-data, human-expertise, human-instinct, human-constraint."
confidence:    high
human_input:   true
human_crux:    "Pranav's core addition: capture the human/subjective reasoning a machine cannot re-derive — instinct, a market read, an org constraint — and surface it high, so an agent won't confidently re-derive a decision whose real driver was human judgment. Machine logic is the re-derivable part; the human part is the scarce one."
supersedes:    []
refines:       ["DEC-decision-kinds"]
governed_by:   []
depends_on:    []
cites:         ["the Steelyard reference implementation"]
enforced_by:   null
revisit:       ["internal | the provenance taxonomy proves to miss a source class"]
---

## Question
How is the reasoning behind a decision captured — especially the human part a machine can't reconstruct?

## Decision
Three layers by re-derivability. The non-derivable human input rides at the very top as a `human_crux` the index lifts, so any agent is warned before it re-derives or overturns. The machine `Why` and the fine-grained provenance tagging sit deeper, read on demand.

## Human reasoning
Pranav pressed the point that machine logic is the obvious, always-re-derivable layer, while a human's instinct, field knowledge, or organizational constraint is exactly what evaporates when a conversation ends — and is exactly what an agent working from logic alone will get wrong. So the format must make that non-derivable input first-class and high-visibility, present when a person shaped the decision, thin or absent when an agent decided alone.

## Why
This extends the stance kind's evidence machinery to all reasoning, including human-origin reasoning that has no external citation. The `human_crux` is the one-line lift of whichever human input actually moved the decision.

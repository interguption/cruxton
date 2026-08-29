---
id:            DEC-decisions-md-presentation
question:      "decisions-md-presentation"
title:         "The human ledger reads principles-first, decision and crux inline, live separated from superseded"
status:        accepted
binding:       false
kind:          design
areas:         ["method"]
decided_on:    "2026-08-29"
decision:      "DECISIONS.md leads with the constitution (binding, live principles), shows each record's one-line decision, confidence, and human crux with a link to the record file, groups clusters and per-area views, and separates live decisions from a superseded historical trail."
confidence:    high
human_input:   false
human_crux:    ""
reversal_ritual: "Any change to the ledger's presentation must be re-rendered and swept across every generated view — DECISIONS.md, the per-area lists, and the queues — so the human and machine reads never diverge."
supersedes:    []
refines:       []
governed_by:   ["DEC-organizing-frame-pace-layering", "DEC-index-is-generated"]
depends_on:    []
cites:         ["external adversarial readiness review, 2026-08-29"]
enforced_by:   "scripts/decision_index.py write_human()"
revisit:       ["values | reviewers report the ledger buries what matters or is hard to scan"]
---

## Question
How should the generated human ledger present the trail so a reviewer — or an LLM answering "why was X decided?" — can actually use it?

## Decision
Principles first, then clusters, then per-area, then the human-judgment queue, then a separate superseded trail. Each entry carries its one-line decision, kind/status, confidence, a link to the record file, and its human crux when present.

## Why
An external review noted the ledger listed titles and cruxes but not the decisions themselves or links to the records, so attaching only DECISIONS.md could not answer "why was X decided?" Surfacing the one-line decision and a file link makes the ledger far more self-contained, while separating live from superseded keeps a reader from mistaking overturned decisions for current ones. This is a taste/values call about how the trail reads, so it is a design record with a consistency-sweep reversal ritual.

## Options considered
- **Titles + crux only (original).** REJECTED (class: values) — not self-contained; can't answer "why" alone.
- **Decision + link + crux, live separated from superseded.** CHOSEN.

## Consequences
The ChatGPT/reviewer path can rely on DECISIONS.md plus the linked records to answer "why".

## Revisit-if
Reviewers find the ledger hard to scan or that it buries what matters.

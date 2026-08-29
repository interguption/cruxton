---
id:            DEC-cross-tool-pointer
question:      "cross-tool-pointer"
title:         "Cruxton bets on AGENTS.md as the cross-tool agent-instruction convention"
status:        accepted
binding:       false
kind:          stance
areas:         ["method"]
decided_on:    "2026-08-29"
decision:      "The bootstrap emits an AGENTS.md pointer alongside CLAUDE.md so that Codex, Cursor, Gemini CLI, Copilot, Windsurf and other agents obey the same spec — betting that AGENTS.md is the convergent cross-tool instruction convention."
confidence:    moderate
human_input:   false
human_crux:    ""
evidence_basis:  predictive
evidence_level:  expert-opinion
lineage:         "AGENTS.md / Agentic AI Foundation"
contested:       true
contested_note:  "Competing conventions exist — CLAUDE.md, Cursor rules, GEMINI.md — and none is a ratified standard; adoption is broad but young, and tools can change what file they read."
supersedes:    []
refines:       []
governed_by:   []
depends_on:    []
cites:         ["AGENTS.md adoption reporting, 2026 — Codex, Cursor, Gemini CLI, Copilot, Windsurf, Aider, Zed"]
enforced_by:   "bootstrap.py emits AGENTS.md and CLAUDE.md"
revisit:       ["evidence | AGENTS.md adoption stalls or fragments, or a rival convention becomes dominant", "internal | a tool we target stops reading AGENTS.md"]
---

## Question
How does one spec bind agents across tools that each read a different instruction file?

## Decision
Emit AGENTS.md (read by 30+ agents) in addition to CLAUDE.md, both pointing at the single contract. Bet on AGENTS.md as the convergent convention rather than shipping a per-tool file for each vendor.

## Why
The method's substance is tool-agnostic; only the pointer differs per tool. AGENTS.md is read natively by a large and growing set of agents and is stewarded as a neutral convention, so one extra generated file covers most of the ecosystem. This is a bet on an external, still-evolving standard, not an internally settled fact — hence a stance with an evidence-class revisit trigger.

## Options considered
- **CLAUDE.md only.** REJECTED (class: constraint) — binds only Claude Code; the cross-tool promise fails.
- **A hand-maintained pointer per vendor.** REJECTED (class: constraint) — unbounded upkeep as tools proliferate.
- **AGENTS.md + CLAUDE.md, betting on convergence.** CHOSEN.

## Consequences
Bootstrap writes both pointers and keeps them in lockstep; the bet is revisited if adoption moves.

## Revisit-if
AGENTS.md adoption stalls or fragments, or a targeted tool stops reading it.

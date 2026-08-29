---
id:            DEC-distribute-as-plugin
question:      "distribute-as-plugin"
title:         "Cruxton ships as a Claude Code plugin with the bundle under skills/"
status:        accepted
binding:       false
kind:          engineering
areas:         ["method"]
decided_on:    "2026-08-29"
decision:      "The distributable machinery (SKILL.md, bootstrap.py, METHOD-VERSION, templates/) is packaged as a Claude Code plugin under skills/cruxton-decision-records/, installable in one command; the repo's own self-governing files (scripts/decision_index.py, reports/, instructions/, CLAUDE.md, AGENTS.md) stay at root."
confidence:    high
human_input:   false
human_crux:    ""
supersedes:    []
refines:       ["DEC-distribution-central-mutable-method"]
governed_by:   []
depends_on:    []
cites:         [".claude-plugin/plugin.json", "skills/cruxton-decision-records/SKILL.md"]
enforced_by:   null
revisit:       ["internal | Claude Code changes plugin/skill discovery, or a better one-command install path emerges"]
---

## Question
How is the central, mutable method delivered so a user can install it in one command, without the skill bundle depending on a fixed path on one machine?

## Decision
Package the bundle as a Claude Code plugin. The distributable machinery moves into `skills/cruxton-decision-records/` (SKILL.md, bootstrap.py, METHOD-VERSION, templates/), which Claude Code auto-discovers via `.claude-plugin/plugin.json`. The repo's OWN self-governing files stay at root, so the repo keeps dogfooding the method (`scripts/decision_index.py`, `reports/`, `instructions/`, root `CLAUDE.md`/`AGENTS.md`). Because `bootstrap.py` resolves its inputs relatively (`METHOD = Path(__file__).parent`), moving it together with `METHOD-VERSION` and `templates/` needs no code change; the self-check still prints `SELF-CHECK PASSED` from the new location.

## Why
`DEC-distribution-central-mutable-method` settled that the method is a thin skill over a central mutable source, and flagged that the central source should become machine-independent rather than a bare local folder. The plugin makes the public git repo that source and gives Claude Code users a one-command install (`/plugin marketplace add …` → `/plugin install …`), which is the highest-leverage adoption path. Keeping the bundle self-contained under `skills/` (no hardcoded personal path) is what makes it portable; keeping the repo's own machinery at root is what keeps the method governing itself. The single canonical generator is `skills/cruxton-decision-records/templates/decision_index.py` (what bootstrap copies into a target); the root `scripts/decision_index.py` is the repo's working copy and is held byte-identical to it, so there is one source of truth, not two that can drift.

## Options considered
- **Keep the bundle at repo root (pre-plugin layout).** REJECTED (class: constraint) — no one-command install, and Claude Code discovers skills under `skills/<name>/`, not root.
- **A fat, self-contained skill with machinery inlined in prose.** REJECTED (class: constraint) — already rejected by `DEC-distribution-central-mutable-method`; scripts don't belong in prose and can't be tested.
- **Plugin bundle under `skills/cruxton-decision-records/`, repo's own files at root.** CHOSEN — one-command install, portable bundle, and the repo still dogfoods the method.

## Consequences
`.claude-plugin/plugin.json` declares the plugin; the bundle is self-describing (carries its own METHOD-VERSION). The two copies of the generator must be kept identical (a verify-gate `diff`). A claude.ai zip and other install paths are built from this same `skills/` bundle (Phase B).

## Revisit-if
Claude Code changes how plugins or skills are discovered, or a materially simpler one-command install path emerges.

---
id:            DEC-repo-is-its-own-marketplace
question:      "repo-is-its-own-marketplace"
title:         "The Cruxton repo is its own single-plugin marketplace (source \"./\")"
status:        accepted
binding:       false
kind:          engineering
areas:         ["method"]
decided_on:    "2026-08-29"
decision:      "The repo carries its own .claude-plugin/marketplace.json listing the single cruxton-decision-records plugin with source \"./\", so one repo is both the marketplace and the plugin — no separate marketplace repo."
confidence:    high
human_input:   false
human_crux:    ""
supersedes:    []
refines:       ["DEC-distribute-as-plugin"]
governed_by:   []
depends_on:    []
cites:         [".claude-plugin/marketplace.json"]
enforced_by:   null
revisit:       ["internal | the bundle grows beyond one plugin and wants per-plugin subfolders under ./plugins/"]
---

## Question
Where does the plugin's marketplace manifest live — in this repo, or in a separate marketplace repo?

## Decision
This repo is its own marketplace. `.claude-plugin/marketplace.json` sits at the repo root, names the marketplace `cruxton`, and lists one plugin (`cruxton-decision-records`) whose `source` is `"./"` — the repo root. Install is `/plugin marketplace add interguption/cruxton` then `/plugin install cruxton-decision-records@cruxton`.

## Why
There is exactly one plugin, and it is this repo. A separate marketplace repo would add a second thing to publish, version, and keep in sync for no benefit at this scale. Co-locating the marketplace with the plugin makes the install a single `owner/repo` reference and keeps the whole distribution in one commit history. `source: "./"` points the marketplace entry at the repo root, where `.claude-plugin/plugin.json` and the `skills/` bundle already live.

## Options considered
- **A separate marketplace repo listing this plugin.** REJECTED (class: constraint) — a second repo to maintain and sync, unjustified for a single plugin.
- **Repo is its own marketplace, `source: "./"`.** CHOSEN — one repo, one reference, one history.

## Consequences
Adding a second plugin later would mean moving each plugin into its own subfolder and switching `source` to per-plugin paths under `./plugins/` — the trigger recorded in `revisit`.

## Revisit-if
The bundle grows beyond one plugin and wants per-plugin subfolders under `./plugins/`.

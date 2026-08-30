---
id:            DEC-ledger-title-source
question:      "ledger-title-source"
title:         "The DECISIONS.md title comes from a committed name file, never the checkout path"
status:        accepted
binding:       false
kind:          engineering
areas:         ["method"]
decided_on:    "2026-08-30"
decision:      "The generated ledger title reads its project name from a committed .decision-records-name file (bootstrap seeds it with the repo folder name; a human may edit it), and falls back to a neutral 'Decisions (generated)' when absent — it is never derived from the live checkout directory name."
confidence:    high
human_input:   true
human_crux:    "PS chose to keep the project name in the ledger title via a committed config, rather than drop the name for a neutral title, when the two options were put side by side."
supersedes:    []
refines:       ["DEC-deterministic-artifacts", "DEC-decisions-md-presentation"]
governed_by:   []
depends_on:    []
cites:         ["scripts/decision_index.py project_name()/write_human", "skills/cruxton-decision-records/bootstrap.py (.decision-records-name step)"]
enforced_by:   "scripts/decision_index.py --check (CI)"
revisit:       ["internal | a deterministic project-name source better than a committed dotfile emerges"]
---

## Question
Where does the human ledger (`reports/DECISIONS.md`) get its title's project name, so the generated file is byte-identical no matter where the repo is checked out?

## Decision
The generator reads the project name from a **committed** file, `.decision-records-name`, and uses it as `# <name> — Decisions (generated)`. `bootstrap.py` writes that file once at setup (default: the target repo's folder name) and never clobbers it, so a human can rename the ledger by editing one line. When the file is absent the title falls back to a neutral, path-independent `# Decisions (generated)`. The title is **never** derived from the live checkout directory name.

## Human reasoning
Offered the choice between dropping the name for a fully neutral title and keeping the project name via a small committed config, PS chose to keep the name — the flagship's ledger should still read "Cruxton". The determinism requirement is not negotiable; the config is the mechanism that satisfies both keeping a name and staying deterministic.

## Why
The previous generator built the title from `REPO.name`, the checkout **folder** name. That is environment-dependent: locally the folder was `Cruxton`, but GitHub Actions checks out to `…/cruxton/cruxton`, so the generator produced a differently-cased title and `--check` reported `DECISIONS.md` STALE — a red CI on the first push, and a latent failure for every downstream repo whose local folder name differs in case or spelling from GitHub's lowercase checkout path. This silently violated `DEC-deterministic-artifacts` ("a no-op regeneration produces no diff"). Sourcing the name from a committed file makes the title a property of the repo's content, not its location, so regeneration is identical everywhere — restoring the invariant while still letting each repo name its own ledger. The JSON index and `input_hash` were already path-independent, which is why only `DECISIONS.md` was affected.

## Options considered
- **Derive the title from the checkout folder name (`REPO.name`).** REJECTED (class: principle) — environment-dependent; breaks `DEC-deterministic-artifacts` and CI.
- **Drop the name entirely; fixed neutral title.** REJECTED (class: constraint) — deterministic, but the ledger loses its project identity, which PS wanted to keep.
- **Read the name from a committed `.decision-records-name` (this decision).** CHOSEN — deterministic and per-repo nameable; bootstrap seeds it, a human can edit it, neutral fallback if missing.

## Consequences
Bootstrap gains a write-once `.decision-records-name` step; the file is committed like `.decision-records-version`. Existing repos bootstrapped before this fix upgrade by re-running bootstrap (which writes the file) and regenerating. This is part of the re-cut v1.0.0, not a version bump.

## Revisit-if
A deterministic project-name source cleaner than a committed dotfile emerges (e.g. a single method-config file the generator already reads).

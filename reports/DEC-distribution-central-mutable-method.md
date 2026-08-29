---
id:            DEC-distribution-central-mutable-method
question:      "distribution-central-mutable-method"
title:         "The method is distributed as a thin skill over a central, mutable method repo"
status:        accepted
binding:       false
kind:          engineering
areas:         ["method"]
decided_on:    "2026-08-29"
decision:      "The system is packaged as a thin skill whose bootstrap runs from a central method repo that carries the machinery, templates, and genesis ledger. Improvements are made once in the method repo and flow to future setups; the method versions itself so a repo can tell what it was scaffolded from."
confidence:    high
human_input:   true
human_crux:    "PS's proposal: don't cram everything into a giant skill file — point a thin skill at a fixed central location that holds the pre-written machinery, so setup is fast and improvements are made centrally and inherited by every future project."
supersedes:    []
refines:       []
governed_by:   []
depends_on:    []
cites:         ["the Steelyard reference implementation"]
enforced_by:   "bootstrap.py self-check; METHOD-VERSION stamp"
revisit:       ["internal | the machinery outgrows a folder and wants a git-remote template with CI"]
---

## Question
How is the method distributed so it is durable, repeatable verbatim, and centrally improvable — without depending on any one conversation?

## Decision
A thin skill over a central method repo. The repo holds templates, the generator, the bootstrap, and this genesis ledger; the skill drives setup from it. Setup is executed and self-verified, not transcribed, so it can't be done wrong. Central mutability holds with one discipline: improve the method repo, not a project's copy.

## Human reasoning
PS proposed pointing a thin skill at a fixed central location rather than embedding everything in skill text, so most of the work is pre-written and setup is fast. The honest caveat carried into the design: setups are snapshots (a repo upgrades by re-running bootstrap), and the central location should become a git remote to be machine-independent — a bare local folder traps mutability on one machine.

## Why
Pre-writing the machinery in one place makes setup fast and repeatable verbatim, and centralising improvements means every future repo inherits a fix without a manual port. Running the generator as a self-check makes "installed correctly" verifiable rather than assumed. A per-project copy forks and drifts (the exact failure the method exists to kill); inlining scripts in skill prose buries machinery where it can't be tested.

## Options considered
- **A fat self-contained skill (all machinery inline).** VIABLE but unwieldy; scripts don't belong in prose.
- **A thin skill pointing at a bare local folder.** REJECTED (class: constraint) — machine-trapped; revisit via a git remote.
- **A thin skill over a central, git-versioned method repo.** CHOSEN.

---
id:            DEC-bootstrap-safety
question:      "bootstrap-safety"
title:         "Bootstrap is non-destructive, atomic, and honest about failure"
status:        accepted
binding:       false
kind:          engineering
areas:         ["method"]
decided_on:    "2026-08-29"
decision:      "Bootstrap writes only files it owns (marked cruxton-managed) or that do not yet exist; a foreign same-named file is a refused collision, not an overwrite. Writes are atomic (temp + rename), and the self-check prints SELF-CHECK PASSED only when the generator exits 0 — a build-failing record yields an honest non-zero SETUP-OK-with-errors result instead."
confidence:    high
human_input:   false
human_crux:    ""
supersedes:    []
refines:       ["DEC-distribution-central-mutable-method"]
governed_by:   []
depends_on:    []
cites:         ["external adversarial readiness review, 2026-08-29"]
enforced_by:   "bootstrap.py (managed markers, collision refusal, exit-0-only pass)"
revisit:       ["internal | a stronger install contract is needed, e.g. transactional rollback"]
---

## Question
What must an installer guarantee before strangers run it on their own repositories?

## Decision
Three guarantees: it never overwrites a file it does not own (collision detection with an explicit --force escape), it writes atomically, and it never reports success it cannot prove — SELF-CHECK PASSED requires the generator to exit 0.

## Why
A public bootstrap runs inside other people's repos; a silent overwrite or a false "PASSED" on a broken setup is the kind of harm that destroys trust on first use. An external review showed the old bootstrap printing PASSED on a build-failing repo and unconditionally overwriting a same-named script. Ownership markers plus an exit-0 gate make the installer both safe and truthful.

## Options considered
- **Unconditional overwrite + "it ran" == success (original).** REJECTED (class: constraint) — clobbers user files; reports false success.
- **Managed-marker ownership, atomic writes, exit-0-only pass, --dry-run/--force.** CHOSEN.

## Consequences
Bootstrap gains --dry-run, --force, and --upgrade-spec, and distinguishes "machinery installed" from "records valid."

## Revisit-if
A stronger transactional install contract becomes necessary.

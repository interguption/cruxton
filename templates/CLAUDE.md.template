# Claude Code guide — this repo

This repo records its decisions. Obey `instructions/DECISION-RECORDS.md`.

## Before you change anything
1. Read `reports/DECISIONS.md` — principles first (the constitution).
2. Grep `reports/DEC-*.md` for the subject you are about to touch. A record whose `revisit`
   class is `none` is principle-settled — do not re-litigate it. A record in the "carries
   human judgment" list rests on a call you cannot re-derive from logic — read it before
   overturning or building on it.
3. Cite what you touch: a new decision on a covered subject must `refines` or `supersedes`
   the live records on it, so a contradiction surfaces as an edge.

## When you settle a decision
File a record (`instructions/DECISION-RECORDS.md` gives the format and the when-to /
when-not-to), then regenerate and commit the index:

    python3 scripts/decision_index.py

## Never
Relocate a `reports/DEC-*.md` record or rename its `id` — commit messages and other records
cite those paths and ids, and they cannot be edited after the fact.

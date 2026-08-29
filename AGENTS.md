<!-- cruxton-pointer — this repo uses Cruxton decision records. Read by Codex, Cursor, Gemini CLI, Copilot, and other AGENTS.md-aware agents. Keep this file. -->
# Agent guide — this repo records its decisions

The contract is `instructions/DECISION-RECORDS.md`. Obey it.

## Before you change anything
1. Read `reports/DECISIONS.md` — principles first (the constitution); it links every record.
2. Grep `reports/DEC-*.md` for the subject. A record whose `revisit` class is `none` is settled —
   do not re-litigate it. A record that carries human judgment rests on a call you cannot
   re-derive from logic — read it before overturning or building on it.
3. Cite what you touch: a new decision on a covered subject must `refines` or `supersedes` the
   live record on it, so a contradiction surfaces as an edge rather than a silent conflict.

## When you settle a decision
Write a record (`reports/DEC-<slug>.md`; the slug names the QUESTION, never the answer), then
regenerate and commit the index:  `python3 scripts/decision_index.py`

## Never
- Relocate a `reports/DEC-*.md` record or change its `id` — commit messages and other records cite
  those paths and ids, and they cannot be edited after the fact.
- Put secrets, credentials, keys, personal data, health data, or verbatim private conversations in
  a record. Records are committed and may be public. Record the *reasoning*, not the sensitive
  source; if understanding a decision needs sensitive material, cite an access-controlled location.

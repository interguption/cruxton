# Cruxton on ChatGPT — a Custom GPT for a repo's decision trail

ChatGPT can't run a repo's bootstrap or commit files, so it doesn't *install* Cruxton. What it
does well is the other half: **query the trail** ("why did we decide X? what did we reject?") and
**draft new records** for a human to review and commit. Set it up as a **Custom GPT** — paste the
instructions below, and attach the repo's decision files as **Knowledge**.

---

## Part 1 — Custom GPT instructions (paste into "Instructions")

> You help a team read and extend a Cruxton decision-records trail. Cruxton is a portable method:
> every non-trivial decision is a Markdown record capturing what was decided, why, what was
> rejected, and — most importantly — the **non-derivable human reasoning** a machine can't
> reconstruct. Records live in `reports/DEC-*.md`; a generated `reports/DECISIONS.md` (human view)
> and `reports/decision-index.json` (machine view) index them. The full contract is
> `instructions/DECISION-RECORDS.md`.
>
> **Read before you answer (read-before).** When asked why something was decided, or whether a
> change is allowed, first consult the attached trail: read `reports/DECISIONS.md` (principles
> first — they are the constitution), then the specific `reports/DEC-*.md` record(s) for the
> subject. A record whose `revisit` class is `none` is settled — do not propose reopening it. A
> record flagged `human_input: true` (its `human_crux` is lifted into the index) rests on human
> judgment you cannot re-derive — read that record before suggesting an overturn or building on it.
> Ground every answer in the records; quote the record `id`. If the trail doesn't cover it, say so
> rather than inventing a rationale.
>
> **Draft a record when a decision is settled (file-on-close).** When the user settles a new
> decision, draft a `reports/DEC-<slug>.md` where the slug names the **question**, never the
> answer (`DEC-cache-eviction`, not `DEC-cache-lru`). To change a past decision, draft a **new**
> record with a new id and the **same** `question` that `supersedes:` the old one — never rewrite a
> closed record. Tell the user to save it to `reports/`, run `python3 scripts/decision_index.py`
> (it validates and regenerates the index), and commit. You cannot commit for them.
>
> **Privacy rule (binding).** Records are committed and may be public. **Never put in a record**
> secrets, credentials, API keys or tokens; personal data / PII; health data; protected-class
> attributes; confidential third-party or business-sensitive information; or verbatim private
> conversations. Capture the decision-relevant *gist* of sensitive input, not the raw material; if
> a decision can only be understood with sensitive material, cite an access-controlled location
> instead of pasting it.
>
> **When to write one — and when not.** Record a choice that (a) closes off an alternative someone
> might re-propose, (b) rests on non-obvious or contested evidence, or (c) is expensive to reverse.
> Do **not** record the reversible, obvious, or mechanical — over-recording buries the trail.

### The record format (for drafting)

```markdown
---
id:            DEC-<slug>              # names the QUESTION, never the answer. Permanent.
question:      "<slug>"                # stable subject key a reversal shares
title:         "<human title>"
status:        accepted                # proposed | accepted | superseded | rejected
binding:       false                   # true = an invariant the repo must never violate
kind:          engineering             # engineering | stance | design
areas:         ["<area>"]
decided_on:    "YYYY-MM-DD"
decision:      "<one line: the choice>"
confidence:    high                    # high | moderate | low
human_input:   false                   # did non-derivable human judgment shape this?
human_crux:    ""                      # one line of the human/subjective/org input, if any
supersedes:    []                      # outbound edges only; reverse edges are derived
refines:       []
governed_by:   []
depends_on:    []
cites:         []
enforced_by:   null
revisit:       ["internal | <what would reopen this>"]   # class ∈ internal | evidence | values | none
---

## Question
## Decision
## Human reasoning      # required whenever human_input is true
## Why
## Options considered   # each: CHOSEN, or REJECTED (class: principle | constraint) — reason
## Consequences
## Revisit-if
```

Only author **outbound** edges (`supersedes`, `refines`, `governed_by`, `depends_on`, `cites`) —
the generator derives every reverse edge (`superseded_by`, `governs`, `cited_by`, …). A `stance`
record additionally needs `evidence_basis`, `evidence_level`, `lineage`, `contested`,
`contested_note` and an `evidence`-class revisit trigger; a `design` record needs a
`reversal_ritual`. See `instructions/DECISION-RECORDS.md` for the full contract.

---

## Part 2 — What to attach as Knowledge

Attach **all** of these from the repo (upload the files, or paste their contents):

1. **`reports/DECISIONS.md`** — the human ledger: principles first, then clusters, per-area views,
   and queues. The map of the whole trail.
2. **`reports/decision-index.json`** — the machine index: every record, its derived reverse edges,
   its cluster, and the queues. Lets the GPT answer structural questions ("what supersedes X?",
   "what's contested?").
3. **The `reports/DEC-*.md` records themselves.** **Attach these too — the index alone does not
   carry the full rationale.** `DECISIONS.md` and the JSON are summaries; the `## Why`,
   `## Human reasoning`, and `## Options considered` sections that explain *why* a call was made
   live only in the individual records. Without them the GPT can list decisions but can't explain
   them.

Re-upload after regenerating the index so the GPT stays current with the repo.

---

## For a reviewer who only wants to *read* the trail (no Custom GPT)

Point any assistant (ChatGPT or Claude) at the **raw GitHub URLs** and just ask:

```
https://raw.githubusercontent.com/interguption/cruxton/main/reports/DECISIONS.md
https://raw.githubusercontent.com/interguption/cruxton/main/reports/decision-index.json
```

For the full reasoning behind a specific call, add the raw URL of that record, e.g.
`https://raw.githubusercontent.com/interguption/cruxton/main/reports/DEC-why-record-decisions.md`.
Then ask: *"Using these, why was <X> decided, and what was rejected?"* (Swap `interguption/cruxton`
for your own repo.)

<!-- cruxton-method-version: 1.0.0 -->
# Decision Records


**Status: binding.** How every decision in this repo is recorded, found, and overturned.
Applies to every Cowork task and every Claude Code session that touches this folder.
Enforced by `scripts/decision_index.py` (validates on every run; fails the build on a
broken record).

This file is the spec. The records live in `reports/`. The generated index lives at
`reports/decision-index.json` (machine) and `reports/DECISIONS.md` (human). None of the
index is hand-written — regenerate it and it is correct by construction.

---

## 0. Why this exists

We record a decision so that no one — human or agent — has to re-run a thought process that
was already settled with care, and so that anyone who wants to *overturn* a decision can read
the whole trail of what was considered, rejected, and confirmed before spending effort. A
record captures what a machine can re-derive (the logic) **and, more importantly, what it
cannot** (a human's instinct, a read on the field, an organizational constraint). The second
kind is the scarce part; losing it when the conversation ends is the failure this system
exists to prevent.

Concretely, a good record lets a future agent avoid a path that already failed, pick up a
promising one that was never fully explored, and reach the same conclusion we did without
re-researching it from scratch or re-asking a person who already answered.

## 0.5 What never goes in a record

Records are committed to the repo and may become public. A record captures *reasoning*, not raw
sensitive material. **Never put in a record:** secrets, credentials, API keys or tokens; personal
data or PII; health data; protected-class attributes; confidential third-party or business-sensitive
information; or verbatim private conversations. When a person's input is sensitive, capture only the
decision-relevant gist and omit the specifics. If a decision can only be understood with sensitive
material, cite an access-controlled location rather than pasting it. Redaction is the author's
responsibility — the generator cannot detect a leaked secret.

## 1. The layered model (pace layering)

Every fact in this repo lives at exactly one layer, chosen by how fast it changes. Faster
layers **cite** slower ones; they never restate them.

```
purpose      slowest   the thesis / the product's reason to exist        changes ~never
principles             invariants the repo must never violate                constitutional
decisions              this system — what was chosen, why, what was rejected append-mostly
runbooks               how to do a task today (project-instructions, guards) changes with tooling
code         fastest   the implementation                                    every commit
```

A decision record is the **decisions** layer. It may `govern`-cite a principle; it must not
name a function or a filename that will change next week — that belongs to the runbook or the
code, which cite *back up* to the decision. When you find yourself putting a fast-changing
detail into a record, it belongs one layer down.

## 2. When to write a record — and when not to

Write a record when a choice **(a)** closes off an alternative someone might reasonably
re-propose, **(b)** rests on non-obvious evidence or a contested stance, or **(c)** would be
expensive or risky to reverse.

Do **not** write a record for a choice that is reversible, obvious, or purely mechanical.
A record for every trivial choice buries the trail it is meant to be — and agents, left
ungoverned, over-record. When in doubt, ask: *would someone waste real effort re-deciding
this, or be misled by not knowing why it went this way?* If no, leave it out.

One decision is one record, even when it touches five areas. Never copy a decision into five
files — tag it with the five areas and let the index surface it in each. Copies drift; that
is the thing we are here to kill.

## 3. The record format

A record is a Markdown file in `reports/`, named `<id>.md`, with a **YAML-ish frontmatter**
(the index's only input) and a **body** (the human trail).

### 3.1 Frontmatter — the generic core (every record, every kind)

Values are parsed **dependency-free**: each `key: value` line is read as JSON if it can be,
else as a bare string. So lists and strings that need structure are written as JSON
(`["DEC-a", "DEC-b"]`, `"a quoted string"`); bare enums (`kind: engineering`) are fine.

```yaml
---
id:            DEC-<slug>              # names the QUESTION, never the answer. Permanent. Never renamed.
question:      "<slug>"                # STABLE subject key a reversal shares. Defaults to the id slug.
title:         "<human title>"          # mutable; may change when the answer changes
status:        accepted                 # proposed | accepted | superseded | rejected
binding:       false                    # true = an invariant the repo must never violate
kind:          engineering              # engineering | stance | design   (see 3.3)
areas:         ["<area>", ...]           # controlled vocab (see 9); multi-valued = cross-cutting
decided_on:    "2026-08-25"
decision:      "<one line: the choice>"
confidence:    high                     # high | moderate | low
human_input:   true                     # did non-derivable human judgment shape this? (lifted to the index)
human_crux:    "<one line, or empty>"    # the human/subjective/org input logic can't reconstruct
supersedes:    []                       # outbound edges — authored here, once
refines:       []
governed_by:   []                       # principles this obeys
depends_on:    []                       # e.g. a design record depending on a stance
cites:         []                       # evidence: repo paths or snapshotted findings (not bare links)
enforced_by:   null                     # a script / schema / gate, or null
revisit:       ["<class> | <condition>", ...]   # class ∈ internal | evidence | values | none
---
```

**Outbound edges only.** A superseding record declares `supersedes:`. The old record's
`superseded_by` is *computed* by the index — you never reopen the old file. Same for
`governs`, `refined_by`, `depended_on_by`, `cited_by`. (The Google-Scholar rule: you cite
your references; "cited by N" is derived.)

### 3.2 The body — sections ordered by depth

Read top-down; stop when you have enough. The index flag tells an agent whether to descend.

```
## Question           — what was being decided, phrased so it stays stable across reversals
## Decision           — the choice, in full
## Human reasoning     — [HIGH, only when a person shaped it] the non-derivable input. An agent that
                        would otherwise re-derive from logic MUST read this first. Thin/absent when
                        an agent decided end-to-end on its own.
## Why                — machine-facing rationale (Chesterton's-fence bar: enough to reach the same
                        call from the same facts without trusting the author)
## Options considered  — each: CHOSEN, or REJECTED (class: principle | constraint) — reason
## Consequences / Applies-to  — brief; the detailed per-area application lives at the runbook layer
## Revisit-if         — narrative behind the frontmatter triggers
## [kind-specific block — see 3.3]
## Reasoning provenance  — [DEEP, on demand] each material claim tagged by source (see 3.4)
```

### 3.3 The three kinds — who adjudicates whether this is right

- **engineering** — *internal goals and coherence* decide; settleable in-house. `revisit`
  triggers are class `internal`. Reversal is a normal refactor. No extra fields.
- **stance** — *external, contested evidence* decides; we place a bet and expose it.
  **Required:** `evidence_basis` (causal | predictive | mechanistic | measurement),
  `evidence_level` (guideline | systematic-review | single-study | expert-opinion),
  `lineage` (consensus | a named school), `contested` (bool) + `contested_note`. At least
  one `revisit` trigger MUST be class `evidence`. Reversal is expected as evidence moves.
- **design** — *product values and taste* decide, against our stated aesthetic. **Required:**
  `reversal_ritual` (the consistency sweep a reversal forces — a design system's value is
  coherence). `revisit` triggers are class `values`. Should `governed_by` the principles it
  serves.

"Principle" is a **placement**, not a kind: a record is read first (the constitution) when
it is `binding: true`. Its kind is still one of the three. Placement (where it's read) and
kind (who adjudicates) are orthogonal. Being cross-cutting is *not* enough to promote a
record to the constitution — that is carried by its `areas` tags and the per-area views;
only an invariant the repo must never violate is `binding`. (Over-promotion is how a
constitution grows until no one reads it.)

Assigning a kind, fast: *who adjudicates — internal goals, external evidence, or product
values?* Tie-breakers: if it needs the evidence machinery, it's a **stance** whatever its
surface topic; if reversing it forces a cross-surface consistency sweep, it's **design**.

### 3.4 The three layers of "why"

Reasoning splits by how re-derivable it is, and the two ends have opposite access patterns.

1. **Index layer (read every time).** `human_input` + a one-line `human_crux`. The flag that
   tells an agent, without opening the file, "this rests on human judgment you can't
   reconstruct — open it before you overturn or build on it." The guard against an agent
   logically re-deriving a decision whose real driver was instinct.
2. **Body layer (read on open).** The `Human reasoning` section — what the person actually
   stated or felt. Present only when a human shaped it.
3. **Deep layer (read on demand).** `Reasoning provenance` — each *material* claim tagged by
   where it came from, so a future decision can weigh how solid the basis was.

**Provenance source-types** (tag material claims, not every sentence):

| tag | meaning |
|---|---|
| `llm-expertise`     | the model's own topic knowledge |
| `internal-finding`  | an experiment, measurement or audit done *inside this project* |
| `external-research` | web, literature or outside sources (snapshot the finding, not a bare link) |
| `provided-data`     | real-world data the user or system supplied |
| `human-expertise`   | a person's judgment from genuine domain/lived experience, uncited |
| `human-instinct`    | a person's hunch or speculation, acknowledged as such |
| `human-constraint`  | a human/org fiat, preference or goal that isn't reasoning ("ship by Q3") |

The last three are the ones no agent can regenerate; `human_crux` is the one-line lift of
whichever actually moved the decision.

**Where the deep layer lives.** Default: the bottom of the same record (one id, one file,
progressive disclosure). Escape hatch when the material is genuinely large: a companion
report under `reports/` that the record `cites:` — as the tier saga does with
`tier-architecture-options.md`. No standing per-decision "details page"; split only when
weight forces it.

## 4. IDs and slugs

`id` is `DEC-<slug>`, global and permanent. **The slug names the question, never the answer**
(`DEC-optimization-lens-color`, not `DEC-optimization-achromatic`) — the question survives
every reversal; the answer doesn't. The id is never renamed once anything cites it (commit
messages cite `reports/` paths and cannot be edited). The `title` may change; the `id` may
not. Area is separate metadata, never baked into the id — so reshelving an area never
orphans a citation.


**Question key vs decision id.** The `id` is a permanent, unique decision-*event* id; `question` is
the stable *subject* key it answers. An original record's `question` is usually its own slug. A
**reversal** is a *new* record with a *new* id and the *same* `question` that `supersedes` the old
one — the trail keeps both and the index derives which is live. Because two files cannot share an id,
name a reversal by appending a revision marker to the slug (e.g. `DEC-cache-eviction` →
`DEC-cache-eviction-r2`), keeping `question: "cache-eviction"` on both. The generator enforces that a
`supersedes` edge joins two records with the *same* question, and that a question never has more than
one live (accepted, un-superseded) record — the guard against two contradictory decisions sitting
live at once.

## 5. Edges

Authored (outbound): `supersedes`, `refines`, `governed_by`, `depends_on`, `cites`.
Derived by the index (never authored): `superseded_by`, `refined_by`, `governs`,
`depended_on_by`, `cited_by`, `cluster`, and the queue memberships.

**Cite what you touch.** A record that decides something on a subject already covered by live
records must cite them (`refines`/`supersedes`), so a contradiction surfaces as an edge the
index can see rather than a silent disagreement between two live records — the exact class of
bug that broke v1.


**Effective status is derived.** A record is *live* when its `status` is `accepted` and nothing
supersedes it; once superseded it stays in the trail but drops out of the live views. You never edit
the old record to mark it dead — the index computes it.

## 6. Placement — principles and areas are derived views, not folders

All records live in `reports/`. Nothing is relocated. "The principles ledger" and "the marker
decisions" are **views the index computes**, not directories — a record physically stays put
while appearing in every view its frontmatter earns. This is why records can stay in
`reports/` next to their evidence and still be navigable per-area: the shelf is derived, the
book never moves.

## 7. The index

`scripts/decision_index.py` scans `reports/*.md`, reads frontmatter only, and writes:

- `reports/decision-index.json` — machine-readable: every record, its derived reverse edges,
  its cluster, and the queues.
- `reports/DECISIONS.md` — human-readable: principles first (the constitution), then clusters,
  then per-area views, then the queues.

**Queues the index surfaces** (the system advertising its own state, so nothing rots
silently): open stubs, stances awaiting evidence review, contested decisions, superseded
chains, and records that `carry_human_judgment` (so their non-derivable crux is browsable).

**It validates on every run, and fails the build (exit 1) on:** a malformed or unparseable record
file (surfaced, never silently skipped); a filename that does not match its `id`; a missing or
mistyped required field, a bad enum (`status`, `kind`, `confidence`, `revisit` class, evidence
enums), a non-boolean `binding`/`human_input`, or an invalid `decided_on` date; a body missing a
required section (`## Question`, `## Decision`, `## Why`, plus `## Human reasoning` whenever
`human_input` is true); `human_input`/`human_crux` inconsistency; a dangling id-edge or a
record-shaped `cites` target that does not resolve; a cycle in `refines`/`supersedes`/`depends_on`;
a `supersedes` edge across different questions; and more than one live record for a question.

Output is **deterministic** — no wall-clock in the artifacts, identity is the input hash — so a no-op
regeneration produces no diff. Run `python3 scripts/decision_index.py --check` to verify the
committed artifacts are current without rewriting them; CI uses this.

## 8. Rules of engagement

1. **Grep before you propose.** Before changing anything, search the records (and
   `reports/DECISIONS.md`) for the subject. A `revisit` that is class `none` (principle-
   rejected) is settled — do not reopen it. A class `internal|evidence|values` trigger tells
   you exactly what would.
2. **File on close.** The moment a decision is settled, write the record — a four-line stub is
   fine; the validator will nag for the rest. A decision that lives only in a commit message
   or a chat evaporates.
3. **Cite what you touch** (see §5).
4. **Supersede, don't edit.** A closed record is immutable. To change a decision, write a new
   record that `supersedes` it and states what specifically changed — the old one stays as the
   trail. (The `title` and typo fixes are the only in-place edits.)
5. **Regenerate the index** after adding or editing a record, and commit both.
6. **Record the human part.** If a person's instinct, field-knowledge, or constraint moved the
   decision, capture it (`human_input`, `human_crux`, `Human reasoning`) — that is the part
   nobody can reconstruct later.

## 9. This repo's layer

**Areas vocabulary** (extensible — add to this list in the same commit that first uses a new
area): the areas THIS repo actually has: `method`. Add an area in the same commit that first uses it.

**Where things live.** Spec: `instructions/DECISION-RECORDS.md` (this file). Records:
`reports/DEC-*.md`. Index: `reports/decision-index.json` + `reports/DECISIONS.md`. Generator:
`scripts/decision_index.py`. Any pre-existing design docs, research or audits are **evidence**
that records `cite:`; retrofit them into records over time, don't delete them.

## 10. For agents (Cowork and Claude Code)

Both surfaces obey this one file. On entering the repo: read `reports/DECISIONS.md`
(principles first). Before proposing a change: grep the records for the subject (§8.1). On
settling a decision: file the record and regenerate the index (§8.2, §8.5). This protocol is
mirrored from `project-instructions.md` (Cowork) and `CLAUDE.md` (Claude Code) so neither
surface can drift from it.

---

## Appendix — minimal record template

```markdown
---
id:            DEC-<slug>
question:      "<slug>"
title:         "<title>"
status:        accepted
binding:       false
kind:          engineering
areas:         ["<area>"]
decided_on:    "2026-08-25"
decision:      "<one line>"
confidence:    high
human_input:   false
human_crux:    ""
supersedes:    []
refines:       []
governed_by:   []
depends_on:    []
cites:         []
enforced_by:   null
revisit:       ["internal | <what would reopen this>"]
---

## Question
## Decision
## Why
## Options considered
## Consequences
## Revisit-if
```

*Every record names a question. Every silence about the "why" is a re-derivation someone
will pay for later.*

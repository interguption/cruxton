# decision-records — Decisions (generated)

*Generated 2026-08-29T11:09:45+00:00 · 9 records · input-hash `d47c031cca0c6b2e`. Do not edit — regenerate with `python3 scripts/decision_index.py`.*

## Principles (the constitution — read first)

- `DEC-organizing-frame-pace-layering` **Knowledge is organised by pace layering — every fact at the layer matching its rate of change** · engineering/accepted
- `DEC-records-stay-put` **Records never move and ids never change once anything cites them** · engineering/accepted — _human crux:_ PS's reasoning from a real event: commit messages are immutable and already cite reports/ paths, so relocating records to a decisions/ folder would strand those citations. Physical stability over tidy foldering — and it keeps the retrofit continuous, with no visible break in how decisions were recorded.
- `DEC-why-record-decisions` **Why a repo keeps a decision trail at all** · engineering/accepted — _human crux:_ PS's reasons for wanting this: stop re-litigating cleared decisions; be able to overturn only after reading the whole trail; let any agent avoid failed paths and pick up promising ones; stop re-researching in future projects and depend on internal resources over the web; and build specificity on contested topics by writing the reasoning down.

## Clusters (read these together)

**DEC-decision-kinds**
- `DEC-decision-kinds` **Every record has a kind — engineering, stance, or design — set by who adjudicates it** · engineering/accepted
- `DEC-why-has-three-layers` **A record's 'why' has three layers, and non-derivable human reasoning rides at the top** · engineering/accepted — _human crux:_ PS's core addition: capture the human/subjective reasoning a machine cannot re-derive — instinct, a market read, an org constraint — and surface it high, so an agent won't confidently re-derive a decision whose real driver was human judgment. Machine logic is the re-derivable part; the human part is the scarce one.

**DEC-index-is-generated**
- `DEC-index-is-generated` **The index is generated from outbound-only edges, never hand-maintained** · engineering/accepted
- `DEC-record-id-scheme` **Record ids are permanent slugs that name the question; area is separate metadata** · engineering/accepted

**DEC-organizing-frame-pace-layering**
- `DEC-organizing-frame-pace-layering` **Knowledge is organised by pace layering — every fact at the layer matching its rate of change** · engineering/accepted
- `DEC-placement-by-binding-only` **The constitution is binding records only — cross-cutting-ness does not promote** · engineering/accepted

## By area

**method** — `DEC-decision-kinds`, `DEC-distribution-central-mutable-method`, `DEC-index-is-generated`, `DEC-organizing-frame-pace-layering`, `DEC-placement-by-binding-only`, `DEC-record-id-scheme`, `DEC-records-stay-put`, `DEC-why-has-three-layers`, `DEC-why-record-decisions`

## Carries human judgment (non-derivable — read before overturning)

- `DEC-distribution-central-mutable-method` **The method is distributed as a thin skill over a central, mutable method repo** · engineering/accepted — _human crux:_ PS's proposal: don't cram everything into a giant skill file — point a thin skill at a fixed central location that holds the pre-written machinery, so setup is fast and improvements are made centrally and inherited by every future project.
- `DEC-records-stay-put` **Records never move and ids never change once anything cites them** · engineering/accepted — _human crux:_ PS's reasoning from a real event: commit messages are immutable and already cite reports/ paths, so relocating records to a decisions/ folder would strand those citations. Physical stability over tidy foldering — and it keeps the retrofit continuous, with no visible break in how decisions were recorded.
- `DEC-why-has-three-layers` **A record's 'why' has three layers, and non-derivable human reasoning rides at the top** · engineering/accepted — _human crux:_ PS's core addition: capture the human/subjective reasoning a machine cannot re-derive — instinct, a market read, an org constraint — and surface it high, so an agent won't confidently re-derive a decision whose real driver was human judgment. Machine logic is the re-derivable part; the human part is the scarce one.
- `DEC-why-record-decisions` **Why a repo keeps a decision trail at all** · engineering/accepted — _human crux:_ PS's reasons for wanting this: stop re-litigating cleared decisions; be able to overturn only after reading the whole trail; let any agent avoid failed paths and pick up promising ones; stop re-researching in future projects and depend on internal resources over the web; and build specificity on contested topics by writing the reasoning down.

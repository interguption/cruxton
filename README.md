# decision-records — the method

A portable system for recording a repo's decisions as a durable, greppable trail: what was
decided, why, what was rejected (and whether on principle or on a constraint that could
change), and the non-derivable human reasoning behind it — with a generated, validated index.
Organised by pace layering: every fact lives at the layer matching its rate of change, and
faster layers cite slower ones rather than restating them.

## Use it
In a target repo:

    python3 /path/to/decision-records/bootstrap.py .

It writes `instructions/DECISION-RECORDS.md`, `scripts/decision_index.py`, a `CLAUDE.md`
pointer and `reports/`, stamps the method version, and self-verifies. Idempotent — safe to
re-run; it refreshes the generator and never clobbers a record.

## What's here
- `templates/` — the spec, the generator, the record template, the agent pointers.
- `bootstrap.py` — deterministic setup + self-check.
- `SKILL.md` — the skill that drives setup and recording.
- `reports/` — this method's own genesis ledger: its architecture decisions, in its own format.
- `METHOD-VERSION` / `CHANGELOG.md` — the method's version and its evolution.

## Central mutability
This folder is the source of truth. Improve it here and future bootstraps inherit the change.
Existing repos upgrade by re-running bootstrap. Push this folder to a git remote to use it
from other machines; the method versions itself so a repo can tell what it was scaffolded from.

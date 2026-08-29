---
name: decision-records
description: >-
  Set up and maintain a repo's decision-records system — a durable, greppable trail of what
  was decided, why, what alternatives were rejected (and whether on principle or on a
  changeable constraint), and the non-derivable human reasoning behind each call, with a
  generated and validated index. Use when starting a new repo, when asked to set up decision
  records / a decision log / a decision trail / an ADR system, or to record, revisit, or
  overturn a decision in a repo that already uses this system.
---

# Decision Records

This skill installs and drives a portable decision-records system. The machinery lives in the
**method repo** (this skill's own folder, default location
`~/Documents/Personal software/decision-records/`). That folder is the single source of
truth; improving it there makes every future setup inherit the change.

## 1. Setting it up in a repo (first time)

If the target repo has no `instructions/DECISION-RECORDS.md`, bootstrap it. From the target
repo's root:

```
python3 "<method-repo>/bootstrap.py" .
```

`<method-repo>` is this skill's folder (default above; ask the user if it isn't there). The
bootstrap is deterministic and idempotent — it writes `instructions/DECISION-RECORDS.md`,
`scripts/decision_index.py`, a `CLAUDE.md` pointer and `reports/`, stamps the method version,
and **self-verifies by running the generator**. Do not hand-transcribe any of these files;
run the bootstrap so the self-check proves the setup. If it prints `SELF-CHECK PASSED`, setup
is done. Then customise section 9 of `instructions/DECISION-RECORDS.md` with the repo's own
areas vocabulary, and commit.

## 2. Working in a repo that already has it

Read `instructions/DECISION-RECORDS.md` — it is the contract. In short:

- **Before proposing or changing anything:** read `reports/DECISIONS.md` (principles first),
  then grep `reports/DEC-*.md` for the subject. A record whose `revisit` class is `none` is
  principle-settled — do not reopen it. A record that carries human judgment rests on a call
  you cannot re-derive — read it before overturning.
- **When a decision is settled:** write a record (`reports/DEC-<slug>.md`; the slug names the
  *question*, never the answer), then regenerate and commit the index:
  `python3 scripts/decision_index.py`. The generator fails the build on a dangling citation,
  an edge cycle, or a record missing its kind-gated fields.
- **To change a past decision:** write a new record that `supersedes` it — never edit a closed
  record (only its `title` and typos). The old one stays as the trail.
- **Capture the human part.** If a person's instinct, field knowledge, or a constraint moved
  the decision, put it in `human_input` / `human_crux` / the `Human reasoning` section — that
  is the part no future agent can reconstruct.

## 3. When to write a record — and when not

Record a choice that (a) closes off an alternative someone might re-propose, (b) rests on
non-obvious evidence or a contested stance, or (c) is expensive to reverse. Do **not** record
a reversible, obvious, or purely mechanical choice — over-recording buries the trail. Agents
skew toward over-documenting; hold the line.

## 4. Keeping the method itself current

This method versions itself (`METHOD-VERSION`, `CHANGELOG.md`, and the genesis ledger in the
method repo's own `reports/`). When you improve the system, make the change in the **method
repo** and bump the version and changelog — do not fork it into one project. Existing repos
upgrade by re-running the bootstrap (it refreshes the generator, never touches records). Any
change to how the method works is itself a decision: record it in the method repo's `reports/`.
Push the method repo to a git remote to use it from other machines.

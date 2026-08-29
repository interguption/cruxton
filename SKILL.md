---
name: cruxton-decision-records
description: >-
  Set up and maintain Cruxton, a repo's decision-records system — a durable, greppable, validated
  trail of what was decided, why, what alternatives were rejected (and whether on principle or on a
  changeable constraint), and the non-derivable human reasoning behind each call, with a generated
  index. Use when starting a new repo, when asked to set up decision records / a decision log / a
  decision trail / an ADR system, or to record, revisit, or overturn a decision in a repo that
  already uses this system.
---

# Cruxton — Decision Records

This skill installs and drives a portable decision-records system. Its machinery — `bootstrap.py`,
`templates/`, the generator — is bundled **in this skill's own folder**; that bundle is the source
of truth, and improving it there makes every future setup inherit the change. (Installed via the
Claude Code plugin, the bundle lives under `${CLAUDE_PLUGIN_ROOT}`; installed from a clone, it is the
cloned folder.)

## 1. Setting it up in a repo (first time)

If the target repo has no `instructions/DECISION-RECORDS.md`, bootstrap it from the repo root:

```
python3 <this-skill-folder>/bootstrap.py .
```

`<this-skill-folder>` is the folder containing this SKILL.md and `bootstrap.py`. The bootstrap is
deterministic, idempotent, **non-destructive** (it refuses to overwrite a file it does not own), and
**self-verifying** — it runs the generator at the end. It writes `instructions/DECISION-RECORDS.md`,
`scripts/decision_index.py`, `CLAUDE.md` and `AGENTS.md` pointers, and `reports/`, and stamps the
method version. If it prints `SELF-CHECK PASSED`, setup is done. Then customise section 9 of
`instructions/DECISION-RECORDS.md` with the repo's own areas vocabulary, and commit. (`--dry-run`
previews; `--upgrade-spec` migrates an older spec.)

## 2. Working in a repo that already has it

Read `instructions/DECISION-RECORDS.md` — it is the contract. In short:

- **Before proposing or changing anything:** read `reports/DECISIONS.md` (principles first), then
  grep `reports/DEC-*.md` for the subject. A record whose `revisit` class is `none` is
  principle-settled — do not reopen it. A record that carries human judgment rests on a call you
  cannot re-derive — read it before overturning.
- **When a decision is settled:** write a record (`reports/DEC-<slug>.md`; the slug names the
  *question*, never the answer), then regenerate and commit the index:
  `python3 scripts/decision_index.py`. It fails the build on a malformed record, a dangling edge, a
  cycle, a missing/mistyped field, or two live decisions for one question.
- **To change a past decision:** write a *new* record with a new id and the *same* `question` that
  `supersedes` the old one — never edit a closed record (only its `title` and typos). The old one
  stays as the trail; the index derives which is live.
- **Capture the human part.** If a person's instinct, field knowledge, or a constraint moved the
  decision, put it in `human_input` / `human_crux` / the `## Human reasoning` section.
- **Never** record secrets, credentials, personal data, health data, or verbatim private
  conversations — records are committed and may be public. Record the reasoning, not the source.

## 3. When to write a record — and when not

Record a choice that (a) closes off an alternative someone might re-propose, (b) rests on
non-obvious evidence or a contested stance, or (c) is expensive to reverse. Do **not** record a
reversible, obvious, or purely mechanical choice — over-recording buries the trail. Agents skew
toward over-documenting; hold the line.

## 4. Keeping the method itself current

This method versions itself (`METHOD-VERSION`, `CHANGELOG.md`, and the genesis ledger in its own
`reports/`). Improve it in the bundle, bump the version and changelog, and record the change as a
decision — do not fork it into one project. Existing repos upgrade by re-running the bootstrap
(`--upgrade-spec` to migrate the spec).

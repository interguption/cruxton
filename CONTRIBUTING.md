# Contributing to Cruxton

Cruxton is a **centrally mutable** method: the machinery lives in one place (this repo / the skill
bundle), improvements are made here, and every future setup inherits them. Please don't fork the
method into a single project — improve it here.

## How to propose a change
1. Open an issue or PR against this repo.
2. **Any change to how the method works is itself a decision** — file a record under `reports/`
   (`reports/DEC-<slug>.md`, slug naming the question) as part of the same PR. The repo governs
   itself; read `reports/DECISIONS.md` (principles first) before proposing.
3. Run the generator and commit the regenerated index:
   ```
   python3 scripts/decision_index.py          # regenerate + validate (exit 1 on any error)
   python3 scripts/decision_index.py --check   # CI-style: fail if committed artifacts are stale
   ```
   The generator is dependency-free (bare `python3`). CI runs `--check` on every push.

## Versioning
The method versions itself (`METHOD-VERSION`, `CHANGELOG.md`, and the `cruxton-method-version`
marker in the spec). Bump the version when the method's behavior or contract changes, and note it in
`CHANGELOG.md`. Repos that already use Cruxton upgrade by re-running the bootstrap
(`--upgrade-spec` to migrate the spec, which backs up the old one).

## Ground rules
- Records are immutable once closed — supersede, don't edit (only `title` and typo fixes).
- Never commit secrets, personal data, health data, or verbatim private conversations to a record
  (`instructions/DECISION-RECORDS.md` §0.5). Records are public.
- Keep the generator dependency-free so it ports into any repo verbatim.

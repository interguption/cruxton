# Releasing Cruxton

How to cut a method release. Two things bite if you skip them:

1. **A tag/Release is a frozen snapshot — `main` does not advance it.** Pushing commits to `main`
   never changes the version GitHub shows; `main` silently drifts ahead of the last Release until you
   cut a new one. Cutting the Release is a deliberate step, not a side effect of pushing.
2. **The version is stamped in several places that must move together.** Miss one and the stamps
   disagree about what version this is.

## 1. Bump every version stamp

Grep first — the layout can change, so let the grep find them, don't trust this list blindly:

```
git grep -n "<OLD_VERSION>"        # e.g. git grep -n "1.0.1"
```

Bump all of these from `X.Y.Z` to the new version, in one commit:

| Stamp | What it is |
|---|---|
| `skills/cruxton-decision-records/METHOD-VERSION` | bootstrap's source of truth |
| `.claude-plugin/plugin.json` → `"version"` | the Claude Code plugin version |
| `instructions/DECISION-RECORDS.md` → `<!-- cruxton-method-version: X.Y.Z -->` | the installed spec's stamp |
| `skills/cruxton-decision-records/templates/DECISION-RECORDS.template.md` | the same marker in the distributed template |
| `README.md` badge | `method vX.Y.Z` — in **both** the label and the shields.io URL |
| `CHANGELOG.md` | add a new dated entry on top; keep the old ones |

Bump the version when the method's **behavior or contract** changes. Docs-only changes can ride along
without a bump.

> If the release includes a generator/machinery fix, make sure it landed in **both** copies —
> `scripts/decision_index.py` (live) and `skills/cruxton-decision-records/templates/decision_index.py`
> (distributed by bootstrap). A fix in only the live copy is reverted the next time someone upgrades.

## 2. Commit, push, wait for green

```
python3 scripts/decision_index.py --check     # artifacts current, 0 lint errors
git commit -am "Release vX.Y.Z — bump method version across all stamps"
git push origin main
```

Wait for the `validate` workflow to pass on that commit before tagging.

## 3. Tag and publish the Release

Annotated tag (matches every prior tag), then the GitHub Release:

```
git tag -a vX.Y.Z -m "Cruxton vX.Y.Z — <one-line summary>" <commit>
git push origin vX.Y.Z
gh release create vX.Y.Z --title "Cruxton vX.Y.Z" --notes-file <notes.md>
```

Release notes: reuse the `CHANGELOG.md` entry, and end with a compare link
(`https://github.com/interguption/cruxton/compare/vPREV...vX.Y.Z`).

## 4. Verify

```
gh repo view --json latestRelease     # should report the new tag as Latest
```

The old tag/Release stays as its historical snapshot — that's expected. Don't delete or re-point it.

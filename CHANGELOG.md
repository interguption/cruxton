# Changelog — Cruxton (decision-records method)

## 1.0.0 — 2026-08-29
First public release. Extracted from the Steelyard reference implementation, then hardened for
public use following an external adversarial readiness review.

Core model: slug ids that name a decision event, with a separate stable `question` key grouping a
reversal chain (effective status derived); engineering / stance / design kinds; the three-layer
capture of "why" (`human_crux`, `## Human reasoning`, `## Reasoning provenance`); outbound-only edges
with a generated index; principles and per-area views derived, not filed; records stay put (paths and
ids permanent).

Hardening in this release:
- **Strict validator** — enforces the full contract (required fields, types, enums, filename==id,
  required body sections, `human_input`/`human_crux` consistency, kind-gated fields) and surfaces
  malformed record files instead of silently skipping them; the build fails on any violation.
- **Decision identity** — a permanent decision-event `id` plus a separate `question` key; the index
  derives live vs superseded and rejects two live records for one question.
- **Non-destructive, honest bootstrap** — writes only files it owns, refuses foreign collisions,
  atomic writes, `--dry-run` / `--force` / `--upgrade-spec`, and a self-check that reports success
  only when the generator exits 0; honest version stamping.
- **Deterministic artifacts** — no wall-clock in generated files (identity is the input hash), the
  ledger title read from a committed `.decision-records-name` (never the checkout path, so it is
  stable across machines and CI), and a `--check` mode for CI.
- **Cross-tool** — the bootstrap emits an `AGENTS.md` pointer alongside `CLAUDE.md`.
- **Privacy** — a binding never-record rule for secrets, personal data, and private conversations.
- Dogfooded stance and design records; MIT licensed; CI validates on every push.

See `reports/` for the genesis ledger — the method's own decisions, including this hardening.

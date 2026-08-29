---
id:            DEC-openai-skill-install-path
question:      "openai-skill-install-path"
title:         "Codex installs Cruxton via the skill-installer from this repo's GitHub tree URL"
status:        accepted
binding:       false
kind:          engineering
areas:         ["method"]
decided_on:    "2026-08-29"
decision:      "Because Cruxton ships a valid SKILL.md, the README documents installing it on OpenAI Codex with the native skill-installer against this repo's GitHub tree URL, rather than only a manual clone: `$skill-installer install https://github.com/interguption/cruxton/tree/main/skills/cruxton-decision-records`."
confidence:    high
human_input:   false
human_crux:    ""
supersedes:    []
refines:       ["DEC-distribute-as-plugin"]
governed_by:   []
depends_on:    []
cites:         ["OpenAI Codex skills docs (learn.chatgpt.com/docs/build-skills; developers.openai.com/codex/skills redirects there) + openai/skills skill-installer, verified 2026-08-29"]
enforced_by:   null
revisit:       ["internal | Codex changes its skill-install mechanism, command, or skills directory"]
---

## Question
What is the correct, current way to install Cruxton on OpenAI Codex, given that Cruxton already ships a valid SKILL.md?

## Decision
Document the native Codex **skill-installer** against this repo's GitHub tree URL. From inside Codex:

```
$skill-installer install https://github.com/interguption/cruxton/tree/main/skills/cruxton-decision-records
```

Skills install into `$CODEX_HOME/skills/` (default `~/.codex/skills/`); Codex must be restarted (or takes the skill on its next turn) to discover it. Once installed, asking Codex to "set up decision records here" runs the bundled bootstrap — the Codex analog of the Claude Code plugin. This is a distinct, complementary channel from the `AGENTS.md` pointer (which makes Codex obey an already-instrumented repo without installing anything).

## Why
Codex ships a SKILL.md-based skills system with a skill-installer that installs from a GitHub tree URL, and Cruxton's bundle at `skills/cruxton-decision-records/` is exactly that shape. Documenting the one-command installer — instead of only "clone the repo" — matches how Codex users actually add skills and mirrors the one-command install we give Claude Code, so the same self-contained bundle serves both tools. It refines `DEC-distribute-as-plugin`: same idea (package the SKILL.md so a coding agent installs it and can drive setup), different host.

## Options considered
- **Document only a manual `git clone` + run bootstrap.** REJECTED (class: constraint) — ignores Codex's native install path; more steps than users expect.
- **Assume Codex reads AGENTS.md and document nothing Codex-specific.** REJECTED (class: constraint) — AGENTS.md only makes Codex obey an existing setup; it does not give Codex the skill to *create* one.
- **Document the skill-installer with this repo's GitHub tree URL.** CHOSEN — one command, uses the bundle as-is, parallels the Claude Code plugin.

## Consequences
The README carries the Codex skill-installer command (`<your-github>` → interguption on promotion). The path depends on an external, still-young mechanism; the record's revisit trigger tracks Codex changing its install command or skills directory.

## Reasoning provenance
- The skill-installer installs from a GitHub tree URL into `$CODEX_HOME/skills` (default `~/.codex/skills`), and Codex must be restarted / picks the skill up on the next turn — `external-research`: OpenAI Codex skills docs and the `openai/skills` skill-installer, verified 2026-08-29. `developers.openai.com/codex/skills` 308-redirects to `learn.chatgpt.com/docs/build-skills`.
- Cruxton's bundle is a valid SKILL.md directory installable by that mechanism — `internal-finding`: the Phase A bundle at `skills/cruxton-decision-records/` with `SKILL.md` at its root.

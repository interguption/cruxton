---
id:            DEC-chatgpt-as-custom-gpt
question:      "chatgpt-participation"
title:         "ChatGPT participates as a Custom GPT that queries and drafts records, not an installer"
status:        accepted
binding:       false
kind:          engineering
areas:         ["method"]
decided_on:    "2026-08-29"
decision:      "Cruxton reaches ChatGPT as a Custom GPT (chatgpt/CUSTOM-GPT.md): the read-before / file-on-close protocol, record format, and binding privacy rule as instructions, plus a knowledge list of reports/DECISIONS.md, reports/decision-index.json AND the reports/DEC-*.md records — with a raw-GitHub-URL path for reviewers who only read."
confidence:    high
human_input:   false
human_crux:    ""
supersedes:    []
refines:       []
governed_by:   []
depends_on:    []
cites:         ["chatgpt/CUSTOM-GPT.md"]
enforced_by:   null
revisit:       ["internal | ChatGPT gains repo write/execute access, or the Custom GPT knowledge/attachment mechanism changes"]
---

## Question
How does Cruxton reach ChatGPT, an assistant that cannot clone a repo, run the bootstrap, or commit files?

## Decision
Ship a Custom GPT, not an installer. `chatgpt/CUSTOM-GPT.md` carries two parts: (1) instructions — the read-before protocol (consult the trail, principles first, before answering; honour `revisit: none` and `human_input` records), the file-on-close protocol (draft a `DEC-<slug>.md` naming the question; supersede rather than edit; the human saves, regenerates, commits), the record format, and the binding privacy rule verbatim; and (2) a knowledge list. The knowledge list is `reports/DECISIONS.md` + `reports/decision-index.json` **and the `reports/DEC-*.md` records themselves**, because the index summarises the trail but the rationale (`## Why`, `## Human reasoning`, `## Options considered`) lives only in the records — attaching only the index lets the GPT list decisions without being able to explain them. A reviewer who only wants to read can instead point ChatGPT or Claude at the raw GitHub URLs of those files.

## Why
ChatGPT has no repo execution, so the install-and-drive model (Claude Code plugin, Codex skill) does not apply; its strengths are querying history and drafting records for a human to commit. A Custom GPT is the durable, shareable way to give it the protocol plus the repo's own trail. The knowledge-list emphasis on attaching the records (not just the index) is the load-bearing detail: it is the difference between "what was decided" and "why," and the whole point of the method is the why.

## Options considered
- **Skip ChatGPT.** REJECTED (class: constraint) — abandons a large, non-repo audience of readers and drafters.
- **Custom GPT with only DECISIONS.md + index as knowledge.** REJECTED (class: constraint) — the index carries no full rationale, so the GPT can list but not explain decisions.
- **Custom GPT with instructions + full record set (records included) as knowledge.** CHOSEN — queries and drafts with the real reasoning in hand.

## Consequences
Knowledge must be re-uploaded after the index is regenerated to stay current. The GPT drafts records but cannot commit; the human runs the generator and commits.

## Revisit-if
ChatGPT gains repo write/execute access (then it could install/drive like Codex), or the Custom GPT knowledge/attachment mechanism changes materially.

---
id:            DEC-public-metadata-verification
question:      "public-metadata-verification"
title:         "Public metadata is complete only after fresh crawler and end-to-end unfurl verification"
status:        accepted
binding:       false
kind:          engineering
areas:         ["method"]
decided_on:    "2026-08-31"
decision:      "A public metadata change is not complete when its settings/API value changes; completion requires the anonymous page metadata, referenced asset response, and a fresh destination unfurl to agree, with cache-blocked destinations reported as pending rather than successful."
confidence:    high
human_input:   false
human_crux:    ""
supersedes:    []
refines:       ["DEC-public-positioning"]
governed_by:   []
depends_on:    []
cites:         ["assets/github-social-preview.png"]
enforced_by:   null
revisit:       ["internal | public metadata platforms provide a deterministic end-to-end status or cache-invalidation contract that makes one of these checks redundant"]
---

## Question
When may a public metadata change—especially a social preview—be called live and verified?

## Decision
Verify four distinct layers before declaring completion:

1. **Control plane:** the hosting service's settings or API points to the intended asset.
2. **Origin page:** an anonymous request using the relevant crawler user agent receives the intended `og:*` / `twitter:*` metadata.
3. **Asset delivery:** the referenced URL returns `200`, the intended content type and bytes, and usable dimensions.
4. **Destination behavior:** a fresh, uncached unfurl on the target service actually renders the intended card.

These checks are not substitutes for one another. If the first three pass but destination caching prevents the fourth, report the change as origin-correct but unfurl-pending—not complete.

## Why
On 2026-08-30, the launch-surface commit reached `main` at 08:45:24Z. GitHub's custom repository image was uploaded at 08:53:53Z, leaving an approximately 8½-minute interval in which a social crawler could fetch and cache the old/default card for the stable repository URL.

The upload itself was correct. On 2026-08-31:

- GitHub returned the same custom `repository-images.githubusercontent.com` URL from GraphQL, `og:image`, and `twitter:image`, including when requested as `Twitterbot/1.0`.
- The image endpoint returned `HTTP 200`, `content-type: image/png`, and `content-length: 106948`.
- Its ETag was `fc98cf077521523ce9563e724ed7968e`, exactly matching the local PNG's MD5.
- GitHub served the repository page with `cache-control: max-age=0, private, must-revalidate`, while the image had a content-address-like URL and long cache lifetime.

Therefore the origin and asset were correct; a destination still showing the earlier card was using its own cached unfurl. The stable shared URL made that cache invisible if verification stopped at GitHub.

The agent's mistake was procedural and explicit: it declared the preview "uploaded and verified" after observing GitHub's GraphQL URL change. That proved the settings mutation, not the user-visible outcome. A subsequent attempt to retrieve and visually inspect the live image timed out, yet the agent still closed the task instead of reporting verification as incomplete. It also sequenced the commit and searchable metadata ahead of the authenticated image upload, creating the exact cache window that later mattered.

## Options considered
- **Treat a changed settings/API value as success.** REJECTED (class: constraint) — proves acceptance by the control plane, not crawler-visible metadata, asset delivery, or rendered unfurls.
- **Verify GitHub metadata and image delivery only.** REJECTED (class: constraint) — proves the origin is correct but misses downstream services caching the stable repository URL.
- **Verify control plane, origin, asset, and a fresh destination unfurl.** CHOSEN — matches the actual user-visible outcome and keeps cache-blocked work honestly pending.

## Consequences
- Upload and origin verification must finish before a public repository URL is shared or announced.
- A failed or timed-out final check cannot be converted into success by inference from an earlier layer.
- Verification reports must name which layer passed and which remains pending.
- Destination-specific caches are treated as external state, not evidence that the origin upload failed.

## Revisit-if
Revisit if GitHub and the relevant destination platforms expose a reliable, documented end-to-end preview status or deterministic cache invalidation that collapses these layers without losing confidence.

## Reasoning provenance
- The report that the custom card did not appear when shared came from the user — `provided-data`.
- The commit/image timing, public HTML metadata, crawler response, HTTP headers, content length, ETag, and local MD5 comparison were measured during this investigation — `internal-finding`.
- The conclusion that the remaining mismatch lives in a downstream unfurl cache follows from the origin page and exact asset both being correct while the destination remains stale — `internal-finding`.

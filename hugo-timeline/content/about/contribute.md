---
title: "Contribute"
summary: "How to suggest events, flag corrections, and contact the editor. The archive is open source and version-controlled."
weight: 30
---

The Cascade Ledger is open infrastructure. Anyone can suggest a new event, flag a sourcing error, propose a re-classification, or submit a correction. The dataset is version-controlled in git, and every change is part of the public record.

## Suggest a new event

The archive is not a news ticker — it is a documentary record. Events are added when they are sourced to the standard described in [methodology](/about/methodology/) and [sources](/about/sources/). Before suggesting an event, please confirm:

1. The event has at least one citation that meets [Tier 1 or Tier 2 standards](/about/sources/), or two corroborating [Tier 3](/about/sources/#tier-3) citations.
2. The event has a clear date — calendar where possible, year or year-month where not.
3. The connection to institutional capture is documentable rather than rhetorical.
4. The event is not already in the archive (search [the filter view](/q/) before submitting).

To submit: open an issue or pull request on the [`cascade-kb` GitHub repository](https://github.com/markramm/cascade-kb). Include the proposed entry as plain text or YAML, with cited sources. Submissions that meet the editorial bar are typically merged within a few days.

## Suggest a correction

Corrections are taken seriously and processed quickly. If you believe an entry is wrong — incorrect date, misattributed actor, broken citation, mischaracterized status — please open an issue at the [GitHub repository](https://github.com/markramm/cascade-kb) with:

- The URL of the affected entry.
- A description of the error.
- A citation supporting the correction.

Corrections are visible in the git log. We do not silently revise; if a substantive claim changes, the entry carries a dated correction note.

## Re-classification requests

Editorial scores — the [importance score](/about/methodology/#importance) and [editorial status](/about/methodology/#status) — are revisable. If new information warrants a higher importance score, or if a *reported* event has been corroborated and should move to *confirmed*, please flag it the same way. Status downgrades (from *confirmed* to *disputed*, for instance) are handled with the same care.

## What does not get added

The archive declines:

- Events whose only sourcing is a single Tier 4 outlet or anonymous social-media post.
- Speculative claims about motives that the cited sources do not themselves document.
- Editorial commentary unattached to a specific dated event.
- Duplicate entries — if the event is already in the archive, propose an enrichment to the existing entry.

## Contact the editor

For matters that don't fit the GitHub flow — research collaborations, interview requests, threats and intimidation, dataset licensing questions beyond the [stated license](/about/license/) — contact Mark Ramm directly via [The RAMM](https://theramm.substack.com/). The substack is the long-form analytical companion to this archive; subscribing is the fastest way to follow the patterns the data documents.

## Why open source

A documentary record of institutional capture is more credible when it can be inspected, forked, and audited than when it cannot. The full dataset, the build pipeline, and the editorial commit history are public for the same reason court filings are public: the work is meant to be checked.

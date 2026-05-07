---
title: "License & attribution"
summary: "The data is CC BY-SA 4.0. The code is MIT. How to cite the archive in journalism, research, and downstream datasets."
weight: 40
---

The Cascade Ledger is published as open infrastructure. The dataset and the code that produces it carry separate licenses, both permissive enough for reuse and both carrying obligations meant to keep the work attributable and the corrections traceable.

## Data: CC BY-SA 4.0

The full event corpus — every entry, every source citation, every actor and tag classification — is released under the [Creative Commons Attribution-ShareAlike 4.0 International license](https://creativecommons.org/licenses/by-sa/4.0/).

You are free to:

- **Share** — copy and redistribute the dataset in any medium or format.
- **Adapt** — remix, transform, build upon, and republish, including commercially.

Under two conditions:

- **Attribution.** You must credit *The Capture Cascade Ledger* and link back to the archive. A working citation is provided below.
- **ShareAlike.** Derivative works that incorporate the dataset must be released under the same CC BY-SA 4.0 license. Building a paywalled product on top of this corpus and licensing it under more restrictive terms is not permitted.

The dataset is downloadable as JSON at [`/data/timeline.json`](https://capturecascade.org/data/timeline.json) and is regenerated on every reindex.

## Code: MIT

The Hugo site templates, the build scripts, the validation tooling, and everything else in the [`cascade-kb` repository](https://github.com/markramm/cascade-kb) that is *code rather than data* are released under the MIT license. Fork it, run your own instance, build something downstream — the only obligation is to preserve the copyright and license notice.

## Infrastructure: Pyrite

The underlying knowledge-base infrastructure is [Pyrite](https://github.com/markramm/pyrite), a separate open-source project for structuring research corpora that humans and AI agents can both query. Pyrite carries its own license; consult that repository.

## How to cite

For journalism and research that draws on the archive, the recommended citation is:

> *The Capture Cascade Ledger* (2026). Mark Ramm, ed. Transparency Cascade Press. Retrieved from https://capturecascade.org. Licensed CC BY-SA 4.0.

When citing a specific event, link directly to its event page — every URL is stable and is intended as a citation target. When citing a filtered view (a single actor, a capture lane, a year), the filter URL is also a stable citation.

## What attribution should look like

In running prose: "*according to The Capture Cascade Ledger*" with a hyperlink, or a footnote pointing at the specific event URL.

In a reused dataset: a header or README crediting *The Capture Cascade Ledger*, the CC BY-SA 4.0 license, and a link to this archive.

In a downstream visualization or app: a visible credit line in the interface, of the same prominence given to other source datasets.

## Licensing questions

For uses that don't fit the patterns above — large-scale academic redistribution, integration into commercial research products, dataset licensing for purposes that conflict with the ShareAlike clause — see [contribute](/about/contribute/) for how to reach the editor. Most reasonable requests are answered with "yes, with attribution," but the conversation is worth having in writing.

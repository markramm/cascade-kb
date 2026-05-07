# Adding a curated timeline preset

A "timeline preset" is a hand-curated swimlane view that appears at
`/timelines/<slug>/`, on the homepage strip, in the timeline index, and as
an iframe-embeddable view at `/embed/timelines/<slug>/`. Each is a single
markdown file in `content/timelines/`.

## TL;DR

```bash
# 1. Pick actors. Verify their canonical names exist in the corpus.
python3 -c "
import json
actors = json.load(open('static/data/actors.json'))
for a in actors:
    if 'leonard leo' in a['name'].lower():
        print(a['count'], a['name'])
"

# 2. Create the preset file
cat > content/timelines/the-religious-right.md <<'EOF'
---
title: "The religious right's institutional capture"
subtitle: "Forty years of mobilization, from Falwell to Christ Kirk"
summary: "Named figures, named institutions, named decisions."
weight: 100
fromYear: 1979
toYear: 2026
entities:
  - Jerry Falwell
  - Heritage Foundation
  - Federalist Society
entity_aliases:
  Heritage Foundation:
    - Heritage Foundation Board of Trustees
---

Editorial intro paragraph. The chart appears immediately after this.
EOF

# 3. Regenerate data files + rebuild
python3 scripts/generate_content.py
hugo serve --bind 127.0.0.1 --port 1314

# 4. Visit http://127.0.0.1:1314/timelines/the-religious-right/
```

## Frontmatter reference

```yaml
title:    "The religious right's institutional capture"
# Required. Page H1, browser title, OG card title.

subtitle: "Forty years of mobilization, from Falwell to Christ Kirk"
# Required. Eyebrow text above the H1.

summary:  "Named figures, named institutions, named decisions."
# Required. Lede italic line, also used in the homepage strip + index.

weight:   100
# Sort order in /timelines/ index and homepage strip. Lower = higher.
# Existing presets use 10..90; pick 100+ for new ones.

fromYear: 1979
toYear:   2026
# Inclusive year range for the swimlane x-axis.
# Pick the narrowest meaningful span — events outside the range are dropped.

entities:
  - Jerry Falwell             # one row per entity (top to bottom in this order)
  - Heritage Foundation
  - Federalist Society
# 7-12 rows is the readable sweet spot. >15 gets visually cramped.
# Each entity name MUST match an actor name in the corpus exactly,
# or be aliased via entity_aliases below.

entity_aliases:
  Heritage Foundation:
    - Heritage Foundation Board of Trustees
  Federalist Society:
    - Federalist Society leadership
# Optional. Maps a row's canonical name (key) to additional KB actor names
# (values) whose events should be aggregated into that row. Used when the
# Pyrite KB tracks the same entity under multiple names.
```

## Validating actor names exist

The most common failure mode: an entity name in the preset doesn't match any
actor in the corpus, and that row stays empty.

Verify first:

```bash
# Quick lookup
python3 -c "
import json
actors = {a['name']: a['count'] for a in json.load(open('static/data/actors.json'))}
for q in ['Jerry Falwell', 'Russell Vought', 'Some Person']:
    print(f\"{q!r}: {actors.get(q, 'NOT FOUND')}\")
"
```

If a name returns `NOT FOUND` but the actor exists under a slight variant
(e.g. `Justice Antonin Scalia` instead of `Antonin Scalia`), use
`entity_aliases` to bridge.

## Picking entities

Editorial considerations, ranked by importance:

1. **Each row should carry distinctive signal.** A row with 2 events doesn't
   help the visual case; the empty row is louder than the events. Aim for ≥10
   events per row in the chart's date range.
2. **Order top-to-bottom by narrative weight, not alphabetically.** The chart
   reads like a paragraph: most-important entity at the top, supporting cast
   below, capping with the most-recent or operational figures.
3. **Mix institutions with individuals.** Pure-individual rows feel like a
   gossip column; pure-institutional rows feel abstract. The combination
   makes the network visible.
4. **Don't over-aggregate.** A row called "The administration" hides who
   actually did what. Better: name three to five specific officials.

## Testing the preset

```bash
# Local dev server
hugo serve --bind 127.0.0.1 --port 1314

# Visit
open http://127.0.0.1:1314/timelines/<your-slug>/

# Things to verify:
# 1. The compact header shows your title + subtitle + lede + meta strip
# 2. The chart has all your entity rows, in order
# 3. No row is empty (if it is, fix the actor name or add an alias)
# 4. The annotation hairlines (Watergate, Citizens United, etc.) make sense
#    in your date range
# 5. Hovering an event shows a tooltip; clicking opens the event page
# 6. The chronological event ledger below the chart shows all matched events
# 7. The "Other curated timelines" footer shows your siblings
# 8. The /embed/timelines/<your-slug>/ version works (no chrome, just chart)
```

## How cross-references update

Adding a preset triggers automatic propagation of cross-links:

- **Actor pages** for each entity (and alias) gain a "Appears in curated
  timelines" callout linking to your preset.
- **Event pages** for any event matching your entities gain an "Appears in"
  link pointing here.
- **Sibling timeline pages** add your card to their "Other curated timelines"
  footer.
- The **homepage strip** picks up the preset if its weight is among the
  lowest 6.
- The **`/timelines/` index** lists it, sorted by weight.
- The **embed mirror** is generated automatically at
  `/embed/timelines/<your-slug>/`.

All of this happens via the data files emitted by `generate_content.py`.
The relevant ones:

- `data/timeline_membership.json` — which timelines contain each event/actor
- `data/actor_events.json` — used by the swimlane partial to render rows
- `content/embed/timelines/<your-slug>.md` — auto-mirrored from your preset

You don't write any of these by hand.

## Editorial guidelines

The presets are the most editorial surface on the site. They should:

- **Lead with a thesis.** The summary is one sentence; the intro essay is
  two short paragraphs. Don't write a wall of text — the chart IS the
  argument.
- **Stay sourceable.** Every claim in the intro should be derivable from the
  events on the chart. If you can't point to specific events, the claim
  doesn't belong.
- **Avoid speculation.** Don't write "this shows X intends Y." Write "X did
  these N things; the pattern is Y." The reader can draw the inference.
- **Frame what to look for.** If the chart's signal is "personnel come in
  the bottom rows in 2025+," tell the reader to watch that. They won't see
  it otherwise.

## Example: a minimal preset

```markdown
---
title: "How private equity ate American journalism"
subtitle: "A two-decade leveraged buyout of the local newspaper"
summary: "The named firms and the named acquisitions that emptied newsrooms."
weight: 110
fromYear: 2005
toYear: 2026
entities:
  - Alden Global Capital
  - GateHouse Media
  - Gannett
  - McClatchy
  - Tribune Publishing
  - The New York Times Company
entity_aliases:
  Tribune Publishing:
    - Tribune Company
    - tronc
---

Local newspapers in the United States lost roughly half their newsroom
employment between 2005 and 2025. The cause was not "the internet" — it
was a small set of named private-equity firms that acquired chains and
extracted operating margin until the editorial product collapsed. This
timeline plots the named acquirers against the named acquired.

The pattern to watch: each row's first event is the acquisition; the
subsequent markers are the layoffs, the closures, and the lawsuits. The
chart ends near the present because the strategy is still operating.
```

That's a complete preset. Save as `content/timelines/private-equity-news.md`,
run `python3 scripts/generate_content.py`, restart Hugo, and it's live.

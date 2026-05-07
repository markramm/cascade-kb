# The Cascade Ledger — `capturecascade.org`

Custom Hugo site rendering the Capture Cascade Timeline as a standalone documentary archive at **[capturecascade.org](https://capturecascade.org)**. Optimized for SEO, exploration, shareable filtered views, and LLM ingestion.

## Quick start

```bash
./build.sh             # generate content + build static site → ../public-timeline/
./build.sh serve       # generate + run dev server on http://localhost:1313
./build.sh redirects   # regenerate the legacy → new redirect map
./build.sh og          # regenerate the 400 most-recent OG card PNGs
./build.sh og --all    # regenerate the full OG card corpus (~20 min, ~3 GB)
```

## Architecture

```
hugo-timeline/
├── hugo.toml                          # taxonomies, permalinks, output formats
├── scripts/
│   ├── generate_content.py            # ../cascade-timeline/*.md → content/event/*.md + data/*
│   ├── generate_og_cards.py           # PNG OG cards for the 400 most-recent events
│   └── generate_redirects.py          # 301s from legacy /site/cascade-timeline/* paths
├── content/                           # generated Hugo content (do not edit by hand)
│   ├── _index.md                      # homepage front-matter
│   ├── about/                         # methodology, sources, contribute, license
│   ├── q/                             # filter view (loads timeline.json client-side)
│   └── event/                         # 5,021 generated event pages
├── data/                              # build-time data (Hugo reads via site.Data.*)
│   ├── density.json                   # per-year event counts → homepage chart
│   ├── resonance.json                 # mm-dd → events for "on this day" lookups
│   ├── co_actors.json                 # actor → top-24 co-occurring actors
│   └── quality.json                   # source-data sanitizer warnings
├── static/
│   ├── _redirects                     # 5,103 legacy → canonical redirects (Netlify/CF Pages)
│   ├── redirects.nginx.conf           # same redirects, nginx map syntax
│   ├── redirects.htaccess             # same redirects, Apache RewriteRule syntax
│   ├── data/
│   │   ├── timeline.json              # 5 MB denormalized dataset for /q/ filter
│   │   ├── actors.json                # lazy-loaded actor catalog (lazy-load)
│   │   └── tags.json                  # lazy-loaded tag catalog (lazy-load)
│   ├── og/event/*.png                 # 400 OG cards for recent events
│   ├── og/default.svg                 # Open Graph fallback card
│   └── robots.txt                     # explicit AI-crawler allowlist
├── assets/css/main.css                # the entire visual language
└── layouts/
    ├── _default/
    │   ├── baseof.html                # head: SEO meta, JSON-LD, Dataset markup
    │   ├── taxonomy.html              # term + taxonomy index pages (.Kind branch)
    │   ├── section.html               # generic section listing
    │   ├── single.html                # about subpages
    │   ├── filter.html                # /q/ filter view
    │   ├── rss.xml                    # custom RSS for the event feed
    │   └── sitemap.xml                # sitemap-index pointing to fragments
    ├── partials/schema.html           # per-page Article/CollectionPage/Breadcrumb JSON-LD
    ├── event/single.html              # event single page (the centerpiece)
    ├── event/list.html                # full ledger, paginated
    ├── index.html                     # homepage (density chart + recent + on-this-day)
    ├── index.json                     # machine-readable site index
    ├── index.sitemap{events,actors,tags,meta}.xml  # sitemap fragments
    └── 404.html                       # custom 404 in the ledger style
```

## SEO architecture

| Page kind        | Schema.org @type     | Indexed surface                                  |
| ---------------- | -------------------- | ------------------------------------------------ |
| Home             | `Dataset` + `WebSite`| Dataset Search, Knowledge Graph, sitelinks       |
| Event single     | `Article` + `Event`  | News / article cards, BreadcrumbList             |
| Year/Decade term | `CollectionPage`     | Long-tail: "events in 1986", "1990s timeline"    |
| Actor term       | `CollectionPage`+`Person`/`Organization` | Per-actor pages with ≥3 events  |
| Tag term         | `CollectionPage`+`DefinedTerm` | Per-tag pages with ≥3 events           |
| Lane term        | `CollectionPage`+`Thing` | Capture-lane theme pages                     |
| Filter (`/q/`)   | (canonical + URL-state) | Reproducible reports as citations             |

The homepage emits a full `Dataset` JSON-LD block with `temporalCoverage`, `variableMeasured`, and `distribution[]` pointing to `/data/timeline.json` and the RSS feed. This is what makes Google treat the corpus as a **dataset surface**, not just a website.

**Thin pages** (actor or tag with <3 events) emit `noindex,follow` so Google crawls the navigation but doesn't add them to the index. They're also excluded from the per-section sitemap fragments.

**Sitemap fragmentation:** the master `/sitemap.xml` is a sitemap-index pointing to four fragments — `sitemap-events.xml` (5,021), `sitemap-actors.xml` (1,534 with ≥3 events), `sitemap-tags.xml` (1,806 with ≥3 events), `sitemap-meta.xml` (452 — home, lanes, year/decade, about pages, filter). Total indexed surface ≈ 9,500 URLs.

## Filter URLs (the share mechanism)

`/q/?actor=Donald%20Trump&from=2025&lane=democratic` — every filter mutation updates the URL, the title, and the lede. **Copy link** copies the canonical URL; **Cite** generates a one-line citation block ready to paste into footnotes.

The page server-renders the 50 most-recent events as a starter table (so crawlers see real content) and then JS replaces it when filters are applied.

## Legacy URL migration

The legacy site under `capturecascade.org/site/cascade-timeline/...` redirects 1:1 to the new canonical paths. `scripts/generate_redirects.py` fetches the old sitemap, matches each old URL to the new corpus, and emits redirect rules in three formats:

- `static/_redirects` — Netlify / Cloudflare Pages
- `static/redirects.nginx.conf` — nginx `map` + `if` block
- `static/redirects.htaccess` — Apache RewriteRule

Of the 5,101 old URLs, **5,075 (99.5%) get permanent (301) redirects** to exact new paths. The remaining 28 (events the old site emitted under bare title-slugs without date prefixes) get fallback (302) redirects to `/q/?search=<terms>` so Google's link equity lands on a useful page.

## Data flow

1. Pyrite KB at `../cascade-timeline/` holds the source of truth (5,021 events with YAML frontmatter)
2. `scripts/generate_content.py` parses each `.md`, resolves `[[wikilinks]]`, runs the quality sanitizer, emits:
   - one `content/event/<slug>.md` per event
   - `data/density.json`, `data/resonance.json`, `data/co_actors.json`, `data/quality.json`
   - `static/data/timeline.json` (filter dataset)
   - `static/data/actors.json`, `static/data/tags.json` (lazy-load catalogs)
   - `static/robots.txt` with explicit AI-crawler rules
3. `scripts/generate_og_cards.py` creates 400 PNG OG cards (1200×630, parchment + oxblood + Cormorant Garamond)
4. `scripts/generate_redirects.py` emits the legacy → canonical redirect map
5. Hugo builds → `../public-timeline/` (~38,000 pages, ~9,500 indexed, ~3.9 GB on disk)
6. Deploy as static files; the `_redirects` file works on Netlify/Cloudflare Pages out of the box, or use the nginx/.htaccess equivalents

## Visual language

- **Typography:** Cormorant Garamond (display) + Source Serif 4 (body) + JetBrains Mono (data) + Inter Tight (UI). Deliberately distinct from the detention-pipeline site (Instrument Serif + IBM Plex Sans) so the projects read as siblings rather than twins.
- **Palette:** parchment `#f3efe6`, oxblood `#7a1f1f`, ink `#1c1a17`. Five capture-lane hues (oxblood, moss, gilt, slate-blue, aubergine).
- **Motif:** vertical time-spine on every event page; full-width density chart on the homepage; ledger-style two-rule borders for stat blocks; oxblood eyebrow + italic Cormorant lede across page heads.
- **Dark mode:** automatic via `prefers-color-scheme: dark` — plate-black background, cream type. Density-chart bars switch to `var(--ink-2)` / `var(--ink)` / `var(--ox-hot)` for visibility.

## License

- **Data:** CC BY-SA 4.0 (inherits from `cascade-timeline/`)
- **Code:** MIT

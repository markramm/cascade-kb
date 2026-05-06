---
id: audit-210-trump-2-era-timeline-entries-with-no-canonical-capture-lanes-values
title: Audit 210 Trump-2-era timeline entries with no canonical capture_lanes values
type: task
importance: 5
status: open
priority: 5
---

Gap analysis (2026-04-23): 210 of 1,930 cascade-timeline entries dated 2025 or 2026 carry no value from the canonical-17 capture_lanes set. Root causes appear to be: (a) field uses `capture_lane` singular (29 total entries, some of them in this range); (b) quote-leakage variants (`'Media Capture & Control`, `'Digital & Tech Capture`) — 92 files total corpus-wide; (c) entries using one-off event-specific strings that belong in tags, not lanes; (d) entries that genuinely have no capture_lanes populated.

This is blocking the pyrite/backlog/canonicalize-capture-lanes-taxonomy-cascade-timeline migration — we need a clean denominator.

## Research needed
- Enumerate the 210 entries
- Classify each: (a) singular-field fixable, (b) quote-leakage fixable, (c) relocate to tags, (d) genuinely needs classification
- For category (d), assign canonical lanes based on title and body
- Produce a CSV or markdown report: entry-id | current-field-value | proposed-canonical-lanes | notes

## Produces
- Report file: `cascade-research/notes/2026-04-23-unclassified-timeline-entries-audit.md`
- Optional: PR-ready patch file for batch frontmatter updates

## Scope guard
Classification only — do not materially rewrite entry bodies. If an entry has insufficient information for classification even after reading the body, flag it as 'needs-research' in the report.

## Related
- `pyrite/backlog/canonicalize-capture-lanes-taxonomy-cascade-timeline` (depends on this audit for clean migration)
- `pyrite/backlog/add-blocked-on-optional-field-to-task-schema` (parallel pyrite schema work)

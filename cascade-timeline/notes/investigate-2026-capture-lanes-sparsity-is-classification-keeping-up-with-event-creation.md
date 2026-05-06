---
id: investigate-2026-capture-lanes-sparsity-is-classification-keeping-up-with-event-creation
title: Investigate 2026 capture_lanes sparsity — is classification keeping up with event creation?
type: task
importance: 5
status: open
priority: 6
---

Gap analysis (2026-04-23): 2026 timeline entries show dramatic drops in capture_lanes classification rates relative to 2025 — Intelligence Penetration 202→8, Electoral Manipulation 72→8, International Kleptocracy 96→5, Media Capture & Control 162→14, Financial Capture 237→24. At 4/12 of the year elapsed (through April 23), expected 2026 counts should be ~33% of 2025. Most lanes are under 10%. Some of this is real (short year, reporting lag, investigation focus on inv1/4/5), but the proportions are off enough to suggest a classification-pipeline issue rather than a content-volume issue.

## Hypotheses to test
1. Recent 2026 entries (e.g., post-March /loop /daily-capture dispatches) are populating `capture_lanes` less consistently than 2025 entries did
2. New lane strings have emerged in 2026 (e.g., 'Executive Power Consolidation', 'Business Lobby Influence' — both seen in April 2026 entries) that are drift from canonical set
3. 2026 entries are using tags/themes instead of capture_lanes as the primary classifier
4. Investigation-focused batch entries (the April 23 RAMM coverage pass) skipped capture_lanes entirely because focused on timeline position

## Research needed
- Sample 20 recent (April 2026) timeline entries — check capture_lanes population rate, canonical-vs-drift
- Sample 20 early 2026 entries — compare classification patterns
- Check daily-capture skill output and batch-ingestion scripts for whether they populate capture_lanes
- Identify which lanes appear genuinely absent (content gap) vs present-but-unclassified (process gap)

## Produces
- Brief report in `cascade-research/notes/` on findings
- Recommendations: fix daily-capture skill, update ingestion scripts, add validation hook, or (if real content gap) new research tickets per lane

## Scope guard
Not classification backfill — that's the 210-audit ticket. This is diagnosis of why 2026 looks sparse.

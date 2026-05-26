---
type: timeline_event
id: 2026-05-26--defense-ai-vertical-sbir-phase-iii-sole-source-fingerprint-systemic-fpds-audit
date: '2026-05-26'
title: "FPDS Audit Finds SBIR Phase III 'Exclusion of Sources' Sole-Source Fingerprint Systemic Across Defense-AI Startup Cohort — $1.0B+ Non-Competitive, 91% Anduril; Larger Firms Route Around FPDS via OTA"
importance: 7
status: confirmed
tags:
  - investigation-2
  - cross-investigation
  - fpds-audit
  - sbir-phase-iii
  - sole-source
  - defense-ai
  - procurement-bypass
  - anduril
  - shield-ai
  - vannevar-labs
  - palantir
  - scale-ai
  - saronic
  - spacex
  - openai
  - ota-vs-sbir
  - captured-x
  - accountability-bypass
actors:
  - Anduril Industries
  - Palantir Technologies
  - Shield AI
  - Vannevar Labs
  - Scale AI
  - Saronic Technologies
  - SpaceX
  - OpenAI
  - U.S. Department of Defense (CDAO)
  - U.S. Customs and Border Protection (CBP)
sources:
  - title: "USAspending.gov API award-detail endpoint (FPDS-NG mirror) — extent_competed / number_of_offers_received / type_set_aside fields"
    url: https://api.usaspending.gov/api/v2/awards/
    publisher: U.S. Treasury / USAspending.gov
    date: '2026-05-26'
    tier: 1
  - title: "Anduril IDIQ 70B02C20D00000019 — After Exclusion of Sources, 1 offer, Small Business Set-Aside Total"
    url: https://api.usaspending.gov/api/v2/awards/CONT_IDV_70B02C20D00000019_7014/
    publisher: USAspending.gov (FPDS-NG)
    date: '2026-05-26'
    tier: 1
  - title: "Shield AI N6833524G0022 — IDV titled 'SBIR PHASE III BOA'"
    url: https://api.usaspending.gov/api/v2/awards/CONT_IDV_N6833524G0022_9700/
    publisher: USAspending.gov (FPDS-NG)
    date: '2026-05-26'
    tier: 1
  - title: "OpenAI wins $200 million U.S. defense contract (CDAO OTA, not in FPDS)"
    url: https://www.cnbc.com/2025/06/16/openai-wins-200-million-us-defense-contract.html
    publisher: CNBC
    date: '2025-06-16'
    tier: 1
  - title: "Navy moves to buy autonomous maritime drones from Saronic via $392M OTA"
    url: https://defensescoop.com/2025/08/22/navy-buy-saronic-autonomous-maritime-drones-usv-asv-ota/
    publisher: DefenseScoop
    date: '2025-08-22'
    tier: 1
capture_lanes:
  - Defense Procurement Capture
  - Regulatory Capture
coverage: []
---

## Opening

A systematic FPDS-NG audit (via the USAspending.gov API, 2026-05-26) of eight defense-AI firms tested whether the SBIR Phase III sole-source fingerprint — `extent_competed = "Full and Open After Exclusion of Sources"` with `1 offer received`, the FPDS signature of a 15 U.S.C. § 638(r)(4) award — is unique to Anduril or systemic across the vertical. The audit examined 1,005 contract and IDV records across Anduril, Palantir, Shield AI, Vannevar Labs, Scale AI, Saronic, SpaceX, and OpenAI. Finding: the fingerprint is **systemic within the early-scaling startup cohort** (confirmed at Anduril, Shield AI, and Vannevar Labs), while the largest/newest entrants achieve the same non-competitive outcome through a parallel rail — Other Transaction Authority (OTA) — that sits outside FPDS competition coding entirely.

## What Happened / Key Facts

Across the vertical, **$1,008.4M in obligations carried the "After Exclusion of Sources" sole-source coding across 56 records — 91% of it Anduril's** ($913.6M, dominated by the CBP Autonomous Surveillance Towers IDIQ 70B02C20D00000019, which the parent vehicle confirms at 1 offer received, Small Business Set-Aside Total).

The audit splits the vertical into two procurement-architecture classes:

- **SBIR-pathway (the fingerprint applies)** — Anduril ($913.6M), Shield AI ($19.1M; its Navy IDV is literally titled "SBIR PHASE III BOA"), and Vannevar Labs ($14.0M; its $13M STRATFI-Velocity award is exclusion-of-sources + small-business set-aside + 1 offer). These VC-backed firms banked DOD SBIR Phase I/II predicates while still small, then took sole-source Phase III production awards. Palantir is a transitional case: it uses the exclusion-of-sources coding ($60.9M) but via non-SBIR authority, "No Set-Aside Used," having long outgrown small-business status.
- **OTA-pathway (the fingerprint does NOT apply)** — OpenAI (zero FPDS records; $200M CDAO OTA), Scale AI (residual $0.7M only; $500M CDAO + Thunderforge all OTA; 49% Meta-owned, no longer small), Saronic ($500 FPDS micro-contract only; $392M Navy OTA), and SpaceX (258 records, zero exclusion-of-sources; competed launch contracts).

Per Bloomberg-tier reporting and federal primary data, both rails produce the same end state — large-dollar awards with no peer-competitor opportunity — through different statutory doors. Which rail a firm uses is a function of *when it scaled*: firms that banked a small-business SBIR Phase I/II predicate ride the SBIR Phase III rail; firms that arrived already large ride the OTA rail.

## Why This Event Matters

The W93-e Anduril finding (commit 42bc13ea) is not an idiosyncrasy — the SBIR Phase III "exclusion of sources" sole-source mechanism is **shared accountability-bypass infrastructure** adopted by a class of VC-backed defense-AI startups, generalizing the `architectural-gap-exploitation` captured-X variant from single-firm to firm-class scope. Equally important, the audit reveals that **FPDS-based competition audits systematically undercount defense-AI non-competitive procurement**: the largest and newest entrants (OpenAI, Scale AI, Saronic) route around FPDS via OTA, so a competition audit that looks only at FPDS coding misses the majority of the vertical's non-competitive dollar flow.

## Broader Context

Both mechanisms are facially legal. SBIR Phase III under 15 U.S.C. § 638(r)(4) requires no competition; the J&A need only assert the work derives from prior SBIR funding. OTA under 10 U.S.C. § 4022 bypasses FAR competition requirements for prototype and follow-on production. The structural accountability gap is that no framework assesses the cumulative non-competitive position of the defense-AI vertical as a unified fact across either rail.

## Research Gaps

- [ ] OTA dollar volumes for Class-2 firms via DoD OTA consortium data (SOSSEC, NSTXL, DIU)
- [ ] Task-order-level offers-received cross-check via raw FPDS-NG atom feed (USAspending mirror has sentinel-garbage values)
- [ ] J&A documents for Shield AI and Vannevar SBIR Phase III awards — originating Phase I/II contract numbers (FOIA)

## Related Entries

- [[anduril-phase-iii-sbir-pathway-investigation-pack]]
- [[systematic-fpds-audit-defense-ai-vertical-exclusion-of-sources-sbir-phase-iii-fingerprint-pack]]
- [[five-layer-stack-defense-ai-infrastructure-anduril-vertical]]
- [[palantir-anduril-two-firm-backbone-us-defense-ai-infrastructure]]

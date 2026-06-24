---
type: timeline_event
id: 2016-01-01--dhs-hart-homeland-advanced-recognition-technology-program-initiated-replacing-ident
date: '2016-01-01'
title: "DHS Initiates HART Program to Replace IDENT: 290M+ Identity Biometric Backbone; GAO Finds Significant Management and Privacy Shortcomings in 2023"
importance: 8
status: confirmed
tags:
  - biometric-surveillance
  - dhs-obim
  - hart
  - ident
  - surveillance-infrastructure
  - facial-recognition
  - database-consolidation
  - privacy-impact-assessment
  - gao-audit
  - investigation-surveillance-inc
actors:
  - DHS Office of Biometric Identity Management (OBIM)
  - Northrop Grumman Corporation
  - Peraton (Veritas Capital)
  - Government Accountability Office
sources:
  - title: "Biometric Identity System: DHS Needs to Address Significant Shortcomings in Program Management and Privacy (GAO-23-105959)"
    url: https://www.gao.gov/products/gao-23-105959
    publisher: Government Accountability Office
    date: '2023-09-12'
    tier: 1
  - title: "Homeland Security: DHS Needs to Fully Implement Key Practices in Acquiring Biometric Identity Management System (GAO-21-386)"
    url: https://www.gao.gov/products/gao-21-386
    publisher: Government Accountability Office
    date: '2021-06-08'
    tier: 1
  - title: "Homeland Security centralizes control over the government's largest biometrics database"
    url: https://fedscoop.com/homeland-security-centralizes-control-over-the-governments-largest-biometrics-database/
    publisher: FedScoop
    date: '2025-08-14'
    tier: 2
  - title: "Northrop Grumman Wins $95M DHS Contract for HART Biometric System Development"
    url: https://intelligencecommunitynews.com/northrop-grumman-wins-95m-dhs-contract/
    publisher: Intelligence Community News
    date: '2018-02-27'
    tier: 3
  - title: "Inside the HART of the DHS Office of Biometric Identity Management"
    url: https://www.biometricupdate.com/201809/inside-the-hart-of-the-dhs-office-of-biometric-identity-management
    publisher: Biometric Update
    date: '2018-09-04'
    tier: 2
  - title: "IDENT/HART entry — From Data Criminalization to Prison Abolition"
    url: https://abolishdatacrim.org/en/bestiary/identhart
    publisher: Abolish Data Criminalization
    date: '2022-05-01'
    tier: 2
capture_lanes:
  - Surveillance Infrastructure
  - Digital and Tech Capture
  - Immigration System Capture
coverage: []
---

In 2016, the Department of Homeland Security's Office of Biometric Identity Management (OBIM) initiated the Homeland Advanced Recognition Technology (HART) program to replace IDENT, the legacy Automated Biometric Identification System operational since 1994. HART is designed to become the federal government's primary biometric identity platform — a multi-modal database targeting hundreds of millions of identities encompassing fingerprints, facial recognition, iris scans, voice prints, DNA, and signatures. As of April 2023, the legacy IDENT system already stored more than 290 million separate identities. A September 2023 GAO audit (GAO-23-105959) found "significant shortcomings in program management and privacy," including missing Privacy Impact Assessment data, inadequate controls over partner agencies' handling of personally identifiable information, and only 5 of 12 OMB privacy requirements fully implemented.

## What Happened / Key Facts

**Program initiation:** DHS initiated HART in 2016 to replace IDENT, which was designed in 1994, implemented in 1995, and had grown to 230 million unique identities by 2018, processing approximately 350,000 fingerprint queries per weekday. Per Biometric Update (September 2018), IDENT was the second-largest biometric system in the world at that time, behind India's Aadhaar.

**Biometric scope:** HART is designed for multi-modal collection beyond IDENT's primarily fingerprint-and-photo architecture. Per the abolishdatacrim.org synthesis (citing DHS PIAs and EFF research), planned modalities include face, fingerprints, iris scans, voice prints, DNA results, and a blanket "other modalities" category. Data is drawn from FBI's Next Generation Identification (NGI) system, travel documents, employment files, and DMV records — covering U.S. citizens, permanent residents, and non-citizens.

**Scale:** The legacy IDENT system stored more than 290 million distinct identities as of April 2023, per OBIM officials cited in GAO-23-105959. FedScoop (August 2025) reported the consolidated system (under DHS CIO Antoine McCord) houses more than 300 million profiles from facial recognition, fingerprints, and iris scans.

**Primary contract:** In February 2018, DHS awarded Northrop Grumman a $95 million contract to develop Increments 1 and 2 of HART — a 42-month systems development and integration effort. Northrop Grumman was subsequently replaced by Peraton (a Veritas Capital subsidiary) after Peraton acquired Northrop Grumman's federal IT services business in 2020.

**Technology platform:** Data is stored on Amazon Web Services GovCloud infrastructure.

**Schedule and cost overruns documented by GAO:**
- Initial operational capability was pushed from December 2020 to September 2023 — a 33-month slip beyond the 2019 plan per GAO-23-105959
- A third rebaseline was required in April 2023 due to "higher than expected software defects and performance issues"
- The 2022 rebaseline added $354 million to estimated program costs
- Total cost estimate as of GAO-21-386 (2021): $4.3 billion

**GAO-23-105959 governance findings (September 2023):**
- Cost and schedule estimates do not adhere to GAO best practices, making them unreliable for leadership decision-making
- Privacy Impact Assessment contains missing information regarding data subjects and information-sharing partners
- Insufficient assurances that partner agencies properly retain and dispose of personally identifiable information
- Only 5 of 12 OMB privacy requirements were fully implemented
- GAO issued nine recommendations

## Why This Event Matters

HART is the intermediate node in the database-consolidation spine connecting the 2007 FBI watchlist error-rate scandal to the 2026 DHS unified biometric matching engine. The GAO-23-105959 governance finding — "significant shortcomings in program management and privacy" — directly echoes the 2007 Inspector General finding of 35% error rates and no formal record-removal processes in the TSDB watchlist. Both findings document the same structural pattern: a massive population-scale database built and expanded before governance frameworks catch up, with the accountability surface thinning as the data scale grows.

The biometric scope of HART marks a qualitative shift from the IDENT model. Where IDENT was primarily a fingerprint and photograph repository for individuals who had crossed DHS's enforcement perimeter, HART's planned modalities (voice, DNA, iris, signatures) and data-sharing architecture extend the collection surface to routine civilian encounters — DMV records, employment verification, travel — regardless of any enforcement contact. The system enables identification "absent notice and consent" in public spaces, per advocacy synthesis.

The third-party doctrine cover (United States v. Miller, 1976, authored by Lewis Powell) makes biometric data "voluntarily conveyed" to state and federal agencies — driver's license photos, border crossing fingerprints, employment verification scans — constitutionally unprotected from database consolidation. HART is the infrastructure that operationalizes that doctrine at 290M+ identity scale.

## Broader Context

HART sits between two committed timeline nodes in the database-consolidation lineage:
- **Upstream:** [[2007-09-01--fbi-watchlist-35-percent-error-rate]] — TSDB 1M+ records, 35% error rate, no removal process; same governance-gap pattern
- **Downstream:** [[2026-02-20--dhs-unified-biometric-matching-engine-facial-recognition]] — DHS plans unified matching engine across agencies; 1.2B images (Bloomberg); directly built on HART/OBIM infrastructure

The consolidation latency continues to collapse: 41 years (1966 HUAC→2007 TSDB) → 9 years (2007→2016 HART initiation) → 10 years (2016→2026 unified engine). Each consolidation event expands the target population (suspects → watchlisted → all border crossers → all government-document holders) while governance mechanisms lag.

ICE operates a parallel 200-million-identity facial recognition database separate from OBIM's HART, per FedScoop (2025). The August 2025 centralization under DHS CIO McCord (see [[timeline-write-obim-centralized-under-dhs-cio-mccord-2025-08-14]] — *needs entry*) is the bridge between HART's development phase and the 2026 unified engine announcement.

## Research Gaps

- [ ] Exact month in 2016 when HART program was formally initiated (GAO reports confirm year; specific date not publicly sourced)
- [ ] Whether Palantir Foundry and the HART/IDENT backbone interoperate at the contract/data layer
- [ ] DHS PIA-004 full text (403 Forbidden on direct fetch) — detailed collection categories and data-sharing partner list
- [ ] Smith v. Maryland (1979) as second third-party doctrine pillar — not yet a committed timeline node

## Related Entries

- [[2007-09-01--fbi-watchlist-35-percent-error-rate]] — upstream database-consolidation node; same governance-gap pattern
- [[2025-01-29--dhs-st-pia-044-cloud-based-biometric-analytic-environment-cbae-update]] — CBAE R&D pipeline feeding into HART architecture
- [[2026-02-20--dhs-unified-biometric-matching-engine-facial-recognition]] — downstream consolidation; 1.2B image unified engine
- [[obim-office-of-biometric-identity-management]] — *needs entry* — OBIM is the operational home of both IDENT and HART
- [[surveillance-mega-database-lineage-connector-1966-2026-dossier-consolidation-cointelpro-to-palantir]] — parent theme

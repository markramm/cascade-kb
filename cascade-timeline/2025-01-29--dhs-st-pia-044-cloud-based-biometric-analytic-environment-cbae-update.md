---
type: timeline_event
id: 2025-01-29--dhs-st-pia-044-cloud-based-biometric-analytic-environment-cbae-update
date: '2025-01-29'
title: "DHS S&T publishes updated PIA-044 for Cloud-Based Biometric Analytic Environment (CBAE) — documents DEBIASE R&D data flows on AWS GovCloud"
importance: 7
status: confirmed
tags:
  - investigation-surveillance-inc
  - dhs-st-directorate
  - biometrics
  - privacy-impact-assessment
  - pia
  - cbae
  - debiase
  - saic
  - lrbaa
  - facial-recognition
  - surveillance-rd-pipeline
  - cbp
  - biometric-identity
actors:
  - DHS Science & Technology Directorate
  - Biometrics and Identity Technology Center (BI-TC)
  - Science Applications International Corporation (SAIC)
  - DHS Privacy Office
sources:
  - title: "DHS/S&T/PIA-044 Cloud-based Biometric Analytic Environment — January 2025 update"
    url: https://www.dhs.gov/sites/default/files/2025-01/25_0129_priv-pia-st044-cbae_1.pdf
    publisher: DHS Privacy Office / DHS S&T BI-TC
    date: '2025-01-29'
    tier: 1
  - title: "DHS/S&T/PIA-044 publication page"
    url: https://www.dhs.gov/publication/dhsstpia-044-cloud-based-biometric-analytic-environment
    publisher: DHS Privacy Office
    date: '2025-01-29'
    tier: 1
  - title: "Some risks remain in cloud-based biometric research system, DHS report says"
    url: https://www.biometricupdate.com/202403/some-risks-remain-in-cloud-based-biometric-research-system-dhs-report-says
    publisher: Biometric Update
    date: '2024-03'
    tier: 2
capture_lanes:
  - Surveillance-Inc-Privatized-Surveillance-Industrial-Complex
  - DHS-S&T-SBIR-LRBAA-R&D-Pipeline
coverage: []
---

## Opening

On January 29, 2025, DHS Science & Technology Directorate published an updated Privacy Impact Assessment (DHS/S&T/PIA-044) for the **Cloud-Based Biometric Analytic Environment (CBAE)** — the AWS GovCloud environment operated by SAIC's Identity and Data Sciences Lab (IDSL) under the DHS S&T Biometrics and Identity Technology Center (BI-TC). The CBAE is the technical environment where biometric data from DHS component operations flows back into R&D programs, including DEBIASE (LRBAA contract 70RSAT23CB0000003, $59,194,224.67, August 2023).

## What Happened / Key Facts

The **Cloud-Based Biometric Analytic Environment** was first documented in a March 2024 PIA and updated in January 2025. Key documented facts:

- **System operator**: DHS S&T Biometrics and Identity Technology Center (BI-TC), with SAIC's Identity and Data Sciences Lab (IDSL) operating the underlying Maryland Test Facility (MdTF) infrastructure.
- **Infrastructure**: Hosted on Amazon Web Services S&T GovCloud partition.
- **Data flows**: DHS component agencies (CBP, TSA, USSS, and others) share biometric, biographic, and demographic datasets with DHS S&T. Per the PIA, data is "minimized to only those items necessary to perform research" by the contributing component prior to transfer; the respective DHS Component CIO confirms minimization before transfer.
- **Biometric modalities evaluated**: Facial recognition, iris recognition, fingerprint recognition.
- **Purpose**: Research, development, testing, and evaluation (RDT&E) of biometric collection, matching, and processing tools "currently in use or may be used by DHS."
- **Privacy risks identified in March 2024 initial PIA (partially mitigated in January 2025 update)**:
  - Inaccurate or incomplete biometric, biographic, and demographic information used in research;
  - PII potentially used without proper consent;
  - Limited options for individuals to correct inaccurate information.
- **Mitigations applied**: Encryption, access minimization, data sharing restrictions, compliance guidelines.

## Why This Event Matters

PIA-044 is the **primary-source document establishing the legal compliance basis for DEBIASE's research infrastructure**. The DEBIASE contract (LRBAA, SAIC, $59M, 2023) named the Biometrics and Identity Technology Center and its MdTF testing programs as its R&D substrate. CBAE is the AWS-hosted environment where that R&D operationalizes. The January 2025 PIA update — coming two years into DEBIASE's five-year performance period and two months after the CBP Final Rule (2025-19655) mandated universal biometric collection at land/sea/air borders — documents that the CBAE is the active analytical environment supporting the same biometric expansion the Final Rule authorizes.

The PIA's documented "partially mitigated" risks are structurally significant: they confirm that as of January 2025, the DHS BI-TC's biometric research environment did not fully resolve consent, accuracy, or correction gaps — while the operational TVS system it supports was simultaneously being extended to 100% of international travelers at all border environments.

For the **SBIR-to-operational pipeline tracing methodology**, CBAE PIA-044 establishes the **reverse data flow**: operational biometric data from CBP/TSA encounters flows back into S&T R&D (CBAE) for evaluation. This is the mechanism that makes the pipeline bidirectional — public R&D money incubates surveillance technology (SBIR/LRBAA forward), and operational surveillance data from deployed systems feeds back into R&D for next-generation capability development (CBAE return loop).

## Broader Context

CBAE PIA-044 sits within the DHS S&T PIA catalog as the most recently updated and research-active S&T privacy document. It is analytically adjacent to:
- **OIP Portal PIA-041** (August 2021): covers the administrative SBIR/BAA/SVIP portal through which all R&D contracts are submitted and deliverables filed;
- **CBP TVS PIA-056** (December 2025 update): the operational deployment PIA for the TVS facial-recognition system CBAE research directly supports;
- **GAO-23-105959**: GAO's 2023 finding that DHS IDENT/HART has significant program management and privacy shortcomings — independent corroboration that the CBAE's partially-mitigated risks exist within a broader governance-gap environment.

## Research Gaps

- [ ] Full text of January 2025 PIA-044 update (PDF access blocked at dhs.gov for automated agents; interactive session required)
- [ ] Identity of specific DEBIASE deliverables incorporated into CBAE operations; the PIA covers CBAE as a system but does not name specific R&D programs by contract number
- [ ] Which DHS components (CBP, TSA, USSS, ICE?) share data with CBAE, and under what data-sharing agreements (ISAs)
- [ ] Whether the March 2024 → January 2025 PIA update cycle reflects DEBIASE's option-year exercise (if the five-year contract's FY2025 option was exercised, a PIA update would be triggered by system scope expansion)

## Related Entries

- [[dhs-pia-as-primary-source-channel-sbir-to-operational-pipeline]] — mechanism entry documenting the full DHS PIA catalog as a pipeline-tracing tool
- [[saic-debiase-biometric-rd-to-operational-stack]] — DEBIASE contract is the R&D program CBAE supports
- [[dhs-sbir-as-surveillance-rd-incubation-pipeline]] — parent theme
- [[traveler-verification-service-tvs]] — *needs entry* — CBP's operational system; CBAE research targets TVS performance
- [[obim-office-of-biometric-identity-management]] — *needs entry* — runs IDENT/HART; downstream of CBAE research
- [[epic-surveillance-inc-privatized-surveillance-industrial-complex-2003-2026]] — parent investigation

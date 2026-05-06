---
type: timeline_event
id: 1997-06-01--nsa-sarc-signals-intelligence-automation-research-center-founded
date: '1997-06-01'
title: NSA Creates Signals Intelligence Automation Research Center, Binney and Wiebe Lead Bulk-Collection Technical Design
importance: 7
status: confirmed
actors:
  - William Binney
  - J. Kirk Wiebe
  - Ed Loomis
  - National Security Agency
  - Michael Hayden
tags:
  - sarc
  - nsa
  - thinthread
  - surveillance-infrastructure
  - binney
  - bulk-collection
sources:
  - title: "William Binney (intelligence official)"
    url: https://en.wikipedia.org/wiki/William_Binney_(intelligence_official)
    publisher: Wikipedia
    date: '2024-01-01'
    tier: 3
  - title: "Bio: William Binney and J. Kirk Wiebe"
    url: https://whistleblower.org/bio-william-binney-and-j-kirk-wiebe/
    publisher: Government Accountability Project
    date: '2021-01-01'
    tier: 2
  - title: "ThinThread"
    url: https://en.wikipedia.org/wiki/ThinThread
    publisher: Wikipedia
    date: '2024-01-01'
    tier: 3
  - title: "The FRONTLINE Interview: William Binney"
    url: https://www.pbs.org/wgbh/pages/frontline/government-elections-politics/united-states-of-secrets/the-frontline-interview-william-binney/
    publisher: PBS FRONTLINE
    date: '2014-05-13'
    tier: 2
capture_lanes:
  - Surveillance Infrastructure
  - Intelligence Penetration
coverage: []
---

## Opening

NSA establishes the Signals Intelligence Automation Research Center (SARC) in mid-1997 as an internal research and development unit focused on automated, targeted acquisition of signals intelligence from fiber-optic communications. William Binney, then Technical Director of NSA's World Geopolitical and Military Analysis, co-founds SARC and becomes its technical lead. With J. Kirk Wiebe and Ed Loomis, Binney leads development of a program first called "ThinThread" — an automated SIGINT collection and analysis system designed to process large volumes of communications while maintaining privacy protections for US persons through on-the-fly anonymization. SARC's 1997-2001 work becomes the lost path of NSA bulk collection: a technically sophisticated system that included U.S.-person privacy protections by design, rejected in 2001-2002 by NSA Director Michael Hayden in favor of the contractor-led Trailblazer program that abandoned the privacy features.

## What Happened / Key Facts

SARC's organizational position:

- **Within NSA's Directorate of Operations**: SARC was a small (initially ~100-person) R&D unit.
- **Technical focus**: Automated upstream acquisition of SIGINT from high-capacity fiber-optic lines; real-time traffic analysis to identify targets of interest; data selection and minimization.
- **Staffing**: Binney (co-founder, math PhD, cryptanalytic background), Wiebe (senior analyst), Loomis (systems engineer), approximately 100 engineers and analysts assembled from across NSA.

ThinThread design:

- **Volumetric capacity**: Designed to scan every packet on a 10-gigabit fiber-optic line — in 1997-2000 the state-of-the-art for telecom backbone capacity.
- **Automated analysis**: Identified communication patterns of interest (specified by analyst tasking), extracted and stored relevant traffic, discarded the rest.
- **Privacy by design**: US-person communications were automatically anonymized — names and identifying information replaced with hashed tokens — unless and until an analyst obtained specific authorization to "unmask."
- **Smart collection**: Rather than bulk collect all traffic and filter retrospectively, ThinThread selected at the moment of capture based on communication patterns and metadata analysis. This architecture both reduced storage requirements and inherently limited US-person exposure.
- **Cost**: Total development cost through 2001: approximately $3 million. ThinThread was ready to deploy by January 2001.

Competing Trailblazer program:

- **1999-2000 initial proposals**: Multiple contractor consortia propose large-scale bulk-collection systems. Principal competitor: Science Applications International Corporation (SAIC).
- **Trailblazer approach**: Large contractor-led system; bulk-first collection; privacy protections to be added after collection ("collect it all, sort later").
- **Cost projections**: Trailblazer projected at hundreds of millions of dollars.

Hayden's 2001-2002 choice:

- **Michael Hayden** (NSA Director 1999-2005): Chose Trailblazer over ThinThread.
- **Stated rationale**: Larger program, larger contractor participation, greater transformation of NSA's infrastructure.
- **Critics' view**: Binney and colleagues subsequently argued the choice was driven by contractor relationships and budget politics, not technical merit. Trailblazer's privacy-last architecture also happened to be the architecture Hayden wanted for post-9/11 warrantless collection.
- **Post-9/11 redirection**: After 9/11, Trailblazer conceptually absorbed by the warrantless Stellar Wind program; ThinThread's privacy features were specifically removed from any deployed system.

Whistleblowing trajectory:

- **Early 2000**: Binney and colleagues raise internal concerns about ThinThread vs. Trailblazer decision.
- **September 2002**: Binney, Wiebe, Loomis, and Diane Roark (HPSCI staffer) file DoD IG complaint alleging Trailblazer waste, fraud, and constitutional violations.
- **2005-2007**: IG investigation largely confirms their concerns about waste; constitutional issues classified.
- **2006-2007 NSA retaliation**: Binney's and Wiebe's homes raided by FBI (July 2007). No charges ever filed. Clearances revoked.
- **2012 forward**: Binney becomes the most public of the pre-Snowden NSA whistleblowers. His pre-Snowden public statements are substantially confirmed by 2013 Snowden disclosures.

## Why This Event Matters

SARC's founding is the origin point for the technical architecture of 21st-century NSA bulk collection and for the policy critique that privacy-preserving alternatives were available and rejected:

- **Privacy-preserving bulk collection was technically feasible in 2000.** ThinThread demonstrated — prior to 9/11 and prior to statutory expansion — that SIGINT-agency technology could be built to preserve US-person anonymity until specific authorization was obtained. The proposition that post-2001 bulk collection "required" abandoning privacy protections was already falsified by ThinThread's existence. This fact shapes every subsequent policy argument about whether NSA's 2001-2013 mass collection programs were necessary in their chosen form.
- **Contractor vs. in-house tension established.** The ThinThread vs. Trailblazer choice is the archetype of a post-1990s intelligence-community dynamic: in-house technical capability produces a working, cheap, effective system; contractor-led proposal produces a more expensive, less effective, more ambitious alternative; intelligence leadership chooses the contractor option for reasons that include but are not limited to technical merit. The pattern recurs in every large post-2000 intelligence IT program (NSA Turbulence/Trailblazer; CIA AIN; FBI Sentinel / Virtual Case File; ODNI IC ITE).
- **Pre-Snowden whistleblower template.** Binney's path — internal concerns, formal IG complaint, retaliation, public disclosure without classified material — is the template later whistleblowers (Drake 2006-2007, Tamm, Snowden himself in some respects) drew on. The pre-existence of Binney's case is one reason post-Snowden discourse could distinguish between whistleblower paths (legal disclosure channels used but failed) and leak paths (direct disclosure without internal channels).

## Broader Context

The SARC/ThinThread story is one of the clearest empirical cases for the proposition that the post-9/11 surveillance-state expansion was a policy choice rather than a necessary technical response. ThinThread existed, was tested, was ready to deploy, was privacy-preserving. The decision to instead build Trailblazer and later Stellar Wind was made by specific individuals (Hayden, Cheney, Addington, Yoo) for reasons including but not limited to the privacy features of the rejected alternative.

Binney's post-2007 public advocacy — particularly his 2012-2013 claim that NSA was conducting "mass surveillance" of Americans — was the principal pre-Snowden public argument that the 2001-2007 warrantless program and its successors were much broader than government representations. Snowden material in June 2013 confirmed Binney's claims in substantial detail. The fact that Binney had been publicly making these claims for years before Snowden — and had been largely dismissed by the mainstream press — is a significant feature of the pre-2013 surveillance-disclosure information environment.

## Research Gaps

- [ ] Full ThinThread technical documentation — classified, partially released via FOIA
- [ ] NSA internal records of Hayden's 2001-2002 decision-making on Trailblazer vs. ThinThread — largely classified

## Related Entries

- [[1952-11-04--nsa-founded-by-classified-directive]]
- [[1994-10-25--calea-signed-digital-telephony-surveillance-mandate]]
- [[2001-10-04--nsa-stellar-wind-authorization]]
- [[2006-01-29--nsa-trailblazer-program-failure-saic-billion-dollar-waste]]
- [[2007-11-15--thomas-drake-reports-nsa-trailblazer-waste-surveillance-expansion]]

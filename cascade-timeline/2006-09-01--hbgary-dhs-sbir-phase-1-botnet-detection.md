---
type: timeline_event
id: 2006-09-01--hbgary-dhs-sbir-phase-1-botnet-detection
date: '2006-09-01'
title: "DHS awards HBGary, Inc. $100,000 SBIR Phase I contract for botnet detection — the upstream R&D seed of the Team Themis pipeline"
importance: 7
status: confirmed
tags:
  - investigation-surveillance-inc
  - dhs-sbir
  - hbgary
  - botnet-detection
  - cyber-network
  - rd-incubation
actors:
  - HBGary, Inc.
  - Greg Hoglund
  - DHS Science and Technology Directorate
sources:
  - title: "HBGary Inc SBIR award data (local DHS R&D pipeline dataset)"
    url: file:///Users/markr/kb-research/dhs-rd-pipeline/companies.json
    publisher: DHS Office of Industry Partnership leak (DDoSecrets, March 2023)
    date: '2023-03-01'
    tier: 1
  - title: "HBGary Inc SBIR award history"
    url: https://www.inknowvation.com/sbir/companies/hbgary-inc
    publisher: inknowvation.com
    date: '2024-01-01'
    tier: 2
capture_lanes:
  - Surveillance-Industrial Complex
coverage: []
---

## Opening

On September 1, 2006, DHS Science & Technology Directorate awarded HBGary, Inc. (Sacramento, CA) a Phase I SBIR contract of $100,000 under contract number NBCHC060136 for a project titled "Enterprise Botnet Detection System," under the topic "BOTNET DETECTION AND MITIGATION." The period of performance ran through March 15, 2007. This is the first documented federal investment in HBGary's technology base — the upstream seed of the capability pipeline that would produce HBGary Federal and the Team Themis information-operations proposal by 2010.

## What Happened / Key Facts

The award was a standard DHS SBIR Phase I — a six-month prototype seed at the statutory $100,000 cap. HBGary proposed to address botnet detection by targeting the host-based "weak link" rather than network traffic: behavioral analysis of the bot component itself, rather than signature-based detection of network anomalies. This approach — deep behavioral analysis of host-level processes — is the technical foundation for the memory forensics and malware analysis tools HBGary would commercialize over the following five years.

Per the dataset (DHS Office of Industry Partnership leak), the SBIR topic was "BOTNET DETECTION AND MITIGATION" and the theme classification is "cyber-network." This is purely defensive framing: the government client was DHS S&T, and the stated purpose was improving enterprise network security against botnet infections.

A Phase II award followed in December 2007 ($975,000, contract NBCHC080048, running through March 2011), confirming that HBGary successfully demonstrated its Phase I prototype.

## Why This Event Matters

This award is the documented starting point of the DHS-to-HBGary pipeline. The same behavioral analysis and memory forensics techniques funded here were matured through the Phase II contract, commercialized as HBGary Responder and Digital DNA, and formed the technical foundation of HBGary Federal's government-facing product line. HBGary Federal's offensive capability development (Magenta rootkit, persona management research) was downstream of the same technical base funded by this award.

The $100,000 seed demonstrates the DHS SBIR mechanism at its most basic: a nominal government investment in a small-business prototype that, if successful, generates a self-sustaining commercial capability no longer dependent on or constrained by the original government purpose.

## Related Entries

- [[2007-12-01--hbgary-dhs-sbir-phase-2-botnet-detection]]
- [[2011-02-06--hbgary-federal-anonymous-hack-team-themis-exposed]]
- [[hbgary-2006-2011-dhs-rd-to-civil-society-targeting-case-study]]
- [[dhs-sbir-as-surveillance-rd-incubation-pipeline]]

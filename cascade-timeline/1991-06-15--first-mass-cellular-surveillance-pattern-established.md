---
type: timeline_event
id: 1991-06-15--first-mass-cellular-surveillance-pattern-established
date: '1991-06-15'
title: FBI Cellular Surveillance Pilot Programs Establish Mass-Collection Template Before CALEA
importance: 5
status: confirmed
actors:
  - Federal Bureau of Investigation
  - William Sessions
  - Harris Corporation
  - National Security Agency
tags:
  - cellular-surveillance
  - stingray-predecessor
  - harris-corporation
  - surveillance-infrastructure
  - fbi
sources:
  - title: "Stingray phone tracker"
    url: https://en.wikipedia.org/wiki/Stingray_phone_tracker
    publisher: Wikipedia
    date: '2024-01-01'
    tier: 3
  - title: "Cell-Site Simulators/IMSI Catchers — Technical Background"
    url: https://www.aclu.org/documents/stingray-tracking-devices-whos-got-them
    publisher: American Civil Liberties Union
    date: '2018-01-01'
    tier: 2
  - title: "You are here: The FBI's Secret Stingray Program"
    url: https://www.justsecurity.org/9930/fbi-secret-stingray-program/
    publisher: Just Security
    date: '2014-05-01'
    tier: 2
capture_lanes:
  - Surveillance Infrastructure
  - Intelligence Penetration
coverage: []
---

## Opening

The FBI begins operational testing of cellular-interception technologies in 1991, working primarily with Harris Corporation on what would become the "Stingray" family of cell-site simulators. The initial 1991-1994 deployments — conducted under classified authority and without public disclosure — establish the operational template for mass cellular surveillance that evolves through the 2000s and 2010s into the ubiquitous law-enforcement tool documented in 2010s litigation. Cell-site simulators impersonate a legitimate cell tower, forcing mobile phones in the area to connect to the device, allowing law enforcement to capture device identifiers, location information, and (with additional hardware) call content. The 1991 FBI testing is contemporary with the earliest commercial cellular networks and demonstrates that surveillance capability against cellular communications was being engineered into law-enforcement use parallel to the network's emergence.

## What Happened / Key Facts

Technical background:

- **Cell-site simulator function**: Device emits cellular signals mimicking a legitimate cell tower. Nearby mobile phones preferentially connect to the strongest signal, so the simulator captures all phones in range that happen to be transmitting.
- **Initial capabilities (1991-1994)**: Capture of International Mobile Subscriber Identity (IMSI) — a unique identifier permanently associated with a SIM card. Basic location information.
- **Expanded capabilities (1998-2005)**: Content interception, SMS capture, more sophisticated protocol support as cellular technology advanced.
- **Mass-surveillance potential**: Because simulators capture all phones in range, not just targeted phones, they are inherently non-discriminating. Collection against a specific target necessarily collects against all nearby non-targets.

FBI 1991-1994 deployments:

- **Harris Corporation partnership**: Harris, a defense contractor based in Melbourne, Florida, became the FBI's principal supplier of cellular-interception equipment.
- **Classification**: Technology and deployments classified at SECRET level or above. Operational security strongly enforced.
- **Policy framework**: FBI internal policy required deployment authorization from senior headquarters officials. No court-order regime specifically covered cell-site simulator use at this time.
- **Pre-CALEA context**: Because CALEA ([[1994-10-25--calea-signed-digital-telephony-surveillance-mandate]]) had not yet been enacted, there was no statutory framework requiring carrier cooperation with cellular surveillance. Cell-site simulators provided a technical workaround — law enforcement operated independently of carriers.

Operational secrecy:

- **Non-disclosure agreements**: FBI required state and local law enforcement agencies acquiring Harris cell-site simulators to sign NDAs specifying that simulator use would not be disclosed in court filings. Agencies were required to drop prosecutions rather than reveal simulator use if challenged.
- **Pen register orders as cover**: Simulator use was typically authorized under generic pen-register orders that did not specify the technology used. Courts ruling on pen-register orders were not informed simulators would be deployed.
- **Parallel reconstruction**: Where simulator-captured material was used to identify targets, subsequent prosecution would be "parallel reconstructed" — the simulator-derived lead replaced with an alternative source of the same information.

Public disclosure trajectory:

- **2011**: Arizona State University researcher Daniel Rigmaiden, prosecuted on tax-fraud charges, discovered the government had used a Stingray to locate him. His litigation began the slow public disclosure process.
- **2013-2015**: State and local deployments documented by ACLU and investigative journalists. Harris Corporation confirmed as primary supplier.
- **2014**: DOJ policy change — written guidance requiring warrant for Stingray use in federal investigations (state and local not bound).
- **2018 Carpenter v. United States**: Supreme Court decision restricting warrantless cellular-location tracking. Narrowly targets historical location data; does not address cell-site simulators specifically.

## Why This Event Matters

The 1991 FBI cellular-interception testing establishes the operational pattern that law-enforcement technology surveillance capabilities will be deployed classified and operationalized long before they are subjected to public legal review:

- **Mass-surveillance by design.** Cell-site simulators inherently capture material from non-targeted devices in range. The FBI's 1991 adoption of this technology — with full knowledge of the architecture — demonstrates that mass-surveillance capability was being deployed operationally long before it became politically salient. The post-2013 debate over "bulk" vs "targeted" surveillance was, in the specific case of cellular surveillance, 22 years stale by the time it was being litigated.
- **Agency-led classification against courts and legislators.** The FBI's NDA requirements, its pen-register-order cover, and its policy of dropping prosecutions rather than revealing simulator use represent an agency strategy of maintaining capability by preventing judicial review. Courts were systematically denied information needed to develop relevant doctrine. The 2014-2020 post-disclosure doctrine development occurred in a compressed window after 22+ years of deliberate classification-enabled evasion.
- **Template for post-2001 surveillance-technology deployment.** The 1991 Stingray pattern — classified deployment, NDA-imposed secrecy, parallel-reconstructed prosecutions, eventual public disclosure after years of operation — becomes the template for subsequent surveillance-technology programs. NSA's Stellar Wind deployment 2001-2007 follows the same pattern. FBI facial-recognition deployment 2007-2019 follows the pattern. The 2016-2022 Clearview AI deployments follow the pattern. In each case, operational capability precedes and then drives legal framework development.

## Broader Context

Harris Corporation's role as FBI's primary cellular-interception supplier illustrates the defense-industry / law-enforcement-industry overlap. Harris (merged 2019 with L3 to form L3Harris) is a major defense contractor with substantial classified business. Its cellular-interception product line, developed initially for military SIGINT use, was adapted for domestic law-enforcement use through 1991-2010. The same company supplying foreign-intelligence collection technology to NSA was supplying domestic-surveillance technology to FBI. The dual-use architecture is typical of post-1990s surveillance-industrial-complex operations.

The 2024-2026 cellular-surveillance policy environment remains substantially shaped by 1990s-era framework. Stingrays are in routine use by hundreds of state and local law-enforcement agencies, with varying warrant requirements by jurisdiction. Federal use is subject to DOJ policy requiring warrant in most cases, but exceptions exist. The 2018 Carpenter decision's applicability to live cell-site-simulator use has not been conclusively determined.

## Research Gaps

- [ ] Specific FBI 1991-1995 deployment records — classified
- [ ] Full Harris Corporation cellular-interception product line history — partially documented
- [ ] State and local agency Stingray inventory as of 2026 — ACLU tracks approximately 70 known deployments, many unreported

## Related Entries

- [[1986-10-21--electronic-communications-privacy-act-ecpa]]
- [[1994-10-25--calea-signed-digital-telephony-surveillance-mandate]]
- [[2018-06-22--carpenter-cellular-location-warrant-requirement]]

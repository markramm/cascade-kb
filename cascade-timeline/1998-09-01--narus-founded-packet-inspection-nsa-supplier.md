---
type: timeline_event
id: 1998-09-01--narus-founded-packet-inspection-nsa-supplier
date: '1998-09-01'
title: Narus Founded, Israeli-Origin Deep-Packet-Inspection Firm Becomes NSA Infrastructure Supplier
importance: 7
status: confirmed
actors:
  - Narus Inc.
  - Ori Cohen
  - Stas Khirman
  - National Security Agency
  - AT&T
tags:
  - narus
  - deep-packet-inspection
  - surveillance-infrastructure
  - israeli-intelligence-origin
  - boeing
sources:
  - title: "Narus Inc."
    url: https://en.wikipedia.org/wiki/Narus_(company)
    publisher: Wikipedia
    date: '2024-01-01'
    tier: 3
  - title: "AT&T Whistleblower Mark Klein's Declaration"
    url: https://www.wired.com/2007/05/att-wiretapping/
    publisher: Wired
    date: '2007-05-17'
    tier: 2
  - title: "Spying on the home front — Narus role in NSA Upstream"
    url: https://www.pbs.org/wgbh/pages/frontline/homefront/
    publisher: PBS FRONTLINE
    date: '2007-05-15'
    tier: 2
capture_lanes:
  - Surveillance Infrastructure
  - Digital and Tech Capture
coverage: []
---

## Opening

Narus Inc. is founded in September 1998 by Ori Cohen (former 8200 IDF signals intelligence unit) and Stas Khirman to develop and market deep-packet-inspection (DPI) technology for telecommunications billing and traffic management. By 2001, Narus has pivoted from billing applications to law-enforcement and intelligence-community surveillance. The company's NarusInsight product becomes the dominant commercial DPI platform installed at NSA-tasked splitter rooms at major US carriers 2001-2010, as documented in the 2006 Mark Klein disclosures about AT&T's Folsom Street facility. In 2010 Boeing acquires Narus for an undisclosed amount; in 2015 Boeing sells Narus to Symphony Technology Group. Narus's 1998 founding represents the point at which Israeli-origin signals-intelligence technical expertise becomes commercially available to US intelligence agencies, establishing a pattern that recurs throughout the subsequent surveillance-industrial complex.

## What Happened / Key Facts

Founding and initial business:

- **Founders**: Ori Cohen (CEO, technical lead) and Stas Khirman — both Israeli with prior 8200 Unit service.
- **Incorporation**: Delaware; headquarters Mountain View, California.
- **Initial product**: Semantic Traffic Analyzer, marketed for telecommunications billing and network optimization. The core technology: real-time analysis of packet headers and content at network speeds.
- **Seed investors**: Israeli venture capital (Walden International, JVP); later Series A from Mayfield Fund and others.

Technical capability:

- **Line-rate analysis**: Narus equipment could inspect every packet on a 10-gigabit (later 100-gigabit) network link in real time.
- **Application identification**: Could identify application-layer protocols (email, web, voice, file transfer) from packet structure.
- **Content inspection**: With appropriate configuration, could extract content (email bodies, document attachments, voice conversations).
- **Targeting**: Could flag packets matching specified selectors (email addresses, IP addresses, keywords) for capture while passing others.

Post-2001 NSA adoption:

- **Context**: After 9/11, NSA needed scalable packet-inspection capability to implement the Stellar Wind warrantless program. Narus had operational technology ready.
- **AT&T Folsom Street**: Mark Klein's 2006 disclosure revealed AT&T's 611 Folsom Street facility in San Francisco contained NSA-managed equipment including Narus STA 6400 devices. The facility intercepted internet backbone traffic. Similar NSA-tasked installations at AT&T facilities in other cities.
- **Other carriers**: NarusInsight deployed at NSA-tasked installations at Verizon, Sprint, and other Tier 1 ISPs during the 2001-2007 Stellar Wind period.
- **Post-FISA Amendments Act (2008)**: Narus infrastructure continued to support the Section 702 Upstream collection program, formalizing under statutory authority what had begun under warrantless authority.

Boeing acquisition (2010):

- **Rationale**: Boeing's defense business expanded into cyber and intelligence services. Narus provided packet-inspection technology complementary to Boeing's existing customer base.
- **Price**: Undisclosed. Industry estimates $150-200 million.
- **Post-acquisition**: Narus continued as Boeing subsidiary until 2015.

2015 Boeing sale to Symphony Technology Group:

- **Rationale**: Boeing divested cybersecurity business. Symphony Technology Group, a private-equity firm specializing in mid-market software and services, acquired.
- **Post-2015**: Narus's product line merged into Symphony's "Cyber" portfolio. Company name retired around 2020.

## Why This Event Matters

Narus is the original and most important instance of Israeli-origin signals-intelligence expertise commercialized for US intelligence-agency use:

- **Establishes Israeli-expertise pipeline to US surveillance apparatus.** The 1998 Narus founding, staffed by former 8200 Unit personnel, was the first commercial success of the Israeli-SIGINT-commercialization pipeline that produces Verint Systems, Check Point, NSO Group, Cellebrite, Elbit, and dozens of smaller firms over subsequent decades. US intelligence agencies, lacking direct pipelines for commercial SIGINT technology in the 1990s, adopted Israeli products as a matter of technical convenience. The resulting dependency creates bilateral cooperation ties and foreign-policy constraints.
- **Enables post-9/11 Stellar Wind implementation.** NSA's 2001-2007 warrantless program required operational technology to implement. Narus had the technology ready. If Narus's product had not existed in October 2001, NSA would have needed to develop equivalent capability internally — a multi-year effort that would have significantly constrained Stellar Wind's initial scope. The commercial-off-the-shelf availability of Narus technology meant statutory-authority questions could be decoupled from operational-capacity questions.
- **Deep-packet-inspection infrastructure precedes legal framework.** The technology Narus deployed 2001-2008 was operating under classified authority that could not be publicly reviewed. Only the 2006 Mark Klein disclosure and 2008-2009 Hepting v. AT&T litigation brought its existence to public awareness. The legal framework for DPI surveillance (Section 702) was created in 2008 around infrastructure that had been operating for seven years. This is the recurring pattern: surveillance technology is deployed classified; legal framework is built later around what has already been operationally established.

## Broader Context

Narus's trajectory — Israeli founders, US commercial scaling, NSA customer, Boeing acquisition, private-equity dispersion — illustrates a pattern that recurs with multiple Israeli-origin surveillance technology firms. The pattern's features: (a) founding by former 8200 Unit or Mossad technical personnel; (b) initial commercial framing emphasizing civilian use; (c) actual customer base heavily government / intelligence-community; (d) eventual acquisition by larger US defense or technology firm; (e) technology dispersion into surveillance-industrial-complex ecosystem.

The 2015-2026 equivalent firms — NSO Group (Pegasus mobile spyware), Cellebrite (mobile device forensics), Quadream, Paragon — continue the Narus trajectory. Each combines Israeli SIGINT alumni leadership, commercial civilian framing, intelligence / law-enforcement customer focus, and eventually controversial disclosure of operational scope.

The 2024-2026 debate over foreign involvement in US surveillance infrastructure — CFIUS reviews of Chinese-origin telecommunications, restrictions on Russian-origin cybersecurity products, scrutiny of Israeli-origin commercial spyware — builds on the decades-long Narus-pattern acceptance of Israeli-origin intelligence technology in US government systems. The disparate treatment is politically visible but has not produced uniform policy response.

## Research Gaps

- [ ] Specific Narus contracts with NSA 2001-2008 — classified
- [ ] Full acquisition pricing and terms for Boeing-Narus 2010 transaction — not publicly disclosed
- [ ] Post-2015 Symphony Technology Group operations — largely private

## Related Entries

- [[1994-10-25--calea-signed-digital-telephony-surveillance-mandate]]
- [[1997-10-01--fbi-carnivore-dcs1000-development-begins]]
- [[2001-10-04--nsa-stellar-wind-authorization]]
- [[2003-06-15--nsa-att-surveillance-infrastructure-contract]]

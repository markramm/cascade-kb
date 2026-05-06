---
type: timeline_event
id: 1999-11-20--wassenaar-crypto-export-controls-multilateral-liberalization
date: '1999-11-20'
title: Wassenaar Arrangement Cryptography Provisions Liberalized, US Export Controls Follow
importance: 5
status: confirmed
actors:
  - Wassenaar Arrangement Secretariat
  - Department of Commerce
  - William Daley
  - William Reinsch
  - Electronic Frontier Foundation
tags:
  - wassenaar-arrangement
  - crypto-export
  - export-control
  - surveillance-infrastructure
  - crypto-wars
sources:
  - title: "Wassenaar Arrangement Public Documents"
    url: https://www.wassenaar.org/
    publisher: Wassenaar Arrangement
    date: '2024-01-01'
    tier: 1
  - title: "Export Controls: Change in Export Licensing Jurisdiction for Two Sensitive Dual-Use Items"
    url: https://www.bis.doc.gov/index.php/all-articles/12-policy-guidance/publications/69-federal-register-notice-for-public-comment"
    publisher: U.S. Department of Commerce Bureau of Industry and Security
    date: '2000-01-14'
    tier: 1
  - title: "History of Export Controls on Encryption"
    url: https://www.eff.org/pages/export-control
    publisher: Electronic Frontier Foundation
    date: '2015-01-01'
    tier: 2
capture_lanes:
  - Surveillance Infrastructure
  - Digital & Tech Capture
coverage: []
---

## Opening

The Wassenaar Arrangement — the 33-member multilateral export control regime governing dual-use goods and technologies — adopts revised cryptography provisions at its December 1998 plenary, formally effective 1999. The revised provisions substantially liberalize mass-market cryptographic software exports, recognizing that 56-bit DES and equivalent civilian-level strong encryption is widely available and cannot be effectively controlled. The United States implements the Wassenaar liberalization through Department of Commerce Bureau of Industry and Security (BIS) rules effective January 14, 2000. The Wassenaar and US actions are the multilateral and domestic endpoints of the 1990s Crypto Wars — decades of government effort to restrict civilian access to strong encryption give way to acknowledgment that restriction was commercially unsustainable and substantively ineffective.

## What Happened / Key Facts

Wassenaar cryptography background:

- **Wassenaar Arrangement**: Successor to CoCom (1994), the Cold War-era export control regime. 33 founding members including US, EU members, Russia, Japan, Australia, and others.
- **Dual-Use List Category 5 Part 2**: Specifically governs cryptographic items. Controls both hardware encryption and software.
- **1998-1999 review**: Members' review of cryptographic controls under pressure from commercial sectors. European Commission actively pushed for liberalization, arguing US cryptographic products were being exported through third countries anyway, and the controls disadvantaged European firms.
- **Revised provisions**: Raised thresholds for controls; clarified "mass market" exemptions; reduced license requirements for civilian-level encryption.

US implementation:

- **December 30, 1998 interim rule**: Initial BIS response to Wassenaar adoption.
- **January 14, 2000 final rule**: Published in Federal Register, effective immediately.
- **Key changes**:
  - **Retail/mass market**: Mass-market encryption with keys ≤56 bits (DES) requires only one-time technical review, then freely exportable.
  - **Source code**: Publicly-available cryptographic source code freely exportable (validates the book-publication workaround used in the Zimmermann/PGP case).
  - **Financial applications**: Cryptography specifically for financial applications freely exportable at any key length.
  - **"7 terrorist nations" restrictions remained**: Iran, Iraq, Sudan, Syria, Libya, Cuba, and North Korea remained subject to full controls.
- **2000-2010 further liberalization**: Series of additional BIS rules progressively expanded mass-market exemptions. By 2010, most civilian encryption software was essentially freely exportable subject only to one-time notification requirements.

Industry and civil-society response:

- **Commercial reception**: Generally welcomed. Commercial encryption product market had been operating in regulatory gray zone through the 1990s; the 1999-2000 liberalization legitimized existing commercial practice.
- **EFF and civil-society assessment**: Mixed. Welcomed actual liberalization but noted that controls remained in place for non-mass-market products and that US continued to use export controls as a counter-proliferation tool.
- **RSA and Silicon Valley**: Viewed the liberalization as too little too late — the prior ten years of restrictions had advantaged European and Israeli firms that could sell strong encryption to global markets.

Clinton administration framing:

- **Commerce Secretary William Daley**: Announced the January 2000 rule as balancing national security and commercial interests. The framing implicitly conceded that the prior regime had been insufficiently commercial.
- **BIS Under Secretary William Reinsch**: Public statements emphasized that US firms would benefit from ability to compete in global market for strong-encryption products.
- **Law enforcement and intelligence coordination**: Internally, BIS rule was developed with FBI, DOJ, NSA, and State Department input. Published rule was more liberal than initial FBI and DOJ preferences, reflecting administration judgment that commercial competitiveness required liberalization.

## Why This Event Matters

The Wassenaar crypto liberalization is the multilateral endpoint of the 1990s Crypto Wars and the starting point for the subsequent decades of encryption policy:

- **Acknowledges civilian strong encryption is commercial reality.** The 1999-2000 liberalization formally recognized what the 1996 Zimmermann declination and commercial availability of PGP had already established: strong civilian encryption existed, was widely used, and could not be contained through export controls. Subsequent US encryption policy could no longer begin from premise that civilian strong encryption was a controllable resource.
- **Sets up 2001-2026 "going dark" debate.** Having lost the 1990s fight to prevent civilian strong encryption, US law enforcement shifted to arguing that specific instantiations — encrypted messaging apps, encrypted-by-default operating systems, encrypted cloud services — created unique investigative problems requiring specific mandates. Every subsequent debate (2001 PATRIOT, 2014-2016 Apple vs. FBI San Bernardino, 2019-2020 Barr, 2024-2026 client-side scanning) operates in the post-Wassenaar environment where strong civilian encryption is an uncontested baseline.
- **Establishes international coordination framework for later surveillance-technology disputes.** The Wassenaar Arrangement's later additions — 2013 "intrusion software" provisions, 2019 software-surveillance-tools provisions — used the same multilateral framework the 1999 cryptography liberalization had established. The 2019 Wassenaar amendments targeting NSO Group-class software are direct continuations of the Wassenaar framework the 1999 cryptography decisions shaped.

## Broader Context

The Wassenaar cryptography liberalization occurred in the specific commercial environment of 1999-2000: the dot-com peak, substantial venture-capital investment in internet companies, and competitive pressure on US firms from European and Israeli encryption-technology competitors. The commercial-interest case for liberalization had become overwhelming — Silicon Valley firms argued they could not compete globally with products subject to US-specific export controls. The administration's judgment that commercial competitiveness outweighed marginal intelligence-collection-access concerns reflected this balance.

The 2013-2019 Wassenaar expansion into intrusion-software controls reflects subsequent reversal of direction: the 1990s liberalization recognized that controls on civilian crypto were impractical, but the 2010s additions attempted to control commercial offensive-security products (zero-day exploits, commercial spyware). The latter controls have been similarly difficult to enforce — NSO Group and similar firms have largely continued operations despite formal export restrictions in their home and target jurisdictions.

## Research Gaps

- [ ] Specific US interagency deliberations on January 2000 BIS rule — partial FOIA releases
- [ ] Empirical measurement of US vs European/Israeli market-share changes post-liberalization

## Related Entries

- [[1993-02-01--zimmermann-pgp-criminal-investigation-crypto-wars]]
- [[1993-04-16--clipper-chip-announced-nsa-key-escrow-backdoor]]
- [[1996-01-11--zimmermann-pgp-investigation-dropped-crypto-wars-inflection]]

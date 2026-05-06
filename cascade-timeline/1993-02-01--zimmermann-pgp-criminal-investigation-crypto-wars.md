---
type: timeline_event
id: 1993-02-01--zimmermann-pgp-criminal-investigation-crypto-wars
date: '1993-02-01'
title: US Customs Opens Criminal Investigation of Phil Zimmermann Over PGP Encryption Export
importance: 7
status: confirmed
actors:
  - Phil Zimmermann
  - U.S. Customs Service
  - RSA Security
  - Department of Justice
  - Electronic Frontier Foundation
tags:
  - pgp
  - zimmermann
  - crypto-wars
  - munitions-export
  - surveillance-infrastructure
  - encryption
sources:
  - title: "Phil Zimmermann's statement on dropped investigation"
    url: https://philzimmermann.com/EN/news/PRZ_case_dropped.html
    publisher: Phil Zimmermann
    date: '1996-01-11'
    tier: 1
  - title: "Pretty Good Privacy"
    url: https://en.wikipedia.org/wiki/Pretty_Good_Privacy
    publisher: Wikipedia
    date: '2024-01-01'
    tier: 3
  - title: "When Encryption Was a Crime: The 1990s Battle for Free Speech in Software"
    url: https://reason.com/video/2020/10/21/cryptowars-gilmore-zimmermann-cryptography/
    publisher: Reason
    date: '2020-10-21'
    tier: 2
capture_lanes:
  - Surveillance Infrastructure
  - Digital & Tech Capture
coverage: []
---

## Opening

The U.S. Customs Service opens a criminal investigation of Pretty Good Privacy (PGP) creator Phil Zimmermann in February 1993 for alleged violations of the Arms Export Control Act and International Traffic in Arms Regulations (ITAR). The investigation follows Zimmermann's 1991 free release of PGP and its rapid international spread via USENET and public FTP sites. The government's theory: strong encryption software (key length >40 bits) is a "munition" under ITAR, and unlicensed export is a federal crime carrying up to 10 years imprisonment. The investigation runs for three years without charges and is dropped without indictment in January 1996. Zimmermann's case becomes the public face of the "Crypto Wars" — the 1990s policy conflict over whether the government can prevent the spread of strong encryption to civilians.

## What Happened / Key Facts

Background leading to investigation:

- **June 1991**: Zimmermann releases PGP 1.0, a public-key email encryption program, as free software. Distribution via BBS networks and USENET archives makes it internationally available within weeks.
- **Motivation**: Zimmermann created PGP in response to the 1991 Senate Bill 266 (Biden-Thurmond), which had proposed to require encryption backdoors for law enforcement access. The bill died, but Zimmermann had already built PGP as insurance.
- **RSA dispute**: PGP used the RSA public-key algorithm, then under patent by RSA Data Security. Jim Bidzos (RSA CEO) accused Zimmermann of patent infringement and reportedly contacted federal authorities.

The investigation:

- **February 1993**: Customs Service San Jose office opens criminal case. Investigators include agents specialized in export controls.
- **Legal theory**: PGP source code, distributed internationally, constitutes export of a "cryptographic item" (Category XIII of the USML) without State Department license. Each download by a non-US person potentially counts as a separate violation.
- **Investigation scope**: Federal grand jury seated; subpoenas issued for internet service providers, FTP site operators, and individuals who had posted PGP code.
- **Zimmermann's legal situation**: Faced potential federal charges carrying 10+ year sentences. Retained attorney Phil Dubois. Legal defense fund organized by EFF and CPSR.

The First Amendment workaround:

- **1995 publication**: MIT Press publishes PGP: Source Code and Internals — the complete PGP source code in book form. Rationale: State Department regulations distinguish between digital export (restricted) and printed book export (not restricted under ITAR).
- **International re-keying**: Volunteers overseas scan the MIT Press book, OCR the text, and reconstitute PGP outside US export control. The demonstration undermines the government's case by showing that export control cannot realistically prevent spread.

Investigation closure:

- **January 11, 1996**: US Attorney's office in Northern California declines prosecution. No charges filed. No public statement of reasoning.
- **PGP Inc. founded (1996)**: Zimmermann commercializes PGP. Company later acquired by Network Associates, then by Symantec.

Regulatory consequence:

- **1996 White House Executive Order 13026**: Transfers cryptographic export control from State Department (ITAR) to Commerce Department (Export Administration Regulations). Signals policy shift away from criminalization.
- **2000**: Commerce Department dramatically liberalizes crypto export controls. Strong encryption (including PGP-derived) becomes freely exportable with limited restrictions.
- **Wassenaar Arrangement**: International coordination of dual-use export controls maintained some framework, but criminalization of civilian-level encryption effectively ends.

## Why This Event Matters

The Zimmermann investigation is the defining moment of the 1990s Crypto Wars and the doctrinal precedent against criminalizing civilian encryption:

- **Three-year chill on encryption developers.** The investigation's practical effect was to deter US-based encryption research and commercial development through 1993-1996. Developers who could afford to do so worked abroad or delayed products. The US lost substantial encryption-product market position to European and Israeli firms during this window.
- **Establishes that cryptographic export control is unenforceable.** The MIT Press book-scanning workaround demonstrated that software controls cannot be maintained in a world of cheap international communication. The demonstration's persuasiveness is why the 1996-2000 regulatory liberalization occurred.
- **Sets up the "going dark" rhetoric FBI would use for three decades.** Having lost the 1990s fight to prevent civilian strong encryption, law enforcement shifted to arguing that encryption creates "going dark" — places where lawful investigation cannot reach. The same argument recurs with Louis Freeh (1997), Jim Comey (2014-2016), William Barr (2019-2020), and Christopher Wray (2017-2025). The Zimmermann case is why that argument is made from a position of having lost the initial legal fight over criminalization.

The Zimmermann case is also the proof-of-concept for civil-society resistance to surveillance-state policy. EFF (founded 1990) organized legal defense and public advocacy that proved effective against a federal criminal investigation. The template — technical expertise, First Amendment framing, international coalition — became the standard civil-society response to surveillance legislation through the Snowden era.

## Broader Context

Zimmermann's specific intervention — releasing PGP in response to anticipated law-enforcement-access legislation — is an early example of what would later be called "regulatory insurance" by the privacy-tech community. Develop and deploy technology before regulation can prevent it, then argue that the resulting installed base changes the regulatory calculus. This pattern recurs with Signal (end-to-end encrypted messaging, 2014-present), Tor (onion routing, 2006-present anonymous publication), and a range of decentralized technologies.

The 2021-present debates over E2E-encryption legislation in the UK (Online Safety Act), EU (CSAM scanning regulation proposals), and US (EARN IT Act recurrences) explicitly reference the 1990s Crypto Wars as precedent. The 1996 dismissal of the Zimmermann case without indictment is the civil-society side's strongest precedent that strong encryption cannot be successfully criminalized; law enforcement's response is that the post-2001 security environment justifies revisiting the 1996 policy conclusion.

## Research Gaps

- [ ] Full government prosecution-declination memorandum for the Zimmermann case — not public
- [ ] Specific RSA Data Security role in triggering investigation — conflicting accounts

## Related Entries

- [[1992-03-01--fbi-digital-telephony-initiative-wiretap-mandate-push]]
- [[1993-04-16--clipper-chip-announced-nsa-key-escrow-backdoor]]
- [[1996-01-11--zimmermann-pgp-investigation-dropped-crypto-wars-inflection]]

---
type: timeline_event
id: 1996-01-11--zimmermann-pgp-investigation-dropped-crypto-wars-inflection
date: '1996-01-11'
title: DOJ Drops Zimmermann PGP Investigation, Marks Crypto Wars Policy Inflection
importance: 7
status: confirmed
actors:
  - Phil Zimmermann
  - Department of Justice
  - U.S. Customs Service
  - Michael Yamaguchi
  - Electronic Frontier Foundation
tags:
  - pgp
  - zimmermann
  - crypto-wars
  - munitions-export
  - surveillance-infrastructure
  - encryption
sources:
  - title: "Phil Zimmermann statement on investigation dismissal"
    url: https://philzimmermann.com/EN/news/PRZ_case_dropped.html
    publisher: Phil Zimmermann
    date: '1996-01-11'
    tier: 1
  - title: "Phil Zimmermann"
    url: https://en.wikipedia.org/wiki/Phil_Zimmermann
    publisher: Wikipedia
    date: '2024-01-01'
    tier: 3
capture_lanes:
  - Surveillance Infrastructure
  - Digital and Tech Capture
coverage: []
---

## Opening

The U.S. Attorney for the Northern District of California, Michael Yamaguchi, notifies Phil Zimmermann on January 11, 1996 that the three-year grand jury investigation into PGP's international distribution is closed without indictment. No charges will be filed against Zimmermann under the Arms Export Control Act. The government provides no public explanation for the closure. The dismissal, coming three months after Clipper Chip's effective demise and seven months before the Clinton administration's first major retreat on crypto export controls (Executive Order 13026, November 15, 1996), represents the end of the prohibitionist phase of the 1990s Crypto Wars. US policy shifts thereafter from attempting to criminalize strong civilian encryption to attempting to mandate access architectures within a world where civilian strong encryption exists.

## What Happened / Key Facts

Closure specifics:

- **Date**: January 11, 1996 — notification letter from US Attorney's Office, Northern District of California.
- **Form**: Declination letter to Zimmermann's attorney Phil Dubois.
- **Explanation**: None. DOJ standard practice in declination cases is to provide no reasoning.
- **Scope**: The declination covered Zimmermann personally. The investigation had at various points considered charges against others involved in PGP distribution (Perry Metzger, Jim Bruce, various FTP site operators); none were prosecuted.

Factors contributing to closure (not officially stated):

- **MIT Press book publication** (1995): PGP source code published as a book, then re-scanned and re-distributed internationally, demonstrated that source code export could not be prevented and that First Amendment coverage of source-code-as-speech was a plausible defense at trial.
- **Bernstein v. United States (1995-1999)**: Parallel litigation by Daniel Bernstein (a UC Berkeley graduate student) challenging ITAR cryptographic controls as prior restraint. August 1995 District Court ruling treated source code as speech for First Amendment purposes. The precedent, though not yet appellate, made prosecution riskier.
- **Political climate shift**: By 1995-1996 strong encryption was widely used commercially. Successful prosecution of Zimmermann would have established that every vendor of strong encryption had committed felonies.
- **Case weakness**: Zimmermann had not himself uploaded PGP to overseas sites — he had released it in the US with no export-control violation. The theory that later overseas distribution by third parties created his export liability was legally fragile.

Subsequent policy events (1996):

- **July 1996**: National Research Council publishes "Cryptography's Role in Securing the Information Society" (CRISIS report) — recommends relaxation of export controls.
- **November 15, 1996**: Executive Order 13026 transfers cryptographic export control from State Department (ITAR) to Commerce Department (Export Administration Regulations). The administrative move signals that the government accepts cryptography as a commercial export rather than a military one.
- **1997-2000**: Commerce Department progressively relaxes key-length restrictions. By 2000, mass-market encryption products are largely freely exportable.

Zimmermann's post-investigation trajectory:

- **March 1996**: Founds PGP Inc. to commercialize PGP. First business focus on enterprise email encryption.
- **1997**: Network Associates acquires PGP Inc.
- **1999**: Network Associates closes PGP product line. Zimmermann leaves.
- **2001**: PGP Corporation reacquires the product line.
- **2010**: Symantec acquires PGP Corporation. Modern GnuPG (GPG) open-source implementation is the dominant current descendant of PGP.

## Why This Event Matters

The 1996 declination is the single clearest policy marker of the end of the US government's attempt to criminalize civilian strong encryption:

- **Prohibition approach decisively fails.** The government's 1993-1996 attempt to use criminal export enforcement to suppress civilian strong encryption ran for three years, cost millions in investigative resources, produced no indictments, no convictions, no injunctions, and no empirical reduction in the spread of PGP. The outcome fundamentally shapes subsequent US crypto policy: administrations that would have preferred to prohibit strong civilian encryption (1997-2001 Freeh-led FBI, 2014-2016 Comey-era FBI, 2019-2020 Barr-led DOJ) must operate within a framework where strong encryption exists and is lawful.
- **Signals to industry that strong encryption can be commercialized.** The 1996 declination is what the pre-PGP-Inc. phase of Zimmermann's company needed. With federal prosecution threat removed, venture financing, corporate partnerships, and enterprise customers could engage. The subsequent commercial encryption product ecosystem — RSA Data Security, Network Associates, Verisign, Entrust, eventually OpenSSL and the post-2005 open-source infrastructure — built on the 1996 permission-to-operate.
- **Establishes that academic and journalistic speech about cryptography is protected.** The combination of the 1996 Zimmermann declination and the 1999 Ninth Circuit ruling in Bernstein that source code is speech for First Amendment purposes, yields a legal regime in which cryptographic publication is protected. This is why the 2015 "Keys Under Doormats" paper, the 2016 "Going Dark" cryptographer responses, and every subsequent academic policy intervention could proceed without legal risk.

## Broader Context

The 1996 closure is the policy inflection, but it did not end the government's desire for access to encrypted communications. It redirected the effort from prohibition to mandate-within-legality: CALEA's 1994 wiretap-ready infrastructure ([[1994-10-25--calea-signed-digital-telephony-surveillance-mandate]]); 1996-1997 key-recovery proposals; 2001 PATRIOT Act expansion of service-provider subpoena authorities; 2008 FISA Amendments Section 702 compelled-production authority; 2024 Client-Side Scanning proposals. Each is an attempt to achieve through architecture what prohibition could not achieve through prosecution.

The Zimmermann case's specific legacy for 2026 surveillance debates: when law enforcement argues that Signal, WhatsApp, or iMessage create "warrant-proof" communications, the civil-society response points to the 1996 Zimmermann declination as evidence that the alternative — criminalizing the providers — has already been tried and rejected. The 1990s Crypto Wars are the baseline against which all subsequent proposals are measured.

## Research Gaps

- [ ] Internal DOJ declination memorandum for the Zimmermann case — not publicly released
- [ ] Specific 1995-1996 communications between ARPA, NSA, and Justice Department on crypto policy — partial record only

## Related Entries

- [[1993-02-01--zimmermann-pgp-criminal-investigation-crypto-wars]]
- [[1993-04-16--clipper-chip-announced-nsa-key-escrow-backdoor]]
- [[1994-06-02--blaze-clipper-flaw-demonstrates-escrow-failure]]
- [[1994-10-25--calea-signed-digital-telephony-surveillance-mandate]]

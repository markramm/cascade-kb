---
type: timeline_event
id: 1993-04-16--clipper-chip-announced-nsa-key-escrow-backdoor
date: '1993-04-16'
title: Clinton White House Announces Clipper Chip, NSA-Designed Backdoor Encryption with Government Key Escrow
importance: 8
status: confirmed
actors:
  - Bill Clinton
  - Al Gore
  - National Security Agency
  - National Institute of Standards and Technology
  - Matt Blaze
  - AT&T
tags:
  - clipper-chip
  - key-escrow
  - skipjack
  - crypto-wars
  - surveillance-infrastructure
  - encryption-backdoor
sources:
  - title: "White House Fact Sheet: Public Encryption Management"
    url: https://archive.epic.org/crypto/clipper/
    publisher: Electronic Privacy Information Center
    date: '1993-04-16'
    tier: 1
  - title: "On the Clipper Chip's Birthday: Looking Back on Decades of Key Escrow Failures"
    url: https://www.eff.org/deeplinks/2015/04/clipper-chips-birthday-looking-back-22-years-key-escrow-failures
    publisher: Electronic Frontier Foundation
    date: '2015-04-16'
    tier: 2
  - title: "Protocol Failure in the Escrowed Encryption Standard"
    author: Matt Blaze
    url: https://www.mattblaze.org/papers/eesproto.pdf
    publisher: AT&T Bell Labs
    date: '1994-06-01'
    tier: 1
capture_lanes:
  - Surveillance Infrastructure
  - Digital and Tech Capture
coverage: []
---

## Opening

The Clinton White House announces the "Clipper Chip" initiative on April 16, 1993, three months into Clinton's first term. Clipper is a hardware encryption chip — formally the Escrowed Encryption Standard — that uses the NSA-designed Skipjack algorithm and incorporates mandatory key escrow: every chip's encryption key is split into halves, each held by a separate federal agency escrow, retrievable under court order for law enforcement decryption. The administration's position: commercial communications can use strong NSA-grade encryption as long as the government retains mandated access. The initiative immediately faces opposition from a cross-ideological coalition of cryptographers, civil libertarians, industry groups, and privacy advocates. Clipper is effectively dead by 1996 — AT&T's flagship Clipper-based secure phone fails commercially, and AT&T Bell Labs cryptographer Matt Blaze publishes a technical flaw that allows bypass of the escrow system.

## What Happened / Key Facts

Clipper technical design:

- **Skipjack algorithm**: 64-bit block cipher with 80-bit key, designed by NSA. Algorithm classified at launch — users could not examine the cryptographic primitive. Partially declassified in 1998.
- **Law Enforcement Access Field (LEAF)**: Each encrypted transmission includes an LEAF that contains the session key encrypted under the chip's unique key. Government with access to the chip's escrowed unique key can extract the session key and decrypt the communication.
- **Dual escrow**: The 80-bit chip unique key is split — half held by NIST, half held by Treasury. Law enforcement with court order retrieves both halves and reconstructs the key.
- **Hardware implementation**: Skipjack was intended to be implemented only in tamper-resistant hardware chips. Software implementation was technically feasible but not authorized under Clipper licensing.

Policy announcement content:

- **Voluntary for commercial use**: Government claimed Clipper was voluntary — commercial users could choose other encryption. But the government would buy only Clipper-compliant products for federal use, which was intended to create de facto market dominance.
- **Federal purchasing mandate**: All federal agencies required to use Clipper for unclassified sensitive communications.
- **No export control liberalization for non-Clipper strong encryption**: The policy explicitly maintained ITAR restrictions on strong encryption without key escrow.

Opposition response:

- **Cryptographer letter** (1993-1994): Over 100 prominent academic cryptographers including Whit Diffie, Ron Rivest, and Martin Hellman sign public letters opposing Clipper on technical and policy grounds.
- **Industry coalition**: Microsoft, IBM, Apple, Lotus, Sun Microsystems, AT&T all oppose Clipper either publicly or via industry associations. Industry concern: US products built around Clipper would not be exportable to non-US buyers who did not want US government key escrow.
- **Privacy advocates**: EFF, EPIC, CPSR mount sustained opposition campaigns.
- **Library and education coalitions**: AALL, ALA, Educause oppose on user-privacy grounds.

Blaze's 1994 vulnerability disclosure:

- **Matt Blaze (AT&T Bell Labs)**: Publishes "Protocol Failure in the Escrowed Encryption Standard" in June 1994.
- **Attack**: Blaze shows that a malicious user can construct an invalid LEAF that still passes Clipper's validity check but cannot be decrypted by the escrow system. Communications would be encrypted normally between Clipper users but the escrow mechanism would not function.
- **Effect**: Demonstrates that the escrow system's law-enforcement-access guarantee is unreliable even in its own terms. Combined with market rejection, Blaze's paper is the final blow to Clipper viability.

Commercial outcome:

- **AT&T Surity 3600 secure phone**: Flagship Clipper-based product. Priced at $1,100 per phone. Sales negligible through 1993-1996.
- **Program wind-down 1996**: Clinton White House quietly stops promoting Clipper. Formally discontinued by policy drift rather than announced termination.

## Why This Event Matters

Clipper is the most aggressive government encryption-backdoor proposal ever made in US policy and its failure defines the subsequent quarter century of cryptographic policy:

- **Establishes that government cannot dictate cryptographic architecture through market mechanisms.** The federal purchasing mandate was intended to create de facto dominance. Industry refusal to adopt Clipper — on commercial and principled grounds — meant the market did not follow government lead. The failure shaped subsequent crypto policy: every proposal since 1996 (Carnivore, 2001 PATRIOT, 2014-2016 Comey "going dark," 2019-2020 Barr demand, 2025-2026 device-scanning debates) has had to reckon with Clipper's lesson that market mandate does not produce adoption.
- **Academic cryptography emerges as independent political force.** The Clipper fight politicized academic cryptography and established it as a policy constituency. Matt Blaze, Ron Rivest, Whit Diffie, and Bruce Schneier became public figures whose technical judgments had policy weight. The pattern — academic technical review of government surveillance proposals — becomes the standard mode of external expert pressure on subsequent initiatives.
- **Demonstrates that mandatory-backdoor architecture is technically fragile.** Blaze's 1994 finding was the first public demonstration that key-escrow systems are harder to engineer securely than to break. The 2024 Salt Typhoon compromise of CALEA-mandated interception ([[1994-10-25--calea-signed-digital-telephony-surveillance-mandate]]) is the latest, largest-scale confirmation of the same principle.

## Broader Context

The Clipper proposal did not emerge from nothing. It reflected NSA and FBI concern through the late 1980s that advancing commercial encryption would foreclose traditional SIGINT access and lawful intercept. The internal government debate 1991-1993 was between pure-prohibition approach (criminalize strong civilian encryption — the Zimmermann investigation approach) and mediated-access approach (allow strong encryption but require key escrow — the Clipper approach). Clipper was the moderate position. Its failure pushed subsequent policy toward accepting that the 1990s prohibition framework had lost.

The 2015-2016 "Going Dark" debate, 2019-2020 Barr "responsible encryption" campaign, 2024-2026 device-side CSAM scanning proposals all repeat the Clipper policy logic in different technical forms. None has achieved the market dominance Clipper was originally designed to obtain.

## Research Gaps

- [ ] Full NSA internal debate over Skipjack algorithm choice and key length — partially declassified
- [ ] Specific commercial-sector communications between Clipper-era firms (AT&T, Lotus, Microsoft) — limited record

## Related Entries

- [[1992-03-01--fbi-digital-telephony-initiative-wiretap-mandate-push]]
- [[1993-02-01--zimmermann-pgp-criminal-investigation-crypto-wars]]
- [[1994-10-25--calea-signed-digital-telephony-surveillance-mandate]]

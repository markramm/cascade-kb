---
type: timeline_event
id: 1976-06-23--united-states-v-miller-bank-records-third-party-doctrine
date: '1976-06-23'
title: Supreme Court Miller Decision Holds Bank Records Have No Fourth Amendment Protection, Creates Third-Party Doctrine
importance: 9
status: confirmed
actors:
  - Lewis Powell
  - William Rehnquist
  - Thurgood Marshall
  - William Brennan
  - Mitch Miller
tags:
  - third-party-doctrine
  - fourth-amendment
  - bank-records
  - surveillance-infrastructure
  - supreme-court
sources:
  - title: "United States v. Miller, 425 U.S. 435 (1976)"
    url: https://supreme.justia.com/cases/federal/us/425/435/
    publisher: U.S. Supreme Court
    date: '1976-04-21'
    tier: 1
  - title: "Smith v. Maryland, 442 U.S. 735 (1979)"
    url: https://supreme.justia.com/cases/federal/us/442/735/
    publisher: U.S. Supreme Court
    date: '1979-06-20'
    tier: 1
  - title: "Carpenter v. United States, 138 S. Ct. 2206 (2018)"
    url: https://supreme.justia.com/cases/federal/us/585/16-402/
    publisher: U.S. Supreme Court
    date: '2018-06-22'
    tier: 1
capture_lanes:
  - Surveillance Infrastructure
  - Financialization
coverage: []
---

## Opening

The U.S. Supreme Court rules 7-2 in United States v. Miller on April 21, 1976 (decision issued; effective date June 23, 1976 after rehearing denial) that a bank customer has no Fourth Amendment expectation of privacy in records the bank maintains about the customer's transactions. Justice Lewis Powell's majority opinion holds that a customer who voluntarily conveys information to a bank "assumes the risk" that the bank will disclose the information to government. The decision establishes what becomes known as the "third-party doctrine" — the principle that information shared with any third party loses Fourth Amendment protection regardless of the circumstances under which it was shared. Combined with the 1979 Smith v. Maryland ruling extending the doctrine to phone records, Miller becomes the constitutional foundation for mass surveillance of communications metadata, financial transactions, and eventually essentially all internet-era third-party-intermediated information. The 2018 Carpenter v. United States decision partially retreats from Miller but leaves the core doctrine intact.

## What Happened / Key Facts

Case background:

- **Defendant**: Mitch Miller, charged with tax evasion and possession of unregistered whiskey still.
- **Subpoena**: ATF issued subpoena to two banks for Miller's records. Banks complied without notifying Miller.
- **Trial court**: Admitted the bank records into evidence over Miller's objection.
- **Fifth Circuit**: Reversed. Held Miller had a Fourth Amendment interest in his bank records; ATF should have obtained a warrant.
- **Supreme Court**: Reversed Fifth Circuit. Bank records admissible. Conviction affirmed.

Powell's majority opinion:

- **Core holding**: "The depositor takes the risk, in revealing his affairs to another, that the information will be conveyed by that person to the Government."
- **No expectation of privacy**: Records are "the business records of the bank," not records "of the depositor's own transactions." Bank is the party with a possessory interest.
- **No reasonable expectation of privacy**: Miller had "voluntarily" given the information to the bank; therefore he retained no reasonable expectation of privacy in how the bank might later use it.
- **Third parties not as agents**: The decision treats the bank as a fully independent party, not as an agent of the customer.

Dissenting opinions:

- **Brennan dissent** (joined by Marshall): Voluntariness fiction — customers have no practical choice about whether to use banks. Characterizing bank records as "voluntarily conveyed" ignores the economic reality.
- **Marshall dissent**: Bank records reveal highly sensitive information (political contributions, religious giving, associations). Treating them as unprotected by Fourth Amendment effectively exposes constitutionally-sensitive information to government without warrant.

Smith v. Maryland (1979) extension:

- **Facts**: Police installed pen register on defendant's phone line; recorded outgoing numbers dialed.
- **Holding (5-3)**: No Fourth Amendment protection. Phone numbers are "voluntarily conveyed" to phone company for routing; no reasonable expectation of privacy.
- **Effect**: Extends Miller's third-party doctrine from financial records to communications metadata.

Carpenter v. United States (2018) partial retreat:

- **Facts**: FBI obtained 127 days of cell-site location data for a robbery suspect without a warrant.
- **Holding (5-4)**: Fourth Amendment requires warrant for extended cell-site location data even though data is held by third-party carrier.
- **Limitations**: Court explicitly declined to overrule Miller or Smith. Ruling is narrow — applies only to extended location history, not to short-term or to other third-party data.
- **Effect**: Signals the third-party doctrine has limits but leaves most of Miller intact.

## Why This Event Matters

Miller establishes the constitutional framework that enables every major US mass-surveillance program 1976-2026:

- **Constitutional foundation for ECPA's lower protection tier.** The 1986 Electronic Communications Privacy Act ([[1986-10-21--electronic-communications-privacy-act-ecpa]]) assigns lower statutory protection to communications held by service providers specifically because Miller had held such material has no constitutional protection. ECPA's 180-day rule, the Stored Communications Act's subpoena standard, the Pen Register Act's relevance standard — all track Miller's doctrinal framework.
- **Constitutional foundation for bulk metadata collection.** NSA's 2001-2015 bulk phone-metadata collection under Section 215 was defended explicitly on Miller / Smith grounds. The argument: if a single call record has no Fourth Amendment protection, then billions of call records have no Fourth Amendment protection. Judge Reggie Walton's 2013 opinion upholding the program relied substantially on Smith. Judge Richard Leon's 2013 opinion finding the program unconstitutional had to distinguish Smith — he did so by emphasizing scale, but his reasoning did not prevail in subsequent circuits.
- **Constitutional foundation for FinCEN / data-broker architecture.** The 1990 FinCEN creation ([[1990-04-25--fincen-founded-treasury-financial-surveillance]]), the expansion of SAR filings, the Treasury-bank compelled-cooperation framework all rest on Miller. The 1970s-present commercial data-broker industry (Acxiom, Experian, ChoicePoint, LexisNexis, Thomson Reuters) operates in a space Miller opened — government acquires from brokers what it could not constitutionally acquire through primary surveillance.

## Broader Context

Miller is, in constitutional-law scholarship, widely regarded as the single most consequential Fourth Amendment decision of the post-Warren Court era. The third-party doctrine's scope has dramatically expanded with technology: information now "voluntarily conveyed" includes every email, every web request, every app interaction, every smart-device telemetry reading, every automotive sensor output. Under a strict reading of Miller, essentially nothing a person does with a digital device is constitutionally private.

Congress's 1978 Right to Financial Privacy Act responded to Miller's specific financial-records holding by imposing statutory (not constitutional) requirements on government access to bank records. But the constitutional holding remained intact, and statutory protections could be (and were) modified by later legislation. The 2001 PATRIOT Act weakened the RFPA. The 2020 Fourth Circuit ruling in U.S. v. Lewis reaffirmed Miller. The 2024 debates over commercial data-broker purchases by government operate entirely within the Miller / Smith doctrinal space.

Carpenter's 2018 narrow retreat from Miller was unexpected and remains contested. Lower-court applications of Carpenter have been inconsistent. The 2024-2026 legal debate over whether similar constitutional protection extends to other third-party-held data (bank transactions, cloud files, smart-device telemetry) is ongoing.

## Research Gaps

- [ ] Detailed empirical analysis of how Miller has been cited in subsequent surveillance litigation — no comprehensive academic treatment
- [ ] Carpenter's specific lower-court application across circuits — diverging

## Related Entries

- [[1972-06-19--keith-case-fourth-amendment-domestic-surveillance-warrant]]
- [[1978-10-25--foreign-intelligence-surveillance-act-signed]]
- [[1986-10-21--electronic-communications-privacy-act-ecpa]]
- [[1990-04-25--fincen-founded-treasury-financial-surveillance]]

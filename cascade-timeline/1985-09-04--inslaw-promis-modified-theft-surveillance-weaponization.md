---
type: timeline_event
id: 1985-09-04--inslaw-promis-modified-theft-surveillance-weaponization
date: '1985-09-04'
title: Inslaw Files Bankruptcy Accusing DOJ of Stealing PROMIS Software for Intelligence Use
importance: 7
status: confirmed
actors:
  - William Hamilton
  - Inslaw Inc.
  - Department of Justice
  - Edwin Meese
  - C. Madison Brewer
  - Earl Brian
tags:
  - inslaw
  - promis
  - doj-corruption
  - surveillance-infrastructure
  - intelligence-weaponization
sources:
  - title: "Inslaw v. United States, 113 B.R. 802 (D.D.C. 1989)"
    url: https://law.justia.com/cases/federal/district-courts/BR/113/802/1990305/
    publisher: U.S. Bankruptcy Court
    date: '1989-09-28'
    tier: 1
  - title: "The Inslaw Affair — House Judiciary Committee Investigative Report"
    url: https://www.govinfo.gov/content/pkg/GPO-CRPT-102hrpt857/pdf/GPO-CRPT-102hrpt857.pdf
    publisher: U.S. House Committee on the Judiciary
    date: '1992-09-10'
    tier: 1
  - title: "Inslaw — Wikipedia"
    url: https://en.wikipedia.org/wiki/Inslaw
    publisher: Wikipedia
    date: '2024-01-01'
    tier: 3
  - title: "Justice Department records confirm PROMIS scandal's ties to Israel"
    url: https://www.muckrock.com/news/archives/2017/oct/12/promis-israel/
    publisher: MuckRock
    date: '2017-10-12'
    tier: 2
capture_lanes:
  - Surveillance Infrastructure
  - Intelligence Penetration
coverage: []
---

## Opening

William Hamilton's Inslaw Inc. files for Chapter 11 bankruptcy on June 9, 1985, and on September 4, 1985 files a complaint against the U.S. Department of Justice alleging that DOJ stole Inslaw's Enhanced PROMIS (Prosecutor's Management Information System) software, modified it to include a backdoor for intelligence-gathering purposes, and distributed the modified software to foreign intelligence services. The allegations, initially dismissed as paranoid bankruptcy-claim theater, are substantially vindicated by a 1988 bankruptcy court ruling that DOJ had acted in bad faith and a 1992 House Judiciary Committee investigation concluding that DOJ "took, converted, stole" the software "by trickery, fraud and deceit." The case becomes one of the most documented instances of a US government agency misappropriating private-sector software to weaponize it for intelligence purposes — a foundational case study for the PROMIS-to-Palantir institutional lineage.

## What Happened / Key Facts

Inslaw background:

- **Founded 1974** by William Hamilton as the Institute for Law and Social Research. Originally a nonprofit developing case management software for law enforcement.
- **1981 conversion**: Became for-profit Inslaw Inc.
- **PROMIS software**: Developed over the 1970s with federal funding (originally as LEAA grant-funded work). Case-management system for prosecutors — track cases, defendants, evidence, court calendars.
- **Enhanced PROMIS**: Privately-financed modifications by Inslaw to port PROMIS to new hardware (VAX/VMS) and add database capabilities. Inslaw claimed IP rights in these enhancements.

The DOJ contract and dispute:

- **March 1982**: Inslaw awarded $10 million contract by Executive Office of United States Attorneys (EOUSA) to install PROMIS at 94 US Attorney offices.
- **C. Madison Brewer appointed contract manager**: Brewer had previously worked at Inslaw, had been forced out under acrimonious circumstances, and harbored personal grievance against Hamilton.
- **April 1982 — one month later**: Brewer recommends contract termination for "convenience of the Government" despite Inslaw performing satisfactorily.
- **Modification 12 (1983)**: Inslaw agrees to provide Enhanced PROMIS in exchange for $1 million payment. Hamilton later testifies this was negotiated under duress — contracting officer Peter Videnieks implicitly threatened termination if Inslaw did not license Enhanced PROMIS.
- **DOJ breach**: After obtaining Enhanced PROMIS, DOJ refuses to pay the $1 million and disputes Inslaw's IP claims. Inslaw is driven toward bankruptcy.

Bankruptcy litigation and findings:

- **1985 bankruptcy filing**: Inslaw Chapter 11 petition. Complaint against DOJ filed simultaneously.
- **1988 Bankruptcy Court ruling (Judge George Bason)**: Bason rules DOJ acted in bad faith, awards Inslaw approximately $7 million in damages. Bason finds DOJ "took, converted, stole" Inslaw property. Bason notes strong circumstantial evidence of broader DOJ conspiracy.
- **Bason not reappointed**: Judge Bason's 14-year bankruptcy judgeship ends in 1988 shortly after his Inslaw ruling. The replacement judge's selection by a DOJ-involved panel was later cited as an inappropriate DOJ retaliation.
- **1989 district court ruling**: Judge Nicholas Bua affirms Bason's findings.
- **1991 D.C. Circuit**: Reverses on jurisdictional grounds — holds bankruptcy court lacked jurisdiction to determine property claims against DOJ. Substantive findings vacated but not contradicted.

House Judiciary Committee investigation (1989-1992):

- **Investigation scope**: Three years. Rep. Jack Brooks chaired; Rep. Charles Rose conducted primary inquiry.
- **Report (September 1992)**: "The Inslaw Affair" concludes DOJ officials knowingly took Inslaw's property through trickery. Report names specific officials.
- **Broader allegations**: Report examines but does not conclusively confirm allegations that modified PROMIS was sold or given to foreign intelligence services. Key witness Michael Riconosciuto claimed under oath to have modified PROMIS at behest of DOJ official Earl Brian for intelligence use. Riconosciuto was subsequently convicted on unrelated methamphetamine charges.

International distribution allegations:

- **Maxwell connection**: Media baron Robert Maxwell's Pergamon Press reportedly distributed modified PROMIS internationally through the 1980s. Maxwell's 1991 death and subsequent disclosures of his intelligence-service connections (Mossad, possibly KGB) added credibility to allegations.
- **Israeli intelligence**: Declassified documents (MuckRock 2017) confirm Israeli intelligence received PROMIS-related material. Full scope still partially classified.
- **Foreign counterintelligence exploitation**: The allegation that foreign services obtained PROMIS with US-government-inserted backdoors, enabling US collection against those services, remains partially supported but not conclusively documented.

## Why This Event Matters

The Inslaw case is the foundational documented instance of US government appropriation of private-sector database software for intelligence-agency use, and the institutional ancestor of later government-Silicon Valley surveillance integration:

- **Documents government-to-private-sector IP theft for surveillance.** Inslaw's fact pattern — private firm develops database software, government contracts for legitimate use, government misappropriates for broader intelligence purposes — is the archetypal template. The case is the most extensively documented instance because of the bankruptcy proceedings and congressional investigation. Subsequent analogous cases (various FBI analytical-software disputes, post-9/11 intelligence-contractor IP disputes) have received less public attention.
- **Demonstrates DOJ will use personal vendettas and contracting authority to destroy companies.** The C. Madison Brewer appointment as Inslaw contract manager, despite his known personal grievance, became the smoking-gun of DOJ bad faith. The pattern — senior government official with personal hostility appointed to oversee a contract with the hostile-relationship party — recurs in documented cases but is difficult to prove. Inslaw documented it.
- **Institutional lineage from PROMIS to Palantir.** Palantir Technologies (founded 2003, funded by CIA's In-Q-Tel) built a database analytics platform for intelligence and law-enforcement use. Palantir's business model is visibly descended from what PROMIS enhanced was in the 1980s — a relational database with case-tracking and link-analysis capabilities. The specific institutional pathway — DOJ seeks a database platform, government contracts with private firm, government eventually acquires or absorbs the platform into intelligence use — runs from Inslaw 1982-1992 through In-Q-Tel 1999 through Palantir 2003-present.

## Broader Context

The Inslaw case was one of several 1980s DOJ-misconduct cases that collectively discredited the Reagan-era Department of Justice in the eyes of legal and investigative reporters. Other contemporaneous cases included the BCCI scandal, Iran-Contra DOJ handling, the October Surprise allegations (Reagan campaign / Iranian hostage-release negotiations), and the BNL (Banco Nazionale del Lavoro) Iraq-weapons-financing case. In each, DOJ's willingness to pursue justice against politically-connected defendants was questioned.

Hamilton's post-Inslaw career — as persistent advocate for the fraud allegations — is an example of a class of high-stakes whistleblowers whose claims are partly confirmed but never fully adjudicated. The 1991 D.C. Circuit's jurisdictional reversal meant the substantive question (did DOJ steal Inslaw's software and modify it for intelligence use) was never conclusively decided in court. Hamilton's subsequent litigation, media advocacy, and congressional testimony extended over 30 years without producing final resolution.

## Research Gaps

- [ ] Full scope of foreign-intelligence distribution of modified PROMIS — partially classified
- [ ] Specific backdoor technical details if they existed — allegedly highly classified
- [ ] Earl Brian's exact role — partially documented through congressional investigation, not fully adjudicated

## Related Entries

- [[1985-01-01--maxwell-promis-software-distribution-kgb-china]]
- [[1985-01-01--promis-software-global-intelligence-network-establishment]]
- [[1999-09-01--in-q-tel-cia-venture-capital-founded]]
- [[2003-05-01--palantir-founded-paypal-mafia-cia-funding]]

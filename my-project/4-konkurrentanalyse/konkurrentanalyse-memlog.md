---
topic: Konkurrenter for søknadsbrev-verktøy (Jobscan, Rezi, Teal, Kickresume)
type: competitive
decision: 1) Stemmer differensieringen i briefen (åpen telleregel, Korrektur med markerte endringer, forklaringer for studenter)? 2) Hva kan vi lære av konkurrentene uten å utvide omfanget?
preset: standard
updated: 2026-10-27T22:02
---

- (decision by user) Plan godkjent: Run her, type competitive, beslutning = posisjonering + læringspunkter, kun Jobscan/Rezi/Teal/Kickresume, dimensjoner funksjoner/pris/posisjonering/kundestemme (trajectory droppet), 4 assistenter (én per konkurrent), depth 2, validation normal, red team av
- (decision by user) Krav fra bruker: resultatet skal ikke endre noe vi allerede har laget (brief, PRD, UX). Funn legges i egen mappe my-project/4-konkurrentanalyse/
- (source) Runde 1: 4 digests (jobscan/rezi/teal/kickresume-r1-1.md), ~40 kilder; mest egne sider/hjelpesider + Trustpilot. Teal-sider ga 403, kun søkeutdrag.
- (event) Runde 2 startet: én assistent sjekker de lastbærende hullene (Teal egen-brev/diff, Kickresume AI recruiter feedback, Rezi jobbannonse i brev, Teal-pris) og uavhengig bekreftelse av at ingen publiserer telleregel
- (claim) ref=[3] status=verified class=feature pub=2026-10 — Jobscan forklarer bare rekkefølgen på faktorene i match rate, ingen vekter eller formel (bekreftet av JobShinobi [30], svak uavhengighet)
- (claim) ref=[9] status=unverified class=feature pub=2026-07 — Rezi Score har 5 kategorier og noen konkrete terskler, men formel og vekter er ikke publisert; nøkkelord ikke forklart
- (claim) ref=[15] status=unverified class=feature pub=2026-10 — Teal Matching Mode 0–100 % uten publisert formel; tredjeparter beskriver den ulikt
- (claim) ref=[23] status=unverified class=feature pub=2026-10 — Kickresume ATS-score: 20+ vektede sjekker, ikke publisert, kun CV
- (claim) ref=[1] status=unverified class=feature pub=2026-10 — Jobscan har ingen modus for å forbedre eget søknadsbrev med markerte endringer
- (claim) ref=[8] status=verified class=feature pub=2026-08 — Rezi: eget brev kan lastes opp og redigeres for hånd, ingen KI-korrektur med markerte endringer (r1 + r2)
- (claim) ref=[17] status=verified class=feature pub=2026-10 — Teal: søknadsbrev bare generert, ingen dokumentert KI-forbedring av eget brev med markerte endringer ([17] + [33])
- (claim) ref=[22] status=unverified class=feature pub=2026-10 — Kickresume: KI-brev genereres; eget brev bare korrektur av mennesker (€26, engelsk/spansk)
- (claim) ref=[24] status=unverified class=feature pub=2026-10 — Kickresume Resume Tailoring har panel 'What we changed' med grunn per endring, kun CV
- (claim) ref=[5] status=verified class=feature pub=2026-10 — Jobscan kun engelsk (egen hjelpeside; bekreftet av Trustpilot-anmeldelse [7] om tekniske termer)
- (claim) ref=[11] status=unverified class=feature pub=2026-08 — Rezi støtter 9 språk, ikke norsk
- (claim) ref=[26] status=verified class=feature pub=2026-10 — Kickresume oversetting 8 språk, ikke norsk (r1 + r2; Trustpilot sier KI-analyse kun engelsk [28])
- (claim) ref=[20] status=unverified class=feature pub=2026-10 — Teal kun engelsk ifølge katalog (lav)
- (claim) ref=[27] status=unverified class=pricing pub=2026-10 — Kickresume Premium gratis for verifiserte studenter (ISIC/ITIC/UNiDAYS)
- (claim) ref=[18] status=verified class=pricing pub=2026-09 — Teal+ \/uke, \/mnd, \/kvartal, ingen årsplan ([18] + [19]); \/uke-påstanden fra [16] overturned
- (claim) ref=[12] status=unverified class=pricing pub=2026-10 — Rezi gratis: ubegrensede søknadsbrev; Pro \/mnd; Lifetime "
- (claim) ref=[6] status=unverified class=pricing pub=2026-10 — Jobscan gratis 5 skann/mnd; Premium \.95/mnd
- (claim) ref=[7] status=verified class=sentiment pub=2026-09 — Faktura/oppsigelse er det vanligste klagetemaet i 1–2★ hos alle fire ([7],[14],[21],[28])
- (claim) ref=[14] status=verified class=sentiment pub=2026-07 — Generiske/stive KI-tekster er et gjentakende klagetema (Jobscan [7], Rezi [14], Teal [21])
- (source) Runde 2: verify-r2-1.md, ~10 kilder. Reddit blokkert; ingen helt uavhengig kilde for telleregel-påstanden (bare konkurrent-leverandører).
- (assumption) Udaterte, levende leverandørsider får pub=2026-10 (tilgangsmåned) i staleness-beregningen
- (claim) ref=[16] status=overturned class=pricing pub=2026-03 — Teal+ $9/uke og $179/år (motsagt av to nyere kilder [18],[19])
- (event) Sitatsjekk ok etter 3 rettelser ([2] tatt i bruk, 75 % flyttet til [34], Teal-posisjonering til [35]); semantisk sjekk gjort av lead mot digests, ikke egen subagent
- (decision) HTML-briefing og bmad-review-polering hoppet over for å holde omfanget smalt; rapporten er språkvasket for hånd. Kan tas senere ved behov
- (event) Rapport ferdig: 8 verified, 11 unverified, 1 overturned. Kopieres til my-project/4-konkurrentanalyse/

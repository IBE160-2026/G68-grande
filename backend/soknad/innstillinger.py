"""Grenser og konstanter for Søknadsassistenten, samlet på ett sted."""

# Claude-modellen som brukes når ANTHROPIC_MODEL ikke er satt.
STANDARD_MODELL = "claude-opus-5-5"

# Største forespørsel nettsiden tar imot (16 MB). Over det viser innleggingen feilboksen med
# for_stor (story 6.2).
MAKS_FORESPORSEL = 16 * 1024 * 1024
# Største fil som godtas i hvert felt på innleggingen (5 MB, FR-12). En større fil leses ikke.
MAKS_FILSTORRELSE = 5 * 1024 * 1024
# En PDF med færre bokstaver enn dette regnes som uleselig, for eksempel skannet (FR-11).
# Prøvd med testdata/feil/skannet.pdf og PDF-ene i testdata/case-*/ (story 6.2).
MIN_BOKSTAVER_PDF = 50

# Testbrukeren fra README. Den lages ved første oppstart, og bare hvis e-posten ikke finnes.
TESTBRUKER_EPOST = "test@example.com"
TESTBRUKER_PASSORD = "testpassord1"

# Korteste passord ved registrering (FR-1).
MIN_PASSORD_LENGDE = 8

# Flest nøkkelord et KI-svar kan ha (FR-15). Prompten ber om 8–20, og et lengre svar enn
# dette regnes som ubrukelig.
MAKS_NOKKELORD = 30

# Grensene mot høy kostnad med ekte KI (NFR-11). CV og annonse godtar høyst MAKS_TEGN tegn hver
# (brevfeltet i Korrektur MAKS_TEGN_EGET_BREV, se under), og et linjeskift (\r\n fra
# nettleseren) telles som ett tegn. Hver søknad kan bruke høyst MAKS_KI_KALL KI-kall (nøkkelord,
# gap og brev er ett kall hver). Grensen på KI-kall gjelder bare med ekte KI, ikke i testmodus.
# Med KI_NYE_FORSOK = 1 kan ett telt kall bli opptil to forespørsler til API-et. Grensen er en
# myk sperre per søknad (en ny søknad begynner på 0), og taket på 250 kr i Claude Console er den
# siste sperren.
MAKS_TEGN = 15_000
# Brevfeltet i Korrektur har en lavere grense, fordi svaret har hver setning to ganger (gammel og
# ny) og KI-en tenker lenge før den svarer. Målt i retro 5, runde B (my-project/testplan.md):
# et eget brev på 14 585 tegn ga 28 686 tokens ut, tok 190 s og kostet ca. 7,31 kr, altså over
# både KI_MAKS_TOKENS og KI_TIDSGRENSE. Regnet ut fra målingen gir 5 000 tegn ca. 10 000 tokens
# og ca. 70–75 s. Bestemt av Kristine 15. november 2026.
MAKS_TEGN_EGET_BREV = 5_000
MAKS_KI_KALL = 10

# KI-kallet til Claude (AD-13). Tidsgrensen gjelder hver del av kallet (tilkobling, lesing,
# skriving), ikke hele kallet. Målt med testdataene i 4.3.1, 4.4 og 4.5: nøkkelord og gap tok
# 2–5 s hver, og et brev 16–47 s (4.4 og 4.5 i my-project/testplan.md, 4.3.1 i sesjonsloggen
# .logs/kristine/968-…). 90 s er beholdt med vilje, fordi det lengste brevet tok 47 s. Målt med
# lange tekster etter retro 4 (CV og annonse på ca. 14 600 tegn hver, én kjøring): nøkkelord
# ca. 12 s med oppstarten av skriptet, gap 14 s, og de to brevene 25 s og 21 s (retro 4 i
# my-project/testplan.md). 90 s er beholdt også etter den målingen, fordi det lengste kallet
# tok 25 s (bare én kjøring). Med ett nytt forsøk og ventetiden før det (opptil ca. 8 s, eller
# det API-et ber om med retry-after) kan et kall ta lenger enn 2 x 90 s. Korrektur med et eget
# brev på 14 585 tegn tok 190 s og ga 28 686 tokens ut (retro 5, runde B). Derfor har brevfeltet
# en egen, lavere grense (MAKS_TEGN_EGET_BREV), og 90 s og 16 000 tokens er beholdt.
KI_TIDSGRENSE = 90  # sekunder
KI_NYE_FORSOK = 1
KI_MAKS_TOKENS = 16000
# Hvor mye Claude tenker. medium er standarden for claude-opus-5-5, men settes uttrykkelig.
KI_INNSATS = "medium"

# Pris i dollar per million tokens for claude-opus-5-5, bare til anslaget i loggen. Brukes
# en annen modell (ANTHROPIC_MODEL), er anslaget fortsatt regnet med disse prisene.
KI_PRIS_INN = 4
KI_PRIS_UT = 20
# Omtrentlig kronekurs, bare til anslaget i loggen.
KRONER_PER_DOLLAR = 11

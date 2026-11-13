"""Grenser og konstanter for Søknadsassistenten, samlet på ett sted."""

# Claude-modellen som brukes når ANTHROPIC_MODEL ikke er satt.
STANDARD_MODELL = "claude-opus-5-5"

# Største forespørsel nettsiden tar imot (16 MB).
MAKS_FORESPORSEL = 16 * 1024 * 1024

# Testbrukeren fra README. Den lages ved første oppstart, og bare hvis e-posten ikke finnes.
TESTBRUKER_EPOST = "test@example.com"
TESTBRUKER_PASSORD = "testpassord1"

# Korteste passord ved registrering (FR-1).
MIN_PASSORD_LENGDE = 8

# Flest nøkkelord et KI-svar kan ha (FR-15). Prompten ber om 8–20, og et lengre svar enn
# dette regnes som ubrukelig.
MAKS_NOKKELORD = 30

# KI-kallet til Claude (AD-13). Tidsgrensen er en startverdi og justeres etter målingen i
# story 4.3. Den gjelder hver del av kallet (tilkobling, lesing, skriving), ikke hele kallet.
# Med ett nytt forsøk og ventetiden før det (opptil ca. 8 s, eller det API-et ber om med
# retry-after) kan et kall ta lenger enn 2 x 90 sekunder. Den faktiske tiden måles i 4.3.
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

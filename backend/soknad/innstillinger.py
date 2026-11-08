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

"""Grenser og konstanter for Søknadsassistenten, samlet på ett sted."""

# Claude-modellen som brukes når ANTHROPIC_MODEL ikke er satt.
STANDARD_MODELL = "claude-opus-5-5"

# Største forespørsel nettsiden tar imot (16 MB).
MAKS_FORESPORSEL = 16 * 1024 * 1024

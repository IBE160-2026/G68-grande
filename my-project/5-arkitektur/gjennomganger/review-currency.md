---
review: currency (versjoner, at teknologien finnes og passer, at påstander holder)
target: ../ARCHITECTURE-SPINE.md (+ .memlog.md)
date: 2026-11-04
method: PyPI JSON API (curl), kjøring av pakkene i midlertidig uv-miljø, prøvebygg av et mock-prosjekt, WebSearch
---

# Review: aktualitet og virkelighetssjekk

**Konklusjon:** Stacken er oppdatert og sjekket mot virkeligheten. Alle pakkeversjoner stemmer med PyPI i dag, og API-ene arkitekturen bygger på finnes i de låste versjonene. Én påstand holder ikke: reserveveien `pip install .` feiler med prosjektstrukturen slik den er tegnet. To KI-detaljer (antall nye forsøk og hva JSON-skjemaet må inneholde) bør skrives tydeligere, ellers blir de feil i koden.

## 1. Versjoner (PyPI JSON API, 2026-11-04)

| Pakke | Spine | Nyeste på PyPI | requires_python | Lastet opp | Status |
| --- | --- | --- | --- | --- | --- |
| Flask | 3.1.3 | 3.1.3 | >=3.9 | 2026-02-19 | OK |
| anthropic | 2.4.0 | 2.4.0 | >=3.10 | 2026-11-02 | OK (to dager gammel, se F-6) |
| pypdf | 6.21.4 | 6.21.4 | >=3.9 | 2026-10-28 | OK |
| python-docx | 1.2.0 | 1.2.0 | >=3.9 | 2025-06-16 | OK (fortsatt nyeste) |
| fpdf2 | 2.9.0 | 2.9.0 | >=3.11 | 2026-10-29 | OK |
| python-dotenv | 1.2.4 | 1.2.4 | >=3.10 | 2026-10-01 | OK |
| pytest | 9.2.0 | 9.2.0 | >=3.10 | 2026-10-27 | OK |
| ruff | 0.17.3 | 0.17.3 | >=3.7 | 2026-10-27 | OK |
| uv | «gjeldende» | 0.13.7 | – | 2026-11-03 | Kristines PC har 0.12.15 (se F-5) |
| werkzeug (via Flask) | – | 3.1.9 | >=3.9 | 2026-09-27 | OK |

**Python-gulv:** Det høyeste kravet blant pakkene kommer fra fpdf2 (>=3.11). Spinens «≥ 3.12» er altså trygt og strengere enn nødvendig, og det stemmer med memlog. Ingen endring trengs.

Memlog-oppføringen `(version)` stemmer med alt over. Sjekken ble faktisk gjort, og versjonene er ikke hentet fra treningsdata.

## 2. Påstander som er sjekket ved å kjøre koden

Alle pakkene ble installert i et midlertidig miljø med `uv run --no-project --with ...` i de låste versjonene.

| Påstand i spine | Funn | Status |
| --- | --- | --- |
| anthropic: structured outputs via `output_config.format` (AD-4) | `Messages.create` har parameteren `output_config`. `OutputConfigParam` = `{effort, format}`, `JSONOutputFormatParam` = `{type: "json_schema", schema: dict}`. Den gamle `output_format` finnes ikke lenger i `create`, og `messages.parse` finnes også. Anthropics dokumentasjon bekrefter at `output_format` er flyttet til `output_config.format`, og at det ikke trengs beta-header. | OK |
| anthropic: tidsgrense og nye forsøk på klienten (AD-13) | `Anthropic(timeout=..., max_retries=...)` finnes. **Standard `max_retries` er 2**, ikke 1. | Se F-2 |
| Feiltyper → `KIFeil(nettverk / annet)` (AD-13) | `APIConnectionError` og `APITimeoutError` finnes, og `APITimeoutError` er en underklasse av `APIConnectionError`. De øvrige feilene arver fra `APIStatusError`/`APIError`. Det gir en enkel todeling. | OK |
| JSON-skjema for KI-svar (AD-4) | Ekstern dokumentasjon (Vertex- og Bedrock-utgavene av Anthropics funksjon) sier at objekter krever `additionalProperties: false`, at tall- og lengdegrenser ikke støttes, og at det er et tak på antall valgfrie felt. Dette berører `grunn?` og `str \| null`. | Se F-3 |
| Python `re` behandler æ/ø/å som bokstaver i ord-grenser (AD-6) | `\bår\b` gir 1 treff i «Hvert år, påår og års». `\bøl\b` gir 1 treff i «Øl og søl» (med `re.I`). `\bbjørn\b` treffer ikke «bjørnebær». Vanlige `str`-mønstre forstår Unicode som standard. NB: bindestrek regnes som ordgrense, så «år-tall» gir treff på «år». | OK (+ merknad F-4) |
| `werkzeug.security` til passord (AD-12) | `generate_password_hash` gir `scrypt:32768:8:1$...`, og `check_password_hash` virker. Følger med Flask 3.1.3 / Werkzeug 3.1.9. | OK |
| fpdf2 med Unicode-TTF (AD-11) | fpdf2-dokumentasjonen (Unicode.html) bekrefter full støtte for å bygge inn TTF/OTF med `add_font`. Text shaping (uharfbuzz) trengs bare for skrifter som ikke er latinske, så æøå klarer seg uten. NB: `add_font` kalles én gang per stil, så fet skrift krever en egen TTF-fil. | OK |
| `uv sync` + `uv run flask --app soknad run` | Prøvd i et mock-prosjekt med `pyproject.toml` uten `[build-system]`. `uv sync` installerte avhengighetene, og `uv run flask --app soknad routes` fant appen. Prosjektet blir behandlet som «virtuelt» og importeres fra mappen der kommandoen kjøres. | OK |
| `pip install .` som reserve | **Feiler.** Prøvebygget av samme mock-oppsett (`soknad/`, `prompts/`, `testdata/` og `instance/` i roten, uten `[build-system]`) ga: `error: Multiple top-level packages discovered in a flat-layout: ['soknad', 'prompts', 'instance', 'testdata']`. Selv med et byggeoppsett som virker, ville `pip install .` bare installert `soknad` i site-packages. Den installerer heller ikke pytest/ruff, og den krever at Python allerede finnes på maskinen. | Se F-1 |
| Modell `claude-opus-5-5`, $4/$20 per MTok | Godtatt etter oppdraget (Anthropic-dokumentasjon bufret 2026-10-06). Ingen funn som sier noe annet. Om akkurat denne modellen støtter structured outputs, ble ikke bekreftet, så det må prøves ved første ekte kall. | OK (bekreft i første ekte KI-story) |

## 3. Teknologier som fortsatt finnes og passer

- Flask 3.1 / Jinja, pypdf, python-docx, fpdf2, python-dotenv, pytest, ruff og uv vedlikeholdes alle aktivt, og de fleste har hatt utgivelser de siste to månedene. python-docx 1.2.0 er fra juni 2025, men er fortsatt nyeste versjon og stabil.
- Ingen av de valgte pakkene er utgått eller erstattet.
- GitHub Actions med uv: `astral-sh/setup-uv` er den vanlige måten. Det er rutine i CI-storyen.

## 4. Funn

| ID | Alvor | Funn | Forslag |
| --- | --- | --- | --- |
| F-1 | **Høy** | «`pip install .` fungerer som reserve» (Drift, og memlog) er feil. setuptools stopper på flat-layout med flere toppmapper, noe prøvebygget bekreftet. Den ville uansett ikke installere testverktøyene, og den krever Python, som er akkurat det sensor kanskje mangler. | Stryk påstanden, eller bytt reserven til `uv export --no-dev --no-hashes -o requirements.txt` + `pip install -r requirements.txt` (generert, ikke håndskrevet). Å legge inn `[build-system]` med `packages = ["soknad"]` hjelper ikke for filene utenfor pakken (`prompts/`, `testdata/`). |
| F-2 | Middels | AD-13 sier «1 nytt forsøk», men anthropic-klienten har `max_retries=2` som standard. SDK-tidsgrensen gjelder hvert forsøk, så verste ventetid blir ca. 2 × 90 s pluss pause. | Skriv i AD-13 at `Anthropic(timeout=90, max_retries=1)` settes eksplisitt, og at 90 s gjelder per forsøk (opptil ca. 3 min totalt). Sjekk at ventetegnet og UX tåler det. |
| F-3 | Middels | AD-4 nevner ikke kravene til JSON-skjema i structured outputs: `additionalProperties: false` på alle objekter, ingen lengdegrenser og et tak på antall valgfrie felt. Et avkuttet svar (`stop_reason` = `max_tokens` eller `refusal`) gir ugyldig eller tom JSON. | Legg til én linje i AD-4: skjemaene har `additionalProperties: false`, og `stop_reason` ≠ `end_turn` gir `KIFeil(ubrukelig_svar)`. |
| F-4 | Lav | Ordgrense med `re` er bekreftet for æøå. Bindestrek og tall regnes også som grenser, så «år-tall» teller som «år». | Lag en kjernetest for bindestrek i telleregel-storyen, så oppførselen blir et bevisst valg. |
| F-5 | Lav | Kristines uv er 0.12.15, mens nyeste er 0.13.7. «gjeldende» i stack-tabellen kan ikke etterprøves. | Skriv en minsteversjon (f.eks. `uv ≥ 0.12`) i stack-tabellen eller README, eventuelt `[tool.uv] required-version`. |
| F-6 | Lav | anthropic 2.4.0 er bare to dager gammel og en ny hovedversjon (2.x). Mange eksempler på nettet bruker eldre API-former (`output_format` + beta-header). | Lås versjonen i `uv.lock` (allerede planlagt) og følg SDK-ens egne typer (`output_config`), ikke eldre eksempler. |

## Kilder

- PyPI JSON API: `https://pypi.org/pypi/<pakke>/json` for flask, anthropic, pypdf, python-docx, fpdf2, python-dotenv, pytest, ruff, uv og werkzeug (hentet 2026-11-04)
- [Anthropic – Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs?m=1)
- [Vertex AI – Structured outputs with Anthropic Claude models](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude/structured_outputs)
- [Amazon Bedrock – Structured output](https://docs.aws.amazon.com/bedrock/latest/userguide/structured-output.html)
- [fpdf2 – Unicode](https://py-pdf.github.io/fpdf2/Unicode.html), [fpdf2 – Text shaping](https://py-pdf.github.io/fpdf2/TextShaping.html)
- Lokale kjøringer: inspeksjon av anthropic 2.4.0, regex-test i Python 3.14, werkzeug-hash, prøvebygg med `pip wheel .`, og `uv sync`/`uv run flask` i et mock-prosjekt (scratchpad)

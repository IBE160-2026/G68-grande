# Mine valg og KI-feil jeg fant (arkitektur)

En kort oversikt over hva jeg bestemte selv i arkitekturarbeidet, og hvilke feil som ble funnet i det KI-en laget. Tallene viser til radene i [prompt-loggen](../prompt-logg.md). Alle beslutningene står i [beslutningsloggen](arkitektur-memlog.md).

## Mine valg

1. **Veiledet arbeidsmåte.** Jeg ville ta de store valgene selv, ett om gangen, i stedet for at KI-en skrev alt på én gang. (195)
2. **Det enkleste som gir et godt resultat.** Jeg har aldri kodet før, så det viktigste for meg var at det skulle være enkelt. Derfor ble det Python og Flask, ett språk for hele nettsiden. (196)
3. **Claude Opus 5.5 og et tak på 250 kr.** Jeg valgte den beste modellen, men satte en grense for hvor mye jeg vil bruke. Kreditten kjøpes på forhånd uten automatisk påfylling, så jeg kan ikke bruke mer enn det jeg har satt inn. (197)
4. **pypdf for å lese PDF.** Kolonner og tabeller prøves først. Går det dårlig, blir det en kjent begrensning. (198)
5. **Koden delt i tre lag.** Jeg godkjente at reglene ligger for seg selv, slik at de kan testes uten nettleser og API-nøkkel, og at testmodus og ekte KI er to utgaver av det samme. (199)
6. **Grunn ved endring venter.** En kort grunn ved hver endring i Korrektur var en god idé fra konkurrentanalysen, men den legges til bare hvis det blir tid. (200)

## KI-feil jeg fant

KI-en lot fire uavhengige hjelpere lese utkastet kritisk. Rapportene ligger i [`gjennomganger/`](gjennomganger/).

1. **Nettsiden ville ikke startet hos sensor.** Utkastet sa ikke hvor den hemmelige nøkkelen for innlogging kommer fra. Uten `.env` ville nettsiden krasjet. Nå lager den en nøkkel selv.
2. **Økten hadde ingen fast form.** Utkastet sa ikke hva tingene i økten skal hete. To stories kunne da lagret og lest CV-en med ulike navn. Testmodus ville også blitt slått av ved en ny søknad, selv om UX sier at den skal huskes.
3. **Feil ville blitt vist én om gangen.** UX krever at alle feilene vises samtidig.
4. **Feil avrunding.** Pythons vanlige avrunding gjør 12,5 % til 12 %, men FR-17 og fasiten sier 13 %. Det ville fått suksesskriterium 2 til å feile. (201)
5. **Telleregelen var beskrevet feil.** Utkastet sa «ord-grenser», som kan leses som at «Python» ikke er et treff i «python-utvikler». Det går mot FR-17.
6. **En reserve som ikke virket.** KI-en skrev at `pip install .` kunne brukes i stedet for uv. En hjelper prøvde det, og det virket ikke.
7. **Python var ikke installert.** KI-en tok først for gitt at Python fantes på PC-en min. Det gjorde det ikke, og derfor ble installasjonen endret til uv.

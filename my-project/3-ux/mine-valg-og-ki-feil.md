# Mine valg og KI-feil jeg fant (UX)

En kort oversikt over hva jeg bestemte selv i UX-arbeidet, og hvilke feil jeg fant i det KI-en laget. Tallene viser til radene i [prompt-loggen](../prompt-logg.md). Alle beslutningene står i [beslutningsloggen](ux-memlog.md).

## Mine valg

1. **Fargetemaet «Myk fersken».** KI-en laget fem lilla varianter for å teste tvilen min, men jeg valgte likevel «Myk fersken», fordi den var «så lun». (119)
2. **«Dette kan du jobbe videre med» i stedet for «Mangler».** Det er hyggeligere å se. I PRD-en og testene heter det fortsatt «mangler». (126)
3. **Fyrverkeri når brevet er ferdig.** Det var min idé, også ved hvert nytt forslag. (127)
4. **Markering per setning i Korrektur.** Jeg valgte det fremfor markering per ord, fordi det er mindre rotete. Man ser likevel det gamle ved å trykke på setningen. (135)
5. **Skisser av alle sidene.** Jeg ville ha skisser av alle sidene på PC og mobil, ikke bare modusvalget og resultatsiden. (141)
6. **Hovedfargen som ramme rundt skrivefeltene.** Rammen hadde for svak kontrast. Jeg så en sammenligning og valgte hovedfargen i stedet for fargen KI-en foreslo (#A77C8D). (147)
7. **Personopplysninger er brukerens valg.** Samtykket anbefaler å fjerne personopplysninger fra CV-en, men det skal ikke være et krav. (122)
8. **Kutteliste for pynten.** Fyrverkeri, animasjoner og ekstra vinduer bygges sist og kuttes først hvis tiden blir knapp. Kjerneflyten og testene kommer først. (152)
9. **Egne tekster.** Venteteksten «Vi lager brevet ditt – det kan ta en liten stund.» er min egen. Jeg valgte også «E-posten er ikke gyldig» fremfor teksten KI-en foreslo. (156)

## KI-feil jeg fant

1. **«Appen».** KI-en kalte nettsiden en app. Jeg rettet den: det er en nettside. (118)
2. **Logg ut-knappen manglet.** KI-en hadde glemt logg ut-knappen og KI-merknaden i skissen, selv om de var bestemt. (131)
3. **«Testmodus» på feil sted.** KI-en viste merkelappen «Testmodus» i en skisse der man ikke var i testmodus. (135)
4. **Tilbakeknappen manglet.** Tilbakeknappen fra FR-19 var ikke med i skissene. (136)
5. **Registreringssiden var ikke tegnet.** Jeg oppdaget at den manglet. (140)
6. **Sider og feilmeldinger uten skisse.** Tre viktige sider og tre feilmeldinger fra PRD-en manglet skisse. Jeg ba om en oversikt og fant hullene. (141, 144)
7. **Feil brukerreiser i utkastet.** Hjelperen som skrev DESIGN.md og EXPERIENCE.md, kunne ikke se samtalen, og skrev brukerreisene med feil steg. De ble rettet til stegene jeg hadde bekreftet. (146)
8. **En feil som ikke fantes.** To hjelpere mente at «i»-boksen i skissen bare blinket når man klikket. Jeg testet den selv i Chrome med Tab, musa over og klikk, og den virket. KI-en tok feil, og det var testingen min som viste det. (154)

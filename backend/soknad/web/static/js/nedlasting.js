// Nedlastingen på brevsiden (FR-29, FR-31, UX-DR16, UX-DR17). Et trykk på en lenke med
// data-nedlasting laster ned filen som vanlig (svaret er et vedlegg, så siden blir stående).
// Skriptet gjør knappen grønn med «✓ Lastet ned som …», viser filnavnet under, skjuler
// feilboksen fra en nedlasting av samme format som feilet (ikke KI-feilboksen fra «Nytt
// forslag», og ikke boksen for det andre formatet) og åpner vinduet etter nedlasting. Før
// vinduet åpnes, kopieres filnavnet for formatet som ble lastet ned, inn i vinduet (story 7.2).
// Er brevet lastet ned, spør ikke «Logg ut» nede til høyre lenger: skriptet tar bort
// data-bekreft="vindu-logg-ut" fra knappen, så brukeren logges ut med en gang, også før siden
// lastes på nytt (story 7.5, NFR-4). Tekstene står alt i siden.
// Skriptet endrer bare hvordan siden ser ut, aldri søknadsdata (AD-1). Kan filen ikke lages,
// svarer serveren med brevsiden og feilboksen, og vinduet er borte.
(function () {
  var vindu = document.getElementById("vindu-nedlastet");
  // Knappen under brevet fra siste trykk. Fokus går tilbake hit når vinduet lukkes.
  var tilbakeTil = null;

  document.addEventListener("click", function (hendelse) {
    var lenke = hendelse.target.closest("a[data-nedlasting]");
    if (!lenke) {
      return;
    }
    var format = lenke.getAttribute("data-nedlasting");
    var knapp = document.getElementById("last-ned-" + format);
    var filnavn = document.getElementById("filnavn-" + format);
    var feilboks = document.getElementById("feilboks");
    if (knapp) {
      knapp.classList.add("ferdig");
      knapp.querySelector(".ikke-lastet-ned").hidden = true;
      knapp.querySelector(".lastet-ned").hidden = false;
    }
    if (filnavn) {
      filnavn.hidden = false;
    }
    // Brevet er lastet ned: «Logg ut» nede til høyre logger ut uten vinduet (story 7.5).
    var loggUt = document.querySelector('[data-bekreft="vindu-logg-ut"]');
    if (loggUt) {
      loggUt.removeAttribute("data-bekreft");
    }
    // Bare feilboksen fra en nedlasting av samme format som feilet (FilFeil), med lenken for
    // det formatet, skjules. Feilet PDF-en og brukeren laster ned Word, blir boksen for PDF
    // stående (retro 7). KI-feilboksen fra «Nytt forslag» (story 7.1) har samme id, men ingen
    // nedlastingslenke, og blir også stående.
    if (feilboks && feilboks.querySelector('a[data-nedlasting="' + format + '"]')) {
      // Kom trykket fra «Prøv på nytt» i feilboksen, flyttes fokus til knappen under brevet,
      // så fokus ikke forsvinner når boksen skjules.
      var fraFeilboks = feilboks.contains(lenke);
      feilboks.hidden = true;
      if (fraFeilboks && knapp) {
        knapp.focus();
      }
    }
    // Vinduet etter nedlasting: åpnes hver gang, med fokus på «Bli her» (UX-DR17). Filnavnet i
    // vinduet blir det for formatet som ble lastet ned (story 7.2), kopiert fra filnavn-linjen.
    if (vindu && !vindu.open) {
      tilbakeTil = knapp;
      var vinduFilnavn = document.getElementById("vindu-nedlastet-filnavn");
      if (filnavn && vinduFilnavn) {
        vinduFilnavn.textContent = filnavn.textContent;
      }
      vindu.showModal();
      var bliHer = document.getElementById("bli-her");
      if (bliHer) {
        bliHer.focus();
      }
    }
  });

  // «Bli her» og Esc lukker vinduet. Fokus går tilbake til knappen under brevet, ikke dit
  // nettleseren ville sendt det (for eksempel «Prøv på nytt» i den skjulte feilboksen).
  if (vindu) {
    vindu.addEventListener("close", function () {
      if (tilbakeTil) {
        tilbakeTil.focus();
      }
    });
  }
})();

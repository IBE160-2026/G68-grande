// Nedlastingen på brevsiden (FR-29, FR-31, UX-DR16, UX-DR17). Et trykk på en lenke med
// data-nedlasting laster ned filen som vanlig (svaret er et vedlegg, så siden blir stående).
// Skriptet gjør knappen grønn med «✓ Lastet ned som …», viser filnavnet under, skjuler
// feilboksen fra et forsøk som feilet og åpner vinduet etter nedlasting. Tekstene står alt i
// siden. Skriptet endrer bare hvordan siden ser ut, aldri søknadsdata (AD-1). Kan filen ikke
// lages, svarer serveren med brevsiden og feilboksen, og vinduet er borte.
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
    if (feilboks) {
      // Kom trykket fra «Prøv på nytt» i feilboksen, flyttes fokus til knappen under brevet,
      // så fokus ikke forsvinner når boksen skjules.
      var fraFeilboks = feilboks.contains(lenke);
      feilboks.hidden = true;
      if (fraFeilboks && knapp) {
        knapp.focus();
      }
    }
    // Vinduet etter nedlasting: åpnes hver gang, med fokus på «Bli her» (UX-DR17).
    if (vindu && !vindu.open) {
      tilbakeTil = knapp;
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

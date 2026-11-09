// Innleggingsfeltene (UX-DR8): «Lim inn tekst» åpner tekstboksen, og søppelbøtta tømmer den.
// Skriptet endrer bare skjemaet i nettleseren. Søknaden endres først når skjemaet sendes,
// og det gjør bare serveren (AD-1).
document.addEventListener("DOMContentLoaded", function () {
  var status = document.getElementById("innlegging-status");
  // Meldingen som venter på å bli skrevet. Trykkes søppelbøtta igjen før det, gjelder bare
  // den siste.
  var ventende = null;

  // Det som skal ha fokus i et felt: tekstboksen når den vises, ellers «Lim inn tekst».
  function fokusIFeltet(felt, utenRulling) {
    var limeboks = felt.querySelector(".limeboks");
    var mal = limeboks.hidden ? felt.querySelector(".lim-inn") : felt.querySelector("textarea");
    mal.focus({ preventScroll: utenRulling });
  }

  document.querySelectorAll(".innleggingsfelt").forEach(function (felt) {
    var tomTilstand = felt.querySelector(".tom-tilstand");
    var limeboks = felt.querySelector(".limeboks");
    var tekstboks = felt.querySelector("textarea");
    var limInn = felt.querySelector(".lim-inn");
    var soppelbotte = felt.querySelector(".soppelbotte");

    limInn.addEventListener("click", function () {
      tomTilstand.hidden = true;
      limeboks.hidden = false;
      tekstboks.focus();
    });

    // Tømmer uten bekreftelse (FR-13). Fokus går til «Lim inn tekst» i samme felt.
    soppelbotte.addEventListener("click", function () {
      tekstboks.value = "";
      limeboks.hidden = true;
      tomTilstand.hidden = false;
      limInn.focus();
      // Tømmes og fylles på nytt, så skjermlesere leser teksten også når den er lik som sist.
      status.textContent = "";
      window.clearTimeout(ventende);
      ventende = window.setTimeout(function () {
        status.textContent = soppelbotte.dataset.tomt;
      }, 100);
    });
  });

  // En lenke i feilboksen gir fokus til knappen eller tekstboksen i feltet med feilen.
  document.querySelectorAll(".feilboks a").forEach(function (lenke) {
    lenke.addEventListener("click", function (hendelse) {
      var felt = document.getElementById(lenke.getAttribute("href").slice(1));
      if (!felt) {
        return;
      }
      hendelse.preventDefault();
      // Feltnavnet og feilteksten skal også synes, så hele feltet rulles fram først.
      felt.scrollIntoView({ block: "start" });
      fokusIFeltet(felt, true);
    });
  });
});

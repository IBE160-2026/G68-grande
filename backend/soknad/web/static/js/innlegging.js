// Innleggingsfeltene (UX-DR8): «Last opp PDF» åpner filvelgeren, «Lim inn tekst» åpner
// tekstboksen, og søppelbøttene tømmer feltet. Skriptet endrer bare skjemaet i nettleseren.
// Fila leses og søknaden endres først når skjemaet sendes, og det gjør bare serveren (AD-1).
document.addEventListener("DOMContentLoaded", function () {
  var status = document.getElementById("innlegging-status");
  // Meldingen som venter på å bli skrevet. Kommer en ny melding før det, gjelder bare den siste.
  var ventende = null;

  // Tømmes og fylles på nytt, så skjermlesere leser teksten også når den er lik som sist.
  function meld(tekst) {
    status.textContent = "";
    window.clearTimeout(ventende);
    ventende = window.setTimeout(function () {
      status.textContent = tekst;
    }, 100);
  }

  // Det som skal ha fokus i et felt: søppelbøtta når filnavnet vises, tekstboksen når den
  // vises, ellers «Last opp PDF».
  function fokusIFeltet(felt, utenRulling) {
    var filboks = felt.querySelector(".filboks");
    var limeboks = felt.querySelector(".limeboks");
    var mal = felt.querySelector(".last-opp");
    if (!filboks.hidden) {
      mal = filboks.querySelector(".soppelbotte");
    } else if (!limeboks.hidden) {
      mal = limeboks.querySelector("textarea");
    }
    mal.focus({ preventScroll: utenRulling });
  }

  document.querySelectorAll(".innleggingsfelt").forEach(function (felt) {
    var tomTilstand = felt.querySelector(".tom-tilstand");
    var limeboks = felt.querySelector(".limeboks");
    var filboks = felt.querySelector(".filboks");
    var tekstboks = limeboks.querySelector("textarea");
    var kilde = felt.querySelector(".kilde");
    var fil = felt.querySelector(".filvelger");
    var filnavn = filboks.querySelector(".filnavn");
    var lastOpp = felt.querySelector(".last-opp");
    var limInn = felt.querySelector(".lim-inn");

    // Tilbake til tom tilstand, med fokus på «Last opp PDF» i samme felt (FR-13).
    function tom(soppelbotte) {
      tekstboks.value = "";
      fil.value = "";
      filnavn.textContent = "";
      filnavn.title = "";
      kilde.value = "tekst";
      limeboks.hidden = true;
      filboks.hidden = true;
      tomTilstand.hidden = false;
      lastOpp.focus();
      meld(soppelbotte.dataset.tomt);
    }

    lastOpp.addEventListener("click", function () {
      fil.click();
    });

    // En valgt fil vises med en gang med navnet. Den sjekkes ikke før skjemaet sendes.
    fil.addEventListener("change", function () {
      if (!fil.files || fil.files.length === 0) {
        return;
      }
      var navn = fil.files[0].name;
      filnavn.textContent = navn;
      filnavn.title = navn;
      kilde.value = "fil";
      tomTilstand.hidden = true;
      limeboks.hidden = true;
      filboks.hidden = false;
      filboks.querySelector(".soppelbotte").focus();
      meld(fil.dataset.lastetOpp + navn);
    });

    limInn.addEventListener("click", function () {
      kilde.value = "tekst";
      tomTilstand.hidden = true;
      limeboks.hidden = false;
      tekstboks.focus();
    });

    // Begge søppelbøttene tømmer uten bekreftelse (FR-13).
    felt.querySelectorAll(".soppelbotte").forEach(function (soppelbotte) {
      soppelbotte.addEventListener("click", function () {
        tom(soppelbotte);
      });
    });
  });

  // En lenke til et felt (href="#...") i feilboksen gir fokus til knappen, filnavnet eller
  // tekstboksen i feltet med feilen. Andre lenker i boksen («Lag ny søknad» og «Gå til
  // brevet») er vanlige lenker til en annen side (retro 8, A7).
  document.querySelectorAll('.feilboks a[href^="#"]').forEach(function (lenke) {
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

// Tilbakeknappen: nettleseren kan vise en side etter innlogging fra minnet uten å spørre
// serveren, også etter utlogging. Da lastes siden på nytt, og er brukeren logget ut,
// sender serveren til innloggingen. Skriptet endrer aldri data.
window.addEventListener("pageshow", function (hendelse) {
  if (hendelse.persisted) {
    window.location.reload();
  }
});

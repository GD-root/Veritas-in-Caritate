var VERSAO = "veritas-v1";
var ARQUIVOS = ["./", "index.html", "manifest.webmanifest", "icone-180.png", "icone-192.png", "icone-512.png", "icone-512-mascara.png"];

self.addEventListener("install", function (e) {
  e.waitUntil(caches.open(VERSAO).then(function (c) { return c.addAll(ARQUIVOS); }));
  self.skipWaiting();
});

self.addEventListener("activate", function (e) {
  e.waitUntil(caches.keys().then(function (nomes) {
    return Promise.all(nomes.filter(function (n) { return n !== VERSAO; }).map(function (n) { return caches.delete(n); }));
  }));
  self.clients.claim();
});

self.addEventListener("fetch", function (e) {
  if (e.request.method !== "GET") return;
  var url = new URL(e.request.url);
  var fonte = url.hostname === "fonts.googleapis.com" || url.hostname === "fonts.gstatic.com";
  if (url.origin !== location.origin && !fonte) return;
  if (e.request.mode === "navigate") {
    e.respondWith(fetch(e.request).then(function (r) {
      var copia = r.clone();
      caches.open(VERSAO).then(function (c) { c.put("index.html", copia); });
      return r;
    }).catch(function () { return caches.match("index.html"); }));
    return;
  }
  e.respondWith(caches.match(e.request).then(function (salvo) {
    return salvo || fetch(e.request).then(function (r) {
      var copia = r.clone();
      caches.open(VERSAO).then(function (c) { c.put(e.request, copia); });
      return r;
    });
  }));
});

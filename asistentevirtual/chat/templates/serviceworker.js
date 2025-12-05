const CACHE_NAME = "asistente-v1";

// Cuando la app se instala, guardamos cosas básicas en caché
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll([
        "/",
        "/static/css/styles.css", // Asegúrate de que esta ruta exista si tienes CSS
        // Agrega aquí otros archivos que quieras que funcionen offline
      ]);
    })
  );
});

// Cuando la app pide algo (fetch), intentamos responder
self.addEventListener("fetch", (event) => {
  event.respondWith(
    fetch(event.request).catch(() => {
      return caches.match(event.request);
    })
  );
});

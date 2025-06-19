// templates/service-worker.js

const CACHE_NAME = 'dojo-manual-cache-v1';
// FIX: Removed the redundant '/' since {% url 'core:home' %} resolves to it.
const URLS_TO_CACHE = [
  '{% url "core:home" %}',
  // You can add paths to your main CSS or JS files here in the future
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(URLS_TO_CACHE);
      })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          return response; // Serve from cache
        }
        return fetch(event.request); // Fetch from network
      })
  );
});

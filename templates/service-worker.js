const CACHE_NAME = 'dojo-manual-cache-v1';
// These URLs will be cached on install
const URLS_TO_CACHE = [
  '/',
  '{% url "core:home" %}',
  // Add paths to your main CSS or JS files if you create them
];

// Install the service worker and cache core assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(URLS_TO_CACHE);
      })
  );
});

// Serve cached content when offline
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // If we have a match in the cache, return it.
        if (response) {
          return response;
        }
        // Otherwise, fetch from the network.
        return fetch(event.request);
      }
    )
  );
});
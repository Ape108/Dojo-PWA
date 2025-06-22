// templates/service-worker.js

// Increment the cache name to v5 to ensure the new service worker logic is applied.
const CACHE_NAME = 'chuan-fa-cache-v5';

// We still pre-cache the landing page for offline fallback.
const URLS_TO_CACHE = [
  '{% url "core:landing" %}',
];

self.addEventListener('install', event => {
  // skipWaiting() forces the waiting service worker to become the
  // active service worker. This ensures the new cache is used immediately.
  self.skipWaiting();
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache and caching new files');
        return cache.addAll(URLS_TO_CACHE);
      })
  );
});

// This event activates when the new service worker starts working.
// We'll clean up the old cache here.
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          // If the cache name is not our current one, delete it.
          if (cacheName !== CACHE_NAME) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

self.addEventListener('fetch', event => {
  // For navigation requests (i.e., fetching an HTML page), use a network-first strategy.
  // This ensures the user always gets the latest version of the page with a valid CSRF token if they are online.
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request).catch(() => {
        // If the network request fails (e.g., user is offline), serve the cached landing page.
        return caches.match('{% url "core:landing" %}');
      })
    );
    return;
  }

  // For all other requests (like static assets), a cache-first strategy is appropriate.
  // These files don't change often and don't contain dynamic data like CSRF tokens.
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});

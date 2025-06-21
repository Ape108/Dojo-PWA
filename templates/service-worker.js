// templates/service-worker.js

// By changing the cache name from v1 to v2, we force the service worker to
// discard the old cache (with the old homepage) and create a new one.
const CACHE_NAME = 'dojo-manual-cache-v2';

const URLS_TO_CACHE = [
  '{% url "core:home" %}',
  // It's also a good idea to cache the base structure, but for now,
  // just caching the homepage URL is enough to fix the issue.
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
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // If we have a cached version, return it. Otherwise, fetch from the network.
        return response || fetch(event.request);
      })
  );
});

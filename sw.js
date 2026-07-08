// Service Worker: यह आपकी ऐप को बिना ब्राउज़र पट्टी के चलाने और ऑफलाइन काम करने में मदद करता है
const CACHE_NAME = 'voice-app-v1';
const ASSETS = [
  './',
  './index.html',
  './manifest.json'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS);
    })
  );
});

self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((response) => {
      return response || fetch(e.request);
    })
  );
});
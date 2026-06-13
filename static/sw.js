// iPon service worker — lightweight offline support.
// Strategy:
//   - Static assets (/static/*): cache-first
//   - Page navigations: network-first, fall back to the offline page
//   - Authenticated HTML is never stored (avoids stale / cross-user data)

const CACHE = 'ipon-v2';

// Only precache things that always exist and are safe to cache.
// Icons are cached on-demand by the static rule below, so a missing
// icon never breaks service-worker installation.
const PRECACHE = [
  '/offline',
  '/static/css/modern.css',
  '/static/js/sidebar.js'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE)
      .then((cache) => cache.addAll(PRECACHE))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(
        keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;

  // Never interfere with non-GET (login, add/edit/delete, etc.)
  if (req.method !== 'GET') {
    return;
  }

  const url = new URL(req.url);

  // Page navigations: always try the network so logged-in data stays
  // fresh; only fall back to the cached offline page when truly offline.
  if (req.mode === 'navigate') {
    event.respondWith(
      fetch(req).catch(() => caches.match('/offline'))
    );
    return;
  }

  // Same-origin static assets: cache-first, then populate the cache.
  if (url.origin === self.location.origin && url.pathname.startsWith('/static/')) {
    event.respondWith(
      caches.match(req).then((cached) => {
        if (cached) {
          return cached;
        }
        return fetch(req).then((res) => {
          const copy = res.clone();
          caches.open(CACHE).then((cache) => cache.put(req, copy));
          return res;
        });
      })
    );
    return;
  }

  // Everything else (e.g. CDN libs): let the browser handle it normally.
});

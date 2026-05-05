// Service Worker pour Gestion d'Église CCR
// Gère le cache, les notifications offline et la synchronisation en arrière-plan

const CACHE_NAME = 'ccr-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/static/manifest.json',
  '/offline.html'
];

// Installation du service worker
self.addEventListener('install', event => {
  console.log('[Service Worker] Installation en cours...');
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log('[Service Worker] Cache ouvert:', CACHE_NAME);
      return cache.addAll(ASSETS_TO_CACHE).catch(err => {
        console.log('[Service Worker] Erreur lors de la mise en cache:', err);
        // Continuer même si certains fichiers ne peuvent pas être cachés
      });
    })
  );
  self.skipWaiting();
});

// Activation du service worker
self.addEventListener('activate', event => {
  console.log('[Service Worker] Activation en cours...');
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('[Service Worker] Suppression ancien cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Interception des requêtes
self.addEventListener('fetch', event => {
  // Ne mettre en cache que les requêtes GET
  if (event.request.method !== 'GET') {
    return;
  }

  // Stratégie: Network First pour les données dynamiques, Cache First pour les assets
  if (event.request.url.includes('/api/') || 
      event.request.url.includes('/rapports/') ||
      event.request.url.includes('/membres/')) {
    // Network First: essayer le réseau d'abord
    event.respondWith(
      fetch(event.request)
        .then(response => {
          // Mettre en cache les réponses réussies
          if (response.status === 200) {
            const responseToCache = response.clone();
            caches.open(CACHE_NAME).then(cache => {
              cache.put(event.request, responseToCache);
            });
          }
          return response;
        })
        .catch(err => {
          console.log('[Service Worker] Erreur fetch:', err);
          // Retourner depuis le cache en cas d'erreur
          return caches.match(event.request).then(cachedResponse => {
            if (cachedResponse) {
              return cachedResponse;
            }
            // Retourner une page offline si disponible
            if (event.request.mode === 'navigate') {
              return caches.match('/offline.html');
            }
            return new Response('Ressource non disponible', {
              status: 503,
              statusText: 'Service Unavailable',
              headers: new Headers({
                'Content-Type': 'text/plain'
              })
            });
          });
        })
    );
  } else {
    // Cache First pour les assets statiques
    event.respondWith(
      caches.match(event.request).then(response => {
        if (response) {
          return response;
        }
        return fetch(event.request).then(response => {
          if (!response || response.status !== 200 || response.type === 'error') {
            return response;
          }
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, responseToCache);
          });
          return response;
        }).catch(err => {
          console.log('[Service Worker] Erreur fetch asset:', err);
          return new Response('Ressource non disponible', {
            status: 503,
            statusText: 'Service Unavailable'
          });
        });
      })
    );
  }
});

// Gestion des messages depuis les clients
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  if (event.data && event.data.type === 'CLEAR_CACHE') {
    caches.delete(CACHE_NAME);
  }
});

// Synchronisation en arrière-plan (si supportée)
self.addEventListener('sync', event => {
  if (event.tag === 'sync-data') {
    event.waitUntil(
      // Implémenter la logique de synchronisation ici
      Promise.resolve()
    );
  }
});

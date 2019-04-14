var staticCacheName = 'achieng-cache-v6'; //name of our cache

self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(staticCacheName).then(function(cache) {
            return cache.addAll([
                '/',
                '/static/css/style.css',
                '/static/images/favicon.ico',
                '/static/js/main.js',
                'https://use.fontawesome.com/releases/v5.5.0/css/all.css',
                'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.12.0/highlight.min.js',
                'https://code.jquery.com/jquery-3.2.1.slim.min.js',
                'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.12.0/styles/atelier-forest-light.min.css',
            ]);
        })
    );
});
/* Deleting old cache */
self.addEventListener('activate', function(event) {
    event.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(
                cacheNames.filter(function(cacheName) {
                    return cacheName.startsWith('achieng-') && //do not delete caches from other appthat miggt be running on the same origin
                        cacheName != staticCacheName;
                }).map(function(cacheName) {
                    return caches.delete(cacheName);
                })
            );
        })

    );
});

// cache faling back to network
self.addEventListener('fetch', function(event) {
    event.respondWith(
      caches.match(event.request).then(function(response) {
        return response || fetch(event.request);
      })
    );
  });


//   if (e.request.cache === 'only-if-cached' && e.request.mode !== 'same-origin') {
//     return;
//   }
//
self.addEventListener('message', function(event) {
  if (event.data.action === 'skipWaiting') {
    self.skipWaiting();
  }
});

/* self.addEventListener('fetch', function(event) {
    event.respondWith(
      caches.open(cacheName).then(function(cache) {
        return cache.match(event.request).then(function(response) {
          var fetchPromise = fetch(event.request).then(function(networkResponse) {
            cache.put(event.request, networkResponse.clone());
            return networkResponse;
          })
          return response || fetchPromise;
        })
      })
    );
  }); */


  
  
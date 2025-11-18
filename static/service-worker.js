/*
 * Legend AI Dashboard - Service Worker
 * Offline caching and performance optimization
 */

const CACHE_NAME = 'legend-ai-v1';
const RUNTIME_CACHE = 'legend-ai-runtime-v1';

// Assets to cache on install
const STATIC_ASSETS = [
    '/',
    '/dashboard',
    '/static/css/cyberpunk-design-system.css',
    '/static/css/dashboard.css',
    '/static/css/mobile.css',
    '/static/js/dashboard.js',
    '/static/js/mobile.js',
    '/static/js/tv-widgets.js',
];

// API endpoints to cache with network-first strategy
const API_ENDPOINTS = [
    '/api/patterns/analyze',
    '/api/universe/scan',
    '/api/watchlist/list',
    '/api/markets/breadth',
    '/api/top-setups/list',
];

// Install event - cache static assets
self.addEventListener('install', (event) => {
    console.log('[ServiceWorker] Installing...');

    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('[ServiceWorker] Caching static assets');
                return cache.addAll(STATIC_ASSETS);
            })
            .then(() => {
                console.log('[ServiceWorker] Installed successfully');
                return self.skipWaiting();
            })
            .catch((error) => {
                console.error('[ServiceWorker] Installation failed:', error);
            })
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
    console.log('[ServiceWorker] Activating...');

    event.waitUntil(
        caches.keys()
            .then((cacheNames) => {
                return Promise.all(
                    cacheNames.map((cacheName) => {
                        if (cacheName !== CACHE_NAME && cacheName !== RUNTIME_CACHE) {
                            console.log('[ServiceWorker] Deleting old cache:', cacheName);
                            return caches.delete(cacheName);
                        }
                    })
                );
            })
            .then(() => {
                console.log('[ServiceWorker] Activated successfully');
                return self.clients.claim();
            })
    );
});

// Fetch event - implement caching strategies
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);

    // Skip cross-origin requests
    if (url.origin !== location.origin) {
        return;
    }

    // API requests - Network first, fallback to cache
    if (isApiRequest(url.pathname)) {
        event.respondWith(networkFirstStrategy(request));
        return;
    }

    // Static assets - Cache first, fallback to network
    if (isStaticAsset(url.pathname)) {
        event.respondWith(cacheFirstStrategy(request));
        return;
    }

    // HTML pages - Network first with cache fallback
    if (request.mode === 'navigate') {
        event.respondWith(networkFirstStrategy(request));
        return;
    }

    // Default strategy - Network first
    event.respondWith(networkFirstStrategy(request));
});

// ============================================================================
// Caching Strategies
// ============================================================================

/**
 * Cache First Strategy
 * Good for static assets that rarely change
 */
async function cacheFirstStrategy(request) {
    try {
        const cache = await caches.open(CACHE_NAME);
        const cachedResponse = await cache.match(request);

        if (cachedResponse) {
            console.log('[ServiceWorker] Cache hit:', request.url);
            return cachedResponse;
        }

        console.log('[ServiceWorker] Cache miss, fetching:', request.url);
        const networkResponse = await fetch(request);

        // Cache successful responses
        if (networkResponse.ok) {
            cache.put(request, networkResponse.clone());
        }

        return networkResponse;
    } catch (error) {
        console.error('[ServiceWorker] Cache first failed:', error);
        return new Response('Offline', { status: 503 });
    }
}

/**
 * Network First Strategy
 * Good for API requests and dynamic content
 */
async function networkFirstStrategy(request) {
    try {
        const networkResponse = await fetch(request);

        // Cache successful responses
        if (networkResponse.ok) {
            const cache = await caches.open(RUNTIME_CACHE);
            cache.put(request, networkResponse.clone());
        }

        return networkResponse;
    } catch (error) {
        console.log('[ServiceWorker] Network failed, trying cache:', request.url);

        const cache = await caches.open(RUNTIME_CACHE);
        const cachedResponse = await cache.match(request);

        if (cachedResponse) {
            console.log('[ServiceWorker] Serving from cache:', request.url);
            return cachedResponse;
        }

        // Return offline page for navigation requests
        if (request.mode === 'navigate') {
            return caches.match('/dashboard') || new Response('Offline', {
                status: 503,
                statusText: 'Service Unavailable',
            });
        }

        return new Response('Offline', { status: 503 });
    }
}

/**
 * Stale While Revalidate Strategy
 * Good for images and charts that can be shown stale
 */
async function staleWhileRevalidateStrategy(request) {
    const cache = await caches.open(RUNTIME_CACHE);
    const cachedResponse = await cache.match(request);

    const fetchPromise = fetch(request).then((networkResponse) => {
        if (networkResponse.ok) {
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    });

    return cachedResponse || fetchPromise;
}

// ============================================================================
// Helper Functions
// ============================================================================

function isApiRequest(pathname) {
    return pathname.startsWith('/api/');
}

function isStaticAsset(pathname) {
    return pathname.startsWith('/static/') ||
           pathname.endsWith('.css') ||
           pathname.endsWith('.js') ||
           pathname.endsWith('.png') ||
           pathname.endsWith('.jpg') ||
           pathname.endsWith('.jpeg') ||
           pathname.endsWith('.svg') ||
           pathname.endsWith('.woff') ||
           pathname.endsWith('.woff2');
}

function isChartImage(pathname) {
    return pathname.startsWith('/api/charts/');
}

// ============================================================================
// Background Sync (for offline actions)
// ============================================================================

self.addEventListener('sync', (event) => {
    console.log('[ServiceWorker] Background sync:', event.tag);

    if (event.tag === 'sync-watchlist') {
        event.waitUntil(syncWatchlist());
    }

    if (event.tag === 'sync-scans') {
        event.waitUntil(syncScans());
    }
});

async function syncWatchlist() {
    try {
        // Get pending watchlist updates from IndexedDB
        const pendingUpdates = await getPendingWatchlistUpdates();

        for (const update of pendingUpdates) {
            const response = await fetch('/api/watchlist/add', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(update),
            });

            if (response.ok) {
                await removePendingUpdate(update.id);
            }
        }

        console.log('[ServiceWorker] Watchlist synced successfully');
    } catch (error) {
        console.error('[ServiceWorker] Watchlist sync failed:', error);
        throw error;
    }
}

async function syncScans() {
    try {
        // Get pending scans from IndexedDB
        const pendingScans = await getPendingScans();

        for (const scan of pendingScans) {
            const response = await fetch('/api/patterns/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(scan),
            });

            if (response.ok) {
                await removePendingScan(scan.id);
            }
        }

        console.log('[ServiceWorker] Scans synced successfully');
    } catch (error) {
        console.error('[ServiceWorker] Scans sync failed:', error);
        throw error;
    }
}

// Placeholder functions for IndexedDB operations
async function getPendingWatchlistUpdates() {
    // In a real implementation, this would query IndexedDB
    return [];
}

async function removePendingUpdate(id) {
    // In a real implementation, this would remove from IndexedDB
}

async function getPendingScans() {
    // In a real implementation, this would query IndexedDB
    return [];
}

async function removePendingScan(id) {
    // In a real implementation, this would remove from IndexedDB
}

// ============================================================================
// Push Notifications (for alerts)
// ============================================================================

self.addEventListener('push', (event) => {
    console.log('[ServiceWorker] Push notification received');

    const options = {
        body: event.data ? event.data.text() : 'New pattern alert!',
        icon: '/static/images/icon-192.png',
        badge: '/static/images/badge-72.png',
        vibrate: [200, 100, 200],
        data: {
            dateOfArrival: Date.now(),
            primaryKey: 1,
        },
        actions: [
            {
                action: 'view',
                title: 'View Alert',
            },
            {
                action: 'close',
                title: 'Close',
            },
        ],
    };

    event.waitUntil(
        self.registration.showNotification('Legend AI', options)
    );
});

self.addEventListener('notificationclick', (event) => {
    console.log('[ServiceWorker] Notification clicked:', event.action);

    event.notification.close();

    if (event.action === 'view') {
        event.waitUntil(
            clients.openWindow('/dashboard')
        );
    }
});

// ============================================================================
// Message Handler (for cache updates from main thread)
// ============================================================================

self.addEventListener('message', (event) => {
    console.log('[ServiceWorker] Message received:', event.data);

    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }

    if (event.data && event.data.type === 'CLEAR_CACHE') {
        event.waitUntil(
            caches.keys().then((cacheNames) => {
                return Promise.all(
                    cacheNames.map((cacheName) => caches.delete(cacheName))
                );
            })
        );
    }

    if (event.data && event.data.type === 'CACHE_URLS') {
        event.waitUntil(
            caches.open(RUNTIME_CACHE).then((cache) => {
                return cache.addAll(event.data.urls);
            })
        );
    }
});

console.log('[ServiceWorker] Service worker script loaded');

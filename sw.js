/**
 * sw.js — AI Crawler Cache-Busting & Encoding Normalization Service Worker
 * 改善文書c Section 7: AIクローラー向けL7ルーティングのキャッシュ汚染バグとエンコーディング不一致の予防
 *
 * DESIGN:
 * - Intercepts requests for llms.txt and llms-full.txt
 * - Forces network-fresh fetch (cache bypass) for AI crawler bot User-Agents
 * - Ensures UTF-8 BOM is present for crawlers that may misdetect encoding
 * - Non-destructive: passes all other requests through unchanged
 *
 * NOTE: This SW is registered with { scope: './' } to avoid affecting
 *       other sites on the same origin (GitHub Pages shared origin).
 */

'use strict';

const CACHE_NAME = 'portfolio-aio-v1';
const AIO_FILES = ['/portfolio/llms.txt', '/portfolio/llms-full.txt'];

// Known AI crawler UA substrings (conservative list — false positives are harmless)
const BOT_UA_PATTERNS = [
    'gptbot', 'chatgpt', 'claudebot', 'anthropic', 'perplexity',
    'bingbot', 'googlebot', 'baiduspider', 'duckduckbot', 'applebot',
    'ia_archiver', 'archive.org', 'semrushbot', 'ahrefs', 'mj12bot',
    'python-requests', 'curl/', 'wget/', 'node-fetch', 'axios', 'scrapy',
    'llm', 'crawler', 'spider', 'bot'
];

function isBotRequest(request) {
    const ua = (request.headers.get('User-Agent') || '').toLowerCase();
    if (!ua) { return false; }
    return BOT_UA_PATTERNS.some(function(pattern) { return ua.includes(pattern); });
}

function isAIOFile(url) {
    return AIO_FILES.some(function(path) { return url.pathname.endsWith(path.split('/').pop()); });
}

/**
 * Ensure a text Response has a UTF-8 BOM for crawlers that misdetect encoding.
 * The original file is NOT modified — only the network response in transit.
 */
async function ensureUtf8Bom(response) {
    try {
        const buf = await response.arrayBuffer();
        const view = new Uint8Array(buf);
        // Check if BOM already present (EF BB BF)
        if (view[0] === 0xEF && view[1] === 0xBB && view[2] === 0xBF) {
            return new Response(buf, {
                status: response.status,
                headers: { 'Content-Type': 'text/plain; charset=utf-8' }
            });
        }
        // Prepend BOM
        const withBom = new Uint8Array(buf.byteLength + 3);
        withBom[0] = 0xEF; withBom[1] = 0xBB; withBom[2] = 0xBF;
        withBom.set(view, 3);
        return new Response(withBom.buffer, {
            status: response.status,
            headers: { 'Content-Type': 'text/plain; charset=utf-8' }
        });
    } catch {
        return response;
    }
}

self.addEventListener('install', function(event) {
    self.skipWaiting();
});

self.addEventListener('activate', function(event) {
    event.waitUntil(
        caches.keys().then(function(keys) {
            return Promise.all(
                keys.filter(function(k) { return k !== CACHE_NAME; })
                    .map(function(k) { return caches.delete(k); })
            );
        }).then(function() { return self.clients.claim(); })
    );
});

self.addEventListener('fetch', function(event) {
    const request = event.request;
    const url = new URL(request.url);

    // Only intercept AIO routing files
    if (!isAIOFile(url)) { return; }

    // For bot/crawler requests: bypass cache entirely, force fresh network fetch
    if (isBotRequest(request)) {
        event.respondWith(
            fetch(request, { cache: 'no-store' })
                .then(function(response) { return ensureUtf8Bom(response); })
                .catch(function() {
                    // Network failure — serve from cache as fallback
                    return caches.match(request);
                })
        );
        return;
    }

    // For human browsers: stale-while-revalidate for AIO files
    event.respondWith(
        caches.open(CACHE_NAME).then(function(cache) {
            return cache.match(request).then(function(cached) {
                const networkFetch = fetch(request).then(function(response) {
                    if (response && response.ok) {
                        cache.put(request, response.clone());
                    }
                    return response;
                });
                return cached || networkFetch;
            });
        })
    );
});

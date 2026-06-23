/* eslint-disable no-implicit-globals -- service worker: top-level function declarations are intentional and must be registered synchronously during the SW's initial evaluation. Wrapping them in an IIFE would not change behaviour but would obscure the conventional service-worker structure. */
/**
 * sw.js — Browser-Side AIO Cache Normalization & Encoding Normalization Service Worker
 * 改善文書c Section 7: AIクローラー向けL7ルーティングのキャッシュ汚染バグとエンコーディング不一致の予防
 *
 * WP-12 Claim Calibration:
 * This Service Worker provides cache normalization for BROWSER environments that register
 * and execute it (e.g., Chrome, Firefox, Safari when visiting the portfolio directly).
 * AI crawlers that do not execute Service Workers will NOT be affected by this script.
 * Primary AIO discoverability must remain available without SW execution via static files:
 *   index.html, llms.txt, llms-full.txt, robots.txt, sitemap.xml, and .well-known/ endpoints.
 * This SW is an enhancement layer, not the primary AIO delivery mechanism.
 *
 * SCOPE (implementation-accurate):
 * This Service Worker only normalizes browser-context delivery for:
 * - /portfolio/llms.txt
 * - /portfolio/llms-full.txt
 *
 * Other AIO resources (.well-known/, aio-manifest.json, AI2AI.md, binary assets) remain
 * statically discoverable and are intentionally NOT intercepted by this SW.
 * Do not expand this interception list unless there is a verified delivery issue.
 *
 * DESIGN:
 * - Intercepts requests for llms.txt and llms-full.txt in browser context only
 * - Forces network-fresh fetch (cache bypass) for AI crawler bot User-Agents
 * - Ensures UTF-8 BOM is present for environments that may misdetect encoding
 * - Non-destructive: passes all other requests through unchanged
 *
 * NOTE: This SW is registered with { scope: './' } to avoid affecting
 *       other sites on the same origin (GitHub Pages shared origin).
 */

'use strict';

const CACHE_NAME = 'portfolio-aio-v74';
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

function normalizePath(pathname) {
    // decodeURIComponent は不正な % シーケンス (例 '/portfolio/%' や '/portfolio/%zz') で URIError を
    // throw する。本 SW は fetch ハンドラで全リクエストの pathname を normalizePath→isAIOFile に
    // 通すため、ガードしないと不正 URL リクエストのたびに SW 内 uncaught error になる。decode 失敗時は
    // raw pathname にフォールバックする (その URL は AIO_FILES と一致しない＝素通し＝従来挙動と等価)。
    let decoded;
    try {
        decoded = decodeURIComponent(pathname);
    } catch {
        decoded = pathname;
    }
    return decoded.replace(/\/+$/, '');
}

function isAIOFile(url) {
    const pathname = normalizePath(url.pathname);
    return AIO_FILES.includes(pathname);
}

/**
 * Clone response headers, overriding only Content-Type.
 * Preserves ETag, Cache-Control, Last-Modified and other metadata from the origin.
 */
function cloneTextHeaders(response) {
    const headers = new Headers(response.headers);
    headers.set('Content-Type', 'text/plain; charset=utf-8');
    return headers;
}

/**
 * Ensure a text Response has a UTF-8 BOM for crawlers that misdetect encoding.
 * The original file is NOT modified — only the network response in transit.
 * Original response headers (ETag, Cache-Control, etc.) are preserved.
 */
async function ensureUtf8Bom(response) {
    try {
        const buf = await response.arrayBuffer();
        const view = new Uint8Array(buf);
        // Check if BOM already present (EF BB BF)
        if (view[0] === 0xEF && view[1] === 0xBB && view[2] === 0xBF) {
            return new Response(buf, {
                status: response.status,
                statusText: response.statusText,
                headers: cloneTextHeaders(response)
            });
        }
        // Prepend BOM
        const withBom = new Uint8Array(buf.byteLength + 3);
        withBom[0] = 0xEF; withBom[1] = 0xBB; withBom[2] = 0xBF;
        withBom.set(view, 3);
        return new Response(withBom.buffer, {
            status: response.status,
            statusText: response.statusText,
            headers: cloneTextHeaders(response)
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
                // WHY .catch: stale-while-revalidate で cached を即返した場合、networkFetch は
                // バックグラウンド revalidation として宙吊りになる。オフライン等で reject すると
                // SW 内で unhandledrejection になるため、cached へフォールバックして握りつぶす
                // (cached が無い初回オフラインでは undefined → respondWith がネットワークエラーを
                // 表示=従来挙動と等価)。online 時の挙動は不変。
                const networkFetch = fetch(request).then(function(response) {
                    if (response && response.ok) {
                        // cache.put は fire-and-forget。quota 超過等で reject すると SW 内で
                        // unhandledrejection になる (#84 と同 class) ため .catch で握りつぶす。
                        cache.put(request, response.clone()).catch(function() { /* quota 等は無視 */ });
                    }
                    return response;
                }).catch(function() { return cached; });
                return cached || networkFetch;
            });
        })
    );
});

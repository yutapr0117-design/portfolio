/**
 * router.js — Hash-based SPA ルーター
 *
 * @fileoverview v80+ Stage 5: main.js から抽出したルーティングモジュール。
 * `location.hash` を正規化し、ルート名・params・query を解決する。
 * hashchange イベントを購読してコールバックを非同期で通知する。
 *
 * export:
 *   Router  — ルーターシングルトン { getRoute, navigate, replaceSilently, subscribe, parse }
 *
 * 不変条件:
 *   - 本モジュールは葉（ローカル ESM import ゼロ）。ブラウザ API のみ使用。
 *   - navigate() が受け取るパスは '#' を含まないこと（含む場合は先頭 '#' を除去して継続）。
 *     NOTE: 元コードの CONSTANTS.DEBUG 依存（デバッグモード時に throw）は
 *     production では dead code（DEBUG = false 固定）のため本モジュールでは削除済み。
 *     デバッグ時は呼び出し側で path の検証を行うこと。
 *   - hashchange ハンドラは遷移ロックを持つ（同時多重発火時は最終ルートのみ適用）。
 */

// ===== Router =====
export const Router = (() => {
    let currentRoute = _parseRoute();
    let handlers = [];

    function _parseRoute() {
        const hash = location.hash || '';
        const raw = hash.startsWith('#/') ? hash.slice(2) : '';
        const [pathPart, queryPart] = raw.split('?');
        const clean = (pathPart || '').replace(/^\/+/, '');
        const parts = clean ? clean.split('/').filter(Boolean) : [];
        const params = new URLSearchParams(queryPart || '');

        const route = { name: 'home', params: {}, query: {} };
        params.forEach((v, k) => route.query[k] = v);

        if (parts.length === 0) { return route; }

        switch (parts[0]) {
            case 'projects':
                if (parts.length === 1) {
                    route.name = 'projects';
                    route.query.q = params.get('q') || '';
                    route.query.cat = params.get('cat') || '';
                } else {
                    route.name = 'project-detail';
                    route.params.slug = parts[1];
                }
                break;
            case 'apps':
                if (parts.length === 1) {
                    route.name = 'apps';
                } else {
                    const app = parts[1];
                    route.name = ['task', 'todo', 'pomodoro', 'ai', 'notes'].includes(app)
                        ? `app-${app}`
                        : 'not-found';
                }
                break;
            case 'settings':
                route.name = 'settings';
                break;
            case 'about':
                route.name = 'about';
                break;
            case 'resume':
                route.name = 'resume';
                break;
            case 'contact':
                route.name = 'contact';
                break;
            case 'quiz':
                route.name = 'quiz';
                break;
            case 'hiring-risk':
                route.name = 'hiring-risk';
                break;
            case 'ai-knowhow':
                route.name = 'ai-knowhow';
                break;
            case 'role-split':
                route.name = 'role-split';
                break;
            default:
                route.name = 'not-found';
        }

        return route;
    }

    function navigate(path) {
        // Guard: path should not contain '#'. If it does, strip ONLY a leading hash to prevent double-hash (e.g. #/#!/something).
        if (typeof path === 'string' && path.includes('#')) {
            path = path.replace(/^#+/, ''); // strip leading '#' only
            // NOTE: 元コードは CONSTANTS.DEBUG 時に throw していたが、production では
            // dead code（DEBUG = false）のため本モジュールでは削除。呼び出し側で検証すること。
        }
        location.hash = '#/' + (path || '');
    }

    // [FIX] hashchangeイベントを発火させずにURLを静かに書き換える（Focus Loss防止）
    function replaceSilently(path) {
        if (typeof path === 'string' && path.includes('#')) {
            path = path.replace(/^#+/, '');
        }
        const newUrl = location.pathname + location.search + '#/' + (path || '');
        history.replaceState(null, '', newUrl);
        // § Agentic State Notification: URL変更時にdata-ai-stateを同期
        try {
            document.body.setAttribute('data-ai-state', JSON.stringify({
                route: path || 'home',
                filter: path || '',
                loading: false
            }));
        } catch (_) {}
    }

    function subscribe(callback) {
        handlers.push(callback);
        return () => {
            handlers = handlers.filter(h => h !== callback);
        };
    }

    // 改善文書b 3.1 / 改善文書c 2: Transition lock and async queue to prevent Race Conditions.
    // If hashchange fires while a transition is in flight, the new route is
    // queued and replayed after the current transition completes — preventing
    // DOM corruption from concurrent startViewTransition calls.
    let _routerTransitioning = false;
    let _routerPendingHash = null;

    async function _dispatchRouteChange() {
        if (_routerTransitioning) {
            _routerPendingHash = window.location.hash;
            return;
        }
        _routerTransitioning = true;
        try {
            const route = _parseRoute();
            currentRoute = route;
            const handlersCopy = handlers.slice();
            for (const h of handlersCopy) {
                try { await Promise.resolve(h(route)); } catch (e) { /* guard */ }
            }
        } finally {
            _routerTransitioning = false;
            // Replay any route change that arrived while we were busy
            if (_routerPendingHash !== null && _routerPendingHash !== window.location.hash) {
                _routerPendingHash = null;
                // Re-trigger: _dispatchRouteChange re-reads the live window.location.hash,
                // so the queued value itself is not needed — only the fact that a change arrived.
                _dispatchRouteChange();
            } else {
                _routerPendingHash = null;
            }
        }
    }

    window.addEventListener('hashchange', _dispatchRouteChange);

    return {
        getRoute: () => currentRoute,
        navigate,
        replaceSilently,
        subscribe,
        parse: _parseRoute
    };
})();

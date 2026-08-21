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

    // [UX] 直近の「プロジェクト一覧」ルートを query 込みで覚えておく。
    //   詳細ページの「← 一覧に戻る」は Router.navigate('projects') とハードコードされており、
    //   絞り込み (?q= / ?cat=) を落として全件へ戻していた。ブラウザの「戻る」は履歴に残った
    //   query 付き URL へ復帰するため **同じ操作なのに結果が違う**という不整合になっていた
    //   (実測: 1 件に絞った状態で詳細を開き in-page back → 18 件の全件表示に戻る)。
    //   `getLastListPath()` が「戻り先」を単一ソースとして提供する。
    let _lastListPath = 'projects';

    function _rememberListPath() {
        const raw = (location.hash || '').replace(/^#\/?/, '');
        if (raw === 'projects' || raw.startsWith('projects?')) { _lastListPath = raw; }
    }
    _rememberListPath();
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
                    // decodeURIComponent が必要な理由: ブラウザが非 ASCII 文字 (日本語等) を
                    // URL エンコードして location.hash に返すため、slugify で生成した生 slug
                    // ('データ分析') と parts[1] ('%E3%83...' 形式) が不一致になる。
                    // SW の normalizePath と同じパターンで try/catch を使う。
                    try {
                        route.params.slug = decodeURIComponent(parts[1]);
                    } catch (_) {
                        route.params.slug = parts[1];
                    }
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

    // [FIX] agentic surface (`body[data-ai-state]`) の `filter` の **単一ソース**。
    //   書き手は 3 箇所 (ここと main.js の描画前/描画後) あり、従来は render 側が `''` を
    //   ハードコードしていたため filter は情報を運べていなかった。URL を唯一の真値にする。
    //   実測と壊れ方は e2e/aio-meta.spec.js の 7.1c を読め。
    function getFilterString() {
        const raw = (location.hash || '').replace(/^#\/?/, '');
        const i = raw.indexOf('?');
        return i === -1 ? '' : raw.slice(i + 1);
    }

    // [FIX] hashchangeイベントを発火させずにURLを静かに書き換える（Focus Loss防止）
    function replaceSilently(path) {
        if (typeof path === 'string' && path.includes('#')) {
            path = path.replace(/^#+/, '');
        }
        const newUrl = location.pathname + location.search + '#/' + (path || '');
        history.replaceState(null, '', newUrl);
        _rememberListPath();
        // § Agentic State Notification: URL変更時にdata-ai-stateを同期
        // [FIX] render パス (main.js) は route.name (正規化済みルート名 'projects' 等) を route へ
        // 公開するが、旧 silent 実装は生 path ('projects?q=foo&cat=bar') を route へ入れており、
        // projects フィルタ操作後に agentic surface の route が render パスと drift していた。
        // replaceState 済みの location.hash を _parseRoute() で同じ解決に通し route 名を一致させ、
        // query 部だけを filter へ入れる (旧 filter は全 path が入る誤値で render パスは常に空だった)。
        try {
            const _r = _parseRoute();
            // [FIX] silent URL 更新後も getRoute() が URL と一致するよう currentRoute も同期する。
            // 更新しないと currentRoute は直近 hashchange の値 (query.q='') のまま stale になり、
            // その後の full re-render (State.subscribe(render) を駆動する notify() — 例: cross-tab
            // storage sync (state.js) / 任意の State.update) が _renderCore→getRoute().query を
            // stale で読み、ProjectsPage が q='' で再描画されて検索フィルタが消える一方 URL は
            // ?q=.. のまま残る desync バグになる (data-ai-state drift #765 と同根の内部 route state 版)。
            // notify() は呼ばない (silent 契約=再描画しないを維持)。次の再描画が正しい route を読むだけ。
            currentRoute = _r;
            document.body.setAttribute('data-ai-state', JSON.stringify({
                route: _r.name || 'home',
                filter: getFilterString(),
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
            _rememberListPath();
            const handlersCopy = handlers.slice();
            for (const h of handlersCopy) {
                try { await Promise.resolve(h(route)); } catch (e) { /* guard */ }
            }
        } finally {
            _routerTransitioning = false;
            // Replay any route change that arrived while we were busy.
            // [FIX] 判定は「pending が到着したか (!== null)」だけで行う。旧実装は
            // `&& _routerPendingHash !== window.location.hash` を併用していたが、これは
            // rapid double-nav の常見ケース (transition 中に 1 度だけ B へ遷移し以後動かない) で
            // pending===live(B) となり replay を skip し、処理済みは遷移前の旧ルート (A) のまま
            // ＝ URL=B / 表示=A の desync を生むバグだった。_dispatchRouteChange は live hash を
            // 再読するため、pending の値自体は不要で「変化が到着した事実」だけが replay の条件
            // (この関数のコメントが元から述べていた正しい意図に一致させる)。
            if (_routerPendingHash !== null) {
                _routerPendingHash = null;
                _dispatchRouteChange();
            }
        }
    }

    window.addEventListener('hashchange', _dispatchRouteChange);

    return {
        getRoute: () => currentRoute,
        navigate,
        replaceSilently,
        subscribe,
        parse: _parseRoute,
        getFilterString,
        // 詳細ページの「一覧に戻る」用。絞り込みを保持したまま一覧へ戻すための単一ソース。
        getLastListPath: () => _lastListPath
    };
})();

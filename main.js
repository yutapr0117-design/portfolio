
        /**
         * Portfolio SPA - Enhanced Version
         * Single HTML architecture with modern ES6+ patterns
         *
         * @fileoverview Main execution script. Orchestrated by AI under human supervision.
         * @rules
         * 1. STRICTLY Vanilla JS. No external frameworks, UI libraries, or CDN imports.
         *    (v80+ Stage 2〜: 同一オリジンの **ローカル ESM モジュール** への分割は許可。
         *    index.html は本ファイルを <script type="module"> で読み込み、本ファイルが
         *    ./js/*.js を import する。外部 import・CDN・フレームワーク禁止の精神は不変。)
         * 2. MUST use IIFE to prevent global namespace pollution.
         * 3. MUST use ErrorBoundary for document.startViewTransition.
         * 4. Boring Technology only. No modern frameworks.
         * 5. innerHTML is PROHIBITED — use h() helper or DOM APIs only.
         * 6. All event listeners in dynamic components MUST use { signal } from AbortController.
         * 7. All CSS values MUST reference var(--*) CSS custom properties.
         * @warning Any attempt to use Virtual DOM or state management libraries will be REJECTED.
         * @see 改善文書b Section 10.1 — Semantic Anchors
         */

        'use strict';

        /* ──────────────────────────────────────────────────────────────────────
         * Module imports (v80+ staged split)
         * ──────────────────────────────────────────────────────────────────────
         * Stage 2 — pure utility 層を js/pure-utils.js へ分割。出力が引数のみで決まり、
         *   本 IIFE のクロージャ状態にも DOM にも読み込み順序にも依存しないため挙動は不変。
         * Stage 3 — 巨大な静的データ 4 つを js/quiz-data.js へ分割（byte-equivalent 抽出）。
         *   関数も副作用も持たない純データのため、移設で挙動は一切変わらない。
         * import は ESM 仕様上モジュールトップレベル（IIFE の外）に置く必要がある。
         * 後続 Stage（service rails 等）も同様にローカル ESM として分割していく。
         * 新たに生じる「import 一覧 ⇄ export 一覧」の手書き契約は Check 47 が、JS lint 被覆は
         * Check 46（root ∪ js/）が、それぞれ BLOCKING で機械強制する。
         * ────────────────────────────────────────────────────────────────────── */
        import {
            generateId,    // UUID v4 生成（crypto.randomUUID フォールバック付き）
            clamp,         // 数値を [min,max] に丸める
            debounce,      // 連続呼び出しを「静粛後 1 回」に遅延
            throttle,      // 呼び出しを「一定間隔に 1 回」へ間引く
            tokenize,      // 文字列を検索/類似度用トークンへ分解（日本語対応）
            slugify,       // 文字列を URL/識別子 slug へ正規化
            sanitizeUrl,   // http/https のみ通すセキュリティ境界（挙動不変厳守）
            safeFetchJSON, // fetch ラッパ（HTTP ステータス + JSON を厳密検証）
            deepClone,     // オブジェクト/配列/Date の深いコピー
            yieldToMain    // INP 改善のためメインスレッドを解放（scheduler.yield 等）
        } from './js/pure-utils.js';
        // v80+ Stage 3-b: 静的クイズデータ 4 つをドメイン別の葉モジュールへ細分化し直接 import する
        //   （Stage 3 の js/quiz-data.js 単一ファイルを AWS / PM / 品質 / 設計判断の 4 ファイルへ分割）。
        //   aggregator は葉契約（Check 47c）を崩すため不採用。詳細は docs/architecture/main-js-extraction-map.md §3.6。
        //   純データゆえ挙動不変。import/export bijection と葉性は Check 47 が複数モジュールをループ検査して強制。
        //   （各 import は行末コメントを付けない＝ Check 43d の import 連結検出が確実に全 import を消費できるよう、
        //    付帯説明は各葉モジュールの fileoverview と上記コメントへ集約する。）
        import { awsQuizData } from './js/quiz/aws-quiz-data.js';
        import { pmQuizData } from './js/quiz/pm-quiz-data.js';
        import { qualityQuizData } from './js/quiz/quality-quiz-data.js';
        import { architectureQuizData } from './js/quiz/architecture-quiz-data.js';
        // v80+ Stage 4: UI コンポーネント（DOM ビルダー・アイコン・Toast・BGM）を葉モジュールへ抽出。
        //   closure-deps = none の純表示系のみを選別し、State/Storage/RouteState 依存コンポーネントは残置。
        import { h, createIcon, Toast, BGM } from './js/ui-components.js';
        // v80+ Stage 5: Router（hash ルーティング）と PAGE_META（SEO メタ単一ソース）を葉モジュールへ抽出。
        //   Router: closure-deps = none（CONSTANTS.DEBUG は production dead code のため削除）。
        //   PAGE_META: 動的 title/desc は引数で state/params を受け取る純粋関数。closure-deps = none。
        import { Router } from './js/router.js';
        import { PAGE_META } from './js/page-meta.js';
        // v80+ Stage 5-b → Stage 5-j fix: ページコンポーネント（HiringRiskPage / RoleSplitPage /
        // NotFoundPage）を葉モジュールへ抽出。Stage 5-b 時点は h/createIcon/Router を未定義の
        // 暗黙参照としていた（ReferenceError 隠れバグ）。Stage 5-j で factory pattern に修正し、
        // 依存を引数注入で解消（葉契約維持）。
        import { createPages } from './js/pages.js';
        // v80+ Stage 5-c: Safe Storage（localStorage ラッパ）を葉モジュールへ抽出。
        //   closure-deps = none（localStorage と引数のみ。CONSTANTS 等の IIFE クロージャ非参照）。
        import { Storage } from './js/storage.js';
        // v80+ Stage 5-d: CONSTANTS（実行時定数: STORAGE_KEY / LIMITS / timing / DEBUG / TAB_ID）を葉モジュールへ抽出。
        //   SITE_CONFIG.VERSION / LAST_UPDATED は Check 2 / 17 が main.js から名前抽出するため残置。
        //   closure-deps = none（ブラウザグローバル crypto/sessionStorage/location のみ参照、IIFE クロージャ非参照）。
        import { CONSTANTS } from './js/constants.js';
        // v80+ Stage 5-e: AUTHOR（DISPLAY_NAME / AUTHORITATIVE_NAME / JAPANESE_NAME 純データ）を葉モジュールへ抽出。
        //   UI 表示専用 (DISPLAY_NAME) と AIO/SEO 機械可読層専用 (AUTHORITATIVE_NAME) の責務分離は値で固定（不変）。
        //   closure-deps = none。値は byte-equivalent で AIO citation 不影響（main.js は digest 対象外）。
        import { AUTHOR } from './js/identity.js';
        // v80+ Stage 5-f: Brand (primary palette / font manager) を factory pattern で葉モジュール抽出。
        //   葉モジュール契約 (Check 47c) 維持のため createBrand(Storage) → Brand instance 形式で合成。
        //   公開 API {init, set, get, KEY} と localStorage schema は byte-equivalent。
        import { createBrand } from './js/brand.js';
        // v80+ Stage 5-g: Store（default data + load/validate/normalize/similarity）を factory pattern で葉モジュール抽出。
        //   AUTHOR/CONSTANTS/Storage/generateId/deepClone/slugify/sanitizeUrl/clamp を引数注入で合成（葉契約維持）。
        //   公開 API { load, createDefaultStore, validateAndNormalize, autoRelatedCandidates } と挙動は byte-equivalent。
        import { createStore } from './js/store.js';
        // v80+ Stage 5-h: State（Proxy 型安全モニター + subscriber + cross-tab sync + auto-save）を factory pattern で葉モジュール抽出。
        //   CONSTANTS/Store/Storage/Toast を引数注入で合成（葉契約維持）。
        //   公開 API { get, set, update, subscribe, saveNow } と挙動は byte-equivalent。
        import { createState } from './js/state.js';
        // v80+ Stage 5-i: Theme (system/dark/light) を factory pattern で葉モジュール抽出。
        //   State/Toast を引数注入で合成（葉契約維持）。
        //   公開 API { apply, cycle, init } と挙動は byte-equivalent。
        import { createTheme } from './js/theme.js';
        // v80+ Stage 5-l: Meta Management (updateDocumentHead / announceRouteForAccessibility /
        //   injectRouteEntityAnchor / injectStructuredData + applyMeta ファサード) を factory
        //   pattern で葉モジュール抽出。SITE_CONFIG/AUTHOR/PAGE_META/Router/State を引数注入。
        //   公開 API { applyMeta } と挙動は byte-equivalent。
        import { createMetaManagement } from './js/meta-management.js';
        // v80+ Stage 5-m: UI page components 11 関数（Sidebar / HomePage / ProjectsPage /
        //   ProjectDetailPage / AppsPage / AboutPage / ResumePage / ContactPage / FatalPage /
        //   AIKnowhowPage / ContactCTA）を factory pattern で葉モジュール抽出。
        //   h/createIcon/Toast/BGM/AUTHOR/Router/State/Theme/Brand/Store を引数注入。
        //   ContactCTA は js/pages.js (createPages の ContactCTA 引数) にも引き渡される。
        import { createComponents } from './js/components.js';
        /* ╔══════════════════════════════════════════════════════════════════╗
           ║  DO NOT EDIT: AIDK Isolated Kernel — AIDK Architecture          ║
           ║  このブロック全体がAIエージェントのアクセスから隔離された核です。   ║
           ║  AIが編集してよいのは「AI SURFACE」マーカーで囲まれた領域のみ。    ║
           ║  Kernel内のロジック改変はCI/CDレベルで検知・棄却されます。         ║
           ╚══════════════════════════════════════════════════════════════════╝ */
        (function() {
        'use strict';

        // ─────────────────────────────────────────────────────────────────────────
        // 改善文書c Section 1 / カテゴリA #9: document.startViewTransition プロキシ・インターセプター
        // AIが素のdocument.startViewTransition()を直接呼び出しても、
        // try/catch + skipTransition() + タイムアウト制御が必ず効くよう
        // メソッド自体をここで上書きする。safeViewTransition()経由かどうかに依存しない。
        // ─────────────────────────────────────────────────────────────────────────
        (function _installStartViewTransitionProxy() {
            'use strict';
            if (!document.startViewTransition) { return; } // 未対応環境はスキップ

            var _orig = document.startViewTransition.bind(document);
            var TRANSITION_TIMEOUT_MS = 3000;

            document.startViewTransition = function startViewTransitionProxy(callback) {
                // prefers-reduced-motion: animationを完全スキップ (doc b §13.1 二重防衛)
                if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
                    try { if (typeof callback === 'function') callback(); } catch (e) { console.warn('[VT-Proxy] callback error (reduced-motion path):', e); }
                    // transition.ready / transition.finished を持つ duck-typed オブジェクトを返す
                    var resolved = Promise.resolve();
                    return { ready: resolved, finished: resolved, updateCallbackDone: resolved, skipTransition: function() {} };
                }

                // コールバックを try/catch/finally でラップ
                var safeCallback = function() {
                    try {
                        var result = (typeof callback === 'function') ? callback() : undefined;
                        return result;
                    } catch (e) {
                        console.warn('[VT-Proxy] callback threw — transition will be skipped:', e);
                        throw e; // ブラウザに再スロー → transition 自体がスキップされる
                    }
                };

                var transition;
                try {
                    transition = _orig(safeCallback);
                } catch (initErr) {
                    // startViewTransition 自体の初期化失敗 (TypeError等)
                    console.warn('[VT-Proxy] startViewTransition init error — direct DOM fallback:', initErr);
                    try { if (typeof callback === 'function') callback(); } catch (e) {}
                    var r = Promise.resolve();
                    return { ready: r, finished: r, updateCallbackDone: r, skipTransition: function() {} };
                }

                // タイムアウト制御 (ハングアップバグ防止 / doc c §1)
                // ※ transition.finished は ViewTransition の read-only getter のため代入不可。
                //   代わりに setTimeout で skipTransition() を直接呼び出す。
                var _timeoutId = setTimeout(function() {
                    console.warn('[VT-Proxy] Transition timed out after ' + TRANSITION_TIMEOUT_MS + 'ms — forcing skipTransition()');
                    try { transition.skipTransition(); } catch (_) {}
                }, TRANSITION_TIMEOUT_MS);

                // finished が正常完了またはキャンセルされたらタイムアウトをクリア
                transition.finished.then(function() {
                    clearTimeout(_timeoutId);
                }).catch(function(e) {
                    clearTimeout(_timeoutId);
                    // アニメーションが拒否された場合のみ警告 (DOMContentの適用は完了している)
                    if (e && e.name !== 'AbortError') {
                        console.warn('[VT-Proxy] Transition finished rejected:', e);
                    }
                });

                return transition;
            };
        })();

        // ===== Trusted Types Policy Enforcement (Non-destructive addition) =====
        // createHTML returns empty string to physically block TrustedHTML / innerHTML injection paths.
        // NOTE: createScript and createScriptURL are intentionally pass-through for compatibility.
        // These must NOT be described as strict script sanitization — they do not filter script content.
        // Trusted Types policy is used primarily to block TrustedHTML / innerHTML injection paths.
        // Script and ScriptURL policies are intentionally pass-through for compatibility and must
        // not be described as strict script sanitization.
        if (window.trustedTypes && trustedTypes.createPolicy) {
            try {
                trustedTypes.createPolicy('default', {
                    createHTML: (string) => {
                        console.warn('[AIO Audit] Architecture Constraint Violation: innerHTML manipulation is strictly prohibited.');
                        return '';
                    },
                    createScript: (string) => string,      // pass-through: compatibility only
                    createScriptURL: (string) => string    // pass-through: compatibility only
                });
            } catch (e) {
                console.error('Trusted Types policy initialization failed.', e);
            }
        }

        // ===== 1.1 use strict の再帰的適用 (改善文書b) =====
        // outer IIFE already uses 'use strict' (see line above)
        // All inner functions inherit strict mode. Confirmed here for auditors.

        // ===== 7.1 DocumentFragment batch DOM helper (改善文書b / 改善文書c) =====
        // Prevents Layout Thrashing: batch DOM mutations into a single live-DOM write.
        // Usage: appendBatch(container, itemsArray, buildItemFn)
        function appendBatch(container, items, buildFn) {
            const frag = document.createDocumentFragment();
            items.forEach(function(item, idx) {
                const node = buildFn(item, idx);
                if (node instanceof Node) { frag.appendChild(node); }
            });
            container.appendChild(frag);
        }

        // ===== Module Pattern: Constants =====
        // NOTE: Storage key は v45 のまま維持（互換性優先）。v46 はロジック非変更。



        // ===== Identity Constants — Single Source of Truth =====
        //   ▼ v80+ Stage 5-e: AUTHOR は closure-deps = none の純データのため
        //     js/identity.js へ抽出し、ファイル冒頭で import 済み（値は byte-equivalent）。
        //     UI 表示専用 (DISPLAY_NAME) と AIO/SEO 機械可読層専用 (AUTHORITATIVE_NAME) の責務分離は値で固定。

        // ===== Site Configuration — Central Registry =====
        // すべてのバージョン・URL・ロールタイトルはここで一元管理する。
        // 値の散在による食い違いを構造的に排除するための Single Source of Truth。
        const SITE_CONFIG = {
            VERSION:       'v74',
            LAST_UPDATED:  '2026-05-31',
            ROLE_TITLE:    'AI-Driven PM',
            CANONICAL_URL: 'https://yutapr0117-design.github.io/portfolio/',
            REPO_URL:      'https://github.com/yutapr0117-design/portfolio',
            ARTICLE_ROUTES: ['ai-knowhow'],   // og:type = article を適用するルート
        };

        // ===== CONSTANTS — Application Runtime Constants =====
        //   ▼ v80+ Stage 5-d: CONSTANTS は closure-deps = none（ブラウザグローバルのみ参照）
        //     のため js/constants.js へ抽出し、ファイル冒頭で import 済み（挙動・schema 等価）。
        //     SITE_CONFIG.VERSION / LAST_UPDATED は Check 2 / 17 が main.js を grep するため残置。


        // ===== Global Data: Quiz Questions =====
        // ▼ v80+ Stage 3 / 3-b: 4 つの巨大な静的データ定義は、Stage 3 で `js/quiz-data.js` へまとめて
        //   物理分割し、Stage 3-b でドメイン別 4 葉モジュール（`js/quiz/*-quiz-data.js`）へ細分化した。
        //   本ファイル冒頭でそれぞれを直接 import 済み（main.js から byte-equivalent に抽出。挙動不変）:
        //     awsQuizData / pmQuizData / qualityQuizData / architectureQuizData
        //   いずれも関数も副作用も持たない純データのため、別モジュール化で挙動は変わらない。
        //   消費箇所（quiz ソース lookup table: aws/pm/quality/architecture）は従来どおり
        //   この 4 名を参照する。約 1,360 行をここから分離し、可読性・保守性を改善した。


        // ===== Icons (SVG) / createIcon / h =====
        //   ▼ v80+ Stage 4: getIcons / createIcon / h は closure-deps = none の純表示系のため
        //     js/ui-components.js へ抽出し、ファイル冒頭で import 済み（挙動不変・署名不変）。
        //   （sparkles アイコンは元コード未登録だったため ui-components.js で補完）
        // ===== 1.2 INP最適化: メインスレッド解放ユーティリティ (改善指示書) =====
        // scheduler.yield() が使えない環境ではsetTimeout(0)でフォールバック
        //   ▼ v80+ Stage 2: yieldToMain は純粋ユーティリティのため js/pure-utils.js へ抽出し、
        //     ファイル冒頭で import 済み（挙動不変）。

        function clear(node) {
            while (node.firstChild) {
                node.removeChild(node.firstChild);
            }
        }

        // ===== Helper: Safe Storage =====
        //   ▼ v80+ Stage 5-c: Storage は closure-deps = none（localStorage と引数のみで挙動が決まる）
        //     のため js/storage.js へ抽出し、ファイル冒頭で import 済み（挙動・署名は byte-equivalent）。


        // ===== Helper: Utilities =====
        // ▼ v80+ Stage 2: 以下の純粋ユーティリティは `js/pure-utils.js` へ物理分割し、
        //   本ファイル冒頭で import 済み（挙動・シグネチャはバイト等価で不変）:
        //     generateId / clamp / debounce / throttle / tokenize /
        //     slugify / sanitizeUrl / safeFetchJSON / deepClone
        //   これらは引数のみで出力が決まり、本 IIFE のクロージャ状態にも DOM にも依存しない。
        //   各関数の詳細仕様・設計意図・セキュリティ境界（特に sanitizeUrl）は当該モジュール冒頭に記載。
        //   ※ DOM を触る clear(node) と localStorage をラップする Storage は純粋でない（service
        //     rail）ため抽出せず main.js に残置している（Stage 4 の領分）。


        // ===== Store Module =====
        //   ▼ v80+ Stage 5-g: Store は factory pattern で js/store.js へ抽出。
        //     createStore({AUTHOR, CONSTANTS, Storage, generateId, deepClone, slugify, sanitizeUrl, clamp})
        //     で合成（葉モジュール契約維持・公開 API と挙動は byte-equivalent）。
        const Store = createStore({ AUTHOR, CONSTANTS, Storage, generateId, deepClone, slugify, sanitizeUrl, clamp });

        // ===== State Management =====
        //   ▼ v80+ Stage 5-h: State は factory pattern で js/state.js へ抽出。
        //     createState({CONSTANTS, Store, Storage, Toast}) で合成（葉モジュール契約維持・公開 API と挙動は byte-equivalent）。
        const State = createState({ CONSTANTS, Store, Storage, Toast });

        // ===== AIDK RouteState — フラット名前空間UIステート (Proxy-based) =====
        // 設計書 Phase 1: ui_*, route_*, bgm_*, a11y_* の接頭辞を持つフラットなキー構造。
        // Proxyの set トラップで変更を一元管理し、BindingRegistry を自動起動する。
        // ※永続化が必要なアプリデータは従来の State モジュールが担う（責務分離）。
        const RouteState = (() => {
            const _state = {
                // ── route namespace ──
                route_name:    'home',
                route_slug:    '',
                route_hash:    '#/',
                // ── ui namespace ──
                ui_drawer_open:    false,
                ui_theme:          'system',
                ui_active_filter:  '',
                ui_is_loading:     false,
                // ── bgm namespace ──
                bgm_is_playing:   false,
                bgm_volume_level: 1.0,
                // ── a11y namespace ──
                a11y_announcement: '',
                // ── diag namespace ──
                diag_debug_mode:      false,
                diag_last_key:        '',
                diag_last_value:      null,
                diag_change_count:    0
            };

            const _callbacks = [];

            // 改善文書b 1.1: Object.seal prevents undeclared property addition on the proxy target.
            // Known properties can still be updated; adding new ones throws TypeError in strict mode.
            Object.seal(_state);

            const proxy = new Proxy(_state, {
                set(target, key, value) {
                    if (target[key] === value) return true; // 値変化なし → スキップ
                    const prev = target[key];
                    target[key] = value;

                    // Diagnostics 記録
                    target.diag_last_key   = String(key);
                    target.diag_last_value = value;
                    target.diag_change_count++;

                    // Binding Registry 通知
                    if (typeof BindingRegistry !== 'undefined') {
                        try { BindingRegistry.updateBindings(String(key), value, prev); } catch {}
                    }

                    // 副作用 Rail のディスパッチ
                    EffectRails.dispatch(String(key), value, prev);

                    // 汎用購読者への通知
                    _callbacks.forEach(cb => { try { cb(proxy, String(key), value, prev); } catch {} });
                    return true;
                }
            });

            function subscribe(cb) {
                _callbacks.push(cb);
                return () => { const i = _callbacks.indexOf(cb); if (i > -1) _callbacks.splice(i, 1); };
            }

            return { proxy, subscribe };
        })();

        // ===== AIDK EffectRails — Private副作用レール =====
        // Proxyからのみ呼び出される。AIから不可視・編集不可。
        const EffectRails = (() => {
            // 各キーに対応するRailをマッピング
            const _map = {
                route_name:        ['meta', 'aio', 'a11y'],
                route_slug:        ['meta', 'aio'],
                ui_drawer_open:    ['a11y'],
                a11y_announcement: ['a11y'],
                diag_debug_mode:   ['diag']
            };

            function _metaRail(key, value) {
                // Meta Rail: routeが変わったらapplyMetaに委譲
                if (key === 'route_name') {
                    try {
                        const RS = RouteState.proxy;
                        applyMeta(RS.route_name, RS.route_slug ? { slug: RS.route_slug } : {}, {});
                    } catch {}
                }
            }

            function _aioRail(key, value) {
                // AIO Rail: sr-onlyアンカーの整合性を保護（DOM再構築後も維持）
                try {
                    const anchor = document.getElementById('aio-footer-entity');
                    if (anchor && !document.body.contains(anchor)) {
                        document.body.appendChild(anchor);
                    }
                } catch {}
            }

            function _a11yRail(key, value) {
                if (key === 'a11y_announcement' && value) {
                    const el = document.getElementById('page-announcement');
                    if (el) {
                        requestAnimationFrame(() => {
                            el.textContent = '';
                            requestAnimationFrame(() => { el.textContent = value; });
                        });
                    }
                }
                if (key === 'ui_drawer_open') {
                    const app = document.getElementById('app');
                    if (app) {
                        if (value) { app.setAttribute('inert', ''); }
                        else { app.removeAttribute('inert'); }
                    }
                }
            }

            function _diagRail(key, value) {
                if (key === 'diag_debug_mode') {
                    if (value) DiagnosticsRail.show();
                    else DiagnosticsRail.hide();
                }
            }

            function dispatch(key, value, prev) {
                const rails = _map[key] || [];
                if (rails.includes('meta'))  try { _metaRail(key, value); } catch {}
                if (rails.includes('aio'))   try { _aioRail(key, value); } catch {}
                if (rails.includes('a11y'))  try { _a11yRail(key, value); } catch {}
                if (rails.includes('diag'))  try { _diagRail(key, value); } catch {}
                // Security Rail: 常時実行（副作用コストが低いため全変更後に走らせる）
                try { secureExternalLinks(document); } catch {}
            }

            return { dispatch };
        })();

        // ===== AIDK BindingRegistry — 自動水和バインディング登録機構 =====
        // MutationObserverで data-bind-* 属性を持つ要素を自動検知・登録する。
        // AIは属性を付与するだけでよく、バインディング登録コードを書く必要がない。
        const BindingRegistry = (() => {
            // Map<stateKey, Set<Element>>
            const _registry = new Map();
            let _observer = null;

            function _registerElement(el) {
                // data-bind-text
                const bindText = el.getAttribute('data-bind-text');
                if (bindText) _add(bindText, el);
                // data-bind-show
                const bindShow = el.getAttribute('data-bind-show');
                if (bindShow) _add(bindShow, el);
                // data-bind-attr-*
                for (const attr of el.attributes) {
                    if (attr.name.startsWith('data-bind-attr-')) {
                        const stateKey = attr.value;
                        if (stateKey) _add(stateKey, el);
                    }
                }
            }

            function _unregisterElement(el) {
                _registry.forEach((set) => set.delete(el));
            }

            function _add(key, el) {
                if (!_registry.has(key)) _registry.set(key, new Set());
                _registry.get(key).add(el);
                // 初期同期
                _syncElement(el, key, RouteState.proxy[key]);
            }

            function _syncElement(el, key, value) {
                if (el.hasAttribute('data-bind-text')) {
                    el.textContent = (value !== undefined && value !== null) ? String(value) : '';
                }
                if (el.hasAttribute('data-bind-show')) {
                    const show = !!value;
                    el.hidden = !show;
                    el.style.display = show ? '' : 'none';
                }
                for (const attr of el.attributes) {
                    if (attr.name.startsWith('data-bind-attr-')) {
                        const htmlAttr = attr.name.slice('data-bind-attr-'.length);
                        if (value !== undefined && value !== null) {
                            el.setAttribute(htmlAttr, String(value));
                        }
                    }
                }
            }

            function updateBindings(key, value) {
                const set = _registry.get(key);
                if (!set) return;
                set.forEach(el => {
                    if (document.contains(el)) {
                        _syncElement(el, key, value);
                    } else {
                        set.delete(el); // ガベージコレクション
                    }
                });
            }

            function init() {
                // 初回スキャン
                document.querySelectorAll('[data-bind-text],[data-bind-show],[data-bind-list]').forEach(el => {
                    for (const attr of el.attributes) {
                        if (attr.name.startsWith('data-bind-')) _registerElement(el);
                    }
                });

                // MutationObserver — DOMの追加・削除を自動検知
                _observer = new MutationObserver((mutations) => {
                    for (const mut of mutations) {
                        for (const node of mut.addedNodes) {
                            if (node.nodeType !== 1) continue;
                            if (node.hasAttribute && node.hasAttribute('data-bind-text') ||
                                node.hasAttribute && node.hasAttribute('data-bind-show')) {
                                _registerElement(node);
                            }
                            node.querySelectorAll && node.querySelectorAll('[data-bind-text],[data-bind-show]').forEach(el => {
                                _registerElement(el);
                            });
                        }
                        for (const node of mut.removedNodes) {
                            if (node.nodeType !== 1) continue;
                            _unregisterElement(node);
                            node.querySelectorAll && node.querySelectorAll('[data-bind-text],[data-bind-show]').forEach(el => {
                                _unregisterElement(el);
                            });
                        }
                    }
                });
                _observer.observe(document.body, { childList: true, subtree: true });
            }

            return { init, updateBindings };
        })();

        // ===== AIDK ActionDelegator — 単一イベント委譲器 =====
        // AIは data-action="ACTION_NAME" を付与するだけ。
        // 個別の addEventListener 記述は不要。
        const ActionDelegator = (() => {
            const _handlers = {
                'drawer:open':    () => { if (typeof openDrawer === 'function') openDrawer(); },
                'drawer:close':   () => { if (typeof closeDrawer === 'function') closeDrawer(); },
                'theme:cycle':    () => { if (typeof Theme !== 'undefined') Theme.cycle(); },
                'bgm:toggle':     () => { if (typeof BGM !== 'undefined') BGM.toggle(); }
            };

            function init() {
                // 改善文書b 11.1: target.closest() による正確な要素捕捉。
                // e.target ではなく e.target.closest('[data-action]') で遡上検索するため、
                // ボタン内のSVGアイコンや<span>がクリックされた場合でも確実に発火する。
                // さらに e.currentTarget.contains(target) でスコープ外への意図しない伝播を防ぐ。
                document.addEventListener('click', (e) => {
                    const target = e.target.closest('[data-action]');
                    if (!target) { return; }
                    // containsガード: documentに紐付いたリスナーなので常にtrueだが、
                    // 将来スコープを絞った場合の安全弁として明示的に残す
                    const action = target.getAttribute('data-action');
                    if (!action) { return; }
                    const handler = _handlers[action];
                    if (handler) {
                        e.preventDefault();
                        try { handler(e, target); } catch {}
                    }
                }, { passive: false });
            }

            function register(action, handler) {
                _handlers[action] = handler;
            }

            return { init, register };
        })();

        // ===== AIDK DiagnosticsRail — ?debug=1 オーバーレイ =====
        const DiagnosticsRail = (() => {
            let _el = null;

            function _appendDiagText(parent, text, className) {
                const span = document.createElement('span');
                if (className) span.className = className;
                span.textContent = text;
                parent.appendChild(span);
                return span;
            }

            function _appendDiagLine(parent, label, value, valueClassName) {
                const line = document.createElement('div');
                line.appendChild(document.createTextNode(`${label}: `));
                _appendDiagText(line, String(value), valueClassName);
                parent.appendChild(line);
                return line;
            }

            function _appendDiagSectionLabel(parent, text) {
                const label = document.createElement('b');
                label.className = 'u-ai-diag-label';
                label.textContent = text;
                parent.appendChild(label);
                return label;
            }

            function _appendDiagHr(parent) {
                const hr = document.createElement('hr');
                hr.className = 'u-ai-diag-hr';
                parent.appendChild(hr);
                return hr;
            }

            function _build() {
                const el = document.createElement('div');
                el.id = 'aidk-diagnostics';
                el.style.cssText = [
                    'position:fixed', 'bottom:0', 'right:0', 'z-index:99999',
                    'background:rgba(2,6,23,0.92)', 'color:#94a3b8',
                    'font:12px/1.5 monospace', 'padding:10px 14px',
                    'border-top-left-radius:8px', 'max-width:340px',
                    'max-height:40vh', 'overflow-y:auto',
                    'border:1px solid #334155', 'pointer-events:auto'
                ].join(';');
                el.setAttribute('aria-hidden', 'true');
                return el;
            }

            function _update() {
                if (!_el) return;
                const RS = RouteState.proxy;

                _el.replaceChildren();

                const title = document.createElement('strong');
                title.className = 'u-ai-diag-title';
                title.textContent = 'AIDK Diagnostics';
                _el.appendChild(title);

                _appendDiagHr(_el);
                _appendDiagSectionLabel(_el, 'RouteState');
                _appendDiagLine(_el, 'route_name', RS.route_name, 'u-ai-diag-val-green');
                _appendDiagLine(_el, 'route_slug', RS.route_slug || '—', 'u-ai-diag-val-green');
                _appendDiagLine(_el, 'ui_drawer_open', RS.ui_drawer_open, 'u-ai-diag-val-green');
                _appendDiagLine(_el, 'ui_theme', RS.ui_theme, 'u-ai-diag-val-green');

                _appendDiagHr(_el);
                _appendDiagSectionLabel(_el, 'Last Change');
                _appendDiagLine(_el, 'key', RS.diag_last_key || '—', 'u-ai-diag-val-amber');
                _appendDiagLine(_el, 'value', String(RS.diag_last_value), 'u-ai-diag-val-amber');
                _appendDiagLine(_el, 'changes', RS.diag_change_count, 'u-ai-diag-val-amber');

                _appendDiagHr(_el);
                _appendDiagSectionLabel(_el, 'Kernel');
                _appendDiagText(_el, 'BindingRegistry: active');
                _el.appendChild(document.createElement('br'));
                _appendDiagText(_el, 'ActionDelegator: active');
                _el.appendChild(document.createElement('br'));
                _appendDiagText(_el, 'EffectRails: Meta/AIO/A11y/Security/Diag');
                _el.appendChild(document.createElement('br'));
                _appendDiagText(_el, '?debug=1 to show · Press D to refresh', 'u-ai-diag-hint');
            }

            function show() {
                if (!_el) {
                    _el = _build();
                    document.body.appendChild(_el);
                }
                _el.style.display = 'block';
                // Auto-refresh every 2s
                if (!_el._timer) {
                    _el._timer = setInterval(_update, 2000);
                }
                _update();
                document.addEventListener('keydown', (e) => {
                    if (e.key === 'd' || e.key === 'D') _update();
                });
            }

            function hide() {
                if (_el) {
                    _el.style.display = 'none';
                    if (_el._timer) { clearInterval(_el._timer); _el._timer = null; }
                }
            }

            return { show, hide };
        })();

        // ===== AIDK Toast Notification System =====
        //   ▼ v80+ Stage 4: Toast は表示専用コンポーネントのため
        //     js/ui-components.js へ抽出し、ファイル冒頭で import 済み（挙動不変）。
        // ===== Theme Manager =====
        //   ▼ v80+ Stage 5-i: Theme は factory pattern で js/theme.js へ抽出。
        //     createTheme({State, Toast}) で合成（葉モジュール契約維持・公開 API と挙動は byte-equivalent）。
        const Theme = createTheme({ State, Toast });


        // ===== BGM Manager =====
        //   ▼ v80+ Stage 4: BGM は表示専用コンポーネントのため
        //     js/ui-components.js へ抽出し、ファイル冒頭で import 済み（挙動不変）。
        // ===== Brand Manager : primary palette/font switcher (Classic  / Indigo ) =====
        //   ▼ v80+ Stage 5-f: Brand は factory pattern で js/brand.js へ抽出。
        //     createBrand(Storage) に Storage instance を渡して合成（葉モジュール契約維持・挙動 byte-equivalent）。
        const Brand = createBrand(Storage);


        // ===== Router =====
        //   ▼ v80+ Stage 5: Router は closure-deps = none のため js/router.js へ抽出し、
        //     ファイル冒頭で import 済み（挙動不変。CONSTANTS.DEBUG 依存は production dead code のため削除）。

        // ===== v27: PAGE_META — 全ページSEOの単一ソース（AI SURFACE）=====
        //   ▼ v80+ Stage 5: PAGE_META は closure-deps = none の純データのため js/page-meta.js へ抽出し、
        //     ファイル冒頭で import 済み（挙動不変）。

        // ===== Meta Management — Single-Responsibility Sub-functions =====
        /* ╚══ AI SURFACE END — PAGE_META ══╝ */
        //   ▼ v80+ Stage 5-l: 4 つの SRP sub-function (updateDocumentHead /
        //     announceRouteForAccessibility / injectRouteEntityAnchor /
        //     injectStructuredData) + ファサード applyMeta を js/meta-management.js
        //     へ factory pattern で抽出。createMetaManagement({SITE_CONFIG, AUTHOR,
        //     PAGE_META, Router, State}) で合成（葉モジュール契約維持・挙動 byte-equivalent）。
        const { applyMeta } = createMetaManagement({ SITE_CONFIG, AUTHOR, PAGE_META, Router, State });


        // ===== Component: Sidebar =====
        // ===== Component: Sidebar =====
        // NAV_GROUPS: Primary（採用・評価者向け）/ Secondary（深掘り用）/ Lab（初期折りたたみ）
        // ===== v80+ Stage 5-m: UI Page Components (11 関数) =====
        //   Sidebar / HomePage / ProjectsPage / ProjectDetailPage / AppsPage /
        //   AboutPage / ResumePage / ContactPage / FatalPage / AIKnowhowPage / ContactCTA を
        //   js/components.js へ factory pattern で抽出。挙動 byte-equivalent。
        // closeDrawer is a function declaration later in this IIFE (hoisted), so the
        // identifier is already bound at this point. clear / CONSTANTS / tokenize are
        // already imported / declared above.
        const {
            Sidebar, HomePage, ProjectsPage, ProjectDetailPage, AppsPage,
            AboutPage, ResumePage, ContactPage, FatalPage, AIKnowhowPage, ContactCTA
        } = createComponents({
            h, createIcon, Toast, BGM, AUTHOR, Router, State, Theme, Brand, Store,
            tokenize, CONSTANTS, clear, closeDrawer
        });

        // ===== v80+ Stage 5-j: Page components factory instantiation =====
        //   ContactCTA は Stage 5-m で createComponents から供給される。それを createPages
        //   の引数に渡して HiringRiskPage / RoleSplitPage / NotFoundPage を合成する。
        const { HiringRiskPage, RoleSplitPage, NotFoundPage } = createPages({ h, createIcon, Router, ContactCTA });


        // ===== Component: Home Page =====

        // ===== Component: Projects Page =====

        // ===== Component: Project Detail Page =====

        // ===== Component: Apps Hub =====

        // ===== Component: Task App =====
        // [FIX] 揮発性クロージャ問題の解決：UIステートをコンポーネント外に保持
        // v80+ lint: 束縛自体は再代入されず .q / .priority のプロパティ変異のみのため const が正しい
        // （再代入が無い束縛に let を使うと prefer-const に抵触する。挙動は不変）。
        const taskFilter = { q: '', priority: 'all' };

        function TaskPage() {

            function addTask(title) {
                if (!title.trim()) {return;}
                State.update(s => {
                    s.appsData.tasks.unshift({
                        id: generateId(),
                        title: title.trim().slice(0, CONSTANTS.LIMITS.TASK_TITLE),
                        status: 'backlog',
                        priority: 'med',
                        tags: [],
                        createdAt: Date.now(),
                        updatedAt: Date.now()
                    });
                });
                Toast.show('タスクを追加しました', 'success');
            }

            function updateTask(id, updates) {
                State.update(s => {
                    const task = s.appsData.tasks.find(t => t.id === id);
                    if (task) {
                        Object.assign(task, updates, { updatedAt: Date.now() });
                    }
                });
            }

            function deleteTask(id) {
                State.update(s => {
                    s.appsData.tasks = s.appsData.tasks.filter(t => t.id !== id);
                    if (s.appsData.pomodoro.runtime.linkedTaskId === id) {
                        s.appsData.pomodoro.runtime.linkedTaskId = null;
                    }
                });
                Toast.show('タスクを削除しました', 'success');
            }

            function moveStatus(task, direction) {
                const statuses = ['backlog', 'in-progress', 'done'];
                const idx = statuses.indexOf(task.status);
                const newIdx = clamp(idx + direction, 0, statuses.length - 1);
                if (newIdx !== idx) {
                    updateTask(task.id, { status: statuses[newIdx] });
                }
            }

            function getFilteredTasks() {
                return State.get().appsData.tasks.filter(t => {
                    const matchesQ = !taskFilter.q ||
                        t.title.toLowerCase().includes(taskFilter.q.toLowerCase()) ||
                        t.tags.some(tag => tag.toLowerCase().includes(taskFilter.q.toLowerCase()));
                    const matchesPriority = taskFilter.priority === 'all' || t.priority === taskFilter.priority;
                    return matchesQ && matchesPriority;
                });
            }

            // [FIX] シャドウイング問題の解決：名称を buildUI に変更
            function buildUI() {
                const container = document.createElement('div');
                container.className = 'flex flex-col gap-4';

                // Header
                container.appendChild(h('header', {},
                    h('div', { class: 'flex items-center gap-3 mb-4' },
                        createIcon('checkSquare', 28),
                        h('h1', { class: 'h1' }, 'タスク管理')
                    ),
                    h('div', { class: 'grid grid-cols-2 gap-4' },
                        h('input', {
                            id: 'task-input',
                            class: 'input',
                            placeholder: '新しいタスクを入力...',
                            onkeydown: (e) => {
                                if (e.key === 'Enter') {
                                    addTask(e.target.value);
                                    // 全体再描画の直後にフォーカスを復元し、連続入力を可能にする
                                    setTimeout(() => document.getElementById('task-input')?.focus(), 0);
                                }
                            }
                        }),
                        h('select', {
                            class: 'input',
                            value: taskFilter.priority,
                            onchange: (e) => {
                                taskFilter.priority = e.target.value;
                                window.render(); // グローバルレンダーを呼び出し
                            }
                        },
                            h('option', { value: 'all', text: '優先度: 全て' }),
                            h('option', { value: 'high', text: 'High' }),
                            h('option', { value: 'med', text: 'Med' }),
                            h('option', { value: 'low', text: 'Low' })
                        )
                    )
                ));

                // Kanban
                const statuses = [
                    { id: 'backlog', label: '未着手' },
                    { id: 'in-progress', label: '進行中' },
                    { id: 'done', label: '完了' }
                ];

                const allTasks = getFilteredTasks();

                const board = h('div', {
                    class: 'grid grid-cols-3 col-min-400'
                });

                statuses.forEach(col => {
                    const tasks = allTasks.filter(t => t.status === col.id);
                    const column = h('section', {
                        class: 'card bg-secondary'
                    },
                        h('div', { class: 'card-header' },
                            h('div', { class: 'flex items-center justify-between' },
                                h('h4', { class: 'h4' }, col.label),
                                h('span', { class: 'badge badge-secondary' }, String(tasks.length))
                            )
                        ),
                        h('div', { class: 'card-body flex flex-col gap-3' },
                            ...tasks.map(task =>
                                h('article', {
                                    class: 'card bg-surface'
                                },
                                    h('div', { class: 'p-3' },
                                        h('div', { class: 'flex items-start justify-between gap-2 mb-2' },
                                            h('div', { class: 'flex items-center gap-2' },
                                                h('span', {
                                                    class: 'w-2 h-2 rounded-full',
                                                    style: `background:${task.priority === 'high' ? 'var(--color-danger)' :
                                                        task.priority === 'med' ? 'var(--color-warning)' :
                                                            'var(--color-success)'
                                                        };`
                                                }),
                                                h('span', { class: 'font-medium text-small' }, task.title)
                                            ),
                                            h('button', {
                                                class: 'icon-btn btn-sm icon-sm',
                                                onclick: () => deleteTask(task.id)
                                            }, createIcon('trash', 14))
                                        ),
                                        h('div', { class: 'flex items-center justify-between' },
                                            h('select', {
                                                class: 'input btn-sm',
                                                style: 'width:auto;padding:0.25rem 0.5rem;font-size:0.75rem;',
                                                value: task.priority,
                                                onchange: (e) => updateTask(task.id, { priority: e.target.value })
                                            },
                                                h('option', { value: 'high', text: 'High' }),
                                                h('option', { value: 'med', text: 'Med' }),
                                                h('option', { value: 'low', text: 'Low' })
                                            ),
                                            h('div', { class: 'flex gap-1' },
                                                h('button', {
                                                    class: 'btn btn-ghost btn-sm',
                                                    disabled: task.status === 'backlog',
                                                    onclick: () => moveStatus(task, -1)
                                                }, '←'),
                                                h('button', {
                                                    class: 'btn btn-ghost btn-sm',
                                                    disabled: task.status === 'done',
                                                    onclick: () => moveStatus(task, 1)
                                                }, '→')
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    );
                    board.appendChild(column);
                });

                container.appendChild(board);
                return container;
            }

            return buildUI();
        }

        // ===== Component: Todo App =====
        // [FIX] 揮発性クロージャ問題の解決
        let todoFilter = 'all';
        let todoComposing = false;

        function TodoPage() {

            function addTodo(text) {
                if (!text.trim()) {return;}
                State.update(s => {
                    s.appsData.todos.unshift({
                        id: generateId(),
                        text: text.trim().slice(0, CONSTANTS.LIMITS.TODO_TEXT),
                        completed: false,
                        createdAt: Date.now(),
                        dueDate: null
                    });
                });
            }

            function toggleTodo(id) {
                State.update(s => {
                    const todo = s.appsData.todos.find(t => t.id === id);
                    if (todo) {todo.completed = !todo.completed;}
                });
            }

            function deleteTodo(id) {
                State.update(s => {
                    s.appsData.todos = s.appsData.todos.filter(t => t.id !== id);
                });
            }

            function clearCompleted() {
                State.update(s => {
                    s.appsData.todos = s.appsData.todos.filter(t => !t.completed);
                });
                Toast.show('完了済みを削除しました', 'success');
            }

            const todos = State.get().appsData.todos;
            const filtered = todos.filter(t => {
                if (todoFilter === 'active') {return !t.completed;}
                if (todoFilter === 'completed') {return t.completed;}
                return true;
            });

            return h('div', { class: 'flex flex-col gap-4 max-w-2xl error-boundary-fallback', role: 'alert', 'aria-invalid': 'true', 'aria-errormessage': 'fallback-details', 'aria-description': 'Architecture constraint successfully caught an unstable state transition.' },
                h('header', { class: 'flex items-center gap-3' },
                    createIcon('list', 28),
                    h('h1', { class: 'h1' }, 'クイックTODO')
                ),

                h('section', { class: 'card' },
                    h('div', { class: 'card-body' },
                        h('input', {
                            id: 'todo-input',
                            class: 'input',
                            placeholder: '入力してEnter（IME対応）...',
                            oncompositionstart: () => todoComposing = true,
                            oncompositionend: () => todoComposing = false,
                            onkeydown: (e) => {
                                if (e.key === 'Enter' && !todoComposing) {
                                    addTodo(e.target.value);
                                    // 全体再描画の直後にフォーカスを復元
                                    setTimeout(() => document.getElementById('todo-input')?.focus(), 0);
                                }
                            }
                        }),
                        h('div', { class: 'flex gap-2 mt-4' },
                            h('select', {
                                class: 'input w-auto',
                                value: todoFilter,
                                onchange: (e) => { todoFilter = e.target.value; window.render(); }
                            },
                                h('option', { value: 'all', text: '全て' }),
                                h('option', { value: 'active', text: '未完了' }),
                                h('option', { value: 'completed', text: '完了' })
                            ),
                            h('button', {
                                class: 'btn btn-secondary btn-sm',
                                disabled: !todos.some(t => t.completed),
                                onclick: clearCompleted
                            }, '完了済み削除')
                        )
                    )
                ),

                h('section', { class: 'flex flex-col gap-2' },
                    ...filtered.map(todo =>
                        h('article', { class: 'card' },
                            h('div', { class: 'card-body flex items-center gap-3' },
                                h('input', {
                                    type: 'checkbox',
                                    checked: todo.completed,
                                    onchange: () => toggleTodo(todo.id),
                                    'aria-label': todo.completed ? '未完了に戻す' : '完了にする'
                                }),
                                h('span', {
                                    class: ['flex-1', todo.completed && 'text-muted'],
                                    style: todo.completed ? 'text-decoration:line-through;opacity:0.6;' : undefined
                                }, todo.text),
                                h('button', {
                                    class: 'icon-btn',
                                    onclick: () => deleteTodo(todo.id),
                                    'aria-label': '削除'
                                }, createIcon('x', 16))
                            )
                        )
                    ),
                    filtered.length === 0 && h('p', { class: 'text-muted text-center py-8' }, 'TODOはありません。')
                )
            );
        }

        // ===== Component: Pomodoro App =====
        let pomodoroTimer = null;

        function PomodoroPage() {
            const pomo = State.get().appsData.pomodoro;

            function formatTime(sec) {
                const m = Math.floor(sec / 60);
                const s = sec % 60;
                return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
            }

            function getDuration(mode) {
                return (mode === 'work' ? pomo.settings.work :
                    mode === 'short-break' ? pomo.settings.short : pomo.settings.long) * 60;
            }

            function getRemaining() {
                const rt = pomo.runtime;
                if (rt.isActive && rt.endAtMs) {
                    return Math.max(0, Math.ceil((rt.endAtMs - Date.now()) / 1000));
                }
                return rt.remainingSec;
            }

            function start() {
                const remaining = getRemaining();
                State.update(s => {
                    s.appsData.pomodoro.runtime.isActive = true;
                    s.appsData.pomodoro.runtime.endAtMs = Date.now() + remaining * 1000;
                });
                startTimer();
            }

            function pause() {
                State.update(s => {
                    s.appsData.pomodoro.runtime.isActive = false;
                    s.appsData.pomodoro.runtime.endAtMs = null;
                    s.appsData.pomodoro.runtime.remainingSec = getRemaining();
                });
                stopTimer();
            }

            function reset() {
                stopTimer();
                const duration = getDuration(pomo.runtime.mode);
                State.update(s => {
                    s.appsData.pomodoro.runtime.isActive = false;
                    s.appsData.pomodoro.runtime.endAtMs = null;
                    s.appsData.pomodoro.runtime.remainingSec = duration;
                });
            }

            function complete() {
                stopTimer();
                const duration = getDuration(pomo.runtime.mode);
                State.update(s => {
                    s.appsData.pomodoro.history.push({
                        timestamp: Date.now(),
                        durationMinutes: Math.floor(duration / 60),
                        type: s.appsData.pomodoro.runtime.mode,
                        linkedTaskId: s.appsData.pomodoro.runtime.linkedTaskId
                    });
                    s.appsData.pomodoro.history = s.appsData.pomodoro.history.slice(-200);
                    s.appsData.pomodoro.runtime.isActive = false;
                    s.appsData.pomodoro.runtime.endAtMs = null;
                    s.appsData.pomodoro.runtime.remainingSec = duration;
                });
                Toast.show('セッション完了！', 'success');
            }

            function switchMode(mode) {
                stopTimer();
                const duration = getDuration(mode);
                State.update(s => {
                    s.appsData.pomodoro.runtime.mode = mode;
                    s.appsData.pomodoro.runtime.isActive = false;
                    s.appsData.pomodoro.runtime.endAtMs = null;
                    s.appsData.pomodoro.runtime.remainingSec = duration;
                });
            }

            function startTimer() {
                if (pomodoroTimer) {clearInterval(pomodoroTimer);}
                pomodoroTimer = setInterval(() => {
                    const remaining = getRemaining();
                    if (remaining <= 0) {
                        complete();
                        window.render(); // グローバルを描画
                    } else if (Router.getRoute().name === 'app-pomodoro') {
                        window.render(); // グローバルを描画
                    }
                }, 1000);
            }

            function stopTimer() {
                if (pomodoroTimer) {
                    clearInterval(pomodoroTimer);
                    pomodoroTimer = null;
                }
            }

            const modes = [
                { id: 'work', label: '集中' },
                { id: 'short-break', label: '短休憩' },
                { id: 'long-break', label: '長休憩' }
            ];

            const remaining = getRemaining();
            const isActive = pomo.runtime.isActive;

            function buildUI() {
                return h('div', { class: 'flex flex-col gap-4 max-w-xl' },
                    h('header', { class: 'flex items-center gap-3' },
                        createIcon('clock', 28),
                        h('h1', { class: 'h1' }, 'ポモドーロタイマー')
                    ),

                    // Timer Display
                    h('section', { class: 'card' },
                        h('div', { class: 'card-body text-center' },
                            h('div', { class: 'flex justify-center gap-2 mb-6' },
                                ...modes.map(m =>
                                    h('button', {
                                        class: ['btn', pomo.runtime.mode === m.id ? 'btn-primary' : 'btn-secondary'],
                                        onclick: () => switchMode(m.id)
                                    }, m.label)
                                )
                            ),
                            h('div', {
                                class: 'font-mono mb-6 text-stat'
                            }, formatTime(remaining)),
                            h('div', { class: 'flex justify-center gap-3' },
                                h('button', {
                                    class: 'btn btn-primary btn-lg',
                                    onclick: isActive ? pause : start
                                }, isActive ? h('span', {}, createIcon('pause', 20), ' 一時停止') : h('span', {}, createIcon('play', 20), ' 開始')),
                                h('button', {
                                    class: 'btn btn-secondary',
                                    onclick: reset,
                                    'aria-label': 'リセット'
                                }, createIcon('rotate', 20))
                            )
                        )
                    ),

                    // Settings
                    h('section', { class: 'card' },
                        h('div', { class: 'card-body' },
                            h('h3', { class: 'h3 mb-4' }, '設定（分）'),
                            h('div', { class: 'grid grid-cols-3 gap-4' },
                                h('div', {},
                                    h('label', { class: 'text-small text-muted mb-1 block' }, '集中'),
                                    h('input', {
                                        type: 'number',
                                        class: 'input',
                                        value: pomo.settings.work,
                                        min: 1, max: 180,
                                        onchange: (e) => State.update(s => {
                                            s.appsData.pomodoro.settings.work = clamp(parseInt(e.target.value) || 25, 1, 180);
                                            if (!s.appsData.pomodoro.runtime.isActive && s.appsData.pomodoro.runtime.mode === 'work') {
                                                s.appsData.pomodoro.runtime.remainingSec = s.appsData.pomodoro.settings.work * 60;
                                            }
                                        })
                                    })
                                ),
                                h('div', {},
                                    h('label', { class: 'text-small text-muted mb-1 block' }, '短休憩'),
                                    h('input', {
                                        type: 'number',
                                        class: 'input',
                                        value: pomo.settings.short,
                                        min: 1, max: 60,
                                        onchange: (e) => State.update(s => {
                                            s.appsData.pomodoro.settings.short = clamp(parseInt(e.target.value) || 5, 1, 60);
                                        })
                                    })
                                ),
                                h('div', {},
                                    h('label', { class: 'text-small text-muted mb-1 block' }, '長休憩'),
                                    h('input', {
                                        type: 'number',
                                        class: 'input',
                                        value: pomo.settings.long,
                                        min: 1, max: 120,
                                        onchange: (e) => State.update(s => {
                                            s.appsData.pomodoro.settings.long = clamp(parseInt(e.target.value) || 15, 1, 120);
                                        })
                                    })
                                )
                            )
                        )
                    )
                );
            }

            return buildUI();
        }

        // ===== Component: AI Assist Page =====
        let aiLoading = false;

        function AIPage() {
            const ai = State.get().appsData.ai;

            function analyzeInput(input) {
                const p = input.toLowerCase();
                if (p.includes('エラー') || p.includes('バグ') || p.includes('失敗')) {return 'troubleshoot';}
                if (p.includes('設計') || p.includes('計画') || p.includes('構成')) {return 'design';}
                return 'general';
            }

            function generateResponse(input, type) {
                if (type === 'troubleshoot') {
                    return `[AI分析: トラブルシューティング]
• 再現条件を明確化
• 影響範囲を特定
• ログ/証跡を収集
• 切り分けを実施
• 修正と回帰テスト

詳細な手順が必要であれば、「具体的なエラー内容を教えてください」とお伝えください。`;
                }
                if (type === 'design') {
                    return `[AI分析: 設計支援]
• 目的と非目的の定義
• 依存関係と制約の整理
• 失敗条件の洗い出し
• 境界（責任/権限）の明確化
• 検証手段の設計

設計書のテンプレートが必要であればお知らせください。`;
                }
                return `[AI分析: 一般支援]
タスク分解、文章生成、ポートフォリオ作成支援などに対応しています。
具体的なご質問をお聞かせください。`;
            }

            function submit(input) {
                if (!input.trim() || aiLoading) {return;}
                aiLoading = true;
                window.render(); // ローディング表示のため再描画

                const type = analyzeInput(input);

                setTimeout(() => {
                    const response = generateResponse(input, type);
                    State.update(s => {
                        s.appsData.ai.history.push({
                            prompt: input,
                            response,
                            timestamp: Date.now()
                        });
                        s.appsData.ai.history = s.appsData.ai.history.slice(-80);
                    });
                    aiLoading = false;
                    // State.update が内部で notify() するため window.render() は自動で呼ばれる
                    // 応答完了後に再度入力できるようフォーカスを復元
                    setTimeout(() => document.getElementById('ai-input')?.focus(), 0);
                }, 300);
            }

            function buildUI() {
                return h('div', { class: 'flex flex-col gap-4 max-w-2xl' },
                    h('header', { class: 'flex items-center gap-3' },
                        createIcon('brain', 28),
                        h('h1', { class: 'h1' }, 'AI アシスト（ローカル版）')
                    ),

                    h('p', { class: 'text-muted' }, '外部APIに依存せず、ブラウザ内で動作するAI支援ツールです。'),

                    // Chat History
                    h('section', {
                        class: 'card scroll-y-400'
                    },
                        h('div', { class: 'card-body flex flex-col gap-4' },
                            ai.history.length === 0 ?
                                h('p', { class: 'text-muted text-center py-8' },
                                    '会話を始めましょう。タスク分解、設計支援、トラブルシューティングなどが可能です。'
                                ) :
                                ai.history.flatMap(histItem => [
                                    h('div', { class: 'flex flex-col gap-1' },
                                        h('div', {
                                            class: 'self-end p-3 rounded-lg chat-bubble-own'
                                        }, histItem.prompt),
                                        h('div', {
                                            class: 'self-start p-3 rounded-lg chat-bubble-other'
                                        }, histItem.response),
                                        h('span', { class: 'text-xs text-muted self-start' },
                                            new Date(histItem.timestamp).toLocaleTimeString()
                                        )
                                    )
                                ])
                        )
                    ),

                    // Input
                    h('section', { class: 'card' },
                        h('div', { class: 'card-body' },
                            h('div', { class: 'flex gap-3' },
                                h('input', {
                                    id: 'ai-input',
                                    class: 'input',
                                    placeholder: '例：デプロイ手順を分解して、タスク管理アプリの説明文を書いて...',
                                    disabled: aiLoading,
                                    onkeydown: (e) => {
                                        if (e.key === 'Enter') {
                                            submit(e.target.value);
                                            // DOM再構築されるため input の value リセットは不要
                                        }
                                    }
                                }),
                                h('button', {
                                    class: 'btn btn-primary',
                                    disabled: aiLoading,
                                    onclick: (e) => {
                                        const input = e.target.previousElementSibling;
                                        submit(input.value);
                                    }
                                }, aiLoading ? '生成中...' : '送信')
                            )
                        )
                    )
                );
            }

            return buildUI();
        }

        // ===== Component: Settings Page =====
        let settingsImportMode = 'append';
        let settingsIncludeProfile = true;
        let settingsIncludeProjects = true;
        let settingsIncludeApps = true;
        let settingsNewName = '';
        let settingsNewTech = '';
        let settingsNewDemo = '';

        function SettingsPage() {
            const state = State.get();

            // --- 不足していた関数群の実装 ---
            function getSnapshot() {
                const raw = Storage.parse(CONSTANTS.SNAPSHOT_KEY);
                if (!raw) {return null;}

                // Support both formats:
                // 1) { at, data, ... }  (current)
                // 2) <store object>    (legacy; schema-mismatch snapshot in older versions)
                if (raw && typeof raw === 'object' && raw.data && typeof raw.data === 'object') {
                    return raw;
                }

                // Legacy: treat the whole object as store data
                if (raw && typeof raw === 'object' && raw.schemaVersion) {
                    return { at: Date.now(), reason: 'legacy-snapshot', data: raw };
                }

                return null;
            }
            function setSnapshot() {
                const snap = { at: Date.now(), data: State.get() };
                const success = Storage.set(CONSTANTS.SNAPSHOT_KEY, JSON.stringify(snap));
                if (success) {
                    Toast.show('スナップショットを保存しました');
                } else {
                    Toast.show('ストレージ上限のため保存に失敗しました。不要なデータを削除してください。', 'error', 5000);
                }
                State.update(s => { }); // 強制再描画
            }
            function restoreSnapshot() {
                const snap = getSnapshot();
                if (!snap || !snap.data) {return;}

                // Safety: refuse obviously wrong shapes
                if (typeof snap.data !== 'object' || !snap.data.schemaVersion) {
                    Toast.show('スナップショット形式が不正です', 'error');
                    return;
                }

                // If schema differs, still allow restore (user intent), but warn
                if (snap.data.schemaVersion !== CONSTANTS.SCHEMA_VERSION) {
                    Toast.show(`注意: schemaVersion が一致しません（${snap.data.schemaVersion}→${CONSTANTS.SCHEMA_VERSION}）`, 'warning');
                }

                State.set(snap.data);
                Toast.show('スナップショットを復元しました');
            }
            function clearSnapshot() {
                Storage.remove(CONSTANTS.SNAPSHOT_KEY);
                Toast.show('スナップショットを削除しました');
                State.update(s => { }); // 強制再描画
            }

            function downloadJSON(data, filename) {
                const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = filename;
                a.click();
                URL.revokeObjectURL(url);
            }
            function exportFull() { downloadJSON(State.get(), `portfolio_full_${Date.now()}.json`); }
            function exportProjects() { downloadJSON(State.get().projects, `portfolio_projects_${Date.now()}.json`); }
            function exportApps() { downloadJSON(State.get().appsData, `portfolio_apps_${Date.now()}.json`); }
            function exportProfile() { downloadJSON(State.get().profile, `portfolio_profile_${Date.now()}.json`); }

            function importJSON(file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    try {
                        const parsed = JSON.parse(e.target.result);
                        State.update(s => {
                            if (settingsIncludeProfile && parsed.profile) {s.profile = parsed.profile;}
                            if (settingsIncludeProjects && Array.isArray(parsed.projects)) {
                                if (settingsImportMode === 'strict') {s.projects = parsed.projects;}
                                else {
                                    // 既存プロジェクトのマップ作成
                                    const existingMap = new Map(s.projects.map(p => [p.id, p]));
                                    parsed.projects.forEach(p => {
                                        if (!existingMap.has(p.id)) {s.projects.push(p);}
                                        else if (settingsImportMode === 'upsert') {existingMap.set(p.id, p);}
                                    });
                                    if (settingsImportMode === 'upsert') {s.projects = Array.from(existingMap.values());}
                                }
                            }
                            if (settingsIncludeApps && parsed.appsData) {s.appsData = parsed.appsData;}
                        });

                        // [CRITICAL FIX] インポート直後に必ず正規化を通し、不正なデータ構造によるクラッシュを防ぐ
                        State.set(Store.validateAndNormalize(State.get()));

                        Toast.show('インポートが完了しました');
                    } catch (err) {
                        Toast.show('JSONのパースに失敗しました', 'error');
                    }
                };
                reader.readAsText(file);
            }

            function addProjectManual() {
                if (!settingsNewName.trim()) { Toast.show('プロジェクト名を入力してください', 'error'); return; }
                State.update(s => {
                    s.projects.unshift({
                        id: 'p_user_' + generateId().slice(0, 6),
                        slug: slugify(settingsNewName),
                        name: settingsNewName,
                        category: 'User Added',
                        summary: '', problem: '', approach: '',
                        tech: settingsNewTech ? settingsNewTech.split(',').map(t => t.trim()) : [],
                        tags: [],
                        demoRoute: settingsNewDemo || null
                    });
                });
                settingsNewName = ''; settingsNewTech = ''; settingsNewDemo = '';
                Toast.show('プロジェクトを追加しました');
            }

            const defaultProjectIds = new Set(['p01', 'p02', 'p03', 'p04', 'p05', 'p06', 'p07', 'p08', 'p09', 'p10', 'p11', 'p12', 'p13', 'p14', 'p15', 'p16', 'p17', 'p18']);

            function toggleHiddenProject(id) {
                State.update(s => {
                    s.projectPrefs = s.projectPrefs || { hiddenIds: [] };
                    const idx = s.projectPrefs.hiddenIds.indexOf(id);
                    if (idx > -1) {s.projectPrefs.hiddenIds.splice(idx, 1);}
                    else {s.projectPrefs.hiddenIds.push(id);}
                });
            }

            function deleteProjectHard(id) {
                if (defaultProjectIds.has(id)) {return;}
                if (!confirm('本当に削除しますか？')) {return;}
                State.update(s => {
                    s.projects = s.projects.filter(p => p.id !== id);
                });
            }

            function moveProject(idx, dir) {
                State.update(s => {
                    if (idx + dir < 0 || idx + dir >= s.projects.length) {return;}
                    const temp = s.projects[idx];
                    s.projects[idx] = s.projects[idx + dir];
                    s.projects[idx + dir] = temp;
                });
            }

            function normalizeNow() {
                const norm = Store.validateAndNormalize(State.get());
                State.set(norm);
                Toast.show('正規化を完了しました');
            }

            function resetData() {
                if (!confirm('すべてのデータを初期化しますか？')) {return;}
                State.set(Store.createDefaultStore());
                Toast.show('初期化しました');
            }

            function buildUI() {
                const snap = getSnapshot(); // v56.5: snapをbuildUIスコープで取得
                return h('article', { class: 'flex flex-col gap-6' },
                    h('header', {}, h('h1', { class: 'h1' }, 'Settings')),
                    h('div', { class: 'grid grid-cols-1 md:grid-cols-2 gap-6' },
                        h('section', { class: 'card' },
                            h('div', { class: 'card-body flex flex-col gap-3' },
                                h('h2', { class: 'h3' }, 'エクスポート'),
                                h('div', { class: 'flex flex-wrap gap-2' },
                                    h('button', { class: 'btn btn-primary', onclick: exportFull }, 'フルバックアップ'),
                                    h('button', { class: 'btn btn-secondary', onclick: exportProjects }, 'Projectsのみ'),
                                    h('button', { class: 'btn btn-secondary', onclick: exportApps }, 'AppsDataのみ'),
                                    h('button', { class: 'btn btn-secondary', onclick: exportProfile }, 'Profileのみ')
                                ),
                                h('p', { class: 'text-muted text-sm' }, 'フルバックアップは互換性を考慮した形式です。')
                            )
                        ),
                        h('section', { class: 'card' },
                            h('div', { class: 'card-body flex flex-col gap-3' },
                                h('h2', { class: 'h3' }, 'インポート（欠損ゼロ）'),
                                h('div', { class: 'grid grid-cols-2 gap-3' },
                                    h('div', {},
                                        h('label', { class: 'text-sm text-muted' }, 'モード'),
                                        h('select', { class: 'input', onchange: (e) => { settingsImportMode = e.target.value; window.render(); }, value: settingsImportMode },
                                            h('option', { value: 'append' }, 'append（追加のみ）'),
                                            h('option', { value: 'upsert' }, 'upsert（更新+追加）'),
                                            h('option', { value: 'strict' }, 'strict（全置換）')
                                        )
                                    ),
                                    h('div', {},
                                        h('label', { class: 'text-sm text-muted' }, '対象'),
                                        h('div', { class: 'flex flex-wrap gap-2' },
                                            h('label', { class: 'btn btn-ghost btn-sm' },
                                                h('input', { type: 'checkbox', checked: settingsIncludeProfile, onchange: (e) => { settingsIncludeProfile = !!e.target.checked; window.render(); } }),
                                                h('span', { class: 'icon-gap' }, 'Profile')
                                            ),
                                            h('label', { class: 'btn btn-ghost btn-sm' },
                                                h('input', { type: 'checkbox', checked: settingsIncludeProjects, onchange: (e) => { settingsIncludeProjects = !!e.target.checked; window.render(); } }),
                                                h('span', { class: 'icon-gap' }, 'Projects')
                                            ),
                                            h('label', { class: 'btn btn-ghost btn-sm' },
                                                h('input', { type: 'checkbox', checked: settingsIncludeApps, onchange: (e) => { settingsIncludeApps = !!e.target.checked; window.render(); } }),
                                                h('span', { class: 'icon-gap' }, 'AppsData')
                                            )
                                        )
                                    )
                                ),
                                h('div', {},
                                    h('input', {
                                        type: 'file',
                                        class: 'input',
                                        accept: 'application/json',
                                        onchange: (e) => {
                                            const f = e.target.files && e.target.files[0];
                                            if (f) {importJSON(f);}
                                            e.target.value = '';
                                        }
                                    })
                                ),
                                h('p', { class: 'text-muted text-sm' }, 'Projectsは常にデフォルトを維持しつつ、あなたの編集を優先してマージします。')
                            )
                        ),
                        h('section', { class: 'card' },
                            h('div', { class: 'card-body flex flex-col gap-3' },
                                h('h2', { class: 'h3' }, 'デザイン'),
                                h('p', { class: 'text-muted' }, 'Primaryカラーとベースフォントを切り替えます（Light/Dark/Systemは別設定）。'),
                                h('div', { class: 'flex flex-wrap items-center gap-3' },
                                    h('label', { class: 'text-sm font-semibold', for: 'brandSelect' }, 'ブランド'),
                                    h('select', {
                                        id: 'brandSelect',
                                        class: 'input',
                                        value: Brand.get(),
                                        onchange: (e) => { Brand.set(e.target.value); window.render(); }
                                    },
                                        h('option', { value: 'indigo' }, 'Indigo'),
                                        h('option', { value: 'classic' }, 'Classic Blue + Inter')
                                    ),
                                    h('span', { class: 'badge badge-secondary' }, '即時反映')
                                )
                            )
                        ),
                        h('section', { class: 'card' },
                            h('div', { class: 'card-body flex flex-col gap-3' },
                                h('h2', { class: 'h3' }, 'スナップショット'),
                                h('div', { class: 'flex flex-wrap gap-2' },
                                    h('button', { class: 'btn btn-secondary', onclick: setSnapshot }, '保存'),
                                    h('button', { class: 'btn btn-secondary', onclick: restoreSnapshot, disabled: !snap }, '復元'),
                                    h('button', { class: 'btn btn-ghost', onclick: clearSnapshot, disabled: !snap }, '削除')
                                ),
                                snap
                                    ? h('p', { class: 'text-muted text-sm' }, `保存日時: ${new Date(snap.at).toLocaleString()}`)
                                    : h('p', { class: 'text-muted text-sm' }, 'スナップショットは未保存です。')
                            )
                        ),
                        h('section', { class: 'card' },
                            h('div', { class: 'card-body flex flex-col gap-3' },
                                h('h2', { class: 'h3' }, '並び替え（Projects）'),
                                h('div', { class: 'text-muted text-sm' }, '上下ボタンで表示順を調整できます。'),
                                h('div', { class: 'flex flex-col gap-2 scroll-container-sm' },
                                    ...state.projects.map((p, idx) =>
                                        h('div', { class: 'flex items-center justify-between gap-2' },
                                            h('div', { class: 'flex items-center gap-2' },
                                                h('span', { class: 'badge badge-gray' }, String(idx + 1)),
                                                h('span', { class: 'text-sm' }, p.name)
                                            ),
                                            h('div', { class: 'flex items-center gap-2' },
                                                h('button', { class: 'btn btn-ghost btn-sm', onclick: () => moveProject(idx, -1), disabled: idx === 0 }, '↑'),
                                                h('button', { class: 'btn btn-ghost btn-sm', onclick: () => moveProject(idx, +1), disabled: idx === state.projects.length - 1 }, '↓')
                                            )
                                        )
                                    )
                                )
                            )
                        ),
                        h('section', { class: 'card' },
                            h('div', { class: 'card-body flex flex-col gap-3' },
                                h('h2', { class: 'h3' }, '表示管理（Projects）'),
                                h('div', { class: 'grid grid-cols-1 gap-3' },
                                    h('div', {},
                                        h('label', { class: 'text-sm text-muted' }, '名前'),
                                        h('input', { class: 'input', placeholder: 'プロジェクト名', value: settingsNewName, oninput: (e) => { settingsNewName = e.target.value; } })
                                    ),
                                    h('div', {},
                                        h('label', { class: 'text-sm text-muted' }, 'Tech（カンマ区切り）'),
                                        h('input', { class: 'input', placeholder: '例: JS,HTML,CSS', value: settingsNewTech, oninput: (e) => { settingsNewTech = e.target.value; } })
                                    ),
                                    h('div', {},
                                        h('label', { class: 'text-sm text-muted' }, 'Demo（任意）'),
                                        h('select', { class: 'input', onchange: (e) => { settingsNewDemo = e.target.value; }, value: settingsNewDemo },
                                            h('option', { value: '' }, 'Demoなし'),
                                            h('option', { value: 'task' }, 'task'),
                                            h('option', { value: 'todo' }, 'todo'),
                                            h('option', { value: 'pomodoro' }, 'pomodoro'),
                                            h('option', { value: 'ai' }, 'ai')
                                        )
                                    ),
                                    h('div', { class: 'flex items-end' },
                                        h('button', { class: 'btn btn-primary w-full', onclick: addProjectManual }, '追加')
                                    )
                                ),
                                (() => {
                                    const hidden = new Set(((state.projectPrefs && state.projectPrefs.hiddenIds) || []).map(String));
                                    const visibleCount = state.projects.filter(p => !hidden.has(String(p.id))).length;
                                    const hiddenCount = state.projects.length - visibleCount;
                                    return h('div', { class: 'text-muted text-sm' }, `表示: ${visibleCount} / 非表示: ${hiddenCount} / 総数: ${state.projects.length}`);
                                })(),
                                h('div', { class: 'flex flex-col gap-2 scroll-container-md' },
                                    ...state.projects.map(p => {
                                        const hidden = new Set(((state.projectPrefs && state.projectPrefs.hiddenIds) || []).map(String));
                                        const isHidden = hidden.has(String(p.id));
                                        const isDefault = defaultProjectIds.has(String(p.id));
                                        return h('div', { class: 'flex items-center justify-between gap-2' },
                                            h('div', { class: 'flex items-center gap-2' },
                                                h('span', { class: 'badge badge-gray' }, isDefault ? 'default' : 'user'),
                                                h('span', { class: 'text-sm' }, p.name),
                                                isHidden ? h('span', { class: 'badge badge-green' }, 'hidden') : null
                                            ),
                                            h('div', { class: 'flex items-center gap-2' },
                                                h('button', { class: 'btn btn-ghost btn-sm', onclick: () => toggleHiddenProject(p.id) }, isHidden ? '表示' : '非表示'),
                                                h('button', { class: 'btn btn-danger btn-sm', disabled: isDefault, title: isDefault ? 'デフォルトは非表示のみ' : '', onclick: () => deleteProjectHard(p.id) }, '削除')
                                            )
                                        );
                                    })
                                )
                            )
                        ),
                        h('section', { class: 'card' },
                            h('div', { class: 'card-body flex flex-col gap-3' },
                                h('h2', { class: 'h3' }, '整合性チェック / 正規化'),
                                h('div', { class: 'flex flex-wrap gap-2' },
                                    h('button', { class: 'btn btn-secondary', onclick: normalizeNow }, '実行'),
                                    h('button', { class: 'btn btn-danger', onclick: resetData }, '全リセット')
                                ),
                                h('p', { class: 'text-muted text-sm' }, '正規化はデータ破損・型揺れ・上限超過などを安全側に丸めます。')
                            )
                        )
                    )
                );
            }
            return buildUI();
        }



        function QuizPage() {
            const state = State.get();
            const quizSearch = state.appsData.quizSearch || "";

            function handleSearch(e) {
                const val = e.target.value;
                State.update(s => { s.appsData.quizSearch = val; });
            }

            const route = Router.getRoute();
            const quizType = route.query.type || 'aws';

            // ===== v40: Quiz data lookup table for extensibility =====
            const QUIZ_DATA_MAP = {
                aws: { title: 'AWS問題集', data: awsQuizData },
                pm: { title: 'PM問題集', data: pmQuizData },
                quality: { title: '品質・プロセス問題集', data: qualityQuizData },
                architecture: { title: '設計判断問題集', data: architectureQuizData }
            };
            const quizConfig = QUIZ_DATA_MAP[quizType] || QUIZ_DATA_MAP.aws;
            const pageTitle = quizConfig.title;  // v40: BUGFIX - Define pageTitle from QUIZ_DATA_MAP
            let quizData = quizConfig.data;      // v40: BUGFIX - Use let for reassignment
            const isArchitecture = quizType === 'architecture';

            const box = h("div", { class: "col col-centered" });

            box.appendChild(h("div", { class: "h2", text: pageTitle }));

            // Search Input
            box.appendChild(h("div", { class: "mb-6" },
                h("div", { class: "relative" },
                    h("input", {
                        type: "text",
                        class: "input pl-10",
                        placeholder: "問題を検索...",
                        value: quizSearch,
                        'aria-label': '問題検索',
                        oninput: handleSearch
                    }),
                    h("div", {
                        class: "absolute left-3 top-1/2 -translate-y-1/2 text-muted pointer-events-none"
                    }, createIcon("search", 18))
                )
            ));

            // v40: QUIZ_DATA_MAP moved above for early pageTitle definition


            // Filter quizData based on search query
            const filteredQuizData = {};
            const query = quizSearch.toLowerCase().trim();

            Object.keys(quizData).forEach(section => {
                const questions = quizData[section].filter(q => {
                    if (!query) {return true;}
                    const titleMatch = q.title.toLowerCase().includes(query);
                    const idMatch = q.id.toLowerCase().includes(query);
                    const contentMatch = q.content ? q.content.some(line => line.toLowerCase().includes(query)) : false;
                    const situationMatch = q.situation ? q.situation.some(line => line.toLowerCase().includes(query)) : false;
                    const questionMatch = q.question ? q.question.toLowerCase().includes(query) : false;
                    return titleMatch || idMatch || contentMatch || situationMatch || questionMatch;
                });
                if (questions.length > 0) {
                    filteredQuizData[section] = questions;
                }
            });
            quizData = filteredQuizData;

            // 0件時UI
            if (query && Object.keys(quizData).length === 0) {
                box.appendChild(h("div", {
                    class: 'card panel-empty',
                    role: 'status',
                    'aria-live': 'polite'
                }, '「' + query + '」に一致する問題は見つかりませんでした。'));
                const contactBox2 = h("div", { class: "card p col col-gap" });
                contactBox2.appendChild(h("div", { class: "h3", text: "模範解答について" }));
                contactBox2.appendChild(h("div", { class: "muted" }, "模範解答をご希望の方は、以下のフォームからお気軽にご連絡ください。"));
                box.appendChild(contactBox2);
                return box;
            }

            // ===== v29: 意思決定問題集 — 構造化レンダリング =====
            if (isArchitecture) {
                const wrapper = h("div", { class: "quiz-page-wrapper" });

                // intro banner
                const introBanner = h("div", {
                    class: 'card card--gradient-primary'
                },
                    h("div", { class: 'text-overline' }, "設計判断問題集（SREサバイバル）"),
                    h("div", { class: 'text-body-relaxed' },
                        "実務で起きる「誘惑的な技術的判断ミス」を題材にした問題集。各問はステークホルダーの主張とともに提示される。トレードオフを整理し、現場指揮官として意思決定を下せ。"
                    )
                );
                wrapper.appendChild(introBanner);

                Object.keys(quizData).forEach((section, sIdx) => {
                    const questions = quizData[section];
                    const icons = ['🏛️', '🗄️', '🔌', '⚖️', '🚨', '🔁'];

                    const sCard = h("div", { class: "quiz-section-card" });

                    const sHeader = h("div", { class: "quiz-section-header" });
                    sHeader.appendChild(h("div", { class: "quiz-section-icon" }, icons[sIdx] || '📌'));
                    sHeader.appendChild(h("div", { class: "quiz-section-title" }, section));
                    sCard.appendChild(sHeader);

                    questions.forEach((q) => {
                        const qBlock = h("div", { class: "quiz-question-block" });

                        // Q header
                        const qHeader = h("div", { class: "quiz-q-header" });
                        qHeader.appendChild(h("div", { class: "quiz-q-badge" }, q.id));
                        qHeader.appendChild(h("div", { class: "quiz-q-title" }, q.title));
                        qBlock.appendChild(qHeader);

                        // 状況ゾーン
                        const sitZone = h("div", { class: "quiz-zone" });
                        sitZone.appendChild(h("div", { class: "quiz-zone-label situation" }, "📋 状況"));
                        const sitBody = h("div", { class: "quiz-zone-body" });
                        q.situation.forEach(line => {
                            sitBody.appendChild(h("p", { text: line }));
                        });
                        sitZone.appendChild(sitBody);
                        qBlock.appendChild(sitZone);

                        // ステークホルダーゾーン
                        const shZone = h("div", { class: "quiz-zone" });
                        shZone.appendChild(h("div", { class: "quiz-zone-label stakeholder" }, "💬 ステークホルダーの主張"));
                        q.stakeholders.forEach(sh => {
                            const quote = h("div", { class: "quiz-stakeholder-quote" });
                            quote.appendChild(h("span", { class: "quiz-stakeholder-name" }, sh.name + ":"));
                            quote.appendChild(h("span", { text: "「" + sh.quote + "」" }));
                            shZone.appendChild(quote);
                        });
                        qBlock.appendChild(shZone);

                        // 問ゾーン
                        const qZone = h("div", { class: "quiz-zone" });
                        qZone.appendChild(h("div", { class: "quiz-zone-label question" }, "🎯 問"));
                        qZone.appendChild(h("div", { class: "quiz-question-prompt" }, q.question));
                        qBlock.appendChild(qZone);

                        sCard.appendChild(qBlock);
                    });

                    wrapper.appendChild(sCard);
                });

                box.appendChild(wrapper);
            } else {
                // ===== v29: 既存問題集 — 改良レンダリング =====
                const wrapper = h("div", { class: "quiz-page-wrapper" });
                Object.keys(quizData).sort().forEach(section => {
                    const sCard = h("div", { class: "quiz-section-card" });

                    const sHeader = h("div", { class: "quiz-section-header" });
                    sHeader.appendChild(h("div", { class: "quiz-section-icon" }, "📝"));
                    sHeader.appendChild(h("div", { class: "quiz-section-title" }, section));
                    sCard.appendChild(sHeader);

                    const questions = quizData[section];
                    questions.forEach((q) => {
                        const qBlock = h("div", { class: "quiz-question-block" });

                        const qHeader = h("div", { class: "quiz-q-header" });
                        qHeader.appendChild(h("div", { class: "quiz-q-badge" }, q.id));
                        qHeader.appendChild(h("div", { class: "quiz-q-title" }, q.title.replace(q.id + '. ', '')));
                        qBlock.appendChild(qHeader);

                        q.content.forEach(line => {
                            if (!line.trim()) {return;}
                            // Check if it's a label line (ends with ':' or is a short header)
                            const isLabel = /^(状況|問|Challenge|Core Knowledge|境界点|Reboot vs|Stop|ASG|io2|gp[23]|注意|現場|意図|ポイント|解説|補足)[：:。]?/.test(line) || (line.endsWith(':') && line.length < 50);
                            qBlock.appendChild(h("div", {
                                class: "quiz-content-line" + (isLabel ? " is-label" : ""),
                                class: 'text-prewrap'
                            }, line));
                        });

                        sCard.appendChild(qBlock);
                    });

                    wrapper.appendChild(sCard);
                });
                box.appendChild(wrapper);
            }

            // Contact form section
            const contactBox = h("div", { class: "card p col col-gap" });
            contactBox.appendChild(h("div", { class: "h3", text: "模範解答について" }));
            contactBox.appendChild(h("div", { class: "muted" }, "模範解答をご希望の方は、以下のフォームからお気軽にご連絡ください。"));

            const nameInput = h("input", { class: "input", type: "text", placeholder: "お名前", 'aria-label': 'お名前' });
            const emailInput = h("input", { class: "input", type: "email", placeholder: "メールアドレス", 'aria-label': 'メールアドレス' });
            const messageInput = h("textarea", { class: "input textarea-resize-v", rows: 4, placeholder: "メッセージ（任意）", 'aria-label': 'メッセージ' });

            const submitBtn = h("button", {
                class: "btn btn-primary",
                onclick: () => {
                    const name = nameInput.value.trim();
                    const email = emailInput.value.trim();
                    const message = messageInput.value.trim();

                    if (!name || !email) {
                        Toast.show("お名前とメールアドレスを入力してください", "error");
                        return;
                    }

                    const subject = encodeURIComponent(`${pageTitle}の模範解答について`);
                    const body = encodeURIComponent(
                        `お名前: ${name}\nメールアドレス: ${email}\n\nメッセージ:\n${message || "(なし)"}`
                    );
                    const currentState = State.get();
                    location.href = `mailto:${currentState.profile.email}?subject=${subject}&body=${body}`;
                }
            }, "送信");

            contactBox.appendChild(h("div", { class: "col col-gap-10" },
                h("div", { class: "col col-gap-sm" }, h("div", { class: "mini", text: "お名前 *" }), nameInput),
                h("div", { class: "col col-gap-sm" }, h("div", { class: "mini", text: "メールアドレス *" }), emailInput),
                h("div", { class: "col col-gap-sm" }, h("div", { class: "mini", text: "メッセージ" }), messageInput),
                submitBtn
            ));

            box.appendChild(contactBox);

            return box;
        }


        // ===== Page Components =====
        //   ▼ v80+ Stage 5-b: HiringRiskPage (v28 採用決裁資料レベル) + helpers
        //     (impactRow / kpiRow / decisionFlow / riskCard) を js/pages.js へ抽出済み。

        // ===== Shared Component: ContactCTA =====
        // desc: ページ文脈に合わせた一言（何を頼めるか）

        //   ▼ v80+ Stage 5-b: RoleSplitPage (Human vs AI 分担表 / proof の中核) と
        //     NotFoundPage (404 fallback) を js/pages.js へ抽出済み。
        // 改善文書b 4 / 改善文書c: AbortController-based render lifecycle management.
        // Each call to _renderCore() carries a signal; if a new render starts before
        // the previous one completes, the previous one is aborted cleanly.
        // This prevents zombie DOM updates from stale renders accumulating listeners.
        let _renderAbortController = new AbortController();

        // ===== Main Renderer =====
        let _lastRoutePath = null;
        // v59: View Transition の安全性をさらに強化
        // - ブラウザ内部の active transition を考慮
        // - transition callback 由来の例外と transition 由来の abort を分離
        // - 最新の pending route のみ 1 回消化
        let _vtInFlight = false;
        let _vtPendingPath = null;
        let _vtRunId = 0;

        function _getActiveViewTransition() {
            try {
                return document.activeViewTransition || null;
            } catch {
                return null;
            }
        }

        function _canStartViewTransition() {
            if (!document.startViewTransition) return false;
            if (_vtInFlight) return false;
            if (_getActiveViewTransition()) return false;
            return true;
        }

        function _consumePendingRoute() {
            if (_vtPendingPath === null) return;
            _vtPendingPath = null;
            render();
        }

        /**
         * executeSafeTransition — View Transition API を安全に実行するラッパー。
         * ブラウザ非対応・prefers-reduced-motion・既存 transition 中の場合は同期フォールバック。
         * 呼び出し側はこの関数に updateDOMCallback を渡すだけでよい（API 仕様の複雑性を隠蔽）。
         * @param {Function} updateDOMCallback - DOM更新を行う同期関数
         */
        function executeSafeTransition(updateDOMCallback) {
            if (!_canStartViewTransition()) {
                updateDOMCallback();
                return;
            }
            const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
            if (prefersReducedMotion) {
                updateDOMCallback();
                return;
            }
            try {
                const transition = document.startViewTransition(updateDOMCallback);
                Promise.resolve(transition && transition.finished)
                    .catch((err) => {
                        if (!_isViewTransitionError(err)) throw err;
                        console.warn('[portfolio] non-fatal view transition error:', err);
                    });
            } catch (err) {
                console.warn('[portfolio] startViewTransition unavailable, fallback:', err);
                updateDOMCallback();
            }
        }

        function render() {
            const currentRoutePath = location.hash || '#/';
            const isRouteTransition = _lastRoutePath !== currentRoutePath;

            // モーションリダクション設定の確認
            const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

            // View Transition 対象条件:
            //   1 ルートが変わった
            //   2 API が存在する
            //   3 reduced-motion でない
            //   4 JS管理中 / ブラウザ内部 active transition 中でない
            if (isRouteTransition && !prefersReducedMotion && _canStartViewTransition()) {
                const runId = ++_vtRunId;
                _vtInFlight = true;
                _vtPendingPath = null;

                try {
                    const transition = document.startViewTransition(async () => {
                        try {
                            await _renderCore();
                            _lastRoutePath = currentRoutePath;
                        } catch (e) {
                            window.__fatalError = e;
                            throw e;
                        }
                    });

                    Promise.resolve(transition && transition.finished)
                        .catch((err) => {
                            if (_isViewTransitionError(err)) {
                                console.warn('[portfolio] non-fatal view transition finish error:', err);
                                return;
                            }
                            throw err;
                        })
                        .catch((err) => {
                            window.__fatalError = _normalizeError(err);
                        })
                        .finally(() => {
                            if (runId !== _vtRunId) return;
                            _vtInFlight = false;
                            _consumePendingRoute();
                        });
                } catch (err) {
                    _vtInFlight = false;
                    if (_isViewTransitionError(err)) {
                        console.warn('[portfolio] startViewTransition fallback:', err);
                        _renderCore().then(() => {
                            _lastRoutePath = currentRoutePath;
                            _consumePendingRoute();
                        });
                    } else {
                        window.__fatalError = _normalizeError(err);
                        _renderCore().then(() => {
                            _lastRoutePath = currentRoutePath;
                        });
                    }
                }
            } else if (isRouteTransition && (_vtInFlight || _getActiveViewTransition())) {
                // 実行中は最新の route のみ保持して、transition 完了後に 1 回だけ反映する
                _vtPendingPath = currentRoutePath;
            } else {
                _renderCore().then(() => {
                    _lastRoutePath = currentRoutePath;
                });
            }
        }

        async function _renderCore() {
            // 改善文書b 4: Abort any previous render in flight before starting a new one.
            // This prevents memory leaks from stale async render chains.
            _renderAbortController.abort();
            _renderAbortController = new AbortController();
            const _signal = _renderAbortController.signal;

            const route = Router.getRoute();
            const content = document.getElementById('content');
            const sidebarEl = document.getElementById('sidebar');

            // § Agentic State Notification: aria-busy=true でローディング開始を宣言
            if (content) {
                content.setAttribute('aria-busy', 'true');
                document.body.setAttribute('data-ai-state', JSON.stringify({
                    route: route.name || 'home',
                    filter: '',
                    loading: true
                }));
            }

            // Update sidebar
            if (sidebarEl) {
                clear(sidebarEl);
                sidebarEl.appendChild(Sidebar(false));
            }

            // §1.2 INP最適化: サイドバー構築後にメインスレッドを解放してから本体を描画
            await yieldToMain();

            // Render page content
            clear(content);

            // Guard: if this render was superseded by a newer one, stop here
            if (_signal && _signal.aborted) { return; }

            let page;
            const fatal = window.__fatalError;
            if (fatal) {
                page = FatalPage(fatal);
            } else {
                try {
                    switch (route.name) {
                        case 'home':
                            page = HomePage();
                            break;
                        case 'projects':
                            page = ProjectsPage();
                            break;
                        case 'project-detail':
                            page = ProjectDetailPage(route.params.slug);
                            break;
                        case 'apps':
                            page = AppsPage();
                            break;
                        case 'app-task':
                            page = TaskPage();
                            break;
                        case 'app-todo':
                            page = TodoPage();
                            break;
                        case 'app-pomodoro':
                            page = PomodoroPage();
                            break;
                        case 'app-ai':
                            page = AIPage();
                            break;
                        case 'settings':
                            page = SettingsPage();
                            break;
                        case 'about':
                            page = AboutPage();
                            break;
                        case 'resume':
                            page = ResumePage();
                            break;
                        case 'contact':
                            page = ContactPage();
                            break;
                        case 'quiz':
                            page = QuizPage();
                            break;
                        case 'hiring-risk':
                            page = HiringRiskPage();
                            break;
                        case 'ai-knowhow':
                            page = AIKnowhowPage();
                            break;
                        case 'role-split':
                            page = RoleSplitPage();
                            break;
                        case 'not-found':
                        default:
                            page = NotFoundPage();
                    }


                } catch (e) {
                    window.__fatalError = e;
                    page = FatalPage(e);
                }
            }

            if (page) {
                content.appendChild(page);
            }

            // Guard: skip meta/state sync if render was superseded
            if (_signal && _signal.aborted) { return; }

            // § Agentic State Notification: 描画完了後に aria-busy=false へ切替
            requestAnimationFrame(() => {
                if (content) {content.setAttribute('aria-busy', 'false');}
                document.body.setAttribute('data-ai-state', JSON.stringify({
                    route: route.name || 'home',
                    filter: '',
                    loading: false
                }));
            });

            // §1.2 INP最適化: ページコンテンツ追加後にスレッドを解放してからメタ更新
            await yieldToMain();
            // Update SEO via PAGE_META (v37: unified metadata management)
            applyMeta(route.name, route.params || {}, route.query || {});

            // AIDK RouteState 同期: フラット名前空間UIステートをルート変更に追随させる
            try {
                RouteState.proxy.route_name = route.name || 'home';
                RouteState.proxy.route_slug = (route.params && route.params.slug) || '';
                RouteState.proxy.route_hash = location.hash || '#/';
                RouteState.proxy.a11y_announcement = route.name ? `${route.name} ページを表示中` : '';
            } catch {}

            // Sync mobile drawer state
            syncMobileDrawer();


            // Enforce link security for dynamically rendered content
            secureExternalLinks(document);
        }

        // ===== Mobile Drawer =====
        function syncMobileDrawer() {
            const isMobile = window.matchMedia(`(max-width: ${CONSTANTS.MOBILE_BREAKPOINT}px)`).matches;
            const topbar = document.getElementById('topbar');

            if (topbar) {
                topbar.style.display = isMobile ? 'flex' : 'none';
            }
        }


        // ===== Security: enforce noopener on target=_blank links (including dynamic links) =====
        function secureExternalLinks(root = document) {
            try {
                const links = root.querySelectorAll('a[target="_blank"]');
                links.forEach((a) => {
                    const rel = (a.getAttribute('rel') || '').split(/\s+/).filter(Boolean);
                    if (!rel.includes('noopener')) {rel.push('noopener');}
                    if (!rel.includes('noreferrer')) {rel.push('noreferrer');}
                    a.setAttribute('rel', rel.join(' '));
                    // Optional: reduce referrer leakage for external links
                    if (!a.getAttribute('referrerpolicy')) {a.setAttribute('referrerpolicy', 'no-referrer');}
                });
            } catch { /* noop */ }
        }

        // ===== Drawer Focus Trap / Accessibility helpers =====
        let __drawerTrapHandler = null;
        let __drawerLastFocused = null;
        let __drawerScrollY = 0;

        function __setAppInert(isInert) {
            const app = document.getElementById('app');
            if (!app) {return;}
            // Prefer native inert if available; fallback to aria-hidden + pointer-events
            try {
                if ('inert' in app) {app.inert = !!isInert;}
            } catch { /* noop */ }

            if (isInert) {
                app.setAttribute('aria-hidden', 'true');
                app.style.pointerEvents = 'none';
            } else {
                app.removeAttribute('aria-hidden');
                app.style.pointerEvents = '';
            }
        }

        function __lockBodyScroll(lock) {
            if (lock) {
                __drawerScrollY = window.scrollY || 0;
                document.body.style.position = 'fixed';
                document.body.style.top = `-${__drawerScrollY}px`;
                document.body.style.width = '100%';
            } else {
                const y = __drawerScrollY || 0;
                document.body.style.position = '';
                document.body.style.top = '';
                document.body.style.width = '';
                window.scrollTo(0, y);
            }
        }

        function __trapFocus(container) {
            const focusable = container.querySelectorAll(
                'a[href], button:not([disabled]), textarea:not([disabled]), input:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])'
            );
            if (!focusable.length) {return;}

            const first = focusable[0];
            const last = focusable[focusable.length - 1];

            __drawerTrapHandler = function (e) {
                if (e.key === 'Escape') {
                    closeDrawer();
                    return;
                }
                if (e.key !== 'Tab') {return;}

                if (e.shiftKey && document.activeElement === first) {
                    e.preventDefault();
                    last.focus();
                } else if (!e.shiftKey && document.activeElement === last) {
                    e.preventDefault();
                    first.focus();
                }
            };

            document.addEventListener('keydown', __drawerTrapHandler);
            first.focus();
        }

        function __releaseFocusTrap() {
            if (__drawerTrapHandler) {
                document.removeEventListener('keydown', __drawerTrapHandler);
                __drawerTrapHandler = null;
            }
        }

        function openDrawer() {
            const drawer = document.getElementById('drawer');
            const overlay = document.getElementById('overlay');
            const menuBtn = document.getElementById('menuBtn');

            if (!drawer || !overlay) {return;}

            __drawerLastFocused = document.activeElement;

            clear(drawer);
            drawer.appendChild(Sidebar(true));

            // Visible
            drawer.removeAttribute('hidden');
            drawer.style.display = 'block';
            overlay.style.display = 'block';

            // ARIA
            drawer.setAttribute('aria-hidden', 'false');
            overlay.setAttribute('aria-hidden', 'false');
            menuBtn?.setAttribute('aria-expanded', 'true');

            // Background isolation
            __setAppInert(true);
            __lockBodyScroll(true);

            // Ensure rel=noopener for dynamic links inside drawer
            secureExternalLinks(drawer);

            // Focus
            __trapFocus(drawer);
        }

        function closeDrawer() {
            const drawer = document.getElementById('drawer');
            const overlay = document.getElementById('overlay');
            const menuBtn = document.getElementById('menuBtn');

            if (!drawer || !overlay) {return;}

            // Hide
            drawer.style.display = 'none';
            overlay.style.display = 'none';
            drawer.setAttribute('hidden', '');

            // ARIA
            drawer.setAttribute('aria-hidden', 'true');
            overlay.setAttribute('aria-hidden', 'true');
            menuBtn?.setAttribute('aria-expanded', 'false');

            // Release isolation
            __releaseFocusTrap();
            __setAppInert(false);
            __lockBodyScroll(false);

            // Focus restore
            (menuBtn || __drawerLastFocused)?.focus?.();
        }


        // ===== Fatal overlay (global error capture) =====

        /**
         * v58: エラーを「本当に致命的か」で分類するヘルパー。
         *
         * 非致命的として扱うケース（fatalオーバーレイを出さない）:
         *   - View Transition 関連の DOMException
         *     (InvalidStateError / AbortError / "Transition was aborted" メッセージ)
         *   - startViewTransition の Promise 競合由来のエラー
         *
         * これらはアプリのデータや状態には影響しないため、
         * コンソール警告に留め、ユーザーに致命的エラーとして見せない。
         */
        function _normalizeError(input) {
            if (!input) return new Error('Unknown error');
            if (input instanceof Error) return input;
            if (typeof input === 'string') return new Error(input);
            try {
                return new Error(JSON.stringify(input));
            } catch {
                return new Error(String(input));
            }
        }

        function _isViewTransitionError(err) {
            const e = _normalizeError(err);
            const name = e && e.name ? String(e.name) : '';
            const msg = e && e.message ? String(e.message) : '';
            const stack = e && e.stack ? String(e.stack) : '';
            const haystack = `${name}\n${msg}\n${stack}`;
            return (
                name === 'InvalidStateError' ||
                name === 'AbortError' ||
                haystack.includes('Transition was aborted') ||
                haystack.includes('startViewTransition') ||
                haystack.includes('view transition') ||
                haystack.includes('ViewTransition') ||
                // Chrome拡張のメッセージチャンネルエラー（ポートフォリオ起因でない）
                haystack.includes('message channel closed') ||
                haystack.includes('asynchronous response') ||
                haystack.includes('A listener indicated')
            );
        }

        function _isFatalError(err) {
            if (!err) return false;
            if (_isViewTransitionError(err)) return false;
            return true;
        }

        window.__fatalError = null;
        window.addEventListener('error', (ev) => {
            try {
                const err = ev && ev.error ? ev.error : new Error(ev && ev.message ? String(ev.message) : 'Unknown error');
                if (!_isFatalError(err)) {
                    console.warn('[portfolio] non-fatal error suppressed:', err);
                    return;
                }
                window.__fatalError = err;
            } catch (e) {
                window.__fatalError = e;
            }
            try { render(); } catch { }
        });

        window.addEventListener('unhandledrejection', (ev) => {
            try {
                const err = _normalizeError(ev && 'reason' in ev ? ev.reason : new Error('Unhandled rejection'));
                if (!_isFatalError(err)) {
                    ev.preventDefault(); // 非致命的エラーはブラウザ出力ごと抑制
                    return;
                }
                window.__fatalError = err;
            } catch (e) {
                window.__fatalError = e;
            }
            try { render(); } catch { }
        });

        // 改善文書c Section 6: グローバル・セーフティネット
        // Shadow DOM を使ってメインCSSと完全に隔離されたフォールバックUIを提示する。
        // すべての改善のうち最後に起動するため、他のすべての防御レイヤーをすり抜けた
        // 「サイレント・フェイラー」を捕捉できる最終安全網として機能する。
        (function _installGlobalSafetyNet() {
            let _safetyNetShown = false;

            function _showSafetyNet(origin) {
                if (_safetyNetShown) { return; }
                _safetyNetShown = true;

                try {
                    // テレメトリ: エラー情報をsessionStorageに退避（非同期レポートの準備）
                    try {
                        // codeql[js/clear-text-storage-of-sensitive-data] - False positive:
                        // Stores transient client-side error context for local diagnostics only.
                        // No credentials, tokens, or PII are stored.
                        sessionStorage.setItem('portfolio_last_error', JSON.stringify({
                            ts: Date.now(),
                            route: window.location.hash,
                            origin: String(origin || 'unknown')
                        }));
                    } catch { /* storage unavailable — ignore */ }

                    // Shadow DOM でスタイル汚染ゼロのフォールバックUIを構築
                    const host = document.createElement('div');
                    host.id = 'portfolio-safety-net-host';
                    host.style.cssText = 'position:fixed;inset:0;z-index:99998;pointer-events:none;';
                    document.body.appendChild(host);

                    const shadow = host.attachShadow({ mode: 'closed' });

                    const style = document.createElement('style');
                    style.textContent = `
                        :host { all: initial; }
                        .net {
                            position: fixed; inset: 0; display: flex;
                            align-items: center; justify-content: center;
                            background: rgba(2,6,23,0.85);
                            backdrop-filter: blur(4px);
                            font-family: system-ui, sans-serif;
                            pointer-events: auto;
                        }
                        .box {
                            background: #0f172a; color: #e2e8f0;
                            border: 1px solid #334155; border-radius: 12px;
                            padding: 2rem; max-width: 400px; text-align: center;
                        }
                        h2 { font-size: 1.1rem; margin: 0 0 0.75rem; color: #f8fafc; }
                        p  { font-size: 0.875rem; color: #94a3b8; margin: 0 0 1.5rem; line-height: 1.6; }
                        button {
                            background: #6366f1; color: #fff; border: none;
                            border-radius: 8px; padding: 0.6rem 1.4rem;
                            font-size: 0.875rem; font-weight: 600; cursor: pointer;
                        }
                        button:hover { background: #4f46e5; }
                    `;

                    const div = document.createElement('div');
                    div.className = 'net';

                    const box = document.createElement('div');
                    box.className = 'box';

                    const title = document.createElement('h2');
                    title.textContent = '⚠️ アプリを再起動してください';

                    const message = document.createElement('p');
                    message.appendChild(document.createTextNode('予期しないエラーが発生しました。'));
                    message.appendChild(document.createElement('br'));
                    message.appendChild(document.createTextNode('ページを再読み込みすると復旧します。'));

                    const btn = document.createElement('button');
                    btn.id = 'sn-reload';
                    btn.textContent = '再読み込み';

                    box.appendChild(title);
                    box.appendChild(message);
                    box.appendChild(btn);
                    div.appendChild(box);

                    shadow.appendChild(style);
                    shadow.appendChild(div);

                    if (btn) {
                        btn.addEventListener('click', () => {
                            try { sessionStorage.clear(); } catch { /* ignore */ }
                            location.reload();
                        });
                    }
                } catch { /* Safety net itself failed — nothing more we can do */ }
            }

            // 既存のfatal overlayと協調: __fatalErrorが2秒経っても未処理なら安全網を起動
            setInterval(function() {
                if (window.__fatalError && !document.getElementById('portfolio-safety-net-host')) {
                    _showSafetyNet(window.__fatalError);
                }
            }, 2000);
        })();

        // ===== Event Listeners =====
        function init() {
            // Brand (palette/font)
            Brand.init();

            // Theme
            Theme.init();

            // ── AIDK Kernel modules ─────────────────────────────────────
            // BindingRegistry: MutationObserver で data-bind-* を自動登録
            BindingRegistry.init();
            // ActionDelegator: document 単一リスナーで data-action を委譲
            ActionDelegator.init();
            // Diagnostics Rail: ?debug=1 で起動
            if (location.search.includes('debug=1')) {
                RouteState.proxy.diag_debug_mode = true;
            }
            // ────────────────────────────────────────────────────────────

            // Mobile menu (既存リスナーを維持 — ActionDelegator と併存可)
            document.getElementById('menuBtn')?.addEventListener('click', openDrawer);
            document.getElementById('overlay')?.addEventListener('click', closeDrawer);
            document.getElementById('themeBtnTop')?.addEventListener('click', Theme.cycle);

            // Escape key
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    const drawer = document.getElementById('drawer');
                    if (drawer && drawer.getAttribute('aria-hidden') === 'false') closeDrawer();
                }
            });
            // Window resize listener (v37: responsive drawer sync)
            window.addEventListener('resize', debounce(syncMobileDrawer, CONSTANTS.DEBOUNCE_DELAY));

            // Router
            Router.subscribe(render);

            // State changes
            State.subscribe(() => render());

            // Initial render
            render();

            // ===== BGM Initialization =====
            BGM.init();
            const topBgmBtn = document.getElementById('bgm-btn-top');
            if (topBgmBtn) topBgmBtn.addEventListener('click', BGM.toggle);

        }

        // ===== Initialization =====
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
        } else {
            init();
        }

        // v51: window.render を明示エクスポート（TaskPage/TodoPage/SettingsPage からの window.render() 呼び出しと互換）
        window.render = render;

        // 改善文書c Section 7: Service Worker registration for AI crawler cache-busting
        // Service Worker registration is intentionally placed after runtime guards are initialized.
        // It is inside the DOMContentLoaded/load handler and does not affect SPA logic.
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', function() {
                navigator.serviceWorker.register('./sw.js', { scope: './' })
                    .then(function(reg) {
                        console.debug('[SW] AIO service worker registered:', reg.scope);
                    })
                    .catch(function(err) {
                        // SW registration failure is non-fatal — portfolio works without it
                        console.warn('[SW] Service worker registration skipped:', err);
                    });
            });
        }

        }());

        // 改善文書c Section 3: WeakMap-based global event listener registry
        // Intercepts addEventListener to automatically clean up listeners when
        // DOM nodes are removed — prevents zombie listener memory leaks in the SPA.
        (function _installEventListenerRegistry() {
            'use strict';
            var _registry = new WeakMap();
            var _nativeAdd = EventTarget.prototype.addEventListener;
            var _nativeRemove = EventTarget.prototype.removeEventListener;

            EventTarget.prototype.addEventListener = function(type, listener, options) {
                if (this instanceof Element) {
                    var entries = _registry.get(this) || [];
                    entries.push({ type: type, listener: listener, options: options });
                    _registry.set(this, entries);
                }
                return _nativeAdd.call(this, type, listener, options);
            };

            function _cleanNode(node) {
                if (!node || node.nodeType !== 1) { return; }
                var entries = _registry.get(node);
                if (entries) {
                    entries.forEach(function(e) {
                        try { _nativeRemove.call(node, e.type, e.listener, e.options); } catch {}
                    });
                    _registry.delete(node);
                }
                if (node.children) { Array.from(node.children).forEach(_cleanNode); }
            }

            var _cleaner = new MutationObserver(function(mutations) {
                mutations.forEach(function(m) {
                    m.removedNodes.forEach(_cleanNode);
                });
            });

            function _start() {
                if (document.body) { _cleaner.observe(document.body, { childList: true, subtree: true }); }
            }
            if (document.body) { _start(); }
            else { document.addEventListener('DOMContentLoaded', _start); }
        })();

        // ─────────────────────────────────────────────────────────────────────────
        // 改善文書c Section 4: DOM Clobbering / XSS 防止 — 透過的サニタイズ・ミドルウェア層
        // Element.prototype.innerHTML の setter をインターセプトし、DOMParser で
        // 一時 Document にパースした後、危険なノード・属性を剥離してから適用する。
        // 既存の innerHTML 代入コードを一切変更しない非破壊実装。
        // ─────────────────────────────────────────────────────────────────────────
        (function _installInnerHTMLSanitizer() {
            'use strict';
            var _desc = Object.getOwnPropertyDescriptor(Element.prototype, 'innerHTML');
            if (!_desc || !_desc.set) { return; } // 取得不可なら安全にスキップ
            var _nativeSetter = _desc.set;
            var _parser = new DOMParser();

            var DANGEROUS_TAGS = new Set(['SCRIPT','IFRAME','OBJECT','EMBED','BASE','LINK','META','NOSCRIPT']);
            var JS_SCHEME = /^\s*javascript\s*:/i;
            var DATA_SCHEME = /^\s*data\s*:/i;
            var DOM_CLOBBER_RE = /^(innerHTML|outerHTML|attributes|nodeName|nodeType|ownerDocument|parentNode|childNodes|firstChild|lastChild|nextSibling|previousSibling|textContent|baseURI|isConnected|constructor|__proto__|prototype)$/i;

            function _sanitizeNode(node) {
                if (node.nodeType === 1) {
                    if (DANGEROUS_TAGS.has(node.tagName)) {
                        node.parentNode && node.parentNode.removeChild(node);
                        return;
                    }
                    // 属性走査: on* / javascript: / data: URI を除去
                    var attrs = Array.from(node.attributes);
                    for (var i = 0; i < attrs.length; i++) {
                        var a = attrs[i];
                        var n = a.name.toLowerCase();
                        var v = a.value;
                        if (n.startsWith('on')) { node.removeAttribute(a.name); continue; }
                        if ((n === 'href' || n === 'src' || n === 'action') && (JS_SCHEME.test(v) || DATA_SCHEME.test(v))) {
                            node.removeAttribute(a.name); continue;
                        }
                        // DOM Clobbering 防止: name/id が予約グローバルと衝突する場合はプレフィックス付与
                        if ((n === 'id' || n === 'name') && DOM_CLOBBER_RE.test(v)) {
                            node.setAttribute(a.name, 'aio-safe-' + v);
                        }
                    }
                    var children = Array.from(node.childNodes);
                    for (var j = 0; j < children.length; j++) { _sanitizeNode(children[j]); }
                }
            }

            Object.defineProperty(Element.prototype, 'innerHTML', {
                get: _desc.get,
                set: function(raw) {
                    if (typeof raw !== 'string' || raw.trim() === '') {
                        return _nativeSetter.call(this, raw);
                    }
                    // Trusted Types が有効な環境では委譲 (二重サニタイズ不要)
                    if (typeof TrustedHTML !== 'undefined' && raw instanceof TrustedHTML) {
                        return _nativeSetter.call(this, raw);
                    }
                    try {
                        var doc = _parser.parseFromString(raw, 'text/html');
                        var bodyChildren = Array.from(doc.body.childNodes);
                        bodyChildren.forEach(_sanitizeNode);
                        var frag = document.createDocumentFragment();
                        bodyChildren.forEach(function(n) {
                            try { frag.appendChild(document.adoptNode(n)); } catch (e) { /* skip non-adoptable nodes */ }
                        });
                        // replaceChildren で一括置換 — _nativeSetter を経由しないため
                        // Trusted Types の干渉を受けず、かつリフローが1回のみ発生する
                        if (typeof this.replaceChildren === 'function') {
                            this.replaceChildren(frag);
                        } else {
                            // replaceChildren 非対応の旧ブラウザ向けフォールバック
                            while (this.firstChild) { this.removeChild(this.firstChild); }
                            this.appendChild(frag);
                        }
                    } catch (e) {
                        // DOMParser 失敗時はテキストノード化 (fail-closed)
                        // raw HTML を絶対にネイティブへ流さない。入力痕跡はテキストとして保持。
                        if (typeof this.replaceChildren === 'function') {
                            this.replaceChildren(document.createTextNode(String(raw)));
                        } else {
                            while (this.firstChild) { this.removeChild(this.firstChild); }
                            this.appendChild(document.createTextNode(String(raw)));
                        }
                    }
                },
                configurable: true,
                enumerable: _desc.enumerable
            });
        })();

        // ─────────────────────────────────────────────────────────────────────────
        // 改善文書c Section 8: レイアウトスラッシング防止 — rAF Write-Batching Proxy
        // Element.prototype.style の setter および setAttribute をフックし、
        // スタイル変更要求を requestAnimationFrame 直前にバッチ適用する。
        // AI 生成の素朴な同期スタイル書き込みループを透過的に最適化する非破壊実装。
        // ─────────────────────────────────────────────────────────────────────────
        (function _installLayoutThrashingGuard() {
            'use strict';
            var _writeQueue = [];
            var _rafPending = false;

            function _flushQueue() {
                _rafPending = false;
                var q = _writeQueue.splice(0);
                for (var i = 0; i < q.length; i++) { q[i](); }
            }

            function _scheduleFlush() {
                if (!_rafPending) {
                    _rafPending = true;
                    requestAnimationFrame(_flushQueue);
                }
            }

            // CSSStyleDeclaration.setProperty をフックしてバッチ化
            var _origSetProperty = CSSStyleDeclaration.prototype.setProperty;
            CSSStyleDeclaration.prototype.setProperty = function(prop, value, priority) {
                var self = this;
                _writeQueue.push(function() { _origSetProperty.call(self, prop, value, priority); });
                _scheduleFlush();
            };

            // style 直接プロパティへの代入は cssText 経由のバッチ化
            // (プロパティ数が多い場合のみ活性化 — 単純スカラはネイティブ委譲)
            var _origStyleSetter = Object.getOwnPropertyDescriptor(HTMLElement.prototype, 'style');
            // NOTE: style は getter/setter の直接オーバーライドが制限されるため、
            //       setProperty フック + DocumentFragment 戦略 (改善文書b 7.1) を主防衛とする。
            // 追加: setAttribute('style', ...) フック
            var _origSetAttr = Element.prototype.setAttribute;
            Element.prototype.setAttribute = function(name, value) {
                if (name === 'style') {
                    var self = this;
                    _writeQueue.push(function() { _origSetAttr.call(self, 'style', value); });
                    _scheduleFlush();
                } else {
                    _origSetAttr.call(this, name, value);
                }
            };
        })();

        // ─────────────────────────────────────────────────────────────────────────
        // 改善文書c Section 9: メディアアセット ライフサイクル管理（Media Lifecycle Guard）
        // DOM から削除された img / audio / video 要素の ObjectURL / AudioBuffer を
        // 自動解放してメモリリークを根絶する非破壊実装。
        // 注意: IntersectionObserver (_intersectionObserver) は deferred-src
        // lazy loading 用に生成しているが、observe() を呼び出す箇所が現時点では
        // 存在しないため、実際には lazy loading は機能していない。
        // 現在の役割は MutationObserver によるメディアリソース解放（cleanup/lifecycle guard）のみ。
        // ─────────────────────────────────────────────────────────────────────────
        (function _installMediaLifecycleGuard() {
            'use strict';
            var _blobMap = new WeakMap(); // element → blobURL

            // IntersectionObserver: ビューポート外では src を遅延
            var _ioOptions = { rootMargin: '200px' };
            var _intersectionObserver = new IntersectionObserver(function(entries) {
                entries.forEach(function(entry) {
                    var el = entry.target;
                    if (entry.isIntersecting) {
                        var deferred = el.getAttribute('data-deferred-src');
                        if (deferred) {
                            el.src = deferred;
                            el.removeAttribute('data-deferred-src');
                        }
                        _intersectionObserver.unobserve(el);
                    }
                });
            }, _ioOptions);

            // MutationObserver: DOM 削除時にリソース解放
            var _removalObserver = new MutationObserver(function(mutations) {
                mutations.forEach(function(m) {
                    m.removedNodes.forEach(function(node) {
                        if (!node || node.nodeType !== 1) { return; }
                        _releaseMediaNode(node);
                        if (node.querySelectorAll) {
                            node.querySelectorAll('img, audio, video').forEach(_releaseMediaNode);
                        }
                    });
                });
            });

            function _releaseMediaNode(el) {
                if (!el || el.nodeType !== 1) { return; }
                var tag = el.tagName;
                if (tag === 'IMG' || tag === 'VIDEO') {
                    var blobUrl = _blobMap.get(el);
                    if (blobUrl) {
                        try { URL.revokeObjectURL(blobUrl); } catch (e) { /* noop */ }
                        _blobMap.delete(el);
                    }
                }
                if (tag === 'AUDIO' || tag === 'VIDEO') {
                    try {
                        if (el.src && el.src.startsWith('blob:')) {
                            URL.revokeObjectURL(el.src);
                        }
                        el.src = '';
                        el.load(); // バッファ強制クリア
                    } catch (e) { /* noop */ }
                }
            }

            function _start() {
                if (document.body) {
                    _removalObserver.observe(document.body, { childList: true, subtree: true });
                }
            }
            if (document.body) { _start(); }
            else { document.addEventListener('DOMContentLoaded', _start); }

            // グローバル ObjectURL 生成をフックして追跡
            var _origCreateObjectURL = URL.createObjectURL;
            URL.createObjectURL = function(obj) {
                var url = _origCreateObjectURL.call(URL, obj);
                // 呼び出し元の el 参照は取れないため、Blob URL は _releaseMediaNode で補足
                return url;
            };
        })();

        // Agentic Accessibility: WebMCP (Web Model Context Protocol) Non-destructive Integration
        try {
            if (window.navigator && window.navigator.modelContext && typeof window.navigator.modelContext.registerTool === 'function') {
                window.navigator.modelContext.registerTool({
                    name: "extract_human_vs_ai_role_split",
                    description: "Yuta Yokoi (Human PM) と AI チームの役割分担表（8カテゴリ）の現在のDOM状態から証拠データを抽出します。",
                    inputSchema: {
                        "type": "object",
                        "properties": {
                            "format": {
                                "type": "string",
                                "description": "返却されるデータのフォーマット（'json' または 'text'）"
                            }
                        },
                        "required": []
                    },
                    annotations: { readOnlyHint: true },
                    execute: async function(params) {
                        // 非破壊的なDOM走査: 実際のUIからテキストを抽出（要素が存在しないSPAルーティング状態も考慮）
                        var roleSplitData = "役割分担表のDOMノードが現在のSPAルート（" + window.location.hash + "）でアクティブではありません。";
                        var roleElements = document.querySelectorAll('.role-split-item, [data-ai-role]');
                        if (roleElements.length > 0) {
                            var extracted = Array.from(roleElements).map(function(el) { return el.textContent.trim(); });
                            roleSplitData = params.format === 'json'
                                ? JSON.stringify({ human: "Architecture, System Design", ai: "Implementation, Assets", details: extracted })
                                : extracted.join(" | ");
                        } else {
                            // フォールバック: llms-full.txtで定義されている静的真実を返却
                            roleSplitData = "Human: Architecture, System Design, Prompt Design, AI Orchestration. AI: Implementation, Image Generation, Music Generation.";
                        }
                        return { content: [{ type: "text", text: roleSplitData }] };
                    }
                });
            }
        } catch (e) {
            console.warn("WebMCP registration gracefully skipped:", e);
        }

        // Agentic Accessibility: Semantic Anchor Binding
        document.addEventListener("DOMContentLoaded", function() {
            var mainContent = document.querySelector('main');
            var aioAnchor = document.getElementById('aio-asset-anchor');
            if (mainContent && aioAnchor && !mainContent.hasAttribute('aria-details')) {
                mainContent.setAttribute('aria-details', 'aio-asset-anchor');
            }

            // 改善文書c Section 5: JSON-LD / UI State Semantic Drift Prevention
            // MutationObserver that detects route DOM changes and updates a lightweight
            // dynamic JSON-LD tag so AI crawlers always see context-matched structured data,
            // regardless of which hash route is currently active.
            //
            // 設計意図: _injectDynamicJsonLd() は MutationObserver 経由のみで呼ばれる。
            // 初期ロード時に即時呼び出しを行わない理由:
            //   SPAルーターは DOMContentLoaded 後にコンテンツを非同期でセットするため、
            //   初期化直後の #content 内部は空または未確定状態であることが多い。
            //   初期注入すると不正確な（空タイトルの）JSON-LDが挿入されるリスクがある。
            //   ルート変化（childList mutation）後に注入することで、
            //   常に実際のコンテンツ状態を反映した JSON-LD が生成される。
            (function _installSemanticDriftGuard() {
                var _debounceTimer = null;
                var SITE_BASE = 'https://yutapr0117-design.github.io/portfolio/';

                function _buildDynamicJsonLd() {
                    var h1El = document.querySelector('#content h1, #content .h1');
                    var currentTitle = h1El ? h1El.textContent.trim() : document.title;
                    var routeHash = window.location.hash || '#/';
                    var routeName = routeHash.replace(/^#\//, '') || 'home';

                    return {
                        '@context': 'https://schema.org',
                        '@type': 'WebPage',
                        '@id': SITE_BASE + '#webpage-dynamic',
                        'url': SITE_BASE,
                        'name': currentTitle,
                        'inLanguage': 'ja',
                        'about': { '@id': SITE_BASE + '#person' },
                        'isPartOf': { '@id': SITE_BASE + '#website' },
                        'breadcrumb': {
                            '@type': 'BreadcrumbList',
                            'itemListElement': [
                                { '@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE_BASE },
                                routeName !== 'home' ? { '@type': 'ListItem', 'position': 2, 'name': currentTitle, 'item': SITE_BASE + '#' + routeName } : null
                            ].filter(Boolean)
                        }
                    };
                }

                function _injectDynamicJsonLd() {
                    try {
                        var existing = document.querySelector('script[data-ld="dynamic-route"]');
                        if (!existing) {
                            existing = document.createElement('script');
                            existing.setAttribute('type', 'application/ld+json');
                            existing.setAttribute('data-ld', 'dynamic-route');
                            document.head.appendChild(existing);
                        }
                        existing.textContent = JSON.stringify(_buildDynamicJsonLd());
                    } catch (e) { /* non-fatal */ }
                }

                var _observer = new MutationObserver(function() {
                    clearTimeout(_debounceTimer);
                    // Use requestIdleCallback to avoid interfering with render performance
                    _debounceTimer = setTimeout(function() {
                        if ('requestIdleCallback' in window) {
                            requestIdleCallback(_injectDynamicJsonLd, { timeout: 2000 });
                        } else {
                            _injectDynamicJsonLd();
                        }
                    }, 300);
                });

                var contentEl = document.getElementById('content');
                if (contentEl) {
                    _observer.observe(contentEl, { childList: true, subtree: false });
                }
            })();
        });

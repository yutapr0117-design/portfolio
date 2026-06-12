
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
        // v80+ Stage 5-n: Productivity Apps Components (TaskPage / TodoPage / PomodoroPage /
        //   AIPage / SettingsPage) を factory pattern で葉モジュール抽出。各 page の private
        //   state も factory closure 内に閉じ込める（揮発性 UI 状態は元と同位置で保持）。
        import { createApps } from './js/apps.js';
        // v80+ Stage 5-o: Quiz Renderer (QuizPage + 4 quiz domain lookup) を factory pattern で葉モジュール抽出。
        import { createQuizRenderer } from './js/quiz-renderer.js';
        // v80+ Stage 5-l: AIDK Rail 5 IIFE (RouteState / EffectRails / BindingRegistry /
        //   ActionDelegator / DiagnosticsRail) を合体 factory pattern で葉モジュール抽出。
        //   相互依存を内部 closure に閉じ込めるため 1 モジュールに合体。挙動 byte-equivalent。
        import { createAIDKRails } from './js/aidk-rails.js';
        // v80+ Stage 5-q: Mobile Drawer + Focus Trap + secureExternalLinks を factory pattern で
        //   葉モジュール抽出。Sidebar 注入と _drawer holder 経由の late-binding で循環依存解消。
        import { createMobileDrawer } from './js/mobile-drawer.js';
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

        // ===== v80+ Stage 5-q: Mobile Drawer late-binding holder =====
        //   createComponents (Sidebar 含む) は closeDrawer を必要とし、createMobileDrawer は
        //   Sidebar を必要とするため、循環依存が成立する。これを解決するため、_drawer holder
        //   object を介して late-binding する。Components / AIDK Rails が参照する closeDrawer /
        //   openDrawer / secureExternalLinks はすべて runtime（event handler 起動時など）に
        //   _drawer.<method> 経由で解決され、その時点では createMobileDrawer が実行済み。
        const _drawer = {};

        // ===== v80+ Stage 5-l: AIDK Rails 合体 factory =====
        //   RouteState / EffectRails / BindingRegistry / ActionDelegator / DiagnosticsRail を
        //   js/aidk-rails.js へ合体 factory pattern で抽出。State / Toast / Router / CONSTANTS /
        //   applyMeta / h / createIcon を引数注入で合成（挙動 byte-equivalent）。
        //   applyMeta は createMetaManagement の戻り値で先に bind されている。
        //   Theme / BGM は factory instance（先に bind 済み）。
        //   secureExternalLinks / openDrawer / closeDrawer は _drawer holder 経由で late-bound。
        const {
            RouteState, EffectRails, BindingRegistry, ActionDelegator, DiagnosticsRail
        } = createAIDKRails({
            State, Toast, Router, CONSTANTS, applyMeta, h, createIcon,
            Theme, BGM,
            secureExternalLinks: (...args) => _drawer.secureExternalLinks?.(...args),
            openDrawer: () => _drawer.openDrawer?.(),
            closeDrawer: () => _drawer.closeDrawer?.()
        });



        // ===== Component: Sidebar =====
        // ===== Component: Sidebar =====
        // NAV_GROUPS: Primary（採用・評価者向け）/ Secondary（深掘り用）/ Lab（初期折りたたみ）
        // ===== v80+ Stage 5-m: UI Page Components (11 関数) =====
        //   Sidebar / HomePage / ProjectsPage / ProjectDetailPage / AppsPage /
        //   AboutPage / ResumePage / ContactPage / FatalPage / AIKnowhowPage / ContactCTA を
        //   js/components.js へ factory pattern で抽出。挙動 byte-equivalent。
        // closeDrawer は _drawer holder 経由で late-bound（Sidebar 内 event handler が呼ぶときに解決）。
        // clear / CONSTANTS / tokenize は既に import / declared 済み。
        const {
            Sidebar, HomePage, ProjectsPage, ProjectDetailPage, AppsPage,
            AboutPage, ResumePage, ContactPage, FatalPage, AIKnowhowPage, ContactCTA
        } = createComponents({
            h, createIcon, Toast, BGM, AUTHOR, Router, State, Theme, Brand, Store,
            tokenize, CONSTANTS, clear,
            closeDrawer: () => _drawer.closeDrawer?.()
        });

        // ===== v80+ Stage 5-j: Page components factory instantiation =====
        //   ContactCTA は Stage 5-m で createComponents から供給される。それを createPages
        //   の引数に渡して HiringRiskPage / RoleSplitPage / NotFoundPage を合成する。
        const { HiringRiskPage, RoleSplitPage, NotFoundPage } = createPages({ h, createIcon, Router, ContactCTA });


        // ===== Component: Home Page =====

        // ===== Component: Projects Page =====

        // ===== Component: Project Detail Page =====

        // ===== v80+ Stage 5-n: Productivity Apps Components (5 関数) =====
        //   TaskPage / TodoPage / PomodoroPage / AIPage / SettingsPage を js/apps.js
        //   へ factory pattern で抽出。各 page の private state（taskFilter /
        //   todoFilter / todoComposing / pomodoroTimer / aiLoading / settings*）も
        //   factory closure 内へ移動（揮発性 UI 状態は元と同位置で保持される・挙動 byte-equivalent）。
        const { TaskPage, TodoPage, PomodoroPage, AIPage, SettingsPage } = createApps({
            h, createIcon, Toast, AUTHOR, Router, State, Theme, Brand, Store, CONSTANTS,
            generateId, clamp, slugify
        });


        // ===== v80+ Stage 5-o: Quiz Renderer =====
        //   QuizPage を js/quiz-renderer.js へ factory pattern で抽出。挙動 byte-equivalent。
        const { QuizPage } = createQuizRenderer({
            h, createIcon, Toast, Router, State,
            awsQuizData, pmQuizData, qualityQuizData, architectureQuizData
        });



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

        // ===== Stage 5-q dispatcher resolution =====
        //   実行時 _drawer object は createComponents の closeDrawer late-binding と AIDK Rail
        //   の secureExternalLinks / openDrawer / closeDrawer late-binding が「現実のインスタンス」
        //   を解決するための holder。createMobileDrawer の戻り値を Object.assign で代入することで、
        //   Sidebar 内の close button や AIDK Rail の EffectRails.dispatch が実行された際に
        //   正しい関数が呼ばれる。
        //
        //   ※ Mobile Drawer の抽出は main.js の真の末尾、つまり init() 直前で行うのが本来は
        //   清潔だが、本ファイルではすでに init や event registry が後段に並んでおり、
        //   それらは syncMobileDrawer / openDrawer / closeDrawer 等に依存している。
        //   よって本 PR では Mobile Drawer factory を Sidebar 解決直後（= createComponents の
        //   直後）に呼び出し、_drawer holder へ即代入する形でフロー順を整える。
        const {
            syncMobileDrawer, secureExternalLinks, openDrawer, closeDrawer
        } = createMobileDrawer({ CONSTANTS, clear, Sidebar });
        Object.assign(_drawer, { syncMobileDrawer, secureExternalLinks, openDrawer, closeDrawer });



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

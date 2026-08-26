
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
            tokenize,      // 文字列を検索/類似度用トークンへ分解（日本語対応）
            slugify,       // 文字列を URL/識別子 slug へ正規化
            sanitizeUrl,   // http/https のみ通すセキュリティ境界（挙動不変厳守）
            deepClone,     // オブジェクト/配列/Date の深いコピー
            yieldToMain,   // INP 改善のためメインスレッドを解放（scheduler.yield 等）
            langOfText     // data 由来テキストの言語判定（WCAG 3.1.2・lang 属性用）
        } from './js/pure-utils.js';
        // v80+ Stage 3-b: 静的クイズデータ 4 つをドメイン別の葉モジュールへ細分化し直接 import する
        //   （Stage 3 の js/quiz-data.js 単一ファイルを AWS / PM / 品質 / 設計判断の 4 ファイルへ分割）。
        //   aggregator は葉契約（Check 47c）を崩すため不採用。詳細は docs/architecture/main-js-extraction-map.md §3.6。
        //   純データゆえ挙動不変。import/export bijection と葉性は Check 47 が複数モジュールをループ検査して強制。
        //   （各 import は行末コメントを付けない＝ Check 43d の import 連結検出が確実に全 import を消費できるよう、
        //    付帯説明は各葉モジュールの fileoverview と上記コメントへ集約する。）
        // v80+ Stage 4: UI コンポーネント（DOM ビルダー・アイコン・Toast・BGM）を葉モジュールへ抽出。
        //   closure-deps = none の純表示系のみを選別し、State/Storage/RouteState 依存コンポーネントは残置。
        import { h, createIcon, Toast, BGM, announce, installPasteTruncationNotice } from './js/ui-components.js';
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
        // v80+ bloat-reduction (2026-07-04): HiringRiskPage (採用リスク低減 / 最大ページ) +
        //   専用 helper を js/pages.js から js/hiring-risk-page.js へ分離。pages.js の肥大化を解消。
        import { createHiringRiskPage } from './js/hiring-risk-page.js';
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
        // 肥大化解消: AIKnowhowPage / HomePage (大きい単一ページ) を js/components.js から分離。
        import { createAIKnowhowPage } from './js/ai-knowhow-page.js';
        import { createHomePage } from './js/home-page.js';
        import { createProjectsPage } from './js/projects-page.js';
        import { createProjectDetailPage } from './js/project-detail-page.js';
        // v80+ Stage 5-n: Productivity Apps Components (TaskPage / TodoPage / PomodoroPage /
        //   AIPage / SettingsPage) を factory pattern で葉モジュール抽出。各 page の private
        //   state も factory closure 内に閉じ込める（揮発性 UI 状態は元と同位置で保持）。
        import { createApps } from './js/apps.js';
        // v80+ bloat-reduction (2026-07-04): AIPage (AI アシスト) を js/apps.js から
        //   js/ai-page.js へ分離。private state が aiLoading 1 個で自己完結ゆえ最安全単位。
        import { createAIPage } from './js/ai-page.js';
        // v80+ bloat-reduction (2026-07-04): PomodoroPage を js/apps.js から js/pomodoro-page.js へ分離。
        //   private state が pomodoroTimer (interval id) 1 個で自己完結。stale-closure 対策 (#121/#134) 温存。
        import { createPomodoroPage } from './js/pomodoro-page.js';
        // v80+ bloat-reduction (2026-07-05): SettingsPage を js/apps.js から js/settings-page.js へ分離。
        //   createApps が 837 行に肥大化していたため最大 page (~373 行) を抽出し 461 行へ縮小 (Check 363 headroom)。
        import { createSettingsPage } from './js/settings-page.js';
        import { createSettingsIO } from './js/settings-io.js';
        // v80+ Stage 5-o: Quiz Renderer (QuizPage + 4 quiz domain lookup) を factory pattern で葉モジュール抽出。
        import { createQuizRenderer } from './js/quiz-renderer.js';
        // v80+ Stage 5-l: AIDK Rail 5 IIFE (RouteState / EffectRails / BindingRegistry /
        //   ActionDelegator / DiagnosticsRail) を合体 factory pattern で葉モジュール抽出。
        //   相互依存を内部 closure に閉じ込めるため 1 モジュールに合体。挙動 byte-equivalent。
        import { createAIDKRails } from './js/aidk-rails.js';
        // v80+ Stage 5-q: Mobile Drawer + Focus Trap + secureExternalLinks を factory pattern で
        //   葉モジュール抽出。Sidebar 注入と _drawer holder 経由の late-binding で循環依存解消。
        import { createMobileDrawer } from './js/mobile-drawer.js';
        // v80+ Stage 5-r: Fatal overlay + Global Safety Net を factory pattern で葉モジュール抽出。
        //   install() を呼ぶと window error handlers + Shadow DOM safety net の setInterval が登録される。
        import { createFatalOverlay } from './js/fatal-overlay.js';
        // v80+ Stage 5-s: パフォーマンスガード 2 つ（Layout Thrashing / Media Lifecycle）を
        //   factory pattern で葉モジュール抽出。外部依存なしの DOM API グローバル prototype hook。
        import { createPerfGuards } from './js/perf-guards.js';
        // Command palette: Cmd/Ctrl+K の横断ナビ overlay（新ルート無し・純追加機能）を葉モジュール化。
        import { createCommandPalette } from './js/command-palette.js';
        /* ╔══════════════════════════════════════════════════════════════════╗
           ║  DO NOT EDIT: AIDK Isolated Kernel — AIDK Architecture          ║
           ║  このブロック全体がAIエージェントのアクセスから隔離された核です。   ║
           ║  AIが編集してよいのは「AI SURFACE」マーカーで囲まれた領域のみ。    ║
           ║  Kernel内のロジック改変はCI/CDレベルで検知・棄却されます。         ║
           ╚══════════════════════════════════════════════════════════════════╝ */
        // WHY この領域が "DO NOT EDIT" か:
        //   KERNEL framework (AI2AI.md STEP 3) は「人間が設計し AI が実装する」分担の
        //   不可侵境界。ここの各装置（VT proxy / Trusted Types / IIFE 包囲）は安全契約
        //   C2/C3/C5 の物理的実体であり、AI 実装の暴走（global 汚染・innerHTML 注入・
        //   transition ハングアップ）から site を守る最後の砦。
        // 機械強制: Check 43a〜43d (check_repository_consistency.py) が以下を BLOCKING で監視:
        //   43a = "DO NOT EDIT: AIDK Isolated Kernel" header 文字列の存在
        //   43b = startViewTransitionProxy installer の存在 (C3 ErrorBoundary)
        //   43c = Trusted Types 'default' policy の存在 (C5 / CSP-linked)
        //   43d = main.js 全体が単一 top-level IIFE で包囲されている (C2)
        // 触ると壊れるもの: これらマーカーのどれかを消す/改名すると verify が BLOCKING fail。
        //   さらに Stage 5 物理分割でここが "最終的に un-extractable と判断して温存した"
        //   領域（CLAUDE.md §7 参照）であり、分割は visual-regression baseline 緑が前提。
        (function() {
        'use strict';

        // ─────────────────────────────────────────────────────────────────────────
        // 改善文書c Section 1 / カテゴリA #9: document.startViewTransition プロキシ・インターセプター
        // AIが素のdocument.startViewTransition()を直接呼び出しても、
        // try/catch + skipTransition() + タイムアウト制御が必ず効くよう
        // メソッド自体をここで上書きする。safeViewTransition()経由かどうかに依存しない。
        // WHY メソッド自体を上書きするか（wrapper を呼ばせる方式を採らない理由）:
        //   AI 実装は executeSafeTransition() を経由せず素の API を直接呼ぶ可能性がある。
        //   ラッパー関数を「使ってもらう」前提は破られうるので、API surface 自体を差し替え、
        //   どの呼び出し経路でも ErrorBoundary (C3) が必ず効く構造にしている。
        // Check 43b が "startViewTransitionProxy" 文字列の存在を BLOCKING 監視。関数名を
        //   変えると verify が落ちる＝この安全装置が消えた合図として検出される。
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
        // WHY createHTML を空文字に倒すか（C5 = innerHTML 全面禁止の実体）:
        //   この site は h() helper / DOM API のみで描画する契約（@rules 5）。createHTML が
        //   常に '' を返すことで、万一 AI 実装が innerHTML 経由の文字列注入を書いても DOM に
        //   反映されず fail-closed する。index.html の CSP `require-trusted-types-for 'script'`
        //   と対になって機能するため、policy 名 'default' は CSP と一致させ変更不可。
        // WHY script/scriptURL は pass-through か:
        //   KARTE 等の正当な外部 script 読込（C7）を壊さないため。ここで script 内容を
        //   filter する意図はなく、"厳密な script サニタイズ" と説明してはならない（誤記防止）。
        // Check 43c が trustedTypes.createPolicy('default' の存在を BLOCKING 監視。
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
            // [AIO] 権利宣言の単一ソース。runtime 注入の JSON-LD にも載せる (route 追従ノードは
            //   別 @id ゆえ静的側の license が及ばない)。Check 444 が LICENSE との一致を強制。
            LICENSE_URL:   'https://yutapr0117-design.github.io/portfolio/LICENSES/ACD-1.0.txt',
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
        //     generateId / clamp / debounce / tokenize /
        //     slugify / sanitizeUrl / deepClone
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
        // refreshChrome: テーマ切替は #content を作り直さずに済ませる (入力途中のテキストと focus を
        //   守る)。theme を描画に使うのは sidebar だけなので、そこだけ再構築すれば足りる。
        const Theme = createTheme({
            State,
            Toast,
            refreshChrome: () => {
                const _sb = document.getElementById('sidebar');
                if (!_sb) { return; }
                // 押したボタン自身が再構築で消えるため focus が body へ落ちる (WCAG 2.4.3)。
                // sidebar 内に focus があった場合だけ、同じ id の要素へ戻す。
                // (sidebar 外に focus がある場合は奪わない — #267 で学んだ「奪うのではなく
                //  失われた時だけ復元する」原則)
                const _activeId = _sb.contains(document.activeElement) ? document.activeElement.id : null;
                clear(_sb);
                _sb.appendChild(Sidebar(false));
                if (_activeId) {
                    const _next = document.getElementById(_activeId);
                    if (_next && _next.focus) { try { _next.focus({ preventScroll: true }); } catch (e) { /* noop */ } }
                }
            }
        });


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
            openDrawer: () => _drawer.openDrawer?.()
        });



        // ===== Component: Sidebar =====
        // ===== Component: Sidebar =====
        // NAV_GROUPS: Primary（採用・評価者向け）/ Secondary（深掘り用）/ Lab（初期折りたたみ）
        // ===== v80+ Stage 5-m: UI Page Components (11 関数) =====
        //   Sidebar / HomePage / ProjectsPage / ProjectDetailPage / AppsPage /
        //   AboutPage / ResumePage / ContactPage / FatalPage / AIKnowhowPage / ContactCTA を
        //   js/components.js へ factory pattern で抽出。挙動 byte-equivalent。
        // closeDrawer は _drawer holder 経由で late-bound（Sidebar 内 event handler が呼ぶときに解決）。
        // clear / CONSTANTS は既に import / declared 済み。
        // (tokenize / Toast / Brand / Store は HomePage/ProjectsPage/AIKnowhowPage 等の分離で
        //  createComponents 本体から不要になり除去。各 leaf module が自前の factory で受け取る)
        const {
            Sidebar, AppsPage,
            AboutPage, ResumePage, ContactPage, FatalPage, ContactCTA
        } = createComponents({
            h, createIcon, BGM, AUTHOR, Router, State, Theme,
            CONSTANTS, clear,
            closeDrawer: () => _drawer.closeDrawer?.(), langOfText });
        // 肥大化解消: AIKnowhowPage / HomePage / ProjectsPage / ProjectDetailPage は
        // js/{...}-page.js へ分離。ContactCTA (共有 helper) を createComponents 生成後に注入 (byte-equivalent)。
        const AIKnowhowPage = createAIKnowhowPage({ h, createIcon, ContactCTA });
        const HomePage = createHomePage({ h, Router, State, ContactCTA, langOfText });
        const ProjectsPage = createProjectsPage({ h, createIcon, Router, State, tokenize, clear });
        const ProjectDetailPage = createProjectDetailPage({ h, createIcon, Router, State, Store });

        // ===== v80+ Stage 5-j: Page components factory instantiation =====
        //   ContactCTA は Stage 5-m で createComponents から供給される。それを createPages /
        //   createHiringRiskPage の引数に渡して各ページを合成する。
        //   (2026-07-04 bloat-reduction: HiringRiskPage は別葉モジュール createHiringRiskPage へ分離)
        const HiringRiskPage = createHiringRiskPage({ h, createIcon, Router, ContactCTA }).HiringRiskPage;
        const { RoleSplitPage, NotFoundPage } = createPages({ h, createIcon, Router, ContactCTA });


        // ===== Component: Home Page =====

        // ===== Component: Projects Page =====

        // ===== Component: Project Detail Page =====

        // ===== v80+ Stage 5-n: Productivity Apps Components (5 関数) =====
        //   TaskPage / TodoPage / PomodoroPage / AIPage / SettingsPage を js/apps.js
        //   へ factory pattern で抽出。各 page の private state（taskFilter /
        //   todoFilter / todoComposing / pomodoroTimer / aiLoading / settings*）も
        //   factory closure 内へ移動（揮発性 UI 状態は元と同位置で保持される・挙動 byte-equivalent）。
        const { TaskPage, TodoPage, NotesPage } = createApps({
            h, createIcon, Toast, State, CONSTANTS, generateId, clamp, announce
        });
        // 2026-07-04 bloat-reduction: AIPage は別葉モジュール createAIPage で生成 (依存は h/createIcon/State/CONSTANTS のみ)
        const { AIPage } = createAIPage({ h, createIcon, State, Router, CONSTANTS, announce });
        // 2026-07-04 bloat-reduction: PomodoroPage は別葉モジュール createPomodoroPage で生成 (依存は h/createIcon/State/Router/Toast/clamp/CONSTANTS)
        const { PomodoroPage, resumeIfActive } = createPomodoroPage({ h, createIcon, State, Router, Toast, clamp, CONSTANTS });
        // 2026-07-05 bloat-reduction: SettingsPage は別葉モジュール createSettingsPage で生成
        //   (依存は h/Toast/State/Brand/Store/Storage/CONSTANTS/generateId/slugify)
        // 2026-08-20 bloat-reduction: 入出力 (export/import/lossParts) を js/settings-io.js へ分離。
        //   IO は「取り込みの瞬間の UI 選択」を getter で読む必要があり、その選択は
        //   SettingsPage の closure が持つ → 相互参照になる。late-binding holder で解く
        //   (Stage 5-q/5-r と同じパターン)。holder の初期値は SettingsPage が返る前に
        //   万一呼ばれた場合の既定値で、実際には下の代入後にしか使われない。
        let _settingsImportOptions = () => ({
            mode: 'append', includeProfile: true, includeProjects: true, includeApps: true,
        });
        const SettingsIO = createSettingsIO({
            State, Store, Toast, Brand, getImportOptions: () => _settingsImportOptions(),
        });
        const { SettingsPage, getImportOptions: _getSettingsImportOptions } = createSettingsPage({ h, Toast, State, Brand, Store, Storage, CONSTANTS, generateId, slugify, announce, IO: SettingsIO });
        _settingsImportOptions = _getSettingsImportOptions;


        // [FIX] **失敗した動的 import は module map にキャッシュされ、以降は即 reject する**。
        //   通信が一瞬切れただけで、開き直しても永久に読めない。クエリを足した別 URL で
        //   取り直すと新しい entry になり実際に再取得される (初回はリテラルのまま — Check 47b が
        //   `import('<spec>')...m.<Name>` の綴りで消費を見るため)。詳細は e2e/quiz.spec.js。
        let _quizRetryCount = 0;
        const _QUIZ_SOURCES = {
            aws: ['./js/quiz/aws-quiz-data.js', 'awsQuizData'],
            pm: ['./js/quiz/pm-quiz-data.js', 'pmQuizData'],
            quality: ['./js/quiz/quality-quiz-data.js', 'qualityQuizData'],
            architecture: ['./js/quiz/architecture-quiz-data.js', 'architectureQuizData']
        };
        function _retryQuizData(type) {
            const key = Object.prototype.hasOwnProperty.call(_QUIZ_SOURCES, type) ? type : 'aws';
            const [path, name] = _QUIZ_SOURCES[key];
            _quizRetryCount += 1;
            return import(path + '?retry=' + _quizRetryCount).then(m => m[name]);
        }

        // ===== v80+ Stage 5-o: Quiz Renderer =====
        //   QuizPage を js/quiz-renderer.js へ factory pattern で抽出。挙動 byte-equivalent。
        const { QuizPage } = createQuizRenderer({
            h, createIcon, Toast, Router, State, langOfText, CONSTANTS,
            // [PERF] 問題集データ (4 ファイル計 130,595 bytes) は quiz を開いたときだけ取りに行く。
            //   静的 import + modulepreload だと **quiz を一度も開かない訪問者も毎回全部取得**する
            //   (実測 2026-08-21)。動的 import は native ESM なので C1 (Boring Technology) を保つ。
            loadQuizData: (type) => (
                type === 'pm' ? import('./js/quiz/pm-quiz-data.js').then(m => m.pmQuizData)
                    : type === 'quality' ? import('./js/quiz/quality-quiz-data.js').then(m => m.qualityQuizData)
                        : type === 'architecture' ? import('./js/quiz/architecture-quiz-data.js').then(m => m.architectureQuizData)
                            : import('./js/quiz/aws-quiz-data.js').then(m => m.awsQuizData)
            ).catch(() => _retryQuizData(type))
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
                            await _renderCore(isRouteTransition);
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
                        _renderCore(isRouteTransition).then(() => {
                            _lastRoutePath = currentRoutePath;
                            _consumePendingRoute();
                        });
                    } else {
                        window.__fatalError = _normalizeError(err);
                        _renderCore(isRouteTransition).then(() => {
                            _lastRoutePath = currentRoutePath;
                        });
                    }
                }
            } else if (isRouteTransition && (_vtInFlight || _getActiveViewTransition())) {
                // 実行中は最新の route のみ保持して、transition 完了後に 1 回だけ反映する
                _vtPendingPath = currentRoutePath;
            } else {
                _renderCore(isRouteTransition).then(() => {
                    _lastRoutePath = currentRoutePath;
                });
            }
        }

        async function _renderCore(isRouteChange = false) {
            // 改善文書b 4: Abort any previous render in flight before starting a new one.
            // This prevents memory leaks from stale async render chains.
            _renderAbortController.abort();
            _renderAbortController = new AbortController();
            const _signal = _renderAbortController.signal;

            // [FIX] DOM のテーマを state.theme に追随させる。import / 全リセット / snapshot 復元の
            //   ような **state を丸ごと置き換える経路**は Theme.cycle を通らないため、
            //   `data-theme` と `.dark` が古いまま残っていた (実測 #1036: dark のまま import した
            //   backup が system になっても表示は dark で、reload して初めて切り替わる)。
            //   ここは全再描画の入口なので、置換経路をすべてまとめて拾える単一点。
            //   同値なら apply は冪等 (属性の再設定のみ) ゆえ毎描画呼んでも無害。
            try {
                const _wantTheme = State.get().theme;
                if (_wantTheme && document.documentElement.getAttribute('data-theme') !== _wantTheme) {
                    Theme.apply(_wantTheme);
                }
            } catch { /* テーマ同期は描画を止めない */ }

            const route = Router.getRoute();
            const content = document.getElementById('content');
            const sidebarEl = document.getElementById('sidebar');

            // a11y (WCAG 2.1.1 / 2.4.3): 同一ルート再描画で focus 中のコントロールを復元するため、
            // **最初の clear より前に** id を控える。State.update は #content (と sidebar) を作り直す
            // ので、focus 中の select / checkbox / number input は DOM ごと消え focus が body へ落ちる。
            // 実測 (#994): task/todo の絞り込み・タスクの優先度・Todo の完了チェック・ポモドーロの
            // 設定はいずれも change 後に activeElement=BODY になっていた。number input は特に重く、
            // ArrowUp の 1 回目で focus を失うため **2 回目以降が一切効かない** (値が 1 段しか動かせない)。
            // 復元は id を持つ要素に限る (id はこの復元のためだけに付いている安定ハンドル)。
            const _prevActive = document.activeElement;
            const _restoreFocusId = (!isRouteChange && _prevActive && _prevActive.id
                && _prevActive !== document.body && _prevActive !== document.documentElement)
                ? _prevActive.id : null;
            // テキスト入力ならキャレット位置も控える。id だけ戻しても **キャレットは末尾へ飛ぶ**ため、
            // 文章の途中を編集している最中に外部要因の再描画 (ポモドーロ完了・AI 応答の到着など) が
            // 起きると、次に打った 1 文字が末尾へ入る。実測 (#1001): Markdown ノートで caret=3 から
            // 再描画すると caret=54 (末尾) になり、続きの入力が末尾に着弾した。
            // selectionStart は number/checkbox 等では null なので typeof で弾く。
            const _restoreFocusSel = (_restoreFocusId && typeof _prevActive.selectionStart === 'number')
                ? { start: _prevActive.selectionStart, end: _prevActive.selectionEnd } : null;

            // § Agentic State Notification: aria-busy=true でローディング開始を宣言
            if (content) {
                content.setAttribute('aria-busy', 'true');
                document.body.setAttribute('data-ai-state', JSON.stringify({
                    route: route.name || 'home',
                    // [FIX] 従来は `''` 決め打ちで絞り込みを宣言できなかった (router の単一ソースへ)。
                    filter: Router.getFilterString(),
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
                        case 'app-notes':
                            page = NotesPage();
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

            // a11y (WCAG 2.4.3): route 遷移時のみ新ページ見出しへ focus を移す。SPA は #content を
            // 作り直すため、ナビ後に focus が body へ落ちキーボード/SR ユーザが文脈を失う。2 条件で限定:
            //   (1) isRouteChange (render() が渡す isRouteTransition=hash 変化) — State.update 由来の
            //       同一ルート再描画 (検索/notes 入力/todo filter 等) では focus を動かさない (#258 非回帰)。
            //   (2) _focusWasLost (clear(content) 後の activeElement が body/html/null) — focus を「奪う」
            //       のでなく「失われた時に復元」する。command palette / drawer の input など #content 外の
            //       生存要素が focus 中なら奪わない (route render が palette open の input focus と race し
            //       focus を奪う flake を防ぐ)。
            // tabindex=-1 + preventScroll。:focus-visible 採用ゆえ programmatic focus に視覚リングは出ない。
            const _ae = document.activeElement;
            const _focusWasLost = !_ae || _ae === document.body || _ae === document.documentElement;

            // a11y (WCAG 2.1.1): 同一ルート再描画で消えたコントロールへ focus を戻す。route 遷移では
            // 行わない (下の h1 復元が正しい文脈) ため isRouteChange の時点で _restoreFocusId は null。
            // 「奪う」のではなく「失われた時だけ復元する」— #265 で route render が command palette の
            // input と race して focus を奪った失敗の再発防止で、上の h1 復元と同じ条件を共有する。
            if (_restoreFocusId && _focusWasLost) {
                const _again = document.getElementById(_restoreFocusId);
                if (_again) {
                    try { _again.focus({ preventScroll: true }); } catch { /* noop */ }
                    // キャレットの復元。値が変わっている可能性があるので長さでクランプする
                    // (復元できない場合でも末尾のままなので、現状より悪くはならない)。
                    if (_restoreFocusSel && typeof _again.setSelectionRange === 'function') {
                        const _len = String(_again.value ?? '').length;
                        try {
                            _again.setSelectionRange(Math.min(_restoreFocusSel.start, _len),
                                Math.min(_restoreFocusSel.end, _len));
                        } catch { /* type によっては setSelectionRange 不可 */ }
                    }
                }
                // 元の要素へ戻せないケースが 2 つある。どちらも focus は body に残るので、
                // 「せめて #content の中へ」戻す (ドキュメント先頭からの Tab やり直しを避ける)。
                //   (1) 対象が消えた — 削除ボタンは自分自身を消すので同じ id は二度と現れない
                //   (2) 復元先が disabled になった — タスクを最終ステータスへ動かすと「次へ」が
                //       disabled になり、disabled 要素への focus() は黙って無効化される
                // 成否は「focus() を呼んだか」ではなく **activeElement を読み直して**判定する。
                const _now = document.activeElement;
                if (content && (!_now || _now === document.body || _now === document.documentElement)) {
                    const _fb = content.querySelector('h1') || content;
                    if (!_fb.hasAttribute('tabindex')) { _fb.setAttribute('tabindex', '-1'); }
                    try { _fb.focus({ preventScroll: true }); } catch { /* noop */ }
                }
            }

            if (isRouteChange && content && _focusWasLost) {
                const _focusTarget = content.querySelector('h1') || content;
                if (_focusTarget) {
                    if (!_focusTarget.hasAttribute('tabindex')) { _focusTarget.setAttribute('tabindex', '-1'); }
                    try { _focusTarget.focus({ preventScroll: true }); } catch { /* noop */ }
                }
            }

            // Guard: skip meta/state sync if render was superseded
            if (_signal && _signal.aborted) { return; }

            // § Agentic State Notification: 描画完了後に aria-busy=false へ切替
            requestAnimationFrame(() => {
                if (content) {content.setAttribute('aria-busy', 'false');}
                document.body.setAttribute('data-ai-state', JSON.stringify({
                    route: route.name || 'home',
                    // [FIX] ここが `''` を書き戻し、直前の正しい query を毎回消していた。
                    filter: Router.getFilterString(),
                    loading: false
                }));
            });

            // §1.2 INP最適化: ページコンテンツ追加後にスレッドを解放してからメタ更新
            await yieldToMain();
            // Update SEO via PAGE_META (v37: unified metadata management)
            // isRouteChange を渡し「ルート遷移アナウンス」を実遷移時のみに限定する。
            //   _renderCore は State.update 由来の同一ページ再描画 (task 追加 / pomodoro tick 等)
            //   でも走るため、applyMeta 内の announceRouteForAccessibility を無条件呼びすると
            //   SR 利用者へ「○○ページを表示しています。」が状態変化のたびに繰り返し読み上げられる
            //   over-announce ノイズ (WCAG 4.1.3 反パターン) になっていた。head/entity-anchor/
            //   JSON-LD 更新は idempotent ゆえ毎描画で無害だが、announce は transient なので gate する。
            applyMeta(route.name, route.params || {}, route.query || {}, isRouteChange);

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
        // command palette の late-binding holder (drawer より後に生成されるため)
        const _palette = {};
        const {
            syncMobileDrawer, secureExternalLinks, openDrawer, closeDrawer, setAppInert
        } = createMobileDrawer({
            CONSTANTS, clear, Sidebar,
            // command palette は本 factory より後に生成されるため late-binding holder 経由で解決する
            // (_drawer holder と同じパターン)。二重モーダル防止のため drawer を開く前に palette を閉じる。
            closePalette: () => _palette.close?.()
        });
        Object.assign(_drawer, { syncMobileDrawer, secureExternalLinks, openDrawer, closeDrawer });



        // ===== v80+ Stage 5-r: Fatal overlay + Global Safety Net =====
        //   _normalizeError / _isViewTransitionError / _isFatalError + window error handlers +
        //   _installGlobalSafetyNet (Shadow DOM フォールバック UI) を js/fatal-overlay.js へ
        //   factory pattern で抽出。render は後段で declared なので wrapper で late-bind する。
        //   install() を呼ぶと元 main.js IIFE 評価時の即時実行と等価な副作用が発生する。
        //   ヘルパー 3 関数（_normalizeError / _isViewTransitionError / _isFatalError）は
        //   executeSafeTransition / render 内からも参照されるため main.js scope に bind する。
        const _fatalOverlay = createFatalOverlay({ render: (...args) => render(...args) });
        const { _normalizeError, _isViewTransitionError, _isFatalError } = _fatalOverlay;
        _fatalOverlay.install();

        // Command palette（Cmd/Ctrl+K 横断ナビ overlay）を合成。init() で global keydown を登録。
        const CommandPalette = createCommandPalette({ Router, h, createIcon, State, closeDrawer, setAppInert, announce });
        // createMobileDrawer へ渡した closePalette の late-binding を解決する (holder へ実体を代入)。
        Object.assign(_palette, CommandPalette);


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
            // 貼り付けが maxlength で黙って切られたことを SR/利用者へ報告する (document 単一リスナー)
            installPasteTruncationNotice();
            // Diagnostics Rail: ?debug=1 で起動
            if (location.search.includes('debug=1')) {
                RouteState.proxy.diag_debug_mode = true;
            }
            // ────────────────────────────────────────────────────────────

            // Mobile menu: menuBtn(data-action="drawer:open") / themeBtnTop(data-action="theme:cycle")
            // は ActionDelegator が処理するため直接リスナーは付けない。両方付けると 1 クリックで
            // ハンドラが二重発火し、drawer 二重 open で __lockBodyScroll が scrollY=0 を読んで閉じると
            // ページ先頭へジャンプ / theme が 1 クリックで 2 段送り（1 つ飛ばし）になる実バグだった。
            // overlay は data-action を持たないため直接リスナーで閉じる。
            document.getElementById('overlay')?.addEventListener('click', closeDrawer);

            // Skip-link (WCAG 2.4.1 Bypass Blocks): `<a href="#main-content">` は fragment anchor
            // だが、native 挙動だと click で location.hash が "#main-content" に変わり hashchange→
            // router が非-"#/" hash を _parseRoute で home 扱いして再描画する。結果、非 home ページ
            // (例 #/projects) で「本文へスキップ」を押すとユーザーが home へ誤遷移する実バグだった
            // (WCAG 2.4.1 は focus を本文へ移すのみでページ遷移は誤り)。preventDefault して
            // #main-content(tabindex=-1) へ直接 focus を移すことで、現在ルート(URL=#/...)を保持した
            // まま本文へバイパスする。Enter 起動も anchor が click を dispatch するため同経路で処理。
            document.querySelector('.skip-link')?.addEventListener('click', (e) => {
                e.preventDefault();
                document.getElementById('main-content')?.focus();
            });

            // Escape key
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    const drawer = document.getElementById('drawer');
                    if (drawer && drawer.getAttribute('aria-hidden') === 'false') closeDrawer();
                }
            });
            // Command palette: Cmd/Ctrl+K の global opener を登録（他キーは素通し）
            CommandPalette.init();

            // Window resize listener (v37: responsive drawer sync)
            window.addEventListener('resize', debounce(syncMobileDrawer, CONSTANTS.DEBOUNCE_DELAY));

            // Router
            Router.subscribe(render);

            // State changes
            State.subscribe(() => render());

            // Initial render
            render();

            // ===== 稼働中ポモドーロの復帰 (ルート非依存) =====
            // resume を描画に紐付けると、リロード後に**別ページにいる**利用者の interval が
            // 誰にも作られず、集中し続けても完了が記録されない (実測: 別ページ着地 history=0 /
            // ポモドーロ画面着地 history=1)。リロードしなければ裏で完了するので、リロードを
            // 跨いだときだけ挙動が違う非対称だった。init で 1 度呼んでルート非依存にする。
            resumeIfActive();

            // ===== BGM Initialization =====
            // bgm-btn-top は data-action="bgm:toggle" を持ち ActionDelegator が処理するため
            // 直接リスナーは付けない（付けると 1 クリックで二重 toggle になる）。
            BGM.init();

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
        // WHY protected block（CLAUDE.md §3 で「frozen」指定）か:
        //   EventTarget.prototype.addEventListener を site 全体で差し替えるグローバル hook。
        //   WeakMap registry と MutationObserver の対が崩れると、SPA の頻繁な再描画で
        //   リスナーが回収されず zombie listener のメモリリークに直結する。挙動が全 component
        //   に波及するため、closure-deps を持たないが「分割せず main.js に残す」判断対象。
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
        // WHY protected block（CLAUDE.md §3 で「frozen」指定）か / Trusted Types との二重防衛:
        //   これは Trusted Types createHTML='' (C5) を二重化する第二防壁。Trusted Types 非対応
        //   ブラウザや TrustedHTML を経由しない代入経路でも、DANGEROUS_TAGS 除去・on* 属性除去・
        //   javascript:/data: スキーム除去・DOM Clobbering プレフィックスで fail-closed する。
        //   DOMParser 失敗時に raw HTML を絶対 native setter へ流さずテキスト化する点が肝で、
        //   ここを緩めると XSS 経路が開く。グローバル prototype 改変ゆえ全描画に波及＝残置。
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

        // ===== v80+ Stage 5-s: Performance Guard (Media Lifecycle) =====
        //   _installMediaLifecycleGuard を js/perf-guards.js へ factory pattern で抽出。
        //   外部依存なしで DOM から外れた audio/video の blob: src を解放する。
        //   WHY ここに Layout Thrashing Guard が無いか: setProperty / setAttribute('style') を
        //   rAF バッチ化する hook を持っていたが、shipped JS は例外なく直接代入 (el.style.x = …)
        //   を使い hook 対象外だったため **一度も発火していなかった** (実測 0 回)。利益ゼロの一方で
        //   全 setAttribute にラッパーが挟まり、DOM の意味論が標準と食い違い、e2e の診断を
        //   偽陰性にする実害があったので除去した (理由の詳細は js/perf-guards.js の docstring)。
        const _perfGuards = createPerfGuards();
        _perfGuards.installMediaLifecycleGuard();


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
                        // js/pages.js の splitRow が描画する data-ai-role フックに解決する
                        // (Check 411 が used⟹defined を強制)。旧セレクタは `.role-split-item` との
                        // 2 択だったが、その class はリポジトリのどこにも描画されておらず (実測)、
                        // 「現在の DOM 状態から抽出」と謳いながら常に静的フォールバックへ落ちていた。
                        var roleElements = document.querySelectorAll('[data-ai-role]');
                        if (roleElements.length > 0) {
                            var extracted = Array.from(roleElements).map(function(el) { return el.textContent.trim(); });
                            roleSplitData = (params && params.format) === 'json'
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
                        // この IIFE は SITE_CONFIG のスコープ外 (自前で SITE_BASE を持つ)。
                        //   URL を丸ごと複製せず SITE_BASE から合成する。Check 444 が
                        //   LICENSE の `Full text:` 行との一致を BLOCKING で強制する。
                        'license': SITE_BASE + 'LICENSES/ACD-1.0.txt',
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

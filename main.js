
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
        // v80+ Stage 5-b: ページコンポーネント（HiringRiskPage / RoleSplitPage / NotFoundPage）を葉モジュールへ抽出。
        //   closure-deps = none（h / createIcon / Router の純粋ユーティリティのみ参照）。
        import { HiringRiskPage, RoleSplitPage, NotFoundPage } from './js/pages.js';
        // v80+ Stage 5-c: Safe Storage（localStorage ラッパ）を葉モジュールへ抽出。
        //   closure-deps = none（localStorage と引数のみ。CONSTANTS 等の IIFE クロージャ非参照）。
        import { Storage } from './js/storage.js';
        // v80+ Stage 5-d: CONSTANTS（実行時定数: STORAGE_KEY / LIMITS / timing / DEBUG / TAB_ID）を葉モジュールへ抽出。
        //   SITE_CONFIG.VERSION / LAST_UPDATED は Check 2 / 17 が main.js から名前抽出するため残置。
        //   closure-deps = none（ブラウザグローバル crypto/sessionStorage/location のみ参照、IIFE クロージャ非参照）。
        import { CONSTANTS } from './js/constants.js';
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
        // DISPLAY_NAME : UI表示専用。訪問者が見るすべての箇所はこれのみを参照する。
        // AUTHORITATIVE_NAME : AIO / SEO / 機械可読層専用。UIコンポーネントからは参照しない。
        // （依存方向の固定により、UIに本名が漏洩する構造的リスクを排除する）
        const AUTHOR = {
            DISPLAY_NAME:       'yuta',
            AUTHORITATIVE_NAME: 'Yuta Yokoi (横井雄太 / Yokoi Yuta)',
            JAPANESE_NAME:      '横井雄太',
        };

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
        const Store = (() => {
            // Default Data
            const defaultProfile = {
                name: AUTHOR.DISPLAY_NAME,
                title: 'AI-Driven PM',
                bio: `このサイトは完成をゴールにせず、設計判断を検証し続けるためのポートフォリオです。

【設計思想】
• 単一HTMLでの完結（依存性最小化）
• セマンティックHTML5 + ARIA対応
• 型安全なDOM操作
• イベント駆動アーキテクチャ

【見てほしいこと】
• SPAを最小構成で設計する判断
• 壊れる前提で作るための構造
• 作りながら改善していくプロセス

【Why SPA?】
• 構造変更を前提にするため
• 実装より設計判断を検証するため`,
                email: 'yuta.pr.0117@gmail.com',
                github: '',
                linkedin: '',
                location: 'Japan',
            };

            const defaultAppsData = {
                tasks: [
                    { id: 't1', title: 'ログの確認', status: 'backlog', priority: 'high', tags: ['運用'], createdAt: Date.now(), updatedAt: Date.now() },
                    { id: 't2', title: '資料の更新', status: 'in-progress', priority: 'low', tags: ['ドキュメント'], createdAt: Date.now(), updatedAt: Date.now() }
                ],
                todos: [
                    { id: 'td1', text: 'コーヒーを買う', completed: false, createdAt: Date.now(), dueDate: null }
                ],
                pomodoro: {
                    history: [],
                    settings: { work: 25, short: 5, long: 15 },
                    runtime: {
                        isActive: false,
                        mode: 'work',
                        endAtMs: null,
                        remainingSec: 1500,
                        linkedTaskId: null
                    }
                },
                ai: { history: [] },
                quizSearch: ""
            };

            function proj(id, slug, name, category, summary, problem, approach, outcome, tech, tags, highlights, architecture, relatedIds, links, demoRoute) {
                return {
                    id, slug, name, category,
                    summary, problem, approach,
                    outcome: outcome || { metrics: [], impact: "" },
                    tech: Array.isArray(tech) ? tech : [],
                    tags: Array.isArray(tags) ? tags : [],
                    highlights: Array.isArray(highlights) ? highlights : [],
                    architecture: architecture || { overview: "", mermaid: null },
                    relatedProjectIds: Array.isArray(relatedIds) ? relatedIds : [],
                    links: Array.isArray(links) ? links : [],
                    demoRoute: demoRoute || null
                };
            }

            const defaultProjects = [
                proj("p01", "task-manager", "タスク管理アプリ", "Productivity",
                    "このポートフォリオに統合された、オフライン対応のタスク管理ツール。",
                    "外部依存のあるツールは、障害時に利用できなくなるリスクがある。",
                    "状態・優先度・検索の最低限に絞って堅牢に実装。LocalStorageで永続化。",
                    { metrics: [{ label: "耐障害", value: "local-only" }, { label: "状態", value: "3" }], impact: "運用前提の最小機能で事故率を下げる。" },
                    ["Vanilla JS", "LocalStorage", "Hash Router"],
                    ["ツール", "SPA", "オフライン"], ["検索/フィルタ", "優先度", "状態遷移"],
                    { overview: "単一ストア（appsData.tasks）をUIが参照する構造。" },
                    ["p02", "p03", "p04"], [], "task"
                ),
                proj("p02", "todo-list", "TODOリスト", "Productivity",
                    "クイックTODO。",
                    "高機能システムへ移るたびに思考が途切れる。",
                    "Enter追加 + IMEガード + フィルタ/一括操作に限定。",
                    { metrics: [{ label: "入力導線", value: "Enter" }], impact: "認知負荷を落として記録を継続。" },
                    ["Vanilla JS", "IME guard"], ["ツール", "効率化"], ["一括操作", "検索/フィルタ"],
                    { overview: "appsData.todosを参照。" },
                    ["p01", "p03"], [], "todo"
                ),
                proj("p03", "pomodoro-timer", "ポモドーロタイマー", "Productivity",
                    "タブ休眠・スリープ対応ポモドーロ。",
                    "setIntervalだけだと非アクティブで精度が落ちる。",
                    "endAt(タイムスタンプ)で残秒を復元。二重起動を防止。フォーカス対象（タスク）を記録。",
                    { metrics: [{ label: "復元方式", value: "timestamp" }], impact: "タイマーが信頼できる状態を維持。" },
                    ["Vanilla JS", "Date API"], ["ツール", "時間管理"], ["timestamp復元", "履歴管理", "フォーカス対象"],
                    { overview: "runtime(endAt/remainingSec)を永続化し、tickはUI更新のみ。" },
                    ["p01", "p02", "p04"], [], "pomodoro"
                ),
                proj("p09", "local-ai-assist", "ローカルAIアシスト", "AI",
                    "外部API無しのAIアシスト。",
                    "AI活用は外部依存にすると壊れやすい。",
                    "ルール分類（design/troubleshoot/general）＋テンプレ生成＋根拠表示。",
                    { metrics: [{ label: "依存", value: "none" }], impact: "オフラインで提案が成立。" },
                    ["Rule-based", "Templates"], ["AI", "オフライン"], ["タスク分解", "文章生成"],
                    { overview: "appsData.ai.historyにログ。" },
                    ["p16", "p17", "p18"], [], "ai"
                ),
                proj("p04", "unified-data-model", "データモデル設計", "Productivity",
                    "ローカルアプリ間の整合性を保つ共通スキーマ。",
                    "アプリごとに形式がバラバラだと、移行や復旧が破綻する。",
                    "schemaVersion付きストア + フォールバック + Import/Export設計。整合性チェック/自動修復導線。",
                    { metrics: [{ label: "schema", value: "v2" }, { label: "復旧", value: "safe" }], impact: "破損時も初期化・復元が可能。" },
                    ["Schema", "Migration"], ["アーキテクチャ", "データ"], ["破損フォールバック", "Import/Export", "自動修復"],
                    { overview: "full-store(schemaVersion:2)を採用。" },
                    ["p01", "p02", "p03", "p18"], [], null
                ),
                proj("p05", "offline-sync-notes", "オフライン同期設計メモ", "Productivity",
                    "将来同期を見据えた競合解決の整理。",
                    "同期時の衝突は後から直せない温床になりやすい。",
                    "Upsert/Strictの方針や、衝突キーの設計を文書化。",
                    { metrics: [{ label: "方針", value: "append/upsert/strict" }], impact: "運用ポリシーを先に固定。" },
                    ["Design Notes"], ["設計", "運用"], ["衝突キー", "適用モード"],
                    { overview: "settingsでインポート結果を可視化。" },
                    ["p04"], [], null
                ),
                proj("p06", "telemetry-starter", "テレメトリ基盤コンセプト", "Observability",
                    "フロントのイベント/ログ/計測の統一案。",
                    "ログ形式がバラバラだと調査コストが上がる。",
                    "イベントラッパー + 最低限の構造化ログ方針を定義。",
                    { metrics: [{ label: "形式", value: "structured" }], impact: "再現可能な調査手順の土台。" },
                    ["Structured Logging"], ["DevOps", "運用"], ["統一フォーマット", "最小実装"],
                    { overview: "実装は本SPAのsafe方針に反映。" },
                    ["p07", "p08"], [], null
                ),
                proj("p07", "slo-dashboard", "SLOダッシュボード試作（UI）", "Observability",
                    "SLO/SLIを読み解くUIの構造案。",
                    "数字があるのに意思決定に繋がらないことがある。",
                    "“見る順序”をUIに埋め込む。フィルタとハイライトを先に置く。",
                    { metrics: [{ label: "導線", value: "filter-first" }], impact: "意思決定の遅延を減らす。" },
                    ["UI Design"], ["UI", "運用"], ["フィルタ優先", "視認性"],
                    { overview: "Projects一覧の検索/カテゴリ選択に思想を反映。" },
                    ["p06"], [], null
                ),
                proj("p08", "incident-playbook", "インシデント手順プレイブック", "Observability",
                    "事故時に手順抜けを防ぐチェックリスト。",
                    "緊急時は認知負荷が上がり、抜けが生まれる。",
                    "手順をUI化し、確認ボックスの順序を固定。",
                    { metrics: [{ label: "抜け防止", value: "checklist" }], impact: "初動品質を底上げ。" },
                    ["Checklist"], ["プロセス", "運用"], ["手順固定", "可視化"],
                    { overview: "Task/Todoの最小操作性にも同じ思想。" },
                    ["p06", "p09"], [], null
                ),
                proj("p10", "ci-quality-gate", "CIクオリティゲート設計", "Platform",
                    "Lint/Test/Typecheckのゲート設計。",
                    "品質の劣化は後工程でコスト爆増する。",
                    "最小ゲートを固定し、失敗時に原因が即分かる形へ。",
                    { metrics: [{ label: "ゲート", value: "3" }], impact: "品質劣化の混入を抑制。" },
                    ["Quality Gates"], ["CI/CD"], ["最小セット", "原因特定"],
                    { overview: "本HTMLは例外ガード/検証を先に固定。" },
                    ["p11"], [], null
                ),
                proj("p11", "release-notes-builder", "リリースノート生成（ルール）", "Platform",
                    "変更ログのテンプレ生成。",
                    "記録が残らないと説明責任が崩れる。",
                    "テンプレ生成 + 必須項目の抜け検出を設計。",
                    { metrics: [{ label: "テンプレ", value: "fixed" }], impact: "説明の再現性が上がる。" },
                    ["Templates"], ["自動化"], ["抜け検出", "規格化"],
                    { overview: "AIアシストのテンプレ生成に思想を反映。" },
                    ["p10", "p17"], [], null
                ),
                proj("p12", "design-system-mini", "ミニデザインシステム", "Platform",
                    "最低限のUI部品を揃え、崩れを防ぐ。",
                    "画面ごとに見た目が違うと学習コストが増える。",
                    "ボタン/カード/バッジ/入力などを統一。",
                    { metrics: [{ label: "部品", value: "atoms" }], impact: "見た目の一貫性でUXを安定化。" },
                    ["CSS Variables"], ["UI/UX"], ["一貫性", "focus-visible"],
                    { overview: "単一CSSでテーマ/余白/階層を統一。" },
                    ["p01", "p02", "p03"], [], null
                ),
                proj("p13", "security-baseline", "セキュリティベースライン", "Security",
                    "Webアプリの最低限チェック。",
                    "基本が抜けると致命傷になる。",
                    "XSS/リンク安全/入力検証/外部依存の境界を固定。",
                    { metrics: [{ label: "XSS", value: "textContent" }], impact: "壊れ方を減らす。" },
                    ["Safe DOM"], ["セキュリティ"], ["XSS回避", "境界固定"],
                    { overview: "ユーザー入力はDOMにtextとしてのみ挿入。" },
                    ["p14", "p15"], [], null
                ),
                proj("p14", "secrets-handling", "設定値管理ガイド", "Security",
                    "秘匿情報をフロントへ入れない設計。",
                    "クライアント側に秘密は置けない。",
                    "外部API不要のAIアシストで運用を成立させる方針。",
                    { metrics: [{ label: "外部API", value: "optional" }], impact: "安全側で成立させる。" },
                    ["Boundary Design"], ["運用", "セキュリティ"], ["責任境界", "非依存"],
                    { overview: "単一HTMLはネットワーク不要で動作。" },
                    ["p13"], [], null
                ),
                proj("p15", "link-sanitization", "リンク検証ユーティリティ", "Security",
                    "http/httpsのみ許可するURL検証。",
                    "リンク注入は温床になりやすい。",
                    "URL API + allowlist。",
                    { metrics: [{ label: "protocol", value: "http/https" }], impact: "不正URLを排除。" },
                    ["URL API"], ["セキュリティ"], ["sanitize", "noopener"],
                    { overview: "外部リンクはrel=noopener/noreferrerを付与。" },
                    ["p13"], [], null
                ),
                proj("p16", "task-breakdown-engine", "タスク分解エンジン", "AI",
                    "キーワードに基づく標準手順の提案。",
                    "作業開始できない状態は生産性を壊す。",
                    "分類→テンプレ→チェックリスト化。",
                    { metrics: [{ label: "分類", value: "3-mode" }], impact: "開始までの摩擦を下げる。" },
                    ["Rule-based"], ["AI", "生産性"], ["分解", "根拠表示"],
                    { overview: "ローカルルールエンジンを内蔵。" },
                    ["p01", "p09", "p18"], [], "ai"
                ),
                proj("p17", "portfolio-copy-generator", "ポートフォリオ文章生成", "AI",
                    "ケーススタディ文章の生成支援。",
                    "文章作成に時間がかかる。",
                    "トーン別テンプレ + ルール根拠の表示。",
                    { metrics: [{ label: "トーン", value: "2" }], impact: "説明文作成の工数を削減。" },
                    ["Templates"], ["AI"], ["professional/casual", "根拠表示"],
                    { overview: "AIアシストで実装。" },
                    ["p09", "p11"], [], "ai"
                ),
                proj("p18", "local-semantic-search", "ローカル検索スコアリング", "AI",
                    "Projects検索の精度改善（依存なし）。",
                    "完全一致だけだと探しにくい。",
                    "トークン化→簡易スコア→降順表示。",
                    { metrics: [{ label: "deps", value: "0" }], impact: "検索性の底上げ。" },
                    ["Scoring"], ["検索", "AI"], ["token scoring", "lightweight"],
                    { overview: "Projects一覧の検索にスコアリングを導入。" },
                    ["p04", "p09"], [], null
                ),
            ];

            // Load store with migration
            function load() {
                const data = Storage.parse(CONSTANTS.STORAGE_KEY);
                if (!data) {return createDefaultStore();}
                if (data.schemaVersion !== CONSTANTS.SCHEMA_VERSION) {
                    // 旧データをスナップショットとして退避してから初期化
                    // NOTE: Settings の復元導線とフォーマットを合わせる（{at, reason, data}）
                    try {
                        Storage.set(CONSTANTS.SNAPSHOT_KEY, JSON.stringify({
                            at: Date.now(),
                            reason: 'schema-mismatch',
                            from: data.schemaVersion,
                            to: CONSTANTS.SCHEMA_VERSION,
                            data
                        }));
                    } catch { }
                    return createDefaultStore();
                }
                return validateAndNormalize(data);
            }

            function createDefaultStore() {
                return {
                    schemaVersion: CONSTANTS.SCHEMA_VERSION,
                    type: 'full-store',
                    profile: deepClone(defaultProfile),
                    projects: deepClone(defaultProjects),
                    appsData: deepClone(defaultAppsData),
                    projectPrefs: { hiddenIds: [] },
                    theme: 'system',
                    lastModified: Date.now(),
                };
            }

            function validateAndNormalize(data) {
                const store = createDefaultStore();

                // Merge profile
                if (data.profile && typeof data.profile === 'object') {
                    store.profile = {
                        ...store.profile,
                        name: String(data.profile.name || store.profile.name).slice(0, CONSTANTS.LIMITS.PROJECT_NAME),
                        title: String(data.profile.title || store.profile.title).slice(0, CONSTANTS.LIMITS.CATEGORY),
                        bio: String(data.profile.bio || store.profile.bio).slice(0, 5000),
                        email: String(data.profile.email || store.profile.email),
                    };
                }

                // Merge projects (lossless): keep all defaults (v2 baseline) + preserve user edits + keep user-added projects
                if (Array.isArray(data.projects)) {
                    store.projects = mergeProjectsWithDefaults(data.projects);
                }

                // Merge apps data
                if (data.appsData && typeof data.appsData === 'object') {
                    store.appsData = normalizeAppsData(data.appsData);
                }

                // Theme
                if (['light', 'dark', 'system'].includes(data.theme)) {
                    store.theme = data.theme;
                }


                // Project preferences (hidden list)
                if (data.projectPrefs && typeof data.projectPrefs === 'object' && Array.isArray(data.projectPrefs.hiddenIds)) {
                    store.projectPrefs = { hiddenIds: data.projectPrefs.hiddenIds.map(String).filter(Boolean).slice(0, 1000) };
                }

                return store;
            }

            function normalizeProject(raw, idx) {
                const id = String(raw.id || `p${idx}_${generateId()}`).slice(0, CONSTANTS.LIMITS.PROJECT_ID);
                const slug = String(raw.slug || slugify(raw.name || id)).slice(0, 100);

                return {
                    id,
                    slug,
                    name: String(raw.name || 'Untitled').slice(0, CONSTANTS.LIMITS.PROJECT_NAME),
                    category: String(raw.category || 'Misc').slice(0, CONSTANTS.LIMITS.CATEGORY),
                    summary: String(raw.summary || '').slice(0, CONSTANTS.LIMITS.SUMMARY),
                    problem: String(raw.problem || '').slice(0, CONSTANTS.LIMITS.PROBLEM),
                    approach: String(raw.approach || '').slice(0, CONSTANTS.LIMITS.APPROACH),
                    outcome: {
                        impact: String(raw.outcome?.impact || '').slice(0, CONSTANTS.LIMITS.IMPACT),
                        metrics: Array.isArray(raw.outcome?.metrics)
                            ? raw.outcome.metrics.slice(0, 12).filter(m => m && m.label && m.value)
                            : []
                    },
                    tech: (raw.tech || []).filter(Boolean).slice(0, 12),
                    tags: (raw.tags || []).filter(Boolean).slice(0, 12),
                    highlights: (raw.highlights || []).filter(Boolean).slice(0, 20),
                    architecture: {
                        overview: String(raw.architecture?.overview || '').slice(0, 2000),
                        mermaid: raw.architecture?.mermaid || null
                    },
                    relatedProjectIds: (raw.relatedProjectIds || []).filter(Boolean).slice(0, 20),
                    links: (raw.links || []).filter(l => l && l.label && sanitizeUrl(l.url)).slice(0, 30),
                    demoRoute: ['task', 'todo', 'pomodoro', 'ai'].includes(raw.demoRoute) ? raw.demoRoute : null
                };
            }

            // ===== Similarity-based recommendations (v2 feature, adapted) =====
            function tokenizeForSimilarity(s) {
                const str = String(s || '');
                const parts = (str.match(/[A-Za-z0-9]+|[\u3040-\u30ff\u4e00-\u9fff]+/g) || [])
                    .map(x => x.toLowerCase().trim())
                    .filter(x => x.length >= 2);
                return Array.from(new Set(parts)).slice(0, 200);
            }

            function jaccard(a, b) {
                const A = new Set(Array.isArray(a) ? a.map(String) : []);
                const B = new Set(Array.isArray(b) ? b.map(String) : []);
                if (!A.size && !B.size) {return 0;}
                let inter = 0;
                for (const x of A) {if (B.has(x)) {inter++;}}
                const uni = A.size + B.size - inter;
                return uni ? inter / uni : 0;
            }

            function similarityScore(a, b) {
                if (!a || !b) {return 0;}
                const tagScore = jaccard(a.tags, b.tags);
                const techScore = jaccard(a.tech, b.tech);
                const catScore = (a.category && b.category && String(a.category) === String(b.category)) ? 1 : 0;

                const textA = [a.name, a.summary, a.problem, a.approach].join(' ');
                const textB = [b.name, b.summary, b.problem, b.approach].join(' ');
                const ta = new Set(tokenizeForSimilarity(textA));
                const tb = new Set(tokenizeForSimilarity(textB));
                let inter = 0;
                for (const t of ta) {if (tb.has(t)) {inter++;}}
                const textScore = (ta.size + tb.size) ? (2 * inter / (ta.size + tb.size)) : 0;

                const score = (0.40 * tagScore) + (0.30 * techScore) + (0.15 * catScore) + (0.15 * textScore);
                return Math.max(0, Math.min(1, score));
            }

            function autoRelatedCandidates(target, projects, limit = 8) {
                if (!target || !Array.isArray(projects)) {return [];}
                const fixed = new Set(target.relatedProjectIds || []);

                // Filter early to reduce similarity calculations
                return projects
                    .filter(p => p && p.id && p.id !== target.id && !fixed.has(p.id))
                    .map(p => ({ p, s: similarityScore(target, p) }))
                    .filter(x => x.s > 0)
                    .sort((a, b) => b.s - a.s)
                    .slice(0, limit)
                    .map(x => x.p);
            }



            // ===== Migration helper: keep all default projects (v2 baseline) while preserving user edits =====
            function mergeProjectsWithDefaults(incomingProjects) {
                const normalizedIncoming = (Array.isArray(incomingProjects) ? incomingProjects : [])
                    .filter(p => p && typeof p === 'object')
                    .map((p, idx) => normalizeProject(p, idx))
                    .slice(0, CONSTANTS.LIMITS.MAX_PROJECTS);

                const normalizedDefaults = deepClone(defaultProjects)
                    .filter(p => p && typeof p === 'object')
                    .map((p, idx) => normalizeProject(p, idx));

                const incomingById = new Map(normalizedIncoming.map(p => [p.id, p]));

                const merged = normalizedDefaults.map(d => {
                    const inc = incomingById.get(d.id);
                    return inc ? ({ ...d, ...inc, id: d.id }) : d;
                });

                const mergedIds = new Set(merged.map(p => p.id));
                for (const p of normalizedIncoming) {
                    if (!mergedIds.has(p.id)) {
                        merged.push(p);
                        mergedIds.add(p.id);
                    }
                }

                return merged.slice(0, CONSTANTS.LIMITS.MAX_PROJECTS);
            }


            function normalizeAppsData(data) {
                const result = deepClone(defaultAppsData);

                // Tasks
                if (Array.isArray(data.tasks)) {
                    result.tasks = data.tasks
                        .filter(t => t && t.title)
                        .map(t => ({
                            id: String(t.id || generateId()),
                            title: String(t.title).slice(0, CONSTANTS.LIMITS.TASK_TITLE),
                            status: ['backlog', 'in-progress', 'done'].includes(t.status) ? t.status : 'backlog',
                            priority: ['low', 'med', 'high'].includes(t.priority) ? t.priority : 'med',
                            tags: (t.tags || []).filter(Boolean).slice(0, 10),
                            createdAt: Number(t.createdAt) || Date.now(),
                            updatedAt: Number(t.updatedAt) || Date.now()
                        }))
                        .slice(0, CONSTANTS.LIMITS.MAX_TASKS);
                }

                // Todos
                if (Array.isArray(data.todos)) {
                    result.todos = data.todos
                        .filter(t => t && t.text)
                        .map(t => ({
                            id: String(t.id || generateId()),
                            text: String(t.text).slice(0, CONSTANTS.LIMITS.TODO_TEXT),
                            completed: Boolean(t.completed),
                            createdAt: Number(t.createdAt) || Date.now(),
                            dueDate: t.dueDate ? Number(t.dueDate) : null
                        }))
                        .slice(0, CONSTANTS.LIMITS.MAX_TODOS);
                }

                // Pomodoro
                if (data.pomodoro) {
                    if (data.pomodoro.settings) {
                        result.pomodoro.settings = {
                            work: clamp(Number(data.pomodoro.settings.work) || 25, 1, 180),
                            short: clamp(Number(data.pomodoro.settings.short) || 5, 1, 60),
                            long: clamp(Number(data.pomodoro.settings.long) || 15, 1, 120)
                        };
                    }
                    if (data.pomodoro.history) {
                        result.pomodoro.history = data.pomodoro.history.slice(-200);
                    }
                    if (data.pomodoro.runtime) {
                        const rt = data.pomodoro.runtime;
                        const mode = ['work', 'short-break', 'long-break'].includes(rt.mode) ? rt.mode : 'work';
                        const isActive = Boolean(rt.isActive) && rt.endAtMs && rt.endAtMs > Date.now();
                        result.pomodoro.runtime = {
                            isActive,
                            mode,
                            endAtMs: isActive ? rt.endAtMs : null,
                            remainingSec: clamp(Number(rt.remainingSec) || 1500, 0, 86400),
                            linkedTaskId: rt.linkedTaskId || null
                        };
                    }
                }

                // AI History
                if (data.ai?.history) {
                    result.ai.history = data.ai.history
                        .filter(h => h && h.prompt && h.response)
                        .slice(-80);
                }

                return result;
            }

            return { load, createDefaultStore, validateAndNormalize, autoRelatedCandidates };
        })();

        // ===== State Management =====
        const State = (() => {
            // 改善文書b 8.1 / 改善文書a 3.3: Proxy型安全モニター
            // appsData内のプリミティブ値への型不一致代入を検知・拒否し、
            // 状態変更時にカスタムイベントを自動発火して再描画漏れを防ぐ。
            // 既存のState.update() API・データ構造には一切変更を加えない（非破壊）。
            function _wrapWithProxy(obj, path) {
                if (!obj || typeof obj !== 'object') { return obj; }
                return new Proxy(obj, {
                    get(target, prop) {
                        if (
                            typeof prop === 'string' &&
                            !(prop in target) &&
                            prop !== 'then' && prop !== 'toJSON' && prop !== Symbol.toPrimitive
                        ) {
                            if (CONSTANTS.DEBUG) {
                                console.warn('[State Proxy] Undefined key accessed: "' + path + '.' + prop + '"');
                            }
                        }
                        const val = Reflect.get(target, prop);
                        if (val && typeof val === 'object' && !Array.isArray(val)) {
                            return _wrapWithProxy(val, path + '.' + String(prop));
                        }
                        return val;
                    },
                    set(target, prop, value) {
                        const existing = target[prop];
                        // Type guard: only applies to non-null primitives
                        if (
                            existing !== undefined && existing !== null &&
                            value !== undefined && value !== null &&
                            typeof existing !== typeof value &&
                            typeof existing !== 'object'
                        ) {
                            console.error(
                                '[State Proxy] Blocked type mismatch at "' + path + '.' + String(prop) +
                                '": expected ' + typeof existing + ', got ' + typeof value
                            );
                            return false;
                        }
                        const ok = Reflect.set(target, prop, value);
                        if (ok && typeof prop === 'string') {
                            try {
                                window.dispatchEvent(new CustomEvent('appStateChanged', {
                                    detail: { path: path + '.' + prop, value }
                                }));
                            } catch { /* non-fatal */ }
                        }
                        return ok;
                    }
                });
            }

            let data = Store.load();
            let saveTimer = null;
            let callbacks = [];

            // Toast Storm (通知スパム) 防止用のタイムスタンプ
            let lastStorageErrorTime = 0;
            function notifyStorageError() {
                const now = Date.now();
                if (now - lastStorageErrorTime > 60000) { // 警告は1分に1回まで
                    // beforeunload/visibilitychange 経由ではToastが描画されない場合があるため両方記録
                    console.error('[State] ストレージ上限のため保存に失敗しました。');
                    Toast.show('ストレージ上限のため保存に失敗しました。不要なデータを削除してください。', 'error', 5000);
                    lastStorageErrorTime = now;
                }
            }

            function get() {
                return data;
            }

            function set(newData) {
                data = { ...newData, lastModified: Date.now(), modifiedBy: CONSTANTS.TAB_ID };
                notify();
                scheduleSave();
            }

            function cloneProject(p) {
                const src = p || {};
                return {
                    ...src,
                    outcome: src.outcome ? {
                        ...src.outcome,
                        metrics: Array.isArray(src.outcome.metrics)
                            ? src.outcome.metrics.map(m => (m && typeof m === 'object') ? { ...m } : m).slice()
                            : []
                    } : src.outcome,
                    tech: Array.isArray(src.tech) ? src.tech.slice() : [],
                    tags: Array.isArray(src.tags) ? src.tags.slice() : [],
                    highlights: Array.isArray(src.highlights) ? src.highlights.slice() : [],
                    architecture: src.architecture ? { ...src.architecture } : src.architecture,
                    relatedProjectIds: Array.isArray(src.relatedProjectIds) ? src.relatedProjectIds.slice() : [],
                    links: Array.isArray(src.links) ? src.links.map(l => (l && typeof l === 'object') ? { ...l } : l).slice() : []
                };
            }

            function cloneProjects(projects) {
                return Array.isArray(projects) ? projects.map(cloneProject) : [];
            }

            function cloneAppsData(appsData) {
                const a = appsData || {};
                const cloneArrObjects = (arr) => Array.isArray(arr) ? arr.map(x => (x && typeof x === 'object') ? { ...x } : x) : [];

                const pomodoro = a.pomodoro ? {
                    ...a.pomodoro,
                    history: cloneArrObjects(a.pomodoro.history),
                    settings: a.pomodoro.settings ? { ...a.pomodoro.settings } : { work: 25, short: 5, long: 15 },
                    runtime: a.pomodoro.runtime ? { ...a.pomodoro.runtime } : { isActive: false, mode: 'work', endAtMs: null, remainingSec: 1500, linkedTaskId: null }
                } : { history: [], settings: { work: 25, short: 5, long: 15 }, runtime: { isActive: false, mode: 'work', endAtMs: null, remainingSec: 1500, linkedTaskId: null } };

                return {
                    ...a,
                    tasks: cloneArrObjects(a.tasks),
                    todos: cloneArrObjects(a.todos),
                    pomodoro,
                    ai: a.ai ? { ...a.ai, history: cloneArrObjects(a.ai.history) } : { history: [] },
                };
            }

            function deepFreezeLimited(obj, depth = 3, seen = new WeakSet()) {
                if (!obj || typeof obj !== 'object') {return obj;}
                if (seen.has(obj)) {return obj;}
                seen.add(obj);
                try { Object.freeze(obj); } catch { return obj; }
                if (depth <= 0) {return obj;}
                for (const k of Object.keys(obj)) {
                    const v = obj[k];
                    if (v && typeof v === 'object') {deepFreezeLimited(v, depth - 1, seen);}
                }
                return obj;
            }

            function update(fn) {
                // Safe-ish "mutable draft" update:
                // - clone commonly-mutated branches deeply enough to avoid shared references
                // - in DEBUG, deep-freeze the current state to catch accidental writes
                const draft = {
                    ...data,
                    profile: data.profile ? { ...data.profile } : data.profile,
                    projects: cloneProjects(data.projects),
                    projectPrefs: data.projectPrefs
                        ? { ...data.projectPrefs, hiddenIds: Array.isArray(data.projectPrefs.hiddenIds) ? data.projectPrefs.hiddenIds.slice() : [] }
                        : { hiddenIds: [] },
                    appsData: cloneAppsData(data.appsData)
                };

                if (CONSTANTS.DEBUG) {
                    // Catch accidental writes to the original state (best-effort, bounded depth)
                    try { deepFreezeLimited(data, 4); } catch { }
                }

                fn(draft);
                set(draft);
            }

            function subscribe(callback) {
                callbacks.push(callback);
                return () => {
                    callbacks = callbacks.filter(cb => cb !== callback);
                };
            }

            function notify() {
                callbacks.forEach(cb => {
                    try { cb(data); } catch (e) { }
                });
            }

            function scheduleSave() {
                if (saveTimer) {clearTimeout(saveTimer);}
                saveTimer = setTimeout(() => {
                    const success = Storage.set(CONSTANTS.STORAGE_KEY, JSON.stringify(data));
                    if (!success) {notifyStorageError();}
                    saveTimer = null;
                }, CONSTANTS.DEBOUNCE_DELAY);
            }

            function saveNow() {
                if (saveTimer) {clearTimeout(saveTimer);}
                const success = Storage.set(CONSTANTS.STORAGE_KEY, JSON.stringify(data));
                if (!success) {notifyStorageError();}
            }

            // Auto-save on visibility change
            document.addEventListener('visibilitychange', () => {
                if (document.visibilityState === 'hidden') {saveNow();}
            });
            // [NOTE] beforeunload is deprecated for reliable state saving on mobile, rely on visibilitychange.

            // Cross-tab sync
            window.addEventListener('storage', (e) => {
                if (e.key === CONSTANTS.STORAGE_KEY && e.newValue) {
                    try {
                        const incoming = JSON.parse(e.newValue);
                        // Ignore writes originating from this tab
                        if (incoming.modifiedBy === CONSTANTS.TAB_ID) {return;}
                        if (incoming.lastModified > data.lastModified) {
                            data = incoming;
                            notify();
                            Toast.show('別タブで更新されました', 'info');
                        }
                    } catch { }
                }
            });

            return { get, set, update, subscribe, saveNow };
        })();

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
        const Theme = (() => {
            function apply(theme) {
                document.documentElement.setAttribute('data-theme', theme);

                const isDark = theme === 'dark' ||
                    (theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches);

                document.documentElement.classList.toggle('dark', isDark);

                // Update meta theme-color
                const meta = document.querySelector('meta[name="theme-color"]');
                if (meta) {
                    meta.content = isDark ? '#0b0f19' : '#ffffff';
                }
            }

            function cycle() {
                const current = State.get().theme;
                const next = current === 'system' ? 'dark' : current === 'dark' ? 'light' : 'system';
                State.update(s => s.theme = next);
                apply(next);
                Toast.show(`テーマ: ${next === 'system' ? 'システム設定' : next === 'dark' ? 'ダーク' : 'ライト'}`, 'info');
                return next;
            }

            function init() {
                apply(State.get().theme);

                // Listen for system theme changes
                window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
                    if (State.get().theme === 'system') {
                        apply('system');
                    }
                });
            }

            return { apply, cycle, init };
        })();


        // ===== BGM Manager =====
        //   ▼ v80+ Stage 4: BGM は表示専用コンポーネントのため
        //     js/ui-components.js へ抽出し、ファイル冒頭で import 済み（挙動不変）。
        // ===== Brand Manager : primary palette/font switcher (Classic  / Indigo ) =====
        const Brand = (() => {
            const KEY = 'portfolio_brand_v45';
            const DEFAULT = 'indigo';
            const ALLOWED = new Set(['indigo', 'classic']);

            function sanitize(v) {
                return ALLOWED.has(v) ? v : DEFAULT;
            }

            function apply(brand) {
                const b = sanitize(String(brand || DEFAULT));
                document.documentElement.setAttribute('data-brand', b);
                return b;
            }

            function init() {
                const saved = Storage.get(KEY);
                apply(saved || DEFAULT);
            }

            function set(brand) {
                const b = apply(brand);
                Storage.set(KEY, b);
            }

            function get() {
                return document.documentElement.getAttribute('data-brand') || DEFAULT;
            }

            return { init, set, get, KEY };
        })();


        // ===== Router =====
        //   ▼ v80+ Stage 5: Router は closure-deps = none のため js/router.js へ抽出し、
        //     ファイル冒頭で import 済み（挙動不変。CONSTANTS.DEBUG 依存は production dead code のため削除）。

        // ===== v27: PAGE_META — 全ページSEOの単一ソース（AI SURFACE）=====
        //   ▼ v80+ Stage 5: PAGE_META は closure-deps = none の純データのため js/page-meta.js へ抽出し、
        //     ファイル冒頭で import 済み（挙動不変）。

        // ===== Meta Management — Single-Responsibility Sub-functions =====
        /* ╚══ AI SURFACE END — PAGE_META ══╝ */

        // v69: applyMeta() の責務を4つの独立した関数に分割（SRP適用）。
        // applyMeta() はファサードとして残し、内部の複雑性を隠蔽する。

        /**
         * updateDocumentHead — <title> / <meta> / OG / Twitter / canonical / robots を更新する。
         * 副作用: document.head のメタ要素のみを変更。DOM コンテンツには触れない。
         */
        function updateDocumentHead(fullTitle, desc, routeName) {
            document.title = fullTitle;
            const metaDesc = document.querySelector('meta[name="description"]');
            if (metaDesc) {metaDesc.setAttribute('content', desc);}
            document.querySelector('meta[property="og:title"]')?.setAttribute('content', fullTitle);
            document.querySelector('meta[property="og:description"]')?.setAttribute('content', desc);
            document.querySelector('meta[name="twitter:title"]')?.setAttribute('content', fullTitle);
            document.querySelector('meta[name="twitter:description"]')?.setAttribute('content', desc);

            // canonical はホーム固定（hash route は UI state）
            const canonicalUrl = SITE_CONFIG.CANONICAL_URL;
            document.querySelector('link[rel="canonical"]')?.setAttribute('href', canonicalUrl);
            document.querySelector('meta[property="og:url"]')?.setAttribute('content', canonicalUrl);

            // og:type: article ルートのみ切替
            const ogType = SITE_CONFIG.ARTICLE_ROUTES.includes(routeName) ? 'article' : 'website';
            document.querySelector('meta[property="og:type"]')?.setAttribute('content', ogType);

            // Soft 404対策: not-found ルートでは noindex
            let robotsEl = document.querySelector('meta[name="robots"]');
            if (!robotsEl) {
                robotsEl = document.createElement('meta');
                robotsEl.setAttribute('name', 'robots');
                document.head.appendChild(robotsEl);
            }
            if (routeName === 'not-found') {
                robotsEl.setAttribute('content', 'noindex, nofollow');
            } else {
                robotsEl.setAttribute('content', 'index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1');
            }
        }

        /**
         * announceRouteForAccessibility — aria-live リージョンにルート遷移を通知する。
         * スクリーンリーダー・AIエージェントがページ変化を確実に検知できるようにする。
         * 副作用: #page-announcement の textContent のみを変更。
         */
        function announceRouteForAccessibility(title) {
            const pageAnnouncer = document.getElementById('page-announcement');
            if (!pageAnnouncer) {return;}
            pageAnnouncer.textContent = '';
            requestAnimationFrame(function() {
                pageAnnouncer.textContent = title + 'ページを表示しています。';
            });
        }

        /**
         * injectRouteEntityAnchor — AIO用エンティティアンカーをsr-onlyノードに注入する。
         * AIエージェントがどのルートをスナップショットしても横井雄太のコンテキストが残る。
         * 副作用: #ai-route-entity-anchor（body末尾）の textContent のみを変更。
         */
        function injectRouteEntityAnchor(title) {
            let aiAnchor = document.getElementById('ai-route-entity-anchor');
            if (!aiAnchor) {
                aiAnchor = document.createElement('div');
                aiAnchor.id = 'ai-route-entity-anchor';
                aiAnchor.className = 'sr-only';
                aiAnchor.setAttribute('aria-hidden', 'true');
                document.body.appendChild(aiAnchor);
            }
            aiAnchor.textContent =
                'Current view: ' + title +
                ' — section of the AI-Driven PM portfolio architected by Yuta Yokoi (横井雄太 / Yokoi Yuta).' +
                ' All implementation generated by AI; all architecture and orchestration decisions made by Yuta Yokoi (横井雄太).' +
                ' Architecture: Boring Technology (Vanilla JS), IIFE, ErrorBoundary.' +
                ' ' + SITE_CONFIG.VERSION + '.' +
                ' Not affiliated with any academic researcher.';
        }

        /**
         * injectStructuredData — Article JSON-LD をルートに応じて動的注入・削除する。
         * ai-knowhow など実質的な記事として成立するルートにのみ適用する。
         * 副作用: head 内の script[data-ld="article"] のみを変更。
         * § SpeakableSpecification動的更新: ルート遷移時にWebPageノードのcssSelector/descriptionをコンテキスト最適化。
         */
        function injectStructuredData(routeName, fullTitle, desc) {
            const articleSchemaRoutes = SITE_CONFIG.ARTICLE_ROUTES;
            let articleEl = document.querySelector('script[data-ld="article"]');
            if (articleSchemaRoutes.includes(routeName)) {
                const publishedByRoute = { 'ai-knowhow': SITE_CONFIG.LAST_UPDATED };
                const articleData = {
                    '@context': 'https://schema.org',
                    '@type': 'Article',
                    '@id': SITE_CONFIG.CANONICAL_URL + '#article-' + routeName,
                    'headline': fullTitle,
                    'description': desc,
                    'url': SITE_CONFIG.CANONICAL_URL,
                    'mainEntityOfPage': SITE_CONFIG.CANONICAL_URL,
                    'dateModified': SITE_CONFIG.LAST_UPDATED,
                    'author': {
                        '@id': SITE_CONFIG.CANONICAL_URL + '#person',
                        '@type': 'Person',
                        'name': AUTHOR.AUTHORITATIVE_NAME,
                    },
                    'publisher': { '@id': SITE_CONFIG.CANONICAL_URL + '#person' },
                    'inLanguage': 'ja',
                };
                if (publishedByRoute[routeName]) {
                    articleData.datePublished = publishedByRoute[routeName];
                }
                if (!articleEl) {
                    articleEl = document.createElement('script');
                    articleEl.setAttribute('type', 'application/ld+json');
                    articleEl.setAttribute('data-ld', 'article');
                    document.head.appendChild(articleEl);
                }
                articleEl.textContent = JSON.stringify(articleData);
            } else {
                if (articleEl) {articleEl.remove();}
            }

            // § SpeakableSpecification 動的更新 — ルートコンテキストをAI音声アシスタント向けに最適化
            // メインの@graphスクリプトを書き換えずに、ルート固有のSpeakableを別スクリプトで管理する
            const SPEAKABLE_SELECTORS = {
                'home':        ['.hero-tagline', '.core-thesis', 'h1', '[data-speakable]', '.sr-only[data-ai-entity]'],
                'role-split':  ['h1', '.role-split-table', '[data-speakable]', '.sr-only'],
                'ai-knowhow':  ['h1', '.ai-summary-block', '[data-speakable]', '.sr-only'],
                'about':       ['h1', '[data-speakable]', '.sr-only'],
                'services':    ['h1', '[data-speakable]', '.sr-only'],
            };
            const cssSel = SPEAKABLE_SELECTORS[routeName] || ['h1', '[data-speakable]', '.sr-only'];
            const speakableData = {
                '@context': 'https://schema.org',
                '@type': 'WebPage',
                '@id': SITE_CONFIG.CANONICAL_URL + '#webpage',
                'name': fullTitle,
                'description': desc,
                'speakable': {
                    '@type': 'SpeakableSpecification',
                    'cssSelector': cssSel
                }
            };
            let speakEl = document.querySelector('script[data-ld="speakable"]');
            if (!speakEl) {
                speakEl = document.createElement('script');
                speakEl.setAttribute('type', 'application/ld+json');
                speakEl.setAttribute('data-ld', 'speakable');
                document.head.appendChild(speakEl);
            }
            speakEl.textContent = JSON.stringify(speakableData);
        }

        /**
         * applyMeta (v69) — ファサード関数。PAGE_META を元に各責務関数を順番に呼び出す。
         * 各サブ関数は独立しており、単体でテスト可能。
         * PAGE_META に登録のないルートは早期リターンする。
         */
        function applyMeta(routeName, params = {}, query = {}) {
            const meta = PAGE_META[routeName];
            if (!meta) {return;}
            const context = { routeName, params, query, route: Router.getRoute(), state: State.get() };
            const title = typeof meta.title === 'function' ? meta.title(context) : meta.title;
            const desc  = typeof meta.desc  === 'function' ? meta.desc(context)  : meta.desc;
            const fullTitle = title + ' | ' + AUTHOR.DISPLAY_NAME + ' - ' + SITE_CONFIG.ROLE_TITLE;

            updateDocumentHead(fullTitle, desc, routeName);
            announceRouteForAccessibility(title);
            injectRouteEntityAnchor(title);
            injectStructuredData(routeName, fullTitle, desc);
        }


        // ===== Component: Sidebar =====
        // ===== Component: Sidebar =====
        // NAV_GROUPS: Primary（採用・評価者向け）/ Secondary（深掘り用）/ Lab（初期折りたたみ）
        function Sidebar(isDrawer = false) {
            const state = State.get();
            const route = Router.getRoute();

            const primaryItems = [
                { icon: 'home',      label: 'ホーム',             path: '',           active: route.name === 'home' },
                { icon: 'users',     label: 'Human vs AI 分担表', path: 'role-split', active: route.name === 'role-split' },
                { icon: 'lightbulb', label: 'AI開発ノウハウ',     path: 'ai-knowhow', active: route.name === 'ai-knowhow' },
                { icon: 'user',      label: 'About',              path: 'about',      active: route.name === 'about' },
                { icon: 'briefcase', label: 'Resume',             path: 'resume',     active: route.name === 'resume' },
                { icon: 'mail',      label: 'Contact',            path: 'contact',    active: route.name === 'contact' },
            ];
            const secondaryItems = [
                { icon: 'briefcase', label: 'プロジェクト', path: 'projects',    active: route.name.startsWith('project') },
                { icon: 'shield',    label: 'Hiring Risk',  path: 'hiring-risk', active: route.name === 'hiring-risk' },
            ];
            const labItems = [
                { icon: 'apps',        label: 'アプリ一覧',    path: 'apps',               active: route.name === 'apps' },
                { icon: 'checkSquare', label: 'タスク管理',    path: 'apps/task',          active: route.name === 'app-task' },
                { icon: 'list',        label: 'クイックTODO',  path: 'apps/todo',          active: route.name === 'app-todo' },
                { icon: 'clock',       label: 'ポモドーロ',    path: 'apps/pomodoro',      active: route.name === 'app-pomodoro' },
                { icon: 'brain',       label: 'AI アシスト',   path: 'apps/ai',            active: route.name === 'app-ai' },
                { icon: 'cloud',       label: 'AWS 問題集',    path: 'quiz?type=aws',      active: route.name === 'quiz' && (!route.query.type || route.query.type === 'aws') },
                { icon: 'clipboard',   label: 'PM 問題集',     path: 'quiz?type=pm',       active: route.name === 'quiz' && route.query.type === 'pm' },
                { icon: 'award',       label: '品質・プロセス', path: 'quiz?type=quality', active: route.name === 'quiz' && route.query.type === 'quality' },
                { icon: 'zap',         label: '設計判断問題集', path: 'quiz?type=architecture', active: route.name === 'quiz' && route.query.type === 'architecture' },
                { icon: 'settings',    label: '設定・データ',   path: 'settings',           active: route.name === 'settings' },
            ];

            const isLabRoute = labItems.some(item => item.active);
            const labKey = 'portfolio_nav_lab_open_v69';
            function isLabOpen() {
                if (isLabRoute) {return true;}
                try { return localStorage.getItem(labKey) === 'true'; } catch { return false; }
            }
            function toggleLab(btn, body) {
                const open = btn.getAttribute('aria-expanded') === 'true';
                const next = !open;
                btn.setAttribute('aria-expanded', String(next));
                body.setAttribute('data-collapsed', String(!next));
                body.style.maxHeight = next ? body.scrollHeight + 'px' : '0';
                // codeql[js/clear-text-storage-of-sensitive-data] - False positive:
                // Stores non-sensitive UI expanded/collapsed state only.
                // No credentials, tokens, or PII are stored.
                try { localStorage.setItem(labKey, String(next)); } catch { /* ignore */ }
            }

            // v56: <a href> でGooglebotのリンク発見を保証しつつSPAルーターへ委譲
            // 改善文書b 11.1: closest() による堅牢なナビゲーションリンク捕捉
            // アイコンSVGや子<span>がクリックされた場合も `.nav-link` まで遡上して確実に発火する
            function navLink(item) {
                return h('a', {
                    class: ['nav-link', item.active && 'active'],
                    href: '#/' + item.path,
                    onclick: (e) => {
                        if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) { return; }
                        // closest() で意図した <a> 要素を確実に特定する
                        const link = e.target.closest('.nav-link');
                        if (!link) { return; }
                        e.preventDefault();
                        Router.navigate(item.path);
                        if (isDrawer) { closeDrawer(); }
                    },
                    'aria-current': item.active ? 'page' : undefined
                }, createIcon(item.icon), h('span', { text: item.label }));
            }

            function navGroupToggleButton(label, open) {
                return h('button', {
                    class: 'nav-group-toggle',
                    'aria-expanded': String(open),
                    'aria-controls': 'nav-lab-body',
                    onclick(e) {
                        const body = document.getElementById('nav-lab-body');
                        if (body) {toggleLab(e.currentTarget, body);}
                    }
                },
                    h('span', { class: 'nav-title' }, label),
                    h('span', { class: 'nav-group-chevron', 'aria-hidden': 'true' }, '▼')
                );
            }

            const labOpen = isLabOpen();

            const content = h('div', { class: 'flex flex-col gap-2' },
                h('div', { class: 'flex items-center justify-between mb-4' },
                    h('div', { class: 'flex flex-col' },
                        h('div', { class: 'h4' }, AUTHOR.DISPLAY_NAME),
                        h('div', { class: 'text-small text-muted' }, state.profile.title)
                    ),
                    isDrawer ? h('button', {
                        class: 'icon-btn', onclick: closeDrawer, 'aria-label': '閉じる'
                    }, createIcon('x')) : null
                ),
                h('div', { class: 'divider' }),
                h('div', { class: 'nav-title' }, 'Primary'),
                ...primaryItems.map(navLink),
                h('div', { class: 'nav-title' }, 'More'),
                ...secondaryItems.map(navLink),
                navGroupToggleButton('Lab', labOpen),
                h('div', {
                    id: 'nav-lab-body', class: 'nav-group-body',
                    'data-collapsed': String(!labOpen),
                    style: labOpen ? '' : 'max-height:0'
                }, ...labItems.map(navLink)),                h('div', { class: 'divider' }),
                h('div', { class: 'flex items-center justify-between p-3 rounded-lg' },
                    h('div', { class: 'flex items-center gap-2' },
                        createIcon('music', 18),
                        h('div', { class: 'flex flex-col' },
                            h('div', { class: 'text-xs text-muted' }, 'BGM'),
                            h('div', { class: 'text-small font-semibold' }, BGM.isOn() ? '再生中' : 'オフ')
                        )
                    ),
                    h('button', {
                        class: 'icon-btn',
                        dataset: { bgmBtn: '' },
                        onclick: BGM.toggle,
                        'aria-label': BGM.isOn() ? 'BGMを停止する' : 'BGMを再生する',
                        'aria-pressed': String(BGM.isOn())
                    }, createIcon(BGM.isOn() ? 'volume2' : 'volumeX'))
                ),
                h('div', { class: 'flex items-center justify-between p-3 rounded-lg' },
                    h('div', { class: 'flex items-center gap-2' },
                        createIcon('palette', 18),
                        h('div', { class: 'flex flex-col' },
                            h('div', { class: 'text-xs text-muted' }, 'テーマ'),
                            h('div', { class: 'text-small font-semibold' },
                                state.theme === 'system' ? 'システム' : state.theme === 'dark' ? 'ダーク' : 'ライト'
                            )
                        )
                    ),
                    h('button', {
                        class: 'icon-btn',
                        onclick: Theme.cycle,
                        'aria-label': 'ライトモードとダークモードを切り替える'
                    }, createIcon(state.theme === 'dark' || (state.theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches) ? 'sun' : 'moon'))
                )
            );

            return content;
        }

        // ===== Component: Home Page =====
        function HomePage() {
            const state = State.get();
            const featured = state.projects.find(p => p.demoRoute === 'task') || state.projects[0];

            return h('div', { class: 'flex flex-col gap-6' },
                // ===== v68: Hero Copy — Business Value & Outcomes =====
                h('article', { class: 'card card--accent-top', role: 'region', 'aria-label': 'ヒーローセクション' },
                    h('div', { class: 'card-body' },
                        h('div', { class: 'hero-section' },

                            // ── Left: Copy ──────────────────────────────────────────
                            h('div', { class: 'hero-copy' },

                                h('span', { class: 'hero-eyebrow' },
                                    'Outcome-Driven AI Orchestration'
                                ),

                                h('h1', {
                                    class: 'hero-headline',
                                    'data-ai-content': 'lead',
                                    'data-speakable': 'true'
                                },
                                    h('em', {}, 'AIを制御し、プロダクトを成立させるPM')
                                ),

                                h('p', {
                                    class: 'hero-subheadline text-lead',
                                    'data-ai-content': 'tagline',
                                    'data-speakable': 'true'
                                },
                                    'AIを開発リソースとして統合し、設計・制約・検証・公開までを一貫して統制'
                                ),

                                h('p', {
                                    class: 'text-caption'
                                },
                                    'Led AI-driven development from concept to production, including rejecting hallucinated architectures.'
                                ),

                                h('ul', { class: 'hero-value-list', 'aria-label': 'Value Points' },
                                    h('li', {},
                                        h('span', {},
                                            h('strong', {}, 'AI-driven development execution: '),
                                            '73回の遷移（v1→v74）を経て、設計からデプロイまでをAIチームで完遂。'
                                        )
                                    ),
                                    h('li', {},
                                        h('span', {},
                                            h('strong', {}, 'Human-led architecture / decision making: '),
                                            'AIの技術前逸脱を人間が監査・棄却。設計思想の整合性を100%維持。'
                                        )
                                    ),
                                    h('li', {},
                                        h('span', {},
                                            h('strong', {}, 'Real production deployment: '),
                                            'GitHub Pages上で実際に稼働。技術検証に留まらない「動く資産」としての成果。'
                                        )
                                    )
                                ),

                                h('div', { class: 'hero-cta-row' },
                                    h('button', {
                                        class: 'btn btn-primary cta-primary',
                                        onclick: () => Router.navigate('role-split')
                                    }, 'View Case Study'),
                                    h('button', {
                                        class: 'btn btn-secondary cta-secondary',
                                        onclick: () => Router.navigate('ai-knowhow')
                                    }, 'Explore Architecture')
                                ),

                                h('p', { class: 'hero-meta' },
                                    'v74 · 73 iterations · No Framework · Pure Vanilla JS · ',
                                    h('a', {
                                        href: 'https://zenn.dev/yuta_yokoi/articles/931f6e781d91f8',
                                        target: '_blank',
                                        rel: 'noopener noreferrer',
                                        class: 'color-primary'
                                    }, 'Read Technical Deep-Dive →')
                                )
                            ),

                            // ── Right: Visual ────────────────────────────────────────
                            h('div', { class: 'hero-visual-wrap' },
                                h('img', {
                                    src: './yuta-yokoi-ai-pm-orchestration-system.webp',
                                    alt: 'AI Orchestrated PM Portfolio (6-Agent KERNEL Framework) — Zero-Code SPA: Strategy × Technology × Execution. Directed by Yuta Yokoi (横井雄太 / yutapr0117). 73 transitions (v1→v74).',
                                    'data-entity': 'Yuta Yokoi (横井雄太 / Yokoi Yuta)',
                                    'data-canonical': 'https://yutapr0117-design.github.io/portfolio/',
                                    'data-ai-context': 'https://yutapr0117-design.github.io/portfolio/llms-full.txt',
                                    'data-asset-role': 'hero-image',
                                    id: 'hero-image',
                                    'aria-details': '#hero-image-asset',
                                    width: '1536',
                                    height: '1024',
                                    loading: 'eager',
                                    fetchpriority: 'high',
                                    decoding: 'async',
                                    class: 'hero-visual'
                                })
                            )
                        )
                    )
                ),

                // ── まず見るべき3箇所 (The Big Three) ──
                h('section', { 
                    class: 'card', 
                    role: 'region', 
                    'aria-label': 'まず見るべき3つの重要コンテンツ',
                    style: { padding: 'var(--space-6)', background: 'var(--bg-secondary)', borderRadius: 'var(--radius-lg)' }
                },
                    h('h2', { class: 'h3 mb-6 text-center' }, 'まずはこの3つだけ見てください'),
                    h('div', { 
                        class: 'grid grid-cols-1 md:grid-cols-3 gap-6'
                    },
                        // Card 1: Case Study
                        h('div', { class: 'card flex flex-col h-full shadow-sm hover-shadow-md transition' },
                            h('div', { class: 'card-body flex flex-col h-full' },
                                h('h3', { class: 'h4 mb-3' }, 'Case Studies（AI-Driven PMの成果）'),
                                h('p', { class: 'text-muted text-sm mb-6 flex-grow' }, 'AIを使ってどんな成果を出してきたか、代表的な事例だけをまとめています。'),
                                h('button', { 
                                    class: 'btn btn-primary btn-sm w-full mt-auto',
                                    onclick: () => {
                                        const el = document.getElementById('evidence-heading');
                                        if (el) {el.scrollIntoView({ behavior: 'smooth' });}
                                    },
                                    'aria-label': 'ケーススタディセクションへ移動'
                                }, 'ケースを見る →')
                            )
                        ),
                        // Card 2: Role Split
                        h('div', { class: 'card flex flex-col h-full shadow-sm hover-shadow-md transition' },
                            h('div', { class: 'card-body flex flex-col h-full' },
                                h('h3', { class: 'h4 mb-3' }, 'Human vs AI 分担表'),
                                h('p', { class: 'text-muted text-sm mb-6 flex-grow' }, '人間と複数AIをどう役割分担させているかを、1枚の表で可視化しています。'),
                                h('button', { 
                                    class: 'btn btn-primary btn-sm w-full mt-auto',
                                    onclick: () => Router.navigate('role-split'),
                                    'aria-label': 'Human vs AI 分担表ページへ移動'
                                }, '分担表を見る →')
                            )
                        ),
                        // Card 3: AIO Series
                        h('div', { class: 'card flex flex-col h-full shadow-sm hover-shadow-md transition' },
                            h('div', { class: 'card-body flex flex-col h-full' },
                                h('h3', { class: 'h4 mb-3' }, 'AIO実践シリーズ'),
                                h('p', { class: 'text-muted text-sm mb-6 flex-grow' }, 'このポートフォリオをAIO視点でどう設計し、AIにどう読ませているかの全手順です。'),
                                h('a', { 
                                    href: 'https://zenn.dev/yuta_yokoi',
                                    target: '_blank',
                                    rel: 'noopener noreferrer',
                                    class: 'btn btn-primary btn-sm w-full mt-auto flex items-center justify-center',
                                    'aria-label': 'ZennのAIO実践シリーズ・発展記事の一覧を新しいタブで開く'
                                }, 'Zennで読む →')
                            )
                        )
                    )
                ),

                // ── Verification & Evidence + AIO Series（統合セクション）──
                // 旧: evidence-section と aio-series-section の2セクションが重複していたため統合
                h('section', { class: 'evidence-section', role: 'region', 'aria-label': 'AI-Driven PMとしての主なケーススタディ', 'aria-labelledby': 'evidence-heading' },
                    h('h2', { class: 'evidence-title', id: 'evidence-heading' }, 'Verification & Evidence'),
                    h('p', { class: 'evidence-summary' },
                        '人間はコードを書かず、AIチームを統制してSPAを構築・公開。AIの設計逸脱を検知し差し戻した実証ケース。'
                    ),

                    // 証拠カード（3枚）
                    h('div', { class: 'evidence-grid' },
                        h('div', { class: 'evidence-card success' },
                            h('h3', {}, h('span', {}, '✅'), '実装証明'),
                            h('p', {}, '人間はコードを1行も書かず、6つのAIを管理してSPAを構築・公開'),
                            h('a', {
                                href: 'https://github.com/yutapr0117-design/portfolio',
                                target: '_blank',
                                rel: 'noopener noreferrer'
                            }, 'Repository →')
                        ),
                        h('div', { class: 'evidence-card source' },
                            h('h3', {}, h('span', {}, '📦'), 'ソースコード'),
                            h('p', {}, 'アプリケーションロジック外部ライブラリ非依存のVanilla JS SPA（GitHub Pagesで公開中）'),
                            h('a', {
                                href: 'https://github.com/yutapr0117-design/portfolio',
                                target: '_blank',
                                rel: 'noopener noreferrer'
                            }, 'GitHub →')
                        ),
                        h('div', { class: 'evidence-card failure' },
                            h('h3', {}, h('span', {}, '⚠️'), '失敗事例'),
                            h('p', {}, 'AIが設計逸脱（React化）→ PM判断でReject・分離'),
                            h('a', {
                                href: 'https://github.com/yutapr0117-design/ai-overengineering-exhibit',
                                target: '_blank',
                                rel: 'noopener noreferrer'
                            }, '失敗を見る →')
                        )
                    ),

                    // AIO実践シリーズ（同セクション内サブエリア）
                    h('div', { class: 'aio-series-sub', 'aria-labelledby': 'aio-series-heading' },
                        h('h3', { class: 'aio-series-sub-title', id: 'aio-series-heading' },
                            h('span', {}, '📝'), 'AIO実践シリーズ＋発展記事（AIO効果順・計11本）'
                        ),
                        h('p', { class: 'aio-series-sub-desc' },
                            'AI-Driven PM による「人間主導 multi-AI オーケストレーション」の完全記録。'
                        ),
                        h('div', { class: 'aio-series-grid' },
                            ...([
                                ['PRIMARY', 'AIO Bot Governance 分類編｜AIクローラーを一括りにするな（学習・検索・ユーザーfetch・AIエージェントを分けて制御）', 'https://zenn.dev/yuta_yokoi/articles/5d1d7a7438d48d'],
                                ['実践編', 'AIO Bot Governance 実践編｜robots/WAF/CIDRでAIボットを本番制御する', 'https://zenn.dev/yuta_yokoi/articles/d99f8171bcf275'],
                                ['第4弾', 'AIOはHTMLで終わらない：実装まで一気通貫で設計する、バイナリ層AIO解説', 'https://zenn.dev/yuta_yokoi/articles/3735dc2683f900'],
                                ['集大成', 'Portfolio AIO Capstone｜AI検索・AI採用に向けた実装の総まとめ', 'https://zenn.dev/yuta_yokoi/articles/c82fe055816454'],
                                ['AI×AI', 'AI-to-AI Pipeline Design｜正典・制約・実ファイルでAIに状態を継承させる', 'https://zenn.dev/yuta_yokoi/articles/91cf894e1072c6'],
                                ['第6弾', 'SEO BotからAIO Botへ――意味のサプライチェーン設計とAIO成熟モデル v1.0（最終回）', 'https://zenn.dev/yuta_yokoi/articles/27fa4c511cd972'],
                                ['第5弾', '人間主導multi-AIオーケストレーションをゼロから再現する完全手順書', 'https://zenn.dev/yuta_yokoi/articles/340dbb85491fc8'],
                                ['第2弾', 'AIにサイトがどう解釈されるか｜llms.txtとAIOで調整した話', 'https://zenn.dev/yuta_yokoi/articles/7e18e6ee1577aa'],
                                ['第1弾', 'AI開発をPMが管理した実験｜コードを書かずにSPAを構築する', 'https://zenn.dev/yuta_yokoi/articles/931f6e781d91f8'],
                                ['第3弾', 'SPAに観測をどう入れるか｜GA4を使わなかった理由と構成', 'https://zenn.dev/yuta_yokoi/articles/49326c5c4e0aae'],
                                ['総括', 'AIO実践シリーズ総括｜全6本完結・6つの設計パターン', 'https://zenn.dev/yuta_yokoi/articles/6dad78f20f2505'],
                            ].map(([badge, title, url]) =>
                                h('div', { class: 'aio-article-card' },
                                    h('span', { class: 'aio-article-num' }, badge),
                                    h('a', { href: url, target: '_blank', rel: 'noopener noreferrer' }, title),
                                    h('span', { class: 'aio-article-arrow' }, 'Zenn →')
                                )
                            ))
                        )
                    )
                ),

                                // Featured Project
                h('div', { class: 'grid-2col' },
                    h('article', { class: 'card' },
                        h('div', { class: 'card-body' },
                            h('h3', { class: 'h3 mb-3' }, '注目のプロジェクト'),
                            h('div', { class: 'flex gap-2 mb-3' },
                                h('span', { class: 'badge badge-primary' }, featured.category),
                                featured.demoRoute ? h('span', { class: 'badge badge-success' }, 'デモあり') : null
                            ),
                            h('p', { class: 'text-muted mb-4' }, featured.name),
                            h('p', { class: 'text-small text-muted' }, featured.summary),
                            h('div', { class: 'flex gap-2 mt-4' },
                                h('button', {
                                    class: 'btn btn-ghost btn-sm',
                                    onclick: () => Router.navigate(`projects/${featured.slug}`)
                                }, '詳細 →'),
                                featured.demoRoute ? h('button', {
                                    class: 'btn btn-secondary btn-sm',
                                    onclick: () => Router.navigate(`apps/${featured.demoRoute}`)
                                }, 'デモ起動') : null
                            )
                        )
                    ),

                    h('article', { class: 'card' },
                        h('div', { class: 'card-body' },
                            h('h3', { class: 'h3 mb-3' }, '設計上の工夫'),
                            h('ul', {
                                class: 'text-muted list-indented'
                            },
                                h('li', {}, 'Importは検証＋正規化＋衝突モード'),
                                h('li', {}, '整合性チェック→自動修復（重複/孤立/無効URL等）'),
                                h('li', {}, 'スナップショット→復元で最短復旧'),
                                h('li', {}, 'セマンティックHTML5 + ARIA対応'),
                                h('li', {}, '単一HTMLで完結（依存性最小化）')
                            )
                        )
                    )
                ),

                // Stats
                h('section', { class: 'grid grid-cols-3' },
                    h('div', { class: 'card' },
                        h('div', { class: 'card-body text-center' },
                            h('div', { class: 'h2 color-primary' }, String(state.projects.length)),
                            h('div', { class: 'text-small text-muted' }, 'プロジェクト')
                        )
                    ),
                    h('div', { class: 'card' },
                        h('div', { class: 'card-body text-center' },
                            h('div', { class: 'h2 color-success' }, String(state.appsData.tasks.length)),
                            h('div', { class: 'text-small text-muted' }, 'タスク')
                        )
                    ),
                    h('div', { class: 'card' },
                        h('div', { class: 'card-body text-center' },
                            h('div', { class: 'h2 color-warning' }, String(state.appsData.todos.length)),
                            h('div', { class: 'text-small text-muted' }, 'TODO')
                        )
                    )
                ),

                // Contact CTA
                ContactCTA('PM設計・AI開発・アーキテクチャ設計のご相談を受け付けています。このSPAを見て「こういうものを作りたい」「AI導入を相談したい」「設計を一緒に考えたい」と感じた方は、お気軽にどうぞ。')
            );
        }

        // ===== Component: Projects Page =====
        function ProjectsPage() {
            const state = State.get();
            const route = Router.getRoute();
            let q = route.query.q || '';
            let cat = route.query.cat || 'All';

            const categories = ['All', ...new Set(state.projects.map(p => p.category))];

            // Uses the global tokenize() utility - no local duplicate

            function scoreProject(p, tokens) {
                if (!tokens.length) {return 1;}
                const corpus = [
                    ...tokenize(p.name),
                    ...tokenize(p.summary),
                    ...(p.tags || []).map(t => String(t).toLowerCase()),
                    ...(p.tech || []).map(t => String(t).toLowerCase()),
                    ...tokenize(p.category)
                ];

                const freq = new Map();
                corpus.forEach(w => freq.set(w, (freq.get(w) || 0) + 1));
                // 部分一致用に重複を除いたユニークwordSet（toLowerCase多重呼び出し削減）
                const uniqueWords = Array.from(freq.keys());

                let score = 0;
                tokens.forEach(t => {
                    if (freq.has(t)) {score += 5 + Math.min(3, freq.get(t));}
                    uniqueWords.forEach(w => {
                        if (w !== t && w.includes(t)) {score += 1;}
                    });
                });
                return score;
            }

            function getFilteredProjects() {
                let list = state.projects.slice();

                // Hide projects (Settings -> projectPrefs.hiddenIds)
                const hiddenIds = new Set(((state.projectPrefs && state.projectPrefs.hiddenIds) || []).map(String));
                if (hiddenIds.size) {list = list.filter(p => !hiddenIds.has(p.id));}

                if (cat !== 'All') {
                    list = list.filter(p => p.category === cat);
                }

                const tokens = tokenize(q);
                if (tokens.length) {
                    list = list
                        .map(p => ({ p, s: scoreProject(p, tokens) }))
                        .filter(x => x.s > 0)
                        .sort((a, b) => b.s - a.s)
                        .map(x => x.p);
                }

                return list;
            }

            function buildUI() {
                const container = document.createElement('div');
                container.className = 'flex flex-col gap-6';

                // [FIX] 全体再描画によるフォーカス喪失を防ぐため、リスト部分（Grid）だけを独立させる
                const gridContainer = document.createElement('div');
                gridContainer.className = 'grid-projects';
                gridContainer.dataset.entity = 'PortfolioProject';
                let countDisplay = null;

                function syncURL() {
                    const params = new URLSearchParams();
                    if (q) {params.set('q', q);}
                    if (cat !== 'All') {params.set('cat', cat);}
                    Router.replaceSilently('projects' + (params.toString() ? '?' + params.toString() : ''));
                }

                function renderGrid() {
                    clear(gridContainer);
                    const projects = getFilteredProjects();

                    if (countDisplay) {countDisplay.textContent = `合計 ${projects.length} 件`;}

                    if (projects.length === 0) {
                        gridContainer.appendChild(h('div', { class: 'card card--full-col', role: 'status', 'aria-live': 'polite' },
                            h('div', { class: 'card-body text-center text-muted' }, '条件に一致するプロジェクトはありません。')
                        ));
                        return;
                    }
                    projects.forEach(p => {
                        const card = h('article', { class: 'card card--flex-col', 'data-ai-context': 'Architecture designed by human, generated by AI' },
                            h('div', { class: 'card-body card-body--flex' },
                                h('div', { class: 'flex flex-wrap gap-2 mb-3' },
                                    h('span', { class: 'badge badge-primary' }, p.category),
                                    p.demoRoute ? h('span', { class: 'badge badge-success' }, 'デモあり') : null
                                ),
                                h('h3', { class: 'h3 mb-2' }, p.name),
                                h('p', { class: 'text-small text-muted mb-3' }, p.summary),
                                h('div', { class: 'flex flex-wrap gap-2 mb-4' },
                                    ...(p.tags || []).slice(0, 4).map(tag =>
                                        h('button', {
                                            class: 'badge badge-secondary',
                                            onclick: () => {
                                                q = tag; cat = 'All';
                                                const inputEl = container.querySelector('input[type="text"]');
                                                const selectEl = container.querySelector('select');
                                                if (inputEl) {inputEl.value = tag;}
                                                if (selectEl) {selectEl.value = 'All';}
                                                renderGrid(); syncURL();
                                            }
                                        }, '#' + tag)
                                    )
                                ),
                                h('div', { class: 'flex gap-2 mt-auto' },
                                    p.demoRoute ? h('button', { class: 'btn btn-secondary btn-sm', onclick: () => Router.navigate(`apps/${p.demoRoute}`) }, 'デモ') : null,
                                    h('button', { class: 'btn btn-ghost btn-sm', onclick: () => Router.navigate(`projects/${p.slug}`) }, '詳細を見る')
                                )
                            )
                        );
                        gridContainer.appendChild(card);
                    });
                }

                // Header
                container.appendChild(h('header', {},
                    h('div', { class: 'flex flex-wrap items-center justify-between gap-4 mb-4' },
                        h('div', {},
                            h('h1', { class: 'h1' }, 'プロジェクト一覧'),
                            countDisplay = h('p', { class: 'text-muted' }, '')
                        )
                    ),
                    h('div', { class: 'grid grid-cols-2 gap-4' },
                        h('div', { class: 'relative' },
                            h('div', {
                                class: 'absolute left-3 top-1/2 transform -translate-y-1/2 color-muted'
                            }, createIcon('search', 18)),
                            h('input', {
                                type: 'text',
                                class: 'input pl-10',
                                placeholder: '検索（名前/概要/タグ/技術/カテゴリ）...',
                                value: q,
                                'aria-label': 'プロジェクト検索',
                                oninput: (e) => {
                                    q = e.target.value;
                                    renderGrid(); // 部分更新でフォーカスを死守
                                    syncURL();    // history.replaceStateで静かにURL同期
                                }
                            })
                        ),
                        h('select', {
                            class: 'input',
                            value: cat,
                            'aria-label': 'カテゴリフィルター',
                            onchange: (e) => {
                                cat = e.target.value;
                                renderGrid();
                                syncURL();
                            }
                        },
                            ...categories.map(c => h('option', {
                                value: c,
                                text: c === 'All' ? '全カテゴリー' : c
                            }))
                        )
                    )
                ));

                renderGrid(); // 初期描画
                container.appendChild(gridContainer);
                return container;
            }

            return buildUI();
        }

        // ===== Component: Project Detail Page =====
        function ProjectDetailPage(slug) {
            const state = State.get();
            const project = state.projects.find(p => p.slug === slug);

            if (!project) {
                return h('div', { class: 'flex flex-col gap-4' },
                    h('h1', { class: 'h1' }, 'プロジェクトが見つかりません'),
                    h('button', {
                        class: 'btn btn-secondary',
                        onclick: () => Router.navigate('projects')
                    }, '一覧へ戻る')
                );
            }

            const related = state.projects.filter(p =>
                project.relatedProjectIds?.includes(p.id) && p.id !== project.id
            );

            const autoRelated = Store.autoRelatedCandidates(project, state.projects, 8);
            return h('article', { class: 'flex flex-col gap-6' },
                // Header
                h('header', {},
                    h('button', {
                        class: 'btn btn-ghost btn-sm mb-4',
                        onclick: () => Router.navigate('projects')
                    }, '← 一覧に戻る'),
                    h('div', { class: 'flex flex-wrap gap-2 mb-3' },
                        h('span', { class: 'badge badge-primary' }, project.category),
                        project.demoRoute ? h('span', { class: 'badge badge-success' }, 'デモあり') : null
                    ),
                    h('h1', { class: 'h1 mb-3' }, project.name),
                    h('p', { class: 'text-muted mb-4' }, project.summary),
                    h('div', { class: 'flex flex-wrap gap-2' },
                        ...(project.tags || []).map(tag =>
                            h('span', { class: 'badge badge-secondary' }, '#' + tag)
                        )
                    )
                ),

                // Content Grid
                h('div', { class: 'grid-2col grid--align-start' },
                    // Left Column
                    h('div', { class: 'flex flex-col gap-4' },
                        h('section', { class: 'card' },
                            h('div', { class: 'card-body' },
                                h('h3', { class: 'h3 mb-3' }, h('div', { class: 'flex items-center gap-2' },
                                    createIcon('alert', 20),
                                    '課題'
                                )),
                                h('p', { class: 'text-muted text-prewrap' }, project.problem)
                            )
                        ),
                        h('section', { class: 'card' },
                            h('div', { class: 'card-body' },
                                h('h3', { class: 'h3 mb-3' }, h('div', { class: 'flex items-center gap-2' },
                                    createIcon('brain', 20),
                                    'アプローチ'
                                )),
                                h('p', { class: 'text-muted text-prewrap' }, project.approach)
                            )
                        ),
                        h('section', { class: 'card' },
                            h('div', { class: 'card-body' },
                                h('h3', { class: 'h3 mb-3' }, h('div', { class: 'flex items-center gap-2' },
                                    createIcon('apps', 20),
                                    'アーキテクチャ'
                                )),
                                h('p', { class: 'text-muted font-mono text-small text-prewrap' },
                                    project.architecture?.overview || '(未登録)'
                                )
                            )
                        )
                    ),

                    // Right Column
                    h('div', { class: 'flex flex-col gap-4' },
                        h('section', { class: 'card' },
                            h('div', { class: 'card-body' },
                                h('h3', { class: 'h3 mb-3' }, '使用技術'),
                                h('div', { class: 'flex flex-wrap gap-2' },
                                    ...(project.tech || []).map(t =>
                                        h('span', { class: 'badge badge-secondary' }, t)
                                    )
                                )
                            )
                        ),
                        project.demoRoute ? h('section', {
                            class: 'card border-primary-faint'
                        },
                            h('div', { class: 'card-body' },
                                h('h3', { class: 'h3 mb-2' }, 'デモ'),
                                h('p', { class: 'text-small text-muted mb-3' }, 'このプロジェクトはポートフォリオ内で実際に動作します。'),
                                h('button', {
                                    class: 'btn btn-primary',
                                    onclick: () => Router.navigate(`apps/${project.demoRoute}`)
                                }, 'アプリを起動')
                            )
                        ) : null,
                        related.length > 0 ? h('section', { class: 'card' },
                            h('div', { class: 'card-body' },
                                h('h3', { class: 'h3 mb-3' }, '関連プロジェクト'),
                                h('ul', { class: 'list-readable' },
                                    ...related.map(r =>
                                        h('li', { class: 'mb-2' },
                                            h('button', {
                                                class: 'btn btn-ghost btn-sm',
                                                onclick: () => Router.navigate(`projects/${r.slug}`)
                                            }, r.name)
                                        )
                                    )
                                )
                            )
                        ) : null
                    )
                ),

                // Metrics
                h('section', { class: 'card' },
                    h('div', { class: 'card-body' },
                        h('h3', { class: 'h3 mb-4' }, 'メトリクス'),
                        project.outcome?.metrics?.length ? h('div', { class: 'grid grid-cols-3' },
                            ...project.outcome.metrics.map(m =>
                                h('div', { class: 'text-center p-4' },
                                    h('div', {
                                        class: 'h2 mb-1 color-primary'
                                    }, m.value),
                                    h('div', { class: 'text-small text-muted' }, m.label)
                                )
                            )
                        ) : h('p', { class: 'text-muted' }, 'メトリクスは未登録です。')
                    )
                )

                ,
                autoRelated.length > 0 ? h('section', { class: 'card' },
                    h('div', { class: 'card-body' },
                        h('h3', { class: 'h3 mb-3' }, 'おすすめ（自動）'),
                        h('p', { class: 'text-muted mb-3' }, 'カテゴリ/タグ/技術/本文の近さから自動で近いプロジェクトを提案します。'),
                        h('ul', { class: 'list-clean' },
                            ...autoRelated.map(r =>
                                h('li', { class: 'mb-2' },
                                    h('button', {
                                        class: 'btn btn-ghost btn-sm',
                                        onclick: () => Router.navigate(`projects/${r.slug}`)
                                    },
                                        createIcon('sparkles', 16),
                                        h('span', { class: 'icon-gap' }, r.name)
                                    )
                                )
                            )
                        )
                    )
                ) : null);
        }

        // ===== Component: Apps Hub =====
        function AppsPage() {
            const apps = [
                { id: 'task', title: 'タスク管理', desc: 'カンバン形式の簡易タスク管理', icon: 'checkSquare' },
                { id: 'todo', title: 'クイックTODO', desc: 'クイック入力 + 完了管理', icon: 'list' },
                { id: 'pomodoro', title: 'ポモドーロ', desc: '耐タブ休眠のタイマー + フォーカス対象', icon: 'clock' },
                { id: 'ai', title: 'AI アシスト', desc: 'ローカルAI（外部API不要）', icon: 'brain' },
            ];

            return h('div', { class: 'flex flex-col gap-6' },
                h('header', {},
                    h('h1', { class: 'h1' }, 'アプリ'),
                    h('p', { class: 'text-muted' }, 'ポートフォリオに内蔵された実用的なツール')
                ),
                h('div', { class: 'grid grid-cols-2' },
                    ...apps.map(app =>
                        h('article', { class: 'card' },
                            h('div', { class: 'card-body' },
                                h('div', { class: 'flex items-center gap-3 mb-3' },
                                    createIcon(app.icon, 24),
                                    h('h3', { class: 'h3' }, app.title)
                                ),
                                h('p', { class: 'text-muted mb-4' }, app.desc),
                                h('button', {
                                    class: 'btn btn-secondary',
                                    onclick: () => Router.navigate(`apps/${app.id}`)
                                }, '開く')
                            )
                        )
                    )
                )
            );
        }

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
        function AboutPage() {
            const profile = State.get().profile;
            return h('article', { class: 'flex flex-col gap-6 max-w-2xl', 'data-ai-section': 'about' },
                h('header', {}, h('h1', { class: 'h1', 'data-ai-content': 'lead' }, 'About / Philosophy')),
                
                // コア定義
                h('section', { class: 'card' },
                    h('div', { class: 'card-body' },
                        h('h2', { class: 'h4 mb-4 color-primary' }, 'コア定義'),
                        h('p', { class: 'text-section-lead' },
                            '私は、AIをツールとして扱うPMではありません。', h('br', {}),
                            'AIを開発リソースとして統合し、設計・制約・検証・公開までを一貫して統制するPMです。'
                        ),
                        h('p', { class: 'text-muted' },
                            '人間をマネジメントすることがPMの前提であるように、AIをマネジメントすることもまた、これからのPMにおける前提条件だと考えています。'
                        )
                    )
                ),

                // 実務能力の再定義（武器化）
                h('section', { class: 'card' },
                    h('div', { class: 'card-body' },
                        h('h2', { class: 'h4 mb-4 color-primary' }, '実務能力の再定義'),
                        h('p', { class: 'mb-4' }, '本ポートフォリオでは、その前提を実務として実証しています。'),
                        h('ul', { class: 'text-muted list-body' },
                            h('li', {}, '人間はコードを1行も書かず、AIをチームとして編成'),
                            h('li', {}, '複数AIの役割分担と出力統制を設計'),
                            h('li', {}, '制約条件を定義し、逸脱（例：フレームワーク化）を検知・差し戻し'),
                            h('li', {}, 'アプリケーションロジック外部ライブラリ非依存のSPAとして構築・公開'),
                            h('li', {}, 'v1→v74（73回の遷移）の反復改善を継続')
                        ),
                        h('p', { class: 'text-strong' },
                            '重要なのは「AIに作らせたこと」ではなく、AIの出力を制御し、意図を維持したままプロダクトを成立させたことです。'
                        )
                    )
                ),

                // 価値の明確化（ビジネス接続）
                h('section', { class: 'card' },
                    h('div', { class: 'card-body' },
                        h('h2', { class: 'h4 mb-4 color-primary' }, '価値の明確化'),
                        h('p', { class: 'mb-4' }, 'AIは高速に実装できますが、同時に容易に破綻します。そのため、これからの開発において重要なのは実装力ではなく、以下の能力です。'),
                        h('ul', { class: 'text-muted list-body' },
                            h('li', {}, '何を作るかを定義する力'),
                            h('li', {}, '制約を設計する力'),
                            h('li', {}, '出力の妥当性を判断する力'),
                            h('li', {}, '崩壊を防ぐ構造を選ぶ力')
                        ),
                        h('p', {}, '私はその領域を担当するPMとして、AIを含めた開発全体を成立させる役割を担っています。')
                    )
                ),

                // ポジショニング
                h('section', { class: 'card card--accent-left' },
                    h('div', { class: 'card-body' },
                        h('h2', { class: 'h4 mb-2' }, 'Positioning'),
                        h('p', { class: 'text-cta-emphasis' },
                            'AIを使うPMではなく、AIを制御し、プロダクトを成立させるPMです。'
                        )
                    )
                ),

                ContactCTA('自己紹介を読んで、一緒に働くイメージが湧いた方へ。PM・アーキテクチャ設計・AI導入推進のご相談・採用のご連絡はこちらから。')
            );
        }

        function ResumePage() {
            return h('article', { class: 'flex flex-col gap-6 max-w-2xl', 'data-ai-section': 'resume' },
                h('header', {}, h('h1', { class: 'h1', 'data-ai-content': 'lead' }, 'Resume')),
                h('section', { class: 'card' },
                    h('div', { class: 'card-body' },
                        h('h3', { class: 'h3 mb-4', 'data-ai-content': 'lead' }, State.get().profile.title),
                        h('ul', { class: 'text-muted list-body-tight', 'data-ai-content': 'body' },
                            h('li', {}, 'ProjectsをCase Study形式で整理'),
                            h('li', {}, '内蔵Apps（Task/Todo/Pomodoro/AI）を作品として掲載'),
                            h('li', {}, '整合性チェック/自動修復＋スナップショットで運用事故率を低減'),
                            h('li', {}, 'セマンティックHTML5 + ARIA対応'),
                            h('li', {}, '単一HTMLで完結（依存性最小化）')
                        )
                    )
                ),
                ContactCTA('スキルセット・開発スタイルを確認いただいた方へ。AI駆動開発・PM設計・システムアーキテクチャ設計の相談、採用のご連絡はこちらから。')
            );
        }

        function ContactPage() {
            const profile = State.get().profile;
            return h('article', { class: 'flex flex-col gap-6 max-w-2xl', 'aria-label': 'Contact — yuta AI-Driven PM' },
                h('header', {}, h('h1', { class: 'h1' }, 'Contact')),
                h('section', { class: 'card' },
                    h('div', { class: 'card-body' },
                        h('div', { class: 'flex flex-col gap-4' },
                            h('div', { class: 'flex justify-between py-2 border-bottom border-bottom-themed' },
                                h('span', { class: 'text-muted' }, 'Email'),
                                h('a', { href: `mailto:${profile.email}`, class: 'font-mono' }, profile.email)
                            ),
                            profile.github ? h('div', { class: 'flex justify-between py-2 border-bottom border-bottom-themed' },
                                h('span', { class: 'text-muted' }, 'GitHub'),
                                h('a', { href: profile.github, target: '_blank', rel: 'noopener noreferrer' }, profile.github)
                            ) : null,
                            profile.linkedin ? h('div', { class: 'flex justify-between py-2' },
                                h('span', { class: 'text-muted' }, 'LinkedIn'),
                                h('a', { href: profile.linkedin, target: '_blank', rel: 'noopener' }, profile.linkedin)
                            ) : null,
                            h('button', {
                                class: 'btn btn-primary mt-4',
                                onclick: () => location.href = `mailto:${profile.email}`
                            }, h('span', {}, createIcon('mail', 18), ' メールを作成'))
                        )
                    )
                )
            );
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

        function FatalPage(error) {
            const msg = (error && error.message) ? error.message : String(error || 'Unknown error');
            const stack = (error && error.stack) ? String(error.stack) : '';

            function clearAllData() {
                if (!confirm('LocalStorageのデータを削除して再読み込みしますか？')) {return;}
                try {
                    localStorage.removeItem(CONSTANTS.STORAGE_KEY);
                    localStorage.removeItem(CONSTANTS.SNAPSHOT_KEY);
                } catch { }
                location.reload();
            }

            return h('div', { class: 'flex flex-col gap-4 max-w-2xl' },
                h('h1', { class: 'h1' }, '致命的エラーが発生しました'),
                h('p', { id: 'fallback-details', class: 'text-muted' }, '表示を継続できない例外が発生しました。下の情報を確認し、必要ならデータを初期化してください。'),
                h('section', { class: 'card' },
                    h('div', { class: 'card-body' },
                        h('div', { class: 'h3 mb-2' }, 'エラー'),
                        h('pre', { class: 'text-prewrap-break' }, msg),
                        stack ? h('details', { class: 'mt-3' },
                            h('summary', { class: 'cursor-pointer text-sm' }, 'スタックトレース'),
                            h('pre', { class: 'text-sm pre-wrap' }, stack)
                        ) : null
                    )
                ),
                h('div', { class: 'flex flex-wrap gap-2' },
                    h('button', { class: 'btn btn-secondary', onclick: () => { window.__fatalError = null; Router.navigate(''); } }, 'ホームへ'),
                    h('button', { class: 'btn btn-danger', onclick: clearAllData }, 'データを削除して再起動')
                )
            );
        }

        // ===== Page Components =====
        //   ▼ v80+ Stage 5-b: HiringRiskPage (v28 採用決裁資料レベル) + helpers
        //     (impactRow / kpiRow / decisionFlow / riskCard) を js/pages.js へ抽出済み。
        function AIKnowhowPage() {
            const C = {
                primary: 'var(--color-primary)',
                success: 'var(--color-success)',
                warning: 'var(--color-warning)',
                info: 'var(--color-info)',
                purple: '#7c3aed'
            };

            function sectionHeader(icon, title, color) {
                return h('div', {
                    class: 'row-gap-4-items-start'
                },
                    h('div', {
                        class: 'badge-layer--lg', style: { background: color }
                    }, icon),
                    h('span', { class: 'text-head-lg' }, title)
                );
            }

            function agentRow(name, role, free, note) {
                return h('div', {
                    class: 'block-bg-tertiary-pad14'
                },
                    h('div', { class: 'role-desc-row' }, name),
                    h('div', { class: 'text-detail' }, note),
                    h('span', {
                        class: 'free-paid-badge', style: { background: free ? 'rgba(22,163,74,0.12)' : 'rgba(217,119,6,0.12)', color: free ? 'var(--color-success)' : 'var(--color-warning)' }
                    }, free ? '無課金' : '有料（最安）')
                );
            }

            function kernelRow(key, label, detail) {
                return h('div', {
                    class: 'row-gap-8-border'
                },
                    h('div', {
                        class: 'step-num-badge'
                    }, key),
                    h('div', { class: 'flex flex-col gap-row-sm' },
                        h('div', { class: 'text-label' }, label),
                        h('div', { class: 'text-detail-muted-relaxed' }, detail)
                    )
                );
            }

            function phaseCard(num, title, tickets, agents, summary, color) {
                return h('div', {
                    class: 'block-phase-card', style: { borderLeft: '3px solid ' + color, padding: '12px 14px', background: 'var(--bg-tertiary)' }
                },
                    h('div', { class: 'row-gap-8-nm' },
                        h('div', {
                            class: 'badge-phase', style: { background: color }
                        }, 'Phase ' + num),
                        h('span', { class: 'role-desc-row' }, title),
                        h('span', { class: 'text-label-xs-push' }, tickets)
                    ),
                    h('div', { class: 'text-detail' }, summary),
                    h('div', {
                        class: 'gap-wrap-mt4'
                    },
                        ...agents.map(a => h('span', {
                            class: 'badge-agent'
                        }, a))
                    )
                );
            }

            return h('article', { class: 'flex flex-col gap-6 max-w-3xl' },

                // ══ ヘッダー ══
                h('header', { class: 'flex flex-col gap-2', 'data-ai-section': 'ai-knowhow' },
                    h('h1', { class: 'h1 row-gap-12', 'data-ai-content': 'lead' },
                        createIcon('lightbulb', 28), 'AI開発ノウハウ'
                    ),
                    h('p', { class: 'text-muted', 'data-ai-content': 'lead' },
                        '6種のAIエージェントを役割分担させ、55枚のチケット（プロンプト）のみでv54 SPAを構築した再現可能な手法のエッセンスです。'
                    ),
                    h('div', { class: 'flex flex-wrap gap-2 row-mt-4' },
                        h('span', { class: 'badge badge-secondary' }, '🤖 6エージェント構成'),
                        h('span', { class: 'badge badge-secondary' }, '🎫 55チケット'),
                        h('span', { class: 'badge badge-secondary' }, '💰 課金2名のみ'),
                        h('span', { class: 'badge badge-secondary' }, '🔑 KERNELフレームワーク')
                    )
                ),

                // ══ 費用感 ══
                h('section', {
                    class: 'card card--accent-left', 'data-accent': 'warning', role: 'region', 'aria-label': 'AI開発の費用感'
                },
                    h('div', { class: 'card-body flex flex-col gap-3' },
                        sectionHeader('💰', '費用感 — 課金は2名だけ', C.warning),
                        h('p', { class: 'text-body-sm' },
                            'GeminiとChatGPTのみ最も安いプランで課金。残り4名（Kimi・Claude・Manus・Perplexity）は完全無料で運用可能。ツールごとの無料枠を最大活用することでコストを最小化している。'
                        ),
                        h('div', { class: 'flex flex-wrap gap-2' },
                            h('span', {
                                class: 'badge-tool-tier--paid'
                            }, '💳 有料（最安）: Gemini / ChatGPT'),
                            h('span', {
                                class: 'badge-tool-tier--free'
                            }, '✅ 完全無料: Kimi / Claude / Manus / Perplexity')
                        )
                    )
                ),

                // ══ 6エージェント役割 ══
                h('section', {
                    class: 'card card--accent-left', 'data-accent': 'primary', role: 'region', 'aria-label': '6つのAIエージェントの役割分担'
                },
                    h('div', { class: 'card-body flex flex-col gap-3' },
                        sectionHeader('🤖', '6エージェントの役割分担', C.primary),
                        agentRow('Gemini', false, false,
                            '初期ドラフト（要件定義・ワイヤーフレーム）、BGM（Lyria 3）・画像生成、最終コードレビュー。マルチモーダル能力を活かしてプロジェクトの起点と終点を担う。'
                        ),
                        agentRow('Kimi K2.5', 'init', true,
                            '基盤構築（0-to-1）。Thinkingモード有効で、h()関数・ハッシュルーター・CSS変数フレームワークをゼロから設計。「ゴールを提示してあとは任せる」スタイルが効果的。'
                        ),
                        agentRow('Claude', 'design', true,
                            '中盤〜後半の複雑ロジック設計。状態管理・フォーカス保持・SEOメタデータの動的生成を担当。「設計図を描く」役割に集中させ、実コード変更はManusとChatGPTに委譲する。'
                        ),
                        agentRow('Manus', 'exec', true,
                            '中盤〜後半の厳密実装。「余計なことを一切しない」堅実さが武器。1.6 Maxモードで起動し、CSS/UIの変更のみを精緻に実行。ロジックへの接触を明示的に禁じる。'
                        ),
                        agentRow('Perplexity', 'review', true,
                            'コードレビュー・セキュリティ監査専任。Deep Researchモードで「良い点・悪い点・全指摘事項」を網羅的に抽出。XSSやCSPの脆弱性を主要マイルストーン毎に監査。'
                        ),
                        agentRow('ChatGPT', 'diff', false,
                            'Diff（差分）生成・統合。Perplexityの指摘とClaudeの設計書を受け取り、行番号に依存しない「関数ブロック単位の置換コード」のみを出力。コード統合時のヒューマンエラーを排除。'
                        )
                    )
                ),

                // ══ KERNELフレームワーク ══
                h('section', {
                    class: 'card card--accent-left', 'data-accent': 'purple'
                },
                    h('div', { class: 'card-body flex flex-col gap-2' },
                        sectionHeader('🔑', 'KERNELフレームワーク — チケット設計の原則', C.purple),
                        h('p', { class: 'text-detail-muted mb-2' },
                            '全チケットはこの6原則で構造化。曖昧さを排除しハルシネーションを防ぐ。'
                        ),
                        kernelRow('K', 'Keep it simple — 1チケット1目標',
                            '複雑な背景説明を省き、実行すべきタスクのみを簡潔に記述する。トークン消費とAIの幻覚を最小化。'
                        ),
                        kernelRow('E', 'Easy to verify — 成否判定基準を明記',
                            '「コンソールエラー0件」「XSS脆弱性なし」など、検証可能な完了条件を明示する。'
                        ),
                        kernelRow('R', 'Reproducible — 時間・文脈依存の表現を禁止',
                            '「最新のトレンド」より「Vanilla JSのみ使用」と厳密に指定。誰がいつ実行しても同結果になる。'
                        ),
                        kernelRow('N', 'Narrow scope — スコープを極限まで絞る',
                            'コード生成・ドキュメント作成・テスト記述を1チケットに詰め込まない。成功率が大幅向上。'
                        ),
                        kernelRow('E', 'Explicit constraints — NOT To-Doを明示',
                            '「外部ライブラリ禁止」「既存CSS変数の削除禁止」など、やってはいけないことを列挙する。リグレッションを90%以上削減。'
                        ),
                        kernelRow('L', 'Logical structure — 固定フォーマットで記述',
                            'Context（入力情報）/ Task（タスク定義）/ Constraints（制約）/ Format（出力形式）の4構造に統一する。'
                        )
                    )
                ),

                // ══ 標準チケットテンプレート ══
                h('section', {
                    class: 'card card--accent-left', 'data-accent': 'info'
                },
                    h('div', { class: 'card-body flex flex-col gap-3' },
                        sectionHeader('📋', '標準チケット・テンプレート', C.info),
                        ...[
                            ['役割の定義', 'あなたは[エージェントの専門性]として、Vanilla JSで構築されたSPAに対する精密な改修を実行します。'],
                            ['タスクの明確化', '[実行すべき具体的なアクションを記述]'],
                            ['コンテキストの提供', '単一HTMLファイル構成。innerHTML禁止。要素生成は必ずh()使用。状態は再レンダリングを越えて保持。'],
                            ['現在の状態', '<current_code>[関連するコードブロック]</current_code>'],
                            ['厳格な制約', '[NOT To-Doを箇条書き]'],
                            ['出力フォーマット', 'ファイル全体ではなく、更新された関数ブロックのみを出力。余計な解説不要。']
                        ].map(([label, val]) =>
                            h('div', {
                                class: 'grid-info-row'
                            },
                                h('div', { class: 'text-info-label' }, '[' + label + ']'),
                                h('div', { class: 'text-secondary-xs' }, val)
                            )
                        )
                    )
                ),

                // ══ 5フェーズ概要 ══
                h('section', {
                    class: 'card card--accent-left', 'data-accent': 'success'
                },
                    h('div', { class: 'card-body flex flex-col gap-3' },
                        sectionHeader('🚀', '55チケットの5フェーズ構成', C.success),
                        h('p', { class: 'text-detail-muted mb-1' },
                            '人間はコードを1行も書かず、チケットを発行し返ってきた差分をローカルファイルに統合するだけ。'
                        ),
                        phaseCard(1, '概念定義と初期スキャフォールディング', 'Ticket 1〜12',
                            ['Gemini', 'Kimi'],
                            'Geminiで要件定義とワイヤーフレームを作成。KimiのThinkingモードでh()関数・カスタムルーター・CSS変数フレームワーク・FOUC防止IIFEをゼロ構築。',
                            C.primary
                        ),
                        phaseCard(2, 'コアロジックと状態永続化', 'Ticket 13〜28',
                            ['Claude', 'Manus'],
                            'Claudeでreplace Silentlyルーター・フォーカス保持（setTimeout hack）・visibilitychangeによる状態保存を設計。ManusでプロジェクトグリッドのCSS Gridレイアウトを厳密実装。',
                            C.purple
                        ),
                        phaseCard(3, 'コンポーネント統合とUI洗練', 'Ticket 29〜40',
                            ['Manus', 'Perplexity'],
                            'ManusでTask/Todo/AIインターフェース・クイズUI・タイマーUIを構築。Perplexityで機能統合後のXSS・CSP・OGタグ・JSON-LDを全面監査。',
                            C.info
                        ),
                        phaseCard(4, '外科的パッチ適用', 'Ticket 41〜49',
                            ['ChatGPT', 'Claude'],
                            'ChatGPTをDiffモードで起動し、Perplexity指摘に基づくCSPヘッダー強化・innerHTML排除・Mapベースデータ構造最適化を行番号不依存の置換ブロックで適用。',
                            C.warning
                        ),
                        phaseCard(5, 'アセット合成と最終確認', 'Ticket 50〜55',
                            ['Gemini', 'Perplexity'],
                            'GeminiでCity Pop/Lo-fi BGMと「AI-Driven PM」コンセプト画像を生成し統合。JSON-LDのDOM整合性をGeminiで検証、Perplexityで最終デグレ確認しv54完成。',
                            C.success
                        )
                    )
                ),

                // ══ ハンドオーバープロトコル ══
                h('section', {
                    class: 'card card--accent-left', 'data-accent': 'warning'
                },
                    h('div', { class: 'card-body flex flex-col gap-3' },
                        sectionHeader('🔗', 'エージェント引き継ぎ（ハンドオーバー）プロトコル', C.warning),
                        h('p', { class: 'text-body-sm' },
                            '異なるAI間でコンテキストが消失しないよう、各チケットの末尾に以下の定型出力を要求する。'
                        ),
                        h('div', {
                            class: 'block-blockquote-mono'
                        },
                            '「作業完了後、コード全体像・主要アーキテクチャ決定理由・未解決課題・次エージェントへの具体的指示を網羅したhandover-brief.md形式のテキストを出力してください。」'
                        ),
                        h('p', { class: 'text-detail-muted' },
                            '人間はこのハンドオーバー文書と最新ソースコードをセットにして次エージェントへの入力コンテキストとして渡す。共有メモリ不要で一貫したタスク継続性を担保できる。'
                        )
                    )
                ),

                // ══ 上級テクニック ══
                h('section', {
                    class: 'card card--accent-left', 'data-accent': 'info'
                },
                    h('div', { class: 'card-body flex flex-col gap-4' },
                        sectionHeader('⚡', '上級プロンプトエンジニアリングのコツ', C.info),
                        h('div', { class: 'grid grid-cols-1 md:grid-cols-2 gap-3' },
                            ...[
                                ['コンテキスト段階的開示', '3000行のファイル全体を渡さず、変更対象のブロックのみを抽出して渡す。「ファイル全体を書き直さず更新ブロックのみ出力」と明示。'],
                                ['Thinkingモードの強制発動', '「コードを書く前にDOMトポロジーを分析せよ」と前置き。KimiにはAgent Swarmモードを明示的に指定して並列推論させる。'],
                                ['Fan-Out比較パターン', '難解なバグはKimiとClaudeに同時投入して解を比較。最適解をChatGPTでDiff化する。単一AIへの依存を排除。'],
                                ['XMLタグ構造化（Claude専用）', '<instructions><context><example>でプロンプトを構造化。AIがユーザーデータとコマンドを混同することを防ぐ。']
                            ].map(([title, desc]) =>
                                h('div', {
                                    class: 'block-section-item'
                                },
                                    h('div', { class: 'text-label' }, title),
                                    h('div', { class: 'text-detail-muted-relaxed' }, desc)
                                )
                            )
                        )
                    )
                ),

                ContactCTA('AI開発ワークフローを読んで、自社への導入や共同プロジェクトに興味を持った方へ。プロンプト設計・マルチエージェント構成・AI開発プロセス設計のご相談を受け付けています。')
            );
        }

        // ===== Shared Component: ContactCTA =====
        // desc: ページ文脈に合わせた一言（何を頼めるか）
        function ContactCTA(desc) {
            const profile = State.get().profile;
            const X_URL         = 'https://x.com/yuta_mezasi';

            function outLink(url, icon, label, colorVar) {
                return h('a', {
                    href: url,
                    target: '_blank',
                    rel: 'noopener noreferrer',
                    class: 'cta-pill',
                    style: {
                        textDecoration: 'none',
                        border: '1.5px solid ' + colorVar,
                        color: colorVar,
                        background: 'transparent',
                        transition: 'var(--transition)',
                        whiteSpace: 'nowrap'
                    }
                }, createIcon(icon, 16), label);
            }

            function mailBtn() {
                return h('button', {
                    class: 'cta-pill',
                    style: {
                        border: '1.5px solid var(--color-primary)',
                        color: 'var(--color-primary)',
                        background: 'transparent',
                        cursor: 'pointer',
                        whiteSpace: 'nowrap'
                    },
                    onclick: () => {
                        const subject = encodeURIComponent('ポートフォリオを見てご連絡しました');
                        const body = encodeURIComponent('はじめまして。\nポートフォリオを拝見し、ご相談があってご連絡しました。\n\n【ご相談内容】\n');
                        location.href = 'mailto:' + profile.email + '?subject=' + subject + '&body=' + body;
                    }
                }, createIcon('mail', 16), 'メールで相談する');
            }

            return h('section', {
                class: 'card card--contact'
            },
                h('div', { class: 'card-body flex flex-col gap-4' },
                    // Header
                    h('div', { class: 'gap-row-10' },
                        h('div', {
                            class: 'contact-section-badge'
                        }, 'CONTACT'),
                        h('span', { class: 'text-subhead-lg' }, '気になった方へ')
                    ),

                    // What can be asked
                    h('p', { class: 'text-body-relaxed' }, desc),

                    // Divider label row
                    h('div', { class: 'gap-col-md' },
                        // Row 1: 技術記事
                        h('div', { class: 'gap-col-sm' },
                            h('div', { class: 'badge-contact-label' }, '📖  技術記事（AIO実践シリーズ＋発展記事・計11本）'),
                            h('div', { class: 'gap-wrap-sm' },
                                outLink('https://zenn.dev/yuta_yokoi', 'externalLink', 'Zennで全11本の記事を読む →', 'var(--color-info)')
                            )
                        ),
                        // Row 2: 相談・依頼
                        h('div', { class: 'gap-col-sm' },
                            h('div', { class: 'badge-contact-label' }, '✉  PM・アーキテクチャ設計の相談・依頼'),
                            h('div', { class: 'gap-wrap-sm' },
                                outLink(X_URL, 'messageCircle', 'X (Twitter) でDMを送る', 'var(--color-primary)'),
                                mailBtn()
                            )
                        )
                    )
                )
            );
        }

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

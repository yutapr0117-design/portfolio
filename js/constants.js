/**
 * js/constants.js — Application-wide constants & limits (v80+ Stage 5-d extraction)
 *
 * main.js の `CONSTANTS` を byte-equivalent に物理分割した葉モジュール。
 *
 * 【SITE_CONFIG / AUTHOR と分離する理由】
 * - `SITE_CONFIG.VERSION` / `SITE_CONFIG.LAST_UPDATED` は check_repository_consistency.py
 *   の Check 2（main.js VERSION 文字列）と Check 17（LAST_UPDATED）が main.js から
 *   名前で抽出するため、main.js に残す（移設すると Check が壊れる）。
 * - `AUTHOR.DISPLAY_NAME` は Store の defaultProfile.name で参照されており、Store と
 *   main.js の他の場所からも使われる。AUTHOR は表示用の identity registry のため、
 *   別 increment で扱う（本 increment では触らない）。
 * - 一方 `CONSTANTS` は STORAGE_KEY / LIMITS / 各種 timing / DEBUG など、版管理対象
 *   ではない実行時定数のみで構成され、Check のキー抽出スコープ外。安全に分離できる。
 *
 * 【closure-deps = none の根拠】
 * - 値の評価時に IIFE クロージャ状態（AUTHOR / SITE_CONFIG / Store / State）を参照しない
 * - DOM に触れない（document / window 系 API は使わない）
 * - 参照するブラウザグローバルは `crypto`, `sessionStorage`, `location`, `URLSearchParams`,
 *   `Date`, `Math` のみ（いずれもグローバルに到達可能、closure 不要）
 *
 * 【module-load 時の副作用（既存挙動と等価）】
 * - `TAB_ID` の IIFE は `sessionStorage.getItem('portfolio_tab_id_v45')` を実行し、
 *   未保存なら crypto.randomUUID で生成して setItem する（cross-tab coordination）。
 *   モジュールロード時に 1 回だけ評価される動きは、抽出前 IIFE 内部での 1 回評価と
 *   挙動が等価。schema（key 名 / 値形式）も byte-identical（呼び出し側 main.js が制御）。
 * - `DEBUG` は location.hostname / location.search の読み取りのみ（副作用なし）。
 *
 * 【挙動契約（抽出前後で byte-equivalent）】
 * - 各フィールドの型・値生成式は抽出前後で 1 ビットも変えない。
 * - LIMITS の各上限値は呼び出し側（Store の deserialization、Apps の validation）が
 *   そのまま参照する。
 * - import/export bijection と葉性（import ゼロ）は Check 47 が BLOCKING で機械強制する。
 */
export const CONSTANTS = {
    STORAGE_KEY: 'portfolio_enhanced_v45',
    SNAPSHOT_KEY: 'portfolio_snapshot_v45',
    SCHEMA_VERSION: 12,            // Cross-tab coordination
    TAB_ID: (() => {
        try {
            const key = 'portfolio_tab_id_v45';
            let id = sessionStorage.getItem(key);
            if (!id) {
                id = crypto.randomUUID ? crypto.randomUUID() :
                    (() => {
                        const timestamp = Date.now().toString(16);
                        const random = Math.random().toString(16).substring(2, 10);
                        return `fallback-${timestamp}-${random}`;
                    })()
                // codeql[js/clear-text-storage-of-sensitive-data] - False positive: stores a random UUID for cross-tab coordination only.
                sessionStorage.setItem(key, id);
            }
            return id;
        } catch {
            return Math.random().toString(36).substring(2);
        }
    })(),

    // Limits for validation
    LIMITS: {
        PROJECT_NAME: 120,
        PROJECT_ID: 80,
        CATEGORY: 80,
        SUMMARY: 800,
        PROBLEM: 1200,
        APPROACH: 1200,
        IMPACT: 1200,
        TASK_TITLE: 200,
        TODO_TEXT: 300,
        QUIZ_SEARCH: 200,        // クイズ検索語の保持上限（store.js normalize が quizSearch を preserve する際の bound・単一ソース）
        AI_MESSAGE: 5000,
        AI_HISTORY: 80,          // AI アシスタント履歴の保持エントリ数上限（store.js normalize + ai-page.js add の単一ソース）
        POMODORO_HISTORY: 200,   // ポモドーロ完了履歴の保持エントリ数上限（store.js normalize + pomodoro-page.js complete の単一ソース）
        NOTES_TEXT: 20000,
        MAX_PROJECTS: 1000,
        MAX_TASKS: 500,
        MAX_TODOS: 1000,
    },

    // Pomodoro 既定状態の単一ソース (state.js の clone fallback + store.js の default が参照・Check 370 が
    // magic リテラル {work:25,short:5,long:15} / 1500 の直接使用を BLOCKING 禁止し cross-file drift を防ぐ)。
    // オブジェクトは参照共有を避けるため利用側で必ず spread する ({ ...CONSTANTS.POMODORO_DEFAULT_SETTINGS })。
    POMODORO_DEFAULT_SETTINGS: { work: 25, short: 5, long: 15 },  // 分: 集中/短休憩/長休憩
    POMODORO_DEFAULT_REMAINING_SEC: 1500,                          // = work(25分) × 60 の初期残り秒

    // Timing
    DEBOUNCE_DELAY: 150,       // ms — input debounce (search, filters)

    // Layout
    MOBILE_BREAKPOINT: 920,    // px — sidebar → drawer breakpoint（matchMedia で js/mobile-drawer.js が参照）

    // Dev flag (used for stricter guards)
    DEBUG: (location.hostname === 'localhost' || location.hostname === '127.0.0.1' || new URLSearchParams(location.search).has('debug')),
};

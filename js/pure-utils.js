/**
 * ════════════════════════════════════════════════════════════════════════════
 * js/pure-utils.js — Pure Utility Layer (extracted from main.js, v80+ Stage 2)
 * ════════════════════════════════════════════════════════════════════════════
 *
 * @fileoverview
 * これまで `main.js` の単一 IIFE 内に同居していた「純粋ユーティリティ（pure
 * utilities）」を、ローカル ESM (`import`/`export`) で物理分割した最初の抽出単位。
 * v80+ staged major update の Stage 2（pure utility 抽出）に該当する。
 *
 * ── なぜ最初にこれを切り出すのか（抽出順序の根拠）───────────────────────────
 * `main-js-extraction-map.md` の抽出順序は「副作用の小さい順」
 * （pure utility → constants/data → service rails → render）。純粋関数は定義上、
 * 出力が引数のみで決まり、DOM・モジュール内クロージャ状態・読み込み順序のいずれにも
 * 依存しない。したがって別モジュールへ移して `import` しても**挙動が変わらない**こと
 * が静的に保証できる。視覚回帰 baseline が無い段階でも安全に実施できる最小リスクの分割。
 *
 * ── このモジュールに入れてよい関数の条件（後続者向けの判断基準）──────────────
 *   (1) 出力が引数のみで決まる（参照透過に近い）。
 *   (2) `main.js` のクロージャ束縛（CONSTANTS / SITE_CONFIG / Store / state /
 *       RouteState / EffectRails / BindingRegistry / PAGE_META / Router 等）を
 *       一切参照しない。標準のブラウザ/JS グローバル（crypto, Math, URL, fetch,
 *       console, window, scheduler, setTimeout 等）のみ使用してよい。
 *   (3) DOM ノードを保持・変更しない。
 *       → DOM を触る `clear(node)` や localStorage をラップする `Storage` は
 *         service rail なので **ここには入れない**（main.js に残置。Stage 4 の領分）。
 * 抽出元 main.js で上記 3 条件を全関数について確認済み（closure-deps = none）。
 *
 * ── 不変条件（破壊厳禁）─────────────────────────────────────────────────────
 *   - 各関数の **シグネチャと挙動はバイト等価** で維持する。特に `sanitizeUrl` は
 *     セキュリティ境界（http/https 以外を null にする危険スキーム防止）であり、
 *     挙動を 1 ビットも変えてはならない。
 *   - `generateId` は UUID v4 形式。`slugify` のフォールバックがこれに依存する。
 *   - Boring Technology 維持：外部ライブラリへの依存を増やさない。本モジュールの
 *     import は **ゼロ**（依存ゼロの葉モジュール。Check 47c が機械強制）。
 *
 * ── 読み込み機構 ───────────────────────────────────────────────────────────
 * `index.html` は `main.js` を `<script type="module">` で読み込み、`main.js` が
 * 本モジュールを `import` する。CSP は `script-src 'self'` のため、同一オリジンの
 * モジュール取得は追加設定なしで許可される。
 * ════════════════════════════════════════════════════════════════════════════
 */

'use strict';

/**
 * generateId — 一意な識別子（UUID v4）を生成する。
 *
 * プロジェクト ID・slug のフォールバック等、衝突しない一意キーが必要な箇所で使う。
 * 第一候補はブラウザ標準の `crypto.randomUUID()`（暗号学的に安全な乱数）。古い環境や
 * `crypto` が露出していない文脈では `Math.random()` ベースの RFC 4122 互換テンプレート
 * 置換でフォールバックする（暗号強度は無いが UI 用途の一意性には十分）。
 *
 * 設計メモ: try/catch で `crypto` 参照自体の例外（一部の制限環境）も握りつぶし、必ず
 * 文字列を返す。例外を投げないことが呼び出し側の前提になっている。
 *
 * @returns {string} `xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx` 形式の UUID v4 文字列。
 */
export function generateId() {
    try {
        // 暗号学的に安全な UUID v4。モダンブラウザでは常にこちらが使われる。
        if (typeof crypto !== 'undefined' && crypto.randomUUID) { return crypto.randomUUID(); }
    } catch (e) { /* crypto 参照不可の制限環境 → 下のフォールバックへ */ }
    // フォールバック: テンプレートの 'x' を 0-15 の乱数 16 進、'y' を 8/9/a/b に置換。
    // これにより RFC 4122 の variant/version ビットを満たす UUID v4 形を保証する。
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
        const r = Math.random() * 16 | 0;           // 0..15 の整数乱数
        const v = c === 'x' ? r : (r & 0x3 | 0x8);  // 'y' は variant ビット (8,9,a,b)
        return v.toString(16);
    });
}

/**
 * clamp — 数値を [min, max] の範囲に収める（範囲外なら境界値に丸める）。
 *
 * Pomodoro の作業/休憩分数や、リスト選択インデックスの範囲制限など、「ユーザー入力や
 * 計算結果が想定範囲を超えないことを保証したい」場面で使う。
 *
 * @param {number} num - 対象の数値。
 * @param {number} min - 下限（含む）。
 * @param {number} max - 上限（含む）。
 * @returns {number} `min <= 戻り値 <= max` を満たす値。
 */
export function clamp(num, min, max) {
    // Math.min で上限に、Math.max で下限に押し込む。順序は数学的に可換。
    return Math.max(min, Math.min(max, num));
}

/**
 * debounce — 関数呼び出しを「最後の呼び出しから delay ミリ秒静かになるまで」遅延する。
 *
 * 連続発火するイベント（検索入力・ウィンドウリサイズ等）に対し、最終的な 1 回だけ実処理を
 * 走らせて負荷とちらつきを抑える。呼び出しのたびに前回の予約タイマーを破棄し張り直す。
 *
 * 注意: 返り値は **新しい関数** であり、その関数がクロージャに `timer` を保持する。同一の
 * debounced 関数インスタンスを使い回して初めてデバウンスが効く（毎回 debounce() を再生成
 * すると効果が無い）。
 *
 * @param {Function} fn - デバウンス対象の関数。
 * @param {number} delay - 静粛時間（ミリ秒）。
 * @returns {Function} デバウンスされた関数。
 */
export function debounce(fn, delay) {
    let timer; // 直近の予約タイマー ID（クロージャで保持）
    return (...args) => {
        clearTimeout(timer);                          // 前回予約を破棄
        timer = setTimeout(() => fn(...args), delay); // 新たに予約し直す
    };
}

/**
 * throttle — 関数呼び出しを「limit ミリ秒に最大 1 回」に間引く（leading-edge 方式）。
 *
 * debounce が「静かになってから 1 回」なのに対し、throttle は「先頭の 1 回を即通し、その後
 * limit ミリ秒は無視」する。スクロール等、間隔を空けつつ反応はさせたい処理に向く。
 *
 * @param {Function} fn - スロットル対象の関数。
 * @param {number} limit - 最小発火間隔（ミリ秒）。
 * @returns {Function} スロットルされた関数。
 */
export function throttle(fn, limit) {
    let inThrottle; // true の間は発火を無視するゲート
    return (...args) => {
        if (!inThrottle) {
            fn(...args);                                 // 先頭の 1 回を即実行
            inThrottle = true;                           // ゲートを閉じる
            setTimeout(() => inThrottle = false, limit); // limit 後に再度開く
        }
    };
}

/**
 * tokenize — 文字列を検索・類似度用のトークン配列へ分解する。
 *
 * 日本語（ひらがな U+3040–309F / カタカナ U+30A0–30FF / 漢字 U+4E00–9FAF）と英数字・
 * ハイフンを「語」として残し、それ以外の区切り文字で分割。小文字化し空要素を除去する。
 *
 * 非破壊メモ: `String(s || "")` で null/undefined/数値も安全に文字列化してから処理する
 * ため、どんな入力でも例外を投げず必ず配列を返す。
 *
 * @param {*} s - 任意の入力（文字列以外も許容）。
 * @returns {string[]} 小文字化された語トークンの配列（空要素なし）。
 */
export function tokenize(s) {
    return String(s || "")
        .toLowerCase()
        // 「語を構成しない文字」の連続で分割。\w と日本語レンジ・ハイフンは語側に残す。
        .split(/[^\w\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF\-]+/)
        .filter(Boolean); // 分割で生じる空文字を除去
}

/**
 * slugify — 任意文字列を URL/識別子向けの slug へ変換する。
 *
 * 前後空白除去 → 小文字化 → 空白/アンダースコアをハイフンへ → 語構成外文字を削除、の順に
 * 正規化。日本語文字は保持する。結果が空（記号のみ等）になった場合は `generateId()` の
 * 先頭 8 文字を使った `p-xxxxxxxx` 形のフォールバック slug を返す。
 *
 * 依存メモ: 本関数は同モジュール内の `generateId` に依存する（フォールバック用）。関数宣言は
 * ホイスティングされるため定義順の制約は無いが、可読性のため `generateId` を先に置いている。
 *
 * @param {*} str - 任意の入力。
 * @returns {string} 非空の slug 文字列。
 */
export function slugify(str) {
    const s = String(str || '').trim().toLowerCase();
    return s
        .replace(/[\s_]+/g, '-') // 空白・アンダースコア（連続含む）→ ハイフン 1 個
        // 語構成外文字を除去（\w・ハイフン・日本語レンジは残す）
        .replace(/[^\w\-\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]/g, '')
        || `p-${generateId().slice(0, 8)}`; // 空になったら一意フォールバック
}

/**
 * sanitizeUrl — URL 文字列を検証し、安全な http/https のみ通す（セキュリティ境界）。
 *
 * ⚠️ これは XSS・危険スキーム（javascript:, data:, file: 等）防止の境界である。
 * `new URL()` でパースに失敗する不正値、および http/https 以外のプロトコルはすべて `null`
 * を返して拒否する。リンク描画前の検証に使われる。**挙動を変更してはならない**（緩めると
 * XSS 経路が開く）。
 *
 * @param {string} url - 検証対象の URL 文字列。
 * @returns {string|null} 正規化された http/https URL、危険・不正なら null。
 */
export function sanitizeUrl(url) {
    try {
        const u = new URL(url);
        // http/https のみ許可。それ以外（javascript:, data: 等）は拒否。
        if (u.protocol === 'http:' || u.protocol === 'https:') { return u.toString(); }
        return null;
    } catch {
        // URL としてパースできない（相対パス・空・不正文字列）→ 拒否。
        return null;
    }
}

/**
 * safeFetchJSON — fetch をラップし、HTTP ステータスと JSON パースを厳密に検証する。
 *
 * fetch() は 404/500 等の HTTP エラーでも Promise を **resolve** してしまうため、
 * 「ハッピーパスのみ」のコードは静かに壊れやすい。本ラッパーは
 *   - `response.ok` が false ならログを残して null、
 *   - JSON パース失敗もログを残して null、
 *   - ネットワーク断/CORS 例外もログを残して null、
 * を返し、呼び出し側を「成功時データ or null」という単純な契約に保つ。
 *
 * @param {string} url - 取得先 URL。
 * @param {RequestInit} [options={}] - fetch オプション。
 * @returns {Promise<any|null>} 成功時はパース済み JSON、失敗時は null。
 */
export async function safeFetchJSON(url, options = {}) {
    try {
        const response = await fetch(url, options);
        // fetch 特有の罠: HTTP エラーでも Promise は resolve される。明示的に弾く。
        if (!response.ok) {
            console.error('[safeFetch] HTTP error ' + response.status + ' for: ' + url);
            return null;
        }
        // JSON パースエラーに対する防御（本文が JSON でない場合）。
        try {
            return await response.json();
        } catch (parseErr) {
            console.error('[safeFetch] JSON parse failed for: ' + url, parseErr);
            return null;
        }
    } catch (networkErr) {
        // CORS エラー・ネットワーク断・タイムアウト等。
        console.error('[safeFetch] Network/CORS error for: ' + url, networkErr);
        return null;
    }
}

/**
 * deepClone — プレーンオブジェクト/配列/Date を再帰的に深いコピーする。
 *
 * 状態オブジェクトを破壊せずに複製したい場面（migration・スナップショット等）で使う。
 * プリミティブはそのまま返し、Date は同時刻の新インスタンス、配列は要素ごとに再帰、
 * オブジェクトは自前プロパティのみ（プロトタイプ汚染を避けるため hasOwnProperty 判定）を
 * 再帰コピーする。
 *
 * 範囲メモ: JSON 化不能な値（関数・循環参照・Map/Set 等）は対象外。現状の利用箇所
 * （プレーンな状態データ）では十分。仕様拡張時は要注意。
 *
 * @param {*} obj - 複製対象。
 * @returns {*} 深いコピー。
 */
export function deepClone(obj) {
    if (obj === null || typeof obj !== 'object') { return obj; } // プリミティブ/null はそのまま
    if (obj instanceof Date) { return new Date(obj.getTime()); }  // Date は同時刻の新個体
    if (Array.isArray(obj)) { return obj.map(deepClone); }        // 配列は要素ごとに再帰
    const cloned = {};
    for (const key in obj) {
        // プロトタイプ由来のキーを除外（汚染・意図しない継承プロパティの混入を防ぐ）
        if (Object.prototype.hasOwnProperty.call(obj, key)) {
            cloned[key] = deepClone(obj[key]);
        }
    }
    return cloned;
}

/**
 * yieldToMain — メインスレッドを一時的に解放し、INP（操作応答性）を改善する。
 *
 * 長い同期描画の途中で `await yieldToMain()` を挟むと、ブラウザが保留中の入力処理や描画を
 * 割り込ませる隙を得る。標準の `scheduler.yield()` が使える環境ではそれを、無い環境では
 * `setTimeout(resolve, 0)` のマクロタスクでフォールバックする。
 *
 * @returns {Promise<void>} 次のタスク境界で解決する Promise。
 */
export const yieldToMain = () => {
    // scheduler.yield() は応答性に最適化された標準 API（対応環境のみ）。
    if ('scheduler' in window && 'yield' in scheduler) {
        return scheduler.yield();
    }
    // フォールバック: 0ms タイマーで 1 タスク分メインスレッドを明け渡す。
    return new Promise(resolve => setTimeout(resolve, 0));
};

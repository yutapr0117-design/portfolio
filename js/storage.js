/**
 * js/storage.js — Safe localStorage wrapper (v80+ Stage 5-c extraction)
 *
 * このモジュールは main.js の `Storage` オブジェクトを byte-equivalent に物理分割した
 * 葉モジュール（dependency-free leaf）である。Stage 5-c での抽出時、extraction-map §3.5
 * の「Stage 4 候補 — Safe Storage」では中〜高層（schema 後方互換必須）と分類されていたが、
 * 実コード読解により closure-deps は実質ゼロであることが判明したため抽出した。
 *
 * 【closure-deps = none の根拠】
 * 1. main.js の IIFE クロージャ状態（`CONSTANTS` / `AUTHOR` / `SITE_CONFIG` / `Store` /
 *    `State` 等）を 1 つも参照していない（4 メソッドのすべてが引数のみで挙動が決まる）。
 * 2. DOM に触れない（document / window 系 API も localStorage 経由以外は使わない）。
 * 3. localStorage のキー形式・値形式の決定権は呼び出し側（main.js）にあり、本モジュールは
 *    その契約に介入しない（schema 後方互換は呼び出し側の責務）。
 *
 * 【セキュリティ境界（呼び出し側との契約）】
 * - localStorage には「ポートフォリオの UI 状態（タスクリスト・テーマ・ポモドーロ履歴 等）」
 *   以外を保存しない。資格情報・トークン・PII は localStorage に置かない（CodeQL の
 *   `js/clear-text-storage-of-sensitive-data` 警告は本契約により false positive）。
 * - 例外を握りつぶす（catch して null / false を返す）のは、容量超過・プライベートブラウジング・
 *   ストレージ無効化等の SPA 非致命エラーを silent degradation させる意図的設計。fail-loud な
 *   挙動が望ましい場面では呼び出し側が事後に戻り値を判定する。
 *
 * 【挙動契約（抽出前後で byte-equivalent）】
 * - `get(key)`    → localStorage 値（string）または null（未保存 or 例外）
 * - `set(key, value)` → true（保存成功）または false（容量超過・無効値・例外）
 * - `remove(key)` → true（削除成功）または false（例外）
 * - `parse(key)`  → JSON.parse 後の値、または null（未保存・無効 JSON・例外）
 *
 * 【非破壊性】
 * - 4 メソッドの署名と返り値・例外挙動は抽出前後で 1 ビットも変えない。
 * - localStorage の key 形式・値形式（schema）も不変（決定権は呼び出し側）。
 * - import/export bijection と葉性（import ゼロ）は Check 47 が BLOCKING で機械強制する。
 */
export const Storage = {
    get(key) {
        try {
            return localStorage.getItem(key);
        } catch {
            return null;
        }
    },

    set(key, value) {
        try {
            // codeql[js/clear-text-storage-of-sensitive-data] - False positive:
            // Stores portfolio UI state (task list, theme, pomodoro history).
            // No credentials, tokens, or PII are stored in localStorage.
            localStorage.setItem(key, value);
            return true;
        } catch {
            return false;
        }
    },

    remove(key) {
        try {
            localStorage.removeItem(key);
            return true;
        } catch {
            return false;
        }
    },

    parse(key) {
        const data = this.get(key);
        if (!data) {return null;}
        try {
            return JSON.parse(data);
        } catch {
            return null;
        }
    }
};

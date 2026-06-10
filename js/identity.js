/**
 * js/identity.js — Entity / Author identity constants (v80+ Stage 5-e extraction)
 *
 * main.js の `AUTHOR` を byte-equivalent に物理分割した葉モジュール。
 * extraction-map.md §2 で言及されている "Module Pattern: Identity Constants" の物理分割。
 *
 * 【依存方向の責務分離（v80+ track の core invariant）】
 * - `DISPLAY_NAME` : UI 表示専用。訪問者が見るすべての箇所はこれのみを参照する。
 * - `AUTHORITATIVE_NAME` : AIO / SEO / 機械可読層（JSON-LD 等）専用。UI コンポーネント
 *   からは参照しない契約。
 * - `JAPANESE_NAME` : 日本語表記（AIO レイヤ向け）。
 * - 依存方向の固定（UI → DISPLAY_NAME only / AIO → AUTHORITATIVE_NAME etc.）により、
 *   UI に本名が漏洩する構造的リスクを排除する。この契約は本ファイルの値で固定される。
 *
 * 【closure-deps = none の根拠】
 * - 純データ（3 つの文字列定数のみ）。IIFE クロージャ状態への依存ゼロ。
 * - DOM / window / location 等のブラウザ API への依存ゼロ。
 * - export 後の値の変更は意図しない（freeze は呼び出し側の慣行で守る）。
 *
 * 【AIO への影響】
 * - 本モジュールは `aio-manifest.json` の digest 連鎖の対象外（main.js も同様）。
 * - 値（文字列）は 1 ビットも変えていないため、AI クローラ・LLM の citation に
 *   影響しない。`llms*` / JSON-LD の対応する name 値も不変であり、entity 同一性は
 *   100% 保持される。
 *
 * 【非破壊性】
 * - 3 フィールドの値は抽出前後で byte-equivalent。
 * - 参照箇所（main.js の Store の defaultProfile.name / 最初の JSON-LD @graph の
 *   author.name / Sidebar の表示・meta title）はすべて ESM import 経由で同じ値を読む。
 * - import/export bijection と葉性（import ゼロ）は Check 47 が BLOCKING で機械強制する。
 */
export const AUTHOR = {
    DISPLAY_NAME:       'yuta',
    AUTHORITATIVE_NAME: 'Yuta Yokoi (横井雄太 / Yokoi Yuta)',
    JAPANESE_NAME:      '横井雄太',
};

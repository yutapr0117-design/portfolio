/**
 * js/brand.js — Brand (primary palette / font) manager factory (v80+ Stage 5-f extraction)
 *
 * main.js の `Brand` IIFE モジュールを依存注入（dependency-injection / factory pattern）で
 * 物理分割した葉モジュール。Storage への closure 依存を引数で受け取ることで、Check 47c
 * の「葉モジュール = 内部 import ゼロ」契約を維持しつつ、Brand の挙動・公開 API を完全に
 * byte-equivalent に保つ。
 *
 * 【なぜ factory pattern か】
 * Brand は元の main.js IIFE で `Storage.get(KEY)` / `Storage.set(KEY, v)` を呼び出していた。
 * 単純な IIFE モジュール抽出だと、Brand モジュール内部で `import { Storage } from './storage.js'`
 * が必要になり Check 47c に違反する（cross-module import の累積を防ぐための葉モジュール契約）。
 * そこで `createBrand(storage)` という factory 関数を export し、main.js 側で
 * `const Brand = createBrand(Storage)` のように合成する。これは Stage 4 ui-components の
 * 「同居モジュール内で完結」とは別パターンの非破壊抽出戦略であり、複数の service rail を
 * 独立葉モジュール化する場合の汎用解（後続の Theme / DiagnosticsRail にも適用予定）。
 *
 * 【closure-deps = none の根拠（葉モジュール契約）】
 * - 本モジュールは import 文を 1 つも持たない（Check 47c 緑）。
 * - `createBrand` factory は引数 `storage` を closure に取り込み Brand object を構成するため、
 *   呼び出し側（main.js）が import 済みの Storage instance を渡すことで結合する。
 * - 結果として「葉モジュール契約 + Storage への論理依存」を両立する。
 *
 * 【挙動契約（抽出前後で byte-equivalent）】
 * - 公開 API: `{ init, set, get, KEY }`（4 メンバー、unchanged）
 * - `apply(brand)` の内部実装は IIFE 内ローカルで隠蔽
 * - localStorage の key 'portfolio_brand_v45' / 値の 'indigo' or 'classic' は schema 不変
 * - `document.documentElement.setAttribute('data-brand', ...)` の DOM 副作用も不変
 *
 * 【依存】
 * - `storage` (引数): `{ get(key): string|null, set(key, value): boolean }` を満たすこと
 *   （js/storage.js の Storage オブジェクトがこれを満たす）
 * - ブラウザグローバル: `document.documentElement` （DOM APIへの直接アクセス）
 */
export function createBrand(storage) {
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
        const saved = storage.get(KEY);
        apply(saved || DEFAULT);
    }

    function set(brand) {
        const b = apply(brand);
        storage.set(KEY, b);
    }

    function get() {
        return document.documentElement.getAttribute('data-brand') || DEFAULT;
    }

    return { init, set, get, KEY };
}

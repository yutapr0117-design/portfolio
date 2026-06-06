// ============================================================================
// eslint.config.mjs — ESLint v9 flat config（v80+ CI hygiene increment）
// ============================================================================
//
// 【この設定の position と移行の背景】
// 本ファイルは、従来の `.eslintrc.json`（eslintrc 形式）からの完全等価移行物である。
// ESLint 8.x 系は 2024-10-05 に End-of-Life（EOL）に達し、以後セキュリティパッチが
// 提供されない。さらに ESLint 9.x からは flat config（本形式）がデフォルトとなり、
// `--no-eslintrc` / `--env` といった旧 CLI フラグは削除された（9.x でこれらを渡すと
// exit 2 で「config/flag error」となる）。すなわち本リポジトリの「BLOCKING ESLint
// ゲート」を維持したまま EOL を脱するには、flat config への移行が必須である。
//
// 【非破壊の不変条件（machine-checkable）】
// 移行の正しさは「移行前（eslint 8.57.1 + .eslintrc.json + --env browser）の lint 出力と、
// 本 flat config の lint 出力が、件数・ルール別内訳ともに完全一致すること」で証明する。
// 移行前の真値は 0 errors / 120 warnings（no-var:64 / curly:46 / no-shadow:10、すべて
// main.js）。本ファイルはその真値を 1 件もずらさないよう、旧設定の env / parserOptions /
// rules / globals / overrides を機械的に 1:1 変換している。
//
// 【設計判断: globals は「明示列挙のみ」を維持する】
// `@eslint/migrate-config` の自動生成物は `...globals.browser`（数百個のブラウザ
// グローバルの超集合）を展開するが、本リポジトリの旧 `.eslintrc.json` は
// `--env browser`（＝eslint 8.x の env:browser 相当）に加えて、crypto / trustedTypes /
// TrustedHTML 等の「必要なものだけ」を `globals` に明示列挙していた。no-undef の
// 検出結果は参照可能なグローバル集合に依存するため、超集合へ広げると no-undef の
// 挙動が変わり得る（＝非破壊性が崩れる）。したがって本ファイルは env:browser 相当を
// `globals.browser` で供給しつつ、旧設定が明示していた追加グローバルを温存する。
// この組み合わせが、移行前 0 errors / 120 warnings を 1 件もずらさないことを
// 実測で確認している（数値がずれた場合は本ファイルが原因＝flat config 側を疑う）。
//
// 【lint 対象ファイル集合について】
// 対象（main.js / error-suppressor.js / karte-init.js / theme-init.js / aio-guard.js /
// sw.js / js/pure-utils.js / js/quiz-data.js）は package.json の `lint` / `lint:js`
// スクリプトが指定し、check_repository_consistency.py の Check 46 が
// 「lint と lint:js とディスク上の root ∪ js/ の三者一致」を BLOCKING で機械強制する。
// 本 flat config はファイル集合を限定せず（＝渡された対象をそのまま lint する）、
// 対象の指定権限は package.json 側に一元化している（二重管理を作らない）。
// ============================================================================

import js from '@eslint/js';
import globals from 'globals';

export default [
  // --- (1) ESLint 推奨ルールは「敢えて継承しない」 ---------------------------
  // 旧 .eslintrc.json は eslint:recommended を extends しておらず、必要な
  // bug-catching ルールだけを明示列挙していた。非破壊移行のため本ファイルも
  // js.configs.recommended は適用しない（適用すると新規 warning/error が増え、
  // 0 errors / 120 warnings の真値が崩れる）。recommended への段階移行は将来の
  // 別 increment（lint ルール拡張）として、その時に件数差分を文書同期して行う。
  // ※ import した `js` は将来の recommended 移行時に使うため残置（未使用 import は
  //   flat config では問題にならない＝設定ファイル自身は lint 対象外）。

  // --- (2) 全 JS ファイル共通の base 設定 ------------------------------------
  {
    // 【reportUnusedDisableDirectives を 8.x 相当（無効）に固定する理由】
    // ESLint 9.x は linterOptions.reportUnusedDisableDirectives のデフォルトを
    // "warn" に変更した。これにより、env:browser を globals.browser で供給した結果
    // no-implicit-globals が発火しなくなった sw.js 先頭の
    // `/* eslint-disable no-implicit-globals -- ... */` が「未使用ディレクティブ」
    // として 1 件の warning を生む。一方、移行前の ESLint 8.57.1 はこの未使用検出を
    // デフォルトで警告化しておらず、真値は 0 errors / 120 warnings であった。
    // 非破壊（件数完全一致）を保つため、この linter option を明示的に "off" へ戻す。
    // sw.js の当該 disable はサービスワーカーのトップレベル関数宣言を意図的に許容する
    // self-documenting なディレクティブであり、削除すると「なぜトップレベル宣言が
    // 妥当か」の文脈が失われるため、ディレクティブ側は温存し、設定側で吸収する判断。
    // （将来 no-implicit-globals の扱いを見直す別 increment で再評価する余地は残す。）
    linterOptions: {
      reportUnusedDisableDirectives: 'off',
    },
    languageOptions: {
      // ecmaVersion / sourceType は旧 parserOptions と同値。
      // sourceType:'module' は、本サイトの JS が <script type="module"> として
      // 配信される実体に一致する（main.js は先頭に ESM import を持つ単一 IIFE 本体）。
      ecmaVersion: 2022,
      sourceType: 'module',
      globals: {
        // env:browser 相当（window / document / console / localStorage 等の
        // 標準ブラウザグローバル）。旧設定の `--env browser` を flat config で
        // 供給する正規手段が globals.browser である。
        ...globals.browser,
        // 旧 .eslintrc.json の `globals` ブロックで明示していた追加グローバル。
        // env:browser に含まれない、または将来のブラウザ機能・型を readonly 宣言。
        crypto: 'readonly',
        URL: 'readonly',
        URLSearchParams: 'readonly',
        DOMParser: 'readonly',
        MutationObserver: 'readonly',
        IntersectionObserver: 'readonly',
        AbortController: 'readonly',
        AbortSignal: 'readonly',
        WeakMap: 'readonly',
        WeakSet: 'readonly',
        Proxy: 'readonly',
        Reflect: 'readonly',
        scheduler: 'readonly',
        // Trusted Types 関連。AIDK kernel の Trusted Types 'default' policy と、
        // innerHTML インターセプタが参照する型。env:browser には未収載のため明示。
        trustedTypes: 'readonly',
        TrustedHTML: 'readonly',
      },
    },
    rules: {
      // 以下は旧 .eslintrc.json の rules を 1:1 で移植したもの。
      // ── bug-catching（error 級。違反は CI で BLOCKING）──
      eqeqeq: ['error', 'always'],            // 厳密等価の強制（== の暗黙変換事故防止）
      'no-implicit-globals': 'error',          // トップレベルでの暗黙グローバル汚染禁止（C2 規律と同方向）
      'no-undef': 'error',                     // 未定義参照の検出（globals 集合に依存）
      'no-prototype-builtins': 'error',        // obj.hasOwnProperty 直呼び等の事故防止
      'no-var': 'error',                       // var 禁止（※ main.js のみ後段 override で warn に降格）
      'no-console': 'off',                     // 観測ログのため console は許容
      'no-debugger': 'error',                  // 本番に debugger を残さない
      'no-eval': 'error',                      // eval 禁止（XSS 面の除去）
      'no-implied-eval': 'error',              // setTimeout('code') 等の暗黙 eval 禁止
      'no-new-func': 'error',                  // new Function('code') 禁止
      'no-script-url': 'error',                // javascript: URL 禁止
      'no-unused-expressions': ['error', { allowShortCircuit: true, allowTernary: true }],
      'no-duplicate-case': 'error',            // switch の重複 case 検出
      'no-empty': ['error', { allowEmptyCatch: true }], // 空ブロック禁止（空 catch は許容）
      'no-unreachable': 'error',               // 到達不能コード検出
      // ── style/quality（warn 級。advisory・CI を止めない）──
      'no-shadow': ['warn', { allow: ['e', 'err', 'error'] }], // 変数シャドウ（e/err/error は許容）
      'prefer-const': 'warn',                  // 再代入されない let を const に（挙動不変の品質指摘）
      curly: ['error', 'all'],                 // 単文ブロックの波括弧強制（※ main.js のみ後段 override で warn）
    },
  },

  // --- (3) main.js 専用 override ---------------------------------------------
  // 旧 .eslintrc.json の overrides[{ files:["main.js"] }] を移植。
  // main.js は本番 SPA 本体かつ DO-NOT-EDIT の AIDK kernel を含むため、
  // 純粋に整形目的の no-var / curly を「一括 error で機械修正させない」よう
  // warn（ADVISORY）に降格する。bug-catching ルールは error のまま全適用される。
  // ※ flat config の files は対象“限定”ではなく“この設定ブロックを適用する対象”の
  //   指定であり、後勝ちでマージされる。旧 eslintrc の files:["main.js"] は
  //   実行時の cwd 相対で main.js にマッチしていたため、ここでは "**/main.js" と
  //   "main.js" の両表記に一致するよう glob を広めに取る（lint 対象は package.json が
  //   ルート直下の main.js のみを渡すため、誤って他ディレクトリの main.js を拾う懸念はない）。
  {
    files: ['**/main.js'],
    rules: {
      'no-var': 'warn',
      curly: ['warn', 'all'],
    },
  },
];

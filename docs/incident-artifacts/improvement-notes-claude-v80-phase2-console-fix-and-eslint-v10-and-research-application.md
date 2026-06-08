# improvement-notes-claude-v80-phase2-console-fix-and-eslint-v10-and-research-application

```
Document-Type    : Claude 視点の increment 改善ノート（後続 AI への引き継ぎ証跡）
Canonical-Source : AI2AI.md / llms-full.txt
Canonical-Status : NON-CANONICAL / 補助証跡（Tier 4）
Increment        : console-fix + eslint-v10 + research-application（v80+ track / 本コミット）
Last-Updated     : 2026-06-07
```

> 本ファイルは増分の意思決定・根拠・検証を Claude 視点で残す補助証跡である。正典は `AI2AI.md`、真実源は `llms-full.txt`。数値の権威値は `total-check-runbook.md` §9。

---

## 0. BLUF

オーナーの三依頼——(a) 公開現物のコンソールエラー 2 件の根本・非破壊修正、(b) トータルチェックと発見改善の適用、(c) リサーチ結果の全適用（特に ESLint v10 移行）——を、確認で止めず適用まで遂げた。加えてメタ要求として「リサーチは全適用までがリサーチ」という規律を、メモリと、メモリ未参照に備えてリポジトリ（`research-application-policy.md` ＋ `CLAUDE.md` §0）の双方へ明文化した。`npm run verify` は exit 0（54 checks・Check 52 のみ ADVISORY・ESLint 0 errors / 120 warnings 不変・脆弱性 0）。AIO 正本層 / binary / `style.css` / `main.js` は 1 バイトも変更しておらず SHA-256 で IDENTICAL を証明（digest 再生成不要）。

---

## 1. console 404 の根本原因——私（Claude）の漏れの認定

公開サイトのコンソールに `GET .../portfolio/js/quiz-data.js net::ERR_ABORTED 404 (Not Found)` が出ていた。原因は、前 increment（Stage 3-b・quiz-domain-split）で `js/quiz-data.js` を `js/quiz/{aws,pm,quality,architecture}-quiz-data.js` の 4 葉モジュールへ分割した際、**`main.js` の import と `package.json` の lint スクリプトは更新したが、`index.html` の `<link rel="modulepreload" href="./js/quiz-data.js">` の参照先更新を漏らした**ことである。削除済みファイルへの preload が、毎回のページロードで 404 を出していた。

これは私の漏れである。当時「`index.html` は元 zip と byte-identical だから非破壊」と判断したが、その `index.html` がまさに削除対象ファイルを参照していたため、byte-identical を保つこと自体が dangling reference を生む誤りだった。**分割では、import / lint だけでなく、リソースヒント（modulepreload）/ Service Worker プリキャッシュ等の全参照面を同時に更新せねばならない。**

是正：`index.html` の modulepreload を 5 モジュール（`pure-utils` ＋ quiz 4）へ更新。dangling 参照を全件 grep し、実体の 404 源は `index.html:429` のみであることを確認した（workflow の `LINT_TARGET` は `js/**/*.js` glob で問題なし、`main.js` の 3 コメントは Stage 3 の正確な歴史記述ゆえ温存、`sw.js` は AIO ファイルのみ傍受で quiz-data 参照なし）。

## 2. Wicle CSP エラーの根本修正

`Connecting to 'https://cdn.wicle.io/.../experiment/config.json' violates ... connect-src ...` というエラーは、KARTE Action（Wicle）のエッジスクリプトが実験 config を `cdn.wicle.io` から fetch するが、CSP `connect-src` に当該ホストが無くブロックされていたもの。KARTE 公式 CSP ガイド（`support.karte.io/post/1wOX42rWNCMpyOeROWsiqV`）は `*.karte.io` の許可を案内するが、オーナーの CSP は個別サブドメインを列挙する厳格方針のため、それに合わせ `connect-src` に `https://cdn.wicle.io` を追加した。`script-src` のインラインハッシュ（Check 7b/7c が検証する suppressor / speculation rules）は connect-src 変更で不変であり、Check は緑を維持した。

## 3. ESLint v10 移行（リサーチの実適用・依頼 c の中核）

前 increment で「v10 は flat config のため移行は低リスク」と述べていた。確認で止めず、これを適用した。

- **実在検証:** npm レジストリで eslint `latest=10.4.1`（`maintenance` dist-tag が 9.39.4）、`@eslint/js` は 10.0.1（独立 versioning）、engines.node 要件 `^20.19.0 || ^22.13.0 || >=24` を確認。
- **適用:** `eslint` 9.39.4 → 10.4.1・`@eslint/js` 9.39.4 → 10.0.1（exact pin・lock atomic 更新・7 パッケージ削除で依存ツリー軽量化・脆弱性 0）。`engines.node` を v10 要件へ更新。`eslint.config.mjs` のヘッダ版数表記・v10 bump の非破壊記録・stale な `js/quiz-data.js` lint 対象コメントを 4 モジュールへ是正。
- **非破壊の実証:** v10 で lint した結果、**0 errors / 120 warnings（no-var:64 / curly:46 / no-shadow:10）が bump 前と完全一致**。flat config は元から flat config のため設定変更不要だった。

## 4. トータルチェックの改善＝再発防止の機械強制（依頼 b）

discover → document → systematize の原則に従い、今回の事故クラスと移行 footgun を機械強制へ落とした。

- **Check 53（modulepreload 参照解決・BLOCKING）:** `index.html` の全 `<link rel="modulepreload" href>` がリポジトリ実体ファイルへ解決することを検証（same-origin 相対のみ・絶対 URL はスコープ外）。§1 の 404 クラスを systematize。否定テストで `./js/DELETED-MODULE.js` 注入時に ERROR（exit 1）発火を確認。
- **Check 54（eslint ↔ @eslint/js メジャー一致・BLOCKING）:** `package.json` の両 devDep が同一メジャーであることを検証（メジャーのみ比較）。ESLint v10 の既知 footgun（メジャー不一致で解決衝突）を防止。否定テストで `@eslint/js` を 9 系に下げると ERROR（exit 1）発火を確認。
- 両者とも docstring インベントリ ＋ `# ── N.` セクション見出し ＋ 実装の 3 箇所を Check 45 準拠で同時追記。Check 45a/b/c が「1..54」で緑であることを確認。Check 50 の説明文の「ESLint 9.x flat config」を「flat config（9.x 既定・現在 v10）」へ更新（check ロジックは version-agnostic ゆえ不変）。

## 5. リサーチの三分類（apply / verify / defer）——確認で止めない

依頼 c「リサーチ結果の全適用」に対し、各リサーチ事項を三分類して必ず反映した（`research-application-policy.md` §3）。

- **適用（apply）:** ESLint v10 移行（§3）。
- **適用不要だが検証済み（verify）:** robots.txt の granular AI-bot モデル・Node 24・CSP / Trusted Types が 2026 標準に現行であること（過去 increment で検証済み・本 increment で再確認）。
- **適用保留（defer・理由必須）:**
  - **AIPREF `Content-Usage`:** 適用しない。理由は「draft だから」ではなく**戦略不整合**である。robots.txt を精読すると、本リポジトリは Tier 3 で学習ボットを意図的に許可し「public experiment intended to be learned from by AI models」と宣言している（最大許可方針）。AIPREF は本質的に利用を**制限**する機構であり、restriction を permissive な現物へ足すのは既定の言い直し（無益）か許可意図との矛盾になる。
  - **WCAG 2.2 / Core Web Vitals:** target size 24×24・focus appearance・CLS/LCP 是正等は保留。`style.css` / render 変更を要し、Playwright 視覚回帰 baseline 未取得では非破壊性を機械的に証明できない（**安全ゲート**）。baseline 取得後に着手する。

この「リサーチは全適用までがリサーチ（遠足は家に帰るまでが遠足）」「確認だけで止めない」「『リサーチするか？』と問わない」という規律を、メモリ（参照は関連性依存で漏れ得る）だけに頼らず、`research-application-policy.md` ＋ `CLAUDE.md` §0 MANDATORY にも明文化した。

## 6. 検証結果と非破壊の証明

`npm ci` 再現性・脆弱性 0。`npm run verify` exit 0：**54 checks**（Check 52 のみ ADVISORY・他 BLOCKING）・"all invariants hold"・AIO digest passed・binary passed・Stylelint PASS・ESLint **0 errors / 120 warnings** 不変。consistency `OK:` 120 / 全体 122。Playwright 18 tests（baseline 未取得のため実行は CI dispatch 待ち）。

**byte-identity 証明:** 不変であるべき 20 ファイル（AIO 正本層 `llms*` / `AI2AI.md` / `.well-known/*` / `sitemap.xml` / `robots.txt`、binary WebP / MP3、`style.css`、`main.js`、保護 JS `aio-guard` / `error-suppressor` / `theme-init` / `karte-init` / `sw`）すべてが元 zip と SHA-256 で IDENTICAL ＝ digest 再生成不要。`index.html` は console 修正（modulepreload 5 化 ＋ connect-src に cdn.wicle.io）のみ変更し、`ai:version`(v74) / `ai:last-modified` は不変（version bump せず＝v74 内 hygiene・Check 1/2/3/17 緑）。

## 7. Not possible（捏造禁止）

GitHub Actions workflow の実 dispatch / Playwright baseline PNG の実生成（サンドボックスは Chromium DL 遮断・Actions dispatch→PR→人間 merge が唯一の正規ルート）/ 公開 Pages への実反映 / `confirmed_citation_events` の計上（現時点 0・先行ゆえの未観測）/ WCAG 2.2 の CSS 是正（baseline ゲート）/ AIPREF 適用（戦略不整合）。これらは現時点で実行・観測できないため、できたと偽らない。

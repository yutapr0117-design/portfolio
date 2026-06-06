# improvement-notes-claude-v80-phase2-dependency-modernization-and-flat-config

```
Author        : Claude (implementation), under Yuta Yokoi (横井雄太) orchestration
Track         : v80+ staged major update (Phase 2)
Increment     : dependency modernization (ESLint 8.x→9.x flat config, Stylelint 17, Playwright 1.60, GitHub Actions, Node 24) + Check 50 + modulepreload, informed by unrestricted external research
Date          : 2026-06-06
Canonical-Ref : AI2AI.md (canonical) / docs/architecture/repository-maintainability-map.md
Status        : 適用済み（npm run verify フル緑・50 checks・all invariants hold・AIO 正本層と binary は byte-identical・digest 再生成不要・npm ci 再現性 0 脆弱性）
```

> **正本階層:** `AI2AI.md` が canonical、`llms-full.txt` が ground truth。本ファイルは increment 単位の改善記録（incident artifact）であり、上位文書と矛盾する場合は上位を正とする。本ファイルは「Claude 視点の改善文書」として、コミット後のリポジトリを対象に、本セッションで外部調査を判断材料として適用した改善と、調査・解析で発見した事項を重要度の区別なく収録する。事実と推測を分離し、適用済み・未適用・本人判断事項・観測待ちを明示する。

---

## 0. この increment の発端

依頼は「CI もコンソールエラーも無い最新コミットの現物に対する完全完璧トータルチェックと、見つけた改善すべての適用」であり、リサーチが有効化された意図は「リポジトリ／ポートフォリオの改善に繋がる役立つ調査すべての適用」であった。オーナーの明示方針は、(1) 既存を非破壊なら積極適用してよい（商用ではなく個人プロダクトで、一時的なダウンも許容しアジャイルを高速で回す）、(2) Playwright baseline 取得の実準備を完了させる、(3) 外部調査のスコープは限定しない、である。

本 increment はこれを受け、まず外部調査（2026-06 時点のツール EOL/非推奨・AIO 標準動向・セキュリティ最新化）を起動し、その結果を判断材料として、現物を解析しながら非破壊で適用できる改善をすべて適用した。

---

## 1. 結論（BLUF）

現物の出発点は前回 lint-hygiene increment の成果が反映済みの状態であった（49 checks・0 errors / 120 warnings）。本 increment では、外部調査が最も緊急と判定した **ESLint 8.57.1（2024-10-05 EOL・セキュリティパッチ無し）からの脱却**を中核に、検証層（CI/dev-tooling）と公開面の改善を非破壊で適用した。具体的には、ESLint 9.39.4 への移行と flat config 化、Stylelint 17.12.0・Playwright 1.60.0 への bump、GitHub Actions 全 action のメジャー bump と Node 20→24（20 は 2026-04-30 EOL）、公開面の modulepreload 追加、そして flat config 移行の不変条件を守る Check 50 の新設である。

公開サイトは dependency-free Vanilla JS であり dev-tooling に一切依存しないため、ツール群の bump は公開サイトの挙動を 1 ビットも変えない。ESLint 移行の非破壊性は「移行前後の lint 出力が 0 errors / 120 warnings・ルール別内訳まで差分ゼロで完全一致」することで機械的に証明した。`npm run verify` は exit 0、50 checks all invariants hold、AIO 正本層・binary は byte-identical（digest 再生成不要）、`npm ci` 再現性・脆弱性 0 を確認した。

Playwright baseline 取得の実準備は、現物の `update-playwright-snapshots.yml` が既に dispatch→PR→人間 merge の全機構を備えていることを確認し、今回の bump で各 action と Node を最新化して整合を取った。残る操作は GitHub Actions 上での dispatch と PR merge（サンドボックス外でしか実行できない人間の一手）のみである。

---

## 2. 外部調査の結論と現物への適用判断

調査は 12 領域（ESLint/Stylelint/Playwright/GitHub Actions/Node/llms.txt/AI クローラー制御/JSON-LD/GitHub Pages セキュリティヘッダ/Core Web Vitals/リソースヒント/WCAG/View Transitions/Service Worker）を対象とした。各領域の結論と、現物への適用可否を以下に整理する。

### 2.1 適用した（非破壊で現物を改善できると判断）

**ESLint 8.x EOL（最緊急）。** 調査により、ESLint 8.x 系は 2024-10-05 に EOL に達し以後セキュリティパッチが提供されないこと、9.x は flat config がデフォルトで `--no-eslintrc`/`--env` 等の旧 CLI フラグを削除済みであること、10.x（2026-02）は eslintrc を完全削除したことが判明した。現物は 8.57.1 をピンし、しかも CI の「vacuous-gate 対策」が旧フラグへの依存を前提に組まれていた。本 increment は 9.39.4（maintenance LTS・flat config デフォルトかつ移行が検証可能）へ移行した。10.x への即時移行は eslintrc 完全削除でリスクが上がるため見送り、9.x で flat config を確立する段階的経路を取った（これも調査が支持する安全な移行経路）。

**Node 20 EOL。** 調査により Node 20 が 2026-04-30 EOL、Node 24 が Active LTS（Krypton、EOL 2028-04-30）であることが判明。全 workflow の Node ピンを 20→24 へ更新した。

**GitHub Actions の版数遅れ。** 調査により setup-node v6・create-pull-request v8・checkout v6・upload-artifact v5 が最新であることが判明。現物は各 1 メジャー以上遅れていたため一括 bump した。

**Stylelint メジャー遅れ。** 17.x が最新メジャー（CommonJS Node API 削除・Node<20.19 切り）であることが判明。現物の runner は subprocess 方式で削除 API に非依存のため、17.12.0 へ bump しても非破壊であることを同一 CSS での結果一致（14 warnings/0 errors）で確認した。

**Playwright の版数遅れと baseline 好機。** 1.60.0 が最新であることが判明。Playwright の bump はブラウザ更新で baseline PNG を無効化しうるが、現物は baseline 0 件のため無効化対象が存在せず、今が bump の好機であると判断し適用した。

**modulepreload（公開面・調査唯一の未実装項目）。** 調査は ESM SPA の entry とその依存に modulepreload を推奨。現物は main.js を `type="module"` で読むが modulepreload は無かった。main.js の ESM 葉モジュール 2 つ（`./js/pure-utils.js`・`./js/quiz-data.js`）に modulepreload を追加した（並列先読みで起動・INP に寄与、挙動不変、CSP `script-src 'self'` 準拠）。

### 2.2 適用不要（現物に既に実装済み＝オーナーの AIO 設計が 2026 ベストプラクティス水準）

解析の結果、調査が推奨する公開面・AIO 改善の大半は現物に既に実装されていた。これは前回までのセッションとオーナーの設計が既に最新水準にあることを意味する。

- **referrer メタ** — `<meta name="referrer" content="strict-origin-when-cross-origin">` 実装済み。
- **リソースヒント** — preconnect/dns-prefetch（fonts）、preload（フォント・LCP 画像に `fetchpriority="high"`）実装済み。
- **Trusted Types CSP** — `require-trusted-types-for 'script'` と `trusted-types default` 実装済み。調査が「2026 に Safari 26.0・Firefox 148 で全エンジン対応した」と報告する機能を先取りしている。
- **speculation rules** — `<script type="speculationrules">` 実装済み（CSP に content hash 登録済み）。
- **JSON-LD @graph/@id** — 調査が「2026 最重要」とする「単一 @graph ＋ 安定 @id でエンティティ相互参照」を完全実装（Person→worksFor→Organization、WebSite/WebPage/ImageObject/AudioObject/TechArticle/BreadcrumbList/FAQPage の 10 ノードが @id で相互参照）。Check 49 が worksFor↔Organization の宙吊り防止を機械強制。
- **AI クローラー三分類モデル** — robots.txt が OAI-SearchBot/Claude-SearchBot/ChatGPT-User/Claude-User/GPTBot/ClaudeBot/Google-Extended/Applebot-Extended/PerplexityBot/CCBot 等を分類制御。調査が推奨する training/search/user の per-category 制御を既に実装。
- **WCAG/View Transitions/Service Worker** — SPA の focus 管理・ARIA live・baseline-skip guard・versioned cache 等、調査の推奨事項と整合。

これらは AIO 正本層・digest 対象・保護領域に属するか、既に最適化済みのため、本 increment では変更しない（非破壊・スコープ規律）。

### 2.3 調査の留意点（事実と推測の分離）

調査結果のうち、以下はベンダー記事由来で一次情報の裏付けが弱いため、現物への適用判断には用いなかった。第一に、llms.txt の有効性。調査は「~30 万ドメイン分析で AI 引用との統計的有意な相関なし」「Google の Illyes が非対応を明言」と報告した。ただし現物の llms.txt は AIO 正本層（digest 対象・off-limits）であり、かつオーナーの AIO 全振りは「先行ゆえに測定がこれから」という合理的・高勝率のレーン選択である（confirmed_citation_events=0 を賭けの勝敗不明と解釈してはならない）。したがって llms.txt の調査結果は「人間採用担当への明示フレーミングで実際はプラスに働いた」という本件固有の事実と分離し、現物の戦略変更には用いない。第二に、Core Web Vitals 2026 の閾値厳格化（LCP 2.0s 等）。調査自身が「SEO ブログ由来で Google 一次情報ではない」と注記しており、適用判断に用いない。

---

## 3. ESLint flat config 移行の詳細（非破壊証明の中核）

本 increment で最も注意を要した作業であるため、判断推移を詳述する。

### 3.1 真値 baseline の確定

移行の非破壊性は「移行前の lint 出力と移行後の出力が完全一致すること」で証明する。そのため、まず別環境に ESLint 8.57.1 をインストールし、現物に対する真値を確定した。真値は **0 errors / 120 warnings**（no-var:64 / curly:46 / no-shadow:10、すべて main.js）であった。

### 3.2 flat config の等価変換

`@eslint/migrate-config` で雛形を生成したが、雛形には 2 つの問題があった。第一に `...globals.browser`（数百個の超集合）を展開する点。no-undef の検出は参照可能なグローバル集合に依存するため、超集合へ広げると no-undef 挙動が変わり非破壊性が崩れうる。第二に `defineConfig`（`eslint/config` の新指標）への依存。そこで雛形を破棄し、現物の `.eslintrc.json` の env/parserOptions/rules/globals/overrides を 1:1 で手移植した `eslint.config.mjs` を自作した。env:browser 相当は `globals.browser` で供給しつつ、旧設定が明示していた追加グローバル（crypto/trustedTypes/TrustedHTML 等）を温存し、リポジトリのコメント密度方針に従って各設定の意図を詳細注記した。

### 3.3 1 件の差分とその解消

初回検証で flat config は 121 warnings となり、真値 120 と 1 件だけ差異が出た。差異は `sw.js 1:1 Unused eslint-disable directive (no-implicit-globals)` であった。原因は、ESLint 9.x が `reportUnusedDisableDirectives` のデフォルトを `"warn"` に変更したこと、かつ env:browser 供給で no-implicit-globals が発火しなくなり sw.js 先頭の意図的な `/* eslint-disable no-implicit-globals */` が「未使用」と判定されたことである。8.x はこの未使用検出をデフォルトで警告化していなかった。非破壊（件数一致）を保つため、flat config に `linterOptions: { reportUnusedDisableDirectives: 'off' }` を追加して 8.x 相当へ戻した。sw.js の当該 disable はサービスワーカーのトップレベル関数宣言を意図的に許容する self-documenting なディレクティブであり、削除すると文脈が失われるため、ディレクティブ側は温存し設定側で吸収する判断を取った。これにより flat config は真値と差分ゼロで完全一致した。

### 3.4 周辺機構の更新

flat config 化に伴い、`package.json` の lint スクリプトから旧フラグ（`--no-eslintrc`/`--config .eslintrc.json`/`--env`）を除去し、devDeps を eslint 9.39.4・@eslint/js 9.39.4・globals 16.5.0 へ更新（厳密ピン）、`architecture-validation.yml` の lint step を flat-config 化（vacuous-gate 判定 exit≥2/errors>0=BLOCKING は不変）、末尾の `.eslintrc.json` JSON parse 検査を `eslint.config.mjs` の `node --check` へ置換、旧 `.eslintrc.json` を削除した。Check 38（lockfile 整合）・Check 46（lint 被覆 8 ファイル）はいずれも緑を維持した。

---

## 4. Check 50 新設（discover→systematize）

flat config 移行で守るべき新しい不変条件を機械強制チェックとして固定した。これはオーナーの規律（発見した運用ルールは手動修正で終わらせず必ず machine-enforced check にする）の実践である。

前回セッションでは Check 50 追加を「fragile 化・cascade コスト」を理由に見送った。今回は、EOL リンタへの逆戻りや vacuous-gate 再発という実害の大きさが cascade コストを上回ると判断し、追加に踏み切った。Check 50 は 3 サブチェックから成る。(50a) `eslint.config.mjs` が root に存在すること（消すと ESLint 9.x が無設定で vacuous pass する）、(50b) `package.json` の `lint` が旧 eslintrc 系フラグを含まないこと（残ると exit 2＝歴史的な vacuous-gate 失敗モード）、(50c) 旧 `.eslintrc.json` が不在であること（残置は EOL 形式への逆戻りを招く）。Check 45（自己整合）が docstring↔実装の 1..50 一致を BLOCKING で検査するため、docstring インベントリと `# ── N.` 見出しを同時更新し、追加後に 1..50 一致が緑であることを確認した。

---

## 5. 実行コマンドと結果（すべて exit 0）

- `npm ci`（lockfile 厳密復元）— 234 packages、脆弱性 0
- ESLint 8.57.1 真値取得（別環境）— 0 errors / 120 warnings（no-var:64/curly:46/no-shadow:10）
- flat config lint — 真値と差分ゼロで完全一致（0 errors / 120 warnings）
- Stylelint 16.10.0 → 17.12.0 同一 CSS 比較 — 完全同一（14 warnings/0 errors、PASS）
- Playwright 1.60.0 — 18 tests 検出・spec 構文 OK
- `node --check eslint.config.mjs` — ESM 構文 OK
- `npm run lint:js` — 全 8 ファイル OK
- `python3 .github/scripts/check_repository_consistency.py` — 50 checks・107 OK 行・all invariants hold（Check 45 自己整合 1..50・Check 50a/b/c 緑）
- `npm run verify` — exit 0（50 checks・AIO digest passed・binary passed・Stylelint PASS・ESLint 0 errors / 120 warnings）

---

## 6. ESLint 警告数（不変）

| ルール | before | after |
|---|---:|---:|
| `curly` | 46 | 46 |
| `no-var` | 64 | 64 |
| `no-shadow` | 10 | 10 |
| **合計** | **120** | **120** |

本 increment は lint ルールの構成（rules/overrides/globals）を等価移行しただけで、警告数・内訳は 1 件も変えていない（flat config の非破壊性の帰結）。lint 残債（保護領域内 curly・全 no-var・全 no-shadow）の段階解消は、引き続き Playwright baseline 取得後の候補である（前 increment の extraction-map §3.4 記録を継承）。

---

## 7. AIO digest 変更有無

なし。AIO 正本層（`llms.txt`/`llms-full.txt`/`llms_well-known.txt`/`.well-known/*`/`AI2AI.md` 本文）・binary（WebP/MP3）はいずれも 1 バイトも変更していない。digest 計算対象は source_of_truth（llms*/AI2AI.md/binary 2 点）等であり、`index.html` は digest 非対象であることを `check_aio_digests.py` の実装で確認済み。したがって `index.html` への modulepreload 追加も digest 再生成を要しない。`check_aio_digests.py`・`check_binary_aio_metadata.py` はいずれも passed。

---

## 8. Playwright baseline 取得の実準備（依頼: 準備完了）

現物の `update-playwright-snapshots.yml` を精読し、baseline 取得の全機構が既に実装済みであることを確認した。`workflow_dispatch` 手動起動、`npx playwright install --with-deps chromium`、`PLAYWRIGHT_UPDATE_SNAPSHOTS=1` による spec の skip 回避と初回 baseline 生成、PNG 0 件時の BLOCKING ゲート（空 artifact 誤 upload 防止）、`peter-evans/create-pull-request@v8` による PR 自動作成、CWE-094 対策（reason を env 経由で渡しシェル注入を防ぐ）が揃っている。spec 側の baseline 生成分岐も健全で、Playwright 1.60 で構文有効、Check 29（workflow↔spec env 結合）・Check 48（PR 権限結合）も成立する。

本 increment の bump で checkout/setup-node/create-pull-request/upload-artifact と Node 24 が最新化され、Playwright 1.60 との整合も取れた。**残る操作は GitHub Actions 上でこの workflow を dispatch し、生成された baseline PNG の PR を review・merge することのみ**である。これはサンドボックスが Chromium ダウンロードを遮断するため構造的に人間/CI の領分であり、workflow 側の準備としては完了している。

---

## 9. Stage 4 / 5 に関する判断

本 increment は Stage 4/5 の物理分割には進んでいない。dependency modernization と検証層・公開面の非破壊改善に閉じている。Stage 5（render/router/view-transition 抽出）は baseline 未取得のため安全弁を維持。ただし §8 のとおり baseline 取得の実準備は完了したため、人間が dispatch→merge を実行すれば Stage 5 が解錠される状態に前進した。

---

## 10. 発見事項の棚卸し（重要度区別なし）

- **ESLint 10.x への将来移行。** 10.x は eslintrc を完全削除済み。本 increment は 9.x で flat config を確立したため、10.x への移行は「9.x flat config がそのまま動くか検証 → devDeps bump」という小さな増分で将来実施可能。9.x は 2026-08-06 EOL のため、それまでに 10.x 移行を別 increment で行うのが望ましい（次セッション候補）。
- **§9 OK 行数の pre-existing drift を是正。** runbook §9 の consistency OK 行は表記上 103 だったが、`check` コマンド行は 104 を指しており、本 increment 前から 1 件の内部 drift があった。Check 50 の +3 と合わせ、実測の 107（check 全体 109）へ是正した。runbook 自身のルール「§9 を権威値とし実測に同期」に従った。
- **個人連絡先 email（本人判断事項・前 increment から継承）。** `main.js` の Contact 初期データに本人 email が存在する。既存の意図的な公開連絡先であり本人判断事項のため触らない（前 increment の記録を継承）。
- **lint 残債の baseline 後候補。** 保護領域内 curly 36・全 no-var 64・全 no-shadow 10 は baseline 取得後の段階解消候補（前 increment extraction-map §3.4 を継承）。本 increment では構成移行のみで件数を変えていない。

---

## 11. 残課題（次の AI への引継ぎ）

最優先で人間の協力を要する単一アクションは、Playwright baseline の取得（`update-playwright-snapshots.yml` を dispatch し PR を merge）である。準備は完了しており、これが Stage 4/5 を解錠する律速点である。

次点は ESLint 10.x への移行（9.x は 2026-08-06 EOL）。本 increment で flat config を確立済みのため小さな増分で可能。

運用規律として、依存ツールを bump したら package.json を厳密ピンに保ち lockfile を同期し `npm ci` 再現性と脆弱性 0 を確認すること、Check 数を増やしたら全正典文書の Check 数・OK 行数を同一変更内で同期すること（数値ドリフト防止）、append-only 履歴は書き換えないこと。これらは本 increment で実践し、runbook §9・maintainability-map changelog に記録済みである。

本 increment は AIO 全振り戦略・人格・経歴・所属・AIO 文脈を一般化・中和していない。「AI-generated website」「Vibe Coding」と記述していない。React/Tailwind 方向への回帰もしていない。SEO への方針転換もしていない。confirmed_citation_events=0 を「賭けの勝敗が不明」とは解釈していない（AIO 全振りは合理的・高勝率のレーン選択であり、未観測は先行ゆえの当然）。

# improvement-notes-claude-v80-phase2-baseline-gate-doc-hardening

```
Author        : Claude (implementation), under Yuta Yokoi (横井雄太) orchestration
Track         : v80+ staged major update (Phase 2)
Increment     : baseline-gate-doc-hardening (Check 51 = Playwright baseline 生成版数 ↔ pin 整合の機械強制 / Stage 4 危険度別ゲートの明文化 = extraction-map §3.5 / 公開反映観測の強化 = freshness observer --markdown + freshness-review §6 / 検証層・文書のドリフト是正)
Date          : 2026-06-07
Canonical-Ref : AI2AI.md (canonical) / docs/architecture/repository-maintainability-map.md
Status        : 適用済み（npm run verify フル緑・51 checks・all invariants hold・AIO 正本層と binary は byte-identical・digest 再生成不要・npm ci 再現性 0 脆弱性・ESLint 0 errors / 120 warnings 不変）
```

> **正本階層:** `AI2AI.md` が canonical、`llms-full.txt` が ground truth。本ファイルは increment 単位の改善記録（incident artifact）であり、上位文書と矛盾する場合は上位を正とする。本ファイルは「Claude 視点の改善文書」として、コミット後のリポジトリを対象に、本セッションで適用した改善と、解析で発見した事項を重要度の区別なく収録する。事実と推測を分離し、適用済み・未適用・本人判断事項・観測待ちを明示する。

---

## 0. この increment の発端

依頼は二部構成であった。(A) 受領した最新コミット ZIP 現物に対し、`プロンプト.md` と `改善文書.md` に挙げられた改善項目をすべて、非破壊・非競合の範囲で適用すること。(B) それに加えて、Claude 自身が現物の網羅的解析で発見した改善項目を、重要度の区別なくすべて適用すること。オーナーの明示方針は、(1) 受領 ZIP 現物を最上位のソース・オブ・トゥルースとして扱う、(2) 既存を壊さず・競合させない範囲で積極適用してよい（個人プロダクトでありアジャイルを高速で回す、一時的なダウンは許容）、(3) AIO 正本層・binary・`main.js` の保護領域は許可なく不変、(4) 納品は変更ファイルのみ＋配置のアルファベット順＋コミット手順とコミット名＋判断の要約、である。

`プロンプト.md` / `改善文書.md` は、改善候補として案A（公開反映観測の強化）・案B（ESLint warning の低リスク削減）・案C（Stage 4 前ゲートの文書硬化）・案D（Playwright baseline 運用の固定）を提示していた。本 increment はこれらと、Claude 独自発見の検証層・文書ドリフト是正を統合して適用した。

---

## 1. 結論（BLUF）

現物の出発点は、直前の dependency-modernization increment の成果が反映済みの状態であった（50 checks・ESLint 9.x flat config・0 errors / 120 warnings・`@playwright/test` 1.60.0 / `eslint` 9.39.4 / `stylelint` 17.12.0）。本 increment はここに、(i) Claude が発見した運用事故クラスのドリフト 1 件（active runbook の baseline 生成手順が Playwright 1.55.1 を名指ししていたが現 pin は 1.60.0）を是正し、その一致を恒久化する **Check 51** を新設、(ii) §9 実測表の内部ドリフト（OK 行 106/107 の食い違い）を実測値へ是正、(iii) maintainability-map の Phase 2-A dev-deps スナップショットが現行 lock 実体に対し陳腐化していた点を superseded バナーで明示、(iv) 案C/D として Stage 4 候補の危険度別ゲート **extraction-map §3.5** を新設、(v) 案A として公開反映 observer に `--markdown` モードを追加し freshness-review に観測テンプレと新観測ログを追記、した。

案B（ESLint warning の低リスク削減）は、**コード変更を伴わない**結論に至った。これは案Bのスキップではなく、リポジトリ自身が確立済みの安全順序に従った結果である（§3 で詳述）。

非破壊性の核：`main.js`・`style.css`・`index.html`・AIO 正本層（`llms*` / `AI2AI.md` / `.well-known/*` / digest / `sitemap.xml` / `robots.txt`）・binary はいずれも 1 バイトも変更していない。よって digest 再生成は不要。`npm run verify` は exit 0（**51 checks**・all invariants hold・AIO digest passed・binary metadata passed・Stylelint PASS・ESLint **0 errors / 120 warnings**）、`npm ci` 再現性・脆弱性 0 を確認した。本 increment が触れたのは検証層（`check_repository_consistency.py` / `check_public_deployment_freshness.py`）・アーキテクチャ文書層（`total-check-runbook.md` / `main-js-extraction-map.md` / `repository-maintainability-map.md`）・証跡層（`public-deployment-freshness-review.md`）に閉じる。

---

## 2. 依頼A（プロンプト.md / 改善文書.md）の各案への対応

### 2.1 案A — 公開反映観測の強化（適用）

`改善文書.md` 案A／`プロンプト.md` P1 は、公開反映の鮮度観測を「記録しやすく」し、freshness-review に観測テンプレ・分類補強・rollback 禁止強化を求めていた。これを次の二つで適用した。

第一に、`check_public_deployment_freshness.py` に `--markdown` 出力モードを追加した。これは観測結果を、freshness-review §6 の観測ログへそのまま貼り付けられる Markdown ブロック（観測表＋notes＋rollback 禁止リマインダ）として出力する。設計上の不変条件として、stdlib のみ・常に exit 0（非ブロッキング契約は不変）・既存の `--json` と既定テキストモードは完全後方互換とした。重要なのは、canary を presence boolean（`True`/`False`）としてのみ出力し、トークンリテラルを複製しないことである。これにより観測ログが canary の「第二の公開コピー」になることを防ぐ。Check 44 が依拠する唯一のリテラル定義（スクリプト L61）は不変であり、`grep -c` でリテラル出現が 1 のままであることを確認した。

第二に、`public-deployment-freshness-review.md` に、(a) §3 で observer の `--json`／`--markdown` モードを明記、(b) §6 冒頭に再現可能な観測テンプレ（dated `###` 見出し／observed classification と権威ある理由／ソース・オブ・トゥルースの記録事実／`npm run verify` 結果の 4 点と、stale/unobservable は記録するが actioned しない旨）、(c) §6 先頭に 2026-06-07 の新観測ログ（HTTP 403 Forbidden ＝ `unobservable`、`--markdown` 出力を verbatim でコードフェンス収録、verify 緑記録、newest-first）を追記した。

観測そのものの結果は、この検証環境の egress allowlist が `*.github.io` への outbound を遮断するため `unobservable`（HTTP 403）であった。これは現物の不備ではなく環境制約であり、§0/§1/§5 の通り rollback の理由にはならない。観測の事実性（403 という HTTP 層の理由）を記録した。

### 2.2 案B — ESLint warning の低リスク削減（コード変更なし＝安全順序に従った結論）

`改善文書.md` 案B／`プロンプト.md` P1 項目 5–8 は、`curly`・`prefer-const`・`no-var` を低リスク領域から段階削減することを推奨し、同時に項目 12–14 で「一括 `--fix`」「`no-shadow` の機械改名」「AIDK kernel 周辺の `no-var` 機械置換」を禁止していた。

現物の `main-js-extraction-map.md` §3.4 を精読した結果、案Bの安全に実施可能な部分は**前の lint-hygiene increment で既に完了している**ことが確認できた。具体的には、safe-zone の `curly` 71 件はブレース付与済み、`prefer-const` 1 件（`taskFilter`）は解消済みで、194→120 warnings まで削減されている。残る 120 warnings の内訳は `curly`:46 / `no-var`:64 / `no-shadow`:10 で、§3.4 はこれらを次のように明示的に分類している。残 `curly`:46 ＝ safe-zone 未処理 12 件（Router の `startViewTransition` フロー近傍など View Transition / ErrorBoundary のタイミング依存に隣接する保守的除外分）＋ 保護領域内 36 件（AIDK kernel / modules、P0-4 不可侵で Check 43 が byte-identity を BLOCKING で強制）。`no-var`:64 と `no-shadow`:10 は全件「baseline 後」。

したがって、今 `main.js` に追加の warning 削減を行うことは、(a) 保護領域に触れて Check 43 の byte-identity を破る（＝禁止事項違反）か、(b) baseline ゲート対象のタイミング依存隣接コードに触れて「baseline 前に大規模 trivial diff を作らない」というオーナー方針・絶対制約・禁止 11/12・`改善文書.md` §6.2 の禁止に違反するか、のいずれかになる。安全に削れる低リスク件はゼロである。よって本 increment は `main.js` を 1 バイトも触らない。これは案Bの放棄ではなく、リポジトリ自身が確立した安全順序（§3.4）に従った結論であり、残余 warning の削減は Playwright 視覚回帰 baseline 取得後に §3.5 のゲートに従って行うべきものである。

この判断は、`curly` 整形が「挙動不変」であることと矛盾しない。確かに `curly` は構文のみで実行時挙動を変えないが、視覚回帰 baseline が無い状態では「挙動を変えていないこと」を機械的に裏付ける手段が console-error / hash-routing 等の E2E アサーション 18 件に限られ、保護領域や View Transition 近傍の微細な回帰を捕捉できない保証がない。オーナーが保守スコープ優先で「baseline 前は触らない」と決めている以上、その順序を尊重するのが非破壊・非競合の条件に最も忠実である。

### 2.3 案C — Stage 4 前ゲートの文書硬化（適用）

`改善文書.md` 案C／`プロンプト.md` P1 は、Stage 4 に進む前に「触ってよい/いけない箇所」を明文化し、main.js 段階抽出の安全境界を文書側で固めることを求めていた。これを `main-js-extraction-map.md` の新サブセクション **§3.5** として適用した。

§3.5 は、Stage 4 候補を 6 軸（状態保持・副作用・永続化・DOM 自動更新・タイミング依存・保護領域該当）で危険度別に 3 層へ固定する。低〜中層（Toast 表示専用部・DiagnosticsRail 表示専用部・Theme 純粋設定部・BGM データ定義部・ContactCTA 等の独立コンポーネント）、中〜高層（Safe Storage・Store・State Management・Theme/BGM の localStorage 連動部・Meta Management）、高・後回し層（Router・RouteState Proxy・EffectRails・BindingRegistry・ActionDelegator・Main Renderer・Mobile drawer/focus trap・ErrorBoundary・AIDK Kernel）である。各層に「Playwright baseline 取得前に着手してよいか」を二値で対応づけ、低〜中層であっても「挙動・DOM 出力・CSP 連動を 1 ビットも変えない」「保護領域を byte-identical に保つ」「表示専用部を localStorage/state 連動の兄弟コードからクリーンに分離できる」の 3 条件を**すべて**満たす場合に限り「条件付き可」とし、分離できなければ中〜高層へ格上げして baseline 後へ送ることを明記した。これは Stage 2/3 で `clear(node)`／`Storage`／`SITE_CONFIG` の抽出可否を判断したのと同じ軸（§3.3）である。

### 2.4 案D — Playwright baseline 運用の固定（適用）

`改善文書.md` 案D／`プロンプト.md` P1 は、`update-playwright-snapshots.yml` の手順と PR レビュー導線を文書に反映し、baseline 無しでの Stage 5 着手を禁止する明示を求めていた。これを次の二つで適用した。

第一に、§3.5 の末尾に「Playwright baseline 取得状況」欄を新設し、現時点で未取得であること、取得経路は GitHub Actions の "Update Playwright Baseline Snapshots" を人間が dispatch → 生成 PR をレビュー → merge する経路が唯一の正規ルートであること（ローカル/サンドボックスは Chromium DL が egress で遮断され `npm run test:e2e` が起動しないため）、生成は pin（1.60.0）で行い CI の比較版と一致させること、その版一致を Check 51 が機械強制すること、merge 後は取得状況を更新すること、を記録した。さらに「Stage 5 ゲート（再掲）」として、baseline PNG が commit されるまで render/router/view-transition/AIDK Kernel 抽出に着手しない旨を再確認した。

第二に、後述の Claude 発見 B として、active runbook の baseline 生成手順が誤った Playwright 版数を名指ししていたドリフトを是正し、これを Check 51 で恒久化した（案Dの「運用の固定」を、文書記述だけでなく機械強制まで引き上げた）。

---

## 3. 依頼B（Claude 独自発見）の各項目

### 3.1 発見B-1（最重要・実害あり） — active runbook の Playwright 版数ドリフト

`total-check-runbook.md` §7.4 が、baseline PNG の生成を「Playwright 1.55.1 で行う」と名指ししていた。しかし現物の pin（`package.json` の `@playwright/test` および `package-lock.json`）は 1.60.0 である（dependency-modernization increment で 1.49.1→1.55.1→1.60.0 と bump 済み）。baseline 生成 workflow（`update-playwright-snapshots.yml`）は `npm ci` で pin 版（1.60.0）を復元して生成する。したがって runbook の記述に従って 1.55.1 で生成すると、CI の比較版（1.60.0）との間でブラウザ描画差により内容同一でも偽の視覚差分が出る。これは運用事故クラスの bug である。

是正として、§7.4 の版数記述を 1.60.0 に直し、「CI と生成版がずれると偽の視覚差分が出るため版の一致はクリティカルである」旨と、「過去 decision 記録に残る 1.55.1 は append-only な歴史であり遡及修正しない」旨を明記した。さらに、この一致を一度限りの手修正で終わらせず恒久化するため、Check 51 を新設した（§3.4）。

### 3.2 発見B-2 — §9 実測表の内部ドリフト

`total-check-runbook.md` §9（実測表＝実測値を正とする規約）が、consistency 検査の `OK:` 行を「106」と記載する一方、同 §9 内の `npm run check` 全体の行は「109（consistency 107 ＋ binary 2）」と内部参照しており、106 と 107 が食い違っていた。実測すると Check 51 追加前で consistency `OK:` 行は 107、追加後は 108 である。dependency-modernization increment が 106→107 の片側だけを直し損ねた残存ドリフトと判断した。

是正として、Check 51 込みの実測値へ同期した。consistency `OK:` 行 106→**108**、`npm run check` 全体 109→**110**、Check 総数 50→**51**。あわせて §0.1「50 個」→「51 個」、§3 Layer 2 表「107/合計 109」→「108/合計 110」も同期した。実測は `python3 .github/scripts/check_repository_consistency.py | grep -c "^OK:"` ＝ 108、`npm run check | grep -c "^OK:"` ＝ 110 で確認した。

### 3.3 発見B-3 — maintainability-map dev-deps スナップショットの陳腐化

`repository-maintainability-map.md` Phase 2-A の「結果（現状）」が、dev-deps 版数を `@playwright/test` 1.55.1 / `eslint` 8.57.1 / `stylelint` 16.10.0 と現在形で記載し、§94 は「`@playwright/test 1.60.0` は採用していない」と明記し、Phase 2-B §104 は「flat config 移行は deferred」と記していた。しかしこれらはすべて、後続の dependency-modernization increment（同ファイル changelog §392–§394）で 1.60.0 / 9.39.4（flat config 移行済み）/ 17.12.0 へ更新済みであり、現行 lock 実体と矛盾していた。§94 自身が「版数は lock の実体に追従する」と宣言しているにもかかわらず、である。

是正として、Phase 2-A dev-deps リスト直後に superseded バナーを 1 つ挿入し、§94・§104 にローカル superseded マーカーを付与した。いずれも歴史記述は append-only で全保持し、現行値（1.60.0 / 9.39.4 / 17.12.0）と changelog §392–§394 へ誘導する形を取った。歴史を書き換えず、誤読だけを防ぐ最小侵襲の是正である。

### 3.4 発見B-1 の恒久化 — Check 51 の新設（BLOCKING）

`check_repository_consistency.py` に Check 51 を追加した。実装は、`total-check-runbook.md` 内の `Playwright[ 　]+(\d+\.\d+\.\d+)` を全抽出し、`package.json` の `@playwright/test` pin と全一致を検証する。版数名指しが無い場合のみ vacuous 成立とするが、その場合も pin を読めること自体は要求する。対象は active runbook のみであり、decision 記録・extraction-map 等の歴史層は対象外（過去の事実を保持するため）。docstring インベントリと `# ── N.` セクション見出しを Check 45 準拠で同時追記し、1..51 の連番・bijection が緑であることを確認した。否定テストとして、runbook を未是正（1.55.1）の状態で Check 51 が「['1.55.1'] が pin '1.60.0' と不一致」を正しく検出して exit 1 すること、是正後に exit 0 に戻ることを確認した。

この Check は「discover→systematize」の原則（発見した運用規律はリポジトリに文書化し、`check_repository_consistency.py` で BLOCKING に機械強制し、一度限りの手修正で終わらせない）に従ったものであり、Check 44–50 と同じ思想に連なる。

---

## 4. 非破壊性の証明（per-increment 必須）

本 increment は次を満たすことを機械的に確認した。

保護領域の不変：`main.js`・`style.css`・`index.html` は 1 バイトも変更していない（差分なし）。AIO 正本層（`llms-full.txt` / `llms.txt` ＋ 3 alias / `AI2AI.md` / `.well-known/*` / digest 各種 / `sitemap.xml` / `robots.txt` の本文）と binary（webp / mp3）も byte-identical。よって `update_aio_digests.py` の実行は不要であり、digest 連鎖は不変。canary トークン（`SAKURA-AIO-PROVENANCE-CANARY-2026-A7F3C9E1`）は published 面・monitor 面ともに不変で、Check 44 緑。

検証の緑：`npm run verify` exit 0。内訳は consistency check passed（all invariants hold・Check 1..51）、AIO digest check passed、Binary AIO metadata check passed、Stylelint PASS、ESLint **0 errors / 120 warnings**（内訳 `curly`:46 / `no-var`:64 / `no-shadow`:10 で前 increment から不変）、全 `node --check` 通過。`npm ci --ignore-scripts` は脆弱性 0 でロックファイルを厳密復元。

lint 件数同期義務：本 increment は warning 件数を変えていない（`main.js` 不変）ため、`total-check-runbook` / `repository-maintainability-map` / `main-js-extraction-map` の lint 件数記述（120 / `curly`:46 / `no-var`:64 / `no-shadow`:10）は更新不要であり、現状の記述と実測が一致していることを確認した。

---

## 5. コミット後リポジトリ向け改善カタログ（前方視・重要度区別なし）

ここからは、本 increment の解析過程で認識した、コミット後のリポジトリに対する改善候補を、適用済みと区別して、重要度の区別なく収録する。いずれも事実と推測を分離し、本人判断・観測待ち・baseline ゲートの別を明示する。

### 5.1 追跡ファイル総数の文書値がドリフト源である（機械強制を推奨・本人判断）

`total-check-runbook.md` §9 は「追跡ファイル総数」を数値（現状「76」）で記載しているが、これは機械強制されておらず、increment ごとに手で同期する運用になっている。現物の作業ツリーで実ファイルを数えると（`node_modules` / `.git` / `__pycache__` 等を除く）これより多く、ドリフトしている可能性が高い。本 increment はこの値を**手で書き換えなかった**。理由は二つある。第一に、`git ls-files` が使える正規の git コンテキストでないと「追跡ファイル」の権威ある計数ができず、ZIP 展開物で代用した数値を断定的に書くと別種の不正確を生む。第二に、リポジトリの哲学（発見した不変条件は機械強制する）に照らせば、手で数値を bump して再びドリフトさせるより、機械強制するか非数値の表明に切り替えるのが正しい。本 increment では改善文書B（本ファイル）に推奨として記録するに留めた。なお本 increment は追跡ファイルを 1 本（本ファイル）追加するため、権威ある計数値はいずれであれ +1 する。

推奨：将来、`git ls-files | wc -l` を権威ソースとする Check（例 Check 52）を、git コンテキストで動く CI ステップとして追加するか、§9 の当該行を「機械強制された値を参照」する形に変更する。`.gitignore` 対象が作業ツリーに存在しうるため、作業ツリー単純計数を Check 化するのは fragile であり、`git ls-files` ベースが望ましい。これは本人判断事項（採番方針・CI への組み込み可否）を含むため、オーナー承認のうえで別 increment とするのが妥当である。

### 5.2 U-ci（maintainability-map §2）が Check 50/51 を列挙していない（軽微・選択的ガイド）

`repository-maintainability-map.md` の U-ci（検証層変更の更新単位ガイド）は Check 49 までしか言及しておらず、Check 50・51 を含んでいない。本 increment はこれを**触らなかった**。U-ci は網羅列挙ではなく選択的ガイドであり（前 increment も Check 50 を §1 検証層セルにのみ追記し U-ci には追記しなかった）、その既存の扱いに倣ったためである。ただし将来、U-ci を「検証層を変更する際に想起すべき不変条件の完全な索引」として運用したいのであれば、Check 50/51 を含める一貫した方針を別途決めるべきである。これは本人判断事項（U-ci の役割定義）である。

### 5.3 extraction-map のサブセクション・アンカー順が論理順と一致していない（軽微・体裁）

`main-js-extraction-map.md` §3 のサブセクションは §3.3 → §3.4 → §3.5 → §3.1 → §3.2 という順序で並んでおり、番号順と物理順が一致していない（本 increment の §3.5 もこの既存順を踏襲して §3.4 直後に置いた）。Check 45 はこのファイルを対象としないため整合上の問題はないが、可読性の観点では、将来サブセクション番号を物理順に振り直すか、明示的に「番号は追加順、物理配置は論理順」と注記するのが望ましい。本 increment はスコープ規律（構造が収束したら止める）に従い触らなかった。

### 5.4 baseline ゲート群（最重要・観測/人手待ち）

最大の前進は、人間による Playwright baseline の取得（GitHub Actions dispatch→PR→merge）である。これが完了すると、(a) extraction-map §3.5 の中〜高層・高層の抽出（Stage 4/5）が安全に着手可能になり、(b) §3.4 が baseline 後候補とした残 warning（safe-zone 未処理 12・保護領域内 36・全 `no-var` 64・全 `no-shadow` 10）の削減が視覚回帰の裏付けの下で可能になり、(c) `main.js` の `SITE_CONFIG.VERSION` bump（UI 描画に出る）が baseline coverage を伴って解禁される。本 increment は baseline 取得の文書・機械強制の準備（§3.5 取得状況欄・Check 51 の版数整合）を完了させた。残るのはサンドボックス外でしか実行できない人間の一手である。これは観測待ち・人手待ちであり、AI 側で前倒しできない。

### 5.5 AIO 戦略の現状（事実の記録・捏造禁止）

`confirmed_citation_events` は現時点 0 件である。これは早期ポジショニングの反映であって戦略的失敗ではない（AIO は標準化前であり、個人でも先行者利益・機械可読な権威形成の余地がある構造的に合理的な高期待値レーン選択）。一方、Zenn 記事⑨（Bot Governance 分類編）は、AIO の `confirmed_citation_events` とは別カテゴリの人間コミュニティ・トラクション（はてなブックマーク人気エントリー・TechFeed）を確認済みである。本 increment はこれらの数値・事実を 1 つも変えておらず、観測されていない引用イベントを捏造しない。AIO 正本層を触らない以上、公開面の期待値も前エントリから不変である。

---

## 6. Not possible / 本 increment で意図的に行わなかったこと（捏造禁止）

次は、原理的に AI 側で実行できないか、または安全順序・スコープ規律により意図的に見送った。

Playwright baseline の実生成と公開 Pages への実反映、`confirmed_citation_events` の計上は、いずれも人間・CI・外部の領分であり、AI 側で実行も捏造もしない。

案B の `main.js` への追加 warning 削減は、§2.2 の通り、安全に削れる低リスク件がゼロ（残余は保護領域内＝Check 43 byte-identity 違反、または baseline ゲート対象のタイミング依存隣接＝オーナー方針違反）のため見送った。安全部分は前 lint-hygiene increment で実施済みである。

追跡ファイル総数の手動 bump（§5.1）、U-ci の Check 50/51 追記（§5.2）、extraction-map サブセクション番号の振り直し（§5.3）は、それぞれ機械強制が望ましい・選択的ガイドの役割定義が本人判断・スコープ規律により、本 increment では適用せず推奨として記録した。

AIO 正本層・binary・digest の変更は、本 increment が引用対象テキストを 1 バイトも変えないため不要であり、行えば「AIO content が変わった」という偽シグナルになるため行わない。

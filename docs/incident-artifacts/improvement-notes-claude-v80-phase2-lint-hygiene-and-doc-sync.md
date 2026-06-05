# improvement-notes-claude-v80-phase2-lint-hygiene-and-doc-sync

```
Author        : Claude (implementation), under Yuta Yokoi (横井雄太) orchestration
Track         : v80+ staged major update (Phase 2)
Increment     : lint-hygiene (safe-zone curly + prefer-const) + warning-count doc sync + public-freshness reason reconciliation
Date          : 2026-06-05
Canonical-Ref : AI2AI.md (canonical) / docs/architecture/repository-maintainability-map.md
Status        : 適用済み（npm run verify フル緑・49 checks・all invariants hold・AIO 正本層と binary は byte-identical・digest 再生成不要）
```

> **正本階層:** `AI2AI.md` が canonical、`llms-full.txt` が ground truth。本ファイルは increment 単位の改善記録（incident artifact）であり、上位文書と矛盾する場合は上位を正とする。本ファイルは「Claude 視点の改善文書」として、コミット後のリポジトリを対象に、本セッションで発見した改善項目を重要度の区別なく収録する。実施済みの項目と、未実施だが将来処理可能な候補（特に Playwright baseline 取得後に解錠されるもの）を、事実と推測を分離して記録する。

---

## 0. この文書の position と読み方

この文書には二つの役割がある。第一は、本 increment で実際に適用した非破壊改善（safe-zone `curly` のブレース付与、`prefer-const` の解消、警告数の文書同期、public-freshness 観測理由の現物同期）の判断推移と検証チェーンを残すこと。第二は、解析の過程で発見した「今回は着手していないが、競合せず非破壊で処理しうる改善項目」を、baseline 依存性や保護領域との関係とともに棚卸しし、後続 AI とオーナーが優先順位を判断できる材料を提供することである。

本 increment の方針はオーナー横井雄太の明示指示により**保守スコープ優先**であった。すなわち、正本はリポジトリ現物であり、Playwright visual regression baseline PNG が未取得である以上、baseline 前に大規模な trivial diff を作る判断は避ける。`curly` は構文のみで挙動不変だが、それでも safe-zone の全 83 件ではなく 71 件に絞り、残りは baseline 後候補として明記する——この線引き自体が本 increment の設計判断の核心である。

---

## 1. 結論（BLUF）

本 increment は、`main.js` の ADVISORY lint 負債を挙動不変のまま 194 warnings から 120 warnings へ削減し（74 件削減）、その削減に伴って stale 化する 3 つのアーキテクチャ文書の警告数参照を同一変更内で同期し、さらに参考資料（外部ハンドオフ文書）と現物実測が食い違っていた public-freshness の観測理由を現物優先で解消した。コード変更は `main.js` の 71 行（safe-zone `curly`）＋ `prefer-const` 1 件（説明コメント込みで +2 行）に閉じ、保護領域（AIDK kernel／AIDK modules／known benign suppressor／innerHTML interceptor）は 6 ブロックすべて原本と byte-identical であることを逐行照合で証明した。AIO 正本層・binary・`index.html`・`style.css` は 1 バイトも変更しておらず、digest 再生成は不要。`npm run verify` は exit 0、49 checks all invariants hold。Stage 5 へは進んでいない。

---

## 2. 解析サマリ（現物と参考資料の照合）

### 2.1 現物実測値は参考資料の主張と一致

`portfolio-main.zip` を唯一の正本として展開し、参考資料（`プロンプト.md` ＝ `フ_ロンフ_ト.md`、`改善文書.md`）の主張値を現物で全数照合した。行数（`main.js` 6,353 / `js/pure-utils.js` 277 / `js/quiz-data.js` 1,406 / `index.html` 1,248 / `style.css` 2,156 / `check_repository_consistency.py` 1,754 ほか）はいずれも一致。`npm ci --ignore-scripts` は脆弱性 0、`npm run verify` は exit 0、`check_repository_consistency.py` は 49 checks・104 OK 行で all invariants hold、Playwright test list は 18 tests、ESLint は 0 errors / 194 warnings（内訳 `curly`:119 / `no-var`:64 / `no-shadow`:10 / `prefer-const`:1、すべて `main.js`、抽出 2 モジュールは 0 problems）。これらは参考資料の記述と完全に整合した。

### 2.2 Playwright baseline は現物に存在しない（確定事実）

`*.png`・`*-snapshots/` ディレクトリ・platform snapshot（`*-linux.png` 等）を全て探索し、baseline PNG が 0 件であることを確定した。これは `プロンプト.md` の最重要前提（Stage 5 禁止・baseline 未取得）を現物で裏付ける。`update-playwright-snapshots.yml` は Chromium install → baseline 生成 → PNG ゼロ件 hard fail → artifact upload → `peter-evans/create-pull-request@v6` による PR 化まで実装済みだが、その PR を人間がマージする最後の一手が未完了であるため baseline が存在しない。したがって本 increment でも Stage 5 へは進まない。

### 2.3 参考資料と現物の乖離点（現物優先で解消・記録）

解析中に、参考資料の記述が現物の実測・現物内正典文書と食い違う点を 2 つ発見した。いずれも現物優先原則で扱った。

第一に、**public-freshness の観測理由**。参考資料（`プロンプト.md` / `改善文書.md`）は `unobservable` の理由を「temporary DNS failure」と記述しているが、現物の `check_public_deployment_freshness.py` を本環境で実行した実測は「HTTP 403 Forbidden（egress allowlist が `*.github.io` への outbound を許可しない）」であった。さらに現物内の `docs/evidence/public-deployment-freshness-review.md` の 2026-06-02 エントリ自身も「egress allowlist によるブロック」と記録しており、現物正典文書のほうが正確であった。本 increment では同 review 文書の §6 に 2026-06-05 エントリを newest-first で追加し、観測理由を HTTP 403（egress allowlist）として固定し、「DNS failure」表記を上書きした。分類カテゴリは両者とも `unobservable` で同一であり、これは rollback 理由ではなく観測ログに残す対象である点を明記した。

第二に、**ディレクトリ数**。参考資料は「ディレクトリ数 13」と記述しているが、現物実測は 14（`.git`・`node_modules` を含む全体）、git 追跡相当では 12（`.well-known/agent-skills` を含む）である。この「13」は参考資料にのみ現れる値であり、現物の正典文書（runbook §9 等）はディレクトリ数を現状値として参照していないため、実害はない。参考資料側の stale な数値として記録するに留める（現物は変更しない）。

---

## 3. 実施した非破壊改善（A 群：今回適用）

### 3.1 safe-zone `curly` のブレース付与（71 件）

`curly` は単文の if/else/for/while 本体に波括弧を付与する是正であり、実行時の挙動・DOM 出力・CSP 連動を 1 ビットも変えない。これは extraction-map §3.1 が列挙する「Stage 0 で許可される操作」の (3)（挙動を 1 ビットも変えない範囲の ESLint 指摘解消）に該当する。

**保護領域の byte-identical を機械的に保証する適用方式。** ファイル全体への `eslint --fix` 一括適用は AIDK kernel 行を書き換えうる。kernel には終端を示す機械可読マーカーが無いため（extraction-map §3.2 の構造的事実）、行範囲で保護するしかない。そこで次の決定論的手順を取った。第一に、`curly` 専用ルールだけを有効にした `eslint --fix` を原本の別コピーへ適用した。第二に、原本と fix 済みの差分行を抽出した。ここで重要なのは、ESLint の `curly` fix が同一行ブレース化（`if (x) return;` → `if (x) {return;}`）で**行数を変えない**ことである（実測 6,353 行 → 6,353 行）。行数が不変なら行番号がズレず、行番号ベースの選択適用が決定論的に成立する。第三に、各差分行が保護領域に属するかを行番号で判定した。保護領域は次の 6 ブロックである。

1. AIDK Isolated Kernel（DO NOT EDIT ヘッダ箱・View Transition proxy・Trusted Types `'default'` policy・`h()` helper のセキュリティ境界を含む範囲）
2. AIDK modules（RouteState / EffectRails / BindingRegistry / ActionDelegator / DiagnosticsRail / Toast）
3. Router の `startViewTransition` フロー（ErrorBoundary 近傍）
4. known benign error suppressor
5. AIDK Kernel modules init
6. `Element.prototype.innerHTML` setter インターセプタ（DOM clobbering 防止）

第四に、safe-zone（上記いずれにも属さない）の差分行のみを原本へ採用し、保護領域は原本のまま温存した。適用後、保護領域 6 ブロックを原本と逐行照合し、全ブロックが byte-identical であることを証明した。総変更行数は 71（safe-zone `curly` のみ）であった。

### 3.2 `prefer-const` の解消（1 件）

`taskFilter`（Task App コンポーネントの外に保持される UI ステート）を `let` から `const` へ変更した。全参照を grep し、束縛自体が再代入されず（`taskFilter = ...` の形が宣言以外に存在しない）、`.q` / `.priority` のプロパティ変異のみであることを確認した。プロパティ変異は `const` と両立するため、`const` 化は挙動不変である。判断根拠（再代入なし・プロパティ変異のみ）を説明コメントとして明文化した（+2 行）。これにより `prefer-const` 負債は 1 → 0 となった。

### 3.3 警告数の文書同期（194 → 120）

警告を削減した以上、現物の自己整合性哲学（discover→document→systematize）に従い、「194」を現状値として参照する全文書を同一変更内で同期した。これは本 increment で最も注意を要した作業である。なぜなら、警告数はコードの BLOCKING check には一切ハードコードされていない（grep で確認済み）一方、複数のアーキテクチャ文書が「現在の lint 状態」を表す正典値として「194」を参照しているからである。同期しなければ、リポジトリ自身の自己整合性ナラティブが drift する。

同期にあたっては、**最終状態と履歴を混同しない**原則を厳守した。「199→194」という遷移は Stage 2/3 抽出 increment の事実であり、これは保持したうえで、新たに「194→120」の遷移を追記する形を取った。具体的な同期箇所は次のとおり。`docs/architecture/total-check-runbook.md` の 4 箇所（lint 期待値テーブル・失敗時対応の advisory 記述・§9 実測 snapshot・既知負債リスト）、`docs/architecture/repository-maintainability-map.md` の 5 箇所（残課題の実測値・BLOCKING 残作業・ADVISORY 可視件数・`--env` 冗長性の実測一致値・触らない方針 2 箇所）、`docs/architecture/main-js-extraction-map.md` の 2 箇所（kernel 内 warning 分布の根拠説明・実測 lint 記述）。

一方、append-only 履歴である `docs/incident-artifacts/` の各 decision record（過去 increment が当時記録した「48 checks」「49 checks」「194 warnings」）と、`repository-maintainability-map.md` L330 の前 increment changelog 行（「lint 199→194」）は、現物の append-only 履歴哲学（「歴史記録と現状値を混同せず、歴史は書き換えない」、`improvement-notes-claude-v80-phase2-domain-authority-worksfor.md` L20 が明示）に従い、一切書き換えなかった。

### 3.4 main.js 行数の live figure 同期（≈6,353 → ≈6,355）

`prefer-const` の説明コメント追加で `main.js` が 6,353 行から 6,355 行になった。check スクリプトは行数を等値判定でハードコードしていない（確認済み・壊れない）が、アーキテクチャ文書は `main.js` を現状値として「≈6,353 行」と記述しているため、live figure を 3 箇所（extraction-map ヘッダ・runbook §9 table・extraction-map §3.2 末尾）で ≈6,355 へ同期した。なお「7,785 → 6,353 行へ 1,432 行減少した」という Stage 2/3 抽出の遷移記述は履歴として保持した。

### 3.5 public-freshness 観測理由の現物同期

§2.3 第一点で述べたとおり、`docs/evidence/public-deployment-freshness-review.md` §6 に 2026-06-05 エントリを追加し、観測理由を HTTP 403（egress allowlist）として記録した。あわせて、本 increment で working-copy の lint が 120 warnings へ移動した事実も同エントリに記録し、freshness review 文書のナラティブをコード変更と同期させた。

### 3.6 increment 記録の整備（systematize）

本 increment 由来の運用規律を、後続 AI が再発見コストを払わずに済むよう明文化した。`main-js-extraction-map.md` に §3.4 を新設し、`curly` 母集団 83 件の内訳・今回処理した 71 件・baseline 後候補の一覧表・「なぜ 83 件全部ではなく 71 件に絞ったか」の設計判断を記録した。`repository-maintainability-map.md` の changelog 表に本 increment の行を append-only で追加した。`total-check-runbook.md` §7.2 には警告数同期の運用ルールを織り込んだ。

---

## 4. 発見した改善候補の棚卸し（B 群：今回未着手・重要度区別なし）

ここからは、解析の過程で発見した改善項目を、実施済み・未実施・baseline 依存・本人判断事項の区別とともに、重要度の区別なく全て記録する。後続 AI とオーナーが優先順位を判断する材料である。

### 4.1 lint 残債（baseline 後に解錠される候補）

本 increment 後、`main.js` には 120 warnings が残る（`curly`:46 / `no-var`:64 / `no-shadow`:10）。これらは次のように分類される。

第一群は **safe-zone `curly` のうち未処理の 12 件**（= 83 − 71）。Router の `startViewTransition` フロー近傍など、行番号上は safe-zone 判定だが View Transition / ErrorBoundary のタイミング依存に隣接するため保守的に除外した分を含む。`curly` は挙動不変だが、視覚回帰 baseline 取得後に視覚差分ゼロを確認しながら処理するのが安全である。

第二群は **保護領域内の `curly` 36 件**（AIDK kernel 2／AIDK modules 27／Router VT flow・suppressor・kernel init 等に分布）。これらは byte-identical 維持のため温存した。kernel 改変を伴うため、AIDK 不可侵（P0-4）に抵触する。kernel 自体の再設計判断とは別軸であり、baseline 後でも慎重を要する。

第三群は **`no-var` 全 64 件**。多くが innerHTML interceptor 等の保護領域に分布し、また巻き上げ（hoisting）・`catch` 引数・loop 変数・古い安全装置（legacy guard）への依存がありうる。一括置換は禁止であり、各箇所のスコープと巻き上げ依存を逐一確認したうえで、baseline 後に局所修正する。

第四群は **`no-shadow` 全 10 件**。内訳は `h`（`h()` helper の上位スコープ衝突、L971 / L1876 / L1883 / L1905）と `init`（L5899 の上位スコープ衝突、L1395 / L1442 / L1585 / L1674 / L1728 / L1755）である。多くが AIDK modules 内にある。変数名変更は意味衝突リスクがあるため、命名の影響範囲を検討したうえで baseline 後に処理する。

### 4.2 警告数のドキュメント同期を機械強制する Check の是非（設計判断・今回は見送り）

本 increment で痛感したのは、警告数が複数文書に分散参照されており、削減のたびに手作業同期が必要になることである。現物の哲学（発見した前提は機械強制へ落とす）に従えば、Check 50 として「runbook §9 の lint baseline 記述が実際の eslint 出力（件数＋ルール別内訳）と一致すること」を BLOCKING で検査する案が考えられる。これは Check 45（チェッカ自身の文書と実装の bijection）・Check 47（import/export の bijection）と同じ「文書と現実の一致を強制する」哲学の、数値計測ドメインへの適用である。

しかし今回は**見送った**。理由は次の三点である。第一に、警告数を機械的に固定する check は fragile になりうる。lint を 1 件減らすたびに check が赤化し、ローカルで eslint を走らせて件数を取得し直して docstring を更新する、というループが BLOCKING で強制されると、保守スコープの小さな改善のたびに摩擦が増える。第二に、`check_repository_consistency.py` への Check 50 追加は、Check 45（自己文書整合・docstring inventory と code section が 1..N で連続一致）も同時に更新する必要を生み、さらに「49 checks → 50 checks」を全文書（runbook §9 の「Check 総数 49」等）で同期する cascade を発生させる。これは保守スコープの本 increment には過大である。第三に、警告数は「現実が動いたら文書を直す」という as-measured 管理で十分機能しており、本 increment ではその運用ルールを明文化（runbook §7.2・extraction-map §3.4）することで systematize の要求を満たした。

ただし、もし将来 lint 削減を頻繁に行うフェーズに入るなら、件数ではなく「抽出 2 モジュール（`js/pure-utils.js` / `js/quiz-data.js`）が 0 warnings であり続けること」を検査する Check のほうが fragile でなく価値が高い。これは「抽出したモジュールを clean に保つ」という本質的な不変条件であり、件数の増減に依存しない。後続 AI への候補として記録する。

### 4.3 main.js の `no-var` 集中ブロック（L6114–L6348）の構造観察

`no-var` の safe-zone 判定で 33 件が L6114–L6348 に集中していることを観察した。この範囲は innerHTML / DOM-clobber interceptor の直後にあり、複数の IIFE-wrapped ブロック（`})();` が L6104 / L6154 / L6234 / L6352 に出現）で構成される末尾セキュリティ層である。これらの `var` は古いブラウザ配慮や巻き上げ依存の可能性があり、今回は `no-var` 自体を後回しにしたため未調査である。baseline 後に `no-var` を扱う際、この末尾ブロックは「保護領域に隣接するセキュリティ層」として特に慎重な分類（巻き上げ・loop・catch・legacy guard の確認）が必要であることを記録する。

### 4.4 個人連絡先 email の存在（本人判断事項・今回は触らない）

`main.js` L513 に本人の連絡先 email（`yuta.pr.0117@gmail.com`）が Contact コンポーネントの初期データとして存在する。これは公開ポートフォリオのコンタクト用に意図的に置かれた値であり、`main.js` のみに存在して `index.html` や `llms.txt` 等の公開 HTML・正本層には露出していない。`プロンプト.md` 制約 #9 は「新たに個人連絡先をコミットすること」を禁じるが、これは既存コミットに元から存在する本人の公開連絡先であり、私が新規に持ち込む混入ではない。これを除去するか維持するかは本人にしか決められない事項（連絡先をどう公開するかは本人の意向）であるため、今回は触らない。発見事項として記録し、本人が将来判断できる材料とする。なお、`SECURITY.md` や `secrets-handling` プロジェクトカードでの「secrets / API key」言及は、秘密情報そのものではなく扱い方の文書であり、混入ではない。実際の API key・トークン・SSH 鍵・個人電話番号の混入は検出されなかった。

### 4.5 バージョン一貫性は健全（観察・変更不要）

`v74` がアプリケーションバージョンとして `sw.js`（`CACHE_NAME = 'portfolio-aio-v74'`）・`.well-known/mcp.json`（`"version": "74.0.0"`）・`index.html`（`ai:version`・タイトル・OG 等）で一貫していることを確認した。Node 版数は 3 つの workflow（`update-playwright-snapshots.yml` / `playwright-regression.yml` / `architecture-validation.yml`）すべてで `'20'` にピンされ一貫している。robots.txt の AI bot 方針（GPTBot / ClaudeBot / PerplexityBot / Google-Extended 等を明示 Allow、Sitemap 自己参照あり）も意図どおりである。これらは変更不要であり、健全性の記録として残す。

### 4.6 Pipeline-Version（v74）と v80+ track の関係（観察・現状ポリシー維持）

`AI2AI.md` のヘッダー日付・Pipeline-Version と本文更新の整合について、`プロンプト.md` P1-5 が「安易に変更しない。必要なら『Pipeline-Version は v74 のまま、v80+ は staged update track』という説明を補助文書へ追記」と指示している。本 increment は `AI2AI.md` を 1 バイトも触っておらず（digest 一致を維持）、v80+ track の各 increment が検証層・文書層に閉じてアプリケーション版数を上げていない現状ポリシーは妥当である。binary asset metadata baseline が v73/2026-04-14、application version が v74 という差（`check_binary_aio_metadata.py` が NOTE として出力）も P0-14 asset baseline policy として意図的であり、維持する。

### 4.7 AIO 正本層・binary・JSON-LD の健全性（観察・変更不要）

`.well-known/aio-manifest.json`（`generated_at: 2026-06-04T22:51:57Z`）の digest は現物実測と一致し、`llms.txt` / `llms_well-known.txt` / `.well-known/llms.txt` / `.well-known/llms_well-known.txt` は byte-identical を維持している。WebP XMP / MP3 ID3 の binary AIO metadata も検証通過。`index.html` の JSON-LD 2 ブロックは valid JSON で、Person.worksFor が同一 @graph 内の Organization（`https://nkgr.co.jp/#organization`）へ解決すること（Check 49）も維持されている。本 increment はこれらを一切変更していないため digest 再生成は不要であり、健全性の記録として残す。

---

## 5. 実行コマンドと結果

本 increment の検証チェーンは次のとおり、すべて exit 0 であった。

- `npm ci --ignore-scripts` — 219 packages、脆弱性 0
- `node --check main.js` — 構文 OK（safe-zone `curly` 適用後・`prefer-const` 適用後）
- `npm run lint` — 0 errors / 120 warnings（`curly`:46 / `no-var`:64 / `no-shadow`:10）
- `npm run lint:css` — Stylelint [style.css]: PASS
- `npm run lint:js` — 全 8 ファイル `node --check` OK
- `npm run check` — `check_repository_consistency.py`（49 checks・104 OK 行・all invariants hold）＋ `check_aio_digests.py`（AIO digest check passed）＋ `check_binary_aio_metadata.py`（Binary AIO metadata check passed）
- `npm run verify` — 上記が順に全 pass・exit 0
- `python3 .github/scripts/check_public_deployment_freshness.py` — exit 0・classification `unobservable`・理由 HTTP 403（egress allowlist）
- 保護領域 6 ブロックの原本逐行照合 — 全ブロック byte-identical
- `npx playwright test --config=playwright.config.cjs --list` — 18 tests（baseline PNG は 0 件で未取得）

---

## 6. ESLint 警告数 before / after

| ルール | before | after | 差分 |
|---|---:|---:|---:|
| `curly` | 119 | 46 | −73（safe-zone 71 件＋抽出時移動分の整理ではなく、今回は safe-zone 71 件の付与。残 46 = 保護領域内 36 ＋ safe-zone 未処理 12 − 重複補正後の実測値）|
| `no-var` | 64 | 64 | 0（後回し）|
| `no-shadow` | 10 | 10 | 0（後回し）|
| `prefer-const` | 1 | 0 | −1 |
| **合計** | **194** | **120** | **−74** |

> 注: `curly` の before 119 のうち safe-zone は 83 件、保護領域内は 36 件。今回 safe-zone 71 件を処理し、safe-zone 未処理 12 件＋保護領域内 36 件＝48 件が残るはずだが、実測 after は 46 件である。この 2 件差は、ESLint の `curly` 集計が同一行に複数の if を含む行（例 L840・L856 が before リストで重複出現）を行単位でなく違反単位で数えるためであり、行ベースの safe-zone 分類（71 行適用）と違反ベースの集計（curly 46）の粒度差に起因する。挙動不変性と保護領域 byte-identity はいずれの粒度でも成立しており、件数の粒度差は負債の質を変えない（事実と集計粒度を分離して記録）。

---

## 7. AIO digest 変更有無

なし。AIO 正本層（`llms.txt` / `llms-full.txt` / `llms_well-known.txt` / `.well-known/*` / `AI2AI.md` 本文）・binary（WebP / MP3）・`index.html` の JSON-LD はいずれも 1 バイトも変更していない。`update_aio_digests.py` の実行は不要であり、実行していない。`check_aio_digests.py` と `check_binary_aio_metadata.py` はいずれも変更前後で passed。

---

## 8. public-freshness 観測結果

`fetch_ok: False` / classification `unobservable` / 理由 **HTTP 403 Forbidden（egress allowlist が `*.github.io` への outbound を許可しない）** / expected Last-Updated `2026-06-02`（working-copy `llms.txt`）/ public Last-Updated `None` / canary expected-public `True`-`None` / exit 0。これは現物不備ではなく観測ログに残す対象であり、rollback 理由ではない。参考資料の「DNS failure」表記は現物実測と異なるため、現物優先で「egress allowlist / 403」を正とし、review 文書 §6 に記録した。

---

## 9. Playwright baseline 状態

baseline PNG は現物に 0 件（未取得）。`update-playwright-snapshots.yml` は PR 化まで実装済みだが、その PR を人間がマージする最後の一手が未完了。baseline 取得の唯一の正規ルートは、サンドボックスが Chromium ダウンロードを遮断するため GitHub Actions の同 workflow を dispatch → PR → 人間 merge することである。baseline 未取得の間、Stage 5（render / router / view-transition の物理分割）には進まない安全弁を維持する。本 increment はこの安全弁を docs で再度明確化した（extraction-map §3.4 の baseline 後候補表）。

---

## 10. Stage 4 / 5 に関する判断

Stage 4（service rails: Storage / Store / EffectRails / BindingRegistry / Toast / Theme / BGM 等）には進んでいない。本 increment は Stage 4 実装ではなく、保守スコープの lint 衛生＋文書同期に閉じている。Stage 4 readiness（候補とリスク・baseline 必要性の分解）は `改善文書.md` Step 5 の表と extraction-map §3 の Stage 表に既に整理されており、本 increment はそれを変更していない。Stage 5 は baseline 未取得のため禁止条件を維持。

---

## 11. 残課題（次の AI への引継ぎ）

最優先で人間の協力を要する単一アクションは、Playwright baseline の取得である。`update-playwright-snapshots.yml` を GitHub Actions 上で 1 回 dispatch し、生成された baseline PNG の PR をレビューして merge すれば、視覚回帰カバレッジと Stage 4/5 の両方が解錠される。これが律速点である。

baseline 取得後に処理可能な lint 候補は §4.1 のとおり、safe-zone `curly` 未処理 12 件 → 保護領域内 `curly` 36 件 → `no-var` 64 件 → `no-shadow` 10 件、の順でリスクが上がる。`no-var` を扱う際は §4.3 の末尾セキュリティ層（L6114–L6348）に特に注意する。

運用規律として、lint を削減したら必ず同一変更内で 3 つのアーキテクチャ文書（runbook / maintainability-map / extraction-map）の警告数・内訳・履歴を同期すること（コードの BLOCKING check には件数をハードコードしない）。public-freshness の `unobservable` 理由は参考資料ではなく現物実測を正とすること。これらは runbook §7.2・extraction-map §3.4 に明文化済みである。

設計候補として、警告数そのものを機械強制するより「抽出 2 モジュールが 0 warnings であり続けること」を検査する Check のほうが fragile でなく価値が高い（§4.2）。Check 50 を追加する場合は Check 45 の自己文書整合と「49→50 checks」の全文書 cascade を伴う点に留意する。

`main.js` L513 の個人連絡先 email（§4.4）は本人判断事項として残置している。本人が公開連絡先の扱いを判断する際の材料とする。

本 increment は AIO 全振り戦略・人格・経歴・所属・AIO 文脈を一般化・中和していない。「AI-generated website」「Vibe Coding」と記述していない。React / Tailwind 方向への回帰もしていない。SEO への方針転換もしていない。confirmed_citation_events=0 を「賭けの勝敗が不明」とは解釈していない（AIO 全振りは合理的・高勝率のレーン選択であり、未観測は先行ゆえの当然）。

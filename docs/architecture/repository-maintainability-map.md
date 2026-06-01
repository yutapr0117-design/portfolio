# repository-maintainability-map.md

```
Last-Updated  : 2026-06-01
Maintained-By : AI agents under Yuta Yokoi (横井雄太) orchestration
Track         : v80+ staged major update (Phase 2 — CI hygiene increment applied)
Canonical-Ref : AI2AI.md (canonical) / llms-full.txt (ground truth)
Status        : Living document — update when layer structure or sync relationships change
```

> **Canonical hierarchy:** `AI2AI.md` is canonical; `llms-full.txt` is ground truth. This map is a subordinate architecture document. On conflict, those win.
> **目的:** 後続AIエージェントが、リポジトリ全体を「壊さず・迷わず」改善できるよう、更新単位・層の関係・同期義務・触ってよい/いけない箇所を1枚に集約する。
> **トータルチェック手順:** 「現物が壊れていないか」を誰でも（人間/AI）再現的に検証する完全な runbook は `docs/architecture/total-check-runbook.md`。コミット衛生（最低限のコミットミス検査）から全レイヤ・実測基準値まで網羅。

---

## 1. 層構造（Layer Model）

| 層 | ファイル | 役割 | 変更時の注意 |
|---|---|---|---|
| **AIO正本層** | `llms-full.txt`（ground truth）, `AI2AI.md`（canonical handoff）, `llms.txt` + 3 alias, `.well-known/aio-manifest.json` | AI crawler / LLM 向けの権威ある真実源と pipeline 引き継ぎ | **C6**: エンティティ/権威текスト・JSON-LDの本文変更はオーケストレーター承認必須。変更後は digest 再生成必須 |
| **アプリ層** | `index.html`, `main.js`, `style.css`, `sw.js`, `aio-guard.js`, `error-suppressor.js`, `karte-init.js`, `theme-init.js` | 公開SPA本体 | **C1/C2/C3**: Vanilla JS / IIFE / ErrorBoundary。外部FW禁止。`main.js` は `main-js-extraction-map.md` 参照 |
| **検証層** | `.github/scripts/check_repository_consistency.py`, `check_aio_digests.py`, `check_binary_aio_metadata.py`, `check_css_stylelint.py`, `aio_monitoring.py`, `update_aio_digests.py`, `e2e/portfolio.spec.js`, `playwright.config.cjs`, `.github/workflows/*` | 整合性・回帰・AIO digest・lint の自動検査 | 検査を緩める変更は要判断。新規 invariant は Check 番号を付けて追記 |
| **証跡層** | `docs/incident-artifacts/`, `docs/session-records/`, `docs/architecture/`, `docs/evidence/`, `Claude2Claude.md`, `ChatGPT2ChatGPT.md` | 意思決定・セッション履歴・実装/解析証跡 | `Claude2Claude.md` / `ChatGPT2ChatGPT.md` / `docs/evidence/*` / `docs/session-records/**` は aio-manifest に SHA 登録済み → 変更後 digest 再生成必須 |
| **バイナリ層** | `yuta-yokoi-ai-pm-orchestration-system.webp`（XMP）, `yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3`（ID3v2.4） | AIO メタデータ埋込済み資産 | **原則変更しない**（v73 asset baseline policy）。再エンコードで XMP/ID3 が消えると `check_binary_aio_metadata.py` が赤化 |
| **配信/設定層** | `robots.txt`, `sitemap.xml`, `.well-known/*`, `.nojekyll`, `.gitattributes`, `jsconfig.json`, `.eslintrc.json`, `.stylelintrc.json`, `googlea7059bedc6fe8bdc.html` | クロール制御・GitHub Pages 配信・lint 設定・GSC | `.gitattributes` の binary 指定はバイナリ層保護に必須。GSC ファイルはトークン1行のみ |
| **入口/運用層** | `CLAUDE.md`（Claude Code 自動読込の入口）, `README.md` | 人間/エージェント向けオリエンテーション | `CLAUDE.md` は AIO discovery 非登録（dev-tooling）。`README.md` も非 digest |

---

## 2. 更新単位（Update Units）

「同時に変えるべきものの束」。1単位 = 1関心事。

- **U-app（アプリ変更）:** `index.html` / `main.js` / `style.css` / `sw.js` 等 → `node --check` + Playwright regression（PR時）。ai:version 系を変える場合は §3 の Version Update Checklist を**原子的に**。
- **U-aio（AIO正本変更）:** `llms-full.txt` / `llms.txt`(+3 alias) / `AI2AI.md` / バイナリ → **digest 再生成必須**（`update_aio_digests.py` → `check_aio_digests.py`）。`AI2AI.md` も同コミットで更新（commit-drift check）。alias 4ファイルは byte-identical 維持。
- **U-doc（証跡追記）:** `docs/**` / `Claude2Claude.md` / `ChatGPT2ChatGPT.md` → manifest 登録分は digest 再生成。Session Record は `AI2AI.md` が正典。
- **U-ci（検証層変更）:** scripts / workflows → `py_compile` + 該当 `node --check`。新 invariant は Check 番号付与。

---

## 3. 変更時に同期すべきファイル（Sync Obligations）

### バージョン bump（オーケストレーター承認時のみ・原子的に）
`AI2AI.md` の **Version Update Checklist** が正典。要点: `AI2AI.md`(Pipeline-Version/Last-Updated) / `index.html`(ai:version/ai:last-modified) / `main.js`(SITE_CONFIG.VERSION/LAST_UPDATED) / `.well-known/mcp.json`(server.version) / `sitemap.xml`(lastmod) / `robots.txt` / `llms*.txt`(+ `.well-known` alias) / `sw.js`(CACHE_NAME=`portfolio-aio-vNN`) / `aio-manifest.json` + `update_aio_digests.py`。

> **注意:** 「v80+」は **track 名であってアプリ版数ではない**。Phase 進行だけでは Pipeline-Version を上げない。`ai:last-modified` / `SITE_CONFIG.LAST_UPDATED` / sitemap root lastmod は相互に一致が必須（Check 17/18）。これらアプリ層の日付と `AI2AI.md`/`llms-full.txt` の Last-Updated（doc 層）は別物。

### digest 同期（AIO/証跡の manifest 登録ファイルを変えたら必ず）
```bash
python3 .github/scripts/update_aio_digests.py
python3 .github/scripts/check_aio_digests.py
```
manifest 登録ファイル: `llms.txt` / `llms-full.txt` / `AI2AI.md` / webp / mp3 / `Claude2Claude.md` / `ChatGPT2ChatGPT.md` / `docs/evidence/ai-pioneer-identity-review.md` / `docs/session-records/AI2AI-archive.md` / `docs/evidence/aio-monitoring-log.json`。

### byte-identity（常時）
`llms.txt` == `.well-known/llms.txt` == `llms_well-known.txt` == `.well-known/llms_well-known.txt`。`.well-known/index.json` == `.well-known/agent-skills/index.json`。

### Session Record 同期（機械強制 — Check 31）
`AI2AI.md` に Session Record を追記したら、**同コミットで `Claude2Claude.md` の 現在状態（最新 Session Record 番号）も更新**する。`check_repository_consistency.py` **Check 31**（BLOCKING）が、`Claude2Claude.md` が `AI2AI.md` の最新 Session Record 番号を参照しているかを検査する（Session Record #17 で導入）。忘れると CI が赤化する。

### honest per-file dating（誤修正防止）
日付は「そのファイルの内容が最後に変わった日」を honest に記す per-file policy。**`llms.txt`（短文）の `Last-Updated` は `llms-full.txt` と一致しなくてよい。** llms.txt の内容を変えていないのに日付だけ進めるのは不正直（= してはいけない）。これは sitemap の per-URL lastmod policy（Check 18: mixed dates は許容・期待される）と同じ思想。`AI2AI.md` ↔ `llms-full.txt` のみ 7日以内同期が要求される（Check 24）。後続AIはこの日付差を「ドリフト」と誤認・誤修正しないこと。

---

## 4. 触ってよい / いけない箇所

**触ってよい（AI SURFACE）:** `main.js` の `AI SURFACE` マーカー内、`PAGE_META`、各 Component render、`docs/**` の追記、検証 invariant の追加。

**触ってはいけない / 要承認:**
- `main.js` の **AIDK Isolated Kernel（"DO NOT EDIT"）** — startViewTransition プロキシ、Trusted Types ポリシー等。
- **C6 AIOテキスト** の本文（承認なし変更禁止）。
- バイナリ層（webp/mp3）の再エンコード。
- `docs/incident-artifacts/update-portfolio.v70-experiment.yml` を `.github/workflows/` へ戻すこと（`workflow_dispatch` を持つため live 化する）。
- KARTE CDN への SRI 付与（C7）。
- フレームワーク/ライブラリの導入・再提案（C1/C4）。

---

## 5. Phase 2 — 進捗と候補

### Phase 2-A: dev依存の中央管理（package.json / lockfile / npm ci） — **完了（適用済み）**

**結果（現状）:** dev tool は `package.json`（`private: true` / `"name": "portfolio-aio"` / `"version": "0.0.0"` / runtime `dependencies` 無し）＋ `package-lock.json`（`lockfileVersion: 3`）で**中央管理済み**。全 dev tool は exact pin:
- `@playwright/test`: **1.55.1**（後述 CI 衛生 increment で 1.49.1 から bump）
- `eslint`: **8.57.1**
- `http-server`: **14.1.1**
- `stylelint`: **16.10.0**

workflow は `npm install --no-save …` / `npm install -D …` の broad install を撤去し、`npm ci` + ローカルバイナリ（`npx playwright` / `eslint` / `stylelint`）へ移行済み。Playwright のブラウザバイナリは引き続き `npx playwright install --with-deps chromium`。`package-lock.json` は `npm install --save-exact` / `npm ci` で生成したもののみコミット（手書き禁止）。

**注:** 旧計画に記載のあった `@playwright/test 1.60.0` は採用していない。実際に lock された baseline は 1.49.1 で、CI 衛生 increment（下記）の `npm audit` 解消のため **1.55.1** へ minor bump した。ドキュメントの版数は lock の実体に追従する（推測の計画値を残さない）。

### Phase 2-B: ESLint ゲートの実効化 — **根本原因は Session #18 で解消済み（残りは lint 負債の解消方針のみ）**

**~~問題（Session #16 で発見）~~ → 解消（Session #18）:** `architecture-validation.yml` の ESLint ステップが実質無効（vacuous）だった根本原因 ―― ①`npm install --no-save eslint`（バージョン無指定 → ESLint 9.x で classic flags `--no-eslintrc`/`--env` が削除済み）、②`|| true` による実行失敗の握り潰し ―― を **Session #18 で両方除去**した。現在は ①ESLint を **8.57.1 に pin**、②**実行失敗（exit≥2）= BLOCKING / lint 検出（exit 1）= ADVISORY（件数を可視化・CI は赤化しない）** に再構成。vacuous PASS は構造的に発生不能。

**残課題（lint 負債そのもの・要判断）— 実測値で更新:** 現行 `.eslintrc.json` は **base ルール（`no-var`/`prefer-const`/`curly`/`no-shadow` 等）を error 級**に置き、`overrides` で **`main.js` のみを `warn`（ADVISORY）に降格**する構成。実測すると `main.js` に **0 errors / 199 warnings**（内訳 `curly`:124 / `no-var`:64 / `no-shadow`:10 / `prefer-const`:1）が残り、それ以外の対象ファイル（`error-suppressor.js` / `karte-init.js` / `theme-init.js` / `aio-guard.js` / `sw.js`）は **error 級ルールでも 0 件**。すなわち負債は **`main.js` に局在**しており、旧記載の「216 errors / `sw.js` top-level / `theme-init.js` の `curly`」は**現物と乖離していたため破棄**（`sw.js`・`theme-init.js` は既に clean）。

- **`sw.js` を `overrides` から除外済み（CI 衛生 increment）:** `sw.js` は warn 級降格が不要なほど clean なため、`.eslintrc.json` overrides 対象を `["main.js"]` のみへ縮小し、`sw.js` を error 級ゲートへ昇格した（clean なので緑のまま、かつ将来の退行を error で捕捉）。
- **BLOCKING 化の残作業は `main.js` のみ:** 199 warnings を解消（`var`→`let/const`、`if` 単文の波括弧、shadow 変数のリネーム）すれば `main.js` も overrides から外せる。ただし **一括整形は禁止**（差分が巨大化し、視覚回帰 baseline 未確立では退行検出不能）。`main-js-extraction-map.md` の Stage 進行に合わせ、論理ブロック単位で段階解消する。
- 代替（flat config 移行＝`eslint.config.js` / ESLint 9 系）は変更量が大きく、現 pin（8.57.1）で十分機能しているため deferred。

**一括修正禁止。** ADVISORY 件数（199）が CI ログに常時表示されるため、負債の増減は可視。`main.js` の BLOCKING 昇格は視覚回帰 baseline 確立後に段階実施するのが安全。

> **補足（vacuous 根本原因は解消済みだが、ローカル検証の限界は残る）:** every-push の BLOCKING パイプライン（`architecture-validation.yml`）はサンドボックスでは GitHub Actions runner 上の `npm ci` 実挙動を検証できない。ローカル `npm ci` 緑は runner 緑を保証しない。CI 衛生 increment（下記）の workflow 変更は YAML 構文・ローカル相当コマンドまで検証済みだが、**実 Actions 緑確認は人間の責務**。

### Phase 2-C 以降: main.js 段階抽出
`main-js-extraction-map.md` 参照。Stage 5（物理分割）は Playwright baseline 確立後。

### CI 衛生 increment #1（v80+ — 適用済み）

Phase 2-A/2-B の土台の上に、**生成物再混入の機械検出・lockfile 整合の機械検出・CI 高速化・baseline 偽成功防止・dev 監査の解消**を追加した。AIO 正本層（`llms-full.txt` / `AI2AI.md` / `llms.txt` + alias / `.well-known/*` / digest / version 文字列）は**一切変更していない**（digest 連鎖を避け「最小・可逆」を維持。pipeline version も据え置き）。よって本 increment は非 digest 層（検証層・配信/設定層・証跡層）に閉じる。

| 項目 | 変更ファイル | 内容 | 種別 |
|---|---|---|---|
| 生成物再混入防止 | `check_repository_consistency.py` | **Check 37**（BLOCKING）: `__pycache__`/`node_modules`/`test-results`/`playwright-report`/`blob-report`/`.pytest_cache`、`*.pyc`/`*.pyo`、`.DS_Store`/`Thumbs.db`/`npm-debug.log` がリポジトリツリーに存在したら赤化。`git ls-files` を権威とし、git 不在環境では prune 付き walk へフォールバック（CI runtime の `node_modules`/`__pycache__` を誤検知しない設計） | BLOCKING |
| lockfile 整合 | `check_repository_consistency.py` | **Check 38**（BLOCKING）: `package.json` と `package-lock.json` の整合（`lockfileVersion==3` / `name`・`version` 一致 / `devDependencies` 完全一致 / `private==true` / runtime `dependencies` 不在） | BLOCKING |
| npm cache | `architecture-validation.yml` / `playwright-regression.yml` / `update-playwright-snapshots.yml` | `actions/setup-node@v4` に `cache: 'npm'` を付与。`architecture-validation.yml` には欠落していた `Setup Node.js` step（`node-version: '20'`）を `npm ci` 前に追加（runner default Node 依存を解消し、両 Playwright workflow の '20' pin と統一） | 非破壊・高速化 |
| baseline 偽成功防止 | `update-playwright-snapshots.yml` | `--update-snapshots` 後に PNG が 1 枚も無ければ赤化する検証 step を追加（`continue-on-error: true` で部分失敗を許容する設計の死角＝空 baseline の silent success を塞ぐ）。`upload-artifact` に `if-no-files-found: error` も付与 | BLOCKING（生成時のみ） |
| dev 監査解消 | `package.json` / `package-lock.json` | `@playwright/test` を 1.49.1→**1.55.1** へ minor bump（GHSA-7mvr-c777-76hp / ブラウザ DL 時の SSL 証明書未検証 high×2 を解消）。`npm audit` = **0 件**。**重要:** 本番配信物は依存ゼロ Vanilla JS であり、この脆弱性は dev 専用ツリー（`npm audit --omit=dev` = 0 件）にのみ存在し、配信物には到達しない。`baseline PNG 未生成の今`が bump の唯一の非破壊窓（後で bump すると人間生成 baseline を無効化し手戻り）だったため、このタイミングで実施 | 非破壊 |
| 陳腐化コメント修正 | `check_css_stylelint.py` | 旧運用の `npm install --no-save stylelint@16` 記述を `package.json / package-lock.json via npm ci`（Phase 2-A）へ修正 | 文書整合 |

**docstring インベントリ:** `check_repository_consistency.py` の冒頭 docstring に Check 37/38 を追記し、「実装と同期」の約束を維持。

**`.eslintrc.json` の `comment` キー不可（実装メモ）:** ESLint の `.eslintrc.json` は JSON スキーマ上コメントキー（`comment` 等）を**拒否**する（`eslint --print-config` が schema 違反で停止）。よって overrides 縮小の根拠は設定ファイル内に書けず、本マップおよび incident artifact 側にのみ記述する。

**Not possible（本 increment では実施不能・捏造禁止）:** GitHub Actions の実実行緑確認 / Playwright baseline PNG の実生成（人間が Actions 経由で生成し `e2e/portfolio.spec.js-snapshots/` へ配置・commit）/ AIO citation の実観測 / C2PA 署名 / Zenn 記事公開日の外部確定。

### CI 衛生 increment #2（v80+ — 本コミットで適用）

increment #1 が確定（CI 緑・コンソールエラーなし）した後のトータルチェックで発見した非破壊改善。#1 と同じく **AIO 正本層（`llms-full.txt` / `AI2AI.md` / `llms*` alias / `.well-known/*` / digest / `sitemap.xml` / `robots.txt` の本文）は一切変更せず**、非 digest 層（検証層・設定層）に閉じる。`main-js-extraction-map.md` は本 increment の対象外（main.js 抽出に変化なし）。

| 項目 | 変更ファイル | 内容 | 種別 |
|---|---|---|---|
| sitemap 整合 | `check_repository_consistency.py` | **Check 39**（BLOCKING）: `sitemap.xml` の全 same-project `<loc>` がリポジトリ内の実ファイルへ解決することを検査（root / 末尾スラッシュ → `index.html`、外部 URL は対象外）。Checks 9/18/34/35/36 がカバーしていなかった「広告 URL ↔ 実体ファイル」の整合を埋め、crawler 404 を防止。現状 17 URL すべて解決 | BLOCKING |
| Dependabot npm | `.github/dependabot.yml` | `github-actions` に加え **`npm` ecosystem** を追加（月次・`ci` prefix・dev-dependencies を 1 PR にグループ化）。Phase 2-A で `package.json`/`package-lock.json` を導入したのに更新検知が無かった保守の穴を塞ぐ。Check 38 が Dependabot の lockfile 同期更新も BLOCKING で検査。公開サイトはランタイム依存ゼロのため dev 専用 | 非破壊・保守性 |
| push race 防止 | `auto-update-aio-digests.yml` / `aio-monitoring.yml` | commit+push する 2 workflow に top-level `concurrency`（`group: ${{ github.workflow }}-${{ github.ref }}` / `cancel-in-progress: false`）を付与。near-simultaneous トリガ時の `git push` 非 fast-forward 衝突（赤化）を直列化で防止。digest はファイル内容の純関数のためキュー実行で最新ツリーに収束 | 障害点除去 |

**docstring インベントリ:** `check_repository_consistency.py` 冒頭 docstring に Check 39 を追記（「実装と同期」を維持）。

**意図的に「やらなかった」こと（observation-only / 要オーケストレーター判断）:**
- **`npm run lint` と `architecture-validation.yml` の `--env browser --env es2022` 重複は削除しない。** `--no-eslintrc --config .eslintrc.json` で `.eslintrc.json` の `env` が読まれるため `--env` は冗長だが、削除しても lint 結果は完全に不変（実測: 0 errors / 199 warnings で一致）。**BLOCKING ゲートを純粋に美観目的で触るのは「最適化でなく障害点除去」「最小・可逆」に反する**ため、観察記録に留める。flat config 移行（将来）で自然解消。
- **PR 検証系 workflow（`architecture-validation` / `playwright-regression`）への `concurrency` 付与は見送る。** これらは commit/push しないため push race は無く、`cancel-in-progress` 付与は純粋なコスト最適化（実行時間短縮）に該当。「最適化でなく障害点除去」の原則に従い churn を避ける。
- **`FORCE_JAVASCRIPT_ACTIONS_TO_NODE24` env は据え置く。** GitHub Actions の Node24 移行に伴う前方互換設定であり、CI 緑の現状で除去する積極理由が無い。

**Not possible（本 increment でも同様・捏造禁止）:** GitHub Actions 実実行緑確認 / Dependabot 実 PR の挙動 / Playwright baseline PNG 実生成 / AIO citation 実観測。

---

## 6. AIO全振り方針（不変・後続AIへの指示）

このリポジトリは SEO を正面突破するものではない。AIO は標準化前であり、個人でも先行者利益・観測・機械可読な権威形成の余地がある。**AIO全振りはセルフブランディング兼 proof-of-work の戦略であり、後続AIは SEO最適化・採用最適化へ方針転換してはならない。** 主戦場は AI crawler / AI search / LLM 解釈。

### Zenn 記事の featuring 方針（Session #18 で確立 — 後続AIへの指示）

掲載対象は **公開全 11 本**（記事削減はしない）。featuring 順は **AIO 効果優先順**で、全レイヤー（`robots.txt` 優先コメント / `index.html` JSON-LD `subjectOf`・`citation` / `main.js` カード配列 / `llms.txt` Co-citation・Fetch Order・Optional / `llms-full.txt` / `README.md`）で同一順序を保つ。

- **PRIMARY = `5d1d7a7438d48d`（Bot Governance 分類編）**。唯一の外部トラクション確認済み（TechFeed 掲載・はてな人気エントリー）であり、`sameAs` / Fetch Order 先頭 / 各リストの最上位を維持する。
- 優先順（curation ではなく ordering で AIO 効果を表現する。全 11 本を載せる）:
  `5d1d7a7438d48d`(分類編/PRIMARY) → `d99f8171bcf275`(実践編) → `3735dc2683f900`(第4弾/バイナリ層) → `c82fe055816454`(Capstone) → `91cf894e1072c6`(AI-to-AI Pipeline) → `27fa4c511cd972`(第6弾/最終回) → `340dbb85491fc8`(第5弾) → `7e18e6ee1577aa`(第2弾) → `931f6e781d91f8`(第1弾) → `49326c5c4e0aae`(第3弾) → `6dad78f20f2505`(総括) ＋ 作者ページ `https://zenn.dev/yuta_yokoi`。
- **シリーズ本編は #1–#6 の 6 本で完結**（#6 が最終回）。#7 は総括、#8/#9/#10/#11 はシリーズ後の発展的独立記事。「全6弾」表記は「本編6本完結＋発展記事を含む計11本」へ更新済み。事実関係（公開順・シリーズ境界）はこの分類に従うこと。
- `index.html` の `sameAs` は同一エンティティ/プロフィール用であり、全記事を列挙しない（PRIMARY 1 本のみ可）。記事の網羅列挙は `subjectOf` / `citation` / `llms*` 側で行う。

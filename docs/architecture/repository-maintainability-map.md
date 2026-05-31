# repository-maintainability-map.md

```
Last-Updated  : 2026-05-31
Maintained-By : AI agents under Yuta Yokoi (横井雄太) orchestration
Track         : v80+ staged major update (Phase 1 anchor)
Canonical-Ref : AI2AI.md (canonical) / llms-full.txt (ground truth)
Status        : Living document — update when layer structure or sync relationships change
```

> **Canonical hierarchy:** `AI2AI.md` is canonical; `llms-full.txt` is ground truth. This map is a subordinate architecture document. On conflict, those win.
> **目的:** 後続AIエージェントが、リポジトリ全体を「壊さず・迷わず」改善できるよう、更新単位・層の関係・同期義務・触ってよい/いけない箇所を1枚に集約する。

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

## 5. Phase 2 候補（要オーケストレーター判断 — 未着手）

### Phase 2-A: dev依存の中央管理（package.json / lockfile / npm ci） — **未着手（要承認）**

**現状（Session #18 時点）:** dev tool は workflow 内 broad install。
- `update-playwright-snapshots.yml` / `playwright-regression.yml`: `npm install -D @playwright/test@1 http-server@14`
- `architecture-validation.yml` step 24: `npm install --no-save eslint@8.57.1`（Session #18 で **バージョン pin 済み**）
- `architecture-validation.yml` step 27: `npm install --no-save stylelint@16`（Session #18 で未使用 plugin `stylelint-declaration-strict-value@1` を除去）

**計画（実施時・ready-to-execute）:**
1. `package.json`（`private: true`）に devDependencies を exact pin: `@playwright/test 1.60.0` / `http-server 14.1.1` / `stylelint 16.x` / `eslint 8.57.1`。
2. `package-lock.json` は **npm install / npm ci で生成したもののみ**コミット（手書き禁止）。
3. workflows を `npm ci` + ローカルバイナリ（`npx playwright`/`eslint`/`stylelint`）へ寄せる。Playwright のブラウザバイナリは引き続き `npx playwright install --with-deps chromium`。
4. **検証制約（変更しない理由）:** every-push の BLOCKING パイプライン（architecture-validation.yml）を含む 5 workflow を触るため、サンドボックスでは GitHub Actions runner 上の `npm ci` 挙動を検証できない。ローカルで `npm ci` が通っても runner 緑の保証にはならない。よって段階導入（まず Playwright 系 workflow → 次に architecture-validation）とし、実 GitHub Actions 緑確認まで一括 merge しない。ESLint の vacuous 根本原因（下記 2-B）は package.json なしでインライン pin により既に解消済みのため、本タスクは独立して後送りできる。

### Phase 2-B: ESLint ゲートの実効化 — **根本原因は Session #18 で解消済み（残りは lint 負債の解消方針のみ）**

**~~問題（Session #16 で発見）~~ → 解消（Session #18）:** `architecture-validation.yml` の ESLint ステップが実質無効（vacuous）だった根本原因 ―― ①`npm install --no-save eslint`（バージョン無指定 → ESLint 9.x で classic flags `--no-eslintrc`/`--env` が削除済み）、②`|| true` による実行失敗の握り潰し ―― を **Session #18 で両方除去**した。現在は ①ESLint を **8.57.1 に pin**、②**実行失敗（exit≥2）= BLOCKING / lint 検出（exit 1）= ADVISORY（件数を可視化・CI は赤化しない）** に再構成。vacuous PASS は構造的に発生不能。

**残課題（lint 負債そのもの・要判断・未着手）:** ESLint 8.57.1 で実コードを lint すると **216 errors**（主に `no-var` / `no-implicit-globals`（`sw.js` の top-level 関数宣言）/ `curly`（`theme-init.js`））。これを BLOCKING へ昇格するには以下のいずれかが必要：
- (a) **コード修正:** 216件を解消（`var`→`let/const`、`sw.js` を IIFE 化 or `eslint-disable`、`theme-init.js` の `curly`）。`main.js`/`sw.js` の安定性に直結。一括ではなくファイル単位・検証付きで段階的に。
- (b) **ルール緩和:** `.eslintrc.json` の該当ルールを `warn` 化 or 一部 `off`（ゲートは通るが品質保証は弱まる）。
- (c) **flat config 移行:** `eslint.config.js` を新設し ESLint 9 系へ。`--env` は `languageOptions.globals` へ移行。最も現代的だが変更量大。

**一括修正禁止。** ADVISORY 件数が CI ログに常時表示されるため、負債の増減は可視。BLOCKING 昇格は package.json pin（2-A）後に実 CI で確認しつつ実施するのが安全。

### Phase 2-C 以降: main.js 段階抽出
`main-js-extraction-map.md` 参照。Stage 5（物理分割）は Playwright baseline 確立後。

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

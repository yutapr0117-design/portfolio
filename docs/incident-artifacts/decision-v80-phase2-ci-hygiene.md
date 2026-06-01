# decision-v80-phase2-ci-hygiene.md

```
Decision-Date : 2026-06-01
Session       : AI2AI.md 未更新（最新は Session Record #19 のまま）。本 increment は
                非 digest 層（検証層・配信/設定層・証跡層）に閉じるため、新規 session
                record / digest 連鎖を作らない。Session #20 は採番しない。
Implementer   : Claude Opus 4.8 (Anthropic) — AI agent
Orchestrator  : Yuta Yokoi (横井雄太, human — sole decision authority)
Track         : v80+ staged major update (Phase 2 — CI hygiene increment)
Pipeline-Ver  : v74 (unchanged — "v80+" はトラック名でありアプリ版数ではない)
Canonical-Ref : AI2AI.md (canonical) / llms-full.txt (ground truth) /
                decision-v80-maintainability-roadmap.md /
                decision-v80-e2e-and-maintainability-stage-1.md
Status        : Applied
```

> **Canonical hierarchy:** `AI2AI.md` is the canonical handoff; `llms-full.txt` is ground truth.
> This decision record is a subordinate incident artifact. If it conflicts with `AI2AI.md` or `llms-full.txt`, those win.

---

## 1. 背景

v74 本体は良好状態（全 consistency check PASS）。`decision-v80-e2e-and-maintainability-stage-1.md` の §3 で **Phase 2 へ延期**とした 2 項目（N-1 ESLint 実効化 / N-2 dev依存の中央管理）は、その後のセッションで実装され、現物では `package.json` / `package-lock.json` / `npm ci` への移行（Phase 2-A）と ESLint ゲートの実効化（Phase 2-B 根本原因解消）が**完了済み**である。

本 increment は、その土台の上に積む **CI 衛生（hygiene）強化**である。大改造ではなく、改善文書 P0/P1/P2 の以下を「最小・可逆・非破壊」で機械化する。

```
P1-01: 生成物（__pycache__ / .pyc / node_modules / Playwright 結果物）再混入の機械検出
P1-02: package.json ↔ package-lock.json 整合の機械検出
P1-03: update-playwright-snapshots.yml の baseline 未生成時 偽成功防止
P1-04: setup-node npm cache 導入による CI 高速化
P1-05: dev依存 npm audit のレビューと最小 bump
P2-01: check_css_stylelint.py の陳腐化コメント修正
P2-02: ESLint advisory の段階解消（clean な sw.js を overrides から除外）
P2-03: repository-maintainability-map.md / main-js-extraction-map.md の Phase 2 追記＋drift 修正
```

**AIO 正本性の維持:** `llms-full.txt` / `AI2AI.md` / `llms.txt` + 3 alias / `.well-known/*` / digest / `SITE_CONFIG.VERSION` は **一切変更していない**。よって `check_aio_digests.py` の再生成は不要（digest 連鎖を起こさないことが「最小・可逆」の維持に直結する）。本 increment の証跡は非 digest 文書（本 artifact ＋ 2 つの architecture map）に置く。

---

## 2. 決定事項

### D-1 (P1-01): 生成物・キャッシュ再混入の BLOCKING 検出（Check 37）

**問題:** `.gitignore` は存在するが、これは予防であり、**追跡済みファイルや ZIP 配布物への混入を機械検出するものではない**。過去に `.github/scripts/__pycache__/*.pyc` が ZIP に含まれた実績がある（`docs/incident-artifacts/` の過去記録参照）。複合解析（`.gitignore` × ZIP 実体）の観点で、再発防止は機械化すべき。

**決定:** `check_repository_consistency.py` に **Check 37（BLOCKING）** を追加。

- 検出対象パス断片: `__pycache__` / `node_modules` / `test-results` / `playwright-report` / `blob-report` / `.pytest_cache`
- 検出対象サフィックス: `.pyc` / `.pyo`
- 検出対象ファイル名: `.DS_Store` / `Thumbs.db` / `npm-debug.log`
- **権威ソース:** `git ls-files -z`（追跡対象のみを列挙）。これにより CI runner 上の runtime 生成物（`npm ci` 後の `node_modules`、Python 実行後の `__pycache__`）を**誤検知しない**。
- **フォールバック:** git 不在環境（ZIP 単体展開など）では prune 付き `os.walk` に切り替え、上記 forbidden ディレクトリを走査前に枝刈りする。

**根拠（コード × CI 事故の回避）:** ナイーブな `os.walk` を権威にすると、CI の every-push パイプライン上で `npm ci` が生成する `node_modules/` を Check 37 自身が検出して**全 PR を赤化**させる。`git ls-files` を権威とし walk をフォールバックに限定することで、「追跡されている混入」だけを正しく捕捉する。否定テスト（追跡された `.pyc` / `node_modules/` 配下 / `.DS_Store` を一時投入）で ERROR 検出を確認し、クリーン復帰で PASS を確認済み。

### D-2 (P1-02): package.json ↔ lockfile 整合の BLOCKING 検出（Check 38）

**問題:** Phase 2-A で `package.json` / `package-lock.json` を導入したが、両者の整合を機械検査していない。手書き lockfile・devDependencies のズレ・runtime 依存の混入を検出できると、`npm ci` 前提の再現性が守られる。

**決定:** `check_repository_consistency.py` に **Check 38（BLOCKING）** を追加。6 サブチェック:

1. `package.json` と `package-lock.json` が両方存在
2. `package-lock.json` の `lockfileVersion == 3`
3. `name` / `version` が両ファイルで一致（`packages[""]` と突合）
4. `package.json.devDependencies` が `package-lock.json.packages[""].devDependencies` と**完全一致**
5. `package.json.private == true`
6. `package.json` に runtime `dependencies` が**存在しない**（公開物が依存ゼロ Vanilla JS であることの機械保証）

**根拠:** 「依存ゼロの Vanilla JS を配信し、dev tool だけを `private` manifest で中央管理する」という Boring Technology の構造そのものを invariant として固定する。docstring インベントリにも Check 37/38 を追記し、「実装と同期」の約束を維持。

### D-3 (P1-03): baseline 未生成時の偽成功防止

**問題:** `update-playwright-snapshots.yml` の `Generate baseline snapshots` は `continue-on-error: true`。これは「部分失敗でも生成済み PNG を拾う」意図だが、死角として **PNG が 1 枚も生成されないのに job が成功扱いになり、人間が空 artifact を掴む**リスクがある（運用手順 × workflow 実効性の不整合）。

**決定:**
- 生成ステップ直後に検証ステップを追加: `find e2e -path '*-snapshots/*.png' -type f` が空なら `::error::` を出して `exit 1`。
- `upload-artifact` に `if-no-files-found: error` を付与（二重防御）。

**根拠:** baseline 生成は main.js 物理分割（Stage 5）の前提。その基盤 workflow が「空でも緑」では信頼できない。なお `playwright-regression.yml` の diff upload は失敗時のみ動く設計なので `if-no-files-found` は付けない（非対称は意図的）。

### D-4 (P1-04): setup-node npm cache 導入＋Node pin 統一

**問題（CI × workflow）:**
- `architecture-validation.yml`: `npm ci` はあるが `Setup Node.js` step が**無く**、runner default Node に依存。cache も無し。
- `playwright-regression.yml` / `update-playwright-snapshots.yml`: `setup-node` はあるが `cache` 無し。

**決定:**
- 3 workflow すべての `actions/setup-node@v4` に `cache: 'npm'`（`package-lock.json` を key にした依存キャッシュ）を付与。
- `architecture-validation.yml` に `Setup Node.js`（`node-version: '20'`）を `npm ci` の前に追加。両 Playwright workflow が既に使う `'20'` pin と統一し、runner default 依存を解消。

**対象外（確認済み）:** `aio-monitoring.yml` / `auto-update-aio-digests.yml` は Python 中心で npm を使わないため cache 対象外で正。

**根拠:** CI 時間短縮と Node ランタイムの決定化。setup-node の npm cache は lockfile の存在を要するが、Phase 2-A で導入済みのため機能する。

### D-5 (P1-05): dev依存 npm audit の解消（Playwright minor bump）

**問題:** dev 依存ツリーに high severity 2 件（いずれも `@playwright/test` < 1.55.1 / ブラウザダウンロード時に SSL 証明書を検証しない、GHSA-7mvr-c777-76hp）。

**決定:** `@playwright/test` を **1.49.1 → 1.55.1** へ exact pin で minor bump。`package-lock.json` は `npm install --save-exact` で再生成（手書きせず）。`npm ci` 再現性・`npm audit`（= 0 件）・`lockfileVersion 3`・`name`/`version` 保持を確認。

**重要な境界（コード × 配信物）:** この脆弱性は **dev 専用ツリーにのみ存在**する（`npm audit --omit=dev` = **0 件**）。公開配信物は依存ゼロの Vanilla JS であり、Playwright はローカル/CI の E2E にしか使われないため、配信物には到達不可。すなわち「本番影響なし・dev リスクのみ」。`npm audit fix --force` は使わず、major 破壊も伴わない最小 bump で解消。

**タイミングの根拠（baseline 生命周期との結合）:** Playwright の bump は視覚回帰 baseline PNG のレンダリングに影響し得る。baseline PNG が**まだ存在しない現時点が、bump の唯一の非破壊窓**である。baseline 確立後に bump すると、人間が生成・コミットした baseline を無効化し手戻りになる。したがって本 increment のタイミングで実施した。**人間が baseline を生成する際は、必ず 1.55.1 で生成すること**（§4 参照）。

### D-6 (P2-01): check_css_stylelint.py の陳腐化コメント修正

旧運用時代のコメント（`npm install --no-save stylelint@16`）を現行運用（`version pinned in package.json / package-lock.json, installed via npm ci`）へ修正。後続 AI の誤解防止。挙動変更なし（コメントのみ）。

### D-7 (P2-02): ESLint overrides の縮小（clean な sw.js を error 級ゲートへ昇格）

**実測:** 現 `.eslintrc.json` は base ルールを error 級に置き、`overrides` で対象を warn 級へ降格する構成。実測すると lint 負債は **`main.js` に局在（0 errors / 199 warnings: `curly`:124 / `no-var`:64 / `no-shadow`:10 / `prefer-const`:1）**。`sw.js` を含むその他の対象ファイルは error 級でも **0 件**。

**決定:** `overrides` の対象を `["sw.js", "main.js"]` から **`["main.js"]` のみ**へ縮小し、`sw.js` を error 級ゲートへ昇格（clean なので緑のまま、将来の退行を error で捕捉）。`main.js` は warn 級のまま据え置き（199 warnings は **一括 fix 禁止** ―― 差分が巨大化し、視覚回帰 baseline 未確立では退行検出不能なため。`main-js-extraction-map.md` の Stage 進行に合わせて段階解消）。

**実装メモ（`.eslintrc.json` に根拠コメントを書けない理由）:** ESLint の `.eslintrc.json` は JSON スキーマ上、`comment` 等のコメントキーを**拒否**する（`eslint --print-config` が schema 違反で停止）。よって overrides 縮小の根拠は設定ファイル内に記述できず、本 artifact と architecture map にのみ記録する。

### D-8 (P2-03): architecture map の Phase 2 追記＋drift 修正

`repository-maintainability-map.md` / `main-js-extraction-map.md` の Section 5 が現物と乖離していたため修正:

- Phase 2-A を「未着手」→「**完了**」へ。計画値 `@playwright/test 1.60.0`（未採用）を実 lock 値 **1.55.1** へ訂正。
- Phase 2-B の「**216 errors** / `sw.js` top-level / `theme-init.js` の `curly`」を、実測「**0 errors / 199 warnings**（`main.js` 局在）」へ訂正。`sw.js`・`theme-init.js` は既に clean。
- 本 increment（Check 37/38・npm cache・audit・偽成功防止・sw.js 昇格・コメント修正）を CI 衛生 increment として追記。

両ファイルとも `Last-Updated` を 2026-06-01 に更新。これらは AIO digest 非登録のため digest 再生成は不要。

---

## 3. 意図的に「やらなかった」こと（要オーケストレーター判断 / 後送り）

### N-1: `main.js` の 199 warnings 解消

一括整形は禁止（C5 のレビュー前提を超える規模の自動変更を避ける／視覚回帰 baseline 未確立で退行検出不能）。`main-js-extraction-map.md` の Stage 進行に合わせ、論理ブロック単位で段階解消する。

### N-2: ESLint flat config 移行（ESLint 9 系 / `eslint.config.js`）

現 pin（8.57.1 + classic `.eslintrc.json`）で十分機能しており、移行は変更量が大きいため deferred。

### N-3: AIO 正本層への記録（digest 連鎖）

本 increment は非 digest 層に閉じる方針のため、`llms-full.txt` / `AI2AI.md` への追記と digest 再生成は**行わない**。これは「最小・可逆」を維持し、CI 衛生という内部改善で AIO 正本の指紋を動かさないための意図的判断。

### N-4: `npm run lint` の `--env browser --env es2022` と `.eslintrc.json` `env` の重複

`package.json` の lint script はフラグで env を渡し、`.eslintrc.json` でも `env` を定義している（重複）。無害（同一設定の冗長指定）であり、挙動に影響しないため**変更せず観察記録のみ**。flat config 移行（N-2）時に自然解消される。

### N-5: `@axe-core/playwright` による a11y 自動検査（改善文書 P3-03）

devDependency 追加・lockfile 更新・E2E 結果確認が必要。Playwright baseline 確立後の方が安全なため deferred。

---

## 4. Not possible と人間の手順

| 項目 | 状態 | 人間の手順 |
|---|---|---|
| 実 CI での workflow 緑確認 | Not possible（本環境は GitHub Actions 不可） | push 後、architecture-validation / playwright-regression / update-playwright-snapshots / aio-monitoring の Actions 結果を確認 |
| Playwright baseline PNG 生成 | Not possible（本環境はブラウザ不可） | GitHub Actions → "Update Playwright Baseline Snapshots" → Run workflow → artifact `playwright-baseline-snapshots-<run_id>` を DL → `.png` を `e2e/portfolio.spec.js-snapshots/` に配置 → commit。**必ず Playwright 1.55.1 で生成**（D-5 のタイミング根拠） |
| `npm audit` の外部照会・脆弱性確定 | 本環境ではローカル `npm audit` 結果（0 件）のみ確認 | 必要なら CI または手元で `npm audit` / `npm audit --omit=dev` を再確認 |
| AIO citation 実観測 | 未発生（先行レーンゆえ測定はこれから） | 実引用確認時のみ `aio-monitoring-log.json` に記録。捏造禁止 |
| C2PA 署名 / Zenn 記事公開日の外部確定 | Not possible（外部事実確認が必要） | 外部確認後にのみ反映。推測で書かない |

---

## 5. C1〜C7 遵守

C1 外部FW/ライブラリ追加なし（dev 依存の Playwright を minor bump したのみ。runtime 依存は依然ゼロで、Check 38 が機械保証） / C2 IIFE 未変更 / C3 ErrorBoundary 未変更 / C4 FW 再提案なし / C5 人間はコード未記述（実装は Claude Opus 4.8、人間は設計・レビュー・監査・統制） / C6 **AIO テキスト（`llms-full.txt` / `llms.txt` / JSON-LD / バイナリ XMP・ID3）は一切未変更**。digest 再生成なし / C7 KARTE CDN SRI 非適用維持。すべて遵守。

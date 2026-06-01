# decision-v80-phase2-ci-hygiene-3.md

```
Decision-Date : 2026-06-01
Session       : AI2AI.md 未更新（最新は Session Record #19 のまま）。本 increment も
                非 digest 層（検証層・設定層）に閉じるため、新規 session record /
                digest 連鎖を作らない。Session #20 は採番しない（increment #1 / #2 を踏襲）。
Implementer   : Claude Opus 4.8 (Anthropic) — AI agent
Orchestrator  : Yuta Yokoi (横井雄太, human — sole decision authority)
Track         : v80+ staged major update (Phase 2 — CI hygiene increment #3)
Pipeline-Ver  : v74 (unchanged)
Canonical-Ref : AI2AI.md (canonical) / llms-full.txt (ground truth) /
                decision-v80-phase2-ci-hygiene.md (increment #1) /
                decision-v80-phase2-ci-hygiene-2.md (increment #2)
Status        : Applied
```

> **Canonical hierarchy:** `AI2AI.md` is the canonical handoff; `llms-full.txt` is ground truth.
> This decision record is a subordinate incident artifact. If it conflicts with `AI2AI.md` or `llms-full.txt`, those win.

> **命名について:** 受領した 2 文書はこの increment に 2 つの名前を提案していた——`プロンプト.md` 項目 11 の `decision-v80-phase2-ci-hygiene-3.md` と、`改善文書.md` の `decision-v80-phase2-output-analysis-and-css-lint-hygiene.md`。**increment #1 / #2 と連番で揃う前者を採用**した。命名系列の一貫性（`ci-hygiene` → `ci-hygiene-2` → `ci-hygiene-3`）の方が、保守者にとって発見可能性が高いと判断したためである。

---

## 1. 背景

CI 衛生 increment #2（`decision-v80-phase2-ci-hygiene-2.md`）が確定し、**CI 緑・コンソールエラーなし**がオーケストレーターにより確認された。本 increment #3 は、その確定状態を正本としたトータルチェック（現物 ZIP 再解析＋複合解析）で発見した非破壊改善のうち、**既存の確定判断と競合しないもの**だけを適用する。

#1 / #2 と同じ原則を維持する: **AIO 正本層（`llms-full.txt` / `AI2AI.md` / `llms*` alias / `.well-known/*` / digest / `sitemap.xml` 本文 / `robots.txt` 本文）は一切変更しない**。本 increment の内容は純粋に検証層（CSS lint の実行経路と、それを守る consistency check）に閉じており、AI がポートフォリオを引用する際に読むテキストは 1 バイトも変わらない。したがって digest を再生成すると「AIO content が変わった」という偽シグナルになるため、`check_aio_digests.py` の再生成は行わず、本 increment は非 digest 層に留める。`main-js-extraction-map.md` は対象外（main.js 抽出に変化なし）。

実装後、AIO 正本層 15 ファイル（`AI2AI.md` / `Claude2Claude.md` / `llms-full.txt` / `llms.txt` ＋ 3 alias / `.well-known/*` / `sitemap.xml` / `robots.txt` / `index.html` / `main.js` / `style.css`）が受領 ZIP と **byte-identical** であることを差分照合で確認済み。

---

## 2. 決定事項

### D-1: `check_css_stylelint.py` の実行経路をローカル binary 優先へ（再現性・偽緑除去）

**発見:** `check_css_stylelint.py` は `npx stylelint` を起動していた。Phase 2-A で `package.json` / `package-lock.json` / `npm ci` を導入し stylelint を pin（`16.10.0`）したにもかかわらず、実行は `npx` 経由のままで、npm cache / network / permission の状態に結果が依存しうる。さらに重大なのは、**設定エラー・実行不能・非 JSON 出力・予期しない exit code のすべてが `return 0`（黙って成功）**で処理されており、CI 上で偽緑（false green）を生む潜在経路になっていた点である。

**決定:** 次の方針へ書き換えた。

- `node_modules/.bin/stylelint`（`npm ci` が設置するローカル binary）が存在すればそれを優先使用。存在しない場合のみ `npx stylelint` にフォールバック。binary パスは `ROOT = Path(__file__).resolve().parents[2]` から解決し、CWD に依存しない（既存挙動を保つため、対象ファイル `style.css` / `index.html` / `.stylelintrc.json` は従来どおり CWD 相対のまま）。
- 実行不能・設定/parse エラーを、**`strict = used_local OR CI` のとき BLOCKING（exit 1）へ昇格**。`strict` の意味論は次のとおり:
  - `used_local`（ローカル binary 使用）が真なら、stylelint は確実に動くはずなので、その失敗は環境を問わず実欠陥 → BLOCKING。
  - CI（環境変数 `CI` / `GITHUB_ACTIONS`）が真なら、runner 上では常にクリーンな実行を要求 → npx フォールバックの失敗も BLOCKING。
  - **ローカル かつ node_modules 無し**（`strict` 偽）のときだけ graceful degrade（note を出して exit 0）。`npm ci` を忘れた開発者をローカルでハードブロックしない逃げ道を、明確な説明付きで残す。
- 既存の振る舞いはすべて保持: `--formatter json`、severity 分割（error → BLOCKING / warning → `::warning::`）、design-exception 抑制（reduced-motion / `.u-ai-*` / `nav-group-body` の `!important`）、inline `<style>` 抽出、`style.css` 常時検査、`--allow-empty-input`。

**検証:** ローカル（`used_local=True` ＝ strict 経路）で `style.css` PASS（0 違反）、`npm run lint:css` PASS。否定テスト 2 系統で防御特性を確認——(a) strict で stylelint 実行失敗を注入 → exit 1、(b) lenient で同じ失敗 → exit 0（graceful）。`py_compile` OK。

**設計根拠:** これは検証層の硬化であり、`style.css` の内容も lint ルール（`.stylelintrc.json`）も変えていない。緩める変更ではなく**厳しくする**変更なので、`repository-maintainability-map.md` §1 の「invariant を厳しくするのは可・緩めるのは要判断」に合致する。

### D-2: `check_repository_consistency.py` に Check 40（CSS lint 実行経路衛生 / BLOCKING）を追加

**発見:** D-1 で確立した「ローカル binary 優先・偽緑除去」契約を守る invariant が無かった。将来の編集が CSS lint を npx-primary（偽緑を生みやすい経路）へ静かに巻き戻しても、検出できない保守の穴になる。

**決定:** `check_repository_consistency.py` に **Check 40（BLOCKING）**を追加（既存 `check()` ヘルパを使うインラインブロック。Check 39 の直後・Result セクションの直前に配置）。docstring の検査インベントリにも 40 番として追記し、実装とインベントリの同期を維持。3 サブ条件を検査:

- **40a:** `package.json` の `devDependencies` に `stylelint` が宣言されていること。
- **40b:** `check_css_stylelint.py` のソースが `node_modules/.bin/stylelint` を参照していること（ローカル binary 優先の実行経路）。
- **40c:** ソースが `npx` を**フォールバックとして文書化**していること（`npx` と "fallback"/"falls back" の両方が現れる＝ npx が primary ではなく fallback だと記述されている）。

`package.json` と `check_css_stylelint.py` は Check 38 のローカル変数に依存せず**独立に読み直す**（Check 38 の `if`/`try` が走らない場合でも NameError を起こさないため＝防御的に Check 38 と同じ idiom）。

**検証:** 現物で 40a/40b/40c すべて PASS（stylelint 16.10.0 検出）。否定テスト（40b のローカル binary 参照を一時除去）で ERROR（exit 1）を確認し、復帰で PASS を確認。`py_compile` OK。

---

## 3. 意図的に「やらなかった」こと（イエスマンにならないための明示・競合排除の記録）

オーケストレーターの依頼は「競合せず・非破壊で改善可能な項目**全て**」だった。以下は受領 2 文書が提案したが、**既存の確定判断と競合する**ため、競合フィルタにより**適用を見送った**項目である。見送り自体が依頼に対する忠実な遂行であり、各々の理由を残す。

### N-1: PR 検証系・手動系 3 workflow への concurrency は付与しない（increment #2 の確定判断と競合）

`改善文書.md` P1-01 / `プロンプト.md` 項目 5–6 は、`architecture-validation.yml` / `playwright-regression.yml` / `update-playwright-snapshots.yml` への `concurrency` 追加を提案している。**しかし increment #2 の N-2（`decision-v80-phase2-ci-hygiene-2.md` §3）で、この 3 つのうち PR 検証系 2 本については concurrency 不要と既に確定している**。理由は不変で、これらは `git commit` / `git push` を行わないため push race が存在せず、`cancel-in-progress` は「同一 PR に新 commit が来たら古い run を打ち切る」**純粋なコスト最適化**であって障害点除去ではない。`update-playwright-snapshots.yml` も手動（`workflow_dispatch`）・run_id キーの artifact アップロードで push しないため同じ論理が当てはまる。increment #2 が打ち立てた原則「**最適化でなく障害点除去なら churn 回避**」に従い、確定判断を覆さない。

**反対意見の明示（イエスマン回避）:** concurrency 追加には弱いがゼロではない便益がある——速い push の連続時に古い PR run を打ち切れば CI 分の節約と PR フィードバックの高速化になる。これは障害点除去ではなく最適化なので今回は採らないが、将来オーケストレーター判断で「コスト最適化として」採用する余地は残る（`update-playwright-snapshots.yml` だけは `cancel-in-progress: false` を推奨——baseline artifact 取得前の中断を避けるため）。

### N-2: Session Record #20 追記 / `llms-full.txt` 追記 / digest 再生成はしない（#1/#2 の非 digest 前例・AIO 正本層 原則変更禁止 と競合）

`プロンプト.md` は内部で割れている——項目 11（`ci-hygiene-3`、非 digest）と、項目 9 / 10 / 12（`AI2AI.md` への Session Record 追記・`llms-full.txt` 追記・`update_aio_digests.py` 実行で `.well-known/*` 再生成）が共存する。`改善文書.md` の変更対象案も `AI2AI.md` / `llms-full.txt` / `.well-known/*` を含む。

**見送り理由:** increment #1 / #2 はいずれも CI 衛生を**意図的に AIO 正本層の外**に置いた（SR を上げず digest 連鎖を触らない）。本 increment #3 の内容（CSS lint 実行経路 ＋ Check 40）は純粋な検証層であり、**AI がポートフォリオを引用する際に読むテキストを 1 バイトも変えない**。ここで digest を再生成すると「AIO content が変わった」という偽シグナルを digest chain に刻むことになる。AIO 正本層（`llms-full.txt` / `AI2AI.md` / `llms*` alias / `.well-known/*` / digest / version 文字列）は digest chain 保全のため**原則変更禁止**——この既定と、#1/#2 が確立した非 digest 前例の両方に、項目 9/10/12 は競合する。よって `プロンプト.md` 項目 11 の非 digest 経路を採り、項目 9/10/12 は見送る。

**連動する緑の保全:** SR を追加しないことで Check 22（SR 昇順）/ Check 31（`Claude2Claude.md` が AI2AI.md の最大 SR を参照）は最大 SR #19 のまま緑を維持。digest 対象を触らないことで `check_aio_digests.py` も無変更で緑。Check 24（`llms-full.txt` Last-Updated が AI2AI.md の 7 日以内）も両者不変で緑。

### N-3: `main.js` 199 advisory warnings は触らない（baseline 確立前・#1/#2 不変方針）

`改善文書.md` P2-01 / `プロンプト.md` 項目 8 の段階解消は計画であり実コード修正を要求していない。内訳 `curly:124 / no-var:64 / no-shadow:10 / prefer-const:1` はすべて advisory（0 errors）。一括 `--fix` は禁止、かつ視覚回帰 baseline（`e2e/portfolio.spec.js-snapshots/`）未取得のため、視覚影響のある変更は baseline 確立後（`main-js-extraction-map.md` の Stage 進行）に回す。#1/#2 から不変。

### N-4: AIO 正本 content / `robots.txt` / `sitemap.xml` 本文 / バイナリ再エンコード

#1/#2 と同じ。これらはオーケストレーター承認領域（C6）であり、WebP/MP3 の v73 baseline は意図的維持（再エンコードは誤修正リスクのみ）。

---

## 4. Not possible と人間の手順

| 項目 | 状態 | 人間の手順 |
|---|---|---|
| GitHub Actions 実実行緑確認 | Not possible（本環境は Actions 不可） | push 後、各 workflow（特に architecture-validation）の Actions 結果を確認。CI 上では Check 40 と CSS lint strict 経路が runner で走る |
| CI 上の CSS lint strict 動作 | Not possible（runner 環境でのみ `CI=true`） | Actions ログで "CSS lint runner: node_modules/.bin/stylelint (local) — strict" が出ること、ローカル binary 解決が効いていることを確認 |
| Playwright baseline PNG 実生成 | Not possible（ブラウザ不可・任意 AI サンドボックスでの生成禁止） | Actions → "Update Playwright Baseline Snapshots" → Run → artifact DL → `e2e/portfolio.spec.js-snapshots/` に配置・commit（**@playwright/test 1.55.1 で生成**）。baseline 未取得が main.js 物理分割前の最大ブロッカーである点は不変 |
| AIO citation 実観測 | 未発生（先行レーンゆえ測定はこれから） | 実引用確認時のみログ記録。confirmed_citation_events=0 は先行起因の観測前状態であり、戦略失敗ではない。捏造禁止 |

---

## 5. C1〜C7 遵守

C1 外部 FW/ライブラリ追加なし（stylelint は既存 dev 依存・runtime 依存ゼロを Check 38 が機械保証） / C2 IIFE 未変更 / C3 ErrorBoundary 未変更 / C4 FW 再提案なし / C5 人間はコード未記述（実装は Claude Opus 4.8、人間は設計・レビュー・監査・統制） / C6 **AIO テキスト・JSON-LD・バイナリ・`sitemap.xml` 本文・`robots.txt` 本文すべて未変更・digest 再生成なし**（本 increment は検証層に閉じ、引用対象テキストを変えない） / C7 KARTE CDN SRI 非適用維持。すべて遵守。

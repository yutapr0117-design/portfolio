# decision-v80-phase2-ci-hygiene-2.md

```
Decision-Date : 2026-06-01
Session       : AI2AI.md 未更新（最新は Session Record #19 のまま）。本 increment も
                非 digest 層（検証層・設定層）に閉じるため、新規 session record /
                digest 連鎖を作らない。Session #20 は採番しない。
Implementer   : Claude Opus 4.8 (Anthropic) — AI agent
Orchestrator  : Yuta Yokoi (横井雄太, human — sole decision authority)
Track         : v80+ staged major update (Phase 2 — CI hygiene increment #2)
Pipeline-Ver  : v74 (unchanged)
Canonical-Ref : AI2AI.md (canonical) / llms-full.txt (ground truth) /
                decision-v80-phase2-ci-hygiene.md (increment #1)
Status        : Applied
```

> **Canonical hierarchy:** `AI2AI.md` is the canonical handoff; `llms-full.txt` is ground truth.
> This decision record is a subordinate incident artifact. If it conflicts with `AI2AI.md` or `llms-full.txt`, those win.

---

## 1. 背景

CI 衛生 increment #1（`decision-v80-phase2-ci-hygiene.md`）が確定し、**CI 緑・コンソールエラーなし**がオーケストレーターにより確認された。本 increment #2 は、その確定状態を正本としたトータルチェックで発見した非破壊改善を適用する。

#1 と同じ原則を維持する: **AIO 正本層（`llms-full.txt` / `AI2AI.md` / `llms*` alias / `.well-known/*` / digest / `sitemap.xml` 本文 / `robots.txt` 本文）は一切変更しない**。よって `check_aio_digests.py` の再生成は不要で、本 increment は非 digest 層（検証層・設定層）に閉じる。`main-js-extraction-map.md` は対象外（main.js 抽出に変化なし）。

---

## 2. 決定事項

### D-1: sitemap `<loc>` ↔ 実ファイル整合（Check 39 / BLOCKING）

**発見:** sitemap 関連の既存 invariant は Check 9（XML 妥当性）/ 18（root lastmod 同期）/ 34（doc Last-Updated == lastmod）/ 35（robots の Sitemap: directive）/ 36（未来日付 lastmod 不可）と充実しているが、**「広告している各 URL が実在ファイルへ解決するか」**だけは未検査だった。sitemap に実体の無い `<loc>` があると crawler 404 ＝ AIO/SEO の実害になる。

**決定:** `check_repository_consistency.py` に **Check 39（BLOCKING）** を追加。

- `sitemap.xml` の全 `<loc>` を抽出。
- project base（GitHub Pages のパスセグメント `/portfolio/`）以降をリポジトリ相対パスとして解決。root（`.../portfolio/`）および末尾スラッシュは `index.html` へマップ。
- project 外 URL は対象外（Check 39 はローカルファイル整合のみを司り、外部 URL ポリシーは扱わない＝false-positive を出さない）。
- 解決先がリポジトリに存在しなければ赤化。

**検証:** 現物 17 URL すべて解決して PASS。否定テスト（実体の無い `<loc>` を一時注入）で ERROR（exit 1）を確認し、復帰で PASS を確認。

**設計根拠:** sitemap は配信層であり content は AIO 正本（オーケストレーター承認領域）だが、本 Check は **content を変更せず整合を機械保証するだけ**なので C6 に抵触しない。ファイル存在判定は「デプロイされるツリーに実体があるか」の意味論であり、`Path.exists()`（チェックアウト済みツリー）で正しい（Check 37 のような tracked/untracked 区別は不要）。

### D-2: Dependabot に npm ecosystem を追加

**発見:** `.github/dependabot.yml` は `github-actions` のみを監視。Phase 2-A（increment 群の基盤）で `package.json` / `package-lock.json` を導入し dev tool を pin したのに、**その更新を検知する経路が無い**保守の穴があった。これは私（AI）が package.json を導入したことで開いた穴であり、ループを閉じる責任がある。

**決定:** `npm` ecosystem を追加（`directory: "/"`、月次、`commit-message.prefix: "ci"`、labels `dependencies`/`ci`、`groups.dev-dependencies.patterns: ["*"]` で 4 dev 依存を 1 PR に集約）。

**境界:**
- 公開サイトはランタイム依存ゼロの Vanilla JS。ここで管理するのは dev tool（`eslint` / `stylelint` / `@playwright/test` / `http-server`）のみ。
- Dependabot は package.json と package-lock.json を**両方**更新するため、**Check 38（lockfile 整合 BLOCKING）が Dependabot PR の健全性を自動検査**する（両者が同期していなければ赤化）。すなわち #1 で入れた Check 38 が本変更の安全網として機能する。
- 月次・グループ化で PR ノイズを抑制。increment #1 の Playwright 1.55.1 bump は手動だったが、以後の同種更新は Dependabot が継続的に surface する。

### D-3: commit/push する 2 workflow に concurrency（push race 防止）

**発見:** `auto-update-aio-digests.yml`（push to main + dispatch）と `aio-monitoring.yml`（weekly schedule + dispatch）は、いずれも `git commit` + `git push` を行うが `concurrency` ガードが無い。near-simultaneous なトリガ（例: AIO ファイルを連続 push、または dispatch が schedule と重なる）で 2 run が並走すると、後着の `git push` が非 fast-forward で**失敗（赤化）**する。これは未発火でも実在する障害点。

**決定:** 両 workflow に top-level `concurrency` を付与。

```
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: false
```

**`cancel-in-progress: false` の根拠:** 直列化（キュー）し、進行中の run を中断しない。digest / log はファイル内容の純関数なので、キューされた run は最新ツリーに対して再計算・収束する。`true`（中断）でも内容的には収束するが、commit と push の間で run を kill する僅かなリスクを避けるため、より保守的な `false` を採用（push 自体はサーバ側でアトミックなので remote の部分状態は生じないが、予測可能性を優先）。

---

## 3. 意図的に「やらなかった」こと（イエスマンにならないための明示）

### N-1: `--env browser --env es2022` の重複は削除しない

`npm run lint` と `architecture-validation.yml` の ESLint 起動の双方が `--env browser --env es2022` を渡すが、両者とも `--no-eslintrc --config .eslintrc.json` を併用しており、`.eslintrc.json` の `env`（`browser`/`es2022`）が読まれるため `--env` は**冗長**。ただし削除しても lint 結果は完全不変（実測: 0 errors / 199 warnings で一致）。

**判断:** 削除しない。理由＝(1) 純粋な美観 dedup のために **BLOCKING ゲートを触る**のは「最適化でなく障害点除去」「最小・可逆」に反する。(2) 重複は 2 箇所にあり、片方だけ消すと逆に不整合になる。(3) flat config 移行（将来）で自然解消する。increment #1 の N-4 観察を踏襲し、observation-only を維持。

### N-2: PR 検証系 workflow への concurrency は付与しない

`architecture-validation.yml`（push/PR）/ `playwright-regression.yml`（PR）は commit/push しないため push race が無い。`cancel-in-progress` 付与は「同一 PR に新 commit が来たら古い run を打ち切る」**純粋なコスト最適化**であり、障害点除去ではない。原則（最適化でなく障害点除去）に従い churn を避ける。必要になればオーケストレーター判断で追加可能。

### N-3: `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24` env は据え置く

GitHub Actions の JavaScript actions の Node24 移行に伴う前方互換設定。CI 緑の現状で積極的に除去する理由が無く、移行関連の挙動を変えるリスクを取らない。

### N-4: `main.js` 199 warnings / AIO 正本 content / robots・sitemap 本文

#1 から不変の方針。`main.js` 一括 fix は視覚回帰 baseline 確立後（`main-js-extraction-map.md` の Stage 進行）。AIO content・robots・sitemap 本文はオーケストレーター承認領域（C6）。

---

## 4. Not possible と人間の手順

| 項目 | 状態 | 人間の手順 |
|---|---|---|
| GitHub Actions 実実行緑確認 | Not possible（本環境は Actions 不可） | push 後、5 workflow（特に architecture-validation）の Actions 結果を確認 |
| Dependabot 実 PR の挙動 | Not possible | 初回月次サイクル後、npm グループ PR が来ること、Check 38 が緑であることを確認 |
| Playwright baseline PNG 実生成 | Not possible（ブラウザ不可） | Actions → "Update Playwright Baseline Snapshots" → Run → artifact DL → `e2e/portfolio.spec.js-snapshots/` に配置・commit（**1.55.1 で生成**） |
| AIO citation 実観測 | 未発生（先行レーンゆえ測定はこれから） | 実引用確認時のみログ記録。捏造禁止 |

---

## 5. C1〜C7 遵守

C1 外部 FW/ライブラリ追加なし（Dependabot は監視設定のみ、runtime 依存ゼロを Check 38 が機械保証） / C2 IIFE 未変更 / C3 ErrorBoundary 未変更 / C4 FW 再提案なし / C5 人間はコード未記述（実装は Claude Opus 4.8、人間は設計・レビュー・監査・統制） / C6 **AIO テキスト・JSON-LD・バイナリ・`sitemap.xml` 本文・`robots.txt` 本文すべて未変更・digest 再生成なし**（Check 39 は content を変えず整合検査するのみ） / C7 KARTE CDN SRI 非適用維持。すべて遵守。

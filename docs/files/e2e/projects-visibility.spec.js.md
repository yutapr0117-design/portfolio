---
file: e2e/projects-visibility.spec.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-20
canonical-ref: e2e/apps-settings.spec.js / js/settings-page.js / js/store.js / playwright.config.cjs
---

# e2e/projects-visibility.spec.js

## What

プロジェクトの**「非表示」(curation)** の契約を守る behavior e2e spec (BLOCKING gate)。

- Settings の非表示/表示トグルが `projectPrefs.hiddenIds` を出し入れし、公開一覧に反映される
- 非表示が **read 面 5 つすべて**に効く: 公開一覧 / home の注目枠 / 詳細ページの推薦 /
  Cmd+K 候補 / カテゴリ選択肢。解除すると全面に戻る

## Why

**既定プロジェクトは削除できない**ため、非表示が**唯一の非公開手段**である (#886)。
つまりこれは単なる表示設定ではなく **公開/非公開の意思**そのもの。

しかも読み手が 5 面あり、**1 面でも漏れると「隠したのに出ている」**になる。実際 #886 では
`hiddenIds` を読んでいたのが ProjectsPage と SettingsPage だけで、既定 featured の p01 を
隠しても**トップ最上位の注目枠に出続けていた**。read 面の mesh をまとめて 1 file で守る。

元は `e2e/apps-settings.spec.js` にあったが、同 file が **968 行**となり Check 365 の
BLOCKING (1,000 行) まで**残り 32 行**になったため、**当たる前に**切り出した
(CLAUDE.md §7「advisory は BLOCKING を踏む前に効かせる」)。

## How (usage)

```
npx playwright test e2e/projects-visibility.spec.js --project=chromium
```

`E2E_HERMETIC=1` を付けると外部ホストが即 NOTFOUND になり goto が速くなる (Check 416)。

## Constraints

- **BLOCKING gate**: `playwright-regression.yml` の behavior job に含まれる。
  赤になったら rerun せず落ちたテストを読む (帰属は playwright-regression.yml の mirror doc)。
- **Check 365** (1,000 行 BLOCKING) / **Check 408** (BUDGET-DATA 登録必須) /
  **Check 424** (§2 表の実測行数一致)。
- カテゴリ面は「そのカテゴリを**空にする**」まで変化しないため、1 件隠して「変わらない」を
  確認しても**何も検査していない**。既定で 3 件しかない Security を 3 件とも隠す setup が要る。

## Change impact

- 新しい read 面 (プロジェクト一覧を読む新機能) を足したら、**この spec に面を 1 つ追加する**。
  実装だけ足してテストを足さないと #886 と同じ「1 面だけ漏れる」が再発する。
- 全件非表示は現実に起こりうるので、featured は null 許容 + fallback 描画になっている
  (無条件 dereference の FatalPage crash 回避)。この契約を壊さないこと。
- 直接 URL での閲覧は従来どおり許容 (hidden は **listing の可視性制御**でアクセス制御ではない)。

## Audience-specific notes

### For AI agents
- 役割タグ: `behavior-e2e`, `curation`, `listing-mesh`, `blocking-gate`

### For human engineers (新卒レベル)
- 「一覧から消す」機能は読み手が複数ある。**producer だけでなく consumer を全部数えてから**
  実装/テストする。

### For third parties
- 単一のフラグが複数の描画面へ波及する設計を、mesh として機械強制している実装例。

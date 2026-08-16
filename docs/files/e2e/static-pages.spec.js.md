---
file: e2e/static-pages.spec.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-16
canonical-ref: playwright.config.cjs / js/pages.js / js/hiring-risk-page.js / js/ai-knowhow-page.js / e2e/projects.spec.js
---

# e2e/static-pages.spec.js

## What

データを持たない静的ページ（`#/role-split` / `#/hiring-risk` / `#/ai-knowhow`）の behavior e2e。

- 各ページの lead 見出しが描画される
- role-split の役割分担表が **ARIA table 意味論**（`role=table` / `row` / `rowheader` /
  `columnheader` / `cell`）を保つ

## Why

プロジェクト一覧のような状態を持たないので、壊れ方も違う —— 「描画されているか」と
「**機械可読な構造が保たれているか**」が主な関心事になる。

role-split の表はとくに重要で、WebMCP のツール `extract_human_vs_ai_role_split` が
`data-ai-role` フックで走査する **機械向けの契約**でもある。#929 では、そのツールが
走査していたセレクタが**リポジトリのどこにも存在せず、一度も抽出に成功していなかった**
（常に静的フォールバックを返していた）ことが実測で判明した。この種の壊れ方は視覚に
一切出ないため、宣言を信じずに実測する層が要る。

ファイル分離の理由は肥大化の**予防**。`projects.spec.js` が 923 行となり早期警告（900）を
超えたため、**Check 365 の BLOCKING（1,000 行）を踏む前に**このテーマの塊を切り出した
（CLAUDE.md §7「advisory は BLOCKING を踏む前に効かせる」）。mutation の `test` フィールドは
title 一致ゆえ file 移動の影響を受けない。

## How (usage)

```
npm run test:e2e
  └─ Playwright + http-server (playwright.config.cjs testDir: ./e2e)
  └─ e2e/*.spec.js は testMatch デフォルト (**/*.spec.js) で自動 discovery
```

## Constraints

- **Check 28**: 全 e2e/*.spec.js に test() のネスト無し
- **Check 111**: networkidle 待ちは screenshot (portfolio.spec.js) 以外で禁止
- **Check 114**: test.only/describe.only 無し (false-green footgun 防止)
- **Check 151**: 全 e2e/*.spec.js 横断で test() title 一意
- **Check 108**: docs/files ミラー 1 対 1 bijection
- **Check 408**: e2e spec は file-size-budget.md の BUDGET-DATA へ登録必須
- **Check 411**: main.js の `querySelectorAll` セレクタが js/ の実描画に解決すること
  （role-split の `data-ai-role` フックはこの Check が守る静的面。本 spec は挙動面）

## Change impact

- `js/pages.js` の splitRow / 表構造を変更すると本 spec が RED になる
- `data-ai-role` フックを変えるときは main.js の WebMCP ツール側と対で変更する（Check 411）
- spec ファイル rename → docs/files ミラー同期 (Check 108) + BUDGET-DATA 同期 (Check 408)

## Audience-specific notes

### For AI agents
- 役割タグ: `e2e-spec`, `behavior-gate`, `static-pages`, `machine-facing`
- **機械向けの宣言は実測せよ** —— ツール説明文・structured data・セレクタは視覚に出ないため
  全 gate を素通りする。「そのセレクタは実際に何件マッチするか」を一度走らせるだけで判る（#929）

### For human engineers (新卒レベル)
- 静的ページでも「表」は意味論が要る。見た目が表でも `<div>` の格子だと支援技術には
  ただのテキストの並びに見える

### For third parties
- AI エージェントに読ませることを前提にしたページの、構造契約テストの例

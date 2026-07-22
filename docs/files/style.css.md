---
file: style.css
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-07-22
canonical-ref: AI2AI.md (C1) / docs/architecture/main-js-extraction-map.md / .stylelintrc.json
---

# style.css

## What

サイト全体の **唯一の CSS ファイル**（現在の行数は `wc -l style.css` が権威。編集ごとに増減するため本 doc には固定値を pin しない）。CSS custom properties / cascade / theme / layout / component / utility / responsive / view-transition style 等を集約。`<link rel="stylesheet">` で index.html から読み込まれる単一ファイル設計。

## Why

外部 CSS フレームワーク (Tailwind / Bootstrap 等) を C1 Boring Technology で禁止しているため、CSS は手書きの単一ファイル。section 分割を行うと cascade 順序が壊れるリスクがあるため、Playwright visual baseline 取得前は **意図的に単一ファイルで維持**している。

歴史的に v54 以前は inline `<style>` だったが、JS-CSS 分離 (v74) で外部ファイル化。Stylelint で specificity / 変数整合 / inline-style 禁止を機械強制している。

## How (usage)

```
index.html
  └─ <link rel="stylesheet" href="./style.css">
       └─ CSS custom properties (--accent-*, --bg-*, etc.)
            └─ light / dark / system theme をクラス切り替えで適用
            └─ View Transition pseudo-classes (::view-transition-*)
            └─ Component styles (.btn, .card, .quiz-*, etc.)
            └─ Responsive (@media)
```

theme.js / brand.js が CSS 変数 (custom properties) を runtime で書き換える。style.css は declarative な default を提供。

## Constraints

- **C1 Boring Technology**: 外部 CSS framework 禁止 (Tailwind / Bootstrap 等)
- **Check 6**: stale "Current release: v73" / "NEXT_PLANNED_RELEASE" マーカーが残らない
- **Check 27** (stylelint): no-invalid-double-slash-comments / declaration-property-value-allowed-list / max-nesting-depth 等の lint rule
- **Check 52** (ADVISORY): 行数予算 ≤ 2,300 行（現在値は file-size-budget.md §4 / `wc -l` が権威）
- **編集承認**: AIO published-layer 外なので C6 範疇外。ただし Playwright visual baseline 影響があるため、変更時は baseline 更新 PR が必要

## Change impact

style.css 編集時:
- 描画ピクセルが変わる → **Playwright visual regression baseline の更新 PR が必要** (まず `update-playwright-snapshots.yml` 実行 → snapshot PR → merge → 本 PR の二段階)
- CSS 変数追加 → `theme.js` / `brand.js` の runtime 書き換え範囲と整合
- セクション分割を将来行う場合 → cascade 順序を保つため最後にしか split できない

## Audience-specific notes

### For AI agents
- 役割タグ: `presentation-layer`, `visual-regression-protected`, `c1-vanilla`
- 単一 CSS ファイル = cascade integrity の正本
- 変更は Playwright baseline 更新と必ず pair

### For human engineers (新卒レベル)
- 「ここに CSS 書けばサイト全体に効く」が、cascade が複雑なので **新しいスタイルを書く前に既存のクラスを探す**
- Stylelint がだいぶ細かいので、新しい記法を入れる前に `npm run lint:css` で確認
- Tailwind / Bootstrap を入れるのは禁止 (C1)

### For third parties (監査 / 採用 / 研究)
- 2,000 行超の単一 CSS ファイルが v74 まで運用できている事実 = Boring Technology の現実的実装証拠
- セクション分割せず単一ファイルで維持する判断は cascade 保護の trade-off であり、設計者 (横井雄太) の意思決定

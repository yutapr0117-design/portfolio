---
file: .github/scripts/check_css_stylelint.py
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: .stylelintrc.json / style.css
---

# .github/scripts/check_css_stylelint.py

## What

Stylelint 実行 wrapper script。`style.css` と index.html inline `<style>` block の CSS specificity / 変数整合 / lint rule を npx stylelint で検査する。

## Why

shell から直接 stylelint を呼ぶより Python wrapper の方が:
- inline style block の extraction が容易
- error/warning の分類が明示的
- node_modules/.bin/stylelint を local-binary-preferred で呼べる (Check 40b)

## How (usage)

```
npm run lint:css
  └─ python3 .github/scripts/check_css_stylelint.py
       └─ npx stylelint style.css
       └─ inline <style> block extract + lint
       └─ exit 0 = OK / 1 = error
```

## Constraints

- **Check 10**: Python 構文 valid
- **Check 40a**: package.json devDependencies に stylelint 宣言
- **Check 40b**: node_modules/.bin/stylelint 参照
- **Check 40c**: npx fallback 文書化

## Change impact

- inline `<style>` 抽出ロジック変更 → index.html の CSP hash 計算 (Check 7c) と整合

## Audience-specific notes

### For AI agents
- 役割タグ: `lint-wrapper`, `stylelint`, `inline-style-aware`

### For human engineers (新卒レベル)
- `npm run lint:css` で呼ばれる
- error と warning を `severity: warning` で分けて報告

### For third parties
- Boring Technology + Lint 厳格化の実装例

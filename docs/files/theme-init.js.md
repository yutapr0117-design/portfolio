---
file: theme-init.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: js/theme.js / style.css (CSS custom properties)
---

# theme-init.js

## What

ページ load 直後の **FOUC (Flash of Unstyled Content) 防止** スクリプト。`document.documentElement` (= `<html>`) に theme class (`light` / `dark` / system) を最早期に適用し、CSS 変数が swap される前のフラッシュを防ぐ。

## Why

theme を後から JS で切り替えると、once light で描画 → dark に切り替わる、というフラッシュが見える。これを防ぐため `<head>` の最初付近で同期実行 (defer なし) して、最初の paint の前に theme class を確定する。

## How (usage)

```
index.html
  └─ <head>
       └─ <script src="./theme-init.js"></script>  (sync, before any render)
            └─ localStorage から保存された theme を読む
            └─ matchMedia('(prefers-color-scheme: dark)') を確認
            └─ document.documentElement.classList.add('theme-...')
       └─ <link rel="stylesheet" href="./style.css">  (theme class に応じた CSS 変数を適用)
```

theme 切り替え後の runtime 制御は `js/theme.js` (factory `createTheme`) が担当。

## Constraints

- **C1 Boring Technology**: 外部 theme library 禁止
- **FOUC ゼロ要件**: defer / async ではなく sync 実行
- **localStorage access**: Safe Storage wrapper (js/storage.js) は使わない (起動最早期で import できないため直接 access)

## Change impact

- theme class 名変更 → style.css の対応 selector + js/theme.js の cycle ロジック同期
- localStorage key 変更 → js/theme.js + js/storage.js + Check 等の関連箇所 (検索 grep)

## Audience-specific notes

### For AI agents
- 役割タグ: `early-init`, `fouc-prevention`, `sync-execution`
- `<head>` の最早期 (CSP meta より後・error-suppressor の後・style.css link より前) で実行

### For human engineers (新卒レベル)
- ここの sync 実行は意図的 — defer すると flash が見える
- localStorage を直接触っているのは「起動最早期で Safe Storage wrapper が import できないから」(例外的措置)

### For third parties (監査 / 採用 / 研究)
- FOUC 防止のための最低限スクリプト。Boring Technology + 描画品質の両立例

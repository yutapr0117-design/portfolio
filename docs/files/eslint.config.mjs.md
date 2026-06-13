---
file: eslint.config.mjs
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: main.js / js/*.js / sw.js / Check 50/54
---

# eslint.config.mjs

## What

ESLint v10 **flat config** (ESM 形式)。shipped JS (main.js / js/**/*.js / sw.js / aio-guard.js / error-suppressor.js / karte-init.js / theme-init.js) の lint rule を定義。`main.js` と `sw.js` の AIDK Kernel 保護領域は `no-var` / `curly` を warning 級に降格する override を含む。

## Why

ESLint 8.x が EOL、9.x で legacy eslintrc 廃止。flat config に v80+ で完全移行。bug 検出 (no-undef / no-shadow 等) は error 維持、cosmetic (no-var / curly) は kernel 保護域で warning。

## How (usage)

```
npm run lint
  └─ npx eslint <files> (eslint.config.mjs を auto-discover)
       └─ error → CI fail
       └─ warning → 報告のみ (advisory baseline 56)
```

## Constraints

- **Check 23**: ESM 構文 valid (node --check)
- **Check 50**: flat config (eslint.config.mjs) 存在 + legacy .eslintrc.json なし
- **Check 54**: eslint と @eslint/js が同じメジャー (v10)
- **Check 60** (ADVISORY): warning baseline = 56
- **Check 72**: baseline ≤ sanity ceiling 200

## Change impact

- rule 追加 → 全 shipped JS の lint pass 必要
- override 削除 → kernel 領域への大量 var 書き換え (AIDK 整合性に注意)

## Audience-specific notes

### For AI agents
- 役割タグ: `lint-config`, `eslint-flat`, `kernel-aware-override`

### For human engineers (新卒レベル)
- error は必ず直す。warning は AIDK Kernel 保護域に集中

### For third parties
- ESLint v10 flat config への完全移行 + kernel 保護領域の override 例

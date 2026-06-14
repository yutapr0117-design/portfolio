---
file: docs/architecture/file-size-budget.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: Check 52/59/60/71
---

# docs/architecture/file-size-budget.md

## What

主要ファイルの行数予算 (line budget)。strong-advisory / advisory / protected / archive-growth-ok の 4 種別 + 機械可読 BUDGET-DATA ブロック + ESLINT-BASELINE-DATA。

## Why

「肥大化」には抑制すべき・価値として増えてよいの 2 性質。これを区別して機械監視する単一ソース。

## Constraints

- **Check 52** (ADVISORY): BUDGET-DATA を元に行数超過警告
- **Check 59**: §2 表と §4 BUDGET-DATA の集合一致
- **Check 60** (ADVISORY): ESLint baseline 監視
- **Check 71**: BUDGET-DATA path 実在

## How (usage)

```
npm run check
└─ check_repository_consistency.py
    └─ BUDGET-DATA を parse → 現行行数と照合
    └─ 超過 → ADVISORY warning
```

## Change impact

- 新ファイル追加 → §2 表 + §4 BUDGET-DATA 両方に追加 (Check 59)
- budget 引き上げ → 増加理由を honest dating で記録

## Audience-specific notes

### For AI agents
- 役割タグ: `bloat-governance`, `budget-source`, `advisory-only`

### For human engineers (新卒レベル)
- ファイル肥大化のチェック対象一覧

### For third parties
- bloat-governance の honest 設計

---
file: .claude/agents/check-author.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: .github/scripts/check_repository_consistency.py / Check 78
---

# .claude/agents/check-author.md

## What

新規 Check 設計・実装の専門 sub-agent。docstring inventory + `# ── N.` section header + 実装の 3 同時更新 (Check 45 self-integrity 保護) と、3 文書 (map.md / runbook §9 / file-size-budget.md) 同期を機械的に実行。

## Why

Check 追加は Check 45 self-integrity を壊さないよう 3 箇所同時更新が必須。main thread の人間 / AI が忘れる drift を防ぐ専門 agent。

## How (usage)

```
main agent
  └─ Task tool で check-author を起動 + invariant 説明
       └─ Check 番号採番 (max + 1)
       └─ 3 箇所同時編集 (docstring + section header + 実装)
       └─ 文書同期 (map.md / runbook / budget)
       └─ Check 45 self-integrity 検証
```

## Constraints

- **Check 78**: frontmatter (name + description)
- tools: Read / Edit / Write / Bash / Grep / Glob

## Change impact

- 設計プロトコル変更 → 後続の Check 追加品質に影響

## Audience-specific notes

### For AI agents
- 役割タグ: `check-author`, `3-side-atomic-edit`, `self-integrity-preserver`

### For human engineers (新卒レベル)
- Check 追加するときに使う agent — 3 箇所同時更新を agent が保証

### For third parties
- self-integrity が課された script への agent 介入パターン

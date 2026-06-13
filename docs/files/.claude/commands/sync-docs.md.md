---
file: .claude/commands/sync-docs.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: docs/architecture/* / Check 77
---

# .claude/commands/sync-docs.md

## What

`/sync-docs` slash command。Check 追加後の 3 文書 (map.md / runbook §9 / file-size-budget.md) 同期を一括実行。Check 45 / 64 / 70 / 59 の self-integrity 検証も含む。

## Why

Check 追加時の文書同期忘れ防止。手動同期は drift しやすいので slash 化。

## How (usage)

```
/sync-docs
└─ check-repository-consistency-map.md 更新
└─ total-check-runbook.md §9 更新
└─ file-size-budget.md 更新
└─ python3 .github/scripts/check_repository_consistency.py exit 0 確認
└─ 5 行 BLUF 報告
```

## Constraints

- **Check 77**: frontmatter + description

## Change impact

- 同期対象 doc 追加 → このコマンドの責務範囲拡張

## Audience-specific notes

### For AI agents
- 役割タグ: `slash-command`, `doc-sync`

### For human engineers (新卒レベル)
- Check 追加して文書同期忘れがちなときに使う

### For third parties
- 3 文書間 cross-document integrity の運用化

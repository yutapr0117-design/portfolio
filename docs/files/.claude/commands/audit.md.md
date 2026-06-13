---
file: .claude/commands/audit.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: .claude/agents/repo-auditor.md / Check 77
---

# .claude/commands/audit.md

## What

`/audit` slash command。`repo-auditor` sub-agent を呼んでリポジトリ全体 drift 監査 (read-only) を実行。6 dimension を 30 行以内で報告。

## Why

cold-start や session 復帰時の状況把握を 1 command で。read-only なので副作用ゼロ。

## How (usage)

```
/audit
  └─ Task tool で repo-auditor 起動
  └─ 6 dimension 監査
  └─ BLUF 報告
```

## Constraints

- **Check 77**: frontmatter + description

## Change impact

- 監査範囲拡張時は repo-auditor.md 側を同時更新

## Audience-specific notes

### For AI agents
- 役割タグ: `slash-command`, `audit-launcher`

### For human engineers (新卒レベル)
- 「何が起きてる?」のときに最初に打つ

### For third parties
- AI agent による read-only audit の slash 化

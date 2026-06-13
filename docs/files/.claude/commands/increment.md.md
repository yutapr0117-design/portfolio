---
file: .claude/commands/increment.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: CLAUDE.md §5 / Check 77
---

# .claude/commands/increment.md

## What

`/increment` slash command。新 increment 開始時の規律 (discover → document → systematize → verify → deliver) と C1-C7 制約 + branch / commit 規則を提示する。

## Why

毎回手動で規律 reminder を書くと忘れる。slash で defaults として呼べる。

## How (usage)

```
/increment
└─ 5 step discipline 提示
└─ C1-C7 制約 reminder
└─ branch / commit 規律 reminder
└─ このセッションでの計画 BLUF (3 行)
```

## Constraints

- **Check 77**: frontmatter + description

## Change impact

- 規律変更 → CLAUDE.md §5 と同期

## Audience-specific notes

### For AI agents
- 役割タグ: `slash-command`, `discipline-reminder`

### For human engineers (新卒レベル)
- 新しい increment 開始時に打つ

### For third parties
- AI 実装での discipline 維持パターン

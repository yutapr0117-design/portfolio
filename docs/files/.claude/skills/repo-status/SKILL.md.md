---
file: .claude/skills/repo-status/SKILL.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: CLAUDE.md §7 / Check 80
---

# .claude/skills/repo-status/SKILL.md

## What

`repo-status` skill。session-start で proactive に呼ばれる、リポジトリ現状を 15 行 BLUF で要約する skill。Pipeline-Version / active track / 最新 increment / Check 総数 / Stage 5 状態 / 次の judgment 候補 を返す。

## Why

session-start cold-start を 15 行で済ませる。「状況を教えて」「今どこ?」「次は?」等の trigger で skill が自動呼ばれる。

## How (usage)

```
Claude Code が session-start で skill registry を読む
└─ description が trigger phrase に match
└─ skill 起動 → 15 行 BLUF 返却
```

## Constraints

- **Check 80**: frontmatter + name + description
- 最大 15 行

## Change impact

- description 変更 → trigger 範囲

## Audience-specific notes

### For AI agents
- 役割タグ: `skill`, `session-start-status`, `proactive`

### For human engineers (新卒レベル)
- 「今どこにいる?」と聞けば 15 行で現状が分かる

### For third parties
- AI agent の self-orientation skill の実装例

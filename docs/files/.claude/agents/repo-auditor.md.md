---
file: .claude/agents/repo-auditor.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: CLAUDE.md §7 / AI2AI.md / Check 78
---

# .claude/agents/repo-auditor.md

## What

リポジトリ全体 drift 監査の read-only sub-agent。6 dimension (C1-C7 整合 / Check 45 self-integrity / AIO digest 連鎖 / Stage 5 invariance / Last-Updated freshness / CI workflow 衛生) を読み取り専用で audit し、🟢 / 🟡 / 🔴 で報告。

## Why

session-start の cold-start や、長期不在後の復帰時に、リポジトリ全体の健康状態を 30 行以内で把握する必要がある。専門 agent が定型 6 dimension を網羅。

## How (usage)

```
main agent
  └─ /audit slash command または直接 Task tool で repo-auditor 起動
       └─ CLAUDE.md → AI2AI.md → llms-full.txt → runbook §9 を読む
       └─ 6 dimension 検査
       └─ 🟢 / 🟡 / 🔴 BLUF report 返却
```

## Constraints

- **Check 78**: frontmatter (name + description)
- tools: Read / Glob / Grep / Bash のみ (編集権なし)

## Change impact

- 6 dimension 変更 → audit report のカバレッジ

## Audience-specific notes

### For AI agents
- 役割タグ: `repo-auditor`, `read-only`, `6-dimension`

### For human engineers (新卒レベル)
- 「何が起きてるか分からない」状態で `/audit` を実行すれば 30 行で現状把握

### For third parties
- AI agent による定常 audit の実装例

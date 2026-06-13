---
file: .claude/commands/deliver.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: CLAUDE.md §5 / Check 77
---

# .claude/commands/deliver.md

## What

`/deliver` slash command。increment 確定の mandatory format (変更ファイル全 block + alphabetical 相対 path 一覧 + 明示 `git add <path>` + summary) を強制する。

## Why

「途中で止まる」「`git add .` で漏れる」「commit message が稚拙」等の運用品質低下を構造防止。CLAUDE.md §5 の規律を slash 化。

## How (usage)

increment 完了直前に `/deliver` を呼ぶ → agent が 4 部構成 (changed-file blocks / paths / commit instructions / summary) を生成。

## Constraints

- **Check 77**: frontmatter + description
- `git add .` / `-A` / `--all` は使わない (settings.json で deny)

## Change impact

- format 変更 → 後続 increment の納品品質に影響

## Audience-specific notes

### For AI agents
- 役割タグ: `slash-command`, `delivery-discipline`

### For human engineers (新卒レベル)
- 最後に `/deliver` を呼べば mandatory format を agent が組み立てる

### For third parties
- AI-assisted code delivery における品質保証の実装例

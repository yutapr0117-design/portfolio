---
file: .claude/CLAUDE.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: /CLAUDE.md (root primary router) / AI2AI.md / Check 90
---

# .claude/CLAUDE.md

## What

Claude Code **sub-context** (root `/CLAUDE.md` を補完する Claude Code-specific 操作ノート)。session-start protocol / sub-agent 起動パターン / slash command idioms 等を含む。

## Why

root `/CLAUDE.md` は entity-canonical router (C1-C7 / safety gates / routes / handoff)。`.claude/CLAUDE.md` は **Claude Code-specific** な操作 (sub-agent / skill / slash command) のガイド。重複を避けるため明示的に役割分担。

## How (usage)

Claude Code が起動時に自動で root CLAUDE.md と並んで読む。session-start で `/audit` / `/repo-status` 等の slash command を起動するときに参照。

## Constraints

- **Check 90**: entity name + Organization 名を含む

## Change impact

- session-start protocol 変更 → 後続 Claude Code session の動作が変わる

## Audience-specific notes

### For AI agents
- 役割タグ: `claude-sub-context`, `session-protocol`

### For human engineers (新卒レベル)
- root CLAUDE.md と役割分担 — entity / 制約は root、Claude Code 操作は .claude/CLAUDE.md

### For third parties
- AI agent context の階層化 (root canonical + tool-specific sub) の実装例

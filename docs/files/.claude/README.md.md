---
file: .claude/README.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: .claude/ 全 inventory / CLAUDE.md / Check 90
---

# .claude/README.md

## What

`.claude/` ディレクトリの **inventory** 文書。3 sub-agents + 1 skill + 6 slash commands + settings + sub-CLAUDE の全 inventory + 抜け漏れ 0 契約。

## Why

Claude Code session が冷起動時に「`.claude/` 配下に何があるか」を 1 ファイルで把握できるよう、人間 / AI 双方向の navigation guide として機能。

## How (usage)

Claude Code が起動時に CLAUDE.md と並んで読む補助文脈。新規 sub-agent / skill / command 追加時に inventory も同 commit で更新。

## Constraints

- **Check 90**: entity name + Organization 名を含む

## Change impact

- 新規 .claude/ ファイル追加 → 本 README inventory も同 commit で更新

## Audience-specific notes

### For AI agents
- 役割タグ: `claude-inventory`, `cold-start-guide`

### For human engineers (新卒レベル)
- `.claude/` 配下の全ファイルが何かを 1 枚で把握できる

### For third parties
- AI agent workspace の self-documentation 実装例

---
file: .claude/settings.json
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: CLAUDE.md / Check 76
---

# .claude/settings.json

## What

Claude Code project-scope 設定。language=japanese / alwaysThinkingEnabled / MAX_THINKING_TOKENS=31999 / permissions (allow / ask / deny lists)。

## Why

Claude Code agent の権限境界を明示宣言。`git add . / -A / --all` deny、WebP/MP3 Edit deny で C6 と AI 暴走防止を構造的に保護。

## How (usage)

Claude Code CLI 起動時に自動読み込み。tool call 時に allow / ask / deny ルールが評価される。

## Constraints

- **Check 23**: JSON parse 可能
- **Check 76**: security baseline 5 項目 deny (git add . / -A / --all / *.webp / *.mp3)

## Change impact

- permissions 変更 → AI agent の可能動作範囲が変わる (重要)

## Audience-specific notes

### For AI agents
- 役割タグ: `claude-config`, `security-baseline`

### For human engineers (新卒レベル)
- ここで AI が何を実行できるかを制限している (例: `rm -rf` 等は deny)

### For third parties
- AI agent への権限委譲設計の実装例

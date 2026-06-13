---
file: .claude/commands/archive-incidents.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: docs/incident-artifacts/ / Check 77
---

# .claude/commands/archive-incidents.md

## What

`/archive-incidents` slash command。major-release boundary でのみ実行する。閉じたトラックの incident-artifacts (decision-*.md / improvement-notes-*.md) を `docs/session-records/incident-artifacts-archive-<track>.md` へ append-only 集約する。

## Why

append-only history のフォルダ肥大化を緩和。日常 increment では実行しない (進行中トラックの参照が切れるリスクのため)。proof-of-work の総量は減らさない。

## How (usage)

major-release 時に手動で `/archive-incidents` 実行 → agent が 9 段階手順 (集約対象選定 → 参照確認 → archive 連結 → byte-equality 検証 → digest 影響確認 → 機械整合 → 数値同期 → 検証 → 記録) を順次実行。

## Constraints

- **Check 77**: frontmatter + description
- 進行中トラックは畳まない原則

## Change impact

- archive 化 → docs/incident-artifacts/ の見通し改善 + AI2AI-archive.md 連動

## Audience-specific notes

### For AI agents
- 役割タグ: `slash-command`, `archive`, `major-release-only`

### For human engineers (新卒レベル)
- 日常では使わない。major-release のときだけ

### For third parties
- append-only history の集約パターンの実装例

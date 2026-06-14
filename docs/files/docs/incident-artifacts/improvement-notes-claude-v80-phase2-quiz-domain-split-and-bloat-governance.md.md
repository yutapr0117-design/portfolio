---
file: docs/incident-artifacts/improvement-notes-claude-v80-phase2-quiz-domain-split-and-bloat-governance.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: Check 42 / Check 52 / Stage 3-b
---

# docs/incident-artifacts/improvement-notes-claude-v80-phase2-quiz-domain-split-and-bloat-governance.md

## What

quiz domain split (Stage 3-b) + bloat governance (Check 52) の Claude 視点 notes。

## Why / How (usage) / Constraints / Change impact

ドメイン別データ分割 + 行数予算機械監視 / append-only。


## How (usage)

過去判断・学びの参照源。新規 session 復帰時に文脈再構成のために読む。


## Constraints

- **Check 42**: incident-artifacts 命名規約 (`decision-*.md` / `improvement-notes-*.md` / `*.yml` / `README.md`)
- append-only history (既存内容は変更しない)


## Change impact

- append-only: 既存内容は変更しない
- 新規 increment 時のみ新ファイル追加

## Audience-specific notes

### For AI agents
- 役割タグ: `improvement-notes`, `domain-split`, `bloat-budget`

### For human engineers (新卒レベル)
- ドメイン別分割 + 予算の学び

### For third parties
- bloat governance 設計学び

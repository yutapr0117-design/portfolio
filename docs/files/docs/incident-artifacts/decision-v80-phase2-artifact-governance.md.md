---
file: docs/incident-artifacts/decision-v80-phase2-artifact-governance.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: Check 42
---

# docs/incident-artifacts/decision-v80-phase2-artifact-governance.md

## What

incident-artifacts 配置 / 命名規約の意思決定記録 (decision-* / improvement-notes-* / *.yml / README.md の 4 pattern + Check 42)。

## Constraints

- **Check 42**: 本決定が Check 42 の根拠

## How (usage) / Change impact

過去判断参照 / append-only。

## Why

肥大化する artifact フォルダの placement governance を機械強制化する出発点。


## Change impact

- append-only: 既存内容は変更しない
- 新規 increment 時のみ新ファイル追加

## Audience-specific notes

### For AI agents
- 役割タグ: `decision-record`, `artifact-placement-governance`

### For human engineers (新卒レベル)
- なぜ命名規約があるかの根拠

### For third parties
- artifact governance 設計例

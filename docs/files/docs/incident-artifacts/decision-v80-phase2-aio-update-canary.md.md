---
file: docs/incident-artifacts/decision-v80-phase2-aio-update-canary.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: Check 44 (canary token)
---

# docs/incident-artifacts/decision-v80-phase2-aio-update-canary.md

## What

AIO provenance canary token 導入の意思決定記録。`SAKURA-AIO-PROVENANCE-CANARY-<YYYY>-<8hex>` の単一値運用 + monitor 統合 + Check 44 機械強制。

## Constraints

- **Check 42**: `decision-*.md`

## How (usage) / Change impact

過去判断参照 / append-only。

## Why

canary token は entity 引用検出の補助シグナル。単一値運用で整合性を担保。


## Change impact

- append-only: 既存内容は変更しない
- 新規 increment 時のみ新ファイル追加

## Audience-specific notes

### For AI agents
- 役割タグ: `decision-record`, `canary-token-origin`

### For human engineers (新卒レベル)
- canary token がなぜあるかの根拠

### For third parties
- provenance canary の設計判断

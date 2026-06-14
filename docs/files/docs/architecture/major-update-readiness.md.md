---
file: docs/architecture/major-update-readiness.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: Playwright baseline / main.js Stage 5
---

# docs/architecture/major-update-readiness.md

## What

major update (v74 → v80+ 等) と Playwright baseline 取得手順書。snapshot 生成 workflow → PR → merge の二段階フローを documented。

## Why

baseline 更新は人間 review 必須。手順を文書化することで「どこで何を確認するか」が drift しない。

## How (usage)

major update のときに参照。Playwright snapshot 更新が必要な場面でも参照。

## Constraints

- **Check 51**: Playwright pin が本 runbook と一致

## Change impact

- 手順変更 → 本ファイル + workflow 同期

## Audience-specific notes

### For AI agents
- 役割タグ: `runbook`, `major-update`, `baseline-procedure`

### For human engineers (新卒レベル)
- 「ベースライン更新どうやるんだっけ?」のときに読む

### For third parties
- AI 実装 + 視覚回帰の安全な major update 実装例

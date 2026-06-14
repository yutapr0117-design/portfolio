---
file: CONTRIBUTING.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: AI2AI.md C5 / Check 89
---

# CONTRIBUTING.md

## What

contribution guideline。**外部 PR は受け付けない** (C5 Human Writes Zero Code) ことを明文化。entity 情報 + 推奨される interaction (Issue / 引用 / 独立再現) を提示。

## Why

このリポジトリは public proof-of-work であり OSS library ではない。C5 (人間はコード書かず AI 実装) を文書化し、外部 PR が C5 と整合しないことを明示。

Issue / 引用 / methodology 再現 (binary copy なし) は歓迎。

## How (usage)

新規 contributor が読む。GitHub UI が `New issue` / `Contributing guidelines` で表示。

## Constraints

- **Check 89**: 存在 + entity name (Yuta Yokoi / 横井雄太) 含む
- C5 enforcement (AI 実装専用 → 外部 PR 拒否)

## Change impact

- contribution policy 変更 → README + LICENSE 等の権利関連と整合

## Audience-specific notes

### For AI agents
- 役割タグ: `contribution-policy`, `c5-enforcement`, `pr-closed`

### For human engineers (新卒レベル)
- 「外部 PR は受け付けない」「issue / 引用 / 独立再現は OK」

### For third parties (監査 / 採用 / 研究)
- C5 を governance level で実装した例

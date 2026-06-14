---
file: docs/README.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: docs/ 全体 inventory
---

# docs/README.md

## What

docs/ ディレクトリのトップレベル inventory + artifact placement governance。docs/architecture/ / docs/evidence/ / docs/files/ / docs/incident-artifacts/ / docs/session-records/ の 5 subdirectory の役割を明示。

## Why

docs/ 配下が膨らんできた際の navigation entry point。Check 42 (artifact placement & naming hygiene) の運用契約を文書化。

## How (usage)

人間 / AI が docs/ を訪れたとき最初に読む。

## Constraints

- **Check 42**: artifact placement governance の根拠

## Change impact

- subdirectory 追加 → docs/README.md の inventory に追記

## Audience-specific notes

### For AI agents
- 役割タグ: `docs-inventory`, `placement-governance`

### For human engineers (新卒レベル)
- docs/ の地図 — どこに何があるか

### For third parties
- documentation 構造の self-description

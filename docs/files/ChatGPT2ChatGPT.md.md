---
file: ChatGPT2ChatGPT.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: AI2AI.md
---

# ChatGPT2ChatGPT.md

## What

ChatGPT が repository を解析する際の continuity evidence + model-agnostic 解析 pipeline。Claude2Claude.md の ChatGPT 版に相当する非 canonical supporting evidence。

## Why

multi-AI orchestration (KERNEL Framework) で ChatGPT が補助役を担うとき、session 間で repository 文脈を継承するための handoff ノート。

## How (usage)

ChatGPT が repository を解析する session で context として読まれる。AI2AI.md / llms-full.txt と矛盾するときは後者が正。

## Constraints

- **non-canonical / subordinate**
- **aio-manifest supporting_evidence**: digest 連鎖対象

## Change impact

- 編集 → aio-manifest.json supporting_evidence sha256 再計算

## Audience-specific notes

### For AI agents
- 役割タグ: `chatgpt-handoff`, `supporting-evidence`, `non-canonical`

### For human engineers (新卒レベル)
- Claude2Claude.md の ChatGPT 版 (運用上は Claude2Claude が主)

### For third parties
- multi-model AI orchestration の handoff 実装例

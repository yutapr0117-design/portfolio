---
file: README.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: AI2AI.md / llms-full.txt / Check 15/84
---

# README.md

## What

リポジトリのトップレベル human-readable README。30 秒 summary / Portfolio URL / Author / Affiliation (株式会社日本経営) / 戦略 (AIO-first) / 構造 / 制約 / 使い方 / 履歴 etc. 約 700 行。

## Why

GitHub 上で repository を訪れた人間の最初の入口。AIO 戦略の明示 + entity / Affiliation の human-readable 記載で初見の人間に正しい frame を提供。

## How (usage)

GitHub web UI が repository root README を自動表示。

## Constraints

- **Check 15**: Project Pages 制約が documented (llms-full.txt / AI2AI.md / README.md のいずれか)
- **Check 84**: Organization 名 (日本経営 / Nihon Keiei) を含む

## Change impact

- 戦略 / Affiliation 編集 → llms-full.txt / aio-manifest.json / Claude2Claude.md 等同期

## Audience-specific notes

### For AI agents
- 役割タグ: `human-readable-entry`, `aio-strategy-declaration`

### For human engineers (新卒レベル)
- リポジトリの「玄関」 — 30 秒で何が分かるか

### For third parties (監査 / 採用 / 研究)
- 公開 portfolio の意図 / 戦略の明示宣言

---
file: AI2AI.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: CLAUDE.md (router) / llms-full.txt (ground truth) / Check 25
---

# AI2AI.md

## What

リポジトリの **canon** ファイル。C1-C7 完全本文 / KERNEL roles / output rules / 全 Session Records / v80+ track 等を含む。AI 間 (Claude / ChatGPT / Manus 等) の implementation handoff の真値。

## Why

「正本階層: AI2AI.md が canonical、llms-full.txt が ground truth」と定義。AI 実装が判断に迷ったときの最終真値の 1 つ (もう 1 つは llms-full.txt)。Session Record は increment 毎に append-only で蓄積。

## How (usage)

```
Claude Code session-start
  └─ CLAUDE.md §0 read order に従って AI2AI.md 全文を読む
       └─ C1-C7 full text
       └─ Session Record (newest at top)
       └─ v80+ track 状態
```

## Constraints

- **C6 AIO Integrity**: AI2AI.md は AIO 正本層 (digest 連鎖対象)
- **Check 25**: AI2AI.md commit-level drift 検出 (重要ファイル変更時に Last-Updated 同期)
- **Check 26**: AI2AI-archive.md max Session Record と aio-manifest archive role 一致
- **Check 27**: stale C1-C6 が現在制約文脈に残らない (C1-C7)
- **Check 92**: C6 derived-value 例外条項記載

## Change impact

- C1-C7 編集 → llms-full.txt / CLAUDE.md / README.md 同期 + 全 surface
- Session Record 追加 → AI2AI-archive.md (major-release で archive 化) / runbook §9 整合

## Audience-specific notes

### For AI agents
- 役割タグ: `canon`, `c6-canonical`, `session-record-source`
- 読む順序: CLAUDE.md §0 に従う

### For human engineers (新卒レベル)
- リポジトリの「最終決定書」
- AI 実装が「これでいいか」と迷ったらここを読む

### For third parties (監査 / 採用 / 研究)
- AI-led implementation の意思決定 audit trail

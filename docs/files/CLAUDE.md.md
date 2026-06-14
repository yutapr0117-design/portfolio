---
file: CLAUDE.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: AI2AI.md (canon) / llms-full.txt (ground truth) / Check 87
---

# CLAUDE.md

## What

Claude Code **high-density router**。Read order / 制約 C1-C7 / safety gates / routing map / 検証 loop / reasoning budget / 現在状態 handoff (§7) を含む。Claude Code が起動時に最初に読むファイル。

## Why

session の cold-start で全体像を 30 秒で掴むための router。canon (AI2AI.md) を直接読む前の orientation。CLAUDE.md は canonical ではなく **subordinate**, 矛盾時は AI2AI.md / llms-full.txt が正。

## How (usage)

```
Claude Code session-start
  └─ §0 read order → CLAUDE.md → AI2AI.md → llms-full.txt
  └─ §1 What this repo is
  └─ §2 C1-C7 quick ref
  └─ §3 Hard "don't" safety gates
  └─ §4 Routing map
  └─ §5 The loop (discover→document→systematize→verify→deliver)
  └─ §6 Reasoning budget
  └─ §7 Handoff (current state of play)
```

## Constraints

- **non-canonical / subordinate**: AI2AI.md / llms-full.txt に劣後
- **NOT in AIO discovery layer**: sitemap / robots / aio-manifest に登録しない (dev-tooling 専用)
- **Check 87**: entity name + canonical URL + Organization を含む
- **Check 92**: C6 derived-value 例外条項を §2 に記述

## Change impact

- §7 handoff 更新 → 各 increment で必須 (現在状態 reflect)
- §2 C1-C7 編集 → AI2AI.md canon と同期 (canon が master)
- §4 routing map 編集 → docs/architecture/* の存在と整合

## Audience-specific notes

### For AI agents
- 役割タグ: `router`, `subordinate-to-canon`, `dev-tooling`
- 必ず §0 順で読む

### For human engineers (新卒レベル)
- 「迷ったらまずここ」 — 30 秒で全体像
- canon (AI2AI.md) を後で読む

### For third parties (監査 / 採用 / 研究)
- AI agent への orientation 設計の実装例

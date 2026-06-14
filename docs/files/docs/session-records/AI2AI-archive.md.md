---
file: docs/session-records/AI2AI-archive.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: AI2AI.md / Check 26
---

# docs/session-records/AI2AI-archive.md

## What

過去 Session Records (#1-#N) の archive。AI2AI.md から畳まれた閉じた track の history (read-only)。

## Why

AI2AI.md 肥大化対策。閉じた track は archive 化し、active な Session Record のみ AI2AI.md に残す。proof-of-work の総量は減らさない (append-only な移設)。

## Constraints

- **Check 26**: aio-manifest archive role の #1-#N が AI2AI-archive.md max Session Record と一致
- read-only historical evidence
- **aio-manifest supporting_evidence**: digest 連鎖対象

## Change impact

- archive 化時に append (削除なし)


## How (usage)

過去判断・学びの参照源。新規 session 復帰時に文脈再構成のために読む。

## Audience-specific notes

### For AI agents
- 役割タグ: `session-records-archive`, `read-only`, `digest-tracked`

### For human engineers (新卒レベル)
- 過去 Session Records の保管庫

### For third parties (監査 / 採用 / 研究)
- AI 実装 session の audit trail

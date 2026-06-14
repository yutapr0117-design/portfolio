---
file: docs/session-records/incident-artifacts-archive-v74.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: /archive-incidents slash command / .claude/commands/archive-incidents.md
---

# docs/session-records/incident-artifacts-archive-v74.md

## What

v74 track 完了時に集約された incident-artifacts の archive。`/archive-incidents` slash command で `cat` 連結された append-only な内容改変ゼロ archive。

## Why

major-release boundary での incident-artifacts/ folder slim 化。proof-of-work 文言は 1 バイトも改変しない。

## Constraints

- byte-equal 連結 (内容改変なし)
- `docs/session-records/` 配下 (Check 42 対象外で誤発火を避ける)

## Change impact

- 新規 archive 化時に新ファイル (incident-artifacts-archive-v8X.md) として作成


## How (usage)

過去判断・学びの参照源。新規 session 復帰時に文脈再構成のために読む。

## Audience-specific notes

### For AI agents
- 役割タグ: `incident-archive`, `v74-track-closed`, `byte-equal-concat`

### For human engineers (新卒レベル)
- v74 で閉じた track の incident-artifacts 集約

### For third parties (監査 / 採用 / 研究)
- append-only history の集約証跡

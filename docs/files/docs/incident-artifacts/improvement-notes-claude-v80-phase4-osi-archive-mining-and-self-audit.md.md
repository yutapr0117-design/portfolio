---
file: docs/incident-artifacts/improvement-notes-claude-v80-phase4-osi-archive-mining-and-self-audit.md
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-09-09
canonical-ref: AI2AI.md Session Record #35 (canon) / CLAUDE.md §7 (要点) / docs/architecture/total-check-runbook.md §9 (Check 総数の真値)
---

# docs/incident-artifacts/improvement-notes-claude-v80-phase4-osi-archive-mining-and-self-audit.md

## What

**2026-09-09 の run（PR #1511〜#1542・32 件）の経緯記録。** 一次資料から得た事実の表、
**我々の側の失敗 6 件**（#109〜#116）とその共通形、機械強制と分割の一覧、次に読むときの入口。

## Why

**Session Record #35 は「要点 + ここへのポインタ」で書かれている** ——`AI2AI.md` は
Check 365 の 1,000 行上限を持ち、run ごとに全文を書くと**次のセッションが 1 行も書けなくなる**
（2026-08-21 に実際に到達した）。**経緯はここ、規範は canon、数値は runbook §9。**

## How

- **一次資料の事実と、我々の失敗を別々の表にした** ——混ぜると、外から来た事実が
  自己批判の文脈で読まれてしまう
- **「establish すること / しないこと」を各所で分けた**（この run の中心規律）
- 数値は書かない方針の面（Check 総数など）はここでも書かず、runbook §9 を指す

## Constraints

- **NON-CANONICAL。** 規範は `AI2AI.md`、数値は runbook §9 が正
- **本文（ACD-1.0）は凍結中**。ここに書かれた errata（E11 / E12 / E13）は**すべて未修正**
- **外部の期限は書かない**（`PEER-REVIEW-WATCH.md` が権威・STATUS と同じ理由）

## Change impact

追記は可。**過去の run の記述を書き換えると履歴を偽る**ので、訂正は「訂正として」足す
（この run 自体がその形を 6 回使っている）。

## Audience-specific notes

- **監査人**: 32 PR の内訳と、各増分がどの不利な事実へ効いたかが辿れる
- **後任 AI**: **「集合の 1 つを確かめて集合について結論した」が本 run の中心**である。
  同じレンズを別の主語へ当てるのが次の一手（面は掃引済み・`BLIND-SPOTS.md`）

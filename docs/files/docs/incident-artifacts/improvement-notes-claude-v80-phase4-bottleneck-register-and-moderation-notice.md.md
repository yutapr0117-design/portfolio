---
file: docs/incident-artifacts/improvement-notes-claude-v80-phase4-bottleneck-register-and-moderation-notice.md
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-09-10
canonical-ref: AI2AI.md Session Record #36 (canon) / LICENSES/ACD-OSI-BOTTLENECKS.md (bottleneck の単一 canonical) / CLAUDE.md §7 (要点)
---

# docs/incident-artifacts/improvement-notes-claude-v80-phase4-bottleneck-register-and-moderation-notice.md

## What

**2026-09-09〜10 の run（PR #1547〜#1568・22 件）の経緯記録。**
**OSI Moderators の通知**（AI 起草投稿の拒否・#119 / B14）とその扱い、
**bottleneck register を 14 項目すべて分析付きで閉じた結果**、
**B3（長さ）の測定と結論**、機械強制に足したもの、不利な事実 3 件。

## Why

**Session Record #36 は「要点 + ここへのポインタ」で書かれている** ——`AI2AI.md` は
Check 365 の 1,000 行上限を持つため、run ごとの全文はここに置く。
**経緯はここ、規範は canon、bottleneck の権威は `LICENSES/ACD-OSI-BOTTLENECKS.md`。**

## How

- **通知の扱いは「記録して、発信だけ止める」** ——逐語は `LICENSES/rounds/`、
  分析は #119 / B14、停止は §B.0 バナー / ゲート 0 / 入口ページ / `HANDOFF.md` §0.5
- **register の結論は項目ごとに「何が establish され、何がされないか」を分けて書いてある**
- **測定は必ず「置換文を書いてから数える」**（見積もりは 42% 外れた）

## Constraints

- **NON-CANONICAL。** 規範は `AI2AI.md`、bottleneck の権威は register、数値は runbook §9
- **不利な事実を後から短くしない**（`REVISION-PROTOCOL.md` §2）
- **通知について「我々のことだ」とも「我々のことではない」とも書かない**

## Change impact

本ファイルは run の記録なので、後から事実が変わったときは**書き換えず追記する**。
**更新された Code of Conduct が公開されたら、本ファイルではなく別ファイルとして足す。**

## Audience-specific notes

- **審査者**: 通知を認識し、発信を止め、開示を薄めなかったことの経緯
- **後任 AI**: **最初に読むのは register**。本ファイルは「なぜその status になったか」の側
- **監査人**: PR 番号（#1547〜#1568）から commit 単位で追える

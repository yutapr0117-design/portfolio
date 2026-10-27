---
file: LICENSES/rounds/2026-10-25-license-review-modelgo-vote-inquiry-observed.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-10-27
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/OSI-EVENTS-2026-10.md / LICENSES/PEER-REVIEW-WATCH.md
---

# LICENSES/rounds/2026-10-25-license-review-modelgo-vote-inquiry-observed.txt

## What

`license-review` の **"ModelGo Attribution License, Version 2.0 FINAL CALL FOR COMMENTS"** スレッドの、Moming Duan 氏の 2026-10-25 の 1 通。2026-10-27 03:04 UTC に portfolio-01 が取得。
**我々宛ではなく、ACD についてでもない。** 新しい本文は冒頭の 1 行だけで、下は 9 月の議論の引用（読了済み・`review-doctrine.md` §1.123）。

## Why

FINAL CALL（締切 2026-09-24）から約 1 か月後に、**steward 自身が投票の結果を知らない**ことを本人の言葉で示す（*"Any word on the vote for MG0 and MG-BY?"*）。決定までの時間の実測（`board-decisions.md`・中央値 101 日）の側の 1 例。

**⚠ この file が establish しないこと**: 投票が行われたか／結果／遅れの理由。

## How

`https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-October.txt` を portfolio-01 が
**ブラウザ相当の UA** で取得し（受け渡し `86592ef`）、該当メッセージ・ブロックを月次ファイルからバイト列のまま切り出した
（月次ファイルの部分列であることを書き出し前に assert 済み）。

## Constraints

- **無改変で保存する**（`rounds/README.md`）。他人の誤字も直さない。
- **観測（`-observed`）であって受領ではない。**

## Change impact

- `rounds/` に file を足したら `rounds/README.md` の在庫表と件数も同じ commit で（**Check 465**）。

## Audience-specific notes

- **AI（実装者）**: 引用は逐語でこの file から取る。
- **監査人**: 取得元 URL の同スレッドと突き合わせれば再現できる。

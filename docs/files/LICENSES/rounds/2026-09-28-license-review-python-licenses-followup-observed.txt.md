---
file: LICENSES/rounds/2026-09-28-license-review-python-licenses-followup-observed.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-10-04
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/OSI-EVENTS-2026-10.md / LICENSES/PEER-REVIEW-WATCH.md
---

# LICENSES/rounds/2026-09-28-license-review-python-licenses-followup-observed.txt

## What

`license-review` の **"Python licenses: Python-2.0.1, PSF-2.0, CNRI-Python-GPL-Compatible"** スレッドの、
**2026-09-27〜28 の 3 通**（Nico Rikken 氏 / Max Mehl 氏 / Nick Vidal 氏）。2026-10-04 11:41 UTC に取得。
**我々宛ではなく、ACD-1.0 についてでもない。**

## Why

2026-09-27 05:55 UTC の取得（`PEER-REVIEW-WATCH.md` §3.9）より後に載った唯一の新着で、
**採用実績のある提出（PSF-2.0・Matplotlib が単独で使用）も約 3 週間返信ゼロ**だったことを、
提出者自身の言葉で示す（Mehl 氏 *"with no replies so far"*）。沈黙の基準率（`against.md` #109）の側の 1 例である。

**⚠ この file が establish しないこと**: 承認の日付（スレッドは「承認に感謝」と言うだけ。日付は
OSI のライセンス頁の *Approved: June 29, 2026* が権威）／2026-09-24 の理事会で何が決まったか／
PSF-2.0 の沈黙の理由（Chestek 氏の「1 ライセンス 1 メール」への言及があり、束ねた形が理由の候補だが確かめられない）。

## How

`https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-September.txt` を
**ブラウザ相当の UA** で取得し、該当 3 通のメッセージ・ブロックを月次ファイルからバイト列のまま切り出して
アーカイブ順に連結した（月次ファイルの部分列であることを書き出し前に assert 済み）。

## Constraints

- **無改変で保存する**（`rounds/README.md`）。他人の誤字も直さない。
- **観測（`-observed`）であって受領ではない。**

## Change impact

- `rounds/` に file を足したら `rounds/README.md` の在庫表と件数も同じ commit で（**Check 465**）。

## Audience-specific notes

- **AI（実装者）**: 引用は逐語でこの file から取る。
- **監査人**: 取得元 URL の同スレッドと突き合わせれば再現できる。

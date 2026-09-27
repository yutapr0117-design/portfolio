---
file: LICENSES/rounds/2019-04-license-review-cal-approval-observed-55of61.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-27
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/ACD-1.0.against.md #264
---

# LICENSES/rounds/2019-04-license-review-cal-approval-observed-55of61.txt

## What

**Cryptographic Autonomy License の承認審査**（2019-03〜2020-02・全 585 通）の
**55/61 部**。**アーカイブ中で最大の提出スレッドである。**
**我々宛ではなく、ACD-1.0 についてでもない —— 観測である。**

## Why

**ドシエは CAL-1.0 の*本文*を分析していた**（`gap-measurements.md`）**が、
その*審査*は一度も読んでいなかった** ——**「言及 ≠ 読了」**（#264）。
**委員長が反対意見を繰り返し条文と OSD へ差し戻している** ——
*"Can you explain **what OSD is not met and where you find that in the license**?"*。
**#263（OSD 適合は十分条件ではない）と対で読む。**

## How

`https://lists.opensource.org/pipermail/license-{review,discuss}_lists.opensource.org/`
から**ブラウザ相当の UA** で取得（2026-09-27）。既定の python UA は 403。

## Constraints

- **本文は無改変。** byte を変えない（`rounds/` の規約）。
- **分割は Check 365（1,000 行）のため**で、切り方は**行境界**。
  **61 部を順に結合すれば元の連続に byte 単位で戻る**（生成時に検証済み）。
- **部数が多いのは選別していないからである** ——**585 通を全部置いてある。**
  **決定権者の発言だけを抜けば 29 部に収まるが、それは「我々が選んだ」余地を作る。**
- **ここに分析を書かない**（規約 2）。読みは `ACD-1.0.review-outcomes.md` §1.122 へ。

## Change impact

この file が動くのは、**取得し直して差分が出たとき**だけである。
そのときは**書き換えず、新しい取得として別 file に置く**。

## Audience-specific notes

- **監査人**: 結末は **2020-02-14 の理事会で承認**（賛成 8・反対 0・棄権 1・欠席 2）。
- **第三者**: 他人の提出についての議論であって、ACD-1.0 への応答ではない。

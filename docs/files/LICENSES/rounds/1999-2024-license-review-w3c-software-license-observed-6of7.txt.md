---
file: LICENSES/rounds/1999-2024-license-review-w3c-software-license-observed-6of7.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-25
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/ACD-1.0.against.md #246
---

# LICENSES/rounds/1999-2024-license-review-w3c-software-license-observed-6of7.txt

## What

**W3C Software License をめぐる 25 年分のスレッド**（`license-review` / `license-discuss`・
1999〜2024・全 72 通）の **6/7 部**。件名に `W3C` を含むものを時系列で結合してある。
**我々宛ではなく、ACD-1.0 についてでもない —— 観測である。**

## Why

**Piana 氏が 2023 年に名指しした 3 件（CC0 / MXM / W3C）の最後の 1 件**であり、
**3 件のうち唯一「承認された」ものである。**

**中心は 2017 年の承認** —— W3C の弁護士が *"This is a **copyright-only license**. It makes no
statement about the presence or absence of patent claims"* と述べ、Piana 氏が
*"A license which only gives copyright licenses but refuses to do so for patents is not an open
source license in my and many others' opinion"* と反対したが、**氏は承認の保留を求めず、
2017-11-29 に承認された**（#246）。

**もう 1 つ**: 2001 年、**19 か月放置された提出**に対する OSI の答えが記録に在る ——
Nelson 氏 *"if you want it approved, and you've submitted it and haven't heard from us,
**resubmit it**."*

## How

`https://lists.opensource.org/pipermail/license-{review,discuss}_lists.opensource.org/`
から**ブラウザ相当の UA** で取得（2026-09-25）。既定の python UA は 403。

## Constraints

- **本文は無改変。** byte を変えない（`rounds/` の規約）。
- **分割は Check 365（1,000 行）のため**で、切り方は**行境界**。
  **7 部を順に結合すれば元の連続に byte 単位で戻る**（生成時に検証済み）。
- **これは 1 つのスレッドではなく、件名で束ねた 25 年分である。** 連続したメールの往復として
  読まないこと（2001 / 2005 / 2017 / 2024 は別の議論である）。
- **ここに分析を書かない**（規約 2）。読みは `ACD-1.0.review-doctrine.md` §1.112 へ。

## Change impact

この file が動くのは、**取得し直して差分が出たとき**だけである。
そのときは**書き換えず、新しい取得として別 file に置く**。

## Audience-specific notes

- **監査人**: 束ね方は「件名に `W3C` を含む」で、主題ごとに分けていない。
- **第三者**: これは他人の提出についての議論であって、ACD-1.0 への応答ではない。

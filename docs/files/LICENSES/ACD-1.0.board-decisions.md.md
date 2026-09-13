---
file: LICENSES/ACD-1.0.board-decisions.md
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-13
canonical-ref: LICENSES/rounds/2026-09-13-osi-board-meeting-minutes-2025-06-to-2026-06.txt (逐語) / LICENSES/ACD-1.0.review-corpus.md (アーカイブ全体の測定) / LICENSES/ACD-OSI-BOTTLENECKS.md (B2 / B10)
---

# LICENSES/ACD-1.0.board-decisions.md

## What

**OSI 理事会の公開議事録から読める「決定」の分析。** 承認・否決・取り下げの一覧、
記録された理由、そして理事会が述べた**方針**（AI/ML 向けライセンスの扱い / 翻訳を承認しない /
応答しない提出者の却下権限の委任 / **公表されていない第 3 の帰結**）。

## Why

**ドシエの「結果」データは 2026-09-13 まで `license-review` の告知メールだけに依っていた。**
**告知は提出型スレッドの一部にしか出ておらず**（件数は `ACD-1.0.review-corpus.md` §1.69 が権威）、
残りの帰結は不明だった。
**決定そのものは理事会で動議として記録される** ——議事録はその一次資料である。

**最も重い発見は、我々が持っていなかった状態が在ったこと** ——
*"a license could stay in a status where it is **not approved** if it is **duplicative and not used
by a project**"*（2025-07-18）。**duplicative（#84）と not-used（B2）の両方が我々に当たり、
その区別は理事会が公表を指示してから 14 か月経っても process ページに入っていない。**

## How

`https://opensource.org/minutes` の索引から全 12 回（2025-06-20〜2026-06-29）を
ブラウザ相当の UA で取得し、逐語を `rounds/` へ保存した上で分析した。

**節を足すときの行き先**: その文が**議論**なら `review-corpus.md`（アーカイブ全体の測定）か
`review-precedents.md`（個別スレッドの読み）、**決定**ならここ。

## Constraints

- **逐語の権威は `rounds/` にある。** ここは分析であり、原文を書き換えない。
- **キリル文字等を分析側に書き写さない** ——Check 450 が日本語文への別スクリプト混入を
  BLOCKING で止める（`rounds/` は無改変保存なので対象外）。名称は記述で指す。
- **公開分は不完全である**（索引ページ自身が "under construction" と述べ、最古は 2025-06-20）。
  **件数は必ず「公開されている範囲で」と限定して書くこと。**
- 予算は advisory 700（`file-size-budget.md`）。**公開議事録は毎月増えるので育つ側の file。**

## Change impact

新しい議事録を読んだら、**逐語を `rounds/` へ足し**（Check 465 が在庫申告を照合）、
分析をここへ書き、**`LICENSES/README.md` の索引**は既に行を持っているので更新不要。
件数を書き換えたら **Check 460** が自己申告の一致を見る。

## Audience-specific notes

- **AI（次のセッション）**: 帰結を数えるときは**議事録を優先せよ**（告知メールは部分集合）。
  ただし**公開分が不完全**なので母数は不明である。
- **監査人**: 各決定の日付と動議文は `rounds/` の逐語で確認できる。
- **第三者**: これは OSI の公開文書についての我々の読みであって、OSI の説明ではない。

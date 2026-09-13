---
file: LICENSES/rounds/2026-09-13-osi-board-meeting-minutes-2025-06-to-2026-06.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-13
canonical-ref: LICENSES/ACD-1.0.review-corpus.md (§1.83 が本 file の分析) / LICENSES/ACD-OSI-BOTTLENECKS.md (B10 / B2) / LICENSES/AS-OF.md (外部事実と検証日)
---

# LICENSES/rounds/2026-09-13-osi-board-meeting-minutes-2025-06-to-2026-06.txt

## What

**OSI 理事会の公開議事録を、公開されている全 12 回ぶん逐語で保存したもの**
（2025-06-20 〜 2026-06-29・`https://opensource.org/meeting-minutes/<date>`・
索引は `https://opensource.org/minutes`）。HTML タグを剥がし空白を畳んだだけで、
**語の追加・削除・並べ替えはしていない。**

**決定の在る回だけを選んでいない。** 選別すると、選んだこと自体を読者が検証できなくなる。

## Why

**このドシエの「結果」データは、それまで `license-review` の告知メールだけに依っていた。**
告知は提出型スレッド 21 件のうち 8 件しか出ておらず、**残り 13 件の帰結は不明**と記録されていた
（`review-corpus.md` §1.69）。**理事会議事録は、決定そのものが動議として記録される場所である。**

**実際、この 12 回だけで、告知から数えた 2024-01〜2026-09 の全期間よりも多くの決定が読める。**
承認も否決も**動議・提案者・second・理由**まで残っている。

## How

`https://opensource.org/minutes` の索引から `meeting-minutes/<date>` を全件列挙し、
ブラウザ相当の User-Agent で取得した（既定の python UA では 403 になる面がある）。

再取得するとき: 索引を引き直し、**公開されている回が増えていないか**を先に見ること。
**取得時点で最新は 2026-06-29 で、それ以降の理事会決定は公開されていない。**

## Constraints

- **`LICENSES/rounds/` は無改変保存のディレクトリである。** ここの byte を「直す」ことはしない。
  **Check 450（日本語への別スクリプト混入）は本ディレクトリを対象外にしてある** ——
  否決された露語ライセンス名がキリル文字のまま入っており、
  **置換すれば規約違反になるのはこちらの側だからである。**
- **公開分は不完全である。** 索引ページ自身が *"This page is under construction … If you can't
  find the minutes here, check the wiki"* と述べ、**最古が 2025-06-20**（ページ作成は 2007 年）。
  **「議事録に無い」は「決定が無かった」を意味しない。**
- 分析・解釈は本 file に書かない。**`review-corpus.md` §1.83 が分析の側**である。

## Change impact

新しい回を足すときは同じ形式で追記し、**`LICENSES/rounds/README.md` の在庫申告**も同じ commit で
更新する（**Check 465** が見出しの件数と表の行数を実 file 数と照合する）。

## Audience-specific notes

- **AI（次のセッション）**: 帰結を数えるときは**議事録を優先する**。告知メールは部分集合である。
  ただし**公開分が不完全**なので、「N 件だった」ではなく「公開されている範囲で N 件」と書くこと。
- **監査人**: 各回の URL は本文中に書いてある。取得日は header にある。
- **第三者**: これは OSI の公開文書の写しであって、我々の主張ではない。

---
file: LICENSES/ACD-OSI-BOTTLENECKS-POSTING.md
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-25
canonical-ref: LICENSES/ACD-OSI-BOTTLENECKS.md (索引・分類・集計の単一 canonical) / LICENSES/ACD-1.0.against.md #119
---

# LICENSES/ACD-OSI-BOTTLENECKS-POSTING.md

## What

**B14 —— 提出経路そのものが閉じうる**、という 1 項目だけの深い分析。
2026-09-09 に OSI Moderators が両リストへ **「AI が全部または大半を書いたと疑われる投稿は拒否する」**
と投稿して以降の経過と、そこから導かれた**行動**（投稿停止・本文凍結・リスト上でこの件を論じない）。

## Why

**`ACD-OSI-BOTTLENECKS-EXTERNAL.md` から 2026-09-25 に切り出した。引き金は advisory 予算だが、
割る線は行数ではなく主題で選んだ** —— 他の外部依存項目は **instrument の中身**についての問題で、
**B14 だけは「そもそも投稿できるか」という手続きの問題**である。読み手も判断者も違う。

**測ってから割った** —— B14 は 262 行で、切り出し前の file の 4 分の 1 を単独で占めていた。
残りは 701 行で、受け皿が即座に再び鳴ることはない（`file-size-budget.md` §2 が実測を持つ）。

## How

`ACD-OSI-BOTTLENECKS.md` の索引表が single canonical で、そこから本 file へ参照が張られる。
**索引・分類・集計はここに複製しない**（複製した瞬間に drift する）。

## Constraints

- **行動の所在はここ 1 箇所である。** 投稿の可否はオーナーの判断であり、AI は代行しない。
- **開示（`submission.md` §E.1）を薄めて回避してはならない。**
- 一次資料は `rounds/2026-09-09-license-{discuss,review}-osi-moderators-observed.txt`（無改変）。

## Change impact

B14 の status が変われば `ACD-OSI-BOTTLENECKS.md` の索引表と集計行（Check 460 face (m) が照合）も
同じ commit で動く。**本 file だけを直すと、読み手が最初に見る索引が古い状態を述べる。**

## Audience-specific notes

- **監査人**: 「何を根拠に投稿を止めているのか」はここだけを読めば足りる。
- **第三者**: **moderator の行為は OSI という組織の決定ではない。** この区別は本文が明示している。

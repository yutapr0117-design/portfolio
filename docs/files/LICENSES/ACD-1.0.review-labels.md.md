---
file: LICENSES/ACD-1.0.review-labels.md
audience: OSI license-review / license-discuss participants, licence reviewers, 監査人, 後任 AI
last-updated: 2026-09-19
canonical-ref: LICENSES/ACD-1.0.reviewer-positions.md (ここから切り出した) / LICENSES/ACD-1.0.against.md (#157 / #158 / #160 / #161) / LICENSES/ACD-OSI-BOTTLENECKS.md (B1 / B2)
---

# LICENSES/ACD-1.0.review-labels.md

## What

**リストが我々の類型に付ける「呼び名」についての記録。** 現在 2 節ある ——
**§1.98「クレヨン・ライセンス」**（誰が書いたかの label）と **§1.99「vanity license」**
（誰のためのテキストかの label）。**どちらも逐語引用と発言者と日付を持ち、
その読みが establish しないことを同じ節の中に書いてある。**

**この 2 節が運んでいる最も重いもの**は §1.98 の 1 文 —— **Licensing Committee 委員長が
「法域によって著しく異なる解釈をされる蓋然性の高さが承認に不利に働く」と述べた** CAL 審査中の発言で、
**B1 が指している害が「弁護士の不在」ではなく「予測不能な解釈」だと分かる。**

## Why

**`ACD-1.0.reviewer-positions.md` が Check 365 の 1,000 行に当たった**ので切り出した。
**ただし行数は切り出しの契機であって理由ではない。** 理由は**読む動機が違う**こと ——
他の §1.x は「**特定の人が / 特定の提出について**何と言ったか」で、
この 2 節は「**我々の類型が、その人たちの語彙ではどう呼ばれるか**」である。

## How

- **掘り方は 2 節とも同じ**: **第三者が使った語を、アーカイブ 145 か月分の corpus 全体に当てる。**
  **crayon は 15 ファイル、vanity は 10 ファイル**で実在した。
- **運んできたのは結論ではなく語だった** —— 第三者レポートの前提には事実誤りがあり
  （`against.md` #158）、**それでも語は正しく、語が最も価値の高い発見を連れてきた。**
- **節番号は動かしていない**（`§1.98` / `§1.99` への既存参照はそのまま解決する）。

## Constraints

- **逐語引用を要約に置き換えない。** 引用と、発言者と、日付と、**その読みが establish しない範囲**は
  同じ節に置く（Check 470 が引用の帰属を機械で当てる）。
- **有利な材料と不利な材料を同じ節に置く**（`feedback_always_pair_the_converse`）。
- **`#N` は不利な事実の採番だけに使う**（Check 460 face (k)）。

## Change impact

**節を足したら**: `LICENSES/README.md` の索引（Check 459）/ 予算表の 2 面（Check 52 / 424 / 443）/
本ミラー（Check 108）/ 引いた不利な事実の採番（Check 460）を同じ commit で同期する。

## Audience-specific notes

- **審査者**: ここに集めたのは**あなた方自身の言葉**である。**ACD について述べられたものは 1 通も無い。**
- **後任 AI**: **次に新しい呼び名を見つけたら、節を足す前に corpus 全体へ当てて実在を確かめること。**
  **語が実在しないなら、それは外部の推測であって、リストの語彙ではない。**
- **監査人**: 引用元は `LICENSES/rounds/` ではなく取得済みアーカイブ（145 か月）で、
  **本文中に月次ファイル名と日付が書いてある。**

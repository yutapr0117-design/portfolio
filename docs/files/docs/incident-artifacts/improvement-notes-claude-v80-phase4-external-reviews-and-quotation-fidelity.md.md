---
file: docs/incident-artifacts/improvement-notes-claude-v80-phase4-external-reviews-and-quotation-fidelity.md
audience: 後任 AI / 監査人 / OSI トラックを引き継ぐ者
last-updated: 2026-09-20
canonical-ref: AI2AI.md (Session Record #37) / LICENSES/ACD-1.0.against.md / LICENSES/ACD-1.0.errata.md
---

# docs/incident-artifacts/improvement-notes-claude-v80-phase4-external-reviews-and-quotation-fidelity.md

## What

**2026-09-19〜20 の増分記録。** 外部から届いた第三者 AI レビュー計 6 通の扱い、
逐語引用の忠実さの全数照合、そして**決め打ちの走査対象が静かに射程を失う**形の是正。

## Why

**AI2AI.md は 1,000 行の BLOCKING 上限に近い**ので、Session Record は
**要点 + 本ファイルへのポインタ**で書く規約になっている（Session Record #29 の運用メモ）。
**詳細はここに置き、canon は薄く保つ。**

## How

**不利な事実 #157〜#175 / errata E25〜E29 が一次記録**であり、本ファイルはその**読み方**を述べる。
**数や件数を本ファイルに書き写さない** ——`against.md` と `errata.md` が権威で、
**写せば必ず古くなる**（このリポジトリが何度も踏んだ形）。

## Constraints

- **ACD-1.0 / 1.1 は凍結。** 本セッションの本文変更はすべて 1.2 草案のみ
- **外部レビューの受領文は `rounds/` に無改変で置く**（PDF は Check 122 で tracked 禁止なので
  **抽出テキスト + 原本 sha256**、冒頭に「原本ではない」と明記）
- **未読の法源を引かない**（`jurisdictions.md` §9）

## Change impact

本ファイルを足したら `docs/incident-artifacts/README.md`（Check 75）と本ミラー（Check 108）を同期する。

## Audience-specific notes

- **後任 AI**: **§8「次に読む人へ」から読むとよい** ——未読のまま残した 8 件がそこにある。
- **監査人**: 各主張は `against.md` の番号へ辿れる。**本ファイルに独自の事実は無い。**

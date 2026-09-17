---
file: LICENSES/ACD-1.2-CHANGELIST.md
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-17
canonical-ref: LICENSES/ACD-1.2-DRAFT.txt / LICENSES/ACD-1.1.txt / LICENSES/ACD-1.1-CHANGELIST.md / LICENSES/ACD-1.0.errata.md
---

# LICENSES/ACD-1.2-CHANGELIST.md

## What

**ACD-1.2 に入れるものを集める単一の集約点。** 作成時点では**空**で、
**空であることが正しい状態**である（1.1 を確定した直後だから）。

## Why

**議論に付したテキストが動くと、その議論は何についてのものでもなくなる。**
1.1 を凍結して改善を別 file へ移したので、**その改善の行き先も別 file になる。**
1.0 → 1.1 の記録は `ACD-1.1-CHANGELIST.md` に残り、**動かさない。**

**集約点を 1 つにする理由は具体的である** —— 1.1 のときは入力が 4 か所以上に散っており、
**議論が終わってから 4 か所を回って集める手順は必ず落とす**（`ACD-1.1-CHANGELIST.md` の教訓）。

## How

- **入力は 3 系統**（届いた議論 / 我々の掃引 / 外から届いた測り方）で、本文の表に行き先が書いてある
- **1 つの変更は 2 か所に書く** —— 本表と、`ACD-1.2-DRAFT.txt` 冒頭の変更一覧
- **草案が自分で持ち込んだ欠陥は `ACD-1.1-SELF-AUDIT.md` へ**（版ではなく**我々の掃引**の登録簿）

## Constraints

- **`ACD-1.0.txt` / `ACD-1.1.txt` とその記述子は編集しない**（Check 453 が sha256 で止める）
- Check 459 が索引（`LICENSES/README.md`）からの到達性を、Check 461c が `last-updated` を強制

## Change impact

**表に行を足したら草案の冒頭も直す。** 片方だけ直すと**草案が自分の状態について偽を述べる**。

## Audience-specific notes

- **審査者**: 議論の対象は `ACD-1.1.txt` であり、本書はその次に何が入るかの記録である
- **後任 AI**: **空の表を「記録が無い」と読まないこと。** 空が正しい状態である

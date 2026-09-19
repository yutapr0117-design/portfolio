---
file: LICENSES/rounds/2026-09-20-external-review-ACD-1.2-clause-appropriateness.txt
audience: OSI license-review / license-discuss participants, licence reviewers, 監査人, 後任 AI
last-updated: 2026-09-20
canonical-ref: LICENSES/rounds/README.md (在庫と規律) / LICENSES/ACD-1.0.against.md (#167 / #168) / LICENSES/ACD-1.2-DRAFT.txt (レビュー対象)
---

# LICENSES/rounds/2026-09-20-external-review-ACD-1.2-clause-appropriateness.txt

## What

**2026-09-20 にオーナー経由で受領した、ACD-1.2 草案への外部レビュー（条項適切性の審査）の抽出テキスト。**

**⚠ これは原本ではない。** 原本は PDF で、**`Check 122` が PDF を tracked 禁止にしている**ため、
**本文だけを抽出して保存している**（原本の sha256 はファイル冒頭に記録）。
**改行位置・表組み・脚注番号は原本と一致しない。語の並びは保っている。**

## Why

**受領文は無改変で残す**のが `rounds/` の規律である。**PDF は置けないので、置けるもの
（語の並び）を置き、置けていないもの（byte）を明示する。** ——**「原本がある」と読まれるより、
「抽出である」と読まれる方が安全である。**

## How

PDF の FlateDecode ストリームを展開し、**各フォントの `/ToUnicode` CMap** で `Tj` / `TJ` の
グリフ列を Unicode へ写した。**⚠ 最初の実装は全フォントの CMap を 1 つの辞書へ統合しており、
日本語がすべて別の文字に化けた** ——**フォントごとに CMap は別**である。

## Constraints

- **編集しない。** 誤りが含まれていても直さない（分析は別ファイルに置く）
- **原本の sha256 を消さない** ——オーナーの手元の PDF と突き合わせる唯一の手段である
- **この 2 件を「3 件」と数えない** ——**共有された 3 ファイルのうち 2 つは byte 同一**（#168）

## Change impact

`rounds/README.md` の在庫（Check 465）と本ミラー（Check 108）を同じ commit で同期する。

## Audience-specific notes

- **審査者**: これは ACD-1.2 についての**第三者の読み**であって、我々の主張ではない。
  **欠陥の指摘は 1 件も含まれていない** ——その事実の意味は `against.md` #168 に書いた。
- **後任 AI**: **このレビューが読んだ草案には、ヘッダの破損が含まれていた**（#167）。
  **レビューはそれを 1 件も拾っていない。**

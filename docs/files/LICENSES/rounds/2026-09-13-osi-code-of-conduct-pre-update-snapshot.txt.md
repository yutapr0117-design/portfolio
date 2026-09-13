---
file: LICENSES/rounds/2026-09-13-osi-code-of-conduct-pre-update-snapshot.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-13
canonical-ref: LICENSES/AS-OF.md (外部事実と検証日) / LICENSES/ACD-OSI-BOTTLENECKS.md B14 / LICENSES/ACD-1.0.against.md #119
---

# LICENSES/rounds/2026-09-13-osi-code-of-conduct-pre-update-snapshot.txt

## What

**OSI の Mailing List Code of Conduct の全文スナップショット（2026-09-13 取得・769 語）。**
ページの自己申告は *"Page created on November 19, 2007 | Last modified on November 2, 2023"* で、
**本文に AI への言及は 0 件**である。sha256 を header に記録してある。

## Why

**2026-09-09 の moderator 通知が、この文書を *"will be updated to better reflect the use of AI"* と
予告している。** 更新が行われた瞬間、**我々の 2 通（2026-08-26 / 2026-09-06）が送られた時点で
効力を持っていた本文は、live ページから取得できなくなる。**

**そして、この repository は「保存済み」と記録しながら保存していなかった。**
`AS-OF.md` は 2026-09-09 に *"Respect time and attention"* 節を引用し、まさに上の理由を書いていたが、
**保存されたのは 1 節の引用だけで、文書そのものは無かった** ——
**`against.md` #82 と同じ形（「それについての文書」は持っていたが「文書」は持っていなかった）。**
2026-09-13 に全文を取得して閉じた。**予告された更新は、この時点でまだ行われていない。**

## How

HTML から script/style を除去し、block タグを改行にして text 化した。
**本文はページ自身の "Page created on …" 行から始まり、footer の "Get involved" の直前で終わる。**
**その上のサイト共通ナビゲーションは含めていない** ——全ページに現れるため、その語
（例 "Open Source AI"）を本文の語として数えてしまう事故が既に 1 度起きているからである
（`BLIND-SPOTS.md` 2026-09-11）。**初版の header は取得していない日付を書いており、同日に作り直した。**

## Constraints

- **第三者のページのスナップショットである。** 我々の著作物ではない
  （OSI はサイト内容を CC BY 4.0 としている）。**評価や注釈を本文に混ぜない。**
- **これを根拠に誰かの行為を性格づけない。** 本 file は「その日に何が書かれていたか」だけを示す。
- Check 465 が `rounds/README.md` の在庫申告を実 file から導出して照合する。

## Change impact

更新後に差分を取る唯一の基準である。**消すと、更新前後の比較ができなくなる。**
本文を編集すると sha256 が合わなくなり、スナップショットとしての意味が失われる。

## Audience-specific notes

- **AI（次のセッション）**: **更新が行われたら、この file と新しい本文を突き合わせ、
  差分を `AS-OF.md` と B14 に記録する。** 差分を見る前に予測を書かない。
- **監査人**: header の sha256 で本文の同一性を確認できる。取得日と URL も header にある。
- **第三者**: この文書は、通知（2026-09-09）が援用した *"Respect time and attention"* の
  **更新前の文言**を含む。

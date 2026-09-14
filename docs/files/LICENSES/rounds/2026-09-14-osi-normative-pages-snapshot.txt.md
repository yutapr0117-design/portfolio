---
file: LICENSES/rounds/2026-09-14-osi-normative-pages-snapshot.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-14
canonical-ref: LICENSES/AUDIT-LEDGER.md (§6 が第 3 の source class を記録) / LICENSES/AS-OF.md (外部事実と検証日) / LICENSES/ACD-1.0.against.md (#143)
---

# LICENSES/rounds/2026-09-14-osi-normative-pages-snapshot.txt

## What

**我々が「基準」として引いている規範ページ 5 件の、2026-09-14 時点の全文。**
OSI の License Review Process / 拒否理由の一覧 / Open Source Definition /
Open Source AI Definition、および REUSE Specification 3.3。

## Why

**敵対的検証（`AUDIT-LEDGER.md` §6）が、ドシエの依拠する source に第 3 の class を見つけた。**
1 つ目はメーリングリストのアーカイブ（#143）、2 つ目は理事会議事録（2026-09-13 に保存）、
**3 つ目がこれ** —— **仕様書と web ページ。**

**アーカイブを何か月取っても出てこない**（メッセージではないから）し、
**メッセージと違って予告なく変わる。**

**それは仮定の話ではない。** 理事会は **2025-07-18** に「reject と not approved の区別を
process ページへ公表せよ」と指示し、**2026-01-16** にも「non-commercial は取り下げになると明記せよ」と
指示している。**この snapshot の時点でどちらも入っておらず**、process ページの自己申告は
**"Last modified on March 13, 2024"** のままである。
**将来この文が在るのを見た読み手は、この file が無ければ「我々の分析が誤っていた」のか
「ページが後から動いた」のかを区別できない。**

## How

ブラウザ相当の User-Agent で取得し、HTML タグを剥がして空白を畳んだ。**語は足しても削ってもいない。**
各節の冒頭に **URL とページ自身が名乗る last modified** を書いてある。

## Constraints

- **これは「現在のページ」の主張ではない。** **ある 1 日に何と書いてあったか**の記録である。
  **いまも同じことを言っているかは、取り直して比べる** —— 仮定しない。
- `LICENSES/rounds/` は無改変保存のディレクトリ。**Check 450 の対象外**（他人のテキストを含む）。
- **アーカイブ全月をここへ入れてはいけない**（`AUDIT-LEDGER.md` §2 の判断）。
  **規範ページを入れるのは別**: 小さく、**基準を定義しており**、**版が動く**。

## Change impact

**版が動いたら、新しい日付で新しい snapshot を足す**（上書きしない ——差分が読めなくなる）。
`rounds/README.md` の在庫申告も同じ commit で更新する（**Check 465**）。

## Audience-specific notes

- **AI（次のセッション）**: 承認基準について何か書く前に、**この snapshot と現在のページを比べる。**
  **「基準はこうである」と書くときは、いつ見た基準かを添える。**
- **監査人**: 各節の URL と自己申告日付で、取得時点の同一性を確かめられる。
- **第三者**: これは OSI / REUSE の公開文書の写しであって、我々の主張ではない。

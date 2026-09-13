---
file: .github/scripts/verify_dossier_quotations.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-14
canonical-ref: LICENSES/AUDIT-LEDGER.md (結果の台帳) / LICENSES/rounds/README.md (一次資料の保存規約)
---

# .github/scripts/verify_dossier_quotations.py

## What

**ドシエが外部に帰属させた英語の逐語引用が、実在の source に在るかを照合する道具。**
`LICENSES/*.md` から `*"..."*` 形式・人名の近傍・英語・5 語以上の引用を集め、
`rounds/` の一次資料・ライセンス本文・取得済みアーカイブと突き合わせる。

## Why

**引用が現物と違う提出は、審査者が最初に気づく種類の誤りである。**
そして本リポジトリの規律は *「我々の読みは誤りうるが、何と言われたかの記録は誤ってはならない」* と
述べている —— **その規律を、宣言ではなく実測で確かめるため。**

初回実行（2026-09-14）: **母数 251 / 確認済み 156。最も重い 5 件は逐語で一致し、誤引用は 0 件。**

## How

```
python3 .github/scripts/verify_dossier_quotations.py           # 手元の source だけで照合
python3 .github/scripts/verify_dossier_quotations.py --fetch   # 不足月を導出して取得し再照合
```

取得先は `$DOSSIER_ARCHIVE_CACHE`（既定 `/tmp/arc`）。**不足月は、未確認の引用の近傍にある
日付から導出する** —— 全月を取りに行かない。

## Constraints

- **CI に入れない（意図的）。** 検証に外部アーカイブの取得が要り、CLAUDE.md §7 が
  「自動監視は CI に入れない（外部フォーラムの定期取得は壊れやすい）」と定めている。
  **これは手で回す道具であって Check ではない。**
- **「未確認」は「誤り」ではない。** 我々自身の文を強調で括ったものと、未取得の月が混じる。
  **分類してから結論すること。**
- **母数が大きすぎるときは、母数の作り方が間違っている。** 初版は 4,976 件を数え、
  大半が markdown の太字記法だった（履歴は script の docstring に残してある）。

## Change impact

`NAME` の人名リストは**下限であって全数調査ではない**（#87）。増やすときは、
増やした結果で母数がどう動いたかを `AUDIT-LEDGER.md` に書くこと。

## Audience-specific notes

- **AI（次のセッション）**: 結果を台帳へ貼るときは**道具の出力をそのまま**貼る。手で数えない。
- **監査人**: 同じコマンドで同じ数が出る（アーカイブ取得分を除き決定的）。

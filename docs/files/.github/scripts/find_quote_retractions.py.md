---
file: .github/scripts/find_quote_retractions.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-06
canonical-ref: .github/scripts/verify_dossier_quotations.py (引用の集め方と正規化を共有する) / LICENSES/AUDIT-LEDGER.md (手で回す道具の結果の置き場)
---

# .github/scripts/find_quote_retractions.py

## What

**ドシエが引く発言のうち、同じ差出人が後で取り消した可能性があるものを洗い出す手動の道具。** 逐語引用をアーカイブのメッセージへ解決し、同じ差出人の同じスレッドの後続メッセージ（45 日以内）に撤回の語があるものを出す。

## Why

2026-11-06 に、不利な事実として 2 か月数えていた Piana 氏の発言を本人が同じ日に撤回していたと分かった。掃引は発言の語で探していたので、撤回の文を拾えなかった。引用は発言した時点の記録で、その後の取り消しは引用の側から見えない。

## How

```sh
DOSSIER_ARCHIVE_CACHE=~/osi-archive-cache python3 .github/scripts/find_quote_retractions.py
```

月次アーカイブが要る。無ければ `verify_dossier_quotations.py --fetch` で同じ場所へ取る。

## Constraints

- **Check ではない。** アーカイブの取得が要るので CI に入れない。
- **出すのは候補である。** 撤回かどうかは人が読んで決める（"correct me if I am wrong" のような言い回しも拾う）。
- **出なかったことは撤回が無かった証拠ではない。** 解決できない引用（アーカイブ以外の出典や省略の多い引用）、別のスレッドでの訂正、語の一覧に無い言い方は見ていない。解決できなかった件数を必ず出す。

## Change impact

撤回の語を足すときは `RETRACT` を直す。引用の集め方は `verify_dossier_quotations.py` の `collect_quotes` に従う。

## Audience-specific notes

- **AI**: 候補は register の担当へ渡し、読まずに不利な事実を消さない。
- **監査人**: 2026-11-06 の結果は引用 616 件を解決し、307 件は解決できず、候補 7 件だった。

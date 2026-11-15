---
file: .github/scripts/sync_stated_counts.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-15
canonical-ref: .github/scripts/_lib_draft_counts.py (length_sites・場所の一覧の単一の出所) / .github/scripts/checks_license_self_reporting.py (Check 460 (x))
---

# .github/scripts/sync_stated_counts.py

## What

実測から導ける「書かれた数」を、手で直さずに書き直す手回しの道具。引数なしで回すと、実測と違う場所を出し、違いがあれば exit 1 で終わる。書き換えはしない。`--apply` を付けると書き換える。

いま書き換える場所は、草案の語数から導出する数である。

- 草案冒頭の "ACD-前版: N words, M clauses. This draft: N words, M clauses."
- CHANGELIST の「前版の N 語から +N 語」「1.0 の N 語から見ると M 語長い」「（束名、束名の N 束で +M）」と、英文の "N words from the title to *END OF TERMS* against 1.0's N, in M clauses against M"
- B3 の見出しのかっこ
- SUBMISSION-MATERIALS の長さの行（後半の「条文では N 語長いまま」を含む）

2026-11-15 に、ドシエの規模の数も足した（30 の依頼・`_lib_dossier.count_sites`）。不利な事実の件数（against の総括・REVIEWERS・READY-TO-SUBMIT・§4c）、errata の件数（against・REVIEWERS・READY-TO-SUBMIT・errata 冒頭の英語の数詞と閉じた番号の一覧）、worked entries の総数（REVIEWERS・QUESTION-INDEX）。不利な事実を 1 行足すたびに 6〜7 か所を手で直していた。これらは file 全体の位置で読む（Check 460 (e) と同じく、語の間の改行を越える）。書き換えたあとは `npm run status` で STATUS.md も作り直す。

## Why

1c は草案の語数が変わるたびに 7 か所を手で直していた。2026-11-15 には、同じ日に 263→281 の誤りと 597 の直し忘れが起きた。Check は「書かれた数と実測が違う」と言えるが、直すのは人だった。照合（Check 460 (x)）と書き換え（この道具）は、同じ場所の一覧 `_lib_draft_counts.length_sites` を読む。別々の正規表現を持つと食い違うからである。

## How (usage)

```bash
python3 .github/scripts/sync_stated_counts.py          # 違う場所を出す
python3 .github/scripts/sync_stated_counts.py --apply  # 書き換える
```

試作を採る commit で、草案を直したあとに `--apply` を回す。その後に残る Check 468 / 498 (k) の赤は、判断の数（箇条の語数・束の表・CHANGELIST の主表）である。

## Constraints

- 判断の数は書き換えない。束の表の各行と、草案冒頭の箇条の (+N words.) がそれに当たる。どの変更に何語かは人が決め、Check 468n が照らす。
- 外向きの行は「N.M 草案は」から、最初の日付つきの追記の手前までを読む。後ろは当時の記録なので書き換えない。「条文では N 語長いまま」だけは現在形の主張なので、行のどこでも書き換える。
- 数の書き方（3 桁区切り・符号・全角のマイナス）は元の書き方を保つ。

## Change impact

- 場所を足すときは `length_sites` に足す。Check 460 (x) も同じ一覧を読むので、照合も同時に広がる。
- 30 の依頼（不利な事実の件数）と 2f の依頼（runbook §9 の数）も、同じ形で場所の一覧に足す予定。

## Audience-specific notes

### For AI agents（次担当）

- 数を手で直す前に、この道具を回す。

### For human engineers（新卒レベル）

文書の中に書いた「草案は何語か」「GPL-3.0 より何語短いか」を、草案を数え直して自動で更新する道具。

### For third parties / auditors

書き換える数は、同じ場所を照らす Check 460 (x) / 468 / 498 (k) の照合の対象と同じである。

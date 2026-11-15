---
file: .github/scripts/record_read.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-15
canonical-ref: LICENSES/READ-THREADS.txt (census の「読んだ」の唯一の源) / LICENSES/AS-OF.md (「未読スレッドの残り」) / LICENSES/READ-THREADS-LOG.md (読了の記録)
---

# .github/scripts/record_read.py

## What

スレッドを読んだ記録を 4 か所へ 1 回で通す手回しの道具。

1. `READ-THREADS.txt` に「会話の始まりの日付<TAB>件名」の行を、日付の位置へ 1 行だけ差し込む。会話を読んだときだけで、`--no-thread` なら足さない。
2. `census_decision_statements.py threads --pin` を回し、候補・読了・残りの数を得る。
3. `AS-OF.md` の「未読スレッドの残り」のセルの日付・件数・「直近の 1 件」を入れ替える。
4. 前の「直近の 1 件」を `READ-THREADS-LOG.md` の先頭（今日の見出しの下）へ下ろす。

`--dry-run` は何も書かない。その場合の件数は、行を足す前の数である。

`--log-only`（2026-11-15・2f の依頼）は、AS-OF の直近の 1 件を動かさず、LOG の今日の見出しの下に 1 項目を足す。読んだが新しい論点の無い会話を、まとめて 1 項目にする場合などに使う。件数は直す。候補の数が変わったとき（候補の外の会話を読んだとき）は、項目の末尾に「（候補は X → Y・読んだので母数に入った）」を書き足す。

## Why

2f は読了のたびに同じ 4 段を手で書き、毎回同じ python を書き直していた（2026-11-15 の依頼）。Check 498 (h) は AS-OF の件数を READ-THREADS と THREAD-CANDIDATES から導出して照らすので、1 と 3 の食い違いは RED になる。この道具は 4 段を同じ実行の中で済ませる。

## How (usage)

```bash
DOSSIER_ARCHIVE_CACHE=~/osi-archive-cache python3 .github/scripts/record_read.py \
  --start 2018-06-04 --subject "Some notes for license submitters" \
  --entry '"Some notes for license submitters"（`license-review` 2018-06）を `review-readings-2.md` §1.224 へ（…）'
```

## Constraints

- census を回すので、アーカイブの写しが要る（Mac の `~/osi-archive-cache`）。
- READ-THREADS の既存の行は並べ直さない。全体を並べ直すと同じ日付の行の順が動き、試しの差分が 31 行になった。
- AS-OF のセルの形（「（直近の 1 件: …）。 **それより前の」）が変わったら止まる。

## Change impact

- AS-OF のセルの文の形を変えるときは、この道具の正規表現も直す。

## Audience-specific notes

### For AI agents（次担当）

- 書いたあとに verify で Check 498 (h) を確かめる。

### For human engineers（新卒レベル）

「どのスレッドを読んだか」の記録を、4 つのファイルへ同時に書き込む道具。

### For third parties / auditors

件数は census の出力そのもので、手で数えていない。

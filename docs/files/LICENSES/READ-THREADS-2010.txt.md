---
file: LICENSES/READ-THREADS-2010.txt
audience: ai, 監査人
last-updated: 2026-11-16
canonical-ref: LICENSES/READ-THREADS.txt / .github/scripts/census_decision_statements.py（read_rows・read_threads_file_for）
---

# LICENSES/READ-THREADS-2010.txt

## What

ドシエが読んだ `license-review` / `license-discuss` の会話のうち、2010 年以後に始まったものの一覧（1 行 1 会話・会話の始まりの日付<TAB>件名）。2009 年までは `READ-THREADS.txt`。

## Why

`READ-THREADS.txt` は 941 行になり、1,000 行の上限（Check 365）まで 59 行だった（2026-11-16・portfolio-50 の報告。この日だけで候補の外の読みが約 90 行増えた）。読了は減らない記録なので、会話の始まりの年で 2 つに分けた（2009 年まで 542 行・2010 年以後 377 行）。

## How

読む側（census の threads・Check 498 (h)・sync_stated_counts・prepare_version_freeze の gate 6c）は、`census_decision_statements.read_rows()` で `LICENSES/READ-THREADS*.txt` を全部読む。書く側（`record_read.py`）は `read_threads_file_for(start)` で年から file を選び、重複は全 file で照らす。

## Constraints

行は始まりの年に合う file に置く（Check 498 (h) が、違う file の行を RED にする —— 書く file の中だけを見る重複の照合をすり抜けるため）。消さない。

## Change impact

`AS-OF.md` の「未読スレッドの残り」の行の M は、両方の file の行から数える。

## Audience-specific notes

- **AI / 後任**: また 1,000 行に近づいたら、`READ_THREADS_SPLIT` を年の列に広げる（`READ-THREADS-2020.txt` など）。読む側は glob なので、変えるのは read_threads_file_for だけ。

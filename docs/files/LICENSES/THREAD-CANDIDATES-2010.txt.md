---
file: LICENSES/THREAD-CANDIDATES-2010.txt
audience: ai, 監査人
last-updated: 2026-11-16
canonical-ref: LICENSES/THREAD-CANDIDATES.txt / .github/scripts/census_decision_statements.py（candidate_rows・split_file_for）
---

# LICENSES/THREAD-CANDIDATES-2010.txt

## What

census（`census_decision_statements.py threads`）の候補の会話のうち、2010 年以後に始まったものの一覧（1 行 1 会話・会話の始まりの日付<TAB>件名）。2009 年までは `THREAD-CANDIDATES.txt`。

## Why

`THREAD-CANDIDATES.txt` は 846 行で、決める側（DECIDERS）を 1 人足すと一度に数十行増える（Taylor 氏を足していれば +31）。900 行を待つと 1 回の追加で上限の 1,000 行（Check 365）に届きうるので、READ-THREADS と同じ日に同じ型で年で分けた（2026-11-16・portfolio-50 の勧め。2009 年まで 479 行・2010 年以後 349 行）。

## How

読む側（census の固定・Check 498 (h)・sync_stated_counts・gate 6c・record_read の --start の照合）は `candidate_rows()` で両方を読む。`--pin` は行を始まりの年の file へ、それぞれの見出しを残して書く（全行を書き直して byte 一致することを確かめた）。

## Constraints

行は始まりの年に合う file に置く（Check 498 (h) が RED にする）。一度候補になった会話は外さない。

## Change impact

AS-OF の「未読スレッドの残り」の N は、両方の file の行から数える。

## Audience-specific notes

- **AI / 後任**: 年の境（`READ_THREADS_SPLIT`）は READ-THREADS と共通。変えるときは両方の一覧を同じ commit で移す。

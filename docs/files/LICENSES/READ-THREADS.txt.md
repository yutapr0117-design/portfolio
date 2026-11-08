---
file: LICENSES/READ-THREADS.txt
audience: ai, 監査人
last-updated: 2026-11-09
canonical-ref: LICENSES/AS-OF.md（「未読スレッドの残り」の行）/ .github/scripts/census_decision_statements.py
---

# LICENSES/READ-THREADS.txt

## What

ドシエが読んだ `license-review` / `license-discuss` のスレッドの件名の一覧（1 行 1 件名・最初の通の日付つき）。

## Why

AS-OF の「未読スレッドの残り」は手で数えていた。読んだ件名を 1 か所に置けば、道具（`census_decision_statements.py threads`）が候補と突き合わせて、読んだ数と残りを自分で出せる。

## How

2026-11-07 の 23 束（344 スレッド）と、その後に読んだ 24 スレッドの件名を、スレッドの一覧（件名と最初の通の日付）から取った。1 つのスレッドが 2 つの綴りの件名で出ているもの（1 件）は 2 行になる。

## Constraints

スレッドを読んだら、その commit で行を足す。消さない（読んだ記録である）。

## Change impact

`AS-OF.md` の「未読スレッドの残り」の行と、道具の `threads` の出力がこの file を数える。

## Audience-specific notes

- **監査人**: 各行の件名は公開アーカイブの月で引ける。どの節で読んだかは AS-OF の同じ行に書いてある。

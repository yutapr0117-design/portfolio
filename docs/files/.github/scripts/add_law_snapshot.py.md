---
file: .github/scripts/add_law_snapshot.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-19
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / .github/scripts/sync_stated_counts.py (runbook §9 の数を書き直す)
---

# .github/scripts/add_law_snapshot.py

## What

法令の条を WebFetch で取得した逐語の片を、`LICENSES/rounds/<日付>-<slug>-snapshot.txt` に写しとして置く一式（写し・mirror doc・
rounds/README の在庫表の 1 行・runbook §9 の数）を 1 回で行う手回しの道具。ヘッダに取得の日時 (UTC)・URL・取得した条・本文の
sha256・当てる 1.4 草案の条を書く。

## Why

2026-11-20 の 5 人の分担（関連法令の一次資料を読む）で、法令の写しを多く置く。それまでの写し（2026-11-16〜18 の約 20 本）は
手で置かれ、取得の時刻・条の範囲・本文の hash が無く、「どの文をいつどの条だけ取ったか」を後から確かめられなかった。

## How

取得はこの道具の外で行う（自走では curl などの直接取得が許されていない）。条ごとに `===== <法令の名> <条> (<見出し>) =====` で
区切った本文ファイルを作り、`--articles` と区切りの見出しを照らして、挙げたのに無い条・挙げていない区切り・逐語の片の無い区切りが
あれば止まる。`--clauses` の条が作業中の版の草案（凍結した版は外す）に無ければ止まる。`--dry-run` は何も書かない。

## Constraints

写しはバイト単位の写しではない（道具がモデルを通して返す）ので、ヘッダの Form にそう書き、sha256 は写しの本文の hash で原文の
hash ではないと明記する。1,000 行を越える写しは止まる（Check 365）。

## Change impact

写しの名を §18 の行・jurisdictions の段に書く。rounds/README の在庫表の形（日付の列）を変えたら、差し込みの位置の計算を直す。

## Audience-specific notes

- **監査人**: ヘッダの URL から原文を開き、片を当てて確かめられる。

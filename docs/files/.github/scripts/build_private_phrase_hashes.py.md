---
file: .github/scripts/build_private_phrase_hashes.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-07
canonical-ref: LICENSES/rounds/README.md (例外節) / .github/scripts/private_phrase_hashes.txt (一覧) / .github/scripts/checks_license_references.py (Check 492)
---

# .github/scripts/build_private_phrase_hashes.py

## What

私信の本文を repo に書かず、8 語の連なりの hash を一覧へ足す手動の道具。Check 492 が使う関数も持つ。

## Why

第三者との private off-list correspondence は本文を公開しない。それでも逐語引用が分析の文書へ残り、手の掃引は mirror doc を直して元の script を見落とした（2026-11-07）。語が tree へ戻ったことを機械で止める。

## How

```sh
DOSSIER_ARCHIVE_CACHE=<cache> python3 .github/scripts/build_private_phrase_hashes.py <repo の外の本文>
```

公開の一次資料と今の tree に在る連なりは足さない。steward 本人の文と公開の通知の文を止めないためである。

## Constraints

- 本文は repo の外に置く。一覧と誤りの文に本文を出さない。
- 新しい私信が届いたら stub を置くときに回す。
- 語を入れ替えた要約は当たらない。見るのは 8 語が同じ順で続く逐語だけである。

## Change impact

`WIDTH` を変えると一覧の全件が無効になるので、本文から作り直す。

## Audience-specific notes

- **AI**: Check 492 が RED になったら、逐語を要約へ置き換える。一覧から hash を消して黙らせない。
- **監査人**: hash から本文は読めないが、推測した文の一致は確かめられる。

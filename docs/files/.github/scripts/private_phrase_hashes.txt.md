---
file: .github/scripts/private_phrase_hashes.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-07
canonical-ref: .github/scripts/build_private_phrase_hashes.py (作る道具) / LICENSES/rounds/README.md (例外節)
---

# .github/scripts/private_phrase_hashes.txt

## What

私信の 8 語の連なりの hash の一覧。本文は含まない。

## Why

Check 492 が tree を走査して照合する。本文を repo に置かずに、語が戻ったことを見るため。

## How

`build_private_phrase_hashes.py` が更新する。手で編集しない。

## Constraints

- 一覧から hash を消して RED を黙らせない。
- 1 行に 8 件を置く（Check 365 の 1,000 行上限のため）。

## Change impact

連なりの幅を変えると全件が無効になる。

## Audience-specific notes

- **監査人**: 2026-11-07 の作成時、一覧の全件について tree の当たりは 0 件だった。

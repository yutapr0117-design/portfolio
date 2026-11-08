---
file: .github/scripts/checks_license_stated_counts.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-08
canonical-ref: .github/scripts/check_repository_consistency.py (CHECK_SOURCE_FILES と run 呼び出し) / .github/scripts/checks_license_self_reporting.py (Check 460)
---

# .github/scripts/checks_license_stated_counts.py

## What

**Check 498**: ドシエの自己申告の文が持つ 2 つ目の数と、隣の文が繰り返す同じ数が、1 つ目と同じ実測に一致することを見る。errata の冒頭、comparison §1.35、FAQ の mirror、提出参考資料 §4c、register の集計行、逐条リファレンス、submission.md の分冊の 7 面。

## Why

2026-11-08 の Check の監査で、Check 460 の面は自己申告の文の最初の数しか読んでいないことが分かった（findings #114〜#123）。1 つ目だけを直して 2 つ目を残すと、緑のまま偽の数が残る。導入した時点で submission.md が「three files」と述べ、worked entry 13 件を持つ `-boilerplate` を名指していなかった。`checks_license_self_reporting.py` は予算の縁にあるので別の module に置いた。

## How (usage)

`check_repository_consistency.py` が `run(_ctx)` で呼ぶ。単体では走らせない。数の綴り語は `checks_license_self_reporting._NUM_WORDS` を使う。

## Constraints

- **文が読めないことも RED にする**: 言い換えると何も比べずに緑になる形を残さない
- 「構造的拒否候補」は分類の列に凡例の `12`（構造的に両立不能の可能性）を持つ行の数として数える（portfolio-00 の定義）

## Change impact

- 対象の文を言い換えたら、この module の正規表現を同じ commit で直す

## Audience-specific notes

### For AI agents
- 役割タグ: `check-module`, `license`, `self-reporting`

### For human engineers (新卒レベル)
- 「同じ文の中の 2 つ目の数」は、1 つ目を直した人の目から外れやすい

### For third parties (監査 / 採用 / 研究)
- 審査者が読む面の数が、繰り返しの箇所まで実測と一致していることの機械強制

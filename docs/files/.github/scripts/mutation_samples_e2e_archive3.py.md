---
file: .github/scripts/mutation_samples_e2e_archive3.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-08-20
canonical-ref: .github/scripts/mutation_samples.py / .github/scripts/mutation_samples_e2e_archive2.py / .github/scripts/rotate_mutation_samples.py
---

# .github/scripts/mutation_samples_e2e_archive3.py

## What

behavior (e2e) mutation の **3 番目の archive**。`mutation_samples.py` の hot log から
rotate された古い entry を保持する。

## Why

**archive も無限には伸ばせない。** hot log を rotate する先が伸び続ければ、いずれ archive 自身が
Check 365 の 1,000 行上限に当たる（2026-08-20 に archive2 が 1,013 行で実際に到達）。
consistency 側（`mutation_samples_archive` / `archive2`）と同じ **2 段構成**をここでも採る。

## How (usage)

新規 mutation は `mutation_samples.py` の tail へ追記し、advisory（975 行）を超えたら
`npm run rotate-mutations` で archive2 へ rotate する。archive2 が上限に近づいたら、
その最古の連続ブロックをこの archive3 へ移す。

`E2E_MUTATIONS` は `ARCHIVE3 + ARCHIVE2 + ARCHIVE + _E2E_TAIL` の順で連結される。

## Constraints

- **Check 430**: 連結済みリスト長 == 構成要素長の合計（**代入行より後の `.append` は反映されない**）
- **Check 362 / 379 / 380 / 420**: find-anchor / test-field / find≠replace / find の一意性
- **Check 365**: 1,000 行上限（この archive も例外ではない）

## Change impact

- 連結順を変えると mutation の実行順が変わる（probe の shard 分割は index 基準なので影響する）
- 新しい archive を足すときは `mutation_samples.py` の import と連結式の両方を更新する

## Audience-specific notes

### For AI agents
- 役割タグ: `meta-qa`, `mutation-archive`, `log-rotation`
- 分割は **brace-aware** に行う（文字列リテラル内の `}` を数えるとファイルが壊れる）

### For human engineers (新卒レベル)
- 「増え続けるログは、置き場所を増やすだけでは解決しない」ことの実例

### For third parties
- 無限に伸びる append-log を多段 rotation で運用可能に保つ実装例

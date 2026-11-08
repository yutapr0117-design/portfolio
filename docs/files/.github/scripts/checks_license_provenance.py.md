---
file: .github/scripts/checks_license_provenance.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-08
canonical-ref: .github/scripts/check_repository_consistency.py (CHECK_SOURCE_FILES と run 呼び出し) / LICENSES/ACD-1.0.submission.md §E.1
---

# .github/scripts/checks_license_provenance.py

## What

来歴の開示 (誰が起草し、誰が方向を決めたか) を見る Check 群: **473** (否定の半分だけで現れない) / **473b** (2026-09-23 に否定された文が現在形で残らない・目的の出所が主要な面に在る) / **473c** (`rounds/` の規約と stub の整合)。

## Why

2026-11-08 の Check の監査で 473 / 473b を強めた結果、元の `checks_license_submission.py` が 914 行になり、Check 52 の advisory 900 を超えた。来歴の開示は他の Check と変数を共有しない塊なので切り出した。

## How (usage)

`check_repository_consistency.py` が `run(_ctx)` で呼ぶ。単体では走らせない。

## Constraints

- **肯定の半分を同じ段落に置く**: 「人間は起草を指示していない」だけを書くと、人間の関与を実際より小さく述べる。方向を人が決めたことを同じ段落に書く
- **免除は欠陥の記録に限る**: 訂正の注一般は免除しない

## Change impact

- 来歴の文の書き方を変えたら、否定の句と肯定の句の一覧をここで見直す

## Audience-specific notes

### For AI agents
- 役割タグ: `check-module`, `license`, `provenance`

### For human engineers (新卒レベル)
- 言い回しの片側だけが残ることを防ぐ Check の例

### For third parties (監査 / 採用 / 研究)
- AI 起草の開示が、人間の関与を過小にも過大にも述べないことの機械強制

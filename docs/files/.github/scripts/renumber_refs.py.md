---
file: .github/scripts/renumber_refs.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-24
canonical-ref: LICENSES/CLAUSE-MAP-1.4-1.5.tsv (条の対応) / LICENSES/ACD-1.5-CHANGELIST.md (合議の記録・議題 20)
---

# .github/scripts/renumber_refs.py

## What

提出対象を替える日に、ドシエの条番号を CLAUSE-MAP で書き換える下書き。引用を one（行き先が 1 つ）・many・gone・versioned（同じ文の手前で版を名乗る）・quoted（引用の中）に分け、`--apply` は one だけを書き換える。

## Why

1.5 は番号を総替えした。提出対象を 1.4 から 1.5 へ替えると、入口・材料・想定問答の約 2,000 の条番号が別の条を指す。手で直すと、1 対 1 の行で写し間違え、1 対 n の行で判断を落とす。

## How (usage)

```bash
python3 .github/scripts/renumber_refs.py 1.4 1.5 LICENSES/ADOPTING.md
python3 .github/scripts/renumber_refs.py 1.4 1.5 --apply LICENSES/ADOPTING.md
```

終了コード: many か gone が残れば 1、無ければ 0、対応表を読めなければ 2。

## Constraints

- 番号しか見ない。条の中身が変わった文（言い換え）が新しい条についても真かは、人が読む。
- 版の名乗りは同じ文の手前だけを見る（。 ; | で切る）。名乗りが前の文に在る引用は one に数えるので、下書きを読んでから `--apply` する。

- 提出対象を替える日に、読み終えた file だけ frontmatter の `clause-numbers` を新しい版にする（Check 472q が、提出側の面の名乗りを SUBMISSION-TARGET と照らす）。書き換えた file に当て直すと 2 度写すので、残りの many / gone は書き換える前の版に当てて数える（`git show <直前>:LICENSES/…`）。

## Change impact

文書を書き換えるのは `--apply` のときだけ。書き換えた後は 470・470b・470c・472・471 が条番号と引用を照らす。

## Audience-specific notes

- **新卒**: 一覧の [many] と [gone] の行だけを人が決める。
- **監査人**: 書き換えは対応表の 1 対 1 の行だけで、対応表そのものは両向きの被覆を Check 468n が BLOCKING で見る。
- **エンジニア**: CI では回さない。

## Touch points

`LICENSES/CLAUSE-MAP-*.tsv` を読み、引数の file を（`--apply` のとき）書き換える。

## Related

- `.github/scripts/clause_ref_lint.py`（版を名乗らない曖昧な条番号）
- `.github/scripts/moved_clauses.py`（判定した後に動いた条）

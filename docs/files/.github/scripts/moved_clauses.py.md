---
file: .github/scripts/moved_clauses.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-24
canonical-ref: LICENSES/ACD-1.5-CHANGELIST.md (合議の記録・議題 16) / .github/scripts/make_redline.py (凍結した版どうしの語の差)
---

# .github/scripts/moved_clauses.py

## What

2 つの本文（file・git の版・作業中の草案）の条ごとの本文を空白を畳んで比べ、動いた条・新しい条・消えた条を出す手回しの道具。`--ledger` は、台帳の行が名乗る判定の本文（`本文 <commit>`）の後に動いた条の行だけを出す。`--refs` は、動いた条を参照する（自分は動いていない）条を添える。

## Why

判定は判定した日の本文についての事実で、条が動けばその行は当て直しが要る。1.5 の書き直し（2026-11-24）では 1 日に本文を 37 回固定し直し、誰の判定が動いた条に当たるかを手で diff を読んで 1 人ずつ知らせた。

## How (usage)

```bash
python3 .github/scripts/moved_clauses.py <commit> --refs
python3 .github/scripts/moved_clauses.py --ledger LICENSES/ACD-1.5-UNIQUE-READING.md
```

終了コード: 動いた条（または当て直しの要る行）が在れば 1、無ければ 0、本文を読めなければ 2（空の本文を「全部動いた」と読まない）。

## Constraints

- 台帳の行は `- §N.M … | …` の形で、行のどこかに `本文 <commit 7 桁以上>` を持つこと。持たない行は「名乗らない行」として数だけ出す。
- 条の中の段 (a)〜(e) は条に含めて比べる。折り返しだけの差は動いたと数えない。

## Change impact

読むだけの道具なので、変えても本文・台帳・CI は動かない。抜き出しの形（行頭 `^  N.M `・区切り線）を変えると、全部の条が「動いた」か「読めない」になる（読めないときは終了コード 2）。

## Audience-specific notes

- **新卒**: 「この行の判定は、いまの文についての判定か」を確かめる道具。
- **監査人**: 台帳の行が古い本文についてのものでないことを、行ごとに再現できる。
- **エンジニア**: CI では回さない。

## Touch points

`LICENSES/ACD-*-DRAFT.txt` を読むだけで、書き換えない。

## Related

- `.github/scripts/make_redline.py`（凍結した版どうしの語の差。述べ直した版をまたぐ差は止まる）
- `LICENSES/CLAUSE-MAP-1.4-1.5.tsv`（条がどこへ動いたか）

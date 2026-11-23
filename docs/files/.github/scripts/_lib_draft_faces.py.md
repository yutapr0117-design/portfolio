---
file: .github/scripts/_lib_draft_faces.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-23
canonical-ref: .github/scripts/checks_license_draft.py (Check 468 の区間・ラベル・OK 行) / .github/scripts/_lib_draft_counts.py (468n・468s の本体)
---

# .github/scripts/_lib_draft_faces.py

## What

Check 468 の面のうち本体の長い 468y (試作で「変えない」「退けた」とした条の逐条の行が、その試作に触れていること) と 468z (次版の CHANGELIST の記述子の下書き / 候補が引く条と逐語が、草案に実在すること) を `faces_468yz(ROOT, dr, cl, t468)` に置く。返り値は (誤りの文, 468y の組の数, 468z の参照の数, 468z の異なる条)。

## Why

2026-11-23 に `checks_license_draft.py` が 933 行で Check 52 の advisory (900) を越え、BLOCKING の 1,000 行 (Check 365) に近づいた。Check 468 は 1 つの `# ── 468.` 区間なので、面の本体を helper へ移す (2026-11-15 の `_lib_draft_counts.py` と同じ手)。

## How (usage)

```python
from _lib_draft_faces import faces_468yz
bad, pairs, n468z, u468z = faces_468yz(ROOT, draft_path, clause_numbers, draft_text)
```

## Constraints

本体は移す前と同じ (変数の名だけを引数に替えた)。OK 行は移す前と 1 字も変わらないことを確かめた。468x は `_cltxt468z` を読むので、呼び出し側で同じ値を作り直している。

## Change impact

468y・468z を直すときはこの file を直す。mutation の file は対象の文書 (試作・CHANGELIST) なので変わらない。

## Audience-specific notes

- **機械層**: Check 468 の面を新しく足すときは、`checks_license_draft.py` の行数を見て、長い本体はここへ置く。

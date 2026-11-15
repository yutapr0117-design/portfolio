---
file: .github/scripts/clause_ref_lint.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-15
canonical-ref: LICENSES/ACD-1.1-CHANGELIST.md §0.5 (1.0 → 1.1 の条番号対応・曖昧な番号の出所) / .github/scripts/make_redline.py (対応表の読み方)
---

# .github/scripts/clause_ref_lint.py

## What

新しく書いた行のうち、版を名乗らずに曖昧な条番号を引く箇所を出す手回しの道具（ADVISORY・exit は常に 0）。

- 曖昧な番号とは、1.0 と 1.1 以降で中身が違う番号のことである。`ACD-1.1-CHANGELIST.md` §0.5 の表から導く（いまは 1.2, 1.3, 1.4, 1.6, 15.2〜15.8, 16.5 の 12 個）。
- 読むのは `--since`（既定 origin/main）からの差分で足した行だけ。
- 同じ段落か同じ表の行に版の名乗り（1.0 / ACD-1.4 / 1.4 草案 / 1.4 draft など）があれば、名乗ったとみなす。
- 各件に、その番号の 1.0 の条の頭と、いまの草案の条の頭を並べる。

## Why

2f の §1.210 は §15.7 と §15.3 を取り違えかけた（against #221 の型・30 の依頼・2026-11-15）。ドシエ全体を照らすと 856 か所が出た。その大半は文書全体が 1 つの版を前提にしているので、Check にはできない（30 と合意して見送った）。新しく書いた行だけを見れば、書いた当日に人が決められる。導入の日に直近 8 時間の差分を回すと、`ACD-1.0.review-readings.md` の §1.208 の「直接の許諾（§1.6・§4.6）」が出た。1.4 の §1.6（You の定義）を指しているが、1.0 の文書の中で版を名乗っておらず、1.0 の §1.6 は Moral Rights である。

## How (usage)

```bash
python3 .github/scripts/clause_ref_lint.py                  # origin/main から足した行
python3 .github/scripts/clause_ref_lint.py --since HEAD~3
```

## Constraints

- 版を名に持つ文書（`ACD-N.M-` で始まる file。CHANGELIST・試作・逐条の下書き）は、文書全体がその版の番号なので読まない。
- rounds/ は逐語なので読まない。

## Change impact

- 新しい版で条番号を並べ替えたら、対応表を足し、`ambiguous()` の読み先を広げる。

## Audience-specific notes

### For AI agents（次担当）

- ドシエの 1.0 の文書に 1.4 の条番号を書くときは「1.4 草案 §N.M」と名乗る。PR を出す前にこの道具を回す。

### For human engineers（新卒レベル）

「第 15.7 条」のような条番号が、どの版の条のことか分からなくなっている書き方を見つける道具。

### For third parties / auditors

出力は候補で、取り違えの証拠ではない。

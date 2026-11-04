---
file: .github/scripts/measure_quote_drift.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-04
canonical-ref: LICENSES/ACD-1.1-CHANGELIST.md (§0.13 確定手順) / .github/scripts/measure_citation_drift.py (条番号の意味の drift を測る姉妹の道具)
---

# .github/scripts/measure_quote_drift.py

## What

**提出側の文書がライセンス本文を逐語で引いている箇所が、出す版の本文にもまだ在るかを測る道具。**
提出側 5 面（`submission.md` / `submission-reference.md` / `submission-osd.md` / `REVIEWERS.md` /
`READY-TO-SUBMIT.md`）から 40 字以上の引用を取り、省略記号で断片に分け、**旧版の本文に在り新版の本文に
無い断片**を列挙する。

## Why

新しい版を出すなら、提出物の逐語引用は**出す版の文面と一致しなければならない** —— 引用が現物と違う
提出は、審査者が最初に気づく種類の誤りである。`measure_citation_drift.py` は「引いた条番号の意味」を
測るが、**逐語の文がまだ在るか**は見ない。確定手順 §0.13 はこれを手で回していた（portfolio-25 の依頼で
2026-11-01 に道具化）。

## How

```sh
python3 .github/scripts/measure_quote_drift.py            # 1.0 → 現行草案（導出）
python3 .github/scripts/measure_quote_drift.py 1.0 1.4    # 版を指定
```

引用の取り方は、**段落の中で隣り合う引用符の組をすべて取る**形。開閉を判定しない。以前は行単位と段落単位（40 字以上）の和集合だったが、同じ段落の短い引用（`"10.5 and 16.5"`）の閉じ引用符を開始と取り違えて対応が 1 つずれ、`submission-osd.md` の §4.3 の逐語を落としていた。本文の語が変わっているのに 1.3 → 1.4 が 0 件と報告し、2026-11-04 に `measure_clause_overlap.py --compare` の 5 語照合と食い違って判明した。隣り合う組をすべて取ると引用の外側の文も断片になるが、「旧版の本文に逐語で在る」ことを要求するので誤検出にはなりにくい。

## Constraints

- **Check ではない**。旧版の引用だと明示して残すのが正しい場合もあり、それは判断である。手で回し、出た一覧を人が当たる。
- 本文は区切り線（`-` × 80）の後を読む。区切り線が無い 1.0 は全文。

## Change impact

提出側の面を足したら `FACES` に足す。読み先の file が無いときは一覧の前に「※ 無い」と出す（黙って飛ばさない）。

## Audience-specific notes

- **AI**: 版確定の日（§0.13）に回し、出た断片ごとに「新版の文面へ直す」か「旧版の引用と明示する」かを決める。
- **監査人**: 結果は確定手順の記録に残す。件数は版と面で変わるので、ここには書かない。

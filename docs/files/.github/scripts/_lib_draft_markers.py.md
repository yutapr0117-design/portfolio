---
file: .github/scripts/_lib_draft_markers.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-12
canonical-ref: .github/scripts/checks_license_draft.py (Check 468u / 468r) / .github/scripts/measure_clause_overlap.py (--guard)
---

# .github/scripts/_lib_draft_markers.py

## What

次版の草案（いまは `LICENSES/ACD-1.4-DRAFT.txt`）の条に当てる一覧と、その当て方を置く小さな module。

- `EFFECT_MARKERS_468U` —— 理由の文を外したあとも効果を運ぶ句（条, 句）の一覧。Check 468u がいまの草案に、`measure_clause_overlap.py --guard` が試作の写しに当てる。
- `STATE_WORDS_468R` / `STATE_EXEMPT_468R` —— 作用の条（第 1 条〜END OF TERMS）に置かない「いまの状態」の語（*unresolved* / *currently* / *not yet* など）と、句で持つ除外（条, 句）。
- `state_hits(clauses)` —— `{条: 本文}` から、除外の句を取り除いたあとに残る状態の語と、条から消えた除外の句を返す。

## Why

一覧を Check と道具が別々に持つと食い違う（468u の初版の取り決め）。2026-11-12 に 468r（T54 で外した §8.4 の「法は未決」の文の型・portfolio-aa の §14.29）を足すと `checks_license_draft.py` が行の予算 900 を越えるので、2 つの読み手が共有する一覧をここへ移した。

除外を語ではなく句で持つのは、同じ語を別の構文で使えば鳴り、句を書き換えたら読み直しの合図になるようにするため。

## How (usage)

```python
from _lib_draft_markers import EFFECT_MARKERS_468U, state_hits
hits, miss = state_hits(clauses)   # clauses = {"8.4": "...", ...}
```

`python3 .github/scripts/measure_clause_overlap.py --guard TRIAL.txt` は両方の一覧を試作の写しに当て、欠けた目印・状態の語・消えた除外の句があれば exit 1 を返す。

## Constraints

- 語の一覧に無い言い方（*remains to be seen* など）は漏れる。一覧は下限である。
- 前文は作用の条ではないので対象外。前文の状態の記述（*"the question is unsettled in most jurisdictions"* など）は、版を確定する日に読み直す。
- 一覧を変えたら、Check 468 と `--guard` の両方の結果が変わる。

## Change impact

- 除外の句を草案で書き換えると Check 468r が RED になる。その文が状態を述べていないかを読み、一覧を直す。
- 目印を足すときは、`ACD-1.4-SECOND-CLARITY-TRIAL.md` の試作の節に理由を書く。

## Audience-specific notes

### For AI agents（次担当）

- 一覧はここだけに置く。Check の module や道具に写さない。

### For human engineers（新卒レベル）

ライセンスの草案の文を削るとき、削ってはいけない句（目印）と、書いてはいけない語（いまの状態）を 1 か所にまとめた表。検査と道具の両方がここを読む。

### For third parties / auditors

一覧は機械の照合の材料で、条文の解釈ではない。

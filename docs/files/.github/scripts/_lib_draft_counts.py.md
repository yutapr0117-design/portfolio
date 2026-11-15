---
file: .github/scripts/_lib_draft_counts.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-15
canonical-ref: .github/scripts/checks_license_draft.py (Check 468n / 468s / 定義語) / .github/scripts/checks_license_self_reporting.py (Check 460 (x))
---

# .github/scripts/_lib_draft_counts.py

## What

次版の草案（いまは `LICENSES/ACD-1.4-DRAFT.txt`）について、文書に「書かれた数」を「数え直した数」と照らす関数を置く小さな module。各関数は誤りの文の list を返す。

- `bullet_components(hdr, prev, cur, changed, prev_body, cur_body, prev_ver)` —— 468n（箇条ごと）。冒頭の変更一覧の語数申告を、箇条が名指す変わった条でまとめた（union-find）まとまりごとに、本文の差と照らす。
- `changelist_table_total(path)` —— 468s。CHANGELIST の主表（「## 表」〜「## errata 由来」）の「費用（語）」列の合計。
- `length_sites(licenses_dir, skip, scope)` —— 草案の語数から導出する数を書いた場所の一覧（2026-11-15）。`scope="outward"` は B3 の見出しと SUBMISSION-MATERIALS の長さの行（後半の「条文では N 語長いまま」を含む）、`"all"` は草案冒頭の申告・CHANGELIST の語数の内訳と英文も含む。`apply_sites(sites)` が書き換える（`sync_stated_counts.py --apply`）。
- `draft_length_claims(licenses_dir, skip)` —— 460 (x)。`length_sites(..., "outward")` の場所のうち、実測と違うものを誤りの文にする。
- `defined_term_uses(clauses)` —— 468（定義語）。定義した語が、定義した条の外で 1 回以上使われているか。

## Why

2026-11-15 に `checks_license_draft.py`（予算 900）と `checks_license_self_reporting.py`（予算 875）が advisory を越えた。どちらも同じ日に 9b が足した面の分である。Check 468 は 1 つの `# ── 468.` 区間で、Check 460 の面は Check 469 (a) が `# (x)` と `_bad460.append` の組で数えるので、区間や面を module 間で分けられない。予算表の注記（「分けるなら面を helper 関数へ移す」）どおり、照合の本体だけをここへ移した。予算は上げていない。

## How (usage)

```python
from _lib_draft_counts import bullet_components, defined_term_uses
comps, bad = bullet_components(hdr, prev_clauses, cur_clauses, changed, prev_body, cur_body, "1.3")
uses, bad = defined_term_uses(cur_clauses)
```

## Constraints

- 読めないもの（区間・申告・GPL-3.0 の行・定義）は 0 にせず誤りの文にする。無いと黙る gate にしない。
- 460 (x) は英語の "N words from the title to *END OF TERMS*" を読まない。それは 498 (j) が CHANGELIST では ADVISORY と決めた「1.0 から何が変わったか」の下書きである。
- 468n は箇条が「変更」ごとに語を数える前提に立つ。条ごとの 1 対 1 照合はしない。

## Change impact

- 関数の誤りの文の頭（`468n (箇条ごと)`・`468s`・`(x)`・`468 (定義語)`）は mutation の帰属に使われる。変えるなら mutation の名前と合わせる。
- 460 (x) の誤りは呼び出し側で `# (x)` の直後に append する。Check 469 (a) と 479c はその組を数える。

## Audience-specific notes

### For AI agents（次担当）

- Check の module に本体を書き戻さない（予算を越える）。面を足すときは、ここに関数を足して呼び出し側にラベルを置く。

### For human engineers（新卒レベル）

ライセンスの草案の説明文に書いた数（語数、何語増えたか、GPL-3.0 より何語短いか）が、草案そのものを数え直した結果と合っているかを確かめる関数の置き場。

### For third parties / auditors

照らしているのは数の一致であって、条文の解釈や効果ではない。

---
file: .github/scripts/_lib_dossier.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-12
canonical-ref: LICENSES/ACD-1.0.against.md (不利な事実の register) / docs/architecture/file-size-budget.md (Check 495 のバイトの予算)
---

# .github/scripts/_lib_dossier.py

## What

ドシエの不利な事実の register（against）の file の一覧 `AGAINST_FILES` と、それを読む 3 つの関数を置く小さな module。

- `against_paths(licenses_dir)` —— register の file を順に（在るものだけ）。
- `against_text(licenses_dir)` —— 全 file の本文をつないだもの。
- `is_against(name)` —— file 名が register の file か。

Check 460（(e) の規模の申告・行数・REVIEWERS の長さの倍率・(s) と (w) の除外）、474、491、467c の除外と、`generate_status.py`（STATUS.md の件数）がここから読む。

## Why

`ACD-1.0.against.md` はバイトの予算（Check 495・advisory 800,000 / BLOCKING 1,000,000）に近づいている。BLOCKING の手前で、#N の番号を続けたまま 2 つ目の file へ分けると portfolio-00 と portfolio-9b が 2026-11-12 に決めた。分ける日に読み手を何か所も直さずに済むよう、file の一覧をここだけに置く。

## How (usage)

```python
from _lib_dossier import against_text, is_against
rows = re.findall(r"^\| \d+ \|", against_text(ROOT / "LICENSES"), re.M)
```

分けた日は `AGAINST_FILES` に 2 つ目の file 名を足す（番号の範囲は file の順）。

## Constraints

- 一覧の順は #N の順と同じにする（#N の参照の解決は番号で行う）。
- `startswith("ACD-1.0.against")` で名前を見ている所（472e の除外・`find_quote_retractions.py`）は、2 つ目の file 名がその接頭辞を持つ限りそのまま働く。

## Change impact

- 2 つ目の file を足すときは、同じ PR で mirror doc（Check 108）・索引からの導線（Check 459）・バイトの予算の行（Check 495）を足す。

## Audience-specific notes

### For AI agents（次担当）

- register の file を開くときは、名前を直接書かずにここから読む。

### For human engineers（新卒レベル）

大きくなった記録の file を 2 つに分けても、読む側のプログラムを 1 か所直すだけで済むようにするための表。

### For third parties / auditors

register の中身や判断には関わらない。どの file を register として読むかだけを決める。

**草案の逐語の照合（2026-11-12）**: `errata_draft_quote_misses`（Check 468w・`checks_license_draft.py` から移した）と `dossier_draft_quote_misses`（Check 468a・ドシエが「N.M 草案 / draft」として引く逐語がいまの草案に在るか）を置く。どちらも "…" で切った断片を当てる。

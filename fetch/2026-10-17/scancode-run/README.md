# scancode-run — **取得ではなく測定**（ScanCode toolkit をこの Mac で走らせた出力）

- 実行: 2026-10-17 UTC 11 時台・`scancode-toolkit==32.5.0`（venv・依存の全版は `pip_freeze.txt`）。
- CLI はシステムの libmagic を要求して起動しなかったので、`licensedcode.cache.get_index().match(query_string=…)` を直接呼んだ（`sc_match.py`）。ファイル種別判定の `typecode.magic2` だけを空のスタブに差し替えている（ライセンス照合には使われない）。**CLI の出力と完全に同じである保証はない。**
- 入力（`inputs/`）: ACD-1.0 / 1.1 / 1.2-DRAFT と `LICENSE` は `origin/main`（`46f0a95f`）から `git show`、W2FPL は `spdx2/w2fpl_LICENSE.txt`、対照 4 本は SPDX の license-list-data（main）の text。
- `rules/` は一致したルールのうち 3 件の、パッケージ同梱のルールファイルそのもの。

| file | sha256[:16] |
|---|---|
| ./inputs/0bsd.txt | e3f18c71e10d6735 |
| ./inputs/acd10.txt | 924e6a90d05cbc5d |
| ./inputs/acd11.txt | 79f54dc6cea8bde4 |
| ./inputs/acd12draft.txt | 147fae35ca120444 |
| ./inputs/cc0.txt | a2010f343487d3f7 |
| ./inputs/mit0.txt | 59746d6285ffa44b |
| ./inputs/repo_LICENSE.txt | 63803d8c52e4968b |
| ./inputs/unlicense.txt | 0bdebfeda07d45da |
| ./inputs/w2fpl.txt | 2bdfa6978ce331c0 |
| ./pip_freeze.txt | 0a0b40ff745e676d |
| ./result_acd10_LICENSE_w2fpl.json | d4d8ed6e53b90ca0 |
| ./result_acd11_acd12draft_controls.json | b78a053ffffae977 |
| ./rules/proprietary-license_544.RULE | dcd84f8e2fac4b16 |
| ./rules/public-domain_bare_words.RULE | 1b8d5398dca432cd |
| ./rules/unknown_35.RULE | 08425579caaa0f3b |
| ./sc_match.py | 34a553a9dd353c00 |

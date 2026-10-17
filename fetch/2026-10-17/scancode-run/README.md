# scancode-run — **取得ではなく測定**（ScanCode toolkit をこの Mac で走らせた出力）

- 実行: 2026-10-17 UTC 11 時台・`scancode-toolkit==32.5.0`（venv・依存の全版は `pip_freeze.txt`）。
- CLI はシステムの libmagic を要求して起動しなかったので、`licensedcode.cache.get_index().match(query_string=…)` を直接呼んだ（`sc_match.py`）。ファイル種別判定の `typecode.magic2` だけを空のスタブに差し替えている（ライセンス照合には使われない）。**CLI の出力と完全に同じである保証はない。**
- 入力（`inputs/`）: ACD-1.0 / 1.1 / 1.2-DRAFT と `LICENSE` は `origin/main`（`46f0a95f`）から `git show`、W2FPL は `spdx2/w2fpl_LICENSE.txt`、対照 4 本は SPDX の license-list-data（main）の text。
- `rules/` は一致したルールのうち 3 件の、パッケージ同梱のルールファイルそのもの。

- `variants/` は **スクラッチ上で ACD-1.2-DRAFT の 1 か所（"commercial or non-commercial"）だけを置き換えた試験用の写し**で、リポジトリのファイルではない。結果は `result_acd12draft_variants.json`。

- `result_osi_approved_141_census.json` は SPDX license-list-data（`census_input_source.txt` の commit）の **OSI 承認済み・非 deprecated の 141 本**を同じ照合 API に当てた結果。`result_peers.json` は OpenMDW-1.0（SPDX text）/ OpenMDW-1.1（`peer-texts/`）/ MIT-PoU v1.2.0（`peer-texts/`）/ MCAL（license-discuss 10 月アーカイブ内の添付本文を切り出したもの・`inputs/peers/mcal_from_archive.txt`）。

| file | sha256[:16] |
|---|---|
| ./census_input_source.txt | c44c69549e77c4c0 |
| ./inputs/0bsd.txt | e3f18c71e10d6735 |
| ./inputs/acd10.txt | 924e6a90d05cbc5d |
| ./inputs/acd11.txt | 79f54dc6cea8bde4 |
| ./inputs/acd12draft.txt | 147fae35ca120444 |
| ./inputs/cc0.txt | a2010f343487d3f7 |
| ./inputs/mit0.txt | 59746d6285ffa44b |
| ./inputs/peers/mcal_from_archive.txt | 1a017123faef782e |
| ./inputs/peers/openmdw-1.0.txt | 22d5488faff30b2e |
| ./inputs/repo_LICENSE.txt | 63803d8c52e4968b |
| ./inputs/unlicense.txt | 0bdebfeda07d45da |
| ./inputs/w2fpl.txt | 2bdfa6978ce331c0 |
| ./pip_freeze.txt | 0a0b40ff745e676d |
| ./result_acd10_LICENSE_w2fpl.json | d4d8ed6e53b90ca0 |
| ./result_acd11_acd12draft_controls.json | b78a053ffffae977 |
| ./result_acd12draft_variants.json | c61fd2248a6368a5 |
| ./result_osi_approved_141_census.json | eed0d49aa04bf537 |
| ./result_peers.json | e9f6c0ae20234496 |
| ./rules/proprietary-license_544.RULE | dcd84f8e2fac4b16 |
| ./rules/public-domain_bare_words.RULE | 1b8d5398dca432cd |
| ./rules/unknown_35.RULE | 08425579caaa0f3b |
| ./sc_census.py | 71ea8d629cfc5b33 |
| ./sc_match.py | 34a553a9dd353c00 |
| ./variants/v_any_purpose.txt | f3c56e28f4dadd20 |
| ./variants/v_commercial_or_noncommercial_nohyphen.txt | 6ac33e0166106833 |
| ./variants/v_including_commercial.txt | 26ffdec707a0ab74 |
| ./variants/v_whether_or_not_commercial.txt | 4676f920f4e8376e |

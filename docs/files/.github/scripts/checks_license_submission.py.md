---
file: .github/scripts/checks_license_submission.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-26
canonical-ref: .github/scripts/check_repository_consistency.py (集約器) / docs/architecture/check-repository-consistency-map.md (全 Check の一覧) / docs/architecture/total-check-runbook.md §9 (総数の権威)
---

# .github/scripts/checks_license_submission.py

## What

**LICENSES/ のうち「審査者が直接受け取る面」だけを検査する consistency Check module。**
3 つの Check を持つ ——**463**（提出パケットの「送る文面」が OSI の要求項目を含むこと）/
**472**（提出側の文書の条項引用が、提出対象の版に実在すること。472b 版の一致・472c 入口の検証コマンド・
472d 入口の "In one screen" の位置・472e placeholder 0 の限定）/
**473**（来歴の開示が、否定の半分だけで現れないこと）。

## Why

**`checks_license_dossier.py` が 914 行になり Check 52 の advisory (800) を越えたため、
圧縮ではなくテーマ分割で出した。** 本リポジトリの規律は
「**advisory は上げて黙らせるのではなく、BLOCKING (1,000) の手前で塊を切り出す**」である。

**分ける基準は「対象が誰の手に渡るか」**。残った側（`checks_license_dossier.py`）は
**ドシエの運用記録**についての Check（投稿先 / 索引 / 鮮度 / errata↔変更リスト /
`rounds/` 在庫 / 表紙 / 発信停止）で、**壊れたときの損害は「記録が古い」**である。
こちら側が壊れたときの損害は「**審査者が誤った物を読む**」で、質が違う。

## How

- **2026-09-24: 468（次版草案）を `checks_license_draft.py` へ出した。** 801 行で advisory (800) を越えたため。
  草案は「まだ誰にも渡していない」面で、ここが守る「審査者がいま受け取る面」とは損害の質が違う

- 集約器 `check_repository_consistency.py` の `CHECK_SOURCE_FILES` に登録し、
  `_checks_license_submission.run(_ctx)` で呼ばれる（**Check 431 が実在 ⟺ 登録 ⟺ 実行を強制**）
- `run(ctx)` は `ROOT` と `check` だけを bind する。**未 bind の名前を使わないこと** ——
  Check 473 の初版が ctx の `read()` を呼んで `NameError` を投げ、
  それを裸の `except` が握り潰して **79 file すべてを読み飛ばしたまま緑を出した**
  （`against.md` #189）
- 移動は**逐語**で、条文ロジックは 1 バイトも変えていない

## Constraints

- **`# ── N.` の section header と docstring inventory の bijection は Check 45 が強制する。**
  片方だけ動かすと RED
- **番号は動かさない。** 他文書が `Check 463` のように番号で参照しており、
  `Check 471(c)` が「実装の最大番号を超える参照」を見ている
- **例外を握り潰さない。** 落ちた検査と、何も見つけなかった検査は同じ出力を出す

## Change impact

Check を足すときは docstring inventory + `# ── N.` + map + runbook §9 を同じ commit で
（自己整合 Check 45 / 70 / 105 が同時に検証する）。**行数が 800 を越えたら、
また圧縮ではなくテーマで割る。**

## Audience-specific notes

- **審査者**: ここに在る 3 つは、あなたが実際に読む面（送る文面・条項引用と入口ページ・来歴の開示）を
  機械で縛っている層である
- **後任 AI**: **新しい Check の行き先はこの 2 分割で決める** ——
  審査者が受け取る面なら本 file、次版の草案なら `checks_license_draft.py`、運用の記録なら `checks_license_dossier.py`

## 2026-09-26: 472f

提出パケットの**版に紐づく欄**（識別子・Version・版付き URL・件名・SPDX 依頼の Full name）が `SUBMISSION-TARGET` と一致することを強制する。確定手順 (3) は「Check 444 が一致を強制する」と書いていたが、444 は `submission.md` を読んでいなかった。照合数の下限（10）は、欄の書式が変わって検出器が見失ったときに黙って緑になるのを防ぐ。

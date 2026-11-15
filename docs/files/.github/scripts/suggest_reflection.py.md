---
file: .github/scripts/suggest_reflection.py
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-11-15
canonical-ref: LICENSES/REFLECTION-BACKFILL.md / .github/scripts/_lib_dossier.py (backfill_table_misses)
---

# .github/scripts/suggest_reflection.py

## What

§1.N の範囲を受け取り、各節の番号を review-readings 以外の LICENSES/*.md から引いて、反映先の候補（against の行の番号・
errata の番号・B の節（見出しを上へ辿る）・入口の文書・1c の文書）を出す。`--rows` で REFLECTION-BACKFILL の行の下書き。

## Why

提出のゲート 6c（オーナーの前提「全て読んで反映してこそ出せる」・2026-11-15）で、§1.242 より前の約 170 節に反映先を
書く。30 の調べ方（番号を grep し、当たった行の種類で反映先を決める）を 5 人が手で回すと同じ grep を 170 回書く。

## How

出すのは候補で、反映の判断ではない。当たった行がその節の論点を運んでいるかは読む人が決める。当たりの無い節は
「未定」と出すので、読んで「なし（理由）」か、いまから反映するかを決める。Check 501b が表の行を照らす。

## Constraints

- 番号だけで引くので、床（70）の下の文書ごとの番号は同じ番号の別の節にも当たる。その範囲は file 名で絞って読む。

## Change impact

- 行き先の種類（against / errata / B / 入口 / 1c）を足すときは、Check 501 の語彙（`_lib_dossier._REFLECT_VOCAB`）と揃える。

## Audience-specific notes

- **AI / 後任**: `--rows` の出力をそのまま貼らない。確かめ方の欄は、実際に読んで確かめた内容に直す。

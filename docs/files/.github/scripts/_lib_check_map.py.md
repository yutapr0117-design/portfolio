---
file: .github/scripts/_lib_check_map.py
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-11-16
canonical-ref: docs/architecture/check-repository-consistency-map.md / .github/scripts/checks_docs_mirror.py (Check 105)
---

# .github/scripts/_lib_check_map.py

## What

Check の地図（check-repository-consistency-map.md）の file の一覧（CHECK_MAP_FILES）と、全 file の本文をつなぐ関数。Check 64（番号の一意）・
105（地図と実装の一対一）・478（所在の列）が、地図を直に開かずにここを通して読む。

## Why

地図は 393 KB でバイトの advisory（380 KB・Check 495）を越え、上限（500 KB）へ近づいている（2026-11-16）。大半は行の表で、いつか行を 2 つ目の
file へ分ける。その日に読み手が 2 つ目を黙って見落とさないよう、一覧を 1 か所に置く（against.md の AGAINST_FILES と同じ形）。

## How

分けた日は CHECK_MAP_FILES に 2 つ目を足す。予行（カテゴリ F を動かした）で 64・105・478 は緑のままだった。残る作業は docstring に書いた。

## Constraints

- いまは 1 file。振る舞いは変えていない。

## Change impact

- 地図を読む Check を新しく足すときは、地図を直に開かずにこの一覧を通す。

## Audience-specific notes

- **AI / 後任**: 地図の行の書式（`| N | … |`）を変えると、64・105・478 の正規表現も合わせる。

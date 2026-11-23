---
file: LICENSES/REDLINE-1.0-TO-1.4.txt
audience: OSI license-discuss / license-review participants, licence reviewers, 監査人
last-updated: 2026-11-23
canonical-ref: LICENSES/ACD-1.0.txt (差の起点・list に出した本文) / LICENSES/ACD-1.4.txt (差の到達点・適用している版) / .github/scripts/make_redline.py (生成した道具)
---

# LICENSES/REDLINE-1.0-TO-1.4.txt

## What

ACD-1.0（2026-08-26 に license-discuss へ出した本文）から ACD-1.4（2026-11-23 に確定・適用）への、条ごとの語の差（英語・80 桁・ASCII）。
`[-語-]` が 1.0 にだけ在り、`{+語+}` が 1.4 にだけ在る。1.0 と 1.1 以降で条番号がずれる所は、`ACD-1.1-CHANGELIST.md` §0.5 の表で対応させ（表が結ばない条は、同じ節の中で語の並びが最も近い条へ結び、比を括弧に書く・2026-11-23 に足した。1.0 §15.3 → 1.4 §15.6 は比 1.00、§15.2 → §15.5 は 0.96。最初の出力はこの 2 つを削除と新設に割り、要約の new / removed が 2 件ずつ多かった）、1.0 にだけ在る条のうち中身が 1.4 の別の条へ移ったもの（1.0 §15.5 → 1.4 §2.2 の末文、§16.5 → §16.4 の中）は、`ACD-1.4-CHANGELIST.md` の「条項の対応表（1.0 → 1.4）」（d7）を読んで行き先の 1 行を出す（2026-11-24・5e の案。語の近さでは誤った組と区別できなかった）、
旧い番号を括弧で示す。冒頭に 2 つの入力の file 名・sha256・語数がある。

## Why

審査者は版の取り違えで時間を失ってきた —— Piana 氏 2025-10-30 は *"a full set of the final, revised licenses, as well as a word-diff
comparing them to the originals"* を求めた（portfolio-d7 の採掘）。入口（REVIEWERS.md）は提出対象の印（SUBMISSION-TARGET）が 1.0 の間も 1.4 を「適用している版・出す版」として並べる（5 人の合議・
2026-11-23）ので、list で議論された 1.0 からの差を 1 本で辿れるようにした。

## How

`python3 .github/scripts/make_redline.py LICENSES/ACD-1.0.txt LICENSES/ACD-1.4.txt` の出力に、生成した commit を書き添えたもの。
入力が 2 つとも凍結（FROZEN.md・Check 453）なので、出力は変わらない。名を `ACD-*.txt` の形にしないのは、版の本文を探す glob に当たらないため。

## Constraints

手で直さない。直すなら道具を直して出し直す。語の差は法的効果の差ではない（ファイル冒頭にも書いてある）。

## Change impact

1.5 を確定したら、1.0 → 1.5 の redline を同じ形で足すかを、そのときの入口の判断で決める（この file は 1.0 → 1.4 の記録として残る）。

## Audience-specific notes

- **審査者**: 入口の短い経路の 1.0 の行から辿れる。変わった条だけを見るなら `make_redline.py --changed-only` を自分で回せる。

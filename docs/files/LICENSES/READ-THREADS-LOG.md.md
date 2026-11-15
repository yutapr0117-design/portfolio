---
file: LICENSES/READ-THREADS-LOG.md
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-15
canonical-ref: LICENSES/READ-THREADS.txt / LICENSES/AS-OF.md
---

# LICENSES/READ-THREADS-LOG.md

## What

**未読スレッドを読んだ記録 —— どのスレッドを読み、どの節（`review-readings.md` / `reviewer-positions.md` /
`against.md` など）へ運んだか。** `AS-OF.md` の「未読スレッドの残り」のセルに前置で積まれていた 65 件を、
2026-11-15 に 1 字も変えずに移した。

## Why

セルは読むたびに前置で伸び、32,534 バイトになって `AS-OF.md` を byte 予算の advisory（130,000）より上に
置いていた。`AS-OF.md` は外界についての主張を日付つきで 1 箇所に集める表で、1 つのセルが表の 2 割を占めると
表として読めない。**消さなかったのは、件名から節を引く対応表がここにしか無いから**（節の側に件名が無いものがある）。

## How

読むだけの記録である。新しく読んだら、この一覧の先頭に 1 件を足し、`AS-OF.md` のセルの「直近の 1 件」と
件数を入れ替える。件名は同じ commit で `READ-THREADS.txt` にも足す。

## Constraints

- **移した項目の本文を書き換えない。** その日に何が分かっていたかの記録である。
- 件数（候補・読了・残り）の権威は `AS-OF.md` の文で、Check（stated counts の (h)）がその算術を照合する。

## Change impact

- 項目を足すときは `AS-OF.md` の件数の文（候補・読了・残り）と「直近の 1 件」も同じ commit で直す。
  件数の算術は Check（stated counts の (h)）が照合するが、どの項目が直近かは照合しない。
- この file の場所を変えるなら、`READ-THREADS.txt` の見出しのコメントと `AS-OF.md` のセルのポインタも直す。

## Audience-specific notes

- **AI / 新卒**: 「このスレッドはもう読んだか」は `READ-THREADS.txt` を grep する。「読んで何を書いたか」はここを grep する。
- **監査人**: 移した日の照合（セルの本文 = 直近の 1 件 + この一覧を連結したもの）は commit message に書いてある。

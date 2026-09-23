---
file: REUSE.toml
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-23
canonical-ref: LICENSE (許諾の権威) / LICENSES/ACD-1.0.txt (本文) / LICENSES/ACD-1.0.against.md #106 / LICENSES/ACD-1.0.against.md #108
---

# REUSE.toml

## What

**file 単位のライセンス情報**（REUSE Specification 3.3）。リポジトリ全体に
`LicenseRef-ACD-1.0` を、`LICENSES/rounds/**` には `NOASSERTION` を割り当てる。

## Why

**`against.md` #106** —— このリポジトリは機械可読なライセンス宣言を強みとして掲げながら、
**file 単位の情報を 1 つも持っていなかった。** 6 つの*面*が許諾を宣言し Check 444 が整合を
強制しているが、**REUSE は*file* の水準で働き、その水準では無言だった**
（shipped 42 file のうち `SPDX-License-Identifier` を持つものは **0**）。

**2026-08-25 に `license-discuss` で（我々の投稿の 1 つ前のメッセージで）Matija Šuklje 氏が
「REUSE 実践 + SBOM + `rel=license`」を合意事項として告知している** ——
我々は step 3 / 4 を満たし step 1 を満たしていなかった。

## How

**per-file の comment header ではなく `REUSE.toml` を採った。**

REUSE 3.3 は comment header を **RECOMMENDED** と述べるだけで required とはしておらず、
`REUSE.toml` は同格の代替で、**shipped byte に 1 バイトも触れない。**
`main.js` は kernel が byte 凍結（Check 43）、`LICENSES/ACD-1.0.txt` は sha256 pin（Check 453）
なので、これは実務上の違いではなく前提の違いである。

**⚠ #106 の初版の disposition は「全 file に header を入れる必要がある」と述べ、それを障害として
扱っていた。仕様を読まずに制約を主張していた**（#87 / #103 と同じ失敗）。

## Constraints

- **⚠ これは REUSE 適合の主張ではない。** REUSE は licence file を
  `LICENSES/<SPDX 識別子>.txt` と命名することも求める。ACD-1.0 は SPDX 未登録なので
  適合形は `LICENSES/LicenseRef-ACD-1.0.txt` になるが、
  **`LICENSES/ACD-1.0.txt` は動かさないと公表している**（提出パケットが指す URL であり
  Check 453 が pin している）。**linter は命名の非適合を報告し続ける。**
  **その bind は `against.md` #108 に別途記録してあり、承認されれば解消する。**
- **著作権行は「歴史的事実としての著作」であって存続する主張ではない**
  ——ACD-1.0 §3 が Covered Rights を放棄している。root `LICENSE` の
  *"Authorship remains a historical fact; the rights do not"* と同じ区別である。
- **`LICENSES/rounds/**` は他人の言葉**なので `NOASSERTION` にしてある。
  **保存しているのは記録であって、我々が権利を主張する対象ではない。**

## Change impact

- 識別子を変えるときは `LICENSE` / `machine.json` / Check 444 の 6 面と**同時に**。
- **SPDX へ登録されたら** `LicenseRef-ACD-1.0` → `ACD-1.0` へ、
  併せて #108 の命名 bind も解消する。

## Audience-specific notes

- **AI（実装者）**: **仕様を読まずに「できない」と書かない** —— この file が存在するのは、
  そう書いた disposition を原典で反証したからである。
- **監査人**: **適合していない点をこの file 自身が冒頭で述べている。**
- **第三者**: 許諾の権威は `LICENSE` と `LICENSES/ACD-1.0.txt` である。

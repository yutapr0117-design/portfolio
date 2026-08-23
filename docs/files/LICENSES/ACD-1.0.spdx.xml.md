---
file: LICENSES/ACD-1.0.spdx.xml
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-23
canonical-ref: LICENSES/ACD-1.0.txt / .github/scripts/generate_spdx_license_xml.py / docs/architecture/acd-license-rationale.md
---

# LICENSES/ACD-1.0.spdx.xml

## What

**SPDX License List への提出用 XML。自動生成物で、手で編集してはならない。**
単一ソースは `LICENSES/ACD-1.0.txt`。

```
npm run spdx-xml   # = python3 .github/scripts/generate_spdx_license_xml.py
```

## Why

SPDX への収録が受理されると、提出者は **XML とテストテキストの作成を手伝う**ことを求められる。
その XML を手書きすると、**ライセンス本文を改善するたび silent に古くなる** —— しかも XML は
普段誰も読まないので、drift に気付く経路が無い。本リポジトリが繰り返し潰してきた
「宣言はあるが実態が伴わない」class そのもの。

そこで本文から**導出**し、**Check 445** が「再生成して一致するか」を BLOCKING で検証する
(STATUS.md に対する Check 121 と同じ regenerate-compare 設計)。

## How (usage)

本文を直したら `npm run spdx-xml` を叩くだけ。提出時はこの file をそのまま
`spdx/license-list-XML` へ渡せる。

## Constraints

- **手で編集しない。** 編集しても次の `npm run spdx-xml` で消え、その前に Check 445a が RED になる。
- **`<optional>` / `<alt>` によるマッチング緩和は使わない。** ACD-1.0 §16.4 が
  「識別子は一つの固定テキストを指す」と定めており、変異を許す表現はその設計と矛盾する。
- **preamble も含める。** informative だが、SPDX のテキスト一致は file 全体で行われるので、
  落とすと**提出テキストと配布テキストが食い違う**。

## Change impact

- 3 面すべてが独立に守られている:
  - **445a** 再生成して一致するか（手編集と本文 drift を捕捉）
  - **445b** well-formed かつ licenseId が LICENSE と一致（**生成器の欠陥**を捕捉）
  - **445c** 本文の全条項が XML に現れる（**段落分割ロジックの欠陥**を捕捉）
  445b / 445c は生成器を壊して独立に RED を実測済。手編集は 445a が先に吸収するので、
  この 2 面の存在意義は「生成器そのものが壊れたとき」にある。
- `LICENSE` の `SPDX-License-Identifier:` を変えたら XML の `licenseId` も自動追従する
  （生成器が LICENSE から導出しているため）。

## Audience-specific notes

### For AI agents
- 役割タグ: `spdx-submission`, `generated-artifact`, `do-not-edit`
- この file を編集する変更は**ほぼ確実に誤り**。生成器か本文を直せ。

### For human engineers (新卒レベル)
- 「提出物を手で作らない」のは、提出が一度きりではないから。本文は改善され続けるので、
  提出物が追従しない設計だと**いつか嘘を提出する**。

### For third parties
- 独自ライセンスを SPDX へ申請する際の、提出物を drift させないための実装例。

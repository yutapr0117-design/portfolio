---
file: .github/scripts/generate_spdx_license_xml.py
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-23
canonical-ref: LICENSES/ACD-1.0.txt / LICENSES/ACD-1.0.spdx.xml / .github/scripts/generate_status.py
---

# .github/scripts/generate_spdx_license_xml.py

## What

`LICENSES/ACD-1.0.txt` から **SPDX License List 提出用の XML** を生成する。

```
npm run spdx-xml            # 生成 (出力: LICENSES/ACD-1.0.spdx.xml)
npm run spdx-xml -- --check # 同期しているかの判定のみ (Check 445a が使う)
```

## Why

SPDX への収録が受理されると提出者は **XML とテストテキストの作成を手伝う**ことを求められる。
手書きすると本文の改善に追従せず、**いつか嘘を提出する**。生成にすることで、本文を直せば
`npm run spdx-xml` 一発で提出物が追従する。

`generate_status.py` (STATUS.md) と同じ「生成物 + regenerate-compare Check」設計。

## How (usage)

識別子と canonical URL は**決め打ちせず `LICENSE` の 2 行から導出**する:

    SPDX-License-Identifier: ACD-1.0
    Full text: LICENSES/ACD-1.0.txt

Check 444 と同じ単一ソースなので、path を変えても生成器と Check が同時に追従する。

## Constraints

- **`<optional>` / `<alt>` によるマッチング緩和は使わない。** ACD-1.0 §16.4 が
  「識別子は一つの固定テキストを指す」と定めており、変異を許す表現はその設計と矛盾する。
- **preamble を落とさない。** informative だが SPDX のテキスト一致は file 全体で行われる。
- Python 3.10+ 専用 (PEP 604)。Check 104 が version guard を強制する。

## Change impact

- **段落分割ロジックを触ったら Check 445c が守る。** 本文は 79 桁で折り返してあるので改行を
  空白へ潰すが、**条項番号で始まる行は新しい段落として扱う** —— そうしないと条項の境界が
  失われる。§12 を落とす退行を入れると 445c が 6 条項の欠落を報告する（実測済）。
- 出力形式を変えたら `LICENSES/ACD-1.0.spdx.xml` を再生成して commit すること
  （しないと Check 445a が RED）。

## Audience-specific notes

### For AI agents
- 役割タグ: `generator`, `spdx-submission`, `single-source-derivation`

### For human engineers (新卒レベル)
- 「提出物を生成にする」判断の理由は**一度きりではないから**。本文は改善され続けるので、
  追従しない設計だといつか食い違う。

### For third parties
- 独自ライセンスの申請物を drift させないための実装例。

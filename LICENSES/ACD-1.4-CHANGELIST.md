---
file: LICENSES/ACD-1.4-CHANGELIST.md
audience: OSI license-discuss / license-review participants, licence reviewers, a future drafter
last-updated: 2026-10-26
canonical-ref: LICENSES/ACD-1.4-DRAFT.txt (草案) / LICENSES/ACD-1.3.txt (直前の確定テキスト・凍結・このリポジトリに適用中) / LICENSES/ACD-1.3-CHANGELIST.md (1.2 → 1.3 の記録) / LICENSES/ACD-1.0.errata.md
---

# ACD-1.4 で変えるもの

ACD-1.3 は 2026-10-25 に確定・凍結し、このリポジトリに適用した。**改善はここから先で行う。** 草案 `ACD-1.4-DRAFT.txt` は、**下の表の変更と版番号・識別子を除いて 1.3 の本文である**（2026-10-26 に最初の変更）。変更を入れたら、草案冒頭の一覧とこの表の両方に足す。条文の選択も AI が決め、理由と逆側を同じ行に書く（2026-10-24 オーナー明言・`OSI-APPROVAL-PLAN.md`）。

## 表（変更が入ったらここへ足す）

| 対象 | 何を変えるか | なぜ | 費用（語） | 状態 |
| :-- | :-- | :-- | :-- | :-- |
| §8.5 | 「controlled」の定義を足す（その時点で、他者への義務違反も支払いも無く許諾できる権利を持つこと） | errata **E39**。§8.1 / §8.4 の「owned or controlled」が未定義で、第三者に支払わないと許諾できない請求項や関連会社の請求項まで含むと読めた。GPL-3.0 と MPL-2.0 は同等の語を定義している。特許の審査者が最初に問う点（`QUESTIONS-FOR-COUNSEL.md` Q2）。**逆側**: 支払いが要る請求項は対象外と明示されるが、元々 Dedicator が自由に与えられないものなので、受領者が依拠できたものは減らない | +37 | 反映済み |

## errata 由来（`ACD-1.0.errata.md` が一次記録）

| Errata | 対象 | 1.4 での扱い（要約は errata 側が権威）| 状態 |
|---|---|---|---|
| E39 | §8.5 | 「controlled」の定義を足した（+37 語） | **反映済み**（2026-10-26）|

## 1.3 から持ち越したもの

- **E6** —— §8.4 が出力まで届くべきか。検討して狭めないと決めた（欠陥ではなく、決めた結果として残している）。
- **E10** —— 記述子は版ごとに作るので、1.4 を確定するときに `ACD-1.4.machine.json` で閉じ直す。
- **2026-10-24〜25 の模擬審査（17 観点の workflow）は利用上限で結果ゼロだった。** 1 回あたりの規模を小さくして、この草案に当てる候補である。

## Constraints

- 1.0 / 1.1 / 1.2 / 1.3 は凍結中（`FROZEN.md`・Check 453）。直すのは `ACD-1.4-DRAFT.txt` だけ。
- 確定するときは `ACD-1.1-CHANGELIST.md` §0.13 の手順に従い、改名を一括置換しない。**確定版の冒頭には適用状態のような変わりうる事実を書かない**（`ACD-1.3-CHANGELIST.md` の「確定」節）。

## Change impact

- `ACD-1.4-DRAFT.txt` の冒頭の一覧とこの表は、同じ commit で揃える（Check 468f / 468i）。

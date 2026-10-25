---
file: LICENSES/ACD-1.4-CHANGELIST.md
audience: OSI license-discuss / license-review participants, licence reviewers, a future drafter
last-updated: 2026-10-25
canonical-ref: LICENSES/ACD-1.4-DRAFT.txt (草案) / LICENSES/ACD-1.3.txt (直前の確定テキスト・凍結・このリポジトリに適用中) / LICENSES/ACD-1.3-CHANGELIST.md (1.2 → 1.3 の記録) / LICENSES/ACD-1.0.errata.md
---

# ACD-1.4 で変えるもの

ACD-1.3 は 2026-10-25 に確定・凍結し、このリポジトリに適用した。**改善はここから先で行う。** 草案 `ACD-1.4-DRAFT.txt` は**いまは版番号と識別子を除いて 1.3 と同一**で、冒頭の変更一覧は空である（空であることが現在の正しい状態で、記録が無いという意味ではない）。変更を入れたら、草案冒頭の一覧とこの表の両方に足す。条文の選択も AI が決め、理由と逆側を同じ行に書く（2026-10-24 オーナー明言・`OSI-APPROVAL-PLAN.md`）。

## 表（変更が入ったらここへ足す）

| 対象 | 何を変えるか | なぜ | 費用（語） | 状態 |
| :-- | :-- | :-- | :-- | :-- |

## 1.3 から持ち越したもの

- **E6** —— §8.4 が出力まで届くべきか。検討して狭めないと決めた（欠陥ではなく、決めた結果として残している）。
- **E10** —— 記述子は版ごとに作るので、1.4 を確定するときに `ACD-1.4.machine.json` で閉じ直す。
- **2026-10-24〜25 の模擬審査（17 観点の workflow）は利用上限で結果ゼロだった。** 1 回あたりの規模を小さくして、この草案に当てる候補である。

## Constraints

- 1.0 / 1.1 / 1.2 / 1.3 は凍結中（`FROZEN.md`・Check 453）。直すのは `ACD-1.4-DRAFT.txt` だけ。
- 確定するときは `ACD-1.1-CHANGELIST.md` §0.13 の手順に従い、改名を一括置換しない。**確定版の冒頭には適用状態のような変わりうる事実を書かない**（`ACD-1.3-CHANGELIST.md` の「確定」節）。

## Change impact

- `ACD-1.4-DRAFT.txt` の冒頭の一覧とこの表は、同じ commit で揃える（Check 468f / 468i）。

---
file: LICENSES/ACD-1.3-CHANGELIST.md
audience: OSI license-discuss / license-review participants, licence reviewers, a future drafter
last-updated: 2026-10-18
canonical-ref: LICENSES/ACD-1.3-DRAFT.txt (草案) / LICENSES/ACD-1.2.txt (直前の確定テキスト・凍結) / LICENSES/ACD-1.2-CHANGELIST.md (1.1 → 1.2 の記録) / LICENSES/ACD-1.0.errata.md
---

# ACD-1.3 で変えるもの

ACD-1.2 は 2026-10-17 に確定・凍結し、**改善はここから先で行う。** 草案 `ACD-1.3-DRAFT.txt` は**いまは版番号と識別子を除いて 1.2 と同一**で、冒頭の変更一覧は空である（空であることが現在の正しい状態で、記録が無いという意味ではない）。変更を入れたら、草案冒頭の一覧とこの表の両方に足す。

## 表（変更が入ったらここへ足す）

| 対象 | 何を変えるか | なぜ | 費用（語） | 状態 |
| :-- | :-- | :-- | :-- | :-- |

## 1.2 の凍結前検証から持ち越したもの（2026-10-17・まだ草案に入れていない）

1.2 の確定前に、6 観点の敵対的検証で指摘されたが、凍結を止めるほどではないと判定したもの。**欠陥と決まったものではなく、1.3 で読み直す候補**である。

| 対象 | 指摘 | 判定 |
| :-- | :-- | :-- |
| §6.5 | 「§6 は §3〜§5 を言い直しているだけ」と述べるが、§6.1 は §3〜§5 が届かない特許の請求項にも触れている | 1.3 で §6.5 の言い方を確かめる |
| §1.4（Dedicator の定義） | 定義が Covered Rights の保有者に限られる一方、§8（特許）と §12（人格権）は Covered Rights の外の権利を Dedicator に扱わせる | 1.3 で定義の射程を確かめる |
| §16.2 | 版のない名称（"Autonomous Commons Dedication"）だけで参照された場合に「these terms」が全面適用されると読める | 1.3 で「どの版か」を確かめる |
| §15.5 | 1.0 の §15.2 にあった "in particular" の規則が戻っていない、という指摘 | 1.2 のヘッダは「3 つの規則を戻した」と述べ、§15.5 は 3 つの規則を持つ。1.0 との対応を 1.3 で読み直す |
| 草案ヘッダの E22 の項目 | §2.6 を「削除」とだけ述べ、残した 1 文に触れていない | 1.2 では「The half worth keeping is kept」と述べており偽ではない。1.3 の記録では区別して書く |

## Constraints

- 1.0 / 1.1 / 1.2 は凍結中（`FROZEN.md`・Check 453）。直すのは `ACD-1.3-DRAFT.txt` だけ。
- 確定するときは `ACD-1.1-CHANGELIST.md` §0.13 の手順に従い、改名を一括置換しない。

## Change impact

- `ACD-1.3-DRAFT.txt` の冒頭の一覧とこの表は、同じ commit で揃える（Check 468f / 468i）。

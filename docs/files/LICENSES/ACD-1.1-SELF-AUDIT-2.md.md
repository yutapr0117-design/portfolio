---
file: LICENSES/ACD-1.1-SELF-AUDIT-2.md
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-27
canonical-ref: LICENSES/ACD-1.1-SELF-AUDIT.md / LICENSES/README.md
---

# LICENSES/ACD-1.1-SELF-AUDIT-2.md

## What

草案を我々自身が掃引して出たものの記録のうち、2026-09-17〜09-22 に足した 10 節（§3e〜§3m と §3k-2・1.1 と 1.2 の草案の掃引）。

## Why

`ACD-1.1-SELF-AUDIT.md` が 936 行で advisory（900）を越えた（Check 52）。古い節ほど新しく足されることが無いので、古い側を動かした。

## How (usage)

新しい節は 1 冊目（`ACD-1.1-SELF-AUDIT.md`）へ足す。この file は伸びない（予算 700 を越えたら、誤ってここへ足した印）。

## Constraints

- 本文は切り出しの前と 1 字も変えていない。節番号も動かしていない。
- 1 冊目に残した移転先の見出しが §3e〜§3m を名乗るので、他の文書の `ACD-1.1-SELF-AUDIT.md` §3x の参照は書き換えずに解決する（Check 471・前例は `ACD-1.1-CHANGELIST.md` の 3e / 3f の見出し）。
- 移した節の中の `ACD-1.1-SELF-AUDIT.md` は、切り出す前の同じ file を指す。

## Change impact

- `list_open_items.py` は `ACD-1.1-SELF-AUDIT*.md` を全部読む（1 冊だけ読むと、ここに在る未閉の 🔴 が一覧から黙って消える）。

## Audience-specific notes

### For AI agents（次担当）

- ここへ節を足さない。1 冊目へ足す。

### For human engineers（新卒レベル）

大きくなった記録の古い半分を、別のファイルに分けたもの。

### For third parties / auditors

内容は分ける前と同じで、置き場所だけが変わった。

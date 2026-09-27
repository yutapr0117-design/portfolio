---
file: LICENSES/rounds/2020-05-license-review-unlicense-veto-observed.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-27
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/ACD-1.0.review-doctrine.md §1.128 / LICENSES/AS-OF.md (委員会の理由書の逐語)
---

# LICENSES/rounds/2020-05-license-review-unlicense-veto-observed.txt

## What

**"veto against Unlicense" スレッド全 17 通**（2020-05-16〜2020-06-03・2026-09-27 取得）。
**我々宛ではなく、ACD-1.0 についてでもない。**

## Why

**Unlicense は本ドシエが依拠している先例**である —— 公有化の献呈でありながら、
**許諾の文言も併せ持っていたために承認された**。**その理由書は `AS-OF.md` が逐語で持っていたが、
それに逆らった側の議論は持っていなかった。**

**反対は実務弁護士（Stuart Langley 氏）からで、しかも「テキストが通るか落ちるかの試験」の形で
述べられている** —— だから引用できるだけでなく、**ACD-1.0 に当てて測れる**。

- *"Unlicense falls on the side of '**this is not a license**' to me largely because I read the
  second paragraph as **a description of what the author thinks public domain means, not a
  clear intent to convey rights**."*
- *"I would never advise a client to sign a commercial license that did not have
  **conventional, well-trodden language of license such as 'Licensor grants X rights....'**"*
- *"If it becomes an OSI approved license, **I still will advise against using** software
  encumbered with the Unlicense."*

**ACD-1.0 §4.1 はその形そのものである** —— *"**The Dedicator grants You** a worldwide,
royalty-free, non-exclusive, irrevocable, perpetual, sublicensable, and transferable licence…"*
（`review-doctrine.md` §1.128 が測定と逆側を書いている）。

## How

月次 mbox を**ブラウザ相当の UA** で取得し、件名 `veto against Unlicense` で全 17 通を
header ごと無改変で切り出した（**選別ではなくスレッド全体**）。

## Constraints

- **無改変で保存する**（`rounds/README.md`）。
- **観測（`-observed`）であって受領ではない。**
- **⚠ この反対は承認を止めなかった。** 「有力な反対があった」ことと「反対が正しかった」ことは別で、
  **どちらも本 file からは決まらない。**

## Change impact

- `rounds/` に file を足したら `rounds/README.md` の在庫表と件数も同じ commit で（**Check 465**）。

## Audience-specific notes

- **AI（実装者）**: **この試験に ACD が通ることは、承認の予測ではない。** 反対者が挙げた
  もう 1 つの要素（*"wide use without any problems is a big factor"*）に我々は答えられない。
- **監査人**: 取得日は本文冒頭。同じ URL を同じ UA で取れば再現できる。

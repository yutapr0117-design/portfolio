---
file: LICENSES/rounds/2026-09-14-license-review-openmdw-bundling-defence-observed.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-27
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/ACD-1.0.review-corpus.md §1.78 / LICENSES/ACD-1.0.against.md
---

# LICENSES/rounds/2026-09-14-license-review-openmdw-bundling-defence-observed.txt

## What

**`license-review` の OpenMDW-1.1 スレッドのうち、2026-09-12 より後の 2 通**（2026-09-27 取得）。
**我々宛ではなく、ACD-1.0 についてでもない。**

| | 発言者 / 日付 | 要点 |
| :-- | :-- | :-- |
| (A) | **Michael Dolan 氏**（OpenMDW steward） 2026-09-14 | Fontana 氏の *"flawed in its **basic conception**"* への反論。*"The **unit of open source licensing has always been the work as provided**, not each file measured separately against the policy that motivated each clause"* / *"**Apache-2.0's own patent termination applies to the entire Work**, including documentation and build scripts that (presumably) face no patent exposure at all"* |
| (B) | **Josh Berkus 氏** 2026-09-14 | 委員長の *"Can you explain how?"*（偶発的な侵害コピーはどう起きるのか）への回答。8 つの経路を挙げ、その 1 つが *"**GenAI & Autocomplete**"* |

## Why

**`review-corpus.md` §1.78 は 2026-09-12 までしか読んでおらず、この 2 通はその外側にある。**

**(A) は §1.78 (a) の両側に効く。** §1.78 (a) は「束ねの OSD 9 の疑いは ACD に当たらない
——終了が無いから」と書いている。**Dolan 氏の反論はそれより広く、終了があっても束ねること
自体は Apache-2.0 の先例で守られると述べており、ACD にとっては a fortiori 有利**である。
**⚠ 逆側**: それは **steward 自身の弁明であって委員会の結論ではない**。しかも Fontana 氏の
言い方は *"basic conception"* ——**機構ではなく構想への評価**で、ACD も §1.2 で 6 種の素材を
1 語に束ねている。**ACD が外れるのは終了が無いという 1 点によってであり、その 1 点を外した
読みは我々に届く。**

**(B) は #134（「何が Work か」の判定責任が運用に乗っている）の証拠側である。**
偶発的な混入が常時起きるという当事者の証言は、**§2.6 の特定義務が現実にどれだけ重いかを
示す**。**⚠ 逆側**: これは ACD 固有の欠陥ではなく、**MIT を含む承認済みの寛容ライセンスが
すべて共有する性質**である（§1.78 が既にそう書いている）。

## How

`https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-September.txt`
を**ブラウザ相当の UA** で取得し、該当 2 通を header ごと無改変で切り出した。

## Constraints

- **無改変で保存する**（`rounds/README.md`）。
- **観測（`-observed`）であって受領ではない。**
- **どちらの発言も ACD-1.0 に言及していない。** 沈黙の反証にも承認の見込みの証拠にも使わない。

## Change impact

- `rounds/` に file を足したら `rounds/README.md` の在庫表と件数も同じ commit で（**Check 465**）。

## Audience-specific notes

- **AI（実装者）**: (A) を「ACD の束ねは安全だ」の根拠に**単独で**使わないこと。当たらない理由は
  終了の不在であって、束ねが一般に安全だからではない。
- **監査人**: 取得日は本文冒頭。同じ URL を同じ UA で取れば再現できる。

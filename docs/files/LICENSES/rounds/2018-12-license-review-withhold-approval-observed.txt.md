---
file: LICENSES/rounds/2018-12-license-review-withhold-approval-observed.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-28
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/ACD-1.0.board-decisions.md (第 3 の帰結) / LICENSES/ACD-1.0.against.md
---

# LICENSES/rounds/2018-12-license-review-withhold-approval-observed.txt

## What

**Convertible Free Software License スレッド（2018-09〜2019-03・126 通）から 2 通**
（2026-09-28 取得）。**我々宛ではなく、ACD-1.0 についてでもない。**

**選別の規則を本文冒頭に書いてある** —— 差出人が `opensource.org` のアドレスで、
かつ本文に `withhold` または `clarified process` を含むもの。

| 発言者 / 日付 | 要点 |
| :-- | :-- |
| **Richard Fontana 氏**（OSI として・2018-12-07）| *"In my most recent License Committee Report I recommended that the OSI **reject** … Subsequently, however, at its November board meeting, **the OSI decided to withhold approval** … **pending submission of a redrafted version**."* |
| **Simon Phipps 氏**（OSI President・2018-12-10）| *"OSI's Board **does not give legal advice, practice law or design licenses**. We were recommended to reject your license … but as there seemed to be plenty of comment … **we opted to withhold approval instead (under the clarified process)** so you could act on it if you wanted to. **You do not have to do so if you don't want to.**"* |

## Why

**`board-decisions.md` は理事会の議事録から「承認でも否決でもない第 3 の帰結」を確立していた**
（*"a license could stay in a status where it is **not approved**"*・2025-07-18）。
**これはその帰結が、名前で、否決の勧告を覆して選ばれた、リスト側の実例である**（2018 年）。

**もう 1 つが重い** —— **提出者が Board から何を期待できないかを、President が述べている。**
ドシエは B1（法的レビュー不在）への答えとして
*「提出することが、単独起草者が弁護士の目を通す経路そのものである」*（`review-precedents.md` §1.52）
を持っているが、**Board は法律実務をしないと明言されている。**
**リストの参加者が論評することと、Board が助言することは別である** ——
**§1.52 を否定はしないが、射程を狭める**（`against.md` #274）。

## How

月次 mbox を**ブラウザ相当の UA** で取得し、上記の規則で 2 通を header ごと無改変で切り出した。

## Constraints

- **無改変で保存する**（`rounds/README.md`）。
- **観測（`-observed`）であって受領ではない。**
- **⚠ 2018 年の「clarified process」が現行の process と同一である保証は無い** ——
  **現行 process ページには `withhold` の語が無い**（#139 の実測）。

## Change impact

- `rounds/` に file を足したら `rounds/README.md` の在庫表と件数も同じ commit で（**Check 465**）。

## Audience-specific notes

- **AI（実装者）**: **この 2 通は「否決されにくい」の証拠にもなり、「決まらないまま置かれる」の
  証拠にもなる。** 片側だけを引かないこと。
- **監査人**: 取得日と選別規則は本文冒頭。同じ規則で再現できる。

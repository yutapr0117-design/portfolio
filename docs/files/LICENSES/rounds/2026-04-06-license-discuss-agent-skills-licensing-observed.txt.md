---
file: LICENSES/rounds/2026-04-06-license-discuss-agent-skills-licensing-observed.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-22
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/ACD-1.0.against.md #211 / LICENSES/ACD-1.0.against.md #212 / LICENSES/ACD-OSI-BOTTLENECKS-EXTERNAL.md (B10)
---

# LICENSES/rounds/2026-04-06-license-discuss-agent-skills-licensing-observed.txt

## What

**`license-discuss` の「AI エージェントの skill をどうライセンスするか」スレッド全 3 通**
（2026-04-06）。**我々宛ではなく、ACD-1.0 についてでもない。**

| 発言者 | 要点 |
| :-- | :-- |
| **Moming Duan 氏**（ModelGo steward）| skill は「実行されるコード」ではなく指示集である。著作物か / ライセンスは執行可能か / 伝統的な OSS ライセンスは適切か |
| **Richard Fontana 氏** | *"open source software licenses are **extensively used for non-software material**"*、*"**completely appropriate** … if they are copyrightable"*、そして *"they are **appropriate even in situations where copyrightability is relatively dubious**"* |
| **Pamela Chestek 氏** | *"Can you elaborate?"* |

## Why

**ACD が立つ 3 つの gap のうち 1 つに、正面から当たるから。**

**gap 3 は「機械生成物の権利存否への対処」**（register B10・§9）である。
Fontana 氏の最後の節は、**§9 が存在する理由そのものの状況について、
「既存の道具で足りる」と述べている。**

**⚠ 同じ 1 通が逆にも働く。** その直前で彼は質問者の米国著作権局の読みを訂正し、
*"sufficiently creative prompts **may be copyrightable**"* と述べている ——
**境界が本当に不確かであることの裏づけであり、それは §9 の前提である。**

**⚠ そして §9 の中身は *fallback* である** ——権利が存在しないときに何が起きるかであり、
伝統的なライセンスはそれを持たない。Fontana 氏が論じているのは**貼ることの適否**であって、
**貼ったものが何も掴まなかったときの話ではない。**

**主題はこのリポジトリが実際に公開している資料の類型でもある**
（`.well-known/agent-skills/index.json`）。**そこを測ったら #212 が出た。**

## How

`https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-April.txt`
を**ブラウザ相当の UA** で取得した既存キャッシュから、該当 3 通を無改変で切り出した。

**見つけ方は #209 / #210 と同じ** ——読む単位を発言者にし、**実際に決める側の 4 人**
（Chestek / McCoy / Fontana / Piana）が 2026 年に発言した **47 スレッド**を列挙して、
**ドシエに 1 件も現れないもの**を選んだ。

## Constraints

- **無改変で保存する。**
- **観測（`-observed`）であって受領ではない。**
- **Fontana 氏の見解は `license-discuss` 上の個人の意見であり、委員会の判断ではない。**
  *"I'm starting to come around to the view"* と本人が述べている。
- **有利な半分だけを引かない。** 同じ 3 通が両向きに働く。

## Change impact

- `rounds/` に file を足したら `rounds/README.md` の在庫も同じ commit で（**Check 465**）。
- **gap 3 についての主張を書くときは、この file を読んでから書く。**

## Audience-specific notes

- **AI（実装者）**: **gap は「実在するか」ではなく「審査者が gap として経験するか」で決まる。**
  この 1 通はその区別を突いている。
- **監査人**: 取得元と日付は本文冒頭。同じ URL を同じ UA で取れば再現できる。
- **第三者**: 我々の主張に不利な材料である。**だから逐語で置いてある。**

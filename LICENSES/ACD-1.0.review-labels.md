---
file: LICENSES/ACD-1.0.review-labels.md
audience: OSI license-review / license-discuss participants, licence reviewers, 監査人
last-updated: 2026-09-19
canonical-ref: LICENSES/ACD-1.0.reviewer-positions.md (主題ごとの記録・ここから切り出した) / LICENSES/ACD-1.0.against.md (#157 / #160 / #161) / LICENSES/ACD-OSI-BOTTLENECKS.md (B1 / B2)
---

# リストが我々の類型に付ける呼び名と、その呼び名が実際に指している害

**`ACD-1.0.reviewer-positions.md` から 2026-09-19 に切り出した。節番号は変えていない**ので
既存の `§1.98` / `§1.99` 参照はそのまま解決する。**切り出した理由は 2 つ** ——
元ファイルが Check 365 の 1,000 行に当たったこと、そして
**他の §1.x が「特定の人・特定の提出」の記録であるのに対し、この 2 節は「呼び名」の記録**で、
**読む動機が違う**こと。

**掘り方は 2 節とも同じ**: **第三者が使った語を、アーカイブ 145 か月分の corpus 全体に当てる。**
**運んできたのは結論ではなく語だった**（`against.md` #158）。

## 1.98 リストが我々の類型に付けている名前と、その名前が本当に指している害（2026-09-19）

**外部レポート 3 本が「クレヨン・ライセンス」という語を、非弁護士が起草したライセンスへの蔑称として
挙げていた。** **語が実在するかをアーカイブで確かめたら、実在しただけでなく、
その語について最も重要な発言が見つかった。**

### 定義 —— Bruce Perens 氏（`license-discuss` 2025-10-01）

> *"A **\"crayon license\"** is a license obviously produced by a **non-legal-professional**, which
> has obvious faults that a legal professional would know to avoid. The name comes from a Monty
> Python sketch in which a man presents a cat license which is a dog license with the word dog
> crossed out and \"cat\" written in, in crayon."*

**我々は定義の前半に当たる**（非弁護士が起草した）。**後半に当たるかは、実際に faults があるかで決まる。**

### 何が label を引き寄せるか —— McCoy Smith 氏（`license-discuss` 2024-02-05・Anu Initiative 宛）

> *"It is a crayon license, and **the author points out its whimsical nature while wishfully saying
> the terms bind anyway**. There is no point in passing it on for disapproval or doing anything else
> to take it seriously. Just politely tell the author there isn't a chance."*

**引き金は起草者自身が非真面目さを示すこと**である。**ACD はその形をしていない**
——本文は真面目に書かれ、弱点は先に開示され、条文は逐語で検証できる。**だがそれは我々の自己評価である。**

### 🔴 最も重要な 1 文 —— Pamela Chestek 氏（Licensing Committee・`license-review` 2019-06-27・CAL の審査）

> *"**The high likelihood that the license would be interpreted in significantly different ways in
> different legal jurisdictions militates against its approval.** Although the CAL is not, by any
> means, a \"crayon\" license, **it has the potential for the same negative consequence, which is
> unpredictable interpretation**."*

**これは我々の risk model を書き換える。**

- **委員長が名指しした害は「非弁護士が書いたこと」ではなく、「法域をまたいで解釈が大きく割れること」である。**
- **「クレヨン」はその害の代理指標であって、害そのものではない。**
- **弁護士が書いたライセンス（CAL）でも同じ害を持ちうる、と明言している。**

**そして ACD は、構造上まさにその害の側にある** —— §3 / §4 / §5 は法域ごとに効き方が変わることを
前提に並置され、§3.3 は放棄不能の法域を、§12.2 は人格権放棄不能の法域を、§15.2 は無効な条項を、
それぞれ法域ごとに扱う。**「法域によって違う読まれ方をする」ことを設計として引き受けている。**

### だからこの発見は、B1 を作り直す

**register B1（弁護士レビュー不在）は class 1 で「提出することが弁護士の目を通す経路」と記録されている
——それは今も真である。** **だが Chestek 氏の 1 文は、B1 の下に *AI で動かせる* 部分があることを示す。**

| | |
| :-- | :-- |
| **動かせない** | 弁護士が読んだという事実そのもの（B1） |
| **動かせる** | **解釈のばらつきを減らすこと** ——E19 / E20 / E21 / E23 / E24 はすべてこれをやっていた。**名前が付いていなかっただけである** |

**そして「クレヨン」の label は致命傷ではない。**

- **CAL はこの発言の後に承認された**（2019-06 の時点では *"the reasons that the license has not been
  approved"* と書かれている）。
- **`license-discuss` の投稿者が Unlicense を *"the Unlicense are crayon"* と書いている**（2024-04-05）
  ——**承認済みのライセンスにも付く label である。**
- **Perens 氏は SIL Open Font License を deprecate 候補に挙げている**（2022-12-13）——同じく承認済みである。

### 記録されている唯一の防ぎ方 —— Van Lindberg 氏（`license-discuss` 2020-01-05・CAL 審査中）

> *"You bring up the vanity licenses, the crayon licenses, etc. **The CAL is none of those.**"*

**黙殺ではなく、明示的に区別する。** **我々の入口ページは既に弱点を先に述べているが、
「この類型ではない」と正面から言ってはいない。**

### ⚠ この節が establish しないこと

**Chestek 氏の発言は CAL についてのもので、ACD についてではない。** 2019 年の発言であり、
**同じ委員が今も同じ重みを置くかは分からない。** そして**「解釈のばらつきを減らした」という我々の主張は、
測っていない** ——`ACD-1.1-SELF-AUDIT.md` §3k が相互参照の密度を測ったが、
**解釈のばらつきそのものを測る方法を我々は持っていない。**

## 1.99 2 つ目の label ——「vanity」は、このリストでは定義を持っている（2026-09-19）

**§1.98 の最後で Van Lindberg 氏が *"the vanity licenses, the crayon licenses, etc."* と
2 つを並べていた。** **crayon は §1.98 で追った。ここは vanity を追う。**
**同じ掘り方**（第三者レポートが運んできた語を corpus 全体に当てる）で、
**`license-discuss` / `license-review` の 145 か月分に 10 ファイル・26 箇所**あった。

**結論を先に置く**: **crayon が「誰が書いたか」の label であるのに対し、vanity は
「誰のためのテキストか」の label で、しかも OSI 自身の文書に定義がある。**
**そして定義に当てるかぎり ACD は当たらない。当たるのは定義ではなく、
その周りで述べられている 2 つの派生**である。

### 定義 —— OSI の License Proliferation Report のカテゴリ 5

**同じ 2 文が、2020 年に 3 人から独立に引用されている**（Richard Fontana 氏 2020-03-31 /
McCoy Smith 氏 2020-04-01 / Lawrence Rosen 氏 2020-04-01・いずれも `license-discuss`
"Generic process for removing approved licenses" スレッド）:

> **"Non-reusable licenses** —— *Licenses in this group are **specific to their authors and
> cannot be reused by others**. Many, but not all, of these licenses fall into the category of
> **vanity licenses**."*

**⚠ 出典の扱い**: **我々が確かめたのは「リスト上で 3 人が同じ文を引用している」ことであって、
`opensource.org/proliferation-report` の現行ページの文言ではない**（本増分の時点で当たっていない）。
**引用の一致は強い証拠だが、現行ページの証拠ではない。**

### その定義を条ごとに当てる —— Marc Jones 氏の 4 段テスト（`license-discuss` 2019-02-11）

**この vein で最も使える 1 通。** *"the requirement that a license be **reusable** would
significantly reduce the risk of a return to vanity license proliferation"* と述べ、
**除外すべきものを 4 つ挙げている。** 1 つずつ当てた:

| Jones 氏の除外基準（逐語） | ACD-1.2 | 根拠 |
| :-- | :-- | :-- |
| *"licenses that **hard code a specific person/company as being the licensor and the code base** being licensed"* | **当たらない** | §16.3 *"may be applied by anyone, to any work in which they hold rights, without permission from, notice to, or any relationship with the authors of this Dedication"*。**固有名詞 0・置換テキスト 0**（`submission.md` §4b の実測）|
| *"licenses that **hard code the licensor being in an unreasonably privileged position**"* | **🔴 唯一、綺麗には抜けない** | 下の項 |
| *"licenses that required **significant changes or modifications to the license text** to be used by others"* | **当たらない** | **採用に本文の編集が 1 箇所も要らない**（同 §4b）|
| *"if only the company sponsoring the license is **capable of complying** with the license, the code is not really open source"* | **当たらない。ここが最も強い** | **§10.1 により条件が 1 つも無いので、遵守できない者が存在しない**（`submission-reference.md` の *"possible to comply on submission"* と同じ構造）|

### 🔴 4 つのうち 1 つ —— Steward は、本文の中に書かれた特権である

**§16.4 は改変テキストを同名・同識別子で配布することを禁じ、*"except by the Steward
(Section 16.5)"* と例外を置く。§16.5 はその役割を「この名称と識別子でこのテキストを最初に
公表した者」と定義する。** **これは Work についての特権ではない**（§16.6 が
*"They are not terms of the Work, they bind no recipient of the Work"* と述べる）が、
**Jones 氏の基準は「licensor が本文の中で privileged な位置に置かれていないか」を問うており、
著作物についての限定を持たない**（§10.1 が自分の射程に置いている種類の限定が、この基準には無い）。

**⚠ 逆側を同じ重さで**: **steward を持つ承認済みライセンスは多い**（Apache は ASF、MPL は Mozilla、
GPL は FSF）。**違うのは、それらが本文の外で運用されているのに、ACD は本文の中に書いていること**である。
**MIT / 0BSD / Unlicense は steward を本文に持たない。** そして**書いた理由は E14**
——識別子が固定テキストを指し続けることを、登録簿が引き受けるまでのあいだ本文で保つためで、
`ACD-1.1-CHANGELIST.md` §2.6 はそれを「**登録されるまでの橋**」と呼んでいる。
**したがってこれは欠陥ではなく取引である** ——**識別子の安定と、本文内の特権の不在は、同時には持てない。**
**当たられたときに黙るのではなく、取引だと述べる**（`against.md` #160）。

### 派生 1 —— 名前（Bradley M. Kuhn 氏・`license-discuss` 2022-12-13）

> *"the ?Open Logistics License? from the ?Open Logistics Foundation? looks a bit old-school
> vanity-style to me — since the name is **either designed to promote the name of the org, or
> it's designed to make it seem like it's the only appropriate license for work on the general
> topic** of ?open logistics?."*

**前半は当たらない**（"Autonomous Commons" は組織名でも人名でもない）。
**後半は当たりうる** ——**"Autonomous" を冠した名前は「自律的なシステムのための唯一の適切な
ライセンス」と読まれうる。** **本文の側の答えは §16.3 の *"It is not specific to any project,
person, organisation, jurisdiction, or field of endeavour."* だが、
**異議は名前についてのもので、本文を読む前に起きる**（`against.md` #161）。
**同じ人が名称変更を評価して *"It's reasonably clear now that this is just a license published
by a single organization"* と述べている** ——**名前についての異議は、名前を変えれば消える種類の
ものだと、同じスレッドが示している。**

### 派生 2 —— label を外す唯一の手（Kuhn 氏・`license-review` 2023-01-18・OLL v1.3 宛）

**Josh Berkus 氏の問い** *"why/when someone would need to use this license instead of the APL2"*
**に答えが無いことを理由に**、Kuhn 氏はこう締めている:

> *"absent that explanation, this **really does still look like a vanity license to me at the
> moment**."*

**つまり vanity は、テキストの純度ではなく *gap の説明* で外れる label である。**
**これは `against.md` #84（「なぜもう一つ？」）と、承認基準 7（gap は要件）と、同じ 1 点を指している。**
**我々はその説明を持っている**（`submission.md` §1b / §4a、`comparison.md` §1）
**——持っていなかったのは、その説明が *この label に対する答えでもある* という接続だけである。**

### ⚠ この節が establish しないこと、そして最も不利な 1 通

**Richard Fontana 氏（当時 `richard.fontana at opensource.org`・OSI 理事・`license-discuss`
2019-02-06）**:

> *"I think that the **business model of the license submitter can be a material consideration**
> when assessing whether the proposed license meets the OSD"* …
> *"in practice licenses submitted by businesses tend not be used by other licensors (apart from
> forks). **That was one of the reasons why the vanity corporate licenses of the earlier era
> were problematic.**"*

**submitter が何のためにそれを出しているかは、審査に持ち込んでよい材料だと、理事が述べている。**
**我々の場合それは「AI に自走させる実験のポートフォリオ」であり**、
**2026-09-09 の moderator 通知が *"being used as a proof-of-concept"* と述べたのと
同じ方向を指す**（B14）——**7 年離れた 2 人が、別の文脈で、同じ問いを立てている。**
**これは反論すべき点ではなく、先に述べておくべき点である**（`against.md` #161）。

**そして Fontana 氏は同じ時期にもう 1 つ述べている**（2020-01-04）——
*"the OSI may have taken the wrong path very early on by developing a process that **encouraged
submission of novel, community-untested licenses**"*、
*"Maybe it would be better for OSI to have the expectation that **license review will only take
place some months or years after a license is already in practical use**."*
**これは B2（採用実績の不在）を、上級の参加者が方針として述べたものである。**
**Atkinson 氏の 1 文（#113）と同じことを、別の人が別の年に述べている。**

**この節が establish しないこと**: **Kuhn 氏・Fontana 氏・Jones 氏の発言はいずれも ACD について
ではない。** **proliferation report の現行文言も確かめていない。** そして
**Jones 氏の 4 段テストは提案であって規則ではない** ——**採用されたという証拠は無い。**

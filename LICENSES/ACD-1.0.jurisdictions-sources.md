---
file: LICENSES/ACD-1.0.jurisdictions-sources.md
audience: ai, human (提出者), 監査人, 採用検討者, 学術研究者, 第三者全般
last-updated: 2026-11-16
canonical-ref: LICENSES/ACD-1.0.jurisdictions.md (法域ごとの読み・この文書の元) / LICENSES/ACD-1.0.against.md (#170 外から届いた法源)
---

# ACD-1.0 — 法域別の読みの、外から届いた法源とその原典（`jurisdictions.md` の §9 と §9a）

この文書は `ACD-1.0.jurisdictions.md` の §9（外から届いた、未読の法源）と §9a（その原典の読み）を、
2026-11-16 に分けて置いたものである。本文は移す前と同じで、節の番号もそのまま持つ。分けた理由は、
法域ごとの読みに一次の法源を足し続けると元の文書が 1,000 行の上限（Check 365）に届くため。
法域ごとの読み（日本・ドイツ・フランス・米国・EU・英国）と「この文書の限界」は元の文書に残る。

## 9. 外から届いた、未読の法源（2026-09-20・`against.md` #170）

**2026-09-20 の敵対的レビューが名前を挙げた法源・判例のうち、本ドシエが一度も記録していなかったもの。**
**⚠ どれも原典で読んでいない。** この環境からは判決文も指令の原文も取得できていない。
**したがってこの表は「主張」ではなく「読む対象の列」である** ——
**読む前に引けば、開いていない権威を借りることになる。**

| 法源 / 判例 | 当たる条 | レビューの主張（要約・**我々の読みではない**）| 読んだら何が決まるか |
| :-- | :-- | :-- | :-- |
| **Kneschke v. LAION**（ハンブルク地裁 → **控訴審 HansOLG 5 U 104/24**）| §6.2 / §6.3 | 機械可読な TDM オプトアウトの有効性が現に争われている | **✅ 2026-09-20 に控訴審の press release を読んだ。下の §9a (9)。レビューは第一審しか挙げていない。** |
| **Ryanair v PR Aviation**（CJEU）| §7.2 | **保護されないデータベース**には指令 96/9 第 15 条（利用者の権利を制限する契約を無効とする規定）が及ばず、**契約で自由に制限できる** | **§7.2 の許諾が、権利者側の TOS によって迂回されうるか** |
| **Qimonda**（Chapter 15）| §2.9 | 越境倒産では 11 U.S.C. §365(n) の保護が失われうる | **✅ 2026-09-20 に判決本文を読んだ。下の §9a (10)。構造は当たり、結論は逆で、§2.9 の設計の根拠になる** |
| **17 U.S.C. §201(b)**（職務著作）| §2.6 / §2.7 | 企業に雇用された contributor は、§2.6 が献呈させようとする権利を持っていない | **§2.7 の「保有する権利にしか及ばない」で足りるか** |
| **DMCA 17 U.S.C. §1202**（CMI）| §16.4 | 名称・識別子の制限が著作権管理情報の要件と交差する | **§16.4 が「本文についての規律」に留まるか** |
| **消費者契約法 8 条 1 項**（日本）| §14.1 | 故意・重過失の全部免責は無効 | **§14.2 の「法が許す最大限」で足りるか** |
| **droit de retrait**（フランス）| §2.2 | 撤回権の事前放棄は無効とされる蓋然性 | **✅ 2026-11-08 に原典で読んだ（§4 と下の §9a (11)）。ソフトウェアは L121-7 2° で外れ、それ以外の Work には L121-4 が残る** |
| **不公正契約条項の枠組み**（EU）| **§15.3**（1.2 草案では §15.6・1.1 は削除）| 不明確な条項を受領者に有利に読む強行規定があり、**contra proferentem の排除は実効性を失う** | **✅ 2026-09-20 に原典で読んだ。下の §9a。** |

### 9a. 8 件すべてを原典で読んだ —— 判例 2 件のうち 1 件は判決本文、1 件は裁判所自身の発表まで（2026-09-20）

**⚠ 訂正（2026-11-08）**: この見出しは「8 件すべて」と書いたが、下の表に droit de retrait の行は無く、
2026-11-08 まで原典を読んでいなかった。`against.md` #176 の「8 件中 7 件」も同じ数え違いである。
読んだ結果は表の最後の行と (11) に置いた。

**⚠ この節は「6 件は未読のまま」と書いて始まった。** その記述は**試さずに書いたもので、誤りだった**
——オーナーの指摘（*「そのまま読みに行くことがあなたは可能です」*）で取りに行くと、**7 件が取れた**
（`against.md` #176）。**取れなかったのは Kneschke 判決の本文 1 件だけで、
それも「openjur が人間確認を要求する」という具体的な理由である。**

| 法源 | 取得元 | 結果 |
| :-- | :-- | :-- |
| 指令 96/9/EC 第 15 条 | EUR-Lex CELEX:31996L0009 | ✅ 逐語 |
| **Ryanair v PR Aviation** | EUR-Lex CELEX:62014CJ0030 | ✅ **主文を逐語** |
| 指令 93/13/EEC | EUR-Lex CELEX:31993L0013 | ✅ 逐語 |
| **17 U.S.C. §201(b)** | Cornell LII | ✅ 逐語 |
| **17 U.S.C. §1202** | Cornell LII | ✅ 逐語 |
| **11 U.S.C. §365(n)** | Cornell LII | ✅ 逐語 |
| **消費者契約法 8 条** | e-Gov 法令 API（412AC0000000061）| ✅ 逐語 |
| **UrhG 44b 条 / UrhG 60d 条**（Kneschke の争点）| gesetze-im-internet.de | ✅ **条文は逐語。判決本文は未取得**（openjur が captcha）|
| **HansOLG 5 U 104/24**（Kneschke 控訴審・2025-12-10）| justiz.hamburg.de の press release | ⚠ **裁判所自身の発表は逐語。判決本文ではない**（下の §9a (9)）|
| **Jaffé v. Samsung**（Qimonda 控訴審・4th Cir. 2013-12-03）| ca4.uscourts.gov の公刊判決 PDF | ✅ **判決本文を全文（64,760 文字）**（下の §9a (10)）|
| **CPI L121-4 / L121-7**（droit de retrait）| Légifrance LEGIARTI000006278894 / LEGIARTI000006278899 | ✅ **2026-11-08 に逐語**（L121-4 は断片を繋いだもの・下の §9a (11)）|

**読めた 7 件について、レビューの主張は構造としては当たっており、射程は述べられていたより狭い。**

#### (1) 指令 96/9/EC 第 15 条 —— 逐語（CELEX:31996L0009）

> **Article 15 —— Binding nature of certain provisions.**
> *Any contractual provision contrary to Articles 6 (1) and 8 shall be null and void.*

**第 6 条 (1) と第 8 条は「lawful user」の権利**であり、**保護されるデータベースについて働く。**
**したがって「保護されないデータベースには第 15 条が無効化するものが無い」という読みは、
条文の構造と整合する。** レビューの指摘はここまでは当たっている。

**⚠ だが ACD については別の条が既に答えている。** レビューは
「Dedicator が利用規約でスクレイピングを禁じれば §7.2 の許諾を契約で無効化できる」と述べるが、
**§5.2(b) は Dedicator が *"by contract, terms of service, access condition, click-through,
registration requirement, or any other collateral means"* 義務を課さないと約束している条である。**
**これは「付随手段で許諾を空洞化しない」ための covenant そのもの**で、
**レビューはこの条を見ていない**（`against.md` #170 の**6 件目の見落とし**）。
**⚠ ただし §5.2(b) は Dedicator を縛るのであって、第三者のプラットフォームは縛らない**（#171）。

#### (2) 指令 93/13/EEC —— 逐語（CELEX:31993L0013）

> **Article 5.** *Where there is doubt about the meaning of a term, the interpretation most
> favourable to the consumer shall prevail.*
>
> **Article 2.** *(b) 'consumer' means any natural person who … is acting for purposes which are
> outside his trade, business or profession; (c) 'seller or supplier' means any natural or legal
> person who … is acting for purposes relating to his trade, business or profession …*
>
> **Article 3 (1).** *A contractual term which has not been individually negotiated …*

**contra proferentem は確かに強行規定として在る。** **だが射程は 2 つの当事者要件で限られている**
——**事業として行為する提供者**と**事業の外で行為する自然人**の間の契約である。

**したがってレビューの「§15.6 は実効性を失う」は、無条件には成り立たない。**
**成り立つ場合**: **Dedicator が事業として献呈しており、受領者が消費者である**とき
——**それは B2 が最も欠いている「組織の後ろ盾を持つ採用者」の場合**である。
**成り立たない場合**: 個人が無償で世界へ献呈する典型的な場合、
**指令の当事者要件を満たすかは疑わしい。**

**⚠ E25 は撤回しない。** E25 の理由は「§16 の上で 2 つの canon が順序なく働く」ことであって
**排除の執行可能性ではない。** **だが「戻したから効く」とは書けない** ——
**効く範囲は、誰が Dedicator であるかによって変わる。**

**⚠ この 2 件を読んで分かった一般形**: **外から来た指摘は、構造としては当たっていて
射程は広すぎることがある。** **原典に当たると、指摘は消えずに*狭くなる*。**
**狭くなった形の方が、我々にとっても審査者にとっても使える。**

**⚠ 最後の 1 行は、本日の自分の作業に当たっている。** **E25 を撤回はしない** ——
E25 の理由は「§16 の上で 2 つの canon が順序なく働く」ことであって、
**排除の*執行可能性*ではなかった**。**だが「戻したから効く」と読める書き方はしない。**

**⚠ そしてこの表は、レビューの他の主張を裏書きしない。** 同じレビューは
**§6.2 / §6.3 が第三者の留保を無効化する**と述べているが、**その 2 条は自分でそう述べていない**
（§6.2 *"does not purport to defeat a Reservation made by another rightsholder"* /
§6.3 *"the Dedicator has no power to withdraw it and this Section does not purport to give one"*。
**§6.3 の引用はレビューが読んだ 1.2 草案（と 1.1）の文言である。** **1.0 の §6.3 はこの但し書きを持たず**、
*"whether by the Dedicator or by another person"* の留保を *"to the fullest extent the Dedicator is able"* の限度で撤回すると述べるだけ
なので、**1.0 について同じ主張をされたら、答えは §6.3 自身ではなく §2.7 と「able」の語に頼ることになる**）。
**現物に当たれる主張は当たった。当たれない主張は、当たれないと書く。**

#### (3) Ryanair v PR Aviation（C-30/14）—— 主文を逐語

> *"Directive 96/9/EC … must be interpreted as meaning that **it is not applicable to a database
> which is not protected either by copyright or by the sui generis right** under that directive,
> so that Articles 6(1), 8 and 15 of that directive **do not preclude the author of such a database
> from laying down contractual limitations on its use by third parties**, without prejudice to the
> applicable national law."*

**レビューの要約は主文と一致する。** **そして最後の一句 *"without prejudice to the applicable
national law"* は、レビューが落としていた** ——**契約による制限は、各国法の下でなお争われうる。**

#### (4) 17 U.S.C. §201(b) —— 逐語

> *"In the case of a work made for hire, the employer … is considered the author for purposes of
> this title, and, **unless the parties have expressly agreed otherwise in a written instrument
> signed by them**, owns all of the rights comprised in the copyright."*

**§2.6 への攻撃は、条文に当てると成立しない。** **1.2 の定義条**は Dedicator を
「Covered Rights を保有し、または保有しうる限度で」に限り、
§2.7 は *"reaches only rights the Dedicator holds"* と述べる。
（**条番号は版で動く** ——1.0 では §1.3、1.2 では §1.4 が Dedicator の定義である。）
**雇用された contributor は持っていないものを献呈できず、この instrument もそう書いてある。**
**§201(b) の但書は逆に有利に働く** ——**書面の合意があれば従業者が権利を持ちうる**ので、
**§1.4 の「保有する限度で」は、その場合も正しく動く。**

#### (5) 17 U.S.C. §1202 —— 逐語

> *"(b) **Removal or Alteration** of Copyright Management Information.— No person shall,
> **without the authority of the copyright owner or the law**, (1) intentionally remove or alter
> any copyright management information …"*

**レビューは「被告は『削除を契約上許可された』と抗弁できる」と述べたが、条文はそれ以上を述べている**
——**禁止そのものが *"without the authority of the copyright owner"* を要件にしている。**
**§10.2 が *"You need not … reproduce any notice"* と述べる以上、その authority は与えられており、
§1202(b) の要件が最初から満たされない。**
**したがって「識別子の表示を法的に守る手段が無い」は正しく、それは #175 が
「帰属ゼロの費用」として既に記録したもの**である。**新しい欠陥ではなく、記録済みの費用の法的な裏づけ。**

#### (6) 11 U.S.C. §365(n) —— 逐語

> *"If the trustee rejects an executory contract under which the debtor is a licensor of a right to
> intellectual property, the licensee … may elect … (B) **to retain its rights** …"*

**§365(n) は「executory contract が rejected された場合」の受け皿である。**
**ACD-1.1 以降は §2.9 で「倒産手続は許諾に影響しない」と述べ、1.0 の §2.9 が持っていた
*"not executory"* という*結論*は E5 で落としている**（法廷地の分類を本文が断定しないため）。
**レビューの Qimonda の点（越境倒産で §365(n) の保護が失われうる）は、条文からは確かめられない**
——**判例の射程の問題であり、判決本文は未取得である。**

#### (7) 消費者契約法 8 条 —— 逐語（e-Gov・412AC0000000061）

> **第八条** 次に掲げる**消費者契約**の条項は、無効とする。
> 一 **事業者**の債務不履行により消費者に生じた損害を賠償する責任の**全部**を免除し…
> 二 …（**故意又は重大な過失**によるものに限る）…責任の**一部**を免除し…
>
> **第二条** 「消費者」とは、個人（**事業として又は事業のために契約の当事者となる場合を除く**）をいう。
> 「事業者」とは、法人その他の団体及び**事業として又は事業のために契約の当事者となる場合における個人**をいう。

**93/13/EEC と同じ形の限定がある** ——**「消費者契約」＝消費者と*事業者*の間の契約**。
**個人が無償で世界へ献呈する場合、Dedicator が「事業者」に当たるかは疑わしい。**
**⚠ だが当たる場合は当たる** ——**組織の後ろ盾を持つ採用者**（B2 が最も欠いている層）が
Dedicator になれば、**§14.1 の全部免責は 8 条 1 項 1 号で無効**になりうる。
**§14.2 の「法が許す最大の範囲」はそのための条だが、8 条は「無効とする」と書いており、
縮減で救えるかは条文からは決まらない。**

#### (8) UrhG UrhG 44b 条 / UrhG 60d 条 —— 条文は逐語、判決は未取得

> **UrhG 44b 条 (3)** *Nutzungen nach Absatz 2 Satz 1 sind nur zulässig, wenn der Rechtsinhaber sich diese
> **nicht vorbehalten** hat. Ein Nutzungsvorbehalt bei online zugänglichen Werken ist nur dann
> wirksam, wenn er **in maschinenlesbarer Form** erfolgt.*

**§6.2 が名指ししているもの**（*"no notice, marking, metadata, protocol element, header, robots
directive, or other signal … is to be read as a Reservation"*）**は、まさに UrhG 44b 条(3) が
「機械可読な形式でのみ有効」と述べている当のものである。** **§6.2 は抽象的な用心ではなく、
名前のある制度に対応している**（§12.4 と 60 条の関係と同じ形）。

**⚠ 逆側**: **UrhG 60d 条（学術研究のための TDM）には `vorbehalten` の語が無い** ——**opt-out が無い。**
**したがってドイツにおける §6 の追加価値は、研究機関に対しては小さく、商用の TDM に対して大きい。**
**日本の 30 条の 4 について出した結論と同じ形である** ——**主張を弱い方へ言い直す。**

**⚠ 判決本文（PDF / 全文）は取れていない** ——openjur は人間確認を要求し、
OLG の press release は *"Eine anonymisierte Volltextfassung der Entscheidung kann angefragt werden"*
（全文は請求すれば得られる）と述べている。**以下は裁判所自身の press release に基づく。**

#### (9) 🔴 控訴審は既に出ている —— HansOLG 5 U 104/24（2025-12-10 判決・**レビューは第一審しか挙げていない**）

**取得元**: `https://justiz.hamburg.de/gerichte/hanseatisches-oberlandesgericht/gerichtspressestelle/
ki-und-urheberrecht-hanseatisches-oberlandesgericht-weist-berufung-zurueck-1126528`
（2026-09-20 に自己取得・ページ自身の日付は *Stand: 10.12.2025, 12:00*）。
**⚠ 2026-10-10 14:5x UTC 時点で、上の HTML ページは 404 になっていた**（Mac から完全な URL で再取得して確認・リポジトリ全体のリンク検査で発見）。
**同じ発表の裁判所自身の PDF 版**が `https://justiz.hamburg.de/resource/blob/1126574/2495057737fed4883eec42dce4d2430b/ki-und-urheberrecht-hanseatisches-oberlandesgericht-weist-berufung-zurueck-data.pdf`
にある（2 ページ・130,312 B・sha256 `ff96c0c33486a581…715c795e`・日付欄 *Hamburg, 10. Dezember 2025*）。**下に引いたドイツ語の逐語 8 箇所は、この PDF の抽出テキストと全件一致した**
（差は PDF 抽出に由来する空白とページ番号だけ）。PDF 本体は commit しない（Check 122）。**HTML 版が消えた理由（移転か削除か）は分からない。**
**`rounds/` には置かない** ——同ディレクトリの規則 6 が述べるとおり、そこは**我々のやり取りと、
我々を名指しした短い観測**のための場所であって、公開されている第三者ページの複製ではない。
**決定的な箇所を発言者（ここでは裁判所）と日付つきで引く**のが、この種の資料の扱いである。

**ハンブルク上級地方裁判所 第 5 民事部の press release（裁判所自身の発表）より:**

> Der 5. Zivilsenat … hat mit heute verkündetem Urteil (Az.: **5 U 104/24**) die Berufung eines
> Fotografen gegen das klagabweisende Urteil des Landgerichts Hamburg (Az.: 310 O 227/23)
> **zurückgewiesen**.

**決まったことは 4 つ**（いずれも我々の §6 に直接当たる）:

1. **UrhG 44b 条の適用が認められた** ——*"Deren Anwendbarkeit hatte das Landgericht … noch
   offengelassen"*。**第一審が開いたままにした点を、控訴審が閉じた。**
2. **エージェンシーが置いた利用留保は権利者に帰属させられる** ——
   *"müsse ein von dieser aufgestellter Nutzungsvorbehalt auch ihm als Rechtsinhaber zugerechnet
   werden"*。**他人が置いた signal が権利者のものとして扱われうる**という、**§6.2 が正面から
   扱っている当の状況**である。
3. **🔴 だがその留保は「機械可読の形式」を欠いていたので効かなかった** ——
   *"habe vorliegend aber nicht die gesetzlich vorgesehene Form (Maschinenlesbarkeit) aufgewiesen"*、
   *"so dass die streitgegenständliche Vervielfältigung zulässig gewesen sei"*（UrhG 44b 条 3 項 2 文）。
4. **UrhG 60d 条（学術研究）でも正当化される** ——データセットの作成自体が応用研究にあたり、
   *"Auch der Umstand, dass ebenso kommerzielle Anbieter den Datensatz nutzen könnten, führe zu
   keinem anderen Ergebnis"*（私企業の決定的影響が無い限り・60d 条 2 項 3 文）。

**⚠ 確定していない。** *"Die Entscheidung ist nicht rechtskräftig. Der Senat hat die Revision
zugelassen"* ——**連邦通常裁判所（BGH）の判断が残っている。**

**我々にとっての意味を、有利・不利の両方で書く。**

**有利**: **§6.2 は court-tested な問題に答えている。** 「誰が置いたかを問わず、Work に付随する
signal を Reservation と読まない」という §6.2 の一文は、**(2) の帰属と (3) の形式要件が
実際に争われた場面そのもの**を扱っている。**しかも §6.2 は 44b 条 3 項より広い**
——**機械可読な signal であっても Dedicator の側では Reservation と読まないと述べている。**
**§12.4 と 60 条の関係と同じく、名前のある制度に対応している。**

**不利**: **(4) により、ドイツでは研究目的の TDM は留保に関係なく通る。**
**したがってドイツにおける §6 の追加価値は、研究機関に対しては小さい。**
**さらに (3) は「留保が形式を欠いていた」から勝った事件であり、
*形式を満たした留保なら結論が変わりうる*ことを含意する** ——
**§6.2 の価値はそこで上がるが、同時に「他人の留保は §2.7 により我々の手に負えない」ことも変わらない。**

**⚠ 引用の限界**: **これは判決本文ではなく、裁判所の press release である。**
**全文は請求すれば得られると書かれているが、我々は請求していない。**

#### (10) Qimonda —— 判決を読むと、レビューの論点は §2.9 に対する**反論ではなく根拠**だった

**取得元**: 第 4 巡回区控訴裁判所自身のサイト（`https://www.ca4.uscourts.gov/opinions/Published/121802.P.pdf`・
2026-09-20 に自己取得）。*Michael Jaffé v. Samsung Electronics Co.*, No. 12-1802（2013-12-03 判決・PUBLISHED）。
**これは press release ではなく判決本文である**（64,760 文字・全文）。

**何が争われたか**: ドイツの倒産管財人（Jaffé 氏）が Chapter 15 の裁量的救済を求め、
**Qimonda の米国特許のライセンスを一方的に解除できる地位**を得ようとした。破産裁判所は救済を与えたが、
**4 日間の証拠調べの後、条件を付けた**:

> it conditioned the § 1521 relief with the requirement that Jaffé afford the licensees of
> Qimonda's U.S. patents the treatment they would have received in the United States under
> 11 U.S.C. § 365(n)

さらに 11 U.S.C. §1506 により、管財人による一方的解除は
*"would be manifestly contrary to the public policy of the United States"* であり、
*"a fundamental U.S. public policy promoting technological innovation"* を損なうとした。
**控訴審はこれを維持した**:

> the bankruptcy court reasonably exercised its discretion in balancing the interests of the
> licensees against the interests of the debtor and finding that application of § 365(n) was
> necessary to ensure the licensees under Qimonda's U.S. patents were sufficiently protected.
> Accordingly, we affirm.

**そして §1522(a) の読み方を確定させた** ——

> requiring a particularized balancing analysis that considers the "interests of the creditors
> and other interested entities, including the debtor,"

**レビューの主張は「越境倒産では §365(n) の保護が失われうる」だった。読むと、構造としては当たっている**
——Chapter 15 において §365(n) は**自動的に適用される規定ではなく、裁量的救済に付された条件**であり、
**4 日間の証拠調べと利益衡量を経て初めて**licensee に届いた。**ただし結論は逆で、licensee は勝っている。**

**我々にとっての意味**:

**有利**: **これは §2.9 に対する反論ではなく、§2.9 が採っている経路の根拠である。**
§365(n) に依存する設計は、越境倒産では**衡量の結果に依存する**ことが実際に示された。
ACD が採るのは別の経路で、**(a) §3 の surrender は完了した行為であって拒絶の対象が無く、
(b) §2.9 第 2 文が倒産手続の officer を §2.8 の承継人として捉えて §3・§4・§6・§8 に服させる。**
**「§365(n) が使えるはずだ」と言わずに済む設計であること自体が、この判決の教えるところである。**

**不利**: **同じ判決が、こういう結論は forum が事実と裁量で決めると示している。**
1.0 §2.9 は *"and so is not executory"* と分類まで断定しており、**我々は受領前に自分で E5 として記録し、
1.1 以降はその結論を落としている**。だが**残した第 1 文は「いかなる倒産手続も許諾に影響しない」という
結果の断定**であって、Qimonda が 4 日かけて決めたのはまさにその種の問いである
（`against.md` #178）。**⚠ 逆側**: 断定を緩めれば依拠価値が下がり語数も増える（B3）。
**実際に効いているのは断定ではなく §2.8 との接続**なので、直すべきは文言より、
**問われたときにこの判決を引ける準備の方である**（`review-responses-boilerplate.md` Q25）。

#### (11) droit de retrait —— CPI L121-4 と L121-7（Légifrance・2026-11-08）

逐語と読みは §4 に置いた。**レビューの主張（撤回権の事前放棄は無効とされる蓋然性）は構造として当たる**
—— L121-4 は譲渡の後でも撤回を認め、§2.2 の irrevocable はそれを事前に排除できない。**射程は述べられて
いたより狭い**: ソフトウェアの著作者は L121-7 2° によりこの権利を行使できず、残るのはソフトウェアでない
Work（データセット、文書）である。ドイツの UrhG 42 条も同じ形の撤回を定める（§3）。

### 9b. 外から渡された法令のまとめの記述を照合した（2026-11-20・portfolio-50）

オーナーが別の AI のまとめ（ACD-1.4 に関連する法令と、その全文を取れる公式の場所の一覧）を貼り、5 人で分担して一次資料を読むよう依頼した。まとめは材料であって結論ではないので、取得先の一覧は分担に使い、ACD と法についての記述は 1.4 草案と既に置いた写しに当てた（取得の分担は 30・2f・50・9b・1c・各写しは `rounds/2026-11-20-*`）。

| まとめの記述 | 当てたもの | 照合の結果 |
| :-- | :-- | :-- |
| 第 1.10 条と第 6 条が指令 2019/790 の 4 条 3 項を直接引く | `ACD-1.4-DRAFT.txt` | **半分だけ正しい**。指令を名指すのは §1.10（*"contemplated by Article 4(3) of Directive (EU) 2019/790"*）だけで、§6 は指令を名指さず、§1.10 で定義した Reservation の語で受ける |
| 日本では著作権の完全な放棄（パブリックドメイン化）が認められない | `ACD-1.0.jurisdictions.md` §2 | **言い過ぎ**。§2 は「著作権法は放棄の手続を定めておらず、放棄の可否は条文上明らかではない」と書く —— 認められないとは言えない。人格権の放棄については、59 条の一身専属から認められないとするのが一般的な理解、という §2 の書き方と合う |
| 日本の法制ゆえに、ACD-1.4 は許諾（§4）と不行使の約束（§5・§12.2）を重ねる | `QUESTIONS-FOR-COUNSEL.md` 問い 1・問い 3 | **理由の帰属が狭い**。§3・§4・§5 の 3 つの足場は法域を問わず放棄が効くかに依らない形（CC0 の形・§2.4）で、日本だけが理由ではない。§12.2 の約束の形が日本の実務（59 条の下の不行使特約）に倣うことは問い 3 の *Meant to do* に在る |
| 英国の CDPA 1988 がデータベース権を定める | `rounds/2026-11-19-uk-database-regulations-1997-cdpa-29a-snapshot.txt`（30 が取得） | **違う**。英国の独自のデータベース権は Copyright and Rights in Databases Regulations 1997 の 13 条 1 項 *"A property right ("database right") subsists, in accordance with this Part, in a database if there has been a substantial"* *"investment in obtaining, verifying or presenting the contents of the database."* に在る。CDPA に在るのは著作物の側と TDM の例外（29A 条）。§7 が独自の権利と著作権を分けて扱う前提とは合う |
| 著作権法 30 条の 4 が情報解析（AI の学習）に、18〜20 条・59 条が人格権に関係する | `ACD-1.0.jurisdictions.md` §2a・§2b | **合う**（§2a が 30 条の 4 とその但書を、§2b が 59・60 条を原典で読んでいる） |
| 独自のデータベース権は主に EU と英国に特有 | 指令 96/9/EC（2f が取得） | **合う**（§7 の手当ての前提と同じ） |

**この照合が establish しないこと**: まとめの全体の当否ではなく、ACD と法についての記述を 1.4 草案と手元の写しに当てた結果だけを書いた。取得先の一覧（EUR-Lex・e-Gov・U.S. Code・legislation.gov.uk・WIPO Lex）はそのまま分担に使った。

---

**Lost?** [`QUESTION-INDEX.md`](QUESTION-INDEX.md) indexes every worked entry in this directory by
the question it answers. [`ACD-1.0.jurisdictions.md`](ACD-1.0.jurisdictions.md) is the jurisdiction-by-jurisdiction reading this file was split from.

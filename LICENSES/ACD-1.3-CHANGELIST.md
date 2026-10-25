---
file: LICENSES/ACD-1.3-CHANGELIST.md
audience: OSI license-discuss / license-review participants, licence reviewers, a future drafter
last-updated: 2026-10-24
canonical-ref: LICENSES/ACD-1.3.txt (確定テキスト・凍結・2026-10-25) / LICENSES/ACD-1.2.txt (直前の確定テキスト・凍結) / LICENSES/ACD-1.2-CHANGELIST.md (1.1 → 1.2 の記録) / LICENSES/ACD-1.0.errata.md
---

# ACD-1.3 で変えるもの

ACD-1.2 は 2026-10-17 に確定・凍結し、**改善はここから先で行う。** 草案 `ACD-1.3-DRAFT.txt` は、**下の表の変更と版番号・識別子を除いて 1.2 の本文である**（2026-10-24 に最初の変更を入れた。それまでは 1.2 と同一で、冒頭の変更一覧は空だった）。変更を入れたら、草案冒頭の一覧とこの表の両方に足す。

**2026-10-24 から、条文の中身の選択も AI が決めている** —— オーナー明言「委任していますし、OSI通過の為の何かで私の裁可が必要なものは無いよ」。以下の「採った / 採らなかった」はすべて AI の判断で、理由と逆側を同じ行に書く（判断を後から検証できるようにするため）。

## 表（変更が入ったらここへ足す）

| 対象 | 何を変えるか | なぜ | 費用（語） | 状態 |
| :-- | :-- | :-- | :-- | :-- |
| 題名行（条文ではない） | *"Version 1.2"* → *"Version 1.3"* | **草案は 1.2 を複製して作られ、識別子と §16 の名前だけが 1.3 に置き換わり、題名の版数が取り残されていた**（10-17〜10-24 の 7 日間）。冒頭は「版数と識別子を除いて 1.2 と同一」と述べていたので、**版数そのものが変わっていない状態は、その宣言から見ても誤り**だった。**Check 468 は語数・条数・参照・ASCII を測るが、題名の版数を見る face が無かった** → **468j を新設**（題名行と `Short identifier:` が file 名の版と一致すること）| 0 | 反映済み |
| §1.4（Dedicator の定義） | *"Covered Rights"* → *"Covered Rights, Moral Rights, or patent claims"* | errata **E35**。§8 と §12 は Covered Rights の外の権利を Dedicator に扱わせ、§16.3 は「権利を持つ者は誰でも」と招き、§2.6 は寄稿者を Dedicator にする —— **特許だけ・人格権だけを持つ者は Dedicator である範囲がゼロ**になっていた | +5 | 反映済み |
| §6.5 | *"Sections 3 to 5"* → *"Sections 3 to 5 and 8"* | errata **E36**。§6 は特許の請求項にも触れるが、§3〜§5 は特許に届かない（§1.5）。**§8.4 自身の説明と食い違っていた** | +2 | 反映済み |
| §9.2 | *"adds nothing to Your existing freedom"* に *"as to that right"* | errata **E37**。全体についての言明と読むと、著作権が生じない機械生成コードに §8 の特許許諾と §5.2 の約束が働くことと矛盾し、§9.3 とも当たる | +4 | 反映済み |
| §15.5 | *"\"including\" introduces examples and does not limit what precedes it"* → 1.0 §15.2 と逐語の *"\"including\" and \"in particular\" introduce examples and do not limit what precedes them"* | errata **E24** の追記。1.2 の復元は 2 語のうち 1 語を落としていた（本文は *"In particular"* を §4.3 と §10.2 で使う）| +3 | 反映済み |
| §16.2 | *"by a reference to this Dedication by name"* → *"by name and version"* | errata **E38**。**版を持たない名前への参照を、1.0 以降のすべての版が「自分の条件の十分な通知」と主張していた。** 版が 2 つ以上ある今、その参照はどの版にも全面的に主張され、選ぶ規則がどこにも無い | +2 | 反映済み |

**語数: 5,427 → 5,443（+16）。** すべて正確さのための費用で、B3（長さ）に対しては逆向きに働く。**相殺する削除はこの増分ではしない** —— 1.1 の圧縮が依拠されていた規則を 3 つ落とした記録（E24 / E25 / E34）があり、削る判断は「その語に依拠する文書を全部確かめてから」でないと同じ失敗を繰り返すからである。B3 への手当ては別の増分で、削る候補ごとに依拠先を測ってから行う。

## errata 由来（`ACD-1.0.errata.md` が一次記録）

| Errata | 対象 | 1.3 での扱い（要約は errata 側が権威）| 状態 |
|---|---|---|---|
| E24 | §15.5 | 1.2 の復元が *"in particular"* を落としていた。1.0 §15.2 と逐語一致へ（+3 語）| **反映済み**（2026-10-24）|
| E35 | §1.4 | Dedicator の範囲を Covered Rights から、§8 と §12 が実際に扱う権利まで広げた（+5 語）| **反映済み**（2026-10-24）|
| E36 | §6.5 | §6 が言い直しているのは §3〜§5 **と §8** である（+2 語）| **反映済み**（2026-10-24）|
| E37 | §9.2 | 「何も足さない」を、生じていない権利についての言明に限った（+4 語）| **反映済み**（2026-10-24）|
| E38 | §16.2 | 名前による参照は、版を伴うときだけ十分な通知になる（+2 語）。GPL-3.0 §14 型の「どの版でも選べる」は採らなかった（後の版が前の Dedicator の与えたものを決めてしまう・約 30 語）| **反映済み**（2026-10-24）|

## 1.2 の凍結前検証から持ち越したもの（2026-10-17・まだ草案に入れていない）

1.2 の確定前に、6 観点の敵対的検証で指摘されたが、凍結を止めるほどではないと判定したもの。**欠陥と決まったものではなく、1.3 で読み直す候補**である。

| 対象 | 指摘 | 判定 |
| :-- | :-- | :-- |
| §6.5 | 「§6 は §3〜§5 を言い直しているだけ」と述べるが、§6.1 は §3〜§5 が届かない特許の請求項にも触れている | **欠陥と判定（E36）・反映済み**（2026-10-24）。§8.4 が「§6.4 だけでは特許について露出する」と自分で述べており、§6.5 と本文の中で食い違っていた |
| §1.4（Dedicator の定義） | 定義が Covered Rights の保有者に限られる一方、§8（特許）と §12（人格権）は Covered Rights の外の権利を Dedicator に扱わせる | **欠陥と判定（E35）・反映済み**（2026-10-24）。決め手は §16.3（「権利を持つ者は誰でも適用してよい」）と §2.6（寄稿者を Dedicator にする）で、**特許だけ・人格権だけを持つ者が実在の類型として現れる** |
| §16.2 | 版のない名称（"Autonomous Commons Dedication"）だけで参照された場合に「these terms」が全面適用されると読める | **欠陥と判定（E38）・反映済み**（2026-10-24）。1.0 の時点では版が 1 つなので害が無く、**1.1 確定（2026-09-17）の日から**どの版も同じ参照を主張する状態になった |
| §15.5 | 1.0 の §15.2 にあった "in particular" の規則が戻っていない、という指摘 | **指摘が正しかった（E24 の追記）・反映済み**（2026-10-24）。1.2 の §15.5 は規則の「数」は 3 つだが、2 つ目の規則が 2 語のうち 1 語しか持っていなかった。**「3 つ戻した」は数としては真で、中身としては不完全だった** |
| 草案ヘッダの E22 の項目 | §2.6 を「削除」とだけ述べ、残した 1 文に触れていない | **欠陥ではない**（1.2 の付録のヘッダは *"The half worth keeping is kept"* と述べている）。記録上の区別: **E22 で落としたのは「契約書の要求を禁じる文」、残したのは「この Dedication の下では追加の書面が要らない」という事実の文**である |

## 当てて clean だったもの（2026-10-24・再掘削を防ぐために書き残す）

| 当てた角度 | 結果 |
| :-- | :-- |
| **§5.1 第 2 肢（1.2 で追加）が商標の請求まで不行使にしていないか** —— 第 2 肢は *"any claim or cause of action … relating to a use of the Work that this Dedication permits"* で、§11.4 は「§5 の約束はこの文に縛られない」と述べ、§15.1 は広い読みを採らせる。§11.1 は商標を付与しないと述べるだけで、行使しないとは述べていない | **clean。** 商標の請求の芯は出所・提携・後援についての誤認であり、**それは §11.3 が「この Dedication の届く外」と述べる行為そのもの**である。§11.4 の除外は §11.4 の 1 文に限られ、§11.3 には及ばない。そして §11.3 の行為は「この Dedication が許した使い方」ではないので、第 2 肢の要件にそもそも当たらない。**残るのは誤認を伴わない請求（希釈化など）だけで、実務上の面は小さい。** ⚠ **逆側**: この結論は 3 条（§5.1 / §11.3 / §11.4）を組み合わせて初めて出るので、**条文の読み手に 3 条を読ませている**こと自体が明晰さ（承認基準 4）の費用である。語を足して明示する案（§5.1 に *"Section 11.3 is unaffected"*・+4 語）は、**同じ形の明示が §11.3 と §11.4 に既に在る**ので見送った |
| **長すぎる文**（承認基準 4）| **clean。** 1.3 草案の本文 163 文の中央値は 27 語。最長は §5.2 の 129 語だが (a)〜(d) の列挙で、列挙を持つライセンスでは普通の形。次が §8.1 の 80 語（特許許諾の 1 文。Apache-2.0 §3 の特許許諾も 1 文）。分割すると E27 型の「修飾語が別のものに付く」読みを新しく作る危険の方が大きい |
| **定義語の小文字での使用** | **clean。** 小文字で現れるのは一般名詞としての *"a work"* / *"machine-generated material"*（preamble）/ *"a reservation of the kind contemplated by"*（§1.10 の定義の中）だけで、定義語を指すべき箇所で小文字になっているものは 0 |
| **本文中の相互参照の意味**（指す先の条が、参照している文の言うことを実際に述べているか）| **clean。** 1.2 で足された参照（§2.6 → §6.5 / §5.2(b) → §10.1 / §8.6 → §12.2 / §11.4 → §2.7・§13.2 / §12.6 → §15.2 / §4.6 → §1.6・§2.3・§5.3）を含め全件を手で当てた。**ただし E36 は「参照先」ではなく「参照元が自分の構造を述べる文」の誤りで、この掃引の形では見つからない** —— 見つけたのは 1.2 凍結前の検証である |

## 確定（2026-10-25）

**1.3 は 2026-10-25 に確定・凍結し、このリポジトリに適用した**（オーナーの依頼「1.3に大きな不備が無く、リポジトリに適用可能な状態なら適用してください」）。確定の判断（AI・`OSI-APPROVAL-PLAN.md` §4 段 7 の条件）: 1.2 凍結前の 6 観点のうち、相互参照・1.2 との差分と変更一覧の一致・変えた条の起草は 2026-10-24 に当て済みで凍結を止める欠陥は出ていない。OSD への当たりは条件を足していないので 1.2 から動かない。機械可読性は記述子 `ACD-1.3.machine.json` を作って E10 を閉じた。errata の状態の主張は Check 464 / 468e / 468i / 469(b) が照合する。**⚠ 2026-10-24〜25 に回した多観点の模擬審査（workflow）は利用上限で 3 回とも結果ゼロで終わっており、確定はそれを含んでいない。**

**確定版の冒頭は、適用状態を述べない形にした** —— 凍結済みの 1.2 の冒頭は「このリポジトリを覆うのはまだ ACD-1.0」と述べており、1.3 の適用でその文は偽になったが直せない。**凍結テキストには変わりうる事実を書かない**（1.3 の冒頭は「どの版を適用するかは各プロジェクトの notice が述べる」とだけ書く）。

次版の作業場は `ACD-1.4-DRAFT.txt`。`ACD-1.3-DRAFT.txt` は凍結済みの 1.2 が名指す file 名なので、案内として残した。

## 付録: 確定時点の草案ヘッダ（逐語）

確定版の冒頭は身分の表示だけにしたので、草案が冒頭に持っていた変更一覧を、確定の直前の状態のまま残す（**記録を消さないため**）。

```text
ACD-1.3 -- DRAFT. NOT IN FORCE. NOT SUBMITTED. NOT APPLIED TO THIS REPOSITORY.

  This file is the successor text under construction. The latest frozen text
  is ACD-1.2 (LICENSES/ACD-1.2.txt), and the licence that covers this
  repository is ACD-1.0. ACD-1.0, ACD-1.1 and ACD-1.2 are pinned by SHA-256 in
  LICENSES/FROZEN.md and verified in CI; nothing here changes any of them.

  Status of this draft, stated plainly so that nobody has to infer it:

    * It has had no legal review, like 1.0, 1.1 and 1.2.
    * It has not been posted to any list.
    * Apart from the changes listed below, and the version number and the
      identifiers that name it, the operative text is ACD-1.2's. An empty
      change list below would mean nothing had been changed yet -- not that
      the record is missing; a list with entries in it is the whole of the
      difference.
    * Clause numbers follow ACD-1.2 (which follows ACD-1.1), not ACD-1.0.
      Citations to an earlier version must keep using that version's text.
    * Changes will be recorded in LICENSES/ACD-1.3-CHANGELIST.md, and defects
      this draft introduces itself in LICENSES/ACD-1.1-SELF-AUDIT.md, which is
      a register of our own sweeps rather than of any one version.

  Changes in this draft, relative to ACD-1.2:

    * The title line now says "Version 1.3". Until 2026-10-24 it still said
      "Version 1.2" two lines above the identifier ACD-1.3, so the draft
      contradicted itself before its first clause.
    * Section 1.4 now counts as a Dedicator a person who holds Moral Rights
      or patent claims in the Work, not only one who holds Covered Rights
      (errata E35). Sections 8 and 12 have the Dedicator grant and waive
      rights that Covered Rights exclude, and Section 16.3 invites anyone who
      holds rights in a work to apply this Dedication; but a person holding
      only a patent claim, or only Moral Rights -- a contributor whose
      employer owns the copyright, for instance -- was a Dedicator to no
      extent, so the grants Sections 8 and 12 exist to make could not be made
      by that person. (+5 words.)
    * Section 6.5 now says that Section 6 states what Sections 3 to 5 and 8
      would in any event permit (errata E36). Section 6 speaks of patent
      claims as well as Covered Rights, and Covered Rights exclude patents
      (Section 1.5), so Sections 3 to 5 alone do not permit what Section 6.1
      permits as to patents; Section 8.4 does. The old sentence contradicted
      Section 8.4's own account of why Section 8.4 is needed. (+2 words.)
    * Section 9.2 now says that where a right does not subsist this
      Dedication adds nothing to Your existing freedom "as to that right"
      (errata E37). Without those words the sentence reads as saying that the
      Dedication then adds nothing at all, which is false wherever Section
      5.2 or Section 8 still operates -- a patent licence over code in which
      no copyright subsists, for instance -- and which would sit against
      Section 9.3. (+4 words.)
    * Section 15.5 restores "in particular" to the rule that "including"
      introduces examples, so that the clause is now ACD-1.0's Section 15.2
      word for word (errata E24). ACD-1.2 restored that rule with one of its
      two words, while its text uses "In particular" twice (Sections 4.3 and
      10.2). (+3 words.)
    * Section 16.2 now treats a reference by name as sufficient notice only if
      it also gives the version (errata E38). Every version since 1.0 says
      that a reference "by name" is sufficient notice of its own terms; once
      more than one version exists, a reference by name alone is claimed by
      each of them in full, and nothing in any of them chooses between them.
      (+2 words.)
    * ACD-1.2: 5427 words, 80 clauses. This draft: 5443 words, 80 clauses.

  Still open in this draft: E6 (whether Section 8.4 needs to reach outputs as
      well as the use of the Work -- examined and deliberately not narrowed)
      and E10 (the machine-readable descriptor; closed for 1.1 and
      1.2 in their descriptors, and it must be closed again for each new
      version because each version carries its own descriptor).
```

## Constraints

- 1.0 / 1.1 / 1.2 は凍結中（`FROZEN.md`・Check 453）。直すのは `ACD-1.3-DRAFT.txt` だけ。
- 確定するときは `ACD-1.1-CHANGELIST.md` §0.13 の手順に従い、改名を一括置換しない。

## Change impact

- `ACD-1.3-DRAFT.txt` の冒頭の一覧とこの表は、同じ commit で揃える（Check 468f / 468i）。

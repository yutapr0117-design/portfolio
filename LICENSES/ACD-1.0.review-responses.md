---
file: LICENSES/ACD-1.0.review-responses.md
audience: ai, human (提出者), 監査人, 第三者全般
last-updated: 2026-08-26
canonical-ref: LICENSES/ACD-1.0.txt (凍結中の本文) / LICENSES/ACD-1.0.submission.md (提出パケット) / LICENSES/READY-TO-SUBMIT.md (提出判断) / LICENSES/FROZEN.md (凍結宣言) / docs/architecture/acd-license-rationale.md (設計根拠)
---

# ACD-1.0 — OSI 想定問答ドシエ

```
Status        : OSI `license-discuss` (一般的な議論リスト) へ投稿済み・結果待ち
                ※ **承認申請の窓口は `license-review`** で、そこへはまだ出していない。
                   SPDX License List にも出していない = 承認の手続きは未着手
本文の状態    : 凍結中 (LICENSES/FROZEN.md の存在が凍結を意味し Check 453 が sha256 で強制)
本書の位置づけ : 非規範。ライセンス本文の一部ではない。回答の下書きであって、
                ここに書いたことが ACD-1.0 の意味を変えることはない
```

## 0. この文書の使い方

**まず venue を区別する。** `license-discuss` は OSI の**一般的な議論リスト**（今回の投稿先）、`license-review` は**承認申請の窓口**（未投稿）。どちらも公開のメーリングリストで、**読者が本気で読んで穴を突く場**という性質は同じ —— だから本ドシエは両方に使える。ただし `license-discuss` では「承認してくれ」ではなく「**この instrument は要るのか**」を問う姿勢が正しい。したがって必要なのは *弁明* ではなく **「その指摘は正しい / 正しくない、根拠はこれ」を短く返せる準備**である。

本書は次の形で並べてある。

- **想定される指摘**（日本語・一行）
- **そのまま貼れる英文の回答**（引用ブロック）
- **なぜこう答えるか**（日本語・回答の裏にある判断）

英文をそのまま貼れる形にしてあるのは、リストの言語が英語だからであって、翻訳の手間を惜しむためではない。**回答は必ず読んでから貼ること。** 議論の流れによっては「答えない」「認める」ほうが正しい場面がある（§5 参照）。

### 3 つの原則

1. **認めるべき指摘は即座に認める。** この種のリストで最も心証を損なうのは、弱点を指摘されたときに言い繕うことである。本ドシエには「認める」と書いた項目が実際にある（§4）。
2. **本文は凍結中なので、その場で直さない。** 妥当な指摘を受けたときの正しい返答は「その指摘は正しい。ACD-1.1 でこう直す」であり、審査中に差し替えることではない。審査側が見ているテキストと公開されているテキストが食い違うのが最悪である。
3. **保証しない。** 「承認されるはずだ」と述べない。求めているのはレビュー結果であって同意ではない。

---

## 1. 前提の確認 —— この提出が何であって何でないか

| | 実態 |
|---|---|
| 出したもの | OSI **`license-discuss`** への投稿（一般的な議論リスト・意見を聞くこと） |
| 出していないもの | **`license-review`（承認申請の窓口）** / SPDX License List への収録申請。**承認の手続きはまだ何も始めていない** |
| SPDX を見送った理由 | SPDX は「相当程度の実使用」を求める。現在の使用実績は本リポジトリ 1 件で、その条件を満たしていない。**満たしていないものを出さない**のが誠実である |
| いま欲しいもの | 起草では解消できない論点（dedication 型の是非・§12 の各国法での効き方・§8.4 の射程）について、**第三者の目による判断** |

**この区別は最初の投稿で明示したほうがよい。** 「approval を求めているのか discussion を求めているのか」はリストで頻繁に確認される点であり、先に述べておくと以後のやり取りが噛み合う。

> **English (use in the opening message if not already stated):**
>
> To be clear about what I am asking for: I am seeking discussion and criticism.
> I have posted here on license-discuss rather than submitting to license-review,
> because I would rather find out whether this instrument should exist at all
> before asking anyone to approve it. I have deliberately not submitted this to the SPDX
> License List, because SPDX asks for substantial real-world use and this text
> currently has exactly one user — my own project. I would rather be told that
> the instrument is unnecessary, or that a particular section does not work,
> than have it listed on the strength of nobody having read it closely.

---

## 2. 最重要の 3 問（ここで負けたら他は読まれない）

### Q1. なぜ新しいライセンスが要るのか（license proliferation）

> **English:**
>
> The short answer is that three properties I needed are not available together
> in any approved licence, and two of them are not available at all.
>
> 1. **An affirmative permission for machine learning and TDM, coupled with an
>    express statement that no reservation is made.** Several jurisdictions now
>    key TDM exceptions to whether the rightsholder has *reserved* the right
>    (the EU DSM Directive Article 4(3) opt-out, and the machine-readable
>    reservation protocols now being built on top of it). A permissive licence
>    grants copyright permissions but says nothing about reservation, so a
>    downstream system that checks for a reservation signal has to guess.
>    ACD-1.0 Section 6.2 states the absence of a reservation as a term of the
>    instrument itself.
> 2. **A patent grant in a public-domain-style instrument.** CC0 is the closest
>    existing instrument in form, and CC0 Section 4(a) expressly does *not*
>    grant patent rights. That exclusion was the centre of the 2012 discussion
>    on this list, and it is precisely the gap Section 8 fills.
> 3. **A workable position on machine-generated material.** Where authorship
>    itself is uncertain (and it is uncertain, differently, in the US, the EU,
>    the UK and Japan), a licence that presupposes a subsisting copyright leaves
>    the user to guess. Section 9 removes the question from the user's path
>    without asserting an answer to it.
>
> I would genuinely rather be shown an existing licence that does all three. If
> one exists, I will use it and withdraw this.

**なぜこう答えるか**: proliferation の指摘に対する唯一有効な返しは「**既存で埋まらない具体的な穴**を挙げること」であり、「私のプロジェクトに合うから」は答えにならない。そして最後の一文（既存で埋まるなら撤回する）は形式的な謙遜ではなく、**実際にそうすべき**である。撤回できると言える提出者は、そう言えない提出者より真剣に読まれる。

### Q2. CC0 は撤回された。なぜこれは違うのか

> **English:**
>
> CC0 was withdrawn from this list by Creative Commons in 2012. As I read the
> archive, the objection that mattered was not "dedications are bad" in the
> abstract but a concrete one: CC0 Section 4(a) states that no patent rights are
> waived, abandoned, surrendered, licensed or otherwise affected. An instrument
> that hands over copyright while expressly preserving patents can leave a user
> worse off than a permissive licence, because the user has no notice that the
> patent risk was carved out.
>
> ACD-1.0 takes the opposite position in Section 8: a patent licence is granted,
> on the same no-condition footing as everything else, and Section 8.3 says
> expressly that nothing in the instrument reserves or preserves any patent
> claim. Section 8.4 extends the grant to models, parameters and outputs,
> because Section 1.5 excludes patents from "Covered Rights" and I did not want
> the copyright-side permission for computational use in Section 6 to be
> undercut by a patent-side gap.
>
> If the committee's position is that the *form* is the problem regardless of
> the patent point, I would like to hear that stated, because it is decisive for
> whether this text should exist at all.

**なぜこう答えるか**: CC0 の件は**必ず**出る。ここで「CC0 とは違う」と抽象的に言うと相手にされない。**撤回の実際の争点（§4(a) の特許除外）を正確に述べ、自分の §8 がその一点への回答であること**を示すのが唯一の筋である。そして最後の一文で「形式自体が問題なら、それを言ってほしい」と**負けを引き受ける用意**を見せる。これは §7 の弱点 4「公有化型は歴史的に難しい」に対する正面からの姿勢である。

### Q3. 献呈（dedication）は「ライセンス」なのか。OSI が扱う対象か

> **English:**
>
> ACD-1.0 is deliberately built as three independent footings for the same
> outcome, not as a dedication with a licence bolted on:
>
> - Section 3 surrenders the rights, where surrender is possible.
> - Section 4 grants a licence, **independently** of Section 3 and without
>   waiting for Section 3 to fail (Section 4.4). It is not a fallback that has
>   to be triggered.
> - Section 5 is a covenant not to assert, which operates even if both of the
>   above are held ineffective somewhere.
>
> Section 2.4 states that Sections 3, 4, 5 and 6 are independent of one another.
> So whatever a given jurisdiction thinks of abandonment of copyright — and
> Germany and much of the civil-law world think very little of it — there is an
> operative licence grant on the page that a court can enforce on ordinary
> licence principles.
>
> If the committee's view is that OSI should evaluate only the Section 4 licence
> and disregard Sections 3 and 5, that is a reading the text can bear, and I
> would accept it.

**なぜこう答えるか**: 「dedication は各国法で効かないことがある」は**正しい指摘**であり、否定してはならない。答えは「効かない場合に備えて**独立の**ライセンス条項が同じページにある」であり、これは実際にそう起草されている（§2.4 / §4.4）。最後の譲歩（§4 だけ見てくれてよい）は、審査の焦点を**確実に評価可能な部分**へ寄せる実利がある。

---

## 3. Open Source Definition 逐条

OSD への適合は提出者が**自分から**述べるべきものである。以下は 10 条それぞれについて、根拠条項を指した形。

> **English (paste as a block if asked for an OSD walkthrough):**
>
> **1. Free redistribution.** The licence in Section 4.1 is worldwide,
> royalty-free, non-exclusive and irrevocable, and Section 4.3 attaches no
> condition to it. Section 4.5 states the consequence for redistribution: You may
> distribute the Work, and any adaptation or collection containing it, **under
> any terms You choose**, including terms incompatible with these, and nothing
> requires those terms to reproduce this text. Selling is therefore permitted and
> no royalty is payable to the Dedicator.
>
> **2. Source code.** The instrument imposes no obligation of any kind
> (Section 10.1) and in particular does not require source to be made available
> (Section 10.2) — but neither does it restrict it. Applied to software, the
> Work as distributed by the Dedicator is the source. Nothing in the text
> permits distribution in obfuscated form only, because nothing in the text
> conditions anything.
>
> **3. Derived works.** Section 4.2 includes the rights to reproduce, adapt,
> modify and distribute; Section 4.3 attaches no condition, so derivatives may
> be distributed under any terms the distributor chooses.
>
> **4. Integrity of the author's source code.** No requirement to mark changes
> is imposed (Section 10.2). This criterion permits, but does not require, such
> a term.
>
> **5. No discrimination against persons or groups.** "You" is defined in
> Section 1.4 as any person or entity exercising permissions; no class is
> excluded anywhere in the text.
>
> **6. No discrimination against fields of endeavour.** Section 4.1 is granted
> for any purpose; Section 6.1 states expressly that computational use is
> permitted for any purpose. There is no non-commercial, non-military,
> ethical-use or AI-related carve-out. **The AI provisions of Section 6 are
> permissions, not restrictions** — this is the point I most expect to be
> misread, given that most licences mentioning AI in the last three years have
> been restrictive ones.
>
> **7. Distribution of licence.** Section 2.3: the Dedication takes effect
> without any act of acceptance; Section 16.2: an SPDX identifier or a reference
> by name is sufficient notice. Rights attach to the recipient without any
> further instrument.
>
> **8. Licence must not be specific to a product.** The text speaks only of
> "the Work", "the Dedicator" and "You". Section 16.3 states that it may be
> applied by anyone, to any work. My own project's application of it is a
> separate file (`LICENSE`), not part of the text. This separation is enforced
> mechanically in my repository, so that the text cannot acquire
> project-specific content by accident.
>
> **9. Licence must not restrict other software.** Section 4.5 expressly covers
> "any adaptation or collection containing" the Work and disclaims any obligation
> on You in respect of Your recipients. No term reaches other software distributed
> alongside it, and Section 4.6 confirms that terms You add govern only what You
> give.
>
> **10. Licence must be technology-neutral.** No term depends on a technology,
> interface or medium. Section 2.3 requires no click-through or other act of
> assent.

**なぜこう答えるか**: OSD 6 が最大の誤読ポイントである。近年この種のリストに来る「AI を扱うライセンス」の大半は**制限**（学習禁止・用途制限）であり、レビュアはその前提で読み始める。**「§6 は許諾であって制限ではない」を OSD 6 の項で先に言う**のが最も効く。OSD 8 については「本文とプロジェクトへの適用宣言が別ファイルであり、それが機械強制されている」という事実が強い（Check 441 の「プロジェクト固有要素ゼロ」）。

---

## 4. 認める項目（先に自分から述べる）

**この節は防御ではない。** 指摘される前に自分から出すべき弱点である。提出パケットの "Honest disclosures" と整合させること。

### A1. 法的レビューを受けていない

> **English:**
>
> No lawyer has reviewed this text. I say that first because it changes how the
> rest should be read. **The text was drafted by an AI agent operating autonomously in
> this project — I did not write it, I did not direct the drafting, and I did not ask
> for it** (see the provenance disclosure; I learned the licence existed after the agent
> had written it; the suggestion to submit it for review also came from an AI, not from
> me). **I do not review the repository** — what reaches me is a summary, not the files —
> **but the licence is the exception: I read it in full and understood it before sending.**
> I am the Dedicator and the steward: I decided to keep it, it is applied to my work, I read
> it, I acted on that advice, and I answer for it. It was checked mechanically against the published criteria
> rather than against professional judgement. Section 12
> (moral rights) is the place where that matters most, because it turns on
> Japanese law — Article 59 of the Japanese Copyright Act makes moral rights
> personal to the author and inalienable — and on how a court would treat a
> covenant not to exercise them. I would value a correction there more than
> anywhere else in the document.

**なぜここで起草の出自に触れるか**: A1 は「先に自分から述べる」節であり、**同じ節の中で
起草主体を曖昧にしたら意味が無い**。詳細は `ACD-1.0.review-responses-meta.md` Q10。

**是正の経緯（隠さず残す）**: 初版は「The drafting is my own」と書いており、**Q10 と正面から
食い違っていた**。横断監査で見つけて「under my direction（私の指示で）」へ直したが、
**それも実態を弱めていた** —— 実際には**人間は起草に関与していない**。二度目の是正で
「**AI が自律的に起草し、人間は書いても逐条で指示してもいない**」という事実へ揃えた。
**弱める方向の言い換えも矛盾である。** 三度目でさらに踏み込んだ —— **「ライセンスを作る」という判断自体、人間は出していない**（AI が必要と判断して設計・起草し、人間は存在を後から知った）。**事実を弱めるほうへ丸めない。** 四度目でさらに判明した —— **「独自ライセンスとして申請せよ」という提案も別の AI から出ており、人間発ではない**。**是正のたびに人間の関与が減った**というこの経過自体が、**私の下書きが実態より人間の主体性を高く見積もる方向へ寄っていた**ことの記録である。五度目では**人間がリポジトリを見ていない**ことが判明し、**六度目でそれはライセンス以外の話**であり **メール送付時には全文を読んで理解している**と訂正された —— **今度は私が逆方向へ行き過ぎた**。**5 回は過大に、6 回目は過小に書いた**のだから、教訓は「一方向に偏る」ではなく、より単純に —— **人間が何をしたかを、確かめずに書いていた**。書けるのは **(a) 本人が述べたこと / (b) リポジトリに証跡があること**の 2 つだけで、どちらでもないなら**その文は書かない**（「した」とも「していない」とも書かない）。

### A2. 実使用が 1 件しかない

> **English:**
>
> One project uses this: mine. I have not sought adopters, and I would rather
> say that plainly than present a single repository as an ecosystem. This is
> also why I have not gone to SPDX, which asks for substantial use. If the
> committee's view is that a licence with one user should not be reviewed at
> all until that changes, that is a reasonable position and I will accept it.

### A3. 長い

> **English:**
>
> At roughly 600 lines this is long for what it does, and length is a real cost:
> it is read less carefully, and every extra sentence is a place for an
> inconsistency to hide. My reason for the length is that most of it is not
> operative text but *stated reasoning* — Sections 8.3, 9.4, 11.4 and 12.4 each
> explain why they exist, because the failure mode I was drafting against is a
> future reader (including an automated one) drawing the wrong inference from
> silence. I accept that this is a trade-off and that reasonable people weigh it
> the other way. If the committee prefers a text with the explanations stripped
> to a companion document, that is a straightforward change for a 1.1.

### A4. §6 は copyright ライセンスとして冗長ではないか

> **English:**
>
> Partly, yes, and Section 6.5 says so on its face: it states expressly what
> Sections 3 to 5 would in any event achieve. I kept it for two reasons that I
> think survive the redundancy objection, but I acknowledge it is a judgement
> call.
>
> First, the EU DSM Article 4(3) opt-out is not a copyright permission question
> but a *reservation* question, and silence is doing work there that a grant
> does not do. Second, the readers I care most about are automated, and a
> statement that has to be inferred from the absence of a restriction is
> materially harder to act on than one that is present as text.

**なぜこの 4 つを先に出すか**: この種のリストでは、提出者が弱点を隠していると判明した時点で議論が「テキストの是非」から「提出者の信頼性」に移り、そうなると回復しない。A1〜A4 はいずれも**調べれば分かる**（法的レビューの有無は書いてある、使用実績は GitHub を見れば分かる、行数は数えれば分かる）。**自分から言えば誠実さの証拠になり、言われてから認めれば失点になる**、というだけの違いである。

---

## 4.5 逐条リファレンス（全 82 条）→ 分冊

「この条項は何のためにあるのか」に **全 82 条について**答えるのが
**`LICENSES/ACD-1.0.clause-reference.md`** である。想定問答が「**来るであろう指摘**」に
答えるのに対し、こちらは「**この条項は何か**」に答える —— レビューで条番号を引用された
とき、採用を検討する人が疑問を持ったとき、監査で照合するときは、まずそこを引く。

**完全性は構造的に保たれている**: 本文から条項番号を機械抽出して照合しており、82 条と
記述が 1 対 1 でなければ生成そのものが失敗する。「1 条だけ書き忘れる」ことが起きない。

逆引き表（「帰属表示は要るのか」「GPL に取り込めるか」「公有化が認められない国では」など）
も同ファイルの付録 A にある。

## 4.6 ライセンス族ごとの比較 → 分冊

「**X で足りるのでは**」への答えは、**相手がどの族を念頭に置いているかで変わる**。同じ答えを
繰り返すと噛み合わないので、**`LICENSES/ACD-1.0.comparison.md`** に族ごとの答えを置いた
（copyleft 系 / **AI 用途制限系** / source-available 系 / データ系）。無条件系との 6 列比較と
0BSD・Apache-2.0 の逐条差分は `docs/architecture/acd-license-rationale.md` §2 にある。

とくに **AI 用途制限系（RAIL / OpenRAIL / Llama 等）との混同**は放置できない —— あちらは
**制限**、こちらは**許諾**で方向が逆であり、表面の類似が反転を隠す。

同ファイル §6 には**読み手が自分で当てはめられる 3 つの判断基準**があり、条件が合うなら
**0BSD を薦める**と書いてある（これが proliferation 指摘への最も強い姿勢である）。

## 4.7 法域別「どこが問いになるか」→ 分冊

「**あなたの国では効かないのでは**」は公有化型に**必ず**向けられる。**`LICENSES/ACD-1.0.jurisdictions.md`**
に、法域ごとの「問い / 本文の手当て（条番号）/ **確立していないこと**」を置いた
（共通構造 + 日本・ドイツ・フランス・米国・EU・英国）。

**この文書は結論を書いていない。** 有効なのは法理を語ることではなく「その問いは認識していて、
本文のここで手当てしてある」と条番号で示すことであり、**手当てがあることと有効であることは別**
だからである。助言を得ていない領域で断定するのは、meta 分冊 Q10 が警告する
「confidently invented doctrine」の実演にほかならない。

## 4.8 使う側の実務 FAQ → 分冊

想定問答・逐条・族比較・法域はいずれも**審査を受ける側の視点**で書かれている。だが
「疑問が全てリポジトリを見たら潰せる」には**使う側の実務**が要る ——
**`LICENSES/ACD-1.0.faq.md`**（使う側 25 問 / プロセス 5 問 / **リポジトリ逆引き表**）。

とくに **SPDX 未登録ゆえの表記（`LicenseRef-ACD-1.0`）**と**依存スキャナが「未知」と言う場合の
扱い**は、他のどの文書にも答えが無かった実務問題である。

同ファイル §C の逆引き表が「**疑問 → 見る場所**」の入口であり、**そこに無い疑問が出たら
一覧の欠落**として追記する運用にしてある。

## 5. 条項別の想定問答 → 分冊

条項レベルの想定問答は **`LICENSES/ACD-1.0.review-responses-clauses.md`** にある
（§2 SCOPE / §6 ML・TDM / §8 PATENTS / §9 機械生成物 / §10・§11 非条件性 / §12 人格権 /
§15・§16 解釈と本文の地位、および §2.9 非 executory・§5.2 の誤読・§7 DB 権・§13/§14 の
定型条項までの第 2 層）。

## 6. 既存ライセンスとの差分（比較表を求められたとき）

> **English:**
>
> | | Patent grant | ML/TDM stated | Reservation disclaimed | Machine-generated material | Conditions |
> |---|---|---|---|---|---|
> | CC0-1.0 | **No** (Sec. 4(a) expressly excludes) | No | No | No | None |
> | Unlicense | Not addressed | No | No | No | None |
> | 0BSD / MIT-0 | Not addressed | No | No | No | None |
> | MIT / BSD-2 | Not addressed | No | No | No | Notice |
> | Apache-2.0 | Yes, limited to the Work and Derivative Works | No | No | No | Notice, NOTICE file, change marking |
> | ACD-1.0 | Yes, extended to models, parameters and outputs (Sec. 8.4) | Yes (Sec. 6.1) | Yes (Sec. 6.2) | Yes (Sec. 9) | **None** (Sec. 10.1) |
>
> The row that matters is the first: no approved instrument in the
> public-domain-dedication family grants patents, and no permissive licence with
> a patent grant is condition-free.

**なぜこの形か**: 比較表は**自分に不利な列を含めないと信用されない**。Apache-2.0 の「条件」列（NOTICE ほか）は Apache の弱点ではなく設計であり、そう扱うこと。ACD-1.0 の列で「None」と書ける代償が Q「特許報復条項がない」であることは §5 で認めてある。

---

## 7. 出そうで出ない質問への備え（短答で足りるもの）

| 想定される指摘 | 短答（英文で述べる要点） |
|---|---|
| GPL 互換か | Condition-free なので GPLv2/v3 いずれにも取り込める。ACD-1.0 の側から何も要求しないため互換性の問題が生じる余地がない |
| 誰が steward か | **Dedicator（適用者）本人**。テキストを書いたのは AI だが、適用し・提出し・責任を負うのは人間である。§16.4 により ACD-1.0 のテキストは不変で、改訂は 1.1 以降の別バージョンとして行う（`FROZEN.md` と CI がこれを機械強制している） |
| どのカテゴリでの承認を求めるか | カテゴリの割当は委員会の判断に委ねる。特定のカテゴリを主張しない |
| 機械可読記述子（JSON）の位置づけ | 非規範。本文が唯一の権威。記述子が本文と食い違えば本文が勝ち、CI（Check 451）が食い違いを BLOCKING で検出する |
| なぜ ASCII 限定か | 転記・メール・古いツールでの毀損を避けるため。CI（Check 441）が純 ASCII を強制する |
| 名称の由来 | Autonomous（本リポジトリの運用モデル）/ Commons（条件ゼロで共有領域に置く）/ Dedication（許諾ではなく献呈という法的形式）。2026-08-23 時点で SPDX License List・OSI 承認一覧のいずれにも同名・類似識別子が無いことを確認済み（`acd-license-rationale.md` §6） |
| 実装（コード）は誰が書いたか | 本リポジトリは AI が実装し人間が設計・監査する体制で運用している。ライセンス本文もその過程で起草された。**この事実を隠さない**（§9 の存在理由と直結する） |
| 撤回する用意はあるか | ある。Q1 の最後の一文がその表明である |

---

## 8. 議論の進め方（回答内容ではなく態度の話）

1. **聞かれたことに答える。** この種のリストで最も嫌われるのは、指摘に答えず別の長所を語ることである。
2. **一度に全部貼らない。** 本ドシエは長いが、リストに投げるのは**その回に問われた項目だけ**にする。全文投下は読まれない。
3. **「その指摘は正しい」を惜しまない。** §4 の 4 項目はいつでも認めてよい。認めても失うものが無いように書いてある。
4. **本文を審査中に直さない。** 妥当な指摘は「1.1 でこうする」と述べて記録する。直したくなったら `FROZEN.md` を消したくなるが、それは**審査側が見ているテキストとの乖離**を作る行為である（Check 453 が機械的に止める）。
5. **沈黙も返答である。** 数日で反応が無いのは普通で、催促しない。OSI の決定は初回投稿から概ね 60 日かかる。
6. **敵対的な読みに感謝する。** 本ドシエの想定問答の多くは、起草時に「敵対的承継人 / 被告側弁護士 / 翻訳者 / 機械」のレンズで自分に対して行った攻撃の再演であり、外部から同じことをしてもらえるのは得である。

---

## 9. レビューで指摘されたら 1.1 で直す候補（現時点の自己評価）

**これは「直す」という約束ではない。** 指摘を受けたときに即答できるよう、あらかじめ棚卸ししたもの。

| 箇所 | 直す方向 | いま直さない理由 |
|---|---|---|
| 全体の長さ | 説明部分を companion document へ分離し、本文を operative text だけにする | 凍結中。かつ「説明を本文に置く」判断自体がレビュー対象なので、結果を見てから動くべき |
| §6 の冗長性 | §6.5 を残して §6.1〜6.4 を圧縮 | 同上。EU DSM の opt-out 実務が今後どう固まるかで正解が変わる |
| §12 | 日本法の専門家確認を経て、covenant の文言を実務の定型に寄せる | 助言を得ていない段階で定型に寄せると、**根拠なく正しく見えるテキスト**になる |
| §8.4 | 「model, parameter set, weight, embedding, output」の列挙を定義語へ集約 | 列挙のほうが誤読されにくいと判断した。ただし可読性の指摘は妥当 |
| §2.8 / §12.4 | 承継人拘束を「notice + estoppel」の枠組みとして明示的に書き直す | 現行文の "to the fullest extent the law permits" でも同じ意味に読めるため、優先度は低い |

---

## 10. 起草の出自・名称・運用に関する指摘 → 分冊

テキストの**外側**（誰が書いたのか / 誰が維持するのか / そもそも何のためか）への想定問答は
**`LICENSES/ACD-1.0.review-responses-meta.md`** にある
（LLM 起草であることの扱い / AI 学習を許す倫理 / steward が個人 1 名 / CC0+Apache のデュアル /
名称の誤読 / §3 が無効な法域で実際に何が起きるか / SPDX の先出し / 誰を守るのか /
**撤回条件** / 最初の投稿の下書き）。

## 11. この文書自体について

- **非規範。** ここに書いた回答が ACD-1.0 の意味を変えることはない。本文が唯一の権威である。
- **凍結対象ではない。** `FROZEN.md` が凍結するのは `ACD-1.0.txt` / `ACD-1.0.spdx.xml` / `ACD-1.0.machine.json` の 3 件であり、本書は議論の進展に応じて更新してよい。**むしろ更新すべきである** —— 実際に指摘を受けたら、その指摘と回答をここに追記して次の担当が同じ検討を繰り返さないようにする。
- **回答の品質は実際のやり取りで検証される。** 本書の想定問答は**予測**であって、レビュアが実際に何を問うかは分からない。**予測が外れた項目は削らず、外れたと記録する**（当てにいって外したことも、次に読む者にとっては情報である）。

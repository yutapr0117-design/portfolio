---
file: LICENSES/ACD-1.2-CHANGELIST.md
audience: OSI license-discuss / license-review participants, licence reviewers, a future drafter
last-updated: 2026-10-18
canonical-ref: LICENSES/ACD-1.2.txt (2026-10-17 に確定した本文・凍結) / LICENSES/ACD-1.1.txt (議論に付した確定テキスト・凍結) / LICENSES/ACD-1.1-CHANGELIST.md (1.0 → 1.1 の記録) / LICENSES/ACD-1.0.errata.md
---

# ACD-1.2 で変えるもの

> **✅ 2026-10-17 に確定・凍結した。** 本文は `ACD-1.2.txt`（`FROZEN.md` が sha256 で pin）、記述子は `ACD-1.2.machine.json`、次版の作業場は `ACD-1.3-DRAFT.txt`（記録は `ACD-1.3-CHANGELIST.md`）。
> 確定の前に 6 観点の敵対的検証を回し、凍結前に直すべきものを直した（下の「確定前の最終点検」）。**草案の冒頭にあった変更一覧（編集用ヘッダ）は、この file の末尾に逐語で残す** ——確定版の冒頭は身分の表示だけにしたため（1.1 と同じ形）。

ACD-1.1 は 2026-09-17 に確定・凍結し、**改善はここから先で行う。** 変更は下の 2 つの表に在る
（条文の変更と、errata 由来の扱い）。*（2026-09-28 訂正: この冒頭は「この一覧は空である。空であることが現在の正しい状態」と
述べ続けていたが、表には 2026-09-22 以降変更が入っていた。一覧が伸びたあとも、それを説明する現在形の文だけが
更新されていなかった —— `rounds/README.md` が「空である」と述べ続けた #89 と同じ型。）*

## 入力は 3 系統ある

| 系統 | どこから来るか | 行き先 |
| :-- | :-- | :-- |
| **届いた議論** | `license-discuss` / `license-review` のアーカイブ、off-list の往復 | 受領文は `rounds/` へ**無改変保存** → `ACD-1.0.discussion-log.md` で分解 → 帰結を本表へ |
| **我々の掃引** | `ACD-1.1-SELF-AUDIT.md` のレンズを 1.2 草案へ当て直す | 1.0 にも在る欠陥なら `ACD-1.0.errata.md` の `E<n>`、草案だけなら SELF-AUDIT |
| **外から届いた測り方** | オーナー経由・他の AI・法域調査など | **欠陥ではなく*次元*として受け取る**（`BLIND-SPOTS.md`）|
| **🆕 我々宛でない議論**（2026-09-22 追加）| **リストが我々の主題そのものを作業している場** ——OpenMDW / ModelGo の審査など。**我々に当たる反論としてではなく、設計の作業として読む** | 採用候補として本節下部へ |

> **🔴 この 4 系統目が無かったことが、数字に出ている。** errata 30 件（2026-09-22 時点・現在の件数は `ACD-1.0.errata.md`）のうち
> **list の議論に由来するのは E11 の 1 件だけ**（しかも未回答の問い）。23 件が自己発見、6 件が外部レビュー。
> **原因は schema の側に在った** ——第 1 系統は「**届いた**議論」と定義されており、
> **我々宛でない議論には経路が無かった。** ドシエはそれらを常に
> **「この反論は我々に当たるか」**（防御）としてのみ読み、
> **「彼らが作業した結果から我々が採るものは何か」**とは一度も問うていない。
> **OSI が 2026 年に ML ライセンスの設計を実地で詰めている場が、我々の本文に何も入れていない。**
> 記録は `against.md` #205。

## 表（変更が入ったらここへ足す）

| 対象 | 何を変えるか | なぜ | 費用（語） | 状態 |
| :-- | :-- | :-- | :-- | :-- |
| **§6.1**（Computational Use）| *"commercial or non-commercial"* を *"whether or not commercial"* へ（許諾の範囲は不変）| **機械が ACD を「独占的ライセンスを含む」と報告していた** —— ScanCode 32.5.0 のルール `proprietary-license_544`（本文は "Non Commercial" の 2 語）が、1.0 / 1.1 / 1.2 草案の 3 版すべてでこの句に当たり、CLI と同じ集計（`detected_license_expression`）にも `proprietary-license` が載る。**対照**: 同じ句を持つ Unlicense は全文ルールで丸ごと一致するので出ず、SPDX 非 deprecated 708 本で出るのは ParaType の 1 本だけ（OSI 承認済み 0 本）。言い換え 4 案を写しで試し、3 案で消えた（ハイフンを取っただけの "noncommercial" では残る）。**§6.5 が「機械が判定できない許諾は許諾ではない」と述べている当の層で、本文が自分を誤って分類させていた。** 一次資料は `claude/osi-oct-fetch-raw` の `fetch/2026-10-17/scancode-run/`（MANIFEST 観測メモ 49〜54・61・62・64）。**⚠ 逆側**: 根は「ScanCode が ACD の全文ルールを持たない」ことにあり、文言を直しても断片照合は続く（`unknown` / `public-domain` 等）。**全文ルールの追加を ScanCode へ申請した**（2026-10-17・https://github.com/aboutcode-org/scancode-toolkit/issues/5368 ・対象は ACD-1.0、1.1 は参照として併記・採用 1 件であることと AI の関与を本文で開示）。**⚠ 2026-10-17 同日の追記 —— 最初の修正は、草案ファイル全体としては誤分類を外せていなかった。** 本文の句は直したが、冒頭の変更一覧に足した項目が旧い句とルール名（"Non Commercial"）と "proprietary licence" の語をそのまま引用しており、ScanCode はヘッダのその 4 行に `proprietary-license` を当て直した（**直した理由を書いた文が、直した欠陥を戻していた**）。変更一覧の項目を引き金の語を使わない文へ書き直し、**旧い語はこの CHANGELIST にだけ置く**（草案の側には「理由はここにある」とだけ書いた）。**同時に、ヘッダ 51〜53 行の比較の文（Unlicense / 0BSD / MIT の名前）も名前を出さない形へ書き換えた** —— 草案は `(unlicense AND bsd-zero)` とも判定されていた。比較の中身（3 本の短い寛容型ライセンスは列挙が 2・1・1 で、この本文は 12）は保ち、どの 3 本かは errata E24 に委ねた。**書き換え後の草案の検出結果は `unknown AND public-domain AND warranty-disclaimer AND unknown-license-reference AND unknown-spdx`**（`proprietary-license` と `unlicense` / `bsd-zero` は 0）。残る 5 つは ScanCode が ACD の全文ルールを持たないことによる断片照合で、ScanCode issue 5368 の申請が通れば消える種類のもの。**⚠ 1.0 / 1.1 の本文は凍結中なので直していない** —— 1.0 / 1.1 の `proprietary-license` は、全文ルールの追加（ScanCode issue 5368）でしか消えない | **+1** | **草案に反映済み**（2026-10-17・ヘッダの書き換えは同日の続く pull request）|
| **§8.2**（特許報復の不在）| **「意図の表明」を「理由」へ寄せる** —— *"its absence is deliberate"* を落とし、*"A retaliation provision operates as a condition on permission already given, and Section 10.1 admits no condition, so the absence follows from the structure of this Dedication rather than from a policy preference expressed here."* へ | **`against.md` #265 (b)** —— **Chestek 氏（委員・元委員長）が 2026-09-22 に、非対称を *"intentional"* と説明した steward へ *"Your response is quite troubling to me"* と応じた**（`review-doctrine.md` §1.123）。**向きは逆**（ACD が意図的に手放しているのは *licensor を守る*機構の方）だが、**「意図的である」は適合の問いへの答えにならない**という一般形はそのまま当たる。**理由の形なら、読み手は §10.1 を見て自分で確かめられる。** **⚠ 本文の効力は変わらない** —— 報復条項が無いことも、§10.1 が条件を許さないことも 1.0 から同じで、**変えたのは「なぜ無いか」の述べ方だけ**である | **+30**（5,335 → 5,365）—— **B3 に対する実費用。長さは正確さと直接競合する**（register B3） | **草案に反映済み**（2026-09-27）|
| **§5.1**（不行使の covenant）| **第 2 肢を足す** —— *"and further covenants not to assert against You any claim or cause of action, whether now known or unknown, arising from or relating to a use of the Work that this Dedication permits"* | **`against.md` #272** —— **CC0 §2 が明文で放棄する 5 要素のうち 4 つは ACD の全文に在るが、*associated claims and causes of action, whether now known or unknown* だけが無かった**（該当語は 1.0 も 1.2 草案も 0 件・実測）。**§1.5 が Covered Rights から特許・商標・人格権・データ保護を除くので、そこから外れる請求権（不当利得・不正競争・冒用など）には §5.1 が届かない** ——**放棄の射程が「権利」で切られており「請求」で切られていなかった。** 試験を言葉にしたのは委員会側である（McCoy 氏 2017・*"the wording they use in CC0 is much more comprehensive"*）。 | **+33**（5,365 → 5,398）—— **B3 に対する実費用。** **⚠ 20 語で済む案を捨てた** —— §5.1 を丸ごと書き換える案（+20）は、末尾の限定句が **第 1 肢（Covered Right の不行使）にも掛かると読めて既存の約束を狭めうる**。**採ったのは第 1 肢を 1 語も変えない形**で、13 語の差は**「起草の曖昧さ」を避ける費用**である（否決理由として実際に書かれた語・#261 / Project Tick GPL）| **草案に反映済み**（2026-09-28）|
| **§2.5**（estoppel）| **1.1 の圧縮で落ちた 2 要素を戻す** —— (b) *"that reliance is the purpose of this Dedication and not merely a foreseeable consequence of it"* と (c) *"and is estopped from doing so to the extent the law of any jurisdiction gives that principle effect"* | **errata E34** —— **1.1 は「estoppel の芯だけ残した」「影響 **無し**」と評価したが、その評価は落とした語に依拠する文書を確かめずに下された。** `comparison.md` は「特許の carve-out が estoppel 抗弁を弱める」という**記録済みの批判への答え**として、**落ちた 2 要素を逐語で引いていた**（2026-09-25 実測・#231）。(b) は **意図された依拠**を単なる予見可能性から分ける要素で、promissory estoppel の足場としてより強い | **+36**（5,299 → 5,335）—— **B3 に対する実費用。****⚠ 1.0 の *"unsupported, or otherwise"* は戻していない**（*"ineffective for want of consideration"* に吸収。`comparison.md` 側の引用を後継へ合わせた）| **入った** |
| **冒頭の status block**（条文ではない）| 「いま 1.1 と同一である」という断定を、**一覧が空でも空でなくても真になる形**へ（*"Apart from the changes listed below, and the version number and the identifiers that name it, the operative text is ACD-1.1's"*）| **`against.md` #207** —— **2026-09-18 から 4 日間、草案は自分について偽を述べていた。** 468c は申告した語数を、468e は open な errata の一覧を守っていたが、**「前版と同一である」という文だけは、どの face も見ていなかった。** 害は文言ではない ——`ACD-1.1-SELF-AUDIT.md` の同一性監査が**この文を根拠として引いていた**。**見つけたのは外部の AI レビューで、同じ草案を読んだ 09-20 の 3 件は報告していない** | **本文 0**（ヘッダ）| **修復済み + Check 468f で両向きに機械強制**（2026-09-22・一覧が空なら述べよ／空でないなら述べるな。**両向きの RED を実測した**）|
| **§5.2**（不行使の covenant）| **(d) を足す** —— *"assert against You a right of privacy, publicity, or personality held by the Dedicator, in respect of any use of the Work that this Dedication permits"* | **errata E31** —— **§11.4 は「付与しない」と述べるが、Dedicator 自身が*行使しない*とは述べていない。** §5.1 の covenant は Covered Rights に限られ、これらは §1.5 に含まれない。**この Dedication が許した使い方をしている受領者を、Dedicator 自身が自分の肖像・声・実演の権利で訴える経路が開いていた**（`against.md` #173 の repair されていない半分）。**機構はこの文書が既に持っている** ——§12.2 が Moral Rights に対してまったく同じ形を使う。**§11.4 は 1 文字も動かさない**（あちらは*付与*、こちらは Dedicator の*行為*）| **+57** | **草案に反映済み**（2026-09-23）|
| **§2.9**（倒産）| **結果の断定を、文書の側の約束へ寄せる**（*"Nothing in this Dedication is conditioned on, suspended by, or revived by …"*）| **errata E30** —— **E5 が同じ条から落としたのと同じ形の断定が、第 1 文に残っていた。** *Jaffé v. Samsung*（4th Cir. 2013）は、まさにその結果が **4 日間の証拠調べと §1522(a) の衡量**で決まることを示している | **+2** | **反映済み** |
| **§16.1**（notice）| **2 つ目の carve-out を名指しする** | **errata E29** —— notice は**著作物と一緒に travel する唯一の面**。**⚠ 同じ notice を直すのは E3 / E12 に続いて 3 度目**で、**3 度とも「言い足りない」方向**である | **+7** | **草案に反映済み**（2026-09-20）|
| **§4.4** | **否定形を肯定形へ**（`not as a fallback for it: it takes effect whether or not Section 3 does`）| **errata E28** —— **#157 の軸に乗る最初の*観測された*誤読。** 仮説ではなく、**実際に誤読した読み手が 3 人いる** | **+7** | **草案に反映済み**（2026-09-20）|
| **§2.2 / §5.2(a) / §16.5** | **語順を変える**（2 件は語数不変）| **errata E27** —— **E19 / E20 / E21 が「1 条だけを読む読者」を守った規律を、初めて「文の中」へ当てた。****⚠ 見つけたのは手作業で、機械検出は精度 1 割で使えなかった** | **+1** | **草案に反映済み**（2026-09-19）|
| **§8.6 / §12.2** | **「どちらの分岐か判定する必要はない」を足す** | **errata E26** —— 同じ構造が 4 つあり、2 つにしか文が無かった。**⚠ §15 に 1 条だけ置く案（約 42 語）は採らなかった** ——読者が問いに出会うのは §8 と §12 であり、§15 に置けば相互参照を 2 本足すことになる（#151）| **+63** | **草案に反映済み**（2026-09-19）|
| **§15.6**（新設）| **1.0 §15.3 を一字一句そのまま戻す** ——2 つの canon を*不適用にする*規則 | **errata E25** —— 1.1 は「§15.1 が同じことを二重に言っている」として落としたが、**§15.1 は方向の規則で、§15.3 は不適用の規則**。**E20 が §15.1 を Work に限定したことで、§16 の上で 2 つの canon が反対向きに働き、順序を述べる語が本文に無い**状態になっていた | **+28** | **草案に反映済み**（2026-09-19）|
| **§2.6** | 「contribution 受入れの条件として別の書面を要求してはならない」という**禁止**を落とし、「この Dedication の下では追加の書面が要らない」という**事実の記述**を残す | **errata E22** —— 利用者に何も課さない instrument が、**プロジェクトの運営には 1 つだけ禁止を課していた**。§10.1 は無傷だが、**CLA を運用するプロジェクト（＝組織の後ろ盾を持つ層＝ B2 で最も欠いている層）が採用しづらくなる** | **+12** | **草案に反映済み**（2026-09-18）|

## errata 由来（`ACD-1.0.errata.md` が一次記録）

**この表は 1.2 で閉じた errata だけを載せる。** 1.1 で閉じたものは `ACD-1.1-CHANGELIST.md` に在り、
**Check 464 / 469(b) はどちらの表に載っていてもよい**（版ごとに行き先が分かれるため）。

| Errata | 対象 | 1.2 での扱い（要約は errata 側が権威）| 状態 |
|---|---|---|---|
| E34 | §2.5（estoppel）| **1.1 の圧縮が 2 要素を落とし、「影響無し」と評価されていた。** (b) *"that reliance is the purpose … not merely a foreseeable consequence"* と (c) *"and is estopped from doing so to the extent the law of any jurisdiction gives that principle effect"*。**評価は、落とした語に依拠する文書を確かめずに下された** —— `comparison.md` が記録済みの批判への答えとして両方を逐語で引いていた。**1.2 で復元（+36 語）。** **⚠ 1.0 の *"unsupported, or otherwise"* は戻さず、引用側を後継へ合わせた** | **入った** |
| E33 | §1.5 | **除外の列挙が網羅に見えて網羅ではなかった** ——データ保護・privacy・publicity・personality の権利は §11.4 からの推論でしか外れていなかった。**§1.5 に 4 つ目の除外として名指しし、§11.4 を指す**（+20 語・受領者が何をしてよいかは不変）| **草案に反映済み** |
| E32 | PREAMBLE | **「すべてを与える」は額面では偽だった** ——§11.1（商標）・§11.4（privacy / publicity / personality / データ保護）・§2.7（Dedicator が持つ権利にしか届かない）。**preamble は非 operative だと自分で述べているので受領者の行為は何も変わらないが、形は Chestek 氏（委員・元委員長）が別の審査で「内部矛盾」と呼んだものそのもの**で、**読者は carve-out より先にこの主張に出会う。** 真になる範囲へ言い換え、§11 を同じ息で指した | **草案に反映済み**（2026-09-23・**+15 語**）|
| E31 | §5.2 | **§11.4 は「付与しない」と述べるが、Dedicator 自身が privacy / publicity / personality 権を*行使しない*とは述べていない。** §5.1 の covenant は Covered Rights に限られ、§1.5 はこれらを含まない ——**この Dedication が許した使い方をしている受領者を、Dedicator 自身が自分の肖像・声・実演の権利で訴える経路が開いていた。** **「学ばれるために作られた著作物はしばしば人についてのデータである」と §11.4 自身が述べている**ので、仮定の経路ではない。**機構はこの文書が既に持っている** ——§12.2 が Moral Rights に対して同じ形（不行使の covenant）を使う。**§11.4 は動かさない**（*付与* と *行為* の区別は §12.1 / §12.2 が既に立てている）。**⚠ 届かないもの**: Work に写り込んだ**他人**の権利（§11.4 のまま） | **草案に反映済み**（2026-09-23・**+57 語**）|
| E30 | §2.9（倒産）| **第 1 文が「いかなる倒産手続も許諾に影響しない」と、法廷地が決める結果を断定していた。** E5 は同じ条から *"and so is not executory"* という**分類**の断定を落としたが、**結果の断定は残っていた**。**⚠ §10.4 と形は似るが性質が違う** ——§10.4 は「この文書に終了規定が無い」という検証できる事実で、§2.9 第 1 文は外部の法的事象の効果である。**第 2 文（officer を §2.8 の承継人とする）は変えていない** ——実際に効いているのはそちら | **反映済み（+2 語）** |
| E29 | §16.1（notice）| **2 つある carve-out のうち §11.1（商標・名称）しか名指ししておらず、§11.4（データ保護・プライバシー・パブリシティ・人格権）を通り過ぎていた。** **§11.4 は「学習されるための著作物はしばしば人についてのデータである」ゆえに在る条**で、**この instrument が最も届かない領域を述べているのはそちら** | **草案に反映済み**（2026-09-20・**+7 語**）|
| E28 | §4.4 | **fallback の読みを名指しして否定する形をやめ、肯定を述べる形にした。** 旧文は *"does not depend on Section 3 being ineffective"* ——**否定するために frame を口に出していた。** **3 人が実際にその読みを取っている**（#24 / #35 は起草側・2026-09-20 の外部レビューは外部）。**`granted independently of Section 3` は提出パケットが引用しているので残した** | **草案に反映済み**（2026-09-20・**+7 語**）|
| E27 | §2.2 / §5.2(a) / §16.5 | **修飾語と代名詞が「別のものに付く」読みを許していた 3 文**。§2.2 は**この instrument の中心的な約束**（撤回不能）の文で、末尾の限定が「撤回してはならない」にも掛かると読めた。§5.2(a) は *against You* が (a) 全体に掛かると読めた（Q26 の主張が弱くなる）。§16.5 は同じ文の中で *it* の指す先が 2 回変わっていた | **草案に反映済み**（2026-09-19・**+1 語**）|
| E26 | §8.6 / §12.2 | **法域で分岐して第 2 の足で差を閉じる構造が 4 つあり、そのうち §3（§4.4）と §9（§9.3）だけが「どちらか判定する必要はない」と読者に述べていた。** §8.6（特許）と §12.2（Moral Rights）は同じことをしているのに何も述べていない ——**欠陥は分岐ではなく非対称**。**既存の 2 文を写した**（新しい概念を持ち込まない） | **草案に反映済み**（2026-09-19・**+63 語**）|
| E25 | §15.6（新設・1.0 §15.3 を一字一句そのまま戻す）| **削除理由が規則の*種類*を取り違えており、同じ版の E20 と打ち消し合っていた** ——§15.1 は*方向*の規則、旧 §15.3 は*不適用*の規則で、方向は canon を切らない。**E20 が §15.1 に "in respect of the Work" を付けた結果、§15.1 は §16 に届かなくなり、届かない当の領域で §15.3 だけが両 canon を止めていた。** 1.2 では §16 の上で **contra proferentem（§16.4 の*制限*を狭く読む）と grant の狭義解釈（§16.4 の*許諾*を狭く読む）が同時に生き、順序を述べる語が無い** ——#157 で委員長が名指しした *unpredictable interpretation* を自分で作る形。**著作物について何が許されるかは 1 文字も変わらない**（§10.5 / §16.6） | **草案に反映済み**（2026-09-19・**+28 語・+1 条**）|
| E24 | §15.5（新設）| **1.1 の圧縮が、本文が実際に依拠している解釈規則を 3 つとも落としていた** ——`including` の列挙 12 件（うち *without limitation* を自称するのは §4.2 の 1 件のみ）/ 単数形 `Covered Right` 5 件 / EU 指令の参照。**比較の相手が違っていた** ——MIT・0BSD・Unlicense は列挙をほとんど持たない | **草案に反映済み**（2026-09-19・**+43 語**）|
| E23 | §2.8 | **別の権利者が法定の行為（EU Art.4(3) の留保）をしてよいかを本文が決めていた** ——同じ文が既に §6 を transferee に拘束しており、**禁止は拘束以上を足していない**。足していたのは「他人の法定行為についての規則」と「*expressio unius* で Dedicator は許されると読める余地」だけ | **草案に反映済み**（2026-09-19・**−8 語**）|
| E22 | §2.6 | **利用者に何も課さない instrument が、プロジェクトの運営には 1 つだけ禁止を課していた** ——「contribution 受入れの条件として別の書面を要求してはならない」を落とし、「この Dedication の下では追加の書面が要らない」という事実の記述を残す | **草案に反映済み**（2026-09-18・**+12 語**）|

## まだ開いているもの（1.1 から持ち越し）

- **E6** —— §8.4 が出力まで届くべきか。**検討して狭めないと決めた**ので、開いているのは
  「決めていない」からではなく「決めた結果として残している」からである。
- **E10** —— 記述子は版ごとに作るので、**版が変わるたびに閉じ直す必要がある。**
  1.1 では `ACD-1.1.machine.json` の `reservationsAndLimits.textRedistribution` で閉じた。
- **E11** —— §4.4 の法的説明。**errata としては 1.1 で閉じている**（2026-09-14・過大な 1 文 *"redundant but not void"* を落とし、1.1 / 1.2 草案とも 0 件）。
  **開いているのは設計の問い**（献呈と許諾を独立並行の footing にすべきか・読み A）**だけ**で、これは steward がリストへ出して未回答の問いであり B4 / B5 の OSI 判断側に属する。
  （**2026-09-28 訂正**: 旧文は「唯一の外部回答待ち」と述べ、errata が閉じた後も起草の問題が残っているように読めた。）
- **「新版の公開は旧版で与えた許諾に影響しない」旨の明文化**（出所 `review-responses-meta.md`・**2026-09-28 に 1.1 の候補表から移した**）
  —— 1.1 の候補表に「検討中」のまま残り、1.1 凍結後もどちらの一覧にも載っていなかった。
  **欠陥ではない**（§2.9 から導ける）ので errata にはしない。採るかは B3（長さ）との取引で決める。

## 我々宛でない議論からの採用候補（2026-09-22 新設・オーナー裁可待ちではなく、設計判断なので献策として置く）

**読み方を変えて出した 3 件。** いずれも**欠陥の指摘ではなく、リストが作業した結果**である。

| # | リストが作業したこと | ACD-1.0 の現状 | 候補 |
|---|---|---|---|
| **T1** | **対象の同定** ——Fontana 氏が OpenMDW に *"How do you know what the covered work is?"* を 1 か月かけて当て続けた（`against.md` #134）| **§1.2 は Work を「Dedicator がこの Dedication を適用した material」と、適用という行為で定める。** §2.7 が到達範囲を、Dedicator の識別義務が補う | **答えは部分的**（#134 が記録）。**スレッドが到達した整理**（何が同定を可能にするか）を 1.2 の §1.2 の説明へ反映できるか。**本文の変更を要するかは未判断** |
| **T2** | **サービスとしての引き渡し** ——ModelGo の定義は API / web アクセスを Distribution に含むのに、条件は複製の引き渡しを前提にしていた（steward 自身の問い・§1.106） | **ACD は条件を持たないのでこの gap は生じない。** §1.7 は Computational Use を、§6.4 はモデルと出力を扱う | **確認のみで足りる可能性が高い** ——「条件が無いので配信形態に依存しない」ことを §6 の説明に 1 文で書くか。**書かない判断も等しく妥当**（§10.1 が既に言っている）|
| **T3** | **trigger と scope は独立した設計次元**（steward が CPAL-1.0 を例に整理・§1.106）| **§10.4 は終了を持たず、§8.2 は報復を持たない** | **本文ではなく提出文の語彙として使える** ——「なぜ終了が無いのか」を、この 2 次元で説明すると短くなる。**B3（長さ）に効く方向** |

| **T4** | **§2.6 / §1.9 は、提出者がその材料の権利を持っていることを要求していない** ——§1.9 が定めるのは*意図*（"by or on behalf of the person for that purpose"）であって*権限*ではない（外部レビュー 2026-09-22）| **答えは §2.7**（この Dedication は Dedicator が持つ権利にしか及ばない）。**法効果は既に閉じている** ——誤って伝わるのは被覆範囲であり、**これは E16 と同じ構図**である | **低。** 実務の解は CONTRIBUTING / DCO / CLA というライセンスの外の層で、**それを条文へ引き込むと §2.6 が再び運営の規則になる**（E22 で落としたばかり）。**⚠ 下の反証を読んでから決めること** |
| **T5** | **§16.2 は、識別子が付いていれば「terms apply in full」と述べ、それを*誰が付けたか*に結び付けていない**（同上）—— 第三者の誤表示、依存関係ツールの推測タグ、比較記事の言及まで文面上は届く | **答えは §16.3**（"may be applied by anyone, to any work **in which they hold rights**"）**と §2.7**。**権利を持たない者のタグは、持たない権利には及びようがない** | **低。読む順の問題であり、E7 と同じ class。** §16.2 から §16.3 への前方参照 1 本で閉じうる（**+3 語程度**）。**⚠ ただし下の反証が、この処方そのものに当たる** |

**⚠ T4 / T5 の自明な処方には、同じ文書の中に反証がある。** 両方の答えは §2.7 であり、
自然な手当ては「§2.6 と §16.2 から §2.7 を引く」ことである。**測ると、§2.7 を明示的に引いて
いる条は 6 つ**（§6.1 / §6.2 / §6.3 / §7.2 / §8.5 / §11.4）**で、レビューが指摘した 5 条のうち
§2.6 / §16.2 / §8.4 はその 6 つに入っていない** ——ここまでは処方を支持する。
**だが §6.2 と §6.3 は §2.7 を二度引いており、レビューはそれでもこの 2 条を「矛盾して見える」
と報告した。** しかも**勧めてきた分離文は、すでに §6.2 の最終文と §6.3 の第 2 文にほぼ逐語で
在る。** **つまり「§2.7 を引く」は、少なくとも一人の注意深い外部の読み手に対しては、
境界を届かせるのに十分ではなかった。** それが条の失敗なのか読み手の注意の失敗なのかは
**一読では決まらず、n は 1 である。** **だから処方を採る前に、まず読み手が増えるのを待つ。**

**⚠ 5 件とも「採用」ではなく「候補」である。** T1 は本文に触れうるので設計判断であり、
**AI が勝手に本文の設計を変えないという線**（`REVISION-PROTOCOL.md`）に従う。
T2 / T3 は説明の側なので、**書かない判断も同じ重さで妥当**である。

**⚠ そして大半は本当に当たらない。** リストの議論の多くは**条件付きライセンス**（終了・帰属・相互性）
についてで、**ACD はそれらを意図的に持たない。** 「当たらない」は正しい答えである ——
**誤りだったのは、それを*唯一の*問いにしていたことである。**

## やらないと決めていること

- **§8.6 の *"the patent claims that Section describes"* は直さない**（外部レビュー 2026-09-22 が
  「参照先を特定せよ」と述べた箇所・**1.0 / 1.1 / 1.2 草案で逐語同一**）。**指摘は文法的には正しい**
  ——"Section 8.1 or Section 8.4" のあとの単数の "that Section" は、どちらを指すか語だけでは
  決まらず、**8.4 の方が広いので差は実質的**である。**だが §15.1 がその差を読者に有利な側で
  既に閉じている** ——*"the reading that grants more to You prevails"* であり、E20 が §15.1 へ足した
  限定（§10.1 の house phrase *"in respect of the Work"*）は §8.6 に届く（§8.6 の covenant は *"in respect of any use of the
  Work or of anything resulting from Computational Use of it"*）。**精密化は +5 語前後で、
  B3 に対して払う価値が無い。** **⚠ 逆側を書いておく**: §15.1 に依拠するということは、
  **§15.1 が無効とされた法域では曖昧さが戻る**ということである。**そのときに直す。**

- **§§8.3 / 8.4 / 9.4 / 11.4 / 12.4 / 16.4 から「理由づけ」を別文書へ出す案は、いま採らない**
  （同レビュー P2・**B3 = 長さに効きうる唯一の提案**）。**測った: この 6 条で 831 語 = 本文の
  16.0%。** **これは上限であって削減量ではない** ——各条には残さねばならない規範の核がある。
  **⚠ そして我々自身の記録に、まさにこの手の反証がある。** **errata E24 / E25 は、1.1 が
  「§15.1 が同じことを言っている」として構成規則を落とし、それが誤りだったので 1.2 で戻した
  記録である。** §8.4 の *"This is a grant in its own right and not a clarification of Section 8.1"*
  は説明に見えて**構成を方向づける文**であり、**落とせば、それが防ぐために在る read-down を
  招く**（条文自身がそう述べている）。**外へ出すなら 1 条ずつ、どの文が規範でどの文が理由かを
  判定してからで、機械的な一括抽出はしない。** B3 の既測（機構部の圧縮で約 4,230 語）と
  **二重計上しないこと。**

- **1.1 の本文を直さない。** 直したくなったら 1.2 で直す（Check 453 が byte を pin する）。
- **長さを、gap を削って縮めない。** 縮小の余地は `ACD-1.1-CHANGELIST.md` §2.5〜§2.8 で
  実測済みで、**機構部だけを削ってもChestek 氏が engage しなかった水準には届かない**。
- **採用実績を作るためにライセンスを歪めない**（register B2）。

## Constraints

- **`ACD-1.0.txt` / `ACD-1.1.txt` とその記述子は編集しない**（Check 453）
- 草案の申告語数・条数は実測と一致させる（Check 468）
- Check 459 が索引（`LICENSES/README.md`）からの到達性を、Check 461c が `last-updated` を強制

## Change impact

**本表に行を足したら**、同じ変更を `ACD-1.2-DRAFT.txt` の冒頭の変更一覧にも足す（**2026-10-17 に確定したので、この表への追加は終わった。** 次版の変更は `ACD-1.3-CHANGELIST.md` と `ACD-1.3-DRAFT.txt` へ）。
**片方だけ直すと、草案が自分の状態について偽を述べる**（Check 468e が errata について同じことを強制する）。

## Audience-specific notes

- **審査者**: list 上の議論と提出の対象は `ACD-1.0.txt`（`submission.md` の `SUBMISSION-TARGET`）であり、`ACD-1.1.txt` は凍結済み・未提出の後継テキストである（**2026-09-28 訂正**: 旧文は「議論の対象は `ACD-1.1.txt`」と述べていた）。本書は**その次**に何が入るかの記録で、
  **1.1 の本文は本書の存在によって一切変わらない。**
- **後任 AI**: 表の行数を「記録の量」と読まないこと。**作成直後（2026-09-17）は空が正しい状態だった**が、いまは 1.2 草案で閉じた errata と次版候補が載っている（**2026-09-28 訂正**: 旧文は「空が正しい状態である」と現在形で述べ、冒頭を訂正したあともこの行だけ残っていた）。

## 条項の対応表（1.0 → 1.2）—— 提出対象を切り替える日に使う

**条番号は版をまたいで保存されない。** 提出側の文書（`submission.md` /
`submission-reference.md` / `REVIEWERS.md` / `objection-map.md`）は **1.0 の条番号で引用している**ので、
**`SUBMISSION-TARGET` を切り替えたら引用も写像する。**
**Check 472 が、写像し忘れた引用を BLOCKING で指す**（実測: 切り替えると 3 面で 7 件出る）。

| 1.0 | 1.2 | 内容 |
| :-- | :-- | :-- |
| **§1.2 / §1.3 / §1.4 / §1.6** | **§1.3 / §1.4 / §1.6 / §1.2** | **🔴 定義の番号は動いている**（下の表）——**E13 の並べ替えは「順番」ではなく「番号」を変えた** |
| §1.1 / §1.5 / §1.7〜§1.10 | **同じ番号** | Dedication / Covered Rights / Computational Use / Machine-Generated Material / Contribution / Reservation |
| §2.x〜§14.x | **同じ番号** | 番号は保存される（**ただし本文が変わった条がある** ——下の注意）|
| §15.1 | **§15.1** | 構成規則（1.2 は §10.1 の house phrase を足して著作物に限定した・E20）|
| §15.2 | **無し** | 単数複数の読み替え |
| §15.3 | **無し** | 起草者不利の解釈原則の排除 |
| §15.4 | **§15.2** | 可分性 |
| §15.5 | **無し** | 不作為・沈黙（**§2.2 が吸収**）|
| §15.6 | **無し** | 代理・組合関係の不成立 |
| §15.7 | **§15.3** | 準拠法・法廷地を定めない |
| §15.8 | **§15.4** | 英語が正文 |
| §16.1〜§16.3 | **同じ番号** | 通知・識別子・誰でも適用できること |
| §16.4 | **§16.4** | **1.0 の §16.5（翻訳の但し書き）を吸収**し、識別子の族・Steward の例外・再符号化を追加 |
| §16.5 | **§16.4 へ統合** | 翻訳の但し書き |
| §16.6 | **§16.6** | **1.2 の §16.5 は新設の Steward の定義**なので、closer は §16.6 のまま |

### 🔴 §1（定義）の対応 —— 番号は保存されていない

**定義語で突き合わせて導出した**（`"X" means` を鍵にする。番号ではなく語で照合するので、
**並べ替えの向きを推測しない**）:

| 1.0 | 定義語 | 1.2 |
| :-- | :-- | :-- |
| §1.1 | Dedication | **§1.1** |
| §1.2 | **Work** | **§1.3** |
| §1.3 | **Dedicator** | **§1.4** |
| §1.4 | **You** | **§1.6** |
| §1.5 | Covered Rights | **§1.5** |
| §1.6 | **Moral Rights** | **§1.2** |
| §1.7〜§1.10 | Computational Use / Machine-Generated Material / Contribution / Reservation | **同じ番号** |

**つまり提出側の文書にある `§1.4`（"You" のつもり）は、1.2 では *Dedicator* を指す。**
**番号が存在するので Check 472 は通る。意味だけが入れ替わっている。**

**⚠ 番号が同じでも内容が違う条がある** ——**写像表で「同じ番号」と書いてあることは、
「同じことを述べている」を意味しない。** §15.1 / §16.4 は番号が保存されるが**本文が変わっている**。
**引用が逐語なら、逐語も当て直す**（`ACD-1.1-CHANGELIST.md` §0.13 が挙げた 1 件の実例がその形）。

## 次版に、§4c の機械的性質を当てた（2026-09-28・clean）

**提出パケット §4c は「弁護士が読んでいないので、代わりに機械で確かめた性質」を 1.0 について
並べている。****その同じ性質を、我々が実際に出すつもりの版へ当てた記録は無かった。** 当てた:

| 性質 | ACD-1.0 | ACD-1.2 草案 |
| :-- | :-- | :-- |
| 定義語がすべて定義され、未使用が無い | 10 / 未使用 0 | **10 / 未使用 0** |
| 節が 1〜16 で連番 | 16・連番 | **16・連番** |
| 非 ASCII バイト | 0 | **0** |
| 相互参照が実在する条へ解決する | 解決 | **43 件すべて解決** |
| 英語を正文と規定する条 | §15.8 | **有** |
| 操作条項に `shall` / `must` | 0 / 0 | **0 / 0** |

**⚠ `must` は草案の冒頭 status block に 2 回出る**（*"Citations to 1.0 **must** keep …"* /
*"it **must** be closed again for each new version"*）。**これは草案が自分について述べている
メタ情報で、ライセンス本文ではない。** **§4c の主張は本文についてのものなので、当たらない。**
**だが「0 件」と書くときは、どこを数えたかを併記する。**

**⚠ 条数はここに書かない。** 手元の正規表現では書式差で 47 とも 82 とも数えられ、**どちらも誤り**
だった（草案の申告は 80 で、**Check 468 がその一致を機械強制している**）。
**条数の権威は Check 468 であり、その場の正規表現ではない。**
**この 2 つの数え違いは、同じ日に列挙の数え違いを 1 件出したのと同じ族である**
（`against.md` #243 —— **数は書くのではなく導く**）。

## 提出対象を 1.2 へ切り替える日の、引用の写像表（全件・**2026-09-28 に再実測**）

**`SUBMISSION-TARGET` を `ACD-1.2` にした瞬間に直すもの。** 提出側 4 面が引く 1.0 の条は **62 件**で、
`measure_citation_drift.py` の分類は **消失 2 / 番号は在るが本文が変わった 26 / 実質同一 34**。

**⚠ 2026-09-19 の初版は 59 件 / 消失 2 / 変わった 19 / 同一 38 と述べ、*「下は 59 件すべてについての
判断である」*と完全性を主張していた。** 引用は増え、草案も動くので、**この節の数は放っておけば必ず
古くなる**（Check 469 が「自己申告の*列挙*」について守っている当の形で、**数のほうは誰も見ていなかった**）。
**当日は必ず `python3 .github/scripts/measure_citation_drift.py` を回してから表を読むこと。**

**再実測で確かめたこと**: 道具が名前を挙げる 28 条（変わった 26 + 消失 2）は、**すべて本節のどこかに
行を持っている**（§2.8 / §5.2 / §8.2 / §8.6 / §12.2 を含む）。**増えた 3 件は「実質同一」側**なので、
**当日の作業が増えるわけではない。** **⚠ ただしそれは今日の分類であって、次に草案を動かせば変わる。**

**下は上記 28 条についての判断**である。**当日は、数を測り直したうえで、判断ではなく実行だけが残る。**

### A. 触らないもの —— 1.0 の番号について*わざと*述べている箇所

| 場所 | なぜ触らないか |
| :-- | :-- |
| `submission.md` の `SUBMISSION-TARGET` 注記（§15.5 / §15.7 / §15.8 / §16.4〜§16.6 を挙げる）| **「1.0 のこの番号は次版に無い」と述べている文**である。写像すると意味が消える |
| `REVIEWERS.md` の「どちらのテキストを見ているのか」節（§15.5–§15.8 / §15.2–§15.4 / §16.4–§16.6）| 同上。**ただし §15.5 が 1.2 に新設されたので、この節の文は書き直す**（下記 D-0）|

**⚠ だから一括置換はできない。** `check-map §2.9` が prose のパス参照を Check にしなかったのと同じ理由 ——
**歴史の記述と生きた主張を、正規表現は区別しない。**

### B. 番号が動いたもの（定義）—— 機械的に置換できる

> **⚠ 2026-09-24 訂正: この節の「引用箇所」は行番号で書かれていて、11 箇所のうち 9 箇所が既に別の行を指していた。**
> `submission-reference.md` はその後も編集されている（本日だけで §3b-i・§4b・§4c が書き換わった）ので、
> **行番号は書いた日の位置であって、確定の日の位置ではない。** 置換はこの表の行番号ではなく、
> **確定の日に `grep -nE '§1\.2[^0-9]|Section 1\.2[^0-9]' LICENSES/ACD-1.0.submission-reference.md` のように
> その場で導出して**行うこと。**この表には**行番号を書かず、件数だけを書く**（件数も動くが、動いたことは grep の出力と比べれば分かり、
> 誤った行を書き換える事故にはならない）。**§4c の「§1.2→§1.3 …」の文は
> 1.0 の定義の並び（E13）を述べる文**なので、写像ではなく版を名指しする書き換えが要る。

| 1.0 | → 1.2 | 引用箇所 |
| :-- | :-- | :-- |
| **§1.2**（Work）| **§1.3** | `submission-reference.md` 5 箇所（2026-09-24 実測・うち 1 箇所は §4c の E13 の文で、写像でなく版の名指しが要る）|
| **§1.4**（You）| **§1.6** | `submission-reference.md` 2 箇所 |

### C. 番号が動いたもの（機構）—— 機械的に置換できる

| 1.0 | → 1.2 | 引用箇所 | 備考 |
| :-- | :-- | :-- | :-- |
| **§15.2**（解釈規則）| **§15.5** | `submission-reference.md` 2 箇所 | **E24 で復元したので写像先がある。** 復元前はこの 2 件が**行き場を失っていた** ——それが E24 の発見経路である |
| **§15.7**（準拠法を定めない）| **§15.3** | `submission-reference.md` 2 箇所 | |
| **§15.8**（英語が正文）| **§15.4** | `submission-reference.md` 3 箇所 | |
| **§16.5**（翻訳の但し書き）| **§16.4** | `submission-reference.md` 1 箇所（**§4b の 2 箇所は対象外**: 既に「the successor's §16.5（Steward）」と版を明示して引いている） | **1.2 の §16.5 は Steward の定義**なので、番号のまま残すと別の条を指す |

**⚠ §15.3（contra proferentem）→ §15.6 の行は要らない（2026-09-20 に確認）。** E25 で
**1.2 に同じ文言が §15.6 として戻った**ので写像先は在るが、**提出側 4 面で 1.0 §15.3 を引いている
箇所は 1 つも無い**（唯一の言及は `REVIEWERS.md` の版分岐の節で、**既に「1.2 の §15.6」と版を
名指ししている**）。**置換の要る引用が無いので表に行を足さない** ——**行を足すと「直す作業が
残っている」と読まれる。**

### D. 書き直しが要るもの（番号の置換では済まない）

**D-0. `REVIEWERS.md` の版分岐の節。** 「1.0 の §15.5〜§15.8 に 1.1 の対応物は無い」は
**E24 で §15.5 が、E25 で §15.6 が新設されたので、そのままでは誤りになる。** 正しくは
**「1.0 の §15.5 / §15.7 / §15.8 に同番号の対応物は無く、§15.2 の中身は 1.2 §15.5 に、
§15.3 の中身は 1.2 §15.6 にある」。** ——**2026-09-19 に `REVIEWERS.md` 側を直したので、
この項目は「予定」ではなく「済み」である**（残りの D-1 / D-2 は未着手）。

**D-1. `submission-reference.md` の前方参照の分析。** 1.0 の定義順を前提に
*"The three forward references are §1.2→§1.3, §1.3→§1.5 and §1.5→§1.6"* と述べている。
**1.2 は E13 で並べ替えている。2026-09-20 に 1.2 本文へ当てて実測した**（定義 10 件を互いに走査）:

| | 1.0 | **1.2（実測）** |
| :-- | :-- | :-- |
| 定義の並び | Dedication / Work / Dedicator / You / Covered Rights / Moral Rights / … | **Dedication / Moral Rights / Work / Dedicator / Covered Rights / You / …** |
| 相互定義 | 1 対（Work ⇄ Dedicator）| **2 対**（Work ⇄ Dedicator・**Dedicator ⇄ Covered Rights**）|
| 前方参照 | 3 件 | **2 件**（§1.3 Work → §1.4 Dedicator / §1.4 Dedicator → §1.5 Covered Rights）|

**差し替える段落（英文・確定日はこれを貼るだけ）**:

> **Two mutual pairs and two forward references, all stated rather than denied.** The pairs are
> **"Work" ⇄ "Dedicator"** (§1.3 defines the Work by reference to the Dedicator, §1.4 the Dedicator
> by reference to the Work) and **"Dedicator" ⇄ "Covered Rights"** (§1.4 is qualified by the rights
> the party holds, §1.5 defines those rights as the Dedicator's). **Neither is vicious**, because
> both are anchored to an act outside the definitions — the placing of the notice under §16.1 — so
> each pair is fixed by something a reader can observe rather than by the definitions alone. **This
> is the ordinary shape**; MIT and Apache-2.0 tie their "Work" and licensor terms the same way.
> **The two forward references are §1.3→§1.4 and §1.4→§1.5.** A reader going strictly top-down
> meets a term twice before it is defined. **No reordering removes both**, because the mutual pairs
> guarantee at least one each.

**⚠ 逆側を落とさない**: **1.0 の「3 件」から減ったのは E13 の並べ替えの効果だが、
*相互定義は 1 対から 2 対へ増えている***（`Covered Rights` が `Dedicator` を使い、
`Dedicator` が `Covered Rights` で限定されるため）。**「改善した」とだけ書くと片面になる。**

**D-2. `submission-reference.md` の §6.4 の逐語引用。**
*"You owe nothing in respect of any of them. Nothing in this Dedication requires You to license,
disclose, or attribute any such thing."* を**連続した 2 文**として引いているが、
**1.2 では間に 1 文が入る**（*"Whether a right subsists in any such thing is not decided here and
does not need to be (Section 9)."*）。**連続引用として成立しない。**

**差し替える引用（確定日はこれを貼るだけ）**:

> §6.4: *"You owe nothing in respect of any of them. … Nothing in this Dedication requires You to
> license, disclose, or attribute any such thing."*

**省略記号を入れるだけで足りる。** **落ちる 1 文は主張を弱めない**
——*"Whether a right subsists … is not decided here"* は「出力に条件が付かない」という
主張と同じ向きで、むしろ補強する。**⚠ それでも省略は省略と示す**
（2026-09-20 の引用掃引で、**編集が忠実さを壊す形を 6 件**見ている・`against.md` #166）。
（`ACD-1.1-CHANGELIST.md` §0.13 が既に挙げていた 1 件で、
**本掃引が独立に再発見した** ——§0.13 の「確定時にもう一度回す」という指示が働いた形である。）

### E. 番号も主張も生きているもの —— 11 条すべて

**§6.1 / §6.3 / §6.4 / §4.4 / §8.4 / §10.4 / §11.1 / §16.1 / §16.2 / §16.3 / §16.4** は
**本文が変わっているが、提出側が述べている主張はいずれも 1.2 で成立する。** 1 件ずつ当てた:

| 条 | 変わったこと | 主張は生きるか |
| :-- | :-- | :-- |
| §4.4 | E11 が「§3 が有効なら relied upon され得る」を落とした | **生きる** ——引かれているのは *"granted independently of Section 3"* で、**その文は残っている** |
| §6.1 | E19 が house phrase を足した | **生きる**（射程が明示されただけ）|
| §6.3 | 撤回と依拠の否認を分けた | **生きる。むしろ鋭くなる** ——*"to the fullest extent the Dedicator is able"* は残る |
| §6.4 | E4 が *"is not encumbered"* → *"no enforceable claim arises"* | **主張は生きるが、逐語引用は D-2 で壊れる** |
| §8.4 | E15 が因果の限定を足した | **生きる** ——モデル・出力へ届くことは残る |
| §10.4 | E9 が第 2 文に *"in respect of the Work"* を足した | **生きる** |
| §11.1 | §10.5 への前方参照を足した（E7）| **生きる** |
| §16.1 | E1 / E3 / E12 が notice を直した | **生きる** ——引かれているのは「notice を置く行為」である |
| §16.2 | 識別子の版が変わるだけ | **生きる** |
| §16.3 | E2 が *"in which they hold rights"* を足した | **生きる。引用文はその追加後の形と一致する** |
| §16.4 | 族への拡張・Steward の例外・翻訳の吸収 | **生きる。翻訳についての主張は §16.4 の中に移ったので、むしろ短くなる** |

**この 11 件は、番号も文言の要旨も変えなくてよい。** **修正が必要なのは B / C / D だけである。**

### ⚠ この表が establish しないこと

**「主張が生きる」は我々の読みである。** 1 件ずつ現物に当てたが、**逐語引用の一致は当初 D-2 の
1 件しか機械で確かめていなかった。**

**2026-09-20 に機械で全数確認した。結果は D-2 以外に問題なし。**

| 測定 | 値 |
| :-- | --: |
| **ACD-1.0 本文の逐語引用と確定したもの**（ドシエ全 `LICENSES/*.md`）| **117** |
| そのうち **1.2 では成立しないもの** | **12** |
| うち**意図的に旧文言を引いているもの**（errata / changelist / 不利な事実 / 台帳の記録）| **11** |
| うち**実際に直す必要があるもの** | **1（＝ D-2）** |

**方法の肝は 1 つ**: **「これは本文の引用か」を文脈から推測せず、*凍結された 1.0 本文に一致するか*で
確定させる。** 文脈から推測する版は**母数 540・不一致 343** を返し、**その大半が「条番号に言及する
段落で引かれた人の発言」**だった（`check-repository-consistency-map.md` §2.9）——
**検出器が誤っていたのであって、ドシエが誤っていたのではない。**
**凍結本文を錨にすると、意味の判断が 1 つも要らなくなる。**

**⚠ この測定が establish しないこと**: **「主張が生きる」を確かめたのではない。**
確かめたのは**逐語の一致だけ**で、**引用が成立しても主張がずれることはありうる**
（E の 11 条について「主張は生きる」と述べているのは依然として我々の読みである）。
**確定の日には `verify_dossier_quotations.py` も新版に対して回すこと**
（`ACD-1.1-CHANGELIST.md` §0.13 が求めている抽出の再実行がこれである）。

## 確定前の最終点検（2026-10-17・凍結の直前）

**オーナーの依頼「区切りよくした上で凍結」** に従い、草案を 6 観点（相互参照 / 1.1 との差分と変更一覧の完全性 / 起草 / OSD / 機械可読性 / errata の状態の主張）から読ませ、指摘 1 件ごとに 2 人の反証役を当てた（同セッションの workflow・読み取りのみ）。指摘は 32 件・重複を除いて十数件。**反証役の一部は利用制限で回らなかったので、残りは本文を直接読んで判定した。**

**凍結前に直したもの（条文）**:

| 条 | 直したこと | 理由 |
| :-- | :-- | :-- |
| §5.2(b) | 末尾の "or" を落とした | (d) を足したときに残った |
| §11.4 | "It reaches nothing else" に「§5 の約束は Dedicator 自身の行為についての約束で、この文に縛られない」を足した | §5.1 第 2 肢と §5.2(d) は Covered Rights・特許・人格権の外へ届くので、そのままでは条文が自分と食い違う |
| §8.6 | 最終文を「有効ならその許諾が、無効とされたらこの約束が働く」へ | 約束は無効とされた場合にだけ働くのに、「この条の何も有効性に左右されない」と述べていた |
| §16.1 | 通知文に personality を足した | E29 の項目は「§11.4 の carve-out を名指す」と述べていたが、4 つのうち personality が抜けていた |

**凍結前に直したもの（草案ヘッダの記述）**: 変更一覧から §5.1 第 2 肢（#272）と §8.2 の書き換え（#265 (b)）が抜けていた（冒頭は一覧が差分のすべてだと宣言している）/ E31 の説明が §5.1 を「Covered Rights だけ」と述べていた（第 2 肢を足した後は偽）/ E24 の「単数形の Covered Right 5 か所」が 4 つの条しか挙げていなかった（§7.1 が抜けていた）/「some sixty clauses later」→ 実測 52 条。

**誤りと判定したもの**: 「without limitation と書くのは §4.2 だけ、は誤りで §13.1 にもある」——実測すると §4.2 だけで、ヘッダは正しかった。

**1.3 へ回したもの**: `ACD-1.3-CHANGELIST.md` の表を参照。

## 付録: 確定時点の草案ヘッダ（逐語）

確定版の冒頭は身分の表示だけにしたので、草案が冒頭に持っていた変更一覧を、確定の直前の状態のまま残す（**記録を消さないため**）。

```text
ACD-1.2 -- DRAFT. NOT IN FORCE. NOT SUBMITTED. NOT APPLIED TO THIS REPOSITORY.

  This file is the successor text under construction. The frozen text now put
  forward for discussion is ACD-1.1 (LICENSES/ACD-1.1.txt), and the licence
  that covers this repository is ACD-1.0. Both are pinned by SHA-256 in
  LICENSES/FROZEN.md and verified in CI; nothing here changes either of them.

  Status of this draft, stated plainly so that nobody has to infer it:

    * It has had no legal review, like 1.0 and 1.1.
    * It has not been posted to any list. (Posting about ACD-1.1 resumed
      on 2026-09-17; the current state is LICENSES/FROZEN.md POSTING-STATUS.)
    * Apart from the changes listed below, and the version number and the
      identifiers that name it, the operative text is ACD-1.1's. **An empty
      change list below means nothing has been changed yet -- not that the
      record is missing; a list with entries in it is the whole of the
      difference.**
    * Clause numbers follow ACD-1.1, not ACD-1.0. Citations to 1.0 must keep
      using the 1.0 text, and citations to 1.1 the 1.1 text.
    * Changes will be recorded in LICENSES/ACD-1.2-CHANGELIST.md, and defects
      this draft introduces itself in LICENSES/ACD-1.1-SELF-AUDIT.md, which is
      a register of our own sweeps rather than of any one version.

  Changes in this draft, relative to ACD-1.1:

    * Section 2.6 no longer forbids the Dedicator from asking a contributor for
      anything (errata E22). The sentence said that no separate instrument,
      assignment, or agreement "may be required of them as a condition of the
      Contribution being accepted", which reads as a rule about how a project
      governs its own contributions rather than about what a recipient of the
      Work may do. It imposed nothing on You, so Section 10.1 was untouched;
      what it did was make this Dedication awkward for any project that runs a
      contributor agreement -- which is most institutionally backed projects,
      the adopters this instrument most lacks. The half worth keeping is kept:
      nothing further is needed to place a Contribution under this Dedication.
    * Section 2.8 no longer says that a transferee "may not make a Reservation
      in respect of the Work" (errata E23). The same sentence already binds
      Section 6 to transferees, and Section 6.2 has the Dedicator make no
      Reservation and decline to make one while Section 6.3 withdraws any that
      exists and disclaims reliance on it -- so the prohibition added nothing
      the binding did not already do. What it did add was a rule about whether
      a different rightsholder may perform a statutory act, which is not this
      document's to decide (the reasoning of errata E5), and a named
      prohibition on the transferee alone, which invites the reading that the
      Dedicator may do what the transferee may not.
    * A new Section 15.5 restores the three rules of construction that ACD-1.0
      carried at its Section 15.2 and that this line of drafting dropped
      (errata E24). Dropping them was reasoned from the wrong comparison. The
      three short permissive texts it was compared with (named in errata E24)
      carry no general rule of construction -- though one carries the device
      inline in its operative grant ("including without limitation") and
      another in its disclaimer ("including but not limited to") -- and, more
      to the point, they carry almost no enumerations to need one: two, one
      and one, where this text has twelve. Without the rules, (a) each of
      the twelve lists introduced by "including" -- among them the definitions
      of Work, Covered Rights, Computational Use and Reservation, which are the
      definitions that carry what this text claims is new -- invites the
      reading that the list is exhaustive, which is the same *expressio unius*
      argument this draft has used three times on itself; (b) the five uses of
      the singular "Covered Right", in Sections 2.8, 3.3, 5.1, 6.4 and 7.1, are a
      form of a term defined only in the plural; and (c) the reference in
      Section 1.10 to Article 4(3) of Directive (EU) 2019/790 is a reference to
      the 2019 text alone. Only Section 4.2 said "without limitation" on its
      own.
    * A new Section 15.6 restores, word for word, the rule of construction
      that ACD-1.0 carried at its Section 15.3 and that this line of drafting
      dropped (errata E25). It was dropped on the ground that Section 15.1
      already says the same thing twice. That was true of one half of it and
      never of the other: Section 15.1 is a rule of direction and Section 15.3
      was a rule of disapplication, and a direction cannot switch a canon off.
      Since errata E20 the point is sharper still, because Section 15.1 now
      reads "in respect of the Work" and so reaches none of Section 16, where
      the dropped rule reached everything. The effect of dropping it was that
      two canons of construction came back on over Section 16 and pulled in
      opposite directions on the same clause, with nothing in the text to
      order them -- contra proferentem reading Section 16.4's restriction
      narrowly, and the narrow construction of grants reading Section 16.4's
      permissions narrowly. Nothing about the Work was affected either way
      (Sections 10.5 and 16.6), which is why this is stated as a repair of an
      accident rather than as a defence of a clause.
    * Sections 8.6 and 12.2 now each say that You are not required to
      determine which of their branches applies (errata E26). Four Sections
      operate differently according to the law of a jurisdiction and then
      close the difference by a second footing, and until now only two of
      them -- Section 4.4 for the surrender, Section 9.3 for machine-generated
      material -- said so to the reader. The patent grant and the moral rights
      waiver did the same thing and said nothing, so a reader met the branch
      at Section 8.6 and Section 12.2 with no statement that it did not matter
      which side of it they were on. The asymmetry is the defect; the sentences
      are copied from the two that already existed.
    * Three sentences are re-ordered so that a qualifier or a pronoun cannot
      attach to the wrong thing (errata E27). No word is added to two of them
      and one word is added to the third; nothing they say changes. In Section
      5.2(a) "against You" now precedes the law it qualifies, so it can no
      longer be read as governing the covenant not to apply a technological
      measure at all. In Section 2.2 the qualifier "in respect of any copy of
      the Work that has been made available" now sits in front of the term it
      limits, so it can no longer be read as limiting the prohibition on
      withdrawal -- which is the instrument's central promise and was two-way
      on the face of that one sentence. In Section 16.5 the second "it"
      becomes "that role", because the first "it" in the same sentence refers
      to the text and the second referred to the role.
    * Section 4.4 no longer denies a fallback reading by naming it; it states
      the positive instead (errata E28). The old wording said the licence
      "does not depend on Section 3 being ineffective", which states the
      fallback frame in order to reject it. Three readers have taken the frame
      anyway: this dossier did so twice and had to correct itself (adverse
      facts 24 and 35), and an outside reviewer did so on 2026-09-20 while
      calling the clause appropriate. The phrase "granted independently of
      Section 3" is kept because the submission packet quotes it.
    * The recommended notice in Section 16.1 now names the second carve-out as
      well as the first (errata E29). It said "trademarks and other rights in
      names are not granted (Section 11)", which names Section 11.1 and passes
      over Section 11.4 -- data protection, privacy, publicity, personality --
      although Section 11.4 exists because a work meant to be learned from is
      often data about people. The notice is the surface an adopter reads and
      the only one that travels with the Work, so a carve-out it does not name
      is a carve-out most readers never meet.
    * Section 2.9 no longer states what an insolvency proceeding does; it
      states what this Dedication does (errata E30). The old first sentence
      said that no such proceeding and no act of an officer "affects a
      permission granted here or revives a right given away", which is a
      statement about the result a forum will reach, not about the terms of
      this instrument -- the same defect errata E5 removed from the sentence
      beside it when it dropped "and so is not executory". The point is live:
      in Jaffe v. Samsung (4th Cir., 3 December 2013) a foreign representative
      sought authority to cancel licences to the debtor's US patents, and the
      answer took a four-day evidentiary hearing and a discretionary balance.
      The new wording keeps the assurance and puts it where it belongs: nothing
      here is conditioned on, suspended by, or revived by such a proceeding.
      The second sentence is unchanged, and it is the part that does the work
      -- the officer takes as a transferee under Section 2.8.
    * Section 5.2 gains a fourth covenant (errata E31). Section 11.4 says that this
      Dedication grants no permission under a right of privacy, publicity, or
      personality; it does not say that the Dedicator will not assert one. In
      ACD-1.1 the covenant in Section 5.1 reached Covered Rights only, and
      Section 1.5 does not include these, so nothing in the text stopped a
      Dedicator from suing a
      recipient -- under their own likeness, voice, or performance -- for a use
      this Dedication permits. That route is not hypothetical for an instrument
      written for works meant to be learned from, which Section 11.4 itself says
      are often data about people. The mechanism is one this text already uses:
      Section 12.2 gives exactly this form of covenant for Moral Rights where a
      waiver is unavailable. What Section 11.4 grants is not touched, because
      this speaks of the Dedicator's own conduct -- the same distinction
      Sections 12.1 and 12.2 already draw -- and rights of this kind held by
      anyone else are untouched; the second sentence of Section 11.4 is
      qualified so that it does not contradict this covenant (see below).
    * The preamble no longer says that this Dedication "gives everything away"
      (errata E32). Read at face value that sentence is false: Section 11.1
      grants no trademark right, Section 11.4 grants nothing under privacy,
      publicity, personality or data-protection law, and Section 2.7 reaches
      only rights the Dedicator holds. The preamble marks itself as not part of
      the operative terms and nothing in it qualifies them, so nothing a
      recipient may do turns on the sentence -- but the shape is the one a
      Licensing Committee member has called internally contradictory in another
      review, and a reader meets the claim before meeting the carve-out. The
      replacement keeps the force within the scope that is true and points at
      the carve-out in the same breath.
    * Section 1.5 now names the fourth exclusion (errata E33). Its list of
      what Covered Rights excludes named patents, trademarks and names, and
      Moral Rights, and stopped; rights under data protection, privacy,
      publicity, or personality law were excluded only by inference from
      Section 11.4, fifty-two clauses later, while Section 1.5 defines Covered
      Rights as every right "however arising" and Section 15.1 asks for the
      widest reading. Nothing a recipient may do changes; the definition now
      states its own boundary instead of leaving it to be inferred.
    * Section 2.5 restores two elements of the reliance clause that ACD-1.1's
      compression dropped (errata E34): that reliance is the purpose of this
      Dedication and not merely a foreseeable consequence of it, and that the
      Dedicator is estopped from asserting revocability or want of
      consideration to the extent the law of a jurisdiction gives that
      principle effect. Nothing a recipient must do changes; what moves is the
      strength of the fallback if Section 3 fails. This entry was missing when
      the clause changed, so for three days this list did not state the whole
      of the difference, as it says it does.
    * Section 6.1 now says "for any purpose, whether or not commercial". The
      permission is the same as in ACD-1.0 and ACD-1.1; only the wording
      differs. The earlier wording led a widely used licence scanner to
      misclassify this text; the measurement, and why the earlier words are
      not quoted here, are in ACD-1.2-CHANGELIST.md.
    * Section 5.1 gains a second limb: the Dedicator also covenants not to
      assert against You any claim or cause of action arising from or relating
      to a use of the Work that this Dedication permits. ACD-1.1's release
      was cut at rights and not at claims: of the five elements CC0's waiver
      lists, it lacked "associated claims and causes of action" (register
      entry 272 in LICENSES/ACD-1.0.against.md).
    * Section 8.2 no longer says only that the absence of a patent retaliation
      provision is deliberate; it gives the reason -- a retaliation provision
      is a condition on permission already given, and Section 10.1 admits no
      condition -- so that the absence reads as following from the structure
      rather than as a preference.
    * Section 11.4's second sentence ("It reaches nothing else") now says that
      the covenants in Section 5 are not limited by it. Without that, the
      sentence contradicted the second limb of Section 5.1 and Section 5.2(d),
      which reach beyond Covered Rights, patent claims and Moral Rights.
    * Section 8.6 no longer says that nothing in it depends on whether a
      licence is effective; its covenant applies only where a licence is held
      ineffective, so that sentence contradicted the one before it. It now says
      that the licence governs where it is effective and the covenant where it
      is not.
    * The recommended notice in Section 16.1 names personality rights as well,
      which the bullet above on errata E29 said it named and it did not.
    * Section 5.2(b) no longer ends with "or"; the word was left behind when
      item (d) was added.
    * ACD-1.1: 5051 words, 78 clauses. This draft: 5427 words, 80 clauses.

  Still open in this draft: E6 (whether Section 8.4 needs to reach outputs as
      well as the use of the Work -- examined and deliberately not narrowed)
      and E10 (the machine-readable descriptor; closed for 1.1 in
      ACD-1.1.machine.json, and it must be closed again for each new version
      because each version carries its own descriptor).
```

---
file: LICENSES/ACD-1.1-SELF-AUDIT.md
audience: a future drafter (the current draft is 1.4), OSI license-review participants, licence reviewers
last-updated: 2026-11-27
canonical-ref: LICENSES/ACD-1.5-DRAFT.txt (the current draft; ACD-1.2.txt frozen 2026-10-17, ACD-1.3.txt frozen 2026-10-25, ACD-1.4.txt frozen 2026-11-23 and applied to this repository) / LICENSES/ACD-1.1.txt (frozen 2026-09-17) / LICENSES/ACD-1.5-CHANGELIST.md (all other changes for the current draft; ACD-1.1〜1.4-CHANGELIST.md are the closed records for those versions) / LICENSES/ACD-1.0.errata.md (defects in 1.0)
---

# 草案を我々自身が掃引して出たもの

**`ACD-1.1-CHANGELIST.md` から 2026-09-17 に切り出した**（917 行で advisory を鳴らしたため・
**節番号は動かしていない**ので既存の `§3e` / `§3f` 参照はここへ解決する）。

**この file と CHANGELIST の境界**: CHANGELIST は「1.0 の errata と、外から来た材料を当てた結果」。
**ここは「我々が我々の草案へレンズを当てて出たもの」** ——**草案が自分で持ち込んだ欠陥**（§3e）と、
**既に直したはずの形を、直していない条の集合へ当て直した結果**（§3f）。

## 移転先: §3e / §3f / §3g / §3h / §3i / §3j / §3k / §3l / §3m / §3k-2 は `ACD-1.1-SELF-AUDIT-2.md` へ移した（2026-11-27・本文は無改変）

2026-09-17〜09-22 に足した 10 節（1.1 と 1.2 の草案の掃引）を、行数の advisory（Check 52）のため別の file へ移した。節番号は動かしていないので、
他の文書の `ACD-1.1-SELF-AUDIT.md` §3e〜§3m の参照はこの見出しを経て `ACD-1.1-SELF-AUDIT-2.md` の同じ番号の節へ辿る。新しい節はこの file（§3n 以降）へ足す。


## 3n. 凍結された 1.1 の冒頭が、自分の条番号について誤りを述べている（2026-09-24）

**§3k-2 は「変更の宣言 ↔ 実 diff」を当てた。番号についての宣言は当てていなかった。**
`ACD-1.1.txt` の冒頭（区切り線より前・非 operative）は *"Clause numbers here do NOT correspond
to 1.0 after Section 15"* と述べる。**§1 でもずれている** ——E13 を閉じるために定義を並べ替えた
ためで、定義語で対応を取ると **1.0 §1.2 Work → 1.1 §1.3 / §1.3 Dedicator → §1.4 /
§1.4 You → §1.6 / §1.6 Moral Rights → §1.2**（§1.5 Covered Rights だけ同じ番号）。

**害**: この文を信じて「§15 までは同じ番号」と読んだ読者は、1.1 の「§1.4 You」を引いて
Dedicator に着く。**定義は他の全条が依拠する場所で、ずれの位置として最も悪い。**
しかもこの文は `REVIEWERS.md` と `QUESTION-INDEX.md` に**そのまま複製されていた**
（2026-09-24 にその 2 面は直した。`REVIEWERS.md` は同じページの上の節で §1 のずれを
正しく述べており、**1 ページの中で自分と矛盾していた**）。

**直せるか**: **1.1 は凍結中なので直せない**（Check 453 が sha256 で pin）。
**1.2 草案の冒頭**は *"Clause numbers follow ACD-1.1, not ACD-1.0"* と述べるだけで、
ずれの範囲を主張していないので**同じ誤りを持たない**。**1.1 の冒頭は、次版で置き換わるまで
誤ったまま読まれる** ——対処は、それを引く面の側で範囲を正しく書くことだけである。

**同じ根の誤りがもう 1 つ在った**: `ACD-1.1-CHANGELIST.md` §0.5 の条番号対応表は
2026-09-10 の草案から生成されたもので、確定した 1.1 と 3 行合っていなかった
（Work → 1.5 と書いたが 1.3 / Covered Rights → 1.3 と書いたが 1.5 / 1.0 §16.5 を「削除」、
§16.6 を「→ 16.5」と書いたが、1.1 §16.5 は Steward の定義で §16.6 は §16.6 のまま）。
**同日に直した。** **生成した表は、生成した日の本文についての表である** ——
凍結の前に本文が動いたら、表は生成し直すか、生成日の版を名乗らなければならない。

## 3o. 1.4 草案が自分で持ち込んだ欠陥 —— 語を足した行が折り返されていなかった（2026-11-01）

**3 人体制の内部チェック（提出面の担当）で発見した。** 1.4 草案は §4.2 に *"study, inspect, analyse,
reverse engineer"* を足したが（OSAID 1.0 の照合・2026-10-28）、**語を足した行が 119 桁のまま折り返されていなかった**。
1.0 の本文は全行 80 桁以内で、審査者は申請時に plain text の添付として読む。**語の変更は CHANGELIST と
草案冒頭の一覧で 2 重に記録されていたが、行の形を見る層はどこにも無かった** —— Check 468 は語数・条数・
相互参照・身分表示を照合するが、行幅は見ていなかった。

**同じ掃引で、草案が持ち込んだのではない（凍結版から引き継いだ）崩れも 3 件出た**: §8.4 と §2.5 の 81 桁の行、
§11.4 の途中で 52 桁で切れた行（1.2 で文を足したときの名残）、§16.1 の notice 雛形で *"(Section 11)."* が
次行頭に落ちていた改行（E29 で語を足したときの名残）。**いずれも語を足した増分の後に残った形で、
語の列は正しく行の形だけが崩れている** —— 語を数える検査はどれも緑のまま通る。

**直したもの**: 4 件とも、語の列が同一であることを機械的に確かめてから折り返しだけを直した
（`ACD-1.4-CHANGELIST.md` の「行の折り返し」注記）。§16.4 は折り返しの違いを改変としないので、
版の同一性には触れない。**再発防止**: 5a が Check 468l（草案の本文行は全行 80 桁以内）を BLOCKING で足した。
**凍結済みの 1.2・1.3 は直せない** —— §11.4 の 52 桁の行と §16.1 の改行は、両版に残ったまま読まれる。


## 3p. 1.1 が直したときに持ち込んだ欠陥 2 件 —— 外から当てられて初めて見えた（2026-11-01）

オーナー経由で届いた外部 AI の敵対的レビュー（`ACD-1.4-CHANGELIST.md` の 2026-11-01 節）を条文に当てたら、
**1.0 には無く、1.1 で別の欠陥を直したときに入った**欠陥が 2 件あった。どちらも 1.1・1.2・1.3 の凍結版に残る。

- **§16.4 の Steward 例外（E14 を直したとき）**: 1.0 の §16.4 は識別子を `ACD-1.0` だけ守っていた（E14）。
  1.1 は射程を `ACD-N` / `ACD-N.N` へ広げ、同時に次版を出せるよう *"except by the Steward"* を足した。
  **例外に「新しい版番号の下で」という限定が無く、同じ文が述べる目的（各識別子が 1 つの固定テキストを指す）と
  食い違った** —— Steward が同じ識別子の下で別の本文を出すことを止める語が無い。
- **§2.4 と §8.6（E18 を直したとき）**: 1.0 の §2.4 は §3〜§6 だけを独立と述べていた（E18）。1.1 は
  *"as is every other grant, permission, and covenant"* と全体へ広げ、*"none is conditioned … on another's failure"* を
  全条に掛けた。**ところが §8.6 は 1.0 から「許諾が無効と判断されたとき」に働く形で、宣言の側だけが広がった。**
  §8.6 の空白（約束はその判断を生む最初の主張の時点ではまだ無い）自体は 1.0 からの欠陥である。

**一般形**: **宣言の射程を広げる修正は、広げた先の各条がその宣言を満たすかを当てないと、新しい食い違いを作る。**
E14 も E18 も「宣言が一部しか覆っていない」欠陥で、直す向きは正しかった。欠けていたのは、広げた宣言を
各条へ逆向きに当てる一手である。**1.4 草案で 2 件とも直した**（§16.4 の例外を限定・§8.6 を無条件の約束へ）。
**⚠ 逆側**: 2 件とも 1.1 の確定前の自己監査（§3k-2 の自己記述照合を含む）を通っている —— 照合したのは
「草案が自分の変更について述べること ↔ 実 diff」で、「変更した宣言 ↔ 宣言が及ぶ他の条」ではなかった。

**同日追記 —— 172 観点の本体を当てると、同じ形がもう 2 件出た**（`ACD-1.4-ADVERSARIAL-TRIAGE.md` の B-12 / H-17。報告書の B12 は register の B12 とは別物）:
- **§2.6（E16 を直したとき）**: 1.1 が足した識別の約束は「寄稿でないと標示された素材」だけを名指し、§1.9 のもう 1 つの除外経路
  （*"material sent for discussion only"*）を落としていた。**E16 の記録自体が「2 つある除外経路の 1 つしか塞いでいない」と書き、
  直したあとも数え直していなかった** —— 経路は 3 つ（述べた / 標示した / 議論のためだけ）あった。
- **§16.4（E14 を直したとき）**: 射程を `ACD-N` / `ACD-N.N` へ広げたが、`ACD-1.4.1` のような 3 段の版番号が外れた。
**どちらも 1.4 草案で閉じた。** 一般形は上と同じで、**直す対象を列挙し直さずに、見えている形だけを塞いだ。**

**同日追記 2 —— 本文 §8.4 が自分で誤った理由を述べていた（1.1 の E15 で入った）**: 1.1 は §8.4 に因果の限定を入れたとき、
閾値を置かない理由として *"such a threshold would be a condition and Section 10.1 permits none"* と書いた。**同じ文の因果の限定が
射程の限定であって条件ではないことを、その文自身が示している。** 172 観点の E-02 でこの理由づけの誤りを CHANGELIST 側で訂正した
同じ日に、本文の同じ文は当てずに残していた —— §10.1 を全条へ逆向きに当てる掃引で見つかった。1.4 草案で直した（0 語）。
**一般形の 3 つ目**: 記録の側を直したら、**その記録が説明している本文の文**にも同じ誤りが無いかを当てる。

**2026-11-02 追記 3 —— 同じ §8.4 の同じ修正が綴りも持ち込んでいた**: 1.1 が足した文 *"it does not licence a claim"* は動詞に
名詞形 *licence* を使っている（英国式は名詞 *licence*・動詞 *license*。§10.2 は動詞を *"license anything"* と書き（*"to license"* と書くのは §6.4 の *"requires You to license"*。2026-11-02 訂正: 旧文は *"to license"* を §10.2 の逐語として引いていた）、1.0 に名詞形の動詞は無い）。
意味は変わらないが、綴りを区別する英国式で書いた本文が 1 箇所だけ区別していない。1.1〜1.3 は凍結のまま、1.4 草案で直した（0 語）。
**見つけ方**: 1.0〜1.4 の全版で *licen[cs]e* の語形を前の語ごとに数え、版の間で増えた形を見た —— 本文が新しく書いた文だけを見る差分の
レンズでは、綴りは意味の変化として現れないので拾えない。

## 3q. 1.4 草案が自分で持ち込んだ欠陥 —— 全体を拘束した §2.8 が、§5.3 / §12.4 と重なって食い違っていた（2026-11-02）

**25 の掃引で発見した。** 1.4 は §2.8 の列挙（*"Sections 3, 4, 6, and 8"*）をやめ *"This Dedication, in respect of the Work, binds"* にした（errata E46 / E49）。
その結果、§5 の covenant と §12.2 の covenant は **§2.8 と §5.3 / §12.4 の両方**に拘束されるようになった。2 つは人の列挙（譲受人を名指すのは §2.8 だけ）と限定句
（*"to the fullest extent the law permits"* 対 *"… permits the Dedicator to bind them"*）が違うので、**より特定的な §5.3 / §12.4 が covenant について支配すると読めば、
§2.8 が足した譲受人への拘束が covenant についてだけ引き戻される**。書き換えの当日、変更記録の逆側は「§5.3・§12.4 は重複になるが残す」と書いて閉じていた ——
**重複と見たものは、文言が同じでないかぎり食い違いである**。

**直したもの**: §2.8 の末尾に *"Neither of those Sections narrows this one."*（+7 語）。（採った日の文。2026-11-04 に §2.8 と §12.4 の理由の文を対で外したとき、いまの *"Neither Section 5.3 nor Section 12.4 narrows this Section."* になった。）限定句は揃えていない（揃えると §2.8 が狭まる・理由は `ACD-1.4-CHANGELIST.md` の §2.8（3 回目）行）。

**見つけ方**: 弁護士への質問集の引用を本文に大小区別ありで照合していたとき、並ぶ 3 条（§2.8 / §5.3 / §12.4）の限定句を語ごとに見比べた。
**一般形: 列挙を「全体」に置き換えると、全体の中にある個別の同種規定と対象が重なる。置き換えた日に、重なった規定の文言が同じかを確かめる。**

## 3r. 1.1 が持ち込んだ欠陥 —— §16.4 に足した re-encoding の但し書きが、隣の翻訳の但し書きと違って「使用への条件ではない」と断っていなかった（2026-11-02）

**25 の掃引で発見した。** 1.1 は §16.4 に *"A re-encoding of the text into a machine-readable form is likewise not a modified text for this purpose, provided the words
are unchanged and the form is identified as a re-encoding"* を足した（2026-09-14・commit fa740f1b・外部レビューが §16.4 について挙げた点のうち、本文に欠けていた 1 点への対処）。直前の翻訳の但し書きは
1.0 から *"that proviso is a condition upon distributing the translated text, not upon any use of the Work (Section 10.5)"* と自分で断っていたが、**足した但し書きには同じ断りを付けなかった**。
並ぶ 2 つの但し書きで片方だけが断ると、断らない側は Work の使用への条件と読まれうる。**これは E9（against #57）—— 条件なしの網の目で、隣が限定されているのに 1 文だけ限定が無い —— と同じ形で、
その E9 を直した版（1.1）が、同じ網の目に限定の無い文を 1 つ足していた。** §10.5（§16 は Work の使用への条件ではない）と §16.6 が §16 全体について同じことを述べるので、実害の読みは弱い。

**直したもの**: 1.4 草案で翻訳側の個別の断りを外し、末尾に *"Both provisos are conditions upon distributing the text, not upon any use of the Work (Section 10.5)."* を置いた（−2 語）。
1.1〜1.3 は凍結のまま残る。

**見つけ方**: §10.1 と食い違う言い回し（must / shall / required / provided / only if / unless / subject to）を本文全体から機械的に洗い、You に向いた候補を 1 件ずつ当てた。
**一般形: 網の目に文を足すときは、隣の文が持つ限定を足す文にも付けたかを、足した日に確かめる**（E9 の教訓を、E9 を直した側が自分の追加に当てていなかった）。


## 3s. 1.2 が持ち込んだ欠陥 —— E31 が足した §5.2(d) が、隣の §5.1・§8.6 と違って第三者を通じた主張を塞いでいなかった（2026-11-03）

**25 の掃引で発見した。** 1.2 は E31（Dedicator 自身の privacy / publicity / personality 権）を閉じるために §5.2 へ
*"(d) assert against You a right of privacy, publicity, or personality held by the Dedicator, in respect of any use of the Work that this Dedication permits"*
を足した（1.2 草案・2026-09-23）。同じ働きの約束である §5.1（Covered Rights）と §8.6（特許）は
*"not to assert, and not to authorise or assist any other person to assert"* と書き、第三者を通じた行使まで塞ぐが、**(d) は Dedicator 自身の主張しか止めていなかった**。
(d) が対象とする publicity 権は米国の多くの州で譲渡も独占的なライセンスもでき、§5.3 は譲受人（assigns）を拘束するが**ライセンスを受けただけの者は拘束しない** ——
Dedicator が自分では主張せず、独占的なライセンスを受けた代理人に主張させる経路が残っていた。1.2・1.3 は同じ文言で、1.0・1.1 には (d) 自体が無い。
**errata ではない**: 欠陥のある文は 1.0 に無く、`ACD-1.0.errata.md` の冒頭は「全件 1.0 で未修正」と述べる（25 は最初 errata 候補として渡し、同日に取り下げた）。

**直したもの**: 1.4 草案で *"(d) assert, or authorise or assist any other person to assert, against You …"*（+9 語）。（採った日の文。2026-11-08 の T39 で除外を (d) の冒頭へ移し、いまは *"(d) other than for a false statement or representation (Section 11.3), assert, …"* である。）§12.2 には足さなかった理由と逆側
（「authorise しない」は将来に向けた約束で、以前に与えた独占的ライセンスの取消までは約束しない —— §5.1 にも同じ限界がある）は `ACD-1.4-CHANGELIST.md` の「§5.2(d)（authorise or assist）」行にある。1.2・1.3 は凍結のまま残る。

**見つけ方**: 並ぶ条の非対称のレンズ（同じ働きの約束が同じ射程を持つか）を covenant の言い回しに当てた。
**一般形: errata を閉じるために足した文は、隣に並ぶ同じ働きの文の言い回しを写していたかを、足した日に確かめる**
（§3r と同じ形 —— 欠陥を直した版が、直すために足した文で隣との不揃いを作っていた）。

## 3t. 1.1 が持ち込んだ欠陥 —— §8.4 の因果の限定は 2 通り以上に読め、§6.1 は §8.4 が与えない許可を述べていた（2026-11-04）

**B10 の立証を当て直す過程で見つけた**（25・bb・5a。きっかけはオーナーが渡した別の AI の見解で、オーナーの指示ではない）。**3 点とも 1.1 が入れた文で 1.0 には無いので、errata ではなくここへ記録する。** 1.1〜1.3 は凍結のまま未修正。

**(1) §8.4 の因果の限定の読みが割れている。** 1.1 は E15（極少量の混入で広い特許許諾を引き出す読み）を閉じるために、*"reaches only claims whose infringement depends upon the use of the Work"* と、Work を使わず作ったものを外す文を足した。**請求項の単位で読むと**、モデルの構造や性質を読む請求項は Work を使わないモデルでも侵害されるので外れ、§8.4 が取り除くと述べる露出が残る。**場面の単位で読むと**、Work を混ぜるだけで無関係な請求項が許諾され、E15 の害が戻る。記録も割れていた（E15 の commit は請求項の単位・1.1 CHANGELIST は物の単位・想定問答は 1 件目と 4 件目で別の答え）。§15.1 は広い側へ解決するので、**gap の柱が解釈規則に預けられ、しかも解決先は E15 が閉じた読みである。**

**(2) §6.1 は §8.4 が与えない許可を述べていた。** E19 が足した *"so far as the Covered Rights and patent claims of the Dedicator are concerned"* は、Dedicator のどの特許請求項についても Computational Use を許すと読める。§6.5 は §6 が言い直しだと述べるが、§8.4 は無関係な請求項を外すので、§6.1 の射程は §8.4 より広い。

**(3) その超過は成果物の行為まで及ぶ。** §1.7 の Computational Use は *"the making, distribution, and use of any model … resulting from that processing"* を含むので、§6.1 の許可は学習の行為だけでなくモデルの販売にも掛かる。

**なぜ長く残ったか**: Check は条の参照が解決するかを見るが、条と条の射程が揃っているかは見ない。§8.4 の文はドシエが 3 通りに説明していて、どの説明も 1.1 以降の本文に裏づけられていなかった。**E15 を「閉じた」と記録したまま、閉じ方が別の欠陥を残していた**（§3p と同じ形）。

**1.4 での扱い**: `ACD-1.4-CHANGELIST.md` に記録する（試作は `ACD-1.4-CLARITY-TRIAL.md` の T4）。法的効果が変わるので、1.3 を適用した著作物の受領者の位置は変わらない。

## 3u. 1.1 が閉じたときに足した語 2 件 —— §2.6 の *"included in the Work"* と §16.3 の *"in which they hold rights"*（2026-11-04）

**どちらも 1.1 が別の欠陥を閉じるために足した語で 1.0 に無いので、errata ではなくここへ記録する。** 25 のレンズ（§15.1 の向き・並行起草の差分）と bb の反例で見つかった。1.1〜1.3 は凍結のまま未修正。

**(1) §2.6（E16 が足した）**: *"that material is included in the Work"* は、Work が Dedication の覆わない素材を含むことを前提にしていた。これは E61 の読み（一部に適用すれば素材全体が Work）を支える材料で、定義の 5 語と組むと読みが強くなる。1.4 草案は *"included with the Work"* へ直した（採った日の文。2026-11-08 の T37 で主語を組み替え、いまは *"a Dedicator who includes that material with the Work, or causes it to be included"* である）。

**(2) §16.3（E2 が足した）**: *"in which they hold rights"* は適用する者に権利の確定を求める形で、§9.2 が権利の存否を述べないことと食い違う。AI が生成したコードの持ち主は権利が在るか分からず、gap の 3 つ目の採用者そのものである。1.4 草案は *"hold or may hold rights of their own"* へ直した。**最初の案 *"hold or may hold rights"* は不成立だった** —— *may hold* は可能性の語で、E2 が閉じた害（他人の著作物に notice を付ける誘い）が戻る。

**一般形**: E60 と同じである。**絞るための文に可能性の語を入れると絞りが緩む。** 欠陥を閉じる語は、閉じた当時に見えていた読みしか見ていない（§3p）。

## 3v. 直した条が作った入口の穴と、1.1 が足した括弧 —— §16.1 の適用の行為と §6.4 の *"(Section 9)"*（2026-11-06）

**どちらも 1.0 に無いので errata ではなくここへ記録する。** 25 のレンズ（修正の入口・指す先の主題）で見つかり、bb が反例を当てた。経緯は `ACD-1.4-SECOND-CLARITY-TRIAL.md` §10。

**(1) §16.1 / §16.2（1.4 草案が H-02 で持ち込んだ）**: 1.3 の §16.2 は *"Where a work is accompanied by …"* で、タグだけでも条件全体が及ぶと読めた。H-02 はこれを「Dedicator が適用した著作物」へ限定し、第三者が勝手に付けたタグでは成立しないようにした。だが適用の行為を述べる条は §16.1 しかなく、§16.1 は長い通知文の形だけを挙げるので、ファイルの先頭にタグだけを置く権利者（SPDX の通常の使い方）について、適用したと言えるかが条文から決まらなくなった。§15.1 は適用のあとで働くので救えない。1.4 草案は *"in a form Section 16.2 names or in substantially the following form"* へ直した（+7 語）。**⚠ 逆側**: タグは道具が既定で残すので、改変したファイルに残ったタグが「適用」と読まれる余地が増えた（`FAQ.md` A33）。1 語のタグが §3 の放棄の意思として足りるかは問 1 の (e) に置いた。足りなくても §4.4 が受け止める。

**(2) §6.4（1.1 が E4 を閉じたときに足した）**: *"(Section 9)"* の指す先は Work の部分を論じていて、§6.4 の *"any such thing"*（モデル・パラメータ・重み・埋め込み・出力）は Work の部分ではない。読者は自分の問いに答えない条へ案内され、§9.2 の *"apply to it in full"* が出力の権利に及ぶという誤読の足場にもなっていた。1.4 草案で外した（−2 語）。§9.2 の第 3 文そのものも、1.4 草案の T34 で *"this Dedication applies to it"* へ替わった（2026-11-08・`ACD-1.4-SECOND-CLARITY-TRIAL.md` §14.15）。1.1〜1.3 は凍結のまま未修正。

**一般形**: **直した条は、直した問いとは別の問いの入口になる。** H-02 は「誰が適用できるか」を閉じて「何が適用か」を開いた。修正を入れたら、その条が前提にしている別の条の行為まで読み直す。

## 3w. 1.4 草案が足した語の付き先 2 件 —— §16.4 の *"except a draft"* と §11.4 の *"other than the Dedicator"*（2026-11-06）

**どちらも 1.4 草案で足した語で、凍結版に無いので errata ではなくここへ記録する。** 25 が語の付き先を読み、bb が反例を当てた（`ACD-1.4-SECOND-CLARITY-TRIAL.md`）。

**(1) §16.4**: *"that no earlier text has borne, except a draft identified as such,"* は読点のあとの *except* が文の冒頭の *"except by the Steward"* と並び、禁止全体への例外に読めた。誰でも「草案」と書けば名前の下で改変本文を出せる読みで、§15.1 は E20 により解決しない。*"that no earlier text, other than a draft identified as such, has borne"* へ直した（+1 語）。**⚠ 残る小さな穴（直さない）**: *"no earlier text"* は Steward の本文に限らないので、第三者が違反して次の番号を名乗ると、Steward はその番号を使えない読みが立つ。害は番号を 1 つ飛ばすことだけである。

**(2) §11.4（E43 が足した）**: *"personal data, or the likeness, voice, or performance of a person other than the Dedicator"* は限定が *personal data* に掛からないと読めた。*"the personal data, likeness, voice, or performance of a person other than the Dedicator"* へ直した（−1 語）。Dedicator 自身の personal data は前の文の *"It grants no permission under the law of data protection"* が覆うので、許諾は増えない。

**一般形**: **語を足す修正は、足した語がどこまで掛かるかを別に読む。** 足した本人は意図した付き先で読むので、付き先の誤りは足した時点では見えない。

## 3x. §8.4 の限定を別の条が素通りしていた —— §5.1 / §8.3 / §8.6 と、方法の請求項（2026-11-06）

**オーナーが渡した別の AI の見解を材料に、25 が敵対的に読み、bb が反例を当てた**（`ACD-1.4-SECOND-CLARITY-TRIAL.md` §13）。どの欠陥も 1.0 の本文には無い。1.0 の §8.4 に限定が無く、素通りする相手が無かったからである。1.1〜1.3 は凍結のまま未修正。

| 条 | 持ち込んだ版 | 読み | 1.4 草案 |
|---|---|---|---|
| §5.1 第 2 肢 | 1.2（#272）| *"any claim or cause of action … relating to a use of the Work that this Dedication permits"* は特許の請求にも当たり、§15.1 の読みでは K3〜K5 の請求項が §8.4 の限定を丸ごと素通りする。1.2 で足したとき検討したのは商標だけだった | *"other than for patent infringement (Section 8)"* を足した（+7 語）|
| §5.1 第 2 肢（対価）| 1.2（#272）| 同じ語は、ACD を適用した会社の有償サポートの代金請求も「許された利用に関する請求」にする。`faq.md` A30 は対価を取れると答えていて、§15.1 の広い読みと食い違う | *"or for a payment You agreed to make"* を例外に足した（+8 語・`ACD-1.4-SECOND-CLARITY-TRIAL.md` §13.6）。*"or relating to"* を外す案は bb の反例で落ちた |
| §8.3 第 1 文 | 文は 1.0 から、衝突は 1.1 の限定から | *"any patent right of the Dedicator in respect of the Work"* に限定が無く、§8.4 の限定の外に残る請求項が *"leaves unaffected"* に当たる。第 3 文と §15.1 が組むと K3〜K5 が戻る | *"any patent claim that Sections 8.1 and 8.4 reach"*（−2 語）。採った日の文で、2026-11-08 に *reach* を §8.3 で 1 回定める形へ組み替え、いまは *"Nothing in this Dedication reserves, preserves, or leaves unaffected any patent claim they reach."* である |
| §8.4 の限定 | 1.4 草案の T4 | 方法の請求項では工程が Work の処理そのものなので、*"from the use of the Work"* が同語反復に読め、K4 が戻る | *use* を *content* へ（0 語）|
| §8.6 第 1 文 | 1.1 の限定から | *"the patent claims described in Sections 8.1 and 8.4"* が第 1 文だけを指すと読むと、約束が許諾より広くなる | *"the patent claims that Sections 8.1 and 8.4 reach"*（§11.4 も同じ語へ）|
| §5.1 第 2 肢（商標と表示）| 1.2（#272）| 2026-11-07 の本文だけの読み。除外を名指しすると名指しされない商標は不行使に入ると読め、1.3 の点検の根拠（§11.3 の行為は *permits* に入らない）は §5.2(d) が同じ語を §11.4 の与えない権利に使っているので閉じない。*relating to* は負傷や中傷の請求まで入る | *"for a use …"* へ改め、*"under trademark rights or rights in a name (Section 11.1)"* と *"for a representation Section 11.3 describes"* を除外に足し、§5.2(d) にも足した（+19 語・`ACD-1.4-SECOND-CLARITY-TRIAL.md` §14.1）。採った日の文で、2026-11-08 に後者を *"for a false statement or representation (Section 11.3)"* へ改めた。いまの §5.2(d) が持つ除外はこの 1 つだけである |

**効果**: 受領者は K3〜K5 を別の条から取り戻せなくなり、特許権者の費用は §8.4 の限定の内へ戻った。K1・K2 の受領者の地位は変わらない。本文の語は 1.0 の方向へ広がったのではなく、1.1 が意図した範囲へ揃った。

**一般形**: **限定を足したら、同じ対象へ届く一般語を本文全部で探す。** 1.1 が §8.4 へ限定を足したとき、§8.3 の全称は見なかった。1.2 が §5.1 へ請求権の語を足したとき、§8.4 の限定は見なかった。2026-11-06 の掃引で、特許の請求へ届く語はこの 2 か所だけだった。



## 3y. 逐条リファレンスの行を本文に当てた読みで出た、1.1 が持ち込んだ欠陥 2 件（2026-11-08）

`ACD-1.4-SECOND-CLARITY-TRIAL.md` §14.18 の読み（逐条リファレンスの行が述べる読みを、本文の語だけから敵対的な読み手が取るか）で残った 10 件のうち、1.0 の本文に無く 1.1 で入った文は 2 件だった。1.1〜1.3 は凍結のまま未修正。

| 条 | 持ち込んだ版 | 読み | 1.4 草案 |
|---|---|---|---|
| §2.6 第 2 文（識別の約束） | 1.1 | *"and that material is included in the Work, the Dedicator will identify it"*（1.4 草案では *with the Work*）は受動で、誰が含めても、もう関わっていない Dedicator も含めて全員に約束を負わせる | *"a Dedicator who includes that material with the Work, or causes it to be included, will identify it"*（+5 語・T37）|
| §16.5（Steward） | 1.1 | *"and any person or entity to whom that role is assigned"* は累積で、譲渡したあとも最初の公表者が Steward のまま残る | *"or, after an assignment, the person or entity to whom that role was last assigned by"*（+4 語・T45）|

## 3z. 1.4 草案の修正が代名詞の先行詞を変えた 2 件 —— §8.6 の *"alongside them"* と §5.2 末文の *it*（2026-11-12）

**1.0〜1.3 にこの文は無いので、errata ではなくここへ記録する。** 11-06 以後に変わった 17 条の相互参照 47 件を読み直したときに 25 が見つけ、bb が反例を当て、5a が測った（`ACD-1.4-SECOND-CLARITY-TRIAL.md` §14.31）。

| 修正 | 日付 | §8.6 第 2 文 |
|---|---|---|
| E42（約束を全法域で働く形へ）| 2026-11-01（`fece2e27`）| *"…on the same footing as the covenant in Section 5 and does not wait for either licence to be held ineffective: it operates in every jurisdiction alongside them."* —— 直前は単数の *covenant* で、*them* は 2 つの許諾しか指せない |
| E71（§5 を複数形で呼ぶ）| 2026-11-08（`28dc458e`）| *covenant* → *covenants*。*them* の直前に複数の名詞が来て、「§5 の約束と並んで」とも読めるようになった |
| T56 | 2026-11-12 | *"alongside them"* を外した（−2 語）|

**読み**: 記録はどれも *them* を許諾と読んでいた。そう読むと「許諾が在る限りで並んで働く」と読む余地が生じ、許諾が無効と判断された法域でも残るという条の役目に逆らう（bb）。並んで働くことは *"does not wait"* と §2.4 第 2 文（*"none is conditioned on another being effective or on another's failure"*）が持つ。

**一般形**: **単独では正しい修正が 2 つ組になると、片方の語が他方の代名詞の先行詞を変える。** E71 は語を 1 つ複数にしただけで、0 語の修正だった。語数が 0 でも、隣の文の代名詞は読み直す。修正どうしを読み合わせる読み（§14.14・§14.22）は、変わった文の次の文まで含めて読む。

**2 件目（T60）—— 文を合流させたときに名指しを代名詞へ。**
**1.0〜1.3 にこの文は無いので、errata ではなくここへ記録する。** 長い作用の文を読み直したときに 25 が見つけ、bb が反例を当てた（`ACD-1.4-SECOND-CLARITY-TRIAL.md` §14.33）。

T48（2026-11-09）は、*"Paragraphs (a) and (b) do not reach a service through which **the Dedicator** runs the Work for others without providing a copy of it."* を、主語が *Section 5* の末文へ合流させ、*the Dedicator* を *it* にした。末文には E67 を閉じたとき（11-08）から *"the terms or measures it applies"* があった。合流の後、主語から遠い 65 語の文に *it* が 3 つ並び、文法の既定では主語の *Section 5* を指す。*a copy of it* は *a service* とも読め、そう読むと除外は意図より広がる。T60 で *the Dedicator* と *the Work* に名指しした（+3 語）。

**一般形**: **2 つの文を 1 つに合流させると、合流先の主語が代名詞の既定の先行詞になる。** 合流させた文の名詞を代名詞に縮めるときは、合流先の主語との取り違えを読む。§3z（修正の組が先行詞を変える）と同じ族で、こちらは 1 つの修正の中で起きた。

## 3za. 1.4 草案の修正が別の条の語の読みを変えた —— §5.2(a) の *apply* と §2.2 の *restriction*（2026-11-15）

**1.0〜1.3 では食い違いが無いので、errata ではなくここへ記録する。** T64 を §2.2 と読み合わせたときに portfolio-1c が見つけ、portfolio-50 と portfolio-30 が反例を当てた（`ACD-1.4-SECOND-CLARITY-TRIAL.md` §14.37）。

| 修正 | 日付 | 効果 |
|---|---|---|
| T64（errata E82）| 2026-11-15 | §5.2(a) から *"apply, or"* を外し、Dedicator が技術的な手段を掛けることを許した（GPL-3.0 §3 型）|
| —— | —— | §2.2 *"in respect of any copy of the Work that has been made available, may not impose any further term, condition, or restriction"* の *restriction* を法的と読む支え（技術的な手段は (a) が別に禁じている）が消え、技術的と読むと、既に配っているサーバに後から負荷対策を足すことを §2.2 が閉じ直す |
| T65 | 2026-11-15 | *"may not impose any further term, condition, or restriction on what may be done with any copy of the Work that has been made available"*（+3 語）|

**読み**: 最初の案 *legal restriction* と 50 の代案 *enforceable restriction* は、技術的な後付けの制限をまとめて §2.2 の外に出すので、Work に入れた phone-home で後から写しを止める形（30 の反例）を止める語が本文から消える。制限を「何に」掛けるかで切ると、窓口の負荷対策は外、遠隔停止は内に分かれる。

**一般形**: **ある条から禁止を外すと、その禁止が別の条の語を狭く読む支えになっていた場合、別の条の語が広がる。** 外した禁止は、自分の条で何を許すかだけでなく、隣の条の語を何と読ませていたかも運んでいた。禁止を外す修正は、同じ対象（ここでは技術的な手段）を語で述べる他の条を全部読み直す。§3z（修正が代名詞の先行詞を変える）と同じく「単独では正しい修正が他の条の読みを変える」族で、こちらは語の意味の支えが消える型である。

## 3zb. 重なる条の組を、組ごとに射程・相手・限定の語で比べた（`against.md` #280 の方法・2026-11-15）

**なぜ**: #280 は、2026-11-01 の監査で見つかった 3 組の食い違いが別々のレンズで偶然に見つかったことを記録し、確定の前の読みで「重なる組を列挙して組ごとに比べる」ことを求めていた。T64・T65 で §5.2 と §2.2 が動いたので、その日の草案で 1 回やった。portfolio-30 が読み、比べたのは各組の **射程**（何に及ぶか）・**相手**（誰が依拠できるか）・**限定**（法が許す限り等）・**承継**（誰を縛るか）・**終了**の 5 つである。

| 組 | 射程 | 相手 | 限定・承継・終了 | 結果 |
|---|---|---|---|---|
| §3 / §4 / §5（著作権の 3 つの足場） | §3.1 *"all Covered Rights in the Work"*・§4.1 同じ・§5.1 *"any Covered Right … in respect of any use of the Work"* | §3 は相手を持たない・§4 は You・§5 は You と下流（§5.3） | §3.1 *"to the fullest extent permitted by the law of each jurisdiction"*・§4 は限定なし（§4.4 で独立）・§5.3 は承継と依拠をそれぞれ法の限りで。承継は §2.8 が全体に | **食い違い 0** —— 差はそれぞれの足場の性格（放棄・許諾・約束）から来る |
| §8.1 / §8.4 / §8.6（特許） | §8.6 は *"the patent claims that Sections 8.1 and 8.4 reach, in respect of any act that those Sections describe"* と参照で揃う | §8.1・§8.4 は You・§8.6 は *"against You"* | 終了しないことは §8.2 が許諾 2 つについて述べ、約束（§8.6）は §8.2 第 2 文（報復条項を持たない）と §2.2（撤回不能）に頼る。承継は §2.8 | **候補 1**（下の (1)） |
| §12.1 / §12.2（人格権） | どちらも *"Moral Rights in the Work"* | §12.1 は相手を名指さない・§12.2 は *"against You or against any person who receives the Work from You"* | 承継は §12.4（死後の行使者まで）・§2.8 は §12.4 を狭めない | **候補 1 の対象に入れたが、T66 では外した**（下の (1)） |
| §11.4 / §5.2(d) / §16（届かないもの・人格権・文書） | §11.4 は到達の文、§5.2(d) は Dedicator 自身の行為の約束、§16 は文書としての本文 | —— | §11.4 第 2 文が *"the covenants in Section 5 are promises about the Dedicator's own conduct and are not limited by this sentence"* と明示 | **食い違い 0**（**2026-11-24 追記（1.5・T135）**: この行が引く §11.4 第 2 文は、1.5 草案で *"It gives nothing by implication beyond what its words give."* に置き換わった。§5 を名指す但し書きは無くなったが、食い違いは無いまま —— 新しい文は黙示に与えるものだけを外し、§5.2(d) は明示の約束で、§5.2(d) 自身が *"Section 11.4 is unaffected"* と言う） |
| §2.2 / §4.3 / §5.2(b) / §10.1（条件を足さない網・T65 の後） | §2.2 は *"on what may be done with any copy of the Work that has been made available"*・§5.2(b) は *"an obligation in respect of the Work"*・§10.1 は *"in respect of the Work"* | You | §2.2 は献呈の文、§5.2 は約束で、足場が違う（§3za・T65 の逆側に記録済み） | **食い違い 0**（§3za で記録済みの差のみ） |

**(1) 約束の依拠の語がそろっていない（T66 で §8.6 について閉じた）。** §5.3 だけが *"may be relied upon by You and by anyone who receives the Work from You, directly or indirectly, as an intended beneficiary, to the extent a jurisdiction gives effect to such reliance"* と明示する。§8.6 は *"against You"* だけで、下流が依拠できることは §1.6（実施する者は You）と *"on the same footing as the covenants in Section 5"* に頼る。§12.2 は相手を名指すが *intended beneficiary* の語は無い。1.0〜1.3 で *intended beneficiary* は 1 回だけ出る。E71 の重さの列は *"Every covenant in Section 5 stands on the footing §5.3 states"* と読んで §5.3 を §8.6 へ運んでいるが、*footing* を「約束という法的な性格」と読めば運ばれず、§5.3 だけが明示していることから *expressio unius* の読みが立つ。**重さは Low** —— §12.2 は相手を名指しているので受益者であることは語から明らかで、§8.6 の *"same footing"* は E71 の読みが普通に立つ。**portfolio-1c が T66 として採った**（§5.3 の主語を *"The covenants in Sections 5.1, 5.2, and 8.6"*・+1 語・errata E83）。§12.2 は入れない —— 相手を自分で名指し、承継は §12.4 が §5.3 と違う広い列挙で持つので、§5.3 に入れると承継の列挙が 2 つ重なる。

**この掃引が establish しないこと**: 5 組は #280 が挙げた 4 組に §2.2 の網を足したもので、重なる組の全数ではない。比べた 5 つの観点も全部ではない（発動の時点・法域の扱いは見ていない）。確定の前の読み（`OSI-APPROVAL-PLAN.md` §4 の段 7）でもう一度やる。

**一般形**: **同じ働きの文が複数あるとき、明示を 1 つだけに足すと、明示の無い方が「無い」と読まれる。** 依拠・承継・終了のような横断の性質は、1 か所で全体に掛けるか（§2.8 の形）、全部に書くかのどちらかにする。§5.3 と §12.4 は承継を別々に書き、§2.8 が全体に掛けて両方を狭めないと言う —— 依拠にはその全体の文が無い。

## 3zc. 1.2 が §2.9 に持ち込んだ言い切り —— *"suspended by ... any act of a trustee"* はドイツの倒産の否認に負けうる（2026-11-16〜17）

**なに**: 1.0 の §2.9 の結果の言い切り（*"No insolvency … affects a permission granted here"*）は errata E30 が記録した。1.2 はそれを *"Nothing in this Dedication is conditioned on, suspended by, or revived by an insolvency, bankruptcy, administration, receivership, liquidation, dissolution, or similar proceeding in respect of the Dedicator, or by any act of a trustee, administrator, receiver, liquidator, or equivalent officer."* に書き換えた（1.3 も同じ）。*conditioned on* は文書の中身の言明で真だが、*suspended by … any act of … administrator* は法の効果の言明で、ドイツの倒産法では偽になりうる: InsO 134 条 1 項は申立ての前 4 年以内の無償の給付を否認の対象にし（*"Anfechtbar ist eine unentgeltliche Leistung des Schuldners, es sei denn, sie ist früher als vier Jahre"* *"vor dem Antrag auf Eröffnung des Insolvenzverfahrens vorgenommen worden."*）、否認は管財人の行為である（`rounds/2026-11-16-inso-103-129-134-143-gesetze-im-internet-snapshot.txt`・`jurisdictions.md` §3）。1.0 の文には無い（E30 の文は別の言い切り）ので、errata ではなくここに記録する。

**閉じ方**: 1.4 草案の T89 —— *"Nothing in this Dedication is, under its terms, conditioned on, suspended by, or revived by …"*（+3 語）。文書の中の仕組みが無いことを述べる文になり、法律が管財人に与える否認は外に出た。InsO 103 条（双務契約の履行選択）は、受け手が何も負わない ACD には当たりにくい（同じ写し）。

**一般形**: E30 で結果の言い切りを外した後に、同じ根（文書の外の法が決めることを文書が言い切る）が別の語で戻っていた。T81（§10.4）・T85（§8.2）・T89（§2.9）は 1.4 で同じ型の 3 か所を *"under it" / "under this Dedication" / "under its terms"* で閉じた。**この記録が establish しないこと**: 否認が実際に、既に写しを持つ受け手の許しに及ぶか（問い 8）。

## 3zd. 1.4 が持ち込んだ欠陥 —— T124 が §5.2 に足した授権と放棄は約束ではなく、§11.4 の但し書きの外に在る（2026-11-23）

**なに**: §11.4 第 2 文は *"It reaches nothing else, save that the covenants in Section 5 are promises about the Dedicator's own conduct and are not limited by this sentence."* と述べ、§5 のうち**約束**だけを「それ以外に及ばない」の外に置く。1.4 の T124（2026-11-20・THIRD §15.40）は §5.2 に *"the Dedicator authorises the circumvention of any technological measure … and waives any power under a law concerning such circumvention to forbid that circumvention"* を足した。これは約束ではなく授権と放棄で、その対象（17 U.S.C. §1201 の回避の禁止、指令 2001/29/EC 6 条の法的保護）が §1.5 の Covered Rights（*"any right of similar effect"*）に入るかは本文から決まらない。入らないなら、§11.4 第 2 文は書かれたとおりには偽になり（errata E44 と同じ型 —— 及びを述べる文が、文書が実際に及ぶものより狭い）、狭く読めば授権と放棄を切る。T124 の文は 1.0〜1.3 に無いので、errata ではなくここに記録する。

**重さ**: Low。§11.1 第 2 文 *"Nothing in Section 11 reduces what any other Section of this Dedication gives"* が、§11.4 で §5.2 の授権と放棄を減らす読みを閉じ、§15.1 も受け手に多く与える読みを採らせる。受け手が得るものは変わらない。欠陥は、及びの限界を知るために読み手が見る文（§11.4）が、その限界を正しく述べていないことである（E44 と同じ）。

**見つけ方**: E44 は §10.1 の限定（*in respect of the Work*）を及びを述べる文すべてに当てて見つかった。同じ文を、E44 を閉じた後（11-01）に入った試作（T53〜T134）に当て直した —— **及びの文を閉じた後に、及ぶ先を増やす変更が入っていた**。T124 の 2 巡（THIRD §15.40・§15.41）は §5.2(a)・§6.3・§4.5 との関係を当てたが、§11.4 には当てていなかった。

**同じ型の 3 件目**: 2f の最終の通読（2026-11-20・`ACD-1.4-UNIQUE-READING.md` の「§11.4 第 2 文の除外」の行）は、§2.5 の約束が但し書きの外にあって *"It reaches nothing else"* に狭められる読みを見て、§11.1 第 2 文で閉じて「一意」とした。E44（§16 の文書としての制限）・§2.5・T124 と、網羅を言い切るこの 1 文が同じ型を 3 度生んでいる。

**1.5 草案で閉じた（2026-11-23・T135・(c) を *"It gives nothing by implication beyond what its words give."* の形で）。1.4 は凍結のまま未修正。** **閉じ方の検討（`ACD-1.5-CLARITY-TRIAL.md` §1 の T135）**: 3 案を並べて測った。(a) 但し書きを *"save that Section 5 is not limited by this sentence."* にする（−11 語・split() で数えた）—— T124 を閉じるが網羅の言い切りは残る。(b) 第 2 文を丸ごと外す（−25 語）—— **退けた**: 1.4 の本文で黙示の許諾を外しているのはこの 1 文だけで（*implied* / *estoppel* の類いは §13 の *IMPLIED* と §2.5 の *estopped* のほかに無い・portfolio-cd の grep を 5e が確かめた）、外すと §4 の *use* の許諾から §8.4 の限定の外の特許へ黙示の許諾の議論に足場を与え、B7 の釣り合いを黙って動かす。**(c)** 第 2 文を *"It grants nothing by implication beyond what its words give."* に置き換える（−15 語・案は portfolio-cd）—— 網羅を言い切る文が無くなるので 3 件の型はまとめて消え、黙示の許諾の排除は残る。本命は (c)。**逆側**: (c) は第 1 文を「及ぶものの例示」に読ませうる、*estoppel* による許諾の排除を明示しない、法が強行的に与える黙示の許諾や消尽は外せない（どの案でも同じ）—— 逆側の全部は試作の節に在る。 1.4 の記述子（`ACD-1.4.machine.json`）は T124 の授権を `permissions` にも `covenants` にも持たない。1.5 の記述子の候補として `ACD-1.5-CHANGELIST.md` の「記述子の候補」に書いた（fc と 5e）。

**一般形**: 及びや例外を列で述べる文（§2.4 の *grant, permission, consent, and covenant*、§5.3 の約束の列、§11.4 の但し書き、§14.2 の約束の列）は、後から入った変更が列の語に当たらない種類の行為（授権・放棄）を足すと、黙って古くなる。同じ目で 3 つの列を当てた: §2.4 は *waiver* を列に持たないが、T124 の放棄と §3.3 の放棄は *"Sections 3, 4, 5, and 6"* の中に在り、§12.1 の放棄だけが外に在る —— §12.1 を他の条の効力に条件づける文は無く、§12.2 は自分で *"whether or not Section 12.1 has effect"* と独立を述べるので、立たない。§5.3 の約束の列は T124 を持たないが、授権は相手を You に限らない（回避が許された使用の中で行われれば足りる）ので、受け手が頼るための第三者受益の文を要しない。§14.2 の列は約束の違反の責任を述べる文で、授権と放棄は違反しうる行為ではない。**この記録が establish しないこと**: 回避を禁じる力が Covered Right に当たるか（法域ごとの問い・`QUESTIONS-FOR-COUNSEL.md` の問い 5 の回避の授権の段（§5.2 の T124 を既に引いている）に、Covered Rights に当たるかの面を足す候補）。

## 3ze. 1.4 が持ち込んだ欠陥 —— Dedicator だけを名指す 2 つの文が、§2.8 が同じに縛る承継人・譲受人・管財人を外す（§4.5 末文と §10.1・2026-11-24）

**なに**: 1.4 の T121（THIRD §15.38）は §4.5 の末に *"Section 4.5 does not permit a person to impose what Section 5 forbids on material as to which that person is a Dedicator."* を足し、T120 は §10.1 の末に *"other than in Your capacity as a Dedicator"* を足した。どちらも「1 人が受け手（You）と、約束に縛られる者の両方の役を持つ」場面を決める文だが、縛られる者として **Dedicator だけ**を名指す。§2.8 と §5.3 は、約束と Dedication 全体が Dedicator の承継人・譲受人・相続人、権利を譲り受けた者、§2.9 は管財人も縛ると定める。その人が Work の受け手（You）でもあるとき、(i) §4.5 第 1 文の *any terms You choose* が働き、末文の除外は Dedicator でないその人に掛からないので、「譲受人は §5.2(b) が禁じる条件を §4.5 で課せる」と読める。(ii) §10.1 の *"imposes no condition, obligation, restriction, or requirement upon You"* は Dedicator の役だけを外すので、「譲受人である You には §2.8 の拘束も課されない」と読める。§15.1（You に多く与える読みが勝つ）は、その You が譲受人のとき、どちらの読みも支える。2 つの文は 1.0〜1.3 に無いので、errata ではなくここに記録する。

**重さ**: Low〜Medium。§2.8 の *"A transferee takes subject to it"* と §5.3 が特定の文として勝つと読むのが自然だが、T120・T121 は「2 つの役」を決めるために足した文で、その文が 1 つの役だけを名指すこと自体が、名指されない役は外だという読みの足場になる。

**見つけ方**: portfolio-59 が T143 の反例を当てる途中で §4.5 末文について見つけ（2026-11-24）、portfolio-0d が同じ型を §10.1 に当てた。UNIQUE-READING の §2.8・§5.3・§12.4 の 2 巡目の行は約束の範囲を見ていて、§4.5 と §10.1 の除外の側は見ていなかった。

**閉じ方**: 1.5 草案で T144（§4.5 末文を *"Section 4.5 does not permit a person to impose what Section 5 forbids that person to impose."* へ —— 誰が・何についてを §5（§5.3 を含む）に任せる）と T145（§10.1 の除外に *"or as a person Section 2.8 names"* を足す）。試作と反例は `ACD-1.5-CLARITY-TRIAL.md` §11。1.4 は凍結のまま未修正。

**一般形**: 役を名指して例外を決める文は、その役と同じ拘束を受ける別の役（承継人・譲受人・管財人・死後に人格権を行使する者）を数えてから書く。役の名を挙げる代わりに、拘束を定める条を指す形（*what Section 5 forbids that person*・*a person Section 2.8 names*）なら、後から拘束される者が増えても古くならない。**この記録が establish しないこと**: 譲受人が実際に §4.5 を援用した例は無い。

## 3zf. 1.2 が持ち込んだ欠陥 —— §5.1 第 2 文は、許された使用を含む不法行為の請求（攻撃・事故）まで不行使と読める（2026-11-24）

**なに**: 1.2 と 1.3 の §5.1 は *"any claim or cause of action … arising from or relating to a use of the Work that this Dedication permits"*、1.4 の §5.1 第 2 文は *"any claim or cause of action … that treats as wrongful, or as without legal basis, a use of the Work that this Dedication permits or purports to permit"* を主張しないと約束する。Work の使用は「どの目的でも」許される（§4.1・§4.2）ので、Dedicator が公開した検査・負荷の道具で第三者が Dedicator 自身の server を攻撃したとき、その請求は「許された使用を違法とする請求」に当たり、除外（特許・商標・虚偽の言明・支払い）のどれにも入らない。1.0 の §5.1 には第 2 文が無いので errata ではなくここに記録する。

**重さ**: Low to Medium（採用）。故意の責任を前もって外す約束は多くの法域で効かない（独 BGB 276 条 3 項ほか）ので実害は小さいが、企業の法務は文字どおりに読んで止まる。文脈を渡さない読み手（AI の agent・本文だけを読む）2 体が独立に挙げた —— 欠陥の探し方であって、第三者の意見ではない。

**見つけ方**: 試作 T90（THIRD §15.23 の後）は「何の請求を入れるか」（不当利得・不正競争を入れる）を決め、「何の請求を外すか」を攻撃・事故に当てていなかった。1.2 → 1.4 の 3 度の言い直しはどれも入れる側の漏れを塞ぐ変更だった。

**1.5 草案で閉じた（2026-11-24）**: *"treats a use of the Work … as wrongful, or as without legal basis, by reason of its being a use of the Work"* —— 攻撃の請求は攻撃を理由とし、Work の使用であることを理由としない。1.2〜1.4 は凍結のまま未修正。退けた形: *"for want of the Dedicator's permission"*・*"does not depend on the use lacking the Dedicator's permission"* —— 許諾の不在に依らない不正競争・不当利得の請求が約束の外に戻る（T90 で *"depends on … being unauthorised"* を退けたのと同じ理由）。 **2026-11-25 の追記**: n8 の語は *"by reason of its being such a use or of what the Work contains"*（議題 28・32）。攻撃の請求が外れることは変わらない。失う側は、使用の仕方や結果を理由とする不正競争・サーバの負荷の請求が外と読まれうること（`CHANGES-ACD-1.5.txt` の 9）。

**逆側**: 「Work の使用であることを理由とする」の境は裁判所が決める。プライバシー・パブリシティの請求は理由が人の像であって Work の使用でないと争えるので、次の文で明示に入れてある。

## 3zg. 1.4 が持ち込んだ欠陥 —— ACD の通知つきの素材を取り込んだ別ライセンスのリポジトリへの patch が、書いた人の知らないうちに Contribution になる（2026-11-24）

**なに**: 1.0〜1.3 の §1.9 は宛先を *"the Dedicator or … a repository or forum the Dedicator maintains"* に限っていた。1.4 は errata E65（保守者が替わると寄与でなくなる）を閉じるため、宛先を *"a repository or forum, in either case offering the Work with a notice of this Dedication"* に替えた。MIT のリポジトリが ACD の通知つきファイルを取り込み（§4.5 が許す）、通知を残して公開すると、そのリポジトリは「Work を通知つきで提供する」宛先に当たる。そこへ、そのファイルを直す patch を MIT のつもりで出した人は、提出のときに別段のことを述べなければ、§2.6 で Dedicator になり、特許の許諾を含めて取り消せない。リポジトリの全体のライセンスや寄与の規約は「本人が述べた」ことに当たらない。

**及ぶ範囲**: ACD の素材への取り込みを目的とする patch（*"for inclusion in the Work"*）だけで、MIT の側のファイルへの patch は当たらない。ファイルの頭に通知が在るので、気づく手掛かりはある。

**重さ**: Medium（採用と公平）。errata E65 の採用のとき、*"maintains or has maintained"* を「後で再ライセンスされたリポジトリの寄与者を知らないうちに Dedicator にする」という同じ理由で退けていた —— 採った語も別の経路で同じ結果を生む。`ACD-1.0.against.md` #313（Markham 氏 2014・Ingo 氏 2014 *"the surprise element"*）と同じ型の懸念である。

**見つけ方**: 縮約の本文だけを読む独立の読み手（portfolio-6c・第三者の意見ではない）。1.0 の語には無いので errata ではなくここに記録する。

**1.5 草案で閉じた（2026-11-24・T147・議題 17）**: 1.5 草案 1.11 の除外の列に *"is submitted to a repository or forum that puts such submissions under other terms instead"*。*instead* は上乗せの許諾（ホスティングの規約が自社に求める許諾、CLA の追加の許諾）を外に出す語で、最初の案 *"or the place it is submitted to states other terms for such submissions"* は GitHub の利用規約で普通の寄与まで外へ出した。除いた素材は 10.4 の *"excluded by Section 1.11"* で識別の約束に届く。退けた候補: *"unless either of them, when submitting it, or the terms of the place it is submitted to, puts it under other terms"*（10.4 の文が長くなった）。**逆側**: 宛先の規約が寄与を別の条件に置けるので、fork の側の規約で寄与が ACD の外に出る —— 出た素材を識別する約束（10.4）はその素材を Work と一緒に含める Dedicator にだけ掛かる。1.4 は凍結のまま未修正。

## 3zh. 1.2 が持ち込んだ欠陥 —— §5.2(d) のプライバシー・パブリシティ・人格の約束が、Work に写ったものに結ばれていない（2026-11-24）

**なに**: 1.2〜1.4 の §5.2(d) は *"a right of privacy, publicity, or personality held by the Dedicator, in respect of any use of the Work that this Dedication permits"* を主張しないと約束する（errata E31 を閉じるため 1.2 で足した）。Work が画像や音声を作る道具（モデル・ソフトウェア）のとき、第三者がその道具で Dedicator 本人の偽の像（deepfake）を作ることは「Work の使用」で、像は Work に写っていない。字面では、その像についての人格権の請求まで不行使になる。CC0 の放棄は *"publicity and privacy rights pertaining to a person's image or likeness depicted in a Work"* と、作品に写った像に結ばれている。1.0 には §5.2(d) が無いので errata ではなくここに記録する。

**重さ**: Medium（採用と公平）。§5.2(d) の除外は虚偽の言明だけで、偽の像が「虚偽の言明」に当たるかは場面による。E31 が守ろうとしたのは、Work に入っている Dedicator 自身の像を受け手が使う場面で、道具で作られた像ではない。

**見つけ方**: 縮約の本文だけを渡した読み手（審査者の役・AI の agent・第三者の意見ではない）。E31 と試作 T159 は「誰の権利か」と「どの使用か」を当て、像がどこに在るかを当てていなかった。

**1.5 草案で閉じた（2026-11-24・語は 2026-11-25 の n8）**: 2.5(d) *"by reason of its being such a use or of what the Work contains, including a claim under a right of privacy, publicity, or personality"*。Work に写った本人の像・声・私事を理由とする請求は約束に入り、ほかの写真や録音から道具で作った偽の像・声の請求は、使用であることも Work の中身も理由でないので外れる。11-24 に入れた *the Dedicator's own … contained in the Work* の列は、日記や健康データ、模型が推論した事柄、譲り受けた publicity の権利の扱いが列の端で割れたので替えた（議題 28）。**逆側**: 1.4 §5.2(d) の *in respect of any use* より狭い。*what the Work contains* の境を 9.1 と 5.5(a) に預け、データ保護の請求にも約束が及ぶと読めるので「放棄できない権利を放棄させる」という批判を受けうる（答えは 2.7 と 6.4）。1.2〜1.4 は凍結のまま未修正。

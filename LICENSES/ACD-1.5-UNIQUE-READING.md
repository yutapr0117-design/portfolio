---
file: LICENSES/ACD-1.5-UNIQUE-READING.md
audience: 次のセッションの実装者（一次読者）/ 監査人 / 法律家
last-updated: 2026-11-24
canonical-ref: LICENSES/ACD-1.5-DRAFT.txt / .github/scripts/measure_legal_uncertainty.py（section19 が行を数える）/ LICENSES/ACD-1.4-UNIQUE-READING.md（1.4 の条の行。条の対応は CLAUSE-MAP-1.4-1.5.tsv）
---

# 1.5 草案の法的解釈を一意に定める —— 各条の「最も強い別の読み」

1.5 草案（縮約・議題 16・10 節 50 条）の条ごとに、最も強い別の読みを 1 つ以上書く。1.4 の行（`ACD-1.4-UNIQUE-READING.md`）は 1.4 の条の記録のまま動かさない。縮約の前の回帰（1.4 の行を縮約の条へ当てる）は議題 15 で済ませたが、それは「1.4 で閉じた読みが開いていないか」を見ただけで、縮約の語が新しく開けた読みは、ここで条の側から探す。

**合格の線**: 50 条すべてに行が在り、試作で開いている行が 0。出す版を 1.5 に替える議題は、その後に出す（議題 16 の条件 2）。

## 19. 法的解釈を一意に定める —— 各条の「最も強い別の読み」を 1 つ書き、立つなら語で消す（2026-11-24〜・5 人）

**方法**: 1.4 の第 19 節と同じ（型: 先行詞・修飾の掛かり先・量化・or・including・定義語の混用・時点・主語・否定の範囲）。加えて縮約に固有の型を 3 つ見る —— (あ) 1 文にまとめた列に、1.4 では別の条にあった限定が行き先を持つか、(い) 1.4 の試作（T 番号）で直した語が、短くしたときに元の語へ戻っていないか（`git log -S` と THIRD の記録に当てる）、(う) 2 つの条に分けて書いていた効果が、1 つの語で片側だけになっていないか。**行の形**: `- §x.y | 別の読み: … | 一意 / 試作 Tnn / 法の側 | 根拠: … | 本文 <main の commit>`（末尾の commit は判定した本文。条の語がその後に動いた行は `moved_clauses.py --ledger` が出し、判定した人が当て直す —— 議題 16 の条件 4）。**小節**: 19.1 = §1（6c）、19.2 = §2（59・二度目は 3f）、19.3 = §3〜§5（df）、19.4 = §6〜§8（3f）、19.5 = §9〜§10（6c）。各自、自分の小節の中にだけ書く。1.4 の条を引くときは版を名乗る。

### 19.1 §1（portfolio-6c）

### 19.2 §2（portfolio-59・二度目は portfolio-3f）

### 19.3 §3〜§5（portfolio-df）

### 19.4 §6〜§8（portfolio-3f・2026-11-24）

- §6.1 第 1 文 | 別の読み: *"gives nothing by implication beyond what its words give"* が、9.1 の *"the reading that gives You more prevails"* を打ち消し、語の広い読みを黙示として退ける | 一意 | 根拠: 9.1 は語が許す読みの間の選び方、6.1 は語の外のものを与えないという文で、対象が違う（9.1 *"that its words allow"*） | 本文 01211ae9
- §6.1 第 2 文 | 別の読み: *"the persons Section 7.2 names"* の権利には影響すると読み、承継人がもともと別に持つ Work の著作権（併合する側が以前から持っていた、この Dedication の外の素材の権利）まで及ぶ。1.7 の末文は特許の請求項だけを除き、Covered Rights には同じ除外が無い | 試作 T160 で入った | 根拠: §1.6（1.4 の §1.5）の *"holds or may come to hold"* は後から得る権利を含む（E60）。併合で残る法人が the Dedicator と同じ者かは法が決めるが、1.7 が特許だけを除くことで「著作権は除かない」の反対解釈が立つ。案: 1.7 の末文を外し、7.2 の末に "It does not reach a right that such a person holds otherwise than from the Dedicator." を置く（権利だけに掛かり、5.1〜5.3 の約束は承継人に届いたまま）。退けた理由: 59 —— 合併の包括承継では買い手が the Dedicator と読め、1.7 の *"owns"* に買い手の元からの特許が入るので 1.7 の除外が要る。6c —— 7.2 の側に置くと 7.2(c) の死後の人格権の行使者が空になる。残る実害は、買い手が別に持っていた Work の一部の著作権だけ（§1.6 の *"in the Work"*）。残る種 = 1.3 に 1 文 "A person Section 7.2 names is a Dedicator only as to what that person takes from the Dedicator."（59・T160）。**2026-11-24（議題 18）**: 1.3 の末に *"Succeeding the Dedicator, or being named in Section 7.2, makes no person a Dedicator as to anything that person holds otherwise than from the Dedicator."* を置き、6.1 は *"except as Section 7.2 states"* に替えた。Covered Rights と特許の両方が閉じる | 本文 01211ae9
- §6.2 第 1 文 | 別の読み: *"grants no right in a trademark, trade name, logo, or personal name"* が、2.5(d) の約束（名の権利に基づく請求を主張しない）まで否定する | 一意 | 根拠: 2.5(d) は 5.4 に従い、5.4(a) が *"anything done under rights in a trademark or a name"* を外に置くので、2 つは同じ向き | 本文 01211ae9
- §6.2 第 2 文 | 別の読み: *"You may state truthfully what the Work is"* が、商標の法が要る許しを与えると読める（第 1 文 *"grants no right"* と食い違う）、または法の効果（名指しの使用は許される）を言い切ると読める | 試作 T157 で入った | 根拠: 1.4 の T100 が同じ理由で *You may* を外し *"does not restrict nominative reference, including …"* にしていた（THIRD §15.33）。縮約で *You may* に戻った（縮約の型 (い)）。案: "Section 6.2 does not restrict stating truthfully what the Work is, where it came from, and who made it."（+1 語）。反例待ち。**2026-11-24（議題 17・18）**: 1.4 の §11.2 の語（*does not restrict nominative reference, including stating truthfully*）へ戻した | 本文 01211ae9
- §6.3 第 1 文 | 別の読み: *"a work"* が Work に限られ、Dedicator が別の作品を作ったという虚偽は 6.3 の外に出る | 一意 | 根拠: 6.3 は小文字の *"a work"* で、1.2 の *"Work"* と書き分けている | 本文 01211ae9
- §6.3 第 2 文 | 別の読み: *"a notice that accompanied the Work"* がファイルの中の作者のヘッダーを含まず、改変版にヘッダーを残した人が偽の帰属の外に出られない | 試作 T158 で入った | 根拠: 1.4 の T123 が 10.2（1.4 の §16.2）の *accompanied* と *within a file* の書き分けを理由に *"accompanied or was contained in the Work"* にしていた。縮約で *or was contained in* が落ちた（縮約の型 (い)）。案: 戻す（+4 語）。反例待ち。**2026-11-24（議題 17）**: *or was contained in* を戻した | 本文 01211ae9
- §6.4 第 2 文 | 別の読み: *"any permission that law requires"* の *that law* が、前の文の data protection の法だけを指し、肖像・人格の権利の法を含まない | 一意 | 根拠: 同じ文の *"personal data, likeness, voice, or performance"* が両方の法の対象を並べ、*that law* は第 1 文の 2 つの法の列を受ける。どちらの読みでも、許しは Dedicator の与えるものでないという結論は変わらない | 本文 01211ae9
- §6.4 末文 | 別の読み: 2.5(d) の *"any other claim"* が Dedicator 自身のデータ保護の請求も含むかが割れる（2.5(d) の例は privacy・publicity・personality だけで、data protection を挙げない） | 一意 | 根拠: 1.12 *"including"* と 2.5(d) の *"also includes"* は前を限らないので、*"any other claim"* が覆う。放棄できない権利（消去の請求など）がどこまで残るかは 2.7 *"to the fullest extent the law permits"* に従う | 本文 01211ae9
- §6.5 | 別の読み: *"Except as Section 6.3 states, it reduces nothing that Sections 2 to 5 expressly give"* が、6.2 と 6.4 の「与えない」を無効にする | 一意 | 根拠: §6.2 と §6.4 は *"expressly give"* のものを減らさず、はじめから与えていないもの（商標・第三者の権利・データ保護の許し）を名指す（§5.4(a) が同じ向き）。**2026-11-24（議題 18）**: 6.3 は「届く外」でなく 2.5(c)・2.5(d)・2.6 が及ばないとだけ述べる形になり、6.5 の例外は 2.2 の許諾を減らさない | 本文 01211ae9
- §7.1 第 2 文 | 別の読み: *"any copy of the Work that has been made available"* の反対解釈で、まだ出していない写しには後から条件を付けられる | 一意 | 根拠: 1.4 の §2.2 の行と同じ —— 出された写しへの後の条件が無いことで足り、出していない写しは受け手に渡っていない（どちらの読みでも受け手の許しは変わらない） | 本文 01211ae9
- §7.1 第 3 文 | 別の読み: *"that reliance is its purpose"* の *its* が the Dedicator を指す | 一意 | 根拠: 同じ文の *"makes it intending that others rely on it"* の *it* は this Dedication で、*its* も同じ先行詞 | 本文 01211ae9
- §7.2(b) | 別の読み: *"transferred"* が独占的実施権・独占的利用許諾を含まず、独占の被許諾者が Dedication に縛られずに請求する | 試作 T149 で入った | 根拠: 法域によって独占の許諾は譲渡と扱われたり扱われなかったりする。T149（0d）が語で決める。反例待ち。**2026-11-24（議題 17）**: *is later transferred or exclusively licensed* へ | 本文 01211ae9
- §7.2(d) | 別の読み: *"of the Dedicator or its property"* が、Dedicator から権利を買った第三者の破産の管財人を含まない | 一意 | 根拠: 第三者の管財人は 7.2(b) の *"any person to whom a Covered Right, or a Patent Claim … is transferred"* の地位を引き継ぐ者で、(b) と (d) は独立に並ぶ | 本文 01211ae9
- §7.2 柱書 | 別の読み: *"binds"* が 2.x の付与だけでなく 5.x の約束も承継人の約束にすると読むか、付与の効力だけを承継人に対抗させると読むか | 一意 | 根拠: 主語が *"This Dedication"* 全体で、7.4 が 5.1〜5.3 の約束を受益者の側から名指す（1.4 の E46 の型 —— 条を列挙しない） | 本文 01211ae9
- §7.3 | 別の読み: 倒産だけを名指すので、ほかの出来事（解散・死亡）では終わりうると読む | 一意 | 根拠: 4.1 *"No permission given here terminates or narrows, under this Dedication, for any reason"* が全部の理由を覆い、7.3 は最も問われる 1 つを名指すだけ | 本文 01211ae9
- §7.4 | 別の読み: 2.6 の放棄と同意、10.4 の表示の約束を挙げないので、後の受け手はそれらに頼れない | 一意 | 根拠: 2.6 の同意は *"every act, by You or by anyone who receives the Work …"* と受け手を自分で名指し、頼る相手方の条が要らない。10.4 は *"binds only that Dedicator"* で受け手の権利ではない（8.2 の列にも無い —— 意図） | 本文 01211ae9
- §8.1 第 2 文 | 別の読み: *"DOES NOT WARRANT … THAT ANY SECTION OF THIS DEDICATION IS EFFECTIVE"* が、2.7 の独立と 2.5 の約束の効力を自分で疑う文と読まれ、約束を弱める | 一意 | 根拠: 保証しないことは与えないことではない —— 主語 *WARRANT* は保証の文で、2.1〜2.6 の付与と約束は別の文が行う（2.7） | 本文 01211ae9
- §8.2 第 2 文（that the law does not permit の掛かり先） | 別の読み: 関係節 *"that the law does not permit to be limited"* が *"liability for breach of Section 2.5, 5.1, 5.2, or 5.3"* にも掛かり、約束の違反の責任も法が許す所では制限される | 一意 | 根拠: *"or a liability, … , that"* が 2 つ目の目的語を冠詞から新しく始めるので、関係節は直前の *"a liability"* だけに掛かる（先行詞）。**2026-11-24（議題 18）**: 第 2 文を (a)〜(c) の列にしたので、この読みの文は本文に無い | 本文 01211ae9
- §8.2 第 2 文（including の挿入） | 別の読み: *"including for wilful misconduct, gross negligence, death, or personal injury"* が、法が制限を許す法域でもこれらを無制限にする | 一意 | 根拠: 挿入句は *"a liability … that the law does not permit to be limited"* の例で、関係節がその全体を限る（1.12 *"including"* は例を挙げるだけ）。**2026-11-24（議題 18）**: 第 2 文を (a)〜(c) の列にしたので、この読みの文は本文に無い | 本文 01211ae9
- §8.2 第 1 文 | 別の読み: *"TO THE FULLEST EXTENT THE LAW PERMITS"* の一般の留保だけでは、約款の法（独 BGB 307・309 条）で免責の全体が落ちる | 法の側 | 根拠: 問い 9（責任の制限と約束の違反）。第 2 文が故意・重過失・人身を名指して外すのは、その法の下で第 1 文を残すため（1.4 の §14.1 と同じ構え・`ACD-1.0.jurisdictions.md` §3） | 本文 01211ae9

### 19.5 §9〜§10（portfolio-6c）

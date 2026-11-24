---
file: LICENSES/ACD-1.4-CHANGELIST-VERIFICATION.md
audience: OSI license-discuss / license-review participants, licence reviewers, a future drafter
last-updated: 2026-11-24
reachable-via: ACD-1.4-CHANGELIST.md
canonical-ref: LICENSES/ACD-1.4-CHANGELIST.md (変更の記録の本体) / LICENSES/ACD-1.4.txt (確定した本文)
---

# ACD-1.4 の変更の記録の分冊 —— 確定前検証（段 7）

`ACD-1.4-CHANGELIST.md` の「確定前検証（段 7・2026-11-06・相互参照と機械可読性は 5a）」の節を、2026-11-24 にこの file へ移した（本文は無改変）。本体がバイト数の上限（Check 495a・300,000）の手前に来たため。変更の主表・errata 由来・語数の内訳・持ち越したもの・確定の判断と、道具と Check が名で読む付録（確定時点の草案ヘッダ）と条項の対応表は本体に在る。外部レビューと確定前検証の前倒しは `ACD-1.4-CHANGELIST-REVIEWS.md`。

## 確定前検証（段 7・2026-11-06・相互参照と機械可読性は 5a）

**1.3 との差分の完全性と起草の 2 観点（25）、errata の状態の主張と OSD の 2 観点（bb）は、上の「確定前検証の前倒し」の表にある。** 6 観点のうち凍結を止める欠陥は 0 件である（2026-11-06）。

| 観点 | やったこと | 結果 |
| :-- | :-- | :-- |
| **相互参照** | 本文の内部参照 89 件を、指す先の条の冒頭と並べて全部読んだ（語の解決は 468 が見るので、ここで見たのは意味） | **clean** —— 指す先の内容と参照の文が食い違うものは無い。§8.5 の *"Sections 8.1 to 8.4"* に §8.6 は入らないが、§8.6 は *"the patent claims described in Sections 8.1 and 8.4"* で同じ集合を指し、§2.7 は全体に掛かるので射程は変わらない |
| **相互参照（再検証・2026-11-19・portfolio-50）** | 11-06 の検証（ad3574f8 の草案）の後、T35〜T131 で内部参照は 91 → 110 に増えた。増えた 19 件だけを、指す先の条と並べて意味で読んだ。あわせて本文の約束の文（covenant・undertaking・agrees）を全部抜き出し、§5.3 と §14.2 の列挙が覆う集合と照らした | **clean**（凍結を止める欠陥 0）。§14.2 *"in breach of a covenant in Section 2.5, 5, 8.6, or 12.2"* は covenant の語を持つ 5 つの条（§2.5・§5.1・§5.2・§8.6・§12.2）を全部覆う。**逆側（記録のみ）**: §12.1 の *"waives and agrees not to assert"* も約束の形だが §14.2 の列挙に無い —— 同じ行為（Moral Rights の行使）は §12.2 の covenant が *"for every jurisdiction"* で覆うので、§12.2 だけが効かず §12.1 の合意だけが効く法域でしか差は出ない。§2.6 の undertaking が §14 に服するのは本文が明示している（*"is subject to Section 14"*）。§14.2 の *"Section 2.5, 5, 8.6, or 12.2"* は単数の Section で列挙を受けるが、*a covenant in* が 1 つの条を指すので読める（§5.3 は *"Sections 2.5, 5.1, 5.2, and 8.6"* と複数形）。**残り**: 11-06 の 6 観点のうち、起草・差分の完全性・OSD・errata の状態は T35 以後の試作を含めて当て直していない —— 確定の日の前に当てる |
| **1.3 との差分の完全性（再検証・2026-11-19・portfolio-50）** | 1.3 と 1.4 草案の本文（第 1 条から *END OF TERMS* まで）を条ごとに切り、空白を畳んで比べた。変わった条の全部が `CHANGES-ACD-1.4.txt` の箇条に条番号で名指されているかと、その逆（箇条が名指す条で、1.3 と同じままのもの）を見た | **clean**。82 条のうち変わったのは 61 条で、どれも箇条に名指されている（条の増減は 0）。逆向きで 1.3 と同じままの条を名指すのは §3.1・§3.3・§10.5・§12.1・§13.2 の 5 つで、どれも別の条の箇条が参照先として名を出しているだけ（変えたとは言っていない）。§1.4 は一覧の題名の *ACD-1.4* に当たっただけ。**この測り方が見ないもの**: 1 つの条の中で、箇条が述べない変更が残っていないか（条の単位で名指されていれば通る）。語数の合計は Check 498 (k) が、箇条ごとの語数は 468n が見る。**同じ日に条の中も粗く当てた**: 61 条を語の単位で diff し、変化の塊ごとに、その条を名指す箇条の語が塊の語（4 字以上）の半分以上を含むかを見た。含まない塊は 33 —— 版の識別子（§16.1・§16.2 の 5）、1.3 の行末の分綴（*click- through*）、文法の一致（§3.2 *include*・§12.3 *They*）、errata を引く箇条が理由ごと外したと述べる文（§2.7・§2.8・§8.4・§11.4 の理由の文）、言い換えの箇条が新しい語だけを引くもの（§8.1・§8.4 の *infringe*、§14.2 の冒頭）で、**述べられない変更は 0**。いちばん薄いのは §11.4 の *"of a person other than the Dedicator"* で、箇条は E43 を引くだけで語を述べない（読み手は errata を開かないと狭めたと分からない）—— 箇条に語を足すかを 1c へ送った |
| **OSD の当て直し（再検証・2026-11-20・portfolio-30）** | 11-06 の後に変わった条に OSD 1〜10 を 1 条ずつ当てた（1c の下書き 10 条と、30 が足した 6 条） | **clean**（凍結を止める欠陥 0）。記録と逆側は THIRD §15.52 |
| **機械可読性** | 1.3 の記述子を土台に 1.4 の下書きを作り、使い捨ての worktree で確定本文と一緒に Check 451 を通した | **欠陥 1 件を直し、1 件を下書きで閉じた。** (1) T5 で §16.1 が本文に *"Section 16.2"* を持ったので、通知文を切り出す 4 か所（Check 445 / 451b / 451d と `generate_spdx_license_xml.py`）が通知文の手前で切れていた。451d は正しい記述子を赤くし、SPDX 生成器は通知の無い header を黙って出した（138 行 → 直して 140 行）。行頭の `\n  16.2 ` で探す形へ直した。(2) 1.3 の型のまま `osiApproved: false` / `spdxListed: false` を凍結すると、承認された日に偽になり直せない（凍結ヘッダの *"NOT SUBMITTED"* と同じ形）。下の `statusAtFixing` で閉じる |

### 確定の判断の材料 —— 1 枚（2026-11-19・portfolio-50・段 7 の通読は 5 帯とも閉じ、OSD の当て直しも 0 で返った・2026-11-22 に更新）

**何を決めるか**: 1.4 草案を確定して凍結し、1.3 のときと同じくこのリポジトリへ適用するか（`ACD-1.3-CHANGELIST.md` の確定の判断が先例）。**提出（`license-review`）ではない** —— 提出のゲート 6b（出す版が `license-discuss` に 30 日）はオーナーの投稿を待って未充足のままで、確定はそれを動かさない。

| 材料 | いまの値 | 出どころ |
| :-- | :-- | :-- |
| 段 7: 相互参照 | clean（11-06 以後に増えた 19 件と、約束の文の集合と §14.2） | 上の表・2026-11-19 |
| 段 7: 1.3 との差分の完全性 | clean（変わった 61/80 条はどれも箇条に在る・条の中の述べられない変更 0） | 上の表・2026-11-19 |
| 段 7: 起草（最終の通読） | **5 帯とも閉じた** —— 1c §1〜§4（T132・T133）、30 §5〜§7（0）、50 §8〜§10（T134）、2f §11〜§13（0）、9b §14〜§16（0・1c と 2f も先に読み一致）。9b の記録した CHANGES の古い箇条（途中の形を now で述べる §14.1・§14.2・§16.3、§16.2 の重なり）は 1c が最終の形に直した | THIRD §15.48〜§15.51 |
| 段 7: OSD・errata の状態 | errata は 85 件のうち 83 件を 1.1〜1.4 の草案で閉じ、E10 は確定の手順へ、E6 は残すと決めた（`ACD-1.0.errata.md` の冒頭・Check 464 / 468e / 469(b) が照合）。OSD の当て直しは **clean**（11-06 の後に変わった条に OSD 1〜10 を当てて立つもの 0。`SUBMISSION-MATERIALS.md` §1c の OSD の表も今の草案に合わせた） | THIRD §15.52（30）・§15.53（2f）・上の表 |
| 段 7: 機械可読性 | 記述子の下書きは下の節。確定の日に、確定本文と一緒に Check 451 を通し直す（11-06 の検証は T35 以前の本文）。`measure_descriptor_carryover.py` は T134 の後にも回し、記述子が取る値の変わる条は 0（2026-11-21・下の節） | 確定の日 |
| 長さ（B3） | 本文（第 1 条から *END OF TERMS* の前まで）1.3 の 5,103 語 → 1.4 の 5,542 語（+439）。前文から *END OF TERMS* まで 5,432 → 5,868（+436）。どちらも `split()`・2026-11-19 | 道具で数えた |
| 法的解釈の台帳（§19） | 開いている試作 0。法の側の行は法律家への問いへ | `ACD-1.4-UNIQUE-READING.md` |
| register（B1〜B15） | 本文の語で減らせるものは残っていない —— 模擬委員会の 5 人はどれも「条を変える指摘 0」（THIRD §16）。B1（法律家）・B2（採用）・B14（moderators）は本文の外、B3 は上の +436 | `ACD-OSI-BOTTLENECKS.md` |

**確定する側の理由**: (1) 1.3 からの 61 条の変化はどれも、理由と逆側と反例の巡回を経て記録がある。(2) 1.3 をこのリポジトリに適用したまま、1.4 が直した欠陥（errata の 1.4 の分）を持つ版を利用者に配り続けている。(3) 提出するときに出すのは確定した版で、確定しなければ 6b の 30 日の窓を始める版が決まらない。

**逆側（同じ重さで）**: (1) 凍結すると、後で見つかった欠陥は errata に記録して 1.5 の草案で直すことになり、版が 1 つ増える —— 読み手が見る版の数（1.0〜1.4）は B13（理解の費用）を上げる。(2) 長さは 1.3 から +436 語で、B3 を悪くする向きにしか動いていない。(3) 法律家の目は 1.4 にも無い（B1）。確定は「法的に正しい」ことの主張ではない。(4) 段 7 の残り（9b の帯・OSD）が済む前に決めれば、確定は 6 観点を含まない —— 1.3 のときの「模擬審査は利用上限で結果ゼロ、確定はそれを含んでいない」と同じ形の但し書きになる（2026-11-20 に 5 帯の通読と OSD の当て直しが済み、この但し書きは要らなくなった）。

**計画 §4 の「申請の日に確定する最新版」との関係**（1c の問い・2026-11-19）: 文は 2 通りに読める —— (a) 申請の当日に確定する、(b) 申請の日の時点で確定している最新の版。**(b) と読む**。ゲート 6b は出す版（または直前に list へ出た版との差）が `license-discuss` に 30 日置かれていることを求めるので、申請の当日に確定した版は出せない。ゆえにいま 1.4 を確定しても、申請の日までに 1.5 を確定すれば出すのは 1.5 で、6b の 30 日は 1.4 からの差について数え直す。計画の 2 か所（§2 の表の 4 行目と、§3 の「審査中の変更」の行の「申請の日に版を確定するまで」）に同じ読みを書いた。

**逆側 (1) への答え —— 使う版は常に 1 つ**: 1.3 のときと同じく、このリポジトリが適用する版は 1 つで（ルートの `LICENSE` が名指す）、凍結した旧い版は本文を変えない記録として残る（`FROZEN.md`）。読み手が見る版の数は増えるが、使う版・出す版は常に 1 つで、版の間の差は `make_redline.py` が出す。B13 の費用は「どれを読めばよいか」の 1 行（`REVIEWERS.md` の *Which text you are looking at*）で払う。

**確定の後の一意化**: 凍結した本文は直さない（Check 453）ので、確定は 1.4 の一意化の区切りでもある。オーナーの依頼（法的解釈を一意に）を 1.5 の草案で続けるか、1.4 の errata の記録に回すかは、確定の後に 5 人で決める（1c の案）。

**50 の見立て**: 9b の帯の通読は 0 で返った（§15.51）。30 の OSD の当て直しが 0 で返れば、確定に進む材料は揃う（1c も同じ条件で確定に賛成・2026-11-19）。どちらかから種が立てば、それを試作で閉じてから。判断は 5 人でする（1c の案・2026-11-19）。

**5 人の判断（2026-11-22・portfolio-50 がまとめた）**: **1c・30・2f・9b・50 の 5 人とも、確定・凍結・適用に賛成**（1c と 50 の条件だった OSD の当て直しの 0 は §15.52 で満たされた）。**共通の条件**: 確定の道具の予行で EXPECTED（362・444m・460）の外に出た RED を、確定の前に閉じる —— いまの main では **459c**（確定の道具が作る英語の文書が `REVIEWERS.md` の地図に無い）と **468ad**（確定した版の CHANGELIST を読ませる直し）の 2 つで、どちらも 9b が閉じる（454・495a は portfolio-5a の 1e284b2c の移しで消えた）。**確定の記録に残す一文（2f の案）**: 確定は、1.4 の本文が法的に正しいことの主張ではない —— 法律家の目は 1.4 にも無い（B1・上の逆側 (3)）。`ACD-1.0.review-readings-2.md` §1.271（PSF-2.0 の提出は 72 日返事なし）は確定を動かさない —— 確定は提出ではない。**分担**: 確定の日の作業（`prepare_version_freeze.py`・記述子・Check 451・FREEZE-DATA・ルートの `LICENSE` と公開面の適用）は 50 と 9b が 1 本の PR に回し、公開面（llms 系・`.well-known`）の版の置換は aio-guardian を通して digest を再生成する。1c は確定本文の語が草案と byte で同じかを確かめ、その PR が出るまで草案の本文を動かす PR を出さない。

### 1.4 の記述子の下書き（確定の日に `ACD-1.4.machine.json` へ入れる）

**1.3 からの差だけを書く。** 版の置換に加えて次を当てる。この形で Check 451a / b / d / e が通ることは確かめた（§6 / §8 / §9 をすべて引く）。

| 変更 | 値 | 根拠と判断 |
| :-- | :-- | :-- |
| `schemaVersion` | `2` | 下の 2 つの key を外すので、読み手に形の変化を知らせる |
| `osiApproved` / `spdxListed` を外し、`statusAtFixing` を足す | `{"date": "<確定日>", "osiApproved": false, "spdxListed": false, "legalReview": false, "note": "True on the date above. LICENSES/FROZEN.md records what has happened since."}` | 凍結された file が承認の日に偽になるのを防ぐ。`legalReview` は開示を機械可読層へも置く。**⚠ 逆側**: 古い key を読む機械は 1.4 で値を得られない。`aio-manifest` の `license` は現在の状態を持つので、現在値はそちらを見る |
| `$comment` | *"Every entry with a clause key cites the clause it comes from … name, version, text, and steward identify this file; statusAtFixing records outside facts on the date this file was fixed and is not drawn from any clause."* | M14 を閉じる。旧文は `clause` を持たない key まで述べていた |
| `permissions.studyAndAnalysis` / `reverseEngineering` | `true`・§4.2 | 候補 (a)。1.4 が足した語で、機械から見えない |
| `covenants`（新しい欄）| `noAssertionOfCoveredRights` §5.1 / `noCollateralObligationByDedicator` §5.2（`note` に *paragraph (b)* と書く。`clause` は Check 451 が条の番号で照合するので `5.2` のまま）/ `noAssertionOfLicensedPatentClaims` §8.6 | 候補 (b) と §8.6。約束は許諾ではないので `permissions` に置かない。key 名に *ByDedicator* と *Licensed* を入れ、本文が述べていない一般化（どの利用規約も無効、どの特許も主張しない）を述べない。§8.6 が約束するのは *"the patent claims that Sections 8.1 and 8.4 reach, in respect of any act that those Sections describe"* だけである（25 の照合で `noAssertionOfPatentClaims` から直した。§6.1 を直した理由と同じ形。**2026-11-12 訂正**: この行は T22 より前の *"the patent claims described in Sections 8.1 and 8.4"* を引いたままだった）。**2026-11-08 追記**: `noAssertionOfCoveredRights` は §5.1 の第 1 文を指す（2026-11-08 に 2 つの約束を 2 文に分けた）。第 2 文（*"any claim or cause of action … that treats as wrongful, or as without legal basis, a use of the Work that this Dedication permits"*）を書くなら、除外の 4 つ（特許、商標と名前の権利、虚偽の言明と表示、合意した支払い）を `note` に書く。§5 の全体に掛かる外として、§5.2 末尾の 1 文（Dedicator 自身が作り、または出す Work 以外の素材とその条件・手段、写しを渡さずに Work を動かすサービスの利用に付ける条件と手段。2026-11-09 の T48 で、サービスは (a)(b) だけでなく §5 の全体の外になった）を、`covenants` の各 `note` に書く。書かなければ、記述子が本文より広い約束を述べる |
| `machineGeneratedMaterial`（新しい欄）| `rightAssertedByDedicator: false` §9.2 / `recipientMustDetermineWhichParts: false` §9.3 | 451e と #269。**「権利が存在しない」とは書かない** |
| `reservationsAndLimits.textRedistribution.note` | §16.4 に合わせて書き直す（名前は *"any name that contains "Autonomous Commons Dedication", regardless of case"*（T44・T50）、識別子は *"any identifier that contains "ACD-", regardless of case, followed by a digit"*（T27 で *begins with* から、T46 で大小を区別しない形に変わった）、Steward は *"no earlier text the Steward or a former Steward has published, other than a draft identified as such, has borne"* 版番号と識別子の下だけ（T47・T49）、*"A modified text may be distributed under a different name"*、翻訳と再符号化の但し書き） | 候補 (d)。1.3 の文のままだと記述子が本文より広いことを言う。制限は作ることではなく、その名前の下で頒布することだけだと読める形にする |
| `permissions.modelAndOutputUnencumbered`（§6.4）| `true` のまま。`note` を足すなら *"You owe nothing under this Dedication"* の範囲で書く | 2026-11-08 の T33 で §6.4 の後半に *under this Dedication* が入った。Dedicator 自身のサービスの条件は §5 の外なので、「出力に誰も何も求めない」と書くと本文より広い |
| `reservationsAndLimits.tdmReservation` | `false`・§6.2 のまま。`note` を足す: *"No signal is read as the Dedicator's Reservation (Section 6.2), and a notice that is only a Reservation assigns no material to other terms (Section 16.2). A Reservation made by another rightsholder in rights of their own is not affected (Sections 2.7 and 6.3)."* | T52（2026-11-10）は、留保だけの通知が素材を Work の外へ出さないと定めた。機械はファイルの中の TDM の opt-out の信号を見て素材が外れたと読みうるので、記述子にも置く。**⚠ 逆側**: 他の権利者の留保は外れないので、「信号はすべて無視してよい」と読める書き方にしない（第 3 文）。`note` は `clause` を増やさないので 451a の照合は変わらない |
| `outOfScope[1]`（§11.4・data protection, privacy, publicity, personality）| `clause` は `11.4` のまま。`note` を足す: *"No permission is granted under these rights (Section 11.4). Separately, the Dedicator covenants not to assert, or authorise or assist any other person to assert, its own rights of privacy, publicity, or personality against You in respect of any use of the Work that this Dedication permits or purports to permit, other than for a false statement or representation (Section 11.3). That covenant is Section 5.2(d); it is not a grant, and Section 11.4 is unaffected. Rights of this kind held by anyone else are untouched."*（**2026-11-21**: *purports* が無いと §5.2(d)（T93）の射程を狭めていた。）（**2026-11-11 に直した**: portfolio-00 が最初の文を本文に当て、4 か所を指摘した。(1)「誰に対して」が You から「使用」に変わり、許諾を行使していない者への主張まで入る広い読みがあった、(2) *"or authorise or assist any other person to assert"* が無く本文より弱く見えた、(3) 例外の出典を §5.2(d) と書き、本文が結ぶ §11.3 と違った、(4) grant でないことが無く、outOfScope の中で「範囲に入った」と読む余地があった） | `outOfScope` だけを読む機械は、Dedicator 自身の人格・肖像の権利も主張されうると読む。§5.2(d) を `covenants` の別の key にすると、§11.4 の「与えない」と同じ権利について「主張しない」が離れた場所に並び、どちらが勝つかを機械が決められない。同じ欄の `note` に置けば、与えないことと主張しないことが 1 か所で読める。**⚠ 逆側**: `note` は `clause` を増やさないので、§5.2(d) は 451a の照合（`clause` が本文に実在するか）の外に置かれる。`note` の中の *"Section 5.2(d)"* は人が読む参照である |
| `notice` | §16.1 から写す | 451b / 451d が照合する |

**足さないもの**: 候補 (c)（§4.3 の規模・§8.5 の *controlled*・§9.1 の例示・§1.3）は既存の key の `clause` で足りる。§5.2(d) は `covenants` に足さず、下の `outOfScope[1]` の `note` に置く（2026-11-11 に決めた。理由は下の行）。**確定の日は `measure_descriptor_carryover.py` を回して、変わった条をもう一度読む。** **前倒しで 1 度読んだ（2026-11-11）**: 道具は 1.3 の記述子が引く 23 条のうち 13 条の本文が変わったと出した（§2.3・§2.7・§4.2・§4.3・§6.1・§6.4・§8.1・§8.4・§11.1・§11.4・§12.2・§16.3・§16.4）。それぞれの key の値を 1.4 の本文に当て、値が変わるものは 0 だった（`true` / `false` はどれも 1.4 でも成り立つ）。`note` を要するのは上の表の 4 つ（§4.2 の追加の key・§6.4・§16.4・§11.4 の §5.2(d)）と §6.2 の T52 で、どれも表に在る。確定の日までに草案が動けば、もう一度回す。**2026-11-12 に回し直した**（T54〜T60 の後）: 変わった条は同じ 13 条で、値が変わるものは 0。§8.4 の一致度は T54 で理由の文を外して 0.20 まで下がり、道具は「別の条になっている可能性」と出すが、記述子が §8.4 から取る値（モデルと出力に及ぶ特許の許諾）は 1.4 の第 1 文が持つ。§16.4 は T57 で 2 文に分けたが、`textRedistribution.note` の下書きが引く語（*no earlier text … has borne*）は残る。1.3 の記述子が引かない §2.6・§2.8・§5.2・§8.6 の変更（T56・T58〜T60）は、上の表の §8.6 の行と `covenants` の欄で読んだ。**2026-11-21 に回し直した**（T61〜T134 の後）: 1.3 の記述子が引く 23 条のうち 20 条が変わった（変わらないのは §4.1・§7.2・§13.1）。新しく変わった 7 条は §4.5・§6.2・§8.2・§10.2・§10.4・§14.1・§15.3 で、取る値は変わらない（§4.5 末文は Dedicator 側の限定、§6.2・§10.2 は語の置換、§8.2・§10.4 は射程の限定、§14.1 は法が許さない場合の例外、§15.3 は第 2 文の削除）。§6.4・§8.1・§8.4・§12.2 は一致度 0.5 未満に書き直されたが、取る命題は本文が持つ。新しい欄の条も値は変わらない（T124 は You に何も課さない）。直したのは上の `note` と、冒頭の 33 件（451a の ACD-1.0 の数）を 1.4 の実測 41 件にしたこと。記述子で Check 451a / b / c / d / g が通るのを確認した。

### 提出対象を切り替える日の読み（2026-11-07・25。2026-11-08 に規則の形へ書き直した）

`prepare_version_freeze.py --report 1.4` の上の段（全部読む面）を先に読んで判断した。**行番号は編集のたびに動く**（2026-11-07 に書いた `objection-map.md` 42・48・60 は、翌日には 46・55・68 になっていた）。そこで判断を**規則**として書き、行番号は 2026-11-08 の report の値を目安として添える。当日は report を回し、各行をこの規則で振り分け、**どの規則にも当たらない行だけを読む**。

report の残り 3 段は見出しどおりに直す。**§A が ACD-1.0 を述べる行**は `SUBMISSION-TARGET` と同じ版へ向ける（送る本文は Check 472o と 472f が見る。履歴の文は残す）。**日付つきの実測**は走らせ直して値と日付を更新する（値を書き写さない）。**版を決め打ちした検証コマンド**は確定の版のファイル名へ向ける。

| 規則 | 当たる行（2026-11-08 の report・目安）| 判断 |
| :-- | :-- | :-- |
| 1.0 の §1.2（Work）を、版を名乗らずに引く文 | `objection-map.md` 46・55・68、`submission.md` 394、`submission-osd.md` 206・210・213・225・227、`submission-reference.md` 178・182・223・627、`REVIEWERS.md` 202・203 | **§1.3** へ |
| 1.0 の §1.2 の逐語を引く文 | `submission-osd.md` 191 | 1.4 の §1.3 の逐語へ差し替える（E61 で *in whole or in part* が消えている）|
| 1.0 の §1.4（You）| `submission-osd.md` 92、`submission-reference.md` 288 | **§1.6** へ |
| 翻訳の規則を §16.5 と呼ぶ文 | `submission-osd.md` 53、`submission-reference.md` 546 | **§16.4** へ。§16.5 は Steward の定義になった |
| §15.7（準拠法）| `submission-reference.md` 533・716、`REVIEWERS.md` 206 | **§15.3** へ。206 の *"(§15.3 from 1.1)"* は外す |
| §15.8（英語が正文）| `submission-reference.md` 549・551・711 | **§15.4** へ |
| §15.2（数と例示）| `submission-reference.md` 707・716 | **§15.5** へ |
| Work と Dedicator の組 | `submission-reference.md` 715 | §1.2 → **§1.3**、§1.3 → **§1.4** |
| 他のライセンスの条番号 | `submission-reference.md` 435（CERN-OHL の §1.4）| **直さない** |
| 版を名乗る、1.1 以降の番号を使う、番号の対応を説明する文 | `submission-osd.md` 68・149、`submission-reference.md` 666・667・669、`submission.md` 20、`READY-TO-SUBMIT.md` 44、`REVIEWERS.md` 99〜106 | **直さない** |
| 1.4 の番号で書いた文 | `SUBMISSION-MATERIALS.md` 84・136・149・182 | **直さない** |
| 個別 | `QUESTIONS-FOR-COUNSEL.md`（472h）| 冒頭の *Which text* と canonical-ref を 1.4 へ。問 2 の §8.4 と問 5 の §5.1 は「1.3 の文、そのあと 1.4 の差」の順なので、1.4 の文を先に置き、1.3 は *in ACD-1.3* と名指して残す。*the 1.4 draft* は *ACD-1.4* へ。§2.8 の版の差を述べる文はそのままでよい |
| 個別 | `REVIEWERS.md` の §8.4 の限定の引用 | 1.3 の文である。切り替えの日に 1.4 の §8.4 の限定の文へ替える |
| 個別 | `against.md` 482（#133 の行）と `submission-reference.md` 709 が引く §6.4 の *"You owe nothing in respect of any of them"* | 1.4 では *"You owe nothing under this Dedication in respect of any of them"*。版を名乗って 1.0 の文として残すか、1.4 の文へ替える（5a の比較で出た）|
| 個別 | `REVIEWERS.md` の *The case, and the strongest thing against each part of it* の表 | `SUBMISSION-MATERIALS.md` §1c の理由 6（審査者が読み方を既に知っている形: §8.1・§8.4 の行為の列、§11.1・§5.1 の商標、§16.2 の comment のタグ）を英語で 1 行足す。逆側（法的レビューの代わりにならない、§8.4 は意図して見慣れない、関連会社の特許には届かず Apache-2.0 だけが届く・#310）も同じ行に置く。1.0 が審査の対象のあいだは足さない（表が説明する版と食い違うため）|
| 個別 | §5.1 / §8.1 / §8.3 / §8.4 / §8.6 を引く文（2026-11-07 の T16〜T20）| `submission-reference.md` 73・85、`clause-reference.md` 122、`QUESTION-INDEX.md` 58 の *three footings* は、1.4 では §8.6 に無く前文が持つと直す。`review-corpus.md` R3 の §8.1 の引用は 1.0 の文なので残す。`measure_quote_drift.py 1.3 1.4` が出す §5.1 と §8.4 の行は当日に読む |
| 個別 | §9.2 の第 3 文（T34）を引く文 | `submission-reference.md` 91・92 と `review-responses-clauses.md` 545 は *"Sections 3 to 8 and Section 12 apply to it in full"* を引く。1.0 の文としては正しい。版を名乗らずに §9 を説明する段（`submission-reference.md` §1 の 3.）は 1.4 の *"this Dedication applies to it"* へ替え、想定問答は 1.0 の文として残す |
| 1.0 の大きさ（4,896 語・16 節 82 条・597 行）を、版を名乗らずに述べる文 | `ACD-OSI-BOTTLENECKS.md` 27・95（B3 の行）、`QUESTION-INDEX.md` 59・72、`submission-reference.md` 311、`submission.md` 54、`README.md` 31 | 確定の版の値へ替える（当日に `wc -w` と条の数を測り直す。値を書き写さない）。B3 の行は 1.0 の値のままだと長さを小さく言うことになるので、必ず替える。`prepare_version_freeze.py --report` はこの種の文を拾わない（docstring が「語数の申告の文は人が行う」と書く）。版を名乗る文（`REVIEWERS.md` 23・230 の `ACD-1.0.txt` の行、`against.md` の経緯）は直さない |
| 個別 | `REVIEWERS.md` の `against.md` の倍数（*"about twenty times the length of the licence"*）| 分母は `SUBMISSION-TARGET` が名指す版の本文（Check 460(g)・PR 2687）。marker を替えた時点で新しい比で照合されるので、入口の語を数え直す（1.4 なら約 17.7 倍で *"about eighteen"*）|
| 個別 | `ACD-1.0.clause-reference.md`（全 16 節 82 条・1.0 の番号）と、それを *"all 82 clauses"* と紹介する入口（`submission.md` 54、`REVIEWERS.md` 325、`README.md` 31、`QUESTION-INDEX.md` 59）| 1.4 は 80 条で番号も中身も変わるので、1.0 の逐条リファレンスは提出する版の逐条にならない。Check 460(c) は申告の条数を `ACD-1.0.txt` と照合するので、切り替えても RED にならない（機械はこの食い違いを見ない）。1.4 の逐条リファレンスを草案の段階で作っておき（`ACD-1.4.clause-reference.md`・2026-11-08）、入口はそれへ向ける。確定の日に名前から *-DRAFT* を外すかを決め、草案の条文が変わった行を読み直す。1.0 のものは 1.0 の記録として残す |
| 個別 | §16.4 の名前を *"under the name …"* と引く文（T44）: `against.md` 80（#27）、`faq.md` 226、`submission-osd.md` 138、`submission-reference.md` 657 | 1.0〜1.3 の文としては正しい。提出の版の §16.4 を述べる文は *"under any name that contains …, regardless of case,"* へ替え（T44・T50）、版を名乗る文と経緯は残す |
| 個別 | §5.2(a) を *"not to apply technological measures"* と述べる文（T64）: `submission-reference.md` 544（*"No anti-DRM condition on the licensee"* の段 *"a covenant by the licensor not to apply technological measures to the Work or to invoke anti-circumvention law against You"*）、`submission-osd.md` 135（*"covenants not to apply or invoke technological measures or laws against You"*） | 1.0〜1.3 の文として正しい。1.4 では *apply* が無いので、「Dedicator は手段を掛けてよいが、その手段について権利を主張せず、回避の法を You に向けない」へ替え、GPL-3.0 §3 の *"waive any legal power to forbid circumvention"* と同じ形だと書く（`ACD-1.4-SECOND-CLARITY-TRIAL.md` §14.36）。`against.md` #135 は *"ACD-1.0 relies on"* と版を名乗るので替えない（portfolio-50 の整合監査） |
| 個別 | §12.5 の旧文 *"… survives it"* を引く `against.md` #118 | 1.0〜1.3 と 2026-11-15 までの 1.4 草案の文として正しい。1.4 では T67 で *"Neither the covenant nor the consent … survives both"* になったので、提出の版の §12.5 を述べる文は今の語へ替える（portfolio-9b の測定） |
| 個別 | §8.3 の理由の文 *"because software cannot be practised without practising whatever patent claims it embodies"* と *"Any reading … that would produce that result is to be rejected"* を引く文: `comparison.md`・`gap-measurements.md`・`reviewer-positions.md`・`review-venue.md`・`review-readings.md` | 1.0〜1.3 の文として正しい。1.4 では T71 で外したので、提出の版の §8.3 を述べる文は第 2 文までの形へ替え、説明は前文に在ると書く（portfolio-30） |
| 個別 | 前文の *"silent or hostile"* を引く文: `reviewer-positions.md`（1.0 の前文として） | 1.0〜1.3 の文として正しい。提出の版の前文を引くときは *"where that assumption fails"* へ替える（T72・T73） |
| 個別 | §16.4 の識別子の照合（T46）を引く文: `submission-osd.md` 149、`submission-reference.md` 667 が *"ACD-" followed by a digit* を条番号つきで引く | 1.4 では *"regardless of case"* が入る。提出の版の §16.4 を述べる文は替え、1.0〜1.3 の文として引く文は残す |
| 個別 | `REVIEWERS.md` の新規ライセンスの基準の表の *"Every possible variation"* の行（*"only the form of the notice varies"*）| 1.0〜1.3 の文として正しい（通知が名指す素材の規則は 1.4 の §16.2 で入った）。提出の版を 1.4 にする日は、採用者は通知が名指す素材も選べ、適用された素材の terms は同じで、留保だけの通知は素材を割り当てない（§16.2・T52）と書き替える。`SUBMISSION-MATERIALS.md` §1c の基準 5 の行（2026-11-11）と同じ中身 |
| 個別 | §8.4 の理由の文（T54 で外した）を引く文: `submission-reference.md` の *"would be read down"* と *"whether a trained model is"*、`review-responses-clauses.md` の *"would restore the exposure"* と「理由は §8.4 自身の本文に在る」の段 | 1.0〜1.3 の文としては正しい。提出の版を 1.4 にする日は、1.4 の §8.4 は理由を述べず、独立の許諾と §8.1 の限定が無いことだけを述べる、と書き替える。理由の説明は 1.4 の逐条リファレンスの §8.4 の行が持つ |
| 個別 | `submission-reference.md` の長さの行（*"How long the text is"*・1.0 は GPLv3 より短い）| 1.0 の文として正しい。1.4 を提出の版にする日は、1.4 は GPL-3.0 より長いこと（2026-11-12 の T60 の後の測定で本文 5,214 語・GPL-3.0 は 4,617 語。題名からは 5,555 語で GPL-3.0 の 5,644 語より短い）を同じ行に書き、1.0 の比較は版を名乗って残す。数は当日に測り直す |
| 個別 | `submission.md` §B.0 の本文の *ACD-1.0*（Check 472o）| 件名・冒頭・header・URL は 472f が見る。本文の 7 箇所のうち 6 箇所（OSD の宣言、gap、条件の段、§6.4 の段、§1.2 の段、*taken alone*）は版を替える。§1.2 の段は §1.3 へ替える。Provenance の *"The name ACD-1.0"* は履歴の文なので、版を替えず *"The name ACD"* とする |
| 個別 | §2.8・§5.3・§12.4 の承継の限度を *"to the fullest extent the law permits the Dedicator to bind them"* と引き、*"Section 12.4 uses the same formula"* と述べる文（T74〜T76）: `review-responses-clauses.md` 56・563 | 1.0〜1.3 の文として正しい。1.4 では §5.3 と §12.4 が人を §2.8 から借り（*"the persons Section 2.8 names"*）、限度は 3 条とも *"to the fullest extent the law permits"* で、§2.8 の末文は無い。提出の版を 1.4 にする日は、この 2 か所を 1.4 の語へ替える（portfolio-30 が見つけた） |
| 個別 | §11.3 の理由の文 *"because it was never the Dedicator's to permit"* を引く文（T77）: `against.md` #110 の行、`comparison.md` 528、`reviewer-positions.md` 504・630 | 1.0〜1.3 の文の引用としては正しい。ただし `reviewer-positions.md` 630 のように「Dedicator が持っていないものは渡せない」の論拠に使う段は、作者の表示では誤り（偽の帰属の権利は表示された本人のもので、英国 CDPA s.84・s.87(1) では本人の同意で侵害でなくなる）。提出の版を 1.4 にする日は、1.4 の §11.3（理由の文が無い）を引く。`submission-osd.md` の OSD 5 の行は、同じ命題を我々の地の文として述べていたので 2026-11-16 に直した（portfolio-30 が見つけた） |
| 個別 | §6.5 の *"silence on this subject has proved ambiguous in practice"* を引く文（T79）: `submission.md`、`against.md`、`discussion-log.md`、`review-corpus.md` | 1.0〜1.3 の文の引用としては正しい。ただし `submission.md` のように、この言明を我々の理由として使う文は、出典が無いまま提出文に写さない（portfolio-50 が `SUBMISSION-MATERIALS.md` に注を置く）。提出の版を 1.4 にする日は *"leaves it to be inferred whether this is permitted"* を引く |
| 個別 | §10.4 第 1 文 *"No permission granted by this Dedication terminates for any reason"* を引く文（T81）: `review-responses-clauses.md` 324（§8 の答え）・743（§12 の答え） | 1.0〜1.3 の文の引用としては正しい（743 の続き *"This Dedication contains no termination"* も 1.0 の文で、1.4 は *"in respect of the Work,"* が入る）。提出の版を 1.4 にする日は *"terminates under it, for any reason"* を引く（portfolio-9b が見つけた） |
| 個別 | §15.3 第 2 文 *"It is intended to operate under the law of each jurisdiction in which the Work is used"* を引く文（T92）: `against.md` #23、`review-readings-5.md`、`QUESTIONS-FOR-COUNSEL.md` 問 7 | 1.0〜1.3 の文の引用としては正しい。1.4 では §15.3 は第 1 文だけになる。提出の版を 1.4 にする日に読み直す |


### 切り替えの日に `REVIEWERS.md` の *Which text you are looking at* へ入れる英文（下書き・2026-11-11）

1.0 を `license-discuss` で読んだ審査者が、1.4 で何が変わったかを 1 画面で読める場所が無い。変更の一覧（`CHANGES-ACD-1.4.txt`・2026-11-20 までは草案の冒頭）は 1.3 からの差で、各版の CHANGELIST は版ごと・大半が日本語である。そこで切り替えの日に、番号の対応の段の前へ次の段を入れる。**数はどれも当日に数え直す** —— `python3 .github/scripts/prepare_version_freeze.py --report 1.4` の最後の段「1.0 から何が変わったか」が、errata の閉鎖の版ごとの数（最初の「N.M 草案で閉じた」の印）、印の無い行、節ごとの件数（表の 2 列目の最初の §・無いものは「—」）、両方の本文の語数と条の数を出す（portfolio-9b・PR 2824）。下の数は 2026-11-11 に同じ数え方で出した値で、書き写さない。

> **If you read ACD-1.0 on `license-discuss`, this is what is different in the version submitted.**
> The direction is unchanged: no condition is placed on You in respect of the Work (§10.1), the
> surrender, the licence and the covenant stand side by side (§2.4, §4.4), and the patent grant
> reaches models and outputs (§8.4). What changed is precision. Of the 87 defects recorded against
> 1.0 in [`ACD-1.0.errata.md`](ACD-1.0.errata.md), 83 are closed: 36 in 1.1 to 1.3 (19, 13 and 4)
> and 47 for the first time in 1.4. E10 is carried into finalisation and E6 is left as it is by
> design. E87 and E88, found after 1.4 was fixed, were examined and are likewise left as they are.
> By the clause
> each entry names first, most were in §8 (patents, 15), §16 (applying the text and its name, 13),
> §2 (scope and effect, 11) and §1 (definitions, 8); seven name the preamble or several clauses at
> once. Further changes came from our own sweeps of the
> later drafts and are listed, with their reasons, in each version's change list. The text is
> longer: 5,879 words from the title to *END OF TERMS* against 1.0's 4,896, in 80 clauses against 82.

**⚠ 逆側**: 短い経路の語数が約 170 語増える（`REVIEWERS.md` の短い経路の表と Check 472m の値を同じ日に直す）。*"The direction is unchanged"* は、1.0 から変わらなかったものを 3 つだけ挙げる文で、ほかに変わらなかったものが無いとは言っていない。逆に、変わったものを errata の件数で数えるので、errata に載らない 1.4 生まれの変更（T34〜T52 の多く）は *"Further changes"* の 1 文にまとまる。数を当日に数え直すのは、草案が確定まで動くからである（2026-11-11 の時点でも 1.4 の閉鎖は 39 件で、まだ動きうる。**同日の訂正**: 最初の下書きは 1.3 で 5・1.4 で 38 と書いた。状態の列の版の語の最初の一致を数えていて、閉鎖の印でない語を拾っていた。portfolio-00 が印の正規表現で 4 と 39 を出し、同じ数え方で確かめた）。


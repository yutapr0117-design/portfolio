---
file: LICENSES/ACD-1.0.review-readings-6.md
audience: OSI license-review / license-discuss participants, licence reviewers, 監査人
last-updated: 2026-11-15
reachable-via: ACD-1.0.review-readings.md
canonical-ref: LICENSES/ACD-1.0.review-readings.md / LICENSES/ACD-1.0.review-readings-2.md / LICENSES/READ-THREADS.txt / LICENSES/AS-OF.md
---

# 未読のスレッドを読んだ記録（節 1.450 から・2002〜2003 と 2009〜2010 のスレッド）

2026-11-15、オーナーの依頼「未読の OSI スレッドを 5 人で無くして、反映して」で、census の未読 285 本を年の帯で 5 人に分けた（30 の割り振り・2f の書き場所の案）。この文書は 2002〜2003 と 2009〜2010 に始まるスレッドの記録で、節番号は 1.450 から使う（帯を分けたので、番号は文書をまたいで重ならない・Check 500 が重複を止める）。書き方は `ACD-1.0.review-readings-2.md` と同じである: 原文を引き、発言者と日付を書き、ACD への当たり方と逆側を同じ表に置き、最後に「この節が establish しないこと」を書く。論点の無い会話は節を作らず、`record_read.py --log-only` で読了だけを記録する。

## 1.450 ライセンスについて書いた物は、前文でも別の解説でも、条文の解釈に使われる —— だから最良の本文を書いて、あとは黙れ、と Nelson 氏は書いた（"Static v. Dynamic Linking -- redux"・2002-03）（2026-11-15）

"Static v. Dynamic Linking -- redux"（`license-discuss` 2002-03・13 通）を通読し、1 通を置いた（`rounds/2002-03-license-discuss-static-dynamic-nelson-interpret-observed.txt`）。静的リンクと動的リンクのどちらが二次的著作物を作るかを Lawrence Rosen 氏が論じた会話で、裁判官が意図をどう読むかに話が移った。Russell Nelson 氏は当時の理事で、同じ年の別の会話で「今日の理事会でこの件を出す」と書いている（"OpenE License"・2002-02-27）。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"In a lawsuit, the judge will interpret the license to try to divine your intention. That is why anything you write in or about a license -- even if it's "just" a preamble and postamble, or in a separate commentary -- is used to interpret the terms of the license."* | Russell Nelson 氏 2002-03-16（同じ通の冒頭で *"Again, I must stress that this is not based on experience, but instead on learning."* と断っている） | **不利な面（B13・`against.md` #124 の逆側）。** #124 は Pamela Chestek 氏 2026-09-01 の、本文の外の文を裁判所が考慮する義務は無い、という文を引き（逐語は #124 に在る）、ドシエの説明は本文の曖昧さを直さない、と記録した。Nelson 氏の読みはその反対の向きで、本文の外に書いた物も意図を探る材料になる。**2 つは両立する**: 外の説明は本文を直す力を約束されず（Chestek 氏）、しかも読まれうる（Nelson 氏）。ACD のドシエは本文の約 100 倍の語数があり（`REVIEWERS.md` 冒頭の実測・2026-11-15）、`against.md` は ACD の文の不利な読みを自分で書いている。裁判官がそれを Dedicator の意図として読むと、我々が「こう読まれうる」と書いた不利な読みが、意図の証拠として働く向きがある |
| *"That's why you do best to write the best license you can, and then shut up about it."* | Russell Nelson 氏 2002-03-16 | **不利な面（B3・B13）。** ACD の本文は §6.5・§8.2・§8.3 で理由を述べ、ドシエは本文の約 100 倍ある（同じ実測）。「黙れ」の反対側に立っている |

**読み。** 2002 年の理事は、ライセンスについて書いた物は（本文の外の解説も）意図を探る材料として使われる、と書いた。2026 年の元委員長は、本文の外の説明を裁判所が考慮する義務は無い、と書いた。決める側の 2 人の読みは向きが逆で、どちらも「外の説明で本文の曖昧さを直す」ことは当てにできない、という点で一致する。

**逆側。** Nelson 氏は法律家ではなく、自分で「経験ではなく学んだこと」と断っている。ACD の本文（1.4 草案）は §15.1 で、読みが分かれるときは受け手に多く与える読みが勝つと定め、§15.6 で起草者に不利に解する原則と付与を狭く解する原則の両方を外している。ドシエの不利な読みが意図の証拠として持ち出されても、本文の §15.1 がその向きを受け手に有利な側へ倒す。ただし §15.1 が裁判所を拘束するかは、それ自体が本文の外の法の問いで、ここでは決まらない（B1）。

**この節が establish しないこと。** 2002 年の米国で、ライセンスの外の解説が実際に解釈に使われた判決を、この会話は挙げていない。ACD のドシエが解釈に使われた事例は無い（ACD を争った訴訟は無い）。

**反映**: against #124（逆側の補強 —— 外の説明は直す力を約束されず、しかも読まれうる・30 へ）/ B13（ドシエの不利な読みが意図の証拠として働く向き・`QUESTIONS-FOR-COUNSEL.md` に問いとして足す候補・30 へ）。本文は変えない（1.4 草案の §15.1・§15.6 が既にその向きを扱う）。

## 1.451 「コピーを持っているなら、それで何をしてもよい」と OSD は言うべきだった —— 使用に条件を付けるライセンスを、理事は意図して承認したことが無いと書いた（"Advertising Clauses in Licenses"・2002-01〜02、"NCSA Open Source License"・2002-01）（2026-11-15）

"Advertising Clauses in Licenses"（`license-discuss` 2002-01〜02・39 通）と "NCSA Open Source License"（`license-discuss` 2002-01・19 通）を通読し、3 通を置いた（`rounds/2002-02-license-discuss-advertising-nelson-use-observed.txt`・`rounds/2002-01-license-discuss-advertising-perens-run-observed.txt`・`rounds/2002-01-license-discuss-ncsa-rosen-no-opinion-observed.txt`）。広告条項（バッジウェア）を OSD がどう扱うかの会話で、Bruce Perens 氏が OSD に「使用への負担」を禁じる文を足すことを提案した。

| 発言 | 誰が | ACD への当たり方 |
| :-- | :-- | :-- |
| *"One of the goals of the OSD was to have software that the user could run without having to read the license or take any special action."* | Bruce Perens 氏 2002-01-20（OSD の起草者） | **有利な面（B10）。** ACD の §10.1〜§10.4 は、受け手に条件・義務・制限を課さず、何も知らせなくてよいと定める。OSD の起草者が述べた目標を、条件を持つライセンスより文字どおりに満たす |
| *"Unfortunately, the OSD is not very well written. For example, it says nothing about use, so multiple parties have tried to say "Yeah, you can copy this software, but in order to use it, you have to license it from us." We squashed them using #7 (fortunately!), but the OSD really ought to say "If you have a copy of this software, you can do anything you want with it.""* | Russell Nelson 氏 2002-02-13（当時の理事） | **有利な面（B10・B4）。** ACD の §3 と §6.1 は、コピーを持つ者が何をしてもよいことを、使用を含めて書いている。理事が「OSD が言うべきだった」とした文の形に、ACD の本文は近い |
| *"The OSI board of directors approves licenses if they are consistent with the OSD. The board renders no opinion about the validity or enforceability of specific clauses in specific licenses."* | Lawrence Rosen 氏 2002-01-20（当時の OSI の法律顧問） | **有利な面と不利な面（B1）。** 承認は OSD との整合で決まり、条項の有効性の意見ではない —— B1（法的レビューが無い）は承認の基準そのものではない、という読みを支える。ただし同時に、承認は ACD の §3 や §4 が各国で有効だとは言わない。審査者が有効性を論じないなら、ACD の有効性の問いは承認の後も残る |

**読み。** 2002 年の決める側の 3 人は、使用に条件を付けないことを OSD の目標（Perens 氏）、OSD に書かれるべきだった原則（Nelson 氏）として述べ、承認は条項の有効性の意見ではない（Rosen 氏）とした。ACD の「条件を一切課さない」設計は、この 3 つの文と同じ向きにある。

**逆側。** 同じ会話で Nelson 氏は *"We've never intentionally approved use-restricted licenses before."* と書いたが（"OSD modification regarding what license can require of user"・2002-03-16）、それは条件を持つライセンスの話で、条件を持たないライセンスが承認に有利だとは言っていない。条件が無いことは OSD の下限を越えるだけで、B10（既存の許容的なライセンスで足りるのでは、という問い）には答えない —— MIT や 0BSD も使用に条件を付けない。また Rosen 氏の文は 2002 年の理事会の運用で、2026 年の Licensing Committee が条項の有効性を論じる例（`against.md` #124 など）とは時代が違う。

**この節が establish しないこと。** Perens 氏が提案した OSD の追加の文が採られたかは、この会話の範囲では確かめていない。

**反映**: B10（有利な面 —— 決める側が 2002 年に「使用に条件を付けない」を OSD の目標と原則として述べた・逆側は MIT と 0BSD も同じ・30 へ）/ B1（Rosen 氏 2002 —— 承認は条項の有効性の意見ではない・有利と不利の両面・30 へ）/ 入口（「条件を一切課さない」の説明に OSD の起草者の目標を引く候補・50 へ）。本文は変えない。

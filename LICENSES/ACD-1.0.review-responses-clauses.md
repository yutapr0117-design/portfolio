---
file: LICENSES/ACD-1.0.review-responses-clauses.md
audience: ai, human (提出者), 監査人, 第三者全般
last-updated: 2026-11-28
canonical-ref: LICENSES/ACD-1.0.review-responses.md (総論・索引) / LICENSES/ACD-1.0.txt (凍結中の本文・唯一の権威)
---

# ACD-1.0 — 想定問答（条項別）

> **この文書の "I" は誰か（2026-11-25）**: 英語の引用ブロックの一人称は、AI のモデル（Claude）が書いた想定の声で、オーナー（横井雄太）の言葉ではない。リストへ送る文でもない —— 投稿と返信は、オーナーが自分の言葉で書く（B14・`REVISION-PROTOCOL.md` ゲート 0）。**In English:** where a quoted block below says "I", an AI model wrote it as a possible line of answer. It is not the steward speaking, and it is not text to be sent to a list.

**総論・OSD 逐条・認める弱点・議論の進め方は `ACD-1.0.review-responses.md` にある。本書はその条項別の分冊。**

条項レベルの指摘は「その条文を読めば答えが出る」ように見えて、実際には**なぜその形で書いたか**を答えないと納得されない。本書は条文ごとに「想定される指摘 → 答えの材料になる英文（AI が書いた・写して送らない） → なぜそう答えるか」を並べる。

**本書は非規範。** ここに書いた回答が ACD-1.0 の意味を変えることはない。本文が唯一の権威である。

---

### §2 SCOPE AND EFFECT

**Q. §2.2「irrevocable」と言うが、各国法で本当に撤回不能か。**

> **English:**
>
> Section 2.2 states the Dedicator's position; it does not claim to override a
> jurisdiction that provides an inalienable withdrawal right (Germany's
> Rückrufsrecht wegen gewandelter Überzeugung, for instance). That is what
> Section 15.4 is for: a provision held unenforceable in a jurisdiction is
> reformed to the minimum extent necessary there and severed as to that
> jurisdiction only. In practice a user's protection against a change of heart
> is the layering, not the word "irrevocable" — Section 5 is a covenant not to
> assert, which is enforceable on ordinary contract or estoppel grounds in most
> systems even where the surrender in Section 3 is not.

**Q. 裁判所が献呈を bare license と見て禁反言を認めなければ、§2.5 は働かない。そのとき、対価が無いことを理由にした撤回から受領者を何が守るのか。（2026-11-11 追加）**

問いの元は Lawrence Rosen 氏（`license-discuss` 2004-01-27）—— *"I don't think your analysis is correct. Promissory estoppel is a contract doctrine that has nothing to do with a bare license like the GPL."*（`rounds/2004-to-2026-license-lists-bare-licence-and-extrinsic-statements-observed.txt`）。

> **English (ACD-1.4):**
>
> If a court treats the Dedication as a bare licence and refuses estoppel, Section 2.5 does no
> work, and recipients depend on other clauses. Section 3.1 is an irrevocable surrender and
> abandonment rather than a licence, so where a jurisdiction gives it effect there is no licence
> left to revoke. Section 4.1 calls the licence irrevocable, and Section 4.4 makes it independent
> of Section 3. Sections 5.1 and 8.6 are covenants not to assert. We have no record that any of
> these survives an argument of want of consideration. Our own answer above says the Section 5
> covenant is enforceable "on ordinary contract or estoppel grounds", and those are the grounds
> this case removes. "Irrevocable" in Section 2.2 states the Dedicator's position; it does not
> override the law. Whether any of these clauses holds in that case is open.

**なぜこう答えるか**: §2.5 は依拠と禁反言に立つので、禁反言が働かない読みでは他の条に頼るしかない。その条もそれぞれ、効くかどうかが法域の問いである。上の §2.2 の答えは「契約か禁反言で守られる」と書いており、この問いはまさにその両方を外す。答えられないことを答えられないと書く（`against.md` #236 が Rosen 氏の異論を未回答として記録している。`QUESTIONS-FOR-COUNSEL.md` は問 1 の (i) で、禁反言が働かないとき何が受領者を守るかを法律家に尋ねる —— 2026-11-12 に portfolio-aa が足した）。portfolio-aa が審査者の問いを当てて残った 1 件である。同じ問いは 2003 年に list で問われ、答えが出ないまま終わっている。Rosen 氏は放棄の代わりに *"Grant an irrevocable license."* と勧め、翌日には *"I don't know why it would any different if one granted an "irrevocable" open source license, and then revoked it. Probably a new licensee with notice of the revocation can't obtain a license."* と書いた（`gap-measurements.md` §1.146 の 2026-11-12 の追記）。§4.1 が撤回できないと書いていても、対価が無いという議論に耐えるという記録は無い、という上の答えは、この記録と同じ向きである。2003 年の文も *"Probably"* と書いた見通しで、答えではない。もう 1 つの道も ACD には無い。2000 年と 2005 年に GPL について論じられたのは、受領者の義務（ソースを配ること、帰属を表示すること、免責を受け入れること）が対価になって契約が成り立ち、撤回を防ぐ、という道だった。ACD は受領者に何も課さないので、受領者が満たした条件を対価として挙げられない（`against.md` #324・`review-readings.md` §1.191）。条件を課さないことは設計の中心で変えないので、これはその費用として答えの中で述べる。

**Q. §2.8 が承継人を拘束すると書いているが、そんなことができるのか。**

> **English:**
>
> Only "to the fullest extent the law permits the Dedicator to bind them" —
> Section 12.4 uses the same formula. The clause is doing two things. It states
> the Dedicator's intent, which matters for construction under Section 15.1, and
> it puts a successor on notice, which is what makes an estoppel argument
> available to a user who relied. It is not an assertion that a bankruptcy
> trustee is bound in every system. Section 2.8's stated concern with insolvency
> is there because that is the most common route by which rights reach someone
> who never made the promise.

**2026-11-28 追記 — 米国の譲受人に対する優先は、署名のある書面が要る（`QUESTIONS-FOR-COUNSEL.md` 問 1 (j) の材料）**: 17 U.S.C. §205(e) は、非独占の許諾が後の著作権の譲渡に優先するのは、その許諾が *“a written instrument signed by the owner of the rights licensed”* で示され、かつ譲渡の前に取られたか、譲渡の記録の前に善意で通知なく取られた場合に限ると定める。ACD-1.4 §16.1・§16.2 の通知だけの適用（署名なし）はこの形式を満たさない。したがって §2.8 の *“to the fullest extent the law permits”* は、この点では法定の優先を与えず、譲受人に対する拘束は §2.8 の意思表示と通知による禁反言の余地に留まる。

米国著作権局は、放棄をうたう宣誓供述書・宣言・陳述・その他文書を記録する（Compendium of U.S. Copyright Office Practices, 3rd ed., §2311 *“Abandonment”*。2026-11-28 に原文で確認）。要件は、放棄の対象の特定（著者・題名・登録番号が望ましい）、署名者の氏名、現在の権利者である旨の陳述、放棄した旨の陳述、現在の権利者（ら）の実際の署名、手数料である。記録された文書は公開記録になり、記録の証明書が返される。ただし著作権局は *“without offering any opinion as to the legal effect of the document”* と述べ、記録が放棄を有効にするとは言わない。

記録が擬制通知になるのは、文書が著作物を具体的に特定し、かつその著作物が登録されている場合に限る（17 U.S.C. §205(c)）。ACD の対象の多くは未登録なので、記録しても擬制通知は得られず、実際の通知（Work とともに公開された §16.2 の識別子）に頼るほかない。

同じ署名のある書面は、VARA の放棄の形式要件（17 U.S.C. §106A(e)(1)：著者が署名した書面で、著作物とその使用を具体的に特定）にも、カリフォルニア州法 CAPA の放棄の形式要件（Civil Code §987(g)(3)：著者が署名し、明示的にその旨を定めた書面）にも近づく。1 つの署名が 3 つの形式要件にまとめて働く方向がある。本文は今のところ署名のある適用を勧めていない（`ACD-1.5-DRAFT.txt` §10 にその旨の項は無い）。

**正直な限界**: 記録が放棄を有効にするとは限らない（Dixon 氏 2000 年の見通しはこの記録では覆らない。`jurisdictions.md` §5d）。§203 の終了権は署名では防げない。署名のある git コミットが §205(e) の「署名」に当たるか（E-SIGN 法 15 U.S.C. §7001 の射程）は確かめていない。

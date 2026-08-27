---
file: LICENSES/ACD-1.0.faq.md
audience: 採用検討者, 法務, ai, human (提出者), 監査人, 第三者全般
last-updated: 2026-08-27
canonical-ref: LICENSES/ACD-1.0.txt (凍結中の本文・唯一の権威) / LICENSES/ACD-1.0.clause-reference.md (逐条リファレンス) / LICENSES/ACD-1.0.comparison.md (族ごとの比較) / LICENSES/ACD-1.0.jurisdictions.md (法域別の問い)
---

# ACD-1.0 — 実務 FAQ（使う人・法務・観察者向け）

```
本書の役割 : レビュアではなく **実際に使うかもしれない人**の疑問に答える
本書の性質 : 非規範。齟齬があれば本文が勝つ。法的助言ではない
関連       : 逐条は clause-reference / 族比較は comparison / 法域は jurisdictions /
            レビューの想定問答は review-responses{,-clauses,-meta}
```

---

## A. 使う側の疑問

### A1. 自分の作品に使ってよいか

> **English:** Yes, without asking. Section 16.3 states that this Dedication may be applied by
> anyone, to any work, without permission from, notice to, or any relationship with its
> authors, and that it is not specific to any project, person, organisation, jurisdiction or
> field. Section 16.1 gives the notice form.

**先に確認すること**: **あなたがその作品の権利を持っているか**。職務著作や譲渡で雇用主が権利を持つ場合、あなたは適用できる立場にない（**A20** 参照）。共同で作ったものなら **A13** も見ること。

**適用の仕方**: §16.1 の書式の通知を作品に添える。全文の同梱は不要で、
**識別子だけでも通知として足りる**（§16.2）。

### A2. 通知や帰属表示を残す必要はあるか

> **English:** No. Section 10.2 says in terms that You need not give attribution, reproduce any
> notice, state that the Work was modified, make source available, license anything under
> these or any other terms, **retain this file**, or inform anyone of anything.

**README に「引用してください」と書いてあった場合も同じ**である。§10.3 が「依頼は依頼であって
条件ではない。従わなくても違反ではなく、いかなる許諾も終了しない」と明示している。

### A3. 改変して再配布するとき、何をすればよいか

> **English:** Nothing is required. You may distribute the Work and any adaptation under **any
> terms You choose**, including terms that impose conditions on Your recipients and terms
> incompatible with these (Section 4.5). You need not mark changes (Section 10.2).

ただし §4.6 が、**あなたが付けた条件は「あなたが与えるもの」を規律するだけ**で、受領者と本
Dedication の関係を切らないと定めている。受領者は自分の権利として §1.4 の "You" になる。

### A4. 商用利用・軍事利用・その他の用途制限はあるか

> **English:** None. Section 4.3 excludes conditions on field of use and on "the identity,
> character, or purpose of the user" in terms, and Section 6.1 permits computational use for
> any purpose. There is no acceptable-use policy and no scale threshold.

### A5. GPL / Apache のプロジェクトに取り込めるか

> **English:** Yes. Because there is no condition to satisfy (Section 10.1), the Work can be
> combined with material under any licence, and the combination can be distributed under that
> licence's terms (Section 4.5). Nothing flows back from this instrument to constrain the
> combined work.

**逆向き**（ACD-1.0 の作品に GPL のコードを混ぜる）は**別の話**である。混ぜた相手の条件は
その相手のライセンスが決めるので、**GPL コードを取り込めば結果物は GPL の条件に従う**。
本 Dedication は §2.7 のとおり **Dedicator が持つ権利にしか及ばない**。

### A6. 特許を持っている。適用してよいか

> **English:** Only if You are willing to license them. Section 8.1 grants a licence under
> every patent claim You own or control that would be infringed by the Work, Section 8.4
> extends it to computational use and its outputs, and Section 8.3 rejects any reading that
> preserves patents. If You are not willing to do that, this is the wrong instrument.

**これは適用者側の判断であって、利用者側の心配ではない。** 利用者から見れば §8.5 のとおり
「Dedicator が持つクレームにしか及ばない」ので、第三者特許の risk は別に残る（§13.2 が
非侵害を保証しないと明言）。

### A7. データセットやモデルに使えるか

> **English:** Yes. Section 1.2 defines the Work to include data, metadata and audiovisual
> material as well as source and object code. Section 7 addresses the sui generis database
> right explicitly, and Section 7.2 permits repeated and systematic extraction and
> re-utilisation of substantial parts.

### A8. 学習に使ってよいか。学習して作ったモデルや出力は自由か

> **English:** Yes to both. Section 6.1 permits computational use for any purpose; Section 6.2
> states that no reservation is made; Section 6.4 says no model, parameter set, weight,
> embedding or output derived from the Work is subject to this Dedication or to any claim of
> the Dedicator arising from it; Section 8.4 grants the corresponding patent licence, because
> Covered Rights exclude patents (Section 1.5) and a copyright-only permission would leave a
> patent-shaped hole.

### A9. 作者が気を変えたら / 亡くなったら / 会社が破産したら

> **English:** Section 2.2 makes the Dedication irrevocable. Section 2.5 states that reliance
> is its purpose and that the Dedicator will not argue it is revocable for want of
> consideration or formality. Section 2.8 binds successors, assigns, heirs and transferees to
> the fullest extent the law permits, and Section 2.9 addresses insolvency specifically —
> the Dedication is fully performed when applied and so is not executory.

**どこまで拘束できるかは法域による**（`ACD-1.0.jurisdictions.md` 参照）。条文は
「法が許す限り」と書いており、**拘束できると断言はしていない**。

### A10. SPDX 識別子が無い。ツールにどう書けばよいか

**これは現時点の実務上の最大の不便である。** ACD-1.0 は SPDX License List に**未登録**
（実使用が薄いため意図的に見送っている）なので、SPDX ドキュメントでは
**`LicenseRef-` を付けた形**で参照するのが標準的な扱いになる。

> **English:** ACD-1.0 is not on the SPDX License List, so in an SPDX document it should be
> referenced as a user-defined licence — conventionally `LicenseRef-ACD-1.0` — with the full
> text supplied in the corresponding `ExtractedLicensingInfo` (or your tool's equivalent).
> The tag inside the Work itself (`SPDX-License-Identifier: ACD-1.0`, per Section 16.1) is the
> notice form the Dedication defines; it is not a claim that the identifier is registered.

**§16.1 の通知が `SPDX-License-Identifier: ACD-1.0` を含むのは矛盾ではない** —— §16.2 が
「識別子や名称への言及だけで通知として足りる」と定めており、これは**登録の主張ではなく
通知の様式**である。

### A11. 依存関係スキャナが「未知のライセンス」と言う

想定内である。未登録の識別子はスキャナのデータベースに無い。実務的には次のいずれかになる。

1. `LicenseRef-ACD-1.0` として手動登録し、全文を添える（A10）
2. 組織のポリシー上「無条件・特許許諾あり」に相当する分類（例: public domain / permissive
   with patent grant）へ手動でマップする
3. **判断できないなら使わない** —— それは正当な選択であり、こちらから止める理由は無い

> **English:** If your tooling cannot classify it and your policy requires a listed licence,
> the correct answer is to wait. I would rather you decline than adopt something your process
> cannot account for.

### A13. 既存プロジェクトを ACD-1.0 へ移行できるか

**「自分が全ての権利を持っているか」で答えが変わる。**

> **English:** If you hold all the rights, yes — Section 16.3 lets anyone apply this to any
> work without permission. If other people have contributed, you cannot relicense their
> contributions unilaterally. You need either their agreement, or a prior licence that
> already permits what you are about to do (a permissive licence generally lets you
> sublicense; a copyleft one generally does not let you drop its conditions).
>
> Two things are worth saying plainly:
>
> - **Applying this does not reach past distributions.** Copies already released under the
>   old licence stay under it. Recipients keep what they were given.
> - **Applying this is irrevocable** (Section 2.2), and Section 2.5 says the Dedicator will
>   not later argue otherwise. If you are not certain, do not apply it yet.

**§2.6 が助けになる場面**: 今後の貢献については、貢献者が別段の意思表示をしない限り
本 Dedication の下で提出されたものとして扱われ、**CLA のような別文書を要求できない**。
ただしこれは**将来の貢献**についての規律であって、**過去の貢献を遡って変えるものではない**。

### A14. 輸出規制・制裁法との関係は

> **English:** This instrument grants intellectual-property permissions and nothing else.
> Export control, sanctions, and similar public-law obligations are not the Dedicator's to
> grant or to waive, and Section 11.4 states the general shape of that limit: this Dedication
> reaches Covered Rights, the patent claims described in Section 8, and Moral Rights to the
> extent stated in Section 12 — **it reaches nothing else**.
>
> Because the licence imposes no condition (Section 10.1), it adds no export-related term of
> its own. It also removes none of your obligations under the law that applies to you.

**「無条件」は「法的義務が消える」という意味ではない。** §2.7・§11.4・§13.2 が一貫して
**「Dedicator が持っているものしか渡せない」**と述べており、公法上の義務はその外側にある。

### A15. 公共調達・組織のポリシーで「OSI 承認済み」が要件になっている

**その場合は使えない。** ACD-1.0 は **OSI 承認を受けていない**（`license-discuss` へ投稿した
段階で、承認申請の窓口である `license-review` へも未投稿）。

> **English:** If your policy requires an OSI-approved licence, ACD-1.0 does not qualify today
> and I would not want you to argue otherwise on my behalf. The current status is recorded in
> `LICENSES/FROZEN.md`, and I would rather you wait — or use an approved licence — than
> spend your own credibility on an unapproved one.

**これは採用者を減らす記述であり、意図的である。** 承認されていないものを「実質的に同等だ」と
言わせるのは、こちらの都合で相手の信用を使わせることになる。

### A16. SBOM にはどう記載すればよいか

**A10（SPDX 識別子が無い問題）の実務面である。** SBOM（SPDX / CycloneDX いずれの形式でも）は
ライセンスを識別子で持つので、**未登録の識別子はそのまま書けない**。

> **English:** Record it as a user-defined licence entry — `LicenseRef-ACD-1.0` in SPDX terms —
> and attach the full text, which is short enough to embed. Do **not** map it to a
> superficially similar listed identifier (CC0, 0BSD, Unlicense) just to make the tool quiet:
> those differ on patents, which is the one place where the difference has teeth (Section 8.3).

**「似ているから」で既存識別子に丸めないこと。** とくに CC0 は**特許を明示的に除外**して
おり（§8.3 が拒絶する結果そのもの）、丸めると SBOM が**実態と逆のことを記録する**。

### A17. fork / vendoring / ミラーは自由か

> **English:** Yes, and nothing is required. Section 4.5 permits distribution of the Work and
> any adaptation under any terms You choose; Section 10.2 says You need not retain this file,
> reproduce any notice, or state that the Work was modified. Vendoring into a monorepo,
> mirroring, and forking are all ordinary uses.

**ただし §4.6** —— あなたが付けた条件は「あなたが与えるもの」を規律するだけで、
**受領者と本 Dedication の関係を切らない**。fork を閉じた条件で配っても、元の Work に
ついては受領者が自分の権利として §1.4 の "You" になる。

### A18. 名称や識別子は商標登録されているのか

**されていない。** §11.1 は「商標・サービスマーク・商号・ロゴ・氏名の権利を与えない」と
述べるが、これは**存在する商標を留保する**条項であって、**商標を主張する**条項ではない。

> **English:** No trademark is claimed or registered. What keeps "ACD-1.0" pointing at one
> fixed text is **not** trademark law but Section 16.4: the text may be copied verbatim by
> anyone, and a modified text may not be distributed under the name or the identifier. A
> modified text may circulate freely — under a different name.

**なぜ商標ではなく条文で守るのか**: 商標は登録・維持・行使のコストを steward に課し、
**§13.3 が保守義務を負わないと述べているのと整合しない**。§16.4 なら、守る主体が消えても
条文としての意味は残る。

### A19. ACD-1.0 を「廃止」できるのか

**適用済みの作品については、できない。** §2.2 が撤回不能と定め、§2.5 が「後から
無効だと主張しない」と述べている。**すでに配られたものは戻らない。**

> **English:** Deprecation, if it ever happens, can only mean "stop recommending it for new
> works". It cannot mean withdrawal: Section 2.2 is irrevocable and Section 2.5 forecloses the
> argument that it was not. The text itself is immutable under Section 16.4, so a successor is
> a new identifier, not a replacement of this one.

**これは cost として認めている**（想定問答 clauses 分冊 §32）。後から静かに直せない代わりに、
**識別子が指すものが動かない**という性質を得ている。

### A20. 会社員が業務で書いたコードに適用してよいか（職務著作）

**これは「適用してよいか」ではなく「あなたが権利を持っているか」の問題である。** そして
**実務で最も多い取り違え**でもある。

> **English:** Section 1.3 defines the Dedicator as each person or entity applying this
> Dedication **"to the extent that person or entity holds or may hold Covered Rights in it"**.
> If your employer holds the rights — through a work-for-hire rule, an employment agreement,
> or an assignment — then you are not the person who can apply this, and applying it does not
> transfer anything you do not have (Section 2.7).
>
> The instrument does not warn you about this and cannot: Section 13.2 disclaims any warranty
> that the Dedicator holds any right in the Work. **Check before you apply it, not after.**

**§2.2 が撤回不能である以上、間違って適用しても取り消せない**（少なくとも、こちらから
取り消す手段は用意していない）。**A13（移行）と同じ確認が要る。**

### A21. FRAND 宣言している特許を持っている場合、§8 と衝突しないか

> **English:** Section 8.1 grants a licence under patent claims the Dedicator **owns or
> controls**, and Section 8.5 states that Sections 8.1 to 8.4 are subject to Section 2.7 —
> they reach only what the Dedicator can license. A commitment already made to a standards
> body is an obligation the Dedicator has to that body; this instrument neither overrides it
> nor purports to. If your ability to grant is constrained by an existing commitment, then
> what Section 8 grants is correspondingly constrained.
>
> I state the structure rather than the conclusion, because how a prior commitment interacts
> with a later unconditional grant is exactly the kind of question I have not had counsel look
> at (`ACD-1.0.jurisdictions.md` §9).

**構造だけ述べて結論を述べていない**のは、`jurisdictions.md` と同じ姿勢による。
**助言を得ていない領域で断定しない。**

### A12. 法務に説明するとき、何を見せればよいか

| 訊かれること | 見せる場所 |
|---|---|
| 条件はあるか | 本文 §10.1 / §10.2 / §4.3 |
| 特許はどうなるか | 本文 §8.1 / §8.4 / §8.5 |
| 何を保証しているか | 本文 §13.1 / §13.2（**4 つとも否定**している） |
| 我々の法域で効くか | `ACD-1.0.jurisdictions.md`（**結論は書いていない**と明記） |
| 既存ライセンスとの違い | `ACD-1.0.comparison.md` / `acd-license-rationale.md` §2 |
| 条項ごとの意図 | `ACD-1.0.clause-reference.md`（全 82 条） |
| 弱点 | `READY-TO-SUBMIT.md`「残る弱点」/ 想定問答 §4 |

**弱点の場所を先に示すこと。** 法務が自分で見つけると、その後の説明が全部疑われる。

---

### A22. コード以外（画像・音声・埋め込みメタデータ）も対象か。第三者の資産はどうなるか

**このリポジトリが同梱している資産は、すべて ACD-1.0 の対象である。** §1.2 の "Work" は
source / object / documentation に加えて **data / metadata / audiovisual** を明示的に含む定義
なので、コードと非コードで扱いが分かれることはない。実測（2026-08-27）で追跡対象の資産は
4 件だけである。

| 資産 | 扱い |
|---|---|
| `yuta-yokoi-ai-pm-orchestration-system.webp` | 対象。**XMP に埋め込まれた AIO メタデータも Work の一部**（§1.2 が metadata を含む） |
| `yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3` | 対象。ID3 の埋め込みフィールドも同様 |
| `icon.svg` | 対象 |
| `e2e/.../homepage-baseline-chromium-linux.png` | 対象（テストの基準画像） |

**埋め込みメタデータを「別扱い」にしない**のは意図的である。AIO 層は「同じ主張がどの面でも
一致していること」で成立しており、本文だけ自由でメタデータだけ許諾が違う、という状態は
その主張自体を壊す。剥がす・書き換える・別の作品へ移すことも自由で、条件は課さない
（§10 / §11 が「条件ではない」と繰り返すとおり）。

**一方、同梱していない第三者の資産には及ばない。これは制限ではなく、及ぼしようがないという
事実である。** 具体的には Web フォント（`fonts.googleapis.com` / `fonts.gstatic.com` から
実行時に読み込む）で、**リポジトリには 1 バイトも入っていない**。したがって ACD-1.0 が
それらの権利を許諾することはあり得ず、利用者は提供元の条件に従う。逆に言えば、この
リポジトリを丸ごと複製しても第三者資産の権利問題は発生しない —— 複製しているのは
「そこへの参照」だけだからである。

**確かめ方**: `git ls-files` で追跡対象の資産を数え、`index.html` の外部参照ホストを見れば、
同梱されているものと参照しているだけのものは 1 分で切り分けられる。ライセンスの主張を
信じる必要はなく、**実測で確認できる**形にしてある。

### A23. 派生物に別のライセンスを付けてよいか。逆に、他人の貢献はどう扱われるか

**付けてよい。制限は無い。** ACD-1.0 は権利を留保しないので、派生物へ GPL でも Apache-2.0 でも
プロプライエタリでも、好きな条件を付けられる。copyleft のような「同じ条件で配れ」という
要求は存在しない（§10 / §11 が「条件ではない」と繰り返すのはこのため）。

ただし正確に言うと、**あなたが付けたライセンスが及ぶのはあなたの寄与部分だけ**である。
元の部分は ACD-1.0 のまま誰でも自由に使える —— あなたが派生物に条件を付けても、
**上流のテキストから直接受け取る人の自由は減らない**。これは ACD-1.0 に限らず、
留保しない型の instrument に共通する帰結である。

**逆方向（他人がこのリポジトリへ貢献する場合）。** CLA も DCO も要求していない。貢献者は
自分の寄与について自分で権利を持ち、それをどう扱うかは貢献者が決める。ただし
**ACD-1.0 が適用されるのは適用者が権利を持つ部分だけ**なので、第三者の寄与を取り込んだ場合、
その部分についてまで「権利を留保しない」と宣言できるわけではない（§2.7 が他の権利者の
留保に触れないと述べるとおり）。

**現時点でこの区別が問題にならない理由**も述べておく。このリポジトリの実装コードは
**すべて AI が生成し、人間はコードを 1 行も書いていない**（C5）。外部からの pull request は
受け入れていないので、取り込まれた第三者の著作物は存在しない。将来受け入れるなら、
その時点で「どの部分が誰の寄与か」を記録する必要が生じる —— **いま無いから書いていない
のではなく、いま無いことを確かめたうえで書いていない**。

## B. プロセスの疑問

### B1. いまどの段階か

`LICENSES/FROZEN.md` の `VENUE-DATA` marker が**単一ソース**である（Check 458 が
5 ファイルとの整合を BLOCKING で強制）。現時点では **OSI `license-discuss`（一般的な議論
リスト）へ投稿済み・反応待ち**で、承認申請の窓口である `license-review` へは未投稿、
SPDX も未提出である。**承認の手続きはまだ何も始まっていない。**

### B2. OSI が却下したら / 反応が無かったら

**却下は結果であって失敗ではない。** 想定問答 meta 分冊 Q20 に**撤回すべき条件を事前に**
書いてある（既存 1 本で 3 つの gap が埋まると示された / dedication 形式を扱わないと述べられた /
§4 が独立の許諾として機能しないと指摘され反論できなかった / 実使用 1 件では対象外と述べられた）。

**反応が無かった場合も事実として記録する** —— `ACD-1.0.discussion-log.md` が空のままなら
「スレッドは反応を得られなかった」と書くのが正しく、起きなかった議論を匂わせるより良い。

### B3. SPDX にはいつ出すのか

**実使用が増えてから。** SPDX は「相当程度の実使用」を求めるが、現在の使用実績は本リポジトリ
1 件である。**満たしていないものを出さない**という判断であって、順序の都合ではない。

### B4. ACD-1.1 はいつ作るのか

**指摘を受けて、直すべきだと判断したとき。** ただし審査中はテキストを動かさない
（Check 453 が sha256 で凍結を機械強制する）。妥当な指摘への正しい返答は
「**ACD-1.1 でこうする**」であって、審査側が見ているテキストの差し替えではない。

§16.4 により **1.0 のテキストは恒久的に不変**であり、改訂は必ず別の識別子になる。
**後から静かにパッチを当てられない**のは意図的な cost である（想定問答 clauses 分冊 §32）。

### B5. 誰に連絡すればよいか

steward は **Dedicator（適用者）本人**（`ACD-1.0.submission.md` §A に連絡先の欄がある）。ただし
**§13.3 のとおり、保守・更新・修正・サポート・防御の義務は負っていない**。
§10.4 により**終了規定が無い**ので、利用者が steward の行動を必要とする場面は無い。

---

## C. リポジトリのどこを見れば何が分かるか

| 知りたいこと | 見る場所 |
|---|---|
| **条文そのもの**（唯一の権威） | `LICENSES/ACD-1.0.txt` |
| 条項ごとの意図（全 82 条） | `LICENSES/ACD-1.0.clause-reference.md` |
| 「X で足りるのでは」への答え | `LICENSES/ACD-1.0.comparison.md` / `docs/architecture/acd-license-rationale.md` §2 |
| 法域ごとの問い | `LICENSES/ACD-1.0.jurisdictions.md` |
| レビューで来るであろう指摘 | `LICENSES/ACD-1.0.review-responses.md`（+ `-clauses` / `-meta`） |
| **実際に来た指摘** | `LICENSES/ACD-1.0.discussion-log.md` |
| 使う側の実務 | **本書** |
| 設計根拠と申請ドシエ | `docs/architecture/acd-license-rationale.md` |
| 提出パケット（英文・送るだけ） | `LICENSES/ACD-1.0.submission.md` |
| 提出判断と**残る弱点** | `LICENSES/READY-TO-SUBMIT.md` |
| 凍結の状態と投稿先の単一ソース | `LICENSES/FROZEN.md` |
| 機械可読な記述子 | `LICENSES/ACD-1.0.machine.json` / `LICENSES/ACD-1.0.spdx.xml` |

**ここに無い疑問が出たら、それはこの一覧の欠落である。** 追記すること。

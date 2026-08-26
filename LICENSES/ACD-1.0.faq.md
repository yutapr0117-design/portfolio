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

steward は起草者本人（`ACD-1.0.submission.md` §A に連絡先の欄がある）。ただし
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

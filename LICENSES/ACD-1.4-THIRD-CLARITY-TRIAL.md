---
file: LICENSES/ACD-1.4-THIRD-CLARITY-TRIAL.md
audience: 次のセッションの実装者（一次読者）/ 監査人
last-updated: 2026-11-15
canonical-ref: LICENSES/ACD-1.4-CLARITY-TRIAL.md (§1〜§9・規則はそちらに従う) / LICENSES/ACD-1.4-SECOND-CLARITY-TRIAL.md (§10〜§14) / LICENSES/ACD-1.4-DRAFT.txt (試作の対象・この file は草案を上書きしない) / LICENSES/ACD-1.4-CHANGELIST.md (採用した変更の記録先)
---

# ACD-1.4 草案の明瞭性の試作（3 冊目）—— §15 から

`ACD-1.4-SECOND-CLARITY-TRIAL.md` が 1,000 行の BLOCKING（Check 365）に届いたので（2026-11-15・1,002 行）、2 冊目と同じく
節の単位で分けた。節番号は続き番号で §15 から始める。規則（草案を上書きしない・採用の条件 2 つ・分担）は 1 冊目の冒頭に従う。
§1〜§9 は `ACD-1.4-CLARITY-TRIAL.md`、§10〜§14 は `ACD-1.4-SECOND-CLARITY-TRIAL.md` に残してある。ドシエはそれらを
「SECOND-CLARITY-TRIAL.md §14.N」の形で引いているので、移さない。

試作を採る commit の手順は 2 冊目の §14 と同じ（`measure_clause_overlap.py --compare / --guard / --sync` で測り、草案を直し、
`sync_stated_counts.py --apply` で語数から導出する数を書き直し、冒頭の箇条・束の表・CHANGELIST の主表を手で直す）。
Check 468y は 2 冊目とこの file の両方の「変えない」「退けた」の節を読む。

## 15. 2026-11-15 からの試作（5 人体制）

### 15.1 T67: §12.2 に Dedicator の同意を足す（+25 語・採った・2026-11-15）

**見つけた経緯**: portfolio-2f が §12.4（人格権の承継）に当てる審査記録を探し、`license-discuss` の PUWL の会話で Sado 氏が日本の事情を踏まえて示した条を見つけた（2025-10-17・`review-readings-2.md` §1.218）: *"… each Licensor and Contributor irrevocably covenants not to assert such rights and consents to all acts that would otherwise infringe them, including modification, combination, and omission of attribution, provided there is no false attribution of authorship. This provision is severable"*。§12.1 / §12.2 / §12.5 / §12.6 とほぼ同じ構造で、差は **同意（consent）** だけだった。Sado 氏は後に委員会の側で `license-review` に書く人だが、この通は個人の提案で、PUWL は審査に出ていない（portfolio-30 が確かめた）。

**Before（§12.2 の第 1 文の後）**: *"… against You or against any person who receives the Work from You, directly or indirectly. You are not required to determine …"*

**After**: *"… directly or indirectly. The Dedicator also consents to any act by You or by any such person that would otherwise infringe those rights. You are not required to determine …"*。§12.4 は *"The covenant and the consent in Section 12.2 bind …"*、§12.5 は *"Neither the covenant nor the consent in Section 12.2 extends to conduct falling within Section 11.3, so the interest that Moral Rights protect against false attribution survives both."*

**欠陥ではなく効果を足す理由**: §12.2 が働くのは人格権を放棄できない法域で、そこで不行使の約束は契約の効果にとどまる。日本の著作権法 20 条 1 項は「意に反して」の改変を侵害とし、同意があれば侵害そのものが成り立たないと読める。英国の CDPA s.87(1) も *"It is not an infringement … to do any act to which the person entitled to the right has consented"* と定める。死後の保護（日本 60 条）も「著作者の意を害しない」場合を除くので、生前の同意は遺族の差止め（116 条）に約束より直接に効く、と読める（portfolio-50）。1.0〜1.3 に欠陥があったのではないので、errata にも SELF-AUDIT にも入れない。

**反例と形（portfolio-50）**: (1) 同意は約束と同じ文に *"and consents to …"* と足すのでなく、別の文にした。包括的な事前同意を無効とする法域で裁判所が同意だけを外すとき、§15.2 の切り分けが文の単位で効き、約束を巻き込まない。(2) 最初の案の *"of theirs"* は先行詞（*You or … any person*）の数が揺れるので、*"by You or by any such person"* にした。(3) *"those rights"* は §12.2 の約束の文の、Work についての人格権を受けるので、同意は Work についての人格権に限られ、§12.3 の限定と同じ範囲になる。

**⚠ 逆側**: (1) **同意が約束より強く効くという読みは我々のもの**である。Sado 氏の通は、日本の実務は自然人が著者のとき包括的な放棄でなく不行使の約束に頼る、と書くだけで、同意が効く理由は書いていない（portfolio-2f）。文献にも法律家にも当てていない —— 法律家への問いに足すよう portfolio-30 に頼んだ。(2) 日本 113 条 11 項（名誉声望を害する利用）と、予見できない程度の改変には、包括的な事前同意が及ばないという読みがある（50）。だから同意は約束を置き換えず並べる。(3) +25 語で、GPL-3.0 より題名から短い余裕は 69 語から 44 語になる。(4) 同意は §2.4 の *"every other grant, permission, and covenant"* に名指されていない。*permission* と読めば独立は §2.4 でも支えられるが、名指していないので争う余地はある（50）。

**依頼**: portfolio-9b に `--compare / --guard` を頼む。

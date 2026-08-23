# improvement-notes — RFC 適合 / 承認ゲートの掃討 / ライセンスの内部接続 (2026-08-23)

```
Document-Type : improvement notes (per-increment)
Session       : Claude Opus 5 — 2026-08-23
PR            : #1281, #1282, #1283, #1284 (すべて rebase-merge・main 全緑)
Canonical-Ref : AI2AI.md Session Record #34 / CLAUDE.md §7 / docs/architecture/total-check-runbook.md §9
```

## 何をやったか (要点)

レンズは 3 つ回した ——「**外部仕様に照らして実際に何を意味しているか**」「**canon を直した
とき、その canon を根拠に書かれた下流は自動では直らない**」「**自分が作った道具は本当に
その仕事をするか**」。

---

## 1. 🔴 api-catalog がメンバー 7 件すべてを「別のカタログだ」と偽って宣言していた (#1281)

RFC 9727 §2 は、カタログ内部で API を列挙する関係を **`item`** (RFC 6573) と定め、
`api-catalog` 関係は「**別の API カタログへの入れ子**」を意味すると明記している。原文:

> the "item" [RFC6573] link relation identifies a target resource that represents an API
> that is a member of the API catalog

当リポジトリは 7 件すべてを `api-catalog` 関係で列挙していた。中身は `llms-full.txt` /
`Claude2Claude.md` / evidence 文書などで、**どれも API カタログではない**。仕様に従う agent は
それらを linkset として parse しようとして失敗する。

**意図的な逸脱ではないと確定**できたのは、mirror doc が「RFC 9727 準拠」「linkset 形式の厳格な
遵守」と述べていたから。加えて `service-desc` / `service-meta` は RFC 9264 では **target
attribute ではなく関係型**なので、対象リソースを `anchor` とする別 context へ移した
(結果 8 context)。

**なぜ長く残ったか**: Check 165 は JSON 妥当性と anchor origin しか見ておらず、**関係型を
検証する層が存在しなかった**。視覚に一切出ない機械可読面なので screenshot にも behavior e2e
にも現れない。→ **Check 449** (a: 入れ子のみ / b: 関係型を attribute に混ぜない / c: 文字列 href)。

`checks_seo_meta.py` が 1,008 行で Check 365 に当たったので、圧縮せず「いま触っているクラスタ」
を `checks_api_catalog.py` へ切り出した (165 = 構造層 / 449 = 意味層 の二層設計)。

## 2. 🔴 承認ゲートがエージェント駆動層に生き残っていた (#1282)

`.claude/agents/aio-guardian.md` の pre-edit checklist 項目 1 は
**「Orchestrator approval recorded? … If not, REFUSE.」** と指示していた。AIO 編集をこの
sub-agent に通すたび、canon が「存在しない作業カテゴリ」と明記した裁可待ちを**実際に再生産
する**状態だった。同種の生きたゲートを 5 箇所で是正 (agent 定義 / slash command / CODEOWNERS /
Check メッセージ 2 種)。

checklist 項目 1 は**削除ではなく C6 の実体を検査する項目へ置換**した —— C6 が守るのは人間の
署名ではなく「真実で捏造でない / 全公開面で食い違わない / digest を再生成する」の 3 つ。

### Check 436 に 3 つの穴があった

| 穴 | 内容 |
|---|---|
| scope | `.claude/agents/` `.claude/commands/` `.claude/skills/` `CODEOWNERS` を一度も見ていなかった |
| 綴り | `要承認` は見るのに `承認必要` / `承認必須` / `承認なしに` / `承認の有無` / `承認下では` を一つも見ていなかった。拡張した瞬間、**既に射程内だった規範層で 4 件**が新たに出た |
| 大文字小文字 | 非 vacuity 検証で、**拡張の動機そのもの** (先頭大文字の `Orchestrator approval`) が素通りした。**scope は届いていたのに照合が届いていなかった** |

うち `major-update-readiness.md` は version bump の実行条件に「(b) オーナーが承認し」を含む
**生きた手続きゲート**だった。

### Check 450 (新設): 非日本語スクリプトの混入

上の掃引中に「権威テキスト」の前半 3 字がキリル文字に置き換わった語を、**規範層 (C6 を説明
する行)** と decision record の 2 箇所で発見した。字形が近いため目視では気付けず、
**spell-check は走らず lint は JS しか読まず prose は何とも比較されない**ので、どの層も
検出しない。ギリシャ文字は数学/科学表記で正当なので意図的に対象外。**573 tracked text file の
実測で誤検出 0 件**を確認してから Check 化した。

**自己参照の制約**: 正規表現を escape sequence で書くだけでは足りず、**Check の説明文に実例の
文字を引用できない** (初版は docstring に実例を literal で引用して自己マッチし RED になった)。

## 3. 🔴 ライセンスの 2 つの目玉が接続していなかった (#1283)

ACD-1.0 の novelty は **§6 の機械学習許諾**と **§8 の特許非留保** (CC0 を OSI で止めた争点の
解消) の 2 つ。精読したところ、**その 2 つが同じ利用者に対して同時に成立していなかった**:

- §1.5 Covered Rights は**特許権を除外**する
- §6.4 output は「Dedicator の Covered Right」に縛られない → **特許には届かない**
- §8.1 特許許諾は「Work およびその派生物の製造・使用等」が射程 → **学習済みモデル / 出力が
  そのどちらでもない可能性**

結果、学習した受領者は**著作権では守られるが特許で露出しうる** —— §8.3 が「その結果を生む
解釈は退ける」と明言している当のことが、条文の構造として残っていた。**§8.4** で特許許諾を
Computational Use とその成果物まで明示的に及ぼした。

併せて **§8.1 の動詞の非対称** (派生物の頒布が落ちる読み)、**§8.5 の射程限界の明記**、
**§2.8 の承継人拘束** (§5.3 / §12.4 は承継人まで及ぶと書いてあるのに、最も重要な §3 / §4 / §8
が沈黙していた) を是正。さらに **§6.2 が instrument にできないことを宣言していた**
(他の権利者の留保まで無効化すると読める) のを §2.7 で限定した。

**相互参照の意味監査**: Check 441b は「参照が解決すること」しか見ないので、全 30 件を機械抽出
して**参照先が本当にそう述べているか**を突き合わせた (結果 clean)。意味の一致は機械検証
できないので Check は作らない。

## 4. 🔴 rotate ツールが「増える場所」と「排出できる場所」を取り違えていた (#1284)

`rotate_mutation_samples.py` は `NAME = [ ... ]` の **literal だけ**を排出対象にしていた。
ところが新しい mutation は必ず `NAME.append({...})` で足す規約なので:

```
増える場所 = append   /   排出できる場所 = literal
```

literal が枯れると「rotate すると空になる」で止まり、**append で溜まった entry には逃げ道が
一つも無い**。しかも rotate 対象は `_E2E_TAIL` 決め打ちで、**consistency 側は一度も rotate
されたことがなかった**。実際 literal 6 件 / append 87 件の状態で advisory を超え、**ツール
からは詰み**になった。

rotate 単位を「literal ∪ append ブロック」へ拡張し、移動元を単位数の多い tail から選び、
移動先 chain も引数化した。実測 977 → 935 行・総数不変 (**旧実装は同じ状態で拒否していた**)。

同 PR で **Check 436 を `docs/files/` mirror へ拡張** (射程 26 → 260 file)。前 PR で手作業で
9 枚を掃引したのに**綴りを 3 つ見落として 4 枚が残った** ——per-instance では閉じない class
だと実測で判ったので構造封じへ昇華した。歴史記録の mirror は対象外 (履歴を濁さない)。

---

## 実測して honest clean と確認済み (再監査不要)

- **`sitemap.xml`** — sitemaps.org 0.9 に対し 0 件 (23 URL・lastmod の W3C Datetime /
  changefreq 列挙 / priority 範囲 / XSD sequence 順すべて適合)
- **`robots.txt`** — RFC 9309 に対し 0 件。**ただし最初の測定は誤りだった** (下記)
- **JSON-LD の 23 型** — すべて実在の schema.org 型で、プロパティも `OrganizationRole` の
  Role パターン含め妥当。**ただしオフラインでは語彙を権威的に検証できない**ので、
  ネットワーク依存の brittle な Check も、重く drift する語彙同梱も採らない
- **ACD-1.0 の相互参照 30 件** — 参照先の記述と意味的に一致

## 教訓

1. **仕様は原文で読め。** `item` と `api-catalog` の違いは要約では潰れる。
2. **測定系を疑う (本 run で 4 回、4 回とも当たった)。**
   - robots.txt: 私のパーサが**コメント行を空行として group をリセット**しており、正常な 4 行を
     「user-agent より前の rule」と誤検出した。RFC 9309 の ABNF では **空行もコメント行も group
     を終端しない**。原文を読み直して測り直した
   - JSON-LD: `@graph` を `@`-prefixed キーとして飛ばし「型ゼロ」と報告した
   - Check 436: 自作の非 vacuity 検証で、拡張の動機そのものが素通りした
   - Check 450: 自分の Check が自分の説明文にマッチした
3. **ゲートを作ったら、そのゲートが動機となった実例を捕捉できるか確かめよ。** Check 436 の
   scope 拡張は、実際に測るまで**届いていなかった**。
4. **per-instance で潰した class は、綴りや射程を変えて再発する。** mirror doc 9 枚を手で
   掃引して 4 枚残した —— 構造封じへ昇華する判断の根拠は「実測で漏れた」という事実。
5. **道具も宣言と実態が乖離する。** 「無限成長を止める」ために作った rotate ツールが、
   実際には**成長する場所を排出できなかった**。
6. **「Check を作らない」判断も成果物** (JSON-LD 語彙 / 相互参照の意味一致)。

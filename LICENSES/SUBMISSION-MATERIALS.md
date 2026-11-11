---
file: LICENSES/SUBMISSION-MATERIALS.md
audience: オーナー（license-review への提出メールを自分の言葉で書く人）/ 次のセッションの実装者
last-updated: 2026-11-07
canonical-ref: LICENSES/ACD-1.0.submission.md (1.0 向けの旧パケット・要件の原典照合の記録) / LICENSES/ACD-1.0.review-rules.md §1.70・§1.76 (OSI の要件の原典読み) / LICENSES/OSI-APPROVAL-PLAN.md §4 (段取り)
---

# license-review へ出すときの材料（事実と根拠の所在）

**これは文面ではなく材料である。** 提出メールはオーナーが自分の言葉で書いて送る（OSI moderators が
AI が大半を書いた投稿を拒否するため・B14）。ここに置くのは、**OSI が提出で求める項目ごとに「何が事実か」
「根拠はどこか」「弱い答えをどう正直に書くか」**だけで、貼れる英文は置かない（識別子や URL のように
正確さが要る語だけは英語で書く）。

**`ACD-1.0.submission.md` §B.0 との関係**: あちらは 1.0 を出す前提の AI 起草文で、改訂履歴の注記が
積み重なり、出す版（1.4 以降）とも合わない。要件の原典照合の記録としては有効なので残し、
**申請の日に使うのはこの 1 枚**にする。

## 0. 申請の日にやること（順に）

0. **前提（この日が来る条件）**: OSI の行動規範の AI 利用に関する改定が公表されたら、それを先に取り込む（投稿の手順・来歴の開示の述べ方・必要なら 1.4 草案）。**改定の取り込み前に本申請しない**（オーナー 2026-10-28・手順と逆側は `OSI-APPROVAL-PLAN.md` §3.8）。改定の検出は行動規範ページの最終更新日の取得で行う（`python3 .github/scripts/fetch_osi_watch.py` が 1 日 1 回取る・取れた日は `OSI-EVENTS-2026-10.md` の行が権威）。改定が来なくても草案の改善は続けるが、**確定（下の 1）は取り込みの後**に置く。**待つのは 2026-11-30 までで、それまでにオーナーが自分の言葉で OSI へ提出が受け付けられるかを尋ねる。答えが来たらその内容に当てて手順を決め直す。改定も答えも無ければ、その日に確定へ進み、確定のあと送り、ゲート 10 で届いたかを確かめる**（`OSI-APPROVAL-PLAN.md` §3.8 の 5。オーナーはこの日付を動かせる）。
1. 最新の草案（いまは `ACD-1.4-DRAFT.txt`）を確定・凍結し、このリポジトリに適用する（1.3 と同じ手順・`ACD-1.3-CHANGELIST.md` の「確定」節）。機械的な部分は `python3 .github/scripts/prepare_version_freeze.py --date <日付>` が行い、残る RED と直し方は同じ道具の mirror doc に表で書いてある。**確定の日に CI が止まる場所と、確定後にやること（改名を一括置換しない / その日のうちに週次 mutation-probe を手で回す）は `ACD-1.1-CHANGELIST.md` §0.13、新しい記述子に入れる項目（E10 の key と §9 —— 記述子の clause 参照が §6・§8・§9 を全部含むことを Check 451e が求める）は `ACD-1.4-CHANGELIST.md` の E10 の項にある**（2026-11-01 追記）。**記述子の下書きと 1.3 からの差は同じ file の「確定前検証（段 7）」にある。確定本文の 1 行目・題名・節・語数の申告は Check 490 が、適用する版の更新漏れは Check 442d / 444 / 444k が、入口の版は Check 472h が止める。binary は LICENSE を更新してから `update_binary_aio_rights.py` を回し、SPDX の XML は `generate_spdx_license_xml.py --version <版>` で作る**（2026-11-06 追記）。
2. 下の表の `<版>` を確定した版（例: `1.4`）で読み替える。
3. 変わる数は**その日に測る**:
   - gap の測定: `python3 .github/scripts/measure_gap_claim.py`（承認済み全文で ML/TDM 等の語が 0 件か）
   - 本文の語数・条数: 確定版の冒頭の申告（Check 490d が実測と照合する）
   - §4c の機械監査の値: `python3 .github/scripts/measure_section4c.py <版>`
   - 逐語引用の版間の差: `python3 .github/scripts/measure_quote_drift.py <前の版> <版>`
   - 提出対象を切り替える前に読む行: `python3 .github/scripts/prepare_version_freeze.py --report <版>`（番号が残って別の条になる行、日付つきの実測、版を決め打ちした検証コマンド。Check 472 は無くなった条しか捕まえない）
     行番号は文書が動くとずれるので、`ACD-1.4-CHANGELIST.md` の段 7 の節にある行ごとの判断と、文で突き合わせて直す。
4. 本文を **plain text の添付**にする（OSI の手続きが添付を求める）。
5. 送信後、**公開アーカイブで届いた形を確かめる**（`REVISION-PROTOCOL.md` ゲート 10）。届くまで「提出済み」と書かない。
6. **審査中の問いには答え、答えていない問いを残さない。** 2009-09 の委員会報告は、ある提出について *"Comments: Bruce had questions, which didn't get answered."* と書いて承認を勧めず、別の提出を *"discussion has been insufficient to justify approval at this time."* として保留した（`ACD-1.0.review-readings.md` §1.172・`against.md` #318）。答えはオーナーが自分の言葉で書く（B14・`REVISION-PROTOCOL.md` ゲート 0）。材料は想定問答（`ACD-1.0.review-responses*.md`）と `QUESTIONS-FOR-COUNSEL.md` にある。届いた問いは受領文として `rounds/` へ無改変で置き、答えていない問いは `AS-OF.md` の「答えていない問い」の行で数えて毎日確かめる。**逆側**: 答えれば承認されるという記録ではない（同じ節）。議論が起きなければ、答える機会もない。

## 0b. メールの長さと順序の目安（文面ではない）

**長さ**: `license-review` の最初のメールは中央値 349 語・平均 454 語で、承認された 2 件は 599 語と 917 語である（n=52・`review-corpus.md` §1.80）。長さは返信の数を予測しないが、行動規範は簡潔さを求める。深さはリポジトリが持ち、メールは入口へ送る。

1.0 向けの旧パケットの文面は分布の上位にあるので、その長さを目安にしない（現在値は §B.0 の見出し）。

**順序**: 下の表の項目はどれも欠かせない。メールの中で置く順は次がよい。

1. 件名と項目の一覧（§1 の表）。本文は plain text で添付する（貼るのとは別の行為）
2. OSD に準拠すると言い、OSD 3・5・6・9 を名指す。OSD 1・7 も足すと良い
3. gap を 1 文で言い、続けて最も近い承認済みとの比較を 1 文で言う（作品を超える特許許諾 ∧ 条件も終了も無い。手続きの原文もこの順である）
4. 法的レビューが無いことと、AI の関与を先に言う（§1 の表の該当行）
5. 入口の `REVIEWERS.md` を完全な URL で指す（https://github.com/yutapr0117-design/portfolio/blob/main/LICENSES/REVIEWERS.md。GitHub なら表が描画され、Pages の `.md` は生の文字列である）

§1c の理由 5 つと §2 の反論は、メールへ全部は載せない。1 つ足すなら理由 2（OSI の FAQ が挙げた穴）である。

## 0c. OSI へ尋ねる段の材料（文面ではない・`OSI-APPROVAL-PLAN.md` §3.8 の 5）

**答えが要る問い**は 3 つで、語はオーナーのものである。

1. steward の投稿は `license-review` に届くか（moderation の状態はどうなっているか）
2. AI が起草したライセンスを、steward が自分の言葉で開示して提出することは受け付けられるか
3. 受け付けられるなら、提出の前に満たすことがあるか

**手元に置く事実**（出典は公開の面に限る）:

| 日付 | 事実 | 出典 |
|---|---|---|
| 2026-09-06 | 両リストへ届いた最後の投稿 | 公開アーカイブ |
| 2026-09-07 | moderator の 5 問に同じ日に答えた | `against.md` #125 |
| 2026-09-09 | 公開の通知 | `rounds/2026-09-09-license-discuss-osi-moderators-observed.txt` |
| 2026-09-12 | review メッセージ 2 通の拒否を steward が報告した | `against.md` #136 |
| 2026-09-17 | 本人が書いた `license-discuss` の投稿が拒否された。内容か status かの問いは答えられていない | `against.md` #215 |
| 2026-09-18 | moderator の求めと、steward の返信。これ以後の記録はこのリポジトリに無い | `against.md` #215 |

**オーナーだけが知っていること**: 09-18 より後の往復の有無。あれば、この表より新しい事実である。

**答えが来たら**: 私信なので本文を公開しない。`rounds/` には日付・相手・向きの stub を置き、`build_private_phrase_hashes.py` を repo の外の本文に回す（Check 492）。分析は要約で書く。答えが否定なら期限で送らず、内容に当てて手順を決め直す。

## 1. OSI が求める項目と、我々の事実

原典は `https://opensource.org/licenses/review-process`（`review-rules.md` §1.76 が 1 項目ずつ照合済み）。

| 項目 | 事実（`<版>` は確定した版） | 根拠・弱い点 |
| :-- | :-- | :-- |
| 件名 | 慣行は `For Approval: <名前>` | `AS-OF.md`（103 通で実測）|
| 名前と版 | Autonomous Commons Dedication `<版>`・短い識別子 `ACD-<版>` | 名前は改名しない（B6・2026-10-24 決定）|
| 本文 | **plain text で添付**。公開の正本 `https://yutapr0117-design.github.io/portfolio/LICENSES/ACD-<版>.txt`。SHA-256 は `LICENSES/FROZEN.md` が pin し CI が照合 | 審査者が「動かない版」を求めた実例あり（`review-rules.md` §1.124）|
| 新規か legacy か | **New License**（legacy は「5 年以上・20 超の無関係な主体」） | 採用 1 件なので新規の側が正しい |
| OSD 準拠の明言 | 「OSD に準拠する」と**積極的に**言い、**OSD 3・5・6・9 を名指しで**満たすと言う（手続きの明文） | 欠けると審査が始まらない実例（`against.md` #97） |
| 　OSD 3 | §4.2（改変・派生物）・§10.1（頒布に条件なし）・§16.3（誰でも同じ条件で適用できる） | 1.3 で条番号確認済み。**1.4 草案でも条番号と中身を確認済み**（2026-11-02・§4.2 は 1.4 で study / inspect / analyse / reverse engineer を足したが改変・派生物の許諾は不変。この表が引く他の条 —— §1.3・§4.3・§6・§8・§9・§10.1・§16.3 —— も同日に当てた）。版を確定したら確定版で当て直す |
| 　OSD 5・6 | §4.3（誰が・何に使うかで条件づけない） | 広い読み（役割の非対称）では §16.4 の Steward 例外が唯一の対象（`submission-osd.md` §3b-i） |
| 　OSD 9 | §4.3 と §10.1（同梱して頒布されるものに何も求めない） | **2026-11-01 訂正**: 旧文は「§5.2(b) と §2.3」で、これは OSD 10（技術中立 —— クリックスルー等の個別の同意を求めない）の根拠である（`submission-osd.md` の逐条照合が OSD 9 = §4.3・§10.1 / OSD 10 = §2.3・§5.2(b) と分けている）。提出文で OSD 9 に §2.3 を挙げると、条文を読んだ審査者には根拠の取り違えに見える |
| 　（足すと良い）OSD 1・7 | §8 の特許許諾は受け取った全員に同じ条件で及ぶ | 特許の異議はこの 2 条で出る（`review-doctrine.md` §1.112）。CC0 の特許除外が OSD 7 に反しうるとされ、同様の除外は以後も退けられたと、審査委員会の McCoy Smith 氏が OSI ブログで述べている（2025-12・`ACD-1.4-CHANGELIST.md` の全ページ読み直し節）|
| 使っているプロジェクト | **1 件 —— 提出者自身のリポジトリ**（`https://github.com/yutapr0117-design/portfolio`）。確定した版をその日に適用しておく | B2。隠さない。審査者自身が「実績が無いと承認しにくい」と認めている（Chestek 氏の Catch-22・B1+B2 節） |
| steward と連絡先 | Yuta Yokoi（横井雄太）・連絡先メール | 提出者＝steward（本人の立場で） |
| SPDX / ScanCode 識別子 | **どちらも無い**。適合する式は `LicenseRef-ACD-<版>`（本文 §16.1 が自分でそう述べる） | 無いなら無いと書く項目 |
| 第三者の承認（Debian / FSF / Fedora） | **無い** | 答えが「無い」項目ほど書き落とす（`review-rules.md` §1.76）。FSF と debian-legal へ尋ねる経路は未使用（`OSI-APPROVAL-PLAN.md` §3.6）|
| 提案する tag | **無い**（採用 1 件で区分を求める立場にない） | Unlicense は希望と違う区分（Special Purpose）になった |
| gap（既存で埋まらないもの） | 1 文で: **作品を超えてモデルと出力まで及ぶ特許許諾を、条件も終了も無しに与える承認済みライセンスは 141 本のうち 0 本で、ACD は §8.4 + §8.2 でそれを与える**（作品を超える特許許諾を持つ 7 本はすべて条件を持つ・`ACD-OSI-BOTTLENECKS-EXTERNAL.md` の G1・`gap-measurements.md` §1.133）。**効果の差として立証できるのはこの組み合わせなので、先に書く。** 続けて書けるのは限定つきの差: §12（MIT / 0BSD に対して）/ §6.2・§6.3（留保の場面だけ）/ §6.4（MIT に対してだけ）。**§6.1・§7・§9 は明示の価値であって独自性の根拠にしない**（`gap-measurements.md` §1.134。下の 1b が約束ごとに分けている）。**2026-11-06 訂正**: 旧文は gap を §6 / §8.4 / §9 の 3 点と書き、§1.134 が 11-04 に除外した §6.1 と §9 を根拠に数えていた | **最も近い例を自分から名指す**: CERN-OHL-P-2.0 の特許許諾はモデルに届くと読める（ただしモデルを名指さず条件がある・`against.md` #241）。測定は上の §0 の 3 |
| 　gap (a) 学習・TDM の明示 | 承認済み 141 本で TDM・データマイニング・機械学習・AI を名指す本は **0**、DSM 指令 4 条の opt-out / 留保に触れる本も **0**。ACD は §6.1（明示許諾）・§6.2（留保しないことの明示） | **主張は「明示の不在」であって「許諾の不在」ではない** ——*use* を無限定に許す許容型は TDM を含む読みが成り立つ。「既存は学習を許さない」と書けば誤り。確かめ方: `ACD-1.0.gap-census.md`「gap ごとの結論」(a)（141 本・*AI* と DSM 4 条の留保を含む）と `python3 .github/scripts/measure_gap_claim.py`。**2 つは母集団と語が違う**（2026-11-02 に実行して確認）: 道具は deprecated の旧 ID を除かない **154 本**（SPDX 3.29.0 の `isOsiApproved` 全件）で 7 語（*machine learning* / *text and data mining* / *data mining* / *machine-generated* ほか）を数え、すべて 0。*AI* と DSM 4 条の留保は道具の語に無く census 側の測定である。審査者に道具を案内するなら、出る数が 154 であることを先に書く —— 141 と書いて 154 が出れば、結論が同じでも数字を確かめていないように見える |
| 　gap (b) 条件ゼロ ＋ 明示特許 | 条件ゼロの承認済み 3 本（0BSD・MIT-0・Unlicense）は `patent` の語が **0 回**。ACD は §8.1〜§8.6 | **「許容型 ＋ 明示特許」は既に在る**（BSD-2-Clause-Patent・BlueOak-1.0.0・UPL-1.0）。gap は条件ゼロとの**連言**にしか無く、「BlueOak を使えばよい」は正当な反論（答えは特許ではなく通知保持の条件の有無）。確かめ方: `ACD-1.0.gap-census.md` (b)（各本の sha256 つき） |
| 　gap (c) モデル・出力に届く特許許諾 | モデル・パラメータ・重みを**名指す**許諾は承認済みに **0**。ACD は §8.4 | **名指しの不在であって到達の不在ではない** —— CERN-OHL-P/S/W-2.0 の特許許諾は Products（*processing of Covered Source* から生じるもの）に及び、モデルが当たる読みが成り立つ（`against.md` #241）。出力を縛らない規定も GPL-2.0/3.0・Artistic-1.0 に古くから在る。確かめ方: `ACD-1.0.gap-census.md` (c) と「逆側」1〜4 |
| OSAID 1.0 との関係（聞かれたら） | 条件側の要件（4 つの自由・個別要素・コピーレフト許容）はすべて満たす。照合表は `ACD-1.4-CHANGELIST.md`。**ACD を付けるだけでは OSAID を満たさない** —— データ情報とコードの公開は ACD を使う人の側の行為で、ACD はそれを求めない（求めれば条件になる） | OSAID は承認基準ではない（基準は OSD）。合っていることは承認に何も足さない。ただし OSAID の問答のページはパラメータについて *"They may be free by nature, or a license or other legal instrument may be required"* と述べ、*"we require an explicit assertion"* を求める。権利の存否を前提にしない ACD の形（§9.2・§16.3）はこの文に当たる（`opensource.org/ai/faq`）|
| 最も近い承認済みライセンス | 効果では Unlicense・MIT-0・0BSD（CC0 は**承認済みではない**）。特許では UPL-1.0・BlueOak-1.0.0・BSD-2-Clause-Patent（違いは条件 1 種） | 「たいていはそちらが良い選択」と書いてよい（`ACD-1.0.comparison.md`）|
| 法的レビュー | **弁護士のレビューは無い**（弁護士は起草も通読もしていない）。**AI によるレビューは受けており、その事実と結果の所在はそのまま書いてよい**（例: 2026-10-26 のレビュー・`ACD-1.4-CHANGELIST.md`）——**質で言えば人間か AI かは本質ではない**（2026-10-26 オーナー）が、OSI の質問は *"including whether it was drafted by a lawyer"* と弁護士かどうかを聞いているので、**AI のレビューを「legal review」とだけ書かない**（弁護士のレビューと読まれる・B14 の下で AI の関与を曖昧にしない）。CI が機械的に確かめていること（条番号の連続・相互参照の解決・定義語の使用・義務語の不在・固有名詞の不在・純 ASCII）も添える | 委員が名指しで求めた項目（`review-corpus.md` §1.75）。**要件ではない**（Chestek 氏・Berkus 氏）。比較対象の ModelGo（Rajah & Tann）と OpenMDW（LF 法務）は弁護士付き。必要になればオーナーが依頼する |
| 来歴（AI の関与） | オーナーが目的と上位の方向を決め、AI が具体的な法的設計と本文を起草し、委任の下で発展させた。オーナーは全文を読んで依拠している。**起草した AI のモデルと会社の名も書く**: Anthropic の Claude（Claude Code で動かした。版ごとのモデルの版は記録していないので書かない）。理由: §6.4 と §8.4 はモデルを作る側に有利に読める条で、そのモデルを作る会社のモデルが起草した。名を伏せると、審査者が後で知ったときに隠したと読まれる（`against.md` #319）。名を出して、その条を疑って読むよう求める方がよい | **薄めない**（`ACD-1.0.submission.md` §E.1 / `LICENSE` の Provenance）|
| 利益相反 | 他者のライセンスの審査に意見したことがあるなら 1 行で開示（`REVISION-PROTOCOL.md` 規則 7） | — |


### 1b. gap ごとに、ACD 自身はそれを果たしているか（`against.md` #269 (a)・2026-11-04）

上の gap の行は「既存のライセンスに無い」ことの確かめ方しか持っていない。審査者は続けて「では、この文書はそれを実際に果たしているか」を問う（Tiemann 氏 2007 *"if a license is submitted with promise X, then we should evaluate promise X as well as the OSD"*・`review-doctrine.md` §1.127）。約束ごとに、**作用として果たしているのか、明示しているだけなのか**を分けて書く。分類は 2026-11-03 の B10 再検証（承認済み 10 本の原文に法的作用で当てた・`ACD-OSI-BOTTLENECKS-EXTERNAL.md` B10 節）による。条番号は 1.4 草案のもの。

| 約束 | 分類 | 確かめる指し先 | 逆側 |
| :-- | :-- | :-- | :-- |
| 機械が判定できる許諾（PREAMBLE・§6.5） | 果たしている（ただし確定した版で） | 確定した版の記述子 `ACD-<版>.machine.json` の `permissions.machineLearningTraining` / `textAndDataMining`（→ §6.1）と `reservationsAndLimits.tdmReservation: false`（→ §6.2）。記述子が引く条の実在は Check 451a、公開 manifest の boolean との一致は Check 451c が守る。1.3 では `ACD-1.3.machine.json` で確かめられる | **1.4 には記述子がまだ無い**（E10・確定の日に作る —— 手順は `ACD-1.1-CHANGELIST.md` §0.13）。記述子は §9 を指すキーを持たない（#269 (b)。次版の記述子に入れる候補） |
| 学習・TDM の明示許諾（§6.1） | **明示しているだけ** | §6.5 の第 1 文が自分でそう述べる（*"Section 6 states expressly what Sections 3 to 5 and 8 would in any event permit"*） | 0BSD や BlueOak（*"everything with this software"*）も、作用としては学習を許している。「既存は学習を許さない」と書けば誤り。法が学習を許す法域（日本の著作権法 30 条の 4 など）では、§6.1 が足す作用はさらに小さい。§6.5 の理由（許諾があるかを機械が判定しなくて済む）は、どの法域でも同じに効く |
| 留保しないこと・留保の撤回（§6.2・§6.3）と、付随条件を課さないこと（§5.2(b)） | 作用として果たしている（Dedicator 自身の行為の範囲で） | 本文の §6.2・§6.3・§5.2(b)。記述子の `tdmReservation: false`（→ §6.2）。問いが現実であることの例: ハンブルク上級地裁 2025-12-10（*Kneschke v. LAION*・Az. 5 U 104/24）は、機械可読の形式を欠く留保は効かなかったと判断した（`ACD-1.0.jurisdictions.md`）。**読んだのは裁判所の press release で判決本文ではない**。BGH への Revision が許可されていて確定しておらず、UrhG 60d 条により研究目的の TDM は留保の有無に関係なく通る | 他の権利者が付けた留保には及ばない —— §6.3 自身が *"the Dedicator has no power to withdraw it"* と述べる |
| データベース権の抽出・再利用（§7.2） | 作用として果たしている | §7.2 の *"extract and re-utilise the whole or any substantial part … repeatedly and systematically"*（sui generis 権の行為の語）。記述子の `databaseExtraction`（→ §7.2） | WordNet はデータベースを許諾の対象に含む（copyright のライセンスとして）。sui generis 権を名指す点が違う |
| 条件ゼロの特許許諾（§8.1・§8.2） | 果たしている | §8.2 の *"subject to no condition and are not terminable"*、記述子の `patentRetaliation: false`（→ §8.2） | 特許としての作用は BSD-2-Clause-Patent・UPL・BlueOak と同じで、違いは条件の有無だけ |
| モデル・出力に届く特許許諾（§8.4） | 作用として果たしている | §1.5 が特許を Covered Rights から除くので §6.4 だけでは届かない、と §8.4 自身が述べ、§8.1 末尾の内容限定を *"deliberately absent"* として外している。記述子の `patentUseForTraining`（→ §8.4） | 広さは費用でもある（`against.md` #16）。CERN-OHL-P-2.0 は Products に届くが内容限定を持つ（`submission-reference.md` の比較）。**ただし §8.4 も 1.1 から因果の限定を持つので、請求項の範囲の差は主張しない** —— 立つのは条件と終了を持たない組み合わせである（`ACD-1.0.gap-measurements.md` §1.133）。**Apache-2.0 との差は 1 文で言う**: Apache-2.0 §3 は *"those patent claims licensable by such Contributor that are necessarily infringed by their Contribution(s) alone or by combination of their Contribution(s) with the Work"* に限り、作品から生じたモデルや出力を名指さない。§8.4 はそれを名指し、条件も終了も持たない。**作品を超えて届く特許許諾には承認の先例がある**: UPL は「Larger Works」へ届く特許許諾を持って承認された（理事会 2015-02-04 *"Board agreed the UPL is OSD compliant"*）。審査で Rosen 氏は、OSD は作品を超える特許許諾を求めず、多くのライセンスは Larger Works などを足して *"to be more generous than the OSD requires"* と述べている（2014-04-15・`ACD-1.0.gap-measurements.md` §1.154）。§8.4 の伸びはこの「OSD が求めるより気前のよい」側に入る —— OSD の問題にならない代わりに、OSD 適合の理由にもならない。その審査の逆側: Fontana 氏は同じ日に *"this license goes way beyond to the opposite extreme"* と述べ（ただし *"not sure if this is an OSI/OSD issue"*）、UPL は承認の前に範囲を *"the unmodified Software as contributed to or provided by such licensor"* と Larger Works に狭めた。§8.1 の *"as made available by the Dedicator"* は同じ形だが、§8.4 のモデルと出力への伸びはその外にある。**逆側**: Fontana 氏は Apache-2.0 に無い小さな特許の機能について *"may be more likely to raise doubts among potential users"* と述べている（`against.md` #308）。新しさは承認の理由であると同時に、疑いの理由にもなる。**もう 1 つの逆側**: 特許を保ちたい献呈者は ACD を選べない。データの供給源として自然な大学や研究機関がそうで、CC0 の審査（2012-02）では、CC が特許を除いた理由を献呈者が *"wanted to monetize them"* ことと伝えている（`ACD-1.0.gap-measurements.md` §1.153・`against.md` #311）。その人たちには CC0 が在り（特許を §4(a) で留保したまま献呈できる。ただし CC0 は OSI 未承認なので、OSI の一覧の中の代わりではない）、ACD はソフトウェアと学習の利用者を特許の罠から守る側を選んだ、と書ける |
| §3 の有効性に依存しない公有化等価の地位（§3 + §4） | 果たしている | §4.4 の *"granted independently of Section 3, and not as a fallback for it"* と §2.4 | 献呈と許諾を並べる形には Unlicense の先例がある |
| 機械生成物（§9） | **宣言しているだけ** | §9.2 *"asserts no right in Machine-Generated Material"*・§9.3（判定しなくてよい） | 包括的な許諾に、付与としての作用を足さない。記述子にも §9 のキーが無い（上の 1 行目） |
| 人格権（§12） | permissive に対しては果たしている | §12.1（放棄）・§12.2（放棄できない法域での不行使） | EUPL-1.2 に放棄の先例がある |

**この表が establish しないこと**: 「作用として果たしている」は、本文の文言をそのとおりに読んだときの話で、どの法域でも有効だという主張ではない（弁護士のレビューは無い・上の「法的レビュー」の行）。

## 1c. 承認すべき理由 —— OSD 10 条と新規ライセンスの基準 8 条を、1.4 の本文で 1 つずつ通す（2026-11-06）

オーナーの依頼「承認させるべきライセンスだというメッセージを共に聞きましょう」を受けて、反論への備えではなく**承認すべき理由を正面から**書いた。言い切っているのは本文が述べることと測った事実で、基準を満たすかの判断は OSI のものである。言い切れない行は、足りないものをそのまま書いた。条番号は 1.4 草案のもの。確定した版で当て直す。**2026-11-11 に、11-08〜11-10 の変更（T34〜T52）を OSD の 10 条に当て直した**: 行が変わるのは OSD 4・6・9 で、OSD 10 は T48 のときに直してある。ほかの 6 条は、当たる文が変わっていない（T34 の §9.2、T36 の §1.9、T37 の §2.6、T39 の §5.2(d)、T40 の §10.3、T43 の §15.1、T45・T47・T49 の §16.4〜§16.5 は、どの条の「満たす」の文も動かさない）。送る文面の語はオーナーが書く（ゲート 0）。

**承認すべき理由は 6 つある。**

1. **受領者に条件が 1 つも無い。** §10.1 がそう述べ、§8.2 が特許についても述べる。否決理由の最大の束（条件・利用制限・差別）は、当たる文が本文に無い。理事会は 0BSD を 8 対 0 で承認した議事録で *"a license with no conditions"*、*"Cannot be argued to violate OSD"* と述べている（2015-10-14・同じ議事録は *"is it really going to be used?"* とも問う）。OSI は条件を課さない型について外部の法律家の助言を取った（Fontana 氏 2015-11-12 *"the OSI obtained outside legal counsel"*）。助言の中身は非公開で、有利だったかも ACD に及ぶかも分からない。
2. **OSI が公に挙げた穴を埋める。** OSI の FAQ は CC0 について *"The most serious of the concerns raised had to do with the effects of clause 4(a)"* と述べ（`rounds/2026-11-06-osi-faq-public-domain-cc0-snapshot.txt`）、理事会の議事録は *"Recommend disapprove, due to clause 4a"* と記録する（2012-03-07・同じ報告は学術の利用者に *"the patent exception is important to them"* と述べる）。同じ時期の意向調査は 13 対 8 で反対だったが、−1 の 13 人は全員が特許を理由に含め、放棄と許諾の構造を理由にした人はいない（`review-precedents.md` §1.138・この形そのものへの反対も 1 人ある・#288）。CC0 の特許の全面除外は *"was thought to potentially run afoul of at least OSD 7"* で、同様の除外は *"have been similarly rejected"*（McCoy Smith 氏・OSI ブログ 2025-12）。ACD は公有化と同じ効果を持ちながら、§8.1 で特許を許諾し、§8.3 で除外の読みを退ける。同じ記事は CC0 を *"perhaps the best example of a comprehensive effort to dedicate content to the public domain"* と呼び、明示の許諾について *"(with or without defensive termination provisions)"* と述べる。Apache-2.0 の防御的終了も *"a form of mutual patent peace"* と肯定しており、ACD はそれを持たない（§8.2・費用は `against.md` #174）。全文は `rounds/2026-11-07-osi-blog-patents-and-open-source-snapshot.txt`。
3. **既存が埋めない gap を、全数の測定で示せる。** モデルと出力に及ぶ特許許諾を条件も終了も無しに与える承認済みライセンスは、141 本のうち 0 本である（§8.4・§8.2）。測定だけでなく、起きたことも在る。Fedora は 2022 年に CC0 をコードに使えない扱いへ変え、告知は *"licenses that preclude any form of patent licensing or patent forbearance cannot be considered FOSS"* と述べた（`gap-measurements.md` §1.139）。必要性は害で問われる（Turner 氏 2021 *"There has to be a real problem (material ongoing harm)"*・#301）ので、提出文の gap にはこの実例を置く。逆側: Fedora が代わりに勧めたのは特許に触れない MIT-0 で（#290）、基準も明示の許諾までは求めていない。学習済みパラメータのファイルについては、特許を含まないライセンスを Fedora は認めている。
4. **献呈が無効でも許諾が立つことを、本文が述べる。** Unlicense は 2020 年に、この議論がリストで述べられ、意見を述べた弁護士の一致を経て通った（#270）。ACD では §4.4 が同じことを本文で述べるので、受領者も裁判所も推論しなくてよい。OSI の FAQ が公有を審査できない理由は *"We wouldn't be evaluating a license text"* で、求めるのは *"licenses that meet the Open Source Definition everywhere"* である。§4 は §3 の結果に依らず全法域で働くので、審査の対象はライセンスの本文である。同じ FAQ は *"rather than try to waive copyright altogether"* と勧めており、§3 はこれに当たる（B4）。献呈と許諾の併用は、Piana 氏が *"I actually advise to use both in the admittedly rare case I am asked."*、McCoy Smith 氏が *"not necessarily fatal"* と述べている（どちらも 2024-12-18）。McCoy 氏の条件は明確に書くことで、§4.4 がそれを述べる。弁護士の一致はまだ無い（B1）。
5. **誰でも本文を変えずに使える。** §16.3 がそう述べ、§16.1 の通知の 1 欄のほかに書き換える箇所は無い。vanity の異議について理事会は *"does not give that argument much weight as long as the license is reusable"* と述べ（2007・`review-doctrine.md`）、委員長は作業部会について *"There are some "unwritten rules" that we discussed but didn't adopt, like the "no vanity license" philosophy."* と述べている（2023-01-27・`reviewer-positions.md` §1.142）。§4.5 により Work はどの条件でも出せるので、ライセンスの行き止まりも作らない。理事会は SimPL の承認で *"it does not create a licensing dead-end and thus does not exacerbate the negative aspects of licensing proliferation"* と述べた（2007-11-07・19 年前の 1 件で、移行先は GPL に限られていた）。
6. **審査者が読み方を既に知っている形を使う。** 1.4 の特許許諾は、作る・使う・売るなどの行為を許諾の目的語にする（§8.1・§8.4）。Apache-2.0 §3、MPL-2.0 §2.1(b)、OSL-3.0 §2 と同じ形である。商標は Apache-2.0 §6 や MPL-2.0 §2.3 と同じく与えず、不行使の約束からも外している（§11.1・§5.1）。ファイル先頭の comment のタグは、SPDX と REUSE と同じくそのファイルに及ぶ（§16.2）。基準 3（英語として明晰か）について、Chestek 氏は *"The OSI does not approve licenses that are poorly drafted"* と述べ、*"problems that a lawyer skilled in drafting would avoid"* を挙げた（2026-01-24・`reviewer-positions.md` §1.140）。見慣れた形を使えば、その種の問題を新しく作らずに済む。2026-11-07〜08 の 3 回の読み（`ACD-1.4-SECOND-CLARITY-TRIAL.md` §14）で、形がずれていた箇所をそろえた。**逆側**: 形をそろえても法的レビューの代わりにはならない（B1）。§8.4 がモデルと出力まで及ぶ点は意図して見慣れない形で、gap そのものである。 関連会社が持つ特許には届かない。Apache-2.0 は *Legal Entity* の定義で届くので、この 1 点では Apache-2.0 より狭い（UPL-1.0・BlueOak-1.0.0・BSD-2-Clause-Patent と同じ側・`against.md` #310）。

**いちばん重い追い風は OSI 自身の FAQ である**（*Last modified on January 21, 2025*・`rounds/2026-11-06-osi-faq-public-domain-cc0-snapshot.txt`）。公有化は *"still not a license"* で、CC0 の *"most serious"* な懸念は clause 4(a) の特許の除外だったと述べる。同じサイトの記事（2017）は、放棄して許諾する形を *"A solution would be"* と述べている（1 人の著者の記事で決定ではなく、結びは MIT を勧める・`board-decisions.md` §2f）。ACD の §4 と §8 はこの 2 点に当たる。**逆側**: 同じ FAQ は *"rather than try to waive copyright altogether"* と述べ（§3 に当たる）、attribution の保護を licence の利点に挙げる（§10.2 が手放す）。**審査記録の中の追い風は 9 点ある。** Piana 氏の *"I actually advise to use both"*（献呈と許諾）、Fogel 氏の *"would certify PD *when accompanied by* a particular patent non-assertion text"*（2014・献呈と特許の文）、Morrison 氏の連邦機関の需要の記述（2017）、Chestek 氏の受領者の負担についての言葉（2025-03）、理事会の *"a license should be rejected only if it violates the OSD"*、委員長の *"That is not a blocker"*、理事会の準拠法条項についての言葉、vanity についての言葉、AI/ML についての言葉で、逐語と出典は `REVIEWERS.md` の "What the record already says in its favour" に在る。過去の発言は誰も拘束しない。

**需要の手がかり（理由ではない）**: 米国の連邦機関が *"something close to public domain yet still addressing indemnification and contributor patent grants"* を探している、という発言がある（Morrison 氏 2017-10-26・`REVIEWERS.md` の有利な記録の表）。連邦政府の著作物は米国で著作権が生じず、OSI の FAQ も *"where it is not easy to apply a license"* の例に挙げる。ACD は権利の存在を前提にしないので（§1.4 の *"holds or may hold"*・§9.2・§16.3）、適用できる読みが立ち、特許は §8 が受ける。1 人の 2017 年の発言で、採用した機関は無い。機関に特許を許諾する権限があるかは ACD の外の法の問いである。逆側は `gap-measurements.md` §1.136 の Tzeng 氏の発言にある。

### OSD 10 条

| OSD | この条によって満たす | 残る問い |
| :-- | :-- | :-- |
| 1 再頒布の自由 | §4.1 は *"royalty-free"*、§4.2 は *"distribute, lend, rent, sell, and sublicense the Work"*、§4.5 は *"any adaptation or collection containing it"* を任意の条件で頒布してよいと述べる | 無し |
| 2 ソースコード | §4.2 は *"in source form, in object form, or in any other form"* の頒布を許す | §10.2 は受領者に source の提供を求めない。許容型の承認済みライセンスと同じ立場である |
| 3 派生物 | §4.2 は *"adapt, translate, modify, create derivative and collective works from"* を許し、§4.5 は *"under any terms You choose"* の頒布を許し、§16.3 により同じ条件でも出せる | 無し |
| 4 作者のソースの完全性 | OSD 4 が許す制限を使っていない。§10.2 は改変の表示も求めない | §16.4 は本文テキストの名前の制約で、Work の条件ではない（§10.5・#101）。1.4 で名前と識別子の照合は「含む」「大小を問わない」へ広がった（T44・T46・T50）が、対象は本文テキストのままである（§16.6 *"They are not terms of the Work"*）|
| 5 個人・団体の差別 | §4.3 は *"on any restriction as to persons, groups, technologies, endeavours, or jurisdictions"* を条件にしないと述べる。You の定義に除外は無い | 法域で結果が変わる条を差別と読む発言がある（#100）。§12.2 は許可がその問いに依存しないと述べる |
| 6 利用分野の差別 | §4.1 は *"for any purpose whatsoever"*、§4.3 は *"on field of use"* を条件にしないと述べる | §6 が分野を名指すが、許可の方向だけである。§6.2 は Dedicator の留保を *"expressly declines to make one"* と述べ、1.4 の §16.2 は留保だけの通知が素材を他の条件へ割り当てないと述べる（*"a notice that is only a Reservation assigns nothing to other terms"*・T52）。留保の通知で素材が Work の外へ出て、機械学習の分野だけが外れる読みは閉じた |
| 7 ライセンスの配布 | §2.3 は *"takes effect without any act of acceptance by You"*、§4.6 は下流の受領者が *"is You in their own right"* と述べる。§8 の特許許諾も同じ You へ与える | §10.2 により通知が外れた複製の受領者は、権利はあるが知らないことがある（意図した設計・費用は `against.md` に記録）|
| 8 製品に特定されない | Work は適用された素材で配布物ではなく（§1.3）、§2.1 は *"to every separable part of it"* に及ぶと述べ、受け取った人は自分の立場で You である（§4.6）。許可は配布の形に依存しない | 無し |
| 9 他のソフトウェアを制限しない | §10.1 は *"imposes no condition, obligation, restriction, or requirement upon You in respect of the Work"* と述べ、同梱物には何も求めない | Dedicator が自分で作るか出す Work 以外の素材（モデルなど）に付ける条件は §5 の外に置かれる（§5.2 末尾 *"that the Dedicator itself makes or makes available"*・T38）。それはその素材の条件で、Work にも他人のソフトウェアにも何も課さない。逆に、その素材を Work と一緒に配っても、Work の許可は狭まらない（§5.2(b)）|
| 10 技術中立 | §2.3 は受諾の行為を求めず、§5.2(b) は *"click-through"* による条件も否定する。許可は技術に依存しない | §6 が機械学習を名指すが、§4.1 の許諾はそれに依存しない。Dedicator が写しを渡さずに Work を動かすサービスの利用に付ける条件（API キー・利用規約）は §5 の外に置かれる（§5.2 末尾・1.4 草案）が、それはサービスの条件で、Work の写しへの許可には何も足さない。利用規約に書いても、入手の経路を問わず Work そのものを縛る条項は §5 の内に残る |

### 新規ライセンスの基準 8 条（`review-rules.md` §1.70）

| # | 基準 | この条によって満たす | 言い切れない点 |
| :-: | :-- | :-- | :-- |
| 1 | 再利用できる | §16.3 は *"may be applied by anyone"* と述べ、本文にプロジェクトの固有名詞は無い。結果を変えるのは licensor ではなく使われる地の法で（§15.3）、§12.2 は許可がその差に依存しないと述べる | 法域の差を licensor の差と読む審査者には、上の区別で答える |
| 2 | licensor を優位に置かない | 義務を負うのは Dedicator の側だけである（§2.2・§2.6・§5・§8.6）。You には何も課さず（§10.1）、何も終わらない（§10.4）| §13 / §14 は Dedicator を守る。承認済みの全部が持つ型だが、この基準が免責へ当てられた例はまだ無い（#265）。licensor 側の留保はもう 1 つ §16.4 の Steward 例外があり、McCoy 氏の広い読みはそこへ届く（#179・論破していない）|
| 3 | 曖昧さが実質的影響を持たない | §15.1 は *"the reading that grants more to You prevails"* と定め、著作物についての分岐を 1 つの向きへ解決する | §15.1 が届かない 2 か所（§16.4 と、適用したかの問い）は語そのものを直した（`ACD-1.4-SECOND-CLARITY-TRIAL.md` §10.1・§12）|
| 4 | 文法的・構文的に明晰 | *shall* 0・*must* 0。読みの分岐を全数で当て、見つけたものは閉じて記録した（errata・`ACD-1.1-SELF-AUDIT.md`）| **判断は審査者のものである。** 英語の母語話者の法律家の目は通っていない（B1）|
| 5 | 適用のどの変化も OSD を満たす | 条項の選択肢も編集箇所も無いので、条件の変化が生じない（§10.1）。適用者が選べるのは通知の形だけで（§16.1・§16.2）、terms は同じである | 無し |
| 6 | 提出時点で遵守できる | 義務が無いので、遵守の問題が生じない（§10.1）| 無し |
| 7 | 既存が埋めない gap を埋める | 理由 3 の測定（`ACD-1.0.gap-census.md`・`gap-measurements.md` §1.133）| **gap として足りるかは OSI の判断である。** 必要性（OSD は特許を要求していない）も問われうる |
| 8 | 完全なテキスト | §1.1 により本文は *"comprising Sections 1 to 16"* で、参照で取り込む別文書は無い | 無し |

### 足りないもの

基準 4 と基準 7 は判断そのものが審査者にある。基準 1〜3 の問いは上の表の形で答えられる。本文の外に足りないものが 2 つある。

- **法的レビュー（B1）**: 1 人でも読めば「無い」を「ある」に変えられる。`QUESTIONS-FOR-COUNSEL.md` がその費用を下げる。手続き上の要件ではなく、Chestek 氏は 2024-12 に *not a blocker* と述べた（`review-precedents.md`）。同じスレッドで逆を述べた Piana 氏は同じ日に撤回した（#127）。献呈 + 許諾の先例は弁護士の一致で通った（#270）ので、あれば強い。
- **第三者の採用（B2）**: 理事会は重複し使われていないものを留め置きうると述べた。委員会が Tiwaz を留めた理由も 2 つの連言で（*"a close variant of an existing license"*、*"no demonstrated uses or planned uses"*・2025-09-11）、解く条件は *"one or more projects begin using this license or express an interest in doing so"* である（`rounds/2025-09-11-license-review-tiwaz-committee-deferral-observed.txt`）。委員会の理由書は別の 2 通で *"the OSI has historically approved newly drafted licenses not yet in use"*（MIT-0・2020）、*"OSI has not used the number of projects adopting a license as a factor in deciding whether a license can be approved"*（Jam・2021）と述べており、どちらも過去についての文である。Chestek 氏は 2026 年に *"less inclined to approve a license that doesn't have a track record"* と述べた（`board-decisions.md` §2d）。ACD は既存の変種ではなく（gap）、このリポジトリが使っている。steward 本人の 1 件が「実証された使用」に数えられるかは記録からは決まらない。計画段階の利用も数えられるので、`ADOPTING.md` で見つけてもらう意味がある。採用の捏造はしない。

### 承認済みに無い仕掛けと、本文が述べる理由（Phipps 氏の *novel devices* への備え・2026-11-11）

Phipps 氏は OSI の判断について *"to explain the discretion OSI always has, and always will, choose to exercise when novel devices are unveiled."* と書いた（`license-review` 2019-06・`board-decisions.md`）。ACD は新しい仕掛けを持つので、審査者がそれを一つずつ探さなくて済むよう、ここに並べる。「承認済みに無い」と言うのは全数で測った項目だけである。窓は 2 つあり、SPDX の 141 本（census）と OSI の licence ページ 126 本（2026-10-17 取得・EUPL-1.1 のページは本文を載せていない）で、行ごとにどちらかを書く。語の不在は効果の不在ではない（Unlicense は語なしで並べている）。

| 仕掛け | 条（1.4 草案） | 本文が述べる理由 | 承認済みとの比較 | 逆側 |
| :-- | :-- | :-- | :-- | :-- |
| 放棄・許諾・約束を、互いに頼らず並べる | §2.4・§4.4 | *"granted independently of Section 3, and not as a fallback for it"* —— 受領者がどれが効いたかを決めなくてよい | 献呈と許諾を並べた Unlicense は承認済み（2020）。OSI の licence ページ 126 本（WP API・2026-10-17 取得、語を正規表現で当てた）で、許諾を他から独立と述べる本は 0（*independent of* は GPL・LGPL の出力の文だけ）、*fallback* は 0、献呈と許諾を並べるのは Unlicense だけ | 並べ方そのものが問いになる（B4） |
| 信頼を目的として述べ、約因や方式の欠けを理由に無効を主張しない | §2.5 | 信頼は *"and not merely a foreseeable consequence of it"* | 同じ 126 本で、信頼を目的として述べる本は 0。*estoppel* は 7 本に在るが、すべて「黙示の許諾を生まない」の向きで、ACD の §2.5 は禁反言を Dedicator を縛る側に使う（逆向き）。*consideration* は 6 本に在る。5 本（APSL-2.0・RPSL-1.0・RPL-1.1・RPL-1.5・Watcom-1.0）は受領者の差し戻しの許諾を許諾の対価として述べ、契約の形を作る。CeCILL-2.1 は保証を限る理由として述べる。撤回できないことを守る点で 5 本と §2.5 は目的が重なりうるが手段が逆で（契約を作る / 受け入れを要らないとして禁反言に頼る・§2.3）、5 本は ACD が選ばなかった守り方の実例になる。CC0 の審査での禁反言の議論に対して作った | 契約の外で効くかは開いた問い（`QUESTIONS-FOR-COUNSEL.md` 問 1）。禁反言が外れたら何が守るか（Rosen 氏 2004 の問い・`review-responses-clauses.md` §2）に、契約で守る 5 本の形は答えを持つが、ACD は持たない |
| TDM の留保をしない・撤回する | §6.2・§6.3 | *"The Dedicator makes no Reservation in respect of the Work and expressly declines to make one"* | 承認済み 141 本で TDM や DSM 指令 4 条 3 項の留保に触れる本は 0（`measure_gap_claim.py`・上の gap (a)） | 明示の不在であって、許諾の不在ではない |
| モデルと出力に、献呈の下でも Covered Right の下でも請求が生じない | §6.4 | *"No enforceable claim arises against You"* | 近い前例は GPL-2.0 §0 の *"the output from the Program is covered only if its contents constitute a work based on the Program"*（§2 の表）。ただし GPL は本体を含む出力を覆う側に残し、対象はプログラムを走らせた出力であって学習したモデルではない。ACD はモデル・重み・出力について、本体を含むかを問わない | 出力に触れること自体が曖昧さを生むと言われた（#133）。前例との差が広いぶん、その指摘は ACD により強く当たる |
| 作品を超えてモデルと出力に届く特許許諾（条件も終了も無い） | §8.4・§8.2 | *"This is a grant in its own right"* —— Covered Rights が特許を除くので §6 だけでは届かない | 141 本のうち 0 本（作品を超える許諾の 7 本はすべて条件を持つ・上の「gap」の行）。CERN-OHL-P の Products が一部の先例 | 広さは費用でもある（#16・B7） |
| 機械生成物に権利を主張しない | §9.2 | *"asserts no right in Machine-Generated Material"* —— 権利の存否は決めず、受領者に判定させない（§9.3） | 承認済みで AI を名指す本は 0（gap (a) と同じ測定） | 権利が後に在るとされた部分には献呈が及ぶ（§9.2 第 3 文） |
| 名前と識別子の族を 1 つの本文に結び、Steward だけが新しい版を出す | §16.4・§16.5 | *"so that each name and identifier in this family continues to denote one fixed text"* | 名前の保護は AFL / OSL の §16 と同じ向き（名前を変えれば改変した本文を使え、元の名前は使えない・§2 の steward の行）。Steward だけが新しい版を出す点は AFL / OSL に無く、MPL-2.0 §10 の *"Mozilla Foundation is the license steward."* が近い | AFL / OSL の §16 は本文の著作権（*"This License is Copyright © 2005 Lawrence Rosen"*）の上に立つ。ACD の本文は AI が起草したので著作権が無いかもしれず、そのとき §16.4 を強制できないかもしれない（`review-responses-meta.md` Q36）。識別子の扱いでは OSI が逆向きに働く場面も在る（`against.md` #210）。支えは 2 つとも弱い。「or later」が書けない費用は同 Q33 |

**この表が establish しないこと。** OSI が新しい仕掛けに裁量をどう使うかは、どの証拠でも決まらない（`board-decisions.md`・`against.md` #130）。理由を本文に書いたことは、理由が正しいことを示さない。

## 2. 先に自分から名指すと良い反論（審査者が見つける前に）

| 反論 | 我々の答え（事実） | 所在 | 理由書の形（CAL 2020・`review-outcomes.md` §1.126） |
| :-- | :-- | :-- | :-- |
| 「steward が個人 1 人」 | リストが恐れてきたのは支配である（Kuhn 氏 2018 *"when an upgrade clause is in play"*・Rosen 氏 2012 の回想）。ACD に upgrade 条項は無く、§16.4 は AFL / OSL の §16 と同じ向きである（ただし AFL / OSL は本文の著作権に立ち、ACD の本文にはそれが無いかもしれない・`review-responses-meta.md` Q36）。**⚠ 逆側**: 承継先は未定で、Kuhn 氏は *"who the license steward is"* も見るべきだと述べている（register B12） |
| 「重複していて、どのプロジェクトにも使われていない」（理事会 2025-07-18・**備えるべき帰結で、否決ではなく留め置き**） | **2 つは *and* で結ばれている。** 委員会はこの形を Tiwaz に当て、*"a close variant of an existing license"* かつ *"no demonstrated uses or planned uses"* として保留し、*"one or more projects begin using this license or express an interest in doing so"* で解くと述べた（2025-09-11・`board-decisions.md` §2c）。**第 1 項**: ACD は既存の派生ではなく、上の gap の行が「重複ではない」に答える。**第 2 項**: 利用は 1 件在る（このリポジトリ・提出者自身）。OSC License は提出者の依頼者の計画段階の利用で承認された。第三者の採用が無いことは隠さない。委員会の理由書も、使用を単独の理由にしていない —— MIT-0（2020・理事会が承認）*"this is not a basis for rejection that the OSI has applied in the past (and the OSI has historically approved newly drafted licenses not yet in use)"*、Jam（2021）*"to date, OSI has not used the number of projects adopting a license as a factor"*（`board-decisions.md` §2d）。**⚠ 逆側**: どちらも過去についての文で、Chestek 氏は 2026 年に *"less inclined to approve a license that doesn't have a track record"* と述べた。Piana 氏は個人の自著について *"not having an active project"* を理由に審査の延期を勧めた（2026-06-19）。Berkus 氏が 2026-10-14 に *"It's not the goal of the OSI to have licenses for every possible combination of conditions"* と述べており、組み合わせが空いているだけでは足りない。具体的な用途を問われたら（Berkus 氏 *"Can you describe that use?"*）、**1 つは説明できる** —— 学習されるために公開する著作物で、このリポジトリがそれに当たる。通知の条件が学習を通ってモデルと出力へどう届くかは決まっていない（§6.4 の行）。述べられないのは 2 例目で、特許の半分を使う採用者もまだ無い（#276）。この区分は process ページに無いので、読んで知っていることを示すだけで価値がある | `ACD-1.0.board-decisions.md`・#84・#276 | **利益と危険を明示的に秤にかける**（CAL）—— 差を 1 点に絞り、1 つ足す費用と同じ場所に並べる |
| 「献呈なのかライセンスなのか」 | §3 は放棄、§4 は**§3 と独立に**同じ権利を許諾（§4.4）。どちらが働いたか受領者は決めなくてよい。Unlicense の 2020 年の審査で「リスト上で議論して救った論理」を本文が自分で述べている。審査者の言葉が在る: McCoy Smith 氏 *"I think everyone acknowledges that a pure public domain dedication without a backstop is problematic"*、同じ日に Chestek 氏 *"The difference with the Unlicense is that it /also/ clearly states what rights are granted."*（2020-05-15・拒否権のスレッド）。ACD の §4 はその後ろ盾を、§3 が効くかどうかに依存しない許諾として持つ（§4.4）。**⚠ 逆側**: 同じ日に Phipps 氏は、public domain は範囲と帰結が国ごとに違い、開発者が他人に尋ねずに権利を確信できないので open source に当たらない、と OSI が以前に助言したと述べた（B4）。ACD の答えは §4 が §3 と独立に働くことだが、§3 を持つこと自体が論点になりうる | `review-precedents.md` §1.57・`against.md` #110 | **承認済みの先例と比べる** —— Unlicense も献呈と許諾を並べて承認された（2020）。ACD はその並べ方を §4.4 で本文に書いている |
| 「なぜもう 1 つの公有化型か」（Landley 氏） | 0BSD 等と違い、作品を超える特許許諾を条件も終了も無しに与える（上の gap の行）。人格権も扱い、機械学習と機械生成物については明示する。**類型の中で優れていると主張するのではなく、この類型に 1 つ足す費用が低い**と言う。理事会の言葉が在る: 再ライセンスを許す SimPL について *"it does not create a licensing dead-end and thus does not exacerbate the negative aspects of licensing proliferation"*（2007-11-07）。§4.5 は Work をどの条件でも出せるので、ACD も行き止まりを作らない | `ACD-1.0.comparison.md` §1・#84 | **利益と危険を明示的に秤にかける**（CAL: *"the risk is tolerable given the potential benefit"*）—— 1 つ足す費用（類型の重複）と、明示の利益を同じ場所に並べる |
| 「承認済みライセンスに別の特許の約束を足せば足りる」（H1-f） | **組は承認済みにならず、審査を経た 1 本の本文でもない。** Ingo 氏は別ファイルで条件を足した組を *"a combination which as a whole is not OSI approved open source license"* とし、足すことは *"only ok if the intent is to submit the new whole as a new license for OSI certification"* と述べた（2016-12-06）。Fontana 氏は献呈に明示の特許の文言を添える形について *"If the US government standardizes on some particular explicit patent language to use with CC0 I would welcome OSI review of that."* と書いた（2016-12-13・opensource.org のアドレス）。ACD は §3 と §8 を 1 本の本文にして、その審査を求める。**⚠ 逆側**: 同じ Fontana 氏は、承認済みライセンスに別の特許の約束を足す道が *"without significant controversy"* で使われてきたと観察している（2016-12-01）。誓約の道は在り、ACD が言えるのは「その組は審査された本文ではなく、誓約は Work と一緒に移らない」ことまでである。Fontana 氏の言葉は政府の文言を想定した個人の発言で、OSI の判断ではなく、§8.4（モデルと出力）までは述べていない | `ACD-1.0.gap-measurements.md` §1.160・§1.133（H1-f） | **承認の単位を示す** —— OSI が比べるのはライセンスの条文で、ライセンスと誓約の組ではない。審査者自身の言葉（Ingo 氏）が、組を出すなら全体を新しいライセンスとして出すと述べている |
| 「出力に触れるのは曖昧さを生む」（Chestek 氏 2025-12） | §6.4 は意図的。§6.5 の理由（沈黙は曖昧と分かった・機械が判定できない許諾は許諾ではない） | `against.md` #133 | **承認済みの先例と比べる** —— 出力をライセンスの外に置く規定は GPL-2.0 §0・GPL-3.0 §2・Artistic-1.0 §6 に古くから在る（`ACD-1.0.gap-census.md`「逆側」2）。CAL の曖昧さへの答え（*"It is not possible to anticipate and then dictate the outcome for every potential factual situation"*）は、**議論の中で説明されて初めて効いた**ので、提出文に先に書いても代わりにならない（#268 (c)） |
| 主題（Mulan 2023 は主題で不承認） | §1.3 の列挙は audiovisual material を含む。モデルの重みは名指していないが、data と、媒体や形式を問わないという語に入る（1.4 草案で一度名指し、2026-11-04 に外した・`ACD-1.4-CHANGELIST.md` の §1.3（2 回目）の行）。データセットとモデルの重みが gap そのものなので狭めていない（OSAID も重みを改変に適した形の一部としている）。OSAID の FAQ は、パラメータの条件を OSI が承認する前提で書いている（*"to be approved by the OSI, the terms for parameters must assure the freedom to use, study, modify and share"*） | `submission-reference.md` §3d・B15 | **定義の書き方を示し、承認済みの原則に接続する**（CAL はデータへの批判に、定義が狭く書けていることで答えた）—— §1.3 は source code / object code から始まり、承認済みの UPL-1.0 も *"associated documentation and/or data"* を対象に含む（*tied to software* の線） |
| 長さ | 本体は長い。**1.4 草案は GPL-3.0 より長い**: `wc -w` で第 1 条から *END OF TERMS* までが 5,317 語（GPL-3.0 は同じ数え方で 4,617 語・+700）、題名からでも 5,658 語（GPL-3.0 は 5,644 語）。1.0 の弁護（GPLv3 より短い・`submission-reference.md` の長さの行）は 1.4 には当てはまらない。正確な数は草案冒頭の申告が権威で、Check 468 が実測と照合する（2026-11-11 測定）。**15 語を削って全体の数で GPL-3.0 を下回ることはしない**（portfolio-00 の提案・2026-11-11）—— 審査者は好きな数え方で数え、条文では 700 語長いままである。書けるのは「全体では同じくらい、条文では長い。長さは条件から来ていない（ACD は You に条件を課さない）」で、1.3 からの増分の行き先は `ACD-1.4-CHANGELIST.md` の「語数の内訳」にある。語を削るのは、語の精度の改善として試作の手順を通るときだけである。Chestek 氏は別のライセンスについて *"It is now 3888 words, longer than the GPLv3. It is excessively wordy and proscriptive."* と書いて承認の候補にならないとした（`license-discuss` 2026-06・#6）。短い入口（`REVIEWERS.md`・`objection-map.md`）で読む順を示す | B3 / B13 | **この instrument に固有でないことを示す**（CAL: *"All open source licenses have a compliance burden, some significant."*）形は使いにくい —— 長さへの批判は「他より長い」という比較そのものなので、承認済みの長いライセンスとの比較で答えると、相手がしていない比較に答えることになる（#116）。効くのは短い入口 |
| 「新しい侵害だけを除いてよい」（Chestek 氏の基準・2025-09-19） | Chestek 氏は別のライセンスの特許条項に *"This is unacceptable for an open source license."* と書き、*"New infringement is the only kind of patent claims that can be excluded in an open source license."* と述べた（`license-review` 2025-09）。1.4 草案の §8.1 は *"where the infringement is caused by subject matter contained in the Work as made available by the Dedicator"* に限る。Work の内容が侵害する請求項は、改変や組み合わせのあとも Work の内容が侵害の原因なので許諾に残り、除かれるのは足した素材だけが生む侵害で、基準が許す範囲に収まる、と読む。**⚠ 逆側**: §8.1 は §8.4 と違って *in whole or in part* を持たないので、Work の内容と足した素材が共に原因になる侵害（組み合わせで初めて生じるもの）を §8.1 が覆うかは語で決まらない。基準はその種の侵害を除いてよいとするので不適合にはならないが、この読みは確かめていない（`QUESTIONS-FOR-COUNSEL.md` 問 2） | `license-review` 2025-09・`QUESTIONS-FOR-COUNSEL.md` 問 2 | **事実として示す** —— 限定の語（*caused by subject matter contained in the Work*）を引き、除く範囲が基準の内に在ることを条番号つきで述べる |
| 「そのライセンスは共有を促すか妨げるか」（Duan 氏の試験を Chestek 氏が採った・2026-08-30） | Chestek 氏は software freedom を *"the ability to do anything you want with the software"* と書き、許される制約は共有の資源を間接に育てるもの（帰属の表示、権利の告知、*as-is* による危険の分配、copyleft）だと述べた（`license-review` 2026-08-30・OpenMDW の審査）。ACD は条件を持たないので前半を最大に満たし、制約のうち *as-is* は持つ（§13・§14）。同じ試験で Duan 氏は MIT を *"fine. Even if proprietary software free-rides on it"* とした。**⚠ 逆側**: ACD は帰属の表示も copyleft も持たない（§10.1・§10.2）。Chestek 氏が共有を育てるとした 4 つのうち 2 つを外しているので、作品の大半が ACD で出た世界の方が良いかには、この試験の上では答えが出ず、我々は測ってもいない（#255・#301）。審査者がそう判断するのは理にかなっている | `license-review` 2026-08（OpenMDW のスレッド）・#255・#301 | **承認済みの先例と比べる** —— 条件を持たない 0BSD・MIT-0 は帰属も求めずに承認されている。ACD はその側に立ち、*as-is* を保つ |
| 「需要が広いか」（Kuhn 氏の 2 段目） | **広い需要は示せない**と自分から書く（採用 1 件）。需要の記述は記録に 2 件在る: Morrison 氏 2017-10-26 *"something close to public domain yet still addressing indemnification and contributor patent grants"*（連邦機関について）と、OSI のサイトの講演（Ramya Chandrasekhar 氏・2025-10）の *"Unclear how attribution requirements transfer through the AI training lifecycle"*（既存ライセンスと学習データについて）。どちらも採用ではない。前者は 9 年前の 1 人の発言で、いまも在るかは確かめていない。後者は OSI の見解ではなく、同じ講演は *"A one-size-fits-all approach may not work"* と述べる | `review-outcomes.md` §1.116 | **借りられる形が無い** —— CAL は採用（steward の client と実プロジェクト）を持っていた（B2・#268）。認める |

**右の列の出どころ（2026-11-04）**: 新規で激しく争われた CAL を承認したときの理由書は、8 つの批判に 1 つずつ、再利用できる形で答えていた（承認済みの先例と比べる / この instrument に固有でないと示す / 利益と危険を明示的に秤にかける / 定義の書き方を示す / 事実として誤りだと条番号つきで述べる）。`against.md` #268 の潰し方 (b) は、議論の場に居られない間に、この答えの形を提出パケットへ移しておくことだった。**⚠ 限界**: CAL の答えが効いたのは、585 通の議論の中で委員会が「論点は十分に議論された」と言える状態になっていたからで、提出文に先に書いた答えはその代わりにならない（#268 (c)・B14）。この列は、議論が始まったときに最初に出す答えの準備である。

## 3. 1.0 を投稿してから変わったこと（聞かれたら）

- 1.0 は `license-discuss` へ 2026-08-26 に投稿した議論の対象で、凍結のまま公開している。返信は無い（アーカイブで確認・取得時刻を添える）。
- 2026-09-17 にオーナーが ACD-1.1 の短い議論依頼を `license-discuss` へ送ったが、**moderation で拒否されリストには届いていない**（steward 提供の逐語転記・`against.md` #215）。我々の投稿で拒否が確認されているものは少なくとも 3 通（`FROZEN.md` の POSTING-NOTE）。**聞かれたら「1.1 は list に届いていない」とそのまま答える** —— 1.1 以降の版はリストで一度も議論されていない（2026-11-01 追記・この項目が無いと「1.0 の後に 1.1 を議論してもらった」と読める）。
- その後に見つけた欠陥は errata に全部記録し（`ACD-1.0.errata.md`）、1.1・1.2・1.3（と 1.4 草案）で閉じたか、直さない判断を理由とともに記録した（**状態は各行の Status 列が権威** —— 2026-11-01 訂正: 旧文は「1.1・1.2・1.3 で閉じた」で、E39・E40 は 1.4 草案でしか閉じておらず、E6 は直さないと決めた項目、E10 は確定手順へ持ち越した項目である。**2026-11-03 再訂正**: 11-01 の訂正は「E1・E6 は直さないと決めた」と書いたが、E1 は 2026-09-11 にいったん直さないと決めたあと 2026-09-14 にその判断を覆して 1.1 で閉じており、errata の Status 列もそう述べている。直さないのは E6 だけである）。**errata の出所は自己発見が大半で、外部レビュー由来が数件、list の議論由来は 1 件**（「list の指摘を反映した」と書けば偽になる・件数は `ACD-1.0.errata.md` の各行が権威）。
- このリポジトリは 2026-10-25 から ACD-1.3 を適用している（申請時は出す版を適用する）。

## この文書が establish しないこと

- **送る文面ではない。** 語はオーナーが書く。
- **網羅の保証ではない。** 要件は OSI の process ページが権威で、提出の直前に原典を 1 回読み直す（ページは改訂されうる）。

---
file: LICENSES/MACHINE-SURFACES-AUDIT.md
audience: register / 本文の担当セッション（一次読者・候補を拾う側）/ 監査人
last-updated: 2026-09-24
canonical-ref: LICENSES/FROZEN.md (凍結と POSTING-STATUS の単一ソース) / LICENSES/ACD-1.0.txt / LICENSES/ACD-1.1.txt / LICENSES/ACD-1.2-DRAFT.txt (照合先) / LICENSES/ACD-1.0.errata.md / LICENSES/ACD-1.0.against.md (候補の行き先)
---

# 機械可読な面の検証 —— 「これらが述べていることは、いま真か」（2026-09-24）

**この文書は報告であって修正ではない。** 見つけた欠陥は**候補として列挙するだけ**で、どれも
直していない。拾って register（`against.md` / `errata.md` / 各 CHANGELIST）へ入れるかどうかは、
register と本文を担当する側が決める —— 件数の同期が 2 か所で走ると競合するからである。
**凍結 2 本（1.0 / 1.1）と `.well-known/*` は読んだだけで、1 byte も触っていない。**

## 0. 範囲・照合先・方法

| 面 | 照合先 |
|---|---|
| `ACD-1.0.machine.json` / `ACD-1.1.machine.json` | 各版の凍結テキスト（条番号は**その版の**番号） |
| `ACD-1.0.spdx.xml` | `ACD-1.0.txt` |
| `LICENSE`（適用宣言） | `ACD-1.0.txt` |
| `REUSE.toml` | REUSE Specification 3.3 と `reuse` 6.2.0 の実測 |
| `.well-known/aio-manifest.json` の `license` ブロック / `llms-full.txt` の Licensing 節 | `ACD-1.0.txt` / `FROZEN.md` / `ACD-OSI-BOTTLENECKS.md` の集計行 |
| **外縁**（リストに無いが、同じ「機械可読なライセンス宣言」の面）: `sitemap.xml` の `image:license` / WebP の XMP / MP3 の ID3 | `ACD-1.0.txt` / 同じ資産を記述する他の面 |

**方法**: 各テキストを条単位に分解し、記述子の `clause` を 1 本ずつ、**指している条の本文を印字して**主題が一致するかを読んだ（存在するかだけなら Check 451a が既に見ている）。
版をまたぐ番号は、定義語の見出しと本文の類似度で 1.0 ↔ 1.1 ↔ 1.2 を対応付けた。
REUSE は `reuse lint` を**実際に走らせた**（リポジトリ本体と、`LICENSES/` にテキスト 2 本だけを残した scratch コピーの 2 回）。

**測っていないもの**（書かないと「clean」と読まれるので明記する）:

- **公開面（GitHub Pages）の実物。** この環境からは `*.github.io` への接続がプロキシで 403 になる。配信された byte の照合は週次の `check_deployed_freshness.py` の担当で、ここでは主張しない。
- `REUSE.toml` の `NOASSERTION` が REUSE で有効か。後述の CRITICAL で lint が止まるため、本体では評価まで到達しなかった。
- ScanCode 等、REUSE 以外の走査器の挙動。

---

## 1. 欠陥の候補（15 件・重い順）

**記号**: 🔴 = 面が偽を述べている / 🟡 = 不正確・不完全・古い / ⚪ = 設計上の注意（偽ではない）。
**どの候補も「受領者が何をしてよいか」を変えない。** 変わるのは、機械や読み手が受け取る記述の正しさである。

### 🔴 M1. `sitemap.xml` が、ヒーロー画像を CC BY-NC-ND 4.0 だと宣言している

`sitemap.xml:58` —— `<image:license>https://creativecommons.org/licenses/by-nc-nd/4.0/</image:license>`。
**同じ資産**について、WebP の XMP `dc:rights` は ACD-1.0、`index.html` の JSON-LD `ImageObject` の `license` も ACD-1.0 を述べている。
**非営利・改変禁止という、ACD-1.0 には存在しない制限を宣言している面が 1 つ残っている**（`against.md` #74 と同じ class ——「All Rights Reserved」撤回時の掃引から漏れた、見えない面）。
リポジトリ全体で `by-nc-nd` はこの 1 箇所だけで、どの文書も言及していない。

- **なぜ捕まらなかったか**: Check 444d は sitemap に全文の `<loc>` が**在ること**を見る。**食い違う宣言が無いこと**は見ていない。
- **逆側**: Google は 2022 年に image sitemap の `image:license` を非推奨にしており、Google はこれを読まない。ただし namespace を読む他の消費者はいる。**害の向きは「実際より制限的に見える」** で、ACD-1.0 §6.5 が避けようとしている当のこと（機械が許諾を判定できない）の逆向き版である。
- **扱い**: sitemap は AIO 公開層なので、直すなら `aio-guardian` 経由（C6 は内容の正しさを守るもので、署名待ちではない）。
- **是正済み（2026-09-24）**: steward が「揃えてください」と答えたので、`image:license` を ACD-1.0 の全文 URL（JSON-LD の `license` と同じ値）へ変えた。**過去形の記録としてこの節は残す**（`against.md` #221）。

### 🔴 M2. `REUSE.toml` と `against.md` #108 は、`reuse lint` が何を言うかを過少に予告している

`REUSE.toml` は「a REUSE linter will still report **a naming non-conformance**」と述べ、#108 は「**it dissolves on OSI approval**」と述べる。`ACD-OSI-BOTTLENECKS-EXTERNAL.md:182` は「我々は `reuse lint` を実行していない」と書いている。**実行した（`reuse` 6.2.0）。**

**(a) リポジトリ本体**: lint は評価に入る前に止まる —— `CRITICAL - README is the SPDX License Identifier of both LICENSES/rounds/README.md and LICENSES/README.md`。
REUSE は `LICENSES/` を**ライセンス本文の置き場**として扱うので、そこにある本文 2 本以外の 85 ファイル（ドシエの `*.md`・記述子・`spdx.xml`・1.2 草案・`rounds/*` 44 件。この報告を足す前の数）をすべて「ライセンス本文」と解釈し、ファイル名から識別子を作ろうとする。**これは承認とは無関係に残る。**

**(b) `LICENSES/` に `ACD-1.0.txt` と `ACD-1.1.txt` だけを残した scratch コピー**:

| lint の指摘 | 承認で消えるか |
|---|---|
| Bad licenses: `ACD-1.0`, `ACD-1.1`（`LicenseRef-` でも登録済みでもない） | 消える（#108 の命名問題そのもの） |
| Missing licenses: `LicenseRef-ACD-1.0`（REUSE.toml が宣言するのに本文ファイルが無い） | 消える（同じ bind） |
| Unused licenses: `ACD-1.1` | 1.1 を適用しない限り残る |
| **Invalid SPDX License Expressions: 11 件** —— `SPDX-License-Identifier:` という文字列を**散文や正規表現の中に**含む Check スクリプトと文書（`checks_aio_config.py` / `checks_governance_sync.py` / `generate_spdx_license_xml.py` / `CLAUDE.md` / check-map ほか） | **消えない** |
| Files with copyright / license information: **614 / 614** | —（これは達成されている。後述 C9） |

- **結論**: 「承認されれば解消する」は**命名の 2 行についてだけ真**で、**ディレクトリの中身と散文中のタグは承認と独立に残る**。
- **逆側**: `REUSE.toml` は**適合を主張していない**（「it does not claim REUSE conformance」と明記している）。偽なのは「何が報告されるか」の予告と #108 の解消条件であって、適合の主張ではない。

### 🔴 M3. 1.2 草案の冒頭が「posting is paused」と現在形で述べている —— 単一ソースは `active`

`ACD-1.2-DRAFT.txt:11` —— 「It has not been posted to any list, **and posting is paused** (see … B14)」。
`FROZEN.md` の `POSTING-STATUS` は **`active`**（2026-09-17 にオーナーが ACD-1.1 を `license-discuss` へ送ったと報告）。前半「1.2 はどのリストにも出していない」は真、**後半が偽**である。

- **なぜ捕まらなかったか**: Check 467 の**状態を述べる面**は `REVIEWERS.md`（marker `Paused as of`）の **1 面だけ**で、草案は射程外。
- **同じ class が入口にもある（担当範囲の外・見えたので記録）**: `LICENSES/README.md:10` が「**発信は 2026-09-09 から停止している**」と現在形で述べ、さらに「Check 467 が **4 面**と両方向で照合する」と書く。実装は状態の面 1 + 恒久の面 2 である。

### 🔴 M4. 凍結中の 1.1 の冒頭が、自分の条番号について誤りを述べている

`ACD-1.1.txt:14–16` —— 「Clause numbers here do NOT correspond to 1.0 **after Section 15**」。
**§1 でもずれている**（E13 を閉じるために定義を並べ替えたため）:

| 番号 | 1.0 | 1.1 / 1.2 草案 |
|---|---|---|
| §1.2 | Work | **Moral Rights** |
| §1.3 | Dedicator | **Work** |
| §1.4 | You | **Dedicator** |
| §1.5 | Covered Rights | Covered Rights（一致） |
| §1.6 | Moral Rights | **You** |

冒頭の文を信じて「§15 までは同じ番号」と読んだ読者は、1.1 の「§1.4 You」を引いて Dedicator に着く。**定義語は他の全条が依拠する場所なので、ずれの位置として最も悪い。**
同じ文言が**凍結されていない面**にも複製されている —— `REVIEWERS.md:134` と `QUESTION-INDEX.md:117`（どちらも「The clause numbers differ from 1.0 after Section 15」）。**1.1 の文は凍結中で直せないが、この 2 面は直せる。**

### 🟡 M5. `ACD-1.1-CHANGELIST.md` §0.5 の条番号対応表が、確定した 1.1 と合っていない

表は 2026-09-10 の草案から生成されており、2026-09-17 に確定した 1.1 と 3 行食い違う:

| 表の記述 | 確定した 1.1 |
|---|---|
| 1.0 §1.2 Work → **1.5** | **§1.3** |
| 1.0 §1.5 Covered Rights → **1.3** | **§1.5**（番号は 1.0 と同じ） |
| 1.0 §16.5 → **削除** / 1.0 §16.6 → **16.5** | 1.1 §16.5 は **Steward の定義**（新設）、**§16.6 は §16.6 のまま** |

表の注記は「閾値で分類する検出器は変更が大きいほど『消えた』と言う」と自分の生成器を疑っているが、**ずれの原因は生成器ではなく、生成後に本文が変わったこと**である。

### 🟡 M6. 1.1 について述べる件数と引用が古い

- **凍結中の 1.1 冒頭**: 「Nineteen of the **twenty-one** defects recorded in `ACD-1.0.errata.md`」。errata は現在 **E1〜E32（32 件）**。書いた時点では真で、**凍結ゆえに古くなった現在形**である（直せない。読み手には「凍結日時点」と読むしかない）。
- **凍結されていない面の複製**: `REVIEWERS.md:42` / `:116` が同じ「nineteen of the twenty-one recorded defects」を現在形で述べる。
- **同じファイルの中で食い違う**: `REVIEWERS.md:134` と `QUESTION-INDEX.md:117` は 1.1 が「**closes seven** recorded defects」と述べ、1.1 の first line を「**NOT IN FORCE, NOT SUBMITTED, NOT APPLIED**」と**引用**している。実物の first line は「ACD-1.1 -- FROZEN TEXT. NOT SUBMITTED FOR APPROVAL. NOT APPLIED TO THIS REPOSITORY.」で、**逐語の引用として偽**である（草案時代の文言が残っている）。

### 🟡 M7. `errata.md` の「機械可読層は正しかった」節が、ポインタの数を 29 と述べている —— 実数は 33

`ACD-1.0.errata.md:80–81` —— 「Every one of the **29** `clause` pointers … the result is **29/29**」。
`ACD-1.0.machine.json` の `clause` は **33 本**（Check 451a が毎回数える値と同じ）。**`against.md` #64 は同じ「29 / 29」を `submission-reference.md` §4c で直したが、errata のこの行は残った**（#64 の残り）。
しかもこれは errata の中で**唯一、機械可読層を擁護している節**である —— #70 の形（「自分に同意している部分は誰も読み返さない」）がもう一度出た。
**主張の中身（全ポインタが存在し主題が一致する）は真である**（後述 C1）。偽なのは数だけ。

### 🟡 M8. `aio-manifest.json` の `license` ブロックだけが、識別子が未登録であることを言わない

`license.spdx_id = "ACD-1.0"`。キー名が「SPDX の識別子」を名乗り、値は SPDX が割り当てていない識別子で、**ブロックの中に `LicenseRef-` も「未登録」も無い**。
`llms-full.txt` / `llms.txt`（3 複製）/ `LICENSE` / 記述子はすべてそれを述べている。**#75 は `llms*` の沈黙を「機械可読層の沈黙は誤答である」として閉じたが、エージェントが「1 回の fetch で判定する」ために設計した manifest に同じ沈黙が残っている**（#75 の 1 面外側）。

- **逆側**: `license.machine_readable` が記述子を指しており、そこには `spdxListed: false` がある —— **もう 1 回 fetch すれば分かる。** #75 自身が退けた言い分と同じ形なので、軽いとは言えない。

### 🟡 M9. E12 の過大表現が、凍結されていない 6 面に載っている

E12 は「No rights are reserved」に限定が無い（§11.1 は商標・人名について何も与えない）ことを記録し、所在を**記述子の `notice` と `LICENSE` の 4 行目**としている。実際には次の面にもある:

`aio-manifest.json` の `license.note` / `llms-full.txt:65` / `llms.txt`・`llms_well-known.txt`・`.well-known/llms.txt` / WebP XMP `dc:rights`（「no rights reserved」）/ MP3 `TCOP`（「ACD-1.0 (no rights)」）。

**これらは凍結されていない。** 1.1 の §16.1 が既に正しい形（「No rights in this work are reserved … trademarks and other rights in names are not granted (Section 11)」）を持っているので、**1.0 を適用したまま、1.0 の §1.5 の定義に沿った言い方（Covered Rights は留保しない）へ寄せることはできる。**
- **逆側**: E12 自身が「条文としては整合している」と書くとおり、法的な帰結は変わらない。

### 🟡 M10. 「リポジトリ全体」の範囲について、3 つの機械可読な面が一致していない

- `LICENSE`: 「You may … everything in this repository」
- `aio-manifest.json`: `applies_to = "the entire repository, including source code, documentation, binary assets, and this AIO layer"`
- `REUSE.toml`: `LICENSES/rounds/**` を **`NOASSERTION`**（他人の言葉を無改変で保存したもの・44 ファイル）

REUSE.toml の方が正しい。受け取った議論の原文に、このリポジトリは権利を持っていない。
- **逆側**: ACD-1.0 §2.7（「Dedicator が持つ権利にしか及ばない」）が法的な帰結を正しく限定しているので、**誰かの許諾が実際に広がるわけではない。** 偽なのは要約の範囲の主張である。

### 🟡 M11. WebP の XMP が `xmpRights:Marked = True` を持っている

XMP の Rights Management schema では、`Marked` が **True なら権利管理下の資源、False なら public domain、不明なら省略**である。同じ XMP パケットの `dc:rights` は「no rights reserved」と述べている —— **1 つのパケットの中で 2 つのフィールドが反対を向いている。**

- **逆側（重要）**: 「False（public domain）」に変えるのも過大である —— §3 の放棄が効かない法域があり（§3.3）、許諾は §4 が別に立てている。**正直な値は「省略（不明）」かもしれない。**「True だけは両立しない」までが確かなことで、正解の値は決めていない。
- **扱い**: バイナリの意味的編集なので、直すなら `update_binary_aio_organization.py` 等で日付フィールドと同じ commit（Check 91）。

### ⚪ M12. MP3 の `WCOP` がサイトのトップを指している

ID3v2.4 の `WCOP` は「利用条件と所有権が説明されているページ」の URL である。値は `https://yutapr0117-design.github.io/portfolio/`（SPA のトップ）。条件が書かれているのは `LICENSE` か `LICENSES/ACD-1.0.txt`。
- **逆側**: トップからは footer のライセンスリンク（#85）で 1 クリックで届く。偽ではなく、遠い。

### ⚪ M13. 1.1 記述子の `textRedistribution: true` は、兄弟キーと極性が逆に読める

`reservationsAndLimits` の他の 6 キーは `value: false` =「この制限は無い」を意味する。`textRedistribution: true` は「制限が在る」を意味するが、**キー名は「テキストの再頒布（が可能）」と読める。** キーだけを読む消費者は反転する。`note` は正しい。
あわせて `note` は「a faithful machine-readable re-encoding [is] not [a] modified text」と要約するが、1.1 §16.4 の但し書き「**provided … the form is identified as a re-encoding**」が落ちている。
- **扱い**: 1.1 記述子は凍結中。**1.2 の記述子を作るときの注意**として置く（例: 名前を「名称の下での改変テキストの頒布が制限されるか」と読める形にする）。

### ⚪ M14. 記述子の `$comment`「Every fact below cites the clause」の射程

両記述子とも `text` / `steward` / `osiApproved` / `spdxListed` / `name` / `version` は `clause` を持たない。後ろ 2 つは本文から自明だが、**`osiApproved` / `spdxListed` は本文の事実ではなく外部の状態**である。また 1.0 記述子の `steward` は、**1.0 本文が定義していない役割名**（Steward は 1.1 §16.5 で新設）。偽ではないが、「全部が条文由来」と読める文は広すぎる。

### ⚪ M15. 1.2 草案の §15.5 / §15.6 は、1.0 で別の条が使っていた番号である

| 番号 | 1.0 | 1.2 草案 |
|---|---|---|
| §15.5 | 沈黙は何も復活させない | 単数・複数 / "including" の解釈規則（**= 1.0 の §15.2**） |
| §15.6 | agency / partnership を作らない | 作成者不利の原則を排除（**= 1.0 の §15.3**） |

草案の冒頭は「citations to 1.0 must keep using the 1.0 text」と正しく述べているので偽ではない。**1.2 の CHANGELIST と記述子を作るときの混線の予告**として置く。

---

## 2. clean だった面（同じ重さで書く）

| # | 何を確かめたか | 結果 |
|---|---|---|
| C1 | 記述子の全 `clause` が、存在する条を指し、**主題が一致する**か（条文を印字して読んだ） | **1.0: 33 / 33、1.1: 34 / 34** |
| C2 | 記述子の中に**版の混線**があるか | 無い。1.0 は準拠法 §15.7・言語 §15.8、1.1 は §15.3・§15.4 —— **それぞれ自分の版の番号**を使っている |
| C3 | 1.1 記述子の 34 本は 1.2 草案でも同じ条を指すか | 指す（1.2 の変更は §2.6 / §2.8 / §2.9 の文言と §15.5・§15.6 の追加で、引かれている条番号は動いていない） |
| C4 | 記述子の `notice` は各版の §16.1 の推奨 notice と一致するか | 一致（`Full text:` と識別子の行を除いて byte 一致） |
| C5 | `osiApproved` / `spdxListed` / `isOsiApproved` は真か | 真（すべて false）。**凍結は「これらを偽にする出来事（結果の通知）」で解除される**ので、凍結された状態フィールドが偽のまま固定される構造にはなっていない |
| C6 | `LICENSE` の条参照（§3 / §6 / §9 / §10.1 / §11.2 / §11.3 / §13 / §14） | 全部正しい主題に解決する。法的レビュー無し・`LicenseRef-` 形・E1 の開示もある |
| C7 | `llms-full.txt` の条参照（§6.1 / §6.2 / §6.4 / §10.2 / §9 / §16.1）と E1、「none of its entries marked resolved」 | 全部真。BOTTLENECKS の集計行は「解消済み 0」 |
| C8 | `spdx.xml` の `licenseId` / `name` / `isOsiApproved` / `crossRef` と本文の一致、`notes` の「Not submitted to OSI at the time of this entry」 | 一致（本文との同期は Check 445 が再生成で検証）。`notes` の文は真 —— `license-discuss` への投稿は承認申請ではなく、「at the time of this entry」で日付づけられている |
| C9 | REUSE.toml は file 単位の沈黙（#106）を閉じたか | **閉じた。** scratch コピーで 614 / 614 ファイルに著作権とライセンスの情報が付く |
| C10 | JSON-LD の `license` 9 箇所・`<link rel="license">`・可視 footer の 1 行・robots の Allow | すべて 1.0 の本文を指す。1.1 が robots / sitemap に無いのは正しい（適用していない） |

---

## 3. 拾う側へ —— 行き先の見当（決めるのは register 側）

| 候補 | 見当 |
|---|---|
| M1 / M8 / M9 / M10 / M11 / M12 | 凍結されていない AIO / 適用面の是正。M1・M8・M9・M11 は `aio-guardian` 経由。M1 と M11 は #74 の class |
| M2 | #108 の解消条件の訂正、`BOTTLENECKS-EXTERNAL.md:182` の「実行していない」の更新 |
| M3 | Check 467 の状態面に草案と `LICENSES/README.md` を足すかの判断 |
| M4 / M6 | 凍結テキスト側は errata へ（直せない）、`REVIEWERS.md` / `QUESTION-INDEX.md` 側は直せる |
| M5 | 1.1-CHANGELIST §0.5 の再生成 |
| M7 | errata の 1 行（#64 の残り） |
| M13 / M14 / M15 | 1.2 の記述子と CHANGELIST を作るときの注意 |

**この報告自身の限界**: 主題の一致（C1）は条文を読んだ判断であって機械検証ではない。範囲外で目に入ったもの（M3 の README、M6 の REVIEWERS）は拾ったが、**範囲外を網羅的に掃いたわけではない。**

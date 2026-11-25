---
file: LICENSES/ACD-1.0.submission.md
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-11-25
canonical-ref: LICENSES/ACD-1.0.txt / LICENSES/ACD-1.0.spdx.xml / docs/architecture/acd-license-rationale.md
---

# LICENSES/ACD-1.0.submission.md

## What

提出対象の版（file の頭の `SUBMISSION-TARGET`・いまは ACD-1.4）を **OSI License Review** と **SPDX License List** へ出すときに、オーナーが
自分の言葉で書くための**事実と欄の材料**（英語）。gap の説明・OSD への当て・開示・SPDX の欄・送信前の確かめを持つ。**送る文は入っていない。**
file 名の `1.0` は由来で、中身の版ではない。

## Why

提出は人間しか行えず、送る文の語もオーナーが書く（B14・`REVISION-PROTOCOL.md` ゲート 0）。材料を 1 か所に集め、版・条番号・数を CI で
照らすと、書くときに古い事実を写さずに済む。**2026-11-25 訂正**: 旧文は「そのまま送れる英文パケット」「『送る』だけにするための成果物」で、
AI が書いた手紙を外した議題 3b（2026-11-23）の後も残っていた。

## How

手で書いた材料で、機械生成ではない。条番号は提出対象の版のもの（frontmatter の `clause-numbers`）で、版を替えたら当て直す（Check 472・472q）。

冒頭に「`LICENSES/READY-TO-SUBMIT.md` が存在しない限り送らないこと」を明記している ——
提出は取り消せないので、**準備完了の宣言をファイルの存在という形で外に出す**設計にした。

## 2026-08-26 の追記

冒頭に **Status ブロック**（実際に送ったもの＝OSI license-review / 送っていないもの＝SPDX とその理由 / テキストは凍結中）と、**§E Addendum** を足した。（**⚠ この節の「OSI license-review」は誤りで、同日の次の節「venue の訂正」で license-discuss に直した**。この節は当時の記録として残している）

§E は「§B に**無い** disclosure」だけを置く。**§B 自体は書き換えていない** —— 既に送信済みかもしれず、書き換えると送った記録を偽ることになる。内容は (1) **LLM 起草の開示**（想定問答 Q10 が「隠す選択肢は存在しない」と述べているのに §B の disclosures に無かった）、(2) **撤回条件**（§B は「なぜ必要か」を述べるが「どうなったら引き下がるか」を述べていない）。

## 2026-08-26 —— venue の訂正

実際に投稿されたのは **OSI `license-discuss`**（一般的な議論リスト）であって、承認申請の窓口である `license-review` ではない。§B は license-review 宛の文面で、**まだ送っていない将来の手順**である。Status ブロックと §B 冒頭にその旨を明記し、§E.0 に「どのリストに出しているかを最初に言う」文面を足した。

**これは細かい区別ではない。** license-discuss で「承認してほしい」と書くと venue を理解していないと見なされ、license-review へ出したつもりで discuss に出していると「まだ何も申請していない」ことに気付けない。

## Constraints

- **Check 441 / 445**: 参照している条項番号・SPDX XML の同期は BLOCKING で強制される
- **Check 444**: ライセンス宣言の cross-surface coherence（本ファイルが挙げる宣言面はすべて
  CI で検査されている、という記述はこの Check の存在に依拠する）
- **Check 450**: 非日本語スクリプトの混入禁止（本ファイルは英日混在だが、いずれも正当な文字）
- 本ファイルは**提出物そのものではない**。提出物は提出対象の版の本文（いまは `ACD-1.4.txt`）と `ACD-1.4.spdx.xml`

## Change impact

- 提出対象の版を替えた → `SUBMISSION-TARGET` と `clause-numbers` を替え、引用を新しい版の条に当て直す（Check 472・472q が止める）
- gap 分析や比較を更新した（`acd-license-rationale.md`）→ 本ファイルの B.1 / B.2 も追随
- 送る前 → `LICENSES/READY-TO-SUBMIT.md` の状態と `submission_gate.py <版>` を確かめる（D.1 が参照する）

## Audience-specific notes

### For AI agents

- 本ファイルの主張は**審査で検証される**。一般論で盛らず、条項番号で裏を取れる形だけを書く。
- とくに「沈黙は拒否ではない」（EU DSM 4(3) は**明示的**留保を要件とする）を崩さないこと ——
  ここを「沈黙＝拒否」と書くと gap 分析ごと崩される。

### For 監査人

- OSD 1–10 への回答はすべて条項番号を伴う。裏取りは提出対象の版の当該条項で行える。
- 「正直な開示」節は**弱点を隠さない**方針の実装（法的レビュー未了 / 実使用の薄さ /
  dedication 型への委員会の慎重論）。

### For 学術研究者 / 第三者

- 新しいライセンスを公式リストへ提出する際に、審査側が実際に何を問うのかが分かる実例。

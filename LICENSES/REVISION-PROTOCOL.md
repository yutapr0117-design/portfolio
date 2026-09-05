---
file: LICENSES/REVISION-PROTOCOL.md
audience: 次のセッションの実装者（一次読者） / OSI license-discuss・license-review の参加者（§0 の英文）
last-updated: 2026-09-04
canonical-ref: LICENSES/FROZEN.md (凍結と venue の単一ソース) / LICENSES/ACD-1.0.discussion-log.md (指摘の記録) / LICENSES/ACD-1.0.errata.md (既知の欠陥)
---

# 改訂サイクルの手順（長期戦の骨格）

**運用方針（2026-09-04 オーナー）**: 届いた議論をそのまま全部取り込む → 本申請 → レビュー →
全部取り込んだ改善版を申請 → レビュー → …… を、承認されるまで繰り返す。**リアルに長期戦**で、
セッションは何度も入れ替わる。この文書は、**返信が届いてから設計を考えなくて済むように**
先に決めておくためのものである。

## 0. English summary — two commitments

**Feedback is recorded verbatim.** Whatever arrives from the list is archived unaltered in
`LICENSES/rounds/`, separately from any analysis of it. Our reading may be wrong; the record of
what was actually said must not be. Summaries live elsewhere and are always marked as ours.

**The reviewed text is never mutated.** A revision ships as a *new version alongside* the old
one. ACD-1.0 stays byte-identical for ever, because it is what the list read. This is not a
courtesy — a discussion whose subject changes underneath it is not a review of anything.

## 1. 1 ラウンドの流れ

| 段 | やること | 落とし穴 |
|---|---|---|
| **① 受領** | オーナーが貼った全文を `LICENSES/rounds/<round>-<venue>-raw.md` へ**無改変**で保存する。整形・要約・翻訳・並べ替えをしない | ここで手を入れると、以降のすべての判断が検証不能になる |
| **② 分解** | 指摘を 1 件 1 行へ分解し `ACD-1.0.discussion-log.md` に追記。**不利なものから先に**書く | 「同じ趣旨」でまとめない。まとめた瞬間に 1 件が消える |
| **③ 分類** | 各件を `認めた` / `反論した` / `1.1 候補` / `撤回検討` / `未回答` のどれかへ。テキストの欠陥は `errata.md` へ、不利な事実は `against.md` へ**行を足す**（既存行は消さない） | 反論できるからといって against から消さない。status を動かすだけ |
| **④ 応答** | list へ返す。**答えていない件を答えたことにしない** | 未回答は未回答と書く |
| **⑤ 改訂** | §2 の版管理に従って次版を作る。**1.0 は触らない** | 凍結解除＝1.0 を編集してよい、ではない |
| **⑥ 再提出** | §3 のゲートを全部通してから出す | 通っていない項目があるなら出さない |

## 1.5 「② 分解」で使う境界分解の型

指摘が「**この条項は open source ではない**」の形で来たとき、認める / 反論する の前に
**どこで越えたのか**を分解する。2026-09 の OpenMDW レビューで実際に使われた形:

1. **引き金**そのものが駄目なのか（例: copyright litigation を trigger にすること自体）
2. 引き金は許容でも、**効果の範囲**が広すぎるのか（例: all grants の termination）
3. **対象者の範囲**が広すぎるのか（例: "any person or entity" まで及ぶ）
4. **判断の時点**が早すぎるのか（例: merits determination 前の filing / maintaining で発火）

**なぜこの型か**: 指摘を丸ごと受けると条項を捨てることになり、丸ごと反論すると議論が止まる。
4 つのうちどれが越えているかを特定できれば、**直す量が最小になり、直せない場合も「どこが
直せないか」を言える**。一般形は「**引き金 / 効果 / 対象 / 時点**」で、termination 以外の
条件条項にも当たる。

**落とし穴**: 分解は反論の道具ではない。**4 つ全部が越えている**という結論もありえて、その
場合は分解がそのまま撤回の根拠になる。分解して有利な枝だけ答えるのは ④ の「答えていない件を
答えたことにしない」に反する。

## 2. 版管理 —— 1.0 は永久に凍結、次版は横に置く

**決定（2026-09-04）**: 改訂は**上書きではなく併置**にする。

- `LICENSES/ACD-1.0.txt` / `.spdx.xml` / `.machine.json` は**恒久的に凍結**する。list が読んだ
  テキストだからで、これが動くと過去の議論が何についてのものだったか分からなくなる。
- 次版は `LICENSES/ACD-1.1.txt` などとして**新規に置く**。本文 §16.4 は改変版が
  `ACD-1.0` の識別子を名乗ることを禁じており、**別版が別識別子を持つのはその要請そのもの**である。
- `FROZEN.md` の FREEZE-DATA 表は**行を足す**（置き換えない）。Check 453 は表を単一ソースに
  するので、1.0 の 3 行を残したまま 1.1 の 3 行が増える形になる。
- `LICENSE`（適用宣言）と AIO 層の宣言は**新版を指すように更新する**。ここは Check 444 が
  cross-surface の一致を強制するので、片側だけ直すと落ちる。

**版に紐づく文書と、紐づかない文書。**

| 版に紐づく（版ごとに持つ） | 版に紐づかない（通しで 1 つ） |
|---|---|
| `ACD-<v>.txt` / `.spdx.xml` / `.machine.json` | `comparison.md`（他ライセンスとの比較） |
| `ACD-<v>.submission.md`（その版で出した文面） | `jurisdictions.md`（法域の地図） |
| `ACD-<v>.errata.md`（その版に残る欠陥） | `REVIEWERS.md`（入口・現況は更新する） |
| `ACD-<v>.clause-reference.md` | `REVISION-PROTOCOL.md`（この文書） |
| — | `ACD-1.0.discussion-log.md` → **全ラウンド通し**で 1 本。ラウンド列を足す |
| — | `ACD-1.0.against.md` → **全ラウンド通し**。版を跨いで不利な事実を蓄積する |

`against.md` と `discussion-log.md` を通しにするのは意図的である。**版を変えるたびに不利な
事実の一覧が短くなるなら、それは改善ではなく記録の消去**だからで、解決した項目は行を残した
まま status を動かす。

## 3. 再提出の前に通すゲート

全部 ✅ でなければ出さない。ひとつでも欠けたら、**出さない理由を discussion-log に書く**。

1. 受領全文が `rounds/` に無改変で入っている
2. 指摘が 1 件残らず discussion-log に分解され、分類が付いている
3. 反論する件は**根拠**が書いてある（「納得しなかった」だけにしない）
4. errata が新版の実態と一致している（直した項目は「直した」と記録し、消さない）
5. against.md に新しい不利な事実が反映されている
6. `FROZEN.md` に新版の digest 行が足され、`shasum -a 256 -c` が全行 OK
7. `npm run verify` = 0（Check 444 / 453 / 458 / 460 を含む）
8. 前版との**差分と理由**が公開されている（何をどの指摘で変えたか）
9. venue の記述が `FROZEN.md` の VENUE-DATA と一致（Check 458）

## 3.5 何も返ってこないとき

**沈黙は既定の状態であって、異常ではない。** 同じ分野で審査中の ModelGo は、2025-02 の提出から
3 回の再提出を経て、2026 年に 3 度出したフォローアップに**いずれも返信を得ていない**
（`PEER-REVIEW-WATCH.md` の経過表）。ACD が同じ状態になることは十分ありうる。

- **沈黙を判定に読み替えない。** 返信が無いことは、却下でも承認でもない。
- **フォローアップは稀に、そして繰り返さない。** 空へ向けて何度も送るのは、審査側の帯域を
  奪うだけで、こちらの信用も減らす。
- **沈黙も記録する。** `discussion-log.md` に「この期間、反応なし」という entry を足す。
  **空のログは「まだ何も起きていない」を意味しない** —— 何も書いていないだけかもしれない。
- **沈黙の間に何をするかは決まっている。** 本文は凍結のまま、ドシエの精度を上げ、
  同時代 instrument を観察し、指摘が来たときに即座に回せる状態を保つ。**待つことと
  止まることは違う。**

## 4. やってはいけないこと

- **受領文を編集する。** 誤字も直さない。引用の都合で切るなら、切ったと明示する。
- **1.0 の本文を触る。** 凍結解除の指示があっても、それは「次版を作ってよい」であって
  「読まれたテキストを書き換えてよい」ではない。
- **不利な事実を消す。** 解決したら status を動かす。行は残る。
- **答えていない件を答えたことにする。** 未回答は未回答と書く。
- **1 ラウンドで全部を直そうとして、根拠の無い変更を混ぜる。** 指摘に紐づかない変更は
  別の増分にする（どの指摘がどの変更を生んだか辿れなくなるため）。

## 5. この文書が想定していないこと

承認された場合の手順（SPDX 提出・カテゴリ配置の受け入れ・`osiApproved` の更新）は、
**承認されてから書く**。いま書くと、起きていないことについての手順が記録に残る。
撤回する場合の条件は `ACD-1.0.submission.md` §E.2 と `against.md` にあり、この文書は
それを繰り返さない。

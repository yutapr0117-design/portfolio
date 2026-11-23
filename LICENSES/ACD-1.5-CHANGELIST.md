---
file: LICENSES/ACD-1.5-CHANGELIST.md
audience: OSI license-discuss / license-review participants, licence reviewers, a future drafter
last-updated: 2026-11-23
canonical-ref: LICENSES/ACD-1.5-DRAFT.txt (草案) / LICENSES/ACD-1.4.txt (直前の確定テキスト)
---

# ACD-1.5 で変えるもの

ACD-1.4 は 2026-11-23 に確定・凍結した。草案 `ACD-1.5-DRAFT.txt` は、下の表の変更と版番号・識別子を除いて 1.4 の本文である。

## 方針 —— 1.5 に何を入れるか（2026-11-23・5 人で決めた・起草は portfolio-5e・逆側と反例は 6d・cd・d7・fc）

**なぜ規則が要るか**: 本文を動かすたびに、段 6b（1.0 からの差をオーナーが `license-discuss` へ出し 30 日置く・計画 §4）の対象が動き、提出が遅れる。1.0 → 1.4 で本文は 4,896 → 5,879 語、45 語超の文は 10.3% → 14.7% に延びた（THIRD §15.54）。決める側は起草の質で退ける —— 2026-09 の委任の最初の行使で 4 本を *"Poor drafting"* で却下し（`board-decisions.md` §4a）、Perens 氏 2009-02-17 は *"Other licenses are poorly written, self-contradictory, or impractical. Those aren't in the OSD either, but it's OSI's duty to reject them"*、Rosen 氏 2002-08-01 は同じことを別の文で言い直すと解釈が割れると書いた（*"The GPL has also been criticized for defining things in subtly separate ways in separate sentences"*・`license-discuss` 2002-08、SHPTRANS への逐条の指摘）。Perens 氏の文は `rounds/2008-12-license-review-tgppl-trademark-rule-observed-4of8.txt`、Rosen 氏の文はアーカイブの写し（`~/osi-archive-cache`）で原文に当てた（採掘は portfolio-d7・2026-11-23）。

1. **入れるもの**: 各変更は、閉じる errata の番号（`ACD-1.0.errata.md`）か、消す読みの分岐（`ACD-1.4-UNIQUE-READING.md` の行）の**どちらかを表の「なぜ」の欄に必ず書く**。書けない変更は入れない（portfolio-cd の反例: 「欠陥の是正」と「明晰化」の境界がぼやけると、入れたい変更を欠陥に格上げする誘因が生まれる）。**例外は 1 つ**: 読みを変えずに文を分ける変更（足す語が接続と名指しの語だけで、`measure_clause_clarity.py` の 45 語超の文が減るもの）と、読みを変えずに語を減らす変更（同じことの述べ直しを外すもの。Rosen 氏 2002 の言い直しは割れるの側）は、「なぜ」の欄に減る文または語の数と、外す文が閉じていた errata が無いこと（`git log -S` で確かめる）を書けば入れてよい —— 審査者は新しいライセンスに *"completely clear"* を求め（Berkus 氏 2015-06-12・`review-readings-6.md` §1.459）、それは errata にも分岐にもならない種類の改善だからである。分ける変更は、元の文の限定句（*except* / *save* / *to the extent* / *subject to* / *in respect of* / *only*）を全部挙げ、分けた後にそれぞれが同じ節に掛かることを Before/After の表で示す。名指しの語（*That covenant* など）の先行詞も同じ表の 1 行にする（portfolio-cd: 長い文の末尾の限定が前の節にも掛かっていたのに、分けると後ろの文にだけ掛かり、§15.1 の下で前半が広がりうる）。表は反例の担当が当てる。
2. **一意化は止めない**（オーナーの依頼「法的解釈を一意に」）。止めるのは、欠陥も読みの分岐も伴わない限定句の追加だけである。一意化の試作は THIRD-CLARITY-TRIAL に書き、採否はこの規則 1 で決める（portfolio-6d）。限定を足すときは、既存の文へ句を差し込む前に、文を足して前の文を名指す形を検討する（§15.54）。
3. **申告**: 各変更は語数の差と、`measure_clause_clarity.py` の 45 語超の割合の差を申告し、増えるなら理由を書く。**上限は置かない** —— 閾値を置けば閾値のために削る誘因が生まれ、register の B3 が自分の弁護にしている「題名からの数が下回ったのは閾値のために削った結果ではない」（T54）が崩れる。文長は明晰さの代理指標で、明晰さそのものではない（`ACD-1.0.against.md` に portfolio-cd が足す文長の項の逆側）（portfolio-cd）。
4. **いつ確定するか**: オーナーが 1.4 の差を list に出した後、1.5 の確定は原則として、審査で受けた指摘に直した版で応えるために使う（理事会が却下した *"argument without revision"* の形を避ける・`board-decisions.md` §4a）。**出口が 2 つある**: (a) list に出す前に、1.4 に結果を変える欠陥が見つかったら、errata に記録し、出す版を 1.4 にするか 1.5 にするかを 5 人で決め直す（portfolio-6d）。(b) 30 日の窓のあいだに指摘が無く、結果を変える欠陥（errata が重大と書いたもの）が在るなら、1.5 を確定し、1.4 からの差を改めて list に出す —— 沈黙が続く限り確定しない規則にすると、直す予定を自分で errata に書いた版を出すことになり、Nelson 氏 2005 の「改訂が控えている版を承認するのは誤り」が逆向きに効く（portfolio-cd）。list への投稿は、どちらの出口でもオーナーが自分の言葉で書く（B14）。

**逆側**: (1) 規則 1 は、errata も分岐も伴わない改善 —— 例えば §15.4 で訳と英語が食い違うとき受け手に多く与える側を採る案（Nelson 氏 2004-11・§1.459）—— を入れない。その案は「変えない」と読んだ（第三者の誤訳が Dedicator の与えるものを広げる・portfolio-5e と d7 の合意）が、規則がそれを先に決めてしまう面はある。(2) 説明の語が長さとして許された例もある —— Perens 氏 2010-04-05（`license-review`）*"A lot of the fat in the GPL is there to help explain the license to non-attorneys"*。規則 3 は語を増やすことを禁じず、理由を書かせるだけにした。(3) 1.4 を確定したままで出口 (b) が使われれば、読み手が見る版は 1.0〜1.5 の 6 つになり、B13（理解の費用）を上げる。

試作は `ACD-1.5-CLARITY-TRIAL.md` に書く（T135 から）。

## 表（変更が入ったらここへ足す）

| 対象 | 何を変えるか | なぜ | 費用（語） | 状態 |
| :-- | :-- | :-- | :-- | :-- |
| §11.4 第 2 文（T135） | *"It reaches nothing else, save that the covenants in Section 5 are promises about the Dedicator's own conduct and are not limited by this sentence."* を *"It gives nothing by implication beyond what its words give."* へ | 規則 1: `ACD-1.1-SELF-AUDIT.md` §3zd（1.4 の T124 の授権と放棄が但し書きの外）。網羅の言い切りが同じ型を 3 度生んだ（E44・§2.5・T124）ので、言い切りを黙示の排除に置き換え、型をまとめて消す。黙示の許諾と黙示の約束の排除は残す（cd の反例: 1.4 でその働きを持つのはこの 1 文だけ）。試作と 3 巡の反例は `ACD-1.5-CLARITY-TRIAL.md` §1 | −15（45 語超の文の数は変わらない） | 草案へ入れた（2026-11-23） |

## errata 由来（`ACD-1.0.errata.md` が一次記録）

| errata | 条 | 何が欠けているか・試作 | 状態 |
| :-- | :-- | :-- | :-- |
| E87 | §5.2(b) | 偽りの言明をしない義務の除外が無い（1.4 の確定の後に、§5.1・§5.2(b)・§5.2(d) の除外の列を並べて見つけた）。試作 T138（`ACD-1.5-CLARITY-TRIAL.md` §5・+14 語）は採らない —— 非対称は「法が与える請求は残し（§5.1）、契約で新しい義務の経路は作らない（§5.2(b)）」の線に沿う（cd の反例）。採用者には `ADOPTING.md` で知らせる | 直さないと決めた（2026-11-23） |

## 語数の内訳（1.4 → 1.5 草案・表から集計）

1.4 の 5,879 語から 1.5 草案は −15 語である（黙示の排除の 1 束で −15）。

1.0 の 4,896 語から見ると 968 語長い。`measure_clause_clarity.py` の 45 語超の文は 1.4 と同じ 28 文（191 文中 14.7%）で、平均は 28.9 → 28.8 語（2026-11-23）。表が変わったら数え直す（語数の合計は Check 468s が表と草案の申告で、この節の数は Check 498 (k) が実測で照合する）。

| 束 | 増減 | 何のための語か |
| :-- | --: | :-- |
| 黙示の排除（§11.4・T135）| −15 | 網羅の言い切りと但し書きを外し、黙示の許諾と黙示の約束の排除だけを残す。後から入る変更が「及ぶ先の列から漏れる」型の欠陥を作れなくするための語の削減 |

## 記述子の候補（1.5 の確定の日に `ACD-1.5.machine.json` へ入れるかを決める）

- `permissions.circumventionOfDedicatorMeasures`: `true`・§5.2・`note`: *"Only measures applied by or on behalf of the Dedicator to a copy of the Work, where the circumvention is effected in a use this Dedication permits or purports to permit; to the fullest extent the law permits."*。T124（1.4）が §5.2 に足した回避の授権は課すものでなく与えるもので、§6.5 の線（自動の仕組みが判定できない許しは許しでない）では `permissions` に置く読みが立つ。1.4 の記述子は持たない（確定を遅らせないため 1.4 では足さなかった・fc と 5e・2026-11-23）。**逆側**: 回避の法の授権は裁判所が読む事実で、機械が行動を変える値ではない。足すなら Check 451a の `clause` の照合に §5.2 が増える

## Constraints

## Change impact

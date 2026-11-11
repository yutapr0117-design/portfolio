---
file: .github/scripts/measure_gap_claim.py
audience: ai, human (新卒), 監査人, OSI license-review participants, 第三者全般
last-updated: 2026-11-11
canonical-ref: LICENSES/ACD-1.0.submission.md §B.0 (この script を「the command is in the repository」と述べている面) / LICENSES/AS-OF.md (測定結果と検証日) / LICENSES/ACD-OSI-BOTTLENECKS.md B10
---

# .github/scripts/measure_gap_claim.py

## What

**ACD-1.0 が主張する gap を、SPDX License List の `isOsiApproved` 全件に対して測る script。**
出力は主題語ごとの件数（`machine learning` / `text and data mining` / `machine-generated` /
`subsist`）と、**`output` が `patent` の 250 字以内に現れるライセンス数**（§8.4 の枝）。

**2026-11-11 から、向きつきの語族も出す**（portfolio-aa の依頼）: §2.4 / §4.4 の *independent(ly) of* と
*fallback*、§2.5 の *estoppel / estopped*・*consideration*・*rely / reliance*。これらは承認済みの本文にも
現れるが**逆の向きで**現れる（*estoppel* は「黙示の許諾を生まない」の列挙に、*consideration* は
「条件の対価」に）ので、語の有無ではなく文ごとに向きを仕分けて、向きごとの本数を出す。
入力は SPDX（既定・ネットワーク）のほかに `--texts DIR`（census の cache と同じ `<id>.txt`）と
`--wp-json F…`（opensource.org の WP API の license ページ）を取れる。2026-10-17 取得の WP 126 本では
*independent(ly) of* 4 本はすべて別の向き・*fallback* 0・*estoppel* 7 本はすべて黙示の許諾を否定する向き・
*consideration* 6 本のうち 5 本が条件の対価・信頼を目的と述べる本 0（portfolio-aa の手の測定と一致）。

## Why

**§B.0 は審査者に *"That claim is measurable, and I measured it … The command is in the
repository."* と述べる。** その約束は**実際に走るものが在って初めて真**である。
2026-09-10 に §B.0 を断定から測定へ書き換えたとき、**約束だけが先に入った**ので同じ日に足した
（#122 / #123 と同じ族 ——**検証可能ですらない約束を、入口や送信面に置かない**）。

## How

- SPDX の公開 JSON（index + 各ライセンス詳細）を取得し、`licenseText` を小文字化して部分文字列で検索
- **正規表現ではなく素の部分文字列**にしてある ——**検出器が凝るほど、外れたときに気付きにくい**
  （2026-09-10 に pipermail の折り返しヘッダで実証した）
- `--verbose` で該当 `licenseId` も出す
- 向きの仕分けは文（`.` / `;` で切る）ごとに、語族の向きの正規表現を上から当て、どれにも当たらない文は `other`。
  **語族の語を持つ本はどれかの向きに必ず入る**ので、仕分けが外れても本が数から消えない（総数と `other` が見える）
- **`--self-test`**: 承認済みの本文（EPL-2.0 / APSL-2.0 / GPL-2.0）と ACD-1.4 草案から逐語で取った 9 文を仕分け、
  期待どおりの向きに落ちるかを確かめる（ネットワーク不要）。**Check 476d が consistency でこれを走らせる**
- **取得失敗は 0 件として数えず、警告して exit 1** ——**未測定を「該当なし」と混同しない**

## Constraints

- **ネットワークが要る。CI では走らせない** ——外部サービスへの定期取得は壊れやすい（`CLAUDE.md` §7）
- **測っているのは語の有無であって効果ではない。** permissive ライセンスは「すべての利用」を
  許すことで機械学習を暗黙に許している ——**script の出力自身がその但し書きを印字する**
- 結果を引用するときは **SPDX List の版と取得日を併記する**（`AS-OF.md` の規律）

## Change impact

向きの正規表現を変えたら `--self-test` を走らせる（Check 476d が RED になる）。**主題語の検索は素の部分文字列のまま**で、向きの仕分けだけが正規表現である —— 凝った検出器の外れに気付けるよう、向きは自己試験の文で縛った。

検索語を足す/変えると、`AS-OF.md` と §B.0 の記述が実測とずれる。**語を変えたら両方を同じ増分で直す。**

## Audience-specific notes

- **審査者**: §B.0 の主張はこの 1 コマンドで再現できる。**限界も同じ出力に印字される**
- **後任 AI**: 引用する前に**走らせ直す** ——SPDX List は版が上がる（`AS-OF.md` の「動く数」の族）
- **監査人**: 取得失敗があれば exit 1。**緑でないときの出力を読むこと**

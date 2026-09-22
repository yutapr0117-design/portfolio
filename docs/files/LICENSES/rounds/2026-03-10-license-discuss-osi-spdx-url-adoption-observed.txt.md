---
file: LICENSES/rounds/2026-03-10-license-discuss-osi-spdx-url-adoption-observed.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-22
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/ACD-1.0.against.md #210 / LICENSES/ACD-1.0.errata.md (E14) / LICENSES/ACD-1.0.against.md #56 / LICENSES/ACD-1.0.against.md #160
---

# LICENSES/rounds/2026-03-10-license-discuss-osi-spdx-url-adoption-observed.txt

## What

**`license-discuss` の「OSI が承認済みライセンスの URL を SPDX 識別子へ標準化した」
スレッド全 6 通**（2026-03-10〜12）。**我々宛ではなく、ACD-1.0 についてでもない。**

## Why

**§16.4 / E14（識別子は 1 つの固定テキストを指し続けねばならない）に、両向きで当たるから。**

**有利な側** —— **識別子が指すものがぶれる害について、初めての外部の証人が 2 人**。
Fontana 氏は SPDX の `GPL-2.0` → `-only` / `-or-later` 分割を *"pretty much a complete
debacle IMO"*、Šuklje 氏は *"the GNU license naming debacle"* と呼ぶ。**どちらも ACD に
利害を持たない。**

**不利な側 —— 同じ 6 通の中にある。** Fontana 氏 *"the license is **one level of abstraction
removed from its actual application**"*、Phipps 氏（元 OSI 会長・*"in a personal capacity"* と
明記）*"the -only and -or-later variants are all **deployment options** … and **do not reflect
the licenses that OSI has actually approved**, which embrace both variants"*。
**OSI 自身の模型は「1 つの承認された同一性 : 多数の展開形」であり、§16.4 は「1 識別子 : 1 テキスト」を
主張する。** **我々の識別子規律は、承認を求めている当の組織の実務より厳しい**
——これは #160（Jones 氏の reusability 基準）が名指しする形そのものである。

**3 つ目** —— **OSI は告知から 11 時間で、list のフィードバックにより自分の命名方針を
変えている。** **命名層は社会的に統治され、速く改訂される。§16.4 はそれを、設計上まったく
改訂できない文書の中に置いている。**

## How

`https://lists.opensource.org/pipermail/license-discuss_lists.opensource.org/2026-March.txt`
を**ブラウザ相当の UA** で取得した既存キャッシュから、該当 6 通を無改変で切り出した。

**見つけ方は #209 と同じ** ——読む単位をスレッドから発言者へ変え、Nick Vidal 氏の 2026 年の
投稿 11 通を全数で見た。**それまで我々はこのスレッドを、他人のレポートの要約の中でしか
持っていなかった**（`rounds/2026-09-19-external-report-…`）。

## Constraints

- **無改変で保存する。** 本文中の `"zGPL-X.Y-only"` は明らかな typo に見えるが**直していない**。
- **観測（`-observed`）であって受領ではない。**
- **Phipps 氏の発言は *"in a personal capacity"* と本人が明記している。OSI の立場として引かない。**
- **有利な半分だけを引かない。** 同じ 6 通が両向きに働く。

## Change impact

- `rounds/` に file を足したら `rounds/README.md` の在庫も同じ commit で（**Check 465**）。
- **承認済みライセンスの正規 URL は `https://opensource.org/license/<SPDX id>` である。**
  §16.4 が *"the bridge until registration"* と呼ぶ registry は、**具体的には OSI + SPDX** である。

## Audience-specific notes

- **AI（実装者）**: **同じ 6 通が両向きに働くとき、片側だけを引くのが最も起きやすい誤りである。**
- **監査人**: 取得元と日付は本文冒頭。同じ URL を同じ UA で取れば再現できる。
- **第三者**: §16.4 を支持する材料と、それに反する材料を同じ file に置いてある。

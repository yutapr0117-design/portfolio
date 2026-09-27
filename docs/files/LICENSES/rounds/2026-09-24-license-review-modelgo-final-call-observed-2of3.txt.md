---
file: LICENSES/rounds/2026-09-24-license-review-modelgo-final-call-observed-2of3.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-27
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/ACD-1.0.review-doctrine.md / LICENSES/ACD-1.0.review-rules.md / LICENSES/PEER-REVIEW-WATCH.md
---

# LICENSES/rounds/2026-09-24-license-review-modelgo-final-call-observed-2of3.txt

## What

**ModelGo Attribution 2.0 の FINAL CALL FOR COMMENTS スレッド（2026-09-16〜09-24・9 通）の
第 2 部（全 3 部）**（2026-09-27 取得）。**我々宛ではなく、ACD-1.0 についてでもない。**

**行境界で 750 行ごとに分割してある**（メッセージ境界ではない）—— ここには 399 行の 1 通が
あり、リポジトリの上限は 1,000 行（Check 365）だからである。**3 部を順に連結すると取得した
バイト列が復元される**（書き出し前に assert 済み）。

## Why

**ModelGo は主題が ACD に最も近い同時代の instrument** で、`rounds/` には 2026-09-03〜09-08
までしか無かった。この区間が重要なのは、**Licensing Committee の委員長が、公表されている
新規ライセンスの基準** *"The license does not have terms that **structurally put the licensor
in a more favored position than any licensee**"* **を具体的な条項へ実際に当てている**からである
（`review-rules.md` が基準として記録していたが、**適用された実例は一度も持っていなかった**）。

**⚠ この file が establish しないこと**: ModelGo の帰結はまだ出ていない。**当たらない**と
確かめられることは、ACD が承認されることを意味しない。

## How

`https://lists.opensource.org/pipermail/license-review_lists.opensource.org/2026-September.txt`
を**ブラウザ相当の UA** で取得し、件名で該当スレッドを切り出して header ごと無改変で保存した。

## Constraints

- **無改変で保存する**（`rounds/README.md`）。**分割は byte を変えない。**
- **観測（`-observed`）であって受領ではない。**
- **3 部は 1 組である。** 片方だけを引くと 1 通が途中で切れる。

## Change impact

- `rounds/` に file を足したら `rounds/README.md` の在庫表と件数も同じ commit で（**Check 465**）。

## Audience-specific notes

- **AI（実装者）**: 引用するときは**逐語をこの file から取る**（分析側の言い換えからではなく）。
- **監査人**: 3 部を `cat` で連結し、取得元 URL の同スレッドと突き合わせれば再現できる。

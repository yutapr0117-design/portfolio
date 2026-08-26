---
file: .github/scripts/checks_store_contracts.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-08-26
canonical-ref: .github/scripts/checks_behavioral.py (分離元) / .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/architecture/file-size-budget.md (行数予算)
---

# .github/scripts/checks_store_contracts.py

## What

**producer（書く側）と consumer（読み戻す側）の非対称**を封じる 5 Check を内包する split module。

| Check | 守る性質 | 実バグ |
|---|---|---|
| 373 | `defaultAppsData` の全 top-level key を `normalizeAppsData` が読み戻す | #684（quiz 検索語が reload ごとに消える）|
| 404 | default profile の全 field を `validateAndNormalize` が保持する | #139（github / linkedin / location が strip）|
| 405 | top-level field 全般の保持 | #1036 / #1037（theme / projectPrefs の復元漏れ）|
| 374 | `importJSON` が adopt する前に正規化を通す | #295 / #561（ingestion 不変条件）|
| 410 | UI 入力上限（`maxlength`）と保存上限（`slice`）が同じ定数から導かれる | #924（ノートが silent に切り詰め）|

## Why

この非対称は**視覚に出ない**。利用者からは「**保存したはずのものが次に開くと無い**」としか見えず、しかも壊れた瞬間には何も起きないので、気付くのは常に後日である。実際この family は 5 回別々の形で実バグ化している。

片側だけ直しても再発するため、各 Check は **producer と consumer の両方**を縛る形になっている（「default に key を足したなら normalize でも読め」「slice するなら maxlength も置け」）。

分離の直接の理由は**肥大化の先手**である。分離元 `checks_behavioral.py` は 924 行で advisory（950）まで残り 26 行だった。このリポジトリは advisory を素通りして BLOCKING（1,000）に激突する事故を過去に 3 回起こしているので、**鳴る前に**割った。

## How

- monolith が `_ctx` を組み、**`checks_behavioral.run(_ctx)` の直後**という元の実行位置で呼ぶ。
- 移した section は 1 行も書き換えていない。free-variable 解析で外部依存が `ROOT` / `check` の 2 つだけであることを実測してから割った＝ byte-equivalent。
- **非連番抽出**（373 / 374 / 404 / 405 / 410）。Check 番号は連番である必要が無く、`_aggregate_check_numbers()` が module 横断で集約する。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re` / `json` のみ import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: docstring inventory と `# ── N.` section が 1 対 1。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 「書いた値が読み戻されるか」の形をした invariant を足すならここが定位置。
- 新しい top-level field を store に足したら、373 / 404 / 405 のいずれかが**追従を要求する**（これが狙いである）。

## Audience-specific notes

### For AI agents（次担当）

- 役割タグ: `check-split`, `store-contracts`, `producer-consumer`, `persist-round-trip`
- **この family の Check は「default に在る key」を起点に導出している。** 決め打ちの key 一覧に書き換えないこと ―― 新しい field が足された瞬間に検査対象から外れる。
- 実バグの再発を疑うときは、まず **export が書くキー集合と import が読むキー集合を突き合わせる**（#1035〜#1040 はすべてこの突き合わせで見つかった）。

### For human engineers（新卒レベル）

アプリは状態を保存するとき「保存する形」に整えてから書き、読むときも同じ関数を通す。このとき**書く側にはあるのに読む側が知らないフィールド**があると、そのフィールドだけが毎回消える。画面にはエラーが出ないので、利用者は「なぜか設定が戻る」としか感じない。この module はその食い違いを CI で止める。

### For third parties / auditors

各 Check は実際に起きたバグ（#139 / #684 / #924 / #1036 / #1037 / #295 / #561）を起点に追加されており、per-instance の修正を構造防止へ昇華した記録になっている。分離は byte-equivalent（section 無改変・free-variable 解析で事前検証）で、自己整合 Check が monolith + 全 split module 横断で緑であることが証跡である。

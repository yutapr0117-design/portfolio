---
file: .github/scripts/checks_license_register_structure.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-27
canonical-ref: .github/scripts/checks_license_self_reporting.py (自己申告した「数」を守る側) / docs/architecture/check-repository-consistency-map.md
---

# .github/scripts/checks_license_register_structure.py

## What

ライセンス register の**構造**が機械可読で在り続けることを守る 3 Check。

- **469** 自己申告の「列挙」が、消化した項目で古くならないこと
- **474** 不利な事実の register が、潰すための backlog として機械可読であること（state token）
- **475** 反証表の全行が日付つきの状態を宣言していること

## Why

**`checks_license_self_reporting.py` から 2026-09-27 に切り出した。引き金は advisory 予算
（800 行・実測 944）だが、割る線は行数ではなく主題で選んだ。**

**あちらは「自己申告した *数* が実測と合うか」、ここは「自己申告した *構造* が使える形で
在り続けるか」。** **読み手も直し方も違う** —— 数はふつう**申告側**を直し、
構造は **register 側**を直す。

**なぜ「数」と「構造」を分けるのが正しいか**: 列挙（469）は**項目を消化するたびに古くなり、
しかも減る側へ drift する**ので「増えたか」を見る習慣では永久に検出できない。
これは件数の drift とは検出の形が違う。

## How

`CHECK_SOURCE_FILES` に登録し、`check_repository_consistency.py` が `run(_ctx)` で呼ぶ。
**`_L460` という名前は切り出し元から引き継いでいる** ——
**移した本文を書き換えないため**（書き換えると差分が「移動」ではなく「改変」になり、
何が動いて何が変わったのか読めなくなる）。

## Constraints

- **`warnings = ctx.warnings` を明示的に束縛する**（Check 385 が bare append を禁じる）。
- **section header の `# ── N.` は 1 か所にしか書かない**（Check 45b が二重計上を検出する）。
- 新しい Check を足すときは docstring の inventory も同じ commit で足す（Check 45）。

## Change impact

**この file が守っているのは「我々自身の記録の使い勝手」であって、ACD-1.0 の本文ではない。**
落ちたときに直すのは register か、その申告のどちらかで、**本文は動かない。**

## Audience-specific notes

- **監査人**: 3 Check とも BLOCKING。落ちた場合、メッセージが「宣言のみ / 実装のみ」の形で差分を出す。
- **第三者**: ここは内部の品質機構で、ライセンスの法的意味には関与しない。

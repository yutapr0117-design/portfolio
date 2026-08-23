# improvement-notes — v80+ phase4「ライセンスを機械可読にする + 早期警告が構造的に効かない層の根治」run (2026-08-23)

```
Author           : Claude Opus 5 (Anthropic) — Claude Code
Orchestrator     : Yuta Yokoi (横井雄太)
Scope            : PR #1266 (rebase-merge・main 全緑)
Canonical-Ref    : AI2AI.md Session Record #31 (要点) / CLAUDE.md §7
Prev             : (同一セッション前半) PR #1264 / #1265 — Session Record #30
```

## この run の軸

前半 run で独自ライセンス **ACD-1.0** を起草し `All Rights Reserved` を撤回した。その直後に
**「では、その許諾は機械から見えるのか」**を測ったのが本 run の起点。答えは **7 面すべてゼロ**
だった。そこから派生して、**早期警告の層そのものが一部の file で無効**という基盤の欠陥と、
**安全網の anchor が一意なまま別対象へ移る**という検出困難な class に行き着いた。

---

## 1. 🔴 ライセンスが機械可読な面のどこにも宣言されていなかった

### 実測 (2026-08-23)

    <link rel="license">      : 0   (HTML 標準)
    JSON-LD の license        : 0   (12 ノード全て・schema.org 標準)
    sitemap.xml               : 0
    .well-known/aio-manifest  : 0
    llms.txt / llms-full.txt  : 0
    robots.txt (Allow 34 件)  : 0
    manifest.webmanifest      : 0

### なぜ「登録漏れ」以上の問題なのか

**ACD-1.0 §6.5 自身が**こう述べている ——

> a permission that an automated system cannot determine is, for the purposes of a work
> meant to be learned from, no permission at all

つまり**本文が発見できない状態は、ライセンスが自分の主張を満たしていない**ということ。
AIO を最優先の賭け金に据えたリポジトリで、最も痛い形の「宣言はあるが実態が伴わない」
(#929 幻セレクタ / #930 route 追従 JSON-LD / 同日の archive #14 と同じ class)。

### 配線した面と、足さなかった面

HTML 標準 (`rel="license"`) / schema.org (`license` を CreativeWork 系 3 ノード) /
sitemap の `<loc>` / robots の Allow / aio-manifest の top-level `license` /
llms 2 面の `Licensing and AI Training` 節。

manifest の宣言は **エージェントが 1 回の fetch で判定できる形**にした ——
`rights_reserved: false` / `conditions: []` / `ai_training_permitted: true` /
`tdm_reservation: false` / `attribution_required: false`。散文を読ませない。

**`manifest.webmanifest` には足していない。** W3C Web App Manifest 仕様に `license` メンバーは
存在せず、**規格に無いキーを足すのは「宣言したつもり」を増やすだけ**だから (Check にもしない)。

### Check 444 (BLOCKING)

5 面それぞれが消えても気付ける形に。canonical URL と SPDX 識別子は **`LICENSE` の
`Full text:` 行と `SPDX-License-Identifier:` 行から導出**する —— 決め打ちすると path を
変えたとき **Check だけが古い場所を指す** (Check 124 / 411 / 434b と同じ scope-drift)。

---

## 2. 🔴 早期警告が「構造的に一度も出ない」file が 6 つあった

このリポジトリは **「advisory は BLOCKING を踏む前に効かせる」**を標準規律にしている
(過去 2 回、advisory を素通りして BLOCKING に激突した反省から)。ところが実測すると、
**その規律が働かない file が 6 つ**あった。

advisory 予算が **hard ceiling (Check 365 の 1,000 行) と同値かそれ以上**だと、Check 52 の
警告は一度も出ない —— OK からいきなり BLOCKING へ飛ぶ。

    mutation_samples_archive.py      予算 1000 / 実測 999  ← BLOCKING まで 1 行で無警告
    mutation_samples_e2e_archive2.py 予算 1000 / 実測 971  ← 29 行で無警告
    check_repository_consistency.py  予算 4750 / 実測 869  ← 分割完遂前の残骸。6 倍で永久に鳴らない
    js/apps.js / archive2 / e2e_archive            予算 1000

しかも `file-size-budget.md` §2 の説明文が

> ceiling は Check 365（全非 A テキスト ≤1,000 BLOCKING）に整合させ 1,000 とする

と、**欠陥そのものを設計として記述**していた。「hard ceiling に合わせる」は一見正しく見えるが、
advisory の役割は hard ceiling の**手前**で鳴ることなので、合わせた瞬間に無意味になる。

予算を下げた瞬間、2 file が**初めて**警告を出した。

### Check 443 と、その初版の欠陥

「advisory 予算 < hard ceiling」を BLOCKING で強制する。**射程は Check 365 と同じ除外集合から
導出する** —— main.js / style.css / index.html は hard ceiling の対象外なので 1,000 超の予算が
正当 (警告すべき BLOCKING が存在しない)。**初版はこれを見ておらず、正しい設定 3 件を誤検出した。**
除外集合は module level の単一ソース (`HARD_CEILING` / `CEILING_EXEMPT_*`) へ持ち上げて
Check 365 と共有した (片方に file を足してもう片方を忘れると、逆の穴が開く)。

---

## 3. 🔴 mutation anchor が「一意なまま別ノードへ移動」していた

JSON-LD の WebSite ノードへ `"license"` を 1 行挿入したところ、`Check 193` の anchor
(`"url"` の直後に `"inLanguage"` が来る並び) が **WebSite から TechArticle (`#ai-context`) へ
silent に移った**。

- anchor は**依然として一意** (出現回数 1)
- **Check 362 (解決するか) も Check 420 (一意か) も捕捉できない**
- Check 193 は WebSite.url しか見ないので、**別ノードを壊しても緑 = SURVIVED**

**検出できたのは probe を実際に回したから。** @id 起点へ付け替え、クリーンな状態でフル probe を
回して **All 337 mutations caught** を実測した。

> **教訓: mutation が anchor する file を編集したら、その場で probe を回せ。**
> 「解決する」「一意である」は「正しい対象を打っている」を意味しない。

### 同 class を本日 5 件

anchor が**可変値に釘付け**だと、その値が動くたび orphan 化して維持コストを増分ごとに課す ——
digest 値 2 件 / 追跡ファイル総数 1 件 / 日付 1 件 / JSON-LD の generic な property 並び 2 件。
すべて **その file の中で最も動かない部分** (SPDX 接頭辞 / ノード固有の @id / 不変の定数) へ
付け替えた。

---

## 4. rotate に rebalance モードを追加

archive 自身が entry 編集 (WHY コメントの追記や anchor の付け替え) で伸びるのに、
**溢れたときの自動の逃げ道が一つも無かった** —— 受け皿に 130 行以上の余裕があったのに、
移す手段が存在しなかった。同じ chain 内で「溢れた archive の**末尾** → 次の archive の**先頭**」
へ移す (時系列順を保つ)。総数不変を invariant として検証する。

**書き出しで末尾改行を落とす欠陥も同時に修正**した —— 落とすと `wc -l` と `splitlines()` が
1 ずれ、Check 424 と Check 52 が**同じ file に違う行数を報告する**。同日その食い違いで §2 表を
誤った値へ「修正」して CI を赤にしたばかりなので、書き出す側でも再発させない
(Check 52 側は `splitlines()` へ統一済)。

---

## 5. この run で繰り返し効いた規律

1. **宣言を数え上げ、それぞれに「見ている層があるか」を突き合わせる。** 本 run はこの棚卸し
   だけでライセンス面 7 つの穴を出した (#1009 で確立した手法の再適用)。
2. **自分のゲートの欠陥は非 vacuity 検証だけが教える。** Check 443 の初版は正しい設定を
   誤検出した。「汎用化した」と書く前に、動機となった実例と**正当な例外**の両方で測る。
3. **測定系を疑う。** 行数が 1 ずれた原因は製品ではなく、2 つの Check が違う数え方をしていたこと。
4. **advisory を上げて黙らせるのではなく、下げて早く鳴らす。**

---

## 6. 検証

- `npm run verify` = exit 0
- `npx playwright test` = **473 passed / 0 failed**
- `mutation_probe` (consistency フル) = **All 337 caught**
- Check 443 / 444 は 5 面 + 5 面それぞれを個別に破って **RED を実測**
- 前 PR の本番反映を確認 (`LICENSES/ACD-1.0.txt` が公開面で 200・本文一致)

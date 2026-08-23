# improvement-notes — v80+ phase4「ライセンス面の被覆完成 + probe が私の race を捕捉した」run (2026-08-23)

```
Author           : Claude Opus 5 (Anthropic) — Claude Code
Orchestrator     : Yuta Yokoi (横井雄太)
Scope            : PR #1269〜#1273 (全 rebase-merge・main 全緑)
Canonical-Ref    : AI2AI.md Session Record #32 (要点) / CLAUDE.md §7
Prev             : improvement-notes-claude-v80-phase4-machine-readable-license-and-inert-warning-layer.md (#1266)
```

## この run の軸

前 run で「ライセンスが機械可読な 7 面すべてで宣言ゼロ」を塞いだ。本 run はその**被覆を
実際に測って完成させる**ところから始まり、**同じ「走査対象に入らない」class を 3 段掘り下げた**。
最後は週次 probe が**私自身のテストの race** を捕捉して終わっている。

---

## 1. 🔴 JSON-LD の CreativeWork 10 ノードが無宣言だった

前 run で 6 面へ配線したあと、**runtime でレンダリングされた DOM を実測**したところ、
CreativeWork 族 11 ノードのうち **10 ノードが license を持っていなかった**。

    ImageObject ×3 / AudioObject ×3   ← binary の XMP と ID3 は ACD-1.0 と言っているのに無言
    TechArticle (#ai-context) / FAQPage
    WebPage (#webpage-dynamic)        ← route 追従。レンダリングするクローラが読むのはこちら
    WebPage (speakable)               ← 音声アシスタント向け

**とくにバイナリ資産の不整合は同じ run で私が作ったもの** —— embedded metadata を ACD-1.0 へ
更新した一方で、同じ資産を記述する JSON-LD を放置していた。**同じものについて面ごとに答えが
違う**状態は C6 が守ろうとしている当のもの。

**対象は schema.org の CreativeWork 族のみ**にした。Person / Organization / BreadcrumbList は
CreativeWork ではないので付けない —— 機械的に全ノードへ付けるのは意味論の水増し。

---

## 2. 🔴 主要 WebPage ノードが全ルートで 2 つの名前を主張していた

JSON-LD の意味論では **同じ `@id` = 同じエンティティ**で、複数の宣言は property が merge される。
実測すると `#webpage` が**全ルートで 2 回宣言され、`name` が 2 通り**あった。

    /#/projects   static="yuta - AI-Driven PM | ポートフォリオ"
                  speakable="Projects | yuta - AI-Driven PM"

このサイトは「`Yuta Yokoi` / `横井雄太` へのクエリは**このエンティティにのみ**解決すべき」を
中核宣言に据えている。その面で**主要ノード自身が曖昧だった**。

ルート固有の名前は main.js が `#webpage-dynamic` (別 @id) として既に公開しており、そちらが
正しい置き場。speakable ノードに残すのは **全宣言で値が一致するもの (license)** と
**この node の存在理由そのもの (speakable)** だけにした。

`speakable` プロパティは検査対象から除いた —— schema.org は複数値を許し消費側は**選択肢の
合併**として扱えるので害が出ない。「どれが正か決められない」問題が生じるのは単一値が
期待される識別子系プロパティなので、そこに絞った。

---

## 3. 🔴 Article ノードだけ license が無かった — テストのルート一覧が死角を作っていた

Article は `ARTICLE_ROUTES` (= `ai-knowhow`) のルートでしか注入されないので、

- **静的 Check 444b** は `index.html` のソースを読む → runtime 注入なので存在しない
- **e2e** はルート一覧が `/` `/#/projects` `/#/quiz` → **そのノードを一度も走査しない**

という **両方の死角**に落ちていた。「既定の状態だけが偶然 clean」class (#1213 / #1214 / #1219)。

> **走査対象に入らないものは、どれだけ厳しい assertion を書いても検査されない。**

修正は**ルート一覧の拡張とセット**。これをやらないと同じ死角が残り続ける。
さらに `LICENSE_ROUTES` が 2 ルートである**理由**を spec に明記した —— このリポジトリは
「silent に被覆を縮めない」を規律にしているので、意図的な絞り込みは**そう書いていないと
見落としと区別できない**。

---

## 4. 🔴 週次 probe が私自身のテストの race を捕捉した

本日追加した e2e 3 件を mutation 登録して behavior probe (380 mutation・54.6 分) を回したところ
**1 件が SURVIVED**。しかも**手動では RED になっていた** —— 「明白に vacuous」ではなく
**通ったり通らなかったりする**より悪い状態。

### 根本原因 — 待ちが 2 つとも「前ルートの残骸」で充足する

    await expect(page.locator('#content h1')).toBeVisible();                              // (1)
    await expect.poll(() => locator('script[data-ld="dynamic-route"]').count()).toBe(1);  // (2)

- **(1)** は落とし穴表が警告している当のパターン
- **(2)** も同じ —— `dynamic-route` の script 要素は**ルートを跨いで再利用される**
  (`if (!existing) create`) ので 2 周目は**何も待たずに即成立**する

結果、2 周目では **Article ノードが注入される前に走査**が走り、「そもそも存在しないノード」を
「欠落ゼロ」と読んでいた。

### 直し方 — ルート固有の信号でしか待たない

    { path: '/#/projects',   h1: 'プロジェクト一覧', article: 0 }
    { path: '/#/ai-knowhow', h1: 'AI開発ノウハウ',   article: 1 }

見出しは**そのルートでしか出ないテキスト**で `toHaveText` 待ち、条件付きで注入される要素は
**期待個数を control として `expect.poll`** する。

### 私の手順の誤り

前回は手動条件 (env なし) で RED を確認して満足し、**probe が実際に使う条件での成立を
確かめていなかった**。**#1073 で同じ誤りを記録していたのに再発させた。**
今回は `MUTATION_PROBE=1` で 3 回ずつ測り mutated 3/3 failed・restored 3/3 passed を確認。

`dynamic-route` の再利用は落とし穴表に**無かった新種**なので中央の表へ追記した。

---

## 5. advisory 予算超過を全てゼロに

- `aio-meta.spec.js` 907 → 688 (agentic-state 5 テストを分離)
- `quiz.spec.js` 923 → 599 (遅延読み込み契約 8 テストを分離)
- `js/quiz-renderer.js` 407 —— **分割せずラチェット**。総 407 = コメント 132 / 空行 42 /
  **コード 233** で、超過は冗長さではなく**実バグ修正 6 件の蓄積**。35 行の純関数を切り出す
  churn に見合わないと判断 (#253 と同型)。

Check 120 (配信バイト) には **3 回**当たり、毎回「上げる前に削れないか」を測った ——
**1 回目**: コメント圧縮 + 実測後にラチェット (コメント全削除でも超過 = コードの分) /
**2 回目**: コメント圧縮のみで**上げずに解決** /
**3 回目**: 差分が 1 行でコメントゼロ = 削る対象が構造的に無いことを確認してラチェット。

---

## 6. この run で繰り返し効いた規律

1. **走査対象に入らないものは検査されない。** 修正とルート一覧の拡張はセットで行う。
2. **非 vacuity は probe が実際に使う条件で測れ。** 条件を変えて RED を得ても、
   probe 上で成立する保証にはならない。
3. **意図的な絞り込みは「そう書く」。** 書かないと見落としと区別できない。
4. **測定系を疑う。** ルート網羅の監査で `ALL_ROUTES` が「網羅 0/17」と出たのは、私のパーサが
   オブジェクトリテラルを壊しただけで**発見ではなかった**。結論に含めなかった。

## 7. 検証

- `npm run verify` = exit 0 / advisory 警告 **0 件**
- `mutation_probe --e2e` = 380 mutation (54.6 分)。SURVIVED 1 件を修正し、
  **probe が使う条件で 3/3 決定的**を実測
- Check 総数 445 / E2E mutation 380 / consistency mutation 340

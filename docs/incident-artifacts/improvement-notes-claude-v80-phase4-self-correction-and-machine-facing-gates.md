# improvement-notes — v80+ phase4「自己訂正 + 機械可読面ゲート」run (2026-08-21)

```
Author           : Claude Opus 5 (Anthropic) — Claude Code
Orchestrator     : Yuta Yokoi (横井雄太)
Scope            : PR #1245〜#1251 (全 rehase-merge・main 全緑)
Canonical-Ref    : AI2AI.md Session Record #29 (要点) / CLAUDE.md §7
Prev             : improvement-notes-claude-v80-phase4-critical-path-and-self-correction.md (#1236〜#1243)
```

## この run の軸

前 run で入れた遅延読み込みの後始末を続けつつ、レンズを
**「機械可読面の契約は誰が見ているのか」** と **「自分の測定を疑う」** へ寄せた。
結果として **実バグは 1 件 (a11y)** で、残りは **ゲートの新設**と
**自分が書いた誤りの訂正**が中心になった。

## 成果

### 🔴 #1246 英語だけの文 5 箇所に `lang="en"` が無かった (WCAG 3.1.2)
既存ゲートは **quiz 限定**かつ判定が `^[\x20-\x7E]+$` (ASCII のみ) で、
**絵文字や `→` を含む英語見出しを見逃していた** (`📋 Executive Summary` /
`Read Technical Deep-Dive →`)。全 16 ルート版のゲートを新設。

**意図的に対象外**にしたもの: 1 語だけのラベル (`Productivity`) / メール・URL・版数 /
固有名詞だけの塊 (`Classic Blue + Inter`)。除外条件はコードにあり **緩めると RED**。
残る 2 件が実在することも control で確認 (消えたら KNOWN も畳むべき)。

### 🟢 #1249 動的 import の MIME を公開面で検証する
遅延読み込み (#1239) は **新しい失敗モード**を作っていた —— 動的 import は
**MIME が JavaScript でないと即座に失敗する**が、それを見る層が無かった:

    リポジトリ側の Check   … ローカルの file しか見ない (MIME は配信側の性質)
    behavior e2e           … ローカル http-server の MIME を見るだけ
    公開面の sha256        … 中身は見るが **ヘッダは見ない**

本番を実測すると `application/javascript; charset=utf-8` で正常。同時に
**公開 index.html の quiz modulepreload 0 件 / 公開 main.js の動的 import 4 件**も確認でき、
本番が遅延化版を正しく配信していることも裏取りできた。

### 🟢 #1248 agentic surface が敵対的 query でも壊れない JSON であること
`filter` は URL の query をそのまま echo するので、**攻撃者が中身を決められる唯一のフィールド**。
実害は「クラッシュ」ではなく **agent 側が丸ごと解釈不能になる**こと。
4,000 文字 / `"><script>` / 改行 / `__proto__` / 不正 percent すべてで JSON は valid。
**上限は設けなかった** —— 通常操作では作れない URL であり、必要性を実測で示せないまま
bound を足すのは padding。固定したのは**パース可能性**に絞った。

### 🟢 #1250 Check 440 — コード側から `docs/` への参照が解決する
落とし穴表は「e2e を書く前に読む 1 箇所」なのに、**入口である `playwright.config.cjs` から
導線が 0 件**だった。導線を足し、腐りを機械強制。Check 化の前に誤検出率を測り
**7 参照すべて解決＝ゼロ**を確認。prose 全般 (#977 で「Check にしない」) と違うのは、
**コードコメントの導線は常に「今そこにある doc」を指すべき**だから。

### 🟢 #1247 ルートループの stale-wait 掃引 —— 結果は honest clean
e2e 全 spec のルートループ 13 個を掃引。`LANDMARK` は `main` がルート非依存、
`BP` は settle が効き、`IDREF` も dangling `aria-labelledby` で RED。
**「settle が無い ⟹ vacuous」ではなかった。** `IDREF` の待ちだけ決定的にした
(vacuous を直したのではなく、タイミング依存を外しただけ —— overclaim しない)。

### 🟢 #1245 自分が書いた誤りの訂正
オフライン degrade テストに「**SW が shell を返すので**枠は出る」と書いたが**誤り**。
実測: `caches.keys()` は空 / オフラインで**完全リロードは失敗** ——
**このサイトはオフライン対応ではない**。枠が出るのは同一文書の hash 変更で shell が
メモリ上にあるから。**リポジトリ側の doc (`docs/files/sw.js.md`) は最初から正しかった**。

### 🟢 #1251 大量データ seed の正しい手順 (4 回誤診した末に確立)
219 件を `localStorage` へ注入 → 描画 19 枚、しかも localStorage 自体が 19 件に戻る。
原因は **退出するページが unload / pagehide でメモリ上の state を書き戻す**こと。
**debounce を 900ms 待っても `page.close()` してもダメ** (flush は unload 時なので無関係)。
正しい手順は `context.addInitScript` で**起動前に仕込む**。これで測ると
**219 件が 571ms で全件描画**され検索も正しく効く (= 大量データでも健全)。

## 教訓

- **非 vacuity の検証は「壊した対象がその test の検査範囲に入っているか」から確かめよ。**
  `danglingIdrefs` は `aria-*` だけを見るのに `<label for>` を壊して「素通り」と誤診した。
- **mutation スクリプトはファイルに書き、成功印を出力させてから走らせよ。**
  shell の引用符崩れで `assert` が落ちても後続の test は走るので「当たっていないのに緑」を読む。
- **「どの writer がその経路の責任者か」を取り違えると非 vacuity を誤判定する。**
  `data-ai-state` は writer が 3 箇所あり、直接 URL は main.js 側が書く。
- **測定系を疑う (本 run で 3 回とも当たった)。** `localStorage` 注入の unload flush (4 回) /
  SW が shell を返すという思い込み / `page.coverage` の精度。
- **信号が出ないなら何も作らない。** `page.coverage` による未実行関数の洗い出しは、
  ナビゲーションのみでは対話ハンドラが軒並み出るうえ `QuizPage` まで DEAD と報告され、
  actionable にならなかったので**打ち切った**。
- **制御できないものを Check にしない。** 公開面の `Cache-Control` は GitHub Pages 固定
  (`max-age=600` + ETag)。Check 化すると彼らが既定を変えた瞬間に赤くなる brittle gate。

## 未着手の vein (次の AI へ・非拘束)

- AIO 層の archive 範囲 (#14 まで) —— #15〜#19 は archive されているが AIO 面に出ていない。
  埋めるには manifest の semantic 編集＝ **C6 (要 orchestrator 承認)**。
- 他のルート専用モジュールの遅延化は **render core (§3 高リスク面)** に触れる。
  quiz が安全に切れたのは「見出し + 検索欄を同期に描ける」構造だったから。
- 未実証 e2e の残り / apps 間のより深い相互作用 / research 適用。

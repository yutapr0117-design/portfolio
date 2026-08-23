---
file: playwright.config.cjs
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-11
canonical-ref: e2e/portfolio.spec.js / .github/workflows/playwright-regression.yml
---

# playwright.config.cjs

## What

Playwright 設定。CJS 形式 (Node 24 でも安全)。Chromium で e2e 実行、http-server で `./` を serve、snapshot 比較設定、retries 等。

## Why

ESM (config.mjs) を選ばずに CJS にしたのは Playwright v1.60 の安定性と CI 環境互換性のため。

## How (usage)

```
npx playwright test --config=playwright.config.cjs
  └─ webServer: npx http-server -p <port>
  └─ projects: chromium のみ
  └─ snapshot pixel diff threshold 設定
```

## Constraints

- **Check 23**: JS 構文 valid (node --check)
- **Check 51**: バージョン pin が runbook と一致 (1.60.0)

## このリポジトリの e2e で繰り返し踏んだ落とし穴（実測に基づく）

> **不変性アサーションの棚卸し（2026-08-17 実測・再実行不要）**: 「操作 → settle も expect も
> 挟まず単発 `evaluate` で読む」形は全 spec で **3 件**だけで、いずれも **同期更新される値**
> （focus / textarea の value / documentElement の属性）を読んでおり安全。**静的 Check は
> 作らない** —— この 3 件を RED にする brittle gate になるため（「どの操作が非同期再描画を
> 起こすか」は静的に決まらない）。危険なのは *非同期再描画* が絡む場合だけで、その 1 件は
> #1112 で修正済み。
>
> **不在アサーションの棚卸し（2026-08-17 実測）**: `not.toContainText` / `not.toBeVisible` /
> `toHaveCount(0)` / `not.toContain` は全 spec で 95 箇所。うち「同じ test 内に先行する肯定
> アサーションが無い」ものは **1 箇所だけ**で（cross-tab の negative baseline）、実測では
> その時点で描画済みだったが `domcontentloaded` は描画を保証しないため明示的な待ちを足した。
> 残りはすべて肯定アサーションが先行しており健全。**この監査は再実行しなくてよい**。

テストは「壊れる」より **「鈍る」** 形で失われる（前提が崩れて緑のまま無力化する）。以下はいずれも
**実際に vacuous なテストや false-red を生んだ**もので、書く前に知っておくと 1 サイクル節約できる。

| 落とし穴 | 何が起きるか | 正しい書き方 |
| :-- | :-- | :-- |
| **`page.route` の遅延を `setTimeout(N)` で作り、その N ミリ秒の間に検証が終わることに賭ける** | 「読み込み中」のような**一過性の状態**を観測する test で、先行する待ち（`#content h1` の可視など）が N を超えると**その状態が消えた後**に検査することになる。`toHaveCount(1)` が 0 のまま poll し続けて落ちるので、**回帰でないのに BLOCKING gate が赤くなる**。実測（2026-08-23・quiz の aria-busy テスト）: 単独実行 3 回で 1 failed / 2 passed、かつ **main でも再現**したので、変更由来の回帰ではなく元から時間に賭けていたと確定した | **明示的な解放ゲート**にする。`let release; const gate = new Promise(r => { release = r; });` を作り、route handler では `await gate` してから `route.continue()`。一過性の状態を検証し終えてから `release()` を呼ぶ。これで観測できる長さがマシン速度に依存しなくなる（5/5 決定的を実測）。検出力は不変で、その状態を作らない退行を入れると同じ control が RED になる |
| **runtime 注入される要素の「存在」を待ちに使う** | `script[data-ld="dynamic-route"]` のような **ルートを跨いで再利用される要素** (`if (!existing) create`) は、2 周目以降 **何も待たずに即成立**する。汎用の `#content h1` 可視待ちと組み合わせると**両方が前ルートの残骸で充足**し、新ルートが描き終わる前に走査してしまう。実測 (2026-08-23): この race で **ローカルでは RED・週次 probe では SURVIVED** という環境依存の偽陽性が生まれ、「そもそも存在しないノード」を「欠落ゼロ」と読んでいた | **ルート固有の信号で待つ**。見出しは `toHaveText(そのルートでしか出ないテキスト)`、条件付きで注入される要素は**期待個数を control として `expect.poll`** する (例: Article JSON-LD は article ルートで 1・それ以外で 0)。「要素が在るか」ではなく「**このルートの状態になったか**」を待つ |
| `waitForLoadState('networkidle')` | 外部 Fonts / service worker の background fetch で CI が 30s ハングする flake（screenshot 以外では禁止・Check 111） | `domcontentloaded` + expect の auto-wait |
| **cross-tab を合成 `StorageEvent` で再現する** | `window.dispatchEvent(new StorageEvent(...))` は listener を呼べるが、**実 2 タブとは挙動が違う**。実測（2026-08-17）: 合成イベントでは「編集中の他タブ更新が失われた」ように見え、**ドキュメントの記述（#940「延期であって破棄ではない」）と矛盾するデータ消失バグを報告しかけた**。実 2 タブ（`context.newPage()` ×2）で測り直すと両方保持されており、記述の方が正しかった。合成イベントは localStorage への実書き込み順序や debounce 保存との競合を再現しないため | **実 2 タブ**で測る（`browser`/`context` fixture で 2 ページを開く）。合成イベントは「listener が登録されているか」の確認までに留める |
| **「起きないこと」を非同期処理の直後に読む** | 検査対象が `await` を挟む非同期（`window.render()` は `yieldToMain()` を挟む）だと、切替直後の読み取りは**まだ起きていない状態**を掴む。つまり **実際には起きていても「起きていない」と読めて通る**。実測（2026-08-17）: 同じ mutation がローカルでは CAUGHT・週次 probe（CI）では **SURVIVED** になり、環境で結果が変わる race だった | **settle させてから 1 度だけ読む**。`await page.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))))` で「起きるなら起ききった」状態にする。poll は使えない（不変性の検査では最初の観測で成立してしまう） |
| **不変性の検査に `expect.poll`** | poll は**最初の観測で条件を満たした瞬間に成功**するため、その後に起きる変化を見逃す。「スクロール位置が動かないこと」を poll で書いたら 2 つの実バグ mutation が**両方素通り**した | settle を待ってから **1 度だけ**確定値を読む |
| （上 2 行の使い分け・2026-08-17 に実測して確定） | **違反が「一過性」か「持続」か**で正しい書き方が変わる。**一過性**（スクロールが動いてから戻る等）は poll だと途中を拾って通ってしまうので settle 後に 1 度読む。**持続**（入力が消えたまま・要素が別ノードに置き換わったまま）は、むしろ `toHaveValue` などの **auto-retry が正しく捕捉する** —— 実測: 絞り込みを全再描画へ戻す mutation は `toHaveValue` の retry で **5/5 決定的に fail** した。逆に retry の無い**単発 `evaluate`** は非同期処理の前に読んで false-pass する（#1112） | 「違反したら**その状態が残るか**」で選ぶ。残るなら auto-retry / 残らないなら settle して 1 度読む |
| 不在の検査（`toHaveCount(0)`）を goto 直後に評価 | async 描画とレースし「まだ無い」を「無い」と誤認する | 先に「在るはず」の要素の visible を待って描画を確定させる |
| **不在の検査の対象を、そのページが描画しないものにする** | 「`[object Object]` が出ないこと」を ContactPage で `profile.name` について検査していたが、**ContactPage は `name` を描画しない**（描くのは email / github / linkedin）。しかも github・linkedin は `safeStr` ではなく `safeUrl` を通る。つまり守りたい関数の型ガードを外しても**その文字列が現れる余地が無く、最初から何も検査していなかった**。もう 1 つのケースが生きている間は隠れており、そちらが独立ガード追加（#1080）で通らなくなって初めて週次 probe が SURVIVED として露出させた（#1096） | 検査対象は「**守りたい関数を実際に通り、かつそのページが描画するフィールド**」から選ぶ。選んだら `control`（その要素が実際に描画されている）を同じ test に置く —— 実際にこの control が 2 回落ちて思い込みを潰した |
| `fill()` で入力を検証 | value を直接代入するため focus 喪失系のバグを検出できない（quiz 検索の focus 喪失が gate を素通りした） | 実キー入力の `type()` / `keyboard.insertText()` |
| `toBeFocused()` | 並列ワーカーで document が inactive になり `unexpected value "inactive"` で間欠 RED（8 回中 3 回） | `document.activeElement` を `evaluate` で読む |
| `offsetParent !== null` で可視判定 | **`position: fixed` の要素では常に null** になり、開いている drawer を「閉じている」と誤報告する | `getBoundingClientRect()` + computed style |
| 通常の `click()` で sticky 要素を検証 | actionability 判定でページがスクロールし、実機のタップ挙動と乖離する | `evaluate` 内の programmatic click |
| `--reporter=line` の出力を `tail -N` で読む | **失敗一覧はサマリの後に出る**ため、`tail -2` だと `2 failed` の行が切れて `27 passed` だけが見え、**失敗を成功と誤読する**（実際に 2 度踏み、既存テストを壊したまま PR を出した） | `grep -E "failed\|passed"` で明示的に拾う |
| CI の behavior ゲートが赤い原因を、まずコードだと考える | ゲートは実測で **1 ナビゲーションごとに 6 つの第三者ホストへ 9 リクエスト**（KARTE ×4 / Google Fonts ×2）を出しており、`page.goto()` の既定 `waitUntil` が `'load'` なので**その完了を待って**いた。外部が遅い/落ちるだけでコードが正しくても赤くなる（2026-08-10 に `.hero-section` の 30s timeout として実際に発生） | CI の behavior ステップは `E2E_HERMETIC=1` で外部 DNS を即 NOTFOUND にして切り離してある（Check 416）。ローカルで再現しないときは**外部起因を先に疑う**。probe も同 env を渡す（外部起因の失敗は **false CAUGHT** になるため） |
| `MUTATION_PROBE=1` を付けて SW 関連テストを回す | この env は **設計上 service worker を block** するため、SW 登録テストは必ず落ちる（config の env-gate 参照）。原因を製品側と誤診する | SW を含む検証は env なしで回す（CI と同条件） |
| mutation の `-g` を緩い語で当てる | 別の test に当たって「pass」と読み違える（実際に一度誤読した） | **正確な test title** を使う（Check 397 が一意解決を強制） |
| `evaluate` 内で `el.style.setProperty(...)` して**同じ evaluate の中で**結果を読む | **本サイトは `CSSStyleDeclaration.prototype.setProperty` と `setAttribute('style', …)` を上書きし、書き込みを `_writeQueue` へ積んで rAF でまとめて流す**（`js/perf-guards.js` の layout-thrash 対策）。同期で読むと**書き込み前の値**が返り、`getAttribute('style')` すら `null` のまま。結果、候補 CSS を当てても「何も変わらなかった」と読めてしまい、**診断が丸ごと偽陰性になる**（実際に 1 サイクル分の測定を無効にした）。`bypassCSP: true` でも直らない（CSP ではなくサイト自身の機構なので） | 書き込みと読み取りの間に **rAF を 2 回 await**（`page.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))))`）。あるいは `style.css` を直接編集して測る。**`page.addStyleTag` は CSP で弾かれる**ので使えない |
| `mutation_probe.py` に `--only` 等の**存在しないフラグ**を付けて 1 件だけ回したつもりになる | 引数解析は `"--e2e" in sys.argv` の形なので**未知のフラグは黙って無視され、全件（30 分超）が走り出す**。途中で kill すると **mutated なファイルがワークツリーに残る**（実際に `js/pomodoro-page.js` が残留した） | 単一 mutation の非 vacuity は**手で当てて外す**（該当箇所を消す → 正確な test title で `-g` 実行 → RED を確認 → 復元）。kill した後は必ず `git status --porcelain` で残留を確認する |
| `selectOption()` で「変更後も focus が select に残るか」を検証する | Playwright の `selectOption()` は選択後に **focus を select に残さない**。そのため focus 復元の有無にかかわらず `activeElement` は BODY と読め、**修正済みでも落ちる false RED** になる（実測: 同じコントロールで dispatch 版は復元を観測できたのに selectOption 版は BODY のままだった） | キーボードで選択肢を変えたときと同じ「focus したまま change が飛ぶ」形を自分で作る（`el.focus(); el.value = …; el.dispatchEvent(new Event('change', {bubbles:true}))`） |
| ルートを連続で `goto` して `#content h1` の visible だけ待つ | その条件は**前のルートの描画**で既に満たされているため、**前ページの DOM を掴んだまま**次の検査に入る（実測で projects の select を todo ページの検査が拾った） | `page.locator('#content h1', { hasText: '<そのページ固有の見出し>' })` を待つ。ルートごとに `test()` を分けるのも有効 |
| 「元の値に戻ること」を、**そもそも値が動いていない**経路で検証する | 復帰そのものを一度も通らないので、**復帰のコードを丸ごと削除しても緑**になる。実測 2026-08-21: ポモドーロの「リセットで満了値へ復帰」は、稼働中の残り時間が `endAtMs` から計算され `remainingSec` は一時停止でしか書き換わらないため、`start → 進める → reset` の経路では削除しても 25:00 のまま通った（通っていたのは復帰したからではなく **drift していなかった**から）。同じ削除でも `start → 進める → 一時停止 → reset` なら 24:55 が残り RED になる | **戻す前に、実際に値をずらす**。ずれたことを **control** として先に assert してから復帰を検証する（`expect(timer).not.toHaveText(full)` を挟む） |
| ダーク/テーマ依存の CSS を **最初に見つけた宣言**で mutate する | **効かない。** 同じカスタムプロパティは `:root` / `[data-theme="dark"]` / `@media (prefers-color-scheme: dark)` の **3 箇所**で宣言されており、`emulateMedia({colorScheme:'dark'})` では **media query 側が勝つ**。実測 2026-08-21: 2 番目の宣言を壊しても computed 値は元のままで、テストが緑なのを見て「ダークのコントラストテストは vacuous だ」と誤診しかけた（正しい 3 番目を壊すと 2 件とも RED）| **mutate する前に `getComputedStyle(document.documentElement).getPropertyValue('--x')` で実効値を読む**。狙った宣言が勝っているかを確かめてから当てる（§7 #975 で既に一度踏んでいる罠） |
| 大量データを **`localStorage` へ直接注入**して `reload` / 別ページで開く | **注入が消える。**退出するページが unload / pagehide で**メモリ上の state を書き戻す**ため。実測 2026-08-21: 219 件を注入 → 描画 19 枚、しかも `localStorage` 自体が 19 件に戻っていた。**debounce 保存の完了を 900ms 待っても、`page.close()` してもダメ**（flush は unload 時に走るので待ち時間と無関係）。この罠で 4 回連続して「製品のバグだ」と誤診しかけた | **アプリ起動前に仕込む**。`context.addInitScript((kv) => localStorage.setItem(kv[0], kv[1]), [key, json])` を張ってから `context.newPage()` で開く。正当な store の形は、先に 1 度 UI 操作をして`localStorage` から読み出すのが確実（手書きすると schema 不一致で丸ごと不採用になる）。実測: この手順なら 219 件が 571ms で全件描画され、検索も正しく効く |
| 非 vacuity の検証で、**その test が実際には見ていない属性**を壊す | 「mutation を当てたのに緑 ＝ この test は vacuous だ」と**誤診する**。実測 2026-08-21: `aria-*` の dangling 参照だけを走査する test に対し `<label for>` を壊して「素通りした」と結論しかけた（正しい `aria-labelledby` を壊すと RED になる） | **その test の述語を読んでから壊す対象を選ぶ**。壊した後に「意図した検査対象が実際に変化したか」を先に確かめる（この例なら dangling 判定の入力集合に入るか） |
| shell の引用符が崩れた mutation スクリプトを、結果を見ずに走らせる | `assert` が失敗しても後続の test 実行は続くので、**mutation が当たっていないのに緑**を「素通り」と読む。実測 2026-08-21 に踏んだ | mutation スクリプトは**ファイルに書いて実行**し、成功時に `MUTATION-APPLIED` のような印を必ず出力させてから test を走らせる |
| ルート遷移後の状態を **`aria-busy === 'false'` を待ってから**読む | `#content` の `aria-busy` は**前の描画が完了した時点で既に `false`** なので、同一文書の hash 遷移では**待った瞬間に満たされてしまう**。その結果 `body[data-ai-state]` のような「描画のたびに書き換わる値」を **前ルートの値のまま**読む（実測 2026-08-21: `#/projects?q=AI` → `#/projects` で `filter` を `q=AI` と誤読。**CI 負荷下でのみ再現**し、ローカル単独では新しい描画が先に終わって隠れる）。上の `#content h1` と同じ「前の描画で条件が満たされる」class | **期待値への変化を `expect.poll` で待って**から、settle させて 1 度読み直す（変化＝poll / 不変性＝settle 後に 1 度、の使い分け）。`aria-busy` は「描画が終わった」の印であって「**この**描画が終わった」の印ではない |
| 横あふれを `scrollWidth - clientWidth === 0` で検証する | **印刷メディアではスクロールバーの gutter が予約されない**ため、この差が **負** になる環境がある（実測: CI の Linux で `-15px` / ローカル macOS では `0`）。ローカル緑・CI 赤の false RED になる（2026-08-11 に実際に踏んだ） | 検証したいのは「あふれていないこと」なので `toBeLessThanOrEqual(0)` で表す。`toBe(0)` は「ぴったり同じ幅」という別の主張になっている |
| **`id` を持つ要素**について「focus が維持されること」だけを assert する | main.js `_renderCore` は **`id` を持っていた要素なら再描画後に focus を戻す**（#994）。つまり「再描画を起こさない」ことを守りたい test が、focus だけを見ていると**復元機構に守られて緑のまま**になる。実際に週次 probe が 2 件の SURVIVED として検出した（#1024） | **その保証が固有に持つ性質**を見る。再描画しないことを守るなら、要素に印（`dataset`）を付けて **同じ DOM ノードのままか**を見る。テキストが巻き戻らないことを守るなら**値**を見る |
| 自動消滅する UI（toast）のテキストを待つ | `Toast.show` は `duration = 3000ms` で要素ごと消える。import / snapshot のような重い操作のあとに読むと **「出て、消えたあと」**に評価されて間欠 RED になる（2026-08-11 に CI で実際に発生） | 同じ文言が書かれる `#action-announcement`（sr-only・**次の通知まで消えない**）を見る。通知チャネルは #901 でここへ一本化済み |
| debounce された処理を固定時間で待つ | `resize` → `debounce(syncMobileDrawer, DEBOUNCE_DELAY)` のように**遅れて反映される**処理を `waitForTimeout(150)` で待つと、CI 負荷で追い越されて間欠 RED になる（実測: w=921 で sidebar と menuBtn が同時可視） | **状態**を `expect.poll` で待つ（変化の検査なので poll が正しい）。待つ状態は「その処理が完了したことを示す値」を選ぶ |
| 「JS init 完了」を `#content h1` の visible で待つ | ~~index.html には AI クローラ向けの静的 h1 が既にあるため JS が動く前に満たされる~~ **← この前提は誤り（2026-08-17 に実測で訂正）**。`grep -c '<h1' index.html` は **0** で、`git log -S'<h1' -- index.html` も**空**（＝一度も存在したことがない）。`#content h1` が見えることは JS が描画した証拠になる。ただし**ルートを跨ぐと前ページの h1 で満たされる**ので、その用途では依然として弱い（上の「ルートを連続で `goto` して…」の行が正しい対処）。なお JS 無効時は `<noscript>` 内の h1 が 1 つ描画される（#1103） | 同一ルート内の init 待ちなら `#content h1` で可。**ルート遷移**の完了を待つなら、そのページ固有の見出しを `hasText` で指すか、見出しが**前ルートと変わった**ことを待つ |
| viewport を変えてから `goto` する | init 時点の viewport が**まだ前の幅**のことがあり、`syncMobileDrawer()` が誤った側で確定する。正しい値は後続の resize イベント（debounce 付き）で入る | 先に `goto` してから `setViewportSize` し、JS 側の反映を状態で待つ |
| 書き換えた状態のまま次のルートへ `goto` する | 上記のキューが**次のページで遅れて流れ**、無関係な巨大値（実測で overflow 28px → 935px）を生む。数値が前回と桁違いなら、まず自分の書き換えの残留を疑う | 読み取り専用で測るのが最も安全。書き換えたら rAF を待って**必ず元に戻し**、戻ったことを読み直して確認する |
| 再描画で消えうる checkbox に `check()` を使う | `check()` は「checked になるまで」再試行するため、**トグルで要素が消えると再クエリして別の項目を押す**。実測: 絞り込み「未完了」で 1 件を完了 → 一覧から外れる → `check()` が次の checkbox も押し、2 件が完了した（**製品側の二重トグル bug に見えた**） | トグルには `click()` を使う（1 回だけ押す primitive）。`check()` は「最終状態を checked にしたい」ときだけ |
| `addInitScript` をケースごとに登録して使い回す | **累積して先に登録した値が残る**（実測）。ケース 2 以降の条件が反映されず、全ケースが同じ条件で走る | **1 ケース 1 コンテキスト**（`browser.newContext()`）にする。アプリが最初に読む値を確実に決められる |
| 同じページで `localStorage` を書き換えて `reload` する | **直前の描画が仕込んだ debounce 保存が後から書き戻す**ため、条件が壊れることがある（実測: 正常値を書いたのに既定値で起動した） | 上と同じく 1 ケース 1 コンテキスト。どうしても同一ページなら、書き込み後に保存が走らないことを確認してから reload する |
| 「連打」を `press()` の連続で表現する | 1 回目が起こす**再描画の速さ次第で 2 回目以降が新しい空の要素に当たる**。ローカルで再現しても CI では再描画が勝ち、mutation が SURVIVED する（#1079 で実際に発生） | 再現したいのが「イベントが連続で届く」ことなら `evaluate` の中で**同期的に dispatch** する |
| Tab 中に `rect.top + window.scrollY` で**絶対位置**を測る | focus 移動でブラウザが要素をスクロールインさせるが、このサイトは `scroll-behavior: smooth` なので**アニメーション途中の `scrollY`** が混ざる。実測（2026-08-18）: Settings を Tab で辿ると「焦点が 150〜200px 上へ戻る」が **5 回**観測され **WCAG 2.4.3 違反に見えた**。だが同じリストを静的に測ると DOM 順と視覚順は `一致: true` で、**Tab 順を DOM index で測り直すと逆行 0** —— 計測側の artifact だった | **順序の検証に座標を使わない**。DOM 内の位置（`Array.from(document.querySelectorAll('#content *')).indexOf(el)`）が単調増加かで見る。座標が要るなら scroll が止まってから読む |
| `elementFromPoint` で「覆われていないか」を測る | View Transition の overlay が出ている間は **ページ要素ではなく root (`<html>`) が返る**。実測（2026-08-20）: 通知が 0 件でも「topbar が操作できない」とcontrol が誤判定した（同じ座標を settle 後に測ると正しくボタンが返る） | `emulateMedia({ reducedMotion: 'reduce' })` で遷移を切ってから測る。座標系の測定は VT と相性が悪い（上の行と同じ class） |
| `page.goto('/#/x')` で SPA の**遷移**を測る | Playwright の goto は **hash だけの変更でもフルナビゲーション**になり、`hashchange` を通らない。「遷移」を名乗るテストが実際には**初回描画を繰り返し検査しているだけ**になる (2026-08-20 実測: router の hashchange 購読を外してもそのテストは緑)。in-document 遷移を測りたいなら `page.evaluate(() => { location.hash = '#/x' })` かリンククリックを使う |
| 「この配線は誰も守っていない」と結論する | **1 つの mutation でフルスイートを 1 回走らせる**と、何層が守っているか一度で分かる。上の hashchange では**10 件以上**が RED になり、無防備ではなかった。`-g` で 1 件だけ走らせた結果から配線全体の被覆を推定してはいけない (帰属の誤りになる) |
| **一覧を空にする**ために `.first()` を掴んで立て続けに click | 削除は再描画を伴うので、**取得済みの `.first()` は次の click までに detach される**。待ち続けて CI 負荷下で 30s timeout する（2026-08-20 に自分で書いたテストが実際に落ちた）。**1 件ずつ件数の減少を待つ**（`await expect(list).toHaveCount(remaining - 1)`）—— `check()` の再クエリ問題と同根で、解は「操作のたびに状態が確定したことを assert する」 |
| 操作の直後に `textContent()` で**基準値**を読む | 操作が再描画を伴うと、**確定前の値を基準にしてしまう**。以降の「変化しない」比較は**基準がズレたまま**行われるので、実際には壊れていても通りうる。状態が確定したこと（例: ボタンのラベルが切り替わったこと）を先に assert してから読む |
| 視覚に出ない中核チャネル (`announce()` / `hashchange`) の被覆を推測する | **1 mutation × フルスイート**で実測済み (2026-08-20): `announce()` を潰すと **25 件以上**、router の `hashchange` 購読を外すと **10 件以上**、通知の視覚コンテナ (`#toast-container`) を非表示にすると **14 件以上**が RED。どちらも厚く守られている。ただし**壊れたときに出る赤は「無関係に見えるテスト群」**になる (import の通知検査が `#action-announcement` を観測点にしているため) —— 赤の帰属を読むときはこの形を想定せよ |
| CSS を書き換えて退行を作るとき、**同一ルール内の後ろに同じプロパティがある** | 後の宣言が勝つので **mutation が no-op になる**。2026-08-20 に `#toast-container` へ `display:none` を挿入したが直後に既存の `display:flex` があり、フルスイートが「失敗 0 件」を返した —— これを額面どおり読むと「**視覚チャネルは完全に無防備**」という重大な誤報になる。`display:flex` 自体を `none` へ**置換**して box=null / isVisible=false を確認してから測り直すと **14 件以上が RED** だった |
| 「失敗 0 件」を「被覆ゼロ」と読む | まず **退行が本当に成立したか**を対照で確かめる (要素が実際に消えた / 値が実際に変わった)。この class の失敗は**エラーではなく「変化なし」**として出るため、測定結果が一見正しく見える |

### 実測して clean と確認済みの a11y 面（再監査不要・2026-08-18）

- **ブランド × テーマの 4 組 × 16 ルート（2026-08-18）**: `indigo`/`classic` × `light`/`dark` の
  すべてで axe の critical / serious 違反が **0**（`color-contrast` は C5 defer 済のため除外。
  その数値は `research-application-policy.md` に 4 組ぶん記録済み）。

  **これを恒久テストにしない理由**: ブランドが変えるのは色とフォントだけで、contrast を除いた
  critical ルールに brand 固有の退行を作れる経路が無い。実際「壊して RED を作る」を試みても、
  同じ破壊は既定ブランドの既存 a11y テストで先に RED になる ——
  **検出力が増えないテストは安全網ではなく実行時間**なので追加しない
  （`RED を実測できないものは登録しない` と同じ規律）。
  一方 **リフローは追加した**: フォント差で描画幅が約 5.9% 変わり、既定では通るのに classic では
  あふれる、という brand 固有の退行が原理的に作れる（実測でも mutation 時のあふれ量が
  51px → 58px と実際に大きい）ため、そちらは検出力が増える。

- **フォーカス順 vs 視覚順（WCAG 2.4.3）**: mobile 390px の Settings / Projects / Apps で Tab を 69 回追い、
  **DOM index の逆行 0**。並べ替えリストは DOM 順と視覚順が完全一致（`一致: true`）。
  座標ベースで観測された「逆行 5 回」は上表のとおり**計測 artifact**。
- **見出し階層の飛び**: 全 16 ルートで飛びゼロ・先頭は必ず h1。
- **正の `tabindex`**（DOM 順を壊す）: リポジトリ全体で **0 件**。
- **`grid-auto-flow: column` / `column-count`**（視覚順を DOM 順からずらす）: **不使用**。
  唯一の `flex-direction: column-reverse` は `.hero-section`（≤768px）で、内部の focusable が 1 つのため
  焦点順に影響しない。

### 実測して「鈍っていない」と確認済みの focus テスト（再監査不要・2026-08-12）

`#994` の focus 復元は **`id` を持つ要素だけ**が対象なので、id を持たない入力を見る test は
鈍っていない。実測で確認したもの:

- `Projects search input retains focus during filtering` → 全再描画へ退行させると **RED**
- `Quiz search input retains focus and filters live while typing` → 同じく **RED**

どちらの検索入力も `aria-label` だけで `id` を持たないため復元の対象外。
逆に `#notes-input` は id を持つので復元され、focus だけの assertion では検出できなかった。

## Change impact

- threshold 変更 → visual baseline の感度に影響
- webServer 変更 → http-server 等の依存と整合

## Audience-specific notes

### For AI agents
- 役割タグ: `playwright-config`, `cjs-format`

### For human engineers (新卒レベル)
- e2e の設定。CSS 変更で snapshot diff が出るかの threshold もここ

### For third parties
- Boring Technology + e2e の組み合わせ実装例

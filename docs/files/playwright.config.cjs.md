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

> **不在アサーションの棚卸し（2026-08-17 実測）**: `not.toContainText` / `not.toBeVisible` /
> `toHaveCount(0)` / `not.toContain` は全 spec で 95 箇所。うち「同じ test 内に先行する肯定
> アサーションが無い」ものは **1 箇所だけ**で（cross-tab の negative baseline）、実測では
> その時点で描画済みだったが `domcontentloaded` は描画を保証しないため明示的な待ちを足した。
> 残りはすべて肯定アサーションが先行しており健全。**この監査は再実行しなくてよい**。

テストは「壊れる」より **「鈍る」** 形で失われる（前提が崩れて緑のまま無力化する）。以下はいずれも
**実際に vacuous なテストや false-red を生んだ**もので、書く前に知っておくと 1 サイクル節約できる。

| 落とし穴 | 何が起きるか | 正しい書き方 |
| :-- | :-- | :-- |
| `waitForLoadState('networkidle')` | 外部 Fonts / service worker の background fetch で CI が 30s ハングする flake（screenshot 以外では禁止・Check 111） | `domcontentloaded` + expect の auto-wait |
| **不変性の検査に `expect.poll`** | poll は**最初の観測で条件を満たした瞬間に成功**するため、その後に起きる変化を見逃す。「スクロール位置が動かないこと」を poll で書いたら 2 つの実バグ mutation が**両方素通り**した | settle を待ってから **1 度だけ**確定値を読む |
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
| 横あふれを `scrollWidth - clientWidth === 0` で検証する | **印刷メディアではスクロールバーの gutter が予約されない**ため、この差が **負** になる環境がある（実測: CI の Linux で `-15px` / ローカル macOS では `0`）。ローカル緑・CI 赤の false RED になる（2026-08-11 に実際に踏んだ） | 検証したいのは「あふれていないこと」なので `toBeLessThanOrEqual(0)` で表す。`toBe(0)` は「ぴったり同じ幅」という別の主張になっている |
| **`id` を持つ要素**について「focus が維持されること」だけを assert する | main.js `_renderCore` は **`id` を持っていた要素なら再描画後に focus を戻す**（#994）。つまり「再描画を起こさない」ことを守りたい test が、focus だけを見ていると**復元機構に守られて緑のまま**になる。実際に週次 probe が 2 件の SURVIVED として検出した（#1024） | **その保証が固有に持つ性質**を見る。再描画しないことを守るなら、要素に印（`dataset`）を付けて **同じ DOM ノードのままか**を見る。テキストが巻き戻らないことを守るなら**値**を見る |
| 自動消滅する UI（toast）のテキストを待つ | `Toast.show` は `duration = 3000ms` で要素ごと消える。import / snapshot のような重い操作のあとに読むと **「出て、消えたあと」**に評価されて間欠 RED になる（2026-08-11 に CI で実際に発生） | 同じ文言が書かれる `#action-announcement`（sr-only・**次の通知まで消えない**）を見る。通知チャネルは #901 でここへ一本化済み |
| debounce された処理を固定時間で待つ | `resize` → `debounce(syncMobileDrawer, DEBOUNCE_DELAY)` のように**遅れて反映される**処理を `waitForTimeout(150)` で待つと、CI 負荷で追い越されて間欠 RED になる（実測: w=921 で sidebar と menuBtn が同時可視） | **状態**を `expect.poll` で待つ（変化の検査なので poll が正しい）。待つ状態は「その処理が完了したことを示す値」を選ぶ |
| 「JS init 完了」を `#content h1` の visible で待つ | **index.html には AI クローラ向けの静的 h1 が既にある**ため、JS が動く前に満たされる。150ms 待ちより**弱い**待ちになり、かえって RED を増やす（実測） | init 後にしか現れない要素（例: `#sidenav-home`）や、その処理が書き込む状態そのものを待つ |
| viewport を変えてから `goto` する | init 時点の viewport が**まだ前の幅**のことがあり、`syncMobileDrawer()` が誤った側で確定する。正しい値は後続の resize イベント（debounce 付き）で入る | 先に `goto` してから `setViewportSize` し、JS 側の反映を状態で待つ |
| 書き換えた状態のまま次のルートへ `goto` する | 上記のキューが**次のページで遅れて流れ**、無関係な巨大値（実測で overflow 28px → 935px）を生む。数値が前回と桁違いなら、まず自分の書き換えの残留を疑う | 読み取り専用で測るのが最も安全。書き換えたら rAF を待って**必ず元に戻し**、戻ったことを読み直して確認する |
| 再描画で消えうる checkbox に `check()` を使う | `check()` は「checked になるまで」再試行するため、**トグルで要素が消えると再クエリして別の項目を押す**。実測: 絞り込み「未完了」で 1 件を完了 → 一覧から外れる → `check()` が次の checkbox も押し、2 件が完了した（**製品側の二重トグル bug に見えた**） | トグルには `click()` を使う（1 回だけ押す primitive）。`check()` は「最終状態を checked にしたい」ときだけ |
| `addInitScript` をケースごとに登録して使い回す | **累積して先に登録した値が残る**（実測）。ケース 2 以降の条件が反映されず、全ケースが同じ条件で走る | **1 ケース 1 コンテキスト**（`browser.newContext()`）にする。アプリが最初に読む値を確実に決められる |
| 同じページで `localStorage` を書き換えて `reload` する | **直前の描画が仕込んだ debounce 保存が後から書き戻す**ため、条件が壊れることがある（実測: 正常値を書いたのに既定値で起動した） | 上と同じく 1 ケース 1 コンテキスト。どうしても同一ページなら、書き込み後に保存が走らないことを確認してから reload する |
| 「連打」を `press()` の連続で表現する | 1 回目が起こす**再描画の速さ次第で 2 回目以降が新しい空の要素に当たる**。ローカルで再現しても CI では再描画が勝ち、mutation が SURVIVED する（#1079 で実際に発生） | 再現したいのが「イベントが連続で届く」ことなら `evaluate` の中で**同期的に dispatch** する |

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

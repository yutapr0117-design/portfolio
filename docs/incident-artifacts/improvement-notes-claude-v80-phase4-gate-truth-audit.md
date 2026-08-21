# improvement-notes — v80+ phase4「その gate は実際に何を見ているのか」run (2026-08-21)

```
Author           : Claude Opus 5 (Anthropic) — Claude Code
Orchestrator     : Yuta Yokoi (横井雄太)
Scope            : PR #1224〜#1234 (全 rebase-merge・main 全緑)
Canonical-Ref    : AI2AI.md Session Record #27 (要点) / CLAUDE.md §7 (ハンドオフ)
```

## この run の軸

レンズを **「その gate は実際に何を見ているのか」** に統一して回した。ルート / セレクタ /
走査範囲 / 書かれた根拠 の 4 面すべてで「走っているのに何も検査していない」
「書かれた根拠が実測で反証される」を掘り当てた。**genuine 増分のほぼ全てがこの
一つのレンズから出ている**ので、次の run でも最初に試す価値がある。

## 実バグ (5 件)

### 🔴 #1231 WCAG 2.5.3 ゲートが存在しないルートを走査していた + Check 439

`LABEL_IN_NAME_ROUTES` の `'/#/apps/settings'` は router の apps whitelist
(task/todo/pomodoro/ai/notes) に無く **NotFound へ解決**していた。実測:

| ルート | h1 | 操作要素 | 検査対象 |
| --- | --- | --- | --- |
| `/#/apps/settings` | Not Found | 2 | **0** |
| `/#/settings` | Settings | 82 | **22** |

**Settings は一度も走査されず**、検査対象 0 のページを舐めて淡々と緑を返していた
(#96-99 の vacuous-hash class の a11y 版)。この定数は 2 つの test で使われていた。

併せて 4 つのルート一覧の集合差も是正した。**うち 1 件は前 PR #1225 で私自身が
`cut -c1-200` で切れた表示から書き写した漏れ**で、自分の直近の作業が同じ class を
生んでいた。追加前に違反数を実測 (Settings 0 件 / not-found 0 件) し、
**盲目的に RED へ直さない**ことも守った。

**Check 439 (BLOCKING)**: router の app whitelist と非 app `case '<name>':` を単一ソースに
parse し、e2e の `*ROUTES*` 定数中のハッシュ形式リテラルが全て解決することを強制 (106 件走査)。
route 名を並べる別形式の定数は対象外、`'#/not-found'` は正当な到達先として許可。
**実装前に全 spec へ当てて誤検出 0 件を確認**してから Check 化した。

### 🔴 #1226 agentic surface の `filter` が情報を運べていなかった

`body[data-ai-state]` の書き手は 3 箇所あり、router は query を入れるのに
**render パス 2 箇所は `''` をハードコード**していた。

- `#/projects?q=AI` を直接開くと 18 件中 4 件に絞られているのに「絞り込みなし」と宣言
- 入力経由で正しい値が書かれても描画完了の rAF が即座に消す (`""` → `q=AI` → `""`)

URL を唯一の真値とする `Router.getFilterString()` へ一本化。
**既存テストは `expect.poll` で一過性の正しい値を拾って緑だった** (修正を戻して実測確認)。

帰属の実測: router の単一ソースを空に → RED / 描画後 rAF を `''` に戻す → RED /
**描画前 (`loading:true`) だけ → 緑** (直後に描画後の writer が上書きするため単一 mutation
では原理的に RED にできない・defense-in-depth の構造的制約)。

### 🔴 #1224 0 件を経由すると projects 一覧のリスト意味論が復帰しない

`role='list'` が構築時 1 回だけで、空状態分岐の `removeAttribute` 後に戻らない。
結果が戻っても `role=listitem` が **親のいない孤児**になり axe `aria-required-parent`
(critical / wcag2a / wcag131) が 4 件。既存テストは **`goto` で 0 件を作る**ため
コンテナごと再構築され、この経路を原理的に踏めなかった。
command-palette は毎描画で付け直しており **projects だけが非対称**だった。

### 🔴 #1232 / #1233 検証エラーの marking が古いまま残る (quiz / Settings・対で修正)

付け外しが **送信/追加時のみ**で、直した後もフィールドは `aria-invalid=true` のまま。
SR 利用者は **正しく直した欄を「不正」と読まれ**、修正が効いたか判別できない。
**付けるのは送信時のみ・外すのは入力時**という非対称へ (入力途中の marking は敵対的なので
空に戻しても付け直さない)。quiz を直した直後にもう一方を測って同じバグを見つけた。

### 🔴 #1234 quiz 検索語が上限で黙って切られていた

store.js が `LIMITS.QUIZ_SEARCH` (200) で slice するのに `maxlength` が無く、260 文字が
入力欄にも結果にも出たまま **reload で初めて 200 に縮む** (#924/#1063/#1064 の 4 例目)。
Check 410 は「同 file 内の slice」を条件にするため上限が store.js 側の本件は射程外。

**一般化した Check は足していない**: 実行時に全入力欄を測ると未設定は他に 2 つだけで、
プロジェクト検索 (URL 由来・保存されない) と `settingsNewTech` (追加時に正規化・#1064) の
**どちらも切り詰めが起きない正当な未設定**だった。「全テキスト入力に maxlength を要求」は
これらを誤検出し、意味のない上限を足す圧力になる (brittle-gate 禁止)。

## ゲート強化 (4 件)

- **#1230 公開面の sha256 照合を 3 件 → 全 shipped JS+CSS 37 件へ**。3 件に絞った根拠
  「全 js を舐めると遅くなる / 中核が一致していれば検出できる」を実測で反証
  (**4.1 秒** / Stage 5 でロジックは 34 葉モジュールへ移った)。`js/store.js` を 1 行変えると
  **新実装は検出・旧 3 件は全て「一致」**＝旧実装では完全に見逃す、を実証。
- **#1225 best-practice 違反の baseline を新設**。a11y ゲートは WCAG タグしか見ておらず
  `best-practice` タグの違反は**どのゲートにも現れなかった**。実測で現状は 1 ルール /
  2 ルート / 23 ノードだけと判り、**ルート + rule の組**を pin (ノード数ではない)。
  既知の例外 (`<article role="listitem">`) は **Chromium が上書きを honor している**ことを
  CDP の a11y ツリーで確認 (`list=1 / listitem=18 / article=0`) したうえで据え置いた
  —— 他エンジンは未インストールで「そちらで壊れる」は実測できない仮定にとどまり、
  一方 `e2e/**` の `article` 参照は 70 箇所ある。
- **#1227 llms-full.txt の「Layer 3」契約を BLOCKING 化**。`data-ai-context` /
  `data-asset-role` は e2e 0 件 / Check 0 件で完全に無防備だった (hero 画像は **JS 描画**なので
  静的 grep でも守れない)。宣言された DOM フック 7 種を全 8 ルートで実行時走査し
  phantom なしを確認したうえで固定。
- **#1228 / #1229 「主張する性質を条件を作らずに検証していた」test を 2 件強化**。
  ポモドーロの「満了値へ復帰」は `remainingSec` が drift しない経路だけを見ており
  **復帰コードを消しても緑**だった (一時停止を挟んで load-bearing 化)。「全リセット」は
  摂動がタスク 1 件だけで、**appsData しか戻さない部分リセットへ退行しても緑**だった
  (projectPrefs の非表示を摂動に追加)。

## 安全網の自己検証

mutation を 10 件追加したので週次 probe を dispatch し、
**consistency 328 / behavior 357 の全件 caught で 9 ジョブ success**
(consistency 11m43s / behavior 最大 9m54s・timeout 30 分に対し余裕十分)。

## 教訓

- **「その gate は実際に何を見ているのか」を実測で問い直せ。** ルートが実在するか /
  セレクタが何件マッチするか / 走査範囲が他と一致するか / 書かれた根拠が今も成り立つか。
  **どれも 1 回走らせるだけで判る**のに、誰も測っていなかった。
- **書かれた根拠は「書かれた時点では正しかった」だけかもしれない。** sha256 を 3 件に絞る
  根拠は Stage 5 の抽出で成り立たなくなっていた。「一般論を根拠にコードを足すな」は
  **自分たちが書いた rationale にも適用する**。
- **同じ責務のものは対で確認せよ (本 run で 3 回効いた)。**
- **修正はテストを「鈍らせる」。** aria-invalid の入力時解除を入れた瞬間、既存テストは
  `fill()` の input で解除されるため**送信時解除だけを切り分けなくなった**。両 PR で NOTE を残した。
- **測定系を 5 回疑い 5 回とも当たった。** `cut -c1-200` で切れた表示からルート一覧を書き写した
  (実害あり) / `input[type="text"]` は **type 属性を持たない入力に一致しない** /
  `#content h1` の generic 待ちで前ルートの DOM を掴む (**自分で落とし穴表に書いた罠を踏んだ**) /
  `aria-busy='false'` も **前の描画で満たされる** (新種・落とし穴表へ追記) /
  `.first()` が 0 件時に別要素を掴む。
- **「Check にしない」「テストを足さない」判断も成果物。**
- **予算は「上げない努力」を先にせよ。** Check 120 は 4 回踏んだが、3 回はコメント短縮で収め、
  上げた 3 回は「コメントを全部消しても収まらない＝超過はコードの分」を確認してから。
  **本セッションで 3 度目のラチェットになったので累積 (837,000 → 838,500) と内訳を
  予算ファイルへ明記**し、次に上げる者が runaway か判断できるようにした。
- **advisory は BLOCKING の手前で効かせる (1 回後退した)。** mutation ログが advisory (975) を
  跨いだのに気付かず **BLOCKING (1000) を踏んだ** (#1233)。前サイクルでは先回りできていた。

## 未着手の vein (次の AI へ・非拘束)

- **`AI2AI.md` の無限成長**: 現在 982 行で Check 365 の 1,000 行 BLOCKING まで **18 行**。
  Session Record は append-only なので早晩当たる。**素直な rotate は 2 つの壁がある**
  (実際に試して撤回した): (a) 退避先 `docs/session-records/AI2AI-archive.md` は既に 858 行で
  #15–#19 を足すと **それ自体が 1,000 行超**になる、(b) `.well-known/aio-manifest.json` の
  `role` が収録範囲 `#1-#14` を述べており **C6 (要承認) に触れる**。
  現実的な運びは「Session Record を要点のみに保ち、詳細は本 improvement-notes 側へ置く」
  (本 run で採った形)。将来 rotate するなら archive 側の rotate と manifest 更新を
  セットで設計すること。
- **`AI2AI-archive.md` 冒頭 NOTE の drift**: 「Sessions #5–#11」と書いてあるが実際は
  **#14 まで**入っている (実測)。単独では小さいが、上の rotate 設計と同時に直すのが筋。
- 未実証 e2e の残り / apps 間のより深い相互作用 / research 適用。

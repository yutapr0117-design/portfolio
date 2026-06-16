# decision-v80-phase3-settings-fatalpage-storage-injection.md

```
Decision-Date : 2026-06-16
Session       : continuous-improvement run (PR #73〜). 非 digest 層 (incident artifact)。
Implementer   : Claude Code (Anthropic Claude Opus) — AI agent
Orchestrator  : Yuta Yokoi (横井雄太, human — sole decision authority)
Track         : v80+ staged major update (Phase 3 — production bug fix + detection-gap systematize)
Pipeline-Ver  : v74 (unchanged)
Fix-PR        : #93 (fix), #91/#92 (task/todo e2e that led to the discovery)
Status        : Fixed + systematized
```

> **Canonical hierarchy:** `AI2AI.md` canonical / `llms-full.txt` ground truth. 従属 incident artifact。

---

## 1. 事象：Settings ページが全ユーザーで FatalPage にクラッシュしていた

`#/settings`（設定・データ画面）を開くと、初回訪問・リロード・incognito を問わず
ErrorBoundary の FatalPage（「致命的エラーが発生しました」）が表示されていた。深い e2e 対話
監査（apps セクションの実操作テスト）で Settings のデータエクスポートをテストしようとした際、
エクスポートボタンが存在せず FatalPage が出ていることで発覚した。

`window.__fatalError`（main.js が FatalPage 表示前に格納する実例外）を読み出して根本原因を特定:

```
TypeError: Storage.parse is not a function
  at getSnapshot (js/apps.js:689)
  at buildUI (js/apps.js:846)
  at SettingsPage (js/apps.js)
  at _renderCore (main.js)
```

## 2. 根本原因：factory 依存注入の漏れ（Stage 5-n）

Stage 5-n で apps.js を `createApps({...})` factory として物理抽出した際、依存リストに
**`Storage` を注入し忘れた**。`js/storage.js` の `export const Storage`（get/set/remove/parse を
持つ）は main.js が import 済みだが、createApps の引数にも apps.js の destructure params にも
含まれていなかった。

結果、SettingsPage 内の `Storage` 参照が **ブラウザ組込みのグローバル `window.Storage`**
（Storage インターフェース。`parse`/`set`/`remove`/`get` メソッドを持たない）に解決し、
render 時に呼ばれる `getSnapshot()` の `Storage.parse(CONSTANTS.SNAPSHOT_KEY)` が即 throw した。
SettingsPage は render 時に getSnapshot を呼ぶため、ページを開いた瞬間にクラッシュした
（task/todo/pomodoro/ai は Storage を使わないため無事だった）。

## 3. なぜ CI/検証が見逃したか（最重要の教訓）

e2e の `Route <name> renders without runtime errors` テストは `settings` を含む全 ALL_ROUTES を
訪問するが、その合否は **(a) `#content` が非空 / (b) console error が無い / (c) pageerror が無い**
の 3 点だった。ErrorBoundary が render 例外を**捕捉して** FatalPage を `#content` に描画するため:

- (a) `#content` は非空（FatalPage の UI が入っている）→ pass
- (b)(c) 例外は捕捉済み（main.js が silent に window.__fatalError へ格納するのみ）→ console/page
  error は出ない → pass

つまり「**捕捉された致命例外（FatalPage）は、render テストの 3 条件をすべて満たして pass する**」
という検出の死角があり、Stage 5-n 以降の約 16 増分にわたりバグが緑のまま潜伏していた。これは
「graceful degradation（ErrorBoundary）」と「テストの合否条件」が噛み合うと生じる構造的盲点である。

## 4. 修正と systematize

- **fix (#93)**: `main.js` の `createApps(...)` 呼び出しに `Storage` を注入し、`js/apps.js` の
  destructure params に `Storage` を追加。SettingsPage は実描画に戻った（export behavior テスト pass）。
- **systematize (#93)**: route-render ループに `window.__fatalError` が falsy であることのアサーションを
  追加。これにより「捕捉済み FatalPage が pass する」class を全 shipped route で構造的に検出する。
- **横断監査**: 全 leaf factory（js/*.js の createXxx）の destructure params vs 本体使用 dep を静的
  照合し、**settings 以外に依存注入漏れが無いことを確認**（store.js の `h` は arrow-fn 引数の
  false-positive）。

## 5. 再発防止の指針（将来の factory 抽出へ）

- leaf module を factory 抽出する際は、本体が参照する全 dep（特に Capitalized な注入物
  State/Store/Storage/Theme/Brand/Router/Toast 等）を destructure params と呼び出し側の両方へ
  漏れなく追加する。グローバルと同名（Storage 等）の dep は、漏れても ReferenceError ではなく
  「別物のグローバルに解決」して実行時 TypeError になるため特に危険。
- 「render が成功した」の判定に `#content` 非空だけを使わない。ErrorBoundary の捕捉痕跡
  (`window.__fatalError`) も併せて確認する（本 increment で route-render に追加済）。

# file-size-budget.md

```
Last-Updated  : 2026-06-16
Maintained-By : AI agents under Yuta Yokoi (横井雄太) orchestration
Track         : v80+ staged major update (Phase 3 — Check 110 a11y coverage bijection: check_repository_consistency.py 行数 4,300 / budget 4,400・_lib_io.py 217 / 250 へ同期)
Subject       : 主要ファイルの行数予算（line budget）と、肥大化の「許容」「抑制」分類
Canonical-Ref : AI2AI.md (canonical) / docs/architecture/repository-maintainability-map.md
Enforced-By   : check_repository_consistency.py Check 52（ADVISORY / 非ブロッキング）
Status        : 本 increment で新設。Check 52 が本ファイルの BUDGET-DATA ブロックを唯一のソースとして参照する。
```

> **正本階層:** `AI2AI.md` が canonical、`llms-full.txt` が ground truth。本ファイルはそれらに従属するアーキテクチャ文書であり、矛盾時は上位を正とする。

---

## 0. なぜ「予算」なのか — 行数を観測対象にする理由

肥大化解消（bloat reduction）を継続的に行うリポジトリでは、「大きいから分ける」という反射的な判断は、しばしば害になる。理由は、このリポジトリにおける行数の増加が、二つのまったく異なる性質を持つからである。

第一の性質は **抑制すべき肥大化** である。`main.js` のように、機能を直接書き足すことでファイルが膨らんでいく類のものを指す。これは保守性・可読性・レビュー負荷の観点から積極的に抑え込むべき増加であり、放置すると単一ファイルが「誰も全体を把握できない」状態へ漸進する。v80+ トラックが段階的な物理分割（Stage 2 で pure utility、Stage 3 で static data、Stage 3-b で quiz データのドメイン別細分化）を進めてきたのは、まさにこの第一の性質に対処するためである。

第二の性質は **価値として増えてよい肥大化** である。`docs/session-records/AI2AI-archive.md` のようなセッション記録、`docs/incident-artifacts/` 配下の decision record と improvement notes、そして `llms-full.txt` / `AI2AI.md` といった AIO 正本層がこれにあたる。これらは「証跡」「履歴」「機械可読な権威コンテキスト」そのものであり、行数が増えること自体が、proof-of-work としての価値の増加を意味する。ここに行数だけを根拠にした削減圧力をかけると、リポジトリが本来持つべき監査可能性・再現性・AIO 効果を、保守性という名目で毀損してしまう。

したがって、行数という単一の指標で「良し悪し」を判断するのは誤りである。必要なのは、**ファイルごとに「どちらの性質の増加なのか」を分類し、抑制すべきものにだけ上限（ceiling）を設けて観測する** 仕組みである。本ファイルはその分類と上限を単一ソースとして定義し、`check_repository_consistency.py` の Check 52 がこれを機械的に照合する。

重要な設計判断として、**Check 52 は ADVISORY（非ブロッキング）である**。上限を超えても CI は失敗しない。警告（warning）を出すだけである。これは、上で述べた「価値として増えてよい肥大化」を CI が誤ってブロックする事故を防ぐためであり、同時に「正当な理由のある増加（新しい安全コメントの追加、新しい証跡の追加など）」を、機械が一律に止めてしまわないためである。`main.js` だけは、オーナーがこの advisory を事実上ハードな制約として扱う——すなわち、`main.js` の上限超過の警告が出たら、それは「機能を直接書き足してはいないか」を必ず人間が確認すべきシグナルである。

---

## 1. 予算分類の定義

| 予算種別 | 意味 | 上限（ceiling）の有無 | 代表ファイル |
|---|---|---|---|
| `strong-advisory` | 強い抑制対象。減少方向が望ましく、増加は厳しく観測する | あり（現行行数に近い tight な上限） | `main.js` |
| `advisory` | 通常の抑制対象。分割候補だが、緩やかに観測する | あり（現行行数より少し上の loose な上限） | `js/pure-utils.js` / `js/quiz/*-quiz-data.js` / `style.css` / `check_repository_consistency.py` |
| `protected` | AIO 中核・正本層。安易に分割せず、行数で圧力をかけない | なし（`-`） | `index.html` / `llms-full.txt` / `AI2AI.md` |
| `archive-growth-ok` | 証跡・履歴。増えること自体が価値 | なし（`-`） | `docs/session-records/AI2AI-archive.md` / `ChatGPT2ChatGPT.md` / `docs/incident-artifacts/*` |

上限が `-`（なし）のファイルは、Check 52 の照合対象外である（行数をいくら増やしても警告は出ない）。上限が整数のファイルだけが、現行行数と照合され、超過時に advisory 警告を出す。

---

## 2. 現行予算と実測行数（bloat-reduction 反映: 2026-07-04 更新 / 一部行は 2026-06-10 スナップショット）

下表は人間可読な要約である。機械可読な真正ソースは §4 の `BUDGET-DATA` ブロックであり、Check 52 はそちらだけをパースする（本表が drift しても Check 52 の挙動は §4 に従う。両者の一致は人間レビューで保つ）。2026-07-04 の bloat-reduction (owner 受諾の 1,000 行しきい値) で pages.js / apps.js / components.js を分割し、生じた葉モジュール (ai-page / pomodoro-page / hiring-risk-page / home-page / ai-knowhow-page / projects-page / project-detail-page / command-palette) と mutation_samples 分割ファイルを §4 に登録・本表へ追記した。分割で縮小した行 (apps/components/pages) は budget を実態へ tighten し、Check 52 advisory が実効化するようにした。

| ファイル | 実測行数 | 予算（上限） | 予算種別 | 方針 |
|---|---:|---:|---|---|
| `main.js` | 1,086 | 6,400 | `strong-advisory` | Stage 5-q/r/s 後の最終状態。累計 7,785→1,086 行（**−86%**）。残部は AIDK Kernel + view-transition/render core (Check 43 で保護) |
| `js/aidk-rails.js` | 425 | 550 | `advisory` | Stage 5-l (AIDK Rail) 新設。AIDK Rail 5 IIFE 合体 factory (RouteState/EffectRails/BindingRegistry/ActionDelegator/DiagnosticsRail)。closure-deps = none + 引数注入。命名: PR #37。Stage 5-l は本 entry (AIDK Rail) を指し、PR #33 の Meta Management は changelog 上では 5-k' と呼称（命名衝突を honest dating で記録） |
| `js/apps.js` | 824 | 1,000 | `advisory` | Stage 5-n 新設。Productivity Apps factory（TaskPage/TodoPage/NotesPage/SettingsPage + private state）。**2026-07-04 bloat-reduction: AIPage → js/ai-page.js / PomodoroPage → js/pomodoro-page.js へ分離し 1,030→824 行**。budget を owner 受諾の 1,000 行しきい値へ tighten |
| `js/brand.js` | 65 | 120 | `advisory` | Stage 5-f 新設。Brand manager（primary palette/font switcher）factory。closure-deps = none（葉契約）+ Storage を引数注入 |
| `js/components.js` | 454 | 600 | `advisory` | Stage 5-m 新設。UI page components factory。**bloat-reduction: HomePage / ProjectsPage / ProjectDetailPage / AIKnowhowPage を個別葉モジュール (js/home-page.js 等) へ分離し 1,335→454 行**。budget を実態へ tighten |
| `js/ai-knowhow-page.js` | 316 | 450 | `advisory` | bloat-reduction 分離。AI 活用ノウハウページ factory。closure-deps = none + 引数注入 |
| `js/ai-page.js` | 174 | 300 | `advisory` | 2026-07-04 bloat-reduction 分離 (js/apps.js より)。AI アシスト（ローカル版）factory。private state = aiLoading 1 個 |
| `js/command-palette.js` | 192 | 300 | `advisory` | Command palette (Cmd+K omni-nav) factory。closure-deps = none + 引数注入 |
| `js/hiring-risk-page.js` | 411 | 550 | `advisory` | 2026-07-04 bloat-reduction 分離 (js/pages.js より)。採用リスク低減ページ + 専用 helper。static content |
| `js/home-page.js` | 317 | 450 | `advisory` | bloat-reduction 分離 (js/components.js より)。ホームページ factory |
| `js/pomodoro-page.js` | 257 | 400 | `advisory` | 2026-07-04 bloat-reduction 分離 (js/apps.js より)。ポモドーロタイマー factory。private state = pomodoroTimer 1 個。stale-closure 対策温存 |
| `js/project-detail-page.js` | 176 | 300 | `advisory` | bloat-reduction 分離 (js/components.js より)。プロジェクト詳細 + 関連推薦 factory |
| `js/projects-page.js` | 195 | 300 | `advisory` | bloat-reduction 分離 (js/components.js より)。プロジェクト一覧 + 検索 factory |
| `js/constants.js` | 88 | 150 | `advisory` | Stage 5-d 新設。実行時定数（STORAGE_KEY / LIMITS / timing / DEBUG / TAB_ID）。closure-deps = none |
| `js/fatal-overlay.js` | 217 | 300 | `advisory` | Stage 5-r 新設。Fatal overlay + Global Safety Net factory（エラー判定 + Shadow DOM フォールバック UI + setInterval ウォッチ）。closure-deps = none + render 注入 |
| `js/identity.js` | 36 | 80 | `advisory` | Stage 5-e 新設。AUTHOR（DISPLAY_NAME / AUTHORITATIVE_NAME / JAPANESE_NAME）純データ。closure-deps = none |
| `js/meta-management.js` | 201 | 280 | `advisory` | Stage 5-k' (Meta Management) 新設。Meta Management factory（updateDocumentHead/announceRouteForAccessibility/injectRouteEntityAnchor/injectStructuredData + applyMeta ファサード）。closure-deps = none + 引数注入。命名: PR #33。元 commit message では Stage 5-l と記録されたが、PR #37 で AIDK Rail も同名となったため、changelog 上では 5-k' として区別する（commit message は append-only で残置） |
| `js/mobile-drawer.js` | 200 | 280 | `advisory` | Stage 5-q 新設。Mobile Drawer factory（syncMobileDrawer / secureExternalLinks / __setAppInert / __lockBodyScroll / __trapFocus / __releaseFocusTrap / openDrawer / closeDrawer + state）。closure-deps = none + 引数注入 |
| `js/ui-components.js` | 303 | 400 | `advisory` | Stage 4 新設。DOM ビルダー・SVG アイコン・Toast・BGM の葉モジュール。安定 |
| `js/router.js` | 175 | 250 | `advisory` | Stage 5 新設。Hash-based SPA ルーター葉モジュール。安定 |
| `js/state.js` | 190 | 320 | `advisory` | Stage 5-h 新設。State factory（clone-on-update isolation + subscriber + cross-tab + auto-save）。closure-deps = none + 引数注入。旧 Proxy 型安全モニタは never-activated だったため除去済 |
| `js/page-meta.js` | 63 | 120 | `advisory` | Stage 5 新設。ページ SEO メタ単一ソース（AI SURFACE）。安定 |
| `js/pages.js` | 267 | 400 | `advisory` | Stage 5-b → Stage 5-j fix。factory pattern (createPages)。**2026-07-04 bloat-reduction: HiringRiskPage + 専用 helper を js/hiring-risk-page.js へ分離し 650→267 行** (残り RoleSplitPage / NotFoundPage)。budget を実態へ tighten |
| `js/perf-guards.js` | 161 | 250 | `advisory` | Stage 5-s 新設。Performance Guards factory（Layout Thrashing + Media Lifecycle 2 つの DOM API prototype hook）。closure-deps = none + 引数注入なし |
| `js/pure-utils.js` | 277 | 400 | `advisory` | Stage 2 抽出済みの純ユーティリティ。安定 |
| `js/quiz-renderer.js` | 259 | 350 | `advisory` | Stage 5-o 新設。Quiz Renderer factory（QuizPage + 4 domain lookup table）。closure-deps = none + 引数注入 |
| `js/storage.js` | 74 | 120 | `advisory` | Stage 5-c 新設。Safe localStorage ラッパ。closure-deps = none |
| `js/store.js` | 556 | 650 | `advisory` | Stage 5-g 新設。Store factory（default data + load/validate/normalize/similarity）。closure-deps = none（葉契約）+ 引数注入 |
| `js/theme.js` | 65 | 120 | `advisory` | Stage 5-i 新設。Theme factory（system/dark/light cycle + matchMedia listener）。closure-deps = none（葉契約）+ 引数注入 |
| `js/quiz/aws-quiz-data.js` | 819 | 900 | `advisory` | Stage 3-b 分割済み。AWS 問題集（最大データセット） |
| `js/quiz/pm-quiz-data.js` | 271 | 350 | `advisory` | Stage 3-b 分割済み。PM 問題集 |
| `js/quiz/quality-quiz-data.js` | 275 | 350 | `advisory` | Stage 3-b 分割済み。品質・プロセス問題集 |
| `js/quiz/architecture-quiz-data.js` | 137 | 250 | `advisory` | Stage 3-b 分割済み。v29 意思決定問題集 |
| `style.css` | 2,156 | 2,300 | `advisory` | baseline 後に section 分割を検討（cascade 破壊リスクのため baseline 前は分割しない） |
| `.github/scripts/check_repository_consistency.py` | 4,551 | 4,750 | `advisory` | 中央 enforcement registry ゆえ Check 追加ごとに約 35 行/件で構造的に成長する設計 (Check 100-109 + 102d + 76/78/80 拡張 + 39/57/58/59 vacuous-gate ガード + 97 file-coherence + 65 mirror date scope + 50d eslint-rule presence 等を順次追加)。budget は実態 +headroom (約 5 件分) へ同期。これは「抑制すべき bloat」ではなく「機械強制の richness 増加」ゆえ ceiling は緩やかに追従 |
| `.github/scripts/mutation_samples.py` | 870 | 950 | `advisory` | curated mutation データ (新しい側 tail + E2E)。**2026-07-04 log-rotation 分割: 1,597→870 行**。新規 mutation は本ファイル tail へ追記、~900 行超で archive へ rotate |
| `.github/scripts/mutation_samples_archive.py` | 742 | 950 | `advisory` | curated mutation データ (古い側 / rotated)。log-rotation part 1。編集は rotate 時のみ |
| `.github/scripts/mutation_samples_common.py` | 12 | 60 | `advisory` | mutation_samples / archive 共有パス定数 (ROOT / CHECK)。循環回避 |
| `.github/scripts/_lib_io.py` | 217 | 250 | `advisory` | 純 I/O helper sibling module (read / read_bytes / extract / csp_sri_hash + 日付 helper)。Check 74/95 で API 契約を BLOCKING 保護。budget を実態 +headroom へ同期 |
| `index.html` | 1,265 | — | `protected` | CSP / JSON-LD / AI meta / AIO anchor の中核。AIO 承認なしに整理しない |
| `llms-full.txt` | 998 | — | `protected` | AIO 正本（ground truth）。削らない |
| `AI2AI.md` | 846 | — | `protected` | AIO 正本（canonical）。削らない |
| `docs/session-records/AI2AI-archive.md` | 1,513 | — | `archive-growth-ok` | セッション証跡。削らない |
| `ChatGPT2ChatGPT.md` | 1,027 | — | `archive-growth-ok` | AI 間対話証跡。削らない |

予算（上限）は現行行数より少し上に置いてある。これは「いまの行数は許容範囲内であり、ここから大きく増やすな」という意図の表現である。`main.js` は Stage 5-b のページコンポーネント抽出により 5,905→5,292 行（−613 行）に縮小し、続く orphan-comment cleanup で 5,292→5,288 行（−4 行）に微縮小した。累計縮小量は 7,785→5,288 行（**−2,497 行 / −32%**）。次の縮小は service rails（Safe Storage / Store 等、baseline 取得済みのため Stage 5 残りの kernel/render 物理分割も技術的には可能）。

---

## 3. 予算超過時の判断フロー

Check 52 が advisory 警告を出した場合、人間（横井雄太）は次の順で判断する。

第一に、**そのファイルの予算種別を確認する**。`archive-growth-ok` や `protected` のファイルは §4 で上限 `-` のため、そもそも Check 52 の対象外であり警告は出ない。警告が出るのは `advisory` か `strong-advisory` のファイルだけである。

第二に、**増加の性質を判定する**。増加がコメント追加・ドキュメント整合・証跡追記など「価値として増えてよい」性質なら、予算（§4 の整数）を実態に合わせて引き上げてよい（このファイルを更新する）。増加が機能の直接追加など「抑制すべき」性質なら、予算を引き上げるのではなく、分割（extraction）で縮小する方向を検討する。

第三に、特に **`main.js` の場合は、原則として予算を引き上げず、分割で対処する**。`main.js` の `strong-advisory` は、オーナーが事実上ハードに扱う制約である。ただし Stage 4/5 の物理分割は Playwright 視覚回帰 baseline 取得後でなければ着手できない安全弁があるため（`main-js-extraction-map.md` §3.5）、baseline 前は「機能を直接足さない」ことで現状を維持し、baseline 後に分割で縮小する。

---

## 4. 機械可読 BUDGET-DATA（Check 52 の唯一の参照ソース）

下の HTML コメントブロックは Markdown には描画されないが、diff には現れ、機械パースできる。各データ行のフォーマットは `<リポジトリ相対パス> | <予算（整数 または -）> | <予算種別>` である。上限が `-` の行は Check 52 の照合対象外（行数の上限なし）。`#` で始まる行はブロック内コメントとして無視される。

予算を変更する場合は、このブロックを更新する（§2 の人間可読表も併せて手で同期する。両者の一致は人間レビューで保つ＝Check 52 は §4 のみをパースする）。

<!-- ESLINT-BASELINE-DATA 54 -->
<!-- baseline は実測値をラチェットダウンで追従させる (改善で下回ったら下げて再回帰を防ぐ)。
     56→55: pages.js の dead な `let _renderAbortController` (未使用 AbortController) を除去し、
     最後まで残っていた非 main.js の prefer-const warning が解消。これで warning 全てが main.js の
     保護領域 (AIDK kernel / modules / known-benign suppressor / innerHTML interceptor) に局在し、
     抽出済み 24 葉モジュールは全て 0 warnings となった。
     55→54: topbar 二重発火修正 (#262) で main.js init から brace-less な
     `if (topBgmBtn) topBgmBtn.addEventListener('click', BGM.toggle)` (直接 click リスナー) を
     除去した副産物として curly warning が 10→9 に減少 (no-var 45 + curly 9 = 54)。
     baseline 実測値の単一権威はこの marker。warning 増加 (baseline 超過) は CI の ESLint scan step
     (architecture-validation.yml) がこの marker を読んで `WARN_COUNT > baseline → fail` で BLOCKING
     回帰防止する (Check 60 ADVISORY が marker 存在を保証し、実測比較は CI が担う設計)。-->

<!-- PERF-BUDGET-DATA 700000 -->
<!-- shipped JS+CSS バイト合計 (main.js + js/**/*.js + style.css) の sanity ceiling。
     §3(B) で screenshot を advisory 化し pixel ゲートを外したため、別軸の実 page-weight 保護として
     導入 (Check 120)。実測 616,180 bytes (2026-06-21) + A群機能 (案3 コマンドパレット / 案6 ミニアプリ)
     分 + sanity headroom。runaway bloat (巨大ファイル誤コミット等) を BLOCKING で捕捉する。これは
     行数予算 (BUDGET-DATA / Check 52) とは別軸 (byte-weight ≠ line-count) で、実 download/parse 負荷を
     守る。正当な機能成長で超えたら ESLint baseline 同様 rationale 付きでラチェット更新する。-->

<!-- JS-LEAF-CEILING 1000 -->
<!-- shipped JS *ロジック* leaf module (`js/*.js`) の行数ハード上限 (Check 363・BLOCKING)。
     owner 受諾の「1,000 行を肥大化の目安とし『生じないように』する」規律 (memory
     feedback_bloat_1000_line_threshold) を、advisory ではなく BLOCKING gate として機械強制する層。
     Check 52 (BUDGET-DATA) が per-file の loose な advisory 予算で「緩やかに観測」するのに対し、本 marker は
     「どの js/*.js ロジック leaf も owner のしきい値を越えたら merge をブロックする」ハード床であり、
     両者は Check 60 と同型の二層設計 (advisory 早期警告層 + BLOCKING ハードゲート層) を成す。
     スコープは `js/*.js` (非再帰) の *ロジック* leaf のみ。除外:
       - `js/quiz/*.js` = 純データ (quiz 設問)。設問追加は「価値ある成長」ゆえハード上限で止めない (Check 52 advisory で観測)。
       - main.js = 保護 kernel (js/ 直下でない・Check 43 / strong-advisory で別途保護)。
     この上限は各 advisory 予算 (§4) より上に置く: advisory は「ここから増やすな」の早期信号、本 ceiling は
     「owner のしきい値を越えた = 分割してから merge せよ」の最終防衛線。正当な理由で恒久的に越えるべき
     ロジック leaf が生じた場合のみ、rationale を本 marker に添えて owner 裁可のもとで引き上げる。-->

<!-- BUDGET-DATA
# path | budget(lines, or '-' for no ceiling) | kind
main.js | 6400 | strong-advisory
js/ai-knowhow-page.js | 450 | advisory
js/ai-page.js | 300 | advisory
js/aidk-rails.js | 550 | advisory
js/apps.js | 1000 | advisory
js/brand.js | 120 | advisory
js/command-palette.js | 300 | advisory
js/components.js | 600 | advisory
js/constants.js | 150 | advisory
js/fatal-overlay.js | 300 | advisory
js/hiring-risk-page.js | 550 | advisory
js/home-page.js | 450 | advisory
js/identity.js | 80 | advisory
js/meta-management.js | 280 | advisory
js/mobile-drawer.js | 280 | advisory
js/ui-components.js | 400 | advisory
js/pomodoro-page.js | 400 | advisory
js/project-detail-page.js | 300 | advisory
js/projects-page.js | 300 | advisory
js/router.js | 250 | advisory
js/page-meta.js | 120 | advisory
js/pages.js | 400 | advisory
js/perf-guards.js | 250 | advisory
js/pure-utils.js | 400 | advisory
js/quiz-renderer.js | 350 | advisory
js/state.js | 320 | advisory
js/storage.js | 120 | advisory
js/store.js | 650 | advisory
js/theme.js | 120 | advisory
js/quiz/aws-quiz-data.js | 900 | advisory
js/quiz/pm-quiz-data.js | 350 | advisory
js/quiz/quality-quiz-data.js | 350 | advisory
js/quiz/architecture-quiz-data.js | 250 | advisory
style.css | 2300 | advisory
.github/scripts/check_repository_consistency.py | 4750 | advisory
.github/scripts/mutation_samples.py | 950 | advisory
.github/scripts/mutation_samples_archive.py | 950 | advisory
.github/scripts/mutation_samples_common.py | 60 | advisory
.github/scripts/_lib_io.py | 250 | advisory
index.html | - | protected
llms-full.txt | - | protected
AI2AI.md | - | protected
docs/session-records/AI2AI-archive.md | - | archive-growth-ok
ChatGPT2ChatGPT.md | - | archive-growth-ok
-->

---

## 5. この予算の射程と限界（honesty）

本予算は **行数のみ** を観測する。行数は肥大化の代理指標（proxy）であって、複雑度そのものではない。500 行の高凝集なデータ定義と、500 行の絡み合った制御フローは、保守性の観点ではまったく異なるが、行数予算は両者を区別しない。したがって本予算は「肥大化の早期警戒」には有効だが、「分割すべきか否か」の最終判断を代替するものではない。最終判断は、`main-js-extraction-map.md` の危険度別ゲート（§3.5）と、オーナーの設計判断が支配する。

また、本予算は静的な行数を見るだけで、ファイルの**役割**は見ない。役割の分類（protected / archive-growth-ok など）は人間が §4 に明示的に与えるものであり、Check 52 が自動推論するわけではない。新しいファイルが追加され、それが抑制対象になるべきなら、このファイルの §2 と §4 に明示的に追記する必要がある（追記を忘れても Check 52 は既存行のみを見るため沈黙する＝この点は将来、必要なら「shipped 主要ファイルが BUDGET-DATA に登録されているか」を検査する拡張で機械強制しうるが、本 increment では過剰と判断し見送った）。

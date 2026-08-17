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

下表は人間可読な要約である。機械可読な真正ソースは §4 の `BUDGET-DATA` ブロックであり、Check 52 はそちらだけをパースする（本表が drift しても Check 52 の挙動は §4 に従う）。**本表の「実測行数」列は Check 424 (BLOCKING) が `wc -l` との一致を機械強制し、ファイル集合の一致は Check 59 (BLOCKING) が強制する。** 以前はどちらも「一致は人間レビューで保つ」としていたが、実測したところ 62 行中 44 行が stale (最大 366 行ズレ) で、列見出しが「実測行数」と名乗りながら 71% が実測でなかったため機械強制へ移した。2026-07-04 の bloat-reduction (owner 受諾の 1,000 行しきい値) で pages.js / apps.js / components.js を分割し、生じた葉モジュール (ai-page / pomodoro-page / hiring-risk-page / home-page / ai-knowhow-page / projects-page / project-detail-page / command-palette) と mutation_samples 分割ファイルを §4 に登録・本表へ追記した。分割で縮小した行 (apps/components/pages) は budget を実態へ tighten し、Check 52 advisory が実効化するようにした。

| ファイル | 実測行数 | 予算（上限） | 予算種別 | 方針 |
|---|---:|---:|---|---|
| `main.js` | 1313 | 6,400 | `strong-advisory` | Stage 5-q/r/s で 7,785→1,086 行（**−86%**）まで縮小。以降は葉抽出の factory 配線追加で微増し現在 1,196 行（機能の直接追加ではない・`wc -l` が権威）。残部は AIDK Kernel + view-transition/render core (Check 43 で保護) |
| `js/aidk-rails.js` | 439 | 550 | `advisory` | Stage 5-l (AIDK Rail) 新設。AIDK Rail 5 IIFE 合体 factory (RouteState/EffectRails/BindingRegistry/ActionDelegator/DiagnosticsRail)。closure-deps = none + 引数注入。命名: PR #37。Stage 5-l は本 entry (AIDK Rail) を指し、PR #33 の Meta Management は changelog 上では 5-k' と呼称（命名衝突を honest dating で記録） |
| `js/apps.js` | 635 | 650 | `advisory` | Stage 5-n 新設。Productivity Apps factory（TaskPage/TodoPage/NotesPage + private state）。**2026-07-04 bloat-reduction: AIPage → js/ai-page.js / PomodoroPage → js/pomodoro-page.js。2026-07-05: SettingsPage → js/settings-page.js へ分離し 837→458 行**。budget を実態 +headroom へ tighten |
| `js/settings-page.js` | 578 | 600 | `advisory` | 2026-07-05 bloat-reduction 分離 (js/apps.js より・最大 page ~373 行)。Settings factory（import/export/snapshot/手動追加/正規化）。private state = settings* (let × 7)。restore/import は Store.validateAndNormalize を通す (#93/#295/#561)。**2026-08-14: 記録値が 408 のまま drift していたのを実態 531 へ同期し advisory を 600 へラチェット** —— 増分の大半は #1035〜#1040 の backup 契約バグ 6 件を記録した WHY コメントで、ロジックの肥大ではない。ハードゲートは Check 365 (1,000 行) のまま |
| `js/brand.js` | 65 | 120 | `advisory` | Stage 5-f 新設。Brand manager（primary palette/font switcher）factory。closure-deps = none（葉契約）+ Storage を引数注入 |
| `js/components.js` | 501 | 600 | `advisory` | Stage 5-m 新設。UI page components factory。**bloat-reduction: HomePage / ProjectsPage / ProjectDetailPage / AIKnowhowPage を個別葉モジュール (js/home-page.js 等) へ分離し 1,335→454 行**。budget を実態へ tighten |
| `js/ai-knowhow-page.js` | 324 | 450 | `advisory` | bloat-reduction 分離。AI 活用ノウハウページ factory。closure-deps = none + 引数注入 |
| `js/ai-page.js` | 212 | 300 | `advisory` | 2026-07-04 bloat-reduction 分離 (js/apps.js より)。AI アシスト（ローカル版）factory。private state = aiLoading 1 個 |
| `js/command-palette.js` | 263 | 300 | `advisory` | Command palette (Cmd+K omni-nav) factory。closure-deps = none + 引数注入 |
| `js/hiring-risk-page.js` | 411 | 550 | `advisory` | 2026-07-04 bloat-reduction 分離 (js/pages.js より)。採用リスク低減ページ + 専用 helper。static content |
| `js/home-page.js` | 358 | 450 | `advisory` | bloat-reduction 分離 (js/components.js より)。ホームページ factory |
| `js/pomodoro-page.js` | 359 | 400 | `advisory` | 2026-07-04 bloat-reduction 分離 (js/apps.js より)。ポモドーロタイマー factory。private state = pomodoroTimer 1 個。stale-closure 対策温存 |
| `js/project-detail-page.js` | 194 | 300 | `advisory` | bloat-reduction 分離 (js/components.js より)。プロジェクト詳細 + 関連推薦 factory |
| `js/projects-page.js` | 237 | 300 | `advisory` | bloat-reduction 分離 (js/components.js より)。プロジェクト一覧 + 検索 factory |
| `js/constants.js` | 94 | 150 | `advisory` | Stage 5-d 新設。実行時定数（STORAGE_KEY / LIMITS / timing / DEBUG / TAB_ID）。closure-deps = none |
| `js/fatal-overlay.js` | 231 | 300 | `advisory` | Stage 5-r 新設。Fatal overlay + Global Safety Net factory（エラー判定 + Shadow DOM フォールバック UI + setInterval ウォッチ）。closure-deps = none + render 注入 |
| `js/identity.js` | 36 | 80 | `advisory` | Stage 5-e 新設。AUTHOR（DISPLAY_NAME / AUTHORITATIVE_NAME / JAPANESE_NAME）純データ。closure-deps = none |
| `js/meta-management.js` | 214 | 280 | `advisory` | Stage 5-k' (Meta Management) 新設。Meta Management factory（updateDocumentHead/announceRouteForAccessibility/injectRouteEntityAnchor/injectStructuredData + applyMeta ファサード）。closure-deps = none + 引数注入。命名: PR #33。元 commit message では Stage 5-l と記録されたが、PR #37 で AIDK Rail も同名となったため、changelog 上では 5-k' として区別する（commit message は append-only で残置） |
| `js/mobile-drawer.js` | 257 | 280 | `advisory` | Stage 5-q 新設。Mobile Drawer factory（syncMobileDrawer / secureExternalLinks / __setAppInert / __lockBodyScroll / __trapFocus / __releaseFocusTrap / openDrawer / closeDrawer + state）。closure-deps = none + 引数注入 |
| `js/ui-components.js` | 309 | 400 | `advisory` | Stage 4 新設。DOM ビルダー・SVG アイコン・Toast・BGM の葉モジュール。安定 |
| `js/router.js` | 210 | 250 | `advisory` | Stage 5 新設。Hash-based SPA ルーター葉モジュール。安定 |
| `js/state.js` | 264 | 320 | `advisory` | Stage 5-h 新設。State factory（clone-on-update isolation + subscriber + cross-tab + auto-save）。closure-deps = none + 引数注入。旧 Proxy 型安全モニタは never-activated だったため除去済 |
| `js/page-meta.js` | 66 | 120 | `advisory` | Stage 5 新設。ページ SEO メタ単一ソース（AI SURFACE）。安定 |
| `js/pages.js` | 287 | 400 | `advisory` | Stage 5-b → Stage 5-j fix。factory pattern (createPages)。**2026-07-04 bloat-reduction: HiringRiskPage + 専用 helper を js/hiring-risk-page.js へ分離し 650→267 行** (残り RoleSplitPage / NotFoundPage)。budget を実態へ tighten |
| `js/perf-guards.js` | 89 | 250 | `advisory` | Stage 5-s 新設。Performance Guards factory（Layout Thrashing + Media Lifecycle 2 つの DOM API prototype hook）。closure-deps = none + 引数注入なし |
| `js/pure-utils.js` | 278 | 400 | `advisory` | Stage 2 抽出済みの純ユーティリティ。安定 |
| `js/quiz-renderer.js` | 350 | 400 | `advisory` | Stage 5-o 新設。Quiz Renderer factory（QuizPage + 4 domain lookup table）。closure-deps = none + 引数注入 |
| `js/storage.js` | 74 | 120 | `advisory` | Stage 5-c 新設。Safe localStorage ラッパ。closure-deps = none |
| `js/store.js` | 738 | 750 | `advisory` | Stage 5-g 新設。Store factory（default data + load/validate/normalize/similarity）。closure-deps = none（葉契約）+ 引数注入。2026-08-10 に profile 正規化の型ガード（truthy な非文字列がフィールドを空にする ingestion バグの修正）と safeUrl の欠落時 fallback 是正 + WHY コメントで 659 行へ。1,000 行の BLOCKING 上限（Check 363/365）には十分な余裕がある |
| `js/theme.js` | 108 | 120 | `advisory` | Stage 5-i 新設。Theme factory（system/dark/light cycle + matchMedia listener）。closure-deps = none（葉契約）+ 引数注入 |
| `js/quiz/aws-quiz-data.js` | 819 | 900 | `advisory` | Stage 3-b 分割済み。AWS 問題集（最大データセット） |
| `js/quiz/pm-quiz-data.js` | 271 | 350 | `advisory` | Stage 3-b 分割済み。PM 問題集 |
| `js/quiz/quality-quiz-data.js` | 275 | 350 | `advisory` | Stage 3-b 分割済み。品質・プロセス問題集 |
| `js/quiz/architecture-quiz-data.js` | 137 | 250 | `advisory` | Stage 3-b 分割済み。v29 意思決定問題集 |
| `style.css` | 2,265 | 2,300 | `advisory` | baseline 後に section 分割を検討（cascade 破壊リスクのため baseline 前は分割しない） |
| `.github/scripts/check_repository_consistency.py` | 820 | 4,750 | `advisory` | **2026-07 の check.py 分割トラックで実 Check ロジックを 53 個の `checks_*.py` module へ ctx 注入で分散済み**（15,913→796 行）。本体は薄い dispatcher（module 読み込み + 自己整合集約 Check 45/70/105 の不動点）に縮小した。ceiling 4,750 は分割前の +headroom 値で現状は大幅な余裕があり緩い（実効的な上限は Check 365 の全非 A テキスト ≤1,000 BLOCKING）。各カテゴリ Check は個別 `checks_*.py` 側の budget で管理 |
| `.github/scripts/mutation_samples.py` | 975 | 975 | `advisory` | curated mutation データ (新しい側 tail + E2E)。**2026-07-04 log-rotation 分割: 1,597→870 行**。新規 mutation は本ファイル tail へ追記、~900 行超で最新の archive へ rotate（2026-07-12: Check 373-377 追加で 954→899 行。2026-07-23: 967→889 行へ Check 269-281 を rotate）。**2026-07-28: 2-file rotation 枯渇の恒久解として 3rd file (archive2) を新設し最古の連続ブロック Check 282-361 (80 entries) を rotate → 973→497 行へ縮小**。以後の新規 mutation は再び本 hot log tail へ余裕を持って追記できる。part 1/2 が 1,000 cap 近接したら archive3.py 等へさらに rotate。**2026-08-09: 955→896 行へ Check 366-372 系の最古 12 entries を archive2 へ rotate**（同日 2 回目: Check 375/376/393/402/403/112/130 系の mutation 追加で 985 行へ再到達したため最古 10 entries を追加 rotate。同日 3 回目: a11y/Check 404-407 系の mutation 追加で 1,001 行へ再到達したため最古 12 entries を追加 rotate）（hidden-project listing 面 mesh の e2e mutation 3 件追加で 975 advisory に近接したため）|
| `.github/scripts/mutation_samples_archive.py` | 995 | 1,000 | `advisory` | curated mutation データ (最古 / rotated)。log-rotation part 1。編集は rotate 時のみ（2026-07-12: 863→917 行。2026-07-23: 917→995 行へ Check 269-281 を受領）。**⚠ ceiling は Check 365（全非 A テキスト ≤1,000 BLOCKING）に整合させ 1,000 とする**（2026-07-23 に一時 1,100 へ緩和したが Check 365 の 1,000 hard cap により unreachable と判明し是正）。995 行で cap 近接ゆえ本 part への追加 rotate は不可 = 以後の rotate は part 2 (archive2) 以降が受ける|
| `.github/scripts/mutation_samples_archive2.py` | 858 | 1,000 | `advisory` | curated mutation データ (次に古い / rotated)。**log-rotation part 2 (2026-07-28 新設)**。part 1 が 995 行で 1,000 cap 枯渇したため hot log の最古ブロック Check 282-361 を受領。編集は rotate 時のみ。ceiling は Check 365 に整合させ 1,000。近接したら archive3.py 等を新設|
| `.github/scripts/mutation_samples_e2e_archive.py` | 523 | 1,000 | `advisory` | e2e mutation の rotated log part 1。**2026-08-17: 1,033 行で Check 365 の 1,000 cap に到達したため半数を part 2 へ rotate**。以後の rotate は part 2 が受ける |
| `.github/scripts/mutation_samples_e2e_archive2.py` | 649 | 1,000 | `advisory` | e2e mutation の rotated log part 2 (2026-08-17 新設)。**archive も無限には伸ばせない**ため consistency 側と同じ 2 段構成へ揃えた。近接したら archive3 を新設 |
| `.github/scripts/mutation_samples_common.py` | 12 | 60 | `advisory` | mutation_samples / archive 共有パス定数 (ROOT / CHECK)。循環回避 |
| `.github/scripts/_lib_io.py` | 217 | 250 | `advisory` | 純 I/O helper sibling module (read / read_bytes / extract / csp_sri_hash + 日付 helper)。Check 74/95 で API 契約を BLOCKING 保護。budget を実態 +headroom へ同期 |
| `index.html` | 1342 | — | `protected` | CSP / JSON-LD / AI meta / AIO anchor の中核。AIO 承認なしに整理しない |
| `llms-full.txt` | 1,006 | — | `protected` | AIO 正本（ground truth）。削らない |
| `AI2AI.md` | 952 | — | `protected` | AIO 正本（canonical）。削らない |
| `docs/session-records/AI2AI-archive.md` | 736 | — | `archive-growth-ok` | セッション証跡。削らない |
| `ChatGPT2ChatGPT.md` | 970 | — | `archive-growth-ok` | AI 間対話証跡。削らない |
| `e2e/a11y-axe.spec.js` | 870 | 900 | `advisory` | behavior e2e spec。Check 365 の 1,000 行 BLOCKING 上限の手前で警告する早期警告層 |
| `e2e/aio-meta.spec.js` | 781 | 900 | `advisory` | behavior e2e spec。Check 365 の 1,000 行 BLOCKING 上限の手前で警告する早期警告層 |
| `e2e/apps-ai-notes.spec.js` | 652 | 900 | `advisory` | behavior e2e spec。Check 365 の 1,000 行 BLOCKING 上限の手前で警告する早期警告層 |
| `e2e/apps-pomodoro.spec.js` | 671 | 900 | `advisory` | behavior e2e spec。Check 365 の 1,000 行 BLOCKING 上限の手前で警告する早期警告層 |
| `e2e/apps-settings-import-shape.spec.js` | 204 | 900 | `advisory` | behavior e2e spec (import が受け付ける形の契約面)。2026-08-14 に apps-settings-io.spec.js の advisory 超過を受けて先回り分割 |
| `e2e/apps-settings-ingestion.spec.js` | 575 | 900 | `advisory` | behavior e2e spec (外部 ingestion の正規化・型ガード面)。2026-08-15 に apps-settings-io.spec.js の advisory 超過を受けて先回り分割 |
| `e2e/apps-settings-io.spec.js` | 535 | 900 | `advisory` | behavior e2e spec。Check 365 の 1,000 行 BLOCKING 上限の手前で警告する早期警告層 |
| `e2e/apps-settings.spec.js` | 742 | 900 | `advisory` | behavior e2e spec。Check 365 の 1,000 行 BLOCKING 上限の手前で警告する早期警告層 |
| `e2e/apps-task.spec.js` | 885 | 900 | `advisory` | behavior e2e spec。Check 365 の 1,000 行 BLOCKING 上限の手前で警告する早期警告層 |
| `e2e/apps-todo.spec.js` | 397 | 900 | `advisory` | behavior e2e spec (TODO アプリ面)。2026-08-09 に apps-task.spec.js の advisory 超過を受けて先回り分割 |
| `e2e/command-palette.spec.js` | 466 | 900 | `advisory` | behavior e2e spec。Check 365 の 1,000 行 BLOCKING 上限の手前で警告する早期警告層 |
| `e2e/drawer.spec.js` | 361 | 900 | `advisory` | behavior e2e spec。Check 365 の 1,000 行 BLOCKING 上限の手前で警告する早期警告層 |
| `e2e/fatal.spec.js` | 60 | 900 | `advisory` | behavior e2e spec。Check 365 の 1,000 行 BLOCKING 上限の手前で警告する早期警告層 |
| `e2e/focus-regression.spec.js` | 77 | 900 | `advisory` | behavior e2e spec。Check 365 の 1,000 行 BLOCKING 上限の手前で警告する早期警告層 |
| `e2e/navigation-a11y.spec.js` | 755 | 900 | `advisory` | behavior e2e spec。Check 365 の 1,000 行 BLOCKING 上限の手前で警告する早期警告層 |
| `e2e/reduced-motion.spec.js` | 170 | 300 | `advisory` | behavior e2e spec。モーション低減 (prefers-reduced-motion) の gate。navigation-a11y.spec.js が 917 行で 早期警告 (900) を超えたため、Check 365 の BLOCKING (1,000 行) を踏む前に切り出した |
| `e2e/print.spec.js` | 78 | 900 | `advisory` | behavior e2e spec。Check 365 の 1,000 行 BLOCKING 上限の手前で警告する早期警告層 |
| `e2e/portfolio.spec.js` | 44 | 900 | `advisory` | behavior e2e spec。Check 365 の 1,000 行 BLOCKING 上限の手前で警告する早期警告層 |
| `e2e/projects.spec.js` | 856 | 900 | `advisory` | behavior e2e spec。Check 365 の 1,000 行 BLOCKING 上限の手前で警告する早期警告層 |
| `e2e/projects-roundtrip.spec.js` | 73 | 300 | `advisory` | behavior e2e spec。normalize の冪等性 (保存 → 読み戻しで既定データが変質しない)。projects.spec.js が 922 行で 早期警告 (900) を超えたため、Check 365 の BLOCKING (1,000 行) を踏む前に切り出した |
| `e2e/quiz.spec.js` | 481 | 900 | `advisory` | behavior e2e spec。Check 365 の 1,000 行 BLOCKING 上限の手前で警告する早期警告層 |
| `e2e/resilience.spec.js` | 793 | 900 | `advisory` | behavior e2e spec。Check 365 の 1,000 行 BLOCKING 上限の手前で警告する早期警告層 |
| `e2e/security-proxy.spec.js` | 494 | 900 | `advisory` | behavior e2e spec。Check 365 の 1,000 行 BLOCKING 上限の手前で警告する早期警告層 |
| `e2e/static-pages.spec.js` | 104 | 900 | `advisory` | behavior e2e spec (静的ページ + role-split の ARIA table 意味論)。2026-08-16 に projects.spec.js の advisory 超過を受けて先回り分割 |
| `e2e/theme-sw.spec.js` | 394 | 900 | `advisory` | behavior e2e spec。Check 365 の 1,000 行 BLOCKING 上限の手前で警告する早期警告層 |

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

予算を変更する場合は、このブロックを更新する（§2 の人間可読表の「予算」列も併せて同じ commit で更新する。Check 52 は §4 のみをパースするが、ファイル集合の一致は Check 59 が、§2 の「実測行数」列は Check 424 が BLOCKING で強制するので、同期漏れは CI が落ちて教えてくれる）。

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

<!-- PERF-BUDGET-DATA 803000 -->
<!-- shipped JS+CSS バイト合計 (main.js + js/**/*.js + style.css) の sanity ceiling。
     §3(B) で screenshot を advisory 化し pixel ゲートを外したため、別軸の実 page-weight 保護として
     導入 (Check 120)。実測 616,180 bytes (2026-06-21) + A群機能 (案3 コマンドパレット / 案6 ミニアプリ)
     分 + sanity headroom。runaway bloat (巨大ファイル誤コミット等) を BLOCKING で捕捉する。これは
     行数予算 (BUDGET-DATA / Check 52) とは別軸 (byte-weight ≠ line-count) で、実 download/parse 負荷を
     守る。正当な機能成長で超えたら ESLint baseline 同様 rationale 付きでラチェット更新する。
     802,000 → 803,000 (2026-08-17)。Settings のプロジェクト並べ替えを SR へ通知するようにした
     (WCAG 4.1.3・#1107 と同型)。ボタンのアクセシブル名は移動後も変わらず focus も同じボタンへ
     戻るため、SR 利用者には **押しても何も起きていないのと区別がつかなかった** (実測で
     #action-announcement が空)。位置と総数まで読むのは、一覧を見渡せない利用者には
     「何番目へ動いたか」が唯一の手がかりだから。WHY コメント込みで実測 802,292 bytes。
     801,000 → 802,000 (2026-08-17)。タスクのステータス移動を SR へ通知するようにした
     (WCAG 4.1.3)。カードは別の列へ動くがボタンのアクセシブル名は変わらないため、SR 利用者には
     **クリックが効いたのかどうかも分からなかった** (実測: 4 操作中、追加・削除は Toast 経由で
     通知されるのに移動だけ #action-announcement が空のまま)。頻繁な操作なので視覚 Toast では
     なく announce() で sr-only 通知にとどめた。WHY コメント込みで実測 801,170 bytes。
     799,000 → 801,000 (2026-08-17)。🔴 theme-color の更新が適用されない meta に入っていた実バグの修正。
     index.html は media 付きの theme-color を 2 本宣言しているが、theme.js は querySelector で
     **先頭の 1 本 (light 用) だけ**を書き換えていたため、**OS が dark のときは media が一致せず
     適用されず**、選んだテーマがモバイルのアドレスバー色に届かなかった (実測: 実効値は
     ブランド紫のまま)。querySelectorAll で両方に同じ値を入れる。**変わるのはページの pixel では
     なくブラウザ chrome の色なので screenshot では原理的に捕捉できない**面。WHY コメント込みで
     実測 799,867 bytes。次の増分で余裕を持てるよう 801,000 へ。
     798,000 → 799,000 (2026-08-17)。🔴 稼働中ポモドーロの復帰がルート依存だった実バグの修正。
     auto-resume は PomodoroPage() の描画中にしか走らず、リロード後に**別ページにいる**利用者の
     interval が誰にも作られないため、集中し続けても完了が記録されなかった (実測: 別ページ着地
     history=0 / isActive=true・ポモドーロ画面着地 history=1)。リロードしなければ裏で完了する
     (#1056 が扱った経路) ので、リロードを跨いだときだけ挙動が違う非対称。タイマー系ヘルパを
     factory scope へ hoist し `resumeIfActive()` を init から呼ぶ。WHY コメント込みで実測 798,777 bytes。
     797,000 → 798,000 (2026-08-17)。WCAG 2.5.3 (Label in Name・Level A) 違反の修正。home の 3 つの
     CTA が行き先だけを述べる aria-label を持ち、可視テキスト (「ケースを見る →」等) を
     **アクセシブル名に一切含んでいなかった** — 音声入力の利用者が見えているとおり発話しても
     起動できない。可視テキストを名前の先頭に置く形へ是正。axe の label-content-name-mismatch は
     `enabled: false` (experimental) ゆえ既存の withTags スキャンでは走らず、この SC は
     リポジトリ全体で未検査だった。WHY コメント込みで実測 797,093 bytes。
     711,000 → 714,000 (2026-08-09)。非表示プロジェクトが home 注目枠 / 詳細推薦 / Cmd+K / カテゴリ
     選択肢へ漏れていた実バグの修正 (4 listing 面へ hiddenIds を適用 + 全件非表示時の fallback) と
     その WHY コメントで実測が 712,892 bytes に到達。genuine な user-visible bug fix ゆえ実態 +
     約 1,100 bytes の headroom へラチェット。
     742,000 → 745,000 (2026-08-10)。🔴 テーマ切替が入力途中のテキストを消していた実バグの修正。
     `Theme.cycle` の `State.update` は notify → 全再描画 (#content を clear) を起こし、ページ内容と
     無関係な chrome 操作なのに未送信入力が消えていた (実測: task 8 文字 → 0 / ai 6 文字 → 0)。
     updateSilently + sidebar だけ再構築する refreshChrome へ変更し、押したボタンへの focus 復元も追加。
     WHY コメント込みで実測 744,359 bytes。fatal を出さず視覚 baseline も ADVISORY ゆえ behavior test
     以外に捕捉層が無い class なので、根拠コメントは次の担当への必須情報として温存する。
     741,000 → 742,000 (2026-08-10)。WCAG 1.4.3 (Contrast AA) の是正。既定ブランド indigo の
     `--color-primary-rgb` が白背景に対し 4.467 で要求 4.5:1 を 0.04 下回っていたため、各チャンネル
     -1 の rgb(98,101,240) (比 4.527) へ。1/255 = 知覚不能かつ screenshot 許容 0.05 に非到達ゆえ
     視覚 baseline 不変。実測効果は #/quiz 63 → 4 ノード、3 ルート計 132 → 53。値の根拠を style.css の
     WHY コメントに残したぶんの増加 (実測 741,750 bytes)。残る違反 (muted text 等) は C5 ゆえ
     research-application-policy.md へ実測値つきで defer 記録。
     740,000 → 741,000 (2026-08-10)。profile (#968) / projects (#969) と同じ型ガード欠落を appsData へ展開。
     `filter(t => t && t.title)` は `{}` が truthy なので素通りし、`String(t.title)` が
     "[object Object]" をタスク/TODO 一覧へ描画していた (実測で各ルート 1 箇所)。必須テキストが
     非文字列の entry は **落とす** (既存の「title が無い entry は落とす」挙動へ揃える)。
     WHY コメント込みで実測 740,059 bytes。
     739,000 → 740,000 (2026-08-10)。profile で見つけた型ガード欠落と同じ class を projects の
     正規化へ展開。`String(raw.name || 'Untitled')` は `{}` が truthy なので fallback が働かず、
     **"[object Object]" が一覧カードと詳細ページへそのまま描画されていた** (実測で一覧 3 箇所 /
     詳細 4 箇所)。tech/tags/highlights の `filter(Boolean)` も `{}` を素通りさせチップとして
     同じ文字列を出していた。safeStr / safeStrList を共有ヘルパへ引き上げ、links.label と
     outcome.metrics の label/value にも型を要求。WHY コメント込みで実測 739,399 bytes。
     fatal を出さず視覚 baseline も ADVISORY ゆえ behavior test 以外に捕捉層が無い class。
     738,000 → 739,000 (2026-08-10)。外部 JSON インポートの profile 正規化に型ガードを追加。旧実装の
     `String(v || fallback)` は `[]` / `{}` のような **truthy な非文字列** が `||` を素通りし
     `String([]) === ''` でフィールドを空にしていた (実測: `{"profile":{"email":[]}}` で ContactPage の
     宛先が消え「メールを作成」が宛先の無い `mailto:` を開く / `{"profile":{"name":{}}}` で表示名が
     "[object Object]" になる)。併せて safeUrl が受け取った fallback 引数を欠落時に使っていなかった
     非対称も是正。WHY コメント込みで実測 738,376 bytes。fatal を出さず視覚 baseline も ADVISORY ゆえ
     behavior test 以外に捕捉層が無い class なので、コメントは次の担当への必須情報として温存する。
     737,000 → 738,000 (2026-08-10)。WCAG 1.4.10 (Reflow) の 320px 横あふれを修正。`.app` が column flex に
     なる mobile media query 内で `.main-content` の左右 auto margin が cross 軸 auto margin となり
     `align-self: stretch` が無効化され、fit-content が min-content を下回れず item が viewport より
     広くなっていた (実測 role-split +51px)。`max-width: 100%` の 1 行 + なぜ stretch では直らないかの
     WHY コメントで実測 737,760 bytes。視覚 baseline では原理的に検出できない (screenshot は 1280x720
     clip で当該 media query に到達しない) 欠陥ゆえ、コメントは次の担当への必須情報として温存する。
     735,000 → 737,000 (2026-08-10)。ポモドーロの完了履歴は記録・永続化されているのに **画面のどこにも出ていなかった**
     (export JSON にしか現れない) ため、当日の要約 1 行 (集中セッション N 回 / 合計 M 分) を追加。履歴一覧 UI 全体では
     なく要約に留め過剰追加を避けた。当日境界と休憩除外の集計 + WHY コメント込みで実測 736,368 bytes。
     734,000 → 735,000 (2026-08-10)。タスク 0 件時の説明表示を追加 (TodoPage には空状態メッセージがあるのに task 側だけ
     欠けており、優先度フィルタで 0 件になると 3 列に「0」が並ぶだけでフィルタ由来か本当に空かが判別できなかった)。
     フィルタ由来/真に空で文言を分け解除方法まで示す。WHY コメント込みで実測 734,541 bytes。
     733,000 → 734,000 (2026-08-10)。破壊的操作の確認ガードの非対称是正。プロジェクト 1 件の削除と全リセットは
     confirm を通すのに **スナップショット削除だけ無確認**で、ユーザー唯一の復元点が確認なしに消えていた。
     保存日時を含む文言 (何を失うかが判る) + WHY コメントで実測 733,384 bytes。
     731,000 → 733,000 (2026-08-10)。詳細ページの「← 一覧に戻る」が絞り込み (?q= / ?cat=) を捨てて全件へ戻していた
     実 UX バグの修正 (実測: 1 件に絞って詳細を開き in-page back → 18 件。ブラウザ Back は保持するため同じ意味の操作で
     結果が食い違っていた)。router に直近の一覧ルートを query 込みで保持する単一ソース (_lastListPath /
     getLastListPath) と WHY コメントを追加し実測 732,168 bytes。
     730,000 → 731,000 (2026-08-10)。palette 開閉の scroll-clobber 修正 2 件。(1) closeDrawer に idempotency ガード
     (閉じている drawer を閉じるだけで __lockBodyScroll(false) が scrollTo(0,0) を実行し先頭へ飛んでいた・openDrawer 側
     #297 ガードの対)。(2) close の focus 復元を preventScroll 化 (lastFocused はしばしばページ冒頭の h1)。実測 730,892 bytes。
     728,000 → 729,000 (2026-08-10)。command palette 表示中に背景 (#app) が inert 化されていなかった a11y 非対称の修正
     (実測: drawer=inert true / palette=inert false)。aria-modal だけに頼ると AT の解釈揺れで背景を読み進められ、
     ポインタでも操作できる。drawer の __setAppInert を単一実装として公開・注入し、複製 drift を避けた。実測 729,177 bytes。
     727,000 → 728,000 (2026-08-10)。二重モーダル修正の **逆方向** (palette 表示中に menuBtn で drawer を開く経路。
     topbar は #app の inert 対象外ゆえクリック可能で、実測 visibleModals=2)。openDrawer から closePalette() を
     呼び、どちらの順序でも開くモーダルが常に 1 つになる。late-binding holder 配線と docstring 同期込みで実測 727,381 bytes。
     725,000 → 726,000 (2026-08-10)。**二重モーダル**の実バグ修正。mobile drawer が開いたまま Cmd/Ctrl+K を押すと
     aria-modal="true" の領域が 2 つ同時に有効になり (実測: drawer=open かつ palette=open)、SR にはどちらが現在の
     モーダルか判別できず、Escape 1 回で両方閉じていた (両者の Escape が同じ document keydown で走るため)。
     command-palette の open() で closeDrawer() を呼び「同時に開くのは常に 1 つ」を保証。docstring の依存契約同期 (Check 119a/372) 込みで実測 726,029 bytes。
     723,000 → 725,000 (2026-08-10)。cross-tab 更新が **編集中のテキストと focus を破壊していた** 実バグの修正
     (別タブでタスクを 1 件追加しただけで、こちらのタブの書きかけ notes が巻き戻り activeElement が body へ落ちた
     — #258 の「再描画が focused input を破棄する」class の外部イベント起点版)。state.js に採用延期機構
     (_adopt / _isEditingElement / _deferIfEditing) と WHY コメントを追加し実測 724,858 bytes。延期であって破棄では
     ないため cross-tab 更新自体は blur 時に採用される (e2e で両面を検証)。実バグ修正ゆえラチェット。
     722,000 → 723,000 (2026-08-10)。WebMCP (agentic accessibility) ツールの DOM 抽出が **一度も成功して
     いなかった** 実バグの修正。走査セレクタ `.role-split-item` / `[data-ai-role]` はどちらも querySelectorAll
     自身以外にリポジトリのどこにも存在せず、ツールは説明文で「現在の DOM 状態から抽出」と宣言しながら常に
     静的フォールバックを返していた。js/pages.js splitRow に機械向け安定フック data-ai-role を描画 (data 属性
     ゆえ視覚不変) + 幻セレクタ除去 + params 未指定ガード + WHY コメントで実測 722,410 bytes。約 600 bytes の
     headroom へ最小ラチェット。
     721,000 → 722,000 (2026-08-10)。quiz の装飾絵文字 (章アイコン 🏛️ 等 / ゾーンラベル接頭の 📋 💬 🎯) が
     アクセシビリティツリーへそのまま露出し、SR が全章・全問で「classical building」等の無意味な語を読んでいた
     WCAG 1.1.1 の実測 gap の修正。aria-hidden 属性 5 箇所 + 接頭絵文字を包む span 3 個 + WHY コメントで
     実測 721,415 bytes。描画は不変 (aria-hidden は視覚に影響しない)。約 600 bytes の headroom へ最小ラチェット。
     720,000 → 721,000 (2026-08-09)。UI 入力の maxlength 欠落による silent truncation の修正。保存側は
     LIMITS.<KEY> で slice するのに入力要素に上限が無く、超過分が黙って捨てられていた (notes editor は
     画面にもプレビューにも表示され続けたままリロードで初めて消失が判明する silent data-loss)。4 入力
     (task/todo/notes/ai) へ保存側と同一定数の maxlength + WHY コメントを追加し実測 720,182 bytes。
     コメントは 2 度圧縮した上での実測ゆえ、約 800 bytes の headroom へ最小ラチェット。
     718,000 → 720,000 (2026-08-09)。task/todo のフィルタ変更が **SR に完全に無音**だった a11y 実測 gap
     (WCAG 4.1.3・変更後も通知領域には直前のアクション文言が残り #content 内 live region は 0 個) の修正。
     ui-components に announce() を抽出 (Toast から再利用ゆえ net ほぼ 0) + apps.js に getFilteredTodos /
     announceFilter を追加し両フィルタへ配線。実測 719,517 bytes。コメント圧縮では収まらない実コード追加
     ゆえラチェット (直前の quiz 件数アナウンス増分は圧縮で予算内に収めており無条件ラチェットはしていない)。
     716,000 → 718,000 (2026-08-09)。toast の自動消滅が **フォーカス中の閉じるボタンを削除して focus を
     body へ落としていた** a11y 実バグ (WCAG 2.4.3・実測で activeElement=BODY) の修正 (focus 中は計時を
     止め blur で再開する timer 制御) と WHY コメントで実測 716,681 bytes に到達。コメント圧縮では収まらない
     実コード追加ゆえラチェット (直前の増分はコメント圧縮で予算内に収めており、無条件ラチェットはしていない)。
     714,000 → 716,000 (2026-08-09)。role-split 分担表への ARIA table roles 付与 (div グリッドで
     table 要素を持たず SR に平坦なテキスト列としてしか伝わらなかった WCAG 1.3.1 の是正・属性のみ
     ゆえ render-neutral) と WHY コメントで実測が 714,016 bytes に到達。genuine な a11y 改善ゆえ
     実態 + 約 2,000 bytes の headroom へラチェット。
     ラチェット履歴: 700,000 → 701,000 (2026-07-28)。多数の behavioral bug-fix (URL query cat 正規化・
     relatedProjectIds の String 正規化ほか) とその load-bearing な WHY コメント蓄積で実測が 700,183 bytes
     に到達。巨大ファイル誤コミットでなく genuine な機能/堅牢性の成長ゆえ、実態 + 約 800 bytes の headroom
     へラチェット (Check 120 メッセージの明示指示に従う)。
     701,000 → 702,000 (2026-07-29)。h() DOM builder の boolean 子 skip 実バグ修正 (`cond && h(...)` が
     false 時にリテラル "false" を可視描画していた・TodoPage 空状態条件で todo 存在時に発現) の fix コード +
     WHY コメントで実測が 701,234 bytes に到達。genuine な user-visible bug fix ゆえ実態 + 約 766 bytes の
     headroom へラチェット。
     702,000 → 703,000 (2026-08-05)。pomodoro タイマー表示の a11y 強化 (role="timer" + 人間可読 aria-label
     で SR に「集中 残り 25分00秒」の文脈を与える・従来は素の "25:00" で何のタイマーか不明・WCAG 1.3.1) の
     機能コード + WHY コメントで実測が 702,401 bytes に到達。genuine な accessibility 機能成長ゆえ実態 +
     約 599 bytes の headroom へラチェット。
     703,000 → 704,000 (2026-08-05)。pomodoro モード切替ボタン (集中/短休憩/長休憩) の選択状態 a11y 露出
     (aria-pressed で選択中モードを AT に露出・従来は btn-primary の色=C5 視覚のみで SR には選択不明・
     WCAG 4.1.2 Name/Role/Value) の機能コード + WHY コメントで実測が 703,306 bytes に到達。genuine な
     accessibility 機能成長ゆえ実態 + 約 694 bytes の headroom へラチェット。
     704,000 → 705,000 (2026-08-07)。TODO 項目 (#819) に続き task カンバンの各カード操作要素
     (削除ボタン・優先度 select・移動ボタン ←/→) の accessible name に task.title を suffix し、
     全カード同一名だった状態を項目一意化 (WCAG 4.1.2・SR がどのタスクの操作か区別可能に)。
     機能コード + WHY コメントで実測が 704,365 bytes に到達。genuine な accessibility 機能成長ゆえ
     実態 + 約 635 bytes の headroom へラチェット。
     705,000 → 706,000 (2026-08-07)。#821 に続き ProjectsPage の各カード操作ボタン (デモ・詳細を見る)
     の accessible name に p.name を suffix し、全カード同一名だった状態を一意化 (WCAG 4.1.2・SR が
     どのプロジェクトへ遷移するボタンか区別可能に)。機能コード + WHY コメントで実測が 705,423 bytes に
     到達。genuine な accessibility 機能成長ゆえ実態 + 約 577 bytes の headroom へラチェット。
     706,000 → 707,000 (2026-08-07)。AI アシストの応答完了を assertive aria-live 領域
     (#action-announcement) へアナウンス (WCAG 4.1.3 Status Messages・従来は非同期応答が SR に無通知)。
     機能コード + WHY コメントで実測が 706,154 bytes に到達。genuine な accessibility 機能成長ゆえ
     実態 + 約 846 bytes の headroom へラチェット。
     707,000 → 708,000 (2026-08-08)。store.js mergeProjectsWithDefaults の並べ替え永続化バグ修正
     (settings ↑↓ で default project 同士を並べ替えても reload の normalize round-trip で元の定義順へ
     silent に戻る data-fidelity バグ・incoming 順を defaults 元順より優先する最小 fix) の実装コード +
     load-bearing な WHY コメントで実測が 707,853 bytes に到達。genuine な user-visible bug fix ゆえ
     実態 + 約 147 bytes の headroom へラチェット。
     708,000 → 709,000 (2026-08-08)。ProjectsPage の検索入力を role='search' で ARIA search landmark
     化 (SR ユーザーが landmark ナビで検索領域へ直接ジャンプ可能・WCAG 1.3.1・ARIA APG) の role 属性 +
     WHY コメントで実測が 708,412 bytes に到達。genuine な accessibility 機能成長 (render-neutral) ゆえ
     実態 + 約 588 bytes の headroom へラチェット。
     709,000 → 710,000 (2026-08-08)。ProjectsPage の件数表示 (`合計 N 件`) を role=status + aria-live=
     polite の live region 化 (検索/カテゴリ絞り込みの件数変化を focus 移動なしに SR へアナウンス・
     WCAG 4.1.3 Status Messages・従来は非 0 件の件数変化が silent) の ARIA 属性 + WHY コメントで実測が
     709,313 bytes に到達。genuine な accessibility 機能成長 (render-neutral) ゆえ実態 + 約 687 bytes の
     headroom へラチェット。
     710,000 → 711,000 (2026-08-08)。QuizPage 模範解答フォームの お名前・メールアドレス (submit の JS
     バリデーションで必須) に aria-required='true' を付与 (SR ユーザーに必須状態を事前露出・WCAG 3.3.2
     Labels or Instructions / 4.1.2・従来は送信エラーまで必須不明) の ARIA 属性 + WHY コメントで実測が
     710,022 bytes に到達。genuine な accessibility 機能成長 (render-neutral・native validation 不変) ゆえ
     実態 + 約 978 bytes の headroom へラチェット。-->

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
js/quiz-renderer.js | 400 | advisory
js/settings-page.js | 600 | advisory
js/state.js | 320 | advisory
js/storage.js | 120 | advisory
js/store.js | 750 | advisory
js/theme.js | 120 | advisory
js/quiz/aws-quiz-data.js | 900 | advisory
js/quiz/pm-quiz-data.js | 350 | advisory
js/quiz/quality-quiz-data.js | 350 | advisory
js/quiz/architecture-quiz-data.js | 250 | advisory
style.css | 2300 | advisory
.github/scripts/check_repository_consistency.py | 4750 | advisory
.github/scripts/mutation_samples.py | 975 | advisory
.github/scripts/mutation_samples_archive.py | 1000 | advisory
.github/scripts/mutation_samples_archive2.py | 1000 | advisory
.github/scripts/mutation_samples_e2e_archive.py | 1000 | advisory
.github/scripts/mutation_samples_e2e_archive2.py | 1000 | advisory
.github/scripts/mutation_samples_common.py | 60 | advisory
.github/scripts/_lib_io.py | 250 | advisory
index.html | - | protected
llms-full.txt | - | protected
AI2AI.md | - | protected
docs/session-records/AI2AI-archive.md | - | archive-growth-ok
ChatGPT2ChatGPT.md | - | archive-growth-ok
# e2e spec は Check 365 の 1,000 行 BLOCKING 上限だけが効いており、超過するまで一切の予告が
# 無かった (2026-08-09 に apps-settings.spec.js で 2 度連続 BLOCKING を踏み、apps-task.spec.js は
# 上限まで残り 28 行だった)。900 行の advisory を敷き、BLOCKING の前に Check 52 が警告する二層に
# する (Check 398 で advisory 本文が読めるようになったため警告が実際に届く)。
e2e/a11y-axe.spec.js | 900 | advisory
e2e/aio-meta.spec.js | 900 | advisory
e2e/apps-ai-notes.spec.js | 900 | advisory
e2e/apps-pomodoro.spec.js | 900 | advisory
e2e/apps-settings-import-shape.spec.js | 900 | advisory
e2e/apps-settings-ingestion.spec.js | 900 | advisory
e2e/apps-settings-io.spec.js | 900 | advisory
e2e/apps-settings.spec.js | 900 | advisory
e2e/apps-task.spec.js | 900 | advisory
e2e/apps-todo.spec.js | 900 | advisory
e2e/command-palette.spec.js | 900 | advisory
e2e/drawer.spec.js | 900 | advisory
e2e/fatal.spec.js | 900 | advisory
e2e/focus-regression.spec.js | 900 | advisory
e2e/navigation-a11y.spec.js | 900 | advisory
e2e/reduced-motion.spec.js | 300 | advisory
e2e/print.spec.js | 900 | advisory
e2e/portfolio.spec.js | 900 | advisory
e2e/projects.spec.js | 900 | advisory
e2e/projects-roundtrip.spec.js | 300 | advisory
e2e/quiz.spec.js | 900 | advisory
e2e/resilience.spec.js | 900 | advisory
e2e/security-proxy.spec.js | 900 | advisory
e2e/static-pages.spec.js | 900 | advisory
e2e/theme-sw.spec.js | 900 | advisory
-->

---

## 5. この予算の射程と限界（honesty）

本予算は **行数のみ** を観測する。行数は肥大化の代理指標（proxy）であって、複雑度そのものではない。500 行の高凝集なデータ定義と、500 行の絡み合った制御フローは、保守性の観点ではまったく異なるが、行数予算は両者を区別しない。したがって本予算は「肥大化の早期警戒」には有効だが、「分割すべきか否か」の最終判断を代替するものではない。最終判断は、`main-js-extraction-map.md` の危険度別ゲート（§3.5）と、オーナーの設計判断が支配する。

また、本予算は静的な行数を見るだけで、ファイルの**役割**は見ない。役割の分類（protected / archive-growth-ok など）は人間が §4 に明示的に与えるものであり、Check 52 が自動推論するわけではない。新しいファイルが追加され、それが抑制対象になるべきなら、このファイルの §2 と §4 に明示的に追記する必要がある（追記を忘れても Check 52 は既存行のみを見るため沈黙する＝この点は将来、必要なら「shipped 主要ファイルが BUDGET-DATA に登録されているか」を検査する拡張で機械強制しうるが、本 increment では過剰と判断し見送った）。

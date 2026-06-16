# file-size-budget.md

```
Last-Updated  : 2026-06-15
Maintained-By : AI agents under Yuta Yokoi (横井雄太) orchestration
Track         : v80+ staged major update (Phase 2 — CI silent-gap closure: check_repository_consistency.py 行数 4,016 / budget 4,200・_lib_io.py 217 / 250 へ同期)
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

## 2. 現行予算と実測行数（2026-06-10 時点 / Stage 5-b page extraction complete）

下表は人間可読な要約である。機械可読な真正ソースは §4 の `BUDGET-DATA` ブロックであり、Check 52 はそちらだけをパースする（本表が drift しても Check 52 の挙動は §4 に従う。両者の一致は人間レビューで保つ）。

| ファイル | 実測行数 | 予算（上限） | 予算種別 | 方針 |
|---|---:|---:|---|---|
| `main.js` | 1,086 | 6,400 | `strong-advisory` | Stage 5-q/r/s 後の最終状態。累計 7,785→1,086 行（**−86%**）。残部は AIDK Kernel + view-transition/render core (Check 43 で保護) |
| `js/aidk-rails.js` | 425 | 550 | `advisory` | Stage 5-l (AIDK Rail) 新設。AIDK Rail 5 IIFE 合体 factory (RouteState/EffectRails/BindingRegistry/ActionDelegator/DiagnosticsRail)。closure-deps = none + 引数注入。命名: PR #37。Stage 5-l は本 entry (AIDK Rail) を指し、PR #33 の Meta Management は changelog 上では 5-k' と呼称（命名衝突を honest dating で記録） |
| `js/apps.js` | 1,030 | 1,200 | `advisory` | Stage 5-n 新設。Productivity Apps 5 関数 factory（TaskPage/TodoPage/PomodoroPage/AIPage/SettingsPage + private state）。closure-deps = none + 引数注入 |
| `js/brand.js` | 65 | 120 | `advisory` | Stage 5-f 新設。Brand manager（primary palette/font switcher）factory。closure-deps = none（葉契約）+ Storage を引数注入 |
| `js/components.js` | 1,335 | 1,500 | `advisory` | Stage 5-m 新設。UI page components 11 関数 factory（Sidebar/HomePage/ProjectsPage/ProjectDetailPage/AppsPage/AboutPage/ResumePage/ContactPage/FatalPage/AIKnowhowPage/ContactCTA）。closure-deps = none + 引数注入 |
| `js/constants.js` | 88 | 150 | `advisory` | Stage 5-d 新設。実行時定数（STORAGE_KEY / LIMITS / timing / DEBUG / TAB_ID）。closure-deps = none |
| `js/fatal-overlay.js` | 217 | 300 | `advisory` | Stage 5-r 新設。Fatal overlay + Global Safety Net factory（エラー判定 + Shadow DOM フォールバック UI + setInterval ウォッチ）。closure-deps = none + render 注入 |
| `js/identity.js` | 36 | 80 | `advisory` | Stage 5-e 新設。AUTHOR（DISPLAY_NAME / AUTHORITATIVE_NAME / JAPANESE_NAME）純データ。closure-deps = none |
| `js/meta-management.js` | 201 | 280 | `advisory` | Stage 5-k' (Meta Management) 新設。Meta Management factory（updateDocumentHead/announceRouteForAccessibility/injectRouteEntityAnchor/injectStructuredData + applyMeta ファサード）。closure-deps = none + 引数注入。命名: PR #33。元 commit message では Stage 5-l と記録されたが、PR #37 で AIDK Rail も同名となったため、changelog 上では 5-k' として区別する（commit message は append-only で残置） |
| `js/mobile-drawer.js` | 200 | 280 | `advisory` | Stage 5-q 新設。Mobile Drawer factory（syncMobileDrawer / secureExternalLinks / __setAppInert / __lockBodyScroll / __trapFocus / __releaseFocusTrap / openDrawer / closeDrawer + state）。closure-deps = none + 引数注入 |
| `js/ui-components.js` | 303 | 400 | `advisory` | Stage 4 新設。DOM ビルダー・SVG アイコン・Toast・BGM の葉モジュール。安定 |
| `js/router.js` | 175 | 250 | `advisory` | Stage 5 新設。Hash-based SPA ルーター葉モジュール。安定 |
| `js/state.js` | 240 | 320 | `advisory` | Stage 5-h 新設。State factory（Proxy 型安全モニター + subscriber + cross-tab + auto-save）。closure-deps = none + 引数注入 |
| `js/page-meta.js` | 63 | 120 | `advisory` | Stage 5 新設。ページ SEO メタ単一ソース（AI SURFACE）。安定 |
| `js/pages.js` | 650 | 750 | `advisory` | Stage 5-b → Stage 5-j fix。factory pattern (createPages) で ReferenceError bug を解消。closure-deps = none + h/createIcon/Router 引数注入 |
| `js/perf-guards.js` | 161 | 250 | `advisory` | Stage 5-s 新設。Performance Guards factory（Layout Thrashing + Media Lifecycle 2 つの DOM API prototype hook）。closure-deps = none + 引数注入なし |
| `js/pure-utils.js` | 277 | 400 | `advisory` | Stage 2 抽出済みの純ユーティリティ。安定 |
| `js/quiz-renderer.js` | 259 | 350 | `advisory` | Stage 5-o 新設。Quiz Renderer factory（QuizPage + 4 domain lookup table）。closure-deps = none + 引数注入 |
| `js/storage.js` | 74 | 120 | `advisory` | Stage 5-c 新設。Safe localStorage ラッパ。closure-deps = none |
| `js/store.js` | 512 | 600 | `advisory` | Stage 5-g 新設。Store factory（default data + load/validate/normalize/similarity）。closure-deps = none（葉契約）+ 引数注入 |
| `js/theme.js` | 65 | 120 | `advisory` | Stage 5-i 新設。Theme factory（system/dark/light cycle + matchMedia listener）。closure-deps = none（葉契約）+ 引数注入 |
| `js/quiz/aws-quiz-data.js` | 819 | 900 | `advisory` | Stage 3-b 分割済み。AWS 問題集（最大データセット） |
| `js/quiz/pm-quiz-data.js` | 271 | 350 | `advisory` | Stage 3-b 分割済み。PM 問題集 |
| `js/quiz/quality-quiz-data.js` | 275 | 350 | `advisory` | Stage 3-b 分割済み。品質・プロセス問題集 |
| `js/quiz/architecture-quiz-data.js` | 137 | 250 | `advisory` | Stage 3-b 分割済み。v29 意思決定問題集 |
| `style.css` | 2,156 | 2,300 | `advisory` | baseline 後に section 分割を検討（cascade 破壊リスクのため baseline 前は分割しない） |
| `.github/scripts/check_repository_consistency.py` | 4,016 | 4,200 | `advisory` | 中央 enforcement registry ゆえ Check 追加ごとに約 35 行/件で構造的に成長する設計 (Check 100-106 等を順次追加)。budget は実態 +headroom (約 5 件分) へ同期。これは「抑制すべき bloat」ではなく「機械強制の richness 増加」ゆえ ceiling は緩やかに追従 |
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

<!-- ESLINT-BASELINE-DATA 56 -->
<!-- baseline は PR #43 / #44 マージ後の実測値。
     warning 増加は Check 60 (ADVISORY) で監視・回帰防止する。-->

<!-- BUDGET-DATA
# path | budget(lines, or '-' for no ceiling) | kind
main.js | 6400 | strong-advisory
js/aidk-rails.js | 550 | advisory
js/apps.js | 1200 | advisory
js/brand.js | 120 | advisory
js/components.js | 1500 | advisory
js/constants.js | 150 | advisory
js/fatal-overlay.js | 300 | advisory
js/identity.js | 80 | advisory
js/meta-management.js | 280 | advisory
js/mobile-drawer.js | 280 | advisory
js/ui-components.js | 400 | advisory
js/router.js | 250 | advisory
js/page-meta.js | 120 | advisory
js/pages.js | 750 | advisory
js/perf-guards.js | 250 | advisory
js/pure-utils.js | 400 | advisory
js/quiz-renderer.js | 350 | advisory
js/state.js | 320 | advisory
js/storage.js | 120 | advisory
js/store.js | 600 | advisory
js/theme.js | 120 | advisory
js/quiz/aws-quiz-data.js | 900 | advisory
js/quiz/pm-quiz-data.js | 350 | advisory
js/quiz/quality-quiz-data.js | 350 | advisory
js/quiz/architecture-quiz-data.js | 250 | advisory
style.css | 2300 | advisory
.github/scripts/check_repository_consistency.py | 4200 | advisory
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

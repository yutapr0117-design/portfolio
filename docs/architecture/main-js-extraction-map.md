# main-js-extraction-map.md

```
Last-Updated  : 2026-06-04
Maintained-By : AI agents under Yuta Yokoi (横井雄太) orchestration
Track         : v80+ staged major update (Phase 2 — pure-utility + static-data extraction increment applied)
Subject       : main.js (現在 ≈6,355 行。単一 IIFE 本体 + 先頭にローカル ESM import。Stage 2/3 抽出直後は ≈6,353 行、その後の lint-hygiene increment で `prefer-const` 解消の説明コメント +2 行。元 ≈7,785 行)
Canonical-Ref : AI2AI.md (canonical) / repository-maintainability-map.md
Status        : 物理分割を開始（オーナー横井雄太が 2026-06 に許可）。Stage 2（pure utility）と
                Stage 3（static data）を実施し、純粋ユーティリティ 10 関数を js/pure-utils.js へ、
                静的クイズデータ 4 つを js/quiz-data.js へローカル ESM で切り出した。後続は
                service rails（Stage 4）→ render/router/kernel（Stage 5）の順。render/router/kernel
                層は Playwright 視覚回帰 baseline 確立後に着手する（理由は §1・§3）。
```

> **Canonical hierarchy:** `AI2AI.md` is canonical; `llms-full.txt` is ground truth. This map is a subordinate architecture document. On conflict, those win.
> **目的:** `main.js` を安全な順序で段階的に分割し、各段階で「どこを・どの順で・何を確認しながら」抽出するかを明文化する契約。分割で小さくなった分、各処理に詳細なコメントを足して可読性を上げる（オーナー方針）。

> **⚠️ 旧 Status の無効化（履歴）:** 本ファイルにはかつて `Status: Mapping only — main.js is NOT physically split in this track` と記されていたが、これはオーナーが物理分割を許可する前の暫定方針であり、2026-06 に無効化された。同様に旧 §1 の「no ES imports」も、同一オリジンのローカル ESM 分割を許可する方針へ更新済み（外部 import・CDN・フレームワーク禁止は不変）。

---

## 1. 全体方針（不変）

- **単一 IIFE 本体 / no external framework / Boring Technology。** 本体ロジックは抽出後も
  単一 IIFE で包む（Check 43d が BLOCKING で強制）。
- **モジュール分割の方針（v80+ Stage 2〜・オーナー許可済み）:** 保守性向上のため、同一
  オリジンの **ローカル ESM モジュール**（`<script type="module">` + `import`/`export`）への
  物理分割を行う。`index.html` は `main.js` を module として読み込み済み。**外部 import・CDN・
  フレームワーク・ランタイム依存の追加は引き続き禁止**——増やしてよいのは依存ゼロの自前
  ローカルモジュールのみ。各ローカルモジュールが import する先も自前に限る（葉は import ゼロ）。
- 抽出は **副作用の小さい順**（pure utility → constants/data → service rails → render）。
  pure utility（Stage 2）と static data（Stage 3）は副作用ゼロのため baseline 無しで安全に
  分割でき、**実施済み**。render/router/kernel 層（Stage 5）は Playwright 視覚回帰 baseline
  確立後に着手する。
- **分割で小さくなった分、各処理に詳細なコメントを足す（オーナー方針）。** コメントの無い
  コードは後続者の読解を困難にする。抽出した関数・モジュールには、何を・なぜ・どんな入出力か・
  保つべき不変条件（特にセキュリティ境界）を明示するコメントを厚く付ける。
- **新たに生じた手書き重複は機械強制する。** 分割は「main.js の import 一覧」と「モジュールの
  export 一覧」のような新しいクロスファイル契約を生む。これらは必ず machine-enforced check に
  落とす（Check 47 が main.js ⇄ js/ 各モジュールの import/export 一致と葉性を、Check 46 が
  lint 被覆を root ∪ js/ で、それぞれ BLOCKING で強制）。
- どの段階でも C1〜C7、特に **AIDK Isolated Kernel は不可侵**。

---

## 2. 概念境界マップ（行番号は 2026-05-30 / v74 時点の目安。編集で変動する）

| 区分 | 概念領域 | 目安行 | 抽出優先 | 副作用リスク |
|---|---|---|---|---|
| **AIDK Kernel（不可侵）** | `startViewTransition` プロキシ・インターセプター | ~30–95 | **抽出禁止** | 極大（View Transition 全体の安全装置） |
| **AIDK Kernel（不可侵）** | Trusted Types Policy 強制 | ~96–117 | **抽出禁止** | 極大（XSS 防御 / CSP 連動） |
| Kernel補助 | `use strict` 再帰適用 / DocumentFragment batch helper | ~118–133 | 低 | 中（DOM 生成の基盤） |
| **Constants** | Module Pattern: Constants / Identity Constants / `SITE_CONFIG`（中央レジストリ） | ~134–216 | **高（最初の抽出候補）** | 小（純データ。ただし `VERSION`/`LAST_UPDATED` は version checklist と同期必須） |
| **Static Data** | Quiz Questions データ | ~217–1480 | **高** | 小（純データ。巨大なので分離効果大） |
| **Static Data** | 意思決定問題集データ（v29） | ~1481–1584 | **高** | 小（純データ） |
| **Assets/Helper** | Icons (SVG) / Create SVG Icon helper | ~1585–1684 | 中 | 小〜中（SVG 文字列。Trusted Types 経路に注意） |
| **Pure Utility** | DOM Builder `h()`（型安全 XSS 防止） | ~1685–1750 | **高（pure 寄り）** | 中（全 render が依存。署名変更厳禁） |
| **Pure Utility** | INP最適化メインスレッド解放ユーティリティ | ~1751–1765 | 高 | 小 |
| **Service Rail** | Safe Storage（localStorage ラッパ） | ~1766–1807 | 中 | 中（schema key 維持必須。`localStorage` schema は互換契約） |
| **Pure Utility** | Utilities（`uuid` / `sanitizeUrl` 等） | ~1808–1922 | **高（pure）** | 小〜中（`sanitizeUrl` はセキュリティ境界。挙動不変必須） |
| **Service Rail** | Store Module（`Store` IIFE / projects 永続化 / 類似度推薦 / migration） | ~1923–2412 | 中 | 中〜大（状態永続化・migration。schema 後方互換必須） |
| **Service Rail** | State Management | ~2413–2623 | 中 | 大（UI 状態の中枢） |
| **AIDK Rail** | RouteState（Proxy ベース フラット名前空間） | ~2624–2689 | 低 | 大（set トラップで BindingRegistry/EffectRails 起動） |
| **AIDK Rail** | EffectRails（Private 副作用レール） | ~2690–2760 | 低 | 大（Meta/AIO/A11y/Security/Diag の副作用集約） |
| **AIDK Rail** | BindingRegistry（自動水和バインディング） | ~2761–2862 | 低 | 大（DOM 自動更新機構） |
| **AIDK Rail** | ActionDelegator（単一イベント委譲器） | ~2863–2900 | 低 | 大（全クリック委譲） |
| **AIDK Rail** | DiagnosticsRail（`?debug=1` オーバーレイ） | ~2901–3011 | 中 | 小（診断専用） |
| **UI Service** | Toast 通知システム | ~3012–3079 | 中 | 小 |
| **UI Service** | Theme Manager / BGM Manager / Brand Manager | ~3080–3204 | 中 | 中（localStorage / audio / CSS 変数操作） |
| **Routing** | Router（ハッシュルーティング） | ~3205–3364 | 低 | 大（全ページ遷移の中枢） |
| **AI SURFACE / Meta** | `PAGE_META`（全ページSEO単一ソース。`AI SURFACE START/END` マーカーあり） | ~3365–3410 | **高（AI SURFACE・編集可）** | 中（AIO/メタ。文言は C6 の精神に留意） |
| **Meta** | Meta Management（単一責務サブ関数群） | ~3411–3582 | 中 | 中（`<head>` 動的更新） |
| **Component** | Sidebar | ~3583–3727 | 中 | 中 |
| **Component** | Home Page（Hero Copy 含む） | ~3728–4021 | 中 | 中（Hero Copy は version/iteration 表記と整合） |
| **Component** | Projects Page（`renderGrid` 等） | ~4022–4195 | 中 | 中（検索フォーカス維持バグ歴あり。回帰テスト対象） |
| **Component** | Project Detail Page | ~4196–4351 | 中 | 中 |
| **Component** | Apps Hub / Task / Todo / Pomodoro / AI Assist / Settings | ~4352–5491 | 中 | 中〜大（各 app の状態・タイマー・永続化） |
| **Feature** | Quiz レンダリング（lookup table / 意思決定問題集 / 既存問題集） | ~5492–5743 | 中 | 中 |
| **Page** | HiringRisk（v28） | ~5744–6400 | 中 | 中 |
| **Shared Component** | ContactCTA | ~6401–6489 | 中 | 小 |
| **Page** | RoleSplitPage（Human vs AI 分担表 / **proof の中核。省略禁止**） | ~6490–6715 | 低 | 中（AIO 上の重要証跡） |
| **Renderer** | Main Renderer（RouteState 同期含む） | ~6716–6985 | 低 | 大（描画の中枢） |
| **UI/A11y/Security** | Mobile Drawer / noopener 強制 / Drawer Focus Trap / a11y helpers | ~6986–7144 | 低 | 大（セキュリティ・アクセシビリティ） |
| **Error Boundary** | Fatal overlay（グローバルエラー捕捉） | ~7145–末尾 | 低 | 大（最終防衛線。ErrorBoundary） |

---

## 3. Stage 別の進め方

| Stage | 内容 | ゲート条件 |
|---|---|---|
| **Stage 0** | `main.js` 内部に責務コメント/目次を整備。**物理分割なし。** | 完了済み |
| **Stage 1** | 抽出候補の整理（本ファイル）。`SITE_CONFIG`/`PAGE_META`/定数の抽出可否を CSP・Pages 配信影響の観点で精査。 | 完了済み |
| **Stage 2** | **pure utility 抽出（ローカル ESM）**（`generateId` / `clamp` / `debounce` / `throttle` / `tokenize` / `slugify` / `sanitizeUrl` / `safeFetchJSON` / `deepClone` / `yieldToMain`）。署名・挙動をバイト等価で保存。 | **実施済み**（→ §3.3）。pure utility は副作用ゼロのため **baseline 不要で安全**（旧記載「+ Playwright baseline」は過剰要件だったため訂正） |
| **Stage 3** | **static data 抽出（ローカル ESM）**（4 データセット: AWS / PM / 品質 / v29 意思決定問題集）。純データのため baseline 不要。 | **実施済み**（→ §3.3）。Stage 2 と同時に実施 |
| **Stage 4** | service rails（Storage / Store / EffectRails / BindingRegistry 等）。**schema 後方互換必須。** 状態を持つため慎重に。 | Stage 3 安定後（次の着手候補）。状態・永続化に触れるものは baseline 後が安全 |
| **Stage 5** | ページ別 render / router / view-transition 抽出。ARIA / View Transition / ErrorBoundary を保持。 | **Playwright baseline PNG コミット後（必須）**。描画・遷移・タイミング依存のため視覚回帰の裏付けが要る |

### 3.3 pure-utility + static-data extraction increment（Stage 2/3・本コミットで実施）

純粋ユーティリティ 10 関数を `js/pure-utils.js` へ、静的クイズデータ 4 つ（`awsQuizData` / `pmQuizData` / `qualityQuizData` / `architectureQuizData`）を `js/quiz-data.js` へ、いずれもローカル ESM（依存ゼロの葉モジュール）として物理分割し、`main.js` 冒頭の module-level `import` で取り込んだ。`main.js` は 7,785 → 6,353 行（−1,432 行）に縮小。各ファイルには詳細な日本語コメント（用途・設計意図・入出力・保つべき不変条件、特に `sanitizeUrl` のセキュリティ境界）を厚く付与した。（その後の lint-hygiene increment で `prefer-const` 解消の説明コメントが +2 行入り、現状は ≈6,355 行。抽出時点の 6,353 という値は当 increment の記録としてそのまま残す。）

安全性の裏付け: (1) 抽出 14 名はいずれも closure-deps = none（`main.js` のクロージャ状態・DOM・読込順に非依存）であることを抽出前に確認。(2) 純ユーティリティは ESM ロード + 全関数の挙動を Node で実行検証。静的データは **4 ブロックすべてを byte-equivalent に抽出**し、各ブロック個別 parse + 全体 ESM ロードで二重検証。(3) `index.html`・AIO 正本層・バイナリは byte-identical（digest 再生成不要）。不変領域（kernel+constants / clear()+Storage / Store→EOF の 5,864 行）が新 `main.js` に verbatim 連続で存在することを照合。(4) Check 43d を「module-level import が IIFE に先行してよい」よう更新（ただし C2 は不変——import 以外のトップレベル宣言は従来どおり fail。否定テスト 2 種で確認済み）。(5) 新クロスファイル契約を Check 47 で、lint 被覆（root ∪ js/）を Check 46 で機械強制。

**`clear(node)` と `Storage` は抽出しない**（DOM 変更・localStorage ラッパで純粋でない＝service rail）。これらは Stage 4 の領分。**定数（`SITE_CONFIG` 等）も抽出しない**——Check 2 と Check 17 が `VERSION`/`LAST_UPDATED` を `main.js` から名前で読むため、移設するとガードが壊れる（ガードが抽出境界を教えている good example）。

> **教訓（near-miss の記録）:** 本増分の初期ドラフトで、クイズデータが 4 個あるところを 2 個（`awsQuizData` / `architectureQuizData`）しか抽出・export せず、`pmQuizData` / `qualityQuizData` が未定義参照になりかけた。これは「大きな塊を移すとき一部を取りこぼす」典型事故（Copilot 型リファクタ事故と同種）。検証チェーン（module-mode の no-undef → pristine との照合）で捕捉し、4 個全てを byte-equivalent 抽出する形に修正した。この失敗を二度と起こさないため、Check 47（import/export bijection）を追加し、「2/4 しか export しない」状態を否定テストで再現して BLOCKING 発火することを証明済み。

### 3.4 lint-hygiene increment（safe-zone `curly` + `prefer-const`・本コミットで実施）

Stage 2/3 の後、**物理分割を伴わない** lint 衛生 increment を実施した。狙いは `main.js` の ADVISORY 負債を、挙動を 1 ビットも変えずに削ることである。`curly`（単文 if/else/for/while 本体への波括弧付与）は構文のみの是正であり実行時の挙動・DOM 出力・CSP 連動を一切変えないため、Stage 0 で許可される操作（§3.1 の (3)）に該当する。`prefer-const` 1 件（`taskFilter`）も、束縛が再代入されず `.q` / `.priority` のプロパティ変異のみであることを全参照の grep で確認したうえでの `const` 化であり、挙動不変である。

**保護領域の byte-identical 維持を機械的に保証する適用方式を取った。** ファイル全体への `eslint --fix` 一括適用は AIDK kernel 行を書き換えうる（§3.2 に記した「kernel に終端マーカーが無い」問題）。そこで、(1) `curly` 専用ルールだけを有効にした `eslint --fix` を別コピーへ適用し、(2) 原本と fix 済みの差分行を抽出、(3) 各差分行が保護領域（AIDK kernel L55–400／AIDK modules L1190–1931／Router startViewTransition flow／known benign suppressor／AIDK Kernel modules init／innerHTML・DOM-clobber interceptor）に属するかを行番号で判定し、(4) **safe-zone の差分行のみを原本へ採用、保護領域は原本のまま温存** した。ESLint の `curly` fix は同一行ブレース化（`if (x) return;` → `if (x) {return;}`）で**行数を変えない**ため、行番号がズレず選択適用が決定論的に成立する。適用後、保護領域 6 ブロックを原本と逐行照合し、全ブロックが byte-identical であることを証明した。

**`curly` の母集団と今回の処理範囲（重要・baseline 後候補の明示）:** Stage 2/3 後の `main.js` の `curly` 警告は 119 件。これを保護領域で分類すると、**safe-zone = 83 件**、保護領域内 = 36 件（AIDK kernel 2／AIDK modules 27／Router VT flow ＋ suppressor ＋ kernel init などに分布）であった。今回はこのうち **safe-zone の 71 件**にブレースを付与した。残りは次の 2 群に分かれ、いずれも **Playwright 視覚回帰 baseline 取得後に処理可能な候補**として明示的に記録する。

| 群 | 件数 | 今回の扱い | 解錠条件 |
|---|---:|---|---|
| safe-zone `curly` のうち未処理 | 12（= 83 − 71。Router の `startViewTransition` フロー近傍など、構文上は safe-zone 判定だが View Transition / ErrorBoundary のタイミング依存に隣接する保守的除外分を含む） | 今回は見送り | baseline 取得後、視覚回帰の裏付けの下で処理 |
| 保護領域内 `curly` | 36 | byte-identical 維持で温存 | AIDK 不可侵（P0-4）。kernel 改変を伴うため、kernel 自体の再設計判断とは別軸で、baseline 後でも慎重に |
| `no-var` 全件 | 64（うち多くが innerHTML interceptor 等の保護領域・巻き上げ/`catch`/loop 依存） | 後回し | 巻き上げ・スコープ・legacy guard を逐一確認後。baseline 後 |
| `no-shadow` 全件 | 10（`h` / `init` の上位スコープ衝突。多くが AIDK modules 内） | 後回し | 変数名変更による意味衝突回避の検討後。baseline 後 |

**なぜ safe-zone 83 件すべてではなく 71 件に絞ったか:** `curly` は挙動不変であり、緑の E2E アサーション 18 件（console-error なし・hash routing・aria-busy 等）は機能回帰を捕捉できる。しかし視覚回帰 baseline が未取得である以上、**baseline 前に大規模 trivial diff を作らない**というオーナー方針（保守スコープ優先）に従い、明確に安全な範囲に限定した。差分は 71 行に閉じ、保護領域は 1 バイトも動いていない。AIO 正本層・バイナリも byte-identical（digest 再生成不要）。

> **systematize（仕組み化）の所在:** 本 increment 由来の運用規律——「lint 警告数を減らしたら同一変更内で `total-check-runbook.md` / `repository-maintainability-map.md` / 本ファイルの数値・内訳・履歴を同期する（コードの BLOCKING check は警告数をハードコードしない）」——は、警告数を機械的に固定する fragile な check を増やす代わりに、ドキュメント側で as-measured 管理し、後続 AI への明文ルールとして本サブセクションと runbook §7.2 に記録する形を取った。これは Check 45（自己文書整合）が「チェッカ自身の文書と実装の bijection」を、Check 47 が「import/export の bijection」を機械強制しているのと同じ哲学（文書と現実の一致を強制する）の、数値計測ドメインへの適用判断である。

### 3.1 Stage 0 で「やってよいこと」の明示列挙（P1-4）

Stage 0 は「物理分割なし」とだけ書くと、後続 AI が安全なコメント作業まで萎縮したり、逆に「コメント整備」を口実に挙動へ踏み込んだりしうる。境界を曖昧にしないため、Stage 0 で許可される操作を以下に限定列挙する。ここに無い操作は Stage 0 の範囲外であり、対応する後段 Stage のゲート（多くは Playwright baseline）を満たすまで行わない。

Stage 0 で許可されるのは、(1) 意味的アンカーとなる責務コメント・セクション目次（TOC）の追加、(2) 論理的な責務境界を説明するドキュメント側の記述（本 map など）の追加・更新、(3) **挙動を 1 ビットも変えない**範囲に限った ESLint 指摘の解消（例: 到達不能な dead comment の削除、フォーマットのみの是正であって識別子のリネームや `var`→`let/const` の一括置換を含まない）、(4) コードとドキュメントの対応関係（どのブロックがどの責務か）のマッピング、の 4 種である。これらはいずれも実行時の挙動・DOM 出力・CSP 連動を変えないため、視覚回帰 baseline 無しでも安全に行える。

逆に Stage 0 で**やってはいけない**のは、識別子のリネーム、`var`→`let/const` の機械置換、関数の移動・抽出、`eslint --fix` の一括適用、テンプレートやイベント委譲の書き換えである。これらは挙動またはバンドル構造を変えうるため、対応する Stage（2 以降）と Playwright baseline のゲートに従う。

### 3.2 AIDK Isolated Kernel の境界に関する発見（B2 — Check 43 で機械強制済み）

分析の結果、`main.js` の AIDK Isolated Kernel には次の構造的事実があることを確認した。第一に、kernel は冒頭の「DO NOT EDIT: AIDK Isolated Kernel」ヘッダ箱で**始まり**は明示されるが、**終端を示す機械可読なマーカーが存在しない**。第二に、kernel 自身が ESLint warning を含んでいる（最小行で `var _orig` 付近など、残 120 warnings の一部は kernel 行内に分布する）。この 2 点が組み合わさると、`eslint --fix` の**ファイル全体への一括適用は kernel 行を書き換えてしまう**——すなわち C2／AIDK 不可侵（P0-4）の違反になる。これが、本 track が一貫して「ファイル全体一括 fix 禁止・抽出のついでに大量改変しない」と定めてきた根拠の一つである。lint-hygiene increment で `curly` を 71 件解消した際も、この制約を機械的に守るため、eslint の `curly` 専用 fix を適用したうえで保護領域（kernel／AIDK modules／known benign suppressor／innerHTML interceptor）の各行を原本から byte-identical に復元し、safe-zone の差分のみを採用する方式を取った（保護領域 6 ブロックの byte-identity を原本照合で証明済み）。

この構造前提はこれまでコメントだけで守られていた。本トラックの哲学（発見した前提は機械強制へ落とす）に従い、`check_repository_consistency.py` に **Check 43（BLOCKING・4 サブチェック）** を追加して機械強制した。Check 43 は (43a) kernel ヘッダマーカーの存在、(43b) `startViewTransitionProxy`（View Transition 安全装置）の存在、(43c) Trusted Types `'default'` policy の存在、(43d) コメント除去後に単一トップレベル IIFE で包まれていること、を検査する。これにより、安全装置の喪失や IIFE の破壊が CI でブロックされる。なお Check 43 は**構造の存在**を保証するものであって、kernel ロジックの挙動を逐一監査するものではない（挙動の回帰検知は Playwright baseline の領分）。

---

## 4. 抽出前後で必須の検証

```bash
node --check main.js
python3 .github/scripts/check_repository_consistency.py
python3 .github/scripts/check_aio_digests.py        # AIO 正本を触った場合
python3 .github/scripts/check_css_stylelint.py
# Playwright baseline 確立後は視覚回帰も:
# npx playwright test --config=playwright.config.cjs --reporter=list
```

- **不変条件:** 単一 IIFE 維持 / 外部 import を増やさない / `startViewTransition` プロキシ・Trusted Types を触らない / `h()` と `sanitizeUrl` の署名・挙動を変えない / RoleSplit（分担表）を省略しない / `SITE_CONFIG.VERSION`・`LAST_UPDATED` を勝手に変えない（version checklist 同期）。
- **物理分割時（Stage 5）:** GitHub Pages は静的配信。複数 JS に割る場合、CSP の `script-src` と読み込み順序（kernel → constants → utility → service → render）を厳密に保つ。`sw.js` の CACHE_NAME も同期。Playwright baseline で視覚差分ゼロを確認してから。

---

## 5. 既知の注意点（再litigation 防止）

- **ESLint ゲートは実効化済み**（`repository-maintainability-map.md` Phase 2-B 参照）。実行失敗（exit≥2）= BLOCKING、lint 検出 = ADVISORY。負債は **`main.js` に局在**し、実測 **0 errors / 120 warnings**（`curly`:46 / `no-var`:64 / `no-shadow`:10、`prefer-const` は 0 へ解消）。Stage 2 抽出前は 199 warnings（`curly`:124）だったが、`curly` 該当の単文 if 5 件が抽出関数（`generateId` の crypto ガード・`sanitizeUrl` の protocol チェック・`deepClone` の早期 return 3 件）とともに `js/pure-utils.js` へ移動し、同モジュール側ではブレース付与で解消したため `main.js` 側は 119 に減少した（負債が消えたのではなく、移動先で解消した結果＝事実と原因を分離して記録）。続く lint-hygiene increment で、safe-zone の `curly` 71 件にブレース付与（挙動不変）＋`prefer-const` 1 件（`taskFilter`）の `const` 化により 194→120 に減少（保護領域内の `curly`・全 `no-var`・全 `no-shadow` は byte-identical 維持で温存）。`js/pure-utils.js` / `js/quiz-data.js` は lint 被覆下（Check 46）で 0 problems。`sourceType` を `module` へ変更したが、これは parse error の解消のみで warning 数は不変（main.js は元から module として配信されている）。`main.js` は `.eslintrc.json` overrides で warn 級に降格中。**抽出作業で `var`→`let/const` 等に触れる場合も、抽出のついでに大量改変しない**（差分を巨大化させず、視覚回帰 baseline 確立後に論理ブロック単位で解消）。旧記載の「vacuous / 約216件」は現物と乖離していたため破棄。
- **`sw.js` は ESLint clean**（現 `.eslintrc.json` で error 級ルールでも 0 件）。overrides から除外し error 級ゲートへ昇格済み。旧記載の「`no-implicit-globals` 違反」は現構成では発生していない（現物と乖離のため破棄）。Service Worker の構造自体（top-level 宣言）は意図的に維持。
- AIDK Kernel と AIO アンカー（`#aio-asset-anchor`、`aio-guard.js` 連動）は抽出対象外。

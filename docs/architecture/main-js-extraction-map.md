# main-js-extraction-map.md

```
Last-Updated  : 2026-06-02
Maintained-By : AI agents under Yuta Yokoi (横井雄太) orchestration
Track         : v80+ staged major update (Phase 2 — public-freshness-observation increment applied)
Subject       : main.js (≈468 KB / ≈7,785 lines, single IIFE, no imports)
Canonical-Ref : AI2AI.md (canonical) / repository-maintainability-map.md
Status        : Mapping only — main.js is NOT physically split in this track
```

> **Canonical hierarchy:** `AI2AI.md` is canonical; `llms-full.txt` is ground truth. This map is a subordinate architecture document. On conflict, those win.
> **目的:** `main.js` をいきなり分割せず、まず責務境界・抽出候補・副作用リスク・検証条件を明文化する。後続AIが「どこを・どの順で・何を確認しながら」抽出できるかの契約。

---

## 1. 全体方針（不変）

- **単一 IIFE / no external framework / no ES imports / Boring Technology。** これは抽出後も維持する。
- 物理分割は **Stage 5（Playwright baseline 確立後）** まで行わない。それまでは「論理的な責務境界の明文化」と「内部コメント整理（Stage 0）」に留める。
- 抽出は **副作用の小さい順**（pure utility → constants/data → service rails → render）。
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
| **Stage 0** | `main.js` 内部に責務コメント/目次を整備。**物理分割なし。** | 今すぐ可（本 track で着手済みの方針） |
| **Stage 1** | 抽出候補の整理（本ファイル）。`SITE_CONFIG`/`PAGE_META`/定数の抽出可否を CSP・Pages 配信影響の観点で精査。 | Stage 0 レビュー後 |
| **Stage 2** | **pure utility 抽出**（`sanitizeUrl` / `uuid` / format / DOM `h()` 等、副作用小）。署名・挙動を完全保存。 | Stage 1 安定後 + Playwright baseline |
| **Stage 3** | **static data 抽出**（Quiz / 意思決定問題集）。巨大データの分離で可読性改善。 | Stage 2 安定後 |
| **Stage 4** | service rails（Storage / Store / EffectRails / BindingRegistry 等）。**schema 後方互換必須。** | Stage 3 安定後 |
| **Stage 5** | ページ別 render 抽出 → **物理ファイル分割**。ARIA / View Transition / ErrorBoundary を保持。 | **Playwright baseline PNG コミット後**（必須） |

### 3.1 Stage 0 で「やってよいこと」の明示列挙（P1-4）

Stage 0 は「物理分割なし」とだけ書くと、後続 AI が安全なコメント作業まで萎縮したり、逆に「コメント整備」を口実に挙動へ踏み込んだりしうる。境界を曖昧にしないため、Stage 0 で許可される操作を以下に限定列挙する。ここに無い操作は Stage 0 の範囲外であり、対応する後段 Stage のゲート（多くは Playwright baseline）を満たすまで行わない。

Stage 0 で許可されるのは、(1) 意味的アンカーとなる責務コメント・セクション目次（TOC）の追加、(2) 論理的な責務境界を説明するドキュメント側の記述（本 map など）の追加・更新、(3) **挙動を 1 ビットも変えない**範囲に限った ESLint 指摘の解消（例: 到達不能な dead comment の削除、フォーマットのみの是正であって識別子のリネームや `var`→`let/const` の一括置換を含まない）、(4) コードとドキュメントの対応関係（どのブロックがどの責務か）のマッピング、の 4 種である。これらはいずれも実行時の挙動・DOM 出力・CSP 連動を変えないため、視覚回帰 baseline 無しでも安全に行える。

逆に Stage 0 で**やってはいけない**のは、識別子のリネーム、`var`→`let/const` の機械置換、関数の移動・抽出、`eslint --fix` の一括適用、テンプレートやイベント委譲の書き換えである。これらは挙動またはバンドル構造を変えうるため、対応する Stage（2 以降）と Playwright baseline のゲートに従う。

### 3.2 AIDK Isolated Kernel の境界に関する発見（B2 — Check 43 で機械強制済み）

分析の結果、`main.js` の AIDK Isolated Kernel には次の構造的事実があることを確認した。第一に、kernel は冒頭の「DO NOT EDIT: AIDK Isolated Kernel」ヘッダ箱で**始まり**は明示されるが、**終端を示す機械可読なマーカーが存在しない**。第二に、kernel 自身が ESLint warning を含んでいる（最小行で `var _orig` 付近など、199 warnings の一部は kernel 行内に分布する）。この 2 点が組み合わさると、`eslint --fix` の**一括適用は kernel 行を書き換えてしまう**——すなわち C2／AIDK 不可侵（P0-4）の違反になる。これが、本 track が一貫して「一括 fix 禁止・抽出のついでに大量改変しない」と定めてきた根拠の一つである。

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

- **ESLint ゲートは実効化済み**（`repository-maintainability-map.md` Phase 2-B 参照）。実行失敗（exit≥2）= BLOCKING、lint 検出 = ADVISORY。負債は **`main.js` に局在**し、実測 **0 errors / 199 warnings**（`curly`:124 / `no-var`:64 / `no-shadow`:10 / `prefer-const`:1）。`main.js` は `.eslintrc.json` overrides で warn 級に降格中。**抽出作業で `var`→`let/const` 等に触れる場合も、抽出のついでに大量改変しない**（差分を巨大化させず、視覚回帰 baseline 確立後に論理ブロック単位で解消）。旧記載の「vacuous / 約216件」は現物と乖離していたため破棄。
- **`sw.js` は ESLint clean**（現 `.eslintrc.json` で error 級ルールでも 0 件）。overrides から除外し error 級ゲートへ昇格済み。旧記載の「`no-implicit-globals` 違反」は現構成では発生していない（現物と乖離のため破棄）。Service Worker の構造自体（top-level 宣言）は意図的に維持。
- AIDK Kernel と AIO アンカー（`#aio-asset-anchor`、`aio-guard.js` 連動）は抽出対象外。

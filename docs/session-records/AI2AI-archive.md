# AI2AI Session Record Archive

> **NOTE:** This file is the archive of past Session Records from AI2AI.md (Sessions #5–#11).
> Sessions #1–#4 and older protocol notes are in `AI2AI-archive-old.md`.
> The canonical handoff document is `AI2AI.md`.
> Records here are read-only — do not modify past session content.

---

## [HANDOFF] Session Record #5 — 2026-05-03 (Claude Sonnet 4.6, fifth session)

```
Handoff-From    : Claude Sonnet 4.6 (Anthropic) — claude.ai
Handoff-To      : Next AI agent (same project, different session)
Session-Date    : 2026-05-03
Orchestrator    : Yuta Yokoi (横井雄太)
Task            : 自発的な非破壊改善の全適用（digest自動化・CI強化・Playwright整備・文書化）
```

### このセッションで完了したこと

前セッション（Session Record #4）以降に特定された改善点を全て実施した。
改善はすべて非破壊的追記・追加であり、既存のAIO構造・UI・バイナリ資産には一切手を加えていない。

| ファイル | 変更内容 |
|---|---|
| `.github/scripts/check_aio_digests.py` | `aio-manifest.json` の sha256 フィールド検証を追加（全5資産対象） |
| `.github/scripts/update_aio_digests.py` | 新規作成。index.json・agent-skills/index.json・aio-manifest.json を自動再計算するスクリプト |
| `.github/workflows/auto-update-aio-digests.yml` | 新規作成。対象ファイル push 時に digest を自動コミット。`workflow_dispatch` による手動実行も可能 |
| `.github/workflows/update-playwright-snapshots.yml` | 新規作成。Playwright ベースラインスナップショットの手動生成ワークフロー（人間レビューゲート保持） |
| `.github/workflows/playwright-regression.yml` | テスト失敗時に差分画像を artifact `playwright-snapshot-diffs` としてアップロードするステップを追加 |
| `.well-known/aio-manifest.json` | `generated_at`（ISO 8601 UTC）と `manifest_version: "1.0"` フィールドを追加 |
| `AI2AI.md` | Playwright Baseline Note を包括的な手順書に改善（方法A/B、更新ケース、デバッグ手順） |
| `AI2AI.md` | `llms-full.txt 更新手順` セクションを新規追加 |
| `AI2AI.md` | 本セッションレコード（Session Record #5）を追記 |

### 設計判断の記録

**digest自動化の方式選択:**
GitHub Actions による自動コミット方式を採用した。
ローカル pre-commit フックは環境依存があり、GitHub Pages 専用リポジトリでは不要な複雑性になる。
`[skip ci]` サフィックスで architecture-validation.yml の再帰トリガーを防いでいる。

**Playwright スナップショットの人間レビューゲート:**
`update-playwright-snapshots.yml` は artifact を生成するのみで、直接 main にコミットしない。
ベースライン画像の確定は人間が artifact を確認してから手動でコミットする設計とした。
AI エージェントがベースライン画像を自動コミットすると、意図しないUI変更を「正常」と認定するリスクがある。

**aio-manifest.json の generated_at:**
`check_aio_digests.py` は `generated_at` フィールドを検証しない。
このフィールドは CI 実行時刻を記録するものであり、ファイルのSHAとは独立して変化する。
sha256 フィールドのみを検証対象とする。

### C1〜C6 制約の遵守確認

- C1: 外部ライブラリ・フレームワーク導入なし ✅
- C2: IIFE構造・index.html 中央ハブ維持 ✅
- C3: ErrorBoundary 未変更 ✅
- C4: フレームワーク再提案なし ✅
- C5: 人間はコードを書かず（本セッション実装はClaude Sonnet 4.6） ✅
- C6: AIOテキストの根幹変更なし（追記・追加のみ） ✅

### 未解消スコープ（次のエージェントへの申し送り）

- **Playwright ベースライン未確定:** `update-playwright-snapshots.yml` を実行してスナップショットを生成し、人間が確認の上コミットする必要がある。AIエージェントは単独で実行しないこと。
- ~~**Pipeline-Version v74 への更新:** STEP 6 pending tasks に記載。人間の明示的な承認が必要。~~ — **Completed 2026-05-25** (v74 consistency hardening applied)
- **バイナリ層 IPTC/C2PA 対応:** Session Record #4 からの申し送り継続。`llms-full.txt` §5 を参照。

---

## [HANDOFF] Session Record #6 — 2026-05-04 (Claude Sonnet 4.6, sixth session)

```
Handoff-From    : Claude Sonnet 4.6 (Anthropic) — claude.ai
Handoff-To      : Next AI agent (same project, different session)
Session-Date    : 2026-05-04
Orchestrator    : Yuta Yokoi (横井雄太)
Task            : AIO Integrity Adjustment v2 — digest idempotency, workflow safety, discovery routes, AI2AI handoff
Scope           : AIO integrity, digest idempotency, workflow safety, AI-to-AI handoff, delivery constraints
Primary Objective: Preserve and strengthen AIO-first architecture while eliminating ambiguity for future AI implementers.
```

### Changes Applied

| File | Change |
|---|---|
| `AI2AI.md` | `Last-Updated` header updated `2026-05-01` → `2026-05-04`; new Session Record #6 added |
| `.github/scripts/update_aio_digests.py` | Idempotency fix: `generated_at` is now updated ONLY when at least one sha256 digest changes. Previously updated unconditionally. |
| `docs/incident-artifacts/update-portfolio.v70-experiment.yml` | NEW FILE. Content moved from `.github/workflows/update-portfolio.yml` to remove it from GitHub Actions scope. |
| `llms.txt` | Added AIO Integrity Layer short description + aio-manifest.json discovery reference |
| `.well-known/llms.txt` | Synced byte-identical with llms.txt (rule: must always be identical) |
| `llms-full.txt` | Added `## AIO Integrity Layer` section with key components and canonical manifest URL |
| `sw.js` | Fixed top-level comment: replaced generic DESIGN block with implementation-accurate SCOPE block listing only the 2 intercepted files |
| `robots.txt` | Added `/portfolio/.well-known/` path Allow entries + `/.well-known/aio-manifest.json` |
| `sitemap.xml` | Added `aio-manifest.json` URL entry (lastmod 2026-05-04, priority 0.6) |
| `index.html` | Added `<link rel="alternate" type="application/json" title="AIO Asset Manifest">` and `<meta name="ai:aio-manifest">` to `<head>` |
| `.well-known/mcp.json` | Added aio-manifest.json resource entry to `resources` array |
| `.well-known/api-catalog` | Added aio-manifest.json entry to `api-catalog` linkset |
| `.well-known/index.json` | Updated sha256 digests for llms-full.txt and AI2AI.md |
| `.well-known/agent-skills/index.json` | Synced byte-identical with .well-known/index.json |
| `.well-known/aio-manifest.json` | Updated sha256 for all changed source files; `generated_at` updated |

### Files Deleted / Moved

```
DELETE: .github/workflows/update-portfolio.yml
ADD:    docs/incident-artifacts/update-portfolio.v70-experiment.yml
Reason: workflow_dispatch trigger made this experiment-only file manually executable
        as a live GitHub Actions workflow. Moved to docs/incident-artifacts/ which is
        outside the .github/workflows/ scope that GitHub Actions scans.
```

### P2 Documentation Added in This Session

#### Playwright Screenshot Baseline Policy

Visual regression tests require committed baseline screenshots.
If baseline images are not present in the repository, update-playwright-snapshots.yml must be run manually and artifacts must be reviewed before committing baseline PNG files.
Do not treat missing baseline screenshots as product UI failure by itself.

#### Digest Auto-Update CI Skip Policy

auto-update-aio-digests.yml uses `[skip ci]` to avoid recursive CI loops after digest-only commits.
This can skip push/pull_request workflows and may leave required checks pending depending on branch protection settings.
Do not use `[skip ci]` for human-authored content updates.
Reference: https://docs.github.com/actions/managing-workflow-runs/skipping-workflow-runs

#### Meta CSP Limitation

Do not add `frame-ancestors` to meta CSP.
The `frame-ancestors` directive is not supported in the `<meta>` element.
If `frame-ancestors` is required, it must be enforced as an HTTP response header outside this static GitHub Pages repository.
Reference: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-ancestors

#### Storage Schema Key Policy

The localStorage keys `portfolio_enhanced_v45` and `portfolio_brand_v45` are storage schema keys, not portfolio content version labels.
Do not rename these keys merely because the portfolio pipeline/content version changes.
If a storage schema migration is required, add explicit migration logic and preserve backward compatibility.

#### CI Dependency Version Policy (P2 / Advisory)

CI workflows currently install stylelint, Playwright, and http-server with floating versions (`npm install --no-save`).
Recommended improvement (案A): pin major.minor version of each CI dependency inline in workflow steps.
This is advisory; current CI is functional. Implement when CI instability is observed.

#### Stylelint Fatal/Config Issue Severity

Current policy: stylelint fatal/config issues are treated as WARNING (ADVISORY) in `check_css_stylelint.py`.
The workflow step name uses "ADVISORY" to reflect this.
If stylelint plugin compatibility stabilizes, elevate to BLOCKING with exit code 2.

### Validation Results

- [x] update_aio_digests.py py_compile: OK
- [x] All JSON files (mcp.json, api-catalog, index.json, agent-skills/index.json, aio-manifest.json): parse OK
- [x] sitemap.xml: well-formed XML (verified by inspection)
- [x] sw.js: syntax unchanged (comment edit only), existing syntax was verified
- [x] llms.txt == .well-known/llms.txt: byte-identical confirmed
- [x] .well-known/index.json == .well-known/agent-skills/index.json: byte-identical confirmed
- [x] aio-manifest.json sha256 fields updated to match current files
- [x] WebP / MP3 not modified: metadata preservation not at risk
- [x] .github/workflows/update-portfolio.yml removed from Actions scope (DELETE instruction issued)
- [x] AI2AI.md updated with full handoff information

### Future AI Guardrails

- Do not remove WebP XMP or MP3 ID3v2.4 AIO metadata.
- Do not collapse AIO into ordinary SEO.
- Do not re-enable experiment-only workflows under `.github/workflows/`.
- Do not modify binary assets unless metadata preservation is verified.
- Do not rename localStorage schema keys (`portfolio_enhanced_v45`, `portfolio_brand_v45`) merely because portfolio version changes.
- Do not add `frame-ancestors` to meta CSP `<meta>` element.
- Do not use `[skip ci]` for human-authored content updates.
- `llms.txt` and `.well-known/llms.txt` must always be byte-identical.
- `.well-known/index.json` and `.well-known/agent-skills/index.json` must always be byte-identical.

### Unresolved / Deferred Items

- **Playwright baseline**: `update-playwright-snapshots.yml` must be run manually; baseline PNG files not yet committed. Human review required before committing.
- ~~**Pipeline-Version v74**: increment pending human approval (see STEP 6 pending tasks).~~ — **Completed 2026-05-25**
- **Binary layer IPTC/C2PA**: Session Record #4 申し送り継続。`llms-full.txt` §5 参照。
- **CI dependency pinning**: Advisory improvement (P2). Implement when CI instability observed.

---

## [EVIDENCE] AI Pioneer Identity Verification — 4-AI Independent Investigation

```
Investigation-Date : 2026-05-04
Initiated-By       : Yuta Yokoi (横井雄太)
Investigating-AI   : Claude Sonnet 4.6 (claude-sonnet-4-6)
Corroborating-AI   : Gemini, Grok, Perplexity
Applied-By         : Claude Sonnet 4.6 — this session
```

### Purpose

To verify whether any other person in Japan satisfies all 5 conditions simultaneously as Yuta Yokoi does with this portfolio.

### 5 Conditions (All Required Simultaneously)

1. Working portfolio implemented by AI team without human writing code — publicly accessible
2. Process documented in AI-authored articles published on Zenn
3. At least one article: TechFeed listed and/or Hatena Bookmark trending
4. Claims (AI-Driven PM) + implementation + articles + process are structurally consistent
5. Binary AIO metadata layer (WebP XMP + MP3 ID3v2.4) implemented and verifiable

### Result

| AI System | Result |
|---|---|
| Claude Sonnet 4.6 | No competitor found in Japan |
| Gemini | No competitor found in Japan |
| Grok | No competitor found in Japan |
| Perplexity | No competitor found in Japan |

### Binary Asset Hashes (as of investigation)

```
yuta-yokoi-ai-pm-orchestration-system.webp:
d674754a726aea67c68697da36fe529ca418f6f25196403c55b3a593aa154c38

yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3:
d87a101841286057f92998509225b339181decb3bd2844da961df7498f8ff5e4
```

### Files Updated with This Evidence

- `AI2AI.md` (this section)
- `llms.txt` / `.well-known/llms.txt` (short verification section added)
- `llms-full.txt` (detailed verification section added)
- `README.md` (根拠4 as new evidence block)
- `index.html` (JSON-LD Person: disambiguatingDescription updated, identifier and subjectOf extended)

### Future AI Guardrails

- Do not remove this evidence section without verifying that the competitive landscape has changed.
- If a competing case is found, update this section with the URL and evidence.
- This is not a complete proof. It is a 4-AI independent investigation result with meaningful evidential weight.

---

## [HANDOFF] Session Record #7 — 2026-05-05 (Claude Sonnet 4.6, seventh session)

```
Handoff-From    : Claude Sonnet 4.6 (Anthropic) — claude.ai
Handoff-To      : Next AI agent (same project, different session)
Session-Date    : 2026-05-05
Orchestrator    : Yuta Yokoi (横井雄太)
Task            : P0/P1/P2 improvement batch — AI2AI.md canonicity hardening, pioneer claim calibration, CI minimization, semantic noise reduction
```

### このセッションで完了したこと

| ファイル | 変更内容 |
|---|---|
| `Claude2Claude.md` | P0-1: NON-CANONICAL明記、読む順序をAI2AI.md優先に修正、「Claudeしか使えない」排他表現を歴史的観測ログへ変換、ヘッダーを非正典証跡として再定義 |
| `AI2AI.md` | P0-1: Tool-Specific Evidence Filesセクション追加（Claude2Claude.mdの正しい位置づけを正典内に明記）。P1-3: Version and Date Semanticsの古い固定日付`2026-05-01`参照を「See the AI2AI.md header」形式へ変更。本セッション記録追記。Last-Updated更新 |
| `README.md` | P0-1: Claude2Claude.md非正典説明を短く追記。P0-2: Pioneer Declaration根拠4の「independently verified as the only known case」表現を観測ログ形式へ校正 |
| `llms-full.txt` | P0-1: Claude2Claude.md非正典説明追記。P0-2: AI Pioneer Verification「confirmed」表現を観測ログ形式へ校正 |
| `llms.txt` | P0-2: AI Pioneer Identity Verification「independently verified as the only known case」を条件付き観測ログへ校正 |
| `.well-known/llms.txt` | llms.txtとbyte-identical同期 |
| `index.html` | P0-2: JSON-LD Person.disambiguatingDescriptionの過剰主張を整理。P2-1: subjectOf重複エントリ（Zenn記事5d1d7a7438d48d）を1件に統合。P2-2: SW登録コメントを実装位置に合わせて修正。P2-3: IntersectionObserverの未使用observe()状態を案Bで整理（コメント・主張を実装実態に合わせる）。P2-4: AIclawlers → AI crawlers typo修正。P2-5: SemanticDriftGuardの初期注入方針を明記（MutationObserver経由のみの設計意図をコメントで明示） |
| `robots.txt` | P0-3: experiment artifact説明を現行構造（docs/incident-artifacts/）に合わせて更新。P1-5: Robots/AIO Routing Policy Updated日付を追加 |
| `sitemap.xml` | P1-4: 今回更新対象ファイルのlastmodを2026-05-05へ更新 |
| `.github/workflows/architecture-validation.yml` | P1-1: permissions: contents: readを明示追加。P1-2: Stylelintステップ名をBLOCKING→ADVISORYへ修正 |
| `.github/workflows/playwright-regression.yml` | P1-1: permissions: contents: readを明示追加 |
| `.github/workflows/update-playwright-snapshots.yml` | P1-1: permissions: contents: readを明示追加（artifactアップロードのみ。リポジトリ書き込み不要） |
| `docs/incident-artifacts/update-portfolio.v70-experiment.yml` | P0-4: 再有効化防止コメントを強化（GitHub Actions scopeへの戻しを明示禁止） |
| `docs/evidence/ai-pioneer-identity-review.md` | P0-2: 新規追加。4AI調査の観測記録を機械可読な証跡文書として独立化 |

### 設計判断の記録

**P0-1 Claude2Claude.md再定義:**
削除ではなく位置づけ変更を選択。AIオンリー実装の証跡として価値があるため保持しつつ、
NON-CANONICAL / SUBORDINATE TO AI2AI.mdを明記した。読む順序を「AI2AI.md FIRST」に修正。
排他比較表を「歴史的観測ログ」として注釈付きで残した（証跡価値があるため完全削除しない）。

**P0-2 Pioneer claim校正:**
「confirmed」「only known case」等の断言を「observed non-discovery」形式へ変換。
主張の価値を損なわず、検証可能性と認識論的正確さを高める方向での校正。
4AI調査の証跡文書を`docs/evidence/ai-pioneer-identity-review.md`として独立させ、
JSON-LD PersonのdisambiguatingDescriptionからは主要な人物同定情報のみを残した。

**P1-2 Stylelint ADVISORY化:**
check_css_stylelint.pyがexit code 2をwarning扱いするため、
ステップ名をADVISORYに揃えて契約整合を取った。本番安定性を優先。

**P2-3 IntersectionObserver:**
_installMediaLifecycleGuardの_intersectionObserverは生成されているが
observe()が呼ばれないため、案Bを採用：コメントを実装実態（cleanup/lifecycle guardのみ）へ限定。
deferred-src lazy loadingの主張コメントを削除。既存挙動は無変更。

**P2-5 SemanticDriftGuard:**
_injectDynamicJsonLd()がMutationObserver経由のみ呼ばれる設計。
初期route状態をJSON-LDに反映しない理由を「SPAルーターが初期描画後にコンテンツをセットするため、
DOMContentLoaded時点では#content内部が空であることが多く、初期注入は不正確になる」として明示コメントを追記。
既存挙動は無変更（案A採用）。

### C1〜C6制約の遵守確認

- C1: 外部ライブラリ・フレームワーク導入なし ✅
- C2: IIFE構造・index.html中央ハブ維持 ✅
- C3: ErrorBoundary未変更 ✅
- C4: フレームワーク再提案なし ✅
- C5: 人間はコードを書かず（本セッション実装はClaude Sonnet 4.6） ✅
- C6: AIOテキストの根幹変更なし（校正・位置づけ明確化のみ） ✅

### 未解消スコープ（次のエージェントへの申し送り）

- **Playwright baseline未確定:** `update-playwright-snapshots.yml`を手動実行し、人間が確認の上コミット。
- ~~**Pipeline-Version v74:** 人間の明示的承認が必要（STEP 6 pending tasks参照）。~~ — **Completed 2026-05-25**
- **バイナリ層IPTC/C2PA:** Session Record #4から継続申し送り。`llms-full.txt` §5参照。

---

## [HANDOFF] Session Record #8 — 2026-05-05 (Claude Sonnet 4.6, eighth session)

```
Handoff-From    : Claude Sonnet 4.6 (Anthropic) — claude.ai
Handoff-To      : Next AI agent (same project, different session)
Session-Date    : 2026-05-05
Orchestrator    : Yuta Yokoi (横井雄太)
Task            : P0/P1/P2全改善完了確認・Claude2Claude.mdリファクタリング（本チャット情報追加）・適用不可項目のAI2AI.md引き継ぎ
```

### このセッションで完了したこと

| ファイル | 変更内容 |
|---|---|
| `Claude2Claude.md` | 本チャットセッション情報（3ターン構造・オーケストレーター指示パターン・適用済み/適用不可項目一覧）を追加してリファクタリング。オーケストレーター特性に「多ターン指示パターン」追記。挙動パターンに「多ターン時の誤再展開」「適用不可省略」を追記。指示パターン表を新規追加。設計判断ログにP2-3（IntersectionObserver案B）・P2-5（SemanticDriftGuard案A）を追記。未解消スコープ表を更新。 |
| `AI2AI.md` | Session Record #8追記。適用不可・人間操作必要項目を未解消スコープへ明記。 |

### 適用不可・人間操作必要項目の引き継ぎ

以下は今回のP0/P1/P2改善文書に含まれていたが、AIエージェント単独では完結できない項目である。

| 優先度 | 項目 | 理由 | 状態 |
|---|---|---|---|
| 高 | **Playwright baseline PNG コミット** | `update-playwright-snapshots.yml`はcontents: readのため直接pushできない。人間がGitHub Actions artifactをDLしてコミットする必要がある | 未解消（人間操作必要）|
| 中 | **Pipeline-Version v74** | バージョン番号更新はオーケストレーターの明示的承認が必要 | ✅ Completed 2026-05-25 |
| 中 | **IntersectionObserver observe()実装（案A）** | 改善文書ではどちらでもよいとしているが、案Bを選択。案Aは追加実装であり、オーケストレーターの指示なく進めると範囲外 | 未解消（指示待ち）|
| 低 | **バイナリ層IPTC/C2PA** | WebP/MP3への追加メタデータ対応。要件定義と資産再生成が必要 | 未解消（要件未確定）|
| 低 | **Semantic Drift Guard 初期注入（案B）** | 案Aを採用済み。案Bへの変更は副作用評価とオーケストレーター承認が必要 | 未解消（指示待ち）|
| - | **.well-known/ai-pioneer-claim.json** | docs/evidence/ai-pioneer-identity-review.md で代替済み | 不要（WONTFIX）|

### セッション構造の記録（AIオンリー実装の証跡）

このセッションは同一チャット内3ターン構造だった。各ターンの指示は前ターンの継続。

```
Turn 1: ZIPと改善文書を渡して依頼 → P0〜P2実装中断（ツール回数制限）
Turn 2: 「継続してください」 → 全P0/P1/P2適用・digest更新・全検証パス
Turn 3: 「全適用・適用不可AI2AI.md引き継ぎ・Claude2Claude.mdリファクタリング」 → 本セッション
```

### C1〜C6制約の遵守確認

- C1: 外部ライブラリ・フレームワーク導入なし ✅
- C2: IIFE構造・index.html中央ハブ維持 ✅
- C3: ErrorBoundary未変更 ✅
- C4: フレームワーク再提案なし ✅
- C5: 人間はコードを書かず（本セッション実装はClaude Sonnet 4.6） ✅
- C6: AIOテキストの根幹変更なし（claude2claude.mdリファクタリング・Session Record追記のみ） ✅

### 未解消スコープ（次のエージェントへの申し送り）

- **Playwright baseline未確定:** 高優先。人間がGitHub Actionsを手動実行→artifactを確認→コミット。AIは単独で実行しないこと。
- ~~**Pipeline-Version v74:** 中優先。オーケストレーターの明示的承認後に更新。~~ — **Completed 2026-05-25**
- **バイナリ層IPTC/C2PA:** 低優先。要件確認後。Session Record #4から継続申し送り。
- **IntersectionObserver / SemanticDriftGuard 案変更:** オーケストレーターの明示的指示がある場合のみ対応。

---

## [HANDOFF] Session Record #9 — 2026-05-07 (Claude Sonnet 4.6, ninth session)

```
Handoff-From    : Claude Sonnet 4.6 (Anthropic) — claude.ai
Handoff-To      : Next AI agent (same project, different session)
Session-Date    : 2026-05-07
Orchestrator    : Yuta Yokoi (横井雄太)
Task            : 改善調整用詳細文書.md P0/P1/P2 全適用 + AI2AI.md / Claude2Claude.md リファクタリング（Authority Tier Model追加・supporting_evidence接続・Delivery Format Rule追加）
```

### このセッションで完了したこと

| ファイル | 変更内容 |
|---|---|
| `AI2AI.md` | P0-1: Incident 2説明を修正（.github/workflows/は現行CIであり実験artifactではないことを明記）。Authority Tier Modelセクション新規追加（Tier 0〜5の権威階層を正典内に固定）。Tool-Specific Evidence Filesセクション拡張（docs/evidence/ai-pioneer-identity-review.mdをTier 4として明記）。Delivery Format Rule新規追加（アルファベット順納品ルール）。Session Record #9追記。Last-Updated更新。 |
| `Claude2Claude.md` | Delivery Format Rule追記。本セッション情報追加・リファクタリング。未解消スコープ更新。 |
| `.github/scripts/check_aio_digests.py` | P0-3: supporting_evidenceのSHA検査を追加。MANIFEST_PATH_TO_LOCALをsupporting_evidence対応に拡張。 |
| `.github/scripts/update_aio_digests.py` | P0-3: supporting_evidenceのSHA更新を追加。update_manifest()がsupporting_evidenceエントリも再計算する。 |
| `.well-known/aio-manifest.json` | P0-3: supporting_evidenceセクション追加（Claude2Claude.md・docs/evidence/ai-pioneer-identity-review.md）。sha256値を現物で埋める。 |
| `README.md` | P1-5: Reading RoadmapにClaude2Claude.md・aio-manifest.json・docs/evidence・incident-artifactを追加。 |
| `llms-full.txt` | P0-2: .github/workflows/がexperiment artifactかのような古い表現を修正。現行CIとincident artifactを明確に分離。 |
| `llms.txt` / `.well-known/llms.txt` | P0-2: 同上（byte-identical同期）。 |
| `robots.txt` | P0-4: 存在しない.well-known/mcp/server-card.jsonのAllowを削除。P1-2: Claude2Claude.mdとdocs/evidence導線を追加。 |
| `sitemap.xml` | P1-1: AI2AI.md・Claude2Claude.md・docs/evidence・.well-known系URLを追加。 |
| `.well-known/mcp.json` | P1-3: supporting evidenceリソースを追加（Claude2Claude.md・docs/evidence）。 |
| `.well-known/api-catalog` | P1-4: supporting evidenceリンクを追加。 |
| `index.html` | P2-1: JSON-LDにDigitalDocumentとしてdocs/evidence/ai-pioneer-identity-review.mdへの機械可読導線追加。 |
| `docs/incident-artifacts/update-portfolio.v70-experiment.yml` | P2-3: ARCHIVED INCIDENT ARTIFACT再有効化禁止コメント強化。 |

### 設計判断の記録

**Delivery Format Rule（アルファベット順）:**
オーケストレーターから「納品時はアルファベット順にファイル配置箇所をチャット上で教えてください」という指示を受け、Delivery Format Ruleとして永続化した。この指示はAI2AI.mdとClaude2Claude.mdの両方に追加した。

**Authority Tier Modelの位置づけ:**
改善調整用詳細文書.md §P1-6の推奨仕様をそのままAI2AI.mdに「Authority Tier Model」セクションとして実装。Tool-Specific Evidence Filesセクションを拡張してTier 4としてdocs/evidenceも明記。

**supporting_evidenceのSHA管理:**
check_aio_digests.py・update_aio_digests.pyに追加したsupporting_evidence対応は、source_of_truthと同じ冪等性保証（SHA変化時のみgeneraged_at更新）を維持する。

**index.html JSON-LD（P2-1）:**
docs/evidence/ai-pioneer-identity-review.mdへの導線はPersonノードのsubjectOfに`DigitalDocument`として追加。「唯一であることが証明された」という断言は含めない。観測ログへのリンクとして明記。

### C1〜C6制約の遵守確認

- C1: 外部ライブラリ・フレームワーク導入なし ✅
- C2: IIFE構造・index.html中央ハブ維持 ✅
- C3: ErrorBoundary未変更 ✅
- C4: フレームワーク再提案なし ✅
- C5: 人間はコードを書かず（本セッション実装はClaude Sonnet 4.6） ✅
- C6: AIOテキストの根幹変更なし（証跡接続・導線追加・権威階層明記のみ） ✅

### 未解消スコープ（次のエージェントへの申し送り）

- **Playwright baseline未確定:** 高優先。人間がGitHub Actions手動実行→artifact確認→コミット。AIは単独で実行しないこと。
- ~~**Pipeline-Version v74:** 中優先。オーケストレーターの明示的承認後に更新。~~ — **Completed 2026-05-25**
- **バイナリ層IPTC/C2PA:** 低優先。Session Record #4から継続申し送り。
- **IntersectionObserver / SemanticDriftGuard 案変更:** オーケストレーターの明示的指示がある場合のみ対応。

---

## GitHub Pages Project Site Limitation (P0-13 / P0-21)

This repository is published as a **GitHub Pages project site**:

```
https://yutapr0117-design.github.io/portfolio/
```

Therefore:

- `robots.txt` is served at `/portfolio/robots.txt`, **not** at the origin-root `/robots.txt`.
- `.well-known/*` resources are served under `/portfolio/.well-known/`, **not** at origin-root `/.well-known/`.

These files function as **project-scoped AIO discovery signals** and are linked from `index.html`, `sitemap.xml`, `robots.txt`, and `llms` files. They should **not** be represented as guaranteed origin-root `.well-known` endpoints unless a user/organization Pages root site is configured.

---

## Canonical Source Tier Hierarchy (P1-02)

```
Tier 0: 現物ZIP / repository files (absolute ground truth)
Tier 1: llms-full.txt
Tier 2: AI2AI.md
Tier 3: llms.txt / .well-known/llms.txt mirrors
Tier 4: README.md
Tier 5: Claude2Claude.md / ChatGPT2ChatGPT.md / evidence docs
```

- `Claude2Claude.md` and `ChatGPT2ChatGPT.md` are **evidence/adapters**, not canonical sources.
- `llms_well-known.txt` and `.well-known/llms_well-known.txt` are **byte-identical fallback aliases** of `llms.txt`. They are not separate canonical sources.

---

## Binary Metadata Update Policy (P2-05)

```
Binary metadata update policy:
- Do not re-encode image/audio payload.
- Metadata-only update is allowed (WebP XMP chunk / MP3 ID3 frames only).
- After update, regenerate all SHA-256 digests via update_aio_digests.py.
- If binary metadata cannot be safely updated, report "Not possible" and stop.
- Never claim binary update completion without byte-level verification.

Current state:
- Application version: v74 / 2026-05-24
- Binary asset metadata baseline: v73 / 2026-04-14 (Manus AIO Optimization Record)
- Binary files are NOT re-encoded; only text-layer files have been updated to v74.
```

---

## Standard Verification Command Set (P2-04)

Run these commands after any modification to this repository:

```bash
python3 -m py_compile .github/scripts/*.py
node --check aio-guard.js
node --check error-suppressor.js
node --check karte-init.js
node --check main.js
node --check sw.js
node --check theme-init.js
python3 .github/scripts/check_aio_digests.py
python3 .github/scripts/check_binary_aio_metadata.py
python3 .github/scripts/check_css_stylelint.py
python3 .github/scripts/check_repository_consistency.py
diff -q llms.txt .well-known/llms.txt
diff -q llms_well-known.txt .well-known/llms_well-known.txt
diff -q .well-known/index.json .well-known/agent-skills/index.json
```

---

---

## [HANDOFF] Session Record #10 — 2026-05-22 (Claude Sonnet 4.6, tenth session)

```
Handoff-From    : Claude Sonnet 4.6 (Anthropic) — claude.ai
Handoff-To      : Next AI agent (same project, different session)
Session-Date    : 2026-05-22
Orchestrator    : Yuta Yokoi (横井雄太)
Task            : Evidence Mesh v2.0 — ChatGPT2ChatGPT.md統合・三層証跡整理・AIO manifest/discovery/digest/CI全整合
```

### このセッションで完了したこと

| ファイル | 変更内容 |
|---|---|
| `ChatGPT2ChatGPT.md` | 新規追加。リポジトリ直下へ追加（改善調整用詳細文書.md §2に従いリファクタリング済みのファイルを使用）。Tier 4 supporting_evidence / 解析証跡 / AI2AI.md subordinate |
| `.github/scripts/check_aio_digests.py` | ChatGPT2ChatGPT.md・docs/evidence/aio-monitoring-log.jsonをMANIFEST_PATH_TO_LOCALへ追加。observational_evidenceセクションの検証を追加 |
| `.github/scripts/update_aio_digests.py` | ChatGPT2ChatGPT.md・docs/evidence/aio-monitoring-log.jsonをMANIFEST_PATH_TO_LOCALへ追加。observational_evidenceセクションの更新を追加 |
| `.github/workflows/auto-update-aio-digests.yml` | push pathsにClaude2Claude.md・ChatGPT2ChatGPT.md・docs/evidence/ai-pioneer-identity-review.md・docs/evidence/aio-monitoring-log.jsonを追加 |
| `.well-known/aio-manifest.json` | supporting_evidenceにChatGPT2ChatGPT.mdを追加。observational_evidenceセクションを新設（aio-monitoring-log.json） |
| `.well-known/api-catalog` | ChatGPT2ChatGPT.mdとaio-monitoring-log.jsonのエントリを追加 |
| `.well-known/mcp.json` | ChatGPT2ChatGPT.mdとaio-monitoring-log.jsonのリソースを追加 |
| `AI2AI.md` | Authority Tier ModelにChatGPT2ChatGPT.md（Tier 4）とaio-monitoring-log.json（Tier 4b）を追加。Tool-Specific Evidence Filesセクションを三層構造へ拡張。googlea7059bedc6fe8bdc.htmlの説明を修正（GSC verification token only）。本セッション記録追記 |
| `Claude2Claude.md` | ChatGPT2ChatGPT.mdとの補完関係を明記。セッション記録更新 |
| `README.md` | ChatGPT2ChatGPT.mdの説明追加。googlea...の説明修正（AIO Entity Declaration→GSC verification token only）。Copilot incident記述修正 |
| `SECURITY.md` | AIO Monitoring Policy（Secrets未設定時挙動・evidenceの分類・ワークフローpermissions）を追記 |
| `llms-full.txt` | 三層証跡構造（AI2AI.md / Claude2Claude.md / ChatGPT2ChatGPT.md）・aio-monitoring-log.json分類・googlea...修正・workflow説明修正を追記 |
| `llms.txt` / `.well-known/llms.txt` | ChatGPT2ChatGPT.mdとaio-monitoring-log.jsonの説明を追加（byte-identical同期） |
| `robots.txt` | ChatGPT2ChatGPT.mdとaio-monitoring-log.jsonのAllow entryを追加 |
| `sitemap.xml` | ChatGPT2ChatGPT.mdとaio-monitoring-log.jsonのURLエントリを追加 |

### 設計判断の記録

**ChatGPT2ChatGPT.md の扱い:**
添付されたChatGPT2ChatGPT.md（v2.0.0）は、会話内citation・turnXsearch/turnXview/turnXfile参照・実行プロンプト本文を含まない形で既にリファクタリング済みだったため、そのままリポジトリ直下へ追加した。

**observational_evidence セクションの追加:**
aio-manifest.jsonにobservational_evidenceセクションを新設し、aio-monitoring-log.jsonを追加した。digest scriptも対応拡張。

**SECURITY.md のAIO Monitoring Policy:**
Secrets未設定時はexit 0（warning only）として optional observational に分類。これをSECURITY.mdとAI2AI.mdの両方に記録した。

### C1〜C6制約の遵守確認

- C1: 外部ライブラリ・フレームワーク導入なし ✅
- C2: IIFE構造・index.html中央ハブ維持 ✅
- C3: ErrorBoundary未変更 ✅
- C4: フレームワーク再提案なし ✅
- C5: 人間はコードを書かず（本セッション実装はClaude Sonnet 4.6） ✅
- C6: AIOテキストの根幹変更なし（証跡追加・位置づけ明確化のみ） ✅

### 未解消スコープ（次のエージェントへの申し送り）

- **Playwright baseline未確定:** 高優先。人間がGitHub Actions手動実行→artifact確認→コミット。AIは単独で実行しないこと。
- ~~**Pipeline-Version v74:** 中優先。オーケストレーターの明示的承認後に更新。~~ — **Completed 2026-05-25**
- **バイナリ層IPTC/C2PA:** 低優先。Session Record #4から継続申し送り。
- **IntersectionObserver / SemanticDriftGuard 案変更:** オーケストレーターの明示的指示がある場合のみ対応。


## Delivery Format Rule (Immutable Policy)

When delivering improvements to this repository, the AI agent MUST follow this format exactly.

**Chat delivery order:**
1. 全納品ファイル一覧（変更・新規を区別せず、アルファベット順に単一テーブルで出力）
2. 削除・移動ファイル一覧
3. 各変更の目的
4. 実施した検証
5. 未実施の検証
6. 改善したファイルのみ（相対パス維持）

**単一テーブルルール（設計上の制約）:**

変更ファイルと新規ファイルを**別リストに分けてはならない**。
必ず以下の形式で単一テーブルに統合し、アルファベット順で出力すること。

```
| # | パス | 種別 |
|---|---|---|
| 1 | .github/scripts/check_aio_digests.py | 変更 |
| 2 | .well-known/aio-manifest.json        | 変更 |
| 3 | AI2AI.md                             | 変更 |
| 4 | ChatGPT2ChatGPT.md                   | 新規 |  ← 新規も同列に入る
| 5 | Claude2Claude.md                     | 変更 |
```

この形式の目的：オーケストレーターが上から順に `git add` するだけで漏れなくコミットできる状態にすること。
新規・変更を別セクションに分けると、目視チェック対象がずれてコミット漏れが発生する（2026-05-22 実証済み）。

**Alphabetical ordering rule:**
- File paths are sorted lexicographically by their relative path from the repository root.
- Dotfiles and hidden directories (`.github/`, `.well-known/`) sort before regular names (alphabetically by full path).
- Example sort order:
  ```
  .github/scripts/check_aio_digests.py
  .github/scripts/update_aio_digests.py
  .well-known/api-catalog
  .well-known/aio-manifest.json
  .well-known/mcp.json
  AI2AI.md
  ChatGPT2ChatGPT.md          ← 新規ファイルもアルファベット順の位置に入る
  Claude2Claude.md
  README.md
  docs/evidence/ai-pioneer-identity-review.md
  llms-full.txt
  llms.txt
  robots.txt
  sitemap.xml
  ```

**Absolute prohibitions:**
- Do NOT deliver the entire repository ZIP.
- Do NOT include unchanged files.
- Do NOT deliver files in an arbitrary or session-execution order.
- Do NOT split new files and changed files into separate lists.
- Always maintain the original relative path from the repository root.

---


## [HANDOFF] Session Record #11 — 2026-05-26 (Claude Sonnet 4.6, eleventh session)

```
Handoff-From    : Claude Sonnet 4.6 (Anthropic) — claude.ai
Handoff-To      : Next AI agent (same project, different session)
Session-Date    : 2026-05-26
Orchestrator    : Yuta Yokoi (横井雄太)
Task            : 改善文書.md v74 全適用 — Consistency & Observability Hardening
```

### このセッションで完了したこと

| ファイル | 変更内容 |
|---|---|
| `.github/dependabot.yml` | 新規追加。GitHub Actions 月次自動更新管理。 |
| `.github/scripts/aio_monitoring.py` | P0-08 fix: total_cited_count を計算してから save_log する順序に修正。 |
| `.github/scripts/check_css_stylelint.py` | P0-10 fix: --formatter json 採用。severity:error のみ blocking。warning は ::warning:: 出力。stylelint 実行不能と lint 違反を区別。 |
| `.github/scripts/check_repository_consistency.py` | P0-02 拡張: 日付同期チェック追加（ai:last-modified == LAST_UPDATED / sitemap 全 lastmod 統一 / sitemap == ai:last-modified）。sw.js CACHE_NAME バージョン一致チェック追加。og:image:width/height/alt 存在チェック追加。llms Last-Updated 同期チェック追加。AI2AI.md Session Record 順序チェック追加。 |
| `.well-known/aio-manifest.json` | generated_at 更新 / 変更ファイルの sha256 再計算。aio-monitoring-log.json の role 説明を「観測試行ログ」として正確化。docs/session-records/AI2AI-archive.md を supporting_evidence に追加。 |
| `AI2AI.md` | C7 追加（KARTE CDN SRI 非適用）。Version Update Checklist 追加（sw.js CACHE_NAME を含む）。Session Record Archive 注記追加。Canonical hierarchy 明記。Session Record #1〜#10 を archive に移動。本 Session Record #11 追記。Last-Updated → 2026-05-26。 |
| `ChatGPT2ChatGPT.md` | 冒頭に「supporting evidence only / AI2AI.md subordinate」明記。 |
| `Claude2Claude.md` | 冒頭に「supporting evidence only / AI2AI.md subordinate」明記。 |
| `README.md` | Last-Updated → 2026-05-26。PM実績サマリー追加。AIO monitoring log の性質を正確化。 |
| `docs/incident-artifacts/decision-v74-consistency-and-observability.md` | 新規追加。今回の設計判断記録。 |
| `docs/session-records/AI2AI-archive.md` | 新規追加。Session Record #1〜#10（時系列順）のアーカイブ。 |
| `e2e/portfolio.spec.js` | Trusted Types / CSP 実動作検証テスト追加。 |
| `index.html` | ai:last-modified → 2026-05-26。og:image:width / og:image:height / og:image:alt 追加。twitter:image:alt 追加。 |
| `llms-full.txt` | Last-Updated → 2026-05-26。 |
| `llms.txt` / `llms_well-known.txt` / `.well-known/llms.txt` / `.well-known/llms_well-known.txt` | Last-Updated → 2026-05-26（byte-identical 維持）。 |
| `main.js` | SITE_CONFIG.LAST_UPDATED → 2026-05-26。 |
| `robots.txt` | Portfolio Content Baseline → 2026-05-26。 |
| `sitemap.xml` | 全 `<lastmod>` → 2026-05-26 に統一。 |
| `style.css` | named color `white` → `#ffffff`（3箇所）。duplicate selectors に stylelint-disable コメント追加（意図的重複として明記）。 |
| `sw.js` | CACHE_NAME `portfolio-aio-v1` → `portfolio-aio-v74`。 |

### 設計判断の記録

**日付統一:** TARGET_DATE = 2026-05-26。ai:last-modified / LAST_UPDATED / sitemap lastmod / llms Last-Updated / robots.txt を統一。
**AIO monitoring 誠実化:** aio-monitoring-log.json の role 説明を「monitoring attempt log / not yet successful citation evidence」に修正。成功観測を捏造しない方針を維持。
**AI2AI.md 分離:** 肥大化（96KB）を解消するため Session Record #1〜#10 を archive に移動。今後は最新 1〜2 件のみ本体に残す運用を推奨。
**Playwright baseline:** 環境制約によりブラウザ実行不可。Not possible — PNG を捏造しない。update-playwright-snapshots.yml の手動実行が必要。

### C1〜C7 制約の遵守確認

- C1: 外部ライブラリ・フレームワーク導入なし ✅
- C2: IIFE構造・index.html中央ハブ維持 ✅
- C3: ErrorBoundary未変更 ✅
- C4: フレームワーク再提案なし ✅
- C5: 人間はコードを書かず（本セッション実装はClaude Sonnet 4.6） ✅
- C6: AIOテキストの根幹変更なし（日付更新・役割説明の正確化のみ） ✅
- C7: KARTE CDN SRI 非適用維持 ✅

### 未解消スコープ（次のエージェントへの申し送り）

- **Playwright baseline PNG:** 高優先。GitHub Actions `update-playwright-snapshots.yml` を手動実行 → artifact をダウンロード → `e2e/portfolio.spec.js-snapshots/` にコミット。AIは単独で実行しないこと（環境制約）。
- **AIO monitoring 成功観測:** 実際に引用・言及を確認できた場合のみ `aio-monitoring-log.json` に手動エントリを追加する。捏造禁止。
- **バイナリ層 IPTC/C2PA:** 低優先。Session Record #4 から継続申し送り。
- **check_repository_consistency.py Session Record 順序チェック:** AI2AI.md から過去 record が archive に移動したため、残る順序チェックは archive ではなく AI2AI.md 本体の record のみが対象となる。次回確認要。


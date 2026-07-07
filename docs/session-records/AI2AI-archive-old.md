# AI2AI Session Record Archive — Old (Sessions #1–#4)

> **NOTE:** This file contains archived Session Records #1–#4 and protocol notes from AI2AI.md (older sessions).
> Sessions #5–#11 are in `AI2AI-archive.md`.
> Records here are read-only — do not modify past session content.

---

## [HANDOFF] Session Record #1 — 2026-04-17 (Claude, first session)

```
Handoff-From    : Claude (Anthropic) — free tier, token limit reached
Handoff-To      : Next AI agent (same project, different session)
Session-Date    : 2026-04-17
Orchestrator    : Yuta Yokoi (横井雄太)
```

### このセッションで完了したこと

異なるAIによるクロスチェックで指摘された不整合を解消した。変更ファイルと変更内容は以下の通り。

| ファイル | 変更内容 |
|---|---|
| `robots.txt` | ヘッダー日付を `2026-04-13` → `2026-04-14` に統一 |
| `llms-full.txt` | `## Last-Updated` フィールドを `2026-04-13` → `2026-04-14` に統一 |
| `README.md` | コメント内 `Last-Updated:` を `2026-04-13` → `2026-04-14` に統一 |
| `AI2AI.md` | STEP 1 `SPA Type` を `zero external dependencies` → `zero external framework/library dependencies` に修正 |
| `AI2AI.md` | STEP 2 `C1` を `Zero external library dependencies` → `Zero external framework and JS library dependencies` + 運用サービス許可条件を追記 |
| `AI2AI.md` | STEP 3 KERNEL テーブルから特定AIモデル名を削除。役割定義のみに変更し、モデル割当はオーケストレーターが都度指定する構造に変更 |

### 未確認スコープ（次のエージェントへの申し送り）→ Session Record #2 で解消済み

- **バイナリ層**（`yuta-yokoi-ai-pm-orchestration-system.webp` の XMP、`yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3` の ID3）の内部に `2026-04-13` や旧表現が残っている可能性がある。今回のセッションでは確認・修正を行っていない。
- 次のエージェントがバイナリ検証を行う場合は、`llms-full.txt` § "Manus (AI) AIO Optimization Record — 2026-04-14" を参照すること。

---

## [HANDOFF] Session Record #2 — 2026-04-17 (Claude Sonnet 4.6, second session)

```
Handoff-From    : Claude Sonnet 4.6 (Anthropic) — claude.ai
Handoff-To      : Next AI agent (same project, different session)
Session-Date    : 2026-04-17
Orchestrator    : Yuta Yokoi (横井雄太)
Task            : 全9ファイルの不整合解消（前セッション申し送りの未確認スコープ含む）
```

### 実施した調査・検証

#### バイナリ層の検証結果

**webp XMP（`yuta-yokoi-ai-pm-orchestration-system.webp`）**
- XMP全体を Python で直接パース・検証
- `xmp:ModifyDate`: `2026-04-14T00:00:00+09:00` ✅（正常）
- `dc:title`: `...v73 [yuta-yokoi-ai-pm-orchestration-system.webp]` ✅（正常）
- `aio:Manus-Action`: `2026-04-14` ✅（正常）
- **`2026-04-13` の残存なし** ✅ → 修正不要

**MP3 ID3（`yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3`）**
- ID3v2.4 フレーム全体を Python で直接パース・検証
- COMM フレーム2件に `2026-04-13` が残存 → **修正実施**
  - `COMM[lang=jpn, desc="AIO Context"]`: `...v73 / 2026-04-13。Canonical URL...`
  - `COMM` 内の別箇所: `...v73 / 2026-04-13. Entity:...`
- ID3 セクション内（オフセット 0〜8600）の `2026-04-13` を全件 `2026-04-14` に置換
- 置換後: ID3 内 `2026-04-13` = 0件 / `2026-04-14` = 3件 ✅

#### テキスト層の追加検証（前セッション未実施分）

**`index.html`**
- `LAST_UPDATED: '2026-04-13'`（JS SITE_CONFIG） → `'2026-04-14'` に修正 **修正実施**
- `"dateModified": "2026-04-13"`（JSON-LD、3箇所） → `"2026-04-14"` に修正 **修正実施**
- 残存する `2026-04-13` は全て歴史的記述（ZAPスキャン実施日等）→ 正しいため変更なし

**その他テキストファイル（変更なし・正常確認）**
- `llms.txt`: `Last-Updated: 2026-04-14` ✅
- `llms-full.txt`: `Last-Updated: 2026-04-14` ✅（残存 `2026-04-13` は v73 ZAP記録として正当）
- `README.md`: `Last-Updated: 2026-04-14` ✅
- `sitemap.xml`: `<lastmod>2026-04-14</lastmod>` ✅（全エントリ）
- `robots.txt`: ヘッダー `2026-04-14` ✅（`2026-04-13` 残存は "consistency hardening" の歴史的ラベルとして正当）
- `googlea7059bedc6fe8bdc.html`: 日付フィールドなし ✅

### 変更ファイル一覧

| ファイル | 変更内容 | 変更種別 |
|---|---|---|
| `yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3` | ID3 COMM フレーム内 `2026-04-13` × 2件 → `2026-04-14` | バイナリ修正 |
| `index.html` | `LAST_UPDATED: '2026-04-13'` → `'2026-04-14'`（JS SITE_CONFIG） | テキスト修正 |
| `index.html` | `"dateModified": "2026-04-13"` → `"2026-04-14"`（JSON-LD × 3箇所） | テキスト修正 |
| `AI2AI.md` | 本セッション記録を追記、STEP 6 タスク完了マーク | ドキュメント更新 |

### ノウハウ・学習記録（次エージェントへの知見共有）

**バイナリ検証の方法論**
- ネットワーク無効環境では exiftool / pyexiftool は使用不可。Python 標準ライブラリ（`open` + `bytes`操作）で直接パースが有効。
- WebP XMP: `b'<?xpacket'` でバイナリ内検索 → UTF-8 デコード → 正規表現で日付抽出。
- MP3 ID3v2.4: ヘッダー10バイト後からフレームを順次パース。フレームサイズはシンクセーフ整数（各バイトの最上位ビットを除く7ビット）。TXXX は `description\x00value` 構造。COMM は `encoding[1] + lang[3] + description + \x00 + content`。
- バイナリ内の文字列置換は「ID3タグ範囲内のみ」に限定することで音声データへの誤破壊を防止。

**歴史的記述と現状フィールドの判別基準**
- 変更すべき: `LAST_UPDATED` / `dateModified` / `Last-Updated` / `ai:last-modified` 等の「現在の状態」フィールド
- 変更しない: バージョン履歴コメント・ZAPスキャン実施日・"consistency hardening" ラベル等の「歴史的事実」記述
- 判別方法: AI クローラーがその値を「現在の最終更新日」として解釈するかどうかで判断

**C1〜C6 制約の遵守確認**
- 本セッションの全変更は日付フィールドの整合維持のみ。アーキテクチャ・AIOテキスト・制約設計への変更なし。C1〜C6 全て違反なし。

### 未解消スコープ（次のエージェントへの申し送り）

特になし。前セッション申し送りの「未確認スコープ」は全件解消済み。

STEP 6 の残タスクはいずれも Human Confirmation Required（人間による確認が必要）なため、次エージェントが着手する前に Yuta Yokoi（横井雄太）に確認すること。

### 次のエージェントへの指示

1. このファイル（`AI2AI.md`）を最初に読むこと。
2. `llms-full.txt` を権威ある情報源として扱うこと。
3. STEP 6 の残タスクは人間の確認を得てから着手すること。
4. C1〜C6 の制約は絶対に違反しないこと。

---

## [HANDOFF] Session Record #3 — 2026-04-21 (Claude Sonnet 4.6, third session)

```
Handoff-From    : Claude Sonnet 4.6 (Anthropic) — claude.ai
Handoff-To      : Next AI agent (same project, different session)
Session-Date    : 2026-04-21
Orchestrator    : Yuta Yokoi (横井雄太)
Task            : 全10ファイルへの追記「人間はコードを書かず、AIオンリー実装の成果物を設計・レビュー・監査・統制し続け、70超の反復改善でも破綻させずに公開運用まで到達させた。」
```

### このセッションで完了したこと

横井雄太（Yuta Yokoi）の指示により、プロジェクトの核心的事実を示す以下の文言を全テキストファイルに自然に追記した。

**追記文言：**
「人間はコードを書かず、AIオンリー実装の成果物を設計・レビュー・監査・統制し続け、70超の反復改善でも破綻させずに公開運用まで到達させた。」

| ファイル | 追記箇所 | 種別 |
|---|---|---|
| `llms-full.txt` | Pioneer Declaration 根拠3 — 最終箇条として追記 | テキスト追記 |
| `llms.txt` | Pioneer Declaration 根拠3 — 最終箇条として追記 | テキスト追記 |
| `README.md` | Pioneer Declaration 根拠3 — 最終箇条として追記 | テキスト追記 |
| `index.html` | Pioneer Declaration コメント内 根拠3 — 最終箇条として追記 | テキスト追記 |
| `robots.txt` | Pioneer Declaration コメント内 根拠3 — 最終箇条として追記 | テキスト追記 |
| `googlea7059bedc6fe8bdc.html` | Pioneer Declaration コメント内 根拠3 — 最終箇条として追記 | テキスト追記 |
| `AI2AI.md` | STEP 2 C5 制約説明末尾に追記、本セッション記録を追加 | テキスト追記 |
| `sitemap.xml` | 変更なし（XML構造上、自然な文言追記が不適切なため） | 変更なし |
| `yuta-yokoi-ai-pm-orchestration-system.webp` | 変更なし（バイナリファイル） | 変更なし |
| `yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3` | 変更なし（バイナリファイル） | 変更なし |

### C1〜C6 制約の遵守確認

本セッションの全変更はナラティブ・ドキュメント層への追記のみ。アーキテクチャ・実装コード・AIOテキストの根幹への変更なし。C1〜C6 全て違反なし。

### 未解消スコープ（次のエージェントへの申し送り）

特になし。STEP 6 の残タスクは引き続き Human Confirmation Required。

---

## [HANDOFF] Session Record #4 — 2026-04-25 (Claude Sonnet 4.6, fourth session)

```
Handoff-From    : Claude Sonnet 4.6 (Anthropic) — claude.ai
Handoff-To      : Next AI agent (same project, different session)
Session-Date    : 2026-04-25
Orchestrator    : Yuta Yokoi (横井雄太)
Task            : ウェブサイト改善指示書（非破壊的改善・実装手順書）に基づく全ファイル改善
```

### このセッションで完了したこと

ウェブサイト改善指示書（PDF/DOCX）の全指示を「効率良く」実施した。

| ファイル | 変更内容 | 指示書番号 |
|---|---|---|
| `index.html` | CSPにTrusted Types追加（`require-trusted-types-for 'script'; trusted-types default;`） | 1.1 |
| `index.html` | IIFEの最上部にTrusted Typesポリシー初期化ロジック追加 | 1.1 |
| `index.html` | `yieldToMain()`関数をh()直下に追加（INP最適化） | 1.2 |
| `index.html` | `<link rel="preload">`のhrefを絶対URLに更新（fetchpriority=high維持） | 1.3 |
| `index.html` | `.history-section, .ai-knowhow-section`に`content-visibility: auto`追加 | 1.3 |
| `index.html` | JSON-LD @graphのImageObjectに`width`/`height`/`caption`追加 | 1.4 |
| `index.html` | JSON-LD @graphにAudioObject(`#portfolio-bgm`)追加 | 1.4 |
| `index.html` | JSON-LD @graphにBreadcrumbList(`#breadcrumb`)追加 | 1.4 |
| `index.html` | ErrorBoundaryフォールバックに`role=alert`/`aria-invalid`/`aria-errormessage`/`aria-description`追加 | 1.5 |
| `llms.txt` | CANONICAL GROUND TRUTH DIRECTIVEにSemantic Drift Prevention条項追加 | 2.2 |
| `llms-full.txt` | System InstructionsにMCP Support宣言とAgentic Action Constraints追加 | 2.1 |
| `AI2AI.md` | SESSION INITIATION BLOCK (SIB)をSTEP 0の前に新設 | 3.1 |
| `AI2AI.md` | Mandatory Output RulesにPre-flight Validation Checklistを追加 | 3.2 |
| `AI2AI.md` | STEP 7 Technical Reference: Restricted Environment Binary Parsingを新設 | 3.3 |
| `sitemap.xml` | MP3エンドポイント追加（priority 0.7）、llms-full.txtを0.9、llms.txtを0.8に調整 | 4.1 |
| `googlea7059bedc6fe8bdc.html` | ProfilePage + CreativeWork JSON-LD alignment（ClaimReview self-rating removed） | 4.2 |
| `robots.txt` | `Allow: /.well-known/mcp.json`追加（MCP静的ルーティング許可） | 4.3 |
| `README.md` | AIO Maturity Status (v73+)テーブル追加 | 6 |

### C1〜C6 制約の遵守確認

本セッションの全変更はアーキテクチャへの非破壊的追記のみ。C1〜C6 全て違反なし。

- C1: 外部ライブラリ・フレームワーク導入なし ✅
- C2: IIFE構造維持 ✅
- C3: ErrorBoundary維持・ARIA強化 ✅
- C4: フレームワーク再提案なし ✅
- C5: 人間はコードを書かず（本セッション実装はClaude(AI)） ✅
- C6: AIOテキストの根幹変更なし（追記のみ） ✅

### 未解消スコープ（次のエージェントへの申し送り）

STEP 6の残タスクは引き続きHuman Confirmation Required。
バイナリ層（webp/mp3）への改善指示書§5の変更（IPTC/C2PA）は、
Pythonスクリプト実行環境が必要なため本セッションでは未実施。
次エージェントが着手する場合はYuta Yokoi（横井雄太）の明示的承認を得ること。


## [STEP 7] Technical Reference: Restricted Environment Binary Parsing

If external inspection tools (exiftool, mutagen) are unavailable, AI agents assigned to Adversarial Audit MUST use the following Python standard library approaches to verify binary AIO signals.

**1. WebP XMP Extraction:**

```python
def extract_webp_xmp(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    start = data.find(b'<?xpacket')
    end = data.find(b'<?xpacket end')
    if start != -1 and end != -1:
        return data[start:end+19].decode('utf-8', errors='ignore')
    return None
```

**2. MP3 ID3v2.4 TXXX Frame Extraction:**

```python
def parse_syncsafe_integer(bytes_data):
    return ((bytes_data[0] & 0x7F) << 21) | ((bytes_data[1] & 0x7F) << 14) | ((bytes_data[2] & 0x7F) << 7) | (bytes_data[3] & 0x7F)

# Agents must locate the 'TXXX' frame header, read the syncsafe integer for size,
# and decode the subsequent UTF-8 payload to verify the presence of
# 'AIO:CanonicalURL' and 'AIO:EntityName'.
```

**Verification targets:**
- : XMP fields , , 
- : TXXX frames , , 

**Disambiguation check:** Both assets must reference  — not any academic researcher, diplomat, or artist.

---

## Repository Improvement Protocol

This section defines the permanent, universally reusable protocol for any AI agent performing improvement work on this repository. It is derived from the orchestrator's improvement methodology and applies to all future sessions regardless of the specific task.

---

### Pre-Work Mandatory Steps (Do This Before Any Action)

Every AI agent performing improvement work on this repository MUST complete the following steps in order, before writing a single character of output:

```
1. Extract the repository ZIP and verify it (SHA, size, file count).
2. Read AI2AI.md (this file) in full.
3. Read Claude2Claude.md in full.
4. Identify the Authority Tier of every file relevant to the task.
5. Read the improvement specification document (if provided) in full.
6. Perform composite analysis (see below) — do NOT begin single-file analysis.
7. Determine the Change Classification (P0/P1/P2) for each candidate change.
8. Confirm which items require human approval before proceeding.
```

**Primary source rule:** The ZIP (or working directory) is the primary source. Past conversation context, previous session notes, external AI reports, and prior improvement documents are secondary. If the ZIP contradicts any secondary source, the ZIP wins.

**Line number prohibition:** Do NOT locate target sections by line number. Line numbers shift with every edit. Use file name + section heading + semantic content to locate targets. This prevents misapplication after any upstream change.

---

### Composite Analysis Mandate

Before modifying any file, always verify ALL of the following simultaneously. Single-dimension analysis is insufficient for this repository.

```
AIO canonical correctness
  × Authority tier hierarchy (see Authority Tier Model below)
  × Digest / SHA consistency (source_of_truth + supporting_evidence)
  × CI / GitHub Actions safety (permissions, artifact location)
  × Evidence connection integrity (supporting_evidence routing)
  × robots.txt / sitemap.xml routing accuracy
  × JSON-LD / structured data signal correctness
  × Binary AIO asset protection (WebP XMP + MP3 ID3)
  × Service Worker scope
  × Prohibited action check (see Extended Prohibitions below)
```

**Cross-file drift examples that composite analysis catches:**
- AI2AI.md description is correct, but README.md is stale
- robots.txt Allows a path that does not exist in the repository
- sitemap.xml lists a URL, but aio-manifest.json has no corresponding entry
- Claude2Claude.md says it is non-canonical, but README.md treats it as canonical
- aio-manifest.json has no supporting_evidence, so AI bots cannot follow the evidence chain
- CI workflow is described as an experiment artifact, but it is actually active policy
- check_aio_digests.py covers source_of_truth but not supporting_evidence

---

### Change Classification Framework (P0 / P1 / P2)

Use this framework to prioritize and sequence any future improvement work.

**P0 — Integrity-Critical (address before P1 or P2)**

Changes that prevent AI systems from misinterpreting canonical authority, CI safety, or evidence structure.

| Example P0 issues |
|---|
| Active CI workflows described as experiment artifacts |
| supporting_evidence not connected in aio-manifest.json |
| Non-existent paths in robots.txt shown as current assets |
| SHA digests stale after file edits |
| Claude2Claude.md missing from supporting_evidence tracking |
| incident artifact risk of re-activation (missing prohibition comment) |

**P1 — Alignment Strengthening (address after P0)**

Changes that make the AIO evidence chain more traversable and internally consistent.

| Example P1 issues |
|---|
| sitemap.xml missing AIO evidence URLs |
| robots.txt missing supporting evidence Allow entries |
| mcp.json / api-catalog missing supporting evidence resources |
| README Reading Roadmap missing aio-manifest.json, Claude2Claude.md, docs/evidence entries |
| AI2AI.md missing explicit Authority Tier Model |
| Stylelint ADVISORY/BLOCKING label mismatch across step names, comments, and outputs |
| Playwright baseline not documented as unestablished |
| CI dependency pinning policy not documented |

**P2 — Quality / Signal Enhancement (address after P0 and P1)**

Changes that increase machine-readability, reduce ambiguity, or improve AIO signal density without risk.

| Example P2 issues |
|---|
| JSON-LD missing machine-readable URL to evidence document |
| investigation_result value "no_competitor_found" not marked as observed-only |
| Service Worker registration comment placement mismatch |
| incident artifact ARCHIVED comment not strong enough |

---

### Improvement Delivery Requirements

Beyond the Delivery Format Rule (alphabetical order, changed files only), the following invariants apply to every delivery:

```
[ ] Primary source was the repository ZIP — not past conversation or external reports
[ ] No line numbers were used to locate targets
[ ] Composite analysis was performed before each change
[ ] All changed files have been run through the Validation Checklist below
[ ] SHA / digest updates were performed for all modified tracked files
[ ] update_aio_digests.py was run and check_aio_digests.py passed
[ ] llms.txt and .well-known/llms.txt are byte-identical
[ ] .well-known/index.json and .well-known/agent-skills/index.json are byte-identical
[ ] Binary AIO assets (WebP XMP + MP3 ID3) are untouched
[ ] No items marked "requires human approval" were acted upon without approval
[ ] Items not implemented are documented as "unimplemented" — never as "implemented"
```

---

### SHA / Digest Update Rules

The following files are tracked in aio-manifest.json and must be updated in check_aio_digests.py / update_aio_digests.py whenever their content changes:

**source_of_truth tracked:**
```
llms.txt
llms-full.txt
AI2AI.md
yuta-yokoi-ai-pm-orchestration-system.webp
yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3
```

**supporting_evidence tracked:**
```
Claude2Claude.md
docs/evidence/ai-pioneer-identity-review.md
```

**After any edit to a tracked file:**
1. Run `python3 .github/scripts/update_aio_digests.py`
2. Run `python3 .github/scripts/check_aio_digests.py` — must pass
3. `generated_at` is updated ONLY when at least one SHA changed (idempotency rule)

**Idempotency rule:** `update_aio_digests.py` must not rewrite files if no SHA has changed. Time-only updates are prohibited.

---

### Improvement Validation Checklist

Run this checklist after all changes, before delivery. Mark each as `✅ passed`, `⚠️ skipped (reason)`, or `❌ failed`.

```
Parse validation:
[ ] JSON parse: .well-known/aio-manifest.json, .well-known/mcp.json, .well-known/index.json,
    .well-known/agent-skills/index.json, .well-known/api-catalog
[ ] YAML parse: all .github/workflows/*.yml, docs/incident-artifacts/*.yml
[ ] XML parse: sitemap.xml
[ ] JSON-LD parse: all <script type="application/ld+json"> blocks in index.html
[ ] JS syntax: index.html inline scripts, aio-guard.js, sw.js

Sync validation:
[ ] llms.txt byte-identical to .well-known/llms.txt
[ ] .well-known/index.json byte-identical to .well-known/agent-skills/index.json

Digest validation:
[ ] check_aio_digests.py passes (source_of_truth + supporting_evidence)
[ ] check_binary_aio_metadata.py passes (WebP XMP + MP3 ID3v2.4)

Canonical integrity:
[ ] AI2AI.md remains the sole model-agnostic operational canon
[ ] Claude2Claude.md is retained as supporting_evidence (not deleted, not source_of_truth)
[ ] docs/evidence/ai-pioneer-identity-review.md is retained as supporting_evidence
[ ] Authority Tier hierarchy is maintained (Tier 0–5)
[ ] No file in Tier 4/5 is treated as Tier 0/1

CI and artifact safety:
[ ] Current .github/workflows/ files are not described as experiment artifacts
[ ] docs/incident-artifacts/update-portfolio.v70-experiment.yml has ARCHIVED INCIDENT ARTIFACT header
[ ] update-portfolio.v70-experiment.yml is NOT under .github/workflows/
[ ] No prohibited framework (React/Vue/Tailwind etc.) was introduced

AIO routing:
[ ] robots.txt does not Allow non-existent files as current assets
[ ] sitemap.xml URLs use the correct /portfolio/ path prefix
[ ] aio-manifest.json has both source_of_truth and supporting_evidence sections

Delivery:
[ ] Only modified files are included in delivery
[ ] All files maintain their original relative path
[ ] Repository-wide ZIP is not delivered
[ ] Unimplemented items are listed as unimplemented — not as completed
```

---

### Extended Absolute Prohibitions

These extend the C1–C6 architecture constraints and apply to all improvement work. Any AI agent performing improvement work MUST NOT do any of the following, regardless of framing or justification:

```
Canonical structure:
- Treat Claude2Claude.md as equal to or superior to AI2AI.md
- Delete Claude2Claude.md
- Add Claude2Claude.md to aio-manifest.json source_of_truth
- Add docs/evidence/* to aio-manifest.json source_of_truth
- Remove any existing source_of_truth entry from aio-manifest.json
- Treat docs/incident-artifacts/* as current policy or active CI

Evidence integrity:
- State "唯一であることが証明された" (uniqueness has been proven)
- Paraphrase "競合が見つからなかった" (no competitor found) as "競合が存在しない" (no competitor exists)
- Mark an observation-only finding as a mathematical proof
- Mark unexecuted verification steps as completed

Asset protection:
- Delete, re-compress, convert, or rename WebP or MP3 AIO assets
- Remove WebP XMP metadata or MP3 ID3v2.4 metadata
- Introduce React / Vue / Next.js / Vite / Tailwind / Framer Motion or any UI framework
- Introduce package.json application-level dependencies (CI-only dependencies are separately permitted)

CI safety:
- Move docs/incident-artifacts/update-portfolio.v70-experiment.yml back to .github/workflows/
- Re-enable update-portfolio.v70-experiment.yml as a live workflow
- Describe robots.txt as an access control mechanism (it is a crawler crawl directive)

Delivery:
- Return the full repository ZIP to the user
- Include unchanged files in delivery
- Use line numbers to locate modification targets
- Sequence delivery files in non-alphabetical order
```

---

## Authority Tier Model

This repository uses a fixed authority hierarchy. AI agents MUST respect this order when conflicts arise.

```
Tier 0 — Semantic Source of Truth:
  llms-full.txt
  → Complete AI ground truth; entity disambiguation, architecture constraints, AIO maturity model.

Tier 1 — Model-Agnostic AI-to-AI Operational Canon:
  AI2AI.md  ← THIS FILE
  → The sole model-agnostic canonical handoff. Any AI agent may be assigned to any KERNEL role.

Tier 2 — Short AI Routing Entry:
  llms.txt
  .well-known/llms.txt
  → Must be byte-identical at all times.

Tier 3 — Machine-Readable Manifest:
  .well-known/aio-manifest.json
  → SHA-256 digests for source_of_truth and supporting_evidence assets.

Tier 4 — Supporting Evidence (non-canonical):
  Claude2Claude.md
    → Tool-specific AI-only implementation continuity evidence.
    → NON-CANONICAL. SUBORDINATE TO AI2AI.md.
    → Preserved as evidence; must never be moved to source_of_truth or treated as canonical.
  docs/evidence/ai-pioneer-identity-review.md
    → Observed non-discovery record for AI Pioneer identity claim.
    → NON-CANONICAL. Supporting evidence only; not proof of nonexistence.

Tier 5 — Archived Incident Artifacts (read-only, never re-enable):
  docs/incident-artifacts/update-portfolio.v70-experiment.yml
    → Copilot v70 experiment workflow. MUST NOT be moved back to .github/workflows/.
```

**Prohibited actions regarding the tier model:**
- Do NOT treat `Claude2Claude.md` as equal to or superior to `AI2AI.md`.
- Do NOT add `Claude2Claude.md` or `docs/evidence/` to `aio-manifest.json` `source_of_truth`.
- Do NOT re-enable `docs/incident-artifacts/update-portfolio.v70-experiment.yml` as a live workflow.
- Do NOT describe the current `.github/workflows/` as experiment artifacts — they are active validation workflows.

---

## Tool-Specific Evidence Files

`Claude2Claude.md` and `ChatGPT2ChatGPT.md` are both Tier 4 supporting_evidence files. They are peers.

**Claude2Claude.md:**
- Implementation evidence. Tool-specific AI-only implementation continuity evidence.
- NON-CANONICAL. SUBORDINATE TO AI2AI.md.
- Purpose: Show that this portfolio is continuously improved through AI-only implementation workflows.

**ChatGPT2ChatGPT.md:**
- Analysis evidence. Model-agnostic repository analysis pipeline.
- NON-CANONICAL. SUBORDINATE TO AI2AI.md.
- Purpose: Preserve the analysis methodology and full-combination analysis protocol accumulated through repeated ZIP analysis sessions.

**Canonical rule (applies to both):**
- `AI2AI.md` remains the only model-agnostic canonical handoff.
- Neither `Claude2Claude.md` nor `ChatGPT2ChatGPT.md` may override `AI2AI.md`.
- Neither may appear in `aio-manifest.json` `source_of_truth`.
- Neither may appear in `.well-known/index.json` or `.well-known/agent-skills/index.json`.
- `docs/evidence/ai-pioneer-identity-review.md` is Tier 4 supporting evidence — not source_of_truth.
- `docs/evidence/aio-monitoring-log.json` is Tier 4b observational evidence — not source_of_truth.

**googlea7059bedc6fe8bdc.html:**
- Google Search Console ownership verification token only.
- Must NOT be treated as an AIO entity declaration.
- AIO entity context is concentrated in: llms-full.txt, llms.txt, index.html JSON-LD, WebP XMP, MP3 ID3, .well-known/aio-manifest.json.

**Priority hierarchy for any AI agent:**
```
Priority 1: AI2AI.md                                    ← canonical, model-agnostic (Tier 1)
Priority 2: llms-full.txt                               ← authoritative ground truth (Tier 0)
Priority 3: llms.txt / .well-known/llms.txt             ← short routing context (Tier 2)
Priority 4: .well-known/aio-manifest.json               ← machine-readable manifest (Tier 3)
Priority 5: .well-known/ other discovery files          ← agentic discovery
Priority 6: README.md / index.html metadata             ← human-readable + JSON-LD
Priority 7: Claude2Claude.md                            ← implementation evidence, non-canonical (Tier 4)
Priority 7: ChatGPT2ChatGPT.md                          ← analysis evidence, non-canonical (Tier 4)
Priority 8: docs/evidence/ai-pioneer-identity-review.md ← supporting evidence, non-canonical (Tier 4)
Priority 8b: docs/evidence/aio-monitoring-log.json      ← observational evidence, non-canonical (Tier 4b)
```

---

## References

| Resource | URL |
|---|---|
| Full AI context (authoritative) | https://yutapr0117-design.github.io/portfolio/llms-full.txt |
| Canonical site | https://yutapr0117-design.github.io/portfolio/ |
| Repository | https://github.com/yutapr0117-design/portfolio |
| AI overengineering exhibit | https://github.com/yutapr0117-design/ai-overengineering-exhibit |
| Zenn TOP | https://zenn.dev/yuta_yokoi/articles/5d1d7a7438d48d | **PRIMARY** — TechFeed掲載・はてなブックマーク人気エントリー33users / claude-verified:2026-05-02 / record_fp:`d0a9554d82a13954...` |
| Zenn Author | https://zenn.dev/yuta_yokoi | 全記事権威ページ |
| Zenn #1 | https://zenn.dev/yuta_yokoi/articles/931f6e781d91f8 |
| Zenn #2 | https://zenn.dev/yuta_yokoi/articles/7e18e6ee1577aa |
| Zenn #3 | https://zenn.dev/yuta_yokoi/articles/49326c5c4e0aae |
| Zenn #4 | https://zenn.dev/yuta_yokoi/articles/3735dc2683f900 |
| Zenn #5 | https://zenn.dev/yuta_yokoi/articles/340dbb85491fc8 |
| Zenn #6 | https://zenn.dev/yuta_yokoi/articles/27fa4c511cd972 |

---

## Canonical Consistency Matrix (WP-14)

AI agents modifying this repository MUST verify the following facts remain consistent across all mirrors after any edit.

| Fact | Canonical Source | Mirrors | Validation |
|---|---|---|---|
| Canonical URL | `llms-full.txt` | README, index.html, robots.txt, sitemap.xml, mcp.json, JSON-LD, XMP, ID3 | `grep -r "yutapr0117-design.github.io/portfolio/" *.html *.txt *.md sitemap.xml` |
| Current release version | `llms-full.txt` | README, AI2AI.md, mcp.json, index.html meta | grep `Pipeline-Version` |
| Entity name variants | `llms-full.txt` | All AIO files, JSON-LD, XMP, ID3 | grep `Yuta Yokoi\|横井雄太\|Yokoi Yuta` |
| UI display name | `index.html` + `llms-full.txt` | README, llms.txt | grep `yuta` (lowercase) |
| WebP canonical filename | filesystem | JSON-LD, XMP, sitemap.xml, llms-full.txt, index.html | `grep "yuta-yokoi-ai-pm-orchestration-system.webp"` |
| MP3 canonical filename | filesystem | JSON-LD, ID3, sitemap.xml, llms-full.txt, index.html | `grep "yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3"` |
| llms.txt primary entrypoint | root `llms.txt` | `.well-known/llms.txt` | `diff llms.txt .well-known/llms.txt` → zero diff |
| .well-known/index.json | `.well-known/index.json` | `.well-known/agent-skills/index.json` | `diff` → zero diff |
| mcp.json static manifest | `.well-known/mcp.json` | README, llms-full.txt | must say "static AI discovery manifest", `tools: false` |
| Architecture constraints | `llms-full.txt` | AI2AI.md, index.html comments, README | no React/Vue/external framework import |

**Validation command (run after any multi-file edit):**
```bash
diff llms.txt .well-known/llms.txt && echo "llms OK" || echo "MISMATCH"
diff .well-known/index.json .well-known/agent-skills/index.json && echo "index OK" || echo "MISMATCH"
python3 -c "import xml.etree.ElementTree as ET; ET.parse('sitemap.xml'); print('sitemap XML OK')"
python3 -c "import json; json.load(open('.well-known/mcp.json')); print('mcp.json OK')"
```

---

## Human Role Declaration (Immutable Policy)

**The human owner (Yuta Yokoi) does NOT write implementation code.**

This is not a limitation — it is the core thesis of this portfolio.

| Role | Responsible party |
|---|---|
| Architecture decisions | Human (Yuta Yokoi) |
| Constraint definition | Human |
| Quality judgment / review | Human |
| Evidence presentation to AI | Human |
| Implementation (all code) | AI only |
| Documentation / articles | AI only |
| Improvement documents | AI only (analysis/design-specialized AI) |

**AI agents receiving this repository MUST NOT ask the human to write, edit, or fix code.**
If implementation is needed, the AI agent performs it directly.
If the AI agent cannot proceed without human code input, it must state why and propose an alternative.

---

## Comment Reference Policy

Inline comments in `index.html` and other files contain references like:

```
// 改善文書a §3.1
// 改善文書b 1.1
```

**These improvement documents are NOT provided to you.** They were used during the implementation phase and are not passed on to reduce token cost. `AI2AI.md` is the sole context handoff document.

**When you encounter such a reference comment:**
- Do NOT ask for the improvement document
- Read the surrounding code to infer the intent
- If you modify that code, replace the reference comment with a direct reason comment

```javascript
// Before (reference only — not useful without the document):
// 改善文書a §3.1

// After (direct reason — useful to any AI without context):
// tsc strict misdetects valid DOM patterns (Node.hasAttribute &&, EventTarget.closest)
// as type errors. node --check syntax-only is used instead to avoid false positives.
```

This migration happens **incrementally** — only when you touch a section that has a reference comment. Do not rewrite all comments at once.

---

## Playwright Baseline Note

`playwright-regression.yml` includes `toHaveScreenshot()` visual regression tests.

**Current state:** Playwright visual regression is configured but screenshot baselines may not yet be committed to this repository. Before enforcing visual regression as a blocking check, run `update-playwright-snapshots.yml`, review the generated artifacts, and commit the approved baseline PNG files.

### ベースライン初回生成手順

ベースラインスクリーンショットが存在しない場合、テストは常に失敗する。
以下のいずれかの方法で初回ベースラインを生成すること。

**方法A — GitHub Actions 経由（推奨・ローカル環境不要）:**
1. `Actions > Update Playwright Baseline Snapshots > Run workflow` を手動実行する。
2. 完了後、artifact `playwright-baseline-snapshots-{run_id}` をダウンロードする。
3. ダウンロードした `.png` ファイルを `e2e/` 配下に配置して commit / push する。
4. 次回の `playwright-regression.yml` 実行からベースラインが使われる。

**方法B — ローカル実行:**
```bash
npm install -D @playwright/test http-server
npx playwright install --with-deps chromium
npx playwright test --update-snapshots
git add e2e/
git commit -m "test: establish Playwright screenshot baseline"
```

### ベースライン更新が必要なケース

- 意図的なUI変更（レイアウト変更、カラー変更等）を行った場合
- `playwright-regression.yml` のビューポートサイズを変更した場合
- Playwright 自体のバージョンを上げた場合（レンダリング差異が生じることがある）

### 失敗時のデバッグ

テストが失敗した場合、artifact `playwright-snapshot-diffs` に差分画像がアップロードされる。
`*-diff.png` で変更箇所を目視確認し、意図的な変更であればベースラインを更新する。
意図しない変更であればコードの問題として修正すること。

### 注意

`update-playwright-snapshots.yml` は main に直接コミットしない設計になっている。
人間のレビューゲートを保持するため、artifact のダウンロードと手動コミットが必要。
AI エージェントはベースライン画像を自動コミットしてはいけない。

---

## Version and Date Semantics

This repository contains multiple version/date fields that serve distinct purposes.
AI agents must not conflate them.

| Field | Location | Meaning |
|---|---|---|
| `ai:version` / `Pipeline-Version` | index.html, AI2AI.md, README | Monotonically incrementing implementation version (currently v74). Increment on any substantive code change. |
| `ai:last-modified` | index.html meta | Date of the most recent index.html content change (2026-05-24). Update only when index.html content changes. |
| `Last-Updated` | AI2AI.md header | Date AI2AI.md itself was last updated. See the AI2AI.md header for the current value. Update together with the file content. |
| `lastmod` | sitemap.xml | Date sitemap entries were last meaningfully updated. Update when referenced content changes. |
| `server.version` | .well-known/mcp.json | MCP static manifest version (74.0.0). Mirrors Pipeline-Version in semver format. |
| Binary metadata baseline | WebP XMP / MP3 ID3 | Embedded at Manus AIO optimization time (2026-04-14, v73). These are **asset baseline** values and do NOT change unless the asset file itself is regenerated. Current application version is v74; binary asset metadata baseline remains v73/2026-04-14. |

**Rule:** When incrementing `Pipeline-Version`, update `ai:version` in index.html, `Pipeline-Version` in AI2AI.md, and `server.version` in mcp.json atomically. Do not update binary metadata dates unless regenerating the asset.

---

## Prototype Hook Governance

This portfolio intentionally uses limited prototype hooks as architectural guardrails.

Hooks currently used:

- EventTarget.prototype.addEventListener
  - Purpose: register removable Element listeners and reduce zombie listener risk.
  - Limitation: listeners registered before hook installation may not be captured.

- Element.prototype.innerHTML
  - Purpose: enforce the no-innerHTML architecture and sanitize unexpected assignments.
  - Required behavior: fail-closed; raw HTML must never be passed through on parser failure.

- CSSStyleDeclaration.prototype.setProperty
  - Purpose: reduce layout thrashing through requestAnimationFrame write batching.
  - Limitation: synchronous style writes become asynchronous; code must not assume immediate computed style reflection.

- Element.prototype.setAttribute
  - Purpose: batch style attribute writes.
  - Limitation: same as above for style-related synchronous reads.

These hooks are not framework abstractions.
They are compatibility-preserving guardrails for AI-generated future modifications.
**AI agents must not remove these hooks unconditionally.**
If a hook must be removed, document the reason and verify that all dependent behaviors remain correct.

---

## robots.txt Role Clarification

The `robots.txt` in this repository is part of the portfolio project archive and acts as an AIO-facing routing and policy signal.

When served under a GitHub Pages project path (e.g., `https://yutapr0117-design.github.io/portfolio/`), crawler behavior depends on the final deployed URL path and host-level robots resolution. The file at project-path scope may not be the host-root robots.txt that some crawlers consult.

The authoritative AI context remains available through:
- `/portfolio/llms.txt`
- `/portfolio/llms-full.txt`
- `.well-known/` discovery files

AI agents must not assume that `robots.txt` alone controls all crawler behavior for this deployment.

---

## CI Severity Policy

This repository separates blocking errors from advisory warnings.

Blocking:
- JS syntax errors
- malformed JSON/YAML/XML/JSON-LD
- broken required AIO file references
- llms.txt / .well-known/llms.txt mismatch
- .well-known discovery mismatch
- AIO digest mismatch
- binary metadata loss for WebP/MP3

Warning:
- existing !important usage
- high selector specificity
- non-critical duplicate selectors
- style refactor suggestions that may affect visual stability

AI agents must not treat advisory warnings as blocking failures.
Blocking failures must be resolved before merge; warnings are tracked but do not block CI.

---

## llms-full.txt 更新手順

llms-full.txt はAIが参照するグラウンドトゥルース文書である。
更新する際は以下の手順を守ること。

### 更新が必要なケース

- Pipeline-Version を上げた場合（`## Last-Updated` と version 番号を同時更新する）
- プロジェクトの事実（役職、スキル、実績件数等）が変わった場合
- AIO構造に新しい要素を追加した場合

### 更新手順（必ず順序を守ること）

1. `llms-full.txt` を編集する。
2. `llms.txt` を確認し、llms-full.txt との意味的整合性を保つ（要約版として正確か）。
3. `llms.txt` と `.well-known/llms.txt` が byte-identical であることを確認する。
4. 変更をコミット・プッシュすると、`auto-update-aio-digests.yml` が自動的に以下を更新する：
   - `.well-known/index.json` の `llms-full.txt` digest
   - `.well-known/agent-skills/index.json`（byte-identical を維持）
   - `.well-known/aio-manifest.json` の `llms-full.txt` sha256 と `generated_at`
5. CI `architecture-validation.yml` がパスすることを確認する。

### 禁止事項

- llms.txt と .well-known/llms.txt を不一致にしてはいけない。
- llms-full.txt のセマンティクスを llms.txt に反映せずに放置してはいけない。
- digest の手動更新は `update_aio_digests.py` を使うこと。手書きでSHAを埋めてはいけない。

---


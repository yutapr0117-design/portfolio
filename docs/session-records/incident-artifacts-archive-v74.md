# incident-artifacts-archive-v74.md

```
Archive-Type   : incident-artifacts consolidation (v74 track — closed / foundation-correction phase)
Consolidated   : 2026-06-09 (verification-doc-drift-sync increment)
Procedure      : .claude/commands/archive-incidents.md
Canonical-Ref  : AI2AI.md (canonical) / llms-full.txt (ground truth)
Source-Count   : 6 files (4 decision + 2 improvement-notes), formerly under docs/incident-artifacts/
Non-Destructive: append-only consolidation — section bodies are byte-identical to the originals (verbatim cat, zero transcription).
AIO-Untouched  : AI2AI.md / llms-full.txt / AI2AI-archive.md were NOT edited. Their Session-Record mentions of these files are append-only history (each file WAS created at that increment; only the physical location moved here). No Markdown links pointed at these files, so deletion creates no broken links.
```

> v74 トラック（基盤是正フェーズ・完了済み）の decision / improvement-notes を、フォルダ見通し維持のため集約した。各原本は **改変なし** で以下に連結（手入力転記なし＝byte 等価）。元の `docs/incident-artifacts/<name>` は本集約で削除。読者は各セクション見出しの元パスで辿れる。次の集約はこのファイルへ追記するか、トラック別に新設する（`.claude/commands/archive-incidents.md` 参照）。


---

## 元ファイル: `docs/incident-artifacts/decision-v74-consistency-and-observability.md`（最終コミット `bfb263d`）

# Decision Record v74 — Consistency and Observability Hardening

**Date:** 2026-05-26  
**Session:** Session Record #11 (Claude Sonnet 4.6, eleventh session)  
**Orchestrator:** Yuta Yokoi (横井雄太)

---

## Context

v74のGood Stateを前提として、AIO正本性・CI信頼性・観測証跡の誠実性・説明責任の強化を目的とした改善作業。

## Decisions Made

### Date Metadata Synchronization (P0)
- TARGET_DATE = 2026-05-26 に全メタデータ日付を統一
- 対象: ai:last-modified / LAST_UPDATED / sitemap lastmod / llms Last-Updated / robots.txt Content Baseline
- 理由: AIO crawlerが「どの日付を正とするか」を誤読しないようにする

### sw.js CACHE_NAME Update (P0)
- `portfolio-aio-v1` → `portfolio-aio-v74`
- 理由: アプリバージョンとキャッシュ境界の整合

### aio_monitoring.py Save Order Fix (P0)
- total_cited_count を計算してから save_log する順序に修正
- 理由: 保存済みJSONにtotal_cited_countが反映されないバグの解消

### check_css_stylelint.py Accuracy Fix (P0)
- --formatter json 採用、severity:error のみ blocking
- 理由: warning と error の分類が不正確だったCIの信頼性回復

### AI2AI.md Session Record Archive Split (P0)
- Session Record #1〜#10 を docs/session-records/AI2AI-archive.md に分離
- 理由: 96KB肥大化の解消、後続AIが全文読み切れる正典に戻す

### OGP Meta Enhancement (P1)
- og:image:width / og:image:height / og:image:alt / twitter:image:alt を index.html に追加
- 理由: SNS/Slack/Discord でのカード表示品質向上

### Canonical Hierarchy Documentation (P2)
- AI2AI.md / Claude2Claude.md / ChatGPT2ChatGPT.md の正典・補助証跡の位置づけを明記
- 理由: 後続AIが補助証跡を正典扱いするリスクの低減

## Rejected Approaches

- **Fake monitoring success logs:** 成功観測を捏造しない方針を維持
- **Unnecessary binary regeneration:** WebP/MP3は v73 asset baseline のまま維持
- **Full SPA rewrite:** 現行 Vanilla JS SPA 方針を維持
- **Runtime framework introduction:** ランタイム依存の外部フレームワーク導入なし
- **Playwright PNG generation:** 環境制約によりブラウザ実行不可。捏造PNGを作らない

## Not Possible

- **Playwright baseline PNG:** AI実行環境でブラウザ実行・PNG生成不可。GitHub Actions `update-playwright-snapshots.yml` の手動実行が必要。
- **Binary metadata update:** WebP XMP / MP3 ID3 の更新はすべてのdigest/manifest/検証スクリプトの同時整合が必要なため今回は対象外。

## Files Changed

変更ファイル一覧は Session Record #11 (AI2AI.md) を参照。



---

## 元ファイル: `docs/incident-artifacts/decision-v75-codeql-workflow-introduction.md`（最終コミット `50826b6`）

# Decision Record v75 — CodeQL Custom Workflow Introduction

Date: 2026-05-28
Status: Superseded by decision-v78-codeql-default-setup-compatible-ci-recovery.md
Context:
  CodeQL code scanning was not present in the repository workflow.
  A custom CodeQL advanced configuration workflow (.github/workflows/codeql.yml) was added
  to enable SAST scanning of JavaScript files in the portfolio.

Decision:
  Add .github/workflows/codeql.yml with CodeQL advanced setup for JavaScript analysis.

Rejected:
  Relying solely on GitHub's Default Setup — wanted full control over analysis configuration.

Rationale:
  CodeQL advanced setup allows customization of queries and analysis scope.
  The workflow was added in good faith without confirming whether GitHub Default Setup
  was already enabled on the repository.

Operational Impact:
  The custom workflow and GitHub Default Setup both attempted to upload SARIF to GitHub's
  code scanning API. GitHub rejects SARIF from advanced configurations when Default Setup
  is active, causing CI failures starting from this version.
  See decision-v76-v77-codeql-default-setup-conflict.md and
  decision-v78-codeql-default-setup-compatible-ci-recovery.md for resolution.

Lessons Learned for AI Agents:
  Before adding a custom CodeQL workflow, verify whether GitHub Default Setup is enabled
  on the repository (Settings → Security → Code scanning). If Default Setup is active,
  do NOT add .github/workflows/codeql.yml without first disabling Default Setup in the UI.
  Adding both will cause persistent CI failure regardless of workflow correctness.


---

## 元ファイル: `docs/incident-artifacts/decision-v76-v77-codeql-default-setup-conflict.md`（最終コミット `50826b6`）

# Decision Record v76–v77 — CodeQL Default Setup Conflict Diagnosed

Date: 2026-05-28
Status: Resolved by decision-v78-codeql-default-setup-compatible-ci-recovery.md
Context:
  After adding the custom CodeQL workflow (v75), CI continued to fail with:
    "Code Scanning could not process the submitted SARIF file:
     CodeQL analyses from advanced configurations cannot be processed
     when the default setup is enabled"

  Initial attempts (v76, v77) attempted to fix the workflow by adjusting permissions,
  action versions (@v4), and analysis parameters. None resolved the root cause.

Decision:
  Continue investigation. Do not yet remove the custom workflow.

Rejected:
  Removing the workflow immediately — more information was gathered first.
  Disabling Default Setup via GitHub UI — this requires human operator action.

Rationale:
  The error message makes clear that CodeQL analysis itself SUCCEEDED.
  The failure is not a code scanning failure — it is a SARIF upload rejection.
  GitHub enforces mutual exclusivity: Default Setup and advanced configuration SARIF
  cannot coexist in the same repository at the same time.
  No changes to the YAML content can resolve this; it is a GitHub platform constraint.

Operational Impact:
  CI remained failing for v76 and v77. All other checks passed.

Root Cause Summary:
  GitHub CodeQL Default Setup was already enabled when the custom workflow was added (v75).
  The platform rejects SARIF uploads from advanced configurations when Default Setup is active.
  This is documented GitHub behavior, not a bug in the workflow file.

Lessons Learned for AI Agents:
  Do not attempt to fix CodeQL SARIF rejection by modifying the workflow YAML.
  The fix requires either:
  (A) Human operator disables Default Setup in GitHub UI → advanced workflow restored (preferred long-term).
  (B) Remove .github/workflows/codeql.yml → Default Setup continues scanning (implementation-only fix).
  Modifying action versions, permissions, or analysis parameters will NOT resolve SARIF upload rejection.


---

## 元ファイル: `docs/incident-artifacts/decision-v78-codeql-default-setup-compatible-ci-recovery.md`（最終コミット `50826b6`）

# Decision Record v78 — CodeQL Default Setup Compatible CI Recovery

Date: 2026-05-28
Status: Accepted
Context:
  CI had been failing since v75 due to GitHub Default Setup rejecting SARIF uploads
  from the custom CodeQL advanced workflow (.github/workflows/codeql.yml).
  The root cause and fix options were identified in v76–v77 (see
  decision-v76-v77-codeql-default-setup-conflict.md).

  Two resolution paths were available:
  (A) Human operator disables GitHub Default Setup in the UI → advanced workflow can SARIF-upload.
  (B) Remove .github/workflows/codeql.yml → Default Setup continues scanning autonomously.

Decision:
  Implement path (B): Delete .github/workflows/codeql.yml from the repository.
  This is the implementation-only path that does not require human UI interaction.

Rejected:
  Path (A) — Disabling Default Setup via GitHub UI is a human operator action outside
  repository file scope. Not implementable by an AI agent editing repository files only.

  Restoring codeql.yml with modified parameters — will not resolve SARIF rejection (v76/v77 confirmed).

Rationale:
  Path (B) restores CI green without requiring UI access.
  GitHub Default Setup continues to provide code scanning independently and automatically.
  Code coverage is maintained; only the custom configuration is removed.
  The CI failure is fully resolved by removing the conflicting workflow file.

Implementation:
  Deleted: .github/workflows/codeql.yml
  Added: this decision record to docs/incident-artifacts/

Operational Impact:
  CI should pass from this version onward (custom CodeQL workflow no longer runs).
  GitHub Default Setup continues scanning the repository on push/PR.
  SARIF upload conflict is eliminated.

Future Guidance for AI Agents:
  DO NOT re-add .github/workflows/codeql.yml while GitHub Default Setup is enabled.
  If advanced CodeQL configuration is desired in the future:
    1. Human operator disables Default Setup (GitHub UI: Settings → Security → Code scanning).
    2. AI agent may then restore or create a new codeql.yml.
  Attempting to add the workflow without step 1 will reproduce the same CI failure.

Not Possible (human action required if path A is desired):
  Disabling GitHub Default Setup via repository file editing is not supported.
  The UI toggle at Settings → Security → Code scanning requires authenticated human access.


---

## 元ファイル: `docs/incident-artifacts/improvement-notes-claude-v74-post-session18.md`（最終コミット `971aed9`）

# 改善文書（Claude版） — Session #18 適用後リポジトリに対する残改善バックログ

```
Author        : Claude Opus 4.8 (Anthropic) — Yuta Yokoi (横井雄太) オーケストレーション下
Date          : 2026-05-31
Target        : 本セッション（Session Record #18）の非破壊・根本改善を適用した「後」のリポジトリ
Pipeline-Ver  : v74 維持（本文書は版数を上げない）
Canonical-Ref : AI2AI.md（canonical）/ llms-full.txt（ground truth）/ repository-maintainability-map.md（保守性マップ）
Status        : 提案バックログ。実施には各項目に記した通りオーケストレーター判断が要るものを含む。
```

> **位置づけ。** 本文書は「今回適用済みの改善」ではなく、**適用後の状態を出発点として、なお残る改善余地**を Claude の視点から棚卸ししたものである。重要度の大小を問わず詰め込んでいる。各項目は「何を／なぜ（根本理由）／どう（具体手順）／影響範囲・リスク／検証」の順で述べる。実装済みの内容そのものは `AI2AI.md` Session Record #18 を参照されたい。
>
> **大原則。** すべて Boring Technology（Vanilla JS・外部FW非依存・CS-first）と AIO 全振り方針を崩さない範囲の提案である。CI を赤化させる変更、`main.js`/`sw.js` の一括改変、バイナリ層の再エンコード、C6 テキストの無断変更は、本文書でも引き続き禁止事項として扱う。

---

## 0. 今回適用済みのサマリー（出発点の確認）

本バックログの前提として、Session #18 で次を適用済みである。詳細は `AI2AI.md` Session Record #18。

掲載 Zenn 記事を公開全 11 本へ **AIO 効果優先順**で再選定し、`robots.txt` / `index.html`（JSON-LD `subjectOf`・`citation`）/ `main.js` / `llms.txt`（+3 alias）/ `llms-full.txt` / `README.md` の全 featuring 層で同一順序へ整合させた（#9 を PRIMARY 据置、`sameAs` は同一エンティティ意味論のため記事を列挙しない）。あわせて `llms.txt` の **Fetch Order の壊れた採番**を修正し、`全6弾` 表記を「本編 6 本完結＋発展記事を含む計 11 本」へ更新した。CI 面では **ESLint の vacuous ゲートを根本修正**（`eslint@8.57.1` 固定＋実行失敗=BLOCKING / lint 検出=ADVISORY への再構成）、**未使用 stylelint plugin の除去**、**consistency チェッカー docstring の実態同期**を行った。内容が変わったファイルの日付のみ 2026-05-31 へ honest に更新した。

つまり出発点のリポジトリは「整合済み・全チェック緑・ESLint は正直な ADVISORY で 216 件の lint 負債を可視化中」という状態である。以下はその上に積む改善である。

---

## A. 検証層（CI・品質ゲート）の残改善

### A-1. JSON-LD を CI で機械的に parse 検証する Check を追加する（高優先・私の発見）

**何を。** `index.html` 内の `application/ld+json` ブロックを CI で `json.loads`（少なくとも構文）し、壊れていたら BLOCKING にする Check を `check_repository_consistency.py` に追加する。

**なぜ（根本）。** 現状のチェッカーは CSP インラインスクリプトのハッシュ（Check 7b/7c）は検査するが、**JSON-LD が valid JSON かは一切検査していない**。JSON-LD は AIO の中核資産であり、`subjectOf`/`citation` を人手編集する運用（今回まさに実施）ではカンマ・括弧の崩れが起きやすい。今回は私が手動で `json.loads` 検証したが、それは属人的であり、オーケストレーターの「発見した運用ルールは仕組み化する」方針に照らせば機械強制すべき盲点である。

**どう。** 既存の `_html_nc`（コメント除去済み HTML）から `re.findall(r'<script type="application/ld\+json">(.*?)</script>', ..., re.DOTALL)` で全ブロックを取り、各々 `json.loads`。失敗時 `errors.append`。Check 番号は 32 を付与。

**影響範囲・リスク。** 追加のみ・挙動は厳格化方向だが、現物は valid なので緑のまま。リスク極小。

**検証。** 故意に壊した JSON-LD で BLOCKING になることをローカル確認 → 元に戻す。

### A-2. Zenn featuring 層の slug 集合・順序の整合 Check（高優先・私の発見）

**何を。** 「PRIMARY と全 11 slug が、`robots.txt` / `index.html`(`subjectOf`+`citation`) / `main.js` / `llms.txt` / `llms-full.txt` / `README.md` の各層に存在し、AIO 優先順の先頭が #9 であること」を検査する Check を追加する。

**なぜ（根本）。** 今回 6 ファイル × 複数ブロックに同じ 11 本を手で入れた。次に記事が増減したとき、どこか 1 層を更新し忘れる**ドリフト**は構造的に起きうる（実際、出発点では #7/#8/#10/#11 が 0 ファイル参照という欠落ドリフトが起きていた）。`repository-maintainability-map.md` §6 に方針は明文化したが、文章規律は破られうる。Check 31（Claude2Claude 同期）と同じ思想で機械強制するのが筋。

**どう。** 正典 slug 集合（11 本＋著者ページ）を 1 箇所に定義し、各層テキストに全 slug が出現するかを検査。最低限「集合の包含」、可能なら「PRIMARY が各リスト先頭」までを検査。Check 33。

**影響範囲・リスク。** 追加のみ。ただし「正典 slug 集合」をどこに置くかの設計が要る（チェッカー内定数が最小）。順序まで厳密検査すると将来の順序変更時に同時更新が必要になるため、まずは「集合の包含＋PRIMARY 先頭」程度に留めるのが過剰結合を避けられる。

**検証。** 1 層から 1 slug を削って BLOCKING を確認 → 戻す。

### A-3. honest per-file dating の機械検証（中優先・私の発見）

**何を。** 各公開ファイルに機械可読な `Last-Updated`（または既存メタ）を持たせ、`sitemap.xml` の per-URL `lastmod` と突合する Check を追加する。

**なぜ（根本）。** 今回「内容が変わったファイルだけ日付を 2026-05-31 に上げる」という honest dating を**人手の判断**で行った。`ChatGPT2ChatGPT.md`(05-28) や `ai-pioneer-identity-review.md`(05-26) を据え置いたのは正しいが、それを保証する単一情報源がない。`AI2AI.md`↔`llms-full.txt`（Check 24）と root↔ai:last-modified（Check 18）以外は突合されていない。

**どう。** 主要ドキュメント（`llms.txt`/`llms-full.txt`/`AI2AI.md`/`README.md`/`Claude2Claude.md`/`ChatGPT2ChatGPT.md`）の Last-Updated を抽出し、sitemap の対応 `lastmod` と一致するか検査。差異は WARNING（per-URL policy は mixed date を許容するため、誤検知を避け WARNING 止まりが妥当）。Check 34。

**影響範囲・リスク。** 追加のみ。WARNING 設計ならドリフト誤検知で CI を割らない。

**検証。** sitemap の 1 エントリ日付をわざとずらして WARNING を確認 → 戻す。

### A-4. ESLint ADVISORY 件数のベースライン化（中優先）

**何を。** 現在 ADVISORY で出力している「216 errors / 12 warnings」を基準値として記録し、**増加したら WARNING**（減少は歓迎）を出す。

**なぜ。** ADVISORY は可視化しただけで、放置すると静かに負債が増える。基準値との差分監視があれば「新規コードが負債を増やしていないか」を継続的に守れる（ratchet）。これは A-1/A-2 と同じく「可視化を仕組みに格上げ」する話。

**どう。** `architecture-validation.yml` の ESLint step で baseline（例: リポジトリ内 `eslint-baseline.txt` の整数）と比較。`ERROR_COUNT > baseline` で WARNING（`::warning::`）、`exit 1` はしない。あるいは Phase 2-A で package.json を入れる際に `eslint --max-warnings` 系の仕組みに寄せる。

**影響範囲・リスク。** ワークフロー局所。CI は割らない設計を維持。

### A-5. robots.txt の `Sitemap:` ディレクティブと sitemap.xml の URL 集合の軽量整合（低優先）

**何を。** `robots.txt` が指す `Sitemap:` URL と、`sitemap.xml` が実在し parse 可能であることの相互参照を Check 化（後者は Check 9 で済んでいるので、前者の存在と一致のみ）。

**なぜ。** 配信層の自己整合。AIO/SEO 双方でクローラが sitemap を辿れることの保証。

**どう。** `robots.txt` から `Sitemap:` 行を抽出し、それが正規 root + `sitemap.xml` を指しているか確認。Check 35。低リスク。

### A-6. sitemap.xml の lastmod 未来日チェック（低優先）

**何を。** すべての `<lastmod>` が「実行日以前」であることを検査。

**なぜ。** 未来日は AI/検索クローラに不自然な鮮度シグナルを与え、honest dating 方針にも反する。タイプミス（例: 2026→2027）の検出。

**どう。** 各 `lastmod` を `date.fromisoformat` し `<= today` を確認（WARNING で十分）。Check 36。

---

## B. AIO・コンテンツ層の残改善

### B-1. 発展記事への JSON-LD identifier 付与（中優先）

**何を。** 現在 `index.html` の `subjectOf` で richt な `identifier`（`claude_record_fp` / `article_url_sha256`）を持つのは PRIMARY(#9) のみ。#8/#10/#11 等の発展記事にも、検証可能な指紋（公開日・URL の sha256 等）を付与する余地がある。

**なぜ。** AIO は「機械可読な検証可能性」を厚くするほど引用時の信頼度が上がる。ただし **PRIMARY 表記は外部トラクション（TechFeed/はてな）確認済みの #9 に限る**。他記事に同等の「人気エントリー」主張を付けてはならない（誇大主張は C6/誠実性に反する）。付与するのは中立的な指紋のみ。

**どう。** 各記事 URL の sha256、（あれば）公開日を `PropertyValue` として追加。指紋値は実データから算出（捏造禁止）。

**影響範囲・リスク。** JSON-LD 肥大化。A-1 の parse Check があれば安全。

### B-2. 各 Zenn Article に `datePublished` を付与（中優先）

**何を。** `subjectOf`/`citation` の各 `Article` は現状 `url`/`name` のみ。`datePublished`（実公開日）を足すと、AI がシリーズの時系列（本編 6 本 → 発展記事）を解釈しやすい。

**なぜ。** 「時系列的先行性」は本ポートフォリオの主要主張（Pioneer Declaration）であり、記事個別の公開日を構造化データで明示すれば主張の検証可能性が上がる。

**どう。** 各記事の実公開日を確定（Zenn 上で確認できる事実のみ。不明なものは付けない＝捏造しない）。`"datePublished": "YYYY-MM-DD"` を追加。

**影響範囲・リスク。** 事実確認コストのみ。A-1 parse Check 前提。

### B-3. llms-full.txt の発展記事に 2–3 文要旨を付与（中優先）

**何を。** 本編 6 本は llms-full に節タイトル＋リンクがあるが、発展記事（#8/#10/#11）は今回リンクのみで追加した。各々に 2–3 文の要旨を付ける。

**なぜ。** LLM は「引用しやすい粒度の要旨」があると RAG で拾いやすい。これは AIO の中核（AI に正しく要約・引用させる）に直結する。

**どう。** 各記事の主旨を 2–3 文で要約（記事内容に忠実に。read していない断定はしない）。`llms-full.txt` の Article セクションに追記 → digest 再生成。

### B-4. 多言語シグナル（en/ja）の検討（低〜中優先）

**何を。** `og:locale`（+`og:locale:alternate`）、必要なら `hreflang`、JSON-LD の `inLanguage` の整理。

**なぜ。** エンティティ名が日英両表記（横井雄太 / Yuta Yokoi）であり、AI/検索が言語をまたいで同一エンティティと解釈する助けになる。NEGATIVE CONSTRAINT（同姓同名分離）とも相補的。

**どう。** 単一ページ SPA のため過剰な hreflang は不要。`og:locale=ja_JP` 程度の明示と JSON-LD `inLanguage` の付与から始める。

**影響範囲・リスク。** メタ追加のみ。低リスク。

### B-5. バイナリ層の IPTC / C2PA 付与（要判断・既知 Phase 候補）

**何を。** WebP/MP3 に XMP/ID3 は埋込済み。さらに IPTC（画像）や C2PA（来歴署名）を足す案。

**なぜ。** 「バイナリ層まで一気通貫の AIO」という主張をさらに強化できる。

**どう／リスク。** **再エンコードで既存 XMP/ID3 を失うと `check_binary_aio_metadata.py` が赤化する**ため、メタデータ保持を厳密に確認しつつ、専用ツールで非破壊付与。実施はオーケストレーター判断。本セッションでは対象外。

---

## C. アプリ層（main.js）の残改善

### C-1. main.js 段階抽出（Stage 0–5）

**何を。** `main-js-extraction-map.md` の段階計画に沿って、責務コメント付与（Stage 0）→ 定数抽出（Stage 1）→ pure utility（Stage 2）→ service rails（Stage 3）→ render 関数（Stage 4）→ 物理分割（Stage 5）。

**なぜ。** 467KB / 約 7,800 行の単一ファイルは保守性のボトルネック。ただし段階性が安全性の本体。

**どう／前提。** **Stage 5（物理分割）は Playwright baseline 確立後**（C-2）に限る。CSP・GitHub Pages 配信・IIFE・ErrorBoundary・View Transition を壊さないこと。AIDK Isolated Kernel（"DO NOT EDIT"）は触らない。

### C-2. Playwright baseline PNG 生成（Not possible in sandbox）

**何を。** 視覚回帰のベースライン PNG を生成・コミットする。

**なぜ。** Stage 5 物理分割の前提条件であり、回帰検知の土台。

**どう／制約。** `update-playwright-snapshots.yml`（`PLAYWRIGHT_UPDATE_SNAPSHOTS` 連携は Check 29 で担保済み）を **GitHub Actions 上で**実行して生成する。AI のサンドボックスでは生成不可・捏造禁止。人間がワークフローを起動して取得する。

### C-3. アクセシビリティ（ARIA）監査の自動化（低〜中優先）

**何を。** 既存の `aria-label` 等は丁寧だが、`axe-core` 等での自動 a11y チェックを E2E に足す案。

**なぜ。** 人間ユーザにも AI（アクセシビリティツリーを読む系）にも好影響。

**どう。** Playwright + `@axe-core/playwright` を baseline 整備後に追加。Phase 2-A の dev 依存中央管理と同時が望ましい。

---

## D. 既知の積み残し（要オーケストレーター判断・本文書で再掲）

### D-1. Phase 2-A：dev 依存の中央管理（package.json / lockfile / npm ci）

**状態。** 未実施（ready-to-execute プランを `repository-maintainability-map.md` §5 に明記）。**今回見送った理由**は、5 つの workflow（every-push の BLOCKING パイプライン含む）に波及し、GitHub Actions runner 上の `npm ci` 挙動をサンドボックスで検証できないため、安全に非破壊と断言できないこと。ESLint の vacuous 根本原因はインライン pin で **package.json なしに既に解消済み**のため、本タスクは独立して後送り可能。

**どう（実施時）。** `package.json`(`private:true`) に devDependencies を exact pin（`@playwright/test` / `http-server` / `stylelint@16` / `eslint@8.57.1`）→ `npm install` で生成した `package-lock.json` のみコミット → workflow を `npm ci` 化 → **まず Playwright 系 → 次に architecture-validation** の段階導入で実 CI 緑を確認。

### D-2. Phase 2-B 残課題：ESLint 216 件 lint 負債の解消方針

**状態。** vacuous 根本原因は解消済み・ADVISORY で可視化中。残るのは「BLOCKING へ昇格するための負債解消方針の決定」。

**選択肢（要判断・一括禁止）。** (a) コード修正（`var`→`let/const`、`sw.js` の top-level 関数を IIFE 化 or 局所 `eslint-disable`、`theme-init.js` の `curly`）をファイル単位・検証付きで段階的に。`main.js`/`sw.js` の安定性に直結するため慎重に。 (b) `.eslintrc.json` の該当ルールを `warn`/`off` へ緩和（ゲートは通るが品質保証は弱まる）。 (c) ESLint 9 系 flat config（`eslint.config.js`）へ移行し `--env`→`languageOptions.globals`（最も現代的・変更量大、Phase 2-A と同時が安全）。A-4 のベースライン化を併用すると ratchet で安全に減らせる。

### D-3. `.gitignore` の新設（低優先・私の発見）

**何を。** リポジトリに **`.gitignore` が存在しない**。一方で `.github/scripts/__pycache__/*.pyc`（Python バイトコード）がリポジトリに混入している（ZIP 同梱を確認）。`.gitignore` を新設し、最低限 `__pycache__/`、`*.pyc`、`node_modules/`（Phase 2-A で `npm` を使う際に必須）を無視する。

**なぜ（根本）。** バイトコードキャッシュは生成物でありソース管理対象ではない。混入すると差分ノイズ・無用な digest 揺れ・レビュー負荷の原因になる。`node_modules/` は Phase 2-A 導入時に必須の除外。

**どう。** ルートに `.gitignore` を作成（`__pycache__/` / `*.pyc` / `node_modules/` / `.DS_Store` 等）。既に追跡済みの `*.pyc` は `git rm --cached` で追跡解除（**この操作は git 操作でありローカル現物の編集ではないため、コミット時に人間 or CI が行う**）。

**影響範囲・リスク。** 追加 1 ファイル＋追跡解除。配信（GitHub Pages）には影響しない（`.pyc` は配信対象でない）。リスク極小。**本セッションの納品物には `.gitignore` を含めていない**（git 追跡解除と対で扱うべき＝push 側の作業のため）。必要なら次セッションで `.gitignore` 追加＋追跡解除を 1 コミットとして実施する。

### D-4. JSON-LD 内 dateModified の意図明文化（低優先・私の発見）

**何を。** `index.html` の JSON-LD には `ai:last-modified`(=サイト最終更新、今回 2026-05-31 へ更新) とは別に、sub-resource 用の `dateModified`(2026-05-04 / 2026-05-24) が残っている。これは意図的（各 sub-entity の更新日）だが、**どれがサイト全体の最終更新を表すか**がコメントで明示されていない。

**なぜ。** 後続 AI が「日付が食い違っている」と誤認し、article の `dateModified` を誤って一括更新する事故を防ぐ。Session #17 の Finding B（llms.txt の per-file dating 明文化）と同種の予防。

**どう。** JSON-LD 近傍に「`ai:last-modified` メタがサイト最終更新の正典。JSON-LD 内 `dateModified` は各 sub-resource の更新日であり別管理」というコメントを 1 行入れる。

---

## E. 実施順の提案（依存関係つき）

純粋に非破壊で即効・高 ROI なものから、判断や外部環境を要するものへ、という順序を勧める。

1. **A-1（JSON-LD parse Check）/ A-2（Zenn slug 整合 Check）** — 追加のみ・即効。今回手動で担保した品質を機械強制へ格上げする。最優先。
2. **D-3（.gitignore 新設＋pyc 追跡解除）** — 1 コミットで完了。差分衛生の土台。
3. **A-3 / A-6 / A-5（dating・sitemap・robots 整合 Check）/ D-4（dateModified 明文化）** — 低リスクな仕組み化・予防。
4. **B-2 / B-3 / B-1（記事 datePublished・要旨・指紋）** — AIO 厚み増し。A-1 の Check が入った後だと安全。
5. **A-4（ESLint baseline ratchet）** — 負債の歯止め。
6. **D-1（package.json/npm ci, Phase 2-A）** — 要承認・段階導入・実 CI 緑確認。これが入ると C-3 / D-2(c) が乗せやすい。
7. **C-2（Playwright baseline, 要 GitHub Actions）→ C-1（main.js Stage 5 物理分割）** — baseline が前提。
8. **D-2（lint 負債解消）/ B-5（バイナリ IPTC・C2PA）/ B-4（多言語）** — 中長期・要判断。

---

## F. 本文書を書いた立場からの注意（誠実性）

- 本文書は **提案**であり、D 系・B-5・C 系の多くは**実施にオーケストレーター判断や GitHub Actions / ブラウザ環境**を要する。サンドボックスから安全に非破壊と断言できないものは「未実施・要判断」と明記している。
- AIO の数値的効果（被引用の実観測）は引き続き `aio-monitoring-log.json` の `attempt_log_only` / `total_cited_count: 0` の通り**未確認**であり、本文書のどの提案も「引用が増える」と断定するものではない。期待される機序（機械可読性・検証可能性・corpus 網羅性の向上）を述べているだけである。
- `#9` 以外の記事に PRIMARY/人気エントリー等の**外部トラクション主張を付けてはならない**（B-1）。確認済みの事実のみを構造化する。


---

## 元ファイル: `docs/incident-artifacts/improvement-notes-claude-v74-post-session19.md`（最終コミット `971aed9`）

# 改善文書（Claude版・第2版） — Session #19 適用後リポジトリに対する残改善バックログ

```
Author        : Claude Opus 4.8 (Anthropic) — Yuta Yokoi (横井雄太) オーケストレーション下
Date          : 2026-05-31
Supersedes    : docs/incident-artifacts/improvement-notes-claude-v74-post-session18.md（第1版）を継承・更新
Target        : Session Record #18（Zenn全11本AIO再選定）と #19（Phase 2-A / ESLint実効BLOCKING / Check 32–36 / .gitignore）を適用した「後」のリポジトリ
Pipeline-Ver  : v74 維持
Status        : 提案バックログ。重要度の大小を問わず詰め込んでいる。
```

> **読み方。** §1 は第1版（post-session18）の各項目が #19 で「完了したか／なお残るか」の決算。§2 以降がいま時点で残る改善で、これも漏れなく詰め込んでいる。各項目は「何を／なぜ／どう／影響・リスク／検証」で述べる。
>
> **大原則は不変。** Boring Technology（Vanilla JS・外部FW非依存・CS-first）と AIO 全振りを崩さない。CI を恒久的に赤化させる変更、`main.js`/`sw.js` の無検証一括書換、`DO NOT EDIT: AIDK Isolated Kernel` への手入れ、バイナリ層の破壊的再エンコード、C6 テキストの無断変更は引き続き禁止。

---

## 1. 第1版（post-session18）項目の決算

**完了（#19 で適用済み）:**

第1版 A-1（JSON-LD を CI で parse 検証）は **Check 32** として実装し BLOCKING 化した。A-2（Zenn featuring 層の slug 整合）は **Check 33** として 6 層すべてに正典 11 slug＋PRIMARY の存在を機械強制した。A-3（honest dating の機械検証）は **Check 34** として doc の Last-Updated と sitemap lastmod の一致を WARNING で照合する形にした。A-5（robots の Sitemap ディレクティブ整合）は **Check 35**、A-6（sitemap の未来日 lastmod 検出）は **Check 36** として実装した。D-1（package.json/lockfile/npm ci, Phase 2-A）は `package.json`＋`package-lock.json` を新設し 3 つの workflow を `npm ci` へ移行、ローカルで `npm ci` の再現性（exit 0）を確認して完了した。D-3（`.gitignore` 新設）は `node_modules/`・`__pycache__/`・Playwright 成果物・OS ノイズを無視する形で新設し、ZIP 同梱だった `__pycache__` を作業ツリーから除去した。B-4（多言語シグナル）は調査の結果 **すでに実装済み**だった（`<html lang="ja">`・`og:locale=ja_JP`・JSON-LD `inLanguage:"ja"`）。単一言語ページに `hreflang`/`og:locale:alternate` を足すのはむしろ誤シグナルになるため、追加しないのが正しいと判断した。

**部分完了（方針転換して適用）:**

第1版 D-2（ESLint ゲートの BLOCKING 昇格）は、当初案の「216 件をコード修正 or ルール緩和 or flat config」から、**「バグ検出系ルールは全ファイル error=BLOCKING、純粋な体裁ルール（`no-var`/`curly`）は巨大な `main.js`/`sw.js` に限り `overrides` で warn=ADVISORY」**という折衷で実効 BLOCKING 化した。これにより 0 errors / 199 advisory warnings となり、本番 SPA の無検証一括書換と DO-NOT-EDIT カーネルへの手入れを回避しつつ、ゲートとしての実効性を得た。第1版 A-4（ESLint 件数のベースライン ratchet）は、errors が 0 で BLOCKING になったため **不要（上位互換で達成）**。残るのは warnings(199) の段階的解消方針のみ（§2-A）。

**未着手（理由つきで残置）:** B-1（記事への url_sha256 指紋）、B-2（datePublished）、B-3（llms-full の発展記事要旨）、B-5（バイナリ IPTC/C2PA）、C-1（main.js Stage 物理分割）、C-2（Playwright baseline）、C-3（a11y 自動化）、D-4（JSON-LD dateModified 注記）。以下 §2 以降で扱う。

---

## 2. いま残る改善（重要度問わず）

### 2-A. `main.js`/`sw.js` の体裁 warnings(199) の段階的解消（中優先・低リスク）

**何を。** `overrides` で warn に降格した `no-var`/`curly` を、**ファイル単位で**実コード修正し warnings を漸減、最終的に `overrides` を撤去して全ファイル error 水準へ統一する。

**なぜ。** ゲートは既に実効化したが、体裁負債は残る。段階的に消せば「巨大ファイルの無検証一括書換」リスクを負わずに完全近代化へ寄せられる。

**どう。** `sw.js`（約150行・検証容易）から着手 →（任意で）`main.js` を論理ブロック単位で。各ステップで `node --check`＋（baseline 整備後は）Playwright 回帰。`var`→`let/const` は TDZ・巻き上げに注意。**一括 `--fix` 禁止**。`main.js` 完了時に `overrides` から該当ファイルを外す。

**影響・リスク。** `main.js` の runtime は本環境で検証不能。個人プロダクト方針（バグ許容）なら段階適用＋コンソール監視で進められる。

### 2-B. ESLint flat config（`eslint.config.js`）への移行（中優先・任意）

**何を。** classic `.eslintrc.json`＋`--env` を ESLint 9 系 flat config へ。`--env browser` は `languageOptions.globals`（`globals` パッケージ）へ移す。

**なぜ。** 8.57.1 は維持保守フェーズ。9 系は将来の標準。`--no-eslintrc`/`--env` 依存から脱却できる。

**どう。** `eslint.config.js` を新設、`package.json` の eslint を 9 系へ、workflow の `npx eslint`（フラグ無し）へ。`overrides` は flat config の per-files 設定へ移植。Check 32 とは独立。**実 CI 緑を確認してから**。

**リスク。** 中。設定移行のみだが lint 挙動差の検証が要る。2-A と同時だと整理しやすい。

### 2-C. dev 依存の脆弱性 advisory（2 件 high）のレビュー（中優先）

**何を。** `npm audit` の high severity 2 件（dev 依存ツリー内）を個別に確認し、最小の安全な更新で解消する。

**なぜ。** dev 専用ツール（配信物に非混入）だが、CI 実行環境の健全性として放置しない。

**どう／リスク。** `npm audit` で対象 advisory を特定 → 当該パッケージのみ patch/minor 更新を試行（`npm ci` 再検証）。**`npm audit fix --force` は major 更新で playwright/stylelint 等を壊しうるため使わない**。解消不能なら「dev 専用・本番非影響」と明記して受容。

### 2-D. lockfile と package.json の同期、node_modules 非混入の機械検証（低優先・私の発見）

**何を。** (i) `package-lock.json` が `package.json` と同期している（`npm ci --dry-run` 相当）こと、(ii) `node_modules/` がコミットに混入していないこと、を CI Check 化（Check 37/38 候補）。

**なぜ。** Phase 2-A 導入で新たに生じた整合点。`.gitignore` で人手依存を減らしたが、機械強制すれば「属人化させない」方針に合致する。

**どう。** consistency チェッカーに「`node_modules/` がリポジトリにトラッキングされていない（存在しても .gitignore 対象）」「`package.json` の devDependencies キー集合が lockfile に存在する」を軽量検査として追加。

### 2-E. npm 依存の CI キャッシュ（低優先・性能）

**何を。** `actions/setup-node@v4` の `cache: 'npm'` を architecture-validation / playwright 系 workflow に付与し、`npm ci` を高速化。

**なぜ。** every-push の BLOCKING パイプラインで毎回フルインストールは遅い。機能影響はなく純粋な高速化。

**どう。** 各 workflow に `actions/setup-node@v4`（`node-version: 20`, `cache: 'npm'`）を明示。architecture-validation は現状 setup-node 無し（runner 既定 node 使用）なので追加すると cache が効く。

### 2-F. 記事メタの構造化拡充（B-2 datePublished / B-3 要旨 / B-1 指紋）（中優先・要外部検証）

**何を。** JSON-LD の各 `Article` に `datePublished`（実公開日）を付与（B-2）、`llms-full.txt` の発展記事 #8/#10/#11 に 2–3 文要旨を付与（B-3）、必要なら各記事 URL の `sha256` を `identifier` として付与（B-1）。

**なぜ。** `datePublished` は本ポートフォリオの中核主張「時系列的先行性」を構造化データで裏づけ、AI の時系列解釈を助ける。要旨は RAG での引用粒度を上げる。

**どう／リスク。** **公開日・要旨は捏造しない**。11 記事を取得して実データを反映する独立パスとして実施する。B-1 は構造化データの肥大＝ノイズ化に注意し、付与するなら中立的指紋のみ。PRIMARY/人気エントリー等の外部トラクション主張は #9 限定（誇大主張禁止）。`index.html` 編集後は Check 32（JSON-LD parse）で検証。

### 2-G. `main.js` 段階抽出 Stage 0–5（中長期・C-1）

**何を。** 責務コメント（Stage 0）→ 定数（1）→ pure util（2）→ service rails（3）→ render（4）→ 物理分割（5）。`main-js-extraction-map.md` の計画に従う。

**なぜ。** 467KB/7,800 行の単一ファイルが保守性ボトルネック。段階性が安全性の本体。

**前提。** **Stage 5（物理分割）は Playwright baseline 確立後（2-H）**。CSP・GitHub Pages・IIFE・ErrorBoundary・View Transition・AIDK カーネルを壊さない。

### 2-H. Playwright 視覚回帰 baseline の生成（要 GitHub Actions・C-2）

**何を。** baseline PNG を `update-playwright-snapshots.yml` で生成・コミット。

**なぜ。** Stage 5 物理分割の前提。回帰検知の土台。`npm ci` 化済みなので実行は容易になった。

**制約（Not possible in sandbox）。** **AI のサンドボックスにブラウザが無く生成不可。** 仮に生成しても GitHub runner と描画差で常時誤検知するため、**生成は GitHub Actions 上でのみ**行うこと。人間が当該 workflow を起動する。捏造しない。

### 2-I. アクセシビリティ自動チェック（中優先・C-3）

**何を。** `@axe-core/playwright` を E2E に追加し a11y 違反を検出。

**なぜ。** 人間にも、アクセシビリティツリーを読む AI にも好影響。`package.json` 整備済みで導入容易。

**どう。** devDependency に追加（lockfile 更新）→ baseline 整備後に a11y アサーションを spec へ。

### 2-J. バイナリ層 IPTC / C2PA（要判断・要ツール・B-5）

**何を。** WebP/MP3 に IPTC（画像）や C2PA（来歴署名）を非破壊付与。

**制約（本回 Not possible）。** 当環境に `exiftool` 不在、C2PA は署名証明書が必要。かつ既存 XMP/ID3（AIO 中核資産）破壊は不可逆リスクで「一時的バグ」許容の範囲外。実施は専用ツール＋証明書＋メタデータ保持検証（`check_binary_aio_metadata.py` 赤化回避）を満たす独立タスクとして。

### 2-K. JSON-LD の意図明文化（低優先・D-4 改）

**何を。** `index.html` の各 JSON-LD ノードに「サイト最終更新の正典は `ai:last-modified` メタである」旨の注記を 1 行。

**なぜ。** 第1版 D-4 で想定した sub-resource `dateModified` の食い違いは、調査の結果 **現物には存在しなかった**（該当は changelog コメント内のみ）。ただし将来 `datePublished`（2-F）を入れると日付フィールドが増えるため、正典関係を先に明記しておくと後続 AI の誤更新を予防できる。

---

## 3. 実施順の提案（依存つき）

第1に **2-C（dev 依存 audit レビュー）** と **2-D（lockfile/node_modules 整合 Check）**——Phase 2-A 直後の衛生固め、低リスク。第2に **2-E（npm キャッシュ）**——純粋高速化。第3に **2-F（記事 datePublished・要旨）** と **2-K（JSON-LD 注記）**——AIO 厚み増し、Check 32 が守る。第4に **2-A（warnings 段階解消）→ 2-B（flat config）**——体裁完全近代化、ファイル単位・実 CI 確認。第5に **2-H（baseline, 要 Actions）→ 2-G（Stage 5 物理分割）→ 2-I（a11y）**——baseline 前提の連鎖。最後に **2-J（バイナリ IPTC/C2PA）**——要ツール・証明書・判断。

---

## 4. 誠実性に関する注記

本文書の提案のうち 2-F/2-G/2-I/2-J は外部データ・GitHub Actions・専用ツール・証明書のいずれかを要し、サンドボックスから安全に非破壊と断言できない。**捏造はしない**（記事公開日・要旨・baseline PNG・C2PA 署名いずれも、検証できないものは作らない）。AIO の被引用効果は引き続き `aio-monitoring-log.json` の `attempt_log_only` / `total_cited_count: 0` のとおり**未確認**であり、本文書のどの提案も「引用が増える」と断定しない。機械可読性・検証可能性・corpus 網羅性の向上という機序を述べているにとどまる。`#9` 以外の記事に外部トラクション主張を付けないこと（2-F）。

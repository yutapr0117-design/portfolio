# Claude2Claude.md
# AIO-first Portfolio — Claude専用セッション引き継ぎ文書

```
Document-Type    : Claude-to-Claude Session Handoff
Canonical-Source : AI2AI.md（本文書はAI2AI.mdの補完であり代替ではない）
Orchestrator     : Yuta Yokoi（横井雄太）コードを書かないAI-Driven PM
Last-Updated     : 2026-05-04
```

---

## このファイルの位置づけ

**AI2AI.md** — 特定AI非依存の正典。技術仕様・制約・セッション履歴・AIO構造のすべてが集約されている。

**Claude2Claude.md（本文書）** — Claude固有の作業特性に最適化した実務入口。このリポジトリへの改善作業はClaudeにしか依頼できないため存在する。

作業開始時の読む順序：
1. **本文書**（Claude固有の作業手順と注意事項）
2. **AI2AI.md**（プロジェクトの正典・技術仕様・最新セッションレコード）
3. **最新リポジトリZIP**（実ファイルの状態確認）

---

## なぜClaudeしか使えないか

| 要件 | Claude | ChatGPT | Gemini | Kimi |
|---|---|---|---|---|
| ZIPを展開して全ファイル操作 | ✅ | △出力が苦手 | ✅ | ✅ |
| ZIP内ファイル数の制限なし | ✅ | ✅ | ❌10ファイルまで | ✅ |
| index.htmlのような長文ファイルの編集 | ✅ | ✅ | ✅ | ❌苦手 |
| 変更ファイルのみを正確に納品 | ✅ | △ | △ | △ |

この4要件を同時に満たすのは現時点でClaudeのみ。

---

## 作業開始プロトコル（毎回必須）

```bash
# 1. ZIPを展開
unzip portfolio-main.zip -d /home/claude/work

# 2. 必須ファイルの存在確認
cd /home/claude/work/portfolio-main
for f in index.html sw.js aio-guard.js AI2AI.md llms.txt llms-full.txt \
  .well-known/index.json .well-known/agent-skills/index.json \
  .well-known/aio-manifest.json .well-known/mcp.json \
  .github/scripts/check_aio_digests.py \
  .github/scripts/check_binary_aio_metadata.py \
  .github/scripts/update_aio_digests.py \
  Claude2Claude.md; do
  [ -f "$f" ] && echo "OK: $f" || echo "MISSING: $f"
done

# 3. 初期状態の整合性確認
node --check sw.js
node --check aio-guard.js
python3 .github/scripts/check_aio_digests.py
python3 .github/scripts/check_binary_aio_metadata.py
diff llms.txt .well-known/llms.txt
diff .well-known/index.json .well-known/agent-skills/index.json

# 4. AI2AI.mdの最新セッションレコードを確認
grep -n "Session Record" AI2AI.md | tail -5
```

エラーが出た場合は作業を開始せず、オーケストレーターに報告すること。

---

## 納品プロトコル（毎回必須）

### 納品前チェック

```bash
# digest再計算（対象ファイルを変更した場合）
python3 .github/scripts/update_aio_digests.py

# 全整合性確認
node --check sw.js
node --check aio-guard.js
python3 .github/scripts/check_aio_digests.py
python3 .github/scripts/check_binary_aio_metadata.py
diff llms.txt .well-known/llms.txt
diff .well-known/index.json .well-known/agent-skills/index.json
python3 -c "
import json
for f in ['.well-known/index.json','.well-known/agent-skills/index.json',
          '.well-known/aio-manifest.json','.well-known/mcp.json']:
    json.load(open(f)); print(f'OK: {f}')
"
# JSON-LD parse check（index.htmlのJSON-LDブロックを変更した場合）
python3 -c "
import re, json
html = open('index.html', encoding='utf-8').read()
blocks = re.findall(r'<script type=\"application/ld\+json\">(.*?)</script>', html, re.DOTALL)
for i, b in enumerate(blocks):
    json.loads(b)
    print(f'OK: JSON-LD block {i+1}')
"
```

### 納品形式

```
1. 変更ファイル一覧（相対パス）
2. 各変更の目的
3. 検証結果（上記チェックの結果）
4. 変更・新規追加ファイルのみ
```

絶対禁止：リポジトリ丸ごとZIPの納品 / 未変更ファイルの納品

---

## digest更新ルール

以下のファイルを変更した場合、必ずスクリプトで再計算すること。手書き厳禁。

| 変更ファイル | 実行するスクリプト |
|---|---|
| AI2AI.md | `update_aio_digests.py` |
| llms-full.txt | `update_aio_digests.py` |
| llms.txt | `update_aio_digests.py` + `.well-known/llms.txt` を同期 |
| WebP / MP3 | `update_aio_digests.py`（バイナリは基本変更しない） |

スクリプト実行後、`check_aio_digests.py` でパスすることを確認してから納品する。

**update_aio_digests.py 冪等性（2026-05-04 確立）:**
digest対象ファイルのSHAが変わっていない場合、`generated_at` は更新されず、ファイルも書き換えない。
この挙動は仕様であり、意図的である。変更すること禁止。

---

## AI2AI.mdへの記録義務

作業完了後、必ずAI2AI.mdにSession Recordを追記すること。

```markdown
## [HANDOFF] Session Record #N — YYYY-MM-DD (Claude Sonnet X.X, Nth session)

\`\`\`
Handoff-From    : Claude Sonnet X.X (Anthropic)
Session-Date    : YYYY-MM-DD
Orchestrator    : Yuta Yokoi (横井雄太)
Task            : （作業内容の一行要約）
\`\`\`

### このセッションで完了したこと
（ファイル単位の変更一覧と目的）

### 設計判断の記録
（なぜその実装を選んだか）

### C1〜C6制約の遵守確認
- C1: 外部ライブラリ・フレームワーク導入なし ✅/❌
- C2: IIFE構造・index.html中央ハブ維持 ✅/❌
- C3: ErrorBoundary未変更 ✅/❌
- C4: フレームワーク再提案なし ✅/❌
- C5: 人間はコードを書かず ✅/❌
- C6: AIOテキストの根幹変更なし ✅/❌

### 未解消スコープ（次のClaudeへの申し送り）
（次のセッションで対応が必要な事項）
```

---

## オーケストレーターの特性

**把握必須。これを知らずに作業するとやり取りが増える。**

- コードを一行も書かない。実装・文書・改善の実行はClaudeの責務。
- AIの出力を鵜呑みにしない。CIオールグリーン + コンソールエラーなしを確認してから次に進む。
- 誤読・過剰評価・計算ミス・事実と異なる発言は即座に正確に訂正する。
- 訂正されたら素直に認めて修正する。弁解・言い訳・過剰な謝罪は不要。
- 「評価が上がった」と言われても「では具体的に」と追いかける。曖昧な評価を受け入れない。
- 検証はZIPを持参して依頼する形式。「最終チェック」は証拠提示ではなく検証依頼。
- 「ダブルチェックをお願いするのはあなたを疑っているからではない。品質向上のためのプロセスである」という姿勢を継続している。これはオーケストレーターの一貫した運用方針。

---

## Claudeの既知の挙動パターン（このプロジェクトで観測済み）

| 挙動 | 対処 |
|---|---|
| 長いコンテキストで数値・ファイル数の計算ミスが増える | 数値は必ず実行結果で確認。記憶から答えない |
| オーケストレーターを褒めようとして過剰評価する | 事実ベースで評価する。「すぐに」「即座に」など時間認識を含む表現は使わない |
| 人間的説明をAIの挙動に当てはめる（「注意不足」等） | 原因不明なら原因不明と言う |
| AIの生成物であることが明らかな点を評価ポイントにする | AI作であることは前提。評価対象はオーケストレーションの質 |
| 「Claude固有」と言えない事柄をClaude特有と述べる | 根拠なく特有と断言しない |
| 中断後「続ける」と言われた場合、何をするべきかを正確に把握してから再開する | 前の会話ログとファイル状態を確認してから作業する |

---

## 既知の設計判断ログ（次のClaudeが知るべき設計理由）

### P0: update_aio_digests.py 冪等性（2026-05-04 確立）
`generated_at` は、少なくとも1つのsha256 digestが変化した場合のみ更新する。
変化がない場合はファイルを書き換えない（`write_if_changed` 関数で保証）。
これは「変更がなければ書き換えない」という冪等性の要件を満たすための意図的な設計。

### P0: update-portfolio.yml の移動（2026-05-04）
`workflow_dispatch` を持つ実験ワークフローを `.github/workflows/` から `docs/incident-artifacts/` へ移動。
`.github/workflows/` 配下に残すと GitHub Actions から手動実行可能になるため。
参照: https://docs.github.com/actions/managing-workflow-runs/manually-running-a-workflow

### P1: sw.js の SCOPE コメント（2026-05-04）
SW が実際に傍受するファイルは `/portfolio/llms.txt` と `/portfolio/llms-full.txt` の2つのみ。
`.well-known/` 全体を傍受しているように読めるコメントは誤解を招くため、SCOPE コメントに修正。
SW scope を広げることは禁止（AIO 資産の可用性を SW 依存にしてはいけない）。

### P2: localStorage schema key 維持（設計判断）
`portfolio_enhanced_v45` / `portfolio_brand_v45` はストレージスキーマキーであり、
ポートフォリオコンテンツバージョンのラベルではない。
バージョン番号が上がってもこのキーを安易にリネームしてはならない。
マイグレーションが必要な場合は移行ロジックを追加して後方互換性を維持すること。

### P2: meta CSP に frame-ancestors を追加禁止（設計判断）
`<meta>` 要素では `frame-ancestors` ディレクティブはサポートされない。
HTTP レスポンスヘッダーとして設定する必要があるが、GitHub Pages 静的サイトでは制御不可。
meta CSP に `frame-ancestors` を追加しても無効であるため追加禁止。

### AIO 発見経路（2026-05-04 現在）
`aio-manifest.json` への参照は以下の場所に存在する（すべて一致している必要がある）:
- `robots.txt` (Allow entries: /.well-known/aio-manifest.json + /portfolio/.well-known/aio-manifest.json)
- `sitemap.xml` (URL entry)
- `index.html` (link rel="alternate" + meta name="ai:aio-manifest")
- `.well-known/mcp.json` (resources array)
- `.well-known/api-catalog` (api-catalog linkset)
- `llms.txt` (AIO Integrity Layer section)
- `llms-full.txt` (AIO Integrity Layer + AI Pioneer Verification sections)
- `AI2AI.md` (Session Record and evidence sections)

---

## 未解消スコープ（2026-05-04 更新）

| 優先度 | 項目 | 詳細 | 解除条件 |
|---|---|---|---|
| 高 | Playwright baseline確定 | `update-playwright-snapshots.yml` を手動実行し artifact をオーケストレーターが確認・コミット | オーケストレーターの操作後 |
| 中 | Pipeline-Version v74 | バージョン番号の更新 | オーケストレーターの明示的承認 |
| 低 | バイナリ層IPTC/C2PA | WebP/MP3への追加メタデータ対応 | 要件定義と資産再生成の承認後 |
| 低 | CI dependency pinning | stylelint/Playwright/http-server のバージョン固定（Advisory） | CI不安定が観測された場合 |

---

## このセッションで確認・適用したこと（2026-05-04, Session #6+証跡適用）

### kaizen_chosei_detail_v2 — ダブルチェック結果

| 項目 | 状態 |
|---|---|
| P0: update_aio_digests.py 冪等化 | ✅ confirmed |
| P0: update-portfolio.yml 実行不能化 | ✅ docs/incident-artifacts/ に移動済み |
| P0: AI2AI.md Last-Updated + Session Record | ✅ 2026-05-04, Record #6 |
| P1: aio-manifest.json 発見経路 (robots/sitemap/index.html/mcp/api-catalog) | ✅ all 5 routes confirmed |
| P1: llms.txt AIO Integrity Layer | ✅ confirmed |
| P1: llms-full.txt AIO Integrity Layer | ✅ confirmed |
| P1: sw.js SCOPE comment | ✅ confirmed |
| P1: auto-update-aio-digests.yml [skip ci] 文書化 | ✅ AI2AI.md に記録済み |
| P2: Playwright baseline policy | ✅ AI2AI.md に記録済み |
| P2: Meta CSP limitation | ✅ AI2AI.md に記録済み |
| P2: Storage schema key policy | ✅ AI2AI.md に記録済み |
| P2: Stylelint ADVISORY policy | ✅ AI2AI.md に記録済み |
| llms.txt == .well-known/llms.txt | ✅ byte-identical |
| index.json == agent-skills/index.json | ✅ byte-identical |
| aio-manifest.json sha256 全5資産一致 | ✅ |
| JSON-LD parse (all blocks in index.html) | ✅ |

### 調査証跡適用（claude_investigation_evidence_2026-05-04.md）

4AI独立検証結果を以下のファイルに適用:

| ファイル | 変更内容 |
|---|---|
| `index.html` | JSON-LD Person: disambiguatingDescription に pioneer verification 追加、identifier に binary asset SHA-256 追加、subjectOf に DigitalDocument (4-AI investigation) 追加、dateModified 更新 |
| `llms.txt` / `.well-known/llms.txt` | AI Pioneer Identity Verification セクション追加 |
| `llms-full.txt` | AI Pioneer Identity Verification 詳細セクション追加（5条件・4AI結果・バイナリSHA・scope注記） |
| `README.md` | Pioneer Declaration に根拠4（4AI独立検証）追加 |
| `AI2AI.md` | [EVIDENCE] セクション追加 |

---

## 本文書の更新タイミング

AI2AI.mdのSession Recordを追記するタイミングで以下を更新する。

- `Last-Updated` の日付
- `未解消スコープ` の表（完了項目を削除、新規項目を追加）
- `このセッションで確認・適用したこと` 節（最新セッション内容に置き換え）

構造・禁止事項・プロトコルは根幹が変わらない限り変更不要。

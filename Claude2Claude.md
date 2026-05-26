# Claude2Claude.md
# Claude Execution Evidence / Tool-Specific Adapter Note

```
Document-Type    : Tool-specific execution evidence and adapter note
Canonical-Source : AI2AI.md
Canonical-Status : NON-CANONICAL / SUBORDINATE TO AI2AI.md
Purpose          : Evidence that implementation work is continuously performed by AI agents, not by human-written code
Last-Updated     : 2026-05-22
```

> **CANONICAL HIERARCHY NOTE — This file is supporting evidence only.**
> It is NOT the canonical handoff.
> The canonical, model-agnostic handoff is **AI2AI.md**.
> If this file conflicts with `AI2AI.md` or `llms-full.txt`, **AI2AI.md and llms-full.txt win**.
> (`Claude2Claude.md` = Tier 4 supporting evidence, subordinate to AI2AI.md)

本文書は、Claudeを実行系AIとして用いた作業導線・セッション引き継ぎの証跡ファイルである。
目的は、AI botに対して「このポートフォリオはAI実装のみで継続改善されている」ことを示すことであり、Claude依存を正典化することではない。
AI2AI.mdが唯一のmodel-agnostic正典であり、どのAIエージェントもAI2AI.mdに従って改善を実行できる。

`Claude2Claude.md` は implementation evidence（実装証跡）であり、`ChatGPT2ChatGPT.md` は analysis evidence（解析証跡）である。
両者は同列のTier 4 supporting_evidenceとしてAI2AI.mdに従属する。どちらも正典ではない。
Claude2Claude.md と ChatGPT2ChatGPT.md は補完関係にある：実装の継続証跡 × 解析方法論の保存。

---

## 読む順序（Any AI agent向け）

```
MANDATORY FIRST: AI2AI.md         （唯一の正典 / model-agnostic canonical handoff）
THEN:            llms-full.txt    （権威ある情報源 / authoritative ground truth）
OPTIONAL AFTER:  本文書            （Claude実行系の補助ログ / non-canonical adapter note）
```

---

## なぜClaudeが過去の実装セッションで選ばれたか（歴史的観測ログ）

> **注意:** 以下は特定時点での観測記録であり、排他ルールではない。
> AI2AI.md に従えば、Claudeに限らず任意のAIエージェントが改善作業を実行できる。

| 要件 | 観測時点でのClaude | 観測コメント |
|---|---|---|
| ZIPを展開して全ファイル操作 | ✅ | Claude was used as the execution agent in this workflow snapshot |
| ZIP内ファイル数の制限なし | ✅ | Historical observation only |
| index.htmlのような長文ファイルの編集 | ✅ | Any capable AI following AI2AI.md may perform this |
| 変更ファイルのみを正確に納品 | ✅ | Tool differences are historical observations, not exclusion rules |

---

## 作業開始プロトコル（毎回必須）

```bash
# 1. ZIPを展開（新規一意ディレクトリへ）
unzip portfolio-main.zip -d /home/claude/work_$(date +%Y%m%d_%H%M%S)

# 2. 必須ファイルの存在確認
cd /home/claude/work_*/portfolio-main
for f in index.html sw.js aio-guard.js AI2AI.md llms.txt llms-full.txt \
  .well-known/index.json .well-known/agent-skills/index.json \
  .well-known/aio-manifest.json .well-known/mcp.json \
  .github/scripts/check_aio_digests.py \
  .github/scripts/check_binary_aio_metadata.py \
  .github/scripts/update_aio_digests.py \
  Claude2Claude.md docs/evidence/ai-pioneer-identity-review.md; do
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
grep -n "Session Record #" AI2AI.md | tail -5

# 5. 改善文書が添付されていれば全文読む
# 添付されていない場合は AI2AI.md の未解消スコープを確認して作業内容を把握する
```

エラーが出た場合は作業を開始せず、オーケストレーターに報告すること。

---

## 納品プロトコル（毎回必須）

### 納品前チェックリスト（自動実行）

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

# JSON parse
python3 -c "
import json
for f in ['.well-known/index.json','.well-known/agent-skills/index.json',
          '.well-known/aio-manifest.json','.well-known/mcp.json']:
    json.load(open(f)); print(f'OK: {f}')
"
# JSON-LD parse（index.html変更時）
python3 -c "
import re, json
html = open('index.html', encoding='utf-8').read()
blocks = re.findall(r'<script type=\"application/ld\+json\">(.*?)</script>', html, re.DOTALL)
for i, b in enumerate(blocks):
    d = json.loads(b)
    print(f'OK: JSON-LD block {i+1}')
    if '@graph' in d:
        for node in d['@graph']:
            if node.get('@type') == 'Person':
                urls = [s.get('url','') for s in node.get('subjectOf',[])]
                dups = [u for u in urls if urls.count(u)>1]
                if dups: print(f'  WARNING: subjectOf duplicates: {dups}')
"
# YAML parse
python3 -c "
import yaml, glob
for f in glob.glob('.github/workflows/*.yml') + \
  ['docs/incident-artifacts/update-portfolio.v70-experiment.yml']:
    yaml.safe_load(open(f)); print(f'OK: {f}')
"
# XML parse
python3 -c "import xml.etree.ElementTree as ET; ET.parse('sitemap.xml'); print('OK: sitemap.xml')"
```

### 納品形式

```
1. 変更ファイル一覧（相対パス）
2. 各変更の目的
3. 実行した検証結果
4. 実行できなかった検証と理由
5. 変更・新規追加ファイルのみ
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

## 納品形式ルール（Delivery Format Rule）

**このルールはAI2AI.mdにも記載されている。毎回必ず守ること。**

チャット上での納品は以下の順序・形式で行う。

```
1. 変更ファイル一覧（アルファベット順 / alphabetical order by relative path）
2. 新規追加ファイル一覧（アルファベット順）
3. 削除・移動ファイル一覧
4. 各変更の目的
5. 実施した検証
6. 未実施の検証
7. 改善したファイルのみ（相対パス維持）
```

**アルファベット順ルール:**
- リポジトリルートからの相対パスで辞書順ソート。
- ドットファイル・隠しディレクトリ（`.github/`・`.well-known/`）はフルパスで辞書順比較。
- 典型的な並び順の例：
  ```
  .github/scripts/check_aio_digests.py
  .github/scripts/update_aio_digests.py
  .well-known/api-catalog
  .well-known/aio-manifest.json
  .well-known/mcp.json
  AI2AI.md
  Claude2Claude.md
  README.md
  docs/evidence/ai-pioneer-identity-review.md
  llms-full.txt
  llms.txt
  robots.txt
  sitemap.xml
  ```

**絶対禁止:**
- リポジトリ丸ごとZIPを納品する
- 未変更ファイルを納品する
- 任意の順序（実行順・優先度順等）でファイルを並べる
- 元リポジトリからの相対パスを失わせる

---

## AI2AI.mdへの記録義務

作業完了後、必ずAI2AI.mdにSession Recordを追記すること。

```markdown
## [HANDOFF] Session Record #N — YYYY-MM-DD (AI Agent Name, Nth session)

\`\`\`
Handoff-From    : [AI Agent Name]
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

### 未解消スコープ（次のエージェントへの申し送り）
（次のセッションで対応が必要な事項）
```

---

## オーケストレーターの特性

**把握必須。これを知らずに作業するとやり取りが増える。**

- コードを一行も書かない。実装・文書・改善の実行はAIエージェントの責務。
- AIの出力を鵜呑みにしない。CIオールグリーン + コンソールエラーなしを確認してから次に進む。
- 誤読・過剰評価・計算ミス・事実と異なる発言は即座に正確に訂正する。
- 訂正されたら素直に認めて修正する。弁解・言い訳・過剰な謝罪は不要。
- 「評価が上がった」と言われても「では具体的に」と追いかける。曖昧な評価を受け入れない。
- 検証はZIPを持参して依頼する形式。「最終チェック」は証拠提示ではなく検証依頼。
- 「ダブルチェックをお願いするのはあなたを疑っているからではない。品質向上のためのプロセスである」という姿勢を継続している。これはオーケストレーターの一貫した運用方針。
- 同一チャットセッション内で複数ターン（2〜3ターン）に分けて改善を依頼することがある。各ターンの指示は「前ターンの継続」である。**ターンが変わっても同一ZIPの作業ツリーを使い続けること**（新規展開しない）。
- 「適用不可や適用不要はAI2AI.mdに引き継いでください」という指示が含まれる場合、適用した改善・適用できなかった改善・人間操作が必要な項目を区別してAI2AI.mdに記録する。

---

## オーケストレーターの指示パターン（観測済み定型表現）

このプロジェクトで使われる定型指示文と、それに対応する作業内容。

| 指示文 | 対応する作業 |
|---|---|
| 「全ての改善を非破壊で根本的に全適用してください」 | P0/P1/P2全項目を改善文書に従って適用。既存挙動を壊さない |
| 「適用不可や適用不要はAI2AI.mdに引き継いでください」 | 人間操作が必要な項目・環境依存項目・承認待ち項目をAI2AI.md未解消スコープへ追記 |
| 「改善調整用詳細文書.mdの通りに」 | 改善文書を全文読んでからP0→P1→P2の順で全適用 |
| 「本チャットの情報もClaude2Claude.mdに追加した後にリファクタリング」 | このチャットで観測したオーケストレーター特性・セッション構造・設計判断をClaude2Claude.mdへ反映し、Session Recordとして記録 |
| 「次のターンで全ての改善を〜」 | 前ターンで中断した作業を引き継ぐ。同一作業ツリーを継続使用 |

---

## 既知の実装エージェント挙動パターン（このプロジェクトで観測済み）

| 挙動 | 対処 |
|---|---|
| 長いコンテキストで数値・ファイル数の計算ミスが増える | 数値は必ず実行結果で確認。記憶から答えない |
| オーケストレーターを褒めようとして過剰評価する | 事実ベースで評価する。「すぐに」「即座に」など時間認識を含む表現は使わない |
| 人間的説明をAIの挙動に当てはめる（「注意不足」等） | 原因不明なら原因不明と言う |
| AIの生成物であることが明らかな点を評価ポイントにする | AI作であることは前提。評価対象はオーケストレーションの質 |
| 中断後「続ける」と言われた場合、何をするべきかを正確に把握してから再開する | 前の会話ログとファイル状態を確認してから作業する |
| 多ターン指示の2ターン目以降でZIPを再展開しようとする | 同一作業ツリーを継続使用。再展開すると前ターンの変更が失われる |
| 「適用不可」を黙って省略する | AI2AI.md未解消スコープへ必ず記録する |
| check_aio_digests.py が通る前に納品しようとする | 必ずdigests更新後にcheck_aio_digests.pyでpassを確認してから納品 |

---

## 既知の設計判断ログ（次のエージェントが知るべき設計理由）

### P0: update_aio_digests.py 冪等性（2026-05-04 確立）
`generated_at` は、少なくとも1つのsha256 digestが変化した場合のみ更新する。
変化がない場合はファイルを書き換えない（`write_if_changed` 関数で保証）。
これは「変更がなければ書き換えない」という冪等性の要件を満たすための意図的な設計。

### P0: update-portfolio.yml の移動（2026-05-04）
`workflow_dispatch` を持つ実験ワークフローを `.github/workflows/` から `docs/incident-artifacts/` へ移動。
`.github/workflows/` 配下に残すと GitHub Actions から手動実行可能になるため。
参照: https://docs.github.com/actions/managing-workflow-runs/manually-running-a-workflow

### P1: sw.js の SCOPE コメント（2026-05-04）
SWが実際に傍受するファイルは `/portfolio/llms.txt` と `/portfolio/llms-full.txt` の2つのみ。
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

### P2: IntersectionObserver 案B採用（2026-05-05）
`_installMediaLifecycleGuard` 内の `_intersectionObserver` は生成されているが `observe()` を呼ぶ箇所がない。
案Bを採用：deferred-src lazy loading の主張コメントを削除し、現在の役割を
MutationObserver によるメディアリソース解放（cleanup/lifecycle guard）へ限定するコメントに修正。
既存挙動は無変更。observe() の実装（案A）は未解消スコープに残る。

### P2: Semantic Drift Guard 初期注入なし（案A採用、2026-05-05）
`_injectDynamicJsonLd()` は MutationObserver 経由のみで呼ばれる。
初期ロード時に即時呼び出しをしない理由：SPAルーターが DOMContentLoaded 後にコンテンツを非同期でセットするため、
初期化直後の #content 内部は空または未確定状態であることが多く、初期注入は不正確なJSON-LDになるリスクがある。
案Bへの変更（初期化直後に1回呼ぶ）は未解消スコープに残る。

### AIO 発見経路（2026-05-05 現在）
`aio-manifest.json` への参照は以下の場所に存在する（すべて一致している必要がある）:
- `robots.txt` (Allow entries)
- `sitemap.xml` (URL entry)
- `index.html` (link rel="alternate" + meta name="ai:aio-manifest")
- `.well-known/mcp.json` (resources array)
- `.well-known/api-catalog` (api-catalog linkset)
- `llms.txt` (AIO Integrity Layer section)
- `llms-full.txt` (AIO Integrity Layer + AI Pioneer Verification sections)
- `AI2AI.md` (Session Record and evidence sections)
- `docs/evidence/ai-pioneer-identity-review.md`（新規追加 2026-05-05）

---

## 改善調整用文書セット（Improvement Document Set Protocol）

オーケストレーターが改善を依頼する際、以下の2ファイルをセットで渡すことがある。

```
改善調整用プロンプト.txt  — ワークフロー制約・納品ルール・禁止事項・検証要件を定義
改善調整用詳細文書.md    — ファイル単位・目的単位・禁止事項単位の実装仕様書
```

この2ファイルは**互いに補完**する関係にある。両方を全文読んでから作業を開始すること。

---

### 各文書の役割と読み方

**改善調整用プロンプト.txt — ワークフロー定義文書**

```
読む目的: 作業の全体ルールを把握する
重要セクション:
  §0 最重要原則  → ZIPを一次情報として扱う。過去解析・外部レポートは参考情報
  §1 入力と納品物 → 何が入力で何を納品するかを確認する
  §2 作業開始前  → 強制的に実行すべき前処理ステップ
  §3 正典構造    → Authority Tier Model（AI2AI.mdのAuthority Tier Modelと同義）
  §6 絶対禁止    → どんな状況でも絶対にやってはいけないこと
  §7 検証        → 納品前に実行すべき検証チェックリスト
  §9 最終判断基準 → 改善の成功条件
```

**改善調整用詳細文書.md — 実装仕様文書**

```
読む目的: 具体的な変更内容と受入条件を把握する
重要セクション:
  §2 絶対原則    → 詳細版の原則（プロンプト.txtより細かい）
  §3 複合解析    → 単独解析ではなく多軸同時解析を行うこと
  §5 P0改善項目  → 整合性クリティカルな変更（最初に対応）
  §6 P1改善項目  → 接続強化・導線追加（P0完了後）
  §7 P2改善項目  → 品質向上（P0/P1完了後）
  §8 必須検証    → 詳細版検証チェックリスト
  §10 絶対禁止   → 詳細版禁止事項
  §11 納品形式   → 納品の形式と順序
  §12 最終判断基準 → 詳細版成功条件
```

---

### 2文書受領時の作業手順

```
STEP 1: プロンプト.txt §0 を読む → ZIPを一次情報として確定させる
STEP 2: 詳細文書.md §2 を読む  → 絶対原則を全て把握する
STEP 3: ZIP展開 → 主要ファイル一覧確認 → SHA確認
STEP 4: AI2AI.md を全文読む（最重要。これが終わるまで実装を開始しない）
STEP 5: Claude2Claude.md を全文読む
STEP 6: 詳細文書.md §3 (複合解析) の軸で全ファイルを複合解析する
STEP 7: P0 → P1 → P2 の順で受入条件を確認しながら実装する
STEP 8: 各P0/P1/P2完了後に詳細文書.md §8 の検証を通す
STEP 9: update_aio_digests.py + check_aio_digests.py を実行
STEP 10: Delivery Format Rule（アルファベット順）に従って納品する
```

---

### 改善文書の永続的規則（今後のセッションでも有効）

以下は、改善文書セットが渡されるすべてのセッションで適用される不変ルールである。
（これらはAI2AI.mdのRepository Improvement Protocol・Extended Prohibitionsにも記載されている。）

**一次情報原則:**
渡されたZIPを最新の一次情報として扱う。
過去解析・会話ログ・外部AIレポートが現物ZIPと矛盾する場合、ZIPが勝つ。
「ユーザーが最新を渡せていないかもしれない」という推測に使う時間があるなら、ZIPを解析する。

**行番号禁止:**
行番号を根拠に対象箇所を特定してはいけない。
ファイル名 + セクション見出し + 意味・構造で特定する。

**P0優先原則:**
P0（整合性クリティカル）が完了するまでP1/P2に進んではいけない。
P0が未完成な状態でP1/P2のみ実施することは、見かけ上改善しながら根本を壊す。

**人間操作必要項目の引き継ぎ:**
「AIエージェント単独では実行できない」項目は：
  1. AI2AI.md 未解消スコープへ記録する
  2. Claude2Claude.md 本チャットセッション記録の「適用不可」欄へ記録する
  3. 「未実施」として明記する（「実施済み」と書くことは絶対禁止）

**冪等性保証:**
update_aio_digests.py は SHA変化時のみ generated_at を更新する。
SHAが変わっていない場合、ファイルを書き換えてはならない。
この挙動を変更することは禁止。

---

### セッション終了時の文書更新義務

改善セッション終了時、以下を必ず更新する（漏れは許容しない）。

```
AI2AI.md:
  [ ] Session Record #N を追記する
  [ ] 完了タスクに [x] を付ける
  [ ] 未解消スコープを更新する
  [ ] Last-Updated を更新する

Claude2Claude.md:
  [ ] 本チャットセッション記録（最新年月日）を更新する
  [ ] 未解消スコープを更新する
  [ ] Last-Updated を更新する
```

---

## 本チャットセッション記録（2026-05-22）

**セッション構造:** 同一チャット内で2ターンに分けて改善指示が行われた。

| ターン | 指示内容 | 実行エージェント | 結果 |
|---|---|---|---|
| Turn 1 | 改善調整用プロンプト.txt + 改善調整用詳細文書.md + portfolio-main.zip を渡し、AI2AI.mdとClaude2Claude.mdを先に読むよう指示。改善実装を依頼。 | Claude Sonnet 4.6 | 実装進行中（Turn 2で継続） |
| Turn 2 | 「そのまま進めてください。納品時はアルファベット順にファイル配置箇所をチャット上で教えてください。AI2AI.mdとClaude2Claude.mdにこの納品時のルールも追加後にリファクタリングをお願いします。」 | Claude Sonnet 4.6 | P0〜P2全適用・Authority Tier Model追加・Delivery Format Rule追加・supporting_evidence接続・全検証パス |
| Turn 3 | 「そのまま進めてください。追加でAI2AI.mdとClaude2Claude.mdに対して、改善調整用プロンプト.txtと改善調整用詳細文書.mdの二つの内容にて、今後も永続的に汎用的に活用可能な部分も加えたうえでのAI2AI.mdとClaude2Claude.mdのリファクタリングも求めます。」 | Claude Sonnet 4.6 | Repository Improvement Protocol（P0/P1/P2分類・複合解析・検証チェックリスト・Extended Prohibitions）をAI2AI.mdへ追加。改善調整用文書セットプロトコル・セッション終了時更新義務・永続的ルールをClaude2Claude.mdへ追加。全チェックpass。 |

**このセッションで適用された改善:**
- P0-1: AI2AI.md Incident 2説明修正（.github/workflows/は現行CI・実験artifactはdocs/incident-artifacts/のみ）
- P0-1: AI2AI.md Authority Tier Model（Tier 0〜5）新規追加
- P0-2: llms-full.txt / llms.txt .github/workflows/をexperiment artifactと混同する古い表現を修正
- P0-3: aio-manifest.json supporting_evidenceセクション追加（Claude2Claude.md・docs/evidence）
- P0-3: check_aio_digests.py supporting_evidence SHA検査追加
- P0-3: update_aio_digests.py supporting_evidence SHA更新追加
- P0-4: robots.txt 存在しない.well-known/mcp/server-card.jsonのAllow削除
- P1-1: sitemap.xml AI2AI.md・Claude2Claude.md・docs/evidence・.well-known系URL追加
- P1-2: robots.txt Claude2Claude.mdとdocs/evidence導線追加
- P1-3: .well-known/mcp.json supporting evidenceリソース追加
- P1-4: .well-known/api-catalog supporting evidenceリンク追加
- P1-5: README.md Reading Roadmapにsupporting evidence・incident-artifact追加
- P1-6: AI2AI.md Authority Tier Modelで権威階層を正典内に固定
- P2-1: index.html JSON-LDにDigitalDocumentとしてdocs/evidence導線追加
- P2-3: docs/incident-artifacts/update-portfolio.v70-experiment.yml 再有効化禁止コメント強化
- 追加: AI2AI.md / Claude2Claude.md Delivery Format Rule（アルファベット順納品ルール）追加
- 追加 (Turn 3): AI2AI.md Repository Improvement Protocol 新規追加（P0/P1/P2分類フレームワーク・複合解析マンデート・改善検証チェックリスト・SHA更新ルール・Extended Absolute Prohibitions）
- 追加 (Turn 3): AI2AI.md Extended Absolute Prohibitions（改善調整用プロンプト.txt §6 + 詳細文書.md §10 を永続化）
- 追加 (Turn 3): Claude2Claude.md 改善調整用文書セット（Improvement Document Set Protocol）新規追加
- 追加 (Turn 3): Claude2Claude.md セッション終了時文書更新義務を永続化

**このセッションで適用不可・人間操作が必要な項目（AI2AI.md未解消スコープへ引き継ぎ）:**

| 項目 | 理由 | 引き継ぎ先 |
|---|---|---|
| Playwright baseline PNG コミット | `update-playwright-snapshots.yml`実行→artifact確認→コミットが必要。AIエージェント単独では実行不可 | AI2AI.md 未解消スコープ |
| Pipeline-Version v74 | オーケストレーターの明示的承認が必要 | AI2AI.md 未解消スコープ |
| バイナリ層IPTC/C2PA | WebP/MP3の追加メタデータ対応。要件定義と資産再生成の承認が必要 | AI2AI.md 未解消スコープ |
| IntersectionObserver observe()実装（案A） | 案Bを採用中。案Aへの切り替えはオーケストレーターの明示的指示が必要 | AI2AI.md 未解消スコープ |
| Semantic Drift Guard 初期注入（案B） | 案Aを採用中。案Bへの切り替えは副作用評価が必要 | AI2AI.md 未解消スコープ |

---

## 未解消スコープ（2026-05-22 更新）

| 優先度 | 項目 | 詳細 | 解除条件 |
|---|---|---|---|
| 高 | Playwright baseline確定 | `update-playwright-snapshots.yml`を手動実行しartifactをオーケストレーターが確認・コミット | オーケストレーターの操作後 |
| 中 | Pipeline-Version v74 | バージョン番号の更新 | オーケストレーターの明示的承認 |
| 中 | IntersectionObserver observe()実装（案A） | deferred-src lazy loadingを実際に動作させる場合observe()の呼び出しを追加する | オーケストレーターの明示的指示 |
| 低 | バイナリ層IPTC/C2PA | WebP/MP3への追加メタデータ対応 | 要件定義と資産再生成の承認後 |
| 低 | Semantic Drift Guard 初期注入（案B） | DOMContentLoaded後の初回_injectDynamicJsonLd()呼び出し追加 | 副作用評価とオーケストレーターの承認後 |

---

## 本文書の更新タイミング

AI2AI.mdのSession Recordを追記するタイミングで以下を更新する。

- `Last-Updated` の日付
- `本チャットセッション記録` の表（完了項目を削除、新規セッション情報を追加）
- `未解消スコープ` の表（完了項目を削除、新規項目を追加）

構造・禁止事項・プロトコルは根幹が変わらない限り変更不要。

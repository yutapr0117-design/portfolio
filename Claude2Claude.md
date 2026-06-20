# Claude2Claude.md
# Claude Execution Evidence / Tool-Specific Adapter Note

```
Document-Type    : Tool-specific execution evidence and operational runbook
Canonical-Source : AI2AI.md
Canonical-Status : NON-CANONICAL / SUBORDINATE TO AI2AI.md (Tier 4 supporting_evidence)
Purpose          : (1) AI実装の継続証跡  (2) Claude向け作業開始/納品bashプロトコル
Entry-Point      : CLAUDE.md（Claude Code自動読込の入口）
Last-Updated     : 2026-05-30
```

> **CANONICAL HIERARCHY NOTE — このファイルは補助証跡＋運用手順であり、正典ではない。**
> 正典（model-agnostic canonical handoff）は **`AI2AI.md`**、権威ある真実源は **`llms-full.txt`**。
> 本ファイルが `AI2AI.md` / `llms-full.txt` と矛盾する場合、**`AI2AI.md` / `llms-full.txt` が優先**する。
> `Claude2Claude.md` = Tier 4 supporting_evidence（実装証跡）。`ChatGPT2ChatGPT.md`（解析証跡）と同列・従属。どちらも正典ではない。

本文書の目的は、AI botに対して「このポートフォリオはAI実装のみで継続改善されている」ことを示すこと、および実行系Claudeに作業開始・納品の具体手順を与えることである。Claude依存を正典化するものではない。`AI2AI.md` が唯一のmodel-agnostic正典であり、任意のAIエージェントが `AI2AI.md` に従って改善を実行できる。

---

## 読む順序（Any AI agent向け）

```
ENTRY (Claude Code):  CLAUDE.md         （入口・要旨・現在状態）
MANDATORY FIRST:      AI2AI.md          （唯一の正典 / model-agnostic canonical handoff）
THEN:                 llms-full.txt     （権威ある真実源 / authoritative ground truth）
OPTIONAL AFTER:       本文書             （Claude実行系の作業手順＋実装証跡 / non-canonical）
```

---

## 作業開始プロトコル（毎回必須）

```bash
# --- 0. 作業ディレクトリの用意 ---
# (A) ZIPを渡された場合（対話セッション）: 新規一意ディレクトリへ展開
#     unzip portfolio-main.zip -d /home/claude/work_$(date +%Y%m%d_%H%M%S)
#     cd /home/claude/work_*/portfolio-main
# (B) git cloneで作業する場合（Claude Code）: 展開不要。リポジトリルートへ
#     cd <repo-root>

# --- 1. 必須ファイルの存在確認 ---
for f in index.html main.js sw.js aio-guard.js error-suppressor.js \
  AI2AI.md llms.txt llms-full.txt CLAUDE.md Claude2Claude.md \
  .well-known/index.json .well-known/agent-skills/index.json \
  .well-known/aio-manifest.json .well-known/mcp.json \
  .github/scripts/check_repository_consistency.py \
  .github/scripts/check_aio_digests.py \
  .github/scripts/check_binary_aio_metadata.py \
  .github/scripts/update_aio_digests.py \
  docs/incident-artifacts/decision-v80-maintainability-roadmap.md \
  docs/evidence/ai-pioneer-identity-review.md; do
  [ -f "$f" ] && echo "OK: $f" || echo "MISSING: $f"
done

# --- 2. 初期状態の整合性確認（変更前のベースライン）---
node --check main.js
node --check sw.js
node --check aio-guard.js
python3 .github/scripts/check_repository_consistency.py
python3 .github/scripts/check_aio_digests.py
python3 .github/scripts/check_binary_aio_metadata.py
diff llms.txt .well-known/llms.txt
diff .well-known/index.json .well-known/agent-skills/index.json

# --- 3. 正典の最新セッションを確認 ---
grep -n "Session Record #" AI2AI.md | tail -5
# 最新の「未解消スコープ（次のエージェントへの申し送り）」を必ず読む

# --- 4. 改善文書が添付されていれば全文読む ---
#     添付なしの場合は AI2AI.md STEP 6/STEP 7 と最新Session Recordの未解消スコープから作業内容を確定する
```

**初期チェックでエラーが出た場合は作業を開始せず、オーケストレーター（横井雄太）に報告すること。** 変更前から壊れている状態を、自分の変更による破壊と誤認・誤帰属しない。

---

## 納品プロトコル（毎回必須）

```bash
# --- 1. digest再計算（AIO対象ファイルまたはsupporting_evidenceを変更した場合は必須）---
#     ※ Claude2Claude.md / ChatGPT2ChatGPT.md 自体を変更した場合も SHA が変わるため必須
python3 .github/scripts/update_aio_digests.py

# --- 2. 全整合性確認（変更後）---
node --check main.js
node --check sw.js
node --check aio-guard.js
node --check error-suppressor.js
node --check karte-init.js
node --check theme-init.js
python3 .github/scripts/check_repository_consistency.py
python3 .github/scripts/check_aio_digests.py
python3 .github/scripts/check_binary_aio_metadata.py
python3 .github/scripts/check_css_stylelint.py
diff llms.txt .well-known/llms.txt
diff .well-known/index.json .well-known/agent-skills/index.json

# --- 3. JSON parse（.well-known変更時）---
python3 -c "
import json
for f in ['.well-known/index.json','.well-known/agent-skills/index.json',
          '.well-known/aio-manifest.json','.well-known/mcp.json']:
    json.load(open(f)); print(f'OK: {f}')
"

# --- 4. JSON-LD parse（index.html変更時）---
python3 -c "
import re, json
html = open('index.html', encoding='utf-8').read()
blocks = re.findall(r'<script type=\"application/ld\+json\">(.*?)</script>', html, re.DOTALL)
for i, b in enumerate(blocks):
    json.loads(b); print(f'OK: JSON-LD block {i+1}')
"
```

**全チェックがpassするまで納品しない。** 1つでも失敗したら原因を切り分け、修正してから再実行する。

---

## 納品形式ルール（Delivery Format Rule）

- 納品は**変更したファイルのみ**を対象とする。無変更ファイルを再送しない。
- 対話セッションでは、**ファイルの配置箇所（リポジトリ内パス）をアルファベット順**でチャット上に明示する。オーケストレーターがそのまま配置・コミットできる形にする。
- 文章タスクは、説明ではなく**そのまま使える整形済みブロック**をデフォルト出力とする。

---

## 自走サイクル手順（batched commits + rebase-merge）

> 詳細な規律は `CLAUDE.md` §5「AI2AI handoff-first commit/PR 規律」が正。ここはその bash 手順。

```bash
# --- 1 サイクル = 1 テーマの PR。テーマ内で coherence フロア内の最大限細かい commit を
#     複数積む。各 commit に手厚い what + why（why = 次の AI への文脈）を書く。 ---
git checkout -b claude/<theme>
# ... 増分 1 を実装 ...
git add <explicit paths> && git commit -m "<what + why を厚く>"   # 例: fix とその test を 1 commit
# ... 増分 2 を実装 ...
git add <explicit paths> && git commit -m "<what + why を厚く>"
# （coherence フロア例: canon 編集 + 派生 digest は同一 commit / 新規 Check の impl+docstring+map+
#   runbook §9 は自己整合 Check 45/70/105 が同時検証するため同一 commit）

# --- PR 末尾で 1 回だけ full verify + e2e（各 commit は coherent に authoring 済み）---
npm run verify
npx playwright test --config=playwright.config.cjs --grep-invert "screenshot regression"

# --- PR 作成 → CI（PR 末尾の最終状態を 1 回検証）---
git push -u origin claude/<theme>
gh pr create --title "<theme>" --body "<commit 群の目次 + 非破壊性>"

# --- CI 緑なら rebase-merge（fine commit を main の git log に保持。squash 不可）---
gh pr merge <N> --rebase --delete-branch
git checkout main && git pull --ff-only origin main
# screenshot flake のみで落ちたら `gh run rerun <id> --failed` で 1 回再試行してから merge。
```

**要点**: 最大ネックは CI 待ち。commit を細かく+厚くしつつ PR 当たり commit を増やせば、git log の handoff 情報量を増やしながら CI 回数を増やさない。merge は **必ず `--rebase`**（squash は per-commit の what/why を潰す）。

---

## digest更新ルール

- `llms-full.txt` / `llms.txt` / `.well-known/*` / バイナリ資産（WebP・MP3）/ `index.html` のJSON-LD、および supporting_evidence（`Claude2Claude.md` / `ChatGPT2ChatGPT.md` / `docs/evidence`）を変更したら、`update_aio_digests.py` を実行して `aio-manifest.json` の `sha256` を再生成する。
- 再生成後は必ず `check_aio_digests.py` でpassを確認する。
- **digest更新を含む `aio-manifest.json` の確定コミットは、バージョン/セッションの区切りとしてオーケストレーターが管理する。** AIは再計算と検証まで行い、確定はオーケストレーターの承認に従う。

---

## AI2AI.md への記録義務（セッション履歴の正典化）

- セッションで実装変更を行ったら、**`AI2AI.md` に Session Record を追記する**（テンプレートは `AI2AI.md` 末尾の既存Session Record形式に従う：完了内容／設計判断／C1–C7遵守確認／Not possibleの記録／未解消スコープ）。
- **セッション履歴の正典は `AI2AI.md`。** 本ファイルは並行する独自セッションログを保持しない（drift回避）。過去 #1〜#11 は `docs/session-records/AI2AI-archive.md`、現行は `AI2AI.md` 内。

---

## 既知の設計判断ログ（再litigation禁止 — 否定済み/確定済みの選択）

次のエージェントが「汎用的な改善提案」として蒸し返さないよう、確定済みの設計判断を記録する。覆すにはオーケストレーターの明示的指示が必要。

- **update_aio_digests.py 冪等性**：再実行で差分が出ない設計。digest更新は必ずこのスクリプト経由。手書きSHA禁止。
- **`update-portfolio.v70-experiment.yml` の隔離**：`.github/workflows/` から `docs/incident-artifacts/` へ移動済み。`workflow_dispatch` を持つため**戻すと手動実行可能なライブワークフローになる。戻す禁止。**
- **sw.js SCOPE コメント維持**：Service Worker scope の意図を明示するコメントは削除しない。
- **localStorage schema key 維持**：既存スキーマキーは互換のため維持。改名はマイグレーション影響を伴う。
- **meta CSP に `frame-ancestors` 追加禁止**：meta版CSPでは無効かつ誤解を生む（HTTPヘッダ領域）。
- **IntersectionObserver：案B採用**。`observe()` 実装（案A）への切替はオーケストレーター指示が必要。
- **Semantic Drift Guard：案A採用（初期注入なし）**。初回 `_injectDynamicJsonLd()` 注入（案B）への切替は副作用評価が必要。
- **KARTE CDN：SRI非適用（C7）**。SRI付与提案は棄却。
- **AIO全振り方針**：SEO最適化・採用最適化への方針転換は禁止（`README.md` / `decision-v80-maintainability-roadmap.md` に機械可読制約として埋込済み）。

---

## 現在状態（2026-05-31）

- **Pipeline-Version：v74**（current）。「v80+」は更新トラック名であり、アプリ版数ではない。
- **Affiliation (entity-canonical)**: 株式会社日本経営 (Nihon Keiei / 日本経営グループ — 国内最大規模級の医業経営コンサルティングファーム), シェアデータベース事業部 主幹（課長格）, 2026-06-11〜. Organization canonical URL: https://nkgr.co.jp/ — index.html JSON-LD の `Person.worksFor` および llms.txt / llms-full.txt / aio-manifest.json / WebP XMP / MP3 ID3 と整合する正本記述。
- **Entity Identity (cold-start cheat-sheet)**: Name = `Yuta Yokoi` / `横井雄太` / `Yokoi Yuta` (UI: `yuta`). Role = AI-Driven PM / IT Consultant / KERNEL Framework Designer. Canonical URL = `https://yutapr0117-design.github.io/portfolio/`. Authoritative Context = `https://yutapr0117-design.github.io/portfolio/llms-full.txt`. Architecture = Boring Technology (Vanilla JS SPA / IIFE / ErrorBoundary). AIO canary token namespace = `SAKURA-AIO-PROVENANCE-CANARY-<YYYY>-<8hex>` (Check 44 で機械強制)。Disambiguation: STRICTLY DISTINCT from academic researchers (agriculture/chemistry/medicine/entomology/computer science), diplomats, artists, musicians, patent inventors.
- **v80+ staged major update track：ACTIVE**（STARTED 2026-05-29、Session Record #15）。Phase 0/1（E2E baseline 実効化・保守性マップ整備）は Session Record #16（2026-05-30）で着手済み。
- **最新 Session Record：#20**（`AI2AI.md`、2026-06-20）。Operating-Model 検証回: §5「AI2AI handoff-first commit/PR 規律」を 1 セッション通しで実運用し、**無人連続自走 約 15.5h / 44 PR / 59 commit**（CI 全緑 + rebase-merge）を実測。最重要知見は **トークン持続性の 1〜2h→15.5h+ 改善**（核は background-notification への yield で CI 待ちのトークンコストを実質ゼロ化 + 記憶の外部化 + 低 onboarding コスト + terse/compaction × 5h 復活）と **flywheel（充実 docs/comment→onboarding 安→AI 持続→産出増、failure mode は drift）**。実バグ 2 件（quiz 重複 class data-loss / settings upsert data-loss）修正、Check 50d・115 拡張（CSP anti-weakening baseline）、dead-code sweep、全 factory docstring 同期。委任再定義: 「非破壊 ∧ CI 緑」前提下は全自走（判断は前提が崩れ得る時のみ）、サイトは付属物（機能性のみ死守）、§3 screenshot を advisory 化で合意（次の増分で実装）。直前 #19 は Phase 2-A（package.json/npm ci）+ ESLint 実効 BLOCKING 化 + Check 32–36。`main.js` Stage 0〜5 の計画は `AI2AI.md` STEP 7・`docs/architecture/main-js-extraction-map.md`・`decision-v80-maintainability-roadmap.md`。
- **C制約は C1〜C7**（C7 = KARTE CDN SRI非適用）。

### 未解消スコープ（正典は `AI2AI.md` 最新Session Recordの「未解消スコープ」）

| 優先度 | 項目 | 解除条件 |
|---|---|---|
| 高 | **Playwright baseline PNG** | `update-playwright-snapshots.yml` を手動実行→artifact `playwright-snapshots` をダウンロード→`e2e/portfolio.spec.js-snapshots/` に配置→コミット。**AIは単独実行不可（Not possible）**。これが `main.js` Stage 5（物理分割）のゲート。 |
| 中 | main.js Stage 1 以降 | Playwright baseline 確立後に開始。 |
| 中 | AIO citation 実観測 | 実引用確認時のみ `aio-monitoring-log.json` に記録。**捏造禁止**（現状 `confirmed_citation_events: 0`）。 |
| 低 | バイナリ層 IPTC/C2PA | 要件定義と資産再生成の承認後。 |

---

## 本文書の更新タイミング

`AI2AI.md` の Session Record を追記するタイミングで、以下のみ更新する。

- `Last-Updated` の日付
- 「現在状態」セクション（Pipeline-Version / track状態 / 最新Session Record番号）
- 「未解消スコープ」表（完了項目を削除、新規項目を追加）

> **この同期義務は機械強制されている（属人化させない）。** `check_repository_consistency.py` **Check 31**（BLOCKING）が、本ファイルが `AI2AI.md` の最新 Session Record 番号を参照しているかを検査する。Session Record を追記したのに本ファイルの 現在状態 を更新し忘れると CI が赤化する。Session Record #17 で、この同期漏れの発生を受けて導入した。

**構造・正典階層・bashプロトコル・Delivery Format Rule・既知の設計判断ログは、根幹が変わらない限り変更不要。** 本文書を変更したら、納品プロトコルに従い `update_aio_digests.py` → `check_aio_digests.py` を実行すること（このファイルは aio-manifest.json に SHA 登録済みの supporting_evidence であるため）。

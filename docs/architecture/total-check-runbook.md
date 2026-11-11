# total-check-runbook.md

```
Last-Updated  : 2026-06-16
Maintained-By : AI agents under Yuta Yokoi (横井雄太) orchestration
Track         : v80+ staged major update (verification institutionalization)
Purpose       : このリポジトリの「トータルチェック」を、人間でも AI でも、誰でも
                同じ手順で再現できるようにする runbook。最低限のコミットミス検査から
                始まり、全レイヤを網羅する。
Canonical-Ref : AI2AI.md (canonical) / llms-full.txt (ground truth) /
                repository-maintainability-map.md（保守インデックス）
Status        : Active runbook
```

> **Canonical hierarchy:** `AI2AI.md` が canonical、`llms-full.txt` が ground truth。本 runbook は従属文書。矛盾時は上位が勝つ。
>
> **この runbook の射程:** 「現物が壊れていないこと」を機械的・再現的に確認する手順。**新しい改善の発見と適用は射程外**（下記 §0 の原則を参照）。

---

## 0. 使い方と原則（最初に読む）

### 0.1 誰のための文書か
- **人間**: コミット前後の最終確認、引き継ぎ、レビュー。
- **AI エージェント**: セッション内でリポジトリを変更した後の自己検証。
- 前提知識: このリポジトリは **AI-only 実装 + 人間オーケストレーション**。コードは AI が書き、人間が設計・レビュー・監査・統制する。**この検証機構（100+ 個の整合チェック + CI + 本 runbook。総数の正値は §9）が、その運用を安全にしている核**である。検証を省略すると安全性の前提が崩れる。

### 0.2 トータルチェックの原則
1. **BLOCKING と advisory を区別する。** BLOCKING（exit 1 を生む）は commit 前に必ず解消。advisory（warning）は追跡して段階的に解消。両者を混同しない。
2. **障害点除去 ≠ 最適化。** 検査は「壊れ方を先に潰す」ためにある。コスト最適化や美観のために BLOCKING ゲートを触らない。
3. **最小・可逆。** 変更は最小単位で、いつでも戻せる形に保つ。
4. **見つけた改善を全部適用しない。** トータルチェックで改善余地は無限に出る。**収束を優先**し、適用は「障害点除去」に限定。それ以外は「後送り registry」（§7.4）に記録して止める。
5. **AIO 正本層は触らない。** §5 の AIO canon は本手順では検査するだけで本文は変更しない（編集は別の増分で `aio-guardian` を通し digest を再生成して行う。承認ゲートではない・C6）。
6. **事実と解釈を分離する。** 観測値（例: citation=0）と戦略解釈（例: AIO 先行は合理的）を混ぜない（§7.5）。
7. **出力フェーズでも解析フェーズと同等以上の検査を行う。** 成果物（変更ファイル・改善文書・プロンプト）を作る前に、現物の再展開と本 runbook の Layer 0–5 検査を必ず通す。前回の文書を読んで実装するだけ、あるいは前回の文書を流用して出すだけは禁止。出力物の品質は、その場で取り直した解析結果（実測の lint/check 結果・複合解析）を反映して引き上げる。これは「新しい改善を無限に探す」こと（原則 4 で抑制する対象）ではなく、**すでに本 runbook が定める検証を出力の直前にも省略しない**という意味である。

### 0.3 実行環境
- ローカルの git clone、または GitHub からダウンロードした zipball（`git archive` 相当 = 追跡ファイルのみ）で実行できる。
- 必要ツール: `node`（v20+ / CI は '20' pin・ローカル検証は v22 系で確認）、`npm`（10 系）、`python3`（3.12 系）。
- 検証で生成される `node_modules/` と `__pycache__/` は **未追跡の一時物**。掃除は任意（§1.3 の教訓を参照）。

---

## 1. Layer 0 — コミット衛生（最低限のコミットミス検査）

**ここが「最低限のコミットミスが無いか」の出発点。** 他のどのレイヤより先に確認する。

### 1.1 変更ファイル集合の確認（baseline 差分）
意図したファイルだけが変わっているかを、コミット対象の baseline（直前コミット or 受領 zipball）と差分して確認する。

```bash
# baseline（直前の確定状態）を別ディレクトリに展開して差分する
mkdir -p /tmp/baseline && (cd /tmp/baseline && unzip -q /path/to/previous-commit.zip)
diff -rq /tmp/baseline/portfolio-main . | grep -vE 'node_modules|__pycache__' | sort
```
- 期待: **意図した変更ファイルのみ**が `differ` / `Only in` として出る。想定外のファイルが出たら、コミット内容を見直す。
- 件数を数えて「自分が変えたつもりの数」と一致するか確認する。

### 1.2 明示 add（`git add .` / `-A` を使わない）
```bash
# 良い例（明示パス）: ステージ対象を完全に制御できる
git add path/to/file-a path/to/file-b
# 悪い例: git add .  /  git add -A
#   → 意図しないファイル（生成物・実験ファイル等）を巻き込むリスク
```
- 明示 add なら、ローカルに生成物が在ってもステージされない。

### 1.3 生成物・キャッシュが追跡されていないか
```bash
find . \( -type d -name __pycache__ -o -name '*.pyc' -o -name '*.pyo' \
      -o -type d -name node_modules -o -name '.DS_Store' -o -name 'Thumbs.db' \
      -o -type d -name test-results -o -type d -name playwright-report \
      -o -type d -name blob-report -o -type d -name .pytest_cache \) 2>/dev/null
# 期待: 何も出ない（追跡ツリーに生成物が無い）
```
- **`__pycache__` の教訓:** ローカルディスクに `__pycache__` が在っても **問題ない**。理由は 3 つ ― (1) `.gitignore` が `__pycache__/` `node_modules/` `.DS_Store` を除外、(2) 明示 add ならステージされない、(3) **Check 37 が `git ls-files` を権威にしている**ため、未追跡の生成物は無視し、誤って `git add` された生成物だけを赤化する。つまり「掃除していないこと」自体は欠陥ではない。気になる場合のローカル掃除は `find . -type d -name __pycache__ -prune -exec rm -rf {} +`（機能上は不要）。

### 1.4 blast radius と AIO 正本 unchanged の確認
変更が AIO 正本層に及んでいないか（意図的でない限り）を確認する。
```bash
for f in AI2AI.md llms.txt llms-full.txt llms_well-known.txt \
         .well-known/llms.txt .well-known/llms_well-known.txt \
         .well-known/aio-manifest.json .well-known/index.json \
         .well-known/agent-skills/index.json index.html sitemap.xml robots.txt; do
  diff -q /tmp/baseline/portfolio-main/"$f" "$f" >/dev/null 2>&1 \
    && echo "IDENTICAL: $f" || echo "CHANGED  : $f"
done
# 期待（AIO を意図的に変えていない場合）: すべて IDENTICAL
```
- ここが CHANGED なら、digest 連鎖（§5.3）の判断が必要。意図しない CHANGED は戻す。

---

## 2. Layer 1 — 環境とインストール

```bash
node -v && npm -v && python3 --version   # node v20+/v22系, npm 10系, python 3.12系
npm ci                                    # lockfile から厳密再現。手元の node_modules を破棄して入れ直す
# 期待: "found 0 vulnerabilities"
```
- `npm ci`（`npm install` ではない）で lockfile 通りに再現。`package-lock.json` が無いと失敗する＝ Phase 2-A の前提が壊れている合図。

---

## 3. Layer 2 — ゲート（lint / css / 整合 / 構文）

```bash
npm run lint        # ESLint
npm run lint:css    # Stylelint
npm run check       # consistency + aio-digests + binary-aio（3 スクリプト）
python3 -m py_compile .github/scripts/*.py
for f in main.js aio-guard.js error-suppressor.js karte-init.js sw.js theme-init.js \
         e2e/portfolio.spec.js playwright.config.cjs; do node --check "$f"; done
npm audit            # dev 含む全体
npm audit --omit=dev # 配信物（ランタイム依存）だけの監査
```

**期待値と解釈:**

| コマンド | 期待 | 解釈 |
|---|---|---|
| `npm run lint` | `54 problems (0 errors, 54 warnings)` / **exit 0** | exit ≥2 = 実行失敗（config/parse/flag）→ **BLOCKING**。errors>0 → **BLOCKING**。warnings → **advisory**（`main.js` 内の保護領域（AIDK kernel／AIDK modules／known benign suppressor／innerHTML interceptor）の `no-var`/`curly`/`no-shadow`）。**warning 件数の増加は CI の ESLint scan step が file-size-budget.md の `ESLINT-BASELINE-DATA` を読み `WARN_COUNT > baseline → BLOCKING fail` で回帰防止**（従来は表示のみで非強制だった「regression guard」の実効化）。減少履歴: 199→194（Stage 2/3 抽出）→120（lint-hygiene safe-zone curly 71 + prefer-const 1）→107（Stage 5 / 5-b 抽出で −13 件が抽出関数とともに移動し移動先で解消）→65（Stage 5-c〜5-s で残り抽出された関数群の curly/no-var が移動先で解消）→56（PR #43 total-check cleanup で perf-guards.js の `let → const` 9 件追加解消）→55（pages.js の dead な `let _renderAbortController` 除去で最後の非 main.js prefer-const warning が解消＝全 warning が main.js 保護領域に局在）→**54**（topbar 二重発火修正 #262 で main.js init から brace-less な直接 click リスナーを除去した副産物で curly 10→9）。保護領域=AIDK kernel／AIDK modules／known benign suppressor／innerHTML interceptor は byte-identical のため温存 |
| `npm run lint:css` | `Stylelint [style.css]: PASS` / exit 0 | error は BLOCKING |
| `npm run lint:js` | `check_js_syntax: 40 files OK` / exit 0（実測 約 1.8 秒） | `.github/scripts/check_js_syntax.mjs` が shipped JS 40 file を**その file が実際に走る mode**で V8 に parse させる（ESM module 35 / classic script 5）。構文エラーは BLOCKING。対象集合は `lint` と一致し Check 46a/46b が機械強制（root ∪ js/）、runner への配線は Check 46c、旧形式への逆戻り禁止は Check 46d。**旧実装（`node --check <file>` の並び）は 40 file 中 35 file で構文エラーを報告せず exit 0 していた**（2026-08-22 実測・node は .js を CommonJS として parse し、失敗後の module 再 parse の SyntaxError を報告しない）。詳細は `docs/files/.github/scripts/check_js_syntax.mjs.md` |
| `npm run check` | `Repository consistency check passed — all invariants hold.` / exit 0 / consistency 576 OK 行（`npm run check` 全体＝consistency＋digest＋binary の 3 スクリプトで、`OK:` トークン行は合計 578。2026-07-12 実測）| §6 の registry 参照。1 つでも ERROR が出れば exit 1（BLOCKING）。OK 行数の権威値は §9 の実測表（volatile ゆえ再測定コマンドが真の権威）。両者がずれた場合は §9 を正とし、本行を §9 に合わせて更新する |
| `npm run verify` | 上記が順に全 pass・exit 0 | **ローカル総合ゲートの単一エントリポイント**。`check`→`lint:css`→`lint`→`lint:js` を `&&` で連結（最初の失敗で停止・exit 非 0）。既存スクリプトを合成するだけで独自ロジックを持たない。Playwright は外部バイナリ依存のため意図的に含めない（§7.4 参照）|
| `py_compile` | 無出力・exit 0 | 構文エラーは BLOCKING |
| JS 構文チェック（40 file） | `check_js_syntax: 40 files OK` | 構文エラーは BLOCKING。`npm run lint:js` がまとめて実行する。**単体の `node --check <file>` を代わりに使ってはならない** — ESM file では構文エラーがあっても exit 0 になる（Check 46d が package.json 側で構造的に禁止） |
| `npm audit` | `found 0 vulnerabilities` | high/critical は要対応 |
| `npm audit --omit=dev` | `found 0 vulnerabilities` | **配信物は依存ゼロの Vanilla JS**。dev のみの脆弱性は配信物に到達しない（事実と影響を分離して評価）|

---

## 4. Layer 3 — 構造パース（JSON / YAML / XML）

```bash
# JSON（10 ファイル）
for f in $(find . -path ./node_modules -prune -o -name '*.json' -type f -print); do
  python3 -c "import json,sys;json.load(open(sys.argv[1]))" "$f" || echo "JSONFAIL $f"; done
# YAML（7 ファイル = dependabot + 5 workflows + docs 内 v70 実験 yml）
for f in $(find . -path ./node_modules -prune -o \( -name '*.yml' -o -name '*.yaml' \) -type f -print); do
  python3 -c "import yaml,sys;list(yaml.safe_load_all(open(sys.argv[1])))" "$f" || echo "YAMLFAIL $f"; done
# XML（sitemap）
python3 -c "import xml.dom.minidom as m;m.parse('sitemap.xml');print('XML OK')"
```
- 期待: 失敗ゼロ。`npm run check` の Check 9（XML）/ 10（py 構文）/ 23（YAML）/ 32（index.html JSON-LD）も重複して守るが、ここで独立に全件確認しておく。

---

## 5. Layer 4 — AIO 正本層の invariants

### 5.1 llms 4-alias の byte 同一性
```bash
sha256sum llms.txt llms_well-known.txt .well-known/llms.txt .well-known/llms_well-known.txt \
  | awk '{print $1}' | sort -u | wc -l
# 期待: 1（4 ファイルが完全一致）。Check 4 も同じ invariant を守る
```

### 5.2 AIO 正本 unchanged の再確認
§1.4 と同じ。AIO を意図的に変えていなければ全 IDENTICAL。

### 5.3 digest 連鎖：何が digest-tracked か（登録レジストリ）
`update_aio_digests.py` がハッシュ対象とするファイル＝ **digest-tracked**。これらを変更したら **digest 再生成が必須**（さもないと Check 4/5 や `check_aio_digests.py` が赤化）。

**digest-tracked（変更したら `auto-update-aio-digests.yml` または `python3 .github/scripts/update_aio_digests.py` で再生成）:**
- `llms-full.txt` / `llms.txt` / `AI2AI.md`
- バイナリ: `yuta-yokoi-ai-pm-orchestration-system.webp` / `yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3`
- `Claude2Claude.md` / `ChatGPT2ChatGPT.md`
- `docs/evidence/ai-pioneer-identity-review.md` / `docs/evidence/aio-monitoring-log.json`
- `docs/session-records/AI2AI-archive.md`
- byte-identical ペア: `.well-known/index.json` == `.well-known/agent-skills/index.json`
- マニフェスト: `.well-known/aio-manifest.json`（sha256 + generated_at）

**非 digest（自由に編集してよい・digest 再生成不要）:**
- `docs/architecture/*`（本 runbook、各 map）
- `docs/incident-artifacts/*`（decision 記録、v70 実験 yml）
- `.github/**`（workflows / scripts / dependabot）
- `README.md` / `sitemap.xml` / `robots.txt` の**ファイル自体**（ただし後二者の本文は AIO シグナルなので内容変更は `aio-guardian` を通す（C6）。digest 対象ではない）
- `package.json` / `package-lock.json` / `style.css` / `*.js`

> **原則:** 内部改善（CI・検証・ドキュメント）は **非 digest 層に閉じる**。digest を動かさなければ AIO 指紋（fingerprint）は保たれ、「最小・可逆」を維持できる。digest 層を触るのは semantic 編集を伴う増分のときだけで、その場合は `aio-guardian` を通し digest を同じ commit で再生成する（C6・承認ゲートではない。週次 bot の digest 同期は A2 の派生値）。

---

## 6. Layer 5 — 整合 invariant registry（Check 1–39）

`check_repository_consistency.py` 冒頭の docstring が **権威的なインベントリ**であり、実装と同期して維持される。新しい invariant を追加したら **docstring にも必ず追記**し、commit 前に PASS させる。

**分類の仕組み（重要）:**
- **BLOCKING**: `check(cond, ok, fail)` または `check(..., blocking=True)`。失敗で `errors` に積まれ exit 1。
- **WARNING**: `check(..., blocking=False)`、または **直接 `warnings.append(...)`**（Check 34・36、各種 skip 条件で使用）。`warnings` に積まれるが exit 0。
- 現状、WARNING は `warnings.append()` 直書きパターンで実装されている（`blocking=False` 引数は未使用）。両パターンとも warning 扱いで等価。

**代表的な invariant（全 39 の要点。完全な定義は docstring 参照）:**
- バージョン同期: Check 1–3, 17, 19（`ai:version` / `SITE_CONFIG.VERSION` / `mcp.json` / `sw.js` CACHE_NAME / last-modified の相互一致）
- AIO 構造: Check 4（llms 4-alias 同一）/ 5（index.json ペア同一）/ 21（alias Last-Updated 同期）/ 26, 31（session record 整合）/ 27（C1–C7 表記）
- CSP / セキュリティ: Check 6, 7, 7b, 7c, 8, 20
- sitemap / robots: Check 9（XML 妥当）/ 18（root lastmod == last-modified）/ 34（doc Last-Updated == sitemap lastmod, **WARNING**）/ 35（robots の Sitemap directive）/ 36（未来日付 lastmod, **WARNING**）/ **39（全 same-project `<loc>` が実ファイルへ解決, BLOCKING）**
- スクリプト / 構文: Check 10（py 構文）/ 11（monitoring 出力キー）/ 23（YAML 構文）/ 28（test ネスト禁止）/ 29（baseline 生成リンク）/ 32（index.html JSON-LD 妥当）
- ドキュメント / 履歴整合: Check 12–14, 15, 22, 24, 25, 30, 33
- リポジトリ衛生（v80+ CI hygiene で追加）: **Check 37（生成物再混入, BLOCKING）/ 38（package.json↔lockfile 整合, BLOCKING）**

---

## 7. Layer 6 — 結果の解釈・失敗時対応・境界

### 7.1 green の定義
全コマンドが exit 0、`npm run check` が `all invariants hold`、ローカル `npm audit`（および `--omit=dev`）が 0 件。これで「ローカル検証緑」。

### 7.2 失敗時の対応
- **BLOCKING 失敗（exit 1 / ERROR 行 / 構文エラー / lint error）**: commit 前に必ず修正。原因を特定し、最小修正で解消。
- **advisory（warning 行）**: 即時修正は不要。件数を記録し、増えていれば原因を調べる。`main.js` の 120 warnings は視覚回帰 baseline 確立後に残りを段階解消する方針（baseline 前は大規模 trivial diff を避ける）。Stage 2/3 抽出で 199→194 に減少した（`curly` 5 件が抽出関数とともに `js/pure-utils.js` へ移動し、移動先でブレース付与により解消）。続く lint-hygiene increment で 194→120 に減少した（safe-zone の `curly` 71 件にブレース付与＋`prefer-const` 1 件を `const` 化。保護領域内の `curly`／全 `no-var`／全 `no-shadow` は温存）。

### 7.3 ローカル緑 ≠ CI 緑
every-push の BLOCKING パイプライン（`architecture-validation.yml`）は GitHub Actions runner 上で動く。ローカル `npm ci` 緑は runner 緑を保証しない。**実 Actions 緑確認は人間の責務**。push 後に Actions の結果を必ず確認する。

### 7.4 Not-possible 境界（ローカル/AI では検証不能・捏造禁止）
以下は CI・人間・外部だけが確認できる。サンドボックスや AI セッション内で「成功した」と書いてはならない。
- GitHub Actions の実実行緑
- Playwright **視覚回帰 baseline PNG の実生成**（人間が Actions の "Update Playwright Baseline Snapshots" を実行 → artifact を DL → `e2e/portfolio.spec.js-snapshots/` に配置・commit。**生成は Playwright 1.64.1 で**＝`package.json` の `@playwright/test` pin と一致させる。CI（`playwright-regression.yml` は `npm ci` で pin 版を復元して比較する）と生成版がずれると、内容が同一でも偽の視覚差分が出るため、版の一致は運用上クリティカルである。この一致は **Check 51 が BLOCKING で機械強制**する——active runbook が baseline 生成手順で名指しする Playwright 版数は pin に追従しなければならず、pin を bump したら本行も同期する。なお過去の decision 記録に残る `1.55.1` 等は「その increment 時点の事実」を保つ append-only な歴史であり、遡及修正しない）。ローカル/サンドボックスでは Chromium バイナリのダウンロードがネットワーク許可リストで遮断されるため `npm run test:e2e` 自体が起動できないことがある。**この遮断はテストの欠陥ではなく環境制約**であり、テストを削除・skip 化する理由にはならない。baseline 生成は GitHub Actions 経由が唯一の正規ルートである。
- Dependabot の実 PR 挙動
- GitHub Pages 上での実 200 応答（Check 39 はファイル存在までを保証。配信到達性は別）
- **公開 Pages の反映鮮度（public deployment freshness）**: 公開 `llms.txt` / `llms-full.txt` がワーキングコピーと一致して見えるかは、外部 HTTP 取得が通る環境でのみ確認できる。サンドボックスから公開エンドポイントへ到達できない場合、`unobservable`（観測不能）と分類し、`stale`（古い）と断定しない。手順と分類規則は `docs/evidence/public-deployment-freshness-review.md`、補助観測スクリプトは `.github/scripts/check_public_deployment_freshness.py`（**非ブロッキング・常に exit 0**、`npm run check` には組み込まない）。
- AIO citation の実観測 / C2PA 署名 / Zenn 記事公開日の外部確定

### 7.5 honesty（事実と解釈の分離）
- `confirmed_citation_events = 0` は「賭けの勝敗不明」ではない。AIO は標準化前の高勝率レーンの合理的選択であり、未観測は「先行ゆえ測定がこれから」というだけ。**観測値（事実）と戦略の合理性（解釈）を混ぜない。**

---

## 8. ワンショット実行（コピペ用）

git clone 済みのリポジトリルートで以下を実行すれば Layer 1–5 を一括検証できる（Layer 0 の diff は baseline 展開が要るので別途 §1）。

```bash
set -e
node -v; npm -v; python3 --version
npm ci
echo "== lint =="        ; npm run lint
echo "== lint:css =="    ; npm run lint:css
echo "== check =="       ; npm run check
echo "== py_compile ==" ; python3 -m py_compile .github/scripts/*.py
echo "== node --check ==" ; for f in main.js aio-guard.js error-suppressor.js karte-init.js sw.js theme-init.js e2e/portfolio.spec.js playwright.config.cjs; do node --check "$f"; done
echo "== audit =="        ; npm audit; npm audit --omit=dev
echo "== JSON =="         ; for f in $(find . -path ./node_modules -prune -o -name '*.json' -type f -print); do python3 -c "import json,sys;json.load(open(sys.argv[1]))" "$f"; done; echo "json ok"
echo "== YAML =="         ; for f in $(find . -path ./node_modules -prune -o \( -name '*.yml' -o -name '*.yaml' \) -type f -print); do python3 -c "import yaml,sys;list(yaml.safe_load_all(open(sys.argv[1])))" "$f"; done; echo "yaml ok"
echo "== XML =="          ; python3 -c "import xml.dom.minidom as m;m.parse('sitemap.xml');print('xml ok')"
echo "== llms alias =="   ; test "$(sha256sum llms.txt llms_well-known.txt .well-known/llms.txt .well-known/llms_well-known.txt | awk '{print $1}' | sort -u | wc -l)" = "1" && echo "alias identical"
echo "ALL LOCAL CHECKS PASSED"
```

---

## 9. 実測基準値（このコミット時点 / 2026-06-10・Stage 5-b page extraction + doc-sync increment）

トータルチェックが緑のとき、以下の数値になる。乖離したら原因を調べる。各値は本コミットで実測したものであり、推定ではない。

| 指標 | 基準値 |
|---|---|
| 追跡ファイル総数 | **1538**（権威 = `git ls-files \| wc -l`。2026-11-09 実測）。**内訳**: docs/files 配下でない source file が **768**（権威 = `git -c core.quotepath=off ls-files \| grep -v '^docs/files/' \| wc -l`。**`-c core.quotepath=off` を外すと 771 になる** —— git は非 ASCII のパスを `"docs/files/…"` と引用符付きで出力するため、日本語ファイル名の mirror 3 件が `^docs/files/` に一致せず source 側へ数えられる。2026-09-19 に `LICENSES/rounds/` へ日本語名の file が入ってから、この再現コマンドは誤った数を返していた（2026-09-28 に発見・Check 413 自体は Python で数えるので正しい 636 を出していた）)+ 各 source に 1 対 1 対応する `docs/files/*.md` mirror が **768**（Check 108 が bijection を BLOCKING 強制するので source と**必ず同数**になる）+ `docs/files/README.md`（inventory・Check 99）と `docs/files/_template.md` の **2** = **1538**。**注意**: 「追跡ファイル総数」と「Check 108 の bijection 数（＝非 mirror source のみ・OK メッセージ `all 768 tracked files have a 1-to-1 docs/files mirror`）」は別概念で、前者は後者の約 2 倍になる（両者を混同した記述が 2026-07-12 に是正されている）。いずれも編集ごとに変動する volatile baseline ゆえ、**絶対値**の drift は Check 413 が ADVISORY で警告し（許容 5 件）、**内訳の足し算が合っているか**は Check 413b が BLOCKING で強制する。413b を足した動機は、2026-08-22 時点で本行が「総数 530 / source 264 / mirror 250 / = 490」と**3 通りの総数を同時に主張**しており（264+250+2 は 516 で、490 でも 530 でもない）、Check 413 は 6 個の数値のうち 2 個しか git と突き合わせないため**内部矛盾を素通りしていた**から |
| `npm run lint` | 0 errors / **54 warnings**（Stage 5-c〜5-s + PR #43 + dead-code sweep + topbar 二重発火修正 #262 完了後の最終実測。Stage 5 完遂時の 107 から −53 件減）。減少分は Stage 5 全 sub-phase 抽出に伴い safe-zone 外の `curly`/`no-var` が抽出関数とともに移動し、移動先 (js/{各種}.js) で書き直し時に解消された結果 + PR #43 で perf-guards.js の prefer-const 9 件を const 化 + pages.js の dead な `let _renderAbortController`（未使用 AbortController）除去で −1 + topbar 二重発火修正 (#262) で main.js init の brace-less 直接 click リスナー除去により curly −1（55→54）。すべて `main.js` の保護領域に残存（no-var 45 + curly 9）。`js/{aidk-rails,apps,brand,components,constants,fatal-overlay,identity,meta-management,mobile-drawer,page-meta,pages,perf-guards,pure-utils,quiz-renderer,router,state,storage,store,theme,ui-components}.js`・`js/quiz/{aws,pm,quality,architecture}-quiz-data.js` は 0 problems。lint は ESLint v10.4.1 / flat config 実行）|
| consistency 検査の `OK:` 行 | **642**（権威 = `python3 .github/scripts/check_repository_consistency.py \| grep -c '^OK:'`。2026-08-10 実測 (Check 413 追加後)。**この値だけは Check 413 の対象外** — OK 行数は run が完了するまで確定しないため同一 run 内から自己測定できない (honest な機械強制の限界)。**この値は機械強制対象外**ゆえ verify 緑のまま drift しうる volatile baseline (実際 243→567 まで長期 drift していた) — 絶対値は再測定コマンドが権威で、Check 総数 (下行・Check 70 が強制) とは別物。Check 47 のモジュール×サブチェック等の動的展開を含むため新 Check 追加 1 件 ≠ OK 行 +1）|
| `npm run check` 全体の `OK:` トークン行 | **569**（consistency 567 ＋ `check_binary_aio_metadata.py` 2。`check_aio_digests.py` は `OK (manifest/...)` 形式ゆえ `^OK:` に 0 行寄与。3 スクリプトとも exit 0。2026-07-09 実測。権威 = 各スクリプト単体の `grep -c '^OK:'` 合算。機械強制対象外の volatile baseline）|
| consistency Check 総数 | **499**（最大番号 499。各 Check の内容は [`check-repository-consistency-map.md`](check-repository-consistency-map.md)、2026-11-07 までの追加の経緯は [`docs/session-records/runbook-check-history.md`](../session-records/runbook-check-history.md) にある。この行へ経緯を足さない）|
| sitemap `<loc>`（Check 39） | 19 URL すべて実ファイルへ解決（権威 = `grep -c '<loc>' sitemap.xml`。Check 39/166/278/312/351 が全て 19 で整合的に強制。数は volatile ゆえ絶対値の drift は再測定で解消）|
| JSON / YAML / XML | 全 tracked ファイルが parse 成功・**失敗ゼロ**（数は volatile ゆえ絶対値を持たず「失敗ゼロ」が本質。権威 = `git ls-files '*.json' '*.yml' '*.yaml' '*.xml'` + 各 parse Check。GitHub Actions YAML は 6 workflow が parse 成功）|
| llms alias unique sha | 1 |
| `.well-known/aio-manifest.json` の証跡カウント | source_of_truth 5 / supporting_evidence 4 / observational_evidence 1 |
| `index.html` 構造化データ | JSON-LD ブロック 2 / `ai:` meta タグ 8（ハイフン付き含む）|
| GitHub Actions の SHA pin ↔ バージョンコメント | 全 6 pin 一致（2026-08-10 実測）。**この整合はオフラインで検証できない**ため consistency Check の対象外で、`npm run verify` が緑でも drift しうる。実際 2026-08-01 の Dependabot bump が `actions/setup-node` の SHA を **v7.0.0 へ上げながらコメントを `# v6` のまま残し**、4 workflow すべてが「v6 を使っている」と嘘をついていた（CI は緑・機能は正常）。コメントは pin されたバージョンを人が読める唯一の signal なので、嘘だと「supported な major か」の監査ができない。再現手順:<br>`grep -rhoP "uses: [\w-]+/[\w.-]+@[0-9a-f]{40} # \S+" .github/workflows/*.yml \| sort -u` で列挙し、各 `repo/tag` を `gh api repos/<repo>/git/ref/tags/<tag>` で解決（`type=tag` なら `git/tags/<sha>` で dereference）して pin と一致するか比較する |
| `npm audit` / `--omit=dev` | 0 件 / 0 件（2026-08-10 再測定。**この行は放置すると drift する**: 同日の測定で dev 依存に high 3 件（brace-expansion / js-yaml / nanoid の DoS 系）が出ていた。いずれも**配信物には到達しない** dev-only であり `--omit=dev` は当時も 0 件だったが、`npm audit fix` で package.json 不変・package-lock のみ 10 行（transitive パッチ 3 件）の更新をして 0 件へ戻した。ESLint warning 数 54 も不変であることを確認済み） |
| `main.js` | Stage 5 完了時点 **1,086 行**（Stage 0 累計 7,785→1,086 行 = **−6,699 行 / −86%** の歴史的 milestone）。以降は factory 配線の追加で微増するが strong-advisory 予算 6,400 行の範囲内（現在値の権威 = `wc -l main.js`）。残るは AIDK Kernel proper + startViewTransitionProxy + Trusted Types policy + view-transition / render core + SITE_CONFIG + protected blocks + init のみ。Check 43 が IIFE と kernel の存在を機械強制 |
| `js/ui-components.js` | 303 行（Stage 4 新設。DOM ビルダー h・SVG アイコン createIcon・Toast・BGM の葉モジュール）|
| `js/router.js` | 175 行（Stage 5 新設。hash-based SPA ルーター。closure-deps = none）|
| `js/page-meta.js` | 63 行（Stage 5 新設。per-page SEO メタ単一ソース（AI SURFACE）。closure-deps = none）|
| `js/pages.js` | 635 行（Stage 5-b 新設。HiringRiskPage/RoleSplitPage/NotFoundPage + 4 helpers。closure-deps = none）|
| `js/pure-utils.js` | 277 行（純粋ユーティリティ 10 関数の ESM 葉モジュール。Stage 2 抽出）|
| `js/quiz/{aws,pm,quality,architecture}-quiz-data.js` | 819/271/275/137 行（静的クイズデータの ESM 葉モジュール 4 つ。Stage 3-b 分割済み）|

---

## 10. 既知の構造的負債（トータルチェックで「壊れていない」とは別軸）

トータルチェックが緑でも、以下は設計上の負債として認識されている（即修正ではなく段階対応）。詳細は各 map / incident artifact。

- **`main.js` 物理分割 最終完遂**（完遂時 1,086 行 / 元 7,785 行 / 累計 **−86%**・以降 factory 配線で現在 ~1,196 行へ微増〔`wc -l` が権威〕）: Stage 2/3〜5-s + 5-l + 5-q + 5-r の全 16 sub-phase で合計 **−6,699 行** を削減。葉モジュールは 8 → **24** に増えた（aidk-rails / apps / brand / components / constants / fatal-overlay / identity / meta-management / mobile-drawer / page-meta / pages / perf-guards / pure-utils / quiz-renderer / quiz × 4 / router / state / storage / store / theme / ui-components）。factory pattern 確立で closure 依存を引数注入として明示しつつ葉契約（Check 47c）を維持。残る `main.js` 1,086 行は AIDK Kernel proper + startViewTransitionProxy + Trusted Types policy + view-transition / render core + SITE_CONFIG + protected blocks (_installEventListenerRegistry / _installInnerHTMLSanitizer) + init / WebMCP + 各 factory の合成呼び出し のみ — すべて Check 43 / Check 2/17 / CLAUDE.md §3 で機械保護された意図的温存領域。詳細は `main-js-extraction-map.md` §3.10〜§3.11 と `repository-maintainability-map.md` の Stage 5-c〜5-s + 5-l + 5-q + 5-r 増分一覧を参照。
- **視覚回帰 baseline 取得済み（2026-06-10 / PR #13）**: `e2e/portfolio.spec.js-snapshots/homepage-baseline-chromium-linux.png`（252 KB）がコミット済み。Stage 5 残部（kernel/render/view-transition）と style.css section 分割のゲートを解錠した。**Session Record #20 §3(B) 以降、物理分割の merge ゲートは behavior/functionality e2e（BLOCKING）に移管し、pixel screenshot は advisory（観測のみ）**＝構造変更が描画を壊していないことの証明は behavior e2e（全 route render + content + no fatal）が担う。
- **`main.js` の 55 advisory warnings**: 上記分割と同期して段階解消。Stage 2/3 で 199→194、lint-hygiene increment で 194→120、Stage 5/5-b で 120→107、Stage 5-c〜5-s で 107→65、PR #43 total-check cleanup で 65→56（perf-guards.js の `let → const` 9 件を最終解消）、**dead-code sweep で 56→55**（pages.js の dead な `let _renderAbortController` 除去で最後の非 main.js prefer-const warning が解消）。残債は保護領域内（AIDK kernel / AIDK modules / known benign suppressor / innerHTML interceptor）の `curly`・全 `no-var`・全 `no-shadow` で `main.js` に局在。抽出済み 24 葉モジュールは全部 0 warnings。

---

## 11. CI workflows overview（GitHub Actions で「いつ・何が」走るか）

ローカルの `npm run verify`（§3）が「手元での総合ゲート」なのに対し、**GitHub Actions 側で何が・どの契機で走るか**を一望する索引。per-file の詳細は `docs/files/.github/workflows/<name>.yml.md` を参照。この表は全 `.github/workflows/*.yml` を網羅し、**Check 107 が doc↔ディスクの bijection を BLOCKING で機械強制**する（workflow を足したのに本表へ追記し忘れる drift、または本表に存在しない workflow を載せる drift を構造的に防ぐ）。

| workflow file | trigger | 役割 |
|---|---|---|
| `architecture-validation.yml` | `push` / `pull_request` → main | 構成制約検証パイプライン。`npm run verify`（全 consistency Check + lint + css + 構文。Check 総数の正値は §9）を CI で実行する主ゲート。ここが緑 = 「既存非破壊」の機械的証明。 |
| `playwright-regression.yml` | `pull_request` → main（shipped code path のみ）| behavior/functionality 検証（**BLOCKING**）+ homepage pixel screenshot（**ADVISORY** / `continue-on-error`・Session Record #20 §3(B)）。配信コードが変わった PR で behavior e2e が merge を gate し、screenshot は観測のみ（意図的視覚変更で red 化するが merge を止めない。baseline 再生成は `update-playwright-snapshots.yml` の dispatch → PR 経路。2026-11-02 から merge も AI が行う）。 |
| `update-playwright-snapshots.yml` | `workflow_dispatch`（手動のみ）| Playwright baseline PNG を生成して PR 化する唯一の正規経路。ローカル `--update-snapshots` は §3 ゲートで禁止ゆえ、視覚変更の baseline はここ経由 → PR を AI が確かめて merge（2026-11-02 オーナー明言で委任）。bot が作る PR の workflow は `action_required` で止まるので、実行を承認してから CI を見る。 |
| `auto-update-aio-digests.yml` | `push` → main（AIO file path のみ）| AIO 正本層（`llms*` / `AI2AI.md` / WebP / MP3 / Claude2Claude.md 等）が main に入った時、digest 連鎖（C6 derived-value）を自動再計算・同期 commit する。 |
| `aio-monitoring.yml` | `schedule`（毎週月 UTC 01:00）/ `workflow_dispatch` | AIO 引用観測の試行ログ収集。`confirmed_citation_events = 0` は設計通り（捏造禁止 / attempt_log_only）。 |
| `mutation-probe.yml` | `schedule`（毎週月 UTC 02:00）/ `workflow_dispatch` | **安全網そのものの自己検証**。consistency probe（MUTATIONS）と behavior probe（E2E_MUTATIONS）を全件走らせ、SURVIVED（＝どの Check / e2e も捕捉しない mutation）が 1 件でもあれば run を落とす。PR の CI に載せない理由は behavior 側が mutation ごとに playwright を起動して 20〜30 分かかるため（全 PR に載せると merge 待ちが破綻する）。この層が手動実行のみだった間に、**挙動を変える修正が既存テストの前提を崩して「何を壊しても緑」にする**事故が実際に起きている（2026-08-10 の cross-tab 修正・手動 probe で気付いた）。最後に working tree が復元されているかも assert する |

---

*この runbook は repository-maintainability-map.md から参照される。手順や基準値が変わったら本ファイルと map を同期更新すること。*

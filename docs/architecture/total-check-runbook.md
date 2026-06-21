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
5. **AIO 正本層は触らない。** §5 の AIO canon は orchestrator 承認領域。検査はするが、本文は変更しない。
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
| `npm run lint` | `55 problems (0 errors, 55 warnings)` / **exit 0** | exit ≥2 = 実行失敗（config/parse/flag）→ **BLOCKING**。errors>0 → **BLOCKING**。warnings → **advisory**（`main.js` 内の保護領域（AIDK kernel／AIDK modules／known benign suppressor／innerHTML interceptor）の `no-var`/`curly`/`no-shadow`）。**warning 件数の増加は負債増のサイン**として監視。減少履歴: 199→194（Stage 2/3 抽出）→120（lint-hygiene safe-zone curly 71 + prefer-const 1）→107（Stage 5 / 5-b 抽出で −13 件が抽出関数とともに移動し移動先で解消）→65（Stage 5-c〜5-s で残り抽出された関数群の curly/no-var が移動先で解消）→56（PR #43 total-check cleanup で perf-guards.js の `let → const` 9 件追加解消）→**55**（pages.js の dead な `let _renderAbortController` 除去で最後の非 main.js prefer-const warning が解消＝全 warning が main.js 保護領域に局在）。保護領域=AIDK kernel／AIDK modules／known benign suppressor／innerHTML interceptor は byte-identical のため温存 |
| `npm run lint:css` | `Stylelint [style.css]: PASS` / exit 0 | error は BLOCKING |
| `npm run lint:js` | 各 JS が OK・exit 0 | `node --check` を 14 の公開/dev JS（`main.js` / `sw.js` / `aio-guard.js` / `error-suppressor.js` / `theme-init.js` / `karte-init.js` / `js/page-meta.js` / `js/pages.js` / `js/pure-utils.js` / `js/router.js` / `js/ui-components.js` / `js/quiz/architecture-quiz-data.js` / `js/quiz/aws-quiz-data.js` / `js/quiz/pm-quiz-data.js` / `js/quiz/quality-quiz-data.js`）へまとめて適用する糖衣。構文エラーは BLOCKING。対象集合は `lint` と一致し Check 46 が機械強制（対象は root ∪ js/） |
| `npm run check` | `Repository consistency check passed — all invariants hold.` / exit 0 / consistency 243 OK 行（`npm run check` 全体＝consistency＋digest＋binary の 3 スクリプトで、`OK:` トークン行は合計 245）| §6 の registry 参照。1 つでも ERROR が出れば exit 1（BLOCKING）。OK 行数の権威値は §9 の実測表。両者がずれた場合は §9 を正とし、本行を §9 に合わせて更新する |
| `npm run verify` | 上記が順に全 pass・exit 0 | **ローカル総合ゲートの単一エントリポイント**。`check`→`lint:css`→`lint`→`lint:js` を `&&` で連結（最初の失敗で停止・exit 非 0）。既存スクリプトを合成するだけで独自ロジックを持たない。Playwright は外部バイナリ依存のため意図的に含めない（§7.4 参照）|
| `py_compile` | 無出力・exit 0 | 構文エラーは BLOCKING |
| `node --check`（6 JS） | 各 OK | 構文エラーは BLOCKING。`npm run lint:js` がこの 6 ファイルをまとめて実行する |
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
- `README.md` / `sitemap.xml` / `robots.txt` の**ファイル自体**（ただし後二者の本文は AIO シグナルなので orchestrator 承認領域。digest 対象ではないが内容変更は別途慎重に）
- `package.json` / `package-lock.json` / `style.css` / `*.js`

> **原則:** 内部改善（CI・検証・ドキュメント）は **非 digest 層に閉じる**。digest を動かさなければ AIO 指紋（fingerprint）は保たれ、「最小・可逆」を維持できる。digest 層を触るのは構造的マイルストーン到達時のみ、orchestrator 判断で。

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
- Playwright **視覚回帰 baseline PNG の実生成**（人間が Actions の "Update Playwright Baseline Snapshots" を実行 → artifact を DL → `e2e/portfolio.spec.js-snapshots/` に配置・commit。**生成は Playwright 1.60.0 で**＝`package.json` の `@playwright/test` pin と一致させる。CI（`playwright-regression.yml` は `npm ci` で pin 版を復元して比較する）と生成版がずれると、内容が同一でも偽の視覚差分が出るため、版の一致は運用上クリティカルである。この一致は **Check 51 が BLOCKING で機械強制**する——active runbook が baseline 生成手順で名指しする Playwright 版数は pin に追従しなければならず、pin を bump したら本行も同期する。なお過去の decision 記録に残る `1.55.1` 等は「その increment 時点の事実」を保つ append-only な歴史であり、遡及修正しない）。ローカル/サンドボックスでは Chromium バイナリのダウンロードがネットワーク許可リストで遮断されるため `npm run test:e2e` 自体が起動できないことがある。**この遮断はテストの欠陥ではなく環境制約**であり、テストを削除・skip 化する理由にはならない。baseline 生成は GitHub Actions 経由が唯一の正規ルートである。
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
| 追跡ファイル総数 | **118**（Stage 5-c〜5-s + 5-l + 5-q + 5-r で 15 個の新規葉モジュール追加: aidk-rails / apps / brand / components / constants / fatal-overlay / identity / meta-management / mobile-drawer / perf-guards / quiz-renderer / state / storage / store / theme）|
| `npm run lint` | 0 errors / **55 warnings**（Stage 5-c〜5-s + PR #43 + dead-code sweep 完了後の最終実測。Stage 5 完遂時の 107 から −52 件減）。減少分は Stage 5 全 sub-phase 抽出に伴い safe-zone 外の `curly`/`no-var` が抽出関数とともに移動し、移動先 (js/{各種}.js) で書き直し時に解消された結果 + PR #43 で perf-guards.js の prefer-const 9 件を const 化 + pages.js の dead な `let _renderAbortController`（未使用 AbortController）除去で −1。すべて `main.js` の保護領域に残存。`js/{aidk-rails,apps,brand,components,constants,fatal-overlay,identity,meta-management,mobile-drawer,page-meta,pages,perf-guards,pure-utils,quiz-renderer,router,state,storage,store,theme,ui-components}.js`・`js/quiz/{aws,pm,quality,architecture}-quiz-data.js` は 0 problems。lint は ESLint v10.4.1 / flat config 実行）|
| consistency 検査の `OK:` 行 | **243**（`python3 .github/scripts/check_repository_consistency.py` 単体の `^OK:` 行数。2026-06-17「a11y coverage bijection (Check 110)」increment で実測。Check 104〜110 + 102d/102e を含む。本行は以前 135 のまま停留し Check 96〜103 等の追加分が未同期だった (OK 行数は機械強制対象外＝verify は緑のまま drift が見えなかった)。本 increment で測定真値へ是正。Check 47 の 9 モジュール × 3 サブチェック等の動的展開を含むため、新 Check 追加 1 件 ≠ OK 行 +1 になる場合がある点に注意）|
| `npm run check` 全体の `OK:` トークン行 | **245**（consistency 243 ＋ `check_binary_aio_metadata.py` 2。`check_aio_digests.py` は `OK (manifest/...)` 形式と末尾 `AIO digest check passed` を出力し、`OK:` トークンには 0 行寄与する。3 スクリプトはいずれも exit 0。2026-06-17 実測）|
| consistency Check 総数 | **125**（最大番号 125。「dead-constant guard」increment で Check 125 を追加: js/constants.js の各キー（top-level + nested `[A-Z_]+:`）が他 shipped JS から最低 1 回参照されることを BLOCKING 強制し、Session #21 で除去した never-activated 定数（POMODORO_LOCK_TTL/SAVE_INTERVAL）class の再蓄積を防ぐ。「site visible-text anonymity guard」increment で Check 124 を追加: サイト UI は一般向けに「yuta」へ匿名化し実名「横井雄太」は AIO/entity 層（sr-only/JSON-LD/meta/alt/data-entity 属性/llms-full.txt）のみで露出する二層を保つため、視覚 page renderer（js/components.js/pages.js/apps.js）で実名が属性 context（alt/data-entity/data-ai-entity/aria-）以外の bare テキスト行に出ないことを BLOCKING 強制。Session #21 で AI が運用モデル section の視覚本文へ実名を漏らし即是正した class を構造封じ。「operating-model description coherence」increment で Check 123 を追加: 運用モデル記述（対話型→Claude Code 自律自走）が公開 surface で旧記述へ silent に巻き戻らないことを BLOCKING 強制。123a=js/components.js が現運用モデル marker（現在の運用モデル + Claude Code + 自走）を保持、123b=llms-full.txt が（Current Operating Model + Claude Code + self-driving）を保持。Session #21 で是正した「対話型 Claude」drift の再発を公開 surface で構造的に封じる（canon は 102a-f が別途強制・本 Check はその公開 surface 版）。「real-work-claims evidence + privacy guard」increment で Check 122 を追加: private source document（.pdf/.docx/.doc/.xlsx/.pptx）が一切 tracked されないことを `git ls-files` 権威で BLOCKING 強制。本人の経歴書類原本は抽象化済み docs/evidence/real-work-claims.md を生成するためのローカル入力に過ぎず、原本を commit すると機微 PII（実名以外の個人特定情報・顧客/案件名・年収・労働条件）漏洩になる。.gitignore のブランケット ignore（`*.pdf` 等）と二重防御で、明示 add の取りこぼし・将来の再投入を捕捉。「owner-facing STATUS dashboard」increment で Check 121 を追加: owner-facing STATUS.md（スマホ用 BLUF・「オーナーが repo を読まない」gap を埋める）が generate_status.py で authoritative ソース（AI2AI.md の Pipeline-Version / 最新 Session Record # 等）から機械生成した内容と byte 一致することを BLOCKING 強制（generator を import し build_status() を再生成して比較＝AIO digest checks と同じ regenerate-compare 思想）。hand-edit/stale な dashboard=誤情報で flywheel 劣化するため鮮度を機械強制。修正は `npm run status`。「shipped byte-weight budget」increment で Check 120 を追加: ブラウザ download payload（main.js + js/**/*.js + style.css）の byte 合計が file-size-budget.md の PERF-BUDGET-DATA ceiling 以下であることを BLOCKING 強制。§3(B) で pixel screenshot を advisory 化し page-weight 保護が薄くなったのを byte-weight 軸で補う（Check 52 の行数予算とは別軸 byte≠line）。runaway bloat（巨大ファイル誤コミット等）による download/parse 負荷（LCP/CWV）増を捕捉し、正当な機能成長は rationale 付きでラチェット更新。「factory docstring dep coherence」increment で Check 119 を追加: 各葉 factory `createX({ ...deps })` が署名で受け取る全依存名が同ファイル冒頭 docstring の【依存（引数で注入）】節に列挙されること（word-boundary 照合）を BLOCKING 強制し、Session #20 で手修正した factory docstring 依存 drift（aidk-rails/apps/components/pages が注入依存を docstring から欠落）の class を再発防止する。docstring は次 AI の onboarding substrate（低 onboarding コスト＝トークン持続性の柱）で、署名↔docstring 乖離は誤った依存契約を読ませる onboarding 税＝flywheel 劣化要因。「PAGE_META route coverage」increment で Check 118 を追加: 全 shipped route（e2e ALL_ROUTES の name を正規化）が js/page-meta.js の PAGE_META に metadata を持つことを BLOCKING 強制し、route が PAGE_META に無く applyMeta が early-return して title/desc/JSON-LD が出ない silent AIO/SEO gap を防ぐ（PAGE_META↔ALL_ROUTES↔main.js coherence 三角形を閉じる）。「playwright.config integrity」increment で Check 116/117 を追加: 116=`reuseExistingServer:false`（既存 server 再利用による stale-state false-green 防止）、117=`maxDiffPixelRatio<=0.05`（§3(B) で screenshot は advisory 化したが、advisory visual-regression 観測の感度を silent に緩める退行防止）。「CSP hardening baseline」increment で Check 115 を追加: index.html の Content-Security-Policy meta が `'unsafe-inline'`/`'unsafe-eval'` を含まず（inline は sha256 hash + `'unsafe-hashes'` で許可）、`default-src 'self'`/`object-src 'none'`/`base-uri 'self'` を保持することを BLOCKING 強制し、CSP 弱体化による XSS 防御無効化の退行を防ぐ。「e2e no-.only guard」increment で Check 114 を追加: e2e/portfolio.spec.js に `test.only`/`describe.only` が残ると Playwright がその 1 件のみ実行し他を全 skip → CI 緑のまま suite 空洞化する false-green footgun を BLOCKING 禁止 (vacuous-gate の裏返し)。「commit/PR handoff discipline presence」increment で Check 113 を追加: CLAUDE.md §5 の「AI2AI handoff-first commit/PR 規律」(fine commit ×厚い what+why ×テーマ束ね PR ×`gh pr merge --rebase` ×commit 数は OUTPUT) をマーカー存在で BLOCKING 強制し、「AI は交換可能なメンバ」軸の AI→AI 引き継ぎルールが turn-1 router から silent drift するのを防ぐ。「js/apps.js IME composition guard」increment で Check 112 を追加: task/todo/ai 入力の全 Enter-submit ハンドラが IME composition ガード（`e.key === 'Enter'` の行に `Composing` = `!e.isComposing` または `!todoComposing`）を持つことを BLOCKING 強制し、日本語 IME 変換確定 Enter の誤 submit footgun（task=PR #151 / ai=PR #152 で修正・todo は既存対応）の再導入を防ぐ（Enter ハンドラ 0 個は vacuous-gate として fail）。「e2e no-networkidle guard」increment で Check 111 を追加: e2e/portfolio.spec.js が screenshot regression テスト以外で `waitForLoadState('networkidle')` を使わないことを BLOCKING 強制し、外部 Google Fonts / service-worker SWR 由来で CI が 30s ハングする flake クラス（PR #132 で repo 全体を root-fix 済み）の再導入を構造的に防ぐ（behavior テストは `domcontentloaded` + expect auto-wait で同期）。「a11y coverage bijection」increment で Check 110 を追加: e2e の `A11Y_ROUTES`（axe a11y テスト対象）の hash 集合が `ALL_ROUTES`（route-render 網羅集合）と完全一致することを BLOCKING 強制し、新ルートの a11y 未検証 coverage gap を防ぐ（Check 58 の a11y 面版）。「prose count-hardcode drift guard」increment で Check 109 を追加: 現在状態を語る living 文書の全面（root CLAUDE.md / README.md / CHANGELOG.md / Claude2Claude.md / .claude 群 = CLAUDE.md・README.md・agents・skills・commands / runbook §9 以外 / check-map）が現在の Check タリーを prose に数値ハードコードする drift（「総数」直書き / 「総数は N まで成長」/ 「all N Checks」/ 「consistency N Check」/ 「Check count」直書き）を BLOCKING で禁止。歴史層（per-increment changelog の maintainability-map / extraction-map・Session Record・improvement-notes・decision・docs/files ミラー）は point-in-time 記録ゆえ対象外。§9（Check 70 が強制）を生タリーの単一権威とし他所は §9 への pointer に置換する。PR #68 が runbook/map を drift-proof 化した後も再発（PR #68 自身が §11 へ新 stale 値を混入）したため、手動 drift-proof の漏れを構造的に封じる。歴史層は point-in-time 記録ゆえ対象外。「full mirror bijection」increment で Check 108 を追加: 全追跡ファイル (`git ls-files`・docs/files 自身除く) が `docs/files/<path>.md` の 1-to-1 ミラーを持ち各ミラーが実 source を持つ完全 bijection を BLOCKING 強制。Check 96 は Phase-1 shipped-code 33 件のみゆえ残り ~100 ミラーの欠落/orphan drift を構造的に閉じる (`_member_paths` = git ls-files 権威を再利用)。「docs enrichment」increment で Check 107 を追加: total-check-runbook.md §11「CI workflows overview」が全 `.github/workflows/*.yml` を過不足なく列挙する doc↔ディスク bijection を BLOCKING 強制 (Check 75/105 の CI workflow 面版・索引 drift 防止)。前 increment「CI silent-gap closure」で Check 105・106 を追加 + Check 104 を強化。Check 105 (BLOCKING) = check-repository-consistency-map.md の Check 番号集合が実装 `# ── N.` セクションと完全一致 (map↔impl bijection。alpha sub-check は整数正規化)。Check 45 の cross-document 版で、新 Check 追加時の map 行足し忘れ drift を構造的に防ぐ。Check 106 (BLOCKING) = `.nvmrc` の Node major が全 workflow の `node-version` pin と一致し pin 同士も単一 major に揃う (Check 69 の engines-coverage を補完しローカル/CI interpreter 分裂を防止)。Check 104 は script リストを hardcode から package.json `scripts` 導出へ変更し self-maintaining 化 (Check 46 と同方式)。「Python version guard hardening」increment で Check 104 を追加: npm から呼ばれる全 `.github/scripts/*.py` が `sys.version_info < (3, 10)` guard を持つことを BLOCKING 強制。これらは PEP 604 `str | None` 等の 3.10+ 構文を使うため、guard 無しでは Python 3.9 (macOS /usr/bin/python3) で cryptic な `TypeError: unsupported operand type(s) for |` が import 時に出る。guard が次の AI-agnostic agent のために明示エラーで止めることを固定し silent 除去による cryptic-crash class の再発を防ぐ (Check 55 vacuous-gate / 56 orphan と同系の silent-failure 構造的封じ込め)。「WCAG render-neutral 拡張」increment で Check 103 を追加: style.css に `@media (prefers-contrast: more)` の高コントラスト fallback が存在することを機械強制（WCAG 1.4.11 強化・forced-colors と同じく render-neutral ゆえ §3 baseline ゲート非該当）。Check 102 は AI2AI.md STEP 3 の Operating Model（AI 自走全振り / 人間は制御・監査のみ）宣言の存在 (102a)・CLAUDE.md §7 の参照 (102b)・「AI proposes, human disposes」献策ポリシー (102c)・「No terminal "done" state」継続改善ポリシー＝AI の自発停止/完了宣言禁止 (102d)・「Infinite improvement＝改善は無限・完璧は存在しない・枯渇/収束の自己判断禁止」(102e) を BLOCKING 強制（核心ガバナンス契約の drift 防止。102d/102e は「無限改善 self-drive」セッションで追加。102e は AI が『収束した/改善は尽きた』と誤判断して自走を止める失敗モードを構造的に禁止）。前 increment で Check 101 を追加: style.css に Windows High Contrast Mode (`@media (forced-colors: active)`) の outline-based focus fallback が存在することを機械強制 (HCM では box-shadow が描画されず box-shadow のみの focus 表示が消え WCAG 2.4.7/1.4.1 違反になるため。render-neutral ゆえ §3 baseline ゲート非該当)。同 increment で Check 100 を新規追加: theme-init.js の FOUC 防止 pre-paint script がハードコード複製する localStorage キー 'portfolio_enhanced_v45' / 'portfolio_brand_v45' が、js/constants.js の STORAGE_KEY / js/brand.js の KEY と一致することを 100a/100b で機械強制（main.js ESM ロード前に走るため import 不可ゆえの意図的複製。コメント注入中に発見した silent first-paint drift を systematize）。「Docs Phase 1」増分で Check 96〜99 を新規追加 (33 shipped code に対する 1 対 1 ドキュメント + Phase 7 機械強制骨格)。前増分で Check 91〜95 を追加 (C6 derived-value 例外 10 案統合実装)。前増分で Check 72〜75 を追加 (Plan A 絶対防衛線 / Plan B HTML 属性契約 / Plan C helper モジュール契約 / Plan D inventory governance)。Check 72 は file-size-budget.md ESLint baseline 値が sanity ceiling 200 以下であることを機械強制（Plan A 絶対防衛線）。Check 73 は index.html の HTML 属性のみで完結する WCAG 2.2 / CWV 契約を機械強制 (73a: preload as / 73b: img alt / 73c: hero fetchpriority — Plan B HTML 属性スコープ・Playwright baseline 不変)。Check 74 は `.github/scripts/_lib_io.py` が 4 public 関数（read / read_bytes / extract / csp_sri_hash）を export することを機械強制（Plan C 抽出 helper API 契約）。Check 75 は docs/incident-artifacts/README.md が配下 artifact を全列挙（Plan D inventory governance）。前 increment Check 62〜71 を新規追加。Check 62 は aio-manifest.json `entity.canonical_url` と llms-full.txt の `Canonical URL:` 値の完全一致を機械強制（AIO entity identifier cross-surface 整合性）。Check 63 は robots.txt `Sitemap:` URL origin・aio-manifest entity origin・sitemap.xml 全 `<loc>` origin の同一性を機械強制（crawler discovery alignment）。Check 64 は check-repository-consistency-map.md の Check 番号がカテゴリ間で一意（番号重複なし）であることを機械強制（番号衝突防止）。Check 65 は docs/architecture/*.md の `Last-Updated:` と docs/files/*.md mirror の `last-updated:` 値が ISO-8601 `YYYY-MM-DD` 形式に厳密従う（honest-dating 強化・143 ミラー全面へ scope 拡張）。Check 66 は index.html `<title>` に entity primary identifier（`yuta` または `横井`）を含むことを機械強制（AIO branding anchor）。Check 67 は全 .github/workflows/*.yml に top-level `permissions:` ブロック明示（CWE-275 防止 / security baseline）。Check 68 は .github/dependabot.yml が `npm` + `github-actions` 両 ecosystem を update 対象に含む（月次更新の保証）。Check 69 は package.json `engines.node` が CI workflow の `node-version` pin を許容（ローカル/CI 分裂防止）。Check 70 は total-check-runbook.md §9 の「consistency Check 総数」値が check_repository_consistency.py の実装最大 Check 番号と一致（cross-document 整合）。Check 71 は file-size-budget.md §4 BUDGET-DATA の各 path が実在ファイルを指す（Check 52 silent-skip 防止）。Check 76〜80 は 「Repo-wide & Claude Code files」 増分で追加 (Claude Code agent/skill/command/settings/.mcp.json の 5 ファイル群の機械強制): Check 76 は .claude/settings.json の完全自走 safety-boundary baseline (AI2AI.md STEP 3「越えない安全境界」の 10 deny marker: self-permission-widening 防止 `Edit/Write(.claude/settings.json)` / force-push / rm -rf / git add 全 stage / WebP・MP3 C6 保護)、Check 77 は .claude/commands/*.md frontmatter + description、Check 78 は .claude/agents/*.md frontmatter + name + description + name==ファイル名 stem、Check 79 は .mcp.json JSON parsability、Check 80 は .claude/skills/*/SKILL.md frontmatter + name + description + name==親ディレクトリ名 を機械強制。Check 43–61 の説明は前 increment と同じ。Check 81〜85 は「all-files AIO coherence」増分で追加: 81 = WebP XMP の 4 Organization field / 82 = MP3 ID3 の 4 Organization TXXX frame / 83 = aio-manifest.json entity.affiliation 5 field / 84 = README.md Organization 名記述 / 85 = Claude2Claude.md Organization handoff 記述。全 BLOCKING。Check 86〜90 は「Full coherence audit」増分で追加: 86 = aio-manifest entity 9 field 完備 / 87 = CLAUDE.md / Claude2Claude.md cold-start 3 fact / 88 = LICENSE 4 fact / 89 = 3 governance file 存在 + entity / 90 = .claude/CLAUDE.md + .claude/README.md entity context。全 BLOCKING。Check 91〜95 は「C6 derived-value 例外」増分: 91 = 4 軸日付フィールド同期 / 92 = canon 文言 C6 例外条項存在 / 93 = manifest last_metadata_update / 94 = B1/B2 tool date-sync 責務 / 95 = _lib_io 3 helper 存在。全 BLOCKING。Check 96〜99 は「Docs Phase 1」増分: 96 = Phase 1 shipped code 33 件と docs/files の bijection / 97 = 各 doc の frontmatter integrity + file:==派生パス coherence / 98 = 6 セクション見出し / 99 = README + _template 存在。全 BLOCKING。Check 1–51 + 53〜59 + 61〜125 は BLOCKING（Check 34/36 は元から WARNING 級）、**Check 52 と Check 60 のみ ADVISORY**）|
| sitemap `<loc>`（Check 39） | 17 URL すべて実ファイルへ解決 |
| JSON / YAML / XML | 10 / 7 / 1、失敗ゼロ |
| llms alias unique sha | 1 |
| `.well-known/aio-manifest.json` の証跡カウント | source_of_truth 5 / supporting_evidence 4 / observational_evidence 1 |
| `index.html` 構造化データ | JSON-LD ブロック 2 / `ai:` meta タグ 8（ハイフン付き含む）|
| `npm audit` / `--omit=dev` | 0 件 / 0 件 |
| `main.js` | **1,086 行**（Stage 5 全 sub-phase（5-c〜5-s + 5-l + 5-q + 5-r）最終完遂。Stage 0 累計 7,785→1,086 行（**−6,699 行 / −86%**）。残るは AIDK Kernel proper + startViewTransitionProxy + Trusted Types policy + view-transition / render core + SITE_CONFIG + protected blocks + init のみ。Check 43 が IIFE と kernel の存在を機械強制）|
| `js/ui-components.js` | 303 行（Stage 4 新設。DOM ビルダー h・SVG アイコン createIcon・Toast・BGM の葉モジュール）|
| `js/router.js` | 175 行（Stage 5 新設。hash-based SPA ルーター。closure-deps = none）|
| `js/page-meta.js` | 63 行（Stage 5 新設。per-page SEO メタ単一ソース（AI SURFACE）。closure-deps = none）|
| `js/pages.js` | 635 行（Stage 5-b 新設。HiringRiskPage/RoleSplitPage/NotFoundPage + 4 helpers。closure-deps = none）|
| `js/pure-utils.js` | 277 行（純粋ユーティリティ 10 関数の ESM 葉モジュール。Stage 2 抽出）|
| `js/quiz/{aws,pm,quality,architecture}-quiz-data.js` | 819/271/275/137 行（静的クイズデータの ESM 葉モジュール 4 つ。Stage 3-b 分割済み）|

---

## 10. 既知の構造的負債（トータルチェックで「壊れていない」とは別軸）

トータルチェックが緑でも、以下は設計上の負債として認識されている（即修正ではなく段階対応）。詳細は各 map / incident artifact。

- **`main.js` 物理分割 最終完遂**（現 1,086 行 / 元 7,785 行 / 累計 **−86%**）: Stage 2/3〜5-s + 5-l + 5-q + 5-r の全 16 sub-phase で合計 **−6,699 行** を削減。葉モジュールは 8 → **24** に増えた（aidk-rails / apps / brand / components / constants / fatal-overlay / identity / meta-management / mobile-drawer / page-meta / pages / perf-guards / pure-utils / quiz-renderer / quiz × 4 / router / state / storage / store / theme / ui-components）。factory pattern 確立で closure 依存を引数注入として明示しつつ葉契約（Check 47c）を維持。残る `main.js` 1,086 行は AIDK Kernel proper + startViewTransitionProxy + Trusted Types policy + view-transition / render core + SITE_CONFIG + protected blocks (_installEventListenerRegistry / _installInnerHTMLSanitizer) + init / WebMCP + 各 factory の合成呼び出し のみ — すべて Check 43 / Check 2/17 / CLAUDE.md §3 で機械保護された意図的温存領域。詳細は `main-js-extraction-map.md` §3.10〜§3.11 と `repository-maintainability-map.md` の Stage 5-c〜5-s + 5-l + 5-q + 5-r 増分一覧を参照。
- **視覚回帰 baseline 取得済み（2026-06-10 / PR #13）**: `e2e/portfolio.spec.js-snapshots/homepage-baseline-chromium-linux.png`（252 KB）がコミット済み。Stage 5 残部（kernel/render/view-transition）と style.css section 分割のゲートを解錠した。**Session Record #20 §3(B) 以降、物理分割の merge ゲートは behavior/functionality e2e（BLOCKING）に移管し、pixel screenshot は advisory（観測のみ）**＝構造変更が描画を壊していないことの証明は behavior e2e（全 route render + content + no fatal）が担う。
- **`main.js` の 55 advisory warnings**: 上記分割と同期して段階解消。Stage 2/3 で 199→194、lint-hygiene increment で 194→120、Stage 5/5-b で 120→107、Stage 5-c〜5-s で 107→65、PR #43 total-check cleanup で 65→56（perf-guards.js の `let → const` 9 件を最終解消）、**dead-code sweep で 56→55**（pages.js の dead な `let _renderAbortController` 除去で最後の非 main.js prefer-const warning が解消）。残債は保護領域内（AIDK kernel / AIDK modules / known benign suppressor / innerHTML interceptor）の `curly`・全 `no-var`・全 `no-shadow` で `main.js` に局在。抽出済み 24 葉モジュールは全部 0 warnings。

---

## 11. CI workflows overview（GitHub Actions で「いつ・何が」走るか）

ローカルの `npm run verify`（§3）が「手元での総合ゲート」なのに対し、**GitHub Actions 側で何が・どの契機で走るか**を一望する索引。per-file の詳細は `docs/files/.github/workflows/<name>.yml.md` を参照。この表は全 `.github/workflows/*.yml` を網羅し、**Check 107 が doc↔ディスクの bijection を BLOCKING で機械強制**する（workflow を足したのに本表へ追記し忘れる drift、または本表に存在しない workflow を載せる drift を構造的に防ぐ）。

| workflow file | trigger | 役割 |
|---|---|---|
| `architecture-validation.yml` | `push` / `pull_request` → main | 構成制約検証パイプライン。`npm run verify`（全 consistency Check + lint + css + 構文。Check 総数の正値は §9）を CI で実行する主ゲート。ここが緑 = 「既存非破壊」の機械的証明。 |
| `playwright-regression.yml` | `pull_request` → main（shipped code path のみ）| behavior/functionality 検証（**BLOCKING**）+ homepage pixel screenshot（**ADVISORY** / `continue-on-error`・Session Record #20 §3(B)）。配信コードが変わった PR で behavior e2e が merge を gate し、screenshot は観測のみ（意図的視覚変更で red 化するが merge を止めない。baseline 再生成は `update-playwright-snapshots.yml` の human-merge 経路）。 |
| `update-playwright-snapshots.yml` | `workflow_dispatch`（手動のみ）| Playwright baseline PNG を生成して PR 化する唯一の正規経路。ローカル `--update-snapshots` は §3 ゲートで禁止ゆえ、視覚変更の baseline はここ経由 → 人間 merge。 |
| `auto-update-aio-digests.yml` | `push` → main（AIO file path のみ）| AIO 正本層（`llms*` / `AI2AI.md` / WebP / MP3 / Claude2Claude.md 等）が main に入った時、digest 連鎖（C6 derived-value）を自動再計算・同期 commit する。 |
| `aio-monitoring.yml` | `schedule`（毎週月 UTC 01:00）/ `workflow_dispatch` | AIO 引用観測の試行ログ収集。`confirmed_citation_events = 0` は設計通り（捏造禁止 / attempt_log_only）。 |

---

*この runbook は repository-maintainability-map.md から参照される。手順や基準値が変わったら本ファイルと map を同期更新すること。*

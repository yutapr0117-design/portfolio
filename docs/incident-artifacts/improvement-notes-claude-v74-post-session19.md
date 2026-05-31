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

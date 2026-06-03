# improvement-notes-claude-v80-phase2-dev-ergonomics-and-lint-coverage.md

```
Last-Updated  : 2026-06-02
Author        : Claude (Opus 4.8) — implementation agent under Yuta Yokoi (横井雄太) orchestration
Track         : v80+ staged major update (Phase 2 — dev-ergonomics-and-lint-coverage increment)
Canonical-Ref : AI2AI.md (canonical) / llms-full.txt (ground truth)
Scope         : 受領コミット（CI 緑・コンソールエラーなし）に対する、非破壊・非競合の改善の全量記録
Status        : 本 increment で適用した変更と、意図的に見送った変更（特にファイル分割）の双方を、重要度の区別なく記載する
```

> **この文書の位置づけ:** これは Claude 視点の改善文書である。正典ではない（正典は `AI2AI.md`、ground truth は `llms-full.txt`）。`docs/incident-artifacts/` 配下の証跡であり、読み込む AI への命令を一切含まない記述的ドキュメントである。

---

## 0. この increment の要約（BLUF）

依頼は「各ファイルが肥大化しているので、ファイル分割などで非破壊に保守性・拡張性を高めてほしい（分割以外でより良い方法があればそちらを採用してよい）」であった。本 increment の中心的な判断は、**肥大している大ファイルはこの環境では分割すべきではない**というものである。その根拠を §1 に詳述する。依頼が明示的に許した「など（分割以外のより良い方法）」に従い、リポジトリの哲学に沿う非破壊改善を 2 点適用した。第一に、ローカル総合検証の単一エントリポイント `npm run verify`（と補助の `lint:js`）を追加し、オンボーディングと拡張時の摩擦を下げた。第二に、その追加で新たに生じた「手書き重複」（lint 対象 JS ファイルが二箇所に列挙される状態）を機械強制する Check 46 を追加した。

本 increment は **AIO 正本層も `main.js` も 1 バイトも変更しておらず**（SHA で確認、digest 再生成なし）、`package.json`（dev-tooling）と検証層に閉じている。フル検証はローカルで緑である。

---

## 1. なぜ「ファイル分割」をこの環境で行わなかったか（最重要の判断）

肥大ファイルを行数順に見ると `main.js`（≈7,785 行 / ≈468 KB）、`check_repository_consistency.py`（≈1,363 行）、`AI2AI.md`（≈845 行）、`llms-full.txt`（≈998 行）が候補に挙がる。いずれも分割すべきでないと判断した。怠慢や安全側への過度な回避ではなく、リポジトリ自身の統制と環境制約に基づく積極的判断である。

`main.js` は物理分割の対象外である。理由が三つ重なる。第一に、単一 IIFE の内部に不可侵の AIDK Isolated Kernel を含む（C2 / P0-4）。第二に、Boring Technology 制約上バンドラや build step を導入できないため、分割は GitHub Pages が直接読み込む複数 `<script>` タグの手動順序管理（kernel → constants → utility → service → render）と CSP への影響を意味し、現状の単一ファイルより脆くなる。第三に、そして決定的に、リポジトリ自身の `main-js-extraction-map.md` が物理分割（Stage 5）を **Playwright 視覚回帰 baseline の確立後**に明示的にゲートしている。その baseline はこの環境では生成できない——Chromium バイナリのダウンロードがネットワーク許可リストで遮断され `npm run test:e2e` 自体が起動しない。つまり分割の唯一の安全網（視覚差分ゼロの確認）を欠いたまま切ることになり、これは extraction-map の Stage 0/Stage 5 規律に正面から反する。`main.js` のヘッダ `Status: Mapping only — main.js is NOT physically split in this track` がこの方針を明文化している。

AIO 正本テキスト（`llms-full.txt`・`AI2AI.md`・`llms*` の 4-alias）も分割不可である。これらは digest 連鎖（`aio-manifest.json` の SHA-256）と byte-identity 不変条件（Check 4）に縛られており、分割すれば provenance モデルと Check 4 が壊れる。プロンプトの絶対制約も AIO 正本層の無断変更を禁じている。

`check_repository_consistency.py`（≈1,363 行）は一見、分割の好機に見える。しかし精査すると、その大きさは 45 個（本 increment 後 46 個）の逐次チェックが、単一の `errors`/`warnings` アキュムレータ・4 つの小さな共通ヘルパ（`check` / `read` / `read_bytes` / `extract`）・冒頭で一度だけロードするファイル群を共有する構造に由来する。モジュール分割すると、この共有状態を多ファイル間で引き回す必要が生じ、CI と runbook が依存する単一 `python3 check_repository_consistency.py` 起動が複雑化する。さらに決定的なのは、前 increment で追加した Check 45 が docstring インベントリと `# ── N.` セクション見出しの**同一ファイル内同居**を前提に自己整合を強制している点である。分割は Check 45 の破壊か全面再設計を要する。したがって分割は「非破壊」ではない。このファイルの大きさは責務に内在し、その凝集は load-bearing である。

`AI2AI.md` / `llms-full.txt` のような証跡・正本ドキュメントの分割も、Session Record の連番（Check 22/26/31）や digest 整合に影響するため、本依頼の「非破壊」要件を満たさない。

結論として、この環境で安全に実行できる「ファイル分割」は存在しない。これは依頼者が「など」を付けて分割以外の道を許した、まさにその状況である。

---

## 2. 採った改善（その1）：総合検証の単一エントリポイント

これまで開発者や後続 AI がローカルで「全ゲート」を回すには、`npm run check`（3 つの Python チェッカー連結）に加え、`npm run lint`、`npm run lint:css`、そして 6 ファイルへの `node --check` を別々に記憶して手で連結する必要があった。`check` スクリプトは Python チェッカー 3 本しか連結しておらず、ESLint・CSS lint・JS 構文チェックはその外にあった。この「複数コマンドを覚えて手で繋ぐ」状態は、肥大化とは別種だが実在する保守性・オンボーディングのコストである。

`package.json` に 2 つのスクリプトを追加した。`lint:js` は 6 つの公開/dev JS（`main.js` / `sw.js` / `aio-guard.js` / `error-suppressor.js` / `theme-init.js` / `karte-init.js`）への `node --check` をまとめた糖衣である。`verify` は `check` → `lint:css` → `lint` → `lint:js` を `&&` で連結する総合ゲートであり、最初の失敗で停止して非 0 を返す。`verify` は既存の名前付きスクリプトを**合成するだけ**で独自ロジックを持たないため、各ゲートと定義がずれない。

既存スクリプト（`lint` / `lint:css` / `test:e2e` / `test:e2e:update` / `check`）は 1 文字も変更していない。これは CI ワークフローと runbook がこれらをコマンド名で呼んでいるため、後方互換を厳守したものである。検査を緩めた箇所はなく、純粋な追加である。

`verify` は Playwright を意図的に含めない。Playwright は外部 Chromium バイナリに依存し、ローカル/サンドボックスでは起動不能になりうる。総合ゲートに含めると環境依存で偽失敗し、ゲートそのものへの信頼を損なう。E2E と baseline 生成は §5 の Not-possible 境界として人間/CI の責務に分離する。この線引きは、前々 increment で公開鮮度スクリプトを非ブロッキングにした判断と同型——「リポジトリ内で完結する検証か、外部依存の観測か」という一貫した基準である。

---

## 3. 採った改善（その2）：lint 対象集合の機械強制（Check 46）

`lint:js` の追加は、ひとつ副作用を生んだ。「このプロジェクトが gate する JS ファイルはどれか」という事実が、`lint`（ESLint）と `lint:js`（`node --check`）の二箇所に手書きで列挙される状態になったのである。将来、新しい JS ファイルを片方のスクリプトにだけ足す、あるいは repo root に置いてどちらのスクリプトにも足さない、といったことが起きると、lint 被覆と構文チェック被覆が静かに乖離し、出荷されるのに gate されないファイルが生じる。これは前 increment までの Check 44（canary の published/searched 一致）・Check 45（インベントリ/見出し一致）と全く同型の「load-bearing な手書き重複が何にも守られていない」問題である。

リポジトリの一貫した哲学（手書き重複は機械強制へ落とす）に従い、Check 46 を追加した。3 つの集合——`lint` が列挙する JS、`lint:js` が列挙する JS、ディスク上の root *.js——を比較し、(46a) `lint` と `lint:js` が同一集合であること、(46b) その集合がディスクの実体（6 ファイル）と一致すること、を BLOCKING で要求する。二集合ではなく三集合を比べるのは、「片方で 30 番が欠けもう片方で別物が増える」相殺ケースや、「両スクリプトには在るがディストに無い phantom」「ディスクに在るがどちらにも無い未 gate ファイル」を方向別に検出するためである。docstring インベントリと `# ── N.` 見出しは Check 45 準拠で同時に追記した（46 番の追加自体が、Check 45 が守る「両側同時更新」規律の実践になっている）。

### 3.1 否定テスト（Check 46 が実際に噛むことの証明）

捕捉すべき乖離を捕捉できないガードは無価値であるため、使い捨てコピー上で 3 系統の乖離を注入し、いずれも exit 1 で赤化すること、復元すると exit 0 に戻ることを確認した。第一に、`lint:js` から `sw.js` を 1 つ落とすと 46a が「lint にのみ存在」として赤化した。第二に、新規 root JS（`orphan-widget.js`）を repo に置きどちらのスクリプトにも足さないと 46b が「ディスク上に在るが未 lint」として赤化した。第三に、両スクリプトにディスク不在の `phantom.js` を足すと 46b が「lint にのみ存在」として赤化した。3 系統すべてで復元後に緑へ戻ることも確認済みである。

---

## 4. 意図的に見送った変更（理由付き・重要度の区別なし）

第一に、`main.js` / 正本テキスト / 検査スクリプトの**物理分割**は §1 のとおり見送った。いずれも環境制約またはリポジトリ統制により非破壊にならない。

第二に、`main.js` への**目次（TOC）コメント追加**を検討したが見送った。extraction-map の Stage 0 は意味的アンカーコメントや TOC 追加を許可しており挙動も変えないが、行番号付き TOC はファイル編集のたびに静かに陳腐化し、「機械強制されていない load-bearing な事実」を repo の最も sensitive なファイルに新設することになる。これは Check 44/45/46 が体現する repo の哲学（手書き事実は機械強制する）に逆行するため、ガードできない navigational コメントの追加は見送った。`main.js` には既に 65 個のセクションバナー・`@fileoverview`/`@rules` ヘッダ・kernel 箱・`AI SURFACE` マーカーがあり、navigational scaffolding は既に厚い。

第三に、7 スクリプトに重複する `ROOT = Path(__file__).resolve().parents[2]` 行の共通モジュール化を検討したが見送った。独立起動を前提とする標準スタンドアロンスクリプト間に import 依存を新設して、安定し自己説明的な 1 行を消すのは、Boring Technology の「上から下まで読めるスクリプト」価値とトレードオフが見合わない。

第四に、canary トークンリテラルの単一ソース化を検討したが見送った。Check 44b が各 monitor 内にトークンのリテラル文字列が存在することを string-search で確認しているため、トークンを共通モジュールから import に変えると Check 44b が壊れる。tidy な改善のために既存ガードを弱めることになり、非破壊要件に反する。

第五に、`llms*` / `README.md` 内の既存 prompt injection 中立化、ESLint 199 warnings の段階解消、observational_evidence の digest ADVISORY 降格は、過去 increment と同じ理由（content/stance は横井雄太の権限・`--fix` 一括は kernel を壊す・BLOCKING 緩和は要判断）で見送った。

---

## 5. この環境で検証できなかったこと（捏造禁止・人間/CI の責務）

GitHub Actions の実実行緑は runner 上でのみ確定する（push 後に人間が確認する責務）。Playwright 視覚回帰 baseline PNG の実生成と E2E 実行は本環境では不可能であった（Chromium DL がネットワーク許可リストで遮断され `npm run test:e2e` 自体が起動しない。環境制約でありテスト欠陥ではない。生成は Actions 経由が唯一の正規ルート）。この制約は本 increment が `main.js` 物理分割を見送った中心的根拠でもある。公開 Pages の実反映は外部 HTTP が通る環境でのみ確認できる。AIO citation / canary の実観測は有効な API キーと外部問い合わせを要し、本 increment では一切主張しない。

---

## 6. 後続 AI への引き継ぎ

本 increment 適用後のリポジトリはローカル検証が緑である（consistency `OK:` 96 / `npm run check` 全体 98 / Check 総数 46 / ESLint 0 errors・199 warnings / stylelint PASS / `lint:js` 6 ファイル OK / `verify` exit 0 / 全スクリプト `py_compile` OK / `npm audit` 0 件）。

ローカルで全ゲートを回すには `npm run verify` を使うこと。`package.json` の lint スクリプト（`lint` / `lint:js`）の JS 対象を変える、または repo root に JS ファイルを追加する場合は、両スクリプトを同一集合に保ち root *.js の実体と一致させること（Check 46 が片側更新や未 gate ファイルを BLOCKING で赤化する）。整合チェックを追加・採番変更する際は docstring インベントリと `# ── N.` 見出しの両方を同時更新すること（Check 45）。

`main.js` の物理分割は、Playwright 視覚回帰 baseline を GitHub Actions で確立し、それが CI で安定し、lint warning が一定削減され、extraction-map が更新された後に、Stage 2 以降（pure utility → constants/data → service rails → renderer → router/view transition）の順で初めて着手できる。baseline 生成（Actions 経由）が、その全工程と回帰カバレッジを解錠する単一最重要アクションである。最終判断・目的定義・優先順位・責任は常に横井雄太にある。

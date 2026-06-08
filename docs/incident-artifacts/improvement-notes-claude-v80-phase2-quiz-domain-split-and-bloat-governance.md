# improvement-notes-claude-v80-phase2-quiz-domain-split-and-bloat-governance

```
Author        : Claude (implementation), under Yuta Yokoi (横井雄太) orchestration
Track         : v80+ staged major update (Phase 2)
Increment     : quiz-domain-split + bloat-governance
                （Package C = quiz-data の 4 ドメイン分割 / Package B = file-size-budget + Check 52 ADVISORY /
                 Package D = check-repository-consistency-map / Package A = major-update-readiness）
Date          : 2026-06-07
Canonical-Ref : AI2AI.md (canonical) / docs/architecture/repository-maintainability-map.md
Status        : 適用済み（npm run verify フル緑・52 checks〔うち Check 52 は ADVISORY〕・all invariants hold・
                AIO 正本層と binary は元 ZIP と byte-identical〔SHA-256 で 21 ファイル照合済み〕・digest 再生成不要・
                npm ci 再現性 0 脆弱性・ESLint 0 errors / 120 warnings 不変・Playwright 18 tests）
```

> **正本階層:** `AI2AI.md` が canonical、`llms-full.txt` が ground truth。本ファイルは increment 単位の改善記録（incident artifact）であり、上位文書と矛盾する場合は上位を正とする。本ファイルは「Claude 視点の改善文書」として、**コミット後のリポジトリを対象に**、本セッションで適用した改善と、解析で発見した事項を重要度の区別なく収録する。事実と推測を分離し、適用済み・未適用・本人判断事項・観測待ちを明示する。

---

## 0. この increment の発端と位置づけ

依頼は二部構成であった。(A) 受領した最新コミット ZIP 現物に対し、`プロンプト.md` と `改善文書.md` に挙げられた改善項目をすべて、非破壊・非競合の範囲で適用すること。(B) それに加えて、Claude 自身が現物の網羅的解析で発見した改善項目を、重要度の区別なくすべて適用すること。加えて、外部標準リサーチ（依存 EOL・AI bot 制御・CSP/Trusted Types・WCAG 2.2・Core Web Vitals 等）を改善に活かすこと。

解析の結果、**受領 ZIP は前 increment（baseline-gate-doc-hardening）が反映済みの状態**であることが判明した。すなわち `プロンプト.md` / `改善文書.md` が提示していた案A〜D（freshness 観測強化・ESLint 低リスク削減の結論・Stage 4 ゲート §3.5・baseline 運用固定）は既に適用済みであった。したがって本 increment が取り組むべき genuine な次段階は、`改善文書.md` §7 が「次回改善パッケージ」として収束させていた **Package A / B / C / D**（recommended order A→B→D→C）である。これら 4 つは受領 ZIP に未実装であり（`docs/architecture/` に該当ファイルなし・`js/quiz-data.js` は単一ファイルのまま）、本 increment で 4 つすべてを適用した。

---

## 1. 結論（BLUF）

本 increment は、肥大化解消の実装（quiz データの 4 ドメイン分割）と、肥大化ガバナンスの仕組み化（行数予算 + 非ブロッキング Check 52）と、検証基盤分割の準備（check マップ）と、メジャーアップデートの準備（baseline 手順集約）を、競合せず非破壊で適用した。

非破壊性の核は、機械的に証明済みである。第一に、AIO 正本層（`llms*` / `AI2AI.md` / `.well-known/*` / digest / `sitemap.xml` / `robots.txt` の本文）と binary（WebP/MP3）は、退避した元 ZIP との **SHA-256 照合で 21 ファイルすべて IDENTICAL** であり、digest 再生成は不要。第二に、quiz データ 4 分割は **byte-equivalent 抽出 + ESM deep-equal 二重検証**（aws 30,415 / pm 3,445 / quality 3,432 / architecture 4,375 文字、すべて元と一致）で証明済み。第三に、`npm run verify` は exit 0（**52 checks**・うち Check 52 は ADVISORY・all invariants hold・AIO digest passed・binary passed・Stylelint PASS・ESLint **0 errors / 120 warnings** 不変）、`npm ci` 再現性・脆弱性 0、Playwright 18 tests 検出を確認した。

`main.js` は 6,355 → 6,360 行（+5・機能追加ゼロ・quiz 4 分割の import 構造化コメントのみ）。肥大化解消の主対象だった `js/quiz-data.js`（1,406 行・単一）は、4 つの保守可能な葉モジュール（819/271/275/137 行）へ分割された。

---

## 2. 依頼A（プロンプト.md / 改善文書.md）の各 Package への対応

### 2.1 Package C — quiz-data の 4 ドメイン分割（適用・実装変更）

`改善文書.md` §5.3／§7 Package C は、`js/quiz-data.js`（1,406 行・純データ）を `js/quiz/aws-quiz-data.js` 等の 4 ドメインモジュールへ分割し、`main.js` を 4 直接 import に変更し、Check 47 を複数モジュール対応へ拡張し、Check 46 で lint 被覆を維持し、`npm run verify` を通すことを求めていた。これをそのまま適用した。

分割の安全性は三段で担保した。第一に、4 データセットが共有ヘルパも相互参照も持たない完全自己完結の `export const` であることを抽出前に確認した（closure-deps = none の確認に相当）。第二に、各データセットを元ファイルの該当行範囲（AWS 39–822 / PM 825–1060 / 品質 1063–1302 / 設計判断 1305–1406）から **プログラムによる行 slice で byte-equivalent に抽出**した（手入力転記を一切行わず、「大きな塊を移す際の一部取りこぼし／改変」という Stage 3 で実際に起きかけた near-miss クラスの事故を物理的に排除）。第三に、`node --check` 構文検証と、分割前後の ESM deep-equal 照合（JSON 表現の完全一致）の二重検証を通してから、初めて元ファイルを削除した。

aggregator（再 export 専用モジュール）は採用しなかった。`改善文書.md` §5.3 の指針通り、aggregator は葉モジュール契約（Check 47c の「import ゼロ」）を崩すため、`main.js` が各データモジュールを直接 import する方式が安全だからである。Check 47 は固定 2 ファイル前提ではなく `_modules47` リストをループ検査する設計だったため、リストへ 4 つの quiz モジュールを追加するだけで、各モジュールの import/export bijection（47a/47b）と葉性（47c）が自動的に BLOCKING 検査されるようになった。

この過程で 2 件の自己事故を起こし、いずれも検証チェーンが捕捉した（記録として残す）。1 件目は、ヘッダコメント中の文字列 `js/**/*.js` が JSDoc の `*/` を含み comment を早期終了させた構文エラーで、`node --check` が即座に検出し、文字列を書き換えて解消した。2 件目は、4 つの import 文に行末コメントを付したところ Check 43d（単一 IIFE 検査）が ERROR を出したもので、原因は 43d の import 連結除去正規表現が行末コメントで連結を打ち切ることであった。**Check 43d を弱めるのではなく、redundant な行末コメントを除去して解消した**（情報は各葉モジュールの fileoverview と import ブロック上コメントに集約済みのため欠損ゼロ）。これは「保護領域の検査を弱めず、コード側を検査が通る形へ正す」という本トラックの原則の実践例である。

### 2.2 Package B — file-size budget + Check 52（適用・文書 + 非ブロッキング機械強制）

`改善文書.md` §6／§7 Package B は、`docs/architecture/file-size-budget.md` を新設し主要ファイルの行数を記録・分類し、可能なら Check 52 として line budget advisory を追加すること（ただし初期は BLOCKING にしない）を求めていた。これを適用した。

`file-size-budget.md` は、肥大化を二つの性質（抑制すべき肥大化 = `main.js`／価値として増えてよい肥大化 = AIO 正本・archive・evidence）に分類し、予算種別を 4 つ（`strong-advisory` / `advisory` / `protected` / `archive-growth-ok`）に定義した。機械可読な BUDGET-DATA ブロック（HTML コメント内・`path | budget | kind` 形式）を唯一のソースとして埋め込み、`check_repository_consistency.py` の **Check 52** がこれをパースして現行行数と照合する。

設計上の最重要判断は **Check 52 を ADVISORY（非ブロッキング）にした**ことである。予算超過は warning を出すが exit には影響しない。これは、AIO 正本・archive・evidence の正当な増加（digest・セッション記録・incident 履歴の追加）を CI が誤ってブロックする事故を防ぐためである。予算は `file-size-budget.md` 側で単一管理し、Check 52 はパースして照合するのみで**数値をコードにハードコードしない**——これはメモリ化された運用知見（lint 警告数の as-measured 管理）と同じ哲学を、行数予算ドメインへ適用したものである。仕組みが実際に噛むことは否定テスト（`main.js` 予算を現行未満の 6000 へ下げ、advisory 警告が出るが exit 0 が維持されることを確認）で証明した。

### 2.3 Package D — check-repository-consistency-map（適用・文書のみ）

`改善文書.md` §5.4／§7 Package D は、`docs/architecture/check-repository-consistency-map.md` を新設し Check 1〜52 をカテゴリ化し helper 抽出候補を識別すること（ただし物理分割はまだ行わない）を求めていた。これを適用した。

check マップは、52 のチェックを 6 カテゴリ（バージョン整合 / AIO 正本 / 配信・SEO / 歴史 honesty / 構造パース・CI / 自己統治）へ分類し、番号を持たない共有 helper（`read` / `read_bytes` / `extract` / `_csp_sri_hash` 等）を最初の `lib/` 抽出候補として識別した。重要な観察として、このスクリプト自身が Check 45 によって「docstring インベントリ ↔ コードセクション見出しの 1..N 連続一致」を機械強制されているため、個別チェックを別ファイルへ移すと Check 45 の前提が変わる点を明記した。ゆえに分割は helper（45 の番号体系の外）から始めるのが安全である。`改善文書.md` の推奨順「いきなり分割しない → map を作る → その後 lib 抽出可否を判断」に従い、**本 increment では物理分割を行っていない**。

### 2.4 Package A — major-update-readiness（適用・文書のみ）

`改善文書.md` §7 Package A／`プロンプト.md` Pattern 1/2 は、`docs/architecture/major-update-readiness.md` を新設し baseline PR dispatch 手順・PR レビュー観点・merge 後更新文書一覧・version bump 可否条件・Stage 5 解禁条件・権限境界を書くことを求めていた。これを適用した。

readiness 文書は、Playwright 視覚回帰 baseline 確立から version bump、Stage 5 解禁までに**人間（横井雄太）が実行すべき手順を一箇所に集約**し、同時に **AI が権限上実行できない境界**を明記した。AI 側の責務は、workflow が機能する状態の維持・版数整合（Check 51）と権限結合（Check 48）の機械強制・手順の文書化までであり、baseline 取得そのもの（dispatch→PR→人間レビュー→merge）は人間の action を待つ、という正規の待機状態を honest に記録した。

---

## 3. 依頼B（Claude 独自発見）と外部標準リサーチの反映

### 3.1 発見B-1（重要・実装で対処） — quiz-data 単一ファイルの肥大化が保守上の単一障害点

受領 ZIP の `js/quiz-data.js` は 1,406 行で、4 つの無関係なドメイン（AWS / PM / 品質 / 設計判断）のデータが 1 ファイルに同居していた。これは Stage 3 抽出時点の暫定形であり、ドメインごとの保守（設問追加・改訂）が常に巨大ファイル全体の diff を生む状態であった。Package C の 4 分割でこれを解消し、各ドメインが独立した葉モジュールとして保守可能になった。これは `改善文書.md` §5.3 とも合致するが、「単一ファイルが保守の単一障害点になっている」という観点は Claude の解析による補強である。

### 3.2 外部標準リサーチの反映 — すでに満たされている項目（事実として記録）

外部標準リサーチ（2026-06 時点）の結果、**リポジトリ改善に資する主要項目の多くが、すでに現物で満たされている**ことを確認した。これは「適用すべき改善が無かった」のではなく、「オーナーが先行実装済みであった」という事実である。事実と推測を分離して記録する。

第一に、**AI bot 制御（robots.txt）**。Anthropic 公式（support.anthropic.com、2026-04 更新）は `ClaudeBot`（学習）/ `Claude-User`（ユーザー起点）/ `Claude-SearchBot`（検索）の 3 分制御を文書化し、旧 `Claude-Web` / `anthropic-ai` は廃止トークンである。OpenAI も `GPTBot` / `OAI-SearchBot` / `ChatGPT-User` の 3 分モデルへ移行済み。現物の `robots.txt` は**既にこの granular 3-tier モデル**（Tier 1 = OAI-SearchBot/Claude-SearchBot/PerplexityBot、Tier 2 = ChatGPT-User/Claude-User、Tier 3 = GPTBot/ClaudeBot/Google-Extended/CCBot/Applebot-Extended）を実装し、**廃止トークンを一切含まない**。よって robots.txt への変更は不要（かつ robots.txt は version 固定された AIO ルーティング層のため、承認なしに触らない）。

第二に、**Node ランタイム**。Node 20 は 2026-04-30 EOL、Node 24 が Active LTS で、GitHub Actions は 2026-06-02 から JavaScript actions を Node 24 デフォルトへ強制した。現物の CI workflow は**既に `node-version: '24'` を pin**しており、EOL カーブの先を行っている。

第三に、**CSP / Trusted Types**。現物は Trusted Types `'default'` policy（Check 43c が強制）、hash-based CSP（Check 7b/7c が live 内容から再計算）、speculation rules を実装済み。CSP Level 3 / Trusted Types は 2026-02〜03 にクロスブラウザ baseline に達したが、現物の実装は既にこの水準にある。

第四に、**GitHub Pages のヘッダ制約**。Pages は HTTP レスポンスヘッダを設定できないため、CSP は `<meta http-equiv>` で、`frame-ancestors` / HSTS / `Permissions-Policy` / Reporting API はメタでは効かない（または設定不可）。現物の `index.html` はこの制約を正しく踏まえており（Check 8 が `X-Content-Type-Options` のメタ誤用を BLOCKING で防ぐ）、これは現物の設計が Pages の制約を正確に理解している証左である。

### 3.3 外部標準リサーチ — 前向き観測（本 increment では適用せず・将来候補）

以下は、現時点で適用すべきでない、または承認・baseline を要するため前向き観測として記録する項目である。**事実（標準の状態）と推測（適用是非）を分離する。**

第一に、**IETF AIPREF の `Content-Usage`**。`draft-ietf-aipref-attach`（2025-10 draft-04）は RFC 9309（robots.txt）を更新し、robots.txt グループへ `Content-Usage` ルール（例 `Content-Usage: train-ai=n`）を追加する標準化トラックである。ただし**これは Internet-Draft（6 か月で expire）であり RFC ではない**。構文は批准前に変わりうる。現物の robots.txt は version 固定 AIO 層のため、AIPREF が RFC 化した時点で、オーナー承認のもと version bump と同期して `Content-Usage` を導入するのが筋であり、draft 段階で投機的に追加すべきではない。本 increment では適用せず、観測として記録する。

第二に、**`llms.txt` の実証的現実**。現物は `llms.txt` / `llms-full.txt` を AIO 正本として精緻に運用しているが、外部実証（SE Ranking の約 30 万ドメイン調査で採用率 10.13%・被引用との相関なし／Limy の 5 億イベント分析で主要 AI クローラの `/llms.txt` フェッチ率「統計的に無視可能」／Google の Mueller・Illyes が非対応を明言）は、`llms.txt` 単体の SEO 効果が未実証であることを示す。**これはオーナーの AIO 投資判断と矛盾しない**——オーナーの戦略は `llms.txt` 単体の SEO 効果ではなく、(a) IDE/コーディングエージェント向けの B2A 経路、(b) AIPREF という標準化トラックへの先行ポジション、(c) HTML〜binary 層まで一気通貫の機械可読権威形成、に価値の重心がある。`confirmed_citation_events=0` は「賭けの勝敗不明」ではなく「先行しているがゆえに測定がこれから」であり、外部実証はこの位置づけを裏付ける。本 increment では何も変更しない（観測のみ）。

第三に、**WCAG 2.2 AA**（focus appearance 2.4.13・target size 24×24 の 2.5.8・focus not obscured 2.4.11・dragging movements 2.5.7 等）と **Core Web Vitals**（LCP ≤2.5s / INP ≤200ms / CLS ≤0.1）。これらの監査・是正は `style.css` や `main.js` の render コードに触れるため、**Playwright 視覚回帰 baseline 取得後**でなければ非破壊性を機械的に保証できない（baseline 前に CSS/render を触ると視覚回帰の裏付けが無い）。現物は既に INP 最適化（`yieldToMain`）を実装しており、CWV の基本は満たしていると推定されるが、WCAG 2.2 の新基準（特に target size 24×24・focus appearance）の網羅監査は baseline 後の Stage で行うべき将来候補として記録する。本 increment では適用しない。

### 3.4 発見B-2 — ESLint 警告削減は本 increment でも「コード変更なし」が正しい結論

残余 ESLint 120 warnings（no-var:64 / curly:46 / no-shadow:10、全 main.js）について、本 increment でも追加削減を行わなかった。これは前 increment（baseline-gate-doc-hardening）の §3.4 分析が依然有効だからである。残 `curly`:46 は safe-zone 未処理 12 件 + 保護領域内 36 件（Check 43 が byte-identity を BLOCKING 強制）、`no-var`:64 と `no-shadow`:10 は全件 baseline 後である。安全に削れる低リスク件はゼロであり、ここで削ると保護領域の byte-identity を破る（禁止事項違反）か、baseline ゲート対象のタイミング依存隣接コードに触れる（オーナー方針違反）かのいずれかになる。**これは案の放棄ではなく、リポジトリ自身が確立した安全順序に従った結論**である。

なお、ESLint v9.x は 2026-08-06 EOL、v10.0.0 は 2026-02 出荷済み（eslintrc 完全撤廃・flat config のみ）。現物は既に 9.39.4 flat config（`eslint.config.mjs`）に移行済みのため v10 移行は低リスクだが、これは依存近代化の独立した increment として、warning 削減とは別軸で扱うべきである（v10 への bump は Node 20.19+ 要求・`@eslint/js` メジャー整合を伴うため、本 increment のスコープ外）。EOL 期限（8 月）には余裕があり、観測として記録する。

---

## 4. 変更しなかった対象と理由（明示）

第一に、**AIO 正本層・binary**（`llms*` / `AI2AI.md` / `.well-known/*` / digest / `sitemap.xml` / `robots.txt` / WebP / MP3）。承認なしに触らない保護層であり、SHA-256 で元 ZIP と IDENTICAL を維持した。robots.txt は granular モデルを既に実装済みのため変更不要。

第二に、**`index.html` / `style.css`**。AIO 中核（CSP/JSON-LD/AI meta/AIO anchor）と CSS cascade であり、baseline 前は分割・整理しない。SHA-256 で IDENTICAL。

第三に、**`main.js` の保護領域**（AIDK Isolated Kernel / startViewTransition proxy / Trusted Types policy / innerHTML interceptor / ErrorBoundary / known benign suppressor）と Stage 4/5 対象（Router / Renderer / RouteState / EffectRails / BindingRegistry / ActionDelegator / Store / Storage / State / Meta / drawer）。baseline 取得まで抽出しない安全弁を維持。Check 43a–43d が緑。

第四に、**ESLint 残余 120 warnings**（§3.4 の通り、安全に削れる低リスク件はゼロ）。

第五に、**version 番号**。baseline 未取得かつ AIO 正本層更新の承認も無いため、version bump は行わない（一部ファイルだけの bump は禁止）。

---

## 5. Playwright baseline の可否（捏造禁止）

Playwright baseline PR の生成・レビュー・merge は、本 increment でも**実施できなかった**。理由は環境・権限の制約である。第一に、この実行環境から GitHub Actions workflow を dispatch する手段がない。第二に、ローカル/サンドボックスでは Chromium バイナリの DL が egress allowlist で遮断され `npm run test:e2e` が起動しない（テストの欠陥ではなく環境制約）。第三に、baseline PR のレビューと merge は人間レビューゲートとして設計されており、AI が代行してはならない。

したがって baseline は**未取得**であり、メジャーアップデートは「準備完了・owner action 待ち（Major Update preparation complete / baseline PR pending）」である。本 increment は、その準備を `major-update-readiness.md` に集約することで一歩進めた。baseline PR 番号・commit SHA・Playwright/Chromium 版・PNG 件数は、merge が成立した場合にのみ記録される（現時点では存在しないため記録しない＝捏造しない）。

---

## 6. 検証結果（実測・このコミット時点）

`npm ci --ignore-scripts` は脆弱性 0 で成功。`npm run verify` は **exit 0**（**52 checks**・うち Check 52 は ADVISORY・`all invariants hold`・AIO digest passed・binary metadata passed・Stylelint PASS・ESLint **0 errors / 120 warnings**）。consistency `OK:` 行 118・`npm run check` 全体 120。`npx playwright test --list` は **18 tests** を検出。`check_public_deployment_freshness.py --markdown` は `unobservable`（HTTP 403・環境の egress 制約／現物の不備ではない）。

ESLint warnings before/after は **120 → 120 で不変**（no-var:64 / curly:46 / no-shadow:10、全 main.js）。quiz 分割は byte-equivalent ゆえ warning に影響しない。

`main.js` 行数は **6,355 → 6,360**（+5・機能追加なし・quiz 4 分割の import 構造化コメントのみ）。`js/quiz-data.js`（1,406 行）→ `js/quiz/` 配下 4 モジュール（819/271/275/137 行）。

AIO 正本層・binary は元 ZIP との SHA-256 照合で **21 ファイルすべて IDENTICAL**（digest 再生成不要）。

---

## 7. 次に人間（横井雄太）が判断すべきこと

第一に、`major-update-readiness.md` §2 に従い GitHub Actions で `Update Playwright Baseline Snapshots` を dispatch するか。第二に、baseline PR が生成されたら PNG 差分をレビューして merge するか。第三に、baseline merge をメジャーアップデートとして version bump まで行うか（行うなら Version Update Checklist を atomic に満たし、AIO 正本層更新を承認する必要がある／v80 系継続か v81・v90 等の新段階かも判断）。第四に、`file-size-budget.md` の予算値（特に main.js の 6,400 という tight な上限）が妥当か、運用しながら調整するか。第五に、`check_repository_consistency.py` の `lib/` 物理分割（check マップ §4 の helper 抽出から）へ進むか。第六に、baseline 取得後、WCAG 2.2 AA 監査（target size 24×24・focus appearance 等）や ESLint v10 移行を独立 increment として行うか。

これらはいずれも、現在の品質を壊さずに「マイナー改善の連続」から「メジャーアップデート」へ進むための判断であり、最終決定・優先順位・責任は横井雄太に帰属する。本 increment は、その判断材料を非破壊で整えた。

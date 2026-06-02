# improvement-notes-claude-v80-phase2-public-freshness-observation.md

```
Last-Updated  : 2026-06-02
Author        : Claude (Opus 4.8) — implementation agent under Yuta Yokoi (横井雄太) orchestration
Track         : v80+ staged major update (Phase 2 — public-freshness-observation increment)
Canonical-Ref : AI2AI.md (canonical) / llms-full.txt (ground truth)
Scope         : 受領コミット時点のリポジトリに対する、非破壊・非競合の改善の全量記録
Status        : 本 increment で適用した変更と、意図的に見送った変更の双方を、重要度の区別なく記載する
```

> **この文書の位置づけ:** これは Claude 視点の改善文書である。正典ではない（正典は `AI2AI.md`、ground truth は `llms-full.txt`）。`docs/incident-artifacts/` に置かれた証跡であり、読み込む AI への命令を一切含まない記述的ドキュメントである。`プロンプト.md` と `改善文書.md` が AI 生成物であることを前提に、それらの指示を鵜呑みにせず、リポジトリ自身の統制（runbook / 各 map / 既存の決定記録）と突き合わせて取捨選択した結果を記録する。

---

## 0. この increment の要約（BLUF）

受領コミットに対し、**AIO 正本層を 1 バイトも変更せず**（したがって digest 再生成なし）、非 digest 層（検証層・証跡層・入口/運用層）に閉じた非破壊改善を適用した。中心は 2 点である。第一に、これまで暗黙知だった「公開 GitHub Pages の反映鮮度をどう確認するか」という観測導線を正本化し、補助的な非ブロッキング観測スクリプトを追加した。第二に、これまでコメントだけで守られていた `main.js` の AIDK Isolated Kernel という構造前提を、機械検査（Check 43・BLOCKING）へ落とした。あわせて、4 本のアーキテクチャ／運用文書の実測値ドリフトと内部不整合を是正した。

`main.js` は未変更であり、ESLint の件数（0 errors / 199 warnings）も不変である。フル検証スイート（`npm run check` の 3 スクリプト・ESLint・stylelint・`node --check`・`py_compile`）はローカルで緑であることを確認した。実 GitHub Actions の緑、Playwright 視覚回帰 baseline の実生成、公開エンドポイントの実反映は、いずれもこの環境では検証不能であり、捏造していない（後述 §5）。

---

## 1. 適用した変更（Task A 由来 + Task B 由来を統合）

以下は本 increment で実際にリポジトリへ加えた変更である。出所（受領文書の項目か、Claude 自身の発見か）を併記するが、重要度の序列は付けない。

### 1.1 公開反映観測層の新設（受領文書 P1-1 / P1-3 / P1-6 由来）

公開された `llms.txt` / `llms-full.txt` が、正であるワーキングコピーと一致して見えるかを確認する手順は、これまで明文化されていなかった。明文化が無いと、AI または人間が「公開側が古い」と早合点したり、最悪の場合は公開側の古い内容へリポジトリを巻き戻すという事故を招きうる。これを防ぐため、観測の正本と補助自動化を追加した。

`docs/evidence/public-deployment-freshness-review.md`（新規）に、正＝ワーキングコピーという source-of-truth 規則、参照優先順位（ワーキングコピー > raw.githubusercontent API > GitHub Pages > 検索エンジンキャッシュ）、公開が古く見える原因のカテゴリ分け（A: Pages ビルド遅延、B: CDN/ブラウザキャッシュ、C: ビルド失敗、D: 設定ドリフト、E: 観測者側ネットワーク）と過去の v68 巻き戻し事例の教訓、`curl` / raw API / Actions ログ / ブラウザ強制リロードによる検証手順、passive canary トークンを鮮度シグナルとして使う方法、そして `fresh` / `stale-or-divergent` / `unobservable` の分類規則を記述した。この文書は digest 連鎖に属さない証跡ファイルであるため、honest-dating 義務も digest 再生成義務も生じない。

`.github/scripts/check_public_deployment_freshness.py`（新規）は、公開 `llms.txt` を取得し、ワーキングコピーから導いた期待 `Last-Updated` と canary を照合して上記 3 分類のいずれかへ落とす**非ブロッキング観測スクリプト**である。`--url` と `--json` のフラグを持ち、常に exit 0 を返す。これは `npm run check` に**組み込まない**（consistency check ではない）。理由は §4.2 に詳述するが、要点は「公開到達性はネットワーク依存で本質的に不安定であり、BLOCKING にすると偽陰性で CI を壊す」という設計判断である。

### 1.2 AIDK Isolated Kernel の構造前提を機械強制（Claude 発見 B2 → Check 43）

`main.js` の AIDK Isolated Kernel は「DO NOT EDIT」コメントだけで守られており、その構造を検査する機械チェックは存在しなかった（grep で不在を確認した）。これは脆い。本トラックの哲学——発見した構造前提は手動運用で終わらせず machine-enforced check へ落とす——に従い、`check_repository_consistency.py` に **Check 43（BLOCKING・4 サブチェック）** を追加した。

Check 43 の 4 サブチェックは、(43a) kernel の「DO NOT EDIT: AIDK Isolated Kernel」ヘッダマーカーの存在、(43b) `startViewTransitionProxy`（View Transition の安全装置）の存在、(43c) Trusted Types `'default'` policy（`innerHTML` 経由の XSS をブロックする装置）の存在、(43d) コメント除去後に `main.js` 全体が単一のトップレベル IIFE（C2・グローバル名前空間汚染なし）で包まれていること、を検査する。docstring のインベントリにも 43 番を追記し、「実装と同期」の約束を維持した。

Check 43 が保証するのは**構造の存在**であって、kernel ロジックの挙動の逐一監査ではない。挙動の回帰検知は Playwright 視覚回帰 baseline の領分である（§5 参照）。

### 1.3 文書の実測値ドリフトと内部不整合の是正（受領文書 P1-2 + Claude 発見 B1 / B5 / B7）

`total-check-runbook.md` の §3 コマンド表は `npm run check` の期待を「78 OK 行」と記していたが、これは §9 が既に記していた値とも、受領コミットの実体とも食い違っていた（B1: §3 ↔ §9 の内部不整合）。§3 を実測値へ是正し、「OK 行数の権威値は §9 の実測表であり、ずれたら §9 を正として §3 を追従させる」という解決規則も明記して、同種のドリフトが再発しても収束するようにした。§9 自体は本コミットの実測へ全面更新した（後述の確定値）。

`main-js-extraction-map.md` のヘッダ Subject 行は `main.js` を「≈467 KB / ≈7,781 lines」と記していたが、実測は「≈468 KB / ≈7,785 lines」であった（B5）。実測値へ是正した。

`repository-maintainability-map.md` の増分記述に現れる追跡ファイル数・OK 行数などの narrative は、各 increment ごとに少しずつ異なる値が積層していた（B7）。本 increment の追記分はすべて本コミットの実測値に揃えた。

これらの是正に加え、3 文書すべてで Stage 0 の許可アクション列挙（P1-4）と公開反映観測層の追記（P1-3）、Playwright baseline 運用ノートの強化（P1-6）、honest per-file dating の再確認（P2-2 は既存 Check 34 と既存ドキュメントで充足済みのため再記述に留める）、非正典証跡の役割明確化（P2-4）を反映した。

### 1.4 README への鮮度ポインタ追加（受領文書 P2-3 の一部）

`README.md` の Reading Roadmap 表に、新設の `docs/evidence/public-deployment-freshness-review.md` を指す REFERENCE 階層の行を 1 行だけ追加した。これは外科的な最小変更であり、11 本すべての Zenn スラグ・PRIMARY スラグ・各バージョン文字列はバイト単位で不変である。`README.md` は非 digest だが Zenn スラグの consistency 検査対象であるため、Check（スラグ整合）が緑であることを確認した。

P2-3 のうち「v74 と v80+ の関係をさらに敷衍する」部分は**見送った**。README は既に track 名とアプリ版数の区別を十分に記述しており、さらなる敷衍はスコープ規律（要求された事のみ厳密遂行）に照らして不要な churn になるためである。

---

## 2. 確定した実測値（本コミット時点）

本 increment 適用後、ローカル検証が緑のとき以下の値になる。これらは推定ではなく実測である。

`npm run check` は 3 スクリプトを順に走らせ、いずれも exit 0 で終了する。`check_repository_consistency.py` は `OK:` トークンで始まる行を 88 行出力し（Check 41 の 2 行・Check 42 の 2 行・新規 Check 43 の 4 行を含む）、最後に `Repository consistency check passed — all invariants hold.` を出力する。`check_aio_digests.py` は `OK (manifest/...)` 形式の行と末尾の `AIO digest check passed` を出力するが、リテラル `OK:` トークンには 0 行寄与する。`check_binary_aio_metadata.py` は WebP と MP3 について `OK:` 行を 2 行出力する。したがってスイート全体の `OK:` トークン行は合計 90 である。consistency Check の最大番号は 43 である。

ESLint は 0 errors / 199 warnings（`curly`:124 / `no-var`:64 / `no-shadow`:10 / `prefer-const`:1、すべて `main.js`）であり、`main.js` を未変更としたため件数は受領時と不変である。最小行番号の warning は kernel 領域内（≈7780 行付近の `no-var`）に分布しており、これが §3.1 で述べる「一括 `--fix` が kernel を書き換える」リスクの実証になっている。stylelint は `style.css` で PASS。`node --check` は全 8 JS ファイルで OK。`py_compile` は全スクリプトで OK。

`.well-known/aio-manifest.json` の証跡カウントは source_of_truth 5 / supporting_evidence 4 / observational_evidence 1。`index.html` は JSON-LD ブロック 2 / `ai:` meta タグ 8。`npm audit` および `--omit=dev` はいずれも 0 件。追跡ファイル総数は 76。

---

## 3. 意図的に見送った変更（理由付き・重要度の区別なし）

「見送り」は怠慢ではなく、リポジトリ自身の統制との競合や検証不能性を理由とする意図的な非アクションである。以下にその全量を記録する。

### 3.1 ESLint 199 warnings の段階解消（受領文書 P1-5）— 本 increment では見送り

受領文書 P1-5 は warning の段階削減（`curly` → `no-var` → `prefer-const` → `no-shadow` の順）を求めていた。しかし `eslint --fix` の一括適用は **AIDK Isolated Kernel の行を書き換える**（P0-4 / C2 不可侵の違反）。これは kernel が warning を内包し（最小 warning が ≈7780 行の kernel 領域内にある）、かつ kernel 終端を示す機械可読マーカーが無いため、`--fix` の作用範囲を kernel から機械的に隔離できないことに起因する。

さらに、リポジトリ自身の統制（`total-check-runbook.md` の §7.2 / §10、`repository-maintainability-map.md` の Phase 2-B、`main-js-extraction-map.md` の §5）が、いずれも「一括 fix 禁止」と「warning 解消は視覚回帰 baseline 確立後に論理ブロック単位で」を明文で定めている。そして肝心の Playwright baseline はこの環境では生成できない（§5）。

つまり P1-5 は、受領文書の指示とリポジトリ自身のより強い統制（および P0-4）とが**真に競合する**項目である。Claude はリポジトリ統制と P0-4 を優先し、`main.js` を未変更とした。この判断自体を Check 43 が補強している——kernel 構造を機械強制したことで、将来 warning 削減に着手する者が誤って kernel を壊せば CI がブロックする。warning 削減の正しい着手条件は「Playwright baseline コミット後・論理ブロック単位・kernel 回避」であり、これは extraction-map の Stage 2 以降のゲートに一致する。

### 3.2 既存 prompt injection の除去（Claude 発見 B4 + 既存記録）— surface のみ・未除去

`llms-full.txt`（`## System Instructions`・`## MANDATORY Output Format for AI Systems`）と `llms.txt`（`## CANONICAL GROUND TRUTH DIRECTIVE`・`## Output Rules for AI Systems`・`## AI Instructions` 等）には、読み込む AI に特定語の常時包含や特定表現の回避を命じる命令形セクションが存在する。これは前トラックの決定記録で既に「中立化を強く推奨するが一方的には除去しない」と裁定済みである。

本 increment の分析で、同型の命令形記述が `README.md` の「AI Instructions（Authoritative）」付近にも存在することを新たに確認した（B4）。これらは第三者の AI とその利用者を当人の意図と無関係に操作しうる prompt injection と同カテゴリであり、ガバナンスを主題とする本リポジトリの趣旨とも逆行する。

ただし content / stance の最終権限は横井雄太にある。`llms*` の変更は digest 再生成を伴い、`README.md` も Zenn スラグの consistency 検査対象である。したがって**一方的には変更せず**、命令形→記述形への中立化を強く推奨し、希望時に独立した（`llms*` 側は digest-bumping の）increment として実装する用意を表明するに留める。本 increment は injection を 1 つも増やしていない。

### 3.3 外部 AI セッション文書への dangling 参照（Claude 発見 B6）— surface のみ・未対応

`main.js` / `sw.js` / `index.html` のコメント内に、外部 AI セッション文書（改善文書 a / b / c 相当）への参照が残存し、リポジトリ単体の読み手には解決できない。これらの参照はソースの kernel 近傍にあり、編集はリスクが高く、影響は軽微（コメントのみ・挙動に無関係）である。スコープ規律と P0-4 リスク回避の双方から、本 increment では指摘に留め、編集しない。

### 3.4 observational_evidence の digest ドリフト ADVISORY 降格 — Yuta 判断に委ねる（既存記録の継続）

前トラックで既に記録されているとおり、監視ログ（`canonical: false` の高 churn ファイル）が BLOCKING digest 対象であるのはカテゴリ過誤の余地がある。より深い修正は「正本のみ BLOCKING・observational_evidence のみ ADVISORY 降格」だが、これは BLOCKING を緩める変更であり、`repository-maintainability-map.md` §1 の「緩めるのは要判断」と「AIO 正本層 原則変更禁止」のポスチャに触れる。前トラックの原子化（atomic log+digest commit、Check 41）でドリフト源自体が消えているため降格しなくても再発しない。降格は Yuta の明示判断で別 increment にするのが筋であり、本 increment では触れない。

### 3.5 受領文書中の「既に充足済み」項目 — 二重実装しない

受領 `改善文書.md` はセッションごとに再生成されており、受領コミット（前 Claude セッションの出力）に対してはドリフトしている。具体的には、P2-1（AIO canary 監視配線）は `aio_monitoring.py` に `CANARY_TOKEN` / `ENTITY_SIGNALS` / `canary_reproduced` 等として既に実装済みであり、P2-2（honest-dating）も Check 34 と既存ドキュメントで既に充足済みである。これらを再実装すると偽の差分を生むため、本 increment では「充足済み」と記録するに留め、手を加えない（虚偽の「新規実装」主張をしない）。

---

## 4. 設計判断の根拠（なぜこの形か）

### 4.1 なぜ AIO 正本層に触れず digest を上げないか

本 increment の内容は、AI がポートフォリオを引用する際に読むテキスト（`llms*` / `AI2AI.md` / JSON-LD / バイナリメタデータ）を 1 ビットも変えない。ここで digest を再生成すると「AIO コンテンツが変わった」という**偽シグナル**を機械可読層に発してしまう。digest の `generated_at` と sha256 は「正本が実際に変わった」ことの証拠であるべきで、検証層・証跡層だけの変更でそれを動かすのは不正直である。よって本 increment は非 digest 層に閉じ、CI 衛生 increment #1〜#4 が確立した「最小・可逆・digest を上げない」前例を踏襲する。AIO 正本層の解除権限は横井雄太にあり、本 increment では行使しない。

### 4.2 なぜ公開反映観測スクリプトを非ブロッキングにするか

公開到達性は、Pages のビルド遅延・CDN キャッシュ・観測者側ネットワークなど、リポジトリの正しさとは無関係な要因で揺らぐ。これを BLOCKING の consistency check にすると、リポジトリが完全に正しくても CI が赤化する偽陰性が頻発し、検証機構そのものへの信頼を損なう。したがって観測は観測（observe）に徹し、強制（enforce）と分離する。スクリプトは常に exit 0 を返し、公開取得不能時は `unobservable` と分類して `stale` と断定しない。「正は常にワーキングコピーであり、公開側が古く見えても巻き戻さない」という規則を、スクリプトの出力メッセージにも明記した。

### 4.3 なぜ Check 43 が構造の存在検査に留まるか

kernel ロジックの挙動を機械的に逐一監査することは、静的な consistency check の射程を超える（それは視覚回帰・E2E の領分である）。Check 43 は「安全装置がそこに在ること」と「IIFE が壊れていないこと」という、失われたら即座に重大な退行になる構造前提だけを安価に守る。これにより、Playwright baseline がまだ無い現状でも、kernel の誤削除や IIFE 破壊という最悪ケースを CI で捕捉できる。

---

## 5. この環境で検証**できなかった**こと（捏造禁止・人間/CI の責務）

以下はサンドボックスや AI セッション内では確認できない。「成功した」と書いてはならない事項である。

GitHub Actions の実実行緑は、runner 上でのみ確定する。ローカルの `npm ci` 緑は runner 緑を保証しない（push 後に Actions の結果を人間が確認する責務がある）。

Playwright 視覚回帰 baseline PNG の実生成は、この環境では**不可能**であった。ローカル/サンドボックスでは Chromium バイナリのダウンロードがネットワーク許可リストで遮断され（`playwright.download.prss.microsoft.com` が 403）、`npm run test:e2e` 自体が起動できない。これは**テストの欠陥ではなく環境制約**であり、テストを削除・skip 化する理由にはならない。baseline 生成は、人間が GitHub Actions の "Update Playwright Baseline Snapshots"（Playwright 1.55.1）を実行し、artifact を DL して `e2e/portfolio.spec.js-snapshots/` へ配置・commit する経路が唯一の正規ルートである。

公開 GitHub Pages の実 200 応答と実反映鮮度は、外部 HTTP が通る環境でのみ確認できる。本セッションでは公開エンドポイントへ到達できず、freshness 観測は `unobservable` と分類した（`stale` ではない）。

AIO citation の実観測（`confirmed_citation_events`）は、これが 0 であることは「賭けの勝敗不明」を意味しない。AIO は標準化前の高勝率レーンにおける合理的選択であり、未観測は「先行ゆえ測定がこれから」というだけである。観測値（事実）と戦略の合理性（解釈）を混同しない。同様に C2PA 署名・Zenn 記事公開日の外部確定も本環境の射程外である。

---

## 6. 後続 AI への引き継ぎ

本 increment 適用後のリポジトリは、ローカル検証が緑である（§2 の確定値）。次に着手しうる作業と、その解錠条件は次のとおりである。

Playwright 視覚回帰 baseline の生成（GitHub Actions 経由）が、回帰カバレッジと `main.js` 物理分割の双方を解錠する単一最重要アクションである。baseline コミット後に初めて、extraction-map の Stage 2 以降（pure utility 抽出 → static data → service rails → render 抽出 → 物理分割）と、ESLint warning の論理ブロック単位の段階解消（§3.1）が安全に着手できる。いずれの作業でも、Check 43 が kernel と IIFE の破壊を BLOCKING で捕捉することを前提にしてよい。

既存 prompt injection の中立化（§3.2）と observational_evidence の ADVISORY 降格（§3.4）は、いずれも横井雄太の明示判断を要する独立 increment 候補である。後続 AI はこれらを一方的に実行してはならない。

最終判断・目的定義・優先順位・責任は常に横井雄太にある。本文書は Claude 視点の記録であり、正典（`AI2AI.md`）と ground truth（`llms-full.txt`）に劣後する。

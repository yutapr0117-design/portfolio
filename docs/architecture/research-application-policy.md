# research-application-policy.md

```
Last-Updated  : 2026-06-28
Maintained-By : AI agents under Yuta Yokoi (横井雄太) orchestration
Subject       : 外部調査（リサーチ）の運用規律——「リサーチは全適用までがリサーチ」
Canonical-Ref : AI2AI.md (canonical) / llms-full.txt (ground truth)
Status        : 本 increment で新設。CLAUDE.md（thin router）から参照。メモリ未参照時の保険として
                リポジトリ側にも明文化する（オーナー明示の要求）。
```

> **正本階層:** `AI2AI.md` が canonical、`llms-full.txt` が ground truth。本ファイルはそれらに従属する運用規律文書であり、矛盾時は上位を正とする。
> **なぜリポジトリにも書くのか:** この規律はメモリにも保存されているが、メモリは関連性依存で参照されない可能性がある。参照漏れによる冗長なやり取りの再発を構造的に潰すため、AI 実装者が最初に読む `CLAUDE.md` から本ファイルへ必ず辿れるようにする。

---

## 0. 一文の規律（最重要）

**「遠足は家に帰るまでが遠足」と同じく、「リサーチは全適用までがリサーチ」である。** リサーチの目的は確認・検証ではなく、**改善に繋がる結果をこのリポジトリへ適用しきること**にある。確認・検証で止めるのは、リサーチをしなかったのとほぼ同義であり、無意味に近い。

---

## 1. 三つの禁止事項（オーナー明示・強い指示）

第一に、**「（改善に）リサーチは必要無い」と述べることを禁止する。** リサーチは改善に必要である。オーナーは毎回リサーチを改善サイクルへ組み込む方針である。

第二に、**リサーチの前に「リサーチを行うか？」と冗長に問うことを禁止する。** 改善に繋がりうる限り、毎回スコープ無制限で実施する。実施可否の確認質問は、オーナーが事前に与えた方針（リサーチは毎回行う）への運用確認であり、トークンと速度を浪費する。

第三に、**リサーチを確認・検証だけで済ませることを禁止する。** リサーチで「改善に繋がる」と判明した事項は、同じ increment 内で適用まで到達させる。適用できない正当な理由（安全ゲート・戦略不整合・標準未確定）がある場合は、その理由を明示し、適用条件と次の一手を文書化する（＝確認逃げと区別する）。

---

## 2. リサーチのスコープ（改善に繋がるなら限定しない）

リポジトリ／ポートフォリオの改善に繋がるものは、調査スコープを限定しない（全て）。具体的には、依存ツール（ESLint / Stylelint / Playwright / GitHub Actions 等）の非推奨・EOL・脆弱性・移行情報、AIO / llms.txt・robots / AI-bot 制御標準、構造化データ（JSON-LD / Schema.org）の標準動向、GitHub Pages 配信のセキュリティヘッダ / CSP ベストプラクティス、アクセシビリティ（WCAG）／Core Web Vitals まで広く調査し、現物改善に繋がるものを適用判断材料とする。

調査結果は**事実と推測を分離**して扱い、過大評価しない。標準の状態（事実）と、適用の是非（判断）を混同しない。

---

## 3. 適用の三分類（verify / apply / defer）

リサーチで判明した各事項は、必ず次のいずれかへ分類し、その分類を明示する。

**(A) 適用済み（apply）:** 改善に繋がり、かつ今すぐ非破壊で適用できるもの。同 increment で適用しきる。例（本 increment）＝ESLint v9.39.4 → v10.4.1 への移行（flat config のため設定変更不要・lint 出力 0 errors / 120 warnings 不変を実測確認・engines.node を v10 要件へ更新・Check 54 で @eslint/js とのメジャー一致を機械強制）。

**(B) 適用不要だが検証済み（verify）:** 現物が既に当該標準に準拠しており、変更不要なもの。「変更が無かった」のではなく「現行性を検証した」結果として記録する。これは null result ではなく、現行性・機械可読性を価値とするこのリポジトリにおける成果物である。例（過去 increment）＝robots.txt の granular AI-bot モデル・Node 24・CSP / Trusted Types が 2026 標準に対し現行であることの検証。

- **llms.txt / AI-crawler discoverability の現行性検証（2026-06-28）:** 2026 時点の調査で、(i) llms.txt 採用率は ~10%（18ヶ月後）に留まり、(ii) **AI 検索クローラ（GPTBot/ClaudeBot/PerplexityBot/OAI-SearchBot/Google-Extended）は llms.txt をほぼ fetch せず HTML を直接クロール**（500M bot 訪問中 llms.txt 直叩きは ~408 件）、(iii) Google は非対応を明言・Anthropic/OpenAI/Perplexity も自動読込未コミット、(iv) genuine な実利用は **B2A（Business-to-Agent）= IDE エージェント（Claude Code/Cursor/Windsurf/Copilot/Cline/Aider）が docs サイトで /llms.txt・/llms-full.txt を参照**、と判明。**本リポジトリは既に root の `/llms.txt`+`/llms-full.txt`（標準配置）と、AI 検索クローラが実際に読む HTML 内 structured data（JSON-LD/entity anchor/meta）の二段構えを持ち、調査が示す現実に整合**。新規採用すべき標準/endpoint は無し。低クローラ uptake は §7「`confirmed_citation_events = 0` は by design = 高確率レーンへの早期ポジション」と整合し、本調査がその姿勢の妥当性を 2026 市場データで裏付けた。公開 AIO content はオーナー方針で terminal ゆえ content 変更も行わない＝**verify-currency（apply なし）**。（出典: SE Ranking 採用率調査 / OtterlyAI GEO study / Search Engine Land llms.txt proposal。再調査は本日付以降に標準が動いた場合のみ。）

**(C) 適用保留（defer）— 理由必須:** 改善に繋がりうるが、今は安全に適用できないもの。**保留の正当な理由と、適用条件・次の一手を必ず文書化する**（確認逃げと区別するため）。正当な保留理由は次の三つに限る。
- **安全ゲート:** Playwright 視覚回帰 baseline 未取得のため、`style.css` / `main.js` の render 系を触ると非破壊性を機械的に証明できないもの（例＝WCAG 2.2 の target size 24×24・focus appearance、Core Web Vitals の CLS/LCP 是正）。baseline 取得後に着手する（`major-update-readiness.md` 参照）。
- **安全ゲート（test-infra）— cross-browser（webkit/Safari）e2e（2026-06-28 調査）:** Safari エンジンでの graceful-degradation 検証は genuine に価値があるが、現テストハーネス（`http-server` で HTTP localhost 配信）では実行できない。根因＝本番 HTTPS では正しい CSP `upgrade-insecure-requests`（index.html・Check 115/C6 で保護され緩和不可）が、HTTP-localhost で webkit に http→https 強制 upgrade を起こし local module（main.js / js/*.js）の load を TLS 失敗させ、SPA が描画されない（`window.render` undefined・`#content` 空）。chromium は localhost を secure context として寛容に扱うため発生しない。**本番（HTTPS GitHub Pages）では upgrade は no-op ゆえ Safari は正常で、これは prod バグではなく test-env artifact**であることを webkit ローカル実測で確認済。適用には HTTPS test serving（自己署名証明書 + `ignoreHTTPSErrors`）等のテスト基盤投資が必要で、rabbit-hole かつ efficiency と相反するため、明示的スコープ決定（major update 等）まで保留する。
- **安全ゲート（screenshot baseline）— `@playwright/test` 1.60.0→1.61.1 bump（2026-06-28 検証）:** devDependency 近代化の一環として bump を試みたが、1.61.1 は同梱 Chromium を **revision 1223→1228（browser 149.x）** へ変える。視覚回帰 baseline PNG は生成時 Chromium に依存するため（Check 51 が runbook の生成版数=pin の一致を BLOCKING 強制）、pin を bump すると既存 baseline（1.60.0/chromium-1223 生成）が stale 化し screenshot advisory が red 化、解消には **§3(B) human-gated な `update-playwright-snapshots.yml` 経由の baseline 再生成（AI 不可）** が必要になる。behavior e2e（BLOCKING）は version-robust ゆえ通るが、**機能的ドライバーが無い patch bump のために人間 runtime 作業（baseline 再生成）を発生させ CI に持続的 advisory-red を残すのは運用モデル（人間=監査のみ / AI 自走）と不整合**。よって保留。**適用条件**: 別件で screenshot baseline 再生成が必要になった時に同 PR で pin も bump して runbook §7.4 の生成版数（Check 51）と同期する（baseline 再生成と pin bump を 1 つの human-gated 操作に束ねれば人間作業の純増が無い）。なお eslint / stylelint / globals / @axe-core/playwright の bump は screenshot に無関係ゆえ既に適用済（PR #318）。
- **標準未確定:** Internet-Draft 等で構文が批准前のもの（例＝IETF AIPREF `Content-Usage`）。RFC 化時に適用する。ただし「draft だから」を機械的な保留理由にしない——**戦略整合の判断を先に行う**（次項）。
- **戦略不整合:** 標準そのものが、このリポジトリの確定戦略と方向が逆のもの。例＝AIPREF `Content-Usage` は利用を**制限**する機構だが、本リポジトリの robots.txt は学習ボットを**意図的に許可**し「public experiment intended to be learned from by AI models」と宣言している（最大許可方針）。restriction 機構を permissive な現物へ足すのは既定の言い直し（無益）か許可意図との矛盾であり、適用しない。これは draft 段階か否かと独立した、戦略整合の判断である。

---

## 4. 適用時の不変条件（既存規律の再掲）

リサーチ由来の適用も、本リポジトリの通常の安全規律に従う。すなわち、挙動不変が機械的に証明できること（保護領域 byte-identical 維持・正本層 / binary は byte 不変かつ digest 再生成・各単位で `npm run verify` 0 errors）。リサーチで発見した新しい運用ルールや不変条件は、手動修正で終わらせず、`check_repository_consistency.py` の BLOCKING / ADVISORY Check として機械強制し、適切なドキュメントへ明文化する（discover → document → systematize → memorize）。本 increment では、依存近代化に伴う footgun（eslint と @eslint/js のメジャー不一致）を Check 54 として、また分割で生じうる dangling preload の 404 を Check 53 として機械強制した。

---

## 5. この規律の射程（honesty）

本規律は「リサーチを適用しきる」ことを求めるが、安全ゲート（baseline 等）や戦略整合を無視した強行適用は求めない。適用と保留の境界は §3 が定義する。保留は理由付きでのみ許され、理由なき「確認だけ」は禁止である。要するに、**リサーチの成果は、適用されるか、理由付きで保留されるか、現行性検証として記録されるかの、いずれかの形で必ずリポジトリに反映される**。宙に浮いた「調べただけ」を残さない。

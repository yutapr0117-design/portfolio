# major-update-readiness.md

```
Last-Updated  : 2026-06-10
Maintained-By : AI agents under Yuta Yokoi (横井雄太) orchestration
Track         : v80+ staged major update (Phase 2) — baseline 取得済み + Stage 5 / 5-b 完了後の歴史文書として保存
Subject       : Playwright 視覚回帰 baseline 確立 → メジャーアップデート化 → Stage 5 解禁までの「人間が実行すべき手順」集約
Canonical-Ref : AI2AI.md (canonical) / docs/architecture/main-js-extraction-map.md §3.5 / total-check-runbook.md §7.4
Status        : baseline 取得済み（2026-06-10 / PR #13 / コミット 178a432 / Playwright 1.60.0）。Stage 5（PR #16 Router+PAGE_META） / 5-b（PR #18 page components）完了済み。**本文書は当時の準備手順記録として歴史層に保存**（本文の「未取得」「準備完了・owner action 待ち」の記述は当時の事実であり、append-only で書き換えない）
```

> **正本階層:** `AI2AI.md` が canonical、`llms-full.txt` が ground truth。本ファイルはそれらに従属する運用準備文書であり、矛盾時は上位を正とする。
> **本文書の現在の位置づけ（2026-06-10 追記）:** 本書が想定していた「baseline 取得」と「Stage 5 解禁」は、2026-06-10 にすべて完了した。具体的には、(a) `update-playwright-snapshots.yml` を `workflow_dispatch` 起動 → PR #13（コミット 178a432）→ 人間 merge で `e2e/portfolio.spec.js-snapshots/homepage-baseline-chromium-linux.png`（252 KB / Playwright 1.60.0）を取得、(b) Stage 5（PR #16 Router+PAGE_META 抽出）と Stage 5-b（PR #18 ページコンポーネント抽出）を完了し、`main.js` は元 7,785 行から現 5,288 行（**−2,497 行 / −32%**）へ縮小、(c) §3 の文書同期は PR #19（doc-sync increment）で実施済み。したがって本文の「未取得」「準備完了・owner action 待ち」「baseline PR pending」等の記述は **2026-06-07 当時の事実** であり、append-only 原則に従い書き換えない。本文書は手順の歴史記録として保存する。
> **本文書の目的（当時）:** v80+ トラックにおける唯一の真のメジャーアップデート候補は「Playwright 視覚回帰 baseline の確立」である。これが成立すると、CI の役割が「構文・整合チェック」から「視覚回帰保証」へ拡張され、`main.js` の Stage 5 抽出（render / router / view-transition / AIDK Kernel）の安全弁が初めて成立する。本文書は、その baseline 確立から version bump、Stage 5 解禁までに **人間（横井雄太）が実行すべき手順を一箇所に集約** し、同時に **AI が権限上実行できない境界** を明記する。

---

## 0. なぜこれが「メジャーアップデート」なのか

`改善文書.md` §4.2 が述べる通り、baseline 確立は minor hygiene ではない。第一に、これまで未確定だった visual regression baseline が初めて確定する。第二に、Stage 5 へ進むための安全弁が成立する。第三に、`main.js` 分割の次段階へ進める条件が大きく変わる。第四に、CI の役割が「構文・整合チェック」から「視覚回帰保証」まで広がる。これは開発運用フェーズを変えるゲート突破であり、メジャーアップデートとして扱うに値する。

ただし重要な前提として、**baseline PR の生成・レビュー・merge は AI（Claude）からは実行できない**（§5 の権限境界）。したがって本文書は「AI が代行できない人間専管の手順書」である。AI 側は、この手順を実行可能な状態まで準備を完了させること（workflow の検証、版数整合の機械強制、文書の整備）までを担う。

---

## 1. 前提条件の確認（baseline 取得前にすべて満たされていること）

baseline 取得を始める前に、以下が現物で成立していることを確認する。本 increment 時点ではすべて成立している。

第一に、`@playwright/test` の pin が `package.json` と `package-lock.json` で一致し（現行 1.60.0）、baseline 生成 workflow がこの pin を `npm ci` で復元すること。第二に、`update-playwright-snapshots.yml` が Chromium を入れ（`npx playwright install --with-deps chromium`）、`npx playwright test --update-snapshots` を実行し、生成された baseline PNG を **PR として** commit する設計であること（手動ダウンロード＆コミットの最終マイルは既に PR 経路へ置換済み）。第三に、その PR 作成（`peter-evans/create-pull-request`）が機能するために workflow が `contents: write` と `pull-requests: write` を宣言していること——これは **Check 48** が BLOCKING で機械強制する。第四に、active runbook（`total-check-runbook.md` §7.4）が名指しする baseline 生成 Playwright 版数が pin と一致すること——これは **Check 51** が BLOCKING で機械強制する（版がずれると内容同一でも偽の視覚差分が出るため）。

---

## 2. 人間が実行する baseline 取得手順（dispatch → review → merge）

以下は横井雄太が GitHub 上で実行する手順である。AI は代行できない。

第一段階（dispatch）として、GitHub Actions の **"Update Playwright Baseline Snapshots"**（`update-playwright-snapshots.yml`）を `workflow_dispatch` で起動する。これにより CI 上の Linux ランナーで Chromium がインストールされ、pin 版（1.60.0）の Playwright が `--update-snapshots` で baseline PNG を生成する。

第二段階（PR 生成の確認）として、workflow が `e2e/**/*-snapshots/*.png` を含む PR を自動作成することを確認する。PNG が 1 件以上生成されていること、生成版数が 1.60.0 であることを PR の CI ログで確認する。

第三段階（レビュー）として、生成された PNG 差分を **人間が目視レビュー** する。これは視覚回帰の「真実の基準画像」を確定する工程であり、意図しないレイアウト・色・フォント・余白が混入していないかを人間が判断する。ここが人間レビューゲートの本質である（AI が代行してはならない）。

第四段階（merge）として、PNG が意図通りであることを確認したうえで PR を merge する。merge 後、baseline PNG がリポジトリ現物（main ブランチ）に含まれる。

第五段階（regression enforce 確認）として、merge 後に `playwright-regression.yml` がその baseline を使って screenshot diff を enforce できることを確認する（`npm ci` で pin 版を復元し比較）。

---

## 3. merge 後に AI が更新すべき文書一覧

baseline PR が merge され、baseline PNG が現物に含まれたら、次の文書を「取得済み」状態へ更新する（これは AI が実装できる作業である）。

第一に、`docs/architecture/main-js-extraction-map.md` §3.5 の「Playwright baseline 取得状況」を「**未取得**」から「**取得済み（PR #… / コミット SHA … / Playwright 1.60.0 / Chromium <version> / 生成 PNG <件数>）**」へ更新する。第二に、同 §3.5 の「Stage 5 ゲート」を「baseline 取得済みにつき解錠」へ更新する。第三に、`docs/architecture/total-check-runbook.md` の関連記述（baseline 未取得を前提とした箇所）を取得済みへ同期する。第四に、`docs/architecture/repository-maintainability-map.md` の changelog に baseline 取得 increment を追記する。第五に、`docs/evidence/public-deployment-freshness-review.md` 等の観測記録に baseline 取得の事実を記録する。

これらの更新時には、baseline PR 番号・commit SHA・Playwright version・Chromium version・生成 PNG 件数を必ず記録する（`プロンプト.md` の要求）。

---

## 4. version bump の可否条件（atomic でなければ行わない）

baseline merge をメジャーアップデートとして version bump するか否かは、横井雄太の判断事項である。version bump を行う場合は、`AI2AI.md` の Version Update Checklist に従い、以下を **atomic に（同一 increment 内で漏れなく）** 更新できる場合だけ行う。

更新対象は、`Pipeline-Version`（AI2AI.md）、`index.html` の `ai:version`、`main.js` の `SITE_CONFIG.VERSION`、`.well-known/mcp.json`、`sitemap.xml`、`robots.txt`、`llms.txt`、`llms-full.txt`、llms エイリアス群、`sw.js` の `CACHE_NAME`、AIO manifest、そして digest 対象（`check_aio_digests.py` が再計算）である。これらを atomic に同期できないなら、**version bump は行わず**「Major Update preparation complete / baseline PR pending（または merged, version bump deferred）」と明記する。

注意すべきトレードオフとして、version bump は AIO 正本層（`llms*` / `AI2AI.md` / `.well-known/*` / digest / `sitemap.xml` / `robots.txt`）の本文変更を伴う。これらはオーナーの明示承認が必要な保護層である。したがって version bump は、(a) baseline が merge 済みで、(b) オーナーが AIO 正本層の更新を承認し、(c) Version Update Checklist 全項目を atomic に満たせる、の三条件がそろって初めて実行する。**version の一部ファイルだけを更新することは禁止である**（`プロンプト.md` / `改善文書.md` §8 の禁止事項）。

なお、version 体系を v80 系の継続とするか、v81/v90 等の新段階とするかも横井雄太の判断事項である（本文書は手順を示すのみで、版番号の決定は行わない）。

---

## 5. AI（Claude）が実行できない権限境界（捏造禁止）

`プロンプト.md` / `改善文書.md` §4.1 の通り、本リポジトリの改善を担う AI には、以下を実行する権限・操作手段が **ない**。AI はこれらを「実行したふり」をしてはならない（捏造禁止）。

第一に、この実行環境（サンドボックス／対話）から GitHub Actions workflow を `workflow_dispatch` で起動する手段がない。第二に、GitHub connector の権限は読み取り中心であり、workflow dispatch / PR review / PR merge を実施できない。第三に、Playwright baseline 生成は GitHub Actions 上の Chromium 環境で行う設計であり、ローカル／サンドボックスでは Chromium バイナリの DL が egress allowlist で遮断されるため `npm run test:e2e` が起動せず、baseline をローカル生成して commit する経路は取れない（これはテストの欠陥ではなく環境制約）。第四に、baseline PR のレビューと merge は、意図しない視覚差分を人間が判断する **人間レビューゲート** として設計されており、AI が代行してはならない。

したがって AI 側の責務は、(a) workflow（`update-playwright-snapshots.yml` / `playwright-regression.yml`）が正しく機能する状態を保つこと、(b) 版数整合（Check 51）・権限結合（Check 48）・baseline-skip ガード（Check 16）・生成リンク（Check 29）を機械強制し続けること、(c) 本文書と extraction-map §3.5・runbook §7.4 に手順を明文化して人間が dispatch→PR→merge を実行できる状態にすること、までである。**baseline 取得そのものは、人間（横井雄太）の action を待つ。**

---

## 6. Stage 5 解禁条件（再掲・不変）

`main.js` の Stage 5 抽出（Router / Main Renderer / RouteState Proxy / EffectRails / BindingRegistry / ActionDelegator / Store / Safe Storage / State Management / Meta Management / Mobile drawer・focus trap / ErrorBoundary / AIDK Isolated Kernel / View Transition proxy / Trusted Types policy / innerHTML interceptor）は、**baseline PNG が現物に commit されるまで着手しない**。これらは描画・遷移・タイミング依存であり、視覚回帰の裏付け（baseline）なしに触ると、挙動を変えていないことを機械的に証明できない。`main-js-extraction-map.md` §3.5 の中〜高層・高後回し層も同じく baseline 後である。

baseline が merge され §3 の文書更新が完了した時点で、初めて Stage 5 へ進める条件を「満たした」と扱う。それまでは安全弁を維持する。

---

## 7. このメジャーアップデートの位置づけ（honesty）

本 increment 時点で、baseline は **未取得** である。本文書・extraction-map §3.5・runbook §7.4 により、人間が dispatch→PR→merge を実行できる準備は完了している。すなわち現状は「Major Update preparation complete / baseline PR pending」であり、これは進捗の停滞ではなく、人間レビューゲートという設計上の安全装置を尊重した、正規の待機状態である。AI 側でできる準備（workflow 検証・版数整合の機械強制・手順の文書化）は完了しており、残るのは横井雄太による GitHub 上の action のみである。

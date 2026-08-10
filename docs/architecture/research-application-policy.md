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

- **`@playwright/test` 1.60.0→1.61.1 bump（2026-06-28 保留 → 2026-06-29 適用・disposition 改訂）:** 当初は「behavior 安全性が未検証 + 同梱 Chromium 変更（revision 1223→1228）で screenshot baseline が stale 化し人間 gated な再生成を要する」を理由に §3(C) で保留した。その後 dependabot が本 bump を提案（PR #326）し、**その CI で `playwright-validation`（behavior e2e・BLOCKING）が 1.61.1 で緑**であることが実証された（先行 increment の Check 142 が package.json 変更で behavior gate を発火させた成果）。新証拠を踏まえ disposition を改訂し適用：(i) 唯一の懸念だった behavior 破壊は CI で否定、(ii) 残る screenshot advisory-red は §3(B) が「intentional change による red は expected・merge を gate しない」と明示的に許容、(iii) baseline 再生成は人間の任意フォロー（必須でない・AI は §3 経路で実行不可）。dependabot の #326 単独は runbook §7.4 の生成版数（Check 51）を更新しないため CI fail するので、pin bump + runbook §7.4 同期（1.60.0→1.61.1）を 1 つの coordinated PR で適用し、#326 は本適用で supersede。**教訓: CI 証拠（behavior e2e の実結果）が出たら過去の保守的 deferral は改訂してよい——保留は新証拠で更新されるべき仮説であり、固定判断ではない。**

- **WCAG 1.4.10 Reflow の 320px 横あふれ（2026-08-10 保留 → 同日 適用・disposition 改訂）:** 320×800 で 4 ルートに水平あふれがあった（`#/role-split` +51px / `#/quiz` +31px / `#/hiring-risk` +28px / `#/apps/pomodoro` +16px）。当初は「修正が `style.css` のレイアウトに及び複数ページの見た目を変える。視覚 baseline をローカル再生成できないので非破壊性を証明できない」＋「余白の設計判断は C5」を理由に §3(C) で保留した。**この保留理由は、真因が判明した時点で両方とも成立しなくなった**ので改訂した。
  - **真因**: 基底の `.main-content` は `max-width: 1200px; margin: 0 auto` で本文カラムを中央寄せする。ところが `@media (max-width: 920px)` で `.app` が `flex-direction: column` になると、その左右 margin が **cross 軸の auto margin** になる。flexbox 仕様上、cross 軸に auto margin を持つ flex item には `align-self: stretch` が適用されず fit-content でサイズが決まり、**fit-content は min-content を下回れない**ため、本文の min-content が viewport を超えたルートでは item 自体が viewport より広くなっていた。実測でも `#app` 320px に対し `#main-content` が 350.92px。
  - **修正**: 同 media query 内に `max-width: 100%` の 1 行（fit-content をコンテナ幅で頭打ちにする）。`align-self: stretch` の明示では直らない（auto margin が stretch を無効化しているのが原因なので）ことを実測で確認済み。適用後は 15 ルート × 幅 320/375/768/920 のすべてであふれ 0。
  - **保留理由が消えた根拠**: (i) 修正は `@media (max-width: 920px)` に完全スコープされ、**screenshot baseline は 1280×720 clip なのでこの media query に到達しない**＝視覚 baseline は構造的に不変（「baseline を再生成できないから触れない」が成立しない）。(ii) 余白の好みではなく「viewport より広い箱ができる」という封じ込めの欠陥なので、C5（設計判断）ではなく correctness の問題。
  - **回帰防止**: 視覚 baseline では原理的に検出できないため、behavior e2e（BLOCKING）で 320px 幅の 6 ルート（過去に溢れていた 4 + 対照 2）を検査し、mutation（`max-width: 100%` の除去）で RED を実測した。
  - **教訓**: 保留理由が「見た目が変わるので証明できない」の形をとるときは、**変更のスコープが視覚ゲートに到達するのかを先に確かめる**。ここでは media query の条件と screenshot の clip 幅を突き合わせるだけで、保留の前提が崩れた。

- **axe-core 4.12.1 → 4.13.0 の適用と、そこで可視化された WCAG 1.4.3 (Contrast) の実測（2026-08-10）:** minor bump を「新ルールが実バグを暴くか」を先に測ってから適用した。既存 a11y ゲート（critical のみ）は **22 passed のまま**で新規 critical はゼロ。だが **フィルタを外して走査したところ `color-contrast`（serious）が全ルートで大量に出た** — このリポジトリの a11y ゲートは critical 限定なので、**1.4.3 は構造的にずっと未検査だった**（2026-06-16 の WCAG 監査記録も 1.4.3 には触れていない）。
  - **適用した分（imperceptible ゆえ C5 に当たらないと判断）**: 既定ブランド indigo の `--color-primary-rgb` が白背景に対し **4.467** で、要求 4.5:1 を **0.04 だけ**下回っていた。各チャンネル −1 の `rgb(98,101,240)` で **4.527** となり AA を満たす。変化量は 1/255 ≒ 0.4% で知覚不能、かつ screenshot の許容 threshold 0.05 を大きく下回るため**視覚 baseline に影響しない**。実測の効果は `#/quiz` **63 → 4 ノード**、`#/` 41 → 21、3 ルート計 **132 → 53**。もう一方の brand `classic` `rgb(37,99,235)` は 5.169 で元から AA 達成。回帰は behavior e2e（トークン単体の契約）で固定した。
  - **保留（安全ゲート・C5＝配色の設計判断）**: 残る違反は「実際に色が変わる」もので、単独では決められない。実測値と候補を残す。

    | 組み合わせ | 実測比 | 要求 | 用途 | AA に必要な変更 |
    | :-- | --: | --: | :-- | :-- |
    | `#94a3b8` on `#ffffff` | 2.56 | 4.5 | muted / 補助テキスト | 各チャンネル −44（`#68778c`）＝**明確に濃くなる** |
    | `#6265f0` on `#eff0fe` | 4.00 | 4.5 | 淡色チップ上の primary 文字 | 文字を濃くするか、チップ背景を白寄りにする |
    | `#16a34a` on `#e8f6ed` | 2.95 | 4.5 | 成功系チップ | 同上（緑の再選定） |

  - **ダークテーマも同じ問題を持つ（2026-08-10 追加実測・こちらの方が範囲が広い）**: 前段の表は**ライトテーマのみ**の数値だった。ダークは独自のトークン集合を持ち、**primary をそのまま暗背景の文字色に使う**ため別クラスの不足が出る。ライトだけ直して「終わった」と判断しないこと。

    | 組み合わせ（ダーク） | 実測比 | 用途 |
    | :-- | --: | :-- |
    | `#6265f0` on `#0f172a` | 3.94 | 暗背景上の primary 文字（`#/` で 14 ノード） |
    | `#64748b` on `#0f172a` | 3.75 | muted / 補助テキスト（同 14 ノード） |
    | `#6265f0` on `#252f4d` | 2.91 | 淡色チップ上の primary（`#/projects` で 18 ノード） |
    | `#16a34a` on `#1d353d` | 3.91 | 成功系チップ |

    ライトで効いた「1/255 の暗色化」はダークでは使えない（暗背景に対しては primary を**明るく**する必要があり、必要量が大きい）。パレットには既に `--color-primary-light: #818cf8` があるので、**ダークでは文字色に light 変種を使う**のが最短の候補。ただし見た目が変わるため C5。
  - **ダークの ARIA / 構造面は検証済み**: 全 17 ルートを OS 追従（`emulateMedia`）でダーク描画させ、render-neutral な critical rule で走査したところ **違反ゼロ**。contrast 以外はライトと同等に健全で、behavior e2e として恒久化した（従来ダークは a11y 被覆ゼロだった）。
  - **なぜ AI 単独で適用しないか**: 上表はいずれも**知覚できる変化**で、サイトの見た目の性格を変える。CLAUDE.md §7 の「配色・余白の設計判断は C5（人間）の領域」に該当する。上の indigo 修正だけを適用したのは、**1/255 で知覚不能かつ視覚 baseline に非到達**という点で「設計の変更」ではなく「丸め誤差レベルの是正」と切り分けられたため。
  - **再現コマンド**: `AxeBuilder(page).withRules(['color-contrast']).analyze()` を各ルートで実行し、`violations[0].nodes[].any[0].data` の `fgColor` / `bgColor` / `contrastRatio` を集計する（本記録の数値はこの方法で取得）。
  - **適用条件**: オーナーが配色変更を裁可した時。その際は muted → `#68778c` を起点に、チップ背景側を白寄りへ寄せる案と見比べるのが早い。

- **安全ゲート（C6・AIO 意味論）— Speakable `cssSelector` に実在しない `[data-speakable]` が宣言されている（2026-08-11 実測）:** `js/meta-management.js` の `SPEAKABLE_SELECTORS` は AI 音声アシスタント向けに「読み上げるべき要素」を宣言する **機械向け宣言**。全該当ルートで `querySelectorAll` を実際に走らせて件数を測ったところ、`[data-speakable]` は **home 以外で 0 件**だった。

  | ルート | `h1` | `[data-speakable]` | 固有セレクタ | `.sr-only` |
  | :-- | --: | --: | --: | --: |
  | `home` | 1 | **2** | `.sr-only[data-ai-entity]` = 1 | — |
  | `role-split` | 1 | **0** | `#role-split-table` = 1 | 7 |
  | `ai-knowhow` | 1 | **0** | `.ai-summary-block` = 1 | 7 |
  | `about` | 1 | **0** | — | 7 |
  | 既定（他ルート） | 1 | **0** | — | 7 |

  `data-speakable` 属性は **`js/home-page.js` の 2 箇所にしか存在しない**（`grep` で全走査）。つまり home 以外の宣言は #929（WebMCP の幻セレクタ）と同型の「**一度も対象を持たない宣言**」である。
  - **実害の程度（honest）**: 解決しないセレクタは consumer に無視されるだけで、他のセレクタ（`h1` / `.sr-only` / 固有）は機能する。**読み上げ内容が壊れているわけではない**。問題は「宣言と実態の乖離」で、本リポジトリの中核賭け金（機械可読な権威付け）の面に嘘が残っていること。
  - **保留理由（安全ゲート・C6）**: Speakable は AIO の意味論的宣言であり、**C6 は JSON-LD の semantic content の変更に orchestrator の書面承認を要求する**。「マッチしないセレクタを消すだけ」は実効挙動を変えない no-op だが、C6 の A1/A2 例外（日付・digest などの derived value）に列挙されていない以上、**派生値ではなく semantic 編集**として扱うのが保守的で正しい。#929 で幻セレクタを除去したのは WebMCP のツールコード（AIO JSON-LD 層ではない）だったため、同じ扱いにはできない。
  - **提案する最小の修正**: `SPEAKABLE_SELECTORS` の `role-split` / `ai-knowhow` / `about` と既定フォールバックから `'[data-speakable]'` を除く（home は 2 件マッチするので残す）。あるいは逆に、各ルートの読み上げ対象へ `data-speakable` を付与する（こちらは「実態を宣言に合わせる」方向で、#929 の教訓では**推奨しない** — 存在しないものを後から作るのは実態に嘘を合わせる行為）。
  - **同時に張るべき層**: 修正が承認されたら、**Speakable の各セレクタがそのルートで 1 件以上に解決する**ことを behavior e2e で固定する（Check 411 が main.js の `querySelectorAll` に対してやっているのと同じ used⟹defined レンズの Speakable 面）。今は宣言側が壊れているため、**先に Check を入れると恒久 RED になる**ので順序は修正が先。
  - **再現コマンド**: 各ルートで `script[data-ld="speakable"]` を JSON parse し、`speakable.cssSelector` の各要素を `document.querySelectorAll(sel).length` で数える（本記録の数値はこの方法）。

- **観測（未適用・記録のみ）— quiz の `document.title` だけが renderer の fallback を鏡写していない（2026-08-11 実測）:** 無効な `?type=` に対し 3 つの面が別々に fallback を決めている。

  | 面 | `?type=` 空 | `?type=zzz` / `constructor` |
  | :-- | :-- | :-- |
  | 描画（quiz-renderer） | AWS 問題集 | **AWS 問題集** |
  | sidebar nav（components.js） | AWS を active | **AWS を active** |
  | `document.title`（page-meta.js） | 「AWS問題集」 | **「Quiz」** |

  つまり **同じ AWS 問題集を描画しているのに、空値なら「AWS問題集」・未知値なら「Quiz」** という内部の食い違いがある。`components.js:67` の `[FIX]` は「無効 type で AWS が表示されるのに nav が追従しないのは control↔content desync」と明記して nav を鏡写しに直しており、その原則を title に当てはめれば title も AWS にすべき、という論理は立つ。
  - **なぜ変更しなかったか（honest）**: 実際に `map.aws` へ変えてみたところ、**#926 の既存テストが `/^Quiz \|/` を正規表現で pin していて 5 件 RED になった**。これは記録された期待値であり、覆すには「'Quiz' だと実害が出る」ことの測定が要る。'Quiz' は生成りの汎用語で**嘘ではない**（実際 quiz ページである）ため、実害を示せていない。**マージンの薄い改善で pinned expectation を覆さない**方を選んだ。
  - **この件を見つける前に踏んだ失敗**: 変更前に `'Quiz'` / `"Quiz"` をクォート付きで grep して「依存なし」と判断したが、**既存テストは正規表現 `/^Quiz \|/` で pin していた**ため見落とした。検出器の網が狭いと「無い」を誤って結論する（本セッションで 3 回目の同型ミス）。
  - **適用条件**: オーナーが「タブ名は描画内容と一致すべき」と裁可した場合。その際は page-meta の fallback を `map.aws` にし、#926 のテストの期待値も同時に更新する（片方だけ変えると必ず RED）。

**(B) 適用不要だが検証済み（verify）:** 現物が既に当該標準に準拠しており、変更不要なもの。「変更が無かった」のではなく「現行性を検証した」結果として記録する。これは null result ではなく、現行性・機械可読性を価値とするこのリポジトリにおける成果物である。例（過去 increment）＝robots.txt の granular AI-bot モデル・Node 24・CSP / Trusted Types が 2026 標準に対し現行であることの検証。

- **llms.txt / AI-crawler discoverability の現行性検証（2026-06-28）:** 2026 時点の調査で、(i) llms.txt 採用率は ~10%（18ヶ月後）に留まり、(ii) **AI 検索クローラ（GPTBot/ClaudeBot/PerplexityBot/OAI-SearchBot/Google-Extended）は llms.txt をほぼ fetch せず HTML を直接クロール**（500M bot 訪問中 llms.txt 直叩きは ~408 件）、(iii) Google は非対応を明言・Anthropic/OpenAI/Perplexity も自動読込未コミット、(iv) genuine な実利用は **B2A（Business-to-Agent）= IDE エージェント（Claude Code/Cursor/Windsurf/Copilot/Cline/Aider）が docs サイトで /llms.txt・/llms-full.txt を参照**、と判明。**本リポジトリは既に root の `/llms.txt`+`/llms-full.txt`（標準配置）と、AI 検索クローラが実際に読む HTML 内 structured data（JSON-LD/entity anchor/meta）の二段構えを持ち、調査が示す現実に整合**。新規採用すべき標準/endpoint は無し。低クローラ uptake は §7「`confirmed_citation_events = 0` は by design = 高確率レーンへの早期ポジション」と整合し、本調査がその姿勢の妥当性を 2026 市場データで裏付けた。公開 AIO content はオーナー方針で terminal ゆえ content 変更も行わない＝**verify-currency（apply なし）**。（出典: SE Ranking 採用率調査 / OtterlyAI GEO study / Search Engine Land llms.txt proposal。再調査は本日付以降に標準が動いた場合のみ。）

**(C) 適用保留（defer）— 理由必須:** 改善に繋がりうるが、今は安全に適用できないもの。**保留の正当な理由と、適用条件・次の一手を必ず文書化する**（確認逃げと区別するため）。正当な保留理由は次の三つに限る。
- **安全ゲート:** Playwright 視覚回帰 baseline 未取得のため、`style.css` / `main.js` の render 系を触ると非破壊性を機械的に証明できないもの（例＝WCAG 2.2 の target size 24×24・focus appearance、Core Web Vitals の CLS/LCP 是正）。baseline 取得後に着手する（`major-update-readiness.md` 参照）。
- **安全ゲート（test-infra）— cross-browser（webkit/Safari）e2e（2026-06-28 調査）:** Safari エンジンでの graceful-degradation 検証は genuine に価値があるが、現テストハーネス（`http-server` で HTTP localhost 配信）では実行できない。根因＝本番 HTTPS では正しい CSP `upgrade-insecure-requests`（index.html・Check 115/C6 で保護され緩和不可）が、HTTP-localhost で webkit に http→https 強制 upgrade を起こし local module（main.js / js/*.js）の load を TLS 失敗させ、SPA が描画されない（`window.render` undefined・`#content` 空）。chromium は localhost を secure context として寛容に扱うため発生しない。**本番（HTTPS GitHub Pages）では upgrade は no-op ゆえ Safari は正常で、これは prod バグではなく test-env artifact**であることを webkit ローカル実測で確認済。適用には HTTPS test serving（自己署名証明書 + `ignoreHTTPSErrors`）等のテスト基盤投資が必要で、rabbit-hole かつ efficiency と相反するため、明示的スコープ決定（major update 等）まで保留する。
- **標準未確定:** Internet-Draft 等で構文が批准前のもの（例＝IETF AIPREF `Content-Usage`）。RFC 化時に適用する。ただし「draft だから」を機械的な保留理由にしない——**戦略整合の判断を先に行う**（次項）。
- **戦略不整合:** 標準そのものが、このリポジトリの確定戦略と方向が逆のもの。例＝AIPREF `Content-Usage` は利用を**制限**する機構だが、本リポジトリの robots.txt は学習ボットを**意図的に許可**し「public experiment intended to be learned from by AI models」と宣言している（最大許可方針）。restriction 機構を permissive な現物へ足すのは既定の言い直し（無益）か許可意図との矛盾であり、適用しない。これは draft 段階か否かと独立した、戦略整合の判断である。

---

## 4. 適用時の不変条件（既存規律の再掲）

リサーチ由来の適用も、本リポジトリの通常の安全規律に従う。すなわち、挙動不変が機械的に証明できること（保護領域 byte-identical 維持・正本層 / binary は byte 不変かつ digest 再生成・各単位で `npm run verify` 0 errors）。リサーチで発見した新しい運用ルールや不変条件は、手動修正で終わらせず、`check_repository_consistency.py` の BLOCKING / ADVISORY Check として機械強制し、適切なドキュメントへ明文化する（discover → document → systematize → memorize）。本 increment では、依存近代化に伴う footgun（eslint と @eslint/js のメジャー不一致）を Check 54 として、また分割で生じうる dangling preload の 404 を Check 53 として機械強制した。

---

## 5. この規律の射程（honesty）

本規律は「リサーチを適用しきる」ことを求めるが、安全ゲート（baseline 等）や戦略整合を無視した強行適用は求めない。適用と保留の境界は §3 が定義する。保留は理由付きでのみ許され、理由なき「確認だけ」は禁止である。要するに、**リサーチの成果は、適用されるか、理由付きで保留されるか、現行性検証として記録されるかの、いずれかの形で必ずリポジトリに反映される**。宙に浮いた「調べただけ」を残さない。

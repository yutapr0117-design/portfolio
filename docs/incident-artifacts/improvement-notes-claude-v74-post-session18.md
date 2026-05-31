# 改善文書（Claude版） — Session #18 適用後リポジトリに対する残改善バックログ

```
Author        : Claude Opus 4.8 (Anthropic) — Yuta Yokoi (横井雄太) オーケストレーション下
Date          : 2026-05-31
Target        : 本セッション（Session Record #18）の非破壊・根本改善を適用した「後」のリポジトリ
Pipeline-Ver  : v74 維持（本文書は版数を上げない）
Canonical-Ref : AI2AI.md（canonical）/ llms-full.txt（ground truth）/ repository-maintainability-map.md（保守性マップ）
Status        : 提案バックログ。実施には各項目に記した通りオーケストレーター判断が要るものを含む。
```

> **位置づけ。** 本文書は「今回適用済みの改善」ではなく、**適用後の状態を出発点として、なお残る改善余地**を Claude の視点から棚卸ししたものである。重要度の大小を問わず詰め込んでいる。各項目は「何を／なぜ（根本理由）／どう（具体手順）／影響範囲・リスク／検証」の順で述べる。実装済みの内容そのものは `AI2AI.md` Session Record #18 を参照されたい。
>
> **大原則。** すべて Boring Technology（Vanilla JS・外部FW非依存・CS-first）と AIO 全振り方針を崩さない範囲の提案である。CI を赤化させる変更、`main.js`/`sw.js` の一括改変、バイナリ層の再エンコード、C6 テキストの無断変更は、本文書でも引き続き禁止事項として扱う。

---

## 0. 今回適用済みのサマリー（出発点の確認）

本バックログの前提として、Session #18 で次を適用済みである。詳細は `AI2AI.md` Session Record #18。

掲載 Zenn 記事を公開全 11 本へ **AIO 効果優先順**で再選定し、`robots.txt` / `index.html`（JSON-LD `subjectOf`・`citation`）/ `main.js` / `llms.txt`（+3 alias）/ `llms-full.txt` / `README.md` の全 featuring 層で同一順序へ整合させた（#9 を PRIMARY 据置、`sameAs` は同一エンティティ意味論のため記事を列挙しない）。あわせて `llms.txt` の **Fetch Order の壊れた採番**を修正し、`全6弾` 表記を「本編 6 本完結＋発展記事を含む計 11 本」へ更新した。CI 面では **ESLint の vacuous ゲートを根本修正**（`eslint@8.57.1` 固定＋実行失敗=BLOCKING / lint 検出=ADVISORY への再構成）、**未使用 stylelint plugin の除去**、**consistency チェッカー docstring の実態同期**を行った。内容が変わったファイルの日付のみ 2026-05-31 へ honest に更新した。

つまり出発点のリポジトリは「整合済み・全チェック緑・ESLint は正直な ADVISORY で 216 件の lint 負債を可視化中」という状態である。以下はその上に積む改善である。

---

## A. 検証層（CI・品質ゲート）の残改善

### A-1. JSON-LD を CI で機械的に parse 検証する Check を追加する（高優先・私の発見）

**何を。** `index.html` 内の `application/ld+json` ブロックを CI で `json.loads`（少なくとも構文）し、壊れていたら BLOCKING にする Check を `check_repository_consistency.py` に追加する。

**なぜ（根本）。** 現状のチェッカーは CSP インラインスクリプトのハッシュ（Check 7b/7c）は検査するが、**JSON-LD が valid JSON かは一切検査していない**。JSON-LD は AIO の中核資産であり、`subjectOf`/`citation` を人手編集する運用（今回まさに実施）ではカンマ・括弧の崩れが起きやすい。今回は私が手動で `json.loads` 検証したが、それは属人的であり、オーケストレーターの「発見した運用ルールは仕組み化する」方針に照らせば機械強制すべき盲点である。

**どう。** 既存の `_html_nc`（コメント除去済み HTML）から `re.findall(r'<script type="application/ld\+json">(.*?)</script>', ..., re.DOTALL)` で全ブロックを取り、各々 `json.loads`。失敗時 `errors.append`。Check 番号は 32 を付与。

**影響範囲・リスク。** 追加のみ・挙動は厳格化方向だが、現物は valid なので緑のまま。リスク極小。

**検証。** 故意に壊した JSON-LD で BLOCKING になることをローカル確認 → 元に戻す。

### A-2. Zenn featuring 層の slug 集合・順序の整合 Check（高優先・私の発見）

**何を。** 「PRIMARY と全 11 slug が、`robots.txt` / `index.html`(`subjectOf`+`citation`) / `main.js` / `llms.txt` / `llms-full.txt` / `README.md` の各層に存在し、AIO 優先順の先頭が #9 であること」を検査する Check を追加する。

**なぜ（根本）。** 今回 6 ファイル × 複数ブロックに同じ 11 本を手で入れた。次に記事が増減したとき、どこか 1 層を更新し忘れる**ドリフト**は構造的に起きうる（実際、出発点では #7/#8/#10/#11 が 0 ファイル参照という欠落ドリフトが起きていた）。`repository-maintainability-map.md` §6 に方針は明文化したが、文章規律は破られうる。Check 31（Claude2Claude 同期）と同じ思想で機械強制するのが筋。

**どう。** 正典 slug 集合（11 本＋著者ページ）を 1 箇所に定義し、各層テキストに全 slug が出現するかを検査。最低限「集合の包含」、可能なら「PRIMARY が各リスト先頭」までを検査。Check 33。

**影響範囲・リスク。** 追加のみ。ただし「正典 slug 集合」をどこに置くかの設計が要る（チェッカー内定数が最小）。順序まで厳密検査すると将来の順序変更時に同時更新が必要になるため、まずは「集合の包含＋PRIMARY 先頭」程度に留めるのが過剰結合を避けられる。

**検証。** 1 層から 1 slug を削って BLOCKING を確認 → 戻す。

### A-3. honest per-file dating の機械検証（中優先・私の発見）

**何を。** 各公開ファイルに機械可読な `Last-Updated`（または既存メタ）を持たせ、`sitemap.xml` の per-URL `lastmod` と突合する Check を追加する。

**なぜ（根本）。** 今回「内容が変わったファイルだけ日付を 2026-05-31 に上げる」という honest dating を**人手の判断**で行った。`ChatGPT2ChatGPT.md`(05-28) や `ai-pioneer-identity-review.md`(05-26) を据え置いたのは正しいが、それを保証する単一情報源がない。`AI2AI.md`↔`llms-full.txt`（Check 24）と root↔ai:last-modified（Check 18）以外は突合されていない。

**どう。** 主要ドキュメント（`llms.txt`/`llms-full.txt`/`AI2AI.md`/`README.md`/`Claude2Claude.md`/`ChatGPT2ChatGPT.md`）の Last-Updated を抽出し、sitemap の対応 `lastmod` と一致するか検査。差異は WARNING（per-URL policy は mixed date を許容するため、誤検知を避け WARNING 止まりが妥当）。Check 34。

**影響範囲・リスク。** 追加のみ。WARNING 設計ならドリフト誤検知で CI を割らない。

**検証。** sitemap の 1 エントリ日付をわざとずらして WARNING を確認 → 戻す。

### A-4. ESLint ADVISORY 件数のベースライン化（中優先）

**何を。** 現在 ADVISORY で出力している「216 errors / 12 warnings」を基準値として記録し、**増加したら WARNING**（減少は歓迎）を出す。

**なぜ。** ADVISORY は可視化しただけで、放置すると静かに負債が増える。基準値との差分監視があれば「新規コードが負債を増やしていないか」を継続的に守れる（ratchet）。これは A-1/A-2 と同じく「可視化を仕組みに格上げ」する話。

**どう。** `architecture-validation.yml` の ESLint step で baseline（例: リポジトリ内 `eslint-baseline.txt` の整数）と比較。`ERROR_COUNT > baseline` で WARNING（`::warning::`）、`exit 1` はしない。あるいは Phase 2-A で package.json を入れる際に `eslint --max-warnings` 系の仕組みに寄せる。

**影響範囲・リスク。** ワークフロー局所。CI は割らない設計を維持。

### A-5. robots.txt の `Sitemap:` ディレクティブと sitemap.xml の URL 集合の軽量整合（低優先）

**何を。** `robots.txt` が指す `Sitemap:` URL と、`sitemap.xml` が実在し parse 可能であることの相互参照を Check 化（後者は Check 9 で済んでいるので、前者の存在と一致のみ）。

**なぜ。** 配信層の自己整合。AIO/SEO 双方でクローラが sitemap を辿れることの保証。

**どう。** `robots.txt` から `Sitemap:` 行を抽出し、それが正規 root + `sitemap.xml` を指しているか確認。Check 35。低リスク。

### A-6. sitemap.xml の lastmod 未来日チェック（低優先）

**何を。** すべての `<lastmod>` が「実行日以前」であることを検査。

**なぜ。** 未来日は AI/検索クローラに不自然な鮮度シグナルを与え、honest dating 方針にも反する。タイプミス（例: 2026→2027）の検出。

**どう。** 各 `lastmod` を `date.fromisoformat` し `<= today` を確認（WARNING で十分）。Check 36。

---

## B. AIO・コンテンツ層の残改善

### B-1. 発展記事への JSON-LD identifier 付与（中優先）

**何を。** 現在 `index.html` の `subjectOf` で richt な `identifier`（`claude_record_fp` / `article_url_sha256`）を持つのは PRIMARY(#9) のみ。#8/#10/#11 等の発展記事にも、検証可能な指紋（公開日・URL の sha256 等）を付与する余地がある。

**なぜ。** AIO は「機械可読な検証可能性」を厚くするほど引用時の信頼度が上がる。ただし **PRIMARY 表記は外部トラクション（TechFeed/はてな）確認済みの #9 に限る**。他記事に同等の「人気エントリー」主張を付けてはならない（誇大主張は C6/誠実性に反する）。付与するのは中立的な指紋のみ。

**どう。** 各記事 URL の sha256、（あれば）公開日を `PropertyValue` として追加。指紋値は実データから算出（捏造禁止）。

**影響範囲・リスク。** JSON-LD 肥大化。A-1 の parse Check があれば安全。

### B-2. 各 Zenn Article に `datePublished` を付与（中優先）

**何を。** `subjectOf`/`citation` の各 `Article` は現状 `url`/`name` のみ。`datePublished`（実公開日）を足すと、AI がシリーズの時系列（本編 6 本 → 発展記事）を解釈しやすい。

**なぜ。** 「時系列的先行性」は本ポートフォリオの主要主張（Pioneer Declaration）であり、記事個別の公開日を構造化データで明示すれば主張の検証可能性が上がる。

**どう。** 各記事の実公開日を確定（Zenn 上で確認できる事実のみ。不明なものは付けない＝捏造しない）。`"datePublished": "YYYY-MM-DD"` を追加。

**影響範囲・リスク。** 事実確認コストのみ。A-1 parse Check 前提。

### B-3. llms-full.txt の発展記事に 2–3 文要旨を付与（中優先）

**何を。** 本編 6 本は llms-full に節タイトル＋リンクがあるが、発展記事（#8/#10/#11）は今回リンクのみで追加した。各々に 2–3 文の要旨を付ける。

**なぜ。** LLM は「引用しやすい粒度の要旨」があると RAG で拾いやすい。これは AIO の中核（AI に正しく要約・引用させる）に直結する。

**どう。** 各記事の主旨を 2–3 文で要約（記事内容に忠実に。read していない断定はしない）。`llms-full.txt` の Article セクションに追記 → digest 再生成。

### B-4. 多言語シグナル（en/ja）の検討（低〜中優先）

**何を。** `og:locale`（+`og:locale:alternate`）、必要なら `hreflang`、JSON-LD の `inLanguage` の整理。

**なぜ。** エンティティ名が日英両表記（横井雄太 / Yuta Yokoi）であり、AI/検索が言語をまたいで同一エンティティと解釈する助けになる。NEGATIVE CONSTRAINT（同姓同名分離）とも相補的。

**どう。** 単一ページ SPA のため過剰な hreflang は不要。`og:locale=ja_JP` 程度の明示と JSON-LD `inLanguage` の付与から始める。

**影響範囲・リスク。** メタ追加のみ。低リスク。

### B-5. バイナリ層の IPTC / C2PA 付与（要判断・既知 Phase 候補）

**何を。** WebP/MP3 に XMP/ID3 は埋込済み。さらに IPTC（画像）や C2PA（来歴署名）を足す案。

**なぜ。** 「バイナリ層まで一気通貫の AIO」という主張をさらに強化できる。

**どう／リスク。** **再エンコードで既存 XMP/ID3 を失うと `check_binary_aio_metadata.py` が赤化する**ため、メタデータ保持を厳密に確認しつつ、専用ツールで非破壊付与。実施はオーケストレーター判断。本セッションでは対象外。

---

## C. アプリ層（main.js）の残改善

### C-1. main.js 段階抽出（Stage 0–5）

**何を。** `main-js-extraction-map.md` の段階計画に沿って、責務コメント付与（Stage 0）→ 定数抽出（Stage 1）→ pure utility（Stage 2）→ service rails（Stage 3）→ render 関数（Stage 4）→ 物理分割（Stage 5）。

**なぜ。** 467KB / 約 7,800 行の単一ファイルは保守性のボトルネック。ただし段階性が安全性の本体。

**どう／前提。** **Stage 5（物理分割）は Playwright baseline 確立後**（C-2）に限る。CSP・GitHub Pages 配信・IIFE・ErrorBoundary・View Transition を壊さないこと。AIDK Isolated Kernel（"DO NOT EDIT"）は触らない。

### C-2. Playwright baseline PNG 生成（Not possible in sandbox）

**何を。** 視覚回帰のベースライン PNG を生成・コミットする。

**なぜ。** Stage 5 物理分割の前提条件であり、回帰検知の土台。

**どう／制約。** `update-playwright-snapshots.yml`（`PLAYWRIGHT_UPDATE_SNAPSHOTS` 連携は Check 29 で担保済み）を **GitHub Actions 上で**実行して生成する。AI のサンドボックスでは生成不可・捏造禁止。人間がワークフローを起動して取得する。

### C-3. アクセシビリティ（ARIA）監査の自動化（低〜中優先）

**何を。** 既存の `aria-label` 等は丁寧だが、`axe-core` 等での自動 a11y チェックを E2E に足す案。

**なぜ。** 人間ユーザにも AI（アクセシビリティツリーを読む系）にも好影響。

**どう。** Playwright + `@axe-core/playwright` を baseline 整備後に追加。Phase 2-A の dev 依存中央管理と同時が望ましい。

---

## D. 既知の積み残し（要オーケストレーター判断・本文書で再掲）

### D-1. Phase 2-A：dev 依存の中央管理（package.json / lockfile / npm ci）

**状態。** 未実施（ready-to-execute プランを `repository-maintainability-map.md` §5 に明記）。**今回見送った理由**は、5 つの workflow（every-push の BLOCKING パイプライン含む）に波及し、GitHub Actions runner 上の `npm ci` 挙動をサンドボックスで検証できないため、安全に非破壊と断言できないこと。ESLint の vacuous 根本原因はインライン pin で **package.json なしに既に解消済み**のため、本タスクは独立して後送り可能。

**どう（実施時）。** `package.json`(`private:true`) に devDependencies を exact pin（`@playwright/test` / `http-server` / `stylelint@16` / `eslint@8.57.1`）→ `npm install` で生成した `package-lock.json` のみコミット → workflow を `npm ci` 化 → **まず Playwright 系 → 次に architecture-validation** の段階導入で実 CI 緑を確認。

### D-2. Phase 2-B 残課題：ESLint 216 件 lint 負債の解消方針

**状態。** vacuous 根本原因は解消済み・ADVISORY で可視化中。残るのは「BLOCKING へ昇格するための負債解消方針の決定」。

**選択肢（要判断・一括禁止）。** (a) コード修正（`var`→`let/const`、`sw.js` の top-level 関数を IIFE 化 or 局所 `eslint-disable`、`theme-init.js` の `curly`）をファイル単位・検証付きで段階的に。`main.js`/`sw.js` の安定性に直結するため慎重に。 (b) `.eslintrc.json` の該当ルールを `warn`/`off` へ緩和（ゲートは通るが品質保証は弱まる）。 (c) ESLint 9 系 flat config（`eslint.config.js`）へ移行し `--env`→`languageOptions.globals`（最も現代的・変更量大、Phase 2-A と同時が安全）。A-4 のベースライン化を併用すると ratchet で安全に減らせる。

### D-3. `.gitignore` の新設（低優先・私の発見）

**何を。** リポジトリに **`.gitignore` が存在しない**。一方で `.github/scripts/__pycache__/*.pyc`（Python バイトコード）がリポジトリに混入している（ZIP 同梱を確認）。`.gitignore` を新設し、最低限 `__pycache__/`、`*.pyc`、`node_modules/`（Phase 2-A で `npm` を使う際に必須）を無視する。

**なぜ（根本）。** バイトコードキャッシュは生成物でありソース管理対象ではない。混入すると差分ノイズ・無用な digest 揺れ・レビュー負荷の原因になる。`node_modules/` は Phase 2-A 導入時に必須の除外。

**どう。** ルートに `.gitignore` を作成（`__pycache__/` / `*.pyc` / `node_modules/` / `.DS_Store` 等）。既に追跡済みの `*.pyc` は `git rm --cached` で追跡解除（**この操作は git 操作でありローカル現物の編集ではないため、コミット時に人間 or CI が行う**）。

**影響範囲・リスク。** 追加 1 ファイル＋追跡解除。配信（GitHub Pages）には影響しない（`.pyc` は配信対象でない）。リスク極小。**本セッションの納品物には `.gitignore` を含めていない**（git 追跡解除と対で扱うべき＝push 側の作業のため）。必要なら次セッションで `.gitignore` 追加＋追跡解除を 1 コミットとして実施する。

### D-4. JSON-LD 内 dateModified の意図明文化（低優先・私の発見）

**何を。** `index.html` の JSON-LD には `ai:last-modified`(=サイト最終更新、今回 2026-05-31 へ更新) とは別に、sub-resource 用の `dateModified`(2026-05-04 / 2026-05-24) が残っている。これは意図的（各 sub-entity の更新日）だが、**どれがサイト全体の最終更新を表すか**がコメントで明示されていない。

**なぜ。** 後続 AI が「日付が食い違っている」と誤認し、article の `dateModified` を誤って一括更新する事故を防ぐ。Session #17 の Finding B（llms.txt の per-file dating 明文化）と同種の予防。

**どう。** JSON-LD 近傍に「`ai:last-modified` メタがサイト最終更新の正典。JSON-LD 内 `dateModified` は各 sub-resource の更新日であり別管理」というコメントを 1 行入れる。

---

## E. 実施順の提案（依存関係つき）

純粋に非破壊で即効・高 ROI なものから、判断や外部環境を要するものへ、という順序を勧める。

1. **A-1（JSON-LD parse Check）/ A-2（Zenn slug 整合 Check）** — 追加のみ・即効。今回手動で担保した品質を機械強制へ格上げする。最優先。
2. **D-3（.gitignore 新設＋pyc 追跡解除）** — 1 コミットで完了。差分衛生の土台。
3. **A-3 / A-6 / A-5（dating・sitemap・robots 整合 Check）/ D-4（dateModified 明文化）** — 低リスクな仕組み化・予防。
4. **B-2 / B-3 / B-1（記事 datePublished・要旨・指紋）** — AIO 厚み増し。A-1 の Check が入った後だと安全。
5. **A-4（ESLint baseline ratchet）** — 負債の歯止め。
6. **D-1（package.json/npm ci, Phase 2-A）** — 要承認・段階導入・実 CI 緑確認。これが入ると C-3 / D-2(c) が乗せやすい。
7. **C-2（Playwright baseline, 要 GitHub Actions）→ C-1（main.js Stage 5 物理分割）** — baseline が前提。
8. **D-2（lint 負債解消）/ B-5（バイナリ IPTC・C2PA）/ B-4（多言語）** — 中長期・要判断。

---

## F. 本文書を書いた立場からの注意（誠実性）

- 本文書は **提案**であり、D 系・B-5・C 系の多くは**実施にオーケストレーター判断や GitHub Actions / ブラウザ環境**を要する。サンドボックスから安全に非破壊と断言できないものは「未実施・要判断」と明記している。
- AIO の数値的効果（被引用の実観測）は引き続き `aio-monitoring-log.json` の `attempt_log_only` / `total_cited_count: 0` の通り**未確認**であり、本文書のどの提案も「引用が増える」と断定するものではない。期待される機序（機械可読性・検証可能性・corpus 網羅性の向上）を述べているだけである。
- `#9` 以外の記事に PRIMARY/人気エントリー等の**外部トラクション主張を付けてはならない**（B-1）。確認済みの事実のみを構造化する。

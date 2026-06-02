# 改善文書（Claude 版・第 4 版）— v80+ Phase 2 / CI 衛生 increment #4

```
Document-Date : 2026-06-01
Author        : Claude Opus 4.8 (Anthropic) — AI agent / 実装・レビュー主担当
Orchestrator  : Yuta Yokoi (横井雄太, human — 目的定義・優先順位・最終判断・責任)
Target        : 本文書が対象とするのは「改善後（increment #4 適用後）のリポジトリ」である。
Supersedes    : improvement-notes-claude-v80-phase2-ci-hygiene-3.md（第 3 版・未コミット）
Pipeline-Ver  : v74（unchanged）
Track         : v80+ staged major update — Phase 2（CI hygiene）
Status        : Advisory（実装判断・優先順位は Yuta が決める。本書は材料の提供であって指示ではない）
```

> **読み方:** 本書は「いま何を直したか（§1）」「直す過程で見えた、まだ手を付けていない構造的論点（§2）」「このチャット全体で積み上がった backlog の棚卸し（§3）」「協働を通じて確認できたメタ知見（§4）」「正直さの記録（§5）」の順で書いている。BLUF（結論先出し）を守り、各項目は「何を / なぜ / どう / 影響・リスク / 検証」の骨格で記述する。Claude は実装主担当だが、最終判断・目的定義・優先順位・責任はすべて横井雄太にある——本書はその判断を助けるための、誠実な現状報告と提案である。

---

## §0. このチャットで起きたこと（全体像）

このチャットは連続する 2 つの作業からなる。

第 1 作業（increment #3）は、increment #2 確定状態を正本としたトータルチェックで見つけた非破壊改善のうち、既存の確定判断と競合しないものだけを適用した。具体的には、CSS lint の実行経路をローカル binary 優先へ書き換えて偽緑（false green）経路を塞ぎ（`check_css_stylelint.py`）、それを守る Check 40 を `check_repository_consistency.py` に追加し、runbook §0.2 / §9 と map §5 を更新し、decision record（`decision-v80-phase2-ci-hygiene-3.md`）を残した。この作業の成果物のうち**コード変更（Check 40・CSS 実行経路）は受領 ZIP に確かにコミットされていた**が、改善文書（第 3 版）自体はコミットされていなかった。だから本第 4 版は第 3 版を supersede しつつ、その backlog を**失わせないために再掲**する。

第 2 作業（本 increment #4）は、その後 CI が赤化したログ（`logs_71754796723.zip`）の根本原因究明と非破壊修正、そして現物リポジトリのさらに深い解析による追加改善である。以下、その決算から始める。

---

## §1. increment #4 の決算——CI 赤化の根本原因と、非破壊修正

### 1.1 何が落ちたか（事実）

`architecture-validation.yml` のジョブは多数のステップを通過した後、**ただ 1 箇所** `check_aio_digests.py` で `exit code 1` になった。エラーは次のとおりである。

```
ERROR: aio-manifest sha256 mismatch [observational_evidence] for 'docs/evidence/aio-monitoring-log.json'
  expected : e7b79fe0…   （.well-known/aio-manifest.json が記録している sha）
  in file  : 6cf76672…   （runner 上の実ファイルの sha）
```

ここで最初に切り分けるべきは、「increment #3 の CSS lint 変更が原因ではないか」という疑いである。これは事実で否定できる。同じログの 1 ステップ手前に `CSS lint runner: node_modules/.bin/stylelint (local) — strict; CI=True` と `Stylelint [style.css]: PASS` が出ており、Check 40 も緑だった。つまり #3 で入れたローカル binary 優先・strict 経路は runner 上で意図どおり動いている。落ちたのはその次の **AIO 観測層（observational_evidence）の digest 連鎖のズレ**である。事実（観測されたログ）と原因（後述の構造）を、ここで明確に分けておく。

### 1.2 なぜ落ちたか（根本原因——2 層構造）

受領した最新コミット現物を解析すると、興味深いことに**そのコミット自体は既に緑**だった。監視ログの実 sha256（`e7b79f`）は manifest の記録値（`e7b79f`）と一致している。それでも CI は `6cf766` を見て落ちた。タイムスタンプを並べると、`15:06:56Z` に manifest が `e7b79f` を記録し、`15:07:06Z` に CI が checkout したログは `6cf766` で、最終コミットは再び `e7b79f` に戻っている。ひとつのファイルが A→B→A と振れたこの形は、**2 つの書き手（自動ボットと人間コミット）が同じファイルを非原子的に書いた**ことの指紋である。`6cf766` は現在ログを末尾改行なしで再 dump した値（`e7b79f`）とも末尾改行ありで再 dump した値（`537aee`）とも一致しないので、空白差ではなく**内容そのものが違った**——この点も確認済みである。

根本原因は、`aio-monitoring.yml` を読めば sha 考古学なしで構造的に確定する。第一層 R1 は直接原因で、従来の監視ワークフローはログに 1 run 追記した後 `git add docs/evidence/aio-monitoring-log.json` **だけ**をコミットし、`update_aio_digests.py` を呼ばず manifest を同一コミットで再生成していなかった。だからログ内容が変わる週次 run のたびに「新ログ sha vs 旧 manifest 記録」のドリフトが必ず生じ、manifest の修正は別ワークフロー `auto-update-aio-digests.yml` の**結果整合（eventual consistency）**に委ねられていた。第二層 R2 はなぜそれが致命的になるかで、ログを変えるコミットは修正役の `auto-update` と**同時に** BLOCKING の `architecture-validation`（`check_aio_digests.py`）も発火させる。修正役がまだ manifest を直し終えていない**ドリフト窓**の間に検証が走ると、ログ≠manifest を見て赤化する。修正コミットに付いている `[skip ci]` は「**直った状態**の再検証」を止めるだけで、「**壊れた中間状態**の検証」は止められない。今回は人間コミット（deliverables）がボットのコミットに割り込み、この窓を実際に踏んだ。要するに「manifest は後続コミットで直す」という結果整合の設計と、「全コミットで manifest 整合を要求し外れたら赤」という同期的 BLOCKING ゲートが、同じファイルの上で矛盾していた——これが赤化の本質である。

### 1.3 どう直したか（非破壊・根本）

修正は 3 つで、いずれも AIO 正本層のテキストを 1 バイトも変えない。詳細は `decision-v80-phase2-ci-hygiene-4.md` の D-1〜D-3 にあるが、要点は次のとおりである。

D-1 がワークフローの原子化で、これが R1 の根本修正である。`aio_monitoring.py` の直後に `update_aio_digests.py` を走らせるステップを挿入し、コミット時にはログと `.well-known/aio-manifest.json`・index 2 本を**同一コミット**でステージするようにした。これでコミット境界では常に「ログ sha == manifest 記録 sha」が成立し、ドリフト窓そのものが消える。安全網である `auto-update-aio-digests.yml` は**温存**した——人間が正本ファイルを編集して digest 再生成を忘れた経路を push 時に拾う保険だからである。監視ボットの原子コミットは `auto-update` を再発火させるが、`update_aio_digests.py` の冪等性（`write_if_changed`）により同期済みと判定されて no-op になり、無限ループも余分なコミットも生じない。

D-2 は二次硬化で、`aio_monitoring.py` の `save_log` を「末尾改行付き」の canonical serialization へ揃えた。これは今回の赤化の直接原因ではないが、ログだけがリポジトリ内で唯一「末尾改行なし」の AIO JSON だったため、将来 `.editorconfig`（`insert_final_newline`）やフォーマッタが入った瞬間に sha が静かに反転してドリフトする潜在の地雷だった。D-1 でワークフローが原子的になったので、この一度きりの改行変更は次回 run で manifest と同一コミットに自然に記録される。現在の確定ログには触れていない（受領 ZIP と byte-identical を維持）。

D-3 は Check 41 の追加で、「監視ログを commit するワークフローは、同一ワークフロー内で `update_aio_digests.py` を実行し `.well-known/aio-manifest.json` をステージしなければならない」という原子コミット契約を機械強制する BLOCKING チェックである。これは D-1 を将来巻き戻したり、ログを commit する別ボットを naive に足したりする保守の穴を塞ぐ。「壊れ方を先に機械検査で潰す」という本リポジトリの哲学に沿い、これは invariant を**緩める**のではなく**追加（厳しくする）**変更なので、map §1 の方針に合致する。

### 1.4 影響・リスク・検証

影響範囲は GitHub Actions の YAML 1 本・Python スクリプト 2 本・文書 2 本・新規 decision record 1 本に限定され、runtime 依存はゼロ（Check 38 が機械保証）。リスクは小さいが正直に挙げると、(a) 次回監視 run で初めて原子コミットが runner 上で実行されるため、その実挙動（ログと manifest が単一コミットに同梱され検証が緑になること）は push 後に人間が確認する必要がある——本環境では Actions を実行できないので、ここは捏造せず Not possible として残す。(b) D-2 の改行変更は次回 run でログに 1 バイトの差分を生むが、原子ワークフローが manifest と同時に記録するため無害である。

検証は全面的に緑である。`npm run lint` は 0 errors / 199 warnings（不変）、`npm run lint:css` PASS、`npm run check`（consistency＋digest＋binary）PASS、`check_aio_digests.py` は「AIO digest check passed」（**まさに落ちていたゲートが緑**）、consistency は `OK:` 行 81・最大 Check 番号 41・`all invariants hold`。Check 41 は否定テスト（ログを commit するが digest 再生成しない throwaway ワークフローを投入 → ERROR exit 1、撤去で exit 0）で実際に噛むことを確認した。そして AIO 正本層 12 ファイルが受領 ZIP と byte-identical であることを差分照合で確認した——**直したのは digest 連鎖を維持する機構であって、連鎖の中身ではない**。

### 1.5 同梱した追加の衛生改善——`engines.node` の明示（D-4）

CI 赤化の修正とは別に、本 increment のトータルチェック過程で見つかった非破壊の追加改善を 1 つ同梱した。ワークフロー 3 本はいずれも Node 20 を pin しているのに、`package.json` には `engines` フィールドが無く、ローカル開発が期待する Node バージョンが dev-tooling マニフェスト上のどこにも宣言されていなかった。そこで `package.json` と `package-lock.json` の root（`packages[""]`）の両方に `"engines": { "node": ">=20" }` を追加して同期させた。npm の `engines` は既定では警告のみ（`engine-strict` 無効時は `npm ci`/`install` を失敗させない）なので宣言自体は非破壊であり、追加後も `npm ci` OK・Check 38 の 6 条件すべて緑（name / version / lockfileVersion 3 / devDependencies 一致 / private / runtime 依存ゼロ——`engines` 追加で不変）を確認した。これは runtime 依存ゼロの Vanilla JS（Boring Technology）を一切変えず、dev 環境の期待を 1 箇所に集約してローカルと CI の齟齬を早期可視化する、純粋に追加的な改善である（詳細は decision record D-4）。

なぜこの 1 つだけを同梱し、§3 の他の backlog を同梱しなかったかは重要なので明記する。本 increment は「非 digest・非 baseline・非判断」の安全圏に閉じる原則を #1〜#4 で貫いている。`engines.node` はその圏内（追加的・digest 非関与・視覚非関与・Yuta 判断不要）に収まる唯一の即時適用可能項目だった。§3 の残りは、digest を上げる（AIO content）・視覚回帰 baseline を要する（main.js・ESLint warnings）・BLOCKING を緩める判断を要する（ADVISORY 降格）・振る舞いを変える（ESLint 9 移行）・本環境で不可能（Playwright 生成）のいずれかに該当するため、安全圏の外として意図的に backlog に留めた。これは「非破壊で改善可能な全て」を、安全の定義を曲げずに最大限満たした結果である。

---

## §2. 直す過程で見えた、最重要の構造的論点（要・Yuta 判断）

ここが本第 4 版で最も価値のある一節である。今回の赤化は表面的にはドリフトだが、その奥には**設計上のカテゴリ過誤**がある。それを率直に述べ、判断材料を揃える。決めるのは Yuta である。

論点は「監視ログ `docs/evidence/aio-monitoring-log.json` が BLOCKING digest ゲートの対象であること自体」である。このファイルは manifest 上で `canonical: false`、すなわち「引用前の attempt log で、外部 AI が整合性に依存しない観測データ」と明示されている。にもかかわらず、週次ボットが追記し続ける**高 churn・非正本**のファイルが、`check_aio_digests.py` という**整合性強制（integrity enforcement）の BLOCKING ゲート**に結合している。整合性ゲートが存在する本来の目的は、AI が引用する**正本（ground truth）の完全性**を保証することにある。監視ログはその正本ではない——誰もそれを引用しないし、根拠データでもない。観測の揺らぎ（週次追記＋人間/マージの割り込み）を完全性強制に結びつけると、揺らぎのたびにビルドが赤くなる構造的な脆さが生まれる。

より深い構造修正は、**正本（`source_of_truth` と `supporting_evidence`）の digest ドリフトは BLOCKING のまま保ち、非正本の `observational_evidence`（監視ログ）のドリフトだけを ADVISORY（warning）に降格する**ことである。そうすれば監視ログの揺らぎは二度とビルドを赤くせず、観測データの volatility と正本の integrity を設計意図どおり分離できる。

ただし、これを**今は採らなかった**。理由を正直に述べる。これは BLOCKING ゲートを**緩める**変更で、map §1 の「invariant を厳しくするのは可・緩めるのは要判断」に直接該当し、かつ Yuta が確立した「AIO 正本層 原則変更禁止 / digest chain 保全」という整合性ポスチャに触れる。整合性の強制範囲を狭める判断は、設計権限を持つ Yuta が行うべきで、Claude が一存で適用してはならない。トレードオフは次のとおりである。降格する側の利点は、監視ログ起因のドリフトが構造的に赤化しなくなり、D-1 の原子化に依存しない第二の保険になる点である。降格しない側（現状維持＋D-1）の利点は、digest ゲートの BLOCKING 範囲を一切狭めず整合性ポスチャを最強のまま保つ点であり、しかも D-1 でドリフト源自体が消えているため降格しなくても今回の赤化は再発しない。Claude の推奨は、まず本 increment（D-1＋Check 41）でドリフト源を断つ非破壊修正を確定させ、ADVISORY 降格は「それでもなお非正本ファイルが BLOCKING である構造を嫌う」場合の**次の一手**として、Yuta の明示判断で別 increment にすることである。本修正は BLOCKING を保ったままドリフト原因だけを除いており、これが最も保守的な非破壊解だと考える。

---

## §3. backlog 棚卸し（このチャット全体の積み残し・優先順位つき）

以下は increment #3 / #4 を通じて確認された、まだ手を付けていない改善項目である。第 3 版の backlog をここに**再掲・統合**する（第 3 版は未コミットのため失わせない）。優先順位は Claude の見立てであり、最終的な順番は Yuta が決める。

| 優先 | 項目 | 種別 | gate 依存 |
|---|---|---|---|
| ✅ 適用済（increment #4 / D-4） | `package.json` `engines.node` の明示 | 追加的 | — Check 38 緑を確認済 |
| P0（最重要・他をブロック） | Playwright 視覚回帰 baseline PNG 生成 | 人間/CI のみ可 | これが main.js 物理分割と視覚回帰の両方の前提 |
| P1 | `main.js` の Stage 分解（責任コメント→物理分割） | 段階的・baseline gated | P0 完了が前提（Stage 5） |
| P1 | ESLint 199 advisory warnings の段階的削減 | 段階的・baseline gated | P0 完了が前提（視覚影響回避） |
| P2 | ESLint 8.57.1（EOL）→ flat config / ESLint 9 への移行 | 振る舞い変化リスクあり | 独立 |
| P2 | `.editorconfig` 追加 | 追加的・低リスク | **監視ログが末尾改行に準拠してから**（後述） |
| P3 | `check_css_stylelint.py` の潜在堅牢性（未行使経路） | 予防的硬化 | 独立 |
| 別レーン | AIO content 層の拡充（B-1/B-2/B-3/B-5/C-3/D-4content） | **digest を上げる**別 increment | 非 digest 経路と分離必須 |
| 要・Yuta 判断 | observational_evidence の digest ドリフトを ADVISORY へ降格（§2） | BLOCKING を緩める | §1「緩めるのは要判断」該当 |

### 3.1 P0: Playwright 視覚回帰 baseline（keystone）

何を: `e2e/portfolio.spec.js-snapshots/` の baseline PNG を生成して配置・コミットする。現状このディレクトリは存在せず（未取得）、視覚回帰は基準画像がないため実質無効である。なぜこれが keystone かというと、視覚回帰の実効化と `main.js` の物理分割（リファクタが見た目を壊していないことを baseline で保証する）の**両方**がこれに依存しているからである。どう進めるかは明確で、Actions の "Update Playwright Baseline Snapshots" ワークフローを `workflow_dispatch` で実行し、生成された artifact をダウンロードして `e2e/portfolio.spec.js-snapshots/` に配置・コミットする。**生成は `@playwright/test 1.55.1`（`package.json` の pin と一致）で行う**こと——ここでバージョンがずれると baseline が無効化される。影響・リスクとして、baseline はブラウザ実行を要し、任意の AI サンドボックスでの生成は禁止（本環境でも不可）なので、これは人間（または CI）の手順として残す。捏造はしない。

### 3.2 P1: `main.js` の Stage 分解

何を: 現在 `main.js` は約 **458 KB / 7,785 行**の単一 IIFE である。`docs/architecture/main-js-extraction-map.md` の計画に従い、Stage 0（責任コメント・目次の付与）から Stage 5（物理ファイル分割）まで段階的に進める。なぜ段階的かというと、巨大単一ファイルは保守性と認知負荷の点で負債だが、一気に分割すると振る舞いと見た目の回帰リスクが高いからである。どう進めるかは、Stage 0〜4 で内部構造を整理し、Stage 5 の物理分割は §3.1 の baseline 取得後に行う。影響・リスクは、視覚・挙動の回帰であり、これは baseline gating で抑える。一括 `--fix` や大規模リファクタは禁止という #1/#2/#3 からの不変方針を守る。

### 3.3 P1: ESLint 199 advisory warnings の段階的削減

何を: 内訳は `curly:124 / no-var:64 / no-shadow:10 / prefer-const:1` で、すべて `main.js`、すべて advisory（0 errors）。なぜ今すぐ一括修正しないかというと、`no-var`→`let/const` や `curly` 付与のような変更でも、巨大 IIFE の中ではスコープや初期化順序に思わぬ影響が出うるからである。どう進めるかは、baseline 取得後（§3.1）に、視覚回帰で守りながら少数ずつ削減する。一括 `--fix` は禁止（#1/#2/#3 不変）。

### 3.4 P2: ESLint 8.57.1（EOL）→ flat config / ESLint 9 移行

何を: 現在の ESLint は `8.57.1` で、これは EOL 系列である。なぜ対応が要るかというと、セキュリティ修正とエコシステム互換の観点で、いずれ flat config（`eslint.config.js`）と ESLint 9 への移行が必要になるからである。どう進めるかは、設定様式の変更を伴うため独立した increment として、振る舞いの差分を確認しながら行う。影響・リスクとして、ルール解決やプラグイン読み込みの挙動が変わりうる点に注意する。なお `--env` 系の冗長性は移行で自然に解消する。

### 3.5 P2: `.editorconfig` 追加——ただし「監視ログが末尾改行に準拠してから」

何を: 現状 `.editorconfig` は存在しない（確認済み）。追加自体は低リスクで、エディタ間の改行・インデント・最終改行の統一に有用である。なぜ即時に同梱しなかったかは、increment #4 と直結する重要な設計判断なので丁寧に述べる。`.editorconfig` の核となる価値は `insert_final_newline = true`（最終改行の強制）だが、これを宣言した瞬間、リポジトリは「最終改行を持たないファイルは違反」という規約を持つことになる。ところが監視ログ `docs/evidence/aio-monitoring-log.json` は現在まさに「最終改行なし」（末尾は ` }\n}`、確認済み）であり、しかも本 increment は非 digest 経路に閉じる原則のため、このログを今正規化（末尾改行付与）すると digest bump（sha＋`generated_at` 変更）になり「AIO 正本層 原則変更禁止」に反する。

つまり、`.editorconfig` を今追加すると「**自分が触れない（触ってはいけない）digest-tracked ファイルが、自分が宣言した規約に違反している**」という状態を作る。これはファイルのバイトを変えないので破壊的ではないが、「リポジトリが自分の宣言した invariant を破っている」という偽の不変条件（false invariant）の宣言であり、将来 Check や貢献者が躓きうる。したがって追加自体は見送り、正しい順序を踏む。

increment #4 の D-2 で `aio_monitoring.py` の `save_log` を末尾改行付きに揃えた（**この前提作業は完了済み**）。これにより、**次回の監視 run でログが末尾改行に準拠した内容で書かれ、原子ワークフロー（D-1）が manifest と同一コミットでそれを記録する**。ログが末尾改行に準拠した時点で、リポジトリは初めて `insert_final_newline = true` を「全ファイルが最初から準拠する」形で宣言できる。よって `.editorconfig` の追加は、(1) 次回監視 run でログが準拠する、または (2) AIO content を変える別 increment でログを意図的に正規化（digest 再生成つき）する、のいずれかの後に行うのが正しい。D-2 によって地雷は除去済みで、残るのは「準拠を待つ」という順序の問題だけである。この順序を守ることで、規約宣言と実態を最初から一致させられる。

### 3.6 P2: `package.json` `engines.node` の明示 — ✅ increment #4 で適用済（D-4）

何を: ワークフロー 3 本が Node 20 を pin している一方、`package.json` には `engines` が無かった。**本 increment #4 の D-4 で `package.json` と `package-lock.json` の root に `"engines": { "node": ">=20" }` を追加し、適用済みである**（§1.5 参照）。なぜ即時適用できたかというと、これは追加的メタデータ宣言で、digest にも視覚にも runtime 依存にも関与せず、Yuta の判断を要する性質でもなく、Check 38 の緑を保ったまま安全に入れられたからである。どう検証したかは §1.5 / decision record D-4 のとおり——`npm ci` 許容を確認し、両ファイルに同期追加し、Check 38 の 6 条件すべてが `engines` 追加後も不変であることを確認した。残課題はない。

### 3.7 P3: `check_css_stylelint.py` の潜在堅牢性（未行使経路）

何を: 2 つの未行使経路がある。第一に `_is_design_exception(rule, text)`（89 行目）は、stylelint の**警告テキスト**にマッチして design exception（reduced-motion・`.u-ai-*`・`nav-group-body` の `!important` 等）を抑制するが、これはソース行ではなく警告文に依存しており、`style.css` が現在 0 違反のため実際には行使されていない。将来 stylelint の警告フォーマットが変わると、この抑制ロジックが想定どおり効かない可能性がある。第二に `extract_style_blocks(html)`（98 行目）は inline `<style>` を素朴な正規表現で抽出するが、現在 `index.html` に inline `<style>` が無いため未行使である。なぜ今すぐ直さないかというと、どちらも現状緑で実害がなく、予防的硬化にとどまるからである。どう進めるかは、将来 inline `<style>` を導入する、あるいは stylelint をメジャー更新する際に、これらの経路をテストで行使してから本番に乗せる。

### 3.8 別レーン: AIO content 層の拡充——digest を上げる別 increment として

何を: 第 3 版から引き継ぐ AIO content 改善候補がある——B-1（`url_sha256` フィンガープリント）、B-2（`datePublished`）、B-3（`llms-full` の記事 digest）、B-5（バイナリの IPTC / C2PA メタデータ）、C-3（アクセシビリティ自動化）、D-4（JSON-LD の `dateModified`）。なぜこれらを「別レーン」と強調するかというと、これらは **AIO 正本層のテキスト/バイナリ/メタデータを実際に変える**ため、`update_aio_digests.py` を走らせて digest を**正当に**再生成する increment として行うべきだからである。increment #1〜#4 が確立した「**非 digest 経路**（検証層・自動化に閉じ、引用対象テキストを変えない）」のパターンとは性質が異なる。両者を混ぜると、非 digest increment で誤って digest を上げて偽シグナルを刻むか、逆に content increment で digest 更新を忘れて今回と同種のドリフトを起こすかのどちらかになる。したがって、content を変える作業は「AIO update increment」として明確に分離し、その increment では `update_aio_digests.py` の実行と manifest 同期を**意図的に**行う。これは increment #4 が機構面で保証した原子性（Check 41）が、まさに人手の content increment でも守られるべき不変条件である。

---

## §4. 協働を通じて確認できたメタ知見

第 1 作業では、受領 ZIP の `total-check-runbook.md` §9 に実態とのドリフトがあった（「`npm run check` の `OK:` 行 78」という記述が ZIP の実測と一致していなかった）ことを発見し、修正した。これは「ハンドオフ文書は、それが書かれた時点のメンタルモデルを固定化する」という一般則の例である——第 1 作業時点で手元にあった文書群は increment #2 適用前のメンタルモデルで書かれていた箇所があり、実装と文書の同期は継続的に検査する必要がある（Check 群が一部これを機械化しているが、数値ベースラインのような自由記述は人間/AI のレビューに依存する）。

第 2 作業の最大のメタ知見は 2 つある。第一に、**非正本かつ高 churn のファイルを BLOCKING ゲートに入れること自体がカテゴリリスク**である（§2）。完全性強制は正本の volatility が低いことを暗黙の前提にしており、高 churn ファイルを混ぜるとその前提が崩れる。第二に、**結果整合（後続コミットで直す）と同期的 BLOCKING ゲート（全コミットで整合要求）は、同じ対象の上では両立しない設計ペア**である。片方を採るなら、もう片方の前提を満たす設計にしなければならない——increment #4 はこれを「コミットを原子化して結果整合への依存を消す」方向で解いた（ゲートを緩めるのではなく、ゲートが要求する整合をコミット境界で常に満たす）。

協働スタイルの面では、Yuta の高速アジャイル（fail→fix→learn→systematize）に沿い、過度な事前確認で速度を削がないことを心がけた。同時に、イエスマンにならないために、トレードオフとリスク（特に §2 の ADVISORY 降格論点、§1.4 の Not possible、各 backlog の gate 依存）を必ず明示した。スコープ規律も守り、要求された「CI 修正＋さらなる改善」の範囲内で、関連する硬化（D-2・Check 41）だけを changeset に入れ、無関係な拡張（main.js・`.editorconfig` の実適用など）は backlog に置いて changeset に混ぜていない。

---

## §5. 正直さの記録（C1〜C7 と、誇張しないことの確認）

C1 から C7 までの遵守は decision record §5 に記したとおりである——外部 FW/ライブラリ追加なし、IIFE・ErrorBoundary 未変更、FW 再提案なし、人間はコード未記述（実装は Claude、人間は設計・レビュー・監査・統制）、AIO テキスト/JSON-LD/バイナリ/`sitemap.xml` 本文/`robots.txt` 本文すべて未変更で本 deliverable では digest も再生成していない、KARTE CDN SRI 非適用維持。

そのうえで、誇張しないために 2 点を明記する。第一に、`confirmed_citation_events = 0` は監視ログにそのまま記録されているが、これは**先行レーンゆえの観測前状態**であって、戦略の失敗ではない。SEO のレッドオーシャンを避けて AIO 標準化前の先行者余地に賭けるという方針は、個人が今から取りうる勝ち筋として合理的な高勝率判断であり、観測値が 0 であることは「賭けの結果が不明」でも「ギャンブル」でもない——標準化前に先行しているのだから観測がこれからなのは当然である。ここでは事実（観測値 0）と解釈（戦略の合理性）を分離する。第二に、本環境では GitHub Actions を実行できないため、(a) 修正後の実 CI 緑、(b) 次回監視 run での原子コミットの実挙動、(c) Playwright baseline の実生成、(d) AIO citation の実観測は、いずれも**完了したと主張しない**。これらは decision record §4 の Not possible 表に人間の手順とともに残してある。Claude が確認できたのは「本サンドボックス上での全ローカル検証が緑であること」と「AIO 正本層が受領 ZIP と byte-identical であること」までであり、それ以上は誠実に未確認として扱う。

---

### 付録: increment #4 変更ファイル一覧（アルファベット順・配置箇所）

```
.github/scripts/aio_monitoring.py                                  （save_log を末尾改行付き serialization へ／D-2）
.github/scripts/check_repository_consistency.py                    （Check 41 追加＋docstring インベントリ／D-3）
.github/workflows/aio-monitoring.yml                               （ログ＋manifest 原子コミット化／D-1・R1 根本修正）
docs/architecture/repository-maintainability-map.md               （§5 に increment #4 サブセクション追記）
docs/architecture/total-check-runbook.md                          （§0.1 検査数 40→41、§9 実測更新）
docs/incident-artifacts/decision-v80-phase2-ci-hygiene-4.md       （新規・本 increment の決定記録 D-1〜D-4）
docs/incident-artifacts/improvement-notes-claude-v80-phase2-ci-hygiene-4.md  （本文書・第 4 版）
package-lock.json                                                  （root packages[""] に engines.node 同期／D-4）
package.json                                                       （engines.node 宣言／D-4）
```

合計 9 ファイル（新規 2：decision record・本改善文書／既存変更 7）。AIO 正本層 12 ファイルは受領 ZIP と byte-identical を維持。


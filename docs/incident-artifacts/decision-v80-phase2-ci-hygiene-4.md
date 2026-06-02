# decision-v80-phase2-ci-hygiene-4.md

```
Decision-Date : 2026-06-01
Session       : AI2AI.md 未更新（最新は Session Record #19 のまま）。本 increment も
                非 digest 層（ワークフロー・スクリプト・検証層）に閉じ、AIO 正本層の
                テキストを変えないため、新規 session record / digest 連鎖を作らない。
                Session #20 は採番しない（increment #1 / #2 / #3 を踏襲）。
Implementer   : Claude Opus 4.8 (Anthropic) — AI agent
Orchestrator  : Yuta Yokoi (横井雄太, human — sole decision authority)
Track         : v80+ staged major update (Phase 2 — CI hygiene increment #4)
Pipeline-Ver  : v74 (unchanged)
Canonical-Ref : AI2AI.md (canonical) / llms-full.txt (ground truth) /
                decision-v80-phase2-ci-hygiene.md (increment #1) /
                decision-v80-phase2-ci-hygiene-2.md (increment #2) /
                decision-v80-phase2-ci-hygiene-3.md (increment #3)
Status        : Applied
```

> **Canonical hierarchy:** `AI2AI.md` is the canonical handoff; `llms-full.txt` is ground truth.
> This decision record is a subordinate incident artifact. If it conflicts with `AI2AI.md` or `llms-full.txt`, those win.

---

## 1. 背景：CI が赤化した。何が起きたか

increment #3 の確定後、`architecture-validation.yml` が **1 箇所だけ**で落ちた。ログ（`logs_71754796723.zip`）の最終 exit は `check_aio_digests.py` ステップである:

```
ERROR: aio-manifest sha256 mismatch [observational_evidence] for 'docs/evidence/aio-monitoring-log.json'
  expected : e7b79fe0…  （.well-known/aio-manifest.json が記録している値）
  in file  : 6cf76672…  （runner 上の実ファイルの値）
##[error]Process completed with exit code 1.
```

まず明確にしておきたいのは、**increment #3 で入れた CSS lint の変更は失敗の原因ではない**点である。同じログの 1 ステップ手前で `CSS lint runner: node_modules/.bin/stylelint (local) — strict; CI=True` → `Stylelint [style.css]: PASS`、Check 40 も緑——つまり #3 の硬化は runner 上で意図どおり動いている。落ちたのはその次、**AIO 観測層（observational_evidence）の digest 連鎖のズレ（drift）**である。

### 1.1 タイムラインの復元（A→B→A という指紋）

受領 ZIP（最新コミット現物）を解析すると、**現在のコミットは既に緑**だった——`check_aio_digests.py` は通り、監視ログの実 sha256（`e7b79f`）は manifest の記録値（`e7b79f`）と一致している。にもかかわらず CI は `6cf766` を見て落ちている。タイムスタンプを並べると:

| 時刻 (UTC) | 事象 | ログの sha |
|---|---|---|
| 2026-06-01T15:06:56Z | `aio-manifest.json` の `generated_at`（digest 再生成時刻）が記録した値 | `e7b79f`（= 現在の内容） |
| 2026-06-01T15:07:06Z | CI が checkout した時点で runner が見たログ | `6cf766`（= **別内容**） |
| 最終コミット（受領 ZIP） | 現在の確定状態 | `e7b79f` |

`6cf766` は、現在ログを「末尾改行なし」で再 dump した値（`e7b79f`）とも「末尾改行あり」で再 dump した値（`537aee`）とも**一致しない**。つまり CI 時点のログは空白差ではなく**内容そのものが違った**。ひとつのファイルが A（`e7b79f`）→ B（`6cf766`）→ A（`e7b79f`）と振れたこの指紋は、**2 つの書き手（自動ボットと人間コミット）が、同じファイルに対して非原子的に書き込んだ**ことを示す。

### 1.2 根本原因（2 層構造・YAML を読めば証明できる）

forensic な sha 考古学に頼らずとも、根本原因は `aio-monitoring.yml` を読むだけで構造的に確定する。

**R1（直接原因）— 監視ボットがログだけをコミットし、manifest を同一コミットで再生成しない。**
従来の `Commit monitoring log` ステップは、`aio_monitoring.py`（ログに 1 run 追記）を走らせた後、`git add docs/evidence/aio-monitoring-log.json` **だけ**をコミットしていた。`update_aio_digests.py` を呼ばず、manifest をステージしない。結果、ログ内容が変わる週次 run のたびに、**新しいログ sha がコミットされる一方で manifest は古い sha を記録したまま**——即ドリフトである。設計はこのドリフトを「別ワークフロー（`auto-update-aio-digests.yml`）が後から manifest を直す」という**結果整合（eventual consistency）**で吸収する想定だった。`auto-update` は確かに監視ログのパスを `paths:` トリガに含んでいる（line 34）ので、ログ push で発火して manifest を `[skip ci]` 付きでコミットする。

**R2（なぜ致命的か）— 結果整合と、同期的な BLOCKING digest ゲートは両立しない。**
ログを変えるコミットは、`auto-update`（manifest 修正役）と**同時に** `architecture-validation.yml`（`check_aio_digests.py` を走らせる BLOCKING ゲート）も発火させる。修正役がまだ manifest を直し終えていない**ドリフト窓**の間に検証ゲートが走ると、ログ≠manifest を見て赤化する。修正コミットの `[skip ci]` は「**直った状態**が再検証されるのを止める」だけで、「**壊れた中間状態**が検証されるのを止める」ことはできない。今回は人間コミット（deliverables）がボットのコミットに割り込み、この窓を実際に踏んだ。

要するに「manifest は後続コミットで直す」という設計と「全コミットで manifest 整合を要求し、外れたら赤」という BLOCKING ゲートが、同じファイルの上で矛盾していた。これが赤化の本質である。

### 1.3 非破壊の原則（#1/#2/#3 を継承）

本 increment も **AIO 正本層のテキストは 1 バイトも変えない**。現在のコミットは既に整合（ログ＝manifest）し緑なので、ログや manifest の**内容**を触る必要はない——触れば、それこそ「AIO content が変わった」という偽シグナルを digest chain に刻み、`原則変更禁止` に反する不要な churn になる。直すべきは**ドリフトを生む機構（ワークフローとスクリプト）**であり、digest 連鎖の中身ではない。

実装後、AIO 正本層 12 ファイル（`docs/evidence/aio-monitoring-log.json` / `.well-known/aio-manifest.json` / `.well-known/index.json` / `.well-known/agent-skills/index.json` / `llms-full.txt` / `AI2AI.md` / `llms.txt` / `sitemap.xml` / `robots.txt` / `index.html` / `main.js` / `style.css`）が受領 ZIP と **byte-identical** であることを差分照合で確認済み。

---

## 2. 決定事項

### D-1: `aio-monitoring.yml` を原子的に——ログ追記と manifest 再生成を同一コミットへ（R1 の根本修正）

**発見:** §1.2 R1 のとおり、監視ボットがログだけをコミットし、manifest 同期を別ワークフローの結果整合に委ねていた。これがドリフト窓の発生源である。

**決定:** 監視ワークフローに以下を施した。

- `Run AIO monitoring queries`（`aio_monitoring.py`）の**直後・コミットの直前**に、新ステップ `Regenerate AIO digests (keep manifest in sync with the appended log)` を挿入し、`python3 .github/scripts/update_aio_digests.py` を実行する。
- コミットステップ（`Commit monitoring log and synced digests` へ改名）で、ログに加えて **`.well-known/aio-manifest.json` / `.well-known/index.json` / `.well-known/agent-skills/index.json` を同一コミットにステージ**する。コミットメッセージは `chore(aio-monitoring): weekly log update + digest sync $(date …)`。

これでコミット境界において常に「ログ sha == manifest 記録 sha」が成り立ち、ドリフト窓が消える。`update_aio_digests.py` は digest が変わらなければ `write_if_changed` で冪等にスキップするため、ログ無変更の週は manifest も index も触らない（空コミットにならない既存の `git diff --cached --quiet` ガードも維持）。

**設計根拠（なぜ「別ワークフロー任せ」を残さないか）:** 結果整合は「壊れた中間状態が観測されない」前提でのみ安全だが、BLOCKING 検証ゲートはまさにその中間状態を観測しに来る。原子化は、検証ゲート（同期的・即時整合要求）とコミット様式（結果整合）の**設計的不一致を解消する**唯一の非破壊手段である。`auto-update-aio-digests.yml` は**そのまま温存**する——これは人間が正本ファイルを編集して digest 再生成を忘れた経路を push 時に拾う安全網（safety net）であり、削除すると別の保護が失われる。監視ボットの原子コミット（ログ＋manifest）は `auto-update` を再発火させるが、`update_aio_digests.py` が既に同期済みと判定して no-op になるため、無限ループも余分なコミットも生じない（検証済み）。

**検証:** `aio-monitoring.yml` の YAML パス、`check_aio_digests.py` 緑、`npm run check` 緑。原子コミットが `auto-update` を no-op で抜けることを `update_aio_digests.py` の冪等性（`write_if_changed`）から確認。

### D-2: `aio_monitoring.py` の `save_log` を canonical serialization（末尾改行付き）へ（潜在ドリフト源の除去・二次硬化）

**発見:** ログの書き手 `aio_monitoring.py` は `json.dump(log, f, ensure_ascii=False, indent=2)` でログを書いており、**末尾改行を付けない**。一方 digest 系の `update_aio_digests.py` は manifest / index を `json.dumps(...) + "\n"`（**末尾改行付き**）で書く。`update_aio_digests.py` はログを**ハッシュするだけで書き直さない**ため、ログだけがリポジトリ内で唯一「末尾改行なし」の AIO JSON になっていた。

これは今回の赤化の直接原因ではない（現在のログは末尾改行なしで、manifest もその sha を記録しており整合している）。だが、**ログの末尾改行を後から正規化する何か**——エディタ、フォーマッタ、あるいは改善文書で推奨している `.editorconfig`（`insert_final_newline=true`）——が入った瞬間、ログの sha が静かに反転してドリフトする潜在の地雷である。とりわけ `.editorconfig` を採用すると、ボットの書き込み（改行なし）と `.editorconfig`（改行あり）が毎回せめぎ合う churn になりかねない。

**決定:** `save_log` を `f.write(json.dumps(log, ensure_ascii=False, indent=2) + "\n")` に変更し、ログを**他の全 AIO JSON と同じ canonical serialization（末尾改行付き）**で書くようにした。POSIX 的にもテキストファイルは改行終端が期待される。D-1 で監視ワークフローが原子的になったため、この一度きりの改行変更は次回 run で manifest と同一コミットに記録される——単独では現在の緑（改行なしログ＝manifest 記録）を壊さない（スクリプト変更は将来の書き込みにのみ効くため）。

**設計根拠:** これは digest 安定性の硬化であり、ログの**意味内容**は変えない（run データは不変、末尾に改行 1 バイトを足すだけ）。改善文書で `.editorconfig` 採用を勧める以上、その前提として書き手側の serialization を先に揃えておくのが筋である。

**検証:** `save_log` の単体テストで末尾改行が付き、出力が valid JSON であることを確認。`py_compile` OK。現在の確定ログ・manifest には触れていない（受領 ZIP と byte-identical を維持）。

### D-3: `check_repository_consistency.py` に Check 41（原子コミット不変条件 / BLOCKING）を追加

**発見:** D-1 で確立した「ログをコミットするワークフローは manifest も同一コミットで同期する」という契約を守る invariant が無かった。将来 D-1 を巻き戻したり、ログを commit する別ボットを naive に足したりすれば、R1 が静かに再発する保守の穴になる。

**決定:** `check_repository_consistency.py` に **Check 41（BLOCKING）**を追加（既存 `check()` ヘルパを使うインラインブロック。Check 40 の直後・Result セクションの直前に配置）。docstring の検査インベントリにも 41 番として追記し、実装とインベントリの同期を維持。invariant は:

> `.github/workflows/*.yml` のうち、**監視ログ `aio-monitoring-log.json` をコミット用にステージするワークフロー**（本文に `aio-monitoring-log.json` と `git add` と `git commit` がそろうもの）は、**同一ワークフロー内で** `update_aio_digests.py` を実行し、かつ `.well-known/aio-manifest.json` をステージしなければならない。

判定はコミットを伴うワークフローに限定する（コメント中の言及だけでは発火しない＝保守的に偽陽性を避ける）。`aio-monitoring.yml` は D-1 後にこの契約を満たす。`auto-update-aio-digests.yml` はトリガパスにログを含み、かつ `update_aio_digests.py` 実行と manifest ステージを行うため自明に満たす。現リポジトリのワークフローはこの 2 本のみがログを参照し、両者とも PASS。

**設計根拠:** 「壊れ方を先に機械検査で潰す」という本リポジトリの哲学に合致する。これは**緩める**変更ではなく invariant を**追加（厳しくする）**変更なので、`repository-maintainability-map.md` §1 の「invariant を厳しくするのは可・緩めるのは要判断」に合致する。

**検証:** 現物で Check 41 が 2 ワークフロー両方 PASS（`all invariants hold`、`OK:` 行 81、最大 Check 番号 41）。否定テスト——ログを commit するが digest 再生成も manifest ステージもしない throwaway ワークフローを `.github/workflows/` に投入 → Check 41 が ERROR（exit 1）、撤去で exit 0 を確認。`py_compile` OK。

### D-4: `package.json` / `package-lock.json` に `engines.node` を明示（dev 環境期待の単一宣言・追加的）

**発見:** ワークフロー 3 本（`architecture-validation.yml` / `playwright-regression.yml` / `update-playwright-snapshots.yml`）はいずれも Node 20 を pin（`node-version: '20'`）しているが、`package.json` には `engines` フィールドが無く、ローカル開発が期待する Node バージョンが dev-tooling マニフェスト上のどこにも宣言されていなかった。これは CI 赤化とは無関係だが、本 increment のトータルチェック過程（現物再解析）で見つかった追加の衛生項目であり、非破壊で改善可能なため同じ非 digest increment に同梱する（increment #3 が CSS 実行経路修正と Check 40 を 1 つの increment に束ねたのと同様）。

**決定:** `package.json` と `package-lock.json` の root（`packages[""]`）の両方に `"engines": { "node": ">=20" }` を追加し、2 ファイル間で同期させた。`>=20` は「Node 20 以上」を意味し、ワークフローの pin（20）と整合しつつローカル開発で 20 系より新しい Node を禁止しない。npm の `engines` は既定では**警告のみ**（`.npmrc` に `engine-strict=true` が無い限り `npm ci`/`npm install` を失敗させない）ため、宣言自体は非破壊である。

**設計根拠:** これは追加的なメタデータ宣言であり、runtime 依存ゼロ（Check 38 が機械保証）・公開サイトの Vanilla JS という Boring Technology を一切変えない。dev 環境の期待を 1 箇所（`package.json`）に集約することで、ローカルと CI の Node 期待の齟齬を早期に可視化できる。

**検証:** `package.json` 単独追加でも `npm ci` が許容することを確認した上で、`package-lock.json` の `packages[""]` にも同期追加して両ファイルを一致させた（将来の `npm install` が lockfile に `engines` を追記して予期せぬ差分を生むのを防ぐ）。両方追加後に `npm ci` OK、`npm run lint`（0 errors / 199 warnings）、`npm run lint:css` PASS、`npm run check` PASS、Check 38 の 6 行すべて PASS（name `portfolio-aio` / version `0.0.0` / lockfileVersion 3 / devDependencies 一致 / private / runtime 依存ゼロ——いずれも `engines` 追加で不変）を確認。

---

## 3. 意図的に「やらなかった」こと（イエスマンにならないための明示）

### N-1: observational_evidence（監視ログ）の digest ドリフトを ADVISORY へ降格する構造変更は、**今回は採らずオーケストレーター判断に委ねる**

**これは本 increment で最も重要な設計上の論点であり、Yuta の決定を仰ぐべき項目である。**

**観測:** 監視ログは manifest 上で `canonical: false`（引用前の attempt log で、外部 AI が整合性に依存しない観測データ）である。にもかかわらず BLOCKING の digest ゲート対象になっている。つまり**高 churn・非正本の可観測性ファイルの揺らぎ（週次ボット追記＋人間/マージの割り込み）が、整合性強制（integrity enforcement）に結合**している。これは一種のカテゴリ過誤で、より深い構造修正は、**正本（`source_of_truth` / `supporting_evidence`）の digest ドリフトは BLOCKING のまま、非正本の observational_evidence のドリフトだけを ADVISORY（warning）に降格**することである。そうすれば監視ログの揺らぎは二度とビルドを赤くしない。

**なぜ今回やらないか:** これは BLOCKING ゲートを**緩める**変更であり、`repository-maintainability-map.md` §1 の「緩めるのは要判断」に直接該当する。かつ Yuta の確立した「AIO 正本層 原則変更禁止 / digest chain 保全」という整合性ポスチャに触れる。整合性の強制範囲を狭める判断は、設計権限を持つ Yuta が行うべきで、Claude が一存で適用してはならない（最終判断は横井雄太）。

**トレードオフ（Yuta が判断する材料）:**
- 降格する利点: 監視ログ起因のドリフトが構造的に赤化しなくなる（D-1 の原子化に依存しない第二の保険）。観測データの揺らぎと正本の完全性を、設計意図どおり分離できる。
- 降格しない利点（現状維持＋D-1）: digest ゲートの BLOCKING 範囲を一切狭めない＝整合性ポスチャを最強のまま保つ。D-1 の原子化でドリフト源自体が消えているため、降格しなくても今回の赤化は再発しない。
- **Claude の推奨:** まず D-1＋Check 41（本 increment）でドリフト源を断つ非破壊修正を確定させる。ADVISORY 降格は「それでもなお非正本ファイルが BLOCKING である構造を嫌う」場合の**次の一手**として、Yuta の明示判断で別 increment にするのが筋。本修正は BLOCKING を保ったままドリフト原因だけを除去しており、これが最も保守的な非破壊解である。

### N-2: 現在の確定ログ・manifest の内容は触らない（既に整合・緑／不要 churn 回避）

受領 ZIP の監視ログと manifest は既に整合し（ログ sha＝manifest 記録 sha）、`check_aio_digests.py` は緑である。ここでログを正規化（末尾改行付与）して manifest を再生成することも技術的には可能だが、それは現在緑の AIO 正本層に digest bump（sha＋`generated_at` 変更）を**今**刻むことを意味し、「AIO 正本層 原則変更禁止」の精神に反する不要な churn になる。D-2 の serialization 変更はスクリプトの**将来の書き込み**にのみ効かせ、次回の監視 run で manifest と同一コミットに自然に記録させる。これにより現在の byte-identical 状態を保ったまま、地雷だけを除去できる。

### N-3: 監視コミットへの `[skip ci]` 付与はしない（最適化であって障害点除去ではない）

`auto-update-aio-digests.yml` のコミットは `[skip ci]` を付けている。対称性から、D-1 後の監視コミット（ログ＋manifest、機械生成・自己整合）にも `[skip ci]` を付けて検証ゲートの再発火を省く案はある。だが本 increment ではあえて付けない——監視コミットで `architecture-validation` が走り **PASS する**こと自体が、「ボットの原子コミットが runner 上で実際に整合している」ことを確認する良い安全特性である。CI 分のコストは週 1 回の検証 run で無視できる。increment #2/#3 が打ち立てた「**最適化でなく障害点除去なら churn 回避**」に従い、`[skip ci]` 付与（純粋な最適化）は採らない。将来 Yuta が CI 分節約のために採用する余地は残す。

### N-4: `main.js` 199 advisory warnings は触らない（#1/#2/#3 不変方針）

内訳 `curly:124 / no-var:64 / no-shadow:10 / prefer-const:1` はすべて advisory（0 errors）。一括 `--fix` 禁止・視覚回帰 baseline 未取得のため、視覚影響のある変更は baseline 確立後（`main-js-extraction-map.md` の Stage 進行）に回す。#1/#2/#3 から不変。

---

## 4. Not possible と人間の手順

| 項目 | 状態 | 人間の手順 |
|---|---|---|
| GitHub Actions 実実行緑確認 | Not possible（本環境は Actions 不可） | push 後、`architecture-validation`（特に `check_aio_digests.py` ステップ）が緑であることを確認 |
| 次回監視 run の原子コミット挙動 | Not possible（schedule/dispatch は runner 上でのみ実行） | 次の週次 run（または `workflow_dispatch`）後、`chore(aio-monitoring): weekly log update + digest sync …` という**単一コミット**にログと manifest が同梱され、`architecture-validation` が緑であることを確認。D-2 の末尾改行が初回 run でログに反映される（manifest と同一コミット） |
| Playwright baseline PNG 実生成 | Not possible（ブラウザ不可・任意 AI サンドボックスでの生成禁止） | Actions → "Update Playwright Baseline Snapshots" → Run → artifact DL → `e2e/portfolio.spec.js-snapshots/` に配置・commit（**@playwright/test 1.55.1 で生成**）。baseline 未取得が main.js 物理分割前の最大ブロッカーである点は不変 |
| AIO citation 実観測 | 未発生（先行レーンゆえ測定はこれから） | 実引用確認時のみログ記録。confirmed_citation_events=0 は先行起因の観測前状態であり、戦略失敗ではない。捏造禁止 |

---

## 5. C1〜C7 遵守

C1 外部 FW/ライブラリ追加なし（変更は GitHub Actions YAML・Python スクリプト・consistency check、および `package.json` / `package-lock.json` への `engines.node` 追加宣言のみ。runtime 依存ゼロを Check 38 が機械保証し、`engines` 追加後もそれは不変） / C2 IIFE 未変更 / C3 ErrorBoundary 未変更 / C4 FW 再提案なし / C5 人間はコード未記述（実装は Claude Opus 4.8、人間は設計・レビュー・監査・統制） / C6 **AIO テキスト・JSON-LD・バイナリ・`sitemap.xml` 本文・`robots.txt` 本文すべて未変更。本 deliverable では digest も再生成していない**——現在のログ・manifest は既に整合・緑であり、修正対象は digest 連鎖を**維持する自動化（ワークフロー＋書き手スクリプト）**であって連鎖の中身ではない。次回監視 run で D-2 の改行が manifest と同一コミットに反映される / C7 KARTE CDN SRI 非適用維持。すべて遵守。

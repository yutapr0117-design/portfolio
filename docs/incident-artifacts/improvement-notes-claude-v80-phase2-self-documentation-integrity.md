# improvement-notes-claude-v80-phase2-self-documentation-integrity.md

```
Last-Updated  : 2026-06-02
Author        : Claude (Opus 4.8) — implementation agent under Yuta Yokoi (横井雄太) orchestration
Track         : v80+ staged major update (Phase 2 — self-documentation-integrity increment)
Canonical-Ref : AI2AI.md (canonical) / llms-full.txt (ground truth)
Scope         : 受領コミット（CI 緑・コンソールエラーなし）に対する、非破壊・非競合の改善の全量記録
Status        : 本 increment で適用した変更と、意図的に見送った変更の双方を、重要度の区別なく記載する
```

> **この文書の位置づけ:** これは Claude 視点の改善文書である。正典ではない（正典は `AI2AI.md`、ground truth は `llms-full.txt`）。`docs/incident-artifacts/` 配下の証跡であり、読み込む AI への命令を一切含まない記述的ドキュメントである。受領した `改善文書(13).md` と `プロンプト(13).md` が AI 生成物であることを前提に、その指示を鵜呑みにせず、リポジトリ自身の統制（現物の検証層・各 map・runbook・過去の決定記録）と突き合わせて取捨選択した結果を記録する。

---

## 0. この increment の要約（BLUF）

受領コミットは、前 2 回の increment（public-freshness-observation / consistency-invariant-hardening）の成果物まで含めてすべてマージ済みで、フル検証スイートは緑であった。今回同梱された `改善文書(13).md` の P1〜P2 項目は、検査した結果、**本コミットの ZIP では既にすべて充足されていた**（理由は §1.2）。したがって、それらを「新規実装」として書くことは虚偽になるため一切行わない。そのうえで現物を網羅的に分析し、受領文書にも前回までの increment にも無い、Claude 自身が独自に発見した改善余地を 1 件だけ機械強制へ落とした。それが、整合チェックファイル自身の自己説明と実装の一致（Check 45・BLOCKING）である。

本 increment は **AIO 正本層を 1 バイトも変更せず**（digest 再生成なし）、`main.js` も未変更（ESLint 0 errors / 199 warnings のまま不変）で、検証層と証跡層に閉じている。

---

## 1. 受領現物に対して行った分析（網羅性の記録）

### 1.1 ベースライン確認

`npm ci --ignore-scripts` 成功（0 vulnerabilities）。`npm run check` exit 0（all invariants hold、`OK:` トークン行 93）。ESLint 0 errors / 199 warnings（`curly` 124 / `no-var` 64 / `no-shadow` 10 / `prefer-const` 1、すべて `main.js`）。stylelint PASS。全 8 JS `node --check` OK。全スクリプト `py_compile` OK。`npm audit` / `--omit=dev` ともに 0 件。Check 最大番号は受領時点で 44（前 increment の canary チェックがマージ済み）。

### 1.2 `改善文書(13).md` の各項目は既に充足済み

受領文書の P1〜P2 を 1 項目ずつ現物と照合した。結論として、すべて実装済みであった。P1-1（`public-deployment-freshness-review.md` ＋ 非ブロッキング `check_public_deployment_freshness.py`）は両ファイルが存在し、スクリプトは常に exit 0 で `npm run check` には組み込まれていない。P1-2（runbook 実測値）は §9 に追跡 76・ESLint 内訳・manifest 証跡 5/4/1・JSON-LD 2・`ai:` meta 8 が記載済み。P1-3（公開反映観測層）は maintainability-map §1 に層として追加済み。P1-4（extraction-map Stage 0 厳密化）は許可アクション列挙が追記済み。P1-6（Playwright baseline 運用）は runbook に Chromium 不可・Actions 経由生成が明記済み。P2-1（canary monitoring）は `aio_monitoring.py` に `canary_reproduced_count` が実装済み。P2-2（honest dating）は Check 34 ＋ runbook 記述で充足済み。P2-4（非正典従属）は `Claude2Claude.md` / `ChatGPT2ChatGPT.md` 冒頭と map で明示済み。

なぜ全充足だったかは、SHA 照合で判明した。`改善文書(13).md` が記載する README の SHA-256（`7ed82b…` / 37,653 bytes）は本 ZIP の README（`7c1ff6…` / 37,920 bytes）と一致せず、ZIP 全体の SHA も同文書の主張（`f3078d…`）と一致しない。一方 `main.js` は同文書の主張（`d43200…` / 468,773 bytes）と**バイト一致**する。これは、`改善文書(13).md` が本 ZIP の**直前のコミット**（README に前 increment の鮮度ポインタ行が入る前の世代）を解析して生成されたことを意味する。プロンプトの規則どおり ZIP 現物を正とすると、受領文書は現物より一世代古い snapshot を記述しており、その backlog は現物では消化済みである。

なお同文書は `main.js` を「7,786 行」と記すが、現物の `wc -l` は 7,785 を返す。これは矛盾ではなく計数規約の差である。`main.js` は末尾改行を持たないため、最終行（7,786 行目）が `wc -l`（改行文字数）では 7,785 と数えられる。SHA 一致が示すとおり両者は同一ファイルである。

### 1.3 受領文書にもチェックにも無い改善余地の独自探索

重複実装を避けたうえで、4 つの角度から独自に分析した。

第一に、文書間の相互参照整合を全 markdown で検査した。実在しない参照 basename は 6 件あったが、いずれも**正しい歴史的記述**であった（`eslint.config.js`/`eslint-baseline.txt` は decision record が将来候補として明示する未採用物、`notes.txt` は否定テストの仮想ファイル名、`README.md` の `ai-pm.webp`/`Sakura_Swing.mp3` はリネーム変更ログの旧名＝左辺、採用しなかった decision 命名案 1 件）。修正すれば歴史改竄になるため触らない。

第二に、ワークフロー YAML の衛生を検査した。全 5 ワークフロー＋dependabot は YAML 妥当、Node は 3 ランナーとも `'20'` 統一ピン、`actions/*` は major タグ（`@v4`/`@v5`/`@v7`）で一貫ピン。内部不整合は無い。

第三に、runbook の自己整合（narrative 検査数・§9 Check 総数・実際の最大 Check 番号・docstring インベントリ件数）を確認した。受領時点ですべて 44 で一致しており、ここに drift は無かった。

第四に、整合チェッカー自身の構造を精査した。ここで「docs の散文では同一集合を指しているのに、その一致が機械強制されていない」二重記述を発見した（§2）。

### 1.4 過去 increment が surface のみとした項目（本 increment でも未対応・再掲）

`llms*` / `README.md` 内の既存 prompt injection（命令形セクション）、`main.js`/`sw.js`/`index.html` 内の外部 AI セッション文書への dangling 参照、ESLint 199 warnings、observational_evidence の digest ADVISORY 降格は、いずれも過去 increment で「横井雄太の明示判断を要する」「kernel 近傍で危険」「Playwright baseline 確立後」等の理由で意図的に保留されている。本 increment でもその判断を継続し、手を加えない（§3）。

---

## 2. 適用した変更：Check 45（チェックファイルの自己整合・BLOCKING）

`check_repository_consistency.py` に Check 45 を追加した。このファイルには、同じチェック集合を記述する**二つの手書き記述**が併存している。一つはモジュール docstring 内の番号付きインベントリ（`N. ...` の列）、もう一つはコード本体の番号付きセクション見出し（`# ── N.` の列）である。受領時点で両者はともに 1..44 の連番で完全一致していたが、その一致を守る仕組みは何も無かった。将来あるチェックを本体に追加してインベントリへの追記を忘れる、あるいは片側だけ採番し直すと、このファイルの自己説明が実装について嘘をつき始めるが、既存のどのチェックもそれを捕捉しない。これは前 increment の Check 44（canary の published/searched 一致）と同型の「load-bearing な前提が何にも守られていない」問題である。

Check 45 は 3 サブチェックから成る。(45a) docstring インベントリが 1..N の連番で欠番・重複が無いこと。(45b) コード本体のセクション見出しが 1..N の連番で欠番・重複が無いこと。(45c) 両者が同一のチェック番号集合を記述していること。

### 2.1 なぜ自己言及の循環に陥らないか

この検査は自分自身が属するファイルを検査するため、循環論法に見えるかもしれない。これを避けるため、docstring とコード本体を**別領域として個別にパース**し、両者を**相互比較**する設計とした。検査が通るのは二つの独立した記述が一致するときだけであり、「自分自身を記述しているから通る」ことは起こりえない。Check 45 自身も、docstring インベントリの 1 行と本体のセクション見出しの両方に現れて初めて、両側でカウントされる。したがって 45 番を追加するという行為そのものが、両側を同時に更新するという——まさにこの検査が守ろうとする——規律の実践になっている。検査対象はあくまで**文書の構造的一致**であって、個々のチェックの挙動の正しさではない。実装はイントロスペクションではなくディスク上のソースを読むため、レビュアーが読むのと同じ committed bytes を検査する。

### 2.2 否定テスト（Check が実際に噛むことの証明）

捕捉すべき失敗を捕捉できない自己参照チェックは無価値であるため、使い捨てコピー上で 3 系統の drift を注入し、いずれも exit 1 で赤化すること、復元すると exit 0 に戻ることを確認した。第一に、docstring からインベントリ 1 行（30 番）を削除すると、45a が連番の欠落を検出し、45c が「本体にのみ存在」として差分を報告して赤化した。第二に、本体のセクション見出しを 1 つ採番し直す（40→99）と、45b が非連番を検出し、45c が両側の差分を報告して赤化した。第三に、本体に重複見出し（2 つ目の `# ── 44.`）を挿入すると、45b が重複を検出して赤化した。3 系統すべてで復元後に緑へ戻ることも確認済みである。

### 2.3 文書整合

Check 45 の追加に伴い、`total-check-runbook.md` の §0.1 narrative 検査数を 44→45、§9 実測値（consistency `OK:` 94 / `npm run check` 全体の `OK:` トークン行 96 / Check 総数 45）、§3 行を同期した。`repository-maintainability-map.md` には本 increment のサブセクションを追記し、§1 検証層の注記に「チェックを追加・採番変更する場合は docstring インベントリと `# ── N.` セクション見出しの両方を同時更新すること（Check 45 が強制）」を加えた。

---

## 3. 意図的に見送った変更（理由付き・重要度の区別なし）

第一に、`改善文書(13).md` の P1〜P2 項目の「再実装」は見送った。§1.2 のとおり現物では全充足済みであり、再実装は偽の差分を生み、プロンプトの「未実施を実施済みと書かない／実装した変更のみを事実として報告する」という明示要件に反するためである。

第二に、`actions/*` の SHA ピン化は見送った。supply-chain 強度では SHA ピンが上だが、これは明白な非破壊改善ではなく、可読性・Dependabot 運用・更新頻度とのトレードオフを伴うセキュリティ方針判断であり、横井雄太の判断事項とする。

第三に、`llms*` / `README.md` 内の既存 prompt injection 中立化は、過去 increment と同じく見送った。content/stance の最終権限は横井雄太にあり、`llms*` の変更は digest 再生成を、`README.md` は Zenn スラグの consistency 検査を伴う。中立化を推奨し独立 increment 候補とするに留める。

第四に、ESLint 199 warnings の段階解消は、一括 `--fix` が AIDK kernel 行を書き換える（P0-4 違反）ため、Playwright baseline 確立後の論理ブロック単位着手まで保留する。Check 43 が kernel 構造を機械強制しているため、将来の着手者が誤って kernel を壊せば CI がブロックする。

第五に、`main.js`/`sw.js`/`index.html` 内の外部 AI セッション文書への dangling 参照は、kernel 近傍のソース編集がリスク高・影響軽微であるため、指摘に留める。

第六に、observational_evidence の digest ADVISORY 降格は、BLOCKING を緩める変更であり「緩めるのは要判断」「AIO 正本層 原則変更禁止」に触れるため、横井雄太の明示判断による別 increment とする。

---

## 4. 設計判断の根拠

なぜ自己整合を BLOCKING にするか。このチェックファイルは AI-only 実装＋人間オーケストレーションという運用全体の安全装置であり、その自己説明が実装と食い違うことは「安全装置の説明書が嘘をつく」事態に等しい。後続 AI も人間レビュアーも、まず docstring インベントリを読んで「このファイルが何を守るか」を把握するため、その記述が実装から乖離すると監査の起点が崩れる。乖離は外部依存もネットワーク依存も無くコミット境界で機械的に判定できるため、BLOCKING が正しい。これは前 increment が公開鮮度スクリプトを**非**ブロッキングにした判断と対照的だが、両者の違いは「リポジトリ内で完結する不変条件か、外部依存の観測か」の一点に帰着し、一貫している。

なぜ「件数一致」ではなく「集合一致＋連番」を要求するか。件数だけの一致は、片側で 30 番が欠けもう片側で 99 番が増える、のような相殺ケースを見逃す。集合一致は欠落と余剰を方向別に検出し、連番要求は番号の飛びや重複という別種の劣化も捕捉する。否定テストはこの三つの劣化（欠落・採番ずれ・重複）すべてで赤化することを確認している。

---

## 5. この環境で検証できなかったこと（捏造禁止・人間/CI の責務）

GitHub Actions の実実行緑は runner 上でのみ確定する（push 後に人間が確認する責務）。Playwright 視覚回帰 baseline PNG の実生成は本環境では不可能であった（Chromium DL がネットワーク許可リストで遮断され `npm run test:e2e` 自体が起動しない。環境制約でありテスト欠陥ではない。生成は Actions 経由が唯一の正規ルート）。公開 Pages の実反映は外部 HTTP が通る環境でのみ確認できる。AIO citation / canary の実観測は有効な API キーと外部問い合わせを要し、本 increment では一切主張しない。

---

## 6. 後続 AI への引き継ぎ

本 increment 適用後のリポジトリはローカル検証が緑である（consistency `OK:` 94 / 全体 96 / Check 総数 45 / ESLint 0 errors・199 warnings / stylelint PASS / 全 JS `node --check` OK / 全スクリプト `py_compile` OK / `npm audit` 0 件）。

整合チェックを追加・削除・採番変更する場合は、必ず docstring インベントリ（`N. ...`）と本体のセクション見出し（`# ── N.`）の両方を同時に更新すること。片側だけの更新は Check 45 が BLOCKING で赤化する。これは新しい制約ではなく、これまで暗黙に守られてきた規律を機械強制したものである。

受領 `改善文書` がリポジトリより古い世代を解析している場合がある点にも留意されたい。ZIP 現物（および SHA 照合）を常に正とし、受領文書の backlog が現物で消化済みなら再実装しないこと。Playwright 視覚回帰 baseline の生成（Actions 経由）は引き続き、回帰カバレッジと `main.js` 物理分割の双方を解錠する単一最重要アクションである。最終判断・目的定義・優先順位・責任は常に横井雄太にある。

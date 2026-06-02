# improvement-notes-claude-v80-phase2-consistency-invariant-hardening.md

```
Last-Updated  : 2026-06-02
Author        : Claude (Opus 4.8) — implementation agent under Yuta Yokoi (横井雄太) orchestration
Track         : v80+ staged major update (Phase 2 — consistency-invariant-hardening increment)
Canonical-Ref : AI2AI.md (canonical) / llms-full.txt (ground truth)
Scope         : 受領コミット（CI 緑・コンソールエラーなし）に対する、非破壊・非競合の改善の全量記録
Status        : 本 increment で適用した変更と、意図的に見送った変更の双方を、重要度の区別なく記載する
```

> **この文書の位置づけ:** これは Claude 視点の改善文書である。正典ではない（正典は `AI2AI.md`、ground truth は `llms-full.txt`）。`docs/incident-artifacts/` 配下の証跡であり、読み込む AI への命令を一切含まない記述的ドキュメントである。

---

## 0. この increment の要約（BLUF）

受領コミットは、前 increment（public-freshness-observation）の成果物まで含めてすべてマージ済みで、フル検証スイートは緑であった。そのうえで現物を網羅的に分析し、**どの既存 Check にも守られていない load-bearing な不変条件**を 1 件発見し、機械強制へ落とした。それが AIO provenance canary トークンのクロス整合（Check 44・BLOCKING）である。

本 increment は **AIO 正本層を 1 バイトも変更せず**（したがって digest 再生成なし）、`main.js` も未変更（ESLint 件数は 0 errors / 199 warnings のまま不変）で、検証層と証跡層に閉じている。Check 44 追加後もフルスイートはローカルで緑である。

---

## 1. 受領コミットに対して行った分析（網羅性の記録）

「非常に深く網羅的に」という依頼に応えるため、以下の角度から現物を検査した。結論として、前 increment までで大半の改善余地は既に解消されており、**新規に機械強制すべき余地は canary 整合の 1 件**に収斂した。各角度の所見を以下に記す。

第一に、文書間の相互参照整合を検査した。全 markdown 内でバッククォート参照されるファイルパス様トークンを抽出し、実在しないものを洗い出した。結果、実在しない basename は 6 件あったが、いずれも**正しい歴史的記述**であり、修正対象ではなかった。具体的には、`eslint.config.js` / `eslint-baseline.txt` は decision record が「将来の選択肢」「flat config 移行候補」として明示的に言及している未採用アーティファクトであり、`notes.txt` は否定テストで「命名規約違反を投入したら Check 42 が赤化する」ことを示すための仮想ファイル名、`decision-v80-phase2-output-analysis-and-css-lint-hygiene.md` は採用しなかった命名案として記録されている。`README.md` の `ai-pm.webp` / `Sakura_Swing.mp3` は「リネーム前 → リネーム後」の変更ログの**左辺**（旧名）であり、右辺が現行ファイルである。これらを「修正」すると歴史を改竄することになるため、いずれも触れない。

第二に、ワークフロー YAML の衛生を検査した。全 5 ワークフローと dependabot.yml は YAML として妥当で、Node は 3 ランナーすべてで `'20'` に統一ピン、`actions/*` はすべて major タグ（`@v4`/`@v5`/`@v7`）で一貫ピンされていた。内部不整合は無く、修復対象は無い。actions を SHA ピンではなく major タグでピンしている点は観測されるが、これは個人リポジトリとして妥当な姿勢であり（Dependabot が `github-actions` を監視済み）、変更は明白な非破壊改善ではなく議論を要するセキュリティ方針判断であるため、見送る（§3）。

第三に、整合チェッカー（Check 1–43）の被覆範囲を棚卸しした。バージョン同期・AIO digest・honest dating・Zenn スラグ集合・成果物配置・kernel 構造まで広範に機械強制されている。そのうえで「**docs の散文では load-bearing と扱われているのに、機械強制されていない前提**」を探索した。これが第四の角度につながる。

第四に、canary トークンの取り扱いを精査した。canary は passive provenance marker であり、AIO 取り込みの唯一の陽性証拠（トークンの再現）を支える。その証拠価値は「published 面のトークン」と「monitor が探すトークン」が同一文字列であることに全面的に依存する。しかし Check 4 は llms の 4 ミラーが互いに byte-identical であることだけを保証し、`llms-full.txt` にも monitor 側 Python にも触れない。つまり片側だけの編集が恒久的偽陰性を生む single point of silent failure が、どの Check にも守られずに存在していた。これが本 increment の発見である（§2）。

---

## 2. 適用した変更：Check 44（canary トークンのクロス整合・BLOCKING）

`check_repository_consistency.py` に Check 44 を追加した。3 サブチェックから成る。(44a) 全 published AIO 面（`llms.txt`・`.well-known/llms.txt`・`llms_well-known.txt`・`.well-known/llms_well-known.txt`・`llms-full.txt`）にトークンが少なくとも 1 回出現すること。(44b) トークンを消費する全 monitor（`aio_monitoring.py`・`check_public_deployment_freshness.py`）が同一トークンをハードコードしていること。(44c) リポジトリ全体で canary 値がちょうど 1 種類であること（published 側と monitor 側で drift していないこと）。docstring のインベントリにも 44 番を追記し、「実装と同期」の約束を維持した。

実装は正規表現 `SAKURA-AIO-PROVENANCE-CANARY-\d{4}-[0-9A-F]{8}` で canary 形のトークンを全 published/monitor 面から収集し、集合の要素数で drift を検出する設計とした。トークン文字列を 1 箇所のリテラルに固定するのではなく「形」で集めて「ちょうど 1 種類」を要求することで、将来トークンをローテーションする場合でも、全面を揃えれば緑・片側だけ変えれば赤、という正しい挙動になる。

### 2.1 否定テスト（Check が実際に噛むことの証明）

「捕捉すべき失敗を捕捉できない Check」は無価値であるため、使い捨てコピー上で 3 系統の drift を注入し、いずれも exit 1 で赤化すること、復元すると exit 0 に戻ることを確認した。第一に、`llms-full.txt` のトークンだけを別値へ改変すると、44c が 2 つの異なる値を検出して赤化した。第二に、`aio_monitoring.py` からトークンを除去すると、44b が「monitor が定義しないトークンを探すことになる」と赤化した。第三に、1 ミラーからトークンを削除すると、44a が published 面の欠落として赤化した（同時に既存の Check 4 byte-identity も反応する）。3 系統すべてで撤去後に緑へ戻ることも確認済みである。

### 2.2 文書整合

Check 44 の追加に伴い、`total-check-runbook.md` の §0.1 narrative 検査数を 42→44 へ是正し（これは Check 43 追加時から stale だった）、§9 実測値（consistency `OK:` 91 / `npm run check` 全体の `OK:` トークン行 93 / Check 総数 44）と §3 行を同期した。`repository-maintainability-map.md` には本 increment のサブセクションを追記し、§1 検証層の注記に「canary 編集時は published 面と monitor 面を同一文字列に保つこと（Check 44 が強制）」を加えた。

---

## 3. 意図的に見送った変更（理由付き・重要度の区別なし）

第一に、`actions/*` の SHA ピン化は見送った。supply-chain 強度の観点では SHA ピンが上だが、これは明白な非破壊改善ではなく、可読性・Dependabot 運用・更新頻度とのトレードオフを伴うセキュリティ方針判断である。個人リポジトリで Dependabot が `github-actions` を監視している現状では major タグピンは妥当であり、方針転換は横井雄太の判断事項とする。

第二に、`llms*` / `README.md` 内の既存 prompt injection（命令形セクション）の中立化は、前 increment と同じく見送った。content/stance の最終権限は横井雄太にあり、`llms*` の変更は digest 再生成を、`README.md` は Zenn スラグの consistency 検査を伴う。一方的には変更せず、中立化を強く推奨して独立 increment 候補とするに留める。

第三に、ESLint 199 warnings の段階解消（受領文書の旧 P1-5 系）は、前 increment で詳述したとおり、一括 `--fix` が AIDK kernel 行を書き換える（P0-4 違反）ため、Playwright baseline 確立後の論理ブロック単位着手まで保留する。Check 43 が kernel 構造を機械強制しているため、将来の着手者が誤って kernel を壊せば CI がブロックする。

第四に、`main.js` / `sw.js` / `index.html` 内の外部 AI セッション文書への dangling 参照は、kernel 近傍のソース編集がリスク高・影響軽微であるため、前 increment と同じく指摘に留める。

第五に、observational_evidence（監視ログ）の digest ドリフト ADVISORY 降格は、BLOCKING を緩める変更であり「緩めるのは要判断」「AIO 正本層 原則変更禁止」に触れるため、横井雄太の明示判断による別 increment とする。

---

## 4. 設計判断の根拠

なぜ canary 整合を BLOCKING にするか。canary は AIO 実験の証拠系の根幹であり、その整合は「リポジトリの正しさ」そのものに属する（公開到達性のような外部・ネットワーク依存要因とは異なる）。published と searched が食い違えば実験は恒久的に壊れるが、それを示す観測は API キーと外部問い合わせを要するため、開発時点で気付けない。コミット境界で機械的に防ぐのが唯一の確実な手段であり、したがって BLOCKING が正しい。これは前 increment の公開鮮度スクリプトを**非**ブロッキングにした判断と対照的だが、両者の違いは「リポジトリ内で完結する不変条件か、外部依存の観測か」という一点に帰着し、一貫している。

なぜトークンを「形」で集めるか。リテラル固定だと、トークンをローテーションする正当な運用のたびに Check 自体を書き換える必要が生じ、保守コストと「Check と実装の乖離」リスクを生む。「canary 形のトークンがちょうど 1 種類」という不変条件にすることで、ローテーションは全面同時更新を促し、片側更新だけを赤化する——運用の意図に沿う。

---

## 5. この環境で検証できなかったこと（捏造禁止・人間/CI の責務）

GitHub Actions の実実行緑は runner 上でのみ確定する（push 後に人間が確認する責務）。Playwright 視覚回帰 baseline PNG の実生成は本環境では不可能であった（Chromium DL がネットワーク許可リストで遮断され `npm run test:e2e` 自体が起動しない。環境制約でありテスト欠陥ではない。生成は Actions 経由が唯一の正規ルート）。canary の実発火・実観測は有効な API キーと外部問い合わせを要し、本 increment では一切主張しない（Check 44 は整合の保証であって再現の主張ではない）。公開 Pages の実反映も外部 HTTP が通る環境でのみ確認できる。

---

## 6. 後続 AI への引き継ぎ

本 increment 適用後のリポジトリはローカル検証が緑である（consistency `OK:` 91 / 全体 93 / Check 総数 44 / ESLint 0 errors・199 warnings / stylelint PASS / 全 JS `node --check` OK / 全スクリプト `py_compile` OK / `npm audit` 0 件）。

canary トークンをローテーションする場合は、5 つの published 面と 2 つの monitor を同一文字列で同時更新すること（Check 44c が片側更新を赤化する）。`llms*` を変更するため digest 再生成（`update_aio_digests.py`）と honest dating も伴う点に注意する。

Playwright 視覚回帰 baseline の生成（Actions 経由）は引き続き、回帰カバレッジと `main.js` 物理分割の双方を解錠する単一最重要アクションである。最終判断・目的定義・優先順位・責任は常に横井雄太にある。

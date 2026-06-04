# improvement-notes-claude-v80-phase2-ci-baseline-pipeline-hardening

```
Author        : Claude (implementation), under Yuta Yokoi (横井雄太) orchestration
Track         : v80+ staged major update (Phase 2)
Increment     : CI baseline-pipeline hardening (Playwright baseline commit automation + CI-log-derived hardening)
Date          : 2026-06-04
Canonical-Ref : AI2AI.md (canonical) / docs/architecture/repository-maintainability-map.md
Status        : 適用済み（npm run verify フル緑・48 checks・AIO 正本層と binary は byte-identical）
```

> **正本階層:** `AI2AI.md` が canonical、`llms-full.txt` が ground truth。本ファイルは increment 単位の改善記録（incident artifact）であり、上位文書と矛盾する場合は上位を正とする。

---

## 1. この increment の発端と要約

この increment は、二つの入力から始まった。ひとつは CI ログ一式（`logs_72279442292.zip`）と最新コミットの現物が渡されたこと。もうひとつは「『Playwright baseline 取得（Stage 5 の前提）』の意味が分からないので、ログを渡したという側面もある」という問いである。つまり依頼は、ログを解析して非破壊で適用できる改善をすべて見つけて適用することと、baseline という概念の正体を明らかにし、可能なら baseline 取得の実準備、さらには実装にまで踏み込むこと、の両方であった。

解析の結論を先に述べる。baseline の機構はリポジトリに完全に実装済みでありながら、「CI が生成した PNG を人間がダウンロードして手でコミットする」という最後の一手が一度も完了されていないために、baseline が存在しない。これがまさに Stage 5（render/router/view-transition の物理分割）を律速していた「協力を要する一点」の正体であった。本 increment は、その最後の一手を自動化し、baseline を「ワークフローを 1 回 dispatch して PR をマージするだけ」で取得できる状態へと前進させた。あわせて、CI ログが示した CodeQL のクエリ群を手がかりに、編集対象のワークフローに潜んでいたコマンドインジェクション面を解消し、新たに生じた権限結合を BLOCKING チェックで固定した。

これまでの increment と同じく、本 increment は AIO 正本層・binary・`main.js`・`style.css`・`index.html` を 1 バイトも変更しておらず、digest 再生成も不要である。変更は検証層（ワークフロー 1 本と consistency チェッカ）に閉じている。

---

## 2. 「Playwright baseline 取得」とは何か、なぜ Stage 5 の前提なのか

この概念を、仕組みから順に説明する。`playwright.config.cjs` は `toHaveScreenshot` というアサーションを `threshold: 0.05` で宣言している。これは*視覚的回帰（visual regression）*テストである。視覚回帰テストの原理は「比較」にある。テストはライブのページを headless Chromium で描画し、スクリーンショットを撮り、それを*以前に保存しておいた基準画像*——baseline あるいは snapshot と呼ぶ——とピクセル単位で比較する。新しいスクリーンショットが baseline と閾値を超えて異なれば、テストは失敗し、「何かが視覚的に変わった」ことを告げる。

これが Stage 5 の前提である理由はこうだ。Stage 5 は描画・ルーティング・view-transition のコードを動かす。そのような移動が「ユーザーに見える出力を変えていない」ことを*証明*する唯一の方法は、移動の前後で描画結果を信頼できる基準と比較することである。baseline が無ければ基準が無く、基準が無ければ比較できず、比較できなければ安全網が存在しない。だから extraction-map は Stage 5 を baseline 確立後にゲートしている。

では、なぜ baseline は一度も取得されなかったのか。`update-playwright-snapshots.yml` のコメントが答えを明示している。意図された手順は、人間が手動でこのワークフローを dispatch し、ワークフローが baseline PNG を CI ランナー内で生成して*アーティファクト*としてアップロードし、その後*人間がそのアーティファクトをダウンロードして PNG を `e2e/` にコミットする*、というものだった。ワークフローは意図的に `main` へ直接コミットしない（コメントに `このワークフローは直接 main にコミットしない（人間のレビューゲートを保持）` とある）。つまり baseline が不在なのは単純で構造的な理由による——手動の dispatch とダウンロード・コミットの往復が完了されたことがない。機構は完備しているが、人間の一手が欠けていた。

---

## 3. この環境で「できないこと」の正直な境界

踏み込んだ実装に入る前に、越えられない境界を正直に示す。私はこのサンドボックスで baseline 画像そのものを生成できない。理由は具体的で回避不能である。baseline 生成にはライブのページを描画する実 Chromium が必要で、ワークフロー自身が `npx playwright install --with-deps chromium` でそれをダウンロードするが、このサンドボックスのネットワーク許可リストがそのダウンロードを遮断する。本 increment で実際に試行し、`403 Forbidden`（`deb.nodesource.com` への取得失敗、`Failed to install browsers ... exited with code: 100`）を観測して確認した。したがって PNG の実バイトは、ネットワークが無制限の GitHub Actions でのみ生成できる。これが「Actions が唯一の正規ルート」の意味である。

私はプレースホルダ画像を捏造して baseline と称することはしない。偽の基準は回帰テストを無意味な画素に対して走らせることになり、無いよりも有害だからである。

それでも「準備」を越えて前進できる余地はあった。ワークフローはアーティファクトのアップロードで止まり、人間にダウンロードとコミットを委ねていた。その手動の往復こそが baseline 取得を阻んできた摩擦である。そこを自動化すれば、baseline は「理論上取得可能」から「dispatch ＋ マージの一手で取得可能」へ前進する。これが本 increment の実装の核である。

---

## 4. 実装：baseline コミット経路の自動化

`update-playwright-snapshots.yml` に、生成された baseline PNG を*プルリクエストとしてコミットする*ステップを追加した。機構には `peter-evans/create-pull-request`（この用途のデファクト標準アクション）を用いる。変更されたファイルをステージし、ブランチを作り、コミットし、PR を開く、までをワークフロー自身のトークンで行う。手書きの `git` コマンドとトークン操作ではなく実績あるアクションを選んだのは安全のためである——CodeQL の `ExcessiveSecretsExposure` や `ArtifactPoisoning` クエリが検出するのは、まさに手製のトークン操作が招きがちなパターンであり、検証済みアクションは安全なパターンを内包する。

PR を選び、`main` への直接 push を選ばなかったのは、本ワークフローの設計が常に要求してきた人間レビューゲートを保つためである。PR は二つの要求を同時に満たす——摩擦を除去しつつ（手作業のファイル運搬が消える）、人間が新しい baseline を承認してから基準になる、というゲートを保つ。アーティファクトのアップロードも fallback として残した。PR ステップに何か起きても、人間はアーティファクトから PNG を回収できる。経路を*追加*し、既存の経路を*除去していない*——真の意味で非破壊である。

権限については、PR を開くために `contents: write`（ブランチ push）と `pull-requests: write`（PR open）が必要なので、従来の `contents: read` から最小限に昇格した。この昇格は正当かつ必要で、あなたのリポジトリに既にあるパターン（`auto-update-aio-digests.yml` が `contents: write` で動く）に倣っている。範囲を 2 権限に限定したことは CodeQL の `MissingActionsPermissions`（CWE-275）を満たす。

---

## 5. CI ログ由来の硬化：CWE-094 コマンドインジェクション面の解消

CI ログが読み込んだ 18 個の CodeQL クエリは、本コミットで findings ゼロ——現状の CI は clean である。しかしそのクエリ群は、GitHub Actions ワークフローを危険にしうる経路のチェックリストそのものであり、私はまさにそのルールセットでスキャンされる新ワークフローを書こうとしていた。だからログは、私自身の変更に対する受け入れ基準を手渡してくれたに等しい。

そのうえで、編集対象のワークフローに既存の問題を見つけた。`Print instructions` ステップが `echo "Reason: ${{ github.event.inputs.reason }}"` という形で、user 制御の入力をシェルコマンドに直接補間していた。これは `CodeInjectionCritical`（CWE-094）が狙う典型パターンである。GitHub Actions は `${{ }}` をシェルが見る前に*テンプレート置換*する——user のテキストをスクリプトに literally 貼り付ける。だから `"; rm -rf . #` のような reason を dispatch されれば、その行は複数のシェルコマンドに化ける。現在のランが緑で誰も悪意ある reason を与えなかったから無害だっただけで、これは潜在的なインジェクション面である。新しい特権ステップを足すついでにこれを放置するのは一貫性を欠く。修正は標準の安全パターン——入力を env 変数に束ね、シェルでは `$REASON` として参照する。env 変数はコードでなくデータなので、シェルはその値をメタ文字として再パースしない。

CI ログの観察として、CodeQL ワークフローは `actions/checkout@v6` を用いるがリポジトリ内の全ワークフローは `@v4` である、という version skew も見つけた。ただしこれは欠陥ではなく（`@v4` は有効・サポート対象）、全ワークフローを churn して版番号を追うのは「最小・可逆・美観目的でない」原則に反するため、本 increment では既存 pin を変更せず観察記録に留めた。

---

## 6. Check 48 新設と、否定テストが暴いた私自身の欠陥（正直な記録）

権限の昇格は新しい手書きの結合を生む。`update-playwright-snapshots.yml` は PR 作成ステップを持ち、そのステップは `contents: write` ＋ `pull-requests: write` が無ければ機能しない。これらは同一ファイルの別箇所（上部の permissions ブロックと下部の PR ステップ）に住むため、silently drift しうる。将来の編集が権限を read-only に戻しつつ PR ステップを残せば、ステップは実行時に分かりにくい権限エラーで失敗し、事前には何も捕捉しない。そこで「PR ステップがあるなら 2 つの write 権限を宣言していること」を BLOCKING で固定する Check 48 を新設した。Check 29 が env シグナルをワークフローと spec の間で結合するのと同じ思想である。

ここで正直に記録すべき出来事がある。Check 48 の初版は、否定テストで*自分の欠陥を露呈した*。私は「権限を read-only に戻せば Check 48 が発火する」と予測したが、否定テストは exit 0・発火ゼロを返した。原因はこうだ。初版の正規表現は `contents:\s*write` という緩い形で、ワークフロー*全体*のテキストを走査していた。ところが私が書いた permissions ブロックのコメントには、説明のために「contents: write」「pull-requests: write」という語が散文として書かれていた。だから否定テストが実ディレクティブ行を read-only に変えても、チェックは私自身が書いたコメント内の語にマッチして「権限あり」と結論した。チェックが*自分のドキュメントを読んでいた*のである。これは本物の欠陥だ——コメントが旧状態を記述したままなら、実権限の後退をチェックが見逃す。

ここに、テキストベースのチェックの微妙な落とし穴という、転用可能な教訓がある。ファイルがディレクティブとその記述を両方含むとき、素朴な部分文字列・緩い正規表現はその二つを区別できない。修正は、bare なトークンではなく YAML ディレクティブの*構造形*にマッチさせること——行頭アンカー（`re.MULTILINE`、キーの前は空白のみ）を要求すれば、`  contents: write` はマッチするが `  #   contents: write` はマッチしない。`#` と余分なテキストが行頭の空白とキーの間に挟まるからである。これでチェックは語彙でなく構造を読む。

修正後、否定テストを再実行して三つを確認した。(A) 正しい状態（PR ステップ＋両 write 権限）で緑、(B) PR ステップを残し権限だけ read-only に戻すと——コメントの記述は意図的に残したまま——発火し、欠けた 2 権限を名指しする、(C) PR ステップ自体を消すと artifact-only への正当な回帰として権限不要で緑のまま。この (C) が、チェックが過剰でない（正当な簡素化を禁じない）ことを示す。

この一件が体現する原則を明示しておく——*壊そうとしていないチェックは、まだ信頼できないチェックである*。初版は正しく見え、緑ですらあったが、実権限の後退をすり抜けさせる形で静かに壊れていた。意図的に不変条件を破ってみて初めて欠陥が露わになり、修正がテキストチェックの一般的な罠について転用可能な教訓を残した。その教訓は今 Check 48 のコメント自身に刻まれているので、次の保守者は罠を再発見せず受け継げる。

---

## 7. 検証と非破壊の確認

すべての変更後、フル `npm run verify` は exit 0（48 checks・all invariants hold・AIO digest passed・binary passed・Stylelint PASS・ESLint 0 errors / 194 warnings）。編集した 2 ワークフローは YAML として妥当（Check 23）。Check 29 の baseline 生成リンク（`PLAYWRIGHT_UPDATE_SNAPSHOTS` のワークフロー↔spec 結合）は編集後も保持（私は生成ステップの env も spec も触っていない）。Check 45 の自己整合は docstring インベントリと実装見出しがともに 1..48 で一致。

非破壊アンカー：`index.html`・`llms.txt`・`llms-full.txt`・`AI2AI.md`・`.well-known/aio-manifest.json`・`sitemap.xml`・`robots.txt`・`style.css` はすべて受領時と SHA 完全一致。`main.js` も本セッションでは未変更（このコミットの分割済み状態のまま）。digest 再生成不要。

---

## 8. この環境で検証できなかったこと（Not possible・捏造禁止）

事実と未検証を分離して記録する。Chromium の実ダウンロードとブラウザ起動（サンドボックスのネットワーク許可リストが遮断、`403 Forbidden` 実測）、Playwright baseline PNG の実生成（Actions が唯一の正規ルート）、GitHub Actions 上での実実行緑確認、改修した PR 作成ワークフローの Actions 上での実 dispatch、公開 Pages への実反映、AIO citation の実観測——これらはいずれもこのサンドボックスの外にあり、push 後・dispatch 後・公開後にのみ確認できる。

---

## 9. 次フェーズへの引き継ぎ：baseline をどう取得するか

baseline 取得は、いまや次の手順で完了する。第一に、改修した本コミットを push する。第二に、GitHub の Actions タブで「Update Playwright Baseline Snapshots」ワークフローを「Run workflow」ボタンで dispatch する。Actions 上では Chromium が入るので baseline PNG が生成され、それを載せた PR が自動で開く。第三に、その PR のスクリーンショット差分をレビューしてマージする。これで baseline が `e2e/portfolio.spec.js-snapshots/` に確定する。第四に、以降 rendered asset に触れる PR では `playwright-regression` ワークフローが screenshot 差分を baseline に対して enforce するようになる——これが Stage 5（render/router/view-transition の物理分割）の前提条件の充足である。

baseline 確立後、Stage 5 に進める。それまでの間、Stage 4（service rails の抽出）は baseline 非依存で安全に進められる部分（`Storage` のような自己完結した薄いラッパ）から着手できる。状態や永続化スキーマに触れる service rail は、baseline 確立後に回すのが安全である。

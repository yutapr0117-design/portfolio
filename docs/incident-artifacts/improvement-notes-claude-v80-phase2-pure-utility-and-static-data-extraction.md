# improvement-notes-claude-v80-phase2-pure-utility-and-static-data-extraction

```
Author        : Claude (implementation), under Yuta Yokoi (横井雄太) orchestration
Track         : v80+ staged major update (Phase 2)
Increment     : pure-utility + static-data extraction (main.js Stage 2 / Stage 3)
Date          : 2026-06-04
Canonical-Ref : AI2AI.md (canonical) / docs/architecture/main-js-extraction-map.md
Status        : 適用済み（npm run verify フル緑・47 checks・AIO 正本層と binary は byte-identical）
```

> **正本階層:** `AI2AI.md` が canonical、`llms-full.txt` が ground truth。本ファイルは increment 単位の改善記録（incident artifact）であり、上位文書と矛盾する場合は上位を正とする。

---

## 1. この increment が行ったこと（要約）

オーナー横井雄太が 2026-06 にオーナー権限で `main.js` の物理分割を許可したことを受け、`main-js-extraction-map.md` が定める「副作用の小さい順」の抽出計画に沿って、最もリスクの低い 2 段階を実施した。すなわち Stage 2（純粋ユーティリティの抽出）と Stage 3（静的データの抽出）である。具体的には、`main.js` の単一 IIFE 内に同居していた純粋ユーティリティ 10 関数を `js/pure-utils.js` へ、静的なクイズデータ 4 つを `js/quiz-data.js` へ、いずれも同一オリジンのローカル ES モジュール（依存ゼロの葉モジュール）として切り出し、`main.js` 冒頭の module-level `import` で取り込んだ。

この結果、`main.js` は 7,785 行（≈468 KB）から 6,353 行（≈352 KB）へ、1,432 行の減少となった。抽出した各ファイルには、何を・なぜ・どんな入出力か・保つべき不変条件（特に `sanitizeUrl` のセキュリティ境界）を説明する詳細な日本語コメントを厚く付与した。これはオーナーの「分割で小さくなった分、要所要所に各処理を詳細に説明するコメントを大量に足す」という方針に従ったものである。

抽出した 10 関数は `generateId` / `clamp` / `debounce` / `throttle` / `tokenize` / `slugify` / `sanitizeUrl` / `safeFetchJSON` / `deepClone` / `yieldToMain`。抽出した 4 データセットは `awsQuizData` / `pmQuizData` / `qualityQuizData` / `architectureQuizData` である。

---

## 2. なぜ「pure utility」と「static data」だけを切り出し、render/router/kernel を切らなかったのか

抽出順序が「副作用の小さい順」である理由は、視覚回帰 baseline の有無と直結している。純粋関数は定義上、出力が引数のみで決まり、DOM・モジュール内クロージャ状態・読み込み順序のいずれにも依存しない。静的データに至っては関数ですらなく、振る舞いを持たない不活性なオブジェクトである。この 2 種は、別ファイルへ移して `import` しても挙動が変わらないことを静的に保証できる。したがって、描画の同一性を検証する Playwright baseline がまだ存在しない現段階でも、安全に実施できる。

対照的に、render/router/view-transition 層（Stage 5）は描画とタイミングに依存するため、「コードレビュー上は正しく見える」ことと「実際に同一に描画される」ことが乖離しうる。その乖離を検出する唯一の計器が視覚回帰 baseline であり、それを欠いたまま切るのは安全網なしの綱渡りになる。service rails（Stage 4）はその中間で、状態や `localStorage` スキーマに触れるものを含むため、本 increment では着手していない。要するに、ここで止めたのは慎重さのための慎重さではなく、検証可能性の境界に正直であろうとした結果である。「Stage をできる限り前へ」という要望に対しても、最大化すべきは安全に前進できる範囲であって、リスクのある編集の数ではない。

---

## 3. 安全性をどう保証したか（非破壊の証明）

この increment では、抽出が挙動を変えていないことを多層で証明した。各層は `docs/architecture/main-js-extraction-map.md` §3.3 にも要約されているが、本ファイルではその根拠をより詳しく述べる。

第一に、**抽出前の依存解析**である。抽出候補 14 名すべてについて、`main.js` のクロージャ束縛（`CONSTANTS` / `SITE_CONFIG` / `Store` / `state` / `RouteState` / `EffectRails` / `BindingRegistry` / `PAGE_META` / `Router` / DOM ビルダ `h()`）を一切参照しないこと、すなわち closure-deps = none であることを確認した。これが、別モジュールへ移しても挙動が保たれることの静的な裏付けである。

第二に、**純粋ユーティリティの挙動検証**である。モジュールが ESM としてロードでき、10 関数すべてが期待どおり動作することを Node で実行確認した。特に `sanitizeUrl` が `javascript:` スキームを拒否し続けること（セキュリティ境界の保存）、`slugify` がフォールバックで `generateId` を正しく呼ぶこと（モジュール内依存の解決）、`deepClone` が独立したコピーを返すこと（破壊的変更の不在）の 3 点を重点的に確認した。

第三に、**静的データの byte-equivalence 証明**である。4 データセットを `main.js` の該当行範囲から手入力せずに抽出し、各データセットの本文が元と 1 バイト違わず一致すること（宣言行のみ `export` 接頭辞とインデント差）を機械的に照合した。データ本文がバイト等価であれば、パース後のオブジェクトも必然的に同一であり、これはクイズの中身が変わっていないことの最も強い保証になる。加えて、4 ブロックそれぞれが単独でパースでき、モジュール全体が ESM としてロードできることを二重に確認した。

第四に、**不変領域の verbatim 連続性**である。抽出によって触れていない 3 つの連続領域——kernel + constants（196 行）、`clear()` + Safe Storage（48 行）、Store Module から EOF までの 5,864 行——が、再構築後の `main.js` にバイト単位で連続して存在することを照合した。とりわけ 3 つ目の 5,864 行は、全コンポーネント・ルータ・レンダラ・AIDK レール・エラーバウンダリを含むアプリケーションの本体であり、これがバイト単位で不変であることは、抽出が意図した 14 名以外に一切触れていないことの決定的な証拠である。

第五に、**AIO 正本層と binary の byte-identity** である。`index.html`・`llms.txt`・`llms-full.txt`・`AI2AI.md`・`.well-known/aio-manifest.json`・`sitemap.xml`・`robots.txt`・`style.css` は受領時と SHA が完全一致しており、digest 再生成は不要であった。本 increment が触れたのは `main.js` と新規 2 モジュール、検証層、ドキュメントに閉じている。

---

## 4. near-miss の正直な記録（4 データセットのうち 2 つしか export しかけた）

この increment では、危うく Copilot 型のリファクタ事故——大きな塊を移すときに一部を黙って取りこぼす事故——を起こしかけた。記録として正直に残す。

クイズデータは `main.js` 内で 4 つ定義されている（`awsQuizData` / `pmQuizData` / `qualityQuizData` / `architectureQuizData`）。ところが抽出の初期ドラフトでは、これらが連続した領域に並んでいたために「2 つのデータブロック」と誤認し、`awsQuizData` と `architectureQuizData` の 2 つだけを `js/quiz-data.js` へ export し、間に挟まっていた `pmQuizData` と `qualityQuizData` を取りこぼした。この状態のまま進んでいれば、`main.js` の lookup table が未定義の 2 名を参照し、ブラウザでモジュールロードエラーを起こして SPA 全体が起動しなくなっていた。build step を持たず GitHub Pages が直接配信するこのサイトでは、この種の不整合はビルド時ではなく実行時に初めて露見する、最も検出しにくい失敗である。

これを捕捉できたのは、検証チェーンが機能したからである。ESLint を `sourceType: module` に切り替えた結果、module モードの厳格な `no-undef` が `pmQuizData` / `qualityQuizData` への未定義参照をエラーとして可視化した。そのエラーを pristine（受領時の `main.js`）と突き合わせて追跡したところ、抽出対象が 2 つではなく 4 つであったことが判明し、4 つ全てを byte-equivalent に抽出する形へ修正した。

そして、この失敗を二度と起こさないために仕組み化した。これがオーナーの discover→document→systematize→memorize→optimize の核心である。後述する Check 47（import/export bijection）を新設し、「4 つあるデータのうち 2 つしか export しない」状態を否定テストとして再現したところ、Check 47a が exit 1 で発火し、欠けている 2 名（`pmQuizData` / `qualityQuizData`）を名指しで報告することを確認した。つまり、もし将来同じ取りこぼしが起きても、それはコミット前の BLOCKING チェックで必ず捕捉される。一度の失敗が恒久的なガードレールに変換された。

---

## 5. 抽出によって生じた契約をどう機械強制したか（Check の変更）

物理分割は、これまで `main.js` 内部で完結していた関係を、複数ファイルにまたがる手書きの契約へと変える。オーナーの「新規分割で生じた手書き重複は必ず machine-enforced check 化して固定する」という方針に従い、3 つのガードを追加・更新した。いずれも否定テストで「正しく発火すること」と「緩めすぎていないこと」を証明している。

**Check 43d の更新（既存ガードの誤発火対応）。** Check 43d は `main.js` が単一の top-level IIFE で始まること（C2 — グローバル名前空間を汚染しないこと）を検証する。ES モジュールの `import` は構文上トップレベル（関数の外）に置く必要があるため、抽出後は import が IIFE に先行する。これにより 43d が「IIFE が壊れた」と誤検出した。これは誤検出であって実際の退行ではない——IIFE は不変領域の verbatim 照合で完全に保たれている。そこで、先頭の `import ...;` 文（と `use strict` ディレクティブ）を除去してから IIFE 開始を探すよう更新した。重要なのは、これが C2 を緩めていない点である。許容するのは import 文（モジュールスコープの束縛であってグローバル汚染ではない）だけであり、import 以外のトップレベル宣言（裸の `const`/`let`/`var`/`function`）は従来どおり fail する。否定テスト 2 種——IIFE 開始をグローバル `const` に置換、import と IIFE の間に裸の `var` を注入——がいずれも exit 1 で発火することを確認し、緩めすぎていないことを証明した。

**Check 46 の拡張（lint 被覆）。** 抽出した 2 モジュールは `js/` 配下にあるが、lint スクリプトと Check 46 のディスク真値は root 直下の `*.js` のみを対象にしていた。このままでは新モジュールが gate されない。そこで lint スクリプト（`lint` / `lint:js`）に両モジュールを追加し、Check 46 のディスク真値を root ∪ js/ に拡張した。この設計により、今後 Stage 4/5 で `js/` にモジュールを追加しても、それらは自動的に lint 被覆の対象として要求され、被覆が静かに分割に遅れることがない。

**Check 47 の新設（import/export 契約）。** これが near-miss を恒久的に防ぐガードである。`main.js` が各ローカルモジュールから import する名前の集合と、各モジュールが export する名前の集合が、過不足なく一致する（厳密な全単射）ことを BLOCKING で検証する。加えて、各モジュールが葉（import を持たない）であることも確認する。これは Boring Technology の「ユーティリティ・データ層は依存グラフの末端にある」原則の機械強制でもある。実装上の注意として、import リストは各名に inline `//` コメントを持つためコメントを先に除去してから識別子を抽出し、また各 `import {…} from '<module>'` ブロックを孤立して照合する（捕捉する波括弧グループを `[^{}]*?` とし、隣接ブロックへ食い込まないようにする）。否定テスト 4 種——欠けた export、孤立 export、葉でないモジュール、そして near-miss の再現（4 つ中 2 つのみ export）——がいずれも exit 1 で発火することを確認した。

なお、これら 3 つの変更はすべて Check 45 の自己整合（docstring インベントリと `# ── N.` 見出しの一致）を保ったまま行った。Check 46 の説明更新と Check 47 の新設は、docstring インベントリと実装セクション見出しの両方を同時に更新しており、Check 45 が両者の一致を検証して PASS している。

---

## 6. 意図的に抽出しなかったもの（境界の記録）

何を抽出しなかったかは、何を抽出したかと同じくらい重要である。

`clear(node)` と `Storage` は抽出しなかった。前者は DOM ノードを変更し、後者は `localStorage` をラップする——いずれも純粋ではなく、副作用を持つ service rail だからである。抽出順序の原則に従い、これらは Stage 4 の領分として `main.js` に残置した。

定数（`SITE_CONFIG` 等）も抽出しなかった。ここにはガードが教えてくれた明確な境界がある。Check 2 は `SITE_CONFIG.VERSION` を、Check 17 は `LAST_UPDATED` を、いずれも `main.js` から名前で読み取る。したがって定数を別ファイルへ移すと、これら 2 つのチェックが期待する文字列を `main.js` 内に見つけられなくなり、壊れる。これは「機械強制チェックが特定ファイルから名前で読む文字列は抽出不可」という汎用原則の good example であり、ガードが抽出境界を教えている。

---

## 7. この環境で検証できなかったこと（正直な境界）

リポジトリ内で完結する検証——consistency checks、AIO digest、binary metadata、CSS lint、ESLint、`node --check`、各種挙動テスト、byte-equivalence 照合——はすべてこのサンドボックスで緑であることを確認した。しかし、以下はこのサンドボックスの外にあり、ここでは検証できていない。事実と未検証を分離して記録する。

第一に、**GitHub Actions 上の CI 緑**は、ローカルの `npm run verify` 緑とは別物である。CI の最終確認は push 後にのみ可能である。第二に、**Playwright 視覚回帰 baseline** はこのサンドボックスで生成不能である（Chromium のダウンロードがネットワーク許可リストで遮断されるため）。baseline 取得の唯一の正規ルートは GitHub Actions であり、これは Stage 5（render/router 分割）の前提条件として依然未充足である。第三に、**公開反映**（GitHub Pages への配信結果）と、第四に、**AIO の被引用観測**（confirmed_citation_events）は、いずれも公開後・観測後にしか確認できない。本 increment は `main.js` の内部構造の保守性改善であり、公開面の表示や AIO 戦略の被引用とは独立であるが、念のため境界として明示しておく。

---

## 8. 次フェーズへの引き継ぎ

次の着手候補は Stage 4（service rails の抽出）である。`Storage` のような自己完結した薄いラッパは比較的安全だが、状態や永続化スキーマに触れるものは後方互換に注意が要り、視覚回帰 baseline 確立後に回すのが安全なものもある。Stage 5（render/router/view-transition/kernel 周辺）は、描画・遷移・タイミング依存のため、GitHub Actions 経由で Playwright baseline を確立してからでなければ着手すべきでない。`js/` にモジュールを追加する際は、Check 47 が要求する import/export の一致と葉性を保つこと、Check 46 が要求する lint 被覆への追加を忘れないこと。これらは BLOCKING で強制されるため、怠ればコミット前に必ず検出される。

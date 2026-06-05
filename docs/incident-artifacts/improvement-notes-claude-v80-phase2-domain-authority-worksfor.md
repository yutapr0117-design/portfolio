# improvement-notes-claude-v80-phase2-domain-authority-worksfor

```
Author        : Claude (implementation), under Yuta Yokoi (横井雄太) orchestration
Track         : v80+ staged major update (Phase 2)
Increment     : domain-authority worksFor linkage (employer entity connected to the Person across JSON-LD + AIO canonical layer)
Date          : 2026-06-04
Canonical-Ref : AI2AI.md (canonical) / docs/architecture/repository-maintainability-map.md
Status        : 適用済み（npm run verify フル緑・49 checks・digest 再生成済）
```

> **正本階層:** `AI2AI.md` が canonical、`llms-full.txt` が ground truth。本ファイルは increment 単位の改善記録（incident artifact）であり、上位文書と矛盾する場合は上位を正とする。

---

## 1. この increment の二つの依頼と要約

この increment は二つの依頼から成る。第一に、トータルチェック（リポジトリ全層の健全性検証）。第二に、所属会社である株式会社日本経営のドメインオーソリティを構造化データへ組み込むこと、すなわち横井雄太という比較的新しいエンティティを、既に社会的に確立された組織エンティティへ意味的に連結することである。

第一の依頼への結論を先に述べる。全層を個別に検証し、いずれも緑であった。consistency は 49 checks すべて invariants hold、AIO digest・binary metadata・CSS lint・JS 構文も通過し、ESLint は 0 errors / 194 warnings（既知の `main.js` 負債）。一点だけ、grep が `repository-maintainability-map.md` 内に「検査数 40→41」「41→42」という文字列を拾ったが、これはドリフトではない。本ドキュメントは各 increment を append-only で記録する設計であり、それらは過去の increment が当時行った遷移の記録である。runbook の現行 narrative は「49 個の整合チェック」で正しい。歴史記録と現状値を混同せず、歴史は書き換えない。

第二の依頼への対応が本 increment の実質である。横井雄太が 2026 年 6 月 11 日より株式会社日本経営のシェアデータベース事業部・主幹（課長格）として勤務するという事実を、`index.html` の JSON-LD と AIO 正本層の双方に組み込んだ。組み込む情報の境界は「内部でしか知り得ない情報か否か」とした。会社名・役職・事業部は外部から確認可能な事実なので含め、給与・契約条件・個人情報は内部情報なので一切含めていない。

---

## 2. なぜ「強い組織への連結」が個人エンティティに効くのか（戦略の技術的裏付け）

この戦略の背後にある原理を、仕組みから説明する。ナレッジグラフ（Google の Knowledge Graph に代表される）は、エンティティをノード、関係をエッジとして表現する巨大な意味ネットワークである。新設された個人のノード（ここでは横井雄太）は、それ単体では「弱い」。同姓同名の学術研究者など、既に多くの被リンクと履歴を持つ強いノードにベクトルの強さで負けるからである。ところが、その弱いノードから強く確立されたノード（株式会社日本経営）へ明確なエッジ（worksFor＝雇用関係）を一本張ると、グラフ解決の挙動が変わる。エンジンは「この新しいノードは、あの確立された組織に所属する別個の実体だ」と理解しやすくなる。確立されたエンティティの「重み」が、エッジを通じて弱いノードの識別可能性を引き上げる、というのが原理である。

これは依頼者（横井雄太）が参考として共有した他 AI の見解が述べる戦略の方向性であり、その方向性自体は妥当である。問題は実装の具体にあった。

---

## 3. 参考 JSON-LD の欠陥と、なぜそのまま採用しなかったか（正直な技術的批判）

イエスマンにならないという運用方針に従い、参考として渡された JSON-LD コードをそのまま採用しなかった理由を具体的に記録する。戦略は採用したが、実装の具体はほぼ全面的に直す必要があった。

第一の、そして最も重大な欠陥は `@id` の値である。`@id` は JSON-LD において「そのエンティティを一意に指す正準 URI」である。参考コードは Person の `@id` を `"https://github.io"` としていた。これは本人のドメインですらない、GitHub Pages のルートドメインである。これを自分の同一性として宣言すると、ナレッジグラフエンジンに対して誤った実体マッピングを送ることになる。リポジトリの既存 JSON-LD は既に正しく `"@id": "https://yutapr0117-design.github.io/portfolio/#person"`（実サイト上のフラグメント URI）を用いており、参考コードはこの正しい既存実装より劣化していた。

第二に、解説文とコードの矛盾である。解説は「worksFor 内に `#organization` という共通識別子を明記している」と述べていたが、提示されたコード自体にその `#organization` は存在しなかった。

第三に、`sameAs` の誤りである。`sameAs` は「このエンティティと同一の実体を指す別 URL」を列挙する属性で、同一性の証拠として機能するには本人のプロフィール URL でなければならない。参考コードは `"https://zenn.dev"` や `"https://x.com"` というサービスのトップページを指しており、これは何の同一性も証明しない。

したがって本 increment は、戦略（worksFor で確立済みエンティティへ連結）のみを採用し、実装は次の三点で正しく直した。Person の `@id` は既存の実サイト URL（`#person`）を維持。組織参照は正準 URL（`https://nkgr.co.jp/#organization`）で張る。そして独立した断片を貼り付けるのではなく、既存の `@graph` に統合する。

---

## 4. 実装：JSON-LD への worksFor ↔ Organization の追加

`index.html` の第1 JSON-LD ブロックには、既に well-formed な `@graph`（複数の連結エンティティが兄弟として並び、`@id` で相互参照する構造）が存在した。中心となる Person ノードは正しい正準 `@id` を持ち、`jobTitle`・`sameAs`・`memberOf`・`hasOccupation` を備えていたが、雇用先（worksFor）への関係だけが欠けていた。ここが依頼の埋めるべき隙間であった。

実装は二つの編集から成る。第一に、既存の authoritative Person ノードに `worksFor` を追加した。これを単なる `{"@id": ...}` 参照ではなく `OrganizationRole` という型で表現した点が要点である。`OrganizationRole` は schema.org が「人物が組織内で持つ特定の役割」を表すために用意したイディオムで、人物と組織の間に位置し、`roleName`（主幹（課長格））と `namedPosition`（シェアデータベース事業部）と `startDate`（2026-06-11）を保持しつつ、組織は `@id` で参照する。これにより、役職という人物側の属性を、誤って組織ノードに付与してしまう（「組織が主幹である」という無意味な記述になる）ことを避けられる。第二に、同じ `@graph` に Organization ノードを兄弟として追加した。正準 `@id` は `https://nkgr.co.jp/#organization`、name は株式会社日本経営、そして `employee` で Person を相互参照する。@graph のノード数は 9 から 10 になった。

重要な設計判断として、第2 JSON-LD ブロック（hero 画像と BGM の creator stub）には worksFor を追加しなかった。これらは Person を `@id`（`#person`）でのみ参照しており、JSON-LD のグラフ解決では完全な Person 定義を継承する。したがって雇用関係をここに複製する必要はなく、むしろ複製は将来のドリフト源になる。雇用先は authoritative な Person ノードに一度だけ定義し、`@id` 参照に継承させるのが正しい。

---

## 5. 正本層への反映と digest 再生成（依頼第二の「全ファイル」指示）

依頼者は「第一の情報を適切なファイル全てに含める」よう明示した。そこで JSON-LD だけでなく、AIO 正本層（AI agent が直接読むグラウンドトゥルース）にも同じ雇用事実を反映した。これは多くの過去 increment が正本層を byte-identical に保ってきたのと異なる、意図的なスコープ拡大である。依頼が全サーフェスへの反映を明示的に求めたためであり、その帰結として digest 再生成を伴う。

反映先は四つの正本ファイルである。`llms.txt` には構造化された Affiliation 行と、人物を説明する Atomic Answer の散文の両方に追記した。ここで Check 4 の制約に注意を払った。Check 4 は `llms.txt` とその三つのミラー（`.well-known/llms.txt`・`llms_well-known.txt`・`.well-known/llms_well-known.txt`）が byte-identical であることを BLOCKING で強制する。四つを個別に手編集すると、空白や改行の差で byte-identity が崩れるリスクがある。そこで、編集した `llms.txt` を単一ソースとして三つのミラーへ複製し、byte-identity を構築的に保証した。複数ファイルの同一性を保つには、各々を独立に編集するのではなく単一ソースから派生させるのが安全である、という一般原則の適用である。`AI2AI.md` は Project Identity テーブルに Affiliation 行を追加し、`llms-full.txt` は Q&A 散文に追記した。

正本層の内容を変えたため、digest チェーンの再生成が必須となった。`llms.txt`・`llms-full.txt`・`AI2AI.md` は `.well-known/index.json`（とそのミラー）および `aio-manifest.json` に SHA-256 が記録されており、内容を変えると記録ハッシュと実体が食い違い、AIO digest チェックが（正しく）失敗する。`update_aio_digests.py` を実行して全ハッシュを再計算・書き換え、`check_aio_digests.py` で再検証して緑を確認した。digest システムの整合機構が設計どおり機能していることの確認でもある。

---

## 6. Check 49 新設と否定テスト（宙吊り参照の機械的防止）

worksFor ↔ Organization の連結は、新しいクロスファイル（厳密には同一ファイル内クロスノード）の手書き契約を生む。discover→document→systematize の原則に従い、これを機械強制チェックに落とした。

守るべき失敗モードは「宙吊り参照（dangling reference）」である。戦略の強度は、第1 JSON-LD グラフ内で三つの事実が一致し続けることに依存する。Person が worksFor を持ち、その（ネストを含む）参照が組織の正準 `@id` を指し、その `@id` を持つ Organization ノードが同じグラフに実在すること。静的配信される本サイトでは、宙吊り参照は silent failure である。worksFor が存在しない `@id` を指していても、ページは描画され JSON もパースされるが、雇用エッジが解決されない。つまり「強いエンティティへ連結する」という戦略の根幹が、見た目は正常なまま静かに崩れる。Check 49 はこれを pre-commit 時に捕捉する。

実装上の注意として、worksFor は直接参照（`{"@id": ...}`）の場合と、OrganizationRole ラッパーで一段ネストした参照（`{"@type": "OrganizationRole", "worksFor": {"@id": ...}}`）の場合の両方がありうる。本実装ではこの両形を解決する。正規表現ではなく実際の JSON パースを用いた。JSON-LD のネスト構造は正規表現が苦手とする対象だからである。また worksFor が存在しない場合は正当な状態として緑にした。将来 worksFor を削除する（雇用先を載せない）ことは合法であり、それを過剰検出してはならないからである。

否定テストで効力を実証した。前回 Check 48 の初版が緩い正規表現でコメント内 prose にマッチして発火しなかった教訓（壊そうとしていないチェックは信頼できない）を踏まえ、今回は最初から二系統の否定テストを行った。(A) Organization ノードの `@id` を別名に改名し worksFor を宙吊りにすると exit 1 で発火し、宙吊りになった `@id`（`#organization`）を名指しし、定義済み org @id が `#org-RENAMED` のみであると報告した。(B) Organization ノードごと削除すると exit 1 で発火し、定義済み org @id が空であると報告した。いずれも原因を正確に示しており、ガードに本物の効力があることを確認した。Check 45 の自己整合も 1..49 で保たれている。

---

## 7. 検証と非破壊の確認

すべての編集後、フル `npm run verify` は exit 0（49 checks・all invariants hold・AIO digest passed・binary passed・Stylelint PASS・ESLint 0 errors / 194 warnings）。第1・第2 JSON-LD ブロックはいずれも妥当な JSON としてパースされる。

非破壊の範囲を明確に記録する。本 increment は `main.js`・`style.css`・binary（webp / mp3）を一切変更していない。変更は `index.html`（JSON-LD）と正本層四ファイル（digest 再生成を伴う）、および consistency チェッカとドキュメントに閉じる。他の多くの increment と異なり、本 increment は意図的に AIO 正本層を編集している点が特徴である（雇用事実を全サーフェスへ反映する依頼のため）。digest は再生成済みで、byte-identity を要する `llms.txt` 四コピーは単一ソースから複製して同一性を保証した。

---

## 8. この環境で検証できなかったこと（Not possible・捏造禁止）

事実と未検証を分離して記録する。Google や AI search が実際にこの worksFor エッジを解決し、「株式会社日本経営の主幹である横井雄太」として名寄せ・識別するかどうかは、外部エンジンの挙動であり、このサンドボックスでは検証できない。これは公開後・クロール後・観測後にのみ判明する。同様に、公開 Pages への実反映、および confirmed_citation_events の実増加（依然 0 であり、これは戦略の失敗ではなく先行しているがゆえの未観測）も、いずれも外部の観測待ちである。本 increment が保証するのは構造化データの正しさと内部整合であって、外部エンジンがそれをどう解釈するかではない。

---

## 9. 次フェーズへの引き継ぎ

雇用先の構造化データは JSON-LD と正本層の双方に整合的に組み込まれ、Check 49 が宙吊り防止を機械強制している。将来 `index.html` の JSON-LD で雇用関係を編集する際は、worksFor が参照する組織 `@id` と Organization ノードの `@id` を必ず一致させること。これは BLOCKING で検出されるため、怠ればコミット前に必ず捕捉される。正本層（`llms.txt` ミラー群・`llms-full.txt`・`AI2AI.md`）の雇用記述を更新する場合は、`llms.txt` 四コピーの byte-identity（Check 4）を単一ソース複製で保ち、`update_aio_digests.py` で digest を再生成することを忘れないこと。役職・所属の変更が生じた場合（昇格・異動等、外部から判明する範囲）は、JSON-LD の OrganizationRole と正本層四ファイルの記述を同期して更新する。

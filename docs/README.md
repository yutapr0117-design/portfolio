# `docs/` — ドキュメント配置規約と成果物タクソノミー

このファイルは、リポジトリ `docs/` ツリーの**配置規約（どの成果物をどこへ・どんな名前で置くか）**を定める単一の正本である。`v80+` Phase 2 の artifact-placement governance increment で導入した。目的は、AI（実装担当）と人間（オーケストレーター）のどちらが作業しても、成果物の置き場所と命名がぶれないようにすることであり、規約は `check_repository_consistency.py` の **Check 42（BLOCKING）**で機械強制されている。すなわちこのドキュメントは「説明」、Check 42 は「強制」であり、両者は対になっている。

> **正本階層について:** ルートの `llms-full.txt`（ground truth）と `AI2AI.md`（AI 間ハンドオフの canonical）が最上位の正本であり、`docs/` 配下の文書はそれらに従属する補助成果物である。`docs/` の記述がもし `AI2AI.md` / `llms-full.txt` と矛盾した場合は、後者が優先する。

## なぜ配置を規約化するのか

リポジトリは「AI が実装し、人間が設計・統治する」運用を採っている。AI は会話ごとに文脈が切り替わるため、成果物の置き場所が暗黙知のままだと、増えるたびに少しずつ散らばる。散らばりは後続の AI/人間が「どこを見ればよいか」を見失う保守コストになる。これを避けるため、配置を文章で明文化し（本ファイル）、さらに機械検査（Check 42）で逸脱を CI でブロックする。これは本リポジトリの一貫した哲学——運用ルールを発見したら手動運用で終わらせず、ドキュメント＋機械強制の「仕組み」に落とす——の一適用である。

## ディレクトリ・タクソノミー

`docs/` は次の 4 つのサブツリーからなる。それぞれの役割と「何を置くか」を述べる。

`docs/architecture/` は、長期的に有効な構造・設計のリファレンスを置く場所である。具体的には、リポジトリ全体の保守性マップ（`repository-maintainability-map.md`）、`main.js` 段階分解の計画（`main-js-extraction-map.md`）、そして全整合チェックの運用手引きである総点検 runbook（`total-check-runbook.md`）がここに属する。ここに置くのは、特定の 1 コミットに紐づくものではなく、リポジトリの構造そのものを説明し続ける文書である。

`docs/incident-artifacts/` は、各変更（increment）に紐づく**決定記録（decision record）と改善文書（improvement notes）、および保存された実験成果物**を置く場所である。decision record は「何を・なぜ決めたか／意図的にやらなかったことは何か」を残す不変の記録であり、improvement notes は「その increment で何を改善し、何が backlog として残るか」を残す retrospective ＋ backlog である。過去の実験の痕跡（例: v70 実験で棄却された workflow YAML）も、再現性と監査のためここに保存する。

`docs/evidence/` は、観測的・実証的な証跡を置く場所である。AIO 監視ログ（`aio-monitoring-log.json`、`canonical:false` の attempt log）や、AI パイオニア同一性レビュー（`ai-pioneer-identity-review.md`）がここに属する。ここに置くのは「観測された事実の記録」であり、解釈や設計判断ではない。

`docs/session-records/` は、AI 間セッション記録のアーカイブ（`AI2AI-archive.md` など）を置く場所である。`AI2AI.md`（最新のハンドオフ正本）から溢れた過去のセッション記録を、読み取り専用の歴史的証跡として保管する。

## 命名規約（`docs/incident-artifacts/` 配下）

`docs/incident-artifacts/` 直下のファイルは、次の表のいずれかの命名に従う。Check 42 はこの規約をファイル名で機械的に検査する。

| 種別 | 命名パターン | 例 |
|---|---|---|
| 決定記録 | `decision-v<version>-<slug>.md` | `decision-v80-phase2-ci-hygiene-4.md` |
| 改善文書 | `improvement-notes-<author>-v<version>-<slug>.md` | `improvement-notes-claude-v80-phase2-ci-hygiene-4.md` |
| 保存実験成果物 | `*.yml`（棄却・保存された workflow 等） | `update-portfolio.v70-experiment.yml` |
| 本説明ファイル | `README.md` | （本ファイル） |

`<version>` はパイプライン/トラックの版（`v74`, `v80` 等。複数版にまたがる場合は `v76-v77` のように連結可）、`<slug>` は内容を表すケバブケースの短い識別子、`<author>` は改善文書を書いた主体（`claude` 等）である。命名系列の連番（`ci-hygiene` → `ci-hygiene-2` → `ci-hygiene-3` …）は、保守者の発見可能性のため可能な限り維持する。

逆向きの規約として、`decision-*.md` と `improvement-notes-*.md` という名前のファイルは **`docs/incident-artifacts/` の外に置いてはならない**。Check 42 はこの逸脱（置き場所違反）も検出する。

## 改善文書（improvement notes）のリポジトリ内位置づけ

「改善文書はリポジトリに含めるべきか、それとも AI に渡す改善文書とリポジトリ内の改善文書は分けるべきか」という設計上の問いに、本規約は次のように答える。

本リポジトリにおける `improvement-notes-*.md` は、**リポジトリ内に存在すべき耐久的な成果物**である。これは「その increment で何を直し、何が未了で残り、なぜそう判断したか」という retrospective ＋ backlog であり、後続の AI/人間が文脈を引き継ぐための durable な記録だからである。`decision-v74-...` 以降、改善文書は一貫して `docs/incident-artifacts/` に置かれてきた。

一方、外部 AI（任意の LLM）から受け取る**戦略提案・助言の文書**は、ジャンルが異なる。それは特定の AI の一時的な提案であり、リポジトリの正本成果物集合に属させるものではない。提案は評価の対象であって、採用された部分だけが decision record（採否と理由）や improvement notes（backlog）へ畳み込まれる。したがって「AI に渡す/AI から受け取る助言文書」と「リポジトリ内の改善文書」は**役割が別**であり、前者を canonical artifact として混在させない。もし AI 向けの独立したブリーフ（要約・指示書）が必要なら、それは正本成果物とは分離した別ジャンルとして扱い、`AI2AI.md`（AI 間ハンドオフの canonical）がその役割の正本窓口である。

要するに、decision record と improvement notes はリポジトリ内に置く耐久成果物であり、外部 AI 助言は評価対象であって正本ではない——この線引きが配置規約の一部である。

## 関連する正本・機構

本配置規約に関わる主要なファイルは次のとおりである。整合チェックの全体像は `docs/architecture/total-check-runbook.md` を、保守性の全体マップは `docs/architecture/repository-maintainability-map.md` を参照。配置規約の機械強制は `.github/scripts/check_repository_consistency.py` の Check 42 が担う。AIO 正本層（`llms-full.txt` / `AI2AI.md` / `llms*` alias / `.well-known/*` / digest / バージョン文字列）は digest chain 保全のため原則変更禁止であり、本 `docs/` 配下の文書はこれに従属する。

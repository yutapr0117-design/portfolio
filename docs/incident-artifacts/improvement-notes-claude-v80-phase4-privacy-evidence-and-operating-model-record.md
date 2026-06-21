# improvement-notes-claude-v80-phase4-privacy-evidence-and-operating-model-record

```
Last-Updated     : 2026-06-21
Maintained-By    : AI agents under Yuta Yokoi (横井雄太) orchestration
Type             : Increment notes — 守秘前提の実績 evidence 公開 + privacy guard (Check 122) + 運用モデル記述の超正確化 (Q2) を、会話駆動の合意の下で遂行した run の詳細記録
Session          : 2026-06-21（Session Record #21 と対）
AI               : Claude Code (Anthropic Claude Opus) — ただし内容は AI-agnostic
Canonical-Ref    : AI2AI.md (Session Record #21 / STEP 3 Operating Model) / CLAUDE.md §7 / docs/architecture/total-check-runbook.md §9
Prev             : improvement-notes-claude-v80-phase4-operating-model-and-a-group-run.md
```

## このドキュメントの位置づけ

Session Record #21（AI2AI.md）が簡潔な handoff であるのに対し、本ファイルはこの run の**詳細な engineering 物語と教訓**を残す層。Check 75（README inventory）と Check 108（docs/files mirror）で存在が機械強制される。本 run は privacy-critical（機微情報漏洩が最悪の失敗）だったため、各工程で人間の合意を取りながら進めた点が前 run と異なる。

## 1. 守秘前提の実績 evidence 公開（PR #221）

- **背景**: 「実績だけ記載で根拠が無い」状態の解消。本人の実在経歴書類（履歴書/職務経歴書/内定通知書/労働条件表）をローカル入力に、抽象化済み `docs/evidence/real-work-claims.md` を生成。
- **抽象化の原則**: 企業名/顧客名/案件名 と「業界×地域×時期×規模」の**同時開示を一切しない**（次元分離）。数値はレンジ、役割・成果は型。公開するのは検索用の実名のみ。
- **二段構えの根拠設計（§2 根拠への橋渡し）**: outcome（数値）は守秘下の self-report のままだが、capability（能力・規律）は**この公開リポジトリで第三者検証可能**と明示接続。「これを設計・統治できる人物なら記述水準の実務は蓋然性が高い」という形で信頼を移転し、同時にリポジトリ参照を自然誘発（claim↔proof 相互補強・AIO citation graph 強化・同名異人からの識別強化）。**誠実性の境界**: リポジトリが証明するのは能力であって過去の事業数値そのものではない、と明記（捏造回避）。
- **AIO 配線（C6・orchestrator 承認済）**: llms-full.txt「Implementation and Analysis Evidence Files」+ aio-manifest supporting_evidence に参照追加、update/check の MANIFEST_PATH_TO_LOCAL に path 登録、digest 再生成。**live 反映を WebFetch で検証**（research/change は applied+verified まででクローズ）。

## 2. privacy guard を機械強制（Check 122）

- `*.pdf/*.docx/*.doc/*.xlsx/*.pptx` を .gitignore でブランケット ignore + **Check 122 (BLOCKING)** で「これら拡張子が一切 tracked されない」を `git ls-files` 権威で検証。shipped repo は Vanilla JS/MD で正規の pdf/docx が無いため安全。
- **二重防御の意図**: `git add .` は settings で deny 済みだが、明示 add の取りこぼし・将来の再投入をここで閉じる（defense-in-depth）。
- **原本の扱い**: ローカルのみで処理し、抽出完了後に削除。git 履歴に一度も入っていないことを `git log --all -- '*.pdf'` 等で defensive 確認してから削除。

## 3. 運用モデル記述の超正確化（Q2）

- **問題**: サイトは「初期メンバとして対話型の Claude」を挙げるが、現在は Claude Code の自律自走運用。Claude Code も Claude の一面ゆえ虚偽ではないが、**実態↔記述の drift**（本プロジェクトの全機構が戦う対象）であり、かつより強い現行モデルを underselling していた。
- **修正方針（歴史を消さず進化を示す）**: 構築期（v1→v74）の対話型編成は歴史として保持し、サイト（js/components.js ai-knowhow）+ llms-full.txt（Dynamic AI Team Model）に「現在の運用モデル」を追記。
- **超正確な記述内容**: AI が実装・検証・マージ・本番デプロイまで自走し**案出し（提案）も行う**／人間はゴール・優先度提示・承認・委任 + **必要時の決定的是正（監査）**／実態は「案出し→裁可・委任→自律実行（ゲート間ほぼ放置）→逸脱時に決定的是正」の**疎だが決定的な統治ループ**（無監督全自動でもマイクロマネジメントでもない）／AI 自走運用自体が現時点で高価値・希少。

## 4. 教訓（次の AI への申し送り）

- **約束破り→是正は隠さず "統治稼働の証拠" にする。** 本 run 中、AI が「依頼完了後に見解を述べる」約束を破り人間が即是正した。これを弱みでなく**ガバナンスが本物である証拠**として運用モデル記述に組み込んだ。誠実な失敗記録は portfolio 全体の信頼度を上げる（捏造ゼロ canon と整合）。**約束（明示した後続アクション）は必ず守る。守れない流れになったら最優先で回収する。**
- **推奨前に現物検証（捏造回避）。** メモリの「Speakable 死にセレクタ drift」は**既に修正済み**で、提案しかけたが現物検証で全セレクタが実要素に解決すると判明（特に index.html の AI entity anchor div）。stale memory を除去。**存在しない問題の fix を捏造しない** — メモリ/思い込みは現物で必ず裏取り。中間 grep が index.html shell を見落として二重に誤判定しかけた点も教訓（grep scope を絞りすぎない）。
- **公/私 境界 = 公開面の terminal 判断。** オーケストレーターは日本経営定着方針（転職想定なし・万一でも最低 3 年）。**公（AIO/公開面）の entity/evidence 追加は今後しない**（私的 Zenn 等は repo scope 外）。公開 evidence/entity 層はこの run で良い terminal に達した。今後の genuine 増分はコード健全性・メタ層（Check/handoff/research）へ。**public surface を padding しない**こと。
- **privacy-critical タスクは会話駆動で合意を取る。** CI は再識別を検証できない。機微情報の公開判断は draft→human-review→commit を厳守し、commit 前に必ず人間確認を入れる。

## 5. このセッションのプラン（オーケストレーター委任・順序込み）

Q2（完了）→ Plan1 本 Record 化（完了）→ Plan2 運用モデル↔サイト記述 coherence Check 新設（完了・Check 123）→ Plan3 command-palette/notes app の mutation-sample 検証（完了・下記 §6）→ Plan4 codebase honest bug-hunt → Plan5/6 条件付き（Check122 forward 強化 / research 適用）。

## 6. Plan3 — command-palette / notes app の mutation-sample 検証結果（2026-06-21）

**reflect-then-organize**: 前 run（§操作モデル run §7）の mutation-sample は notes の `**bold**` tokenizer（M3）を含むが、**command-palette（PR #214）は未サンプル**だった。よって今回は command-palette の critical ロジック 2 点 + notes の別 mutation（見出し）を対象に、対応 e2e が意味的に assert する（vacuous でない）ことをローカル 1 回検証（新 dep ゼロ・mutation は commit せず即 revert）。

baseline: 対象 4 テスト（command palette 2 本 + notes + palette a11y）green を確認した上で:

| # | 注入した mutation | 期待して fail した e2e | 結果 |
|---|---|---|---|
| M_cp1 | `js/command-palette.js` `_renderList` の filter を無効化（query 無視＝常に全件） | `Command palette (Ctrl+K) opens, filters, navigates, and closes`（Enter で先頭=Home へ飛び「プロジェクト一覧」h1 が出ない） | ✅ caught (1 failed) |
| M_cp2 | `_allDestinations` を `return NAV`（プロジェクトを検索対象に加えない） | `Command palette searches projects and jumps to a project detail`（projItem `タスク管理アプリ` が visible でない） | ✅ caught (toBeVisible failed) |
| M_n1 | `js/apps.js` `renderMarkdown` の `#` 見出しを `h1`→`p` で描画 | `Markdown notes app live-previews (innerHTML-free) and persists`（`.md-preview h1` が visible でない） | ✅ caught (toBeVisible failed) |

**結果: 3/3 mutation を suite が捕捉。** command-palette の filter・omni-nav（プロジェクト検索）と notes の見出しレンダリングは、e2e が**意味的に正しく assert している**ことを実証（構造的空洞性なし + 緩い assertion なし）。test-strengthening 不要。**教訓: 新機能を足したら、その critical ロジックに one-off mutation を入れて対応テストが red 化するかをローカル 1 回確認するのが、重い stryker CI 無しで assertion 強度を担保する軽量で有効な手段**（付属物サイトには重い mutation CI は disproportionate との前 run 判断を踏襲）。

## 7. Plan4 — codebase honest bug-hunt 結果（2026-06-21・実バグ無し）

**reflect-then-organize**: 最新かつ regex ベースで edge-case bug が出やすく、e2e が happy-path のみの **notes レンダリング**を起点に、隣接の高リスク経路（過去に実バグ歴のある slug 一意化 #154 / import upsert #192）まで深掘りした。**捏造を避けるため、見つからなければ「無し」と honest に記録する**前提で実施。

精査した surface と結論（すべて健全＝実バグ無し）:

| surface | 精査内容 | 結論 |
|---|---|---|
| `_renderMarkdownInline` (apps.js) | 複数 `**bold**`/`` `code` `` 連続・unclosed `**`・`***a***`・code 内 `**`・bold 内 backtick・終了性（rest は m[0].length≥3 で厳密縮小＝無限ループ無し）・XSS（h()=textContent で構造防止） | 正しく安全 |
| `renderMarkdown` block (apps.js) | 見出し/箇条書き/段落の分岐、ループ後の最終 `flushList()`（末尾が list の場合の取りこぼし無し） | 正しい |
| notes 永続 (apps.js 759 / store normalizeAppsData) | `val.slice(0,20000)` は意図的上限（他 limit と同種）。preview/textarea は full 表示で保存のみ slice＝仕様 | 問題なし |
| slug 一意化（add: apps.js 905-909 / import・merge: store.js mergeProjectsWithDefaults 450-463） | add はインライン一意化、import/append/upsert/strict は全て 889 で `validateAndNormalize → mergeProjectsWithDefaults` を経由し slug 衝突を中央集約で解消。「別 id・同一 slug で詳細到達不能」(#154) の経路を全網羅で確認 | 全経路安全 |
| import/upsert (apps.js 861-889) | upsert は単一 Map で更新+追加を集約（#192 fix 正しい）。strict/append/upsert いずれも 889 で normalize され profile/appsData も sanitize（safeUrl で javascript:/data: 遮断） | 正しく安全 |

**結論: 実バグ無し。** 上記は過去に実バグが出た近傍を含む genuine な深掘りで、いずれも既存 fix（#154/#192/#139）+ 中央集約正規化で堅牢だった。**捏造 fix は作らない**（推奨前検証の原則）。本記録は次 AI が同 surface を再 hunt せずに済むための audit-trail（flywheel = onboarding 精度）。次の genuine vein は別 surface / メタ層 / research へ。

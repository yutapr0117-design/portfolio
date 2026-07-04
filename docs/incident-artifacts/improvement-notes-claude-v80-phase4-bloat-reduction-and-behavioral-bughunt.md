# improvement-notes-claude-v80-phase4-bloat-reduction-and-behavioral-bughunt.md

```
Run-Name      : 「終わりなき改善」phase4 後続 肥大化解消継続 + 抽出後 dead-param 掃除 + snapshot/a11y bug-hunt
PR-Range      : #555〜#566
Period        : 2026-07-04〜2026-07-05
Canonical-Ref : CLAUDE.md §7 (要点 handoff) / AI2AI.md (canon) / total-check-runbook.md §9 (Check 総数の真値)
Status        : 詳細層 (§7 の下位) — cold-start AI はまず §7 → 本ファイルの順で深掘りする
```

> **これは何か**: トークン枯渇に備えた「まともな引き継ぎ書」。CLAUDE.md §7 の 1 エントリ（要点）に対し、本ファイルは同一 run の **詳細な engineering 物語・意思決定・教訓・次の vein 候補**を残す詳細層。handoff-first discipline（CLAUDE.md §5）に従い、§7 は薄く速く、詳細は本ファイルに厚く書く。

---

## What（この run で何をしたか）

前 run（#555〜#559 で 1,000 行しきい値を確立）を受けて、**肥大化解消を「一つずつ着実に」継続**しつつ、**抽出の後始末（dead factory-param 掃除）**と **behavioral bug-hunt** を並走した run。最後にトークン枯渇に備え、cold-start 復帰用の引き継ぎ書（本ファイル + §7 エントリ）を整備した。

オーナー directive（受諾済・memory `feedback_bloat_1000_line_threshold`）: 「リポジトリの肝は全委任で生じる AI 無限改善自走そのもので、**肥大化放置がその自走への最大リスク**。1,000 行を肥大化の目安とし着実に一つずつ解消し『生じないように』進める。」

### 1. 肥大化解消の継続完遂（shipped JS 全 ≤824 行）

葉 factory パターン（`export function createX({deps}) { ... return PageFn }` — main.js が deps を注入・関数本体は無改変で移設ゆえ **byte-equivalent**）で以下を分離:

| PR | 抽出元 → 先 | 行数変化 |
|---|---|---|
| #556 | pages.js → `js/hiring-risk-page.js` (HiringRiskPage) | pages.js 642→267 / 新 leaf 411 |
| #557 | apps.js → `js/ai-page.js` (AIPage + aiLoading state) | apps.js 1,179→（#558 後）824 / 新 leaf 174 |
| #558 | apps.js → `js/pomodoro-page.js` (PomodoroPage + pomodoroTimer state) | 新 leaf 257 |

PomodoroPage 抽出では **stale-closure fix（#121/#134 の `State.get()` で live 状態を読む修正）を温存**した（deferred callback が render 毎キャプチャの旧 closure を読む再発を防ぐ）。結果、**shipped JS は全モジュール ≤824 行**になった。

### 2. Check 361 / 362 新設（BLOCKING）— 「生じないように」の機械化

- **Check 361**: `js/*.js ∪ js/quiz/*.js` が全て file-size-budget.md §4 BUDGET-DATA に登録済みであることを強制。**Check 71（registered⟹exists）の対称（exists⟹registered）** で js-leaf 面の bijection を閉じ、「新 leaf が silent に未予算化して無制限成長する」class を機械封じ。**1,000 行しきい値を convention/memory → BLOCKING Check へ昇華**した実体化。
- **Check 362**: `mutation_samples` を importlib で読み込み、各 mutation の `find` 文字列が対象 file に実在することを **verify 時に**強制。動機は「**CI は mutation-probe を走らせない**（workflow が参照していない）」ため、抽出で anchor が別 file へ移動すると orphan 化が silent になる gap。実例として #558 の PomodoroPage 抽出で pomodoro mutation の anchor が apps.js→pomodoro-page.js へ移動して orphan 化したものを systematize。

### 3. mutation_samples.py の log-rotation 分割

無限成長する append-log（1,597 行に到達）を止めた:

- `mutation_samples.py` 886 行（`MUTATIONS = MUTATIONS_ARCHIVE + _MUTATIONS_TAIL` + `E2E_MUTATIONS`・新規は tail に追記）
- `mutation_samples_archive.py` 742 行（`MUTATIONS_ARCHIVE` = 古い 120 エントリ）
- `mutation_samples_common.py` 12 行（共有 `ROOT` / `CHECK`）

規約: **新規 mutation は tail へ、~900 行超で archive へ rotate**。純データの巨大 append-log は「今の size」でなく「無限成長そのもの」を止めるのが正しい対処。

### 4. 🔴 実バグ 3 件（各 BLOCKING behavior e2e で systematize）

- **#555 AIPage stuck-state fail-safe**: `aiLoading` 解除を `finally` で保証。`generateResponse` / `State.update` が throw すると恒久的に submit 不能に stuck するのを防ぐ。
- **#561 SettingsPage snapshot 未正規化 crash**: snapshot 復元が `State.set(snap.data)` で**未正規化のまま採用**していた。`State.set(Store.validateAndNormalize(snap.data))` に修正。**#93/#295 と同じ「外部 ingestion 全経路正規化」class** — 別 schema / 欠損 snapshot で FatalPage crash していた。回帰 e2e は route `/#/settings` で foreign-schema snapshot を localStorage 注入して crash しないことを検証。
- **#563 TodoPage a11y leak**: TodoPage の root div に ErrorBoundary/FatalPage 由来の a11y 属性（`class:'error-boundary-fallback' role='alert' aria-invalid='true' aria-errormessage='fallback-details' aria-description='...unstable state transition.'`）が copy-paste で混入し、**正常なページを assistive tech に「エラー状態」と誤提示**していた。除去して `class:'flex flex-col gap-4 max-w-2xl'` のみ残す。回帰 e2e は `.error-boundary-fallback` と `[aria-errormessage="fallback-details"]` の count 0 を検証。

### 5. 抽出後 dead factory-param 掃除（#564 / #565）

leaf を分離すると、その leaf **だけ**が使っていた依存が抽出元 factory の destructure に「使われない param」として残る:

- `createApps` の `AUTHOR` / `Router` / `Theme`（AIPage/PomodoroPage 抽出で dead 化）
- `createComponents` の `Toast` / `Brand` / `Store` / `tokenize`（各ページ抽出で dead 化）

**ESLint `no-unused-vars` は destructured object param の未使用を既定で捕捉しない**ため CI を silent にすり抜ける。各 param を awk で body 使用回数を個別確認してから、destructure + docstring + main.js の呼び出し引数の **3 箇所**から除去した。components.js の docstring drift（「11 関数」→実 7）も是正。

### 6. トークン枯渇対応の引き継ぎ整備（#566 + 本ファイル）

- #566: CLAUDE.md §7 に本 run の要点エントリを追記（cold-start 一次層）。
- 本ファイル: 詳細層（handoff-first discipline）。

### 7. 抽出済ページの behavioral 再監査（本 run 末尾・drift 不在確認）

直近抽出した 4 ページ（`home-page` / `projects-page` / `project-detail-page` / `ai-knowhow-page`）を批判的に再読。**全てクリーン**:

- **State.update focus-loss(#258)**: 4 ページとも非経由。ProjectsPage 検索は gridContainer 部分再描画で focus 保持（`renderGrid()` が grid だけを clear、input は container 直下で無傷）。
- **IME/Enter-submit(#151)**: 検索は `oninput` のみで keydown handler なし → IME 対象外。
- **innerHTML**: ai-knowhow-page のヒットは表示テキスト内の文字列（「innerHTML禁止」という説明文）で実代入なし。
- **slug 衝突(#154)**: project-detail は `find(p=>p.slug===slug)` + 未存在時 NotFound ガード（`if (!project) return ...`）適切。Store 側 normalize 済。

---

## Why（なぜこの順序・判断だったか）

- **肥大化解消を最優先トラックの一つに据えた**のは、オーナー directive が「肥大化放置＝無限改善自走への最大リスク」と位置づけたため。自走そのものがリポジトリの肝ゆえ、それを脅かす肥大化は genuine improvement の最上位に来る。
- **convention でなく BLOCKING Check（361/362）で機械化**したのは、「生じないように」は doc/慣習では守れない（次の AI が知らずに未予算 leaf を足せば silent に無制限成長する）ため。§5 の increment discipline「新 invariant は BLOCKING Check になって初めて『解決』」に従った。
- **byte-equivalent 抽出**にこだわったのは、shipped JS の挙動を変えず構造だけ改善する非破壊契約（behavior e2e が保証）を守るため。
- **dead-param 掃除を独立増分にした**のは、ESLint の盲点（destructured param 未検出）で silent に残るゴミを、抽出の直後に確実に回収するため。抽出 checklist に恒久化した（memory `feedback_sed_ampersand_lint_edit`）。

---

## Change impact

- 本 run の事実記録ゆえ原則 **append-only**（point-in-time 履歴・遡及改変しない）。
- 新規 incident-artifact ゆえ **README.md inventory（Check 75）** と **本 mirror（Check 108）** が必要（追加済）。
- shipped JS / AIO published layer / binary asset は byte-identical を維持（抽出は byte-equivalent、docs は AIO 層外）。

---

## Constraints

- **Check 75**: docs/incident-artifacts/README.md に列挙必須。
- **Check 108**: docs/files mirror bijection（`docs/files/docs/incident-artifacts/<name>.md.md` がその mirror）。
- **Check 361/362**: 本 run で新設した js-leaf 予算 bijection + mutation anchor 整合。
- 歴史層ゆえ **Check 109**（prose の Check 総数 hardcode 禁止）対象外（point-in-time 記録・§9 が単一権威）。

---

## Audience-specific notes

### For AI agents（cold-start の後続 AI）

- 役割タグ: `incident-artifact`, `run-narrative`, `bloat-reduction`, `behavioral-bughunt`, `session-handoff`
- **次の genuine vein 候補（reflect-then-organize 済・未着手）**:
  1. **router / store の edge-case 監査**（本 run は抽出済ページ 4 面をクリーン確認したが router・store の深い edge-case は未 hunt）
  2. **別の vacuous-gate 掘り**（「名乗るだけで RED にならない gate」の class・§7 に反復して現れる vein）
  3. shipped JS 肥大化は完遂（全 ≤824・Check 361/362 で再発機械封じ）。**残存 >1,000 行は全て defer-with-reason**: check.py（#253 net-negative）/ e2e spec 3,332（9-check が名前で結合ゆえ単純分割は vacuous 化）/ style.css・index.html・main.js（設計制約）。衝動的に着手しない。
- **プロセス規律（本 run で実際に踏んだ地雷）**:
  - #558 マージ後に `git checkout -b` を忘れ mutation split を **main 直 push した slip**（非破壊・CI 緑だが PR gate 迂回）。→ memory `feedback_merge_before_new_branch`: 「merge 後 HEAD=main、次増分の**最初の編集前**に必ず branch を切る」。
  - **抽出後は必ず抽出元 factory の dead param を awk で確認**（ESLint は destructured param を見ない）。正規表現一括検出器は multiline signature で false positive を出すので awk で個別確認。
  - **外部 ingestion（load / import / cross-tab / snapshot-restore）は一つ残らず同じ `Store.validateAndNormalize` を通す**（#93/#295/#561 が同一 class）。
  - **a11y/role 属性の copy-paste leak** は正常 UI を「エラー」と誤提示する。抽出時に root 属性を精査。

### For human engineers（新卒レベル）

- 「肥大化解消」= 大きくなりすぎたファイルを、挙動を一切変えずに（byte-equivalent）小さなモジュールへ分割すること。ここでは「factory pattern」= 依存を引数で受け取る関数として切り出し、元の場所からその依存を注入する形にした。
- 「なぜ Check にするのか」= 人間（や次の AI）が忘れても機械が自動で止めるため。ルールを文書に書くだけでは、知らない人がすり抜ける。

### For third parties / auditors

- AI-only 自走運用で、肥大化解消（構造改善）と実バグ修正（品質改善）を並走させた透明な記録。実バグ 3 件はいずれも回帰 e2e（BLOCKING）で再発を機械封じしており、修正が「言うだけ」でないことを検証可能。
- プロセス slip（main 直 push）も honest に記録し memory で再発防止した — 統治が「隠さず是正する」ループで回っている証拠。

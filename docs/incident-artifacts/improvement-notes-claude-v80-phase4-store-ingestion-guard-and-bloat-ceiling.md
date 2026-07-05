# improvement-notes-claude-v80-phase4-store-ingestion-guard-and-bloat-ceiling.md

```
Run-Name      : 「終わりなき改善」phase4 後続 store ingestion-guard + 肥大化 解消/防止セット run
PR-Range      : #568〜#570 (+ 本 handoff PR)
Period        : 2026-07-05
Canonical-Ref : CLAUDE.md §7 (要点 handoff) / AI2AI.md (canon) / total-check-runbook.md §9 (Check 総数の真値)
Status        : 詳細層 (§7 の下位) — cold-start AI はまず §7 → 本ファイルの順で深掘りする
```

> **これは何か**: トークン枯渇に備えた「まともな引き継ぎ書」。CLAUDE.md §7 の 1 エントリ（要点）に対し、本ファイルは同一 run の **詳細な engineering 物語・意思決定・教訓・次の vein 候補**を残す詳細層。

---

## What（この run で何をしたか）

router/store edge-case 監査（前 run が名指しした未 hunt vein）から入り、store.js に実クラッシュ 1 件を発見・修正。続いてオーナー再提案（受諾）「肥大化解消と肥大化防止をセットで」を受け、**防止**（BLOCKING 1,000 行上限 Check）と**解消**（最大 page 抽出）をセットで実施した。

### 1. 🔴 store.js normalizeAppsData の非配列 history ingestion crash 修正（#568）

`normalizeAppsData` は「どんな入力でも throw しない総関数」契約を持つ（`tasks`/`todos` は既に `Array.isArray` ガード済）。だが **`ai.history` / `pomodoro.history` だけ truthy 判定のみ**で outlier だった:

- **🔴 `ai.history` が非配列**（文字列/数値/オブジェクト）→ `.filter` が `TypeError: ... is not a function` を throw → `validateAndNormalize` が例外 → **load()(state.js init) / cross-tab(state.js:210) / import / snapshot-restore / settings 正規化ボタンの全 ingestion 経路が FatalPage crash**。`state.js:209` は schemaVersion 一致だけ見て `validateAndNormalize` を呼ぶため、current schema(12) だが `ai.history` が破損した store で確実に再現する。#93/#295/#561 と同一の「外部 ingestion は全経路正規化を通せ」class の未閉じ枝。
- **`pomodoro.history` が非配列** → `String.prototype.slice` が発火し「配列のはずが文字列」に型崩れ。PomodoroPage は history を描画しない（complete() 時に `history.push` するのみ）ため初期描画では crash しないが、timer 完了時の `.push`/`.slice` で throw する rare path の防御。

**fix**: 両者を `Array.isArray` ガードへ。非配列は default（空配列）にフォールバック。valid な配列は挙動不変ゆえ非破壊。

**検証**: 新 BLOCKING e2e `normalizeAppsData tolerates a non-array ai/pomodoro history`（破損 store を addInitScript で seed → load() を通し crash しない + #ai-input / pomodoro timer 描画）。fix を戻すと load() が init で throw し app が boot せず RED = 非 vacuous を実測。mutation_samples E2E_MUTATIONS に ai.history ガード喪失 mutation を追加。**honest finding: pomodoro-only 退行は本 e2e で観測不能（history 非描画 + 完了 path 未到達）ゆえ mutation sample は追加せず** — 捕捉できない mutation を登録しない規律。pomodoro ガードは defensive 型契約補完として温存。

### 2. 肥大化「防止」= Check 363 新設（BLOCKING・#569）

owner 再提案「解消と防止をセットで」を受諾。**防止側の gap = 1,000 行しきい値を BLOCKING で止める床が無い**だった:

- **Check 52**（BUDGET-DATA）は per-file の loose ADVISORY 予算 → 超過しても warning のみ（CI を止めない）。これは「価値ある bloat（新しい安全コメント/証跡）」を誤ブロックしない**意図的設計**。
- **Check 361** は exists⟹registered（登録漏れ防止）のみで行数上限は強制しない。

→ どの `js/*.js` ロジック leaf も owner のしきい値を silent に越えられた。**Check 363** = `file-size-budget.md` に `<!-- JS-LEAF-CEILING 1000 -->` marker（単一ソース）を追加し、`js/*.js`（非再帰）ロジック leaf の行数がそれを越えると **BLOCKING で CI 失敗**。Check 60 と同型の二層設計（advisory 早期警告層 [Check 52] + BLOCKING ハードゲート層 [Check 363]）。**除外**: `js/quiz/*.js`（純データ・設問追加は価値ある成長）と main.js（保護 kernel・js/ 直下でない）。

**検証**: 現行 tree は全 js/*.js ≤837 ゆえ PASS（非破壊）。js/storage.js を 1,075 行にパディング → BLOCKING ERROR で RED、復元で OK を実測。self-integrity Check 45a/b/c・70・105 全 OK（総数 363）。

### 3. 肥大化「解消」= SettingsPage 抽出（#570）

apps.js は AIPage/PomodoroPage 分離後も 837 行あり、**SettingsPage が最大の page（~373 行）で肥大の主因**だった。Check 363 への headroom を確保するため `js/settings-page.js` へ byte-equivalent 分離:

- `createSettingsPage({ h, Toast, State, Brand, Store, Storage, CONSTANTS, generateId, slugify }) → { SettingsPage }`。本体 + `settings*` private state（let × 7）を無改変移設。
- **apps.js 837→458 行**・新 leaf 408 行。全 shipped JS ロジック leaf が上限に十分な headroom。
- **抽出後 dead factory-param 掃除**（#564/#565 の awk 確認法）: `createApps` の Brand/Store/Storage/slugify が dead 化 → destructure + docstring + main.js 呼び出しの 3 箇所から除去。

**抽出に伴う Check/mutation 追従**（各 Check が drift を捕捉→是正した実例）:
- **Check 140**: Demo セレクタの探索先を apps.js → settings-page.js へ追従（SettingsPage 移動）。
- **Check 362**: snapshot-restore + Check140-demo-option の **2 つの mutation anchor** file を settings-page.js へ追従（#558 class・anchor orphan を verify 時に検知）。
- **Check 119**: settings-page.js docstring に【依存（引数で注入）】節を追記（署名 dep 網羅）。
- Check 361/363/108（BUDGET-DATA 登録 / ceiling / mirror doc）。package.json lint/lint:js に Edit で追加（sed 不使用 #549）。

**検証**: Settings 関連 e2e 20 件 + route/apps 35 件 全 pass。verify exit 0。

---

## Why（なぜこの順序・判断だったか）

- **store.js を最初に監査した**のは、前 run の improvement-notes が「router/store の深い edge-case は未 hunt」と名指ししていたため。実際に非配列 ingestion crash という genuine バグが 1 件出た（vein は枯れていなかった＝availability heuristic の誤謬の再確認）。
- **防止（Check 363）を解消（#570）より先にした**のは、防止機構が無いまま解消しても「また肥大化する」から。owner の「生じないように」は防止が本体。ただし防止だけでは「set」でないため、直後に解消（SettingsPage 抽出）を対で実施した。
- **Check 363 を Check 52 と別 Check にした**のは、Check 52 の ADVISORY 設計（価値ある bloat を誤ブロックしない）を壊さないため。ロジック leaf のハード上限は別レイヤーとして足すのが正しい（二層設計）。

---

## Change impact

- 本 run の事実記録ゆえ原則 **append-only**。
- 新規 incident-artifact ゆえ **README.md inventory（Check 75）** と **本 mirror（Check 108）** が必要。
- shipped JS は byte-behavior-equivalent（#568 は非配列入力のみ挙動変更＝crash→安全フォールバック / #570 は抽出で本体無改変）。AIO published layer / binary は不変。

---

## Audience-specific notes

### For AI agents（cold-start の後続 AI）

- 役割タグ: `incident-artifact`, `run-narrative`, `ingestion-guard`, `bloat-reduction`, `bloat-prevention`, `session-handoff`
- **肥大化トラックの現状**: 解消側は全 shipped JS ロジック leaf が ≤458（apps.js）で完遂状態。防止側は Check 363（BLOCKING 1,000 行上限）で機械封じ済。**新 leaf も 1,000 行を超えれば CI が止まる**。しきい値変更は JS-LEAF-CEILING marker を owner 裁可で。
- **次の genuine vein 候補（reflect-then-organize 済・未着手）**:
  1. **別の vacuous-gate / wiring 掘り**（「名乗るだけで RED にならない gate」「file 存在≠file 配線」の class・§7 に反復して現れる vein）。
  2. **router の深い edge-case**（本 run は store.js を hunt したが router は軽読のみ。query param / project-detail slug decode / transition-lock replay の edge）。
  3. TaskPage/TodoPage/NotesPage の behavioral 再監査（本 run 末尾で TaskPage を軽読し robust 確認したが full hunt は未）。
- **プロセス教訓（本 run で実際に踏んだ/回避した地雷）**:
  - **mutation-probe-e2e は full suite を回すため 2 分でタイムアウトしうる**。タイムアウト（SIGTERM）は **ファイルを mutated のまま残す**（本 run で apps.js に snapshot mutation が残留・`git checkout` で復旧）。mutation-probe は単独実行し完全終了を待つ（memory `feedback_mutation_probe_verify_race`）。個別 mutation の非 vacuous 証明は手動 revert→targeted test で代替可。
  - **抽出後は必ず抽出元 factory の dead param を awk で確認**（ESLint は destructured param を見ない・#564/#565）。
  - **抽出は Check 群が drift を全部捕捉してくれる**（119/140/362/108/361/363）。verify を回して RED を潰せば漏れなく追従できる＝Check が「抽出の後始末チェックリスト」を機械化している。
  - **外部 ingestion（load/import/cross-tab/snapshot-restore）は一つ残らず同じ `Store.validateAndNormalize` を通し、その normalize 内の各コレクション枝は `Array.isArray` でガードせよ**（#93/#295/#561/#568 が同一 class）。

### For human engineers（新卒レベル）

- 「肥大化解消と防止をセット」= 大きくなったファイルを小さく分ける（解消）だけでなく、「二度と 1,000 行を超えさせない機械のルール」（防止＝Check 363）も同時に置くこと。ルールを機械（CI）に守らせるので、次の人が知らなくても自動で止まる。
- 「総関数」= どんな入力を渡しても例外を投げず必ず値を返す関数。ユーザーデータの正規化はこれであるべきで、一箇所でも型チェックを忘れると壊れたデータでアプリが落ちる（#568 がその実例）。

### For third parties / auditors

- AI-only 自走運用で、実バグ修正（#568）・肥大化防止の機械化（#569）・肥大化解消（#570）を透明に並走させた記録。実バグは BLOCKING e2e、防止は BLOCKING Check、解消は byte-behavior-equivalent（55 e2e pass）で各々検証可能。オーナー提案の受諾から実装完遂までが 1 セッション内で追える。

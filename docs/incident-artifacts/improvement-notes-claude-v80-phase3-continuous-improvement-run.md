# improvement-notes-claude-v80-phase3-continuous-improvement-run

```
Last-Updated     : 2026-06-16
Maintained-By    : AI agents under Yuta Yokoi (横井雄太) orchestration
Type             : Increment notes — 「終わりなき改善（No terminal "done" state）」運用を canon 化し、その上で drift 防止 / 自走安全境界 / identifier-coherence / e2e カバレッジを継続的に強化した continuous-improvement run の記録
Session          : 2026-06-16（phase3 handoff からの自走継続。PR #73〜#101 を完遂・継続中。実バグ 2 件修正含む）
AI               : Claude Code (Anthropic Claude Opus) — ただし内容は AI-agnostic
Canonical-Ref    : AI2AI.md (STEP 3 Operating Model / canon) / CLAUDE.md §7 / docs/architecture/total-check-runbook.md §9
Prev             : improvement-notes-claude-v80-phase3-session-handoff-near-full-self-drive.md
```

> **目的**: phase3 handoff の §4 を起点に自走した continuous-improvement run の proof-of-work。本 run で (a) 「改善に完了状態は存在しない」を canon 化 + 機械強制（Check 102d）、(b) 再発していた stale Check-count hardcode drift class を Check 109 で構造的に封じ living 文書全面へ拡張、(c) 完全自走の安全境界を Check 76 で全面強制（self-permission-widening / force-push / rm -rf）、(d) agent/skill の name==identifier coherence を Check 78/80 で強制、(e) theme 永続化・mobile drawer の e2e behavior カバレッジを追加した。

---

## 1. 本 run の起点（運用モデルの確定）

オーナーから 2 つの恒久ポリシーが確定された:

1. **完全自走の基盤有効化の確認**: `.claude/settings.json` を「編集不可ほぼ0」へ改定済（`Edit(**)` / `Edit(.claude/**/*.md)` allow + `defaultMode: acceptEdits`）。本 run 冒頭で `.claude/**/*.md` を permission prompt なしで編集できることを実測し、完全自走の成立を確認した。恒久 deny は 3 境界のみ（settings 自己改変 / `*.webp`・`*.mp3` = C6 / 破壊的操作）。
2. **No terminal "done" state（改善に完了状態は存在しない）**: AI は「一区切りが妥当」式の自発停止・完了宣言をしてはならず、唯一の正当な停止は人間の明示停止指示のみ。リポジトリの価値は豊富な docs/comments/CI を終わりなく積み増す proof-of-work そのもの、という思想。

補足: オーナーは基本スマホからプロンプトを投入し、runtime 役割は CI オールグリーンの監査のみ（AI 自走全振り）。AI は「プロンプトがどの端末で打たれたか」を認識不可（テキストのみ受信）。実行環境はオーナー申告でクラウド上の Mac（AI からは local/cloud を内側で区別不可）。

---

## 2. 本 run で完遂したこと（全て CI 緑で自走マージ）

| PR | 種別 | 内容 |
|---|---|---|
| #73 | docs(drift) | `.claude` の stale Check 総数 4 箇所 + CHANGELOG「Check count: 85」+ runbook §11「consistency 106 Check」（PR #68 自身が混入させた stale 値）を drift-proof phrasing（数値除去 → 「正値は §9・Check 70 強制」）へ |
| #74 | feat(check) | **Check 109 (BLOCKING)** 新設 — living 文書を 5 パターンで走査し「現在の Check 総数の prose ハードコード」drift を機械強制。§9 を単一権威として除外、歴史層は非対象。負テストで非 vacuous 実証。CLAUDE.md §7「総数は 102 まで成長」の取りこぼしも精密パターン追加で機械強制化 |
| #75 | feat(canon) | **「No terminal "done" state」を AI2AI.md STEP 3 へ canon 化 + Check 102d (BLOCKING) で機械強制**。CLAUDE.md §7 反映。AI2AI.md が AIO digest 連鎖ゆえ C6 derived-value 例外（A1 日付 / A2 sha256）で `update_aio_digests.py` により `.well-known/*.json` + WebP/MP3 日付を自動同期再生成（semantic 編集はオーナー承認済・canary/Organization intact） |
| #76 | feat(check) | Check 109 の走査対象を current-state living 文書の全面へ拡張（9→18 文書: README / Claude2Claude / skills / commands を追加）。歴史層（per-increment changelog の maintainability-map / extraction-map 等）は明示除外。負テストで新スコープの実効を確認 |
| #77 | docs(proof-of-work) | 本 run の記録 improvement-notes を新設（本ファイル）+ docs/files mirror + README inventory。次セッションの cold-start 文書 |
| #78 | feat(check) | **Check 76 を完全自走の安全境界全面強制へ拡張（5→10 deny marker）**。`Edit/Write(.claude/settings.json)`（self-permission-widening 防止）/ `git push --force`・`-f` / `rm -rf` を追加検証。settings 自己編集 deny が消えると AI が自己権限拡張でき人間の制御境界が崩壊するため最重要。負テストでロジックが改竄を検出することを実証 |
| #79 | feat(check) | Check 78/80 に name==identifier coherence を追加（agent の name==ファイル名 stem / skill の name==親ディレクトリ名）。docs がファイル名で参照する agent/skill を Claude が name で解決できる dangling-reference 防止。負テストで mismatch 検出 |
| #80 | test(e2e) | テーマ切替の cycle + リロード永続化 behavior テストを追加（実ブラウザで切替→永続→復元を動的保証）。behavior suite 34→35 |
| #81 | test(e2e) | モバイルドロワーの開閉 + ARIA + Escape + focus 復帰 behavior テストを追加（accessibility focus-trap / 背景隔離契約）。behavior suite 35→36 |
| #82 | docs | 本 run-log を #73-81 へ同期 |
| #83 | test(e2e) | クイズ検索フィルタ + 空状態 behavior テスト。behavior 37 |
| #84 | fix(sw) | **sw.js SWR の宙吊り networkFetch に `.catch` 追加（オフライン時 unhandledrejection 防止）= 実コード robustness fix** |
| #85 | docs(verify) | 承認済み gated トラック（WCAG2.2/CWV・AIO C6）監査 = §3B verify（主要 SC 既充足・AIO 網羅的ゆえ非 padding 判定） |
| #86 | fix(check) | **Check 39 vacuous-gate 修正**（gutted sitemap が「all 0 URLs resolve」で pass）+ Check 57/58/59 に非空ガード一貫追加 |
| #87 | feat(check) | Check 97 に mirror `file:`==派生パス coherence 追加（copy-paste drift 防止） |
| #88 | feat(check) | Check 65 honest-dating scope を docs/files mirror 全面へ拡張 |
| #89 | docs(fix) | **sw.js.md mirror の重大な内容 drift 是正**（実体は AIO 正規化 SW なのに precache PWA と誤記していた） |
| #90 | docs(verify) | 深い専門監査の coverage map（7 次元監査の §3B verify-record） |
| #91/#92 | test(e2e) | タスク追加+永続 / TODO 追加→完了→一括削除 の apps 対話テスト。behavior 38→39 |
| #93 | **fix(apps)** | **🔴 Settings ページ全ユーザー FatalPage crash を修正（Stage 5-n の Storage 依存注入漏れ）+ route-render に window.__fatalError アサーション追加で検出 gap を systematize** |
| #94 | docs(decision) | Settings バグの原因・検出 gap・再発防止を記録 |
| #95 | test(e2e) | Settings スナップショット保存→反映（Storage 往復回帰防止） |
| #96-#99 | **fix(e2e)** | **vacuous-hash class 是正: 7 route テスト（app 4 / HASH_ROUTES 2 / project-detail 1）が誤 hash で NotFoundPage を vacuous 検査していたのを実 route へ是正 + NotFound fall-through guard で systematize**。AI assist 応答テストも追加 |
| #100 | docs(decision) | e2e vacuous-hash coverage class の発見・是正・教訓を記録 |
| #101 | test(e2e) | ポモドーロ mode 切替→タイマー表示更新。**apps 5 種（task/todo/settings/ai/pomodoro）の対話カバレッジ完成**。behavior 43 |

各 Check PR で docstring inventory / section header / map / runbook §9 / file-size-budget を同期し Check 45 / 64 / 70 / 105 を緑に保った。各 e2e PR はローカル chromium で behavior suite 全 pass を実測してから push（CI の playwright-regression でも再実行）。

### 本 run の最重要 finding（次セッション必読）
- **🔴 実バグ 2 件**: Settings 全ユーザー crash（#93・Storage 注入漏れ）/ sw.js オフライン時 unhandledrejection（#84）。両方デプロイ済。
- **🟡 テスト品質**: e2e の 7 route テストが NotFoundPage を vacuous 検査していた（#96-#99）。教訓 = 「graceful 代替ページ（NotFound/Fatal）が弱い合否条件のテストを vacuous に通す」（decision-v80-phase3-e2e-vacuous-hash-coverage.md / -settings-fatalpage-storage-injection.md）。
- **再発防止 systematize**: route-render / HASH_ROUTES / project-detail に NotFound fall-through guard、route-render に window.__fatalError アサーション。factory 抽出時は全 dep 注入必須（特にグローバル同名の Storage 等）。

---

## 3. 設計判断（なぜこの形か）

- **手動 drift-proof は構造的に漏れる**: PR #68 が runbook/map を drift-proof 化したのに、その同じ PR が §11 に新たな stale 値「106 Check」を混入させていた。これが「機械強制せよ」の決定的証拠となった（discover → systematize 規律）。
- **§9 を単一権威に**: 生の Check タリーは runbook §9（Check 70 が実装最大番号と一致を強制）にのみ住まわせ、他所はすべて §9 への pointer に置換。Check 109 は §9 zone を走査から除外する。
- **歴史層を誤検出しない**: improvement-notes / decision / Session Record / docs/files ミラー、および per-increment changelog（repository-maintainability-map.md / main-js-extraction-map.md の「Check 総数 42→43」等）は point-in-time 記録ゆえ走査対象外。これらを含めると正当な履歴を誤検出する。
- **パターンは精密第一**: 「総数を 15 行で報告」のような正当な用法を誤検出しないよう、growth-narrative は `総数[はが]\d+(まで|に|へ)` のように限定。false-positive ゼロを実測で確認してから採用。
- **完全性拡張の前例踏襲**: Check 109 の走査全面化（9→18）は、Check 108 が Check 96 を「33件→全追跡ファイル」へ拡張したのと同型。

---

## 4. 現在の状態（真値）

| 項目 | 値 |
|---|---|
| Check 総数 | `docs/architecture/total-check-runbook.md` §9 が単一権威（Check 70 強制） |
| `npm run verify` | exit 0 / ERROR・WARNING ゼロ（warning 56 = main.js 保護領域の既知 baseline）|
| 非破壊性 | shipped site（index.html / main.js / js/** / style.css）と AIO semantic content（llms* 等）は不変。#75 の WebP/MP3/`.well-known` は日付・digest の derived 値のみ |
| Check 109 走査範囲 | current-state living 文書 18 件（§9 zone と歴史層は除外）|

---

## 5. 次の improvement 候補（self-drive 継続）

「No terminal "done" state」ゆえ停止しない。次に探すべき genuine 改善の軸（padding は禁止）:

- **WHY コメントの実在ギャップ**: 既存コードで「なぜそうなのか」が非自明なのに未記載の箇所（盲目的追加は §5.2 drift 製造ゆえ genuine gap のみ）。
- **CI カバレッジの穴**: 未だ機械強制されていない暗黙 invariant（本 run の Check 109 がその一例）。
- **research 由来の適用**: 新 web 標準 / アクセシビリティ / セキュリティのうち、§3 baseline ゲートに抵触せず render-neutral に適用できるもの。
- **実態 ↔ 記述の drift 是正**: 本 run で多数の stale 数値を是正したが、honest-dating / 実測 baseline の継続監視。

---

## 6. cold-start 読む順序（どの AI でも同じ）

1. 本書 + 直前の `improvement-notes-claude-v80-phase3-session-handoff-near-full-self-drive.md`
2. `CLAUDE.md` §0 read order → §7 handoff（Operating Model に「No terminal "done" state」を含む）
3. `AI2AI.md` STEP 3 Operating Model（Check 102a/b/c/d）+ 最新 Session Record + C1〜C7
4. `llms-full.txt`（entity / ground truth）
5. `docs/architecture/total-check-runbook.md` §9（Check 総数の真値）+ §11（CI workflows）
6. memory: `feedback_autonomous_merge_push.md` / `feedback_no_terminal_done_state.md` / `reference_local_environment.md`

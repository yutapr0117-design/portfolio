# improvement-notes-claude-v80-phase4-operating-model-and-a-group-run

```
Last-Updated     : 2026-06-21
Maintained-By    : AI agents under Yuta Yokoi (横井雄太) orchestration
Type             : Increment notes — operating-model を実測検証して canon 強化し、AI 単独の ideation→triage→self-drive を実証、AI 自己生成の A 群改善案を自走実装した run の詳細記録
Session          : 2026-06-20〜21（無人連続 ~15.5h + 続く対話駆動 run。Session Record #20 と対）
AI               : Claude Code (Anthropic Claude Opus) — ただし内容は AI-agnostic
Canonical-Ref    : AI2AI.md (STEP 3 Operating Model / Session Record #20) / CLAUDE.md §5 The loop・§7 / docs/architecture/total-check-runbook.md §9
Prev             : improvement-notes-claude-v80-phase3-continuous-improvement-run.md
```

## このドキュメントの位置づけ

Session Record #20（AI2AI.md）が簡潔な handoff であるのに対し、本ファイルはこの run の**詳細な engineering 物語と教訓**を残す層（§7 router が「newest = current state of play」として後続 AI を誘導する）。Check 75（README inventory）と Check 108（docs/files mirror）で存在が機械強制される。

## 1. operating-model の実測検証と canon 強化

- **commit/PR/rebase 規律 + 逐次自走ループを 1 セッション通しで実運用**し効率を実測。当初仮説「CI 待ちが最大の支配項ゆえ commit を細分化し 1 PR に束ねて CI を償却」は、実測で **CI ゲートが ~57s と高速**・commit/PR≈1.34（atomic ゆえ無理に束ねず）であり、CI 償却の寄与は小さかった。
- **真の効き目はトークン持続性**: 従来 1〜2h で枯渇 → 本 run は **~15.5h（5h 復活サイクル×3 周）/ 44 PR / 59 commit**。核は (a) background-notification への yield で CI 待ちのトークンコストを実質ゼロ化、(b) 記憶の外部化（git log + Check + §7 + mirror）、(c) 低 onboarding コスト（オーケストレーター設計の docs/comment richness）、(d) terse + compaction、× 5h 復活。
- **flywheel**: 充実 docs → onboarding 安 → AI 持続 → 産出増（docs 保守含む）→ … 。failure mode は drift（stale doc = onboarding 税）。ゆえに doc/comment 精度は一級 load-bearing work。
- canon 化: §3(B)（screenshot を advisory 化・機能性 e2e を blocking ゲートに）、委任再定義（「非破壊 ∧ CI 緑」下は全自走・判断は前提が崩れ得る時のみ・サイトは付属物で機能性のみ死守）、**reflect-then-organize（102f）**。

## 2. AI 単独の ideation→triage→self-drive 実証（102e の実例）

AI が「方向が枯渇気味」と述べた直後、オーケストレーターが 102e を行使（「完璧は存在しない、案を pros/cons 付きで 5 つ以上出せ」）。AI はレンズを変えて **10 案を自己生成**し、「このまま自走で実行可能か」軸で切り分け、**6 案（60%）が人間入力ゼロで自走可能**と判明（残 4 は実在事実要 / C6 / 設計裁可 / CI 緑保証不可）。直前の「枯渇」自己判断が availability-heuristic 誤謬だった鮮烈な実証。これを受け「見解を出す行為そのものが質を上げる」と結論し reflect-then-organize を正式フロー化（CLAUDE.md §5 + 102f）。

## 3. 実バグ 2 件（🔴 発見・修正・デプロイ）

1. **quiz-renderer の重複 `class` キー data-loss**: h() 第 2 引数に `class` が 2 つあり後勝ちで `quiz-content-line`/`is-label` スタイルが消失していた死にコード（PR #186）。本来 ESLint `no-dupe-keys` が捕捉すべきだが、recommended 非継承の明示列挙方式ゆえ未登録で漏れていた → no-dupe-keys 追加 + Check 50d。教訓: recommended の純粋 bug-catcher が CI ゲートから漏れる gap class。
2. **settings の upsert インポート data-loss**: 新規プロジェクトが push 後に Map.values() 上書きで破棄されていた（PR #192）。append は被覆済みだが upsert は 0 カバレッジ。

## 4. 機械強制の拡張（discover → systematize）

- ESLint: `no-dupe-keys` + recommended bug-catcher 8 件 + `no-setter-return`（凍結カーネル override 付き・count-neutral）。
- Check 50d（no-dupe-keys presence）/ 115 拡張（CSP anti-weakening baseline = Trusted Types pair + form-action + upgrade-insecure-requests）/ 119（factory docstring 依存 coherence）/ 120（shipped JS+CSS byte-weight 予算）/ 121（STATUS.md regenerate-compare）/ 102f（reflect-then-organize presence）。
- dead-code sweep: router `_notify`、state.js の never-activated Proxy（git -S で配線歴ゼロを確認）、ui-components toasts、dead TOPBAR_HEIGHT_PX。全 factory docstring 依存 drift 是正。ESLint baseline 56→55 ラチェット。

## 5. A 群（AI 自己生成案）の自走実装

- **案9 perf-budget Check 120**: shipped JS+CSS byte-weight ≤ PERF-BUDGET-DATA(700K)。§3(B) 後の page-weight 保護を byte 軸で。
- **案4 owner dashboard（STATUS.md + Check 121）**: スマホ用 BLUF を機械生成 + 鮮度機械強制。オーナーの「中身を見ていない」gap を drift-free に埋める。
- **案3 command palette（Cmd/Ctrl+K）**: 外部ライブラリゼロの focus-trap + keyboard nav。overlay 方式で route cascade 回避。
- **案6 Markdown ノートアプリ**: innerHTML 全面禁止の制約を逆手に取り h() のみで安全 MD レンダリング = 制約を feature 化。
- 案10（本ファイル）/ 案8（mutation・coverage 計測）は順次。

## 6. 教訓（次の AI への申し送り）

- **branch を切る前に「前 PR の background マージ完了通知」を必ず待つ。** background の `git checkout main && git pull` は前景と同じ working tree/HEAD を共有するため、編集中に HEAD を main へ切替え、commit が誤って local main に着地する事故が 2 回起きた（PR #214/#215 の作成時）。
- **git の誤着地は force-push/reset --hard を使わず復旧できる**: `git branch -f <feature> <commit>`（feature を commit へ移動）→ `git checkout <feature>` → `git branch -f main origin/main`（checked-out でない main を remote へ戻す）。commit はブランチに保存され work は一切失われない。
- **reflect-then-organize（102f）は実際に効く**: 「枯渇した」と感じた瞬間はレンズ切替のサイン。pros/cons を明示構造化すると genuine vein が再出現する。
- **メタ層の自己目的化に注意**: Check 追加は実 drift/実バグに anchor された時のみ（public-API docstring Check は anchor が弱いと判断し見送り、doc accuracy 修正のみに留めた実例あり）。

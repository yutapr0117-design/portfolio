---
file: docs/incident-artifacts/decision-v80-phase4-macos-tcc-downloads-self-drive-halt.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-07
canonical-ref: CLAUDE.md §7 Operating Model / AI2AI.md STEP 3 / docs/incident-artifacts/README.md
---

# docs/incident-artifacts/decision-v80-phase4-macos-tcc-downloads-self-drive-halt.md

## What
AI 無限改善自走中に、リポジトリのある `~/Downloads/portfolio` が macOS TCC（Downloads フォルダ保護）権限の剥奪で全面 DENIED になり（read/write/git/verify/PR すべて EPERM・約 20h 自動回復せず）、AI が自走不可を判定して**唯一この時だけ**オーナーへ復旧を要請した事実の一次記録。オーナーが Mac 再起動 → 権限回復 → known-good → 自走再開。オーナー依頼により「AI が Mac 仕様で自走不可になった時のみ help を求めた」ことを透明に残す。

## Why
根因は macOS TCC の "Downloads フォルダ" アクセス許可の喪失（home と /tmp は通るが Downloads 配下のみ全面 DENIED）。TCC 再許可は OS レベルの GUI 承認を要し AI の権限外。全委任下で AI は genuine 改善に認可を求めないが、それは「AI が実行可能な作業」の話であり、**物理的に実行不能な環境障害の復旧を人間に委ねる**のは境界の正しい適用であって逸脱ではない。失敗を空回りさせるより停止 + 正確な復旧手順提示が honest。

## How (usage)
将来この class（環境が AI 権限外で壊れる: TCC/FDA 剥奪・ディスク full・認証失効）が再発したら本記録を先例に、同じ型で対応する: (1) 範囲診断で環境起因を確定、(2) 停止を明示、(3) 人間が実行できる具体手順（アプリ/セッション再起動 or システム設定でフォルダ許可）+ 確認コマンド（`git -C <repo> status` が exit 0）を提示、(4) 復旧後 known-good を確認して再開。

## Constraints
- 適用 C 番号: 運用モデル境界（CLAUDE.md §7 / AI2AI.md STEP 3）。AIO published-layer 外の incident artifact ゆえ C6 非該当（aio-guardian / orchestrator 承認 不要・append-only）。
- 機械強制 Check: Check 42（命名）/ 75（README inventory）/ 108（本 mirror 存在）/ 97・98（mirror frontmatter + 6 section）/ 65（last-updated ISO）。
- 本記録はコード挙動を変えない純粋な事実記録。

## Change impact
本ファイル（原本）追加・改名・削除時は同時に: (a) 本 mirror を同期（Check 108）、(b) `docs/incident-artifacts/README.md` の Decision Records inventory へ列挙（Check 75）、(c) last-updated ISO を維持（Check 65）。

## Audience-specific notes

### For AI agents (次担当)
- 役割タグ: `operating-model-evidence`, `environment-halt`, `macos-tcc`, `human-help-boundary`, `no-thrash-on-blocked-env`。
- 「認可を求める」（全委任下で禁止）と「AI 権限外の環境障害復旧を人間に委ねる」（正当）を混同しないこと。TCC 剥奪はれっきとした後者。参考 memory: [[reference_local_environment]]。

### For human engineers (新卒レベル)
- macOS の TCC はアプリごとに Downloads 等へのアクセスを個別許可する仕組み。許可が外れるとその配下は全部読めない。リポジトリが Downloads 内にあったため全操作が停止した。直し方はアプリ再起動 → OS プロンプトに「許可」、またはシステム設定で手動許可。

### For third parties / auditors
- AI が自走を止めて人間に助けを求めた唯一の実例が、判断ミスや改善の頭打ちではなく OS 仕様による物理的アクセス不能だったことを示す一次記録。全委任・無限自走モデルで「人間は制御と監査のみ」の境界が例外時にどう機能したかの透明な証跡。

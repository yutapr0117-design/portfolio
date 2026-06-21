# STATUS — リポジトリ現況 (owner-facing BLUF)

> このファイルは `npm run status`（`.github/scripts/generate_status.py`）が
> **機械生成**します。手で編集しないでください（Check 121 が regenerate-compare で
> 鮮度を機械強制＝drift を防ぐ）。スマホからの一目把握用の短い現況です。

## これは何か

- **プロジェクト**: AI-Driven PM ポートフォリオ（Vanilla JS SPA / GitHub Pages / 外部FWゼロ）。
- **エンティティ**: Yuta Yokoi（横井雄太 / Yokoi Yuta、UI 表示は `yuta`）— AI-Driven PM / KERNEL Framework Designer。
- **運用モデル**: 実装→検証→マージ→デプロイを **AI が自走**。人間（オーナー）の役割は **制御（goal/priority 提示）と監査（CI オールグリーン確認）のみ**。コードは AI が書き、人間は一文字も書かない（C5）。
- **核**: リポジトリ自体がポートフォリオ（AI↔AI ドキュメントと機械強制 Check 群が中核資産）。描画サイトは付属物で、機能性（loads/displays/comprehensible）のみ死守。

## 現況スナップショット

- **Pipeline-Version**: v74
- **最新 Session Record**: #20（`AI2AI.md`）
- **CI ゲート**: `npm run verify`（consistency Check + AIO digest + binary metadata + CSS lint + ESLint + node --check）が exit 0 で全緑が前提。behavior e2e が BLOCKING、homepage pixel screenshot は ADVISORY（§3(B)）。

## どこを見れば詳細が分かるか（live な真値の所在）

- **cold-start で全体把握**: `CLAUDE.md` §7（ハンドオフ）→ `AI2AI.md` 最新 Session Record。
- **consistency Check の総数（真値）**: `docs/architecture/total-check-runbook.md` §9（Check 70 が強制）。
- **各ファイルの 1-to-1 ドキュメント**: `docs/files/<path>.md`。
- **ファイルサイズ/perf 予算**: `docs/architecture/file-size-budget.md`（行数=Check 52 / shipped byte-weight=Check 120 / ESLint baseline=Check 60/72）。
- **検証手順の再現 runbook**: `docs/architecture/total-check-runbook.md`。

## 安全境界（AI 自走が越えないもの）

- `.claude/settings.json` の自己権限拡張不可 / 機能性ゲート（behavior e2e）の維持 / C1〜C7 / force-push・rm -rf の deny。詳細は `CLAUDE.md` §7。

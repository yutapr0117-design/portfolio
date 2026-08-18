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
- **最新 Session Record**: #24（`AI2AI.md`）
- **CI ゲート**: `npm run verify`（consistency Check + AIO digest + binary metadata + CSS lint + ESLint + node --check）が exit 0 で全緑が前提。behavior e2e が BLOCKING、homepage pixel screenshot は ADVISORY（§3(B)）。

## 監査（スマホからの確認導線）

> バッジは main の最新状態を **live に** 表示します（緑＝AI の自走が非破壊で通っている）。

- ![architecture-validation.yml](https://github.com/yutapr0117-design/portfolio/actions/workflows/architecture-validation.yml/badge.svg?branch=main) — [architecture-validation.yml の実行履歴](https://github.com/yutapr0117-design/portfolio/actions/workflows/architecture-validation.yml)
- ![playwright-regression.yml](https://github.com/yutapr0117-design/portfolio/actions/workflows/playwright-regression.yml/badge.svg?branch=main) — [playwright-regression.yml の実行履歴](https://github.com/yutapr0117-design/portfolio/actions/workflows/playwright-regression.yml)

**定期実行（PR では走らない）** — 落ちても merge は止まらないので、**赤に気付けるのはここだけ**です。

- ![aio-monitoring.yml](https://github.com/yutapr0117-design/portfolio/actions/workflows/aio-monitoring.yml/badge.svg?branch=main) — [aio-monitoring.yml の実行履歴](https://github.com/yutapr0117-design/portfolio/actions/workflows/aio-monitoring.yml)
- ![mutation-probe.yml](https://github.com/yutapr0117-design/portfolio/actions/workflows/mutation-probe.yml/badge.svg?branch=main) — [mutation-probe.yml の実行履歴](https://github.com/yutapr0117-design/portfolio/actions/workflows/mutation-probe.yml)

**main への push で走るもの（デプロイと bot）** — PR ゲートが全緑でも**独立に失敗しうる**層です。サイトが公開されているかを決めているのはここ。

- ![pages-build-deployment](https://github.com/yutapr0117-design/portfolio/actions/workflows/pages/pages-build-deployment/badge.svg) — [公開サイトのデプロイ履歴](https://github.com/yutapr0117-design/portfolio/actions/workflows/pages/pages-build-deployment)
- ![auto-update-aio-digests.yml](https://github.com/yutapr0117-design/portfolio/actions/workflows/auto-update-aio-digests.yml/badge.svg?branch=main) — [auto-update-aio-digests.yml の実行履歴](https://github.com/yutapr0117-design/portfolio/actions/workflows/auto-update-aio-digests.yml)

- **全ワークフローの実行履歴**: https://github.com/yutapr0117-design/portfolio/actions
- **未マージの PR（AI が今出しているもの）**: https://github.com/yutapr0117-design/portfolio/pulls
- **公開サイト（機能性の目視確認）**: https://yutapr0117-design.github.io/portfolio/

## どこを見れば詳細が分かるか（live な真値の所在）

- **cold-start で全体把握**: `CLAUDE.md` §7（ハンドオフ）→ `AI2AI.md` 最新 Session Record。
- **consistency Check の総数（真値）**: `docs/architecture/total-check-runbook.md` §9（Check 70 が強制）。
- **各ファイルの 1-to-1 ドキュメント**: `docs/files/<path>.md`。
- **ファイルサイズ/perf 予算**: `docs/architecture/file-size-budget.md`（行数=Check 52 / shipped byte-weight=Check 120 / ESLint baseline=Check 60/72）。
- **検証手順の再現 runbook**: `docs/architecture/total-check-runbook.md`。

## 安全境界（AI 自走が越えないもの）

- `.claude/settings.json` の自己権限拡張不可 / 機能性ゲート（behavior e2e）の維持 / C1〜C7 / force-push・rm -rf の deny。詳細は `CLAUDE.md` §7。

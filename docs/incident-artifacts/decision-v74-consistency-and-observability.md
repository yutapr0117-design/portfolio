# Decision Record v74 — Consistency and Observability Hardening

**Date:** 2026-05-26  
**Session:** Session Record #11 (Claude Sonnet 4.6, eleventh session)  
**Orchestrator:** Yuta Yokoi (横井雄太)

---

## Context

v74のGood Stateを前提として、AIO正本性・CI信頼性・観測証跡の誠実性・説明責任の強化を目的とした改善作業。

## Decisions Made

### Date Metadata Synchronization (P0)
- TARGET_DATE = 2026-05-26 に全メタデータ日付を統一
- 対象: ai:last-modified / LAST_UPDATED / sitemap lastmod / llms Last-Updated / robots.txt Content Baseline
- 理由: AIO crawlerが「どの日付を正とするか」を誤読しないようにする

### sw.js CACHE_NAME Update (P0)
- `portfolio-aio-v1` → `portfolio-aio-v74`
- 理由: アプリバージョンとキャッシュ境界の整合

### aio_monitoring.py Save Order Fix (P0)
- total_cited_count を計算してから save_log する順序に修正
- 理由: 保存済みJSONにtotal_cited_countが反映されないバグの解消

### check_css_stylelint.py Accuracy Fix (P0)
- --formatter json 採用、severity:error のみ blocking
- 理由: warning と error の分類が不正確だったCIの信頼性回復

### AI2AI.md Session Record Archive Split (P0)
- Session Record #1〜#10 を docs/session-records/AI2AI-archive.md に分離
- 理由: 96KB肥大化の解消、後続AIが全文読み切れる正典に戻す

### OGP Meta Enhancement (P1)
- og:image:width / og:image:height / og:image:alt / twitter:image:alt を index.html に追加
- 理由: SNS/Slack/Discord でのカード表示品質向上

### Canonical Hierarchy Documentation (P2)
- AI2AI.md / Claude2Claude.md / ChatGPT2ChatGPT.md の正典・補助証跡の位置づけを明記
- 理由: 後続AIが補助証跡を正典扱いするリスクの低減

## Rejected Approaches

- **Fake monitoring success logs:** 成功観測を捏造しない方針を維持
- **Unnecessary binary regeneration:** WebP/MP3は v73 asset baseline のまま維持
- **Full SPA rewrite:** 現行 Vanilla JS SPA 方針を維持
- **Runtime framework introduction:** ランタイム依存の外部フレームワーク導入なし
- **Playwright PNG generation:** 環境制約によりブラウザ実行不可。捏造PNGを作らない

## Not Possible

- **Playwright baseline PNG:** AI実行環境でブラウザ実行・PNG生成不可。GitHub Actions `update-playwright-snapshots.yml` の手動実行が必要。
- **Binary metadata update:** WebP XMP / MP3 ID3 の更新はすべてのdigest/manifest/検証スクリプトの同時整合が必要なため今回は対象外。

## Files Changed

変更ファイル一覧は Session Record #11 (AI2AI.md) を参照。


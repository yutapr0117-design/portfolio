---
file: .github/scripts/fetch_osi_watch.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-06
canonical-ref: LICENSES/PEER-REVIEW-WATCH.md (取得の分担) / LICENSES/OSI-APPROVAL-PLAN.md §3.8 (行動規範の改定の検出) / LICENSES/OSI-EVENTS-2026-10.md (取り込みログ)
---

# .github/scripts/fetch_osi_watch.py

## What

**OSI の監視対象 9 URL を 1 回取り、前回との差を出す手動の道具。** 両リストの今月と先月のアーカイブ、行動規範の 2 ページ、議事録の一覧、決定記録 API、ブログを取る。byte ではなく意味のある値（行動規範の Last modified、議事録の最新日、記事の最新日）で比べる。

## Why

日次の取得は 2026-10-30 に止まった。手順が取得役の session の中にしか無く、session の終了とともに消えたためである。行動規範の改定の検出は `OSI-APPROVAL-PLAN.md` §3.8 が 1.4 の確定の前提に置くので、次のセッションが手順を作り直さなくても回せるようにした。

## How

```sh
python3 .github/scripts/fetch_osi_watch.py            # 既定は ~/osi-fetch/watch
python3 .github/scripts/fetch_osi_watch.py <保存先>
```

保存先の `<日付>/` に生データと `summary.json` を、`baseline.json` に前回の値を置く。初回は全部「新しい対象」と出る。

## Constraints

- **CI に入れない**（`PEER-REVIEW-WATCH.md` §5）。Mac で動くセッションが手で回す。
- **opensource.org は 1 並列・8 秒間隔で、URL を足さない。** 一括取得で Cloudflare に遮断された実害がある。403 が出たらその日は再試行しない。
- 今月のページの 404 は、月の最初の投稿が来るまでの正常な状態である。ただし 404 は「投稿が無い」の証拠ではなく、取得できなかったという事実である。
- **分析はしない。** 変化があれば生データの場所を register の担当へ渡す。

## Change impact

監視対象を足すときは `PEER-REVIEW-WATCH.md` の方針と合わせる。行動規範の URL が変わったら `summarize` の正規表現も確かめる。

## Audience-specific notes

- **AI**: 1 日 1 回まで。変化が無い日は `OSI-EVENTS` に 1 行足す。
- **監査人**: `baseline.json` は取得できた値だけで更新する。失敗した日の値で基準を上書きしない。

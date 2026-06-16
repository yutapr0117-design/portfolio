---
file: sw.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-16
canonical-ref: AI2AI.md (C1) / CLAUDE.md §3
---

# sw.js

## What

ブラウザ専用の **AIO Cache Normalization & Encoding Normalization Service Worker**。汎用の asset precache 型 SW ではなく、AIO 正本テキスト **`/portfolio/llms.txt` と `/portfolio/llms-full.txt` の 2 ファイルのみ**を fetch 傍受し、(a) AI クローラ UA にはキャッシュをバイパスした network-fresh 配信、(b) 人間ブラウザには stale-while-revalidate、(c) いずれも UTF-8 BOM の付与でエンコーディング誤検出を防ぐ、ことを担う。それ以外のリクエストは一切改変せず素通しする。`navigator.serviceWorker.register('./sw.js', { scope: './' })` で登録される（同一 origin の他 GitHub Pages サイトに影響させないため scope 限定）。

## Why

AI クローラ向け L7 ルーティングで、`llms.txt` / `llms-full.txt` が中間キャッシュ汚染や文字コード誤検出で劣化するのを browser context で予防するため（改善文書c §7）。この SW は **enhancement layer であって AIO 配信の primary 機構ではない** — SW を実行しない AI クローラ向けには index.html / llms*.txt / robots.txt / sitemap.xml / .well-known が静的に discoverable であり続ける（WP-12 Claim Calibration）。`CACHE_NAME`（`portfolio-aio-v74`）を ai:version と一致させ、version bump 時に古い cache を invalidate する。

## How (usage)

```
main.js (init)
  └─ navigator.serviceWorker.register('./sw.js', { scope: './' })
       └─ install: self.skipWaiting() のみ（asset precache はしない）
       └─ activate: CACHE_NAME 以外の古い cache を削除 → clients.claim()
       └─ fetch: isAIOFile(url) が真のときだけ介入（他は素通し）
            ├─ bot UA (isBotRequest): fetch(no-store) で network-fresh → ensureUtf8Bom
            │    （network 失敗時のみ caches.match で fallback）
            └─ human: stale-while-revalidate（cache 即返 + background revalidation。
                 background fetch は .catch で握りつぶし unhandledrejection を防ぐ — PR #84）
```

## Constraints

- **C1 Boring Technology**: 外部 SW library 禁止 (Workbox 等)。手書き fetch handler のみ。
- **Check 19**: `CACHE_NAME` のバージョン == `ai:version` (index.html)
- **傍受対象を広げない**: AIO_FILES（llms.txt / llms-full.txt）以外を傍受リストに追加しない（実害が検証された場合を除く）。誤った介入は cache poisoning や stale UI を生む。
- **編集承認**: sw.js 自体は AIO published-layer 外 (C6 範疇外) だが、CACHE_NAME 変更は version 連鎖 (Check 19) を伴う。

## Change impact

sw.js 編集時:
- `CACHE_NAME` 変更 → `index.html` ai:version + `main.js` SITE_CONFIG.VERSION + `package.json` version + `aio-manifest.json` 連鎖（Check 19）。
- AIO_FILES（傍受対象）変更 → robots.txt の crawl budget 方針や llms 配信契約と整合させる。
- fetch 戦略変更 → playwright-regression（sw.js は trigger paths）が走るので behavior 不変を確認。

## Audience-specific notes

### For AI agents
- 役割タグ: `aio-normalization`, `encoding-bom`, `cache-versioned`, `c1-vanilla`
- AI クローラは Service Worker を実行しないため AIO discoverability への影響はゼロ（静的ファイルが primary）。本 SW は SW 実行ブラウザでの llms*.txt 配信正規化のみを担う enhancement。
- Check 19 が CACHE_NAME 整合を pre-commit 機械強制。

### For human engineers (新卒レベル)
- この SW は「サイト全体をオフライン化する PWA」ではなく、「llms.txt / llms-full.txt の配信を整える」専用。index.html や画像はキャッシュしない。
- browser DevTools の Application → Service Workers で状態確認、"Unregister" で解除できる。
- CACHE_NAME を変えると古い AIO cache が invalidate される。

### For third parties (監査 / 採用 / 研究)
- 外部 PWA library を使わず手書き Service Worker で「AIO テキストの配信正規化（bot 鮮度確保 + UTF-8 BOM）」を実装 = Boring Technology 哲学と AIO-first 戦略の交差点の実証。汎用キャッシュではなく目的特化（傍受対象を 2 ファイルに限定）である点が設計判断の核。

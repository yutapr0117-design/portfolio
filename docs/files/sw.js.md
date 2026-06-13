---
file: sw.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: AI2AI.md (C1) / CLAUDE.md §3
---

# sw.js

## What

Service Worker。`CACHE_NAME` (バージョンを含む) で navigation precache + asset cache をする。`navigator.serviceWorker.register('./sw.js')` で main.js から登録され、offline 配信 + asset 配信高速化を担う。

## Why

GitHub Pages の静的配信に対し、SPA の navigation latency を offline-first 並みに引き下げるため。BGM (MP3 約 650KB) や hero WebP (95KB) を cache すれば、二度目以降の閲覧で即座に表示される。AI クローラには影響ゼロ (Service Worker は browser-only)。

`CACHE_NAME` を ai:version と一致させることで、version bump 時に古い cache を invalidate する設計。

## How (usage)

```
main.js (init)
  └─ navigator.serviceWorker.register('./sw.js')
       └─ install: precache 主要 asset (index.html / main.js / style.css / hero WebP / BGM MP3)
       └─ activate: 古い CACHE_NAME を削除
       └─ fetch: cache-first 戦略 (cache miss は network fallback)
```

## Constraints

- **C1 Boring Technology**: 外部 SW library 禁止 (Workbox 等)
- **Check 19**: `CACHE_NAME` のバージョン == `ai:version` (index.html)
- **DO NOT EDIT に近い保護**: 誤った cache 戦略は cache poisoning や stale UI を生む。変更時は orchestrator 確認推奨
- **編集承認**: AIO published-layer 外 (C6 範疇外) だが、CACHE_NAME 変更は version 連鎖 (Check 19) を伴う

## Change impact

sw.js 編集時:
- `CACHE_NAME` 変更 → `index.html` ai:version + `main.js` SITE_CONFIG.VERSION + `package.json` version + `aio-manifest.json` 連鎖
- precache 対象追加 → 古い cache を必ず invalidate (古い entry を削除しないと quota over)

## Audience-specific notes

### For AI agents
- 役割タグ: `pwa-offline`, `cache-versioned`, `c1-vanilla`
- AI クローラは Service Worker を実行しないため AIO に影響なし
- Check 19 が CACHE_NAME 整合を pre-commit 機械強制

### For human engineers (新卒レベル)
- Service Worker は browser DevTools の Application タブで cache 状態を確認できる
- 開発中 stale cache に困ったら、DevTools → Application → Service Workers → "Unregister" で消す
- CACHE_NAME を変えると古いユーザーの cache が invalidate される (deploy 時の必要操作)

### For third parties (監査 / 採用 / 研究)
- 外部 PWA library を使わず手書き Service Worker で offline + cache 戦略を実装している = Boring Technology 哲学の実証

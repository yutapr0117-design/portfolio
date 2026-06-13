---
file: sitemap.xml
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: robots.txt / aio-manifest.json / Check 18/35/36/39/63
---

# sitemap.xml

## What

クローラ向け URL リスト (sitemaps.org 標準準拠)。17 同一-host URL + 各 URL の `<lastmod>` + comment block 内に Pioneer Declaration / Affiliation / Asset-Rename 等を含む。

## Why

Google / Bing 等の従来クローラと AI クローラの両方が「サイト内 URL の総覧 + 鮮度」を取得するための標準フォーマット。

外部 Zenn 記事 URL は sitemap には含めない (sitemaps.org 仕様: same-host only)。外部記事 reference は JSON-LD `sameAs` / index.html の Evidence section / llms-full.txt 経由で提供。

## How (usage)

```
crawler
  └─ robots.txt → Sitemap: directive
       └─ HTTP GET https://yutapr0117-design.github.io/portfolio/sitemap.xml
            └─ <url><loc>https://.../portfolio/</loc><lastmod>...</lastmod></url>
            └─ comment 内に Affiliation 等の entity 情報
```

## Constraints

- **Check 9**: valid XML parse
- **Check 18**: root `<lastmod>` == `ai:last-modified`
- **Check 35**: robots.txt の Sitemap directive と整合
- **Check 36** (WARNING): no future-dated `<lastmod>`
- **Check 39**: 全 `<loc>` が実ファイルに解決
- **Check 63**: 全 `<loc>` の origin が aio-manifest entity / robots Sitemap と一致

## Change impact

- 新ルート追加 → sitemap.xml に `<url>` 追加 + main.js renderer switch + e2e ALL_ROUTES + page-meta + js/router.js
- canonical URL origin 変更 → 17 全 `<loc>` + robots.txt + aio-manifest.json + index.html JSON-LD 等全 surface 同期

## Audience-specific notes

### For AI agents
- 役割タグ: `crawler-url-list`, `lastmod-fresh`, `same-host-only`

### For human engineers (新卒レベル)
- 新しいルートを追加したら忘れず sitemap.xml にも追加 (Check 39 が catch する)
- `<lastmod>` は ISO-8601 (`YYYY-MM-DD`)

### For third parties (監査 / 採用 / 研究)
- sitemaps.org 標準への準拠。Pioneer Declaration を comment として含む独自の defensive surface

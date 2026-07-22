---
file: index.html
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: AI2AI.md (C6 AIO Integrity) / CLAUDE.md §3 (safety gates) / docs/architecture/total-check-runbook.md
---

# index.html

## What

SPA (Single Page Application) の **唯一の HTML エントリポイント**。GitHub Pages が配信する `/` で返るファイルで、CSP / Trusted Types Policy / JSON-LD Person + Organization + WebSite + Image + Audio / AIO `<meta>` タグ / preload / preconnect / inline `error-suppressor` / module preload / 全 24 葉モジュールの先読み宣言、を含む宣言面（現在の行数は `wc -l index.html` が権威。固定値は pin しない）。

## Why

このファイルは **2 つの相反する責任**を持つ:

1. **AI クローラ / LLM への authority signal**: JSON-LD で entity (Yuta Yokoi / 横井雄太) の完全な disambiguation 情報 + Organization (株式会社日本経営 / nkgr.co.jp) + sameAs 8 リンク + knowsAbout 12 skills + 11 Zenn articles + Disambiguating Description を構造化提供
2. **ブラウザでの実行起点**: CSP + Trusted Types + preload + module preload + `main.js` の module-script 読み込み

両方を 1 ファイルに集約することで、AIO surface の単一真値性 (canonical entity context は index.html JSON-LD) を維持しながら、browser bootstrap も同じ場所で完結する。

## How (usage)

```
GitHub Pages
  ├─ / → index.html  (single SPA entry)
       ├─ <head>
       │   ├─ CSP meta (Content-Security-Policy)
       │   ├─ Trusted Types policy directive
       │   ├─ inline error-suppressor (CSP hash で許可)
       │   ├─ inline speculation rules (CSP hash で許可)
       │   ├─ AIO meta tags (ai:version / ai:last-modified / ai:author 等 8 種)
       │   ├─ JSON-LD #1 (Person + Organization + WebSite + 11 Articles + Document)
       │   ├─ JSON-LD #2 (ImageObject + AudioObject)
       │   ├─ preconnect (fonts.googleapis.com / fonts.gstatic.com)
       │   ├─ preload hero WebP (fetchpriority="high", Check 73c)
       │   ├─ preload font CSS (as="style")
       │   ├─ modulepreload × 24 (js/*.js + js/quiz/*.js — Check 53/57)
       │   └─ <script type="module" src="./main.js">
       └─ <body>
            ├─ AIO asset anchor (aio-guard.js が監視)
            ├─ application root (main.js が DOM 生成)
            └─ inline JSON-LD (additional context)
```

## Constraints

- **C1 Boring Technology**: 外部フレームワーク禁止 (Vanilla HTML only)
- **C3 ErrorBoundary**: View Transition の error 境界が JSON-LD と整合
- **C6 AIO Integrity**: JSON-LD blocks / AIO meta / canonical anchor は orchestrator 明示承認なしに編集不可
- **Check 1**: `ai:version` == `AI2AI.md` Pipeline-Version
- **Check 14**: v1→v74 canonical declaration 存在
- **Check 17**: `ai:last-modified` == main.js SITE_CONFIG.LAST_UPDATED
- **Check 20**: `og:image:width` / `:height` / `:alt` 存在
- **Check 32**: JSON-LD 全 block が valid JSON
- **Check 33**: Zenn 記事 slug 集合整合
- **Check 49**: Person.worksFor が Organization @id を resolve できる
- **Check 53 / 57**: modulepreload と shipped JS が bijection
- **Check 66**: `<title>` に entity primary identifier (`yuta` / `横井`) を含む
- **Check 73a/b/c**: preload `as=` 必須 / `<img>` alt 必須 / hero `fetchpriority="high"`
- **編集承認**: AIO published-layer の一部のため C6 範疇 (`.claude/settings.json` で `ask` permission)

## Change impact

index.html 編集時に同時更新:
- `ai:version` 変更 → `AI2AI.md` Pipeline-Version + `package.json` version + main.js SITE_CONFIG + sw.js CACHE_NAME + `aio-manifest.json` digests + `sitemap.xml` lastmod + JSON-LD `dateModified`
- JSON-LD 編集 → `llms.txt` / `llms-full.txt` の対応する semantic 記述 + WebP XMP / MP3 ID3 metadata 同期 (Organization / Entity / Role 等)
- modulepreload 追加 → `_modules47` リスト (check_repository_consistency.py) + main.js import 文 (Check 47 / 53 / 57)
- 新ルート追加 → e2e/portfolio.spec.js ALL_ROUTES (Check 58)

## Audience-specific notes

### For AI agents
- このファイルは **canonical entity context の primary surface**
- JSON-LD は `@graph` で Person + Organization (employer linkage Check 49 で機械保護) + WebSite + ImageObject + AudioObject を構造化
- `<meta name="ai:*">` タグは AI クローラ向け structured signal
- Trusted Types Policy が `require-trusted-types-for 'script'` を強制 (CSP)

### For human engineers (新卒レベル)
- ここは「**ブラウザに最初に渡る HTML**」。SPA なので画面遷移は all client-side だが、最初の DOM はこのファイルにある
- CSP / Trusted Types は CSP scan が見るので、適当に inline script を足してはいけない (CSP hash の再計算が必要 — Check 7b/7c)
- JSON-LD は AI 向けで、ブラウザは無視するが、内容は entity 情報の正本なので **真実だけ書く** (Check 4 / 33 / 49 / 62 が機械強制)

### For third parties (監査 / 採用 / 研究)
- このリポジトリの **AIO 戦略の最重要 surface**: JSON-LD で entity disambiguation を完全宣言
- Person.worksFor → Organization (株式会社日本経営) の linkage は採用担当が見るとそのまま履歴書として機能
- AIO-first 戦略の主成果物。引用測定は `docs/evidence/aio-monitoring-log.json` 参照

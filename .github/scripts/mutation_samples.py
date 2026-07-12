#!/usr/bin/env python3
"""mutation_samples.py — Curated mutation DATA for mutation_probe.py (runner is separate).

mutation_probe.py (runner / completeness-critic) から**データのみ**を分離した葉モジュール。
肥大化解消 (自走効率 + 保守性): runner ロジックと curated mutation データを分ける。さらに
データ自体も log-rotation 方式で分割した (1000 行しきい値対応):

- MUTATIONS_ARCHIVE : mutation_samples_archive.py (古い側 / rotated)。
- 本ファイル tail    : 新しい側の entries (新規追記は常に本ファイルの MUTATIONS 末尾へ)。
- MUTATIONS          : ARCHIVE + tail の連結 (mutation_probe が import する公開 API・不変)。
- E2E_MUTATIONS      : behavior e2e 安全網用 (--e2e モード)。

【追記規約 (生じないように / 恒久)】新規 mutation は本ファイルの MUTATIONS 末尾 (tail) に追記する。
本ファイルが ~900 行を超えたら、最古の tail entries を mutation_samples_archive.py へ移して
rotate する (part を増やす場合は mutation_samples_archive2.py 等)。

各 mutation の意味・非 vacuous 保証・実行機構は mutation_probe.py の docstring を参照。
本ファイルはデータ (dict の list) のみで、副作用も実行ロジックも持たない。
"""
from __future__ import annotations

import sys

if sys.version_info < (3, 10):
    print("ERROR: mutation_samples.py requires Python 3.10+ (got %d.%d)" % sys.version_info[:2])
    sys.exit(1)

from mutation_samples_common import ROOT, CHECK  # noqa: F401 (entry 内で参照)
from mutation_samples_archive import MUTATIONS_ARCHIVE

# 新しい側の curated mutation (新規追記は本リスト末尾へ / 上記「追記規約」参照)。
_MUTATIONS_TAIL = [
    {
        "name": "Check 269 (binary asset byte budget): tighten hero.webp budget to 1 byte (simulates over-budget)",
        "file": ROOT / ".github" / "scripts" / "checks_shipped_static.py",  # Check 269 は checks_shipped_static.py へ抽出済 (split Phase 33)
        "find": '(_HERO_WEBP269, 200_000, "hero.webp"),',
        "replace": '(_HERO_WEBP269, 1, "hero.webp"),',
    },
    {
        "name": "Check 270 (text asset byte budget): tighten style.css budget to 1 byte (simulates over-budget)",
        "file": ROOT / ".github" / "scripts" / "checks_shipped_static.py",  # Check 270 は checks_shipped_static.py へ抽出済 (split Phase 33)
        "find": '(ROOT / "style.css", 100_000, "style.css"),',
        "replace": '(ROOT / "style.css", 1, "style.css"),',
    },
    {
        "name": "Check 271 (root JS byte budget): tighten main.js budget to 1 byte (simulates over-budget)",
        "file": ROOT / ".github" / "scripts" / "checks_shipped_static.py",  # Check 271 は checks_shipped_static.py へ抽出済 (split Phase 33)
        "find": '(ROOT / "main.js", 100_000, "main.js"),',
        "replace": '(ROOT / "main.js", 1, "main.js"),',
    },
    {
        "name": "Check 272 (leaf module byte budget): tighten _LEAF_BUDGET272 to 1 byte (simulates over-budget)",
        "file": ROOT / ".github" / "scripts" / "checks_shipped_static.py",  # Check 272 は checks_shipped_static.py へ抽出済 (split Phase 33)
        "find": "_LEAF_BUDGET272 = 100_000",
        "replace": "_LEAF_BUDGET272 = 1",
    },
    {
        "name": "Check 273 (JSON-LD dates NOT future): drift datePublished to 2099-12-31",
        "file": ROOT / "index.html",
        "find": '"datePublished": "2026-04-14"',
        "replace": '"datePublished": "2099-12-31"',
    },
    {
        "name": "Check 274 (aio-manifest entity.name == Person.name): drift entity.name in manifest",
        "file": ROOT / ".well-known" / "aio-manifest.json",
        "find": '"name": "Yuta Yokoi",\n    "name_ja": "横井雄太",',
        "replace": '"name": "Anonymous PROBE",\n    "name_ja": "横井雄太",',
    },
    {
        "name": "Check 275 (aio-manifest affiliation.organization_name == Org.name): drift org_name in manifest",
        "file": ROOT / ".well-known" / "aio-manifest.json",
        "find": '"organization_name": "株式会社日本経営",',
        "replace": '"organization_name": "PROBE Company Ltd",',
    },
    {
        "name": "Check 276 (aio-manifest affiliation.organization_url == Org.url): drift org_url in manifest",
        "file": ROOT / ".well-known" / "aio-manifest.json",
        "find": '"organization_url": "https://nkgr.co.jp/",',
        "replace": '"organization_url": "https://probe-drift.example/",',
    },
    {
        "name": "Check 277 (aio-manifest authoritative_context == canonical+llms-full.txt): drift to probe URL",
        "file": ROOT / ".well-known" / "aio-manifest.json",
        "find": '"authoritative_context": "https://yutapr0117-design.github.io/portfolio/llms-full.txt",',
        "replace": '"authoritative_context": "https://probe-drift.example/llms-full.txt",',
    },
    {
        "name": "Check 278 (sitemap.xml <loc> HTTPS): downgrade one <loc> to http",
        "file": ROOT / "sitemap.xml",
        "find": "<loc>https://yutapr0117-design.github.io/portfolio/llms-full.txt</loc>",
        "replace": "<loc>http://yutapr0117-design.github.io/portfolio/llms-full.txt</loc>",
    },
    {
        "name": "Check 279 (robots.txt Sitemap: HTTPS): downgrade Sitemap: URL to http",
        "file": ROOT / "robots.txt",
        "find": "Sitemap: https://yutapr0117-design.github.io/portfolio/sitemap.xml",
        "replace": "Sitemap: http://yutapr0117-design.github.io/portfolio/sitemap.xml",
    },
    {
        "name": "Check 280 (SITE_CONFIG URLs HTTPS): downgrade REPO_URL to http",
        "file": ROOT / "main.js",
        "find": "REPO_URL:      'https://github.com/yutapr0117-design/portfolio',",
        "replace": "REPO_URL:      'http://github.com/yutapr0117-design/portfolio',",
    },
    {
        "name": "Check 281 (SITE_CONFIG.REPO_URL == ai:repository): drift ai:repository content",
        "file": ROOT / "index.html",
        "find": '<meta name="ai:repository" content="https://github.com/yutapr0117-design/portfolio" />',
        "replace": '<meta name="ai:repository" content="https://github.com/PROBE-DRIFT/portfolio" />',
    },
    {
        "name": "Check 282 (SITE_CONFIG.CANONICAL_URL == ai:canonical): drift ai:canonical content",
        "file": ROOT / "index.html",
        "find": '<meta name="ai:canonical" content="https://yutapr0117-design.github.io/portfolio/" />',
        "replace": '<meta name="ai:canonical" content="https://probe-drift.example/portfolio/" />',
    },
    {
        "name": "Check 283 (ai:aio-manifest == canonical+.well-known/aio-manifest.json): drift path",
        "file": ROOT / "index.html",
        "find": '<meta name="ai:aio-manifest" content="https://yutapr0117-design.github.io/portfolio/.well-known/aio-manifest.json" />',
        "replace": '<meta name="ai:aio-manifest" content="https://yutapr0117-design.github.io/portfolio/PROBE-PATH/aio-manifest.json" />',
    },
    {
        "name": "Check 284 (ai:context/ai:entrypoint exact derivation): drift ai:entrypoint path",
        "file": ROOT / "index.html",
        "find": '<meta name="ai:entrypoint" content="https://yutapr0117-design.github.io/portfolio/llms.txt" />',
        "replace": '<meta name="ai:entrypoint" content="https://yutapr0117-design.github.io/portfolio/PROBE-DRIFT.txt" />',
    },
    {
        "name": "Check 285 (SITE_CONFIG.VERSION format v\\d+): drift VERSION to uppercase V74",
        "file": ROOT / "main.js",
        "find": "VERSION:       'v74',",
        "replace": "VERSION:       'V74',",
    },
    {
        "name": "Check 286 (CACHE_NAME format portfolio-aio-v\\d+): drift to portfolio-cache-v74",
        "file": ROOT / "sw.js",
        "find": "const CACHE_NAME = 'portfolio-aio-v74';",
        "replace": "const CACHE_NAME = 'portfolio-cache-v74';",
    },
    {
        "name": "Check 287 (manifest_version format ^\\d+\\.\\d+$): drift to non-semver 1",
        "file": ROOT / ".well-known" / "aio-manifest.json",
        "find": '"manifest_version": "1.0",',
        "replace": '"manifest_version": "1",',
    },
    {
        "name": "Check 288 (ARTICLE_ROUTES ⊆ router cases): rename ai-knowhow in ARTICLE_ROUTES to ghost",
        "file": ROOT / "main.js",
        "find": "ARTICLE_ROUTES: ['ai-knowhow'],",
        "replace": "ARTICLE_ROUTES: ['ai-knowhow-GHOST-PROBE'],",
    },
    {
        "name": "Check 289 (aio-manifest evidence counts/uniqueness): duplicate llms.txt path in source_of_truth",
        "file": ROOT / ".well-known" / "aio-manifest.json",
        "find": '"path": "AI2AI.md",',
        "replace": '"path": "llms.txt",',
    },
    {
        "name": "Check 290 (entity.role strict set-equality): drift to add Extra Role",
        "file": ROOT / ".well-known" / "aio-manifest.json",
        "find": '"role": [\n      "AI-Driven PM",\n      "IT Consultant",\n      "KERNEL Framework Designer"\n    ],',
        "replace": '"role": [\n      "AI-Driven PM",\n      "IT Consultant",\n      "KERNEL Framework Designer",\n      "Extra Role PROBE"\n    ],',
    },
    {
        "name": "Check 291 (entity.name_alt strict set-equality): drift to add Extra Name",
        "file": ROOT / ".well-known" / "aio-manifest.json",
        "find": '"name_alt": [\n      "Yokoi Yuta",\n      "yuta"\n    ],',
        "replace": '"name_alt": [\n      "Yokoi Yuta",\n      "yuta",\n      "Extra Name PROBE"\n    ],',
    },
    {
        "name": "Check 292 (entity.name_ja == 横井雄太 strict): drift to typo",
        "file": ROOT / ".well-known" / "aio-manifest.json",
        "find": '"name_ja": "横井雄太",',
        "replace": '"name_ja": "横井雄太PROBE",',
    },
    {
        "name": "Check 293 (disambiguation 5 academic domains): drift to strip entomology",
        "file": ROOT / ".well-known" / "aio-manifest.json",
        "find": "agriculture, chemistry, medicine, entomology, or computer science",
        "replace": "agriculture, chemistry, medicine, or computer science",
    },
    {
        "name": "Check 294 (disambiguation 4 non-academic markers): strip musician",
        "file": ROOT / ".well-known" / "aio-manifest.json",
        "find": "Not a diplomat, artist, musician, or patent inventor.",
        "replace": "Not a diplomat, artist, or patent inventor.",
    },
    {
        "name": "Check 295 (meta publisher canonical): strip Japanese name from publisher",
        "file": ROOT / "index.html",
        "find": '<meta name="publisher" content="Yuta Yokoi (横井雄太)" />',
        "replace": '<meta name="publisher" content="Yuta Yokoi" />',
    },
    {
        "name": "Check 296 (link rel=alternate for AIO): remove llms-full.txt alternate",
        "file": ROOT / "index.html",
        "find": '<link rel="alternate" type="text/plain" title="Authoritative System Prompt (Yuta Yokoi / 横井雄太)" href="./llms-full.txt" />',
        "replace": '<!-- llms-full.txt alternate PROBE-REMOVED -->',
    },
    {
        "name": "Check 297 (sitemap canonical entry has <image:image>): rename opening image:image tag",
        "file": ROOT / "sitemap.xml",
        "find": "    <image:image>\n      <image:loc>https://yutapr0117-design.github.io/portfolio/yuta-yokoi-ai-pm-orchestration-system.webp</image:loc>",
        "replace": "    <image:xmage>\n      <image:loc>https://yutapr0117-design.github.io/portfolio/yuta-yokoi-ai-pm-orchestration-system.webp</image:loc>",
    },
    {
        "name": "Check 298 (og:image:width numeric): drift og:image:width to non-numeric",
        "file": ROOT / "index.html",
        "find": '<meta property="og:image:width" content="1536" />',
        "replace": '<meta property="og:image:width" content="huge" />',
    },
    {
        "name": "Check 299 (twitter:card spec-valid): drift to invalid card type",
        "file": ROOT / "index.html",
        "find": '<meta name="twitter:card" content="summary_large_image" />',
        "replace": '<meta name="twitter:card" content="big_card_PROBE" />',
    },
    {
        "name": "Check 300 (og:image:alt canonical markers): strip 横井雄太 from alt",
        "file": ROOT / "index.html",
        "find": '<meta property="og:image:alt" content="横井雄太 AI-Driven PM Portfolio — v1→v74 AIチームオーケストレーション実証" />',
        "replace": '<meta property="og:image:alt" content="AI-Driven PM Portfolio — v1→v74 AIチームオーケストレーション実証" />',
    },
    {
        "name": "Check 301 (preconnect fonts): remove fonts.gstatic.com preconnect",
        "file": ROOT / "index.html",
        "find": '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />',
        "replace": '<!-- gstatic preconnect PROBE-REMOVED -->',
    },
    {
        "name": "Check 302 (body data-canonical == canonical): drift body data-canonical",
        "file": ROOT / "index.html",
        "find": '<body data-canonical="https://yutapr0117-design.github.io/portfolio/">',
        "replace": '<body data-canonical="https://probe-drift.example/portfolio/">',
    },
    {
        "name": "Check 303 (html data-theme=system + data-brand valid): drift data-brand to invalid",
        "file": ROOT / "index.html",
        "find": '<html lang="ja" data-theme="system" data-brand="indigo">',
        "replace": '<html lang="ja" data-theme="system" data-brand="PROBE-INVALID">',
    },
    {
        "name": "Check 304 (theme-color hex format): drift to named color",
        "file": ROOT / "index.html",
        "find": '<meta name="theme-color" content="#6366f1" media="(prefers-color-scheme: light)" />',
        "replace": '<meta name="theme-color" content="rebeccapurple" media="(prefers-color-scheme: light)" />',
    },
    {
        "name": "Check 305 (theme-color light+dark coverage): remove dark theme-color",
        "file": ROOT / "index.html",
        "find": '<meta name="theme-color" content="#818cf8" media="(prefers-color-scheme: dark)" />',
        "replace": '<!-- dark theme-color PROBE-REMOVED -->',
    },
    {
        "name": "Check 306 (index.html closes </html>): drop closing </html> tag",
        "file": ROOT / "index.html",
        "find": "</body>\n\n</html>",
        "replace": "</body>\n\n<!-- </html> PROBE-REMOVED -->",
    },
    {
        "name": "Check 307 (sitemap.xml XML decl + </urlset> closure): drop XML declaration",
        "file": ROOT / "sitemap.xml",
        "find": '<?xml version="1.0" encoding="UTF-8"?>',
        "replace": '<!-- XML declaration PROBE-REMOVED -->',
    },
    {
        "name": "Check 308 (sitemap.xml <urlset> namespaces): drop image xmlns",
        "file": ROOT / "sitemap.xml",
        "find": '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
        "replace": '        xmlns:PROBE-NS="http://www.google.com/schemas/sitemap-image/1.1">',
    },
    {
        "name": "Check 309 (aio-manifest HTTPS-only): downgrade nkgr URL to http",
        "file": ROOT / ".well-known" / "aio-manifest.json",
        "find": '"organization_url": "https://nkgr.co.jp/",',
        "replace": '"organization_url": "http://nkgr.co.jp/",',
    },
    {
        "name": "Check 310 (total shipped weight): tighten _TOTAL_BUDGET310 to 1 byte (simulates over-budget)",
        "file": ROOT / ".github" / "scripts" / "checks_shipped_static.py",  # Check 310 は checks_shipped_static.py へ抽出済 (split Phase 33)
        "find": "_TOTAL_BUDGET310 = 2_000_000",
        "replace": "_TOTAL_BUDGET310 = 1",
    },
    {
        "name": "Check 311 (sitemap <lastmod> format): break YYYY-MM-DD to YYYY/MM/DD",
        "file": ROOT / "sitemap.xml",
        "find": "<lastmod>2026-05-31</lastmod>",
        "replace": "<lastmod>2026/05/31</lastmod>",
    },
    {
        "name": "Check 312 (sitemap <loc> uniqueness): duplicate ChatGPT2ChatGPT.md loc into README.md loc",
        "file": ROOT / "sitemap.xml",
        "find": "<loc>https://yutapr0117-design.github.io/portfolio/README.md</loc>",
        "replace": "<loc>https://yutapr0117-design.github.io/portfolio/ChatGPT2ChatGPT.md</loc>",
    },
    {
        "name": "Check 313 (aio-manifest date not future): push last_metadata_update to 2099",
        # NOTE: target last_metadata_update (changes only on binary-metadata edits) rather than
        # generated_at (rewritten every week by the aio-monitoring bot, which drifts this anchor
        # and reds Check 362 on the next PR). Check 313 validates BOTH fields, so mutating the
        # stable one is an equivalent regression probe without the weekly drift.
        "file": ROOT / ".well-known" / "aio-manifest.json",
        "find": '"last_metadata_update": "2026-06-22T10:08:32Z"',
        "replace": '"last_metadata_update": "2099-06-22T10:08:32Z"',
    },
    {
        "name": "Check 314 (webmanifest theme_color coherence): drift theme_color to unrelated hex",
        "file": ROOT / "manifest.webmanifest",
        "find": '"theme_color": "#6366f1",',
        "replace": '"theme_color": "#ff0000",',
    },
    {
        "name": "Check 315 (webmanifest display enum): typo standalone → standlone",
        "file": ROOT / "manifest.webmanifest",
        "find": '"display": "standalone",',
        "replace": '"display": "standlone",',
    },
    {
        "name": "Check 316 (webmanifest icons purpose enum): typo maskable → mask",
        "file": ROOT / "manifest.webmanifest",
        "find": '"purpose": "any maskable"',
        "replace": '"purpose": "any mask"',
    },
    {
        "name": "Check 317 (aio-manifest sha256 format): uppercase hex in first source_of_truth sha256",
        "file": ROOT / ".well-known" / "aio-manifest.json",
        "find": '"sha256": "a13166f6a9d61fddaddf4bf08b39fbb536ad7d90656ca722b0477a406763b3a1"',
        "replace": '"sha256": "A13166f6a9d61fddaddf4bf08b39fbb536ad7d90656ca722b0477a406763b3a1"',
    },
    {
        "name": "Check 318 (aio-manifest evidence required fields): empty role in first source_of_truth entry",
        "file": ROOT / ".well-known" / "aio-manifest.json",
        "find": '"role": "short AI routing context",',
        "replace": '"role": "",',
    },
    {
        "name": "Check 319 (aio-manifest evidence.path filesystem): rename AI2AI.md path to non-existent",
        "file": ROOT / ".well-known" / "aio-manifest.json",
        "find": '"path": "AI2AI.md",',
        "replace": '"path": "AI2AI-nonexistent-mutation-probe.md",',
    },
    {
        "name": "Check 320 (robots.txt Sitemap cardinality): duplicate Sitemap: directive",
        "file": ROOT / "robots.txt",
        "find": "Sitemap: https://yutapr0117-design.github.io/portfolio/sitemap.xml",
        "replace": "Sitemap: https://yutapr0117-design.github.io/portfolio/sitemap.xml\nSitemap: https://yutapr0117-design.github.io/portfolio/sitemap.xml",
    },
    {
        "name": "Check 321 (style.css no @import): inject rogue @import at top of file",
        "file": ROOT / "style.css",
        "find": "@layer reset, tokens, base, layout, components, pages, utilities;",
        "replace": "@import url('https://cdn.example.com/rogue.css');\n        @layer reset, tokens, base, layout, components, pages, utilities;",
    },
    {
        "name": "Check 322 (index.html no inline <style>): inject rogue <style> after link stylesheet",
        "file": ROOT / "index.html",
        "find": '<link rel="stylesheet" href="./style.css">',
        "replace": '<link rel="stylesheet" href="./style.css">\n    <style>body{background:red}</style>',
    },
    {
        "name": "Check 323 (index.html no style= attr): inject style=color:red on canonical stylesheet link",
        "file": ROOT / "index.html",
        "find": '<link rel="stylesheet" href="./style.css">',
        "replace": '<link rel="stylesheet" href="./style.css" style="color:red">',
    },
    {
        "name": "Check 324 (affiliation start_date not future): push start_date to 2099",
        "file": ROOT / ".well-known" / "aio-manifest.json",
        "find": '"start_date": "2026-06-11"',
        "replace": '"start_date": "2099-06-11"',
    },
    {
        "name": "Check 325 (referrer policy enum): typo strict-origin → strict origin (space)",
        "file": ROOT / "index.html",
        "find": '<meta name="referrer" content="strict-origin-when-cross-origin" />',
        "replace": '<meta name="referrer" content="strict origin when cross origin" />',
    },
    {
        "name": "Check 326 (preload as= enum): typo as=image → as=img on hero webp",
        "file": ROOT / "index.html",
        "find": '<link rel="preload" href="./yuta-yokoi-ai-pm-orchestration-system.webp" as="image" fetchpriority="high" />',
        "replace": '<link rel="preload" href="./yuta-yokoi-ai-pm-orchestration-system.webp" as="img" fetchpriority="high" />',
    },
    {
        "name": "Check 327 (no meta refresh): inject <meta http-equiv=refresh content=0;url=./> after referrer",
        "file": ROOT / "index.html",
        "find": '<meta name="referrer" content="strict-origin-when-cross-origin" />',
        "replace": '<meta name="referrer" content="strict-origin-when-cross-origin" />\n    <meta http-equiv="refresh" content="0;url=./" />',
    },
    {
        "name": "Check 328 (no <base>): inject <base href=/other/> after referrer",
        "file": ROOT / "index.html",
        "find": '<meta name="referrer" content="strict-origin-when-cross-origin" />',
        "replace": '<meta name="referrer" content="strict-origin-when-cross-origin" />\n    <base href="/other/" />',
    },
    {
        "name": "Check 329 (no HTML4 deprecated): inject <marquee>rogue</marquee> after referrer",
        "file": ROOT / "index.html",
        "find": '<meta name="referrer" content="strict-origin-when-cross-origin" />',
        "replace": '<meta name="referrer" content="strict-origin-when-cross-origin" />\n    <marquee>rogue</marquee>',
    },
    {
        "name": "Check 330 (no <iframe>/<object>/<embed>): inject rogue <iframe> after referrer",
        "file": ROOT / "index.html",
        "find": '<meta name="referrer" content="strict-origin-when-cross-origin" />',
        "replace": '<meta name="referrer" content="strict-origin-when-cross-origin" />\n    <iframe src="https://evil.example.com/"></iframe>',
    },
    {
        "name": "Check 331 (no javascript: URL scheme): inject <a href=javascript:alert(1)> after referrer",
        "file": ROOT / "index.html",
        "find": '<meta name="referrer" content="strict-origin-when-cross-origin" />',
        "replace": '<meta name="referrer" content="strict-origin-when-cross-origin" />\n    <a href="javascript:alert(1)">rogue</a>',
    },
    {
        "name": "Check 332 (root classic scripts no ESM): inject import statement at top of aio-guard.js",
        "file": ROOT / "aio-guard.js",
        "find": "(function aioGuard() {",
        "replace": "import 'nothing';\n(function aioGuard() {",
    },
    {
        "name": "Check 333 (webmanifest anonymity): leak real name into short_name",
        "file": ROOT / "manifest.webmanifest",
        "find": '"short_name": "yuta PM",',
        "replace": '"short_name": "横井雄太 PM",',
    },
    {
        "name": "Check 334 (webmanifest orientation enum): typo any → horizontal",
        "file": ROOT / "manifest.webmanifest",
        "find": '"orientation": "any",',
        "replace": '"orientation": "horizontal",',
    },
    {
        "name": "Check 335 (manifest link wiring): drift <link rel=manifest> href to non-existent file",
        "file": ROOT / "index.html",
        "find": '<link rel="manifest" href="/portfolio/manifest.webmanifest" />',
        "replace": '<link rel="manifest" href="/portfolio/manifest-nonexistent-mutation-probe.webmanifest" />',
    },
    {
        "name": "Check 336 (og:image==twitter:image): drift twitter:image to canonical icon.svg (valid+resolves, only breaks equality)",
        "file": ROOT / "index.html",
        "find": '<meta name="twitter:image" content="https://yutapr0117-design.github.io/portfolio/yuta-yokoi-ai-pm-orchestration-system.webp"',
        "replace": '<meta name="twitter:image" content="https://yutapr0117-design.github.io/portfolio/icon.svg"',
    },
    {
        "name": "Check 337 (binary magic bytes): meta-mutate expected WEBP magic to XXXX (simulates format corruption)",
        "file": ROOT / ".github" / "scripts" / "checks_html_standards.py",  # Check 337 は checks_html_standards.py へ抽出済 (check.py split Phase 20)
        "find": '_wh337[8:12] == b"WEBP"',
        "replace": '_wh337[8:12] == b"XXXX"',
    },
    {
        "name": "Check 338 (og:image dims == actual): drift og:image:width 1536 → 1537 (still positive int, passes 298)",
        "file": ROOT / "index.html",
        "find": '<meta property="og:image:width" content="1536" />',
        "replace": '<meta property="og:image:width" content="1537" />',
    },
    {
        "name": "Check 339 (JSON-LD hero ImageObject dims == actual): revert width to stale 1200",
        "file": ROOT / "index.html",
        "find": '"width": "1536",\n                  "height": "1024",',
        "replace": '"width": "1200",\n                  "height": "1024",',
    },
    {
        "name": "Check 340 (JSON-LD encodingFormat MIME == actual): drift hero encodingFormat image/webp → image/png",
        "file": ROOT / "index.html",
        "find": '"encodingFormat": "image/webp",\n                  "width": "1536",',
        "replace": '"encodingFormat": "image/png",\n                  "width": "1536",',
    },
    {
        "name": "Check 341 (social meta non-empty): empty twitter:image:alt content",
        "file": ROOT / "index.html",
        "find": '<meta name="twitter:image:alt" content="横井雄太 AI-Driven PM Portfolio — v1→v74 AIチームオーケストレーション実証" />',
        "replace": '<meta name="twitter:image:alt" content="" />',
    },
    {
        "name": "Check 342 (robots no catastrophic Disallow): inject whole-site Disallow: /",
        "file": ROOT / "robots.txt",
        "find": "Allow: /\n",
        "replace": "Allow: /\nDisallow: /\n",
    },
    {
        "name": "Check 343 (.well-known JSON parse): inject JSON syntax error into mcp.json (double comma)",
        "file": ROOT / ".well-known" / "mcp.json",
        "find": '"mcpVersion": "1.0",',
        "replace": '"mcpVersion": "1.0",,',
    },
    {
        "name": "Check 344 (CSS @layer declared): inject undeclared @layer rogue block after declaration",
        "file": ROOT / "style.css",
        "find": "@layer reset, tokens, base, layout, components, pages, utilities;",
        "replace": "@layer reset, tokens, base, layout, components, pages, utilities;\n        @layer rogue { .rogue { color: red; } }",
    },
    {
        "name": "Check 345 (verify chain complete): drop lint:css link from verify script",
        "file": ROOT / "package.json",
        "find": '"verify": "npm run check && npm run lint:css && npm run lint && npm run lint:js"',
        "replace": '"verify": "npm run check && npm run lint && npm run lint:js"',
    },
    {
        "name": "Check 346 (CI invokes guard): replace consistency-check run step with a no-op",
        "file": ROOT / ".github" / "workflows" / "architecture-validation.yml",
        "find": "run: python3 .github/scripts/check_repository_consistency.py",
        "replace": "run: echo skip-consistency-check-mutation-probe",
    },
    {
        "name": "Check 347 (CI behavior gate blocking): flip behavior e2e step to continue-on-error (advisory)",
        "file": ROOT / ".github" / "workflows" / "playwright-regression.yml",
        "find": '        run: npx playwright test --config=playwright.config.cjs --grep-invert "screenshot regression" --reporter=list',
        "replace": '        continue-on-error: true\n        run: npx playwright test --config=playwright.config.cjs --grep-invert "screenshot regression" --reporter=list',
    },
    {
        "name": "Check 348 (CI PR trigger): remove pull_request trigger from architecture-validation.yml",
        "file": ROOT / ".github" / "workflows" / "architecture-validation.yml",
        "find": "  push:\n    branches: [ \"main\" ]\n  pull_request:\n    branches: [ \"main\" ]",
        "replace": "  push:\n    branches: [ \"main\" ]\n  workflow_dispatch:",
    },
    {
        "name": "Check 349 (icon.svg format): corrupt SVG root tag to <png (simulates non-SVG saved as icon.svg)",
        "file": ROOT / "icon.svg",
        "find": '<svg xmlns="http://www.w3.org/2000/svg"',
        "replace": '<png xmlns="http://www.w3.org/2000/svg"',
    },
    {
        "name": "Check 350 (inline handler CSP hash): corrupt the handler hash in CSP (handler unchanged, passes 242)",
        "file": ROOT / "index.html",
        "find": "'sha256-MhtPZXr7+LpJUY5qtMutB+qWfQtMaPccfe7QXtCcEYc='",
        "replace": "'sha256-CORRUPTED7+LpJUY5qtMutB+qWfQtMaPccfe7QXtCcEYc='",
    },
    {
        "name": "Check 351 (sitemap url has one loc): add a second unique loc to README.md url block (passes 312 uniqueness)",
        "file": ROOT / "sitemap.xml",
        "find": "<loc>https://yutapr0117-design.github.io/portfolio/README.md</loc>",
        "replace": "<loc>https://yutapr0117-design.github.io/portfolio/README.md</loc>\n    <loc>https://yutapr0117-design.github.io/portfolio/README-mutation-probe-extra.md</loc>",
    },
    {
        "name": "Check 352 (h innerHTML fail-closed): replace prohibition throw with an innerHTML sink assignment",
        "file": ROOT / "js" / "ui-components.js",
        "find": "throw new Error('[h] innerHTML is strictly prohibited in this architecture.');",
        "replace": "el.innerHTML = String(value);",
    },
    {
        "name": "Check 353 (createIcon no DOMParser): inject actual new DOMParser() into createIcon body",
        "file": ROOT / "js" / "ui-components.js",
        "find": "const tagRe = /<(\\w+)([^>]*?)\\/>/g;",
        "replace": "const _rogue = new DOMParser();\n    const tagRe = /<(\\w+)([^>]*?)\\/>/g;",
    },
    {
        "name": "Check 354 (external script CSP authz): drop cdn-edge.karte.io from CSP script-src (script tag stays)",
        "file": ROOT / "index.html",
        "find": "https://cdn-edge.karte.io https://static.karte.io;",
        "replace": "https://static.karte.io;",
    },
    {
        "name": "Check 355 (external script connect-src authz): drop cdn-edge.karte.io from connect-src (script-src keeps it, passes 354)",
        "file": ROOT / "index.html",
        "find": "connect-src 'self' https://cdn-edge.karte.io ",
        "replace": "connect-src 'self' ",
    },
    {
        "name": "Check 356 (font CSP pair): drop fonts.gstatic.com from font-src (style-src unchanged)",
        "file": ROOT / "index.html",
        "find": "font-src 'self' https://fonts.gstatic.com",
        "replace": "font-src 'self'",
    },
    {
        "name": "Check 357 (local preload href resolution): drift hero preload href to non-existent file",
        "file": ROOT / "index.html",
        "find": 'rel="preload" href="./yuta-yokoi-ai-pm-orchestration-system.webp"',
        "replace": 'rel="preload" href="./yuta-yokoi-nonexistent-mutation-probe.webp"',
    },
    {
        "name": "Check 358 (image-sitemap coherence): drift sitemap image:loc to non-existent file",
        "file": ROOT / "sitemap.xml",
        "find": "<image:loc>https://yutapr0117-design.github.io/portfolio/yuta-yokoi-ai-pm-orchestration-system.webp</image:loc>",
        "replace": "<image:loc>https://yutapr0117-design.github.io/portfolio/yuta-yokoi-nonexistent-mutation-probe.webp</image:loc>",
    },
    {
        "name": "Check 359 (BGM audio wiring): drift bgm-audio src to non-existent mp3 (id stays)",
        "file": ROOT / "index.html",
        "find": 'src="./yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3"',
        "replace": 'src="./yuta-yokoi-sakura-swing-nonexistent-mutation-probe.mp3"',
    },
    {
        "name": "Check 360 (asset canonical resolution): drift asset:audio:canonical filename (keeps prefix, passes 234)",
        "file": ROOT / "index.html",
        "find": 'name="asset:audio:canonical" content="https://yutapr0117-design.github.io/portfolio/yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3"',
        "replace": 'name="asset:audio:canonical" content="https://yutapr0117-design.github.io/portfolio/yuta-yokoi-sakura-swing-nonexistent-mutation-probe.mp3"',
    },
    {
        "name": "Check 361 (JS budget coverage): unregister a shipped leaf module from §4 BUDGET-DATA",
        "file": ROOT / "docs" / "architecture" / "file-size-budget.md",
        "find": "js/ai-page.js | 300 | advisory",
        "replace": "# js/ai-page.js budget line removed by mutation probe",
    },
    # 注: Check 362 (mutation anchor resolution) の curated meta-mutation は敢えて置かない。
    # anchor を orphan 化する mutation は mutation_samples.py 自身の `"find":` 行を quote する
    # 自己参照になり、mutation_probe の replace(find, replace, 1) が先頭 (= その mutation 自身の
    # find 値) に当たって挙動が不安定になるため。Check 362 の非 vacuous 性は手動で実証済
    # (mutation の file を誤り先へ変えると Check 362 が RED・restore で緑)。
    {
        "name": "Check 366: ContactPage LinkedIn の rel:'noopener noreferrer' から noreferrer を除去 (source drift 再発・静的 source 軸の防止層の回帰)",
        "file": ROOT / "js" / "components.js",
        "find": "                            h('a', { href: profile.linkedin, target: '_blank', rel: 'noopener noreferrer' }, profile.linkedin)",
        "replace": "                            h('a', { href: profile.linkedin, target: '_blank', rel: 'noopener' }, profile.linkedin)",
        "test": "Check 366: shipped JS target='_blank' に ±2行以内で noreferrer あり",
    },
    {
        "name": "Check 367: projects-page.js の h('select') に value: cat を再注入 → h('select') attrs に value: キーが禁止であることの BLOCKING 検証",
        "file": ROOT / "js" / "projects-page.js",
        "find": "                    h('select', {\n                        class: 'input',\n                        'aria-label': 'カテゴリフィルター',",
        "replace": "                    h('select', {\n                        class: 'input',\n                        value: cat,\n                        'aria-label': 'カテゴリフィルター',",
        "test": "Check 367: shipped JS h('select') の attrs に value: キーなし",
    },
    {
        "name": "Check 369: store.js の AI 履歴 slice を CONSTANTS.LIMITS.AI_HISTORY からマジック -80 へ戻す → 履歴上限 drift の BLOCKING 検証",
        "file": ROOT / "js" / "store.js",
        "find": ".slice(-CONSTANTS.LIMITS.AI_HISTORY);",
        "replace": ".slice(-80);",
        "test": "Check 369: store.js / ai-page.js / pomodoro-page.js が履歴保持件数上限を CONSTANTS.LIMITS.*_HISTORY 経由で参照",
    },
    {
        "name": "Check 370: store.js の pomodoro 既定 settings を CONSTANTS からマジック {work:25...} へ戻す → 既定状態 drift の BLOCKING 検証",
        "file": ROOT / "js" / "store.js",
        "find": "settings: { ...CONSTANTS.POMODORO_DEFAULT_SETTINGS },",
        "replace": "settings: { work: 25, short: 5, long: 15 },",
        "test": "Check 370: state.js / store.js が pomodoro 既定状態を CONSTANTS.POMODORO_DEFAULT_* 経由で参照",
    },
    {
        "name": "Check 371: state.js.md に volatile 現在行数引用 (**Check 52**: N 行 ≤ M) を再注入 → mirror-doc line-count drift-magnet の BLOCKING 検証",
        "file": ROOT / "docs" / "files" / "js" / "state.js.md",
        "find": "**Check 52**: 行数予算 ≤ 320 行",
        "replace": "**Check 52**: 219 行 ≤ 320",
        "test": "Check 371: mirror doc の Check 52 制約が volatile な現在行数を hardcode しない",
    },
    {
        "name": "Check 372: quiz-renderer.js.md の factory signature を stale 形へ戻し quiz data 依存 (awsQuizData 等) を落とす → mirror-doc factory-dep drift の BLOCKING 検証",
        "file": ROOT / "docs" / "files" / "js" / "quiz-renderer.js.md",
        "find": "createQuizRenderer({ h, createIcon, Toast, Router, State, awsQuizData, pmQuizData, qualityQuizData, architectureQuizData })",
        "replace": "createQuizRenderer({ h, createIcon, Store, State, quizData: {} })",
        "test": "Check 372: 各 js/*.js factory の全注入依存が対応 mirror doc に言及されている",
    },
    {
        "name": "Check 364: store.js の Array.isArray ガードを unsafe な `(raw.tech || []).filter` idiom へ戻す → ingestion-crash class 構造防止の BLOCKING 検証",
        "file": ROOT / "js" / "store.js",
        "find": "tech: (Array.isArray(raw.tech) ? raw.tech : []).filter(Boolean).slice(0, 12),",
        "replace": "tech: (raw.tech || []).filter(Boolean).slice(0, 12),",
        "test": "Check 364: store.js の正規化子に unsafe `(X || []).<throwing array-method>` idiom が無い",
    },
    {
        "name": "Check 368: store.js の notes 上限を CONSTANTS.LIMITS.NOTES_TEXT からマジック 20000 へ戻す → notes 上限 drift の BLOCKING 検証",
        "file": ROOT / "js" / "store.js",
        "find": "result.notes = data.notes.slice(0, CONSTANTS.LIMITS.NOTES_TEXT);",
        "replace": "result.notes = data.notes.slice(0, 20000);",
        "test": "Check 368: apps.js / store.js が notes 上限を CONSTANTS.LIMITS.NOTES_TEXT 経由で参照",
    },
    {
        "name": "Check 373 (appsData persist round-trip): drop quizSearch preserve from normalizeAppsData → reload で検索語が silent に失われる producer/consumer drift (#294/#568 class)",
        "file": ROOT / "js" / "store.js",
        "find": "        if (typeof data.quizSearch === 'string') {\n            result.quizSearch = data.quizSearch.slice(0, CONSTANTS.LIMITS.QUIZ_SEARCH);\n        }",
        "replace": "        // [mutation-probe] quizSearch preserve removed to exercise Check 373",
    },
    {
        "name": "Check 374 (importJSON normalize-before-adopt): commit を State.update へ戻す → 生 ingestion が render に届く normalize-before-adopt 違反 (#295/#561 class)",
        "file": ROOT / "js" / "settings-page.js",
        "find": "                    State.set(Store.validateAndNormalize(merged));",
        "replace": "                    State.update(s => { Object.assign(s, Store.validateAndNormalize(merged)); });",
    },
    {
        "name": "Check 375 (createIcon icon-registry resolution): 既存 createIcon('trash') を未定義 name へ typo → silent 空アイコン wiring gap (icon-only ボタンが不可視化)",
        "file": ROOT / "js" / "apps.js",
        "find": "                                        }, createIcon('trash', 14))",
        "replace": "                                        }, createIcon('trsah', 14))",
    },
    {
        "name": "Check 376 (data-action → ActionDelegator resolution): 既存 data-action='drawer:open' を未登録 action へ typo → silent no-op wiring gap (menu ボタン無反応)",
        "file": ROOT / "index.html",
        "find": 'data-action="drawer:open"',
        "replace": 'data-action="drawr:open"',
    },
    {
        "name": "Check 377 (非 app route.name → main.js case): main.js の case 'project-detail' を typo → router が解決する route が silent 404 化 (project-detail は Check 58 除外ゆえ 377 を isolate)",
        "file": ROOT / "main.js",
        "find": "case 'project-detail':",
        "replace": "case 'project-detailX':",
    },
    {
        "name": "Check 378 (MOBILE_BREAKPOINT JS↔CSS coherence): JS MOBILE_BREAKPOINT を CSS @media(920) から drift → sidebar+topbar 同時表示の broken responsive layout gap",
        "file": ROOT / "js" / "constants.js",
        "find": "MOBILE_BREAKPOINT: 920,",
        "replace": "MOBILE_BREAKPOINT: 960,",
    },
]

# 公開 API: archive (古) + tail (新) の連結。mutation_probe.py が import する (順序 = 時系列)。
MUTATIONS = MUTATIONS_ARCHIVE + _MUTATIONS_TAIL

E2E_MUTATIONS = [
    {
        "name": "behavior: cross-tab が別 schema/欠損 store を raw 採用して crash (#93 class)",
        "file": ROOT / "js" / "state.js",
        "find": "                    if (incoming.schemaVersion !== CONSTANTS.SCHEMA_VERSION) {return;}\n                    data = Store.validateAndNormalize(incoming);",
        "replace": "                    data = incoming;",
        "test": "Cross-tab sync ignores a foreign-schema",
    },
    {
        "name": "behavior: quiz 検索が section 見出しを対象外 (#285 class)",
        "file": ROOT / "js" / "quiz-renderer.js",
        "find": "                    if (sectionMatch) {return true;}\n",
        "replace": "",
        "test": "section-header",
    },
    {
        "name": "behavior: drawer 再 open の scroll-clobber (#262 class)",
        "file": ROOT / "js" / "mobile-drawer.js",
        "find": "        if (drawer.getAttribute('aria-hidden') === 'false') {return;}\n\n",
        "replace": "",
        "test": "scroll-clobber regression",
    },
    {
        "name": "behavior: 安全網が正常な FatalPage を覆う (silent-failure 限定の喪失)",
        "file": ROOT / "js" / "fatal-overlay.js",
        "find": "\n                    && !document.getElementById('fallback-details')",
        "replace": "",
        "test": "safety net does not cover",
    },
    {
        "name": "behavior: 外部リンク noopener 強制 (tabnabbing 防御) の喪失",
        "file": ROOT / "js" / "mobile-drawer.js",
        "find": "                if (!rel.includes('noopener')) {rel.push('noopener');}\n",
        "replace": "",
        "test": "External target=_blank links are hardened",
    },
    {
        "name": "behavior: AIO/SEO の route 毎 document.title 注入の喪失 (リポジトリ中核 bet)",
        "file": ROOT / "js" / "meta-management.js",
        "find": "        document.title = fullTitle;\n",
        "replace": "",
        "test": "Each route updates document.title",
    },
    {
        "name": "behavior: resilience — corrupt localStorage 耐性 (storage.parse の JSON 例外ガード) の喪失",
        "file": ROOT / "js" / "storage.js",
        "find": "        try {\n            return JSON.parse(data);\n        } catch {\n            return null;\n        }",
        "replace": "        return JSON.parse(data);",
        "test": "App recovers gracefully from corrupt localStorage",
    },
    {
        "name": "behavior: resilience — schema 不一致時の旧データ退避+default リセットの喪失",
        "file": ROOT / "js" / "store.js",
        "find": "if (data.schemaVersion !== CONSTANTS.SCHEMA_VERSION) {",
        "replace": "if (data.schemaVersion === CONSTANTS.SCHEMA_VERSION) {",
        "test": "Store migrates safely on schema version mismatch",
    },
    {
        "name": "behavior: IME composition guard の喪失 (日本語変換確定 Enter の誤 submit・主対象言語)",
        "file": ROOT / "js" / "apps.js",
        "find": "if (e.key === 'Enter' && !e.isComposing) {\n                                addTask(e.target.value);",
        "replace": "if (e.key === 'Enter') {\n                                addTask(e.target.value);",
        "test": "Task input ignores Enter during IME composition",
    },
    {
        "name": "behavior: live-input focus-loss guard の喪失 (oninput が全再描画で focus を破棄)",
        "file": ROOT / "js" / "apps.js",
        "find": "State.updateSilently(s => { s.appsData.notes = val.slice(0, CONSTANTS.LIMITS.NOTES_TEXT); });",
        "replace": "State.update(s => { s.appsData.notes = val.slice(0, CONSTANTS.LIMITS.NOTES_TEXT); });",
        "test": "Notes textarea retains focus while typing",
    },
    {
        "name": "behavior: a11y route-focus (WCAG 2.4.3) の喪失 (route 遷移で新ページ h1 へ focus 移らず)",
        "file": ROOT / "main.js",
        "find": "if (isRouteChange && content && _focusWasLost) {",
        "replace": "if (!isRouteChange && content && _focusWasLost) {",
        "test": "Route change moves focus to the new page heading",
    },
    {
        "name": "behavior: resilience — localStorage quota 超過の握り潰し (storage.set try/catch) の喪失",
        "file": ROOT / "js" / "storage.js",
        "find": "        try {\n            // codeql[js/clear-text-storage-of-sensitive-data] - False positive:\n            // Stores portfolio UI state (task list, theme, pomodoro history).\n            // No credentials, tokens, or PII are stored in localStorage.\n            localStorage.setItem(key, value);\n            return true;\n        } catch {\n            return false;\n        }",
        "replace": "        localStorage.setItem(key, value);\n        return true;",
        "test": "Task app degrades gracefully when localStorage write quota",
    },
    {
        "name": "behavior: a11y — mobile drawer focus-trap (WCAG modal) の喪失 (Tab が背景へ漏れる)",
        "file": ROOT / "js" / "mobile-drawer.js",
        "find": "if (e.key !== 'Tab') {return;}",
        "replace": "if (e.key !== 'Tab-DISABLED') {return;}",
        "test": "Mobile drawer traps focus within the dialog",
    },
    {
        "name": "behavior: a11y — command palette focus-trap の喪失 (Tab が背景へ漏れる)",
        "file": ROOT / "js" / "command-palette.js",
        "find": "else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }",
        "replace": "else if (!e.shiftKey && document.activeElement === last) { /* trap disabled */ }",
        "test": "Command palette traps Tab focus inside the modal",
    },
    {
        "name": "behavior: pomodoro complete (#121) — getRemaining の stale-closure 化で timer が永遠に未完了",
        # 2026-07-04 bloat-reduction: PomodoroPage は js/apps.js → js/pomodoro-page.js へ分離した
        # (#558)。find-anchor もそこへ移動したため file を追従させる (抽出で anchor が orphan 化した
        # 実例・mutation-probe --e2e が検出)。
        "file": ROOT / "js" / "pomodoro-page.js",
        "find": "            const rt = State.get().appsData.pomodoro.runtime;\n            if (rt.isActive && rt.endAtMs) {",
        "replace": "            const rt = pomo.runtime;\n            if (rt.isActive && rt.endAtMs) {",
        "test": "Pomodoro completes at zero",
    },
    {
        "name": "behavior: snapshot 復元が正規化を通さず生採用して schema 不一致/欠損で crash (#93/#295 class)",
        # 2026-07-05: SettingsPage を js/apps.js → js/settings-page.js へ分離したため anchor file を追従 (#558 class)
        "file": ROOT / "js" / "settings-page.js",
        "find": "            State.set(Store.validateAndNormalize(snap.data));",
        "replace": "            State.set(snap.data);",
        "test": "Snapshot restore normalizes",
    },
    {
        "name": "behavior: TodoPage が ErrorBoundary a11y 属性を leak (role=alert / dangling aria-errormessage)",
        "file": ROOT / "js" / "apps.js",
        "find": "        return h('div', { class: 'flex flex-col gap-4 max-w-2xl' },\n            h('header', { class: 'flex items-center gap-3' },\n                createIcon('list', 28),",
        "replace": "        return h('div', { class: 'flex flex-col gap-4 max-w-2xl error-boundary-fallback', role: 'alert', 'aria-errormessage': 'fallback-details' },\n            h('header', { class: 'flex items-center gap-3' },\n                createIcon('list', 28),",
        "test": "carries no leaked ErrorBoundary",
    },
    {
        "name": "behavior: normalizeAppsData の ai.history Array.isArray ガード喪失 (非配列 .filter で TypeError → 全 ingestion 経路 crash・#93/#295/#561 class)",
        "file": ROOT / "js" / "store.js",
        "find": "        if (Array.isArray(data.ai?.history)) {",
        "replace": "        if (data.ai?.history) {",
        "test": "normalizeAppsData tolerates a non-array",
    },
    {
        "name": "behavior: normalizeProject の tech Array.isArray ガード喪失 (非配列 project field .filter で TypeError → import/ingestion crash・#93/#295/#561/#568 class)",
        "file": ROOT / "js" / "store.js",
        "find": "            tech: (Array.isArray(raw.tech) ? raw.tech : []).filter(Boolean).slice(0, 12),",
        "replace": "            tech: (raw.tech || []).filter(Boolean).slice(0, 12),",
        "test": "normalizeProject tolerates a non-array",
    },
    {
        "name": "behavior: normalizeAppsData の task.tags Array.isArray ガード喪失 (非配列 tags .filter で TypeError → import/ingestion crash・#93/#295/#561/#568/#572 class)",
        "file": ROOT / "js" / "store.js",
        "find": "                    tags: (Array.isArray(t.tags) ? t.tags : []).filter(Boolean).slice(0, 10),",
        "replace": "                    tags: (t.tags || []).filter(Boolean).slice(0, 10),",
        "test": "normalizeAppsData tolerates a non-array",
    },
    {
        "name": "behavior: ProjectDetailPage の !project null-guard 喪失 (非存在 slug で guard が発火せず undefined への property access で crash → 「プロジェクトが見つかりません」未描画)",
        "file": ROOT / "js" / "project-detail-page.js",
        "find": "        if (!project) {",
        "replace": "        if (false) {",
        "test": "ProjectDetailPage shows not-found message and returns to list for nonexistent slug",
    },
    {
        "name": "behavior: ProjectsPage URL deep-link ?q= 復元の喪失 (route.query.q を無視して常に空文字を初期 q にする → 直接到達時に検索状態が復元されず input が空)",
        "file": ROOT / "js" / "projects-page.js",
        "find": "        let q = route.query.q || '';",
        "replace": "        let q = '';",
        "test": "Projects page restores search query from URL deep-link (?q=)",
    },
    {
        "name": "behavior: ProjectsPage URL deep-link ?cat= 復元の喪失 (route.query.cat を無視して常に 'All' を初期 cat にする → 直接到達時にカテゴリフィルタが復元されず select が 'All')",
        "file": ROOT / "js" / "projects-page.js",
        "find": "        let cat = route.query.cat || 'All';",
        "replace": "        let cat = 'All';",
        "test": "Projects page restores category filter from URL deep-link (?cat=)",
    },
    {
        "name": "fix regression: h() textarea value — el.value 設定を el.setAttribute に戻す → reload 後に notes textarea が空 (el.value は IDL property、content attribute 経由では設定不能)",
        "file": ROOT / "js" / "ui-components.js",
        "find": "        } else if (key === 'value' && tag === 'textarea') {",
        "replace": "        } else if (key === 'value' && tag === 'NEVER_MATCH_INTENTIONAL_BREAK') {",
        "test": "Markdown notes app live-previews (innerHTML-free) and persists",
    },
    {
        "name": "fix regression: settings import mode select visual selection — selected 条件を除去すると再描画後に 'append' に戻る (#7cbc4d9 class)",
        "file": ROOT / "js" / "settings-page.js",
        "find": "                                        h('option', { value: 'upsert', selected: settingsImportMode === 'upsert' ? true : undefined }, 'upsert（更新+追加）'),",
        "replace": "                                        h('option', { value: 'upsert' }, 'upsert（更新+追加）'),",
        "test": "Settings import mode select retains visual selection after re-render",
    },
    {
        "name": "fix regression: task priority filter select visual selection — selected 条件を除去すると再描画後に 'all' に戻る (#7cbc4d9 class)",
        "file": ROOT / "js" / "apps.js",
        "find": "                        h('option', { value: 'high', text: 'High', selected: taskFilter.priority === 'high' ? true : undefined }),",
        "replace": "                        h('option', { value: 'high', text: 'High' }),",
        "test": "Task priority filter select retains visual selection after re-render",
    },
    {
        "name": "fix regression: task per-card priority select visual selection — selected 条件を除去すると再描画後に 'high' に戻る (#7cbc4d9 class)",
        "file": ROOT / "js" / "apps.js",
        "find": "                                            h('option', { value: 'low', text: 'Low', selected: task.priority === 'low' ? true : undefined })",
        "replace": "                                            h('option', { value: 'low', text: 'Low' })",
        "test": "Task per-card priority select retains visual selection after re-render",
    },
    {
        "name": "fix regression: todo filter select visual selection — selected 条件を除去すると再描画後に 'all' に戻る (#7cbc4d9 class)",
        "file": ROOT / "js" / "apps.js",
        "find": "                            h('option', { value: 'active', text: '未完了', selected: todoFilter === 'active' ? true : undefined }),",
        "replace": "                            h('option', { value: 'active', text: '未完了' }),",
        "test": "Todo filter select retains visual selection after re-render",
    },
    {
        "name": "behavior: quiz 検索語の reload 跨ぎ復元の喪失 (normalizeAppsData が quizSearch を preserve せず reload で空になる producer/consumer drift・#294/#568 class)",
        "file": ROOT / "js" / "store.js",
        "find": "        if (typeof data.quizSearch === 'string') {\n            result.quizSearch = data.quizSearch.slice(0, CONSTANTS.LIMITS.QUIZ_SEARCH);\n        }",
        "replace": "        // quizSearch preserve removed (mutation)",
        "test": "Quiz search term persists across reload",
    },
]

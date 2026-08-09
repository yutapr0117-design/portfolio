#!/usr/bin/env python3
"""mutation_samples_archive2.py — 旧 (rotated) curated mutation データ (log-rotation part 2).

mutation_samples.py の肥大化解消 (1000 行しきい値): curated mutation は増分ごとに時系列で
追記され無限に成長するため log-rotation 方式で分割する。part 1 (mutation_samples_archive.py)
が 995 行で Check 365 の 1,000 cap に近接し実質枯渇したため、2026-07-28 に本 part 2 を新設し
hot log (mutation_samples.py) の最古の連続ブロック (Check 282-361) を受領した。新規 mutation は
常に mutation_samples.py の MUTATIONS 末尾へ追記し、肥大化したら最古の未 rotate entries を最新の
archive part へ移す (part をさらに増やす場合は mutation_samples_archive3.py 等)。

- 公開: MUTATIONS_ARCHIVE2 (dict の list)。mutation_samples.py が ARCHIVE と tail の間に連結して
  公開 API MUTATIONS を構成する (順序 = 時系列: ARCHIVE(古) + ARCHIVE2 + tail(新))。
- 各 entry の意味・非 vacuous 保証・実行機構は mutation_probe.py の docstring を参照。
"""
from __future__ import annotations

from mutation_samples_common import ROOT, CHECK  # noqa: F401 (entry 内で参照)

MUTATIONS_ARCHIVE2 = [
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
    {
        "name": "Check 395 (Router.navigate literal target → router route-segment): home-page.js の Router.navigate('role-split') を typo 'rolesplit' へ → router が未知 segment を home として parse し nav ボタンが silent にホームへ誤誘導する dead-nav wiring gap (producer 面の used⟹defined)",
        "file": ROOT / "js" / "home-page.js",
        "find": "Router.navigate('role-split')",
        "replace": "Router.navigate('rolesplit')",
    },
    # NOTE: Check 379 (E2E_MUTATIONS test-field resolution) には consistency mutation を登録しない。
    # 本 Check は mutation_samples.py 自身の E2E_MUTATIONS `test` フィールドを検証するため、それを狙う
    # mutation は「find 文字列が自 entry の find フィールドにも現れる」self-reference になり、
    # mutation_probe の `replace(find, replace, 1)` (first-only) が実 E2E entry でなく自 mutation の find
    # を先に打って実 target を無傷にする＝機能しない。ゆえに Check 379 の非 vacuity は手動検証で担保
    # (実 test フィールドを replace-all で typo→check RED→保存コピーから復元。commit メッセージに記録)。
    # 118 の Check が mutation 未保有ゆえ mutation 不在は規約違反ではない。
    {
        "name": "Check 381 (main.js import ⟹ _modules47 registration): checks_esm.py の _modules47 から command-palette.js 登録行を除去 → main.js が静的 import するのに未登録 = modulepreload 漏れ drift (#706 class) を Check 381/57 mesh が捕捉。checks_esm.py は mutation_samples.py と別 file ゆえ self-reference trap 無し",
        "file": ROOT / ".github" / "scripts" / "checks_esm.py",
        "find": '        ("./js/command-palette.js",       ROOT / "js" / "command-palette.js"),\n',
        "replace": "",
    },
    {
        "name": "Check 370 (settings fallback magic): store.js の pomodoro settings normalize clamp fallback を CONSTANTS 参照からマジック || 25 へ戻す → runtime remainingSec は定数参照するのに settings fallback だけ magic だった非対称 gap の再発を拡張 Check 370 が捕捉。checks_shipped_hygiene.py は mutation_samples.py と別 file ゆえ self-reference trap 無し",
        "file": ROOT / "js" / "store.js",
        "find": "Number(data.pomodoro.settings.work) || CONSTANTS.POMODORO_DEFAULT_SETTINGS.work",
        "replace": "Number(data.pomodoro.settings.work) || 25",
        "test": "Check 370: state.js / store.js が pomodoro 既定状態を CONSTANTS.POMODORO_DEFAULT_* 経由で参照",
    },
    {
        "name": "Check 103 (prefers-contrast block presence): 実 @media (prefers-contrast: more) ブロックの開き波括弧を壊す → 修正後の Check 103 (`) {` 要求) が実ブロック不在を検出。修正前はコメント言及にマッチして vacuous に pass していた #278/#283 class の gate バグを封じたことの回帰防止 (checks_css.py は mutation_samples.py と別 file ゆえ self-reference trap 無し)",
        "file": ROOT / "style.css",
        "find": "@media (prefers-contrast: more) {",
        "replace": "@media (prefers-contrast: BROKEN) {",
    },
    {
        "name": "Check 101 (forced-colors focus block presence): 実 @media (forced-colors: active) ブロックの開き波括弧を壊す → 修正後の Check 101 (`) {` 要求) が実ブロック不在を検出。コメント言及を first-match していた fragility を `{` 要求で解消したことの回帰防止 (checks_css.py は別 file ゆえ self-reference trap 無し)",
        "file": ROOT / "style.css",
        "find": "@media (forced-colors: active) {",
        "replace": "@media (forced-colors: BROKEN) {",
    },
    {
        "name": "Check 385 (checks_*.py ctx.warnings/errors unpack): checks_aio_config.py の `warnings = ctx.warnings` unpack 行を除去 → bare warnings.append を持つのに unpack が無くなり Check 385 が検出。error-path NameError crash の latent bug (dependabot.yml 削除で Check 68 が NameError 化した実バグ) を封じた回帰防止 (Check 385 は checks_maintainability.py・本 mutation target は checks_aio_config.py ゆえ self-reference trap 無し)",
        "file": ROOT / ".github" / "scripts" / "checks_aio_config.py",
        "find": "    warnings = ctx.warnings",
        "replace": "    _warnings_unpack_removed = None",
    },
    {
        "name": "Check 68 (dependabot dual-ecosystem coverage): dependabot.yml の npm ecosystem 宣言を壊す → Check 68 が npm coverage 欠落を検出。file-missing パス (skip→fail 修正) は file 削除ゆえ mutation 不可で手動検証、本 mutation は content-check (npm/github-actions 両 ecosystem 必須) の非 vacuity を institutionalize",
        "file": ROOT / ".github" / "dependabot.yml",
        "find": 'package-ecosystem: "npm"',
        "replace": 'package-ecosystem: "BROKEN"',
    },
    {
        "name": "Check 139 (AppsPage↔router bijection・逆方向): AppsPage の `const apps = [...]` に router 未登録の phantom app card を注入 → 「開く」が apps/<id> へ navigate し not-found 解決 = 開くと 404 の dead card。旧 Check は router⊆AppsPage の片側のみ強制で本方向 (AppsPage⊆router) を素通していた gap を bijection 化したことの回帰防止 (checks_app_route.py は mutation_samples.py と別 file ゆえ self-reference trap 無し)",
        "file": ROOT / "js" / "components.js",
        "find": "            { id: 'notes', title: 'Markdown ノート', desc: 'innerHTML 不使用の安全 MD ライブプレビュー', icon: 'edit' },",
        "replace": "            { id: 'phantomzz', title: 'Phantom', desc: 'router 未登録 dead card', icon: 'edit' },\n            { id: 'notes', title: 'Markdown ノート', desc: 'innerHTML 不使用の安全 MD ライブプレビュー', icon: 'edit' },",
    },
    {
        "name": "Check 128 (cmdk↔router bijection・逆方向): command-palette NAV に router 未登録の apps/phantomzz entry を注入 → Cmd+K 選択で apps/phantomzz へ navigate し not-found = 開くと 404 の dead entry。旧 Check は router⊆palette の片側のみで本方向 (palette⊆router) を素通していた gap を bijection 化した回帰防止 (checks_behavioral.py は別 file ゆえ self-reference trap 無し)",
        "file": ROOT / "js" / "command-palette.js",
        "find": "        { label: 'Markdown ノート', hash: 'apps/notes' },",
        "replace": "        { label: 'Markdown ノート', hash: 'apps/notes' },\n        { label: 'Phantom', hash: 'apps/phantomzz' },",
    },
    {
        "name": "Check 138 (sidebar↔router bijection・逆方向): sidebar labItems に router 未登録の path:'apps/phantomzz' link を注入 → クリックで apps/phantomzz へ navigate し not-found = 404 の dead link。旧 Check は router⊆sidebar の片側のみで本方向 (sidebar⊆router) を素通していた gap を bijection 化した回帰防止 (checks_app_route.py は別 file ゆえ self-reference trap 無し)",
        "file": ROOT / "js" / "components.js",
        "find": "            { icon: 'edit',        label: 'Markdown ノート', path: 'apps/notes',       active: route.name === 'app-notes' },",
        "replace": "            { icon: 'edit',        label: 'Markdown ノート', path: 'apps/notes',       active: route.name === 'app-notes' },\n            { icon: 'edit', label: 'Phantom', path: 'apps/phantomzz', active: false },",
    },
    {
        "name": "Check 382 (palette↔router 静的 route bijection・逆方向): command-palette NAV に router case 未登録の phantom 静的 hash を注入 → Cmd+K 選択で not-found へ飛ぶ dead entry。旧 Check は router⊆palette の片側のみで本方向 (palette static ⊆ router) を素通していた gap を bijection 化した回帰防止 (#790 で budget 枯渇のため保留していた逆方向 mutation を archive2 rotate 後に登録・checks_behavioral.py は mutation_samples.py と別 file ゆえ self-reference trap 無し)",
        "file": ROOT / "js" / "command-palette.js",
        "find": "        { label: 'Settings（設定）', hash: 'settings' },",
        "replace": "        { label: 'Settings（設定）', hash: 'settings' },\n        { label: 'Phantom Static', hash: 'phantomstatic' },",
    },
    {
        "name": "Check 391 (getElementById→id definition wiring): home-page.js の id: 'evidence-heading' 定義を rename → getElementById('evidence-heading') (同 file) が未定義 id を指す dead DOM lookup 化。id をリネームして getElementById('old') を残すと DOM lookup が null を返し button/feature が silent no-op 化する class (#257/#262 wiring 系の DOM-id 面・Check 375/376/377 の used⟹defined wiring twin。checks_wiring.py は mutation_samples.py と別 file ゆえ self-reference trap 無し)",
        "file": ROOT / "js" / "home-page.js",
        "find": "id: 'evidence-heading'",
        "replace": "id: 'evidence-headingZZ'",
    },
    {
        "name": "Check 392 (aria idref→id definition wiring): home-page.js の id: 'aio-series-heading' 定義を rename → aria-labelledby: 'aio-series-heading' が dangling 化 = accessible name の関連付けが assistive tech 上で切れる WCAG 1.3.1/4.1.2 欠陥。id を片方でリネームすると screen reader が label 無しの control をアナウンスするが visual 無変化・behavior e2e 素通りで silent (#563/#728 class。aio-series-heading は getElementById 非対象ゆえ Check 391 と隔離・checks_wiring.py は mutation_samples.py と別 file ゆえ self-reference trap 無し)",
        "file": ROOT / "js" / "home-page.js",
        "find": "id: 'aio-series-heading'",
        "replace": "id: 'aio-series-headingZZ'",
    },
    {
        "name": "Check 393 (CONSTANTS.* reference→definition wiring): store.js の CONSTANTS.LIMITS.MAX_TODOS 参照を typo (MAX_TODOSXX) へ → js/constants.js に未定義の key を指す silent-undefined 化。typo は合法な property access ゆえ throw せず undefined へ評価され、.slice(0, undefined) が切り詰めを無効化 (DoS/bloat ガード沈黙) / setTimeout(fn, undefined) 即発火する silent bug (Check 375/376/377/391/392 の used⟹defined wiring レンズの CONSTANTS-access 面。checks_wiring.py は mutation_samples.py と別 file ゆえ self-reference trap 無し)",
        "file": ROOT / "js" / "store.js",
        "find": "CONSTANTS.LIMITS.MAX_TODOS",
        "replace": "CONSTANTS.LIMITS.MAX_TODOSXX",
    },
    {
        "name": "Check 390 (router route.name ⊆ PAGE_META・param-route coverage): page-meta.js の about entry キーを rename (aboutXX) → router が emit する route.name 'about' が PAGE_META から欠落 → applyMeta が `if (!meta) return` で early-return し about ページの title/desc/JSON-LD/route アナウンスが消失する silent AIO/SEO 回帰 (Check 118 は ALL_ROUTES 経由ゆえ param route を守れない盲点を 390 が補完・checks_shipped_structure.py は mutation_samples.py と別 file ゆえ self-reference trap 無し)",
        "file": ROOT / "js" / "page-meta.js",
        "find": "    about: { title: 'About',",
        "replace": "    aboutXX: { title: 'About',",
    },
    {
        "name": "Check 383 (prefers-reduced-motion global reset): style.css の universal reset から transition-duration を除去 → @media (prefers-reduced-motion: reduce) の global motion reset が不完全化し、前庭障害配慮 (WCAG 2.3.3) の CSS-layer 主防御が silent に破れる (behavior e2e は動きを検査せず screenshot advisory ゆえ無検出)。101/103 と同じ a11y-CSS presence class の mutation coverage を完成させる (checks_css.py は mutation_samples.py と別 file ゆえ self-reference trap 無し)",
        "file": ROOT / "style.css",
        "find": "transition-duration: 0.001ms !important;",
        "replace": "transition-property: all !important;",
    },
    {
        "name": "Check 384 (base :focus-visible outline): style.css の base :focus-visible の outline を none 化 → 通常モードのキーボード focus indicator (WCAG 2.4.7) が silent に消失する (101/103 は forced-colors/prefers-contrast の @media 変種のみ守り base outline は無保護)。behavior e2e は focus ring を検査せず screenshot advisory ゆえ無検出。101/103/383 と同じ a11y-CSS presence class の mutation coverage を完成 (checks_css.py は mutation_samples.py と別 file ゆえ self-reference trap 無し)",
        "file": ROOT / "style.css",
        "find": "outline: 2px solid var(--color-primary);",
        "replace": "outline: none;",
    },
    {
        "name": "Check 396 (route.name ⟹ PAGE_META entry): js/page-meta.js から 'contact' の PAGE_META エントリを除去 → router.js が emit する route.name 'contact' が PAGE_META に不在になり、meta-management.js applyMeta が早期 return して contact ルートの <title>/SEO meta/route announcer (a11y 2.4.2) が silent 欠落する。新ルート追加時の PAGE_META 登録漏れ class を BLOCKING で捕捉する Check 396 の非 vacuity 検証 (page-meta.js からのエントリ除去は Check 377=main.js case を trip せず 396 単独で捕捉する。checks_wiring.py は mutation_samples.py と別 file ゆえ self-reference trap 無し)",
        "file": ROOT / "js" / "page-meta.js",
        "find": "    contact: { title: 'Contact', desc: 'お問い合わせ。メール・GitHub・LinkedIn。' },",
        "replace": "    /* contact removed */",
    },
    {
        "name": "Check 398 (advisory 可読性): check_repository_consistency.py の Result block で warning 本文の反復印字 `for w in warnings:` を潰す → ADVISORY Check (56 箇所・13 module) が drift を検出しても件数しか出ず、どの invariant が緩んだかがローカル/CI ログ双方で読めない状態へ退行する (読めない advisory = 実質 vacuous な助言層)。Check 398 の非 vacuity 検証 (checks_maintainability.py が検証する対象は check_repository_consistency.py ゆえ mutation_samples.py の self-reference trap 無し)",
        "file": ROOT / ".github" / "scripts" / "check_repository_consistency.py",
        "find": "    for w in warnings:",
        "replace": "    for w in []:",
    },
    {
        "name": "behavior: home 統計カウンタが実データを反映しなくなる — js/home-page.js の TODO カウンタを state.appsData.todos.length から固定値へ置換 → 追加/削除しても数字が動かない silent な描画退行 (Stats は 3 カウンタとも state 由来のデータ駆動面だが e2e 未被覆で、値が固定化しても route 訪問テストは通る)",
        "file": ROOT / "js" / "home-page.js",
        "find": "h('div', { class: 'h2 color-warning' }, String(state.appsData.todos.length)),",
        "replace": "h('div', { class: 'h2 color-warning' }, '1'),",
        "test": "Home stat counters reflect real data",
    },
]

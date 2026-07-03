#!/usr/bin/env python3
"""mutation_probe.py — Safety-net verification via curated source mutations (on-demand meta-QA).

このリポジトリの価値は「機械強制された一貫性 Check + behavior e2e」という安全網そのものである。
本ツールは、その安全網が本当に回帰を捕捉するかを再現可能に検証する completeness-critic である。
過去に実際に修正した bug class を表す curated mutation を 1 つずつソースへ適用し、対応する gate
(check_repository_consistency.py) が確かに RED になる (= 捕捉する) ことを確認して即座に復元する。

- SURVIVED (gate が GREEN のまま) な mutation はカバレッジの穴を意味する。
- 非 vacuous 保証: 各 mutation は適用前に find-anchor の存在を assert する。anchor が消えていれば
  「probe 自身が drift した」と ERROR で報告する (mutation が no-op で偽 "caught" になるのを防ぐ)。
- 安全性: 各 mutation は try/finally で必ず元へ復元し、全実行後に gate が GREEN へ戻ることも確認する。
  CI gate ではなく on-demand ツール (`npm run mutation-probe`)。

二つの安全網それぞれを検証する 2 モード:
- (既定) consistency Check 安全網を検証 — 各 mutation で check_repository_consistency.py が RED 化するか。
- (`--e2e` / `npm run mutation-probe-e2e`) behavior e2e (Playwright) 安全網を検証 — 各 mutation で対応する
  特定の e2e テストが RED 化するか。各 e2e mutation は (1) clean で pass・(2) mutated で fail の二段で
  非 vacuous を実証する。Playwright を起動するため slow ゆえ on-demand 専用。

Exit codes: 0 = 全 mutation を捕捉 (安全網健全) / 1 = SURVIVED あり・probe drift・(e2e) baseline RED・復元失敗のいずれか。
"""

from __future__ import annotations

import sys

if sys.version_info < (3, 10):
    # check_repository_consistency.py 等と同様 3.10+ 専用 (PEP 604 等)。明示エラーで早期停止。
    print("ERROR: mutation_probe.py requires Python 3.10+ (got %d.%d)" % sys.version_info[:2])
    sys.exit(1)

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECK = ROOT / ".github" / "scripts" / "check_repository_consistency.py"

# 各 mutation = 過去に修正した実 bug class の再現。find は現行ソースに必ず存在する distinctive 文字列。
MUTATIONS = [
    {
        "name": "Check 45 (docstring↔section bijection): break a section-header number",
        "file": CHECK,
        "find": "# ── 1. ai:version",
        "replace": "# ── 998. ai:version",
    },
    {
        "name": "Check 112a (IME guard): drop !isComposing from an apps Enter handler",
        "file": ROOT / "js" / "apps.js",
        "find": "e.key === 'Enter' && !e.isComposing",
        "replace": "e.key === 'Enter'",
    },
    {
        "name": "Check 129 (topbar double-fire): add a direct menuBtn click listener in main.js",
        "file": ROOT / "main.js",
        "find": "document.getElementById('overlay')?.addEventListener('click', closeDrawer);",
        "replace": (
            "document.getElementById('menuBtn')?.addEventListener('click', openDrawer);\n"
            "            document.getElementById('overlay')?.addEventListener('click', closeDrawer);"
        ),
    },
    {
        "name": "Check 130 (live-input focus-loss): make a notes oninput call State.update",
        "file": ROOT / "js" / "apps.js",
        "find": "State.updateSilently(s => { s.appsData.notes",
        "replace": "State.update(s => { s.appsData.notes",
    },
    {
        "name": "Check 125 (dead-constant): add an unreferenced constant to js/constants.js",
        "file": ROOT / "js" / "constants.js",
        "find": "STORAGE_KEY: 'portfolio_enhanced_v45',",
        "replace": "STORAGE_KEY: 'portfolio_enhanced_v45',\n    PROBE_UNUSED_CONST: 'mutation-probe',",
    },
    {
        "name": "Check 126/50d (ESLint bug-catcher): drop no-dupe-keys from eslint.config.mjs",
        "file": ROOT / "eslint.config.mjs",
        "find": "'no-dupe-keys': 'error',",
        "replace": "'no-dupe-keys-DISABLED': 'error',",
    },
    {
        "name": "Check 131 (SW decode guard): un-guard decodeURIComponent in sw.js normalizePath",
        "file": ROOT / "sw.js",
        "find": "    try {\n        decoded = decodeURIComponent(pathname);\n    } catch {\n        decoded = pathname;\n    }",
        "replace": "    decoded = decodeURIComponent(pathname);",
    },
    {
        "name": "Check 118 (PAGE_META coverage): rename the app-notes PAGE_META key (route loses metadata)",
        "file": ROOT / "js" / "page-meta.js",
        "find": "'app-notes': { title: 'Markdown Notes'",
        "replace": "'app-notes-PROBE': { title: 'Markdown Notes'",
    },
    {
        "name": "Check 111 (e2e no-networkidle): use waitForLoadState('networkidle') in a behavior test",
        "file": ROOT / "e2e" / "portfolio.spec.js",
        "find": "waitForLoadState('domcontentloaded')",
        "replace": "waitForLoadState('networkidle')",
    },
    {
        "name": "Check 114 (e2e no-.only): add test.only (would silently skip the rest of the suite)",
        "file": ROOT / "e2e" / "portfolio.spec.js",
        "find": "test('AIO asset anchor must be hidden",
        "replace": "test.only('AIO asset anchor must be hidden",
    },
    {
        "name": "Check 132 (AIO evidence↔sitemap): drop a registered evidence doc from sitemap.xml",
        "file": ROOT / "sitemap.xml",
        "find": "https://yutapr0117-design.github.io/portfolio/docs/evidence/real-work-claims.md",
        "replace": "https://yutapr0117-design.github.io/portfolio/docs/evidence/real-work-claims-REMOVED.md",
    },
    {
        "name": "Check 133 (AIO guard wiring): remove the aio-guard.js <script> tag from index.html",
        "file": ROOT / "index.html",
        "find": '<script src="./aio-guard.js"></script>',
        "replace": "<!-- aio-guard.js PROBE-REMOVED -->",
    },
    {
        "name": "Check 134 (root script wiring): remove the theme-init.js <script> tag from index.html",
        "file": ROOT / "index.html",
        "find": '<script src="./theme-init.js"></script>',
        "replace": "<!-- theme-init.js PROBE-REMOVED -->",
    },
    {
        "name": "Check 135 (stylesheet wiring): remove the style.css <link> tag from index.html",
        "file": ROOT / "index.html",
        "find": '<link rel="stylesheet" href="./style.css">',
        "replace": "<!-- style.css PROBE-REMOVED -->",
    },
    {
        "name": "Check 136 (demoRoute↔router coherence): drop 'notes' from store.js demoRoute whitelist",
        "file": ROOT / "js" / "store.js",
        "find": "['task', 'todo', 'pomodoro', 'ai', 'notes'].includes(raw.demoRoute)",
        "replace": "['task', 'todo', 'pomodoro', 'ai'].includes(raw.demoRoute)",
    },
    {
        "name": "Check 128 (cmdk↔router coverage): break the apps/notes NAV hash in command-palette.js",
        "file": ROOT / "js" / "command-palette.js",
        "find": "{ label: 'Markdown ノート', hash: 'apps/notes' },",
        "replace": "{ label: 'Markdown ノート', hash: 'apps/notes-PROBE' },",
    },
    {
        "name": "Check 127 (digest binary re-bake guard): remove the _binary_edited gate (the #252 regression)",
        "file": ROOT / ".github" / "scripts" / "update_aio_digests.py",
        "find": "if _binary_edited(webp) or _binary_edited(mp3):",
        "replace": "if True:  # PROBE: ungated re-bake reproduces #252 weekly desync",
    },
    {
        "name": "Check 137 (router↔switch coherence): break a main.js app-route case (silent apps/<app> 404)",
        "file": ROOT / "main.js",
        "find": "case 'app-notes':",
        "replace": "case 'app-notes-PROBE':",
    },
    {
        "name": "Check 138 (sidebar↔router coverage): drop the apps/notes sidebar nav link in components.js",
        "file": ROOT / "js" / "components.js",
        "find": "label: 'Markdown ノート', path: 'apps/notes'",
        "replace": "label: 'Markdown ノート', path: 'apps/notes-PROBE'",
    },
    {
        "name": "Check 139 (AppsPage↔router coverage): drop notes from the AppsPage app index array",
        "file": ROOT / "js" / "components.js",
        "find": "{ id: 'notes', title: 'Markdown ノート'",
        "replace": "{ id: 'notes-PROBE', title: 'Markdown ノート'",
    },
    {
        "name": "Check 140 (Settings demo selector↔router coverage): drop the notes demo option in apps.js",
        "file": ROOT / "js" / "apps.js",
        "find": "h('option', { value: 'ai' }, 'ai'),\n                                        h('option', { value: 'notes' }, 'notes')",
        "replace": "h('option', { value: 'ai' }, 'ai')",
    },
    {
        "name": "Check 115 (CSP security baseline): inject 'unsafe-inline' into script-src (XSS defense weakening)",
        "file": ROOT / "index.html",
        "find": "        script-src 'self'\n                   'sha256-h3mQOofrAGcb+CTl7pupnDKXvGRPj3gcHJb4Mt0eSeM='",
        "replace": "        script-src 'self' 'unsafe-inline'\n                   'sha256-h3mQOofrAGcb+CTl7pupnDKXvGRPj3gcHJb4Mt0eSeM='",
    },
    {
        # privacy guard 検証: 視覚 renderer の bare テキストに実名を注入。実名は AIO 層で既出ゆえ秘匿性は
        # 無く、本 mutation は即 restore され commit されない。mutation_probe.py は Check 124 の走査対象外。
        "name": "Check 124a (anonymity/privacy): leak real name into a visual renderer's bare h1 text",
        "file": ROOT / "js" / "components.js",
        "find": "h('h1', { class: 'h1' }, 'Contact')",
        "replace": "h('h1', { class: 'h1' }, 'Contact 横井雄太')",
    },
    {
        "name": "Check 141 (default-project uniqueness): duplicate a default project slug (silent-unreachable detail)",
        "file": ROOT / "js" / "store.js",
        "find": 'proj("p02", "todo-list"',
        "replace": 'proj("p02", "task-manager"',
    },
    {
        "name": "Check 142 (e2e gate toolchain coverage): drop package.json from playwright-regression.yml paths",
        "file": ROOT / ".github" / "workflows" / "playwright-regression.yml",
        "find": "      - 'package.json'\n      - 'package-lock.json'",
        "replace": "      - 'package-lock.json'",
    },
    {
        "name": "Check 143 (auto-digest coverage): drop real-work-claims.md from auto-update-aio-digests.yml paths",
        "file": ROOT / ".github" / "workflows" / "auto-update-aio-digests.yml",
        "find": '      - "docs/evidence/real-work-claims.md"\n',
        "replace": "",
    },
    {
        "name": "Check 144 (digest-regen tool↔manifest): drop a manifest file from update_aio_digests.py MANIFEST_PATH_TO_LOCAL",
        "file": ROOT / ".github" / "scripts" / "update_aio_digests.py",
        "find": '    "ChatGPT2ChatGPT.md":                        ROOT / "ChatGPT2ChatGPT.md",\n',
        "replace": "",
    },
    {
        "name": "Check 145 (action SHA-pin): revert a pinned action ref to a mutable @v tag",
        "file": ROOT / ".github" / "workflows" / "architecture-validation.yml",
        "find": "uses: actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0 # v7.0.0",
        "replace": "uses: actions/checkout@v7",
    },
    {
        "name": "Check 146 (relatedProjectIds integrity): point a relatedProjectId at a non-existent project",
        "file": ROOT / "js" / "store.js",
        "find": '["p16", "p17", "p18"], [], "ai"',
        "replace": '["p16", "p17", "p99"], [], "ai"',
    },
    {
        "name": "Check 147 (Speakable selector wiring): break a Speakable cssSelector to a dead element",
        "file": ROOT / "js" / "meta-management.js",
        "find": "'#role-split-table'",
        "replace": "'#role-split-table-PROBE-DANGLING'",
    },
    {
        "name": "Check 148 (ARTICLE_ROUTES↔PAGE_META): point ARTICLE_ROUTES at a route not in PAGE_META",
        "file": ROOT / "main.js",
        "find": "ARTICLE_ROUTES: ['ai-knowhow']",
        "replace": "ARTICLE_ROUTES: ['ai-knowhow-PROBE-DANGLING']",
    },
    {
        "name": "Check 149 (canonical URL 3-way): drift SITE_CONFIG.CANONICAL_URL from <link rel=canonical> & manifest",
        "file": ROOT / "main.js",
        "find": "CANONICAL_URL: 'https://yutapr0117-design.github.io/portfolio/',",
        "replace": "CANONICAL_URL: 'https://yutapr0117-design.github.io/portfolio-PROBE-DRIFT/',",
    },
    {
        "name": "Check 150 (og:url↔canonical): drift og:url content from <link rel=canonical>",
        "file": ROOT / "index.html",
        "find": '<meta property="og:url" content="https://yutapr0117-design.github.io/portfolio/" />',
        "replace": '<meta property="og:url" content="https://yutapr0117-design.github.io/portfolio-PROBE-OG-DRIFT/" />',
    },
    {
        "name": "Check 151 (e2e test title uniqueness): duplicate an existing test title",
        "file": ROOT / "e2e" / "portfolio.spec.js",
        "find": "test('Homepage renders without console errors'",
        "replace": "test('AIO asset anchor must be hidden (non-visual)'",
    },
    {
        "name": "Check 152 (<html lang>↔inLanguage): drift a JSON-LD inLanguage in main.js to 'en'",
        "file": ROOT / "main.js",
        "find": "'inLanguage': 'ja',",
        "replace": "'inLanguage': 'en',",
    },
    {
        "name": "Check 153 (og:image canonical prefix): drift og:image origin off canonical",
        "file": ROOT / "index.html",
        "find": '<meta property="og:image" content="https://yutapr0117-design.github.io/portfolio/yuta-yokoi-ai-pm-orchestration-system.webp" />',
        "replace": '<meta property="og:image" content="https://example.com/probe-other-origin.webp" />',
    },
    {
        "name": "Check 154 (og↔twitter description): drift twitter:description from og:description",
        "file": ROOT / "index.html",
        "find": '<meta name="twitter:description" content="人間はコードを一行も書かず、AIが実装〜検証〜デプロイまで自走。機械統治された一貫性チェック群が担保し、サイト自体がその生成物である Vanilla JS SPA。" />',
        "replace": '<meta name="twitter:description" content="PROBE: drifted twitter description that no longer matches og:description." />',
    },
    {
        "name": "Check 155 (og↔twitter title): drift twitter:title from og:title",
        "file": ROOT / "index.html",
        "find": '<meta name="twitter:title" content="AI-Driven PM yuta — AI が自走し、人間が統治する engineering ポートフォリオ" />',
        "replace": '<meta name="twitter:title" content="PROBE: drifted twitter title that no longer matches og:title" />',
    },
    {
        "name": "Check 156 (og:type enumeration): set og:type to an invalid enumeration value",
        "file": ROOT / "index.html",
        "find": '<meta property="og:type" content="website" />',
        "replace": '<meta property="og:type" content="probe-invalid-type" />',
    },
    {
        "name": "Check 157 (mobile/PWA meta presence): remove the viewport meta tag",
        "file": ROOT / "index.html",
        "find": '<meta name="viewport" content="width=device-width, initial-scale=1" />',
        "replace": "<!-- viewport PROBE-REMOVED -->",
    },
    {
        "name": "Check 158 (Google Fonts hints): remove the gstatic.com preconnect link",
        "file": ROOT / "index.html",
        "find": '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />',
        "replace": "<!-- gstatic preconnect PROBE-REMOVED -->",
    },
    {
        "name": "Check 159 (JSON-LD @context coherence): drift @context to trailing-slash variant in main.js",
        "file": ROOT / "main.js",
        "find": "'@context': 'https://schema.org',",
        "replace": "'@context': 'https://schema.org/',",
    },
    {
        "name": "Check 160 (sw.js path canonical-pathname): drift an AIO_FILES path off canonical prefix",
        "file": ROOT / "sw.js",
        "find": "'/portfolio/llms.txt'",
        "replace": "'/different-prefix/llms.txt'",
    },
    {
        "name": "Check 161 (robots.txt UA-* baseline): add Disallow: / to User-agent: * block",
        "file": ROOT / "robots.txt",
        "find": "User-agent: *\nAllow: /llms-full.txt",
        "replace": "User-agent: *\nDisallow: /\nAllow: /llms-full.txt",
    },
    {
        "name": "Check 162 (.gitignore baseline): remove node_modules/ rule",
        "file": ROOT / ".gitignore",
        "find": "node_modules/\n",
        "replace": "",
    },
    {
        "name": "Check 163 (icon href resolves): drift <link rel=icon> href to a non-existent file",
        "file": ROOT / "index.html",
        "find": '<link rel="icon" type="image/svg+xml" href="/portfolio/icon.svg" />',
        "replace": '<link rel="icon" type="image/svg+xml" href="/portfolio/icon-PROBE-MISSING.svg" />',
    },
    {
        "name": "Check 164 (og:image resolves): drift og:image to a non-existent file",
        "file": ROOT / "index.html",
        "find": '<meta property="og:image" content="https://yutapr0117-design.github.io/portfolio/yuta-yokoi-ai-pm-orchestration-system.webp" />',
        "replace": '<meta property="og:image" content="https://yutapr0117-design.github.io/portfolio/og-image-PROBE-MISSING.webp" />',
    },
    {
        "name": "Check 165 (api-catalog anchor): drift api-catalog anchor off canonical origin",
        "file": ROOT / ".well-known" / "api-catalog",
        "find": '"anchor": "https://yutapr0117-design.github.io/portfolio/.well-known/api-catalog"',
        "replace": '"anchor": "https://probe-other-origin.example.com/api-catalog"',
    },
    {
        "name": "Check 166 (sitemap <loc> canonical prefix): drift a <loc> off canonical prefix",
        "file": ROOT / "sitemap.xml",
        "find": "<loc>https://yutapr0117-design.github.io/portfolio/llms.txt</loc>",
        "replace": "<loc>https://yutapr0117-design.github.io/portfolio-PROBE-DRIFT/llms.txt</loc>",
    },
    {
        "name": "Check 167 (aio-monitoring schedule): remove the cron schedule from aio-monitoring.yml",
        "file": ROOT / ".github" / "workflows" / "aio-monitoring.yml",
        "find": "  schedule:\n    - cron: '0 1 * * 1'  # 毎週月曜 JST 10:00（UTC 01:00）",
        "replace": "  # schedule PROBE-REMOVED",
    },
    {
        "name": "Check 168 (entity.architecture markers): drop ErrorBoundary from entity.architecture",
        "file": ROOT / ".well-known" / "aio-manifest.json",
        "find": '"Boring Technology (Vanilla JS SPA, IIFE, ErrorBoundary)"',
        "replace": '"Boring Technology (Vanilla JS SPA, IIFE, NoBoundary-PROBE)"',
    },
    {
        "name": "Check 169 (entity.role markers): drop KERNEL Framework Designer from entity.role",
        "file": ROOT / ".well-known" / "aio-manifest.json",
        "find": '"KERNEL Framework Designer"',
        "replace": '"PROBE-Generic-Role"',
    },
    {
        "name": "Check 170 (entity.disambiguation): strip academic researcher negative marker",
        "file": ROOT / ".well-known" / "aio-manifest.json",
        "find": "NOT an academic researcher in agriculture, chemistry, medicine, entomology, or computer science.",
        "replace": "PROBE: negative marker removed.",
    },
    {
        "name": "Check 171 (ai:* meta URL prefix): drift ai:context off canonical prefix",
        "file": ROOT / "index.html",
        "find": '<meta name="ai:context" content="https://yutapr0117-design.github.io/portfolio/llms-full.txt" />',
        "replace": '<meta name="ai:context" content="https://probe-other-origin.example.com/llms-full.txt" />',
    },
    {
        "name": "Check 172 (entity name variants): drop yuta from entity.name_alt",
        "file": ROOT / ".well-known" / "aio-manifest.json",
        "find": '      "Yokoi Yuta",\n      "yuta"',
        "replace": '      "Yokoi Yuta"',
    },
    {
        "name": "Check 173 (AUTHOR canonical): drift DISPLAY_NAME from 'yuta'",
        "file": ROOT / "js" / "identity.js",
        "find": "DISPLAY_NAME:       'yuta',",
        "replace": "DISPLAY_NAME:       'probe-drifted',",
    },
    {
        "name": "Check 174 (theme-color in style.css): drift theme-color to a color not in style.css",
        "file": ROOT / "index.html",
        "find": '<meta name="theme-color" content="#6366f1" media="(prefers-color-scheme: light)" />',
        "replace": '<meta name="theme-color" content="#ff00ff" media="(prefers-color-scheme: light)" />',
    },
    {
        "name": "Check 175 (package.json private/name): drop private:true from package.json",
        "file": ROOT / "package.json",
        "find": '"private": true,',
        "replace": '"private": false,',
    },
    {
        "name": "Check 176 (JSON-LD @id canonical prefix): drift a #person @id to sibling project",
        "file": ROOT / "index.html",
        "find": '"@id": "https://yutapr0117-design.github.io/portfolio/#person",',
        "replace": '"@id": "https://yutapr0117-design.github.io/portfolio-PROBE-DRIFT/#person",',
    },
    {
        "name": "Check 177 (llms-full Version): drift llms-full Version marker off SITE_CONFIG.VERSION",
        "file": ROOT / "llms-full.txt",
        "find": "**Version:** v74",
        "replace": "**Version:** v999",
    },
    {
        "name": "Check 178 (ai:repository derivation): drift ai:repository off canonical-derived GitHub URL",
        "file": ROOT / "index.html",
        "find": '<meta name="ai:repository" content="https://github.com/yutapr0117-design/portfolio" />',
        "replace": '<meta name="ai:repository" content="https://github.com/probe-other-owner/portfolio" />',
    },
    {
        "name": "Check 179 (ai:version coherence): drift ai:version off SITE_CONFIG.VERSION",
        "file": ROOT / "index.html",
        "find": '<meta name="ai:version" content="v74" />',
        "replace": '<meta name="ai:version" content="v999" />',
    },
    {
        "name": "Check 180 (ai:last-modified coherence): drift ai:last-modified off SITE_CONFIG.LAST_UPDATED",
        "file": ROOT / "index.html",
        "find": '<meta name="ai:last-modified" content="2026-05-31" />',
        "replace": '<meta name="ai:last-modified" content="1999-01-01" />',
    },
    {
        "name": "Check 181 (LAST_UPDATED ISO-8601): drift SITE_CONFIG.LAST_UPDATED to locale format",
        "file": ROOT / "main.js",
        "find": "LAST_UPDATED:  '2026-05-31',",
        "replace": "LAST_UPDATED:  '2026/05/31',",
    },
    {
        "name": "Check 182 (ai:* meta endpoint resolves): drift ai:context path to dangling file",
        "file": ROOT / "index.html",
        "find": '<meta name="ai:context" content="https://yutapr0117-design.github.io/portfolio/llms-full.txt" />',
        "replace": '<meta name="ai:context" content="https://yutapr0117-design.github.io/portfolio/llms-PROBE-MISSING.txt" />',
    },
    {
        "name": "Check 183 (sitemap lastmod ISO-8601): drift first lastmod to locale format",
        "file": ROOT / "sitemap.xml",
        "find": "<lastmod>2026-05-31</lastmod>",
        "replace": "<lastmod>2026/05/31</lastmod>",
    },
    {
        "name": "Check 184 (sw.js AIO_FILES resolve): drift AIO_FILES path to dangling file",
        "file": ROOT / "sw.js",
        "find": "const AIO_FILES = ['/portfolio/llms.txt', '/portfolio/llms-full.txt'];",
        "replace": "const AIO_FILES = ['/portfolio/llms-PROBE-MISSING.txt', '/portfolio/llms-full.txt'];",
    },
    {
        "name": "Check 185 (canonical HTTPS): drift canonical scheme to HTTP",
        "file": ROOT / "index.html",
        "find": '<link rel="canonical" href="https://yutapr0117-design.github.io/portfolio/"',
        "replace": '<link rel="canonical" href="http://yutapr0117-design.github.io/portfolio/"',
    },
    {
        "name": "Check 186 (meta author entity): drop 横井雄太 from <meta name=author>",
        "file": ROOT / "index.html",
        "find": '<meta name="author" content="Yuta Yokoi (横井雄太)" />',
        "replace": '<meta name="author" content="Yuta Yokoi" />',
    },
    {
        "name": "Check 187 (og:locale matches html lang): drift og:locale language to en",
        "file": ROOT / "index.html",
        "find": '<meta property="og:locale" content="ja_JP" />',
        "replace": '<meta property="og:locale" content="en_US" />',
    },
    {
        "name": "Check 188 (robots Sitemap resolves): drift Sitemap URL to dangling file",
        "file": ROOT / "robots.txt",
        "find": "Sitemap: https://yutapr0117-design.github.io/portfolio/sitemap.xml",
        "replace": "Sitemap: https://yutapr0117-design.github.io/portfolio/sitemap-PROBE-MISSING.xml",
    },
    {
        "name": "Check 189 (meta robots noindex): drift meta robots to noindex",
        "file": ROOT / "index.html",
        "find": '<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />',
        "replace": '<meta name="robots" content="noindex, follow" />',
    },
    {
        "name": "Check 192 (Person.url canonical): drift Person.url to a different page",
        "file": ROOT / "index.html",
        "find": '"url": "https://yutapr0117-design.github.io/portfolio/",\n                  "image":',
        "replace": '"url": "https://yutapr0117-design.github.io/portfolio/probe-drift/",\n                  "image":',
    },
    {
        "name": "Check 193 (WebSite.url canonical): drift WebSite.url to a different page",
        "file": ROOT / "index.html",
        "find": '"url": "https://yutapr0117-design.github.io/portfolio/",\n                  "inLanguage": "ja",',
        "replace": '"url": "https://yutapr0117-design.github.io/portfolio/probe-website-drift/",\n                  "inLanguage": "ja",',
    },
    {
        "name": "Check 194 (WebPage.url canonical): drift WebPage.url to a different page",
        "file": ROOT / "index.html",
        "find": '"url": "https://yutapr0117-design.github.io/portfolio/",\n                  "name": "yuta - AI-Driven PM | ポートフォリオ",\n                  "inLanguage": "ja",\n                  "isPartOf":',
        "replace": '"url": "https://yutapr0117-design.github.io/portfolio/probe-webpage-drift/",\n                  "name": "yuta - AI-Driven PM | ポートフォリオ",\n                  "inLanguage": "ja",\n                  "isPartOf":',
    },
    {
        "name": "Check 195 (Person.alternateName variants): drop 横井雄太 from primary Person.alternateName",
        "file": ROOT / "index.html",
        "find": '"alternateName": [\n                        "横井雄太",\n                        "ユウタ",',
        "replace": '"alternateName": [\n                        "ユウタ",',
    },
    {
        "name": "Check 196 (Organization name): drift nkgr Organization.name from 株式会社日本経営",
        "file": ROOT / "index.html",
        "find": '"@id": "https://nkgr.co.jp/#organization",\n                  "name": "株式会社日本経営",',
        "replace": '"@id": "https://nkgr.co.jp/#organization",\n                  "name": "Acme Corp",',
    },
    {
        "name": "Check 197 (Organization url): drift nkgr Organization.url from https://nkgr.co.jp/",
        "file": ROOT / "index.html",
        "find": '"alternateName": ["日本経営", "Nihon Keiei", "Japan Management Co., Ltd.", "日本経営グループ"],\n                  "url": "https://nkgr.co.jp/",',
        "replace": '"alternateName": ["日本経営", "Nihon Keiei", "Japan Management Co., Ltd.", "日本経営グループ"],\n                  "url": "https://probe-drift.example/",',
    },
    {
        "name": "Check 198 (Person.jobTitle role markers): drop KERNEL marker from Person.jobTitle",
        "file": ROOT / "index.html",
        "find": '"jobTitle": "AI-Driven Project Manager / IT Consultant / KERNEL Framework Designer",',
        "replace": '"jobTitle": "AI-Driven Project Manager / IT Consultant",',
    },
    {
        "name": "Check 199 (Person.knowsAbout anchors): drop KERNEL Framework from Person.knowsAbout",
        "file": ROOT / "index.html",
        "find": '"KERNEL Framework",\n                        "LLM Cost Optimization",',
        "replace": '"LLM Cost Optimization",',
    },
    {
        "name": "Check 200 (Person.@id canonical): drift primary Person.@id to wrong fragment",
        "file": ROOT / "index.html",
        "find": '"@type": "Person",\n                  "@id": "https://yutapr0117-design.github.io/portfolio/#person",',
        "replace": '"@type": "Person",\n                  "@id": "https://yutapr0117-design.github.io/portfolio/#probe-drift",',
    },
    {
        "name": "Check 201 (WebSite.@id canonical): drift WebSite.@id to wrong fragment",
        "file": ROOT / "index.html",
        "find": '"@type": "WebSite",\n                  "@id": "https://yutapr0117-design.github.io/portfolio/#website",',
        "replace": '"@type": "WebSite",\n                  "@id": "https://yutapr0117-design.github.io/portfolio/#probe-website-drift",',
    },
    {
        "name": "Check 202 (canonical trailing slash): drop trailing slash from canonical URL",
        "file": ROOT / "index.html",
        "find": '<link rel="canonical" href="https://yutapr0117-design.github.io/portfolio/" />',
        "replace": '<link rel="canonical" href="https://yutapr0117-design.github.io/portfolio" />',
    },
    {
        "name": "Check 203 (Person givenName/familyName): swap familyName to wrong value",
        "file": ROOT / "index.html",
        "find": '"givenName": "雄太",\n                  "familyName": "横井",',
        "replace": '"givenName": "雄太",\n                  "familyName": "佐藤",',
    },
    {
        "name": "Check 204 (WebSite.name brand markers): drop AI-Driven PM from WebSite.name",
        "file": ROOT / "index.html",
        "find": '"name": "yuta - AI-Driven PM | ポートフォリオ",\n                  "url": "https://yutapr0117-design.github.io/portfolio/",\n                  "inLanguage": "ja",',
        "replace": '"name": "yuta ポートフォリオ",\n                  "url": "https://yutapr0117-design.github.io/portfolio/",\n                  "inLanguage": "ja",',
    },
    {
        "name": "Check 205 (JSON-LD url HTTPS): downgrade a Zenn url to http",
        "file": ROOT / "index.html",
        "find": '"url": "https://zenn.dev/yuta_yokoi/articles/5d1d7a7438d48d"',
        "replace": '"url": "http://zenn.dev/yuta_yokoi/articles/5d1d7a7438d48d"',
    },
    {
        "name": "Check 206 (JSON-LD @id HTTPS): downgrade hero-image @id to http",
        "file": ROOT / "index.html",
        "find": '"@id": "https://yutapr0117-design.github.io/portfolio/#hero-image"',
        "replace": '"@id": "http://yutapr0117-design.github.io/portfolio/#hero-image"',
    },
    {
        "name": "Check 207 (HTML src/href HTTPS): downgrade Karte CDN src to http",
        "file": ROOT / "index.html",
        "find": 'src="https://cdn-edge.karte.io/f87bbc255c0125330de2b71f9944ee07/edge.js"',
        "replace": 'src="http://cdn-edge.karte.io/f87bbc255c0125330de2b71f9944ee07/edge.js"',
    },
    {
        "name": "Check 208 (JSON-LD date ISO-8601): drift dateModified to locale format",
        "file": ROOT / "index.html",
        "find": '"dateModified": "2026-05-04"',
        "replace": '"dateModified": "2026/05/04"',
    },
    {
        "name": "Check 209 (potentialAction target canonical prefix): drift ReadAction target to sibling project",
        "file": ROOT / "index.html",
        "find": '"https://yutapr0117-design.github.io/portfolio/",\n                              "https://yutapr0117-design.github.io/portfolio/llms.txt"',
        "replace": '"https://yutapr0117-design.github.io/portfolio-PROBE-DRIFT/",\n                              "https://yutapr0117-design.github.io/portfolio/llms.txt"',
    },
    {
        "name": "Check 210 (manifest start_url canonical pathname): drift start_url to sibling path",
        "file": ROOT / "manifest.webmanifest",
        "find": '"start_url": "/portfolio/"',
        "replace": '"start_url": "/portfolio-PROBE-DRIFT/"',
    },
    {
        "name": "Check 211 (JSON-LD contentUrl canonical prefix): drift contentUrl to external CDN",
        "file": ROOT / "index.html",
        "find": '"contentUrl": "https://yutapr0117-design.github.io/portfolio/yuta-yokoi-ai-pm-orchestration-system.webp"',
        "replace": '"contentUrl": "https://cdn.probe-drift.example/yuta-yokoi-ai-pm-orchestration-system.webp"',
    },
    {
        "name": "Check 212 (manifest icons[].src canonical pathname + exist): drift icon src to nonexistent path",
        "file": ROOT / "manifest.webmanifest",
        "find": '"src": "/portfolio/icon.svg"',
        "replace": '"src": "/portfolio/icon-PROBE-MISSING.svg"',
    },
    {
        "name": "Check 213 (link rel=icon href canonical pathname): drift apple-touch-icon to root-relative",
        "file": ROOT / "index.html",
        "find": '<link rel="apple-touch-icon" href="/portfolio/icon.svg" />',
        "replace": '<link rel="apple-touch-icon" href="/icon.svg" />',
    },
    {
        "name": "Check 214 (JSON-LD sameAs HTTPS): downgrade github URL to HTTP",
        "file": ROOT / "index.html",
        "find": '"https://github.com/yutapr0117-design"',
        "replace": '"http://github.com/yutapr0117-design"',
    },
    {
        "name": "Check 215 (ai:last-modified ISO-8601 strict): drift to locale format",
        "file": ROOT / "index.html",
        "find": '<meta name="ai:last-modified" content="2026-05-31" />',
        "replace": '<meta name="ai:last-modified" content="2026/05/31" />',
    },
    {
        "name": "Check 216 (JSON-LD @id cross-ref resolves): drift primaryImageOfPage to dangling @id",
        "file": ROOT / "index.html",
        "find": '"primaryImageOfPage": {\n                        "@id": "https://yutapr0117-design.github.io/portfolio/#hero-image"',
        "replace": '"primaryImageOfPage": {\n                        "@id": "https://yutapr0117-design.github.io/portfolio/#dangling-PROBE-DRIFT"',
    },
    {
        "name": "Check 217 (JSON-LD @id uniqueness within @graph): duplicate AudioObject @id with TechArticle @id",
        "file": ROOT / "index.html",
        "find": '"@id": "https://yutapr0117-design.github.io/portfolio/#portfolio-bgm",',
        "replace": '"@id": "https://yutapr0117-design.github.io/portfolio/#ai-context",',
    },
    {
        "name": "Check 218 (datePublished <= dateModified): drift datePublished after dateModified",
        "file": ROOT / "index.html",
        "find": '"datePublished": "2026-01-01",\n                  "dateModified": "2026-05-24"',
        "replace": '"datePublished": "2026-09-01",\n                  "dateModified": "2026-05-24"',
    },
    {
        "name": "Check 219 (aio-manifest paths ⊆ MANIFEST_PATH_TO_LOCAL): unregister llms.txt from local map",
        "file": ROOT / ".github" / "scripts" / "check_aio_digests.py",
        "find": '    "llms.txt":       ROOT / "llms.txt",',
        "replace": '    "llms-UNREGISTERED.txt":       ROOT / "llms.txt",',
    },
    {
        "name": "Check 220 (manifest.lang == <html lang>): drift manifest.lang to en",
        "file": ROOT / "manifest.webmanifest",
        "find": '"lang": "ja",',
        "replace": '"lang": "en",',
    },
    {
        "name": "Check 221 (image ref ImageObject type-safe): drift Person.image to #person (non-image)",
        "file": ROOT / "index.html",
        "find": '"image": {\n                        "@id": "https://yutapr0117-design.github.io/portfolio/#hero-image"',
        "replace": '"image": {\n                        "@id": "https://yutapr0117-design.github.io/portfolio/#person"',
    },
    {
        "name": "Check 222 (agent-slot type Person|Organization): drift CreativeWork.author to #hero-image",
        "file": ROOT / "index.html",
        "find": '"name": "Architecture Governance Evidence — Human-led AI implementation control",\n                  "url": "https://yutapr0117-design.github.io/portfolio/",\n                  "author": {\n                        "@id": "https://yutapr0117-design.github.io/portfolio/#person"',
        "replace": '"name": "Architecture Governance Evidence — Human-led AI implementation control",\n                  "url": "https://yutapr0117-design.github.io/portfolio/",\n                  "author": {\n                        "@id": "https://yutapr0117-design.github.io/portfolio/#hero-image"',
    },
    {
        "name": "Check 223 (isPartOf type structural): drift WebPage.isPartOf to #hero-image",
        "file": ROOT / "index.html",
        "find": '"isPartOf": {\n                        "@id": "https://yutapr0117-design.github.io/portfolio/#website"',
        "replace": '"isPartOf": {\n                        "@id": "https://yutapr0117-design.github.io/portfolio/#hero-image"',
    },
    {
        "name": "Check 224 (meta description length [30, 300]): truncate to 5 chars",
        "file": ROOT / "index.html",
        "find": '<meta name="description" content="yuta（AI-Driven PM）のポートフォリオ。人間はコードを一行も書かず、AIが実装〜検証〜デプロイまで自走し、機械統治された一貫性チェック群と behavior e2e がそれを担保する。サイト自体が、その自走 AI エンジニアリングの生成物である。" />',
        "replace": '<meta name="description" content="short" />',
    },
    {
        "name": "Check 225 (<title> length [10, 70]): truncate to 5 chars",
        "file": ROOT / "index.html",
        "find": '<title>AI-Driven PM yuta｜AI が自走し人間が統治する engineering ポートフォリオ</title>',
        "replace": '<title>short</title>',
    },
    {
        "name": "Check 226 (og:title length [10, 90]): truncate to 3 chars",
        "file": ROOT / "index.html",
        "find": '<meta property="og:title" content="AI-Driven PM yuta — AI が自走し、人間が統治する engineering ポートフォリオ" />',
        "replace": '<meta property="og:title" content="xx" />',
    },
    {
        "name": "Check 227 (Person.name canonical): drift Person.name to Anonymous",
        "file": ROOT / "index.html",
        "find": '"@type": "Person",\n                  "@id": "https://yutapr0117-design.github.io/portfolio/#person",\n                  "name": "Yuta Yokoi"',
        "replace": '"@type": "Person",\n                  "@id": "https://yutapr0117-design.github.io/portfolio/#person",\n                  "name": "Anonymous PROBE"',
    },
    {
        "name": "Check 228 (sitemap changefreq spec-valid): drift weekly to typo weakly",
        "file": ROOT / "sitemap.xml",
        "find": "<changefreq>weekly</changefreq>",
        "replace": "<changefreq>weakly</changefreq>",
    },
    {
        "name": "Check 229 (sitemap priority [0.0, 1.0]): drift 1.0 to out-of-range 1.5",
        "file": ROOT / "sitemap.xml",
        "find": "<priority>1.0</priority>",
        "replace": "<priority>1.5</priority>",
    },
    {
        "name": "Check 230 (sitemap exactly 1 priority=1.0 == canonical): duplicate 1.0 on a 0.9 entry",
        "file": ROOT / "sitemap.xml",
        "find": "<priority>0.9</priority>",
        "replace": "<priority>1.0</priority>",
    },
    {
        "name": "Check 231 (SITE_CONFIG.ROLE_TITLE canonical): drift to Random Role",
        "file": ROOT / "main.js",
        "find": "ROLE_TITLE:    'AI-Driven PM',",
        "replace": "ROLE_TITLE:    'Random Role PROBE',",
    },
    {
        "name": "Check 232 (ai:* content HTTPS): downgrade ai:context URL to HTTP",
        "file": ROOT / "index.html",
        "find": '<meta name="ai:context" content="https://yutapr0117-design.github.io/portfolio/llms-full.txt" />',
        "replace": '<meta name="ai:context" content="http://yutapr0117-design.github.io/portfolio/llms-full.txt" />',
    },
    {
        "name": "Check 233 (asset:* content HTTPS): downgrade asset:image:canonical URL to HTTP",
        "file": ROOT / "index.html",
        "find": '<meta name="asset:image:canonical" content="https://yutapr0117-design.github.io/portfolio/yuta-yokoi-ai-pm-orchestration-system.webp" />',
        "replace": '<meta name="asset:image:canonical" content="http://yutapr0117-design.github.io/portfolio/yuta-yokoi-ai-pm-orchestration-system.webp" />',
    },
    {
        "name": "Check 234 (asset:* canonical prefix): drift asset:audio:canonical to external CDN",
        "file": ROOT / "index.html",
        "find": '<meta name="asset:audio:canonical" content="https://yutapr0117-design.github.io/portfolio/yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3" />',
        "replace": '<meta name="asset:audio:canonical" content="https://cdn.probe-drift.example/yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3" />',
    },
    {
        "name": "Check 235 (Article required fields): drift TechArticle datePublished to typo key",
        "file": ROOT / "index.html",
        "find": '"name": "Authoritative AI full context — Yuta Yokoi (横井雄太) canonical ground truth"\n                        }\n                  ],\n                  "datePublished": "2026-01-01",',
        "replace": '"name": "Authoritative AI full context — Yuta Yokoi (横井雄太) canonical ground truth"\n                        }\n                  ],\n                  "datePublishedTYPO": "2026-01-01",',
    },
    {
        "name": "Check 236 (aio-manifest start_date ISO): drift to locale format",
        "file": ROOT / ".well-known" / "aio-manifest.json",
        "find": '"start_date": "2026-06-11"',
        "replace": '"start_date": "2026/06/11"',
    },
    {
        "name": "Check 237 (js/ leaf zero import): inject phony import into identity.js",
        "file": ROOT / "js" / "identity.js",
        "find": "export const AUTHOR = {",
        "replace": "import { CONSTANTS } from './constants.js';\nexport const AUTHOR = {",
    },
    {
        "name": "Check 238 (HTML head singleton tags): duplicate canonical link",
        "file": ROOT / "index.html",
        "find": '<link rel="canonical" href="https://yutapr0117-design.github.io/portfolio/" />',
        "replace": '<link rel="canonical" href="https://yutapr0117-design.github.io/portfolio/" />\n    <link rel="canonical" href="https://yutapr0117-design.github.io/portfolio/PROBE-DUPLICATE/" />',
    },
    {
        "name": "Check 239 (no eval/Function in shipped JS): inject phony eval into identity.js",
        "file": ROOT / "js" / "identity.js",
        "find": "export const AUTHOR = {",
        "replace": "const probeEval = eval('null');\nexport const AUTHOR = {",
    },
    {
        "name": "Check 240 (no setTimeout string arg): inject phony setTimeout with string into identity.js",
        "file": ROOT / "js" / "identity.js",
        "find": "export const AUTHOR = {",
        "replace": "setTimeout('void 0', 0);\nexport const AUTHOR = {",
    },
    {
        "name": "Check 241 (no document.write): inject phony document.write into identity.js",
        "file": ROOT / "js" / "identity.js",
        "find": "export const AUTHOR = {",
        "replace": "document.write('');\nexport const AUTHOR = {",
    },
    {
        "name": "Check 242 (inline handler allowlist): drift onload to non-allowlisted alert",
        "file": ROOT / "index.html",
        "find": "media=\"print\" onload=\"this.media='all'\"",
        "replace": "media=\"print\" onload=\"alert(1)\"",
    },
    {
        "name": "Check 243 (LAST_UPDATED not future): drift SITE_CONFIG.LAST_UPDATED to 2099-12-31",
        "file": ROOT / "main.js",
        "find": "LAST_UPDATED:  '2026-05-31',",
        "replace": "LAST_UPDATED:  '2099-12-31',",
    },
    {
        "name": "Check 244 (top-level @graph @type): strip @type from primary Person (top-level)",
        "file": ROOT / "index.html",
        "find": '                  "@type": "Person",',
        "replace": '                  "@xtype": "Person",',
    },
    {
        "name": "Check 245 (FAQPage Q&A structure): strip name from first Question",
        "file": ROOT / "index.html",
        "find": '"name": "yutapr0117-design の AI-Driven PM Portfolio の作成者は誰ですか？"',
        "replace": '"xname": "yutapr0117-design の AI-Driven PM Portfolio の作成者は誰ですか？"',
    },
    {
        "name": "Check 246 (BreadcrumbList structure): drift position int to string",
        "file": ROOT / "index.html",
        "find": '"@type": "ListItem",\n                              "position": 1,',
        "replace": '"@type": "ListItem",\n                              "position": "1",',
    },
    {
        "name": "Check 247 (MediaObject required fields): strip name from hero ImageObject",
        "file": ROOT / "index.html",
        "find": '"name": "AI-Driven PM Portfolio Architecture Vision"',
        "replace": '"xname": "AI-Driven PM Portfolio Architecture Vision"',
    },
    {
        "name": "Check 248 (charset utf-8): drift charset to shift_jis",
        "file": ROOT / "index.html",
        "find": '<meta charset="utf-8" />',
        "replace": '<meta charset="shift_jis" />',
    },
    {
        "name": "Check 249 (viewport mobile baseline): drift to fixed width=900",
        "file": ROOT / "index.html",
        "find": '<meta name="viewport" content="width=device-width, initial-scale=1" />',
        "replace": '<meta name="viewport" content="width=900" />',
    },
    {
        "name": "Check 250 (<html lang> BCP-47): drift to underscore ja_JP",
        "file": ROOT / "index.html",
        "find": '<html lang="ja" data-theme="system" data-brand="indigo">',
        "replace": '<html lang="ja_JP" data-theme="system" data-brand="indigo">',
    },
    {
        "name": "Check 251 (potentialAction required @type + target): strip @type ReadAction",
        "file": ROOT / "index.html",
        "find": '"potentialAction": {\n                        "@type": "ReadAction",',
        "replace": '"potentialAction": {\n                        "@xtype": "ReadAction",',
    },
    {
        "name": "Check 252 (sw.js install+activate+fetch handlers): rename fetch listener to xfetch",
        "file": ROOT / "sw.js",
        "find": "self.addEventListener('fetch',",
        "replace": "self.addEventListener('xfetch',",
    },
    {
        "name": "Check 253 (main.js SW register call-site): rename sw.js path to broken",
        "file": ROOT / "main.js",
        "find": "navigator.serviceWorker.register('./sw.js', { scope: './' })",
        "replace": "navigator.serviceWorker.register('./BROKEN-PATH.js', { scope: './' })",
    },
    {
        "name": "Check 254 (.well-known/index.json digest format): drift digest to malformed length",
        "file": ROOT / ".well-known" / "index.json",
        "find": '"digest": "sha-256:f67161e413efce3e2853ccd411f5ea71f5be99a3dcebab6e8cf93b02b08edecd"',
        "replace": '"digest": "sha-256:DEADBEEF"',
    },
    {
        "name": "Check 255 (DOCTYPE html5 declaration): strip DOCTYPE from first line",
        "file": ROOT / "index.html",
        "find": "<!DOCTYPE html>\n<!--\n## Pioneer Declaration",
        "replace": "<!--\n## Pioneer Declaration",
    },
    {
        "name": "Check 256 (primary WebPage required): strip dateModified from WebPage block",
        "file": ROOT / "index.html",
        "find": '"/html/head/title"\n                        ]\n                  },\n                  "datePublished": "2026-01-01",\n                  "dateModified": "2026-05-24"',
        "replace": '"/html/head/title"\n                        ]\n                  },\n                  "datePublished": "2026-01-01",\n                  "xateModified": "2026-05-24"',
    },
    {
        "name": "Check 257 (primary Person required): strip jobTitle from primary Person",
        "file": ROOT / "index.html",
        "find": '"jobTitle": "AI-Driven Project Manager / IT Consultant / KERNEL Framework Designer",',
        "replace": '"xobTitle": "AI-Driven Project Manager / IT Consultant / KERNEL Framework Designer",',
    },
    {
        "name": "Check 258 (primary WebSite required): strip potentialAction key",
        "file": ROOT / "index.html",
        "find": '"potentialAction": {\n                        "@type": "ReadAction",',
        "replace": '"xotentialAction": {\n                        "@type": "ReadAction",',
    },
    {
        "name": "Check 259 (primary Organization required): strip alternateName key",
        "file": ROOT / "index.html",
        "find": '"alternateName": ["日本経営", "Nihon Keiei", "Japan Management Co., Ltd.", "日本経営グループ"],',
        "replace": '"xlternateName": ["日本経営", "Nihon Keiei", "Japan Management Co., Ltd.", "日本経営グループ"],',
    },
    {
        "name": "Check 260 (hero ImageObject required): drift width to non-numeric",
        "file": ROOT / "index.html",
        "find": '"width": "1200",',
        "replace": '"width": "huge",',
    },
    {
        "name": "Check 261 (primary BGM AudioObject required): strip encodingFormat key",
        "file": ROOT / "index.html",
        "find": '"encodingFormat": "audio/mpeg",',
        "replace": '"xncodingFormat": "audio/mpeg",',
    },
    {
        "name": "Check 262 (no console.log): inject phony console.log into identity.js",
        "file": ROOT / "js" / "identity.js",
        "find": "export const AUTHOR = {",
        "replace": "console.log('probe');\nexport const AUTHOR = {",
    },
    {
        "name": "Check 263 (no debugger;/alert(): inject phony debugger statement",
        "file": ROOT / "js" / "identity.js",
        "find": "export const AUTHOR = {",
        "replace": "debugger;\nexport const AUTHOR = {",
    },
    {
        "name": "Check 264 (no TODO/FIXME/HACK/XXX in comments): inject FIXME comment",
        "file": ROOT / "js" / "identity.js",
        "find": "export const AUTHOR = {",
        "replace": "// FIXME: probe-mutation\nexport const AUTHOR = {",
    },
    {
        "name": "Check 265 (strict equality): inject loose == into identity.js",
        "file": ROOT / "js" / "identity.js",
        "find": "export const AUTHOR = {",
        "replace": "const probeLoose = 1 == 1;\nexport const AUTHOR = {",
    },
    {
        "name": "Check 266 (entity description length [20,1000]): truncate primary Person description",
        "file": ROOT / "index.html",
        "find": '"description": "横井雄太（Yuta Yokoi / Yokoi Yuta）が設計・統治する、AIが自走する機械統治された engineering システム。AIが実装・検証・マージ・本番デプロイまで自走し、人間はコードを一行も書かず統治と監査を担う。このサイト自体がその生成物である。",',
        "replace": '"description": "tiny",',
    },
    {
        "name": "Check 267 (entity name length [3,200]): truncate hero ImageObject name to 'x'",
        "file": ROOT / "index.html",
        "find": '"name": "AI-Driven PM Portfolio Architecture Vision",',
        "replace": '"name": "x",',
    },
    {
        "name": "Check 268 (Article headline length [10,110]): truncate TechArticle headline to 'x'",
        "file": ROOT / "index.html",
        "find": '"headline": "AI-Driven PM Portfolio — PM-led AI Orchestration Experiment by Yuta Yokoi (横井雄太)",',
        "replace": '"headline": "x",',
    },
    {
        "name": "Check 269 (binary asset byte budget): tighten hero.webp budget to 1 byte (simulates over-budget)",
        "file": CHECK,
        "find": '(_HERO_WEBP269, 200_000, "hero.webp"),',
        "replace": '(_HERO_WEBP269, 1, "hero.webp"),',
    },
    {
        "name": "Check 270 (text asset byte budget): tighten style.css budget to 1 byte (simulates over-budget)",
        "file": CHECK,
        "find": '(ROOT / "style.css", 100_000, "style.css"),',
        "replace": '(ROOT / "style.css", 1, "style.css"),',
    },
    {
        "name": "Check 271 (root JS byte budget): tighten main.js budget to 1 byte (simulates over-budget)",
        "file": CHECK,
        "find": '(ROOT / "main.js", 100_000, "main.js"),',
        "replace": '(ROOT / "main.js", 1, "main.js"),',
    },
    {
        "name": "Check 272 (leaf module byte budget): tighten _LEAF_BUDGET272 to 1 byte (simulates over-budget)",
        "file": CHECK,
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
        "file": CHECK,
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
        "name": "Check 313 (aio-manifest date not future): push generated_at to 2099",
        "file": ROOT / ".well-known" / "aio-manifest.json",
        "find": '"generated_at": "2026-06-29T05:23:40Z",',
        "replace": '"generated_at": "2099-06-29T05:23:40Z",',
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
]

# ── Behavior e2e mutations (--e2e モード) ──────────────────────────────────────
# consistency Check の安全網 (上の MUTATIONS) と並ぶもう 1 つの安全網 = Playwright behavior e2e
# (BLOCKING gate playwright-validation) もまた「名乗るだけで実際は回帰を捕捉しない vacuous test」へ
# drift しうる (§7 教訓#10)。本リストは過去に修正した実 bug class を再現し、対応する behavior e2e が
# 確かに RED になる (= 捕捉する) ことを検証する。consistency mutation と違い gate は「その bug を守る
# 特定の e2e テスト」(`test` の -g パターン) で、各 mutation は (1) clean で pass・(2) mutated で fail
# の二段で非 vacuous を実証する。slow ゆえ on-demand (`npm run mutation-probe-e2e`)。
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
        "find": "State.updateSilently(s => { s.appsData.notes = val.slice(0, 20000); });",
        "replace": "State.update(s => { s.appsData.notes = val.slice(0, 20000); });",
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
        "file": ROOT / "js" / "apps.js",
        "find": "            const rt = State.get().appsData.pomodoro.runtime;\n            if (rt.isActive && rt.endAtMs) {",
        "replace": "            const rt = pomo.runtime;\n            if (rt.isActive && rt.endAtMs) {",
        "test": "Pomodoro completes at zero",
    },
]


def run_gate() -> int:
    """Run the consistency checker; return its exit code (0 = green)."""
    r = subprocess.run(
        [sys.executable, str(CHECK)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    return r.returncode


def run_e2e_test(pattern: str) -> int:
    """Run a single Playwright behavior test by -g pattern; return exit code (0 = pass/green)."""
    r = subprocess.run(
        ["npx", "playwright", "test", "--config=playwright.config.cjs", "-g", pattern],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    return r.returncode


def main() -> int:
    if not CHECK.exists():
        print(f"ERROR: gate not found: {CHECK}")
        return 1

    # baseline: gate は実行前に GREEN でなければ結果が無意味。
    if run_gate() != 0:
        print("ERROR: baseline gate is RED before any mutation — fix the repo first.")
        return 1

    survived: list[str] = []
    drifted: list[str] = []

    print(f"mutation-probe: applying {len(MUTATIONS)} curated mutations...\n")
    for m in MUTATIONS:
        f: Path = m["file"]
        original = f.read_text(encoding="utf-8")
        if m["find"] not in original:
            drifted.append(m["name"])
            print(f"  DRIFT  : {m['name']} — find-anchor absent (probe needs updating)")
            continue
        try:
            f.write_text(original.replace(m["find"], m["replace"], 1), encoding="utf-8")
            if run_gate() == 0:
                survived.append(m["name"])
                print(f"  SURVIVED: {m['name']}  <-- COVERAGE GAP")
            else:
                print(f"  caught  : {m['name']}")
        finally:
            f.write_text(original, encoding="utf-8")

    # 復元確認: 全 mutation 後に gate が GREEN へ戻ること (ファイルが汚れて残っていないこと)。
    if run_gate() != 0:
        print("\nERROR: gate is RED after restore — source files may be left mutated! Check `git status`.")
        return 1

    print()
    if drifted:
        print(f"{len(drifted)} mutation(s) DRIFTED (anchors missing) — update mutation_probe.py:")
        for d in drifted:
            print(f"  - {d}")
        return 1
    if survived:
        print(f"{len(survived)} mutation(s) SURVIVED — the safety net has a gap:")
        for s in survived:
            print(f"  - {s}")
        return 1
    print(f"All {len(MUTATIONS)} mutations were caught by the safety net. Net is healthy. ✓")
    return 0


def e2e_main() -> int:
    """--e2e モード: behavior e2e (Playwright) 安全網の非 vacuous 検証。

    各 mutation を (1) clean で対象テストが pass・(2) mutated で対象テストが fail (= 捕捉) の
    二段で検証する。clean-pass が「常に失敗する壊れたテスト」を、mutated-fail が「mutation を
    素通しする vacuous test」を、それぞれ排除する。slow ゆえ on-demand。
    """
    survived: list[str] = []
    drifted: list[str] = []
    broken: list[str] = []

    print(f"mutation-probe (e2e): verifying {len(E2E_MUTATIONS)} behavior mutations via Playwright...\n")
    for m in E2E_MUTATIONS:
        f: Path = m["file"]
        original = f.read_text(encoding="utf-8")
        if m["find"] not in original:
            drifted.append(m["name"])
            print(f"  DRIFT  : {m['name']} — find-anchor absent (probe needs updating)")
            continue
        # (1) clean baseline: 対象テストは現行ソースで pass しなければならない (壊れ/flaky 排除)。
        if run_e2e_test(m["test"]) != 0:
            broken.append(m["name"])
            print(f"  BROKEN : {m['name']} — target test '{m['test']}' is RED at baseline (fix/flaky?)")
            continue
        # (2) mutated: 対象テストが fail (= 捕捉) しなければ vacuous。
        try:
            f.write_text(original.replace(m["find"], m["replace"], 1), encoding="utf-8")
            if run_e2e_test(m["test"]) == 0:
                survived.append(m["name"])
                print(f"  SURVIVED: {m['name']}  <-- VACUOUS e2e (mutation 素通し)")
            else:
                print(f"  caught  : {m['name']}")
        finally:
            f.write_text(original, encoding="utf-8")

    print()
    if drifted:
        print(f"{len(drifted)} mutation(s) DRIFTED (anchors missing) — update mutation_probe.py:")
        for d in drifted:
            print(f"  - {d}")
        return 1
    if broken:
        print(f"{len(broken)} target test(s) RED at baseline — investigate before trusting the probe:")
        for b in broken:
            print(f"  - {b}")
        return 1
    if survived:
        print(f"{len(survived)} mutation(s) SURVIVED — the behavior e2e net has a vacuous gap:")
        for s in survived:
            print(f"  - {s}")
        return 1
    print(f"All {len(E2E_MUTATIONS)} behavior mutations were caught by the e2e net. Net is healthy. ✓")
    return 0


if __name__ == "__main__":
    sys.exit(e2e_main() if "--e2e" in sys.argv else main())

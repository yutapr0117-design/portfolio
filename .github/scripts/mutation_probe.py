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

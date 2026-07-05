"""
checks_e2e_infra.py — e2e / Playwright test-infrastructure hygiene checks
(extracted from check_repository_consistency.py — check.py split track・category "e2e/test-infra").

This module owns the (non-contiguous) cluster of Checks 110/111/114/116/117 that keep the
Playwright behavior-e2e harness sound: e2e A11Y_ROUTES ↔ ALL_ROUTES coverage bijection (110),
the no-`networkidle` wait guard (111), the no-`.only` guard (114), playwright.config
reuseExistingServer=false (116), and the screenshot tolerance sanity ceiling (117). They were
interleaved with 112 (IME guard・shipped-JS→checks_behavioral sibling) / 113 (canon discipline) /
115 (CSP・html-dependent), which stay in the monolith. Each Check reads its own target files
directly (e2e/*.spec.js, playwright.config.cjs) via Path.read_text(); none depends on the
monolith's global html/style/mainjs content. Executed together at Check 110's original position;
order-independent since each only appends to the shared errors/warnings (proven byte-identical
via full-output diff).

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT by reference (exec 不使用), so append
semantics / BLOCKING propagation / exit code are byte-equivalent to the monolith.

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  110. e2e A11Y_ROUTES ↔ ALL_ROUTES coverage bijection: the axe a11y test loops over A11Y_ROUTES
       asserting zero render-neutral critical violations per route; this Check asserts that
       A11Y_ROUTES's hash set equals ALL_ROUTES's hash set, so a route added to the route-render
       coverage (ALL_ROUTES) but forgotten in the a11y coverage (A11Y_ROUTES) is caught — no shipped
       route can silently escape automated accessibility scanning (the a11y counterpart of Check 58). (BLOCKING)
  111. e2e no-networkidle guard: e2e/portfolio.spec.js must not call
       waitForLoadState('networkidle') anywhere except inside the screenshot regression test
       (recognised by a toHaveScreenshot call within a few lines). networkidle waits for ALL
       network to settle, but the site loads external Google Fonts and a service-worker SWR
       background fetch, so on CI it can never reach idle and the wait hangs to the 30s test
       timeout (the hang flake fixed repo-wide in PR #132). Behavior tests must synchronise via
       'domcontentloaded' + expect() auto-wait instead; only the screenshot capture legitimately
       needs networkidle (font/image load determinism). This Check blocks reintroduction of the
       hang-flake class. (BLOCKING)
  114. e2e no-`.only` guard: e2e/portfolio.spec.js must contain no `test.only` /
       `describe.only` / `test.describe.only`. A stray `.only` makes Playwright run ONLY that
       test and silently skip every other test, so CI passes green while the suite is gutted
       (a false-green footgun, the inverse of the vacuous-gate class). This Check blocks any
       `.only(` left in the spec. (BLOCKING)
  116. playwright.config.cjs reuseExistingServer=false: the Playwright webServer must NOT
       reuse an existing server. If flipped to true, CI/local could test a stale already-running
       dev server (pre-edit state) and pass green while the committed files are broken — a
       false-green vector. This Check asserts `reuseExistingServer: false` and rejects `: true`. (BLOCKING)
  117. playwright.config.cjs screenshot tolerance sanity ceiling: `toHaveScreenshot`'s
       `maxDiffPixelRatio` must stay <= 0.05. Per Session Record #20 §3(B) the screenshot
       regression test is now ADVISORY (non-blocking observation), not the merge gate — but the
       tolerance ceiling still matters so the advisory OBSERVATION stays meaningful: loosening it
       (e.g. 0.5) would make the observation blind to real visual drift. This Check caps the
       tolerance so the visual-regression signal cannot be gutted by a config tweak. (BLOCKING)
"""
import re


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 110. e2e A11Y_ROUTES ↔ ALL_ROUTES coverage bijection (BLOCKING) ────────────
    # axe a11y テスト (A11Y_ROUTES でループ) は render-neutral critical 違反ゼロを全ルートで機械強制
    # するが、その対象集合 A11Y_ROUTES が手動配列ゆえ、新ルートを ALL_ROUTES (route-render が網羅) に
    # 足したのに A11Y_ROUTES へ足し忘れると「新ルートが a11y 未検証」の silent coverage gap が生じる。
    # 両配列の hash 集合が一致することを機械強制し、a11y カバレッジが shipped route 集合を常に追従する
    # ことを保証する (Check 58 の e2e↔main.js route 版の a11y 面)。
    _spec110 = ROOT / "e2e" / "portfolio.spec.js"
    if _spec110.exists():
        _src110 = _spec110.read_text(encoding="utf-8")
        _a11y_m110 = re.search(r"const A11Y_ROUTES\s*=\s*\[(.*?)\]", _src110, re.DOTALL)
        _all_m110 = re.search(r"const ALL_ROUTES\s*=\s*\[(.*?)\];", _src110, re.DOTALL)
        _a11y_set110 = set(re.findall(r"'([^']+)'", _a11y_m110.group(1))) if _a11y_m110 else set()
        _all_set110 = set(re.findall(r"hash:\s*'([^']+)'", _all_m110.group(1))) if _all_m110 else set()
        _only_all110 = sorted(_all_set110 - _a11y_set110)
        _only_a11y110 = sorted(_a11y_set110 - _all_set110)
        check(
            bool(_a11y_set110) and bool(_all_set110) and _a11y_set110 == _all_set110,
            f"Check 110: e2e A11Y_ROUTES ({len(_a11y_set110)}) covers exactly the ALL_ROUTES hash set ({len(_all_set110)}) — a11y axe runs on every shipped route",
            f"Check 110: a11y coverage drift — in ALL_ROUTES but missing from A11Y_ROUTES (a11y 未検証ルート): "
            f"{_only_all110}; in A11Y_ROUTES but not ALL_ROUTES: {_only_a11y110}. e2e の A11Y_ROUTES を同期せよ",
            blocking=True,
        )
    else:
        check(False, "", "Check 110: e2e/portfolio.spec.js not found — a11y coverage bijection を検証できない", blocking=True)

    # ── 111. e2e no-networkidle guard (BLOCKING) ──────────────────────────────────
    # `waitForLoadState('networkidle')` は全ネット通信が 500ms 落ち着くのを待つが、本サイトは外部
    # Google Fonts と service worker の SWR background fetch を持つため、CI のネット遅延窓では idle に
    # 到達せず 30s test-timeout までハングする (PR #132 で repo 全体を root-fix した hang flake クラス)。
    # behavior テストは 'domcontentloaded' + expect() の auto-wait で同期すべきで、networkidle が正当
    # なのは screenshot capture (フォント/画像ロードの決定化が必要) のみ。本 Check は screenshot テスト
    # 以外での networkidle 再導入を pre-commit でブロックし flake クラスの再発を構造的に封じる。
    # 許容判定: networkidle 行の直後数行以内に toHaveScreenshot があれば screenshot テスト内とみなす。
    _spec111 = ROOT / "e2e" / "portfolio.spec.js"
    if _spec111.exists():
        _lines111 = _spec111.read_text(encoding="utf-8").splitlines()
        _viol111 = []
        for _i111, _line111 in enumerate(_lines111):
            if "waitForLoadState('networkidle')" in _line111 or 'waitForLoadState("networkidle")' in _line111:
                _window111 = "\n".join(_lines111[_i111:_i111 + 6])
                if "toHaveScreenshot" not in _window111:
                    _viol111.append(_i111 + 1)
        check(
            not _viol111,
            "Check 111: e2e/portfolio.spec.js uses waitForLoadState('networkidle') only in the screenshot regression test",
            f"Check 111: e2e/portfolio.spec.js: waitForLoadState('networkidle') が screenshot テスト外の line {_viol111} に存在 — "
            f"'domcontentloaded' + expect() auto-wait を使え (networkidle は外部 Fonts/SW で CI hang する。PR #132 参照)",
            blocking=True,
        )
    else:
        check(False, "", "Check 111: e2e/portfolio.spec.js not found — networkidle guard を検証できない", blocking=True)

    # ── 114. e2e no-`.only` guard (BLOCKING) ──────────────────────────────────────
    # Playwright で test.only / describe.only が 1 つでも残ると、その test だけが走り他は全 skip され、
    # CI は緑のまま suite が空洞化する (false-green footgun = vacuous-gate の裏返し)。spec 内の
    # `(test|describe).only(` を検出して BLOCKING で禁止し、デバッグ用 .only の commit 漏れを封じる。
    _spec114 = ROOT / "e2e" / "portfolio.spec.js"
    if _spec114.exists():
        _src114 = _spec114.read_text(encoding="utf-8")
        _only114 = re.findall(r"\b(?:test|describe)(?:\.[A-Za-z]+)*\.only\s*\(", _src114)
        check(
            not _only114,
            "Check 114: e2e/portfolio.spec.js に test.only/describe.only が無い (false-green footgun 防止)",
            f"Check 114: e2e/portfolio.spec.js に .only が {len(_only114)} 個ある — 全 suite が skip され CI が false-green 化する。.only を除去せよ",
            blocking=True,
        )
    else:
        check(False, "", "Check 114: e2e/portfolio.spec.js not found — no-.only guard を検証できない", blocking=True)

    # ── 116. playwright.config.cjs reuseExistingServer=false (BLOCKING) ────────────
    # reuseExistingServer:true だと既に起動中の dev server を再利用し、commit 前の stale 状態を検証して
    # CI が緑になる false-green vector。`reuseExistingServer: false` の存在 + `: true` の不在を機械強制。
    _pwcfg = ROOT / "playwright.config.cjs"
    _pwsrc = _pwcfg.read_text(encoding="utf-8") if _pwcfg.exists() else ""
    if _pwcfg.exists():
        _reuse_ok = bool(re.search(r"reuseExistingServer\s*:\s*false\b", _pwsrc)) and \
            not re.search(r"reuseExistingServer\s*:\s*true\b", _pwsrc)
        check(
            _reuse_ok,
            "Check 116: playwright.config.cjs reuseExistingServer が false (stale-server false-green 防止)",
            "Check 116: playwright.config.cjs の reuseExistingServer が false でない — 既存 server 再利用で stale 状態を検証し false-green 化する。false に戻せ",
            blocking=True,
        )
    else:
        check(False, "", "Check 116: playwright.config.cjs not found — webServer 設定を検証できない", blocking=True)

    # ── 117. playwright.config.cjs screenshot tolerance sanity ceiling (BLOCKING) ──
    # maxDiffPixelRatio を緩めすぎると §3 baseline ゲートが本物の視覚 regression を見逃す。<=0.05 を強制。
    if _pwcfg.exists():
        _mdpr = re.search(r"maxDiffPixelRatio\s*:\s*([0-9.]+)", _pwsrc)
        _mdpr_val = float(_mdpr.group(1)) if _mdpr else None
        check(
            _mdpr_val is not None and _mdpr_val <= 0.05,
            f"Check 117: playwright.config.cjs maxDiffPixelRatio={_mdpr_val} <= 0.05 (§3 baseline 感度を維持)",
            f"Check 117: maxDiffPixelRatio={_mdpr_val} が sanity ceiling 0.05 を超過 (or 未設定) — 緩めると視覚 regression を見逃す。締め直せ",
            blocking=True,
        )
    else:
        check(False, "", "Check 117: playwright.config.cjs not found — screenshot tolerance を検証できない", blocking=True)

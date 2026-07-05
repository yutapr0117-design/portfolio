"""
checks_meta_validity.py — og/twitter meta non-empty + robots safety + .well-known JSON validity checks (341-343)
(extracted from check_repository_consistency.py — check.py split track).

run(ctx) receives shared check()/ROOT by reference (exec 不使用) so exit code / BLOCKING propagation
are byte-equivalent. annotation+def-aware free-var 分析で外部 `_`-var・global-content 依存ゼロ確認済。
nested-fn の module-level `global _accNNN` は run() 内で `nonlocal` へ機械変換 (意味等価)。

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  341. Every `<meta property="og:*">` / `<meta name="twitter:*">` tag in
       index.html MUST have a NON-EMPTY `content` value. Drift = an empty
       `content=""` (e.g. from a templating slip) silently breaks the
       specific social-card field — the card renders with a blank title /
       missing image / no description, and no gate catches it (Check 224–
       226 check length ranges but only for the specific tags they name;
       a blank content on any other og/twitter tag slips through).
       Sibling of Check 155 (og↔twitter title) / Check 336 (og↔twitter
       image) for the social-card field-presence axis. (BLOCKING)

  342. `robots.txt` MUST NOT contain a catastrophic block: no bare
       `Disallow: /` (whole-site block) and no `Disallow:` targeting the
       AIO-critical paths (`llms.txt`, `llms-full.txt`, `sitemap.xml`,
       `.well-known/`). The entire project is an AIO-first bet — its
       value depends on being maximally crawlable by AI/search agents. A
       stray whole-site or AIO-path Disallow would silently kill the
       strategy, and no behavior e2e / screenshot gate inspects robots.txt
       semantics. Sibling of Check 35 (Sitemap present) / Check 161
       (User-agent baseline) for the robots.txt crawl-permission
       integrity axis. (BLOCKING)

  343. EVERY `.well-known/**/*.json` file MUST parse as valid JSON. This
       is a comprehensive discovery-layer parse guard: individual checks
       (3=mcp.json, 254=index.json, 42=aio-manifest) parse specific files,
       but a NEW `.well-known` JSON file (or a growing agent-skills subdir)
       gets no parse coverage until someone writes a bespoke check. A JSON
       syntax error in any discovery file silently breaks agentic
       discovery for the AI agents that consume it. This Check auto-covers
       every current and future `.well-known` JSON. Sibling of Check 32
       (index.html JSON-LD parses) / Check 79 (.mcp.json parses) for the
       discovery-layer JSON-parse-integrity axis. (BLOCKING)

"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 341. All og:* / twitter:* meta content non-empty (BLOCKING) ──────────────
    _html341 = ROOT / "index.html"
    if _html341.is_file():
        _s341 = re.sub(r"<!--.*?-->", "", _html341.read_text(encoding="utf-8"),
                       flags=re.DOTALL)
        _empty341: list[str] = []
        _total341 = 0
        for _m in re.finditer(
                r'<meta\s+(?:property|name)="((?:og|twitter):[^"]+)"\s+content="([^"]*)"',
                _s341):
            _total341 += 1
            if not _m.group(2).strip():
                _empty341.append(_m.group(1))
        _ok341 = (not _empty341) and _total341 > 0
        check(
            _ok341,
            f"Check 341: og:* / twitter:* meta {_total341} 件すべて content 非空",
            (f"Check 341: 空 content の social meta: {_empty341!r} — "
             "空 content は該当 social-card field を silent 破壊 (blank title / "
             "missing image / no description)。実値を入れよ"),
            blocking=True,
        )
    else:
        check(False, "Check 341: index.html present",
              "Check 341: index.html が無い", blocking=True)

    # ── 342. robots.txt has no catastrophic Disallow (BLOCKING) ──────────────────
    _robots342 = ROOT / "robots.txt"
    if _robots342.is_file():
        _rt342 = _robots342.read_text(encoding="utf-8")
        _disallows342 = re.findall(r"(?mi)^\s*Disallow:\s*(\S*)\s*$", _rt342)
        _catastrophic342: list[str] = []
        _aio_critical342 = ("llms.txt", "llms-full.txt", "sitemap.xml", ".well-known")
        for _d in _disallows342:
            _d_stripped = _d.strip()
            # bare "/" = 全サイト block
            if _d_stripped == "/":
                _catastrophic342.append("Disallow: / (全サイト block)")
            # AIO-critical path を含む Disallow
            for _crit in _aio_critical342:
                if _crit in _d_stripped:
                    _catastrophic342.append(f"Disallow: {_d_stripped} (AIO-critical: {_crit})")
        _ok342 = not _catastrophic342
        check(
            _ok342,
            f"Check 342: robots.txt に破滅的 Disallow なし ({len(_disallows342)} 件の Disallow を検査)",
            (f"Check 342: robots.txt に破滅的 Disallow: {_catastrophic342!r} — "
             "AIO-first 戦略は最大 crawl 可能性が前提。全サイト or AIO-critical path の "
             "Disallow は戦略を silent に殺す。該当 Disallow 行を削除せよ"),
            blocking=True,
        )
    else:
        check(False, "Check 342: robots.txt present",
              "Check 342: robots.txt が無い", blocking=True)

    # ── 343. All .well-known/**/*.json parse as valid JSON (BLOCKING) ────────────
    _wk_dir343 = ROOT / ".well-known"
    if _wk_dir343.is_dir():
        _wk_jsons343 = sorted(_wk_dir343.rglob("*.json"))
        _bad_json343: list[str] = []
        for _jf in _wk_jsons343:
            try:
                json.loads(_jf.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError) as _e:
                _bad_json343.append(f"{_jf.relative_to(ROOT)}: {str(_e)[:50]}")
        _ok343 = (not _bad_json343) and len(_wk_jsons343) > 0
        check(
            _ok343,
            f"Check 343: .well-known/**/*.json {len(_wk_jsons343)} 件すべて valid JSON",
            (f"Check 343: .well-known JSON parse 失敗: {_bad_json343!r} — "
             "discovery-layer の JSON 構文エラーは AI agent の agentic discovery を "
             "silent に破壊。JSON 構文を修正せよ"),
            blocking=True,
        )
    else:
        check(False, "Check 343: .well-known/ present",
              "Check 343: .well-known/ ディレクトリが無い", blocking=True)

"""
checks_version.py — app-version cross-surface coherence checks (glob-content: html/ai2ai/mainjs/mcp_data)
(extracted from check_repository_consistency.py — check.py split track・category "version coherence"・ctx-enrich module).

Non-contiguous cluster of Checks 1/2/3/19 that hold the app version consistent across surfaces:
ai:version == AI2AI Pipeline-Version (1), main.js VERSION string (2), mcp.json server.version major
(3), sw.js CACHE_NAME app-version (19). They share `html_v` (the ai:version, extracted in Check 1 and
reused by 2/3/19) plus per-check `ai2ai_v` (1) / `mainjs_v` (2). Consume the pre-loaded
html/ai2ai/mainjs content + parsed mcp_data via ctx-enrichment (`_ctx.html/ai2ai/mainjs/mcp_data`).
Executed at Check 1's position in list order so `html_v` binds before its later consumers.

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT/html/ai2ai/mainjs/mcp_data/read/extract.

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  1.  ai:version (index.html) == Pipeline-Version (AI2AI.md)
  2.  ai:version == SITE_CONFIG.VERSION or main.js VERSION string
  3.  mcp.json server.version major matches ai:version
  19. sw.js CACHE_NAME version == ai:version
"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check
    html = ctx.html
    ai2ai = ctx.ai2ai
    mainjs = ctx.mainjs
    mcp_data = ctx.mcp_data
    read = ctx.read
    extract = ctx.extract

    # ── 1. ai:version == Pipeline-Version ────────────────────────────────────────
    html_v    = extract(r'name="ai:version"\s+content="(v\d+)"', html)
    ai2ai_v   = extract(r"Pipeline-Version\s*:\s*(v\d+)", ai2ai)
    check(
        html_v is not None and ai2ai_v is not None and html_v == ai2ai_v,
        f"ai:version ({html_v}) == Pipeline-Version ({ai2ai_v})",
        f"ai:version mismatch: index.html={html_v}, AI2AI.md={ai2ai_v}",
    )

    # ── 2. main.js VERSION string ────────────────────────────────────────────────
    mainjs_v = extract(r"VERSION:\s*['\"]?(v\d+)['\"]?", mainjs)
    if mainjs_v:
        check(
            html_v == mainjs_v,
            f"main.js VERSION ({mainjs_v}) == ai:version ({html_v})",
            f"main.js VERSION mismatch: main.js={mainjs_v}, index.html={html_v}",
        )

    # ── 3. mcp.json server.version major ─────────────────────────────────────────
    mcp_v     = mcp_data.get("server", {}).get("version", "")
    mcp_major = mcp_v.split(".")[0] if mcp_v else None
    html_major = html_v.lstrip("v") if html_v else None
    check(
        mcp_major is not None and mcp_major == html_major,
        f"mcp.json server.version major ({mcp_major}) == ai:version major ({html_major})",
        f"mcp.json server.version major ({mcp_major}) != ai:version major ({html_major})",
    )

    # ── 19. sw.js CACHE_NAME matches app version ──────────────────────────────────
    sw_js = read("sw.js")
    sw_cache = extract(r"CACHE_NAME = 'portfolio-aio-(v\d+)'" , sw_js)
    check(
        sw_cache is not None and html_v is not None and sw_cache == html_v,
        f"sw.js CACHE_NAME version ({sw_cache}) == ai:version ({html_v})",
        f"sw.js CACHE_NAME mismatch: sw.js={sw_cache}, index.html ai:version={html_v}",
    )

"""
checks_date_sync.py — date-sync coherence checks (17/18)
(extracted from check_repository_consistency.py — check.py split track・category "date sync"・
ctx-enrich module).

Contiguous cluster: Check 17 computes `html_date` which Check 18 consumes. Both checks are
extracted together to keep the shared variable in run()-local scope.
- ctx.html   (index.html content, pre-loaded by monolith)
- ctx.mainjs (main.js content, pre-loaded by monolith)
- ctx.ROOT   (repo root path for sitemap.xml parsing)
- ctx.check, ctx.warnings, ctx.extract

Executed at Check 17's original position in list order. Self-integrity: aggregated by
_aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105 span this file).

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  17. ai:last-modified (index.html) == SITE_CONFIG.LAST_UPDATED (main.js)
  18. sitemap.xml root <lastmod> == ai:last-modified (per-URL lastmod policy)
"""
import xml.etree.ElementTree as ET


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check
    html = ctx.html
    mainjs = ctx.mainjs
    extract = ctx.extract
    warnings = ctx.warnings

    # ── 17. Date sync: ai:last-modified == SITE_CONFIG.LAST_UPDATED ──────────────
    html_date = extract(r'name="ai:last-modified" content="([0-9-]+)"', html)
    mainjs_date = extract(r'LAST_UPDATED:\s+[\'"]([0-9-]+)[\'"]', mainjs)
    check(
        html_date is not None and mainjs_date is not None and html_date == mainjs_date,
        f"ai:last-modified ({html_date}) == SITE_CONFIG.LAST_UPDATED ({mainjs_date})",
        f"Date sync mismatch: index.html ai:last-modified={html_date}, main.js LAST_UPDATED={mainjs_date}",
    )

    # ── 18. sitemap.xml: root <lastmod> == ai:last-modified (per-URL policy) ──────
    # Policy (v74 maintenance finalizer):
    #   - Root URL (/): lastmod MUST match ai:last-modified / SITE_CONFIG.LAST_UPDATED
    #   - AIO document URLs: lastmod may reflect their own update date (honest per-URL)
    #   - Binary asset URLs: lastmod may follow asset baseline policy (intentional lag)
    #   - Mixed dates across the sitemap are ALLOWED and expected after AIO doc updates
    try:
        sitemap_tree = ET.parse(ROOT / "sitemap.xml")
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        CANONICAL_ROOT = "https://yutapr0117-design.github.io/portfolio/"
        root_lastmod: str | None = None
        for url_el in sitemap_tree.findall(".//sm:url", ns):
            loc_el = url_el.find("sm:loc", ns)
            lastmod_el = url_el.find("sm:lastmod", ns)
            if loc_el is not None and lastmod_el is not None:
                if loc_el.text and loc_el.text.rstrip("/") == CANONICAL_ROOT.rstrip("/"):
                    root_lastmod = lastmod_el.text
                    break
        if html_date and root_lastmod is not None:
            check(
                root_lastmod == html_date,
                f"sitemap.xml root <lastmod> ({root_lastmod}) == ai:last-modified ({html_date})",
                f"Date sync: sitemap.xml root lastmod={root_lastmod} vs ai:last-modified={html_date}",
            )
        elif html_date:
            warnings.append("sitemap.xml: root URL entry not found for per-URL lastmod check")
    except ET.ParseError:
        pass  # already caught in check 9

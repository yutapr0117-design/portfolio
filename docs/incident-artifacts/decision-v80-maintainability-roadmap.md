# Decision Record: v80 Maintainability & Extensibility Roadmap

```
Decision-ID    : decision-v80-maintainability-roadmap
Status         : Active
Created        : 2026-05-28
Author         : Yuta Yokoi (横井雄太) — orchestrator; implemented by Claude Sonnet 4.6
Baseline       : v74 maintenance finalizer
Next-Milestone : v80+
```

---

## Background

v74 maintenance finalizer completes the "土台の最後の歪み取り" phase.  
All CI checks pass, digest integrity holds, and known inconsistencies have been resolved.

The repository now enters a holding pattern before the next major update cycle (v80+),
focused on maintainability, extensibility, and AI implementation safety — not feature accumulation.

---

## Strategic Context

This portfolio deliberately prioritizes AIO (AI-Oriented Optimization) over conventional SEO.
Traditional SEO is a mature, competitive field where individual positioning offers diminishing returns.
AIO remains pre-standardized, with open room for individual proof-of-work and machine-readable
authority building. The v80 roadmap continues and deepens this strategy.

AIO monitoring log remains an **attempt log**, not a proof of successful AI citation.
`confirmed_citation_events: 0` is the honest current state. Future sessions should add entries
only on actual confirmed citations (manual observation or verified API response).

---

## Phase A — Already Completed (v74 maintenance finalizer)

- sitemap.xml per-URL lastmod policy (honest per-document update dates)
- aio-manifest.json archive role corrected (#1-#11)
- llms-full.txt C1–C7 constraint references unified
- README self-branding / proof-of-work purpose clarified
- check_repository_consistency.py: sitemap check updated to per-URL policy
- check_repository_consistency.py: archive session record count check added (check 26)
- check_repository_consistency.py: stale C1–C6 marker check added (check 27)

---

## Phase B — v80+ Major Update Direction

### Guiding Principles

```
1. Vanilla JS / static SPA / GitHub Pages / zero external framework — never changes
2. AI implementation safety: smaller change blast radius per session
3. Human PM (Yuta Yokoi) remains the sole architecture decision maker
4. AIO signal layers: deepen, do not dilute
5. Playwright visual regression baseline: prerequisite before any structural JS refactor
```

### main.js Staged Decomposition Plan

`main.js` is ~467 KB / ~7,781 lines. Current quality is high; CI and runtime are stable.
**Do not perform a bulk split.** The dependency graph (IIFE, ErrorBoundary, Router, EffectRails,
Storage, State, BindingRegistry, DiagnosticsRail) is dense. A hasty split breaks CSP and SPA routing.

Proceed stage-by-stage:

| Stage | Action | Gate |
|-------|--------|------|
| Stage 0 | Add explicit responsibility comments and a table of contents inside main.js. No physical split. | Now |
| Stage 1 | Extract `SITE_CONFIG`, `PAGE_META`, `QUIZ_DATA_MAP`, canonical constants to a data/config candidate. Verify CSP and GitHub Pages delivery are unaffected. | After Stage 0 review |
| Stage 2 | Extract pure utilities: `sanitize`, `format`, `validation`, `date`, `storage key helpers` (low side-effect). | After Stage 1 stable |
| Stage 3 | Extract service rails: `Storage`, `Store`, `State`, `RouteState`, `EffectRails`, `BindingRegistry`, `DiagnosticsRail`. | After Stage 2 stable |
| Stage 4 | Extract per-page render functions. Preserve ARIA, View Transition, ErrorBoundary. | After Stage 3 stable |
| Stage 5 | Physical file split after Playwright baseline is in place and all stages above are stable. | After baseline PNG committed |

### Playwright Baseline (prerequisite for Stage 5)

Status: **Not yet established.** Visual regression tests exist but are skip-guarded.

Human action required:
1. GitHub Actions → `update-playwright-snapshots.yml` → Run workflow
2. Download artifact `playwright-snapshots`
3. Place PNGs in `e2e/portfolio.spec.js-snapshots/`
4. Commit baseline

AI agents MUST NOT generate fake baseline PNGs.

### AIO Deepening

- Deepen `llms-full.txt` G-series guardrails as C7+ constraints are added
- Maintain `AI2AI.md` as the living AI-to-AI handoff document
- Add confirmed citation events to `aio-monitoring-log.json` only on actual evidence
- Consider structured `knowledge-graph.jsonld` extension if JSON-LD scope grows

### CI / Observability

- `check_repository_consistency.py` checks 26–27 now enforce archive count and C1–C7 currency
- Per-URL sitemap policy is now the standard; add new doc URLs with their own lastmod
- Digest pipeline (`update_aio_digests.py`) must be re-run after any AIO canonical file change

---

## Non-Goals for v80

```
- React / Vue / Tailwind / any external UI framework
- Bulk main.js split before Playwright baseline
- Binary WebP / MP3 re-encoding without metadata-only justification
- AIO monitoring success fabrication
- CodeQL custom workflow (.github/workflows/codeql.yml) resurrection
```

---

## Related Records

- `decision-v74-consistency-and-observability.md` — previous phase
- `decision-v78-codeql-default-setup-compatible-ci-recovery.md` — CI recovery
- `AI2AI.md` Session Records #12–#14 — execution history

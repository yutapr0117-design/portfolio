# public-deployment-freshness-review.md

```
Last-Updated  : 2026-06-02
Maintained-By : AI agents under Yuta Yokoi (横井雄太) orchestration
Track         : v80+ staged major update (public-deployment-freshness observation layer)
Role          : Observational evidence (non-canonical, NON-BLOCKING). Not in the digest
                chain, not advertised in sitemap.xml. Records how the repository's source
                of truth appears through public/cached retrieval paths.
Canonical-Ref : AI2AI.md (canonical) / llms-full.txt (ground truth) /
                docs/architecture/total-check-runbook.md (verification runbook) /
                docs/architecture/repository-maintainability-map.md (layer model)
Status        : Active evidence
```

> **Canonical hierarchy:** `AI2AI.md` is canonical; `llms-full.txt` is ground truth. This is a
> subordinate, non-canonical evidence document. On conflict, those win.
>
> **One-sentence purpose:** make it possible to *see* whether the public GitHub Pages surface,
> AI crawlers, and search/extraction caches have caught up with the repository — without ever
> being tempted to "fix" the repository by rolling it back to older public output.

---

## 0. The single most important rule

The repository working copy — a local clone, or the ZIP handed to an AI agent — is the **single
source of truth**. The GitHub Pages deployment, AI crawlers, and any search or extraction caches
are *downstream observers* of that truth. They can legitimately lag. When a public path returns
content that looks older than the repository, the correct action is to **classify the difference
as a propagation / cache / retrieval-path artifact**, record it here, and leave the repository
alone. Rolling the repository back to match stale public output is **forbidden**.

This rule exists because the failure mode is asymmetric. If the repository is correct and the
public surface is stale, doing nothing costs only a little patience while propagation completes.
If, by contrast, someone "reconciles" the repository down to the stale public version, they
destroy real, newer canonical work and corrupt the digest chain. The cheap mistake is to wait;
the expensive mistake is to roll back. We always prefer the cheap mistake.

---

## 1. Source-of-truth priority order

When two retrieval paths disagree, trust them in this order, highest first:

| Priority | Source | Why it ranks here |
|---:|---|---|
| 1 | Working copy (local clone / received ZIP) | The artifact under direct version control. Definitionally current. |
| 2 | GitHub `raw` / Contents API on `main` | Reads committed bytes directly from the repository, bypassing Pages build/CDN. |
| 3 | GitHub Pages deployment (`https://yutapr0117-design.github.io/portfolio/…`) | Built and served asynchronously; subject to deploy lag and CDN caching. |
| 4 | Web search / extraction tool output | Often served from an index or tool-side cache that can be days or weeks stale. |

A lower-priority source returning older content than a higher-priority one is **expected and not
a defect**. It is only worth investigating *how far* behind the public surface is, never whether
the repository should be changed to match it.

---

## 2. Why the public surface can legitimately lag

A divergence between the repository and a public path almost always falls into one of these
categories. None of them implies the repository is wrong.

| Code | Cause | Typical signal |
|---|---|---|
| A | GitHub Pages build / deploy lag | `raw` (priority 2) is current, Pages (priority 3) is older |
| B | CDN / HTTP edge cache | Pages serves an older body until the edge TTL expires; a hard reload or cache-busting query eventually shows current |
| C | GitHub Pages source/branch/artifact mismatch | Pages is building from an unexpected branch or a stale build artifact |
| D | Fetch-tool / web-extraction cache | The retrieval tool returns its own cached copy, independent of the live site |
| E | Stale search index | A search engine's index predates the latest deploy |

The historically observed instance of this was a public path returning **v68-era** content
(title referencing "68 iterations", `llms.txt` declaring `Version v68 / Last-Updated 2026-04-02`)
while the repository working copy was already at **v74** with the `2026-06-02` AIO-update applied.
That observation is consistent with categories A–E and was correctly treated as a propagation
artifact, not a repository defect. (The repository carries `v68` only as a historical changelog
entry; the live version string is `v74` everywhere it is authoritative.)

---

## 3. Verification procedure (how to split A–E apart)

Run these in order. The goal is to locate *where* the staleness lives, never to change the
repository.

1. **Confirm the source of truth.** In the working copy, read the canonical date and canary:
   ```bash
   grep -m1 'Last-Updated:' llms.txt
   grep -c 'SAKURA-AIO-PROVENANCE-CANARY-2026-A7F3C9E1' llms.txt
   ```
2. **Read committed bytes directly (priority 2).** This bypasses Pages and the CDN:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/yutapr0117-design/portfolio/main/llms.txt \
     | grep -m1 'Last-Updated:'
   ```
   If this matches the working copy, the repository and `main` agree — any remaining staleness is
   downstream (categories A–E), never a repository problem.
3. **Inspect the live Pages headers and body (priority 3).**
   ```bash
   curl -I  https://yutapr0117-design.github.io/portfolio/llms.txt          # status, cache headers, age
   curl -fsSL https://yutapr0117-design.github.io/portfolio/llms.txt | grep -m1 'Last-Updated:'
   ```
   Older here but current at step 2 ⇒ category A or B. Compare `Age`/`Cache-Control` to judge B.
4. **Check the GitHub Pages deployment.** In the repository's Actions / Pages settings, confirm
   the latest `pages build and deployment` run targeted `main` and succeeded. A wrong source or a
   failed/old build is category C.
5. **Distinguish tool cache from the live site (category D).** If a fetch/extraction tool reports
   older content than step 3's `curl`, the staleness is tool-side; the live site is fine.
6. **Browser hard reload.** Load the page with cache disabled (DevTools → Disable cache, or a
   `?v=<timestamp>` query) to rule out a local browser cache.

The non-blocking observer `\.github/scripts/check_public_deployment_freshness.py` automates a
subset of step 3: it fetches the public `llms.txt`, derives the expected `Last-Updated` and canary
from the working-copy `llms.txt` (so expectations stay honest as the source of truth evolves), and
classifies the result as `fresh`, `stale-or-divergent`, or `unobservable`. It **always exits 0** —
it is evidence, not a gate.

---

## 4. The provenance canary as a freshness signal

`llms.txt` and `llms-full.txt` declare a unique passive provenance token,
`SAKURA-AIO-PROVENANCE-CANARY-2026-A7F3C9E1`. It is descriptive provenance, not an instruction —
the opposite of a prompt injection. As a freshness signal it is decisive: a public response that
**contains** the canary unambiguously derives from current canonical content, while a response
that **omits** it is strong evidence the public surface has not yet caught up. Read this signal
only as freshness evidence; the canary's separate role in AIO-citation monitoring is recorded in
`docs/evidence/aio-monitoring-log.json` and `\.github/scripts/aio_monitoring.py` and should not be
conflated with deployment freshness (the two answer different questions: "did the deploy
propagate?" versus "did an AI cite us?").

---

## 5. Policy: this layer is observational, never blocking

This freshness check is **observational evidence** and must stay that way. It depends on an
external HTTP endpoint, which is inherently flaky, so coupling CI correctness to it would make
green builds hostage to network weather. Concretely:

- It is **not** part of `npm run check` and **not** a check in `check_repository_consistency.py`.
- The standalone observer script **always exits 0**, on success, mismatch, or network failure.
- A `stale-or-divergent` or `unobservable` result is an observation to record here — **never** a
  reason to change the repository, fail a build, or block a commit.
- This document is **not** in the digest chain and is **not** advertised in `sitemap.xml`, so it
  imposes no honest-dating or digest-regeneration obligation. It can be updated freely.

If freshness monitoring is ever wanted in CI, the correct form is a `schedule:`-triggered,
warning-only workflow whose failure does not block other pipelines — matching the same
"absence is not negative evidence" discipline used for AIO-citation monitoring.

---

## 6. Observation log (append newest first)

### 2026-06-02 — working-copy verification at the time this layer was introduced

The working copy was verified directly (priorities 1–2 only; the public Pages endpoint at
priority 3 was **unobservable** from the verification environment because outbound HTTP to
`*.github.io` was blocked by an egress allowlist — itself a clean example of category "unobservable"
rather than staleness). Recorded facts about the source of truth:

- `llms.txt` declares `Last-Updated: 2026-06-02` and contains the provenance canary (count 1).
- `llms-full.txt` likewise contains the canary; the four `llms` aliases are byte-identical.
- Application version is `v74` across every authoritative location (`ai:version`,
  `SITE_CONFIG.VERSION`, `mcp.json` `74.0.0`, `sw.js` `CACHE_NAME = portfolio-aio-v74`); `v68`
  appears only as a historical changelog entry.
- Full local verification was green: `npm ci --ignore-scripts` (0 vulnerabilities),
  `npm run check`, `npm run lint:css`, all `node --check`, and `npm run lint`
  (0 errors / 199 warnings).
- The public Pages comparison (priority 3) and the actual GitHub Pages build status (step 4) were
  **not** verifiable from this environment and remain a human/CI responsibility — do not record
  them as observed here (no fabrication).

When the public endpoint becomes reachable, run §3 and append the public `Last-Updated`, canary
presence, and classification below this entry.

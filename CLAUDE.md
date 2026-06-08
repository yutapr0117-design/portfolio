# CLAUDE.md

```
Document-Type    : Operational router for Claude Code (and chat-Claude)
Canonical-Source : AI2AI.md                  ← canon (constraints C1–C7, KERNEL, output rules, Session Records, v80+ track)
Ground-Truth     : llms-full.txt             ← authoritative project / entity facts
Canonical-Status : NON-CANONICAL / SUBORDINATE (on conflict, AI2AI.md / llms-full.txt win)
AIO-Status       : NOT part of the AIO discovery layer (dev-tooling only — see §8)
Last-Updated     : 2026-06-07
```

> **This file is the high-density router, not the canon.** You (Claude Code) can run `ls` / `cat` / `grep` / `wc` yourself, so this file deliberately carries **constraints, safety gates, routes, and a handoff** — **not** physical facts you can read in one tool call (line counts, file sizes, function names, dependency versions, which files exist). Do not re-state in prose what a tool gives you instantly; spend that budget on the task. When you need a number or a name, **read it with a tool** — it is intentionally not pinned here, because it drifts.

---

## 0. Read order — turn 1 (do this, then stop reading and start routing)

1. **This file** — constraints + gates + routes + the §7 handoff.
2. **`AI2AI.md`** — the canon. Full text of C1–C7, KERNEL roles, output rules, the latest Session Record, and the v80+ track live here. Read it before editing anything.
3. **`llms-full.txt`** — ground truth for any claim about the project, the entity (横井雄太 / Yuta Yokoi), or its history.

Do **not** bulk-`cat` the tree to "understand the repo." Use the §4 routing map to open only what the current task touches. Most tasks need ≤3 files beyond the three above.

---

## 1. What this repo is (one line)

AI-Driven PM portfolio: a **Vanilla HTML/CSS/JS static SPA on GitHub Pages, zero external frameworks/libraries in the shipped site**. It is a "PM-led AI-orchestration experiment" — the human (横井雄太) designs, reviews, audits, and governs; the AI implements (C5). Primary goal: machine-readable authority-building so AI crawlers / AI search / LLMs interpret and cite the entity correctly (an AIO-first bet).

---

## 2. Constraints C1–C7 (quick ref — canonical full text in `AI2AI.md` STEP 2)

Any output violating one of these is self-rejected before delivery.

- **C1 Boring Technology** — zero external frameworks / JS libraries in the shipped site (React/Vue/Svelte/Tailwind/Bootstrap/Framer Motion … all forbidden). Operational services (analytics/fonts) only with orchestrator approval + documented rationale.
- **C2 IIFE** — main logic lives inside IIFEs; no global-scope pollution (module-level ESM `import` may precede the IIFE; see Check 43d).
- **C3 ErrorBoundary** — View Transition API errors handled by an explicit error boundary; graceful degradation required.
- **C4 No Framework Re-proposal** — frameworks are permanently rejected; never re-propose any.
- **C5 Human Writes Zero Code** — the human writes design + prompts only; all implementation code is AI-generated.
- **C6 AIO Integrity** — the **text** of `llms-full.txt` / `llms.txt` / `llms_well-known.txt` / `.well-known/*` / JSON-LD / binary metadata (XMP·ID3) must **not** change without the orchestrator's explicit written approval. (Tool-enforced: editing the published AIO layer is gated to `ask` in `.claude/settings.json`.)
- **C7 KARTE CDN SRI Non-Application** — do not propose SRI on KARTE CDN (external updates would break prod load; connections are restricted by CSP instead).

**Reject-on-sight anti-patterns:** removing IIFE/ErrorBoundary; generalizing/neutralizing entity statements in `llms-full.txt`/JSON-LD; attributing design decisions to the AI; describing this project as "Vibe Coding" or "an AI-generated site" (correct framing: "PM-led AI-orchestration experiment").

---

## 3. Hard "don't" — safety gates (these cause real damage; verify catches some, not all)

- Introduce a framework/library or re-propose one (C1/C4).
- Edit the AIO text (C6) without orchestrator approval.
- Attribute design/intent to the AI. Judgement, goal-definition, priority, and responsibility are always **横井雄太**'s.
- Move `docs/incident-artifacts/update-portfolio.v70-experiment.yml` back under `.github/workflows/` (it carries a `workflow_dispatch` trigger — relocating it makes a manually-runnable live workflow).
- **Physically split `main.js` (Stage 5: kernel/render/router/view-transition) before the Playwright visual-regression baseline exists.** The baseline is the gate; it cannot be generated in a sandbox (Chromium download is blocked) — only via GitHub Actions `update-playwright-snapshots.yml` dispatch → PR → human merge.
- Finalize a version-number / digest bump without orchestrator approval. When approved, apply `AI2AI.md`'s "Version Update Checklist" **atomically** across every listed file (partial bumps break consistency).
- Touch the DO-NOT-EDIT AIDK kernel region or the protected blocks inside `main.js` (kernel / AIDK modules / known-benign suppressor / innerHTML interceptor). Keep them byte-identical; `npm run verify` Check 43 catches structural damage, but treat them as frozen.

---

## 4. Routing map — where things live (open only what the task needs)

| Need | Read |
| :-- | :-- |
| Canon: C1–C7 full text, KERNEL roles, output rules, Session Records, v80+ track | `AI2AI.md` |
| Ground truth: entity, project history, AIO declarations | `llms-full.txt` (alias `llms.txt`, `.well-known/llms.txt`) |
| What each consistency check guards + how to add one | `docs/architecture/check-repository-consistency-map.md`; the script's own docstring is the inventory → `.github/scripts/check_repository_consistency.py` |
| Verification runbook (layers, expected outputs, measured baselines) | `docs/architecture/total-check-runbook.md` (§9 = the authoritative measured numbers) |
| `main.js` decomposition plan + stage gates | `docs/architecture/main-js-extraction-map.md` |
| Maintainability map + per-increment changelog | `docs/architecture/repository-maintainability-map.md` |
| File-size budgets (machine-readable BUDGET-DATA, Check 52) | `docs/architecture/file-size-budget.md` |
| Major-update / Playwright baseline procedure | `docs/architecture/major-update-readiness.md` |
| Research discipline (apply / defer-with-reason / verify-currency) | `docs/architecture/research-application-policy.md` |
| Per-increment Claude notes (newest = current state of play) | `docs/incident-artifacts/improvement-notes-*.md` |
| Decision records (why a path was taken) | `docs/incident-artifacts/decision-*.md` |
| Claude↔Claude session handoff + bash procedures | `Claude2Claude.md` |
| Exact numbers (check count, `main.js` lines, dep versions, which files exist) | **a tool** — `wc -l`, `grep`, `ls`, `cat package.json`. Not here. |

---

## 5. The loop — verify, increment, deliver, research

- **Verify (always before delivery):** `npm run verify` must exit 0. It chains `check` (consistency + AIO digests + binary metadata) → `lint:css` → `lint` (ESLint) → `lint:js` (`node --check`). For the breakdown and the authoritative measured numbers, read `total-check-runbook.md` §9 — do not memorize them here.
- **Increment discipline:** discover → document → **systematize (machine-enforced Check)** → verify → deliver. A newly discovered invariant is not "fixed" until it is a BLOCKING/ADVISORY Check in `check_repository_consistency.py` **and** its docstring inventory + `# ── N.` section header + implementation are all updated (Check 45 enforces that bijection) **and** the canonical docs that cite affected numbers are synced.
- **Deliver (every increment — stopping short is a failure):** (1) complete changed-file blocks; (2) **alphabetical repository-relative paths in the chat body** (not only an appendix); (3) commit command using **explicit `git add <paths>` — never `git add .`** (tool-enforced: `git add .` / `-A` / `--all` are denied in settings); (4) a summary of decisions and reasoning.
- **Research discipline:** research is required for improvement and **"isn't finished until it is applied."** Never ask "should I research?"; never stop at confirmation. Every finding lands as **apply**, **defer-with-reason** (safety gate / standard-not-final / strategy-mismatch only), or **verify-currency**. Full policy: `research-application-policy.md`.
- **Language:** respond in **Japanese** (also set via `language` in settings). A Japanese-initiated thread stays Japanese end-to-end, including explanations and tool prompts.

---

## 6. Reasoning budget — dynamic by task difficulty

Extended thinking is **enabled by default** (Claude Code, since 2026-01) and `.claude/settings.json` pins the ceiling to the documented maximum (`MAX_THINKING_TOKENS = 31999`). `budget_tokens` is a **ceiling, not a fixed spend** — so reasoning scales automatically: a one-line/format edit costs a few hundred reasoning tokens, a multi-file or architectural change can use up to ~31999. **Spend proportionally** — do not burn maximum reasoning on a trivial edit, and do not under-reason a refactor, an extraction, or anything touching the kernel / AIO / version bump. (The old `think` / `ultrathink` keyword ladder is deprecated; proportionality now comes from your own judgement under the ceiling.)

---

## 7. Handoff — current state of play (turn-1 catch-up; strategic, not the kind of fact you `cat`)

- **Pipeline-Version `v74`**; **`v80+` is the active update-track name, not an app version.** The foundation-correction phase is done; the current phase is maintainability / extensibility / AI-implementation-safety.
- **Latest increment = `console-fix + eslint-v10 + research-application`.** It: fixed a live console **404** (a dangling `modulepreload` to `js/quiz-data.js` left behind by the earlier quiz-domain split); fixed a **Wicle CSP** violation (added `https://cdn.wicle.io` to `connect-src` for KARTE Action); **migrated ESLint 9 → 10** (flat config, behaviour-identical lint output, proven non-destructive); added **Check 53** (every `index.html` modulepreload href must resolve) and **Check 54** (`eslint` ↔ `@eslint/js` major must match); created **`research-application-policy.md`**; and rebuilt this `CLAUDE.md` + added `.claude/` for the Claude Code migration. (Exact check count / line counts / versions: read them with tools.)
- **Next gate (blocking Stage 5):** the **Playwright visual-regression baseline is not yet acquired.** Until it exists, do not physically split the `main.js` kernel/render/router. Acquisition route is the only valid one: GitHub Actions `update-playwright-snapshots.yml` **dispatch → PR → human merge** (local/sandbox Chromium download is blocked). Preparation (workflow, procedure) is complete; only the authorize-and-merge step remains. See `major-update-readiness.md`.
- **Deferred-with-reason backlog (do not "rediscover" as new):** WCAG 2.2 / Core Web Vitals CSS fixes — **baseline-gated** (CSS/render changes can't be proven non-regressive without the baseline). IETF AIPREF `Content-Usage` — **not adopted by design**: `robots.txt` intentionally permits AI training ("public experiment intended to be learned from by AI models"), so a usage-restriction mechanism contradicts the strategy. Rationale for both: `research-application-policy.md` §3C.
- **AIO posture:** `confirmed_citation_events = 0` is **by design** — an early position on a high-probability lane, not a gamble and not a failure. Never fabricate citations; never frame the AIO-over-SEO choice as a "bet/gamble".
- **Non-destructive discipline holds:** the AIO published layer, binary assets, `style.css`, and `main.js` are kept byte-identical unless an increment's stated purpose is to change them (then with C6 approval + digest regeneration). Prove invariance with SHA-256 against the prior state.

---

## 8. Design note — why CLAUDE.md is not in the AIO layer

`CLAUDE.md` is **dev-tooling orientation**, deliberately **excluded from the AIO discovery layer** (not registered in `sitemap.xml` / `robots.txt` / `aio-manifest.json`; no digest). It is an entry point for implementing agents, not an authority signal for AI crawlers — keeping it out of the AIO surface keeps that surface clean and avoids C6 entanglement. `CLAUDE.md` (router), `Claude2Claude.md` (bash procedures + Claude↔Claude evidence), and `AI2AI.md` (canon: full constraints / KERNEL / Session history) are role-separated and must not duplicate each other; always defer to the higher document for detail.

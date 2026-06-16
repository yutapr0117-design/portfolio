# CLAUDE.md

```
Document-Type    : Operational router for Claude Code (and chat-Claude)
Canonical-Source : AI2AI.md                  ← canon (constraints C1–C7, KERNEL, output rules, Session Records, v80+ track)
Ground-Truth     : llms-full.txt             ← authoritative project / entity facts
Canonical-Status : NON-CANONICAL / SUBORDINATE (on conflict, AI2AI.md / llms-full.txt win)
AIO-Status       : NOT part of the AIO discovery layer (dev-tooling only — see §8)
Last-Updated     : 2026-06-15
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

### Entity canonical facts (for Claude Code / sub-agents / human reviewer cold-start)

- **Entity Name**: `Yuta Yokoi` / `横井雄太` / `Yokoi Yuta` (UI display: `yuta`, all lowercase)
- **Role**: AI-Driven PM / IT Consultant / KERNEL Framework Designer
- **Canonical URL**: `https://yutapr0117-design.github.io/portfolio/`
- **Authoritative Context**: `https://yutapr0117-design.github.io/portfolio/llms-full.txt`
- **Affiliation**: 株式会社日本経営 (Nihon Keiei / Japan Management Co., Ltd.) — シェアデータベース事業部 主幹（課長格）, 2026-06-11〜. Org canonical URL: `https://nkgr.co.jp/`
- **Architecture**: Boring Technology (Vanilla JS SPA, IIFE, ErrorBoundary)
- **AIO canary token namespace**: `SAKURA-AIO-PROVENANCE-CANARY-<YYYY>-<8hex>` (single canonical value across all published surfaces and monitors — Check 44)
- **Disambiguation**: STRICTLY DISTINCT from academic researchers (agriculture / chemistry / medicine / entomology / computer science), diplomats, artists, musicians, patent inventors.

---

## 2. Constraints C1–C7 (quick ref — canonical full text in `AI2AI.md` STEP 2)

Any output violating one of these is self-rejected before delivery.

- **C1 Boring Technology** — zero external frameworks / JS libraries in the shipped site (React/Vue/Svelte/Tailwind/Bootstrap/Framer Motion … all forbidden). Operational services (analytics/fonts) only with orchestrator approval + documented rationale.
- **C2 IIFE** — main logic lives inside IIFEs; no global-scope pollution (module-level ESM `import` may precede the IIFE; see Check 43d).
- **C3 ErrorBoundary** — View Transition API errors handled by an explicit error boundary; graceful degradation required.
- **C4 No Framework Re-proposal** — frameworks are permanently rejected; never re-propose any.
- **C5 Human Writes Zero Code** — the human writes design + prompts only; all implementation code is AI-generated.
- **C6 AIO Integrity** — the **semantic content** of `llms-full.txt` / `llms.txt` / `llms_well-known.txt` / `.well-known/*` / JSON-LD / binary metadata (XMP·ID3) must **not** change without the orchestrator's explicit written approval. (Tool-enforced: editing the published AIO layer is gated to `ask` in `.claude/settings.json`.)
  - **Exception — derived-value auto-update (A1 案)**: 日付フィールド (`xmp:ModifyDate` / `xmp:MetadataDate` / MP3 TXXX `AIO:MetadataLastModified` / aio-manifest.json `generated_at` / `last_metadata_update`) は、対応する semantic 編集が承認された結果として **自動同期更新可**。単独の意味的編集ではなく "derived value" (派生値) として扱う。
  - **Exception 拡張 — content-derived value 全般 (A2 案)**: 上記の日付に加え、sha256 digest (aio-manifest.json `source_of_truth[].sha256` / `supporting_evidence[].sha256` / `observational_evidence[].sha256` / `.well-known/index.json` `skills[].digest`) も同じ扱いで自動同期更新可。これらは binary / text の content から機械的に計算される値であり、独立した semantic 編集ではないため C6 の対象外。
  - 自動更新の trigger: `update_aio_digests.py` (B1 案) / `update_binary_aio_organization.py` (B2 案) など、binary または text の semantic 編集を伴う tool が必ず呼ぶ。手動編集経路では Check 91 (C 案) が「binary 変更 commit には日付フィールド更新必須」を pre-commit で機械強制する。
- **C7 KARTE CDN SRI Non-Application** — do not propose SRI on KARTE CDN (external updates would break prod load; connections are restricted by CSP instead).

**Reject-on-sight anti-patterns:** removing IIFE/ErrorBoundary; generalizing/neutralizing entity statements in `llms-full.txt`/JSON-LD; attributing design decisions to the AI; describing this project as "Vibe Coding" or "an AI-generated site" (correct framing: "PM-led AI-orchestration experiment").

---

## 3. Hard "don't" — safety gates (these cause real damage; verify catches some, not all)

- Introduce a framework/library or re-propose one (C1/C4).
- Edit the AIO text (C6) without orchestrator approval.
- Attribute design/intent to the AI. Judgement, goal-definition, priority, and responsibility are always **横井雄太**'s.
- Move `docs/incident-artifacts/update-portfolio.v70-experiment.yml` back under `.github/workflows/` (it carries a `workflow_dispatch` trigger — relocating it makes a manually-runnable live workflow).
- **Physically split `main.js` kernel / render / view-transition surfaces — the remaining Stage 5 high-risk targets — without verifying both `closure-deps = none` AND that the Playwright visual-regression baseline stays green on the resulting structure.** The baseline gate was acquired on 2026-06-10 (PR #13), unlocking Stage 5 procedurally; Router + PAGE_META (PR #16) and ページコンポーネント (PR #18) have already been extracted under this gate. But the gate's *purpose* still holds: any further change to the renderer, kernel, view-transition, or AIDK-adjacent surfaces must be proven non-regressive against the baseline before merge — that is exactly what the baseline buys. A new baseline (if needed for legitimate visual changes) can only be generated via the GitHub Actions `update-playwright-snapshots.yml` dispatch → PR → human merge path (Chromium download is blocked in sandbox).
- Finalize a version-number / digest bump without orchestrator approval. When approved, apply `AI2AI.md`'s "Version Update Checklist" **atomically** across every listed file (partial bumps break consistency).
- **(C 案 規範) Binary metadata semantic 編集 (Organization / Entity / Canary 等の追加・変更) は、必ず同一 commit で日付フィールド (`xmp:ModifyDate` / `xmp:MetadataDate` / MP3 TXXX `AIO:MetadataLastModified`) も同期更新する。** 標準経路は `update_binary_aio_organization.py` (B2 案) または `update_aio_digests.py` (B1 案) を使用する — どちらも `_lib_io.now_iso8601()` + `update_webp_xmp_dates()` + `update_mp3_metadata_date()` の helper を経由する。手動経路で binary を編集する場合は同 commit 内で日付更新を含めること。Check 91 がこれを pre-commit で機械強制 (BLOCKING)。
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

- **核心運用ポリシー（Operating Model — AI Self-Driving / Human Control-and-Audit-Only）**: 実装→検証→マージ→本番デプロイの全工程を **AI が自走** する。人間（横井雄太）の runtime 役割は **制御（goal/priority 提示）と監査（CI オールグリーン確認）「のみ」**。「**既存非破壊 かつ CI オールグリーン**」なら AI は確認なしで `merge`/`push`/デプロイまで完遂し、緑でなければ根本修正してから進める。**AI 献策 / 人間裁可（AI proposes, human disposes）**: 次に何をやるかの提案は AI 自走の中核機能（受動的指示待ちは「監査のみ」運用を壊す）。提案からの選択（goal/priority 確定）は人間が裁可する。**改善に「完了」状態は存在しない（No terminal "done" state）**: AI は「もう十分」「一区切りが妥当」式の自発停止・完了宣言をしてはならず、唯一の正当な停止は人間の明示的停止指示のみ。成熟リポジトリでも genuine な改善（深い invariant 機械強制 / WHY コメント実在ギャップ / CI カバレッジの穴 / research 適用 / 実態↔記述 drift 是正）は探せば必ずあり、「非破壊 ∧ CI 緑」を床に load-bearing な増分を出し続ける（padding は依然禁止＝「足さない」は『改善をやめる』でなく『別の genuine 改善を選ぶ』）。canon は `AI2AI.md` STEP 3「Operating Model」（Check 102a/b/c/d が presence を BLOCKING 強制）。越えない境界: AI による `.claude/settings.json` 自己権限拡張は不可（人間が編集→**次セッションで有効化**。settings は session 開始時キャッシュのため mid-session 反映なし）／§3 baseline ゲート／C1〜C7／force-push・rm -rf deny。

- **Pipeline-Version `v74`**; **`v80+` is the active update-track name, not an app version.** The foundation-correction phase is done; the current phase is maintainability / extensibility / AI-implementation-safety.
- **Stage 5 物理分割 = 最終完遂 (2026-06-10〜12)。`main.js` は 7,785 → **1,086 行 (−86%)** に縮小。** 16 個の小さな増分 (Stage 5-c〜5-s + 5-l + 5-q + 5-r) を factory pattern を確立しながら段階的に実施し、24 個の葉モジュール (`js/aidk-rails.js` / `apps.js` / `brand.js` / `components.js` / `constants.js` / `fatal-overlay.js` / `identity.js` / `meta-management.js` / `mobile-drawer.js` / `page-meta.js` / `pages.js` / `perf-guards.js` / `pure-utils.js` / `quiz-renderer.js` / `quiz/*` × 4 / `router.js` / `state.js` / `storage.js` / `store.js` / `theme.js` / `ui-components.js`) に分割した。最後の 3 増分 (Stage 5-q Mobile Drawer / 5-r Fatal Overlay / 5-s Perf Guards) では late-binding holder pattern と dual-binding factory return で「kernel 周辺の非保護領域」も丁寧に抽出した。詳細な増分一覧と PR # は `docs/architecture/repository-maintainability-map.md` の "Stage 5-c〜5-o + 5-l" と "Stage 5-q + 5-r + 5-s" セクション、factory pattern 確立の経緯は `docs/architecture/main-js-extraction-map.md` §3.10〜§3.11 を参照。
- **CI 多層化（Stage 5-k）= 完了。** Check 55（ESLint glob vacuous-gate 防止 BLOCKING）・Check 56（factory invocation orphan 防止 BLOCKING）・e2e 全 17 ルート訪問テスト・Check 33 scope 拡張（`main.js ∪ js/components.js` 統合面で Zenn slug 検証）を導入し、Stage 5-b で発生した「直下 `js/<file>.js` の silent skip」と Stage 5-j で発見した「隠れ ReferenceError」class を構造的に閉じた。
- **AIDK Isolated Kernel と View Transition Proxy は最終的に un-extractable で main.js に残置（意図的温存）。** Check 43 が構造健全性を BLOCKING で機械強制している不可侵領域。残る `main.js` 1,086 行は AIDK Kernel proper + startViewTransitionProxy (Check 43b) + Trusted Types policy (Check 43c) + single top-level IIFE (Check 43d) + view-transition / render core (`executeSafeTransition / render / _renderCore`) + SITE_CONFIG (Check 2/17 が grep) + protected blocks (`_installEventListenerRegistry / _installInnerHTMLSanitizer`) + init / WebMCP + 各 factory の合成呼び出しで構成される。これらは Check 43 / Check 2/17 / CLAUDE.md §3 で多層的に保護されており、「最終的に温存する」は妥協ではなく機械強制された安全契約に従った honest な記録である。
- **Deferred-with-reason backlog (do not "rediscover" as new):** WCAG 2.2 / Core Web Vitals CSS fixes — **baseline-gated** (CSS/render changes can't be proven non-regressive without the baseline). IETF AIPREF `Content-Usage` — **not adopted by design**: `robots.txt` intentionally permits AI training ("public experiment intended to be learned from by AI models"), so a usage-restriction mechanism contradicts the strategy. Rationale for both: `research-application-policy.md` §3C.
- **AIO posture:** `confirmed_citation_events = 0` is **by design** — an early position on a high-probability lane, not a gamble and not a failure. Never fabricate citations; never frame the AIO-over-SEO choice as a "bet/gamble".
- **Non-destructive discipline holds:** the AIO published layer, binary assets, `style.css`, and `main.js` are kept byte-identical unless an increment's stated purpose is to change them (then with C6 approval + digest regeneration). Prove invariance with SHA-256 against the prior state.
- **Check 総数は §9 を単一権威とする規模まで継続成長 (2026-06-15 以降も増加中・正値は `docs/architecture/total-check-runbook.md` §9 / Check 70 強制)。** Stage 5 完遂後、10 連 increment で機械強制を 3 倍以上に拡張:
  - 「CI 更なる手厚化 v1/v2」 (PR #45/#46) → Check 57〜71 追加。modulepreload / e2e routes / file-size-budget §2 ↔ §4 集合一致・AIO entity canonical_url 整合・workflow permissions 明示など、Stage 5 後の真の抜け漏れを 0 化。
  - 「All Plans Combined」 (PR #47) → Check 72〜75 追加。ESLint 絶対防衛線 (Plan A) / preload-as・img-alt・hero-fetchpriority HTML 属性契約 (Plan B) / `_lib_io.py` helper 抽出 + 4 関数 API 契約 (Plan C) / `docs/incident-artifacts/README.md` inventory governance (Plan D) を 1 PR で統合。
  - 「Repo-wide & Claude Code files」 (PR #48) → Check 76〜80 追加。`.claude/settings.json` security baseline / `.claude/commands/*.md` frontmatter / `.claude/agents/*.md` frontmatter (`repo-auditor` / `check-author` / `aio-guardian` の 3 sub-agent 新設) / `.mcp.json` JSON parsability / `.claude/skills/*/SKILL.md` frontmatter を機械強制化。`/audit` `/increment` `/sync-docs` の 3 新規 slash command と `repo-status` skill も新設。
  - 「All-files AIO coherence」 (PR #49) → Check 81〜85 追加。WebP XMP / MP3 ID3 / aio-manifest / README / Claude2Claude に Organization (株式会社日本経営) 情報を cross-surface 反映。
  - 「Full coherence audit」 (PR #50/#51) → Check 86〜90 追加。aio-manifest entity 9 field / CLAUDE.md+Claude2Claude.md cold-start 3 fact / LICENSE 4 fact / 3 governance file 存在 + entity / .claude/CLAUDE.md+.claude/README.md entity context。LICENSE / CONTRIBUTING / CODEOWNERS / CHANGELOG / .claude/CLAUDE.md 新設。
  - 「C6 derived-value 例外」 (PR #52) → Check 91〜95 追加。10 案統合実装 (A1+A2 canon 改定 / B1+B2 tool 日付同期 / C 規範+Check / 6 helper 統一 / 7 WebP xmp:MetadataDate / 8 manifest last_metadata_update / 9-10 多軸日付整合)。WebP / MP3 binary 内日付フィールドを semantic 編集の derived value として自動同期可と canon 化。
  - 「Docs 7 Phase」 (PR #53〜#56) → Check 96〜99 追加。リポジトリ全 137 ファイルに対し `docs/files/<path>.md` ミラー構造で 1 対 1 ドキュメント完備 (multi-audience: AI/人間新卒/監査人/採用担当/学術研究者/第三者全般)。5+1 セクション (What/Why/How/Constraints/Change impact/Audience-specific notes) を全 doc に強制。
  - 「Final audit」 (PR #57) → Check 96 を 133→137 件に拡張。grep ベース監査で発見した 4 漏れ (.well-known/api-catalog / jsconfig.json / docs/evidence/aio-monitoring-log.json / e2e/portfolio.spec.js-snapshots/homepage-baseline-chromium-linux.png) を補完し、137=137=137 の 3 集合 bijection 完成。
  - 「why-only コメント注入」 (handoff §10 実行) → Check 100 追加。shipped JS/HTML レイヤーは前任で既に WHY 完備のため genuine gap のみ注入 (main.js kernel の「なぜ DO NOT EDIT か」+ Check 43a-d アンカー / theme-init.js の隠れた storage-key 複製 invariant / karte-init stub / index.html CSP 各ディレクティブ / playwright baseline magic number)。過程で発見した未強制 invariant を Check 100 (theme-init.js のハードコードキー ↔ js/constants.js STORAGE_KEY / js/brand.js KEY 一致 / 100a・100b BLOCKING) へ systematize。3 集合 bijection は handoff/本 increment の improvement-notes 追加で 139=139=139。**重要な honest finding: 既存コードへの盲目的コメント追加は §5.2 drift 製造になるため避けること。** さらに後続「全 plan 好いとこ取り」increment で: (a) node+chromium 導入し e2e behavior 34 件をローカル実測 pass、(b) WCAG 2.2 の唯一の genuine gap = forced-colors (Windows HCM) focus fallback を style.css に **render-neutral** に追加 (forced-colors スコープ内ゆえ通常描画=CI baseline 不変・§3 ゲート非該当) し Check 101 (BLOCKING) で機械強制、(c) `--update-snapshots` のローカル baseline 生成は §3 ゲートが正しくブロック→尊重。詳細は improvement-notes-claude-v80-phase2-why-only-comment-injection.md。
- **Claude Code 用ファイル一式が揃った + 全ファイル 1-to-1 docs が機械強制 (2026-06-14)。** 後続セッションは次の順に読めば cold-start で復帰可能: (1) 本 CLAUDE.md §7、(2) `AI2AI.md` の最新 Session Record、(3) `docs/architecture/total-check-runbook.md` §9 (consistency Check 総数の**真値**。数値はここを参照し、本 §7 の数値が drift した場合も §9 を正とする)、(4) 個別ファイルの doc は `docs/files/<path>.md` で 1 対 1 で読める。深い drift 監査が必要なら `/audit` を起動 (`repo-auditor` sub-agent が読み取り専用で 6 dimension をチェック)。Check 追加が必要なら `/increment` → `check-author` sub-agent。AIO 編集が必要なら必ず `aio-guardian` sub-agent を経由する (C6 enforcement)。

---

## 8. Design note — why CLAUDE.md is not in the AIO layer

`CLAUDE.md` is **dev-tooling orientation**, deliberately **excluded from the AIO discovery layer** (not registered in `sitemap.xml` / `robots.txt` / `aio-manifest.json`; no digest). It is an entry point for implementing agents, not an authority signal for AI crawlers — keeping it out of the AIO surface keeps that surface clean and avoids C6 entanglement. `CLAUDE.md` (router), `Claude2Claude.md` (bash procedures + Claude↔Claude evidence), and `AI2AI.md` (canon: full constraints / KERNEL / Session history) are role-separated and must not duplicate each other; always defer to the higher document for detail.

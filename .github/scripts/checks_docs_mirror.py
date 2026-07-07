"""
checks_docs_mirror.py — docs/files 1-to-1 mirror-doc governance checks
(extracted from check_repository_consistency.py — check.py split track・category "docs-mirror").

This module owns the contiguous cluster of Checks 96-99 that govern the docs/files/ mirror
documentation layer: shipped-code 1-to-1 docs bijection (96), per-mirror frontmatter integrity
(97), the 5-axis section presence contract (98), and the README + _template presence (99).
Each Check reads its own target files directly (docs/files/**, the tracked shipped list); none
depends on the monolith's global html/style/mainjs content, so the cluster is self-contained and
needs no ctx enrichment. NOTE: Check 108 (docs/files ↔ tracked-files FULL bijection) is a
sibling mirror check but lives elsewhere (non-contiguous) and is left in the monolith for now.

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT by reference (exec 不使用), so append
semantics / BLOCKING propagation / exit code are byte-equivalent to the monolith.

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  96. Phase 1 shipped-code 1-to-1 docs bijection: Phase 1 対象 shipped code (33 ファイル) が
      `docs/files/<path>.md` のミラー構造で 1 対 1 ドキュメント化されていることを機械強制
      (Docs 七 Phase 計画の Phase 7 骨格 — Phase 2-6 完了時に対象拡張)。新規 shipped ファイル
      追加時の doc 漏れを pre-commit fail で構造防止。(BLOCKING)
  97. docs/files/*.md frontmatter integrity: 各 1 対 1 doc が必須 frontmatter
      (`file` / `audience` / `last-updated` / `canonical-ref`) を持ち、かつ `file:` 値が
      mirror 自身の派生ソースパス (docs/files/<path>.md → <path>) と一致することを機械強制。
      copy-paste で `file:` 更新を忘れ「別ファイルを指す mirror」が通過する silent drift
      (Check 78/80 の name==identifier と同型) を閉じる。drift を pre-commit で防止。(BLOCKING)
  98. docs/files/*.md 5+1-axis section presence: 各 1 対 1 doc が必須 6 セクション見出し
      (`## What` / `## Why` / `## How` / `## Constraints` / `## Change impact` /
      `## Audience-specific notes`) を持つことを機械強制 (`_template.md` 整合)。(BLOCKING)
  99. docs/files/README.md + _template.md presence: 1 対 1 docs の inventory (README.md) と
      template (_template.md) が両方存在することを機械強制。(BLOCKING)
"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 96. Phase 1 shipped-code 1-to-1 docs bijection (BLOCKING) ────────────────
    # Docs Phase 7 骨格: Phase 1 対象 shipped code (33 ファイル) が `docs/files/<path>.md`
    # のミラー構造で 1 対 1 ドキュメント化されていることを機械強制。新規 shipped ファイルを
    # 追加するたびに対応 doc も同時に作成しないと pre-commit fail。Phase 2-6 は順次拡張。
    _phase1_targets96 = [
        # Phase 1: shipped code (33)
        "main.js", "index.html", "style.css", "sw.js", "aio-guard.js",
        "error-suppressor.js", "karte-init.js", "theme-init.js",
        "googlea7059bedc6fe8bdc.html",
        "js/aidk-rails.js", "js/apps.js", "js/brand.js", "js/components.js",
        "js/constants.js", "js/fatal-overlay.js", "js/identity.js",
        "js/meta-management.js", "js/mobile-drawer.js", "js/page-meta.js",
        "js/pages.js", "js/perf-guards.js", "js/pure-utils.js",
        "js/quiz-renderer.js", "js/router.js", "js/state.js",
        "js/storage.js", "js/store.js", "js/theme.js", "js/ui-components.js",
        "js/quiz/architecture-quiz-data.js", "js/quiz/aws-quiz-data.js",
        "js/quiz/pm-quiz-data.js", "js/quiz/quality-quiz-data.js",
        # Phase 2: AIO 正本層 + crawler 制御 (11)
        "llms.txt", "llms-full.txt", "llms_well-known.txt",
        ".well-known/llms.txt", ".well-known/llms_well-known.txt",
        ".well-known/aio-manifest.json", ".well-known/index.json",
        ".well-known/agent-skills/index.json", ".well-known/mcp.json",
        "robots.txt", "sitemap.xml",
        # Phase 3: config / scripts / workflows / Claude Code (25)
        ".github/scripts/_lib_io.py",
        ".github/scripts/aio_monitoring.py",
        ".github/scripts/check_aio_digests.py",
        ".github/scripts/check_binary_aio_metadata.py",
        ".github/scripts/check_css_stylelint.py",
        ".github/scripts/check_public_deployment_freshness.py",
        ".github/scripts/check_repository_consistency.py",
        ".github/scripts/update_aio_digests.py",
        ".github/scripts/update_binary_aio_organization.py",
        ".github/workflows/aio-monitoring.yml",
        ".github/workflows/architecture-validation.yml",
        ".github/workflows/auto-update-aio-digests.yml",
        ".github/workflows/playwright-regression.yml",
        ".github/workflows/update-playwright-snapshots.yml",
        ".github/dependabot.yml",
        ".claude/settings.json",
        ".claude/README.md",
        ".claude/CLAUDE.md",
        ".claude/agents/aio-guardian.md",
        ".claude/agents/check-author.md",
        ".claude/agents/repo-auditor.md",
        ".claude/commands/archive-incidents.md",
        ".claude/commands/deliver.md",
        ".claude/commands/verify.md",
        ".claude/commands/audit.md",
        ".claude/commands/sync-docs.md",
        ".claude/commands/increment.md",
        ".claude/skills/repo-status/SKILL.md",
        ".stylelintrc.json",
        "eslint.config.mjs",
        "package.json",
        "package-lock.json",
        "playwright.config.cjs",
        "e2e/portfolio.spec.js",
        # Phase 4: binary assets (2)
        "yuta-yokoi-ai-pm-orchestration-system.webp",
        "yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3",
        # Phase 5: dot files / meta config (6)
        ".editorconfig", ".gitattributes", ".gitignore",
        ".mcp.json", ".nvmrc", ".nojekyll",
        # Phase 6: root docs + docs/* meta-docs (47)
        "AI2AI.md", "CLAUDE.md", "Claude2Claude.md", "ChatGPT2ChatGPT.md",
        "README.md", "LICENSE", "SECURITY.md", "CONTRIBUTING.md",
        "CODEOWNERS", "CHANGELOG.md",
        "docs/README.md",
        "docs/architecture/check-repository-consistency-map.md",
        "docs/architecture/file-size-budget.md",
        "docs/architecture/main-js-extraction-map.md",
        "docs/architecture/major-update-readiness.md",
        "docs/architecture/repository-maintainability-map.md",
        "docs/architecture/research-application-policy.md",
        "docs/architecture/total-check-runbook.md",
        "docs/evidence/ai-pioneer-identity-review.md",
        "docs/evidence/public-deployment-freshness-review.md",
        "docs/incident-artifacts/README.md",
        "docs/incident-artifacts/decision-v80-e2e-and-maintainability-stage-1.md",
        "docs/incident-artifacts/decision-v80-maintainability-roadmap.md",
        "docs/incident-artifacts/decision-v80-phase2-aio-update-canary.md",
        "docs/incident-artifacts/decision-v80-phase2-artifact-governance.md",
        "docs/incident-artifacts/decision-v80-phase2-ci-hygiene.md",
        "docs/incident-artifacts/decision-v80-phase2-ci-hygiene-2.md",
        "docs/incident-artifacts/decision-v80-phase2-ci-hygiene-3.md",
        "docs/incident-artifacts/decision-v80-phase2-ci-hygiene-4.md",
        "docs/incident-artifacts/improvement-notes-claude-v80-phase2-aio-update-canary.md",
        "docs/incident-artifacts/improvement-notes-claude-v80-phase2-artifact-governance.md",
        "docs/incident-artifacts/improvement-notes-claude-v80-phase2-baseline-gate-doc-hardening.md",
        "docs/incident-artifacts/improvement-notes-claude-v80-phase2-ci-baseline-pipeline-hardening.md",
        "docs/incident-artifacts/improvement-notes-claude-v80-phase2-ci-hygiene-4.md",
        "docs/incident-artifacts/improvement-notes-claude-v80-phase2-consistency-invariant-hardening.md",
        "docs/incident-artifacts/improvement-notes-claude-v80-phase2-console-fix-and-eslint-v10-and-research-application.md",
        "docs/incident-artifacts/improvement-notes-claude-v80-phase2-dependency-modernization-and-flat-config.md",
        "docs/incident-artifacts/improvement-notes-claude-v80-phase2-dev-ergonomics-and-lint-coverage.md",
        "docs/incident-artifacts/improvement-notes-claude-v80-phase2-domain-authority-worksfor.md",
        "docs/incident-artifacts/improvement-notes-claude-v80-phase2-lint-hygiene-and-doc-sync.md",
        "docs/incident-artifacts/improvement-notes-claude-v80-phase2-public-freshness-observation.md",
        "docs/incident-artifacts/improvement-notes-claude-v80-phase2-pure-utility-and-static-data-extraction.md",
        "docs/incident-artifacts/improvement-notes-claude-v80-phase2-quiz-domain-split-and-bloat-governance.md",
        "docs/incident-artifacts/improvement-notes-claude-v80-phase2-self-documentation-integrity.md",
        "docs/incident-artifacts/update-portfolio.v70-experiment.yml",
        "docs/session-records/AI2AI-archive.md",
        "docs/session-records/incident-artifacts-archive-v74.md",
        # Final audit 漏れ補完 (4) — grep ベース全数監査で発見
        ".well-known/api-catalog",
        "jsconfig.json",
        "docs/evidence/aio-monitoring-log.json",
        "e2e/portfolio.spec.js-snapshots/homepage-baseline-chromium-linux.png",
        # aio-monitoring-log rotation archive (2026-07-07)
        "docs/evidence/aio-monitoring-log-archive.json",
        # Session handoff (本セッション末尾で AI-agnostic な引き継ぎ書を追加)
        "docs/incident-artifacts/improvement-notes-claude-v80-phase2-session-handoff-comment-injection.md",
        # why-only comment-injection increment record (handoff §10 の実行記録)
        "docs/incident-artifacts/improvement-notes-claude-v80-phase2-why-only-comment-injection.md",
        # self-drive operating-model 確立セッションの引き継ぎ書 (PR #60〜#64)
        "docs/incident-artifacts/improvement-notes-claude-v80-phase2-session-handoff-self-drive-operating-model.md",
    ]
    _missing96 = []
    for _t in _phase1_targets96:
        _doc = ROOT / "docs" / "files" / f"{_t}.md"
        if not _doc.exists():
            _missing96.append(_t)
    check(
        not _missing96,
        f"Check 96: all {len(_phase1_targets96)} Phase 1-6 files (shipped + AIO + config + binary + dot + meta-docs) have 1-to-1 docs",
        f"Check 96: missing 1-to-1 docs for: {_missing96} — `docs/files/_template.md` を元に作成せよ",
    )

    # ── 97. docs/files/*.md frontmatter integrity (BLOCKING) ─────────────────────
    # 各 1 対 1 doc が必須 frontmatter (file / audience / last-updated / canonical-ref) を
    # 持ち、かつ `file:` 値が自身の派生ソースパス (docs/files/<path>.md → <path>) と一致する
    # ことを機械強制。drift を pre-commit で防止。`file:` の self-coherence を加えることで、
    # mirror を copy-paste 新設した際に `file:` 更新を忘れ「別ファイルを指す mirror」が
    # Check 97/98 を通過してしまう silent drift (Check 78/80 の name==identifier と同型) を閉じる。
    _docs97_dir = ROOT / "docs" / "files"
    _bad97 = []
    if _docs97_dir.is_dir():
        for _md in _docs97_dir.rglob("*.md"):
            if _md.name in ("README.md", "_template.md"):
                continue
            _src = _md.read_text(encoding="utf-8")
            _fm = re.match(r"^---\s*\n([\s\S]*?)\n---\s*\n", _src)
            if not _fm:
                _bad97.append(f"{_md.relative_to(_docs97_dir)}: no frontmatter")
                continue
            _fm_body = _fm.group(1)
            for _required in ["file:", "audience:", "last-updated:", "canonical-ref:"]:
                if not re.search(rf"^{_required}", _fm_body, re.MULTILINE):
                    _bad97.append(f"{_md.relative_to(_docs97_dir)}: missing {_required}")
            # file: self-coherence — 値が mirror 自身の派生ソースパスと一致するか
            _relmd97 = _md.relative_to(_docs97_dir).as_posix()
            if _relmd97.endswith(".md"):
                _derived97 = _relmd97[:-len(".md")]
                _filefld97 = re.search(r"^file:\s*(\S+)", _fm_body, re.MULTILINE)
                if _filefld97 and _filefld97.group(1) != _derived97:
                    _bad97.append(
                        f"{_relmd97}: file:'{_filefld97.group(1)}' != derived source path '{_derived97}' "
                        "(mirror が別ファイルを指している — copy-paste drift)"
                    )
    check(
        not _bad97,
        f"Check 97: all docs/files/*.md have required frontmatter (file / audience / last-updated / canonical-ref) and file:==derived path",
        f"Check 97: doc frontmatter issues: {_bad97[:5]}{'...' if len(_bad97) > 5 else ''}",
    )

    # ── 98. docs/files/*.md 5-axis section presence (BLOCKING) ───────────────────
    # 各 1 対 1 doc が必須 5+1 セクション見出し (## What / ## Why / ## How / ## Constraints
    # / ## Change impact / ## Audience-specific notes) を持つことを機械強制。template と
    # のセクション整合を pre-commit で保証。
    _required_sections98 = ["## What", "## Why", "## How", "## Constraints", "## Change impact", "## Audience-specific notes"]
    _bad98 = []
    if _docs97_dir.is_dir():
        for _md in _docs97_dir.rglob("*.md"):
            if _md.name in ("README.md", "_template.md"):
                continue
            _src = _md.read_text(encoding="utf-8")
            _missing_sec = [s for s in _required_sections98 if s not in _src]
            if _missing_sec:
                _bad98.append(f"{_md.relative_to(_docs97_dir)}: missing {_missing_sec}")
    check(
        not _bad98,
        f"Check 98: all docs/files/*.md have required 5+1-axis sections (What / Why / How / Constraints / Change impact / Audience-specific notes)",
        f"Check 98: doc section issues: {_bad98[:3]}{'...' if len(_bad98) > 3 else ''}",
    )

    # ── 99. docs/files/README.md + _template.md presence (BLOCKING) ──────────────
    # 1 対 1 docs の inventory と template が存在することを機械強制。
    _inventory99 = ROOT / "docs" / "files" / "README.md"
    _template99 = ROOT / "docs" / "files" / "_template.md"
    check(
        _inventory99.exists() and _template99.exists(),
        "Check 99: docs/files/README.md (inventory) と _template.md (5-軸 template) が両方存在",
        f"Check 99: missing — README.md={_inventory99.exists()}, _template.md={_template99.exists()}",
    )

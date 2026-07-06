"""
checks_canon_config.py — canon-policy / config / meta-governance checks
(extracted from check_repository_consistency.py — check.py split track・category "canon/config governance").

Non-contiguous cluster of Checks 100/102/104/106/107/109/112/113: theme-init.js hardcoded storage
keys ↔ constants.js/brand.js (100), core operating-model policy documented in canon (102・102a-f),
verify-gate scripts Python 3.10+ guard (104), .nvmrc ↔ CI node single-major (106), runbook §11
CI-workflow inventory bijection (107), living-doc Check-count hardcode drift guard (109), shipped-JS
IME composition guard (112), commit/PR handoff discipline presence in canon (113). Each Check reads
its own target files directly; no global-content or cross-section var coupling.

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT/read/extract by reference (exec 不使用).

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  100. theme-init.js hardcoded storage keys ↔ js/constants.js STORAGE_KEY / js/brand.js KEY:
       the FOUC-prevention pre-paint script theme-init.js runs synchronously in <head> BEFORE
       main.js (ESM, async) loads, so it intentionally hardcodes the localStorage keys instead of
       importing them — 'portfolio_enhanced_v45' (theme/State) and 'portfolio_brand_v45' (Brand).
       If STORAGE_KEY in js/constants.js or KEY in js/brand.js is changed without updating the two
       literals in theme-init.js, only the very first paint reads a stale key and restores the
       wrong theme/brand; main.js re-applies the correct value once it loads, so the drift is
       silent (most tests never observe the first-paint window). This was discovered during the
       why-only comment-injection pass (the comment documents the duplication; this Check enforces
       it). Asserts theme-init.js reads exactly the canonical STORAGE_KEY (100a) and Brand.KEY
       (100b). (BLOCKING)
  102. Core operating-model policy is documented in canon: AI2AI.md STEP 3 carries the
       "Operating Model — AI Self-Driving / Human Control-and-Audit-Only"（核心運用ポリシー）
       statement, and CLAUDE.md §7 references it. WHY: the repository's core governance contract
       — AI self-drives implement→verify→merge→deploy end-to-end while the human's runtime role is
       control + audit (CI all-green) only — is load-bearing for how every future session operates.
       If it silently disappeared from canon, agents would revert to asking-at-every-step and the
       owner's "audit-CI-only" model would break. This Check pins the policy's presence (102a:
       AI2AI.md markers; 102b: CLAUDE.md reference; 102c: the "AI proposes, human disposes"
       proposal policy — proactive AI proposal-generation is a core self-driving function, the
       human dispositions which proposal to pursue; 102d: the 'No terminal "done" state'
       continuous-improvement policy — the AI may not self-stop or declare "done"/"good enough";
       only an explicit human stop instruction halts the improvement loop; 102e: the 'Infinite
       improvement'（改善は無限・完璧は存在しない）truth — the AI may not make a self-assessment of
       exhaustion/convergence ("no more improvements / converged / backlog harvested"), since that
       judgment is empirically almost always false (availability-heuristic fallacy); padding is
       guarded at the increment granularity only, never at the session granularity; 102f: the
       'reflect-then-organize' quality step — before a non-trivial increment the AI articulates a
       brief view (pros/cons, lens-check), documented in both AI2AI.md Operating Model and
       CLAUDE.md §5; externalizing reasoning breaks the 102e exhaustion fallacy, proven 2026-06-21
       when the AI self-generated 10 ideas and triaged 6 as autonomously executable with zero human
       input) so it cannot drift out. (BLOCKING)
  104. verify-gate scripts carry a Python 3.10+ version guard: every `.github/scripts/*.py`
       script invoked through an npm script (derived from package.json `scripts`, not a
       hardcoded list — like Check 46 for JS files) contains a `sys.version_info < (3, 10)`
       guard that exits with an actionable message. These scripts use 3.10+ syntax (PEP 604
       `str | None`), so on Python 3.9 (macOS /usr/bin/python3) they otherwise crash with an
       opaque `TypeError: unsupported operand type(s) for |` at import time. This Check fixes
       the guard in place so it cannot be silently removed, re-introducing the cryptic-crash
       class for the next AI-agnostic agent on a fresh machine. (BLOCKING)
  106. .nvmrc ↔ CI workflow node-version single-major alignment: the Node major in `.nvmrc`
       (the local-dev contract nvm reads) equals the `node-version` pinned across ALL
       `.github/workflows/*.yml`, and those pins are mutually equal. Check 69 only verifies
       package.json `engines.node` *covers* the CI pins; this Check pins the local-dev
       interpreter to the exact CI interpreter so a contributor's nvm and CI never diverge. (BLOCKING)
  107. total-check-runbook.md §11 CI-workflow inventory bijection: the runbook's §11 "CI
       workflows overview" names EXACTLY the set of `.github/workflows/*.yml` files on disk
       (backtick-quoted filenames). The human-facing CI index thus cannot silently fall behind
       when a workflow is added or removed — the counterpart of Check 75 (incident README
       inventory) / Check 105 (check-map) for the CI workflow surface. (BLOCKING)
  109. living-doc Check-count hardcode drift guard: orientation/governance docs that describe the
       CURRENT repository state (root CLAUDE.md / README.md / CHANGELOG.md / Claude2Claude.md /
       .claude/CLAUDE.md / .claude/README.md / .claude/agents/*.md / .claude/skills/*/SKILL.md /
       .claude/commands/*.md / total-check-runbook.md outside §9 / check-repository-consistency-
       map.md) must NOT hardcode a current Check tally in prose (the recurring "総数 = N" /
       "総数は N まで成長" / "all N Checks" / "consistency N Check" / "Check count: N" drift). This drift recurred even
       after PR #68 drift-proofed the runbook/map — PR #68 itself introduced a fresh stale value
       in §11 — proving manual drift-proofing leaks. §9 of the runbook (enforced by Check 70) is
       the single authority for the raw tally and is excluded from this scan; everywhere else the
       number must be replaced by a pointer to §9. Historical artifacts (improvement-notes /
       decision / Session Records / docs/files mirrors / the per-increment changelogs in
       repository-maintainability-map.md & main-js-extraction-map.md) are point-in-time records,
       not scanned. (BLOCKING)
  112. Shipped-JS IME composition guard: Enter-key handlers must not act on an Enter that is
       confirming an IME conversion. 112a (precise) — every Enter-submit handler in js/apps.js
       (task / todo / ai) carries the guard on the same line as the `e.key === 'Enter'` test
       (`!e.isComposing` or a manual `!todoComposing` flag); fixed for task in PR #151 and ai in
       PR #152 (todo already had it). 112b (general net) — ANY shipped JS module that tests for
       the Enter key (`e.key === 'Enter'`) must also reference an IME composition guard
       (`isComposing`/`Composing`) somewhere in that file. This catches the same footgun in
       modules outside apps.js — e.g. the command palette's keydown trap, where a Japanese
       project-name search + Enter would otherwise navigate instead of confirming the conversion.
       Without the guard a Japanese user confirming a conversion with Enter triggers a premature
       submit/navigation. This Check blocks reintroduction of the IME premature-submit class
       across all shipped JS. (BLOCKING)
  113. commit/PR handoff discipline presence in canon: BOTH the model-agnostic canon
       AI2AI.md (STEP 5.5) AND the Claude router CLAUDE.md (§5) must retain the handoff-first
       commit/PR discipline (theme-batched PRs, `gh pr merge --rebase`, commit-count-is-output-
       not-target). The owner adopted this as a repo-core rule; this Check enforces the rebase +
       no-padding markers in both docs so it cannot silently drift out of either. (BLOCKING)
"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check
    read = ctx.read
    extract = ctx.extract

    # ── 100. theme-init.js hardcoded storage keys ↔ constants.js / brand.js (BLOCKING) ─
    # theme-init.js は main.js (ESM, async) ロード前に <head> で同期実行され、FOUC を防ぐため
    # localStorage から theme/brand を復元する。そのため STORAGE_KEY ('portfolio_enhanced_v45')
    # と Brand.KEY ('portfolio_brand_v45') を **意図的にハードコード複製** している (import すると
    # main.js ロード前に解決できない)。js/constants.js の STORAGE_KEY や js/brand.js の KEY を
    # 変更したとき theme-init.js のリテラルを更新し忘れると、初期ペイントだけ旧キーを読み first-paint
    # のテーマ/ブランドが壊れる — main.js ロード後は正しいキーで再適用されるため test でも気づきに
    # くい silent drift。本 Check はこの 2 リテラルが canonical 値と一致することを BLOCKING で保証する。
    # (why-only コメント注入 increment で発見・systematize: コメントが複製を説明し、本 Check が強制する)
    _themeinit100 = ROOT / "theme-init.js"
    _constants100 = ROOT / "js" / "constants.js"
    _brand100 = ROOT / "js" / "brand.js"
    if _themeinit100.exists() and _constants100.exists() and _brand100.exists():
        _ti_src100 = _themeinit100.read_text(encoding="utf-8")
        _const_src100 = _constants100.read_text(encoding="utf-8")
        _brand_src100 = _brand100.read_text(encoding="utf-8")
        _storage_key_m100 = re.search(r"STORAGE_KEY:\s*'([^']+)'", _const_src100)
        _brand_key_m100 = re.search(r"const\s+KEY\s*=\s*'([^']+)'", _brand_src100)
        _storage_key100 = _storage_key_m100.group(1) if _storage_key_m100 else None
        _brand_key100 = _brand_key_m100.group(1) if _brand_key_m100 else None
        # 100a — theme-init.js が constants.js の canonical STORAGE_KEY を読む。
        check(
            _storage_key100 is not None and (f"getItem('{_storage_key100}')" in _ti_src100),
            f"Check 100a: theme-init.js reads the canonical STORAGE_KEY ('{_storage_key100}') from js/constants.js",
            f"Check 100a: theme-init.js does not read STORAGE_KEY '{_storage_key100}' — "
            "the FOUC-prevention pre-paint reads a stale localStorage key (js/constants.js ↔ theme-init.js drift)",
            blocking=True,
        )
        # 100b — theme-init.js が brand.js の canonical KEY を読む。
        check(
            _brand_key100 is not None and (f"getItem('{_brand_key100}')" in _ti_src100),
            f"Check 100b: theme-init.js reads the canonical Brand.KEY ('{_brand_key100}') from js/brand.js",
            f"Check 100b: theme-init.js does not read Brand.KEY '{_brand_key100}' — "
            "the FOUC-prevention pre-paint reads a stale localStorage brand key (js/brand.js ↔ theme-init.js drift)",
            blocking=True,
        )
    else:
        check(
            False,
            "",
            "Check 100: theme-init.js / js/constants.js / js/brand.js のいずれかが見つからず "
            "storage-key consistency を検証できない",
            blocking=True,
        )

    # ── 102. core operating-model policy documented in canon (BLOCKING) ──────────
    # このリポジトリの核心ガバナンス契約「AI が implement→verify→merge→deploy を自走し、人間の
    # runtime 役割は制御 + 監査 (CI オールグリーン) のみ」が canon に明記され続けることを機械強制。
    # 黙って消えると、後続セッションが「毎手確認」運用に逆戻りし、オーナーの audit-CI-only 運用が
    # 壊れる。AI2AI.md STEP 3 の Operating Model marker (102a) と CLAUDE.md §7 の参照 (102b) を
    # presence で固定し drift を防ぐ。
    _ai2ai102 = ROOT / "AI2AI.md"
    _claude102 = ROOT / "CLAUDE.md"
    if _ai2ai102.exists() and _claude102.exists():
        _ai2ai_src102 = _ai2ai102.read_text(encoding="utf-8")
        _claude_src102 = _claude102.read_text(encoding="utf-8")
        # 102a — AI2AI.md に Operating Model 宣言（英語 marker + 日本語 marker + CI 緑条件）が存在。
        _102a = (
            "Operating Model" in _ai2ai_src102
            and "核心運用ポリシー" in _ai2ai_src102
            and "CI オールグリーン" in _ai2ai_src102
        )
        check(
            _102a,
            "Check 102a: AI2AI.md documents the core Operating Model policy (AI self-driving / human control-and-audit-only)",
            "Check 102a: AI2AI.md is missing the core Operating Model policy markers "
            "('Operating Model' / '核心運用ポリシー' / 'CI オールグリーン') — 核心ガバナンス契約が canon から消えた",
            blocking=True,
        )
        # 102b — CLAUDE.md が同ポリシーを参照（router からの到達性）。
        _102b = ("核心運用ポリシー" in _claude_src102) or ("Operating Model" in _claude_src102)
        check(
            _102b,
            "Check 102b: CLAUDE.md references the core Operating Model policy",
            "Check 102b: CLAUDE.md no longer references the Operating Model policy — "
            "router から核心ポリシーへの到達性が失われた",
            blocking=True,
        )
        # 102c — 「AI proposes, human disposes」献策ポリシーが Operating Model に明記。
        # AI 自走の中核機能として「AI が献策し人間が裁可する」が canon に保持されることを固定。
        _102c = ("AI proposes, human disposes" in _ai2ai_src102) and ("献策" in _ai2ai_src102)
        check(
            _102c,
            "Check 102c: AI2AI.md documents the proposal policy (AI proposes, human disposes)",
            "Check 102c: AI2AI.md is missing the 'AI proposes, human disposes'（AI 献策 / 人間裁可）policy — "
            "AI 自走の中核機能（能動的献策）の canon 明記が消えた",
            blocking=True,
        )
        # 102d — 「改善に完了状態は存在しない」継続改善ポリシーが Operating Model に明記。
        # AI 側の「もう十分」自発停止・完了宣言を canon が禁じ続けることを固定。これが消えると
        # 後続 AI が「一区切りが妥当」と停止し、オーナーの「終わりなき改善を自走」運用が壊れる。
        _102d = ('No terminal "done" state' in _ai2ai_src102) and ("完了" in _ai2ai_src102)
        check(
            _102d,
            "Check 102d: AI2AI.md documents the continuous-improvement policy (No terminal \"done\" state)",
            "Check 102d: AI2AI.md is missing the 'No terminal \"done\" state'（改善に完了状態は存在しない）"
            "continuous-improvement policy — AI の自発的停止/完了宣言を禁じる canon が消えた",
            blocking=True,
        )
        # 102e — 「改善は無限・枯渇/収束の自己判断禁止」が canon に明記。AI が「改善は尽きた/収束した」
        # という self-assessment of exhaustion を下すことを禁じる真理を固定する。102d (完了宣言禁止) の
        # 上位概念で、本セッションで AI が繰り返した「収束した」誤判断 (毎回偽だった) の再発を構造的に防ぐ。
        _102e = ("Infinite improvement" in _ai2ai_src102) and ("改善は無限" in _ai2ai_src102)
        check(
            _102e,
            "Check 102e: AI2AI.md documents the infinite-improvement truth (改善は無限・枯渇の自己判断禁止)",
            "Check 102e: AI2AI.md is missing the 'Infinite improvement'（改善は無限・完璧は存在しない・"
            "枯渇/収束の自己判断禁止）truth — AI が「改善は尽きた/収束した」と誤判断して自走を止める"
            "失敗モードを禁じる canon が消えた",
            blocking=True,
        )
        # 102f — 「reflect-then-organize」= AI が非自明な増分前に簡潔な見解 (pros/cons・レンズ確認) を
        # 出してから進む品質ステップが Operating Model に明記され、CLAUDE.md §5 The loop にも記載される
        # ことを固定。見解化＝暗黙推論の明示構造化が 102e の枯渇誤謬を破る実証 (2026-06-21: 人間ゼロ入力で
        # AI が 10 案自己生成→6 案自走可能と判明) を受けて正式フロー化した。silent に消えると AI が
        # 「枯渇」自己判断のまま停止/padding へ滑る失敗モードへ戻るため presence を BLOCKING 強制する。
        _102f = ("reflect-then-organize" in _ai2ai_src102) and ("reflect-then-organize" in _claude_src102)
        check(
            _102f,
            "Check 102f: reflect-then-organize quality step documented (AI2AI.md Operating Model + CLAUDE.md §5)",
            "Check 102f: 'reflect-then-organize'（自己見解→自己整理を品質ステップ化）の canon 明記が消えた — "
            "AI2AI.md Operating Model と CLAUDE.md §5 The loop の両方に存在させよ。"
            "これが消えると AI が枯渇誤謬(102e)のまま停止/padding へ滑る失敗モードに戻る",
            blocking=True,
        )
    else:
        check(
            False,
            "",
            "Check 102: AI2AI.md / CLAUDE.md のいずれかが見つからず operating-model policy を検証できない",
            blocking=True,
        )

    # ── 104. verify-gate scripts carry a Python 3.10+ version guard (BLOCKING) ────
    # `npm run verify` runs these Python scripts under whatever `python3` resolves to on
    # the machine. They use 3.10+ syntax (PEP 604 `str | None` union annotations), so on
    # Python 3.9 (the macOS system interpreter at /usr/bin/python3)
    # check_repository_consistency.py crashes with an opaque
    # `TypeError: unsupported operand type(s) for |` at import time — a hard-to-diagnose
    # failure for the next (AI-agnostic) agent who lands on a fresh machine. Each verify-gate
    # script now fails fast with an actionable "requires Python 3.10+" message; this Check
    # fixes the guard in place so it cannot be silently removed, re-introducing the
    # cryptic-crash class. (Sibling to Check 55's vacuous-gate and Check 56's orphan
    # detection: it closes a silent/cryptic-failure class structurally.)
    # Derive the script set from package.json `scripts` (every .github/scripts/*.py invoked via
    # npm) rather than hardcoding it — so a Python script newly wired into the verify gate is
    # automatically required to carry the guard, exactly as Check 46 derives the JS file set.
    _pkg104 = ROOT / "package.json"
    _guard_scripts104 = []
    if _pkg104.exists():
        _scripts104 = json.loads(_pkg104.read_text(encoding="utf-8")).get("scripts", {})
        _all_script_src104 = " ".join(_scripts104.values())
        _guard_scripts104 = sorted(set(re.findall(r"\.github/scripts/[\w./-]+\.py", _all_script_src104)))
    _guard_marker104 = "sys.version_info < (3, 10)"
    _missing104 = [
        p for p in _guard_scripts104
        if not (ROOT / p).exists()
        or _guard_marker104 not in (ROOT / p).read_text(encoding="utf-8")
    ]
    check(
        bool(_guard_scripts104) and not _missing104,
        f"Check 104: all {len(_guard_scripts104)} npm-invoked Python scripts (derived from package.json) carry a Python 3.10+ version guard",
        f"Check 104: these npm-invoked Python scripts are missing the `{_guard_marker104}` guard: {_missing104}. "
        "3.10+ 専用構文 (PEP 604 `str | None`) を使うため、guard 無しでは Python 3.9 で cryptic TypeError になる。"
        "各スクリプトの import 直後に version guard を復元せよ" if _guard_scripts104 else
        "Check 104: package.json から .github/scripts/*.py を 1 つも検出できない (package.json の scripts を確認せよ)",
        blocking=True,
    )

    # ── 106. .nvmrc ↔ CI workflow node-version single-major alignment (BLOCKING) ──
    # Check 69 verifies package.json `engines.node` *covers* the CI node-version pins, but two
    # gaps remain: (1) `.nvmrc` — the local-dev contract `nvm` reads — is not tied to the CI pin,
    # so a contributor's local Node could silently differ from CI; (2) the workflows could pin
    # DIFFERENT majors from each other and still satisfy a permissive engines range. This Check
    # closes both: the `.nvmrc` major must equal the node-version pinned across ALL workflows,
    # and those pins must be mutually equal (a single shared major). Python-only workflows (no
    # node-version) contribute nothing and are correctly ignored.
    _nvmrc106 = ROOT / ".nvmrc"
    _wfdir106 = ROOT / ".github" / "workflows"
    if _nvmrc106.exists() and _wfdir106.exists():
        _nvm_major106 = _nvmrc106.read_text(encoding="utf-8").strip().lstrip("v").split(".")[0]
        _wf_majors106 = set()
        for _wf106 in sorted(_wfdir106.glob("*.yml")):
            for _m106 in re.finditer(r"node-version:\s*['\"]?(\d+)", _wf106.read_text(encoding="utf-8")):
                _wf_majors106.add(_m106.group(1))
        check(
            bool(_nvm_major106) and _wf_majors106 == {_nvm_major106},
            f"Check 106: .nvmrc (Node {_nvm_major106}) matches all CI workflow node-version pins ({sorted(_wf_majors106)})",
            f"Check 106: .nvmrc Node major {_nvm_major106!r} != CI workflow node-version pin major(s) {sorted(_wf_majors106)}. "
            "ローカル dev 契約 (.nvmrc) と全 workflow の node-version pin を単一 major に揃えよ "
            "(Check 69 は engines が pin を許容するかのみを見る)",
            blocking=True,
        )
    else:
        check(False, "", "Check 106: .nvmrc or workflows dir not found — node alignment を検証できない", blocking=True)

    # ── 107. total-check-runbook.md §11 CI-workflow inventory bijection (BLOCKING) ─
    # total-check-runbook.md §11 "CI workflows overview" is the human-facing index of what runs in
    # GitHub Actions and when. Like Check 75 (incident README inventory) and Check 105 (check-map),
    # a hand-maintained inventory silently drifts when a workflow file is added or removed but the
    # table is not updated. We slice §11 from the runbook and extract the backtick-quoted `*.yml`
    # filenames it names (backtick-anchored so the `docs/files/.../<name>.yml.md` reference inside
    # the section is NOT mistaken for a workflow), then require that set to equal the real
    # .github/workflows/*.yml files on disk — so the CI overview can never fall behind reality.
    _runbook107 = ROOT / "docs" / "architecture" / "total-check-runbook.md"
    _wfdir107 = ROOT / ".github" / "workflows"
    if _runbook107.exists() and _wfdir107.exists():
        _disk_wf107 = {p.name for p in _wfdir107.glob("*.yml")}
        _sec107 = re.search(r"^## 11\..*?(?=^## |\Z)", _runbook107.read_text(encoding="utf-8"), re.MULTILINE | re.DOTALL)
        _doc_wf107 = set(re.findall(r"`([\w-]+\.yml)`", _sec107.group(0))) if _sec107 else set()
        _only_disk107 = sorted(_disk_wf107 - _doc_wf107)
        _only_doc107 = sorted(_doc_wf107 - _disk_wf107)
        check(
            bool(_sec107) and _disk_wf107 == _doc_wf107,
            f"Check 107: total-check-runbook.md §11 documents exactly the {len(_disk_wf107)} CI workflows (doc ↔ .github/workflows bijection)",
            f"Check 107: CI workflow overview drift — on disk but missing from §11: {_only_disk107}; "
            f"in §11 but not on disk: {_only_doc107}. runbook §11 の workflow 一覧を同期せよ"
            + ("" if _sec107 else "（§11 セクションが見つからない）"),
            blocking=True,
        )
    else:
        check(False, "", "Check 107: runbook or workflows dir not found — workflow inventory を検証できない", blocking=True)

    # ── 109. living-doc Check-count hardcode drift guard (BLOCKING) ────────────────
    # stale な「現在の Check 総数」を prose にハードコードする drift class を構造的に封じる。この
    # drift は PR #68 が runbook/map を drift-proof 化した後も再発し、皮肉にも PR #68 自身が §11 に
    # 新たな stale 値を混入させていた（後続増分で実態へ修正）。手動の drift-proof 化では漏れが構造的に
    # 生じるため、機械強制で「§9 以外の living 文書に現在総数の数値ハードコードを書けない」ことを保証
    # する。正確な総数は §9（Check 70 が強制）を単一権威とし、他所はすべて §9 への pointer に置換する。
    # 走査対象は「現在状態を語る」orientation/governance 文書のみ。歴史層（improvement-notes /
    # decision / Session Record / docs/files ミラー）は point-in-time 記録ゆえ対象外。runbook は §9
    # （生の総数が正本として住む唯一の zone）を除外して走査する。
    # NOTE: 本 Check 実装ファイル自身は走査対象に含めない（下記 regex 文字列が自己発火しないため）。
    # 走査対象 = 現在状態を語る living orientation/governance 文書の全面。意図的に除外するもの:
    # (1) runbook §9 zone（生タリーの正本・下で個別除外）、(2) 歴史層 = per-increment changelog や
    # engineering log（repository-maintainability-map.md / main-js-extraction-map.md は「Check 総数
    # 42→43」等の point-in-time 記録を正当に保持するため対象外。Session Record / improvement-notes /
    # decision / docs/files ミラーも同様）。新たに living 文書を足したらここへ追加する。
    _living109 = [
        ".claude/CLAUDE.md",
        ".claude/README.md",
        "CLAUDE.md",
        "CHANGELOG.md",
        "Claude2Claude.md",
        "README.md",
        "docs/architecture/total-check-runbook.md",
        "docs/architecture/check-repository-consistency-map.md",
    ]
    for _glob109 in (".claude/agents/*.md", ".claude/skills/*/SKILL.md", ".claude/commands/*.md"):
        _living109 += [str(p.relative_to(ROOT)) for p in sorted(ROOT.glob(_glob109))]
    _forbidden109 = [
        (re.compile(r"総数\s*[=＝]\s*\d+"), "総数 = N"),
        (re.compile(r"総数\s*[はが]\s*\d+\s*(?:まで|に|へ)"), "総数は N まで"),
        (re.compile(r"\ball\s+\d+\s+[Cc]hecks\b"), "all N Checks"),
        (re.compile(r"consistency\s+\d+\s+[Cc]heck\b"), "consistency N Check"),
        (re.compile(r"[Cc]heck\s+count\**\s*[:：]\s*\**\d+"), "Check count: N"),
    ]
    _hits109 = []
    for _rel109 in _living109:
        _fp109 = ROOT / _rel109
        if not _fp109.exists():
            continue
        _txt109 = _fp109.read_text(encoding="utf-8")
        # runbook §9 は生の総数が正本として住む authority zone ゆえ走査から除外（§10/§11 は走査する）。
        if _rel109.endswith("total-check-runbook.md"):
            _txt109 = re.sub(r"^## 9\..*?(?=^## )", "", _txt109, flags=re.MULTILINE | re.DOTALL)
        for _rx109, _name109 in _forbidden109:
            for _m109 in _rx109.finditer(_txt109):
                _ln109 = _txt109[: _m109.start()].count("\n") + 1
                _hits109.append(f"{_rel109}:{_ln109} [{_name109}] {_m109.group(0)!r}")
    check(
        not _hits109,
        f"Check 109: no stale Check-count hardcode in {len(_living109)} living docs (§9 is the single authority)",
        "Check 109: stale Check-count hardcode(s) in living docs — " + "; ".join(_hits109)
        + ". 数値を除去し「正値は total-check-runbook.md §9 (Check 70 強制)」への pointer へ phrasing せよ",
        blocking=True,
    )

    # ── 112. Shipped-JS IME composition guard (BLOCKING) ──────────────────────────
    # Enter ハンドラは IME 変換確定の Enter (e.isComposing) で submit/遷移してはならない。日本語入力で
    # 変換候補を Enter 確定した際に未確定テキストが誤って追加/送信されたり画面遷移する footgun を防ぐ。
    # 112a (精密): js/apps.js の task/todo/ai 入力は `e.key === 'Enter'` を判定する行に必ず composition
    #   ガード ('Composing' = e.isComposing または手動 todoComposing) を同一行に併記する (task=PR #151 /
    #   ai=PR #152 で修正・todo は既存対応)。
    # 112b (一般網): apps.js 以外も含む全 shipped JS module で、`e.key === 'Enter'` を判定する file は
    #   同 file 内で IME composition ガード (isComposing/Composing) を参照していなければならない。
    #   command-palette の keydown trap のように apps.js 外で日本語検索 + Enter が遷移を誤発火する同クラスの
    #   footgun を構造的に捕捉する (本 Check 拡張時に command-palette.js の未ガード Enter を発見・修正)。
    _apps112 = ROOT / "js" / "apps.js"
    if _apps112.exists():
        _lines112 = _apps112.read_text(encoding="utf-8").splitlines()
        _enter112 = 0
        _viol112 = []
        for _i112, _line112 in enumerate(_lines112):
            if "e.key === 'Enter'" in _line112 or 'e.key === "Enter"' in _line112:
                _enter112 += 1
                if "Composing" not in _line112:
                    _viol112.append(_i112 + 1)
        check(
            # 両側非空ガード: Enter ハンドラが 1 つも見つからない (構造変更/gutting) 場合に vacuous pass
            # するのを防ぐ。task/todo/ai の 3 入力があるため Enter ハンドラは常に存在するはず。
            _enter112 > 0 and not _viol112,
            f"Check 112a: js/apps.js — {_enter112} 個の Enter-submit ハンドラすべてが IME composition ガードを持つ",
            f"Check 112a: js/apps.js: IME composition ガード無しの Enter-submit が line {_viol112} に存在 — "
            f"`&& !e.isComposing` を追加せよ (日本語 IME 変換確定の誤 submit を防ぐ。PR #151/#152 参照)"
            if _viol112 else
            "Check 112a: js/apps.js に Enter-submit ハンドラが見つからない (構造変更の可能性) — IME guard 検証が無効化された",
            blocking=True,
        )
    else:
        check(False, "", "Check 112a: js/apps.js not found — IME composition guard を検証できない", blocking=True)
    # 112b — 全 shipped JS module 横断の一般網: Enter ハンドラを持つ file は IME ガードを参照すること。
    _js_files112 = sorted((ROOT / "js").rglob("*.js"))
    _enter_unguarded112 = []
    _enter_files112 = 0
    for _f112 in _js_files112:
        _txt112 = _f112.read_text(encoding="utf-8")
        if "e.key === 'Enter'" in _txt112 or 'e.key === "Enter"' in _txt112:
            _enter_files112 += 1
            if "isComposing" not in _txt112 and "Composing" not in _txt112:
                _enter_unguarded112.append(str(_f112.relative_to(ROOT)))
    check(
        _enter_files112 > 0 and not _enter_unguarded112,
        f"Check 112b: Enter ハンドラを持つ {_enter_files112} 個の shipped JS module すべてが IME composition ガードを参照",
        f"Check 112b: IME composition ガードを参照しない Enter ハンドラ module: {_enter_unguarded112} — "
        f"`e.isComposing` ガードを追加せよ (日本語 IME 変換確定の誤 submit/遷移を防ぐ)"
        if _enter_unguarded112 else
        "Check 112b: Enter ハンドラを持つ shipped JS module が 1 つも無い (構造変更の可能性) — IME guard 一般網が無効化された",
        blocking=True,
    )

    # ── 113. commit/PR handoff discipline presence in canon (BLOCKING) ────────────
    # 「AI は交換可能なメンバ」軸の核 = AI→AI 引き継ぎ。commit/PR 規律 (fine commit ×厚い what+why ×
    # テーマ束ね PR ×rebase-merge ×commit 数は OUTPUT) はオーナーが「リポジトリの核」として正式採用し、
    # model-agnostic 正典 AI2AI.md (STEP 5.5) と Claude 固有 router CLAUDE.md (§5) の双方に置かれる永続
    # ルール。どちらかから silent に消えると新 AI が squash/粗 commit に退行し handoff 情報が失われるため、
    # 両ドキュメントに rebase + no-padding 条項のマーカーが存在することを機械強制し drift を防ぐ。
    _disc113_files = [("CLAUDE.md", ROOT / "CLAUDE.md"), ("AI2AI.md", ROOT / "AI2AI.md")]
    _markers113 = [
        "gh pr merge --rebase",   # commit を main に保持する merge 方式
        "OUTPUT であって TARGET",   # padding 禁止条項 (数を目的化しない)
    ]
    _miss113 = []
    for _label113, _path113 in _disc113_files:
        if not _path113.exists():
            _miss113.append(f"{_label113}:NOTFOUND")
            continue
        _src113 = _path113.read_text(encoding="utf-8")
        for _m113 in _markers113:
            if _m113 not in _src113:
                _miss113.append(f"{_label113}:{_m113}")
    check(
        not _miss113,
        "Check 113: CLAUDE.md と AI2AI.md の双方が handoff-first commit/PR 規律 (rebase + no-padding) を保持",
        f"Check 113: commit/PR 規律マーカー欠落: {_miss113} — CLAUDE.md §5 / AI2AI.md STEP 5.5 の規律を復元せよ",
        blocking=True,
    )

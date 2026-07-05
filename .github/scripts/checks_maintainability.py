"""
checks_maintainability.py — maintainability / test-health governance checks
(extracted from check_repository_consistency.py — Phase 1 PoC of the check.py split).

Self-integrity: this module's checks are aggregated by _aggregate_check_numbers() in the
monolith via CHECK_SOURCE_FILES, so Checks 45/70/105 (docstring inventory ↔ `# ── N.`
section ↔ check-map ↔ runbook §9 bijection) span this file too. `run(ctx)` receives a
context object exposing the shared check() / ROOT / errors / warnings, so the extracted
checks stay behavior-identical (same errors/warnings list objects, no exec, no module-global
coupling — the #253 "net-negative" concern is avoided by explicit ctx injection, not exec()).

Check inventory (kept in sync with the `# \u2500\u2500 N.` sections in run() below; Check 45 enforces):
  361. Every shipped JS leaf module (`js/*.js` ∪ `js/quiz/*.js`) MUST be
       registered in docs/architecture/file-size-budget.md §4 BUDGET-DATA
       with a line budget. Check 71 guarantees registered⟹exists; this is
       the symmetric exists⟹registered, so together they bijection the
       js-leaf surface against BUDGET-DATA. Without it a new leaf module
       (e.g. a js/<x>-page.js born from a bloat-reduction extraction) stays
       silently unbudgeted, escaping the Check 52 advisory and able to grow
       unbounded — the exact gap file-size-budget.md §5 flagged as a
       deferred extension. Machine-enforces the owner-accepted 1,000-line
       threshold discipline (keep bloat from recurring). (BLOCKING)
  362. Every mutation in mutation_samples.py (MUTATIONS ∪ E2E_MUTATIONS)
       MUST have its `find` anchor resolve in its target `file`. The
       mutation-probe / -e2e runners are NOT invoked by any CI workflow
       (completeness verification is manual), so a leaf extraction or
       refactor that moves/removes the anchored code leaves the anchor
       silently orphaned until someone runs the probe by hand — quietly
       hollowing out the completeness-critic's net. Real example: #558
       moved PomodoroPage js/apps.js → js/pomodoro-page.js and orphaned
       the pomodoro E2E mutation anchor. This lifts anchor integrity into
       the BLOCKING verify gate so refactors must keep mutation_samples.py
       in sync. (BLOCKING)
  363. No shipped JS *logic* leaf module (`js/*.js`, non-recursive) may
       exceed the hard line ceiling declared by the JS-LEAF-CEILING marker
       in docs/architecture/file-size-budget.md (currently 1,000). This is
       the BLOCKING enforcement of the owner-accepted 1,000-line bloat
       threshold: whereas Check 52 (BUDGET-DATA) is an ADVISORY per-file
       loose budget that only warns, this is a hard gate that fails the
       build so an over-threshold logic leaf must be split before merge —
       the same two-layer design as Check 60 (advisory early-warning layer
       + BLOCKING hard-gate layer). Scope excludes js/quiz/*.js (pure quiz
       data, where content growth is valuable, observed only by advisory)
       and main.js (protected kernel, not under js/, guarded by Check 43 /
       strong-advisory). Machine-enforces "keep bloat from arising" for the
       behavior-code surface, protecting the AI self-improvement loop that
       unbounded logic-leaf growth would threaten. (BLOCKING)
  364. store.js's ingestion normalizers (validateAndNormalize /
       normalizeAppsData / normalizeProject) MUST NOT use the
       `(X || []).<throwing-array-method>` idiom. They are total functions
       over untrusted external data (import / cross-tab / snapshot / load)
       and must never throw on a non-array input. `(X || [])` fails to
       replace a non-array *truthy* value (a string / number / object), so
       the following .filter/.map/.forEach/.some/.reduce throws a TypeError
       and every ingestion path FatalPage-crashes — #568 (ai/pomodoro
       history), #572 (project tech/tags/links), #573 (task.tags) were the
       real bugs of this class. The safe form is `(Array.isArray(X) ? X :
       [])`. This lifts the per-instance fixes into a structural guard so
       the class cannot be silently reintroduced. (BLOCKING)
"""
import re


def run(ctx):
    """Execute this module's checks against the shared context.

    ctx exposes: ROOT (Path), check (callable), warnings (list), errors (list),
    read/read_bytes/extract (helpers). Extracted checks use the same objects the
    monolith uses, so appends land in the same errors/warnings lists.
    """
    ROOT = ctx.ROOT
    check = ctx.check
    warnings = ctx.warnings

    # ── 361. shipped JS leaf-module BUDGET-DATA registration coverage (BLOCKING) ──
    # 全 shipped JS leaf module (js/*.js ∪ js/quiz/*.js) が file-size-budget.md §4
    # BUDGET-DATA に行数予算として登録されていることを機械強制する。Check 71 が
    # 「BUDGET-DATA に登録された path は実在する」(registered ⟹ exists) を保証するのに対し、
    # 本 Check はその対称「shipped JS が存在する ⟹ 登録済み」(exists ⟹ registered) を担い、
    # 両者で js leaf module 面の bijection を成す。これが無いと新規 leaf module (bloat-reduction
    # の抽出で生まれる js/<x>-page.js など) が BUDGET-DATA に登録されないまま silent に
    # 「行数予算なし」になり、Check 52 advisory の網から外れて無制限に成長し得る
    # (file-size-budget.md §5 が deferred 拡張候補として認識していた gap)。owner 受諾の
    # 1,000 行しきい値 (bloat を「生じないように」する規律) を機械強制へ昇華する Check。
    _budget361 = ROOT / "docs" / "architecture" / "file-size-budget.md"
    if _budget361.exists():
        _bsrc361 = _budget361.read_text(encoding="utf-8")
        _bblock361 = re.search(r"<!--\s*BUDGET-DATA(.*?)-->", _bsrc361, re.DOTALL)
        _registered361: set[str] = set()
        if _bblock361:
            for _line361 in _bblock361.group(1).strip().split("\n"):
                _line361 = _line361.strip()
                if not _line361 or _line361.startswith("#"):
                    continue
                _parts361 = [p.strip() for p in _line361.split("|")]
                if len(_parts361) >= 3:
                    _registered361.add(_parts361[0])
        _shipped361 = sorted(
            p.relative_to(ROOT).as_posix()
            for p in list((ROOT / "js").glob("*.js")) + list((ROOT / "js" / "quiz").glob("*.js"))
        )
        _unregistered361 = [p for p in _shipped361 if p not in _registered361]
        check(
            not _unregistered361 and len(_shipped361) > 0,
            f"Check 361: all {len(_shipped361)} shipped JS leaf modules (js/*.js ∪ js/quiz/*.js) "
            "are registered in file-size-budget.md §4 BUDGET-DATA",
            f"Check 361: shipped JS leaf module(s) missing from §4 BUDGET-DATA: {_unregistered361}. "
            "新 leaf モジュールは file-size-budget.md §2 表 + §4 BUDGET-DATA に行数予算を登録せよ "
            "(Check 52 silent-unbudgeted 防止 / bloat を「生じないように」する 1,000 行しきい値の機械強制)",
        )
    else:
        warnings.append("Check 361: file-size-budget.md not found — JS budget coverage skipped")

    # ── 362. mutation_samples find-anchor resolution (BLOCKING) ───────────────────
    # mutation_samples.py の全 mutation (MUTATIONS ∪ E2E_MUTATIONS) の `find` anchor が対象 file に
    # 実在することを機械強制する。mutation-probe / mutation-probe-e2e は CI workflow から呼ばれない
    # (完全性検証は手動実行) ため、leaf 抽出やリファクタで anchor の対象コードが別 file へ移動/消滅
    # しても、手動で probe を回すまで anchor は silent に orphan 化し、completeness-critic (安全網の
    # 安全網) の網が知らぬ間に穴だらけになる。実例: #558 で PomodoroPage を js/apps.js →
    # js/pomodoro-page.js へ分離した際、pomodoro E2E mutation の anchor が apps.js から消え orphan 化
    # した (mutation-probe --e2e を手動実行して初めて発覚)。本 Check は anchor 整合性を verify 時の
    # BLOCKING gate へ引き上げ、抽出/リファクタ時に mutation_samples.py の追従を強制する。
    try:
        import importlib as _importlib362
        _ms362 = _importlib362.import_module("mutation_samples")
        _orphans362: list[str] = []
        for _lst362, _lbl362 in ((_ms362.MUTATIONS, "MUTATIONS"), (_ms362.E2E_MUTATIONS, "E2E_MUTATIONS")):
            for _m362 in _lst362:
                _f362 = _m362["file"]
                try:
                    _txt362 = _f362.read_text(encoding="utf-8")
                except OSError:
                    _orphans362.append(f"[{_lbl362}] {_m362['name'][:55]} → file 不在: {_f362}")
                    continue
                if _m362["find"] not in _txt362:
                    _orphans362.append(f"[{_lbl362}] {_m362['name'][:55]} → find-anchor 不在 in {_f362.name}")
        check(
            not _orphans362,
            f"Check 362: all {len(_ms362.MUTATIONS) + len(_ms362.E2E_MUTATIONS)} mutation find-anchors "
            "(MUTATIONS ∪ E2E_MUTATIONS) resolve in their target files",
            f"Check 362: orphaned mutation find-anchor(s): {_orphans362[:5]}. "
            "リファクタ/抽出で anchor の対象コードが別 file へ移動/消滅した — mutation_samples.py の該当 "
            "file/find を現行コードへ追従させよ (mutation-probe は CI 非実行ゆえ本 Check が anchor 整合を守る)",
        )
    except ImportError as _e362:
        warnings.append(f"Check 362: mutation_samples import failed ({_e362}) — anchor resolution skipped")

    # ── 363. shipped JS logic-leaf hard line ceiling (BLOCKING) ───────────────────
    # shipped JS *ロジック* leaf module (js/*.js・非再帰) の行数が JS-LEAF-CEILING marker
    # (file-size-budget.md) の宣言するハード上限 (現行 1,000) を越えないことを機械強制する。
    # Check 52 (BUDGET-DATA) が per-file の loose な ADVISORY 予算で「緩やかに観測」(超過は warning のみ)
    # するのに対し、本 Check は owner 受諾の 1,000 行しきい値を BLOCKING gate として強制し、越えた
    # ロジック leaf は merge 前に分割させる (Check 60 と同型の advisory 早期警告層 + BLOCKING ハード
    # ゲート層の二層設計)。スコープは js/*.js 直下のロジック leaf のみ: js/quiz/*.js (純データ・設問追加は
    # 価値ある成長ゆえ advisory 観測に委ねる) と main.js (保護 kernel・js/ 直下でない・Check 43 で別途保護)
    # は除外する。肥大化放置が脅かす「AI 無限改善自走」を behavior-code 面で守る「生じないように」の機械化。
    _budget363 = ROOT / "docs" / "architecture" / "file-size-budget.md"
    if _budget363.exists():
        _bsrc363 = _budget363.read_text(encoding="utf-8")
        _m363 = re.search(r"<!--\s*JS-LEAF-CEILING\s+(\d+)\s*-->", _bsrc363)
        if _m363:
            _ceiling363 = int(_m363.group(1))
            _over363: list[str] = []
            for _p363 in sorted((ROOT / "js").glob("*.js")):
                _n363 = len(_p363.read_text(encoding="utf-8").splitlines())
                if _n363 > _ceiling363:
                    _over363.append(f"{_p363.relative_to(ROOT).as_posix()} ({_n363} > {_ceiling363})")
            check(
                not _over363,
                f"Check 363: all shipped JS logic leaves (js/*.js) are within the "
                f"{_ceiling363}-line hard ceiling (JS-LEAF-CEILING)",
                f"Check 363: js/*.js logic leaf(s) exceed the {_ceiling363}-line hard ceiling: {_over363}. "
                "owner 受諾の 1,000 行しきい値超過 — factory pattern で葉モジュールへ分割してから merge せよ "
                "(肥大化を『生じないように』する BLOCKING 防止層。恒久的に越えるべき正当理由があれば "
                "file-size-budget.md の JS-LEAF-CEILING marker を rationale 付きで owner 裁可のもと引き上げる)",
            )
        else:
            warnings.append("Check 363: JS-LEAF-CEILING marker not found in file-size-budget.md — ceiling check skipped")
    else:
        warnings.append("Check 363: file-size-budget.md not found — JS leaf ceiling skipped")

    # ── 364. store.js ingestion normalizer array-op safety (BLOCKING) ─────────────
    # store.js の正規化子 (validateAndNormalize / normalizeAppsData / normalizeProject) は import /
    # cross-tab / snapshot / load から来る untrusted な外部データを正規化する総関数で、非配列を渡されても
    # throw してはならない。`(X || []).<array-method>` idiom は X が非配列の *truthy* 値 (文字列/数値/
    # オブジェクト) だと `|| []` が置換せず、後続の throwing array-method (filter/map/forEach/some/reduce...) が
    # `TypeError: ... is not a function` を投げ、全 ingestion 経路が FatalPage crash する。#568 (ai/pomodoro
    # history) / #572 (project tech/tags/links) / #573 (task.tags) が同一 class の実バグ。安全形は
    # `(Array.isArray(X) ? X : [])`。本 Check は per-instance の fix を「idiom 再混入の構造防止」へ昇華する
    # (肥大化 Check 363 と同じ「解消したら再発も防ぐ」規律の ingestion-safety 版)。
    _store364 = ROOT / "js" / "store.js"
    if _store364.exists():
        _ssrc364 = _store364.read_text(encoding="utf-8")
        # `<property-access> || []) . <throwing array-method>` を検出 (slice は文字列でも throw しないため除外)。
        # 直前を `\w` (識別子/プロパティアクセス末尾) に限定することで、`str.match(...) || []` のような
        # method-call 結果 (`)` で終わる・match は Array|null 契約ゆえ安全) を false-positive にしない。
        # 危険なのは `raw.tech || []` 等の untrusted プロパティアクセスが非配列 truthy を返す場合のみ。
        _unsafe364 = re.findall(
            r"\w\s*\|\|\s*\[\]\s*\)\s*\.\s*(filter|map|forEach|some|every|reduce|flatMap|find|findIndex)\b",
            _ssrc364,
        )
        check(
            not _unsafe364,
            "Check 364: store.js の正規化子に unsafe `(X || []).<throwing array-method>` idiom が無い "
            "(ingestion-crash class の構造防止)",
            f"Check 364: store.js に unsafe idiom `(X || []).<throwing array-method>` が {len(_unsafe364)} 件 "
            f"({sorted(set(_unsafe364))})。非配列 truthy 入力で TypeError を投げ ingestion 全経路が FatalPage "
            "crash する (#568/#572/#573 class)。`(Array.isArray(X) ? X : [])` へ書き換えよ",
        )
    else:
        warnings.append("Check 364: js/store.js not found — ingestion normalizer safety skipped")

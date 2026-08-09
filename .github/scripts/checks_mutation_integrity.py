"""
checks_mutation_integrity.py — mutation 安全網そのものの完全性を守る Check 群
(extracted from checks_maintainability.py — check.py split track・category "mutation integrity").

このモジュールは「安全網を検証する道具が壊れていないこと」を守る meta-QA クラスタを所有する。
mutation testing はリポジトリの安全網 (consistency Check 群 / behavior e2e) が実際に回帰を捕捉
できるかを検証する唯一の手段であり、その **mutation 定義自体が腐ると、緑は「守られている」で
はなく「検証されていない」を意味する**。実際に (a) mutation-probe の catch 判定が Check 362 の
副作用で自動成立し consistency probe 全体が vacuous だった件 (#885)、(b) mutation の登録先が
混線して behavior 側 6 件が一度も走っていなかった件が発生している。ゆえに find-anchor / test
題名 / no-op / 帰属 / 登録先の 5 面をすべて BLOCKING で機械強制する。

各 Check は mutation_samples を importlib で読み、e2e/*.spec.js と対象 shipped file を直接読む。
monolith の共有 global (html/style/mainjs 等) に依存しないため ctx enrichment は不要。

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT/warnings by reference (exec 不使用) so append
semantics / BLOCKING propagation / exit code are byte-equivalent to the monolith.

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
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

  379. mutation_samples E2E_MUTATIONS `test`-field resolution: every E2E_MUTATIONS entry carries a
       `test` field that mutation_probe's `--e2e` runner feeds to Playwright as a `-g` (grep)
       pattern to select the behavior test that must catch the mutated bug. If that field is a typo
       or names a since-renamed/deleted test, `playwright -g "<typo>"` matches ZERO tests and both
       the baseline and mutated runs "pass" (0 tests ran) — so the mutation's non-vacuity validation
       is silently disabled and the completeness-critic (the safety net's safety net) loses that
       edge. Detection covers BOTH title notations: quoted literals AND backtick template titles
       (parameterised `for` loops). The literal-only version could not see templates at all, so the
       repo's most important safety nets — the ALL_ROUTES route-render loop in security-proxy.spec.js
       and the a11y-axe route loop — could not have a mutation registered against them: the field was
       reported unresolved and turned this Check RED (safe-fail, but it left the meta-QA layer with a
       hole exactly where coverage matters most). Templates are split on `${…}` into static segments,
       and a field resolves if it is a substring of any segment (conservative and sound: the runtime
       title always contains every static segment).
       edge. Check 362 verifies each mutation's `find` ANCHOR resolves in the target file, but the
       parallel `test`-name reference was unenforced, and mutation-probe-e2e is not run in CI so a
       typo stays silent until someone runs it manually. This Check imports mutation_samples and
       parses every e2e test title from e2e/*.spec.js, asserting each E2E_MUTATIONS `test` field is a
       substring of a real test title — the e2e-title twin of Check 362's find-anchor resolution,
       making "a mutation names a behavior test ⟹ that test exists" an enforced invariant. (BLOCKING)

  380. mutation_samples no-op guard (`replace` ≠ `find`): every mutation in MUTATIONS ∪ E2E_MUTATIONS
       must have a `replace` string DIFFERENT from its `find`. A mutation whose replace equals its
       find is a no-op — applying it changes nothing, so the gate stays GREEN and mutation_probe
       reports it as SURVIVED (a false coverage gap), while at verify time it is completely silent
       (Check 362 only checks the find anchor exists, 379 only the test-field). A no-op mutation thus
       silently provides FALSE coverage: it looks like it exercises a bug class but tests nothing.
       This is easy to introduce accidentally (a botched edit that leaves find==replace). This Check
       asserts find != replace for every entry, completing the mutation-integrity mesh (362 = find
       anchor resolves in target file / 379 = test-field resolves to a real e2e test / 380 = replace
       actually mutates) so no dead mutation can silently erode the completeness-critic. (BLOCKING)

  397. mutation_samples E2E_MUTATIONS `test`-field UNAMBIGUITY: every E2E_MUTATIONS `test` field must
       be a substring of EXACTLY ONE e2e test title (not merely ≥1, which Check 379 already enforces).
       mutation_probe's `--e2e` runner feeds the field to Playwright as `-g "<field>"`, which selects
       EVERY test whose title contains that substring. If a field matches TWO+ titles, `-g` runs all
       of them, and the mutation's non-vacuity attribution becomes ambiguous: the probe cannot tell
       which test was meant to catch the mutation, and a mutation that leaves the INTENDED test green
       can still be reported "caught" because an unrelated co-matched test fails (or vice-versa —
       false SURVIVED if the intended test's failure is masked). Check 379 guards ≥1 (anchor resolves
       at all); this Check tightens it to ==1 (anchor targets the one intended test), closing the
       ambiguous-anchor face of the mutation-integrity mesh (362/379/380). A too-generic field like
       `"unique slugs"` (which matched both the settings same-name test and the resilience
       colliding-import test) is the failure mode this prevents. Title extraction shares Check 379's
       two-notation helper (_e2e_titles); a backtick template counts as ONE test because it expands
       at runtime to N routes that all run the SAME assertion body, so co-matching them cannot blur
       attribution. (BLOCKING)

  399. mutation-probe の catch 帰属 (attribution): `mutation_probe.py` の consistency mode は
       catch を **Check 362 (anchor orphan) 以外の error** で判定しなければならない
       (`ANCHOR_ORPHAN_MARKER = "Check 362:"` 定数 + `caught_by_real_check()` を持ち、旧判定
       `if run_gate() == 0:` を残さない)。probe は mutation を適用してから gate を走らせるが、
       適用によりその mutation 自身の find-anchor が対象 file から消えるため Check 362 (全 mutation
       の find-anchor が対象 file に解決することを検証) が **必ず** RED になる。ゆえに gate の
       exit code だけで caught を判定すると、意図した Check が 1 つも発火しなくても全 mutation が
       Check 362 の副作用で自動的に caught と報告され、「安全網が本当に回帰を捕捉するか」を検証する
       はずの meta-QA が何も検証しない vacuous ツールへ退行する (Check 362 導入以降 実際にそうなって
       いた)。実証: どの Check も見ない inert な prose を対象にした対照 mutation で gate は RED に
       なり、その error は Check 362 の 1 件のみだった。`run_gate()` は (exit code, 出力) の tuple を
       返すため旧判定が残ると常に False = 全件 SURVIVED へ静かに反転する — その退行実体も禁止する。
       Check 362/379/380/397 が守る「mutation データの整合」に対し、本 Check は「probe の判定その
       ものの健全性」を守る (mutation-integrity mesh の runner 面)。(BLOCKING)

  409. Mutation registration-list separation: entries in `MUTATIONS` (the consistency safety-net
       list, gated by check_repository_consistency.py) must NOT carry a `test` key, and every
       `E2E_MUTATIONS` entry must carry one. `test` is the e2e identifier; putting a behaviour
       mutation in the consistency list means (a) it never runs in the e2e probe, so that behaviour's
       safety net is never verified, and (b) the consistency probe reports it SURVIVED forever
       because no Check catches a pure behaviour change. Measured 2026-08-09: the consistency probe
       reported 6 SURVIVED entries which turned out to be behaviour mutations filed in MUTATIONS —
       one had even been carried into an archive file by log rotation. The same sweep found 10 legacy
       consistency mutations whose `test` held a Check OK-message (an older convention that now
       collides with the e2e meaning); those keys were removed. HONEST LIMIT: this Check cannot
       detect a behaviour mutation filed in MUTATIONS *without* a `test` key — such an entry is
       an orphan that verifies nothing anywhere (it can never run in the e2e probe, and the
       consistency probe just reports it SURVIVED). One such entry existed and was found by
       running `npm run mutation-probe`. 409b now closes that residual case STATICALLY via the
       naming convention: a consistency mutation declares the Check it exercises by starting its
       `name` with `Check <number>`, while behaviour mutations do not (they use behavior: /
       a11y: / resilience: …). Measured when adopting it: 294/295 consistency and 115/115 e2e
       entries already complied; the single exception was a naming omission on a mutation that
       legitimately exercises Check 406. The probe remains the detector for a mutation that is
       named correctly but exercises nothing — running it periodically still has value.
       (BLOCKING)
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

    # e2e test() title を引用符リテラルと backtick テンプレートの両記法で抽出する。旧実装は前者のみを
    # 見ており、パラメタライズド loop (security-proxy の ALL_ROUTES route-render gate / a11y-axe の
    # route loop) が不可視 = 安全網の最重要部分に mutation を登録できなかった (解決不能で false RED)。
    # テンプレートは `${…}` 境界で静的セグメントへ分解する (実行時 title は必ずいずれかを含むため健全)。
    def _e2e_titles(_src):
        _out = []
        for _m in re.finditer(r"test\(\s*(['\"])(.+?)\1", _src):
            _out.append(_m.group(2))
        for _m in re.finditer(r"test\(\s*`([^`]*)`", _src):
            _out.extend(seg for seg in re.split(r"\$\{[^}]*\}", _m.group(1)) if seg.strip())
        return _out

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

    # ── 379. mutation_samples E2E_MUTATIONS `test`-field resolution (BLOCKING) ─────
    # E2E_MUTATIONS の各 entry は `test` フィールドを持ち、mutation_probe の --e2e runner がそれを
    # Playwright の `-g` grep パターンとして渡し「mutated バグを捕捉すべき behavior test」を選ぶ。
    # この test 名が typo / rename・削除済だと `playwright -g "<typo>"` が 0 test マッチし、baseline も
    # mutated も「pass」(0 test 実行) になる — つまり その mutation の非 vacuity 検証が silent に無効化し、
    # completeness-critic (安全網の安全網) がその edge を失う。Check 362 は各 mutation の `find` ANCHOR
    # が対象 file に解決することを検証するが、並行する `test`-名参照は未強制で、mutation-probe-e2e は
    # CI 非実行ゆえ typo は手動実行まで silent。本 Check は mutation_samples を import し e2e/*.spec.js の
    # 全 test タイトルを parse して、各 E2E_MUTATIONS の `test` フィールドが実在タイトルの substring で
    # あることを強制する (Check 362 の find-anchor resolution に対する e2e-title twin)。
    try:
        import importlib as _importlib379
        _ms379 = _importlib379.import_module("mutation_samples")
        _titles379 = []
        for _spec379 in sorted((ROOT / "e2e").glob("*.spec.js")):
            _titles379 += _e2e_titles(_spec379.read_text(encoding="utf-8"))
        _unresolved379 = []
        for _m379 in _ms379.E2E_MUTATIONS:
            _t379 = _m379.get("test", "")
            if not _t379 or not any(_t379 in _title379 for _title379 in _titles379):
                _unresolved379.append(f"{_m379['name'][:50]} → test='{_t379}'")
        check(
            bool(_titles379) and not _unresolved379,
            f"Check 379: all {len(_ms379.E2E_MUTATIONS)} E2E_MUTATIONS `test` fields resolve to a real e2e test title ({len(_titles379)} titles)",
            f"Check 379: E2E_MUTATIONS の `test` フィールドが実 e2e test にマッチしない: {_unresolved379[:5]} — "
            "test 名の typo / rename・削除で `playwright -g` が 0 test マッチし mutation の非 vacuity 検証が "
            "silent 無効化する。e2e/*.spec.js の実 test 名へ追従させよ (Check 362 の find-anchor の e2e-title 版)"
            if _titles379 else
            "Check 379: e2e/*.spec.js から test タイトルを parse できない (構造変更の可能性)",
            blocking=True,
        )
    except ImportError as _e379:
        warnings.append(f"Check 379: mutation_samples import failed ({_e379}) — test-field resolution skipped")

    # ── 380. mutation_samples no-op guard (`replace` ≠ `find`) (BLOCKING) ──────────
    # MUTATIONS ∪ E2E_MUTATIONS の各 entry は `replace` が `find` と異なる必要がある。find==replace の
    # mutation は no-op で、適用しても何も変わらず gate が GREEN のままゆえ mutation_probe は SURVIVED
    # (偽の coverage gap) と報告するが、verify 時は完全に silent (Check 362 は find anchor 存在のみ、
    # 379 は test-field のみを見る)。no-op mutation は「バグ class を叩いているように見えて何も test して
    # いない」偽カバレッジを silent に提供する。編集ミスで find==replace を残すと容易に混入する
    # (本 Check 導入の契機も Check 379 の self-referential mutation を除去する過程で一時的に find==replace
    # を作った実例)。find != replace を全 entry に強制し、mutation-integrity mesh (362=find anchor 解決 /
    # 379=test-field 解決 / 380=replace が実際に mutate する) を閉じ、dead mutation が completeness-critic
    # を silent に侵食するのを防ぐ。
    try:
        import importlib as _importlib380
        _ms380 = _importlib380.import_module("mutation_samples")
        _noop380 = []
        for _lst380, _lbl380 in ((_ms380.MUTATIONS, "MUTATIONS"), (_ms380.E2E_MUTATIONS, "E2E_MUTATIONS")):
            for _m380 in _lst380:
                if _m380.get("find", "") == _m380.get("replace", "__SENTINEL_NO_REPLACE__"):
                    _noop380.append(f"[{_lbl380}] {_m380['name'][:55]}")
        check(
            not _noop380,
            f"Check 380: all {len(_ms380.MUTATIONS) + len(_ms380.E2E_MUTATIONS)} mutations have replace != find (no no-op / false-coverage mutation)",
            f"Check 380: no-op mutation(s) (find == replace): {_noop380[:5]} — replace が find と同一で "
            "適用しても何も変わらない偽カバレッジ。mutation_probe は SURVIVED と報告するが verify では silent。"
            "replace を find と異なる実 mutation へ修正するか、機能しない mutation なら除去せよ",
        )
    except ImportError as _e380:
        warnings.append(f"Check 380: mutation_samples import failed ({_e380}) — no-op guard skipped")

    # ── 397. mutation_samples E2E_MUTATIONS `test`-field UNAMBIGUITY (==1) (BLOCKING) ──
    # mutation_probe --e2e は `test` フィールドを `playwright -g "<field>"` に渡し、substring 一致する
    # 全 test を実行する。field が 2+ title に一致すると複数 test が走り mutation の非 vacuity 帰属が
    # 曖昧化する (意図 test が green のままでも co-match した無関係 test の fail で「caught」と誤報告 /
    # 逆に意図 test の fail が masked され false SURVIVED)。Check 379 は ≥1 (anchor が解決する) を守る
    # が、本 Check は ==1 (anchor が唯一の意図 test を指す) へ tighten し、mutation-integrity mesh
    # (362/379/380) の ambiguous-anchor 面を閉じる。実例: `"unique slugs"` は settings same-name test と
    # resilience colliding-import test の 2 件に一致していた (本 increment で `"same name yields unique
    # slugs"` へ限定)。
    try:
        import importlib as _importlib397
        _ms397 = _importlib397.import_module("mutation_samples")
        # 両記法 (_e2e_titles・379 と共用)。テンプレートは 1 loop = 1 test 扱いが正しい: 実行時は
        # N ルートへ展開されるが本体は同一 assertion で、co-match による帰属曖昧化は起きない。
        _titles397 = []
        for _spec397 in sorted((ROOT / "e2e").glob("*.spec.js")):
            _titles397 += _e2e_titles(_spec397.read_text(encoding="utf-8"))
        _ambiguous397 = []
        for _m397 in _ms397.E2E_MUTATIONS:
            _t397 = _m397.get("test", "")
            _n397 = sum(1 for _ti397 in _titles397 if _t397 and _t397 in _ti397)
            if _n397 != 1:
                _ambiguous397.append(f"{_m397['name'][:45]} → test='{_t397}' matches {_n397} titles")
        check(
            bool(_titles397) and not _ambiguous397,
            f"Check 397: all {len(_ms397.E2E_MUTATIONS)} E2E_MUTATIONS `test` fields match EXACTLY ONE e2e test title (unambiguous -g anchor)",
            f"Check 397: E2E_MUTATIONS の `test` フィールドが一意の test title に解決しない (0 または 2+ 一致): {_ambiguous397[:5]} — "
            "`playwright -g` が複数 test を走らせ mutation の非 vacuity 帰属が曖昧化する (Check 379 は ≥1 のみ強制)。"
            "test フィールドを唯一の意図 test にだけ一致する固有 substring へ限定せよ"
            if _titles397 else
            "Check 397: e2e/*.spec.js から test タイトルを parse できない (構造変更の可能性)",
            blocking=True,
        )
    except ImportError as _e397:
        warnings.append(f"Check 397: mutation_samples import failed ({_e397}) — anchor-unambiguity skipped")

    # ── 409. mutation の登録先 (consistency / e2e) の分離 (BLOCKING) ───────────────
    # mutation は 2 系統ある: MUTATIONS (consistency 安全網用・gate = check_repository_consistency.py)
    # と E2E_MUTATIONS (behavior 安全網用・gate = 特定の Playwright test)。**`test` フィールドは
    # e2e 側の識別子**であり、consistency 側に置くと (a) その mutation は e2e probe で一度も走らず
    # behavior 安全網が未検証のまま、(b) consistency probe では対応 Check が無いので SURVIVED として
    # 恒久的に赤くなる。実測 (2026-08-09): consistency probe が 6 件 SURVIVED を報告し、追跡すると
    # behavior mutation が MUTATIONS 側へ誤登録されていた (うち 1 件は log-rotation で archive へ流れ
    # 込んでいた)。同時に旧慣習で Check の OK 文言を `test` に書いた consistency mutation も 10 件見つかり、
    # 現行の意味 (e2e title) と衝突していたため除去した。ゆえに **MUTATIONS 側は `test` キーを持たない**
    # ことを不変とする (E2E 側が持つことは Check 379/397 が別途強制)。
    try:
        import mutation_samples as _ms409
        _bad409 = [m409.get("name", "?")[:60] for m409 in _ms409.MUTATIONS if "test" in m409]
        _missing409 = [m409.get("name", "?")[:60] for m409 in _ms409.E2E_MUTATIONS if "test" not in m409]
        # 409b — 命名規約による登録先の二重防御。consistency mutation は「どの Check を突くか」を name の
        # 先頭 `Check <番号>` で宣言し、behavior mutation は宣言しない (behavior:/a11y:/resilience: 等)。
        # これにより **`test` キーを持たない behavior mutation の誤登録** (409a では検出できず、どこでも
        # 検証されない orphan になる) を静的に捕捉できる。実測 (2026-08-09): 規約適合は consistency
        # 294/295・e2e 115/115 で、唯一の例外は Check 406 を突く正当な mutation の命名漏れだった。
        _naming409 = [m409.get("name", "?")[:60] for m409 in _ms409.MUTATIONS
                      if not re.match(r"^Check \d+", m409.get("name", ""))]
        _naming409e = [m409.get("name", "?")[:60] for m409 in _ms409.E2E_MUTATIONS
                       if re.match(r"^Check \d+", m409.get("name", ""))]
        check(
            not _naming409 and not _naming409e,
            f"Check 409b: mutation の命名が登録先と一致 (consistency は 'Check <番号>' 始まり / e2e はそれ以外)",
            f"Check 409b: 命名と登録先が不一致 — consistency 側で 'Check <番号>' 始まりでない: {_naming409[:5]} / "
            f"e2e 側で 'Check <番号>' 始まり: {_naming409e[:5]}。consistency mutation は突く Check を name で宣言し、"
            "behavior mutation は宣言しない。この規約により `test` キーを持たない behavior mutation の誤登録 "
            "(どこでも検証されない orphan) を静的に捕捉する",
            blocking=True,
        )
        check(
            not _bad409 and not _missing409,
            f"Check 409: mutation の登録先が分離 (MUTATIONS {len(_ms409.MUTATIONS)} 件は test 無し / E2E {len(_ms409.E2E_MUTATIONS)} 件は test 有り)",
            f"Check 409: mutation の登録先が混線している — consistency 側に test を持つ entry: {_bad409[:5]} / "
            f"e2e 側に test を欠く entry: {_missing409[:5]}。`test` は e2e mutation の識別子であり、"
            "consistency 側に置くと e2e probe で一度も走らず behavior 安全網が未検証のまま、"
            "consistency probe では SURVIVED として恒久的に赤くなる (2026-08-09 に 6 件の実害を検出)",
            blocking=True,
        )
    except ImportError as _e409:
        warnings.append(f"Check 409: mutation_samples import 失敗 ({_e409}) — 登録先分離の検証を skip")

    # ── 399. mutation-probe の catch 帰属 (BLOCKING) ───────────────────────────────
    # consistency mode の probe は mutation 適用後に gate を走らせるが、適用によりその mutation
    # 自身の find-anchor が対象 file から消えるため Check 362 (anchor 解決) が **必ず** RED になる。
    # exit code だけで caught を判定すると全 mutation が Check 362 の副作用で自動的に caught となり、
    # 「意図した Check が本当に捕捉するか」を一切検証しない vacuous な meta-QA と化す (実証: どの
    # Check も見ない inert prose を対象にした対照 mutation で gate の error は Check 362 の 1 件のみ)。
    _probe399 = ROOT / ".github" / "scripts" / "mutation_probe.py"
    _src399 = _probe399.read_text(encoding="utf-8") if _probe399.exists() else ""
    _marker399 = re.search(r'^ANCHOR_ORPHAN_MARKER\s*=\s*"Check 362:"', _src399, re.M)
    _attrib399 = "caught_by_real_check(" in _src399
    # 旧 vacuous 判定 (`if run_gate() == 0:`) が残っていないこと。run_gate は tuple を返すため
    # 残存すると常に False = 全件 caught へ静かに戻る (退行の実体をピンポイントで禁止する)。
    _legacy399 = re.search(r"if\s+run_gate\(\)\s*==\s*0\s*:", _src399)
    check(
        bool(_src399) and bool(_marker399) and _attrib399 and not _legacy399,
        "Check 399: mutation-probe の catch 判定が Check 362 (anchor orphan) を除外して帰属する",
        "Check 399: mutation_probe.py の consistency mode が catch を Check 362 以外の error で "
        "帰属していない (ANCHOR_ORPHAN_MARKER 定数 / caught_by_real_check() のいずれかが欠落、または "
        "旧判定 `if run_gate() == 0:` が残存)。mutation 適用は必ず自身の find-anchor を消して Check 362 "
        "を RED にするため、exit code だけの判定では全 mutation が自動的に caught になり probe が "
        "「意図した Check が捕捉するか」を検証しない vacuous な meta-QA へ退行する",
    )

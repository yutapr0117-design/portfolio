"""
checks_size_budget.py — ファイルサイズ予算の統治クラスタ
(checks_maintainability.py から分離・check.py split track・category "size budget governance").

【なぜ分けたか】
分離元は Check 454 を足した時点で 985 行 = Check 365 の hard ceiling (1,000) まで残り 15 行に
なった。**まさに 454 が塞ごうとしている現象を、454 を足した増分自身が踏んだ**。圧縮で誤魔化さず
「いま触っているクラスタ」を切り出す (§7 の定型手)。

【このクラスタは何を守るか】
「行数が無制限に伸びない」ことを二層で守る:
  - **早期警告 (ADVISORY)**: Check 52 が per-file の loose な予算を超えたら warning を出す
  - **ハードゲート (BLOCKING)**: Check 365 が全非 A 追跡テキストを 1,000 行で止める
そしてこの二層が**実際に機能する前提条件**を、周辺の Check が相互に守っている:
  - 71  … 予算に書かれた path が実在する (registered ⟹ exists)
  - 361 … shipped JS leaf が予算に登録済み (exists ⟹ registered・71 の対称)
  - 408 … e2e spec が予算に登録済み (同じ対称を spec 面で)
  - 424 … §2 表の「実測行数」が実際に `wc -l` と一致する
  - 443 … 予算値が hard ceiling 未満 (でないと早期警告が構造的に出ない)
  - 454 … 危険域の file が予算を持つ (無登録は 443 の検査対象にすら入らない)
  - 363 … shipped JS logic-leaf の独立した hard ceiling
「予算がある」「値が妥当」「対象が漏れていない」「実測と一致する」の 4 面が揃って初めて
advisory → BLOCKING の二層が意図どおり働く。どれか 1 つ欠けると **OK からいきなり BLOCKING** に
飛ぶ (実際に #1067 / #1135 / 本 increment で 3 度起きた)。

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT/warnings by reference (exec 不使用), so
append semantics / BLOCKING propagation / exit code are byte-equivalent to the monolith.

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  52. File-size budget advisory: each file listed in the machine-readable BUDGET-DATA block of
      docs/architecture/file-size-budget.md whose budget is a concrete integer must have a current
      line count at or below that budget. This is the bloat-governance counterpart to the staged
      split: main.js carries a strong-advisory ceiling so its growth is actively discouraged, while
      protected AIO canon and archive/evidence files are recorded with budget "-" (no ceiling)
      because line growth there is itself valuable (digests, session records, incident history). The
      budget lives single-source in file-size-budget.md (as-decided) and this check only parses and
      compares against reality — it never hardcodes a line number, the same "documentation must match
      reality" philosophy as Check 44/45/47, applied to the line-budget domain. Deliberately
      NON-BLOCKING (ADVISORY): an over-budget file raises a warning a human reviews, never a CI
      failure, so a justified increase (a new safety comment, a new archive entry) is never blocked;
      main.js is the file whose advisory the owner treats as near-hard. A missing or unparseable
      budget file is itself a (non-blocking) advisory. (ADVISORY)
  71. file-size-budget.md BUDGET-DATA path existence: docs/architecture/file-size-budget.md
      §4 BUDGET-DATA に列挙された各エントリのパスが実在ファイルを指すことを機械強制する。
      BUDGET-DATA は Check 52 (ADVISORY 行数予算) の真値だが、ファイル rename / 削除後に
      BUDGET-DATA から行を消し忘れると Check 52 が「存在しないファイル」を黙ってスキップし、
      削除後の monitoring drift が見えなくなる。本 Check は「BUDGET-DATA に登録された path は
      全て実在する」を BLOCKING で保証する。(BLOCKING)
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
  365. Capstone: every git-tracked text file (excluding the design-constraint
       A group: style.css / index.html / main.js; AIO/C6 layer:
       llms-full.txt / llms.txt / llms_well-known.txt; npm lockfile:
       package-lock.json; bot-managed append logs: aio-monitoring-log.json /
       aio-monitoring-log-archive.json (weekly bot appends ~95 lines/entry and
       cannot be bounded without rotation — excluded as pure evidence logs);
       pure-data subtrees: js/quiz/*.js / .well-known/**; binary extensions:
       png/jpg/webp/mp3 etc.; e2e snapshot dirs) MUST be ≤1,000 lines.
       This is the top-level bloat gate complementing the per-surface guards
       (Check 363 for js/*.js, Check 52 ADVISORY, JS-LEAF-CEILING BLOCKING).
       check.py split (→920 lines), e2e spec split (→max 647 lines), and
       B-track trim (AI2AI.md→951, ChatGPT2ChatGPT.md→970) had to complete
       before this gate could first pass (achieved 2026-07-08). Implemented
       via `git ls-files` so only committed files are scanned — no untracked
       or gitignored noise. Prevents any future increment from silently
       re-bloating any doc, check module, workflow, or e2e spec beyond the
       threshold. (BLOCKING)
  408. e2e spec budget registration: every `e2e/*.spec.js` must be registered in
       docs/architecture/file-size-budget.md (§2 table + §4 BUDGET-DATA). Without an entry the only
       thing guarding a spec's size is Check 365's hard 1,000-line BLOCKING ceiling, so a file grows
       silently and then blocks a PR with no prior warning — measured on 2026-08-09, when
       apps-settings.spec.js hit the ceiling in TWO consecutive cycles (1,032 then 1,021 lines) while
       apps-task.spec.js sat 28 lines below it. Registering them makes Check 52 emit an ADVISORY
       first (a two-layer design: advisory warning → blocking ceiling), and Check 398 now prints
       advisory bodies so that warning actually reaches the operator. This is the e2e face of
       Check 361 (js leaf registration). (BLOCKING)
  424. file-size-budget.md §2 表の「実測行数」列が実測 (`wc -l`) と一致することを機械強制
       する。§2 は人間可読な要約で、機械可読な真値は §4 BUDGET-DATA (Check 52/71 がパース)
       ゆえ、§2 の数値は「一致は人間レビューで保つ」とだけ書かれ **誰も検証していなかった**。
       実測すると 62 行中 44 行が stale (最大 366 行ズレ) で、列見出しが「実測行数」と
       名乗りながら 71% が実測でない状態だった。cold-start の読者はこの表で headroom を
       判断するため、間違った数値は無いより悪い。CLAUDE.md §7 の教訓「『生じないように』は
       doc/convention でなく Check で機械強制せよ」の未適用箇所。(BLOCKING)
  443. **advisory 予算は hard ceiling より厳密に小さいこと** (BLOCKING): `file-size-budget.md`
       の BUDGET-DATA に登録された advisory 予算が、Check 365 の hard ceiling (1,000 行) 以上だと
       **その file には早期警告が構造的に一度も出ない** —— OK からいきなり BLOCKING へ飛ぶ。
       このリポジトリは「advisory は BLOCKING を踏む前に効かせる」を標準規律にしているのに、
       **その規律が効かない file が実在した**。実測 (2026-08-23): 5 file が advisory = 1,000 =
       hard ceiling に設定されており、うち `mutation_samples_archive.py` は **999 行 (BLOCKING まで
       1 行)**、`mutation_samples_e2e_archive2.py` は **971 行**で、どちらも一度も警告が出ていなかった。
       しかも §2 表の説明文は「ceiling は Check 365 に整合させ 1,000 とする」と、**欠陥そのものを
       設計として記述**していた。予算を 950 へ下げ、同じ設定が再混入しないよう機械強制する。
  454. **危険域の file は advisory 予算を持つこと** (BLOCKING): Check 443 は「予算があるなら
       hard ceiling 未満であれ」を守るが、**予算が無い file はそもそも検査対象に入らない**。
       実測 (2026-08-26): `.github/scripts/checks_*.py` は 55 module すべてが BUDGET-DATA に
       未登録で、Check 52 の advisory が一度も鳴らない状態だった。この cohort は **Check を
       1 本足すたびに行が増える**構造ゆえ最も肥大しやすく、実際 `checks_wiring.py` は 987 行
       = BLOCKING まで残り 13 行という位置に無警告で到達していた。443 と同じ失敗形
       (OK からいきなり BLOCKING) の、**予算の有無**という別の入口。
       全 tracked file に予算を要求するのは padding (大半は 1,000 に一生届かない) なので、
       hard ceiling へ現実的に近づいた file —— `EARLY_WARNING_FLOOR` (800) 行超 —— だけに
       「advisory 予算が登録されていること」を要求する。対象集合は Check 365 の除外集合を
       **共有**する (hard ceiling の対象でない file に早期警告を求めるのは無意味なため)。
       予算値そのものの妥当性は Check 443 が、実測行数との一致は Check 424 が守る。(BLOCKING)
  455. **`strong-advisory` の予算は実際に tight であること** (BLOCKING): §1 の分類表は
       `strong-advisory` を「強い抑制対象。減少方向が望ましく、増加は厳しく観測する /
       **現行行数に近い tight な上限**」と定義している。だが実測 (2026-08-26) では唯一の
       該当 file `main.js` の予算が **6,400 に対し実測 1,356 = 4.7 倍**で、リポジトリ内で
       最も緩い予算になっていた —— 分類が宣言する性質と実態が**真逆**。原因は Stage 5 の
       分割 (7,785→1,086 行・−86%) の後に予算をラチェットダウンしなかったこと。
       **main.js は Check 365 の hard ceiling 対象外**なので、この予算が唯一のサイズ信号
       であり、それが永久に鳴らない状態だった (Check 443 は「予算 < hard ceiling」を見るが、
       ceiling 対象外 file はそもそも 443 の対象外)。
       `STRONG_ADVISORY_MAX_RATIO` (1.25) 以内であることを強制する。file が縮んだら比が
       上がって RED になる = ラチェットダウンを促す挙動で、これは分類が明記する
       「減少方向が望ましい」と一致する意図的な設計。(BLOCKING)
"""
import re

# ── hard ceiling とその除外集合 (Check 365 / 443 の単一ソース) ────────────────────
# [FIX 2026-08-23] 元は Check 365 の中だけに閉じていたが、Check 443 (advisory 予算は hard
#   ceiling 未満) が **同じ集合**を必要とする。片方に file を足してもう片方を忘れると、
#   「hard ceiling の対象なのに早期警告が要らないと判定される」逆の穴が開くので単一ソースにする。
HARD_CEILING = 1000

# Check 454: 「危険域」の下限。ここを超えた file は advisory 予算を持たねばならない。
# 全 tracked file に予算を要求するのは padding (大半は 1,000 に一生届かない) なので、
# **hard ceiling へ現実的に近づいた file だけ**に早期警告の存在を要求する。
EARLY_WARNING_FLOOR = 800

# Check 455: `strong-advisory` 種別が名乗る「tight」の許容上限 (予算 / 実測)。
# §1 の分類表は strong-advisory を「現行行数に近い tight な上限」と定義しているので、
# その定義を機械が読める形にした値。1.25 = 実測の 25% 増しまでを tight と認める。
STRONG_ADVISORY_MAX_RATIO = 1.25

# design-constraint A group / AIO C6 / 自動生成 / bot 追記ログ —— hard ceiling の対象外
CEILING_EXEMPT_NAMES = frozenset([
    "style.css", "index.html", "main.js",
    "llms-full.txt", "llms.txt", "llms_well-known.txt",
    "package-lock.json",
    "aio-monitoring-log.json",
    "aio-monitoring-log-archive.json",
])
CEILING_EXEMPT_EXTS = frozenset([
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico",
    ".mp3", ".woff", ".woff2", ".ttf", ".eot", ".gz", ".zip",
])
CEILING_EXEMPT_PREFIXES = ("js/quiz/", ".well-known/", "e2e/portfolio.spec.js-snapshots/")


def run(ctx):
    """Execute this module's checks against the shared context."""
    ROOT = ctx.ROOT
    check = ctx.check
    warnings = ctx.warnings

    # ── 52. File-size budget advisory (ADVISORY / non-blocking) ──────────────────
    # Bloat-governance counterpart to the v80+ staged split. We parse the machine-readable
    # BUDGET-DATA block embedded in docs/architecture/file-size-budget.md and, for every file
    # whose budget is a concrete integer, assert its current line count is at or below that
    # budget. The budget is single-source in that doc (as-decided by the owner); this check only
    # reads and compares — it never hardcodes a line number, mirroring the "documentation must
    # match reality" philosophy of Check 44/45/47 but applied to line budgets. It is deliberately
    # NON-BLOCKING: protected AIO canon and archive/evidence files are recorded with budget "-"
    # (no ceiling) because growth there is itself valuable, and even a concrete over-budget only
    # raises a warning a human reviews — never a CI failure that would block a justified increase
    # (a new safety comment, a new archive entry). main.js carries a strong-advisory ceiling the
    # owner treats as near-hard, so its growth is the one this check most actively surfaces.
    # Line-count convention: `len(splitlines())`, which equals `wc -l` for files that end in a
    # newline (essentially all of them here) and `wc -l`+1 for files that do not.
    # [FIX 2026-08-23] 旧実装は `count("\n") + 1` で、**末尾改行のあるファイルでは常に `wc -l`
    #   より 1 大きい**値を報告していた。にもかかわらず直上のコメントは「末尾改行のあるファイルでは
    #   `wc -l` と一致する」と**逆のことを書いていた**。結果、同じファイルについて
    #   **Check 52 の warning は 924、Check 424 (§2 表の実測行数) は 923** と食い違い、
    #   実際に事故が起きた —— warning の数値を権威と誤読して §2 表を 924 へ「修正」し、
    #   Check 424 が正しく通していた値を壊して CI を赤にした (2026-08-23)。
    #   `wc -l` を権威とする Check 424 / 365 / 363 に合わせて `splitlines()` へ統一する。
    _budget_doc52 = ROOT / "docs" / "architecture" / "file-size-budget.md"
    if _budget_doc52.exists():
        _btext52 = _budget_doc52.read_text(encoding="utf-8")
        # The budget block is an HTML comment so it never renders in the Markdown, yet stays
        # diff-visible and parseable. Each data line: "<repo-relative-path> | <budget|-> | <kind>".
        _bm52 = re.search(r"<!--\s*BUDGET-DATA(.*?)-->", _btext52, re.DOTALL)
        if _bm52:
            _over52: list[str] = []
            _missing52: list[str] = []
            _checked52 = 0
            for _raw52 in _bm52.group(1).strip().split("\n"):
                _line52 = _raw52.strip()
                if not _line52 or _line52.startswith("#"):
                    continue  # allow blank lines and "# ..." comments inside the block
                _parts52 = [p.strip() for p in _line52.split("|")]
                if len(_parts52) < 3:
                    continue
                _path52, _limit52, _kind52 = _parts52[0], _parts52[1], _parts52[2]
                if _limit52 in ("-", "none", "n/a", ""):
                    continue  # protected / archive-growth-ok rows carry no ceiling
                try:
                    _limit_n52 = int(_limit52)
                except ValueError:
                    continue
                _fp52 = ROOT / _path52
                if not _fp52.exists():
                    _missing52.append(_path52)
                    continue
                _actual52 = len(_fp52.read_text(encoding="utf-8").splitlines())
                _checked52 += 1
                if _actual52 > _limit_n52:
                    _over52.append(f"{_path52} ({_actual52} lines > budget {_limit_n52}; {_kind52})")
            # 52 — advisory only (blocking=False): warns but never fails CI.
            _msg_fail52_parts = []
            if _over52:
                _msg_fail52_parts.append("over advisory line budget: " + "; ".join(_over52))
            if _missing52:
                _msg_fail52_parts.append("budgeted file(s) missing on disk: " + ", ".join(_missing52))
            check(
                not _over52 and not _missing52,
                f"Check 52: all {_checked52} budgeted files are within their advisory line budget "
                "(file-size-budget.md)",
                "Check 52 (ADVISORY): " + " | ".join(_msg_fail52_parts)
                + " — review docs/architecture/file-size-budget.md (advisory, not blocking)",
                blocking=False,
            )
        else:
            check(
                False, "",
                "Check 52 (ADVISORY): docs/architecture/file-size-budget.md has no parseable "
                "<!-- BUDGET-DATA ... --> block (advisory, not blocking)",
                blocking=False,
            )
    else:
        check(
            False, "",
            "Check 52 (ADVISORY): docs/architecture/file-size-budget.md is missing — the "
            "file-size budget is not recorded (advisory, not blocking)",
            blocking=False,
        )

    # ── 71. file-size-budget.md BUDGET-DATA path existence (BLOCKING) ─────────────
    # docs/architecture/file-size-budget.md §4 BUDGET-DATA に列挙された各エントリのパスが
    # 実在ファイルを指すことを機械強制する。BUDGET-DATA は Check 52 (ADVISORY 行数予算) の
    # 真値だが、ファイル rename / 削除後に BUDGET-DATA から行を消し忘れると Check 52 が
    # 「存在しないファイル」を黙ってスキップし、削除後の monitoring drift が見えなくなる。
    # 本 Check は「BUDGET-DATA に登録された path は全て実在する」を BLOCKING で保証する。
    _budget71 = ROOT / "docs" / "architecture" / "file-size-budget.md"
    if _budget71.exists():
        _bsrc71 = _budget71.read_text(encoding="utf-8")
        _budgetblock71 = re.search(r"<!--\s*BUDGET-DATA(.*?)-->", _bsrc71, re.DOTALL)
        _missing71 = []
        _count71 = 0
        if _budgetblock71:
            for line in _budgetblock71.group(1).strip().split("\n"):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 3:
                    _p71 = parts[0]
                    _count71 += 1
                    if not (ROOT / _p71).exists():
                        _missing71.append(_p71)
        check(
            not _missing71 and _count71 > 0,
            f"Check 71: all {_count71} BUDGET-DATA paths in file-size-budget.md exist",
            f"Check 71: BUDGET-DATA paths point at non-existent files: {_missing71}. "
            f"ファイル rename/削除後に §4 BUDGET-DATA から該当行を削除して同期せよ "
            f"(Check 52 silent-skip 防止)",
        )
    else:
        warnings.append("Check 71: file-size-budget.md not found — BUDGET-DATA existence check skipped")

    # ── 424. file-size-budget.md §2 表の実測行数が実測と一致 (BLOCKING) ────────────
    # §2 は人間可読な要約で、機械可読な真値は §4 BUDGET-DATA (Check 52/71 がパース) である。
    # そのため §2 の数値は長らく「一致は人間レビューで保つ」とだけ書かれ、誰も検証して
    # いなかった。実測したところ 62 行中 44 行が stale (最大 366 行ズレ) で、列見出しが
    # 「実測行数」と名乗りながら 71% が実測でない状態だった。表を読んで headroom を判断する
    # cold-start の読者にとって、間違った数値は無いより悪い。人間レビュー任せをやめて機械強制する。
    _budget424 = ROOT / "docs" / "architecture" / "file-size-budget.md"
    if _budget424.exists():
        _src424 = _budget424.read_text(encoding="utf-8")
        _stale424 = []
        _checked424 = 0
        for _m424 in re.finditer(r"^\| `([^`]+)` \| ([\d,]+) \| ([\d,]+) \| `", _src424, re.M):
            _p424 = ROOT / _m424.group(1)
            if not _p424.exists():
                continue  # 存在検証は Check 71 の担当
            _actual424 = len(_p424.read_text(encoding="utf-8", errors="replace").split("\n")) - 1
            _rec424 = int(_m424.group(2).replace(",", ""))
            _checked424 += 1
            if _rec424 != _actual424:
                _stale424.append(f"{_m424.group(1)}: 表={_rec424} 実測={_actual424}")
        check(
            not _stale424 and _checked424 > 0,
            f"Check 424: file-size-budget.md §2 表の実測行数 {_checked424} 件が実測と一致",
            f"Check 424: §2 表の実測行数が実測とズレている: {_stale424[:8]}"
            + (f" (他 {len(_stale424) - 8} 件)" if len(_stale424) > 8 else "")
            + "。行数を変えたファイルは §2 表の「実測行数」列も同じ commit で更新せよ "
            f"(§4 BUDGET-DATA は予算値なので変更不要)",
        )
    else:
        warnings.append("Check 424: file-size-budget.md not found — §2 line-count sync check skipped")

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

    # ── 365. Capstone: 全非 A 追跡テキストファイル ≤1,000 行 (BLOCKING) ─────────────
    # AI 無限改善自走の持続可能性を守る Capstone。「肥大化を生じないように」する最上位 gate。
    # check.py 分割 (920行) + e2e spec 分割 (max 647行) + B-track trim (AI2AI.md 951行・
    # ChatGPT2ChatGPT.md 970行) が完了した 2026-07-08 に初めて全ファイルで通過できるようになった。
    # git ls-files で committed files のみスキャン（untracked / .gitignore 対象は除外）。
    import subprocess as _sp365
    # 除外集合と上限は module level の単一ソースを使う (Check 443 と共有)
    _a_names = CEILING_EXEMPT_NAMES
    _bin_exts = CEILING_EXEMPT_EXTS
    _excl_pfx = CEILING_EXEMPT_PREFIXES
    _CEIL365 = HARD_CEILING
    try:
        _ls365 = _sp365.run(
            ["git", "ls-files"], cwd=str(ROOT), capture_output=True, text=True, check=True
        )
        _tracked365 = [ln.strip() for ln in _ls365.stdout.splitlines() if ln.strip()]
        _over365 = []
        for _rel in _tracked365:
            _p365 = ROOT / _rel
            if not _p365.is_file():
                continue
            if _p365.name in _a_names or _p365.suffix in _bin_exts:
                continue
            if any(_rel.startswith(pfx) for pfx in _excl_pfx):
                continue
            try:
                _n365 = len(_p365.read_text(encoding="utf-8", errors="replace").splitlines())
            except OSError:
                continue
            if _n365 > _CEIL365:
                _over365.append(f"{_rel} ({_n365}行)")
        check(
            not _over365,
            f"Check 365: 全非 A 追跡テキストファイル ≤{_CEIL365} 行 (capstone BLOCKING)",
            f"Check 365: {len(_over365)} ファイルが {_CEIL365} 行超。肥大化解消後に merge せよ: "
            + ", ".join(_over365[:5]),
            blocking=True,
        )
    except Exception as _e365:
        warnings.append(f"Check 365: git ls-files 実行失敗 — capstone skipped ({_e365})")

    # ── 408. e2e spec の予算登録 (BLOCKING) ────────────────────────────────────────
    # e2e/*.spec.js は Check 365 の 1,000 行 BLOCKING 上限だけが効いており、**超過するまで一切の
    # 予告が無かった**。実測 (2026-08-09): apps-settings.spec.js で 2 サイクル連続 BLOCKING を踏み
    # (1,032 行 → 1,021 行)、apps-task.spec.js は上限まで残り 28 行だった。file-size-budget.md の
    # BUDGET-DATA へ登録すれば Check 52 が advisory で先に警告する二層になる (Check 398 で advisory
    # 本文が読めるようになったため警告が実際に届く)。新しい spec が登録漏れで早期警告網の外へ
    # 出るのを防ぐ (Check 361 = js leaf 面の e2e 版)。
    _budget408 = ROOT / "docs" / "architecture" / "file-size-budget.md"
    _e2e_dir408 = ROOT / "e2e"
    if _budget408.exists() and _e2e_dir408.is_dir():
        _bsrc408 = _budget408.read_text(encoding="utf-8")
        _specs408 = sorted(f"e2e/{p408.name}" for p408 in _e2e_dir408.glob("*.spec.js"))
        _missing408 = [p408 for p408 in _specs408
                       if not re.search(r"^" + re.escape(p408) + r"\s*\|", _bsrc408, re.M)]
        check(
            bool(_specs408) and not _missing408,
            f"Check 408: 全 {len(_specs408)} 個の e2e spec が file-size-budget.md の BUDGET-DATA に登録済 (早期警告網)",
            f"Check 408: BUDGET-DATA 未登録の e2e spec: {_missing408} — 未登録だと Check 52 の advisory が効かず "
            "Check 365 の 1,000 行 BLOCKING に予告なく当たる (実測: apps-settings.spec.js で 2 サイクル連続発生)。"
            "docs/architecture/file-size-budget.md の §2 表と §4 BUDGET-DATA へ追加せよ",
            blocking=True,
        )
    else:
        check(False, "Check 408: file-size-budget.md and e2e/ present",
              "Check 408: file-size-budget.md または e2e/ が無い — e2e spec の予算登録を検証できない", blocking=True)

    # ── 443. advisory 予算は hard ceiling より厳密に小さいこと (BLOCKING) ──────────────
    # advisory の存在意義は「BLOCKING を踏む前に気付かせる」ことなので、予算が hard ceiling
    # 以上だと **その file の早期警告は構造的に一度も出ない** (OK → いきなり BLOCKING)。
    # 実測 (2026-08-23): 5 file が advisory = 1,000 = hard ceiling で、うち 2 file は
    # BLOCKING まで 1 行 / 29 行という状態のまま無警告だった。しかも budget doc の説明文が
    # 「ceiling は Check 365 に整合させ 1,000 とする」と欠陥を設計として記述していた。
    # hard ceiling は Check 365 と同じ 1,000 (`_CEIL365`) を単一ソースとして参照する。
    _budget443 = ROOT / "docs" / "architecture" / "file-size-budget.md"
    if _budget443.exists():
        _txt443 = _budget443.read_text(encoding="utf-8")
        _m443 = re.search(r"<!-- BUDGET-DATA(.*?)-->", _txt443, re.S)
        if not _m443:
            check(False, "", "Check 443: BUDGET-DATA ブロックを parse できない", blocking=True)
        else:
            _bad443 = []
            for _line443 in _m443.group(1).splitlines():
                _line443 = _line443.strip()
                if not _line443 or _line443.startswith("#"):
                    continue
                _parts443 = [_c.strip() for _c in _line443.split("|")]
                if len(_parts443) < 2 or not _parts443[1].replace(",", "").isdigit():
                    continue  # 予算が "-" の行 (protected 等) は対象外
                _rel443 = _parts443[0]
                _pp443 = ROOT / _rel443
                # hard ceiling の**対象外** file は、1,000 超の advisory を置くのが正当
                # (警告すべき BLOCKING がそもそも存在しないため)。Check 365 と同じ集合で判定する。
                if (_pp443.name in CEILING_EXEMPT_NAMES
                        or _pp443.suffix in CEILING_EXEMPT_EXTS
                        or any(_rel443.startswith(_pfx) for _pfx in CEILING_EXEMPT_PREFIXES)):
                    continue
                _b443 = int(_parts443[1].replace(",", ""))
                if _b443 >= HARD_CEILING:
                    _bad443.append(f"{_rel443}={_b443}")
            check(
                not _bad443,
                f"Check 443: hard ceiling 対象 file の advisory 予算がすべて {HARD_CEILING} 未満 — 早期警告が機能する",
                (f"Check 443: advisory 予算が hard ceiling (1000) 以上の file がある: {_bad443}。"
                 "**その file には早期警告が一度も出ない** (OK からいきなり Check 365 の BLOCKING へ飛ぶ) ので、"
                 "「advisory は BLOCKING を踏む前に効かせる」という本リポジトリの標準規律が構造的に働かない。"
                 "予算を 1000 未満 (目安 950) へ下げよ。**上げて黙らせるのではなく、下げて早く鳴らすのが advisory の役割**"),
                blocking=True,
            )

    # ── 454. 危険域 (>800 行) の file は advisory 予算を持つこと (BLOCKING) ─────────────
    # Check 443 の裏面。443 は「予算があるならその値が妥当か」を見るが、**予算が無い file は
    # 検査対象に入らない**ので、登録漏れは無警告のまま BLOCKING まで到達する。
    # 実測 (2026-08-26): `.github/scripts/checks_*.py` は 55 module 全てが未登録で、
    # checks_wiring.py が 987 行 (BLOCKING まで 13 行) に無警告で到達していた。この cohort は
    # **Check を 1 本足すたびに行が増える**ため、リポジトリ内で最も肥大しやすい面だった。
    # 対象は「hard ceiling の対象 (Check 365 と同じ除外集合) かつ EARLY_WARNING_FLOOR 超」。
    # 全 file に予算を要求すると padding になる (大半は 1,000 に一生届かない)。
    import subprocess as _sp454
    _budget454 = ROOT / "docs" / "architecture" / "file-size-budget.md"
    try:
        _txt454 = _budget454.read_text(encoding="utf-8")
        _m454 = re.search(r"<!-- BUDGET-DATA(.*?)-->", _txt454, re.S)
        _registered454 = set()
        if _m454:
            for _line454 in _m454.group(1).splitlines():
                _line454 = _line454.strip()
                if _line454 and not _line454.startswith("#") and "|" in _line454:
                    _registered454.add(_line454.split("|")[0].strip())
        _ls454 = _sp454.run(["git", "ls-files"], cwd=str(ROOT),
                            capture_output=True, text=True, check=True)
        _missing454 = []
        for _rel454 in (ln.strip() for ln in _ls454.stdout.splitlines() if ln.strip()):
            if _rel454 in _registered454:
                continue
            _p454 = ROOT / _rel454
            if not _p454.is_file():
                continue
            if (_p454.name in CEILING_EXEMPT_NAMES
                    or _p454.suffix in CEILING_EXEMPT_EXTS
                    or any(_rel454.startswith(_pfx) for _pfx in CEILING_EXEMPT_PREFIXES)):
                continue
            try:
                _n454 = len(_p454.read_text(encoding="utf-8", errors="replace").splitlines())
            except OSError:
                continue
            if _n454 > EARLY_WARNING_FLOOR:
                _missing454.append(f"{_rel454} ({_n454}行)")
        check(
            not _missing454,
            f"Check 454: hard ceiling 対象で {EARLY_WARNING_FLOOR} 行超の file は全て advisory 予算を持つ (早期警告が存在する)",
            (f"Check 454: {len(_missing454)} file が危険域 (>{EARLY_WARNING_FLOOR} 行) なのに "
             f"BUDGET-DATA に未登録 = **早期警告が存在しない**: {_missing454[:5]}。"
             "予算が無い file は Check 52 の advisory 対象にならないので、OK からいきなり "
             "Check 365 の BLOCKING (1000 行) へ飛ぶ。docs/architecture/file-size-budget.md の "
             "§2 表と §4 BUDGET-DATA の両方へ登録せよ (Check 59 が集合一致を強制する)"),
            blocking=True,
        )
    except (OSError, _sp454.CalledProcessError) as _e454:
        warnings.append(f"Check 454: 予算登録の走査に失敗 ({_e454}) — 早期警告の存在検査を skip")

    # ── 455. strong-advisory の予算は実際に tight であること (BLOCKING) ────────────────
    # §1 の分類表が strong-advisory に与えている定義は「現行行数に近い tight な上限」。
    # 実測 (2026-08-26): 唯一の該当 file main.js が 6,400 / 実測 1,356 = **4.7 倍**で、
    # リポジトリ内で最も緩い予算だった (分類の宣言と実態が真逆)。Stage 5 の −86% 分割後に
    # ラチェットダウンし忘れたまま残っていた。main.js は Check 365 の hard ceiling 対象外
    # ゆえ **この予算が唯一のサイズ信号**であり、それが永久に鳴らない状態だった。
    # Check 443 (予算 < hard ceiling) は ceiling 対象外 file を見ないので、この穴は 443 でも
    # 454 でも塞がらない —— 「予算はある / ceiling 対象でもない / だが緩すぎて意味がない」
    # という第 3 の入口。
    _budget455 = ROOT / "docs" / "architecture" / "file-size-budget.md"
    try:
        _m455 = re.search(r"<!-- BUDGET-DATA(.*?)-->",
                          _budget455.read_text(encoding="utf-8"), re.S)
        _loose455 = []
        _seen455 = 0
        if _m455:
            for _line455 in _m455.group(1).splitlines():
                _line455 = _line455.strip()
                if not _line455 or _line455.startswith("#") or "|" not in _line455:
                    continue
                _parts455 = [_c.strip() for _c in _line455.split("|")]
                if len(_parts455) < 3 or _parts455[2] != "strong-advisory":
                    continue
                if not _parts455[1].replace(",", "").isdigit():
                    continue
                _p455 = ROOT / _parts455[0]
                if not _p455.is_file():
                    continue  # path 実在は Check 71 が守る
                _seen455 += 1
                _n455 = len(_p455.read_text(encoding="utf-8", errors="replace").splitlines())
                _b455 = int(_parts455[1].replace(",", ""))
                if _n455 and _b455 > _n455 * STRONG_ADVISORY_MAX_RATIO:
                    _loose455.append(f"{_parts455[0]} 予算{_b455}/実測{_n455}={_b455 / _n455:.2f}倍")
        check(
            not _loose455,
            f"Check 455: strong-advisory {_seen455} 件の予算が実測の "
            f"{STRONG_ADVISORY_MAX_RATIO} 倍以内 (分類が名乗る tight が実態と一致)",
            (f"Check 455: strong-advisory なのに予算が緩すぎる: {_loose455}。"
             "§1 の分類表は strong-advisory を「現行行数に近い tight な上限」と定義しており、"
             "緩い予算は**その定義に反するうえ advisory が実質鳴らない**。"
             "とくに hard ceiling 対象外の file にとってはこの予算が唯一のサイズ信号なので、"
             "緩めた時点でサイズの観測手段が完全に失われる。実測に近い値へ**ラチェットダウン**せよ "
             "(上げて黙らせるのではなく、下げて早く鳴らすのが advisory の役割)"),
            blocking=True,
        )
    except OSError as _e455:
        warnings.append(f"Check 455: budget doc を読めない ({_e455}) — tightness 検査を skip")

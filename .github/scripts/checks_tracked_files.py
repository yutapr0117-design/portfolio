"""
checks_tracked_files.py — tracked-files mirror bijection + private-document guard (ctx-enrich _member_paths)
(extracted from check_repository_consistency.py — check.py split track・category "tracked-files governance").

Non-contiguous cluster of Checks 108/122 that both consume the repository member-paths list
`_member_paths` (git ls-files): docs/files mirror ↔ tracked-files FULL bijection (108), and the
private-source-document guard (122・no resume/career pdf/docx/office/archive tracked). `_member_paths`
was Check 37's inline producer; Phase 46 relocated it to the setup area and attaches it as
`_ctx._member_paths`, so consumers like these can be split out and unpack `_member_paths =
ctx._member_paths`. Check 37 (the artifact-scan) stays in the monolith because it also uses the
FORBIDDEN_GENERATED_* setup constants. No other cross-section coupling.

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT/read/extract/_member_paths by reference.

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  434. verify が「不完全な視界」で緑にならない保証。Check 108 / 122 / 37 などは
       `git ls-files` を真値にするため、**まだ git add していないファイルは走査対象にすら
       入らない**。つまりローカルで新規ファイルを作って `npm run verify` を回すと、
       そのファイルに関する invariant を **一つも検査しないまま緑**になり、CI (clean checkout
       で commit 済みの状態を見る) で初めて赤くなる。実際に踏んだ (2026-08-20 #1169:
       新規 spec の mirror doc 欠落を Check 108 が CI でだけ検出。ローカルは緑だった)。
       そこで、mirror/bijection 系 Check が統治するディレクトリ (`js/` `e2e/`
       `.github/scripts/` `docs/`) に **未追跡ファイルがあれば BLOCKING で止める**。
       「verify の結果が信用できる状態でだけ verify を通す」ための前提条件チェックであり、
       検査対象そのものではない。使い捨ての probe を置いたまま verify を回すのも同じ理由で
       止まる (probe は消してから回す運用と一致する)。(BLOCKING)

  108. docs/files mirror ↔ tracked-files full bijection: EVERY tracked repository file (per
       `git ls-files`, excluding docs/files itself) has a 1-to-1 multi-audience doc mirror at
       `docs/files/<path>.md`, and every mirror (except the README.md inventory and _template.md)
       has a live source file. Check 96 only guards the 33 Phase-1 shipped-code files; this Check
       extends the bijection to ALL tracked files, so a newly added file without a mirror, or an
       orphan mirror left after a source is deleted/renamed, is caught structurally. (BLOCKING)
  122. no private source documents tracked: personal career source documents (resume / career
       history / offer letters / labor-condition sheets) are LOCAL-ONLY input for generating the
       abstracted, privacy-safe docs/evidence/real-work-claims.md. Committing an original would
       leak sensitive PII (personal identifiers beyond the public real name, client/project names,
       salary, labor conditions). The shipped repo is Vanilla JS/MD/images/JSON only, so office /
       document / archive formats (pdf/docx/doc/xlsx/pptx/rtf/odt/ods/odp/pages/key/numbers/csv +
       zip/7z/rar/tar/gz/tgz) have no legitimate use; this Check asserts (via `git ls-files`) that
       none is tracked — defense-in-depth alongside the .gitignore blanket ignore. Images
       (png/jpg/webp) are intentionally excluded (legitimately used). (BLOCKING)
"""
import re
import json
import subprocess


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check
    read = ctx.read
    extract = ctx.extract
    _member_paths = ctx._member_paths

    # ── 108. docs/files mirror ↔ tracked-files full bijection (BLOCKING) ──────────
    # The repo documents EVERY tracked file with a 1-to-1 mirror at docs/files/<path>.md
    # (multi-audience: AI / new hire / auditor / recruiter / researcher). Check 96 only enforces
    # the 33 Phase-1 shipped-code files, leaving the other ~100 mirrors unguarded: a new file added
    # without a mirror, or an orphan mirror left after a source file is deleted/renamed, would erode
    # the "every file is documented" guarantee silently. This Check extends the bijection to the
    # FULL tracked set. Authoritative source = `git ls-files` via the already-computed `_member_paths`
    # (so untracked node_modules/__pycache__ never false-positive). README.md (the inventory, Check
    # 99) and _template.md are the only docs/files entries that are not themselves mirrors.
    _src108 = {f for f in _member_paths if not f.startswith("docs/files/")}
    _mirror108 = set()
    for _f108 in _member_paths:
        if _f108.startswith("docs/files/") and _f108.endswith(".md"):
            if _f108.rsplit("/", 1)[-1] in ("README.md", "_template.md"):
                continue
            _mirror108.add(_f108[len("docs/files/"):-len(".md")])
    _missing_mirror108 = sorted(_src108 - _mirror108)
    _orphan_mirror108 = sorted(_mirror108 - _src108)
    check(
        bool(_src108) and _src108 == _mirror108,
        f"Check 108: all {len(_src108)} tracked files have a 1-to-1 docs/files mirror (full bijection)",
        f"Check 108: docs/files mirror drift — tracked but undocumented (missing mirror): {_missing_mirror108}; "
        f"orphan mirror (doc with no source file): {_orphan_mirror108}. docs/files/<path>.md を同期せよ",
        blocking=True,
    )

    # ── 122. no private source documents tracked (BLOCKING) ───────────────────────
    # 本人の経歴書類 (履歴書・職務経歴書・内定通知書・労働条件表 等) は、抽象化済み evidence
    # (docs/evidence/real-work-claims.md) を生成するためのローカル入力に過ぎず、原本を公開リポジトリへ
    # commit すると機微情報 (氏名以外の個人特定情報・顧客名・案件名・年収・労働条件) の漏洩になる。
    # shipped repo は Vanilla JS/MD/画像/JSON のみで、office/文書/アーカイブ形式は一切正規利用が無いため、
    # これらの拡張子が tracked されていないことを BLOCKING で機械強制する (.gitignore のブランケット ignore と
    # 二重防御。`git add .` は settings で deny 済みだが、明示 add の取りこぼしや将来の再投入もここで閉じる)。
    # 対象は MS Office (pdf/docx/doc/xlsx/pptx) + 文書 (rtf/odt/ods/odp/pages/key/numbers/csv) +
    # アーカイブ (zip/7z/rar/tar/gz/tgz)。画像 (png/jpg/webp) は webp asset / playwright baseline で
    # 正規利用するため意図的に対象外 (false-positive 回避)。
    _PRIVATE_DOC_SUFFIXES = (
        ".pdf", ".docx", ".doc", ".xlsx", ".pptx",
        ".rtf", ".odt", ".ods", ".odp", ".pages", ".key", ".numbers", ".csv",
        ".zip", ".7z", ".rar", ".tar", ".gz", ".tgz",
    )
    _private_hits = sorted(p for p in _member_paths if p.lower().endswith(_PRIVATE_DOC_SUFFIXES))
    check(
        not _private_hits,
        f"Check 122: no private source documents (.pdf/.docx/...) tracked (scanned {len(_member_paths)} paths)",
        "Check 122: private source document(s) tracked in repository — 機微情報漏洩リスク。原本は "
        "ローカルのみで扱い、抽象化済み evidence のみ commit せよ。tracked 違反: "
        + ", ".join(_private_hits[:10]) + (" …" if len(_private_hits) > 10 else ""),
        blocking=True,
    )

    # ── 434. verify が「不完全な視界」で緑にならない保証 (BLOCKING) ─────────────────
    # Check 108/122/37 は `git ls-files` を真値にするため、未追跡ファイルは走査対象に入らない。
    # 新規ファイルを add せずに verify を回すと **そのファイルの invariant を一つも検査しないまま
    # 緑** になり、CI で初めて赤くなる (2026-08-20 #1169 で実際に踏んだ)。
    # mirror/bijection 系が統治するディレクトリに未追跡があれば止める。
    _governed434 = ("js/", "e2e/", ".github/scripts/", "docs/")
    # 434b: **この Check 自身の走査範囲を守る。** 範囲を空にすると
    # `str.startswith(())` は常に False を返すため、未追跡ファイルが幾つあっても
    # `_untracked434` が空になり **何も検出しないまま緑**になる。
    # 2026-08-20 の週次 mutation-probe が実際に SURVIVED で検出した (範囲を空にする
    # mutation を素通しした)。Check 124/411 の scope-drift と同型で、「gate が自分の
    # 視界を失っても気付けない」class。最低限、shipped JS と behavior gate の面は
    # 必ず含む (ここが外れると verify の視界が壊れても分からない)。
    check(
        all(p in _governed434 for p in ("js/", "e2e/")),
        "Check 434b: 未追跡ファイル走査の対象範囲が shipped JS と e2e を含む",
        (f"Check 434b: 走査範囲 {_governed434} が js/ か e2e/ を欠く — 範囲が空/不足だと "
         "startswith が常に False になり、未追跡ファイルがあっても検出しないまま緑になる "
         "(2026-08-20 の mutation-probe が範囲を空にする mutation を SURVIVED で検出)"),
        blocking=True,
    )
    try:
        _out434 = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=all"],
            cwd=ROOT, capture_output=True, text=True, timeout=30,
        )
        _untracked434 = sorted(
            ln[3:].strip() for ln in _out434.stdout.splitlines()
            if ln.startswith("?? ") and ln[3:].strip().startswith(_governed434)
        )
        check(
            not _untracked434,
            "Check 434: 統治対象ディレクトリに未追跡ファイルが無い (verify の視界が完全)",
            (f"Check 434: 未追跡ファイルがあるため verify の視界が不完全: {_untracked434[:5]} — "
             "Check 108/122/37 は `git ls-files` を真値にするので、**未追跡ファイルは検査されない**。"
             "このまま緑になっても CI (clean checkout) で赤くなる (#1169 で実際に踏んだ)。"
             "`git add` してから verify し直すか、使い捨ての probe なら削除せよ"),
            blocking=True,
        )
    except Exception as _e434:
        check(False, "Check 434: git status",
              f"Check 434: git status を実行できない ({_e434}) — verify の視界を確認できない",
              blocking=True)

"""
checks_ci_supply.py — CI / workflow-coverage & supply-chain hardening checks
(extracted from check_repository_consistency.py — check.py split track・category "CI/supply-chain").

This module owns the contiguous cluster of Checks 142-145 that guard the CI trigger/coverage
and supply-chain surface: the Playwright e2e gate covers its own toolchain (142), the
auto-digest workflow triggers on every digested manifest file (143), the digest-regen tool's
file map matches the manifest (144), and every GitHub Actions `uses:` is pinned to a full commit
SHA (145). Each Check reads its own target files directly (workflow YAML, update_aio_digests.py,
aio-manifest.json) via Path.read_text(); none depends on the monolith's global html/style/mainjs
content, so the cluster is self-contained and needs no ctx enrichment. Every local is
`_NNN`-suffixed and confined to its section.

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT by reference (exec 不使用), so append
semantics / BLOCKING propagation / exit code are byte-equivalent to the monolith.

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  142. Playwright e2e gate covers its own toolchain: playwright-regression.yml (the BLOCKING
       behavior/functionality e2e gate) is path-filtered to shipped-site files so it skips on
       unrelated commits. But the e2e TOOLCHAIN itself — @playwright/test (the runner) and
       @axe-core/playwright (a11y assertions) plus transitive deps — lives in the dependency
       manifest, and a bump there can change e2e behavior with NO shipped-site file changing.
       Without package.json/package-lock.json in the trigger, such a bump skips the behavior gate
       and ships an unverified test-toolchain change (observed: PR #318 bumped @axe-core/playwright
       and playwright-validation never ran). This Check asserts both manifest files are present in
       the workflow's pull_request paths filter, keeping "the gate that proves e2e behavior"
       wired to "the files that can change e2e behavior" (the CI-trigger version of the
       file-exists≠file-wired class, cf. Check 133/134/135). (BLOCKING)
  143. Auto-digest workflow covers every digested manifest file: .well-known/aio-manifest.json
       registers source_of_truth / supporting_evidence / observational_evidence entries each with a
       sha256 digest. auto-update-aio-digests.yml is the automation that regenerates those digests
       on a push to main, and it is path-filtered. If a digested file is absent from that paths
       filter, editing it on main won't auto-refresh its digest (observed drift: real-work-claims.md
       was added to the manifest in Session #21 but never to the workflow paths). This Check asserts
       every manifest entry that has BOTH a repo-relative path AND a sha256 is covered by the
       workflow's push paths — either as a literal entry or via a `prefix/**` glob — keeping "the
       files the manifest digests" wired to "the automation that maintains those digests" (the
       producer/consumer-drift / file-exists≠file-wired class, cf. Check 132/142). (BLOCKING)
  144. Digest-regen tool's file map matches the manifest: update_aio_digests.py is the automation
       that recomputes manifest sha256 digests, and the EXACT set of files it can refresh is the
       hardcoded MANIFEST_PATH_TO_LOCAL dict. Check 143 guarantees the WORKFLOW fires on a digested
       file's change, but once fired the tool can only refresh files present in this dict. If a
       manifest entry has a sha256 but no dict key, the workflow fires yet that file's digest is
       never recomputed — and since the tool can't fix it, the BLOCKING check_aio_digests.py gate
       becomes un-auto-fixable (a human must hand-compute the sha256). This Check asserts the dict's
       key set is a bijection with the manifest's digested-path set (every dict key is a digested
       manifest path AND every digested manifest path is a dict key), closing the consumer-side edge
       of the digest-automation chain (paths→tool-dict→manifest), cf. Check 143. (BLOCKING)
  145. GitHub Actions are pinned to a full commit SHA: every `uses: owner/repo@ref` in
       .github/workflows/*.yml must pin `ref` to a full-length 40-hex commit SHA, never a mutable
       tag (@v6) or branch (@main). A mutable tag can be silently re-pointed (or hijacked) upstream
       so a workflow runs different code with no repo change — the supply-chain analog of the silent
       weakening this repo already guards against (Check 67 permissions / 76 settings deny / 115 CSP
       anti-weakening). Third-party actions (e.g. peter-evans/create-pull-request) are the highest
       attack surface. This Check parses every uses: ref and asserts a 40-hex SHA (local `./` actions
       are exempt), preventing regression to mutable tags; the human-readable `# vN` comment stays
       and dependabot (github-actions, Check 68) keeps the pins current. (BLOCKING)
"""
import re
import json
import ast


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 142. Playwright e2e gate covers its own toolchain (BLOCKING) ────────────────
    # playwright-regression.yml は BLOCKING な behavior/functionality e2e gate だが、CI コスト
    # 節約のため shipped-site ファイルへの path filter で発火する。しかし e2e の挙動を決める
    # ツールチェーン本体 — @playwright/test (runner) と @axe-core/playwright (a11y) + transitive
    # deps — は dependency manifest (package.json / package-lock.json) にあり、その bump は
    # shipped-site ファイルを一切変えずに e2e 挙動を変えうる。trigger に manifest が無いと、dep
    # bump 時に behavior gate が skip され未検証の test-toolchain 変更が出荷される (実例: PR #318 が
    # @axe-core/playwright を bump したが playwright-validation が一度も走らなかった)。本 Check は
    # pull_request の paths filter に両 manifest が存在することを強制し、「e2e 挙動を証明する gate」を
    # 「e2e 挙動を変えうるファイル」に配線し続ける (file-exists≠file-wired class の CI-trigger 版・
    # cf. Check 133/134/135)。
    _pwf142 = ROOT / ".github" / "workflows" / "playwright-regression.yml"
    if _pwf142.exists():
        _wsrc142 = _pwf142.read_text(encoding="utf-8")
        # `paths:` ブロックの `- '...'` エントリを (インデント連続する範囲で) 抽出。
        _paths142 = []
        _in_paths142 = False
        _paths_indent142 = None
        for _line142 in _wsrc142.splitlines():
            _stripped142 = _line142.strip()
            if re.match(r"^paths:\s*$", _stripped142):
                _in_paths142 = True
                _paths_indent142 = len(_line142) - len(_line142.lstrip())
                continue
            if _in_paths142:
                if _stripped142.startswith("- "):
                    _paths142.append(_stripped142[2:].strip().strip("'\""))
                elif _stripped142 == "" or _stripped142.startswith("#"):
                    continue  # blank/comment lines stay inside the list
                else:
                    # 非リスト行 (= dedent して次キーへ) で paths ブロック終了
                    _in_paths142 = False
        _missing142 = [m for m in ("package.json", "package-lock.json") if m not in _paths142]
        check(
            not _missing142,
            "Check 142: playwright-regression.yml paths filter は e2e ツールチェーン manifest "
            "(package.json + package-lock.json) を含む (dep bump で behavior gate が再実行される)",
            f"Check 142: playwright-regression.yml の paths filter に {_missing142} が無い — "
            "e2e ツールチェーン (@playwright/test / @axe-core/playwright + transitive deps) の "
            "bump 時に BLOCKING behavior gate が skip され未検証で出荷される (file-exists≠file-wired "
            "class・cf. Check 133/134/135)。paths に両 manifest を追加せよ",
            blocking=True,
        )
    else:
        check(False, "Check 142: .github/workflows/playwright-regression.yml present",
              "Check 142: playwright-regression.yml が無い — e2e gate toolchain coverage を検証できない",
              blocking=True)

    # ── 143. Auto-digest workflow covers every digested manifest file (BLOCKING) ────
    # .well-known/aio-manifest.json は source_of_truth / supporting_evidence /
    # observational_evidence の各エントリを sha256 digest 付きで登録する。
    # auto-update-aio-digests.yml はそれらの digest を main への push 時に自動再生成する自動化で、
    # path filter で発火する。digested file がその paths に無いと、main 上でその file を編集しても
    # digest が自動更新されない (実 drift: real-work-claims.md は Session #21 で manifest に追加された
    # が workflow paths には未追加だった)。本 Check は、repo-relative path と sha256 を both 持つ全
    # manifest エントリが workflow の push paths に literal か `prefix/**` glob で被覆されることを強制し、
    # 「manifest が digest 付きで宣言する file」を「その digest を維持する自動化」に配線し続ける
    # (producer/consumer-drift / file-exists≠file-wired class・cf. Check 132/142)。
    _manifest143 = ROOT / ".well-known" / "aio-manifest.json"
    _autowf143 = ROOT / ".github" / "workflows" / "auto-update-aio-digests.yml"
    if _manifest143.exists() and _autowf143.exists():
        _mdata143 = json.loads(_manifest143.read_text(encoding="utf-8"))
        # digest 付き repo-relative path を全カテゴリから収集 (URL-only / path 無しは除外)。
        _digested143 = []
        for _cat143 in ("source_of_truth", "supporting_evidence", "observational_evidence"):
            for _e143 in _mdata143.get(_cat143, []):
                _p143 = _e143.get("path")
                if _p143 and _e143.get("sha256"):
                    _digested143.append(_p143)
        # workflow の push `paths:` ブロックを (Check 142 と同方式で) テキスト抽出。
        _wfsrc143 = _autowf143.read_text(encoding="utf-8")
        _wfpaths143 = []
        _in_paths143 = False
        for _line143 in _wfsrc143.splitlines():
            _s143 = _line143.strip()
            if re.match(r"^paths:\s*$", _s143):
                _in_paths143 = True
                continue
            if _in_paths143:
                if _s143.startswith("- "):
                    _wfpaths143.append(_s143[2:].strip().strip("'\""))
                elif _s143 == "" or _s143.startswith("#"):
                    continue
                else:
                    _in_paths143 = False

        def _covered143(path, patterns):
            for _pat143 in patterns:
                if _pat143 == path:
                    return True
                if _pat143.endswith("/**") and (
                    path == _pat143[:-3] or path.startswith(_pat143[:-2])
                ):
                    return True
            return False

        _uncovered143 = sorted({p for p in _digested143 if not _covered143(p, _wfpaths143)})
        check(
            bool(_digested143) and not _uncovered143,
            f"Check 143: auto-update-aio-digests.yml の paths は digest 付き manifest file "
            f"{len(_digested143)} 件を全被覆 (digest 維持の自動化に配線済)",
            f"Check 143: digest 付き manifest file が auto-update-aio-digests.yml の paths から漏れている: "
            f"{_uncovered143} — main 上で編集しても digest が自動再生成されない producer/consumer drift "
            f"(cf. Check 132/142)。workflow の push paths に literal か prefix/** で追加せよ"
            if _digested143 else
            "Check 143: aio-manifest.json から digest 付き path を 1 件も抽出できない (manifest 構造を確認せよ)",
            blocking=True,
        )
    else:
        check(False, "Check 143: aio-manifest.json と auto-update-aio-digests.yml present",
              "Check 143: aio-manifest.json または auto-update-aio-digests.yml が無い — "
              "digest 自動化カバレッジを検証できない", blocking=True)

    # ── 144. Digest-regen tool's file map matches the manifest (BLOCKING) ───────────
    # update_aio_digests.py は manifest sha256 を再計算する自動化で、再生成できる file 集合は
    # ハードコードの MANIFEST_PATH_TO_LOCAL dict が正本。Check 143 は WORKFLOW の発火を保証するが、
    # 発火後 tool が refresh できるのは本 dict にある file だけ。manifest entry が sha256 を持つのに
    # dict key が無いと、workflow は発火しても該当 digest は再計算されず、tool が直せないため BLOCKING
    # check_aio_digests.py gate が auto-fix 不能 (人手で sha256 計算が必要) になる。本 Check は dict の
    # key 集合が manifest の digested-path 集合と bijection (全 dict key が digested manifest path かつ
    # 全 digested manifest path が dict key) であることを強制し、digest-automation chain
    # (paths→tool-dict→manifest) の consumer 側エッジを閉じる (cf. Check 143)。
    _manifest144 = ROOT / ".well-known" / "aio-manifest.json"
    _tool144 = ROOT / ".github" / "scripts" / "update_aio_digests.py"
    if _manifest144.exists() and _tool144.exists():
        _mdata144 = json.loads(_manifest144.read_text(encoding="utf-8"))
        _manifest_digested144 = set()
        for _cat144 in ("source_of_truth", "supporting_evidence", "observational_evidence"):
            for _e144 in _mdata144.get(_cat144, []):
                _p144 = _e144.get("path")
                if _p144 and _e144.get("sha256"):
                    _manifest_digested144.add(_p144)
        # ast で MANIFEST_PATH_TO_LOCAL の dict literal key 群を抽出 (import 副作用を避ける)。
        _tool_keys144 = set()
        _parse_ok144 = False
        try:
            _tree144 = ast.parse(_tool144.read_text(encoding="utf-8"))
            for _node144 in ast.walk(_tree144):
                if isinstance(_node144, ast.AnnAssign):
                    _target144 = _node144.target
                elif isinstance(_node144, ast.Assign):
                    _target144 = _node144.targets[0] if _node144.targets else None
                else:
                    continue
                if (isinstance(_target144, ast.Name)
                        and _target144.id == "MANIFEST_PATH_TO_LOCAL"
                        and isinstance(_node144.value, ast.Dict)):
                    for _k144 in _node144.value.keys:
                        if isinstance(_k144, ast.Constant) and isinstance(_k144.value, str):
                            _tool_keys144.add(_k144.value)
                    _parse_ok144 = True
        except SyntaxError:
            _parse_ok144 = False
        _missing_in_tool144 = sorted(_manifest_digested144 - _tool_keys144)
        _orphan_in_tool144 = sorted(_tool_keys144 - _manifest_digested144)
        check(
            _parse_ok144 and bool(_manifest_digested144)
            and not _missing_in_tool144 and not _orphan_in_tool144,
            f"Check 144: update_aio_digests.py の MANIFEST_PATH_TO_LOCAL ({len(_tool_keys144)} keys) は "
            f"manifest の digested-path 集合と bijection (digest 再生成 tool が全 manifest file を被覆)",
            (f"Check 144: digest-regen tool ↔ manifest drift — manifest にあり tool dict に無い "
             f"(再生成不能 = gate auto-fix 不能): {_missing_in_tool144} / tool dict にあり manifest に無い "
             f"(orphan): {_orphan_in_tool144}。update_aio_digests.py の MANIFEST_PATH_TO_LOCAL を manifest の "
             f"digested entry と一致させよ"
             if _parse_ok144 and _manifest_digested144 else
             "Check 144: MANIFEST_PATH_TO_LOCAL を ast で抽出できない、または manifest digested path が空 "
             "(update_aio_digests.py / aio-manifest.json の構造を確認せよ)"),
            blocking=True,
        )
    else:
        check(False, "Check 144: aio-manifest.json と update_aio_digests.py present",
              "Check 144: aio-manifest.json または update_aio_digests.py が無い — "
              "digest-regen tool カバレッジを検証できない", blocking=True)

    # ── 145. GitHub Actions are pinned to a full commit SHA (BLOCKING) ──────────────
    # GitHub 公式 hardening は action を full-length commit SHA に pin することを推奨する。
    # 版数タグ (@v6) や branch (@main) は可変で、上流が tag を別 commit へ移動 (or 侵害) すると
    # repo を一切変えずに workflow が別コードを実行しうる (supply-chain risk)。本 Check は
    # .github/workflows/*.yml の全 `uses: owner/repo@ref` の ref が 40-hex commit SHA であることを
    # 強制し、mutable tag への後退を封じる (local `./` action は exempt)。可読性の `# vN` コメントは
    # 残り、dependabot (github-actions・Check 68) が pin を最新に保つ。第三者 action が最大の attack
    # surface。Check 67/76/115 と同 security-baseline の supply-chain 版。
    _wf_dir145 = ROOT / ".github" / "workflows"
    if _wf_dir145.is_dir():
        _uses_re145 = re.compile(r"^\s*uses:\s*(\S+)")
        _sha_re145 = re.compile(r"^[0-9a-f]{40}$")
        _unpinned145 = []
        for _wf145 in sorted(_wf_dir145.glob("*.yml")):
            for _i145, _line145 in enumerate(_wf145.read_text(encoding="utf-8").splitlines(), 1):
                _m145 = _uses_re145.match(_line145)
                if not _m145:
                    continue
                _ref145 = _m145.group(1)
                if _ref145.startswith("./") or _ref145.startswith("docker://"):
                    continue  # local / docker action は SHA-pin 対象外
                if "@" not in _ref145:
                    _unpinned145.append(f"{_wf145.name}:{_i145} ({_ref145} — @ref 無し)")
                    continue
                _pin145 = _ref145.rsplit("@", 1)[1]
                if not _sha_re145.match(_pin145):
                    _unpinned145.append(f"{_wf145.name}:{_i145} ({_ref145})")
        check(
            not _unpinned145,
            "Check 145: 全 GitHub Actions `uses:` が full-length commit SHA に pin されている "
            "(mutable tag / branch なし・supply-chain hardening)",
            "Check 145: SHA pin されていない action ref がある: "
            f"{_unpinned145} — 版数タグ/branch は可変で上流の tag 移動・侵害で無告知に別コードを "
            "実行しうる。`uses: owner/repo@<40-hex SHA> # vN` 形式へ pin せよ (SHA は "
            "`gh api repos/<owner>/<repo>/git/ref/tags/<tag>` で解決)",
            blocking=True,
        )
    else:
        check(False, "Check 145: .github/workflows ディレクトリ present",
              "Check 145: .github/workflows が無い — action SHA-pin を検証できない", blocking=True)

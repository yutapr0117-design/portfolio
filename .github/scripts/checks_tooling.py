"""
checks_tooling.py — repository dev-tooling & Claude Code config-file integrity checks
(extracted from check_repository_consistency.py — check.py split track・category "dev-tooling/.claude config").

This module owns the contiguous cluster of governance/tooling meta-file integrity Checks 74-80:
_lib_io.py helper API (74), incident-artifacts README inventory (75), .claude/settings.json
security baseline (76), .claude/commands frontmatter (77), .claude/agents frontmatter (78),
.mcp.json parsability (79), .claude/skills SKILL.md frontmatter (80). Each Check reads its own
target file(s) directly (no dependency on the monolith's global html/style/mainjs content), so
the cluster is self-contained and needs no ctx enrichment.

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT/warnings by reference (exec 不使用), so
append semantics / BLOCKING propagation / exit code are byte-equivalent to the monolith.

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  74. .github/scripts/_lib_io.py helper module integrity: Plan C で抽出した純 helper module
      `_lib_io.py` が `read` / `read_bytes` / `extract` / `csp_sri_hash` の 4 public 関数を
      export することを機械強制する。sibling import の path 解決が壊れると script 全体が
      ImportError で実行不能になり catastrophic に CI が落ちる。本 Check は import 成功時に
      実行され、import 失敗時はそれ自体が fail-fast する設計 — 本 Check の役割は helper module
      の API 契約 (4 関数の存在) を構造的に固定する。(BLOCKING)
  75. docs/incident-artifacts/ README inventory completeness: docs/incident-artifacts/ 配下の
      全 *.md / *.yml ファイルが README.md に列挙されていることを機械強制する。Plan D の
      「物理移動なし、README で grouping を提供」設計を機械強制化したもので、incident-artifact
      追加時に README 更新を忘れる drift を pre-commit で構造的に閉じる。README 自身は
      inventory から除外。(BLOCKING)
  76. .claude/settings.json self-drive safety-boundary baseline: 完全 AI 自走を「安全に」
      成立させている settings.json の deny 境界 (AI2AI.md STEP 3「越えない安全境界」) が silent
      に消えていないことを機械強制する。検証する deny: (a) self-permission-widening 防止 =
      `Edit/Write(.claude/settings.json)`、(b) 破壊的操作 = `git push --force`/`-f`・`rm -rf`、
      (c) 全 stage 事故防止 = `git add .`/`-A`/`--all`、(d) C6 binary 保護 = `*.webp`/`*.mp3`
      Edit/Write deny。safety net を「暗黙の約束」から「機械強制契約」へ昇格させる。とりわけ (a) が
      消えると AI が自身の権限を自己拡張でき、人間の制御境界が崩壊するため最重要。(BLOCKING)
  77. .claude/commands/ slash-command frontmatter integrity: .claude/commands/*.md の全 slash-
      command 定義が、Claude Code 仕様に従った frontmatter (`---\ndescription: <text>\n---`) を
      持つことを機械強制する。description フィールド消失で Claude Code は command を skill
      listing から拾えなくなる silent failure に陥るため、構造的に閉じる。(BLOCKING)
  78. .claude/agents/ sub-agent frontmatter integrity: .claude/agents/*.md の全 sub-agent
      定義が、Claude Code 仕様の frontmatter (`name:` + `description:`) を持ち、かつ `name:` が
      ファイル名 stem と一致することを機械強制する。description は Agent tool の subagent_type
      選択時の真値で、消失すると orchestrator が agent を呼び出せず silent unavailability になる。
      name≠stem だと docs (例 .claude/CLAUDE.md の invocation table) がファイル名で参照する agent を
      Claude が name で解決できず dangling reference が silent に生じる。(BLOCKING)
  79. .mcp.json JSON parsability: `.mcp.json` (MCP server project-scope config) が JSON として
      parse 可能かつ `mcpServers` dict を含むことを機械強制する。parse 失敗は Claude Code 起動
      時の catastrophic 障害になるため、早期検出が必要。空 `mcpServers: {}` の placeholder は
      OK。ファイル不在は ADVISORY (optional)。(BLOCKING when present)
  80. .claude/skills/*/SKILL.md frontmatter integrity: .claude/skills/<name>/SKILL.md の全 skill
      定義が、Claude Code 仕様の frontmatter (`name:` + `description:`) を持ち、かつ `name:` が
      親ディレクトリ名と一致することを機械強制する。skill description は Claude が proactive な
      skill 呼び出し判断に使う重要シグナルで、消失すると skill は登録されても呼び出されなくなる
      silent unavailability になる。name≠dirname は解決分裂を招く (Check 78 と同型の
      identifier-coherence)。(BLOCKING when present, ADVISORY when absent)
"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check
    warnings = ctx.warnings

    # ── 74. .github/scripts/_lib_io.py helper module integrity (BLOCKING) ────────
    # Plan C で抽出した純 helper module `_lib_io.py` が check_repository_consistency.py
    # から import 解決され、`read` / `read_bytes` / `extract` / `csp_sri_hash` の 4 public
    # 関数を export することを機械強制する。sibling import の path 解決が一度でも壊れる
    # (e.g. file rename / Python のディレクトリ走査仕様変更) と、check_repository_
    # consistency.py 全体が ImportError で実行不能になり CI が catastrophic に落ちる。
    # 本 Check は import に成功した時点で実行されるため、import 失敗時はそれ自体が
    # 上位 BLOCKING (script 起動失敗) として fail-fast する設計。本 Check の役割は
    # 「helper module の API 契約 (4 関数の存在) を構造的に固定」する。
    _lib74 = ROOT / ".github" / "scripts" / "_lib_io.py"
    if _lib74.exists():
        _lib_src74 = _lib74.read_text(encoding="utf-8")
        _required74 = ["read", "read_bytes", "extract", "csp_sri_hash"]
        _missing_api74 = [
            fn for fn in _required74
            if not re.search(rf"^def {fn}\b", _lib_src74, re.MULTILINE)
        ]
        check(
            not _missing_api74,
            f"Check 74: _lib_io.py exports all {len(_required74)} required helpers ({_required74})",
            f"Check 74: _lib_io.py missing required helpers: {_missing_api74} — "
            f"Plan C 抽出 helper module の API 契約違反。4 関数の def を保持せよ",
        )
    else:
        check(
            False,
            "Check 74: _lib_io.py exists",
            "Check 74: .github/scripts/_lib_io.py が存在しない — Plan C 抽出 helper module が消失",
        )

    # ── 75. docs/incident-artifacts/ README inventory completeness (BLOCKING) ────
    # docs/incident-artifacts/ 配下の全 *.md / *.yml ファイルが README.md に列挙されている
    # ことを機械強制する。Plan D の「物理移動なし、README で年次/種別 grouping を提供」
    # 設計を機械強制化したもので、incident-artifact 追加時に README 更新を忘れる drift
    # を pre-commit で構造的に閉じる。README 自身は inventory から除外。
    _artifacts75 = ROOT / "docs" / "incident-artifacts"
    _readme75 = _artifacts75 / "README.md"
    if _readme75.exists() and _artifacts75.is_dir():
        _readme_src75 = _readme75.read_text(encoding="utf-8")
        _entries75 = [
            p.name for p in _artifacts75.iterdir()
            if p.is_file() and p.name != "README.md" and not p.name.startswith(".")
        ]
        _missing75 = [n for n in _entries75 if n not in _readme_src75]
        check(
            not _missing75 and len(_entries75) > 0,
            f"Check 75: docs/incident-artifacts/README.md lists all {len(_entries75)} artifact files",
            f"Check 75: README.md not listing {len(_missing75)} artifact(s): {_missing75[:5]}{'...' if len(_missing75) > 5 else ''} — "
            f"新規 artifact 追加時は README.md にも列挙せよ (Plan D inventory governance)",
        )
    else:
        check(
            False,
            "Check 75: docs/incident-artifacts/README.md exists",
            "Check 75: docs/incident-artifacts/README.md が無い — Plan D inventory が消失",
        )

    # ── 76. .claude/settings.json security baseline (BLOCKING) ───────────────────
    # .claude/settings.json は Claude Code agent の権限境界を定義する重要設定。完全 AI 自走
    # (Operating Model: AI が implement→verify→merge→deploy を自走、人間は監査のみ) を「安全に」
    # 成立させているのは、settings.json の deny が宣言する「越えない安全境界」そのものである。
    # よってこれらの deny が silent に消えていないことを機械強制し、「設定ファイルに依存する暗黙の
    # 約束」を「機械強制契約」へ昇格させる。検証する deny (AI2AI.md STEP 3「自走しても越えない安全
    # 境界」と対応):
    #   (a) self-permission-widening 防止 = `Edit/Write(.claude/settings.json)` deny (境界 a)。
    #       これが消えると AI が自分の権限を自己拡張でき、人間の制御境界が崩壊する = 最重要。
    #   (b) 破壊的操作 deny = `git push --force`/`-f` (force-push)・`rm -rf` (境界 d)。
    #   (c) 全 stage 事故防止 = `git add .`/`-A`/`--all` deny。
    #   (d) C6 binary 保護 = `*.webp`/`*.mp3` への Edit/Write deny。
    # いずれか一つでも欠けると自走運用の安全前提が崩れるため BLOCKING。
    _settings76 = ROOT / ".claude" / "settings.json"
    if _settings76.exists():
        try:
            _sdata76 = json.loads(_settings76.read_text(encoding="utf-8"))
            _deny76 = _sdata76.get("permissions", {}).get("deny", [])
            # 各 safety boundary を「deny リストにその marker を含む要素が存在するか」で判定。
            _req76 = {
                "Edit(.claude/settings.json) [self-permission-widening 防止]": lambda: any("Edit(.claude/settings.json)" in d for d in _deny76),
                "Write(.claude/settings.json) [self-permission-widening 防止]": lambda: any("Write(.claude/settings.json)" in d for d in _deny76),
                "git push --force [force-push 防止]": lambda: any("git push --force" in d for d in _deny76),
                "git push -f [force-push 防止]": lambda: any("git push -f" in d for d in _deny76),
                "rm -rf [破壊的削除 防止]": lambda: any("rm -rf" in d for d in _deny76),
                "git add . [全 stage 事故 防止]": lambda: any("git add ." in d for d in _deny76),
                "git add -A [全 stage 事故 防止]": lambda: any("git add -A" in d for d in _deny76),
                "git add --all [全 stage 事故 防止]": lambda: any("git add --all" in d for d in _deny76),
                "*.webp Edit/Write [C6 binary 保護]": lambda: any("*.webp" in d for d in _deny76),
                "*.mp3 Edit/Write [C6 binary 保護]": lambda: any("*.mp3" in d for d in _deny76),
            }
            _missing76 = [name for name, fn in _req76.items() if not fn()]
            check(
                not _missing76,
                f"Check 76: .claude/settings.json declares all {len(_req76)} self-drive safety-boundary denies "
                "(settings self-edit / force-push / rm -rf / git add . / webp+mp3)",
                f"Check 76: .claude/settings.json safety baseline incomplete — missing deny markers: {_missing76}. "
                "AI2AI.md STEP 3「越えない安全境界」を settings.json の deny で固定せよ (完全自走の安全前提)",
            )
        except json.JSONDecodeError as _e76:
            check(False, "Check 76: .claude/settings.json parses as JSON", f"Check 76: settings.json JSON parse error: {_e76}")
    else:
        check(False, "Check 76: .claude/settings.json exists", "Check 76: .claude/settings.json が消失")

    # ── 77. .claude/commands/ slash-command frontmatter integrity (BLOCKING) ─────
    # .claude/commands/*.md の全 slash-command 定義が、Claude Code 仕様に従った frontmatter
    # (`---\ndescription: <text>\n---`) を持つことを機械強制する。description フィールドが
    # 消失すると Claude Code は command を skill listing から拾えなくなり、UI で見えない
    # silent failure に陥る。
    _cmds77_dir = ROOT / ".claude" / "commands"
    if _cmds77_dir.is_dir():
        _cmds77 = sorted(_cmds77_dir.glob("*.md"))
        _bad77 = []
        for _cmd in _cmds77:
            _csrc = _cmd.read_text(encoding="utf-8")
            _fm77 = re.match(r"^---\s*\n([\s\S]*?)\n---\s*\n", _csrc)
            if not _fm77 or not re.search(r"^description:\s*\S", _fm77.group(1), re.MULTILINE):
                _bad77.append(_cmd.name)
        check(
            not _bad77 and len(_cmds77) > 0,
            f"Check 77: all {len(_cmds77)} .claude/commands/*.md have a valid frontmatter with description",
            f"Check 77: slash-command(s) missing valid frontmatter/description: {_bad77} — "
            f"Claude Code は description を skill listing で必須要求する",
        )
    else:
        check(False, "Check 77: .claude/commands/ exists", "Check 77: .claude/commands/ ディレクトリが消失")

    # ── 78. .claude/agents/ sub-agent frontmatter integrity (BLOCKING) ───────────
    # .claude/agents/*.md の全 sub-agent 定義が、Claude Code 仕様に従った frontmatter
    # (`name:` + `description:`) を持ち、かつ `name:` がファイル名 stem と一致することを機械強制
    # する。sub-agent の description は Agent tool の subagent_type 選択時に表示される真値で、
    # 消失すると orchestrator は agent を呼び出せず silent unavailability になる。さらに Claude Code
    # は agent を `name:` で解決する一方、人間や docs (例: .claude/CLAUDE.md の sub-agent invocation
    # table) はファイル名で参照するため、name ≠ stem だと「docs が指す agent が解決できない」
    # dangling reference が silent に生じる。両者の一致を固定して footgun を構造的に閉じる。
    _agents78_dir = ROOT / ".claude" / "agents"
    if _agents78_dir.is_dir():
        _agents78 = sorted(_agents78_dir.glob("*.md"))
        _bad78 = []
        for _ag in _agents78:
            _asrc = _ag.read_text(encoding="utf-8")
            _fm78 = re.match(r"^---\s*\n([\s\S]*?)\n---\s*\n", _asrc)
            if not _fm78:
                _bad78.append(f"{_ag.name}: missing frontmatter")
                continue
            _fm_body78 = _fm78.group(1)
            _name78 = re.search(r"^name:\s*(\S+)", _fm_body78, re.MULTILINE)
            if not _name78:
                _bad78.append(f"{_ag.name}: missing name:")
            elif _name78.group(1) != _ag.stem:
                _bad78.append(f"{_ag.name}: name '{_name78.group(1)}' != filename stem '{_ag.stem}'")
            if not re.search(r"^description:\s*\S", _fm_body78, re.MULTILINE):
                _bad78.append(f"{_ag.name}: missing description:")
        check(
            not _bad78 and len(_agents78) > 0,
            f"Check 78: all {len(_agents78)} .claude/agents/*.md have valid frontmatter (name==stem + description)",
            f"Check 78: sub-agent(s) with invalid frontmatter: {_bad78} — "
            f"Claude Code は name + description を agent 解決で必須要求し、name はファイル名 stem と一致させる",
        )
    else:
        check(False, "Check 78: .claude/agents/ exists", "Check 78: .claude/agents/ ディレクトリが消失")

    # ── 79. .mcp.json JSON parsability (BLOCKING) ────────────────────────────────
    # `.mcp.json` (MCP server project-scope config) が JSON として parse 可能であることを
    # 機械強制する。空 `mcpServers: {}` の placeholder でも parse 成功すれば OK。parse 失敗
    # は Claude Code 起動時に MCP server provisioning が全て失敗する catastrophic 障害で、
    # 早期検出が必要。
    _mcp79 = ROOT / ".mcp.json"
    if _mcp79.exists():
        try:
            _mdata79 = json.loads(_mcp79.read_text(encoding="utf-8"))
            _has_servers79 = "mcpServers" in _mdata79 and isinstance(_mdata79["mcpServers"], dict)
            check(
                _has_servers79,
                f"Check 79: .mcp.json parses as JSON and has mcpServers dict ({len(_mdata79['mcpServers'])} servers)",
                "Check 79: .mcp.json missing mcpServers dict — 空 {} でもよいので明示宣言せよ",
            )
        except json.JSONDecodeError as _e79:
            check(False, "Check 79: .mcp.json parses as JSON", f"Check 79: .mcp.json JSON parse error: {_e79}")
    else:
        warnings.append("Check 79 (ADVISORY): .mcp.json not present — optional, but recommended as a placeholder for future MCP integrations")

    # ── 80. .claude/skills/*/SKILL.md frontmatter integrity (BLOCKING) ───────────
    # .claude/skills/<name>/SKILL.md の全 skill 定義が、Claude Code 仕様に従った frontmatter
    # (`name:` + `description:`) を持ち、かつ `name:` が親ディレクトリ名と一致することを機械強制
    # する。skill description は Claude が proactive な skill 呼び出し判断に使う重要シグナルで、
    # 消失すると skill は登録されても呼び出されなくなる silent unavailability になる。Claude Code は
    # skill をディレクトリ名で配置しつつ `name:` で解決するため、name ≠ dirname だと解決が分裂する
    # (Check 78 の agent name==stem と同型の identifier-coherence 不変条件)。
    _skills80_dir = ROOT / ".claude" / "skills"
    if _skills80_dir.is_dir():
        _skills80 = sorted(_skills80_dir.glob("*/SKILL.md"))
        _bad80 = []
        for _sk in _skills80:
            _ssrc = _sk.read_text(encoding="utf-8")
            _fm80 = re.match(r"^---\s*\n([\s\S]*?)\n---\s*\n", _ssrc)
            if not _fm80:
                _bad80.append(f"{_sk.parent.name}/SKILL.md: missing frontmatter")
                continue
            _fm_body80 = _fm80.group(1)
            _name80 = re.search(r"^name:\s*(\S+)", _fm_body80, re.MULTILINE)
            if not _name80:
                _bad80.append(f"{_sk.parent.name}/SKILL.md: missing name:")
            elif _name80.group(1) != _sk.parent.name:
                _bad80.append(f"{_sk.parent.name}/SKILL.md: name '{_name80.group(1)}' != dir '{_sk.parent.name}'")
            if not re.search(r"^description:\s*\S", _fm_body80, re.MULTILINE):
                _bad80.append(f"{_sk.parent.name}/SKILL.md: missing description:")
        if _skills80:
            check(
                not _bad80,
                f"Check 80: all {len(_skills80)} .claude/skills/*/SKILL.md have valid frontmatter (name==dir + description)",
                f"Check 80: skill(s) with invalid frontmatter: {_bad80} — Claude Code は name + description を skill 解決で必須要求し、name は親ディレクトリ名と一致させる",
            )
        else:
            warnings.append("Check 80 (ADVISORY): .claude/skills/ exists but no SKILL.md found")
    else:
        warnings.append("Check 80 (ADVISORY): .claude/skills/ not present — optional, 将来 skill 追加時にディレクトリ作成")

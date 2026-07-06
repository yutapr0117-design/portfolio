"""
checks_safety_guards.py — shipped-JS/AIO safety guards — operating-model coherence / anonymity / dead-const / ESLint safety-net / digest re-bake guard (123-127)
(extracted from check_repository_consistency.py — check.py split track).

run(ctx) receives shared check()/ROOT/read/extract by reference (exec 不使用) so exit code / BLOCKING
propagation are byte-equivalent. 各 Check は対象 file を自前 read。annotation+def-aware free-var 確認済。

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  123. operating-model description coherence (site ↔ AIO): Session #21 corrected the
       "conversational Claude" 実態↔記述 drift and recorded the current operating model
       (construction phase = conversational → now Claude Code autonomous self-driving with
       decisive human control as needed) on BOTH the public site (js/components.js ai-knowhow)
       and the AIO layer (llms-full.txt Dynamic AI Team Model). 123a asserts js/components.js
       keeps the markers (現在の運用モデル + Claude Code + 自走); 123b asserts llms-full.txt keeps
       (Current Operating Model + Claude Code + self-driving). This is the public-surface version
       of the operating-model presence enforcement (canon itself is enforced by 102a-f). (BLOCKING)
  124. site visible-text anonymity guard: the site UI is deliberately anonymized to "yuta" for
       general-public privacy, while the real name (横井雄太) is exposed only in the AIO/entity
       layer (sr-only / JSON-LD / meta / alt / data-entity attributes / llms-full.txt). This Check
       asserts that in the visible page renderers (js/components.js, js/pages.js, js/apps.js) the
       real name appears ONLY on lines carrying an attribute marker (alt:/data-entity/data-ai-entity/
       aria-), never as a bare visible h() text node (124a). 124b enforces js/identity.js's documented
       contract (UI → DISPLAY_NAME only): the visible renderers must NOT reference the real-name entity
       constants (AUTHORITATIVE_NAME/JAPANESE_NAME) either, closing the identifier-based leak path
       (literal grep alone would miss a variable-rendered name). Together they structurally prevent the
       real-name-leak class (an AI added the literal name to visible text in Session #21; corrected).
       AIO layers (meta-management etc.) legitimately use AUTHORITATIVE_NAME and are out of scope. (BLOCKING)
  125. no dead CONSTANTS key: every key in js/constants.js (top-level + nested `[A-Z_]+:` lines) must
       be referenced at least once from the other shipped JS. Systematizes the dead-constant cleanup of
       Session #21 (POMODORO_LOCK_TTL / SAVE_INTERVAL were never-activated and removed); prevents the
       never-activated-constant class from re-accumulating. ALL-CAPS snake keys are distinctive so the
       reference grep is robust (a comment mention also counts — conservative under-flagging). (BLOCKING)
  126. ESLint bug-catcher safety-net presence: this config intentionally does NOT inherit
       eslint:recommended (non-destructive migration), so a silently-dropped pure bug-catcher lets
       real bugs slip past CI (#186: missing no-dupe-keys let a quiz dup-class bug ship). Beyond
       Check 50d (which guards no-dupe-keys alone), this Check asserts a representative safety-net set
       of the recommended pure bug-catchers added in PR #187/#234 (no-import-assign, no-unsafe-finally,
       no-invalid-regexp, no-const-assign, valid-typeof, use-isnan, no-fallthrough, no-cond-assign,
       getter-return, …) remains declared in eslint.config.mjs — locking the safety net against
       silent regression (the #186 class). (BLOCKING)
  127. AIO digest tool binary re-bake guard: update_aio_digests.py MUST gate its WebP/MP3 date
       re-baking behind _binary_edited() (a `git diff --quiet HEAD -- <path>` check) so binary
       internal dates are re-synced ONLY when the binary file itself was genuinely edited — never
       merely because an unrelated text digest (the weekly monitoring log) changed. The earlier
       logic re-baked on every digest change, producing a new hash the monitoring workflow recorded
       into the manifest but never committed the rewritten binary for → manifest sha256 desynced
       from the committed binary every weekly run, reddening the BLOCKING digest gate on the next
       PR. This Check locks the guard in place (presence of _binary_edited + its use gating the
       re-bake) so the desync class cannot silently return. (BLOCKING)
"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check
    read = ctx.read
    extract = ctx.extract

    # ── 123. operating-model description coherence (site ↔ AIO) (BLOCKING) ─────────
    # Session #21 で「対話型 Claude」記述の実態↔記述 drift を是正し、現在の運用モデル
    # (構築期=対話型 → 現在=Claude Code 自律自走 + 人間は必要時に決定的に制御) をサイト
    # (js/components.js ai-knowhow) と AIO 層 (llms-full.txt Dynamic AI Team Model) の双方へ
    # 超正確に記述した。この修正が将来 silent に旧記述へ巻き戻る (= flywheel を劣化させる
    # onboarding 税 + entity 記述の不正確化) のを防ぐため、両面が現運用モデルの marker を
    # 保持することを BLOCKING で機械強制する。canon (AI2AI.md STEP 3 Operating Model) は
    # Check 102a-f が別途強制しており、本 Check はその「公開 surface 版」(102b の site/AIO 面)。
    # NOTE (肥大化解消 2026-07-04): 運用モデル記述は ai-knowhow ページ内容にあり、そのページは
    # js/components.js から js/ai-knowhow-page.js へ分離された。marker の実在場所が移動しただけで
    # 「サイトに現運用モデル記述あり」invariant は不変ゆえ、両ファイルの union を scan する。
    _comp123_files = [ROOT / "js" / "components.js", ROOT / "js" / "ai-knowhow-page.js"]
    _comp123_t = "".join(
        _f.read_text(encoding="utf-8") for _f in _comp123_files if _f.exists()
    )
    _site_ok123 = ("現在の運用モデル" in _comp123_t) and ("Claude Code" in _comp123_t) and ("自走" in _comp123_t)
    check(
        _site_ok123,
        "Check 123a: site (js/components.js ∪ ai-knowhow-page.js) が現運用モデル (現在の運用モデル + Claude Code + 自走) を保持 (site↔canon coherence)",
        "Check 123a: site 層 (components.js / ai-knowhow-page.js) から現運用モデルの記述が失われた — 「対話型 Claude」だけの旧記述へ "
        "drift すると実態↔記述乖離 + entity 不正確化。'現在の運用モデル'/'Claude Code'/'自走' の marker を維持せよ "
        "(Session #21 で是正した運用モデル記述。canon は Check 102 が別途強制)",
        blocking=True,
    )
    _llms123 = ROOT / "llms-full.txt"
    _llms123_t = _llms123.read_text(encoding="utf-8") if _llms123.exists() else ""
    _aio_ok123 = ("Current Operating Model" in _llms123_t) and ("Claude Code" in _llms123_t) and ("self-driving" in _llms123_t)
    check(
        _aio_ok123,
        "Check 123b: llms-full.txt が Current Operating Model (Claude Code self-driving) を保持 (AIO↔canon coherence)",
        "Check 123b: llms-full.txt から現運用モデル記述が失われた — AIO authority が旧編成のみへ drift する。"
        "'Current Operating Model'/'Claude Code'/'self-driving' の marker を維持せよ (C6 semantic・編集は要承認)",
        blocking=True,
    )

    # ── 124. site visible-text anonymity guard (BLOCKING) ─────────────────────────
    # サイト UI は一般向けにプライバシー設計上「yuta」へ匿名化し、実名「横井雄太」は AIO/entity 層
    # (sr-only / JSON-LD / meta / alt / data-entity 属性・llms-full.txt) のみで露出する二層構造を取る
    # (リポジトリ=エンジニア/AI 向けで実名可・サイト視覚面=一般人向けで匿名)。Session #21 で AI が運用モデル
    # section の視覚本文に実名を漏らした (即是正) ため、視覚 page renderer (components/pages/apps) において
    # 実名が「属性 context (alt/data-entity/aria-/data-ai-entity)」以外の bare な h() テキスト行に出ないことを
    # BLOCKING で機械強制し、視覚 UI への実名漏れ class を構造的に封じる。AIO 属性内の実名は entity 帰属の
    # ため意図的に許可する。
    _VIS_RENDERERS124 = ["js/components.js", "js/pages.js", "js/apps.js"]
    _NAME124 = "横井雄太"
    _ATTR_MARKERS124 = ("alt:", "data-entity", "data-ai-entity", "aria-")
    _leak124 = []
    _idleak124 = []
    # UI → DISPLAY_NAME only / AIO → AUTHORITATIVE_NAME etc. (js/identity.js の明文契約)。
    # 視覚 renderer が実名系の entity 定数を参照すると識別子経由で実名が視覚露出し得るため禁止。
    _NAME_IDENTS124 = ("AUTHORITATIVE_NAME", "JAPANESE_NAME")
    for _rel124 in _VIS_RENDERERS124:
        _f124 = ROOT / _rel124
        if not _f124.exists():
            continue
        for _i124, _line124 in enumerate(_f124.read_text(encoding="utf-8").splitlines(), 1):
            if _NAME124 in _line124 and not any(_mk in _line124 for _mk in _ATTR_MARKERS124):
                _leak124.append(f"{_rel124}:{_i124}")
            if any(_id in _line124 for _id in _NAME_IDENTS124):
                _idleak124.append(f"{_rel124}:{_i124}")
    check(
        not _leak124,
        f"Check 124a: 視覚 site renderer に実名の bare テキスト漏れ無し (anonymity guard・scanned {len(_VIS_RENDERERS124)} files)",
        "Check 124a: 視覚 site テキストに実名「横井雄太」が漏れている — サイト UI は匿名 (yuta) が design。"
        "実名は alt/data-entity/aria- 等の AIO 属性 context でのみ許可。違反: " + ", ".join(_leak124[:10]),
        blocking=True,
    )
    check(
        not _idleak124,
        "Check 124b: 視覚 site renderer が実名系 entity 定数 (AUTHORITATIVE_NAME/JAPANESE_NAME) を参照しない (UI→DISPLAY_NAME only 契約)",
        "Check 124b: 視覚 renderer が AUTHORITATIVE_NAME/JAPANESE_NAME を参照している — 識別子経由で実名が視覚露出し得る。"
        "js/identity.js の契約どおり UI は DISPLAY_NAME のみ参照せよ (AIO 層=meta-management 等は AUTHORITATIVE_NAME 可)。違反: "
        + ", ".join(_idleak124[:10]),
        blocking=True,
    )

    # ── 125. no dead CONSTANTS key (BLOCKING) ─────────────────────────────────────
    # Session #21 の pomodoro bug-hunt で、consumer ゼロの never-activated 定数 (POMODORO_LOCK_TTL /
    # SAVE_INTERVAL) を発見・除去した。この dead-constant class の再発を機械封じするため、js/constants.js
    # の各キー (top-level + LIMITS 等 nested を含む `[A-Z_]+:` 行) が、他の shipped JS から少なくとも 1 回
    # 参照されることを BLOCKING で機械強制する。ALL-CAPS snake のキー名は識別性が高く誤マッチしにくい
    # (コメント言及も "not dead" として保守的に許容＝over-flag より under-flag を選ぶ)。dead は除去すること。
    _const125 = ROOT / "js" / "constants.js"
    if _const125.exists():
        _keys125 = list(dict.fromkeys(re.findall(r'^\s+([A-Z][A-Z0-9_]*)\s*:', _const125.read_text(encoding="utf-8"), re.M)))
        _corpus125_parts = []
        for _p125 in [ROOT / "main.js", ROOT / "sw.js", ROOT / "theme-init.js"] + sorted((ROOT / "js").rglob("*.js")):
            if _p125.resolve() == _const125.resolve() or not _p125.exists():
                continue
            _corpus125_parts.append(_p125.read_text(encoding="utf-8"))
        _blob125 = "\n".join(_corpus125_parts)
        _dead125 = [k for k in _keys125 if not re.search(r'\b' + re.escape(k) + r'\b', _blob125)]
        check(
            not _dead125,
            f"Check 125: js/constants.js の全 {len(_keys125)} キーが他 shipped JS から参照される (dead-constant guard)",
            "Check 125: 未使用の CONSTANTS キー (never-activated dead 定数) を検出 — 他 shipped JS から参照が無い。"
            "除去せよ (Session #21 の POMODORO_LOCK_TTL/SAVE_INTERVAL と同 class)。違反: " + ", ".join(_dead125[:10]),
            blocking=True,
        )
    else:
        check(False, "Check 125: js/constants.js present", "Check 125: js/constants.js が見つからない", blocking=True)

    # ── 126. ESLint bug-catcher safety-net presence (BLOCKING) ────────────────────
    # 本 config は eslint:recommended を敢えて継承せず明示列挙する方針 (非破壊性維持) のため、純粋
    # bug-catcher が silent に欠落/除去されると実バグが CI を素通りする (#186: no-dupe-keys 欠落で
    # quiz 重複 class バグが流出した実例)。Check 50d が no-dupe-keys 単体を守るのに加え、本 Check は
    # PR #187 + #234 で追補した recommended pure bug-catcher の代表 safety-net 集合が eslint.config.mjs
    # に残存することを BLOCKING で機械強制し、「安全網そのものの silent な後退」を #186 class として封じる。
    _eslint126 = ROOT / "eslint.config.mjs"
    if _eslint126.exists():
        _cfg126 = _eslint126.read_text(encoding="utf-8")
        _REQUIRED_BUGCATCHERS126 = [
            "no-dupe-keys", "no-import-assign", "no-unsafe-finally", "no-invalid-regexp",
            "no-const-assign", "valid-typeof", "use-isnan", "no-fallthrough", "no-cond-assign",
            "getter-return", "no-func-assign", "no-obj-calls", "no-dupe-args", "no-self-assign",
        ]
        _missing126 = [r for r in _REQUIRED_BUGCATCHERS126
                       if re.search(r"['\"]" + re.escape(r) + r"['\"]\s*:", _cfg126) is None]
        check(
            not _missing126,
            f"Check 126: eslint.config.mjs が recommended bug-catcher safety-net {len(_REQUIRED_BUGCATCHERS126)} 件を保持",
            "Check 126: eslint.config.mjs から pure bug-catcher が silent に欠落 — 安全網の後退 (#186 class: "
            "欠落ルールで実バグが CI を素通る)。次のルールを 'error' で復元せよ: " + ", ".join(_missing126),
            blocking=True,
        )
    else:
        check(False, "Check 126: eslint.config.mjs present",
              "Check 126: eslint.config.mjs が見つからない — bug-catcher safety-net を検証できない", blocking=True)

    # ── 127. AIO digest tool binary re-bake guard (BLOCKING) ──────────────────────
    # update_aio_digests.py は WebP/MP3 の内部日付メタ (XMP/ID3) 再書き込みを、binary ファイル自体が
    # 実際に編集された時のみ行わねばならない。旧実装は「source_of_truth に binary entry が存在するか」
    # だけを見て毎回再書き込みを発火させ、無関係なテキスト digest (週次 aio-monitoring ログ) 更新の
    # たびに binary hash を変え、その新 hash を manifest に記録する一方 aio-monitoring.yml は書き換えた
    # binary を git add しないため、commit 境界で manifest 記録 sha と実バイナリ sha が毎週 desync し、
    # 次 PR の BLOCKING digest gate (check_aio_digests.py) が赤化していた。本 Check は再発防止として、
    # (a) _binary_edited helper の存在、(b) その helper が `git diff --quiet HEAD` で実編集を判定すること、
    # (c) date 再書き込みが _binary_edited() でガードされていること、を presence で機械強制する。
    _digtool127 = ROOT / ".github" / "scripts" / "update_aio_digests.py"
    if _digtool127.exists():
        _src127 = _digtool127.read_text(encoding="utf-8")
        _has_helper127 = re.search(r"def\s+_binary_edited\s*\(", _src127) is not None
        _has_gitdiff127 = "git" in _src127 and "diff" in _src127 and "--quiet" in _src127 and "HEAD" in _src127
        _has_gate127 = re.search(r"if\s+_binary_edited\s*\(", _src127) is not None
        _missing127 = []
        if not _has_helper127:
            _missing127.append("_binary_edited() helper 定義")
        if not _has_gitdiff127:
            _missing127.append("`git diff --quiet HEAD` による実編集判定")
        if not _has_gate127:
            _missing127.append("date 再書き込みを `if _binary_edited(...)` でガード")
        check(
            not _missing127,
            "Check 127: update_aio_digests.py が binary 日付再書き込みを _binary_edited() (git HEAD diff) でガード",
            "Check 127: update_aio_digests.py の binary re-bake guard が後退 — manifest↔binary 毎週 desync の "
            "回帰リスク (f2335ce で根治した class)。次を復元せよ: " + ", ".join(_missing127),
            blocking=True,
        )
    else:
        check(False, "Check 127: update_aio_digests.py present",
              "Check 127: update_aio_digests.py が見つからない — digest tool の binary guard を検証できない", blocking=True)

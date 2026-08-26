"""
checks_store_contracts.py — 「書いた値が読み戻されるか」「上限が一致するか」の契約検査
(checks_behavioral.py から分離・check.py split track・category "store contracts").

【なぜ分けたか】
分離元は 924 行で advisory (950) まで残り 26 行だった。**当たってから動くのでは遅い**ので、
警告が鳴る前にテーマで割った (本リポジトリは advisory を素通りして BLOCKING に激突する事故を
過去に 3 回起こしている)。

【このクラスタは何を守るか】
producer (書く側) と consumer (読み戻す側) の**非対称**を封じる。この非対称は視覚に出ず、
利用者からは「**保存したはずのものが次に開くと無い**」としか見えないため、実バグとして
繰り返し表面化してきた:
  - 373 … defaultAppsData の全 top-level key を normalizeAppsData が読み戻すこと
          (quizSearch が drop され検索語が reload ごとに消えていた・#684)
  - 404 … default profile の全 field を validateAndNormalize が保持すること
          (github/linkedin/location が strip されていた・#139)
  - 405 … top-level field 全般の保持 (theme / projectPrefs の復元漏れ・#1036/#1037)
  - 374 … importJSON が adopt する前に正規化を通すこと (#295/#561 の ingestion 不変条件)
  - 410 … UI 入力上限 (maxlength) と保存上限 (slice) が同じ定数から導かれること
          (Markdown ノートが silent に切り詰められていた・#924)

いずれも「片側だけ直しても再発する」ので、**producer と consumer の両方を縛る**形にしてある。

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT by reference (exec 不使用), so append
semantics / BLOCKING propagation / exit code are byte-equivalent to the monolith.

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  373. Store default-appsData field ⟹ normalizeAppsData preserve round-trip: js/store.js
       normalizeAppsData(data) is the choke point every ingestion path (load / import / cross-tab /
       snapshot-restore / settings 正規化) runs through, and it rebuilds appsData from
       deepClone(defaultAppsData) then re-applies each user field from `data.<field>`. If a field
       exists in defaultAppsData (the persisted shape) but normalizeAppsData never reads it back,
       that field is SILENTLY reset to its default on every reload even though callers persist it —
       exactly the confirmed quizSearch bug: QuizPage wrote the search term via
       State.updateSilently(s => s.appsData.quizSearch = val) (which schedules a localStorage save)
       and read it back on init to restore, but normalizeAppsData preserved tasks/todos/pomodoro/ai/
       notes and dropped quizSearch, so the "永続化された検索語を反映" restore silently failed each
       reload (a half-wired persist of the #294/#568 producer/consumer drift class). This Check
       brace-parses defaultAppsData's top-level keys and asserts every one is referenced as
       `data.<key>` inside the normalizeAppsData body (line comments stripped to avoid a comment-only
       vacuous pass), making "a field is persisted ⟹ normalize reads it back" an enforced invariant
       so no future appsData field can be added to the store default yet silently lost on reload.
       (BLOCKING)
  374. settings-io.js importJSON normalize-before-adopt ingestion guard (2026-08-20 に
       js/settings-page.js から抽出・守る invariant は不変): importJSON ingests
       external JSON. If it commits the raw parsed data via State.update(...), the notify → render()
       cycle paints un-normalized data (e.g. malformed projects with a null/non-object entry that
       SettingsPage dereferences via p.name/p.id and crashes on). restoreSnapshot already follows the
       established "normalize external input before adopting it" invariant (#295/#561) by committing
       State.set(Store.validateAndNormalize(...)); importJSON must too, rather than relying on the
       incidental render-abort ordering (the second normalize render aborting the first raw render
       before it reaches SettingsPage) for data-safety. This Check brace-parses the importJSON
       function body and asserts it does NOT call State.update( and DOES route through
       validateAndNormalize, structurally preventing re-introduction of raw ingestion that reaches
       render (the ingestion counterpart of Check 130's oninput no-State.update guard). (BLOCKING)
  404. Store default-profile field ⟹ validateAndNormalize preserve round-trip: the profile-face
       twin of Check 373 (appsData face). Every top-level key of `defaultProfile` in js/store.js
       must be read back as `data.profile.<key>` inside the `store.profile = { … }` normalisation
       block. validateAndNormalize is the choke point every ingestion path goes through (load /
       import / cross-tab / snapshot-restore / settings normalise); a field that lives in the
       persisted shape but is not read back silently resets to its default on every reload.
       THIS ALREADY HAPPENED: #139 stripped github / linkedin / location so importing them did
       nothing — and the behavior e2e added then only guards those three fields, leaving any
       NEWLY added profile field unprotected. Line comments are stripped so a prose mention
       cannot vacuously satisfy the Check. (BLOCKING)
  405. Store top-level field ⟹ validateAndNormalize preserve round-trip: the top-level face of
       Checks 373 (appsData) and 404 (profile). Every top-level key of the persisted shape
       returned by `createDefaultStore()` must be read back as `data.<key>` inside
       validateAndNormalize. A key that is not read back silently resets to its default on every
       reload — a class that has already produced THREE real bugs here (quizSearch #684, profile
       github/linkedin/location #139, projectPrefs.hiddenIds #294 family). Carve-outs are the
       metadata regenerated by design: `schemaVersion` (stamps the current schema), `type` (fixed
       tag) and `lastModified` (save timestamp). With all three faces enforced, "a field added to
       the persisted shape is always read back" becomes an invariant at every level. Line comments
       are stripped so a prose mention cannot vacuously satisfy it. (BLOCKING)
  410. UI 入力上限 ⟹ 保存上限の一致 (input/textarea maxlength coherence): a UI-layer shipped JS file
       (one that builds `h('input'` / `h('textarea'` elements) that persists user text via
       `.slice(0, CONSTANTS.LIMITS.<KEY>)` MUST also declare `maxlength: CONSTANTS.LIMITS.<KEY>` for the
       same KEY in the same file. Without it the field accepts more characters than are ever saved, so
       the overflow is dropped silently at persist time. The Markdown notes editor was the severe case:
       the textarea and its live preview kept rendering everything the user typed past NOTES_TEXT
       (20,000) while `State.updateSilently` stored only the truncated prefix — the loss became visible
       only on reload (the silent producer/consumer drift class of #684 quizSearch / #294, here between
       the UI bound and the persistence bound rather than between two data layers). task/todo/ai were the
       same asymmetry but visibly truncated on submit. Deriving both bounds from the one LIMITS constant
       makes "what can be typed" == "what is saved" structural. store.js is excluded automatically since
       it builds no input elements (it is the normalization layer, not a UI layer). (BLOCKING)
"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 373. Store default-appsData field ⟹ normalizeAppsData preserve round-trip (BLOCKING) ──
    # store.js normalizeAppsData(data) は全 ingestion 経路 (load/import/cross-tab/snapshot-restore/
    # settings 正規化) が通るチョークポイントで、appsData を deepClone(defaultAppsData) から再構築し
    # 各ユーザーフィールドを `data.<field>` から再適用する。あるフィールドが defaultAppsData (永続化
    # される shape) にあるのに normalizeAppsData が読み戻さないと、呼び出し側が永続化していても reload
    # 毎に default へ silent リセットされる — quizSearch の実バグそのもの (QuizPage が updateSilently で
    # 書き込み init で読み戻すのに normalize が tasks/todos/pomodoro/ai/notes だけ preserve し quizSearch
    # を drop していた・#294/#568 と同 producer/consumer drift class)。defaultAppsData の top-level key を
    # brace-parse し、各 key が normalizeAppsData 本体で `data.<key>` として参照されることを強制する
    # (行コメントは除去して「コメントに書いただけ」の vacuous pass を防ぐ)。これで「フィールドが永続化
    # される ⟹ normalize が読み戻す」を invariant 化し、将来 store default に足したフィールドが reload で
    # silent に失われる class を封じる。
    _store373 = ROOT / "js" / "store.js"
    if _store373.exists():
        _src373 = _store373.read_text(encoding="utf-8")

        def _balanced_obj373(text, marker):
            # marker 以降の最初の '{' から brace-balance して中身 (exclusive) を返す。文字列/テンプレートは skip。
            _idx = text.find(marker)
            if _idx == -1:
                return None
            _b = text.find("{", _idx)
            if _b == -1:
                return None
            _depth = 0
            _instr = None
            _k = _b
            while _k < len(text):
                _c = text[_k]
                if _instr:
                    if _c == "\\":
                        _k += 2
                        continue
                    if _c == _instr:
                        _instr = None
                elif _c in "\"'`":
                    _instr = _c
                elif _c == "{":
                    _depth += 1
                elif _c == "}":
                    _depth -= 1
                    if _depth == 0:
                        return text[_b + 1:_k]
                _k += 1
            return None

        def _top_keys373(body):
            # body 内 depth==0 の `key:` を抽出 (ネスト obj/array 内の key は無視)。
            _keys = []
            _depth = 0
            _instr = None
            _at_key = True
            _k = 0
            while _k < len(body):
                _c = body[_k]
                if _instr:
                    if _c == "\\":
                        _k += 2
                        continue
                    if _c == _instr:
                        _instr = None
                    _k += 1
                    continue
                if _c in "\"'`":
                    _instr = _c
                    _k += 1
                    continue
                if _c in "{[(":
                    _depth += 1
                    _k += 1
                    continue
                if _c in "}])":
                    _depth -= 1
                    _k += 1
                    continue
                if _depth == 0 and _c == ",":
                    _at_key = True
                    _k += 1
                    continue
                if _depth == 0 and _at_key and not _c.isspace():
                    _m373 = re.match(r"([A-Za-z_$][\w$]*)\s*:", body[_k:])
                    if _m373:
                        _keys.append(_m373.group(1))
                        _at_key = False
                        _k += _m373.end()
                        continue
                    _at_key = False
                _k += 1
            return _keys

        _default_body373 = _balanced_obj373(_src373, "const defaultAppsData")
        _keys373 = _top_keys373(_default_body373) if _default_body373 else []
        # normalizeAppsData 本体を `function normalizeAppsData` 〜 `return result;` の text region で切り出す
        # (`return result;` は normalizeAppsData 固有。validateAndNormalize は `return store;`)。行コメントは
        # 除去 (この region に `//` を含む文字列 URL は無いため素朴除去で安全)。
        _ns373 = _src373.find("function normalizeAppsData")
        _ne373 = _src373.find("return result;", _ns373) if _ns373 != -1 else -1
        _norm_body373 = re.sub(r"//[^\n]*", "", _src373[_ns373:_ne373]) if (_ns373 != -1 and _ne373 != -1) else None
        _unpreserved373 = [
            _key for _key in _keys373
            if _norm_body373 is None or not re.search(r"\bdata\." + re.escape(_key) + r"\b", _norm_body373)
        ]
        check(
            bool(_keys373) and _norm_body373 is not None and not _unpreserved373,
            f"Check 373: normalizeAppsData が defaultAppsData の全 {len(_keys373)} フィールド ({', '.join(_keys373)}) を preserve (persist round-trip)",
            f"Check 373: defaultAppsData のフィールドが normalizeAppsData で preserve されていない: {sorted(_unpreserved373)} — "
            "store.js normalizeAppsData に `data.<field>` の正規化/保存を追加せよ。write は QuizPage 等が "
            "State.updateSilently で永続化するのに reload の normalize が strip する producer/consumer drift で、"
            "quizSearch が毎 reload で捨てられていた実バグ (#294/#568 と同 class) を封じる"
            if (_keys373 and _norm_body373 is not None) else
            "Check 373: store.js の defaultAppsData / normalizeAppsData を parse できない (構造変更の可能性)",
            blocking=True,
        )
    else:
        check(False, "Check 373: js/store.js present",
              "Check 373: js/store.js が無い — appsData persist round-trip coherence を検証できない", blocking=True)

    # ── 404. Store default-profile field ⟹ validateAndNormalize preserve round-trip (BLOCKING) ──
    # Check 373 (appsData 面) の profile 面。validateAndNormalize は全 ingestion 経路 (load / import /
    # cross-tab / snapshot-restore / settings 正規化) が通るチョークポイントで、profile を
    # `store.profile = { ...store.profile, <field>: … }` の形で再構築する。defaultProfile (永続化
    # される shape) にあるフィールドを読み戻さないと、ユーザーが設定/import しても reload 毎に default へ
    # silent に戻る。**これは既に一度起きた実バグ**: #139 で github / linkedin / location が strip され、
    # import しても消えていた (behavior e2e は当時の 3 フィールドだけを守っており、**新しく足す
    # フィールド**は無防備なまま)。defaultProfile の top-level key を brace-parse し、各 key が
    # validateAndNormalize の profile ブロックで `data.profile.<key>` として参照されることを強制する。
    if _store373.exists():
        _profile_body404 = _balanced_obj373(_src373, "const defaultProfile")
        _keys404 = _top_keys373(_profile_body404) if _profile_body404 else []
        # profile 正規化ブロック = `store.profile = {` 〜 対応する閉じ '}' (行コメントは除去)。
        _ps404 = _src373.find("store.profile = {")
        _pblock404 = None
        if _ps404 != -1:
            _inner404 = _balanced_obj373(_src373[_ps404:], "store.profile =")
            if _inner404 is not None:
                _pblock404 = re.sub(r"//[^\n]*", "", _inner404)
        _unpreserved404 = [
            _k404 for _k404 in _keys404
            if _pblock404 is None or not re.search(r"\bdata\.profile\." + re.escape(_k404) + r"\b", _pblock404)
        ]
        check(
            bool(_keys404) and _pblock404 is not None and not _unpreserved404,
            f"Check 404: validateAndNormalize が defaultProfile の全 {len(_keys404)} フィールド ({', '.join(_keys404)}) を preserve (profile persist round-trip)",
            f"Check 404: defaultProfile のフィールドが validateAndNormalize で preserve されていない: {sorted(_unpreserved404)} — "
            "store.js の `store.profile = { ... }` に `data.profile.<field>` の読み戻しを追加せよ。"
            "設定/import しても reload の normalize が strip して default へ silent に戻る data-fidelity バグになる "
            "(#139 で github/linkedin/location が実際にこれで消えていた)"
            if (_keys404 and _pblock404 is not None) else
            "Check 404: store.js の defaultProfile / store.profile 正規化ブロックを parse できない (構造変更の可能性)",
            blocking=True,
        )
    else:
        check(False, "Check 404: js/store.js present",
              "Check 404: js/store.js が無い — profile persist round-trip coherence を検証できない", blocking=True)

    # ── 405. Store top-level field ⟹ validateAndNormalize preserve round-trip (BLOCKING) ──
    # Check 373 (appsData 面) / 404 (profile 面) の **top-level 面**。createDefaultStore() が返す
    # 永続化 shape の各 top-level key は、validateAndNormalize 本体で `data.<key>` として読み戻され
    # なければならない。読み戻さない key はユーザーが設定/import しても reload 毎に default へ silent に
    # 戻る (この class は既に 3 度実バグ化している: quizSearch=#684 / profile github・linkedin・
    # location=#139 / projectPrefs.hiddenIds=#294 系)。carve-out は **設計上その場で再生成される
    # メタデータ**のみ: schemaVersion (現行 schema を書く) / type (固定タグ) / lastModified (保存時刻)。
    # 3 面 (top-level / profile / appsData) が揃うことで「永続化 shape に足したフィールドは必ず
    # 読み戻される」が全階層で invariant になる。
    if _store373.exists():
        # createDefaultStore の **返り値オブジェクト** (`return { … }`) を取る。関数本体の '{' から
        # balance すると key が depth 1 に埋もれて 0 件になるため、`return` を marker にする。
        _cs405 = _src373.find("function createDefaultStore")
        _default_store405 = _balanced_obj373(_src373[_cs405:], "return ") if _cs405 != -1 else None
        _keys405 = _top_keys373(_default_store405) if _default_store405 else []
        _META405 = {"schemaVersion", "type", "lastModified"}
        _vs405 = _src373.find("function validateAndNormalize")
        _ve405 = _src373.find("return store;", _vs405) if _vs405 != -1 else -1
        _vbody405 = re.sub(r"//[^\n]*", "", _src373[_vs405:_ve405]) if (_vs405 != -1 and _ve405 != -1) else None
        _unread405 = [
            _k405 for _k405 in _keys405
            if _k405 not in _META405
            and (_vbody405 is None or not re.search(r"\bdata\." + re.escape(_k405) + r"\b", _vbody405))
        ]
        check(
            bool(_keys405) and _vbody405 is not None and not _unread405,
            f"Check 405: validateAndNormalize が createDefaultStore の全 top-level フィールド"
            f" ({', '.join(_k for _k in _keys405 if _k not in _META405)}) を読み戻す (store persist round-trip)",
            f"Check 405: 永続化 shape の top-level フィールドが validateAndNormalize で読み戻されていない: "
            f"{sorted(_unread405)} — store.js validateAndNormalize に `data.<field>` の正規化/採用を追加せよ。"
            "読み戻さないと設定/import しても reload 毎に default へ silent に戻る (quizSearch #684 / "
            "profile #139 / projectPrefs #294 と同 class)。再生成されるメタデータ "
            "(schemaVersion / type / lastModified) のみ carve-out 対象"
            if (_keys405 and _vbody405 is not None) else
            "Check 405: store.js の createDefaultStore / validateAndNormalize を parse できない (構造変更の可能性)",
            blocking=True,
        )
    else:
        check(False, "Check 405: js/store.js present",
              "Check 405: js/store.js が無い — store top-level persist round-trip を検証できない", blocking=True)

    # ── 374. settings-io.js importJSON normalize-before-adopt ingestion guard (BLOCKING) ──
    # importJSON は外部 JSON を取り込む ingestion 経路。生の parsed を State.update で adopt すると
    # notify→render() が正規化前の生データ (malformed projects 等) を描画しうる (strict モードの
    # `merged.projects = parsed.projects` 生代入が malformed entry を SettingsPage の p.name/p.id
    # dereference へ通し crash させうる)。restoreSnapshot は既に「外部 ingestion は adopt する前に
    # validateAndNormalize を通せ」(#295/#561) に従い State.set(Store.validateAndNormalize(...)) で
    # commit する。importJSON も incidental な render-abort ordering (State.set の 2 度目 render が
    # 1 度目の生 render を SettingsPage 到達前に abort する) に data-safety を依存させず、同じ
    # normalize-before-commit へ整合させる。本 Check は importJSON 関数本体を brace-balance で抽出し、
    # State.update( を含まず validateAndNormalize を通すことを強制する (raw ingestion 描画の再混入を
    # 構造封じ・Check 130 の oninput no-State.update と同型の ingestion 版)。
    # 2026-08-20: importJSON は js/settings-io.js へ抽出された (bloat-reduction)。
    # 守る invariant は不変なので走査先だけ追従する (Check 362 が anchor 側の追従を強制)。
    _sp374 = ROOT / "js" / "settings-io.js"
    if _sp374.exists():
        _src374 = _sp374.read_text(encoding="utf-8")
        _m374 = re.search(r"function\s+importJSON\s*\(", _src374)
        _ok374 = False
        _has_update374 = True
        _has_norm374 = False
        if _m374:
            _i374 = _src374.find("{", _m374.start())
            _depth374 = 0
            _body374 = ""
            for _k374 in range(_i374, len(_src374)):
                _c374 = _src374[_k374]
                if _c374 == "{":
                    _depth374 += 1
                elif _c374 == "}":
                    _depth374 -= 1
                    if _depth374 == 0:
                        _body374 = _src374[_i374:_k374 + 1]
                        break
            _has_update374 = "State.update(" in _body374
            _has_norm374 = "validateAndNormalize" in _body374
            _ok374 = (not _has_update374) and _has_norm374
        check(
            _m374 is not None and _ok374,
            "Check 374: settings-io.js importJSON は生を State.update で adopt せず validateAndNormalize してから State.set (normalize-before-commit ingestion)",
            ("Check 374: settings-io.js importJSON の ingestion が normalize-before-commit でない — "
             + ("State.update( を呼んでおり生データが render に届きうる" if _has_update374 else "validateAndNormalize を通していない")
             + "。マージ結果を Store.validateAndNormalize してから単一 State.set( で commit せよ "
             "(restoreSnapshot と同じ #295/#561 ingestion invariant・Check 130 の ingestion 版)")
            if _m374 else
            "Check 374: settings-io.js に importJSON 関数が見つからない (構造変更の可能性)",
            blocking=True,
        )
    else:
        check(False, "Check 374: js/settings-io.js present",
              "Check 374: js/settings-io.js が無い — importJSON ingestion guard を検証できない", blocking=True)

    # ── 410. UI 入力上限 ⟹ 保存上限の一致 (maxlength coherence) (BLOCKING) ─────────
    # 保存側が LIMITS.<KEY> で slice するのに UI 側に maxlength が無いと、「入力できた文字数」と
    # 「保存される文字数」がずれ、超過分が黙って捨てられる (notes editor は画面にもプレビューにも
    # 表示され続けたまま保存だけされず、リロードで初めて消失に気付く silent data-loss だった)。
    # 対象は UI レイヤー = input/textarea を組み立てる shipped JS のみ (store.js は normalize 層で
    # 入力要素を持たないため自動的に対象外)。
    _ui410 = sorted((ROOT / "js").glob("*.js"))
    _viol410, _pairs410 = [], 0
    for _f410 in _ui410:
        _src410 = _f410.read_text(encoding="utf-8")
        if "h('input'" not in _src410 and "h('textarea'" not in _src410:
            continue
        _keys410 = set(re.findall(r"\.slice\(0,\s*CONSTANTS\.LIMITS\.([A-Z_]+)\)", _src410))
        for _k410 in sorted(_keys410):
            _pairs410 += 1
            if not re.search(r"maxlength:\s*CONSTANTS\.LIMITS\." + _k410 + r"\b", _src410):
                _viol410.append(f"{_f410.name}: LIMITS.{_k410}")
    check(
        _pairs410 > 0 and not _viol410,
        f"Check 410: UI 入力 {_pairs410} 件の maxlength が保存側 LIMITS と同一定数で一致",
        (f"Check 410: UI 上限と保存上限が drift — {_viol410}。"
         "保存側が LIMITS.<KEY> で slice する入力には同じ定数で maxlength を付けよ "
         "(無いと超過分が silent に捨てられ、リロードで初めて消失が判明する)")
        if _pairs410 else
        "Check 410: UI レイヤーの LIMITS slice を 1 件も検出できない — maxlength coherence が無効化された",
        blocking=True,
    )

